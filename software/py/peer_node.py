"""Owner-local ledger integration of bounded peer data; never remote source.

Loaded only after all three installed peer-module pins are checked by node.py.
Pending-request recovery is deliberately not implemented in this cut.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re

import peer_service as transport
import peer_wire as wire
from storage import Refusal, decode, digest, encode, read, require

MIB = 1024 * 1024


def exact(left, right):
    """JSON type-sensitive correspondence: bool is not an integer."""
    return encode(left) == encode(right)


def keys(value, names):
    require(type(value) is dict and set(value) == set(names), "INVALID_FIELDS")


def pin(path, bound):
    path = wire.safe_path(path)
    raw = wire.read_local(path, bound)
    return {"path": str(path), "bytes": len(raw), "sha256": digest(raw)}


def replica_custody(store, config, client, handle):
    """Bounded ledger-only authority, shared with checker-free serving.

    Never open package files or contact a peer here: a committed frozen view
    remains serveable after either custody/analysis copy or source disappears.
    """
    acquisition = store.record(handle, "acquisition", client)
    require(type(acquisition) is dict and "received_package" in acquisition,
            "REPLICA_CUSTODY_UNAVAILABLE")
    keys(acquisition, {"remote", "peer", "endpoint", "catalog_sha256", "bundle_sha256",
        "descriptor_id", "sequence", "snapshot", "package", "received_package", "request",
        "mathematicalAcceptance"})
    require(acquisition["mathematicalAcceptance"] is False, "REPLICA_ACQUISITION_BINDING")
    selection = store.record(acquisition["remote"], "remote", client)
    keys(selection, {"peer", "endpoint", "foundation", "catalog_sha256", "entry"})
    wire.typed_id(selection["foundation"], (1, 2))
    advertised = wire.validate_entry(selection["entry"])
    require(type(selection["peer"]) is str and selection["peer"] in config["peers"]
            and exact(config["peers"][selection["peer"]], selection["endpoint"])
            and type(selection["catalog_sha256"]) is str
            and wire.HEX.fullmatch(selection["catalog_sha256"]), "REPLICA_REMOTE_BINDING")
    require(all(exact(acquisition[name], selection[name])
                for name in ("peer", "endpoint", "catalog_sha256"))
            and exact(acquisition["descriptor_id"], advertised["descriptor_id"])
            and acquisition["bundle_sha256"] == advertised["bundle_sha256"],
            "REPLICA_REMOTE_BINDING")
    request_key = acquisition["request"]
    require(type(request_key) is str and wire.HEX.fullmatch(request_key), "REPLICA_REQUEST_KEY")
    received = acquisition["received_package"]
    keys(received, {"path", "manifest_sha256"})
    # Lexical canonical path binding only. Existence/reparse checks belong to
    # NEW view preparation, never to serving an already committed frozen view.
    expected = store.root / "work" / request_key / "incoming"
    require(type(received["path"]) is str and received["path"] == str(expected)
            and received["manifest_sha256"] == advertised["manifest_sha256"],
            "REPLICA_RECEIVED_PIN")
    cut = store.cut(acquisition["snapshot"])
    sequence = acquisition["sequence"]
    require(cut["provider"] == "P1" and type(cut["cut"]) is int
            and type(sequence) is int and 1 <= sequence <= cut["cut"] <= 8192,
            "REPLICA_SNAPSHOT_MEMBERSHIP")
    offer = store.entry("P1", sequence)
    keys(offer, {"package", "descriptor_id", "formal_metadata", "symbols"})
    require(exact(offer["package"], acquisition["package"])
            and exact(offer["descriptor_id"], advertised["descriptor_id"])
            and exact(offer["formal_metadata"], advertised["formal_metadata"]),
            "REPLICA_OFFER_BINDING")
    rows = store.rows("replica_origin",
        "SELECT client,request_id,raw,phase,response FROM requests WHERE key=?", (request_key,))
    require(rows, "REPLICA_REQUEST_BINDING")
    row = rows[0]
    require(row["client"] == client and type(row["request_id"]) is str
            and re.fullmatch(r"[A-Za-z0-9_-]{1,64}", row["request_id"])
            and digest(encode([client, row["request_id"]])) == request_key
            and type(row["raw"]) is bytes and 0 < len(row["raw"]) <= 131072
            and row["phase"] == "terminal" and type(row["response"]) is bytes
            and 0 < len(row["response"]) <= MIB, "REPLICA_REQUEST_BINDING")
    original = decode(row["raw"])
    require(exact(original, {"client": client, "request_id": row["request_id"],
            "op": "peer_acquire", "args": {"remote": acquisition["remote"]}}),
            "REPLICA_REQUEST_BINDING")
    reply = decode(row["response"])
    require(type(reply) is dict and type(reply.get("existing")) is bool
            and type(reply.get("candidate")) is str, "REPLICA_TERMINAL_BINDING")
    candidate = store.record(reply["candidate"], "candidate", client)
    require(exact(candidate, {"snapshot": acquisition["snapshot"], "sequence": sequence,
            "descriptor_id": advertised["descriptor_id"]}), "REPLICA_CANDIDATE_BINDING")
    expected_reply = {"status": "OK", "untrusted": True, "candidate_only": True,
        "mathematicalAcceptance": False, "native_stages": 0, "candidate": reply["candidate"],
        "snapshot": acquisition["snapshot"], "descriptor_id": advertised["descriptor_id"],
        "existing": reply["existing"], "acquisition": handle}
    require(exact(reply, expected_reply), "REPLICA_TERMINAL_BINDING")
    return acquisition, selection, offer


class PeerOperations:
    def __init__(self, dispatcher):
        self.d = dispatcher
        self.s = dispatcher.store
        self.config = dispatcher.config
        installed = Path(__file__).resolve().parent
        require(Path(wire.__file__).resolve() == installed / "peer_wire.py"
                and Path(transport.__file__).resolve() == installed / "peer_service.py", "PEER_MODULE_PATH")

    def foundation(self, client):
        handle = self.s.head(client)
        context = self.s.record(handle, "context", client)
        foundation = context["description"]["foundation"]
        wire.typed_id(foundation, (1, 2))
        return foundation

    def endpoint(self, alias):
        require(type(alias) is str and alias in self.config["peers"], "UNKNOWN_PEER")
        return self.config["peers"][alias]

    def observe(self):
        checker = self.d.math
        if checker is not None:
            self.d.event["checker_metrics"] = dict(checker.metrics)
            require(checker.metrics["stage_allocations"] == 0 and checker.metrics["pipeline_children"] == 0,
                    "NATIVE_EXECUTION_FORBIDDEN")
        require(self.d.event["stages_allocated"] == 0, "NATIVE_EXECUTION_FORBIDDEN")

    def prepare(self, req):
        try:
            operation = req["op"]
            if operation == "peer_find":
                return self.find(req)
            if operation == "peer_acquire":
                return self.acquire(req)
            if operation == "expose":
                return self.expose(req)
            if operation == "replica_expose":
                return self.replica_expose(req)
            raise Refusal("UNKNOWN_OPERATION")
        except wire.WireError as error:
            raise Refusal(error.code) from None
        except OSError as error:
            raise Refusal("PEER_LOCAL_IO_FAILURE", type(error).__name__ + ": " + str(error)[:512]) from None
        finally:
            self.observe()

    def find(self, req):
        keys(req["args"], {"peer"})
        alias = req["args"]["peer"]
        endpoint = self.endpoint(alias)
        foundation = self.foundation(req["client"])
        found = transport.fetch_catalog(endpoint["port"], foundation)
        self.d.event["peer_catalog_sha256"] = found["sha256"]
        return {"peer": alias, "endpoint": endpoint, "foundation": foundation,
                "catalog_sha256": found["sha256"], "catalog": found["catalog"]}

    def acquire(self, req):
        keys(req["args"], {"remote"})
        selection = self.s.record(req["args"]["remote"], "remote", req["client"])
        keys(selection, {"peer", "endpoint", "foundation", "catalog_sha256", "entry"})
        endpoint = self.endpoint(selection["peer"])
        require(exact(endpoint, selection["endpoint"]), "REMOTE_ENDPOINT_BINDING")
        foundation = self.foundation(req["client"])
        require(exact(foundation, selection["foundation"]), "FOUNDATION_MISMATCH")
        wire.validate_entry(selection["entry"])
        require(type(selection["catalog_sha256"]) is str and wire.HEX.fullmatch(selection["catalog_sha256"]),
                "REMOTE_CATALOG_BINDING")
        # This owns exclusive request-root creation before transfer makes a child.
        checker = self.d.checking()
        incoming = checker.domains.require_write(checker.work_dir / "incoming")
        received = transport.acquire(endpoint["port"], selection["entry"], foundation, incoming)
        require(received["mathematicalAcceptance"] is False and received["native_stages"] == 0
                and Path(received["package"]["path"]).resolve() == incoming
                and received["bundle_sha256"] == selection["entry"]["bundle_sha256"], "TRANSPORT_RESULT_BINDING")
        fresh = self.d.check("offer", received["package"])
        advertised = selection["entry"]
        require(exact(fresh["descriptor_id"], advertised["descriptor_id"])
                and exact(fresh["formal_metadata"], advertised["formal_metadata"])
                and exact(fresh["formal_metadata"]["replay"], advertised["root"])
                and exact(received["root"], advertised["root"]), "ADVERTISED_METADATA_MISMATCH")
        selected = self.reuse(fresh)
        self.seal_package(selected["package"])
        self.d.event["peer_bundle_sha256"] = received["bundle_sha256"]
        return {"offer": selected, "selection": selection, "remote": req["args"]["remote"],
                "received_package": dict(received["package"])}

    def revalidate(self, offer):
        """Read/check existing package and derive metadata without copying it."""
        keys(offer, {"package", "descriptor_id", "formal_metadata", "symbols"})
        checker = self.d.checking()
        checker.checkpoint()
        try:
            store, root = checker.package(offer["package"])
            value, formal = checker.metadata(store, root)
        except ValueError as error:
            raise Refusal("SELECTED_BYTES_REFUSED", type(error).__name__ + ": " + str(error)[:512]) from None
        require(exact(checker.S.C.to_projection(value["descriptor_id"]), offer["descriptor_id"])
                and exact(formal, offer["formal_metadata"])
                and exact([key.hex() for key in value["row"].symbol_keys], offer["symbols"]), "STORED_OFFER_MISMATCH")
        checker.checkpoint()
        return store, root

    def reuse(self, offer):
        """Exact canonical package reuse only; not proof selection/equivalence."""
        require(len(encode(offer)) <= 32768, "ENTRY_LIMIT")
        existing = self.s.descriptor("P1", offer["descriptor_id"])
        if existing is None:
            require(self.s.current("P1")["cut"] < self.config["limits"]["entries"], "ENTRY_QUOTA")
            return offer
        _sequence, prior = existing
        for field in ("descriptor_id", "formal_metadata", "symbols"):
            require(exact(prior[field], offer[field]), "DESCRIPTOR_VARIANT_UNSUPPORTED")
        checker = self.d.checking()
        left, left_root = self.revalidate(prior)
        right, right_root = self.revalidate(offer)
        require(prior["package"]["manifest_sha256"].lower() == offer["package"]["manifest_sha256"].lower()
                and checker.S.same(left_root, right_root)
                and left.closure(left_root) == right.closure(right_root)
                and checker.S.same(left.inventories, right.inventories), "DESCRIPTOR_VARIANT_UNSUPPORTED")
        # Both packages have been checked against their full typed CIDs and
        # normalized manifest commitments; equality assumes SHA-256 security.
        self.d.event["peer_exact_offer_reused"] = True
        return prior

    def _flush_file(self, path, expected_bytes, expected_sha256):
        path = wire.safe_path(path)
        require(path.stat().st_size == expected_bytes, "LOCAL_PACKAGE_CHANGED")
        hasher, total = hashlib.sha256(), 0
        # Write-capable handle permits FlushFileBuffers/_commit on Windows;
        # no mathematical bytes are modified.
        with path.open("r+b") as stream:
            while True:
                chunk = stream.read(65536)
                if not chunk:
                    break
                total += len(chunk)
                require(total <= expected_bytes, "LOCAL_PACKAGE_CHANGED")
                hasher.update(chunk)
                self.d.math.checkpoint()
            require(total == expected_bytes and hasher.hexdigest() == expected_sha256, "LOCAL_PACKAGE_CHANGED")
            stream.flush()
            os.fsync(stream.fileno())

    def seal_package(self, package):
        checker = self.d.checking()
        store, root = checker.package(package)
        directory = wire.safe_path(package["path"], directory=True)
        require(directory.is_relative_to(self.s.root), "OWNED_PACKAGE_REQUIRED")
        manifest = read(directory / "manifest.json", 16 * MIB)
        require(digest(manifest) == package["manifest_sha256"].lower(), "LOCAL_PACKAGE_CHANGED")
        count, total = 0, len(manifest)
        for key in sorted(store.closure(root)):
            _identifier, payload = store.objects[key]
            raw = checker.S.C.dumps(payload)
            count += 1
            total += len(raw)
            require(count <= 8192 and total <= checker.byte_limit + 16 * MIB, "LOCAL_PACKAGE_BOUND")
            self._flush_file(directory / "objects" / (key + ".cbor"), len(raw), digest(raw))
        self._flush_file(directory / "manifest.json", len(manifest), digest(manifest))
        self.d.event["selected_package_files_fsynced"] = count + 1
        self.d.event["package_durability_profile"] = "PROCESS_INTERRUPTION_ONLY_NOT_POWER_LOSS"

    def publication_offer(self, offer):
        try:
            selected = self.reuse(offer)
            self.seal_package(selected["package"])
            return selected
        except wire.WireError as error:
            raise Refusal(error.code) from None
        except OSError as error:
            raise Refusal("LOCAL_PUBLICATION_IO_FAILURE", type(error).__name__ + ": " + str(error)[:512]) from None
        finally:
            self.observe()

    def expose(self, req):
        keys(req["args"], {"selected"})
        handles = req["args"]["selected"]
        require(type(handles) is list and 1 <= len(handles) <= 32 and
                all(type(handle) is str for handle in handles), "EXPOSURE_SELECTION_LIMIT")
        offers, selected, seen = [], [], set()
        for handle in handles:
            data, offer = self.d.selected_candidate(req["client"], handle)
            cut = self.s.cut(data["snapshot"])
            require(cut["provider"] == "P1", "EXPOSURE_PROVIDER")
            sequence = data["sequence"]
            require(sequence not in seen, "EXPOSURE_DUPLICATE")
            seen.add(sequence)
            publication = self.s.require_published("P1", sequence, offer["descriptor_id"])
            offers.append(offer)
            selected.append({"provider": "P1", "sequence": sequence, "descriptor_id": offer["descriptor_id"],
                             "publication": publication})
        foundation = self.foundation(req["client"])
        checker = self.d.checking()
        for offer in offers:
            self.revalidate(offer)
        directory = checker.domains.require_write(checker.work_dir / "peer-view")
        catalog = wire.build_view(directory, foundation, offers)
        checker.checkpoint()
        result = {"kind": "peer_view", "directory": str(directory), "foundation": foundation,
                  "catalog": pin(directory / "catalog.json", wire.CATALOG_MAX),
                  "complete": pin(directory / "complete.json", 4096),
                  "selected": selected, "mathematicalAcceptance": False}
        require(exact(catalog["foundation"], foundation) and len(catalog["entries"]) == len(selected), "EXPOSURE_BINDING")
        self.d.event["peer_view_catalog_sha256"] = result["catalog"]["sha256"]
        return result

    def replica_expose(self, req):
        keys(req["args"], {"acquisition"})
        handle = req["args"]["acquisition"]
        acquisition, selection, offer = replica_custody(self.s, self.config, req["client"], handle)
        foundation = self.foundation(req["client"])
        require(exact(foundation, selection["foundation"]), "FOUNDATION_MISMATCH")
        received = acquisition["received_package"]
        incoming = wire.safe_path(received["path"], directory=True)
        require(incoming == self.s.root / "work" / acquisition["request"] / "incoming",
                "REPLICA_RECEIVED_PATH")
        manifest_raw = wire.read_local(incoming / "manifest.json", wire.MANIFEST_MAX)
        require(digest(manifest_raw) == received["manifest_sha256"], "REPLICA_RECEIVED_CHANGED")
        manifest = wire.parse_manifest(manifest_raw, foundation)
        # Check every selected path before the structural checker reads it.
        # The trusted owner must keep selected files stable during preparation.
        for identifier in manifest["objects"]:
            wire.safe_path(incoming / "objects" / wire.object_name(identifier))
        checker = self.d.checking()
        replica_offer = dict(offer, package=received)
        self.revalidate(replica_offer)  # full closure/inventories/metadata; no export/native work
        directory = checker.domains.require_write(checker.work_dir / "peer-view")
        catalog = wire.build_view(directory, foundation, [replica_offer])
        require(exact(catalog["entries"], [selection["entry"]]), "REPLICA_EXACT_ENTRY_REQUIRED")
        loaded = wire.load_view(directory)  # authenticate the flushed completed view and bundle
        result = {"kind": "peer_view", "directory": str(directory), "foundation": foundation,
            "catalog": pin(directory / "catalog.json", wire.CATALOG_MAX),
            "complete": pin(directory / "complete.json", 4096),
            "selected": [{"provider": "P1", "sequence": acquisition["sequence"],
                "descriptor_id": acquisition["descriptor_id"], "basis": "replica-custody",
                "acquisition": handle}], "mathematicalAcceptance": False}
        require(exact(loaded["catalog"], catalog)
                and digest(loaded["catalog_raw"]) == result["catalog"]["sha256"],
                "REPLICA_VIEW_BINDING")
        checker.checkpoint()
        self.d.event["peer_view_catalog_sha256"] = result["catalog"]["sha256"]
        return {"view": result, "custody": [acquisition, selection, offer]}

    def commit(self, req, prepared):
        self.observe()
        client, operation = req["client"], req["op"]
        common = {"status": "OK", "untrusted": True, "candidate_only": True,
                  "mathematicalAcceptance": False, "native_stages": 0}
        if operation == "peer_find":
            rows = []
            for entry in prepared["catalog"]["entries"]:
                selection = {"peer": prepared["peer"], "endpoint": prepared["endpoint"],
                             "foundation": prepared["foundation"], "catalog_sha256": prepared["catalog_sha256"],
                             "entry": entry}
                handle = self.s.put_record("remote", client, selection)
                rows.append(dict(entry, remote=handle, candidate_only=True))
            return dict(common, peer=prepared["peer"], rows=rows, catalog_sha256=prepared["catalog_sha256"],
                        complete=True, completeness_scope="SELECTED_PEER_CATALOG_ONLY")
        if operation == "peer_acquire":
            offer, selection = prepared["offer"], prepared["selection"]
            snapshot, sequence, existing = self.s.append("P1", offer)
            candidate = self.d.candidate(client, snapshot, sequence, offer)
            evidence = {"remote": prepared["remote"], "peer": selection["peer"], "endpoint": selection["endpoint"],
                        "catalog_sha256": selection["catalog_sha256"], "bundle_sha256": selection["entry"]["bundle_sha256"],
                        "descriptor_id": offer["descriptor_id"], "sequence": sequence, "snapshot": snapshot,
                        "package": offer["package"], "received_package": prepared["received_package"],
                        "request": self.d.key, "mathematicalAcceptance": False}
            acquisition = self.s.put_record("acquisition", client, evidence)
            return dict(common, candidate=candidate, snapshot=snapshot, descriptor_id=offer["descriptor_id"],
                        existing=existing, acquisition=acquisition)
        if operation == "replica_expose":
            # Ledger-only rechecks inside the ordinary visibility transaction.
            keys(req["args"], {"acquisition"})
            acquisition, selection, offer = replica_custody(
                self.s, self.config, client, req["args"]["acquisition"])
            require(exact([acquisition, selection, offer], prepared["custody"])
                    and exact(prepared["view"]["foundation"], selection["foundation"])
                    and exact(prepared["view"]["selected"], [{"provider": "P1",
                        "sequence": acquisition["sequence"], "descriptor_id": acquisition["descriptor_id"],
                        "basis": "replica-custody", "acquisition": req["args"]["acquisition"]}]),
                    "REPLICA_COMMIT_BINDING")
            prepared = prepared["view"]
        if operation in {"expose", "replica_expose"}:
            handle = self.s.put_record("view", client, prepared)
            reply = dict(common, view=handle, catalog_sha256=prepared["catalog"]["sha256"],
                         entries=len(prepared["selected"]), historical_view=True)
            if operation == "replica_expose":
                reply["basis"] = "replica-custody"
            return reply
        raise Refusal("UNKNOWN_OPERATION")
