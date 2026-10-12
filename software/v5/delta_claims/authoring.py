"""Exact-warrant public authoring; one explicit warrant per semantic module.

Canonical relation-row order and native mathematical relation are unchanged.

Owner-source authoring over an actual bounded native-delta admission.

This is preparation, not a checker, receipt, or transferable authority. The
unchanged native frontend and independent delta receiver establish different
boundaries. In particular every onward packet retains uncertified proof ancestry.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
import time

from authoring.context import DEFAULT_LIMITS, SCHEMA as CONTEXT_SCHEMA, _foundation, _records
from authoring.source import REQUEST_SCHEMA, EXPORT_SCHEMA, NATIVE_NAME_LIMITS
from modules import codec as C
from delta.reprepare import emit_relation_rows
from modules.source_rows import SourceRows, decode_source
from modules.receipt.witness import decode_journal
from preparation.owner import OwnerPreparation
from production.producer import MIB, encoded, parse, file_pin, pin_fields, hash_bytes, require, uint
from delta.packet import Envelope, need
from .receiver import DeltaVerifier, VerifiedDelta


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


from .imports import DeltaImportSession


def prepare_delta_context(session, foundation_bytes, foundation_sha256, *, limits=None):
    """Proof-form-neutral frontend context with real delta-specific live authority.

    Pure reconstruction duplicates no mathematical checker. The fixed frontend
    request schema is shared; exact receipt-only ImportSession gates stay intact.
    """
    need(type(session) is DeltaImportSession, "DELTA_AUTHORING_EXACT_SESSION")
    caps = dict(DEFAULT_LIMITS if limits is None else limits)
    C.fields(caps, set(DEFAULT_LIMITS))
    for key, maximum in DEFAULT_LIMITS.items():
        need(0 < C.uint(caps[key], maximum), "DELTA_AUTHORING_CONTEXT_LIMIT:"+key)
    need(type(foundation_bytes) is bytes and len(foundation_bytes) <= caps["data_bytes"],
         "DELTA_AUTHORING_FOUNDATION_INPUT")
    items, binding = session.selection()
    foundation, work = _foundation(foundation_bytes, foundation_sha256, session)
    need(work <= caps["expression_visits"], "DELTA_AUTHORING_FOUNDATION_WORK")
    foundation_names = {C.name_key(name) for name in foundation["names"]}
    groups, addresses, bodies, modules = {}, {}, {}, set()
    demands = {}; stored_bytes = len(foundation_bytes); declarations = 0
    for item in items:
        owner = item["module"]; modules.add(owner)
        for opening in item["openings"]:
            group = C.verify_group_opening(owner, opening); key = owner, opening["index"]
            need(key not in groups, "DELTA_AUTHORING_DUPLICATE_GROUP")
            stored_bytes += len(C.canonical(opening)); declarations += len(group["declarations"])
            need(len(groups)+1 <= caps["groups"] and declarations <= caps["declarations"]
                 and stored_bytes <= caps["data_bytes"], "DELTA_AUTHORING_CONTEXT_CENSUS")
            groups[key] = deepcopy(group)
            for d in group["declarations"]:
                address = owner, C.name_key(d["name"])
                need(address not in addresses, "DELTA_AUTHORING_DUPLICATE_DECLARATION")
                addresses[address] = key
        for body in item["bodies"]:
            key = owner, body["universes"], body["digest"]
            need(key not in bodies and C.body_id(body["expression"], body["universes"]) == body["digest"],
                 "DELTA_AUTHORING_BODY_BINDING")
            stored_bytes += len(C.canonical(body))
            need(stored_bytes <= caps["data_bytes"], "DELTA_AUTHORING_CONTEXT_CENSUS")
            bodies[key] = deepcopy(body["expression"])
    edges = {key: set() for key in groups}; selected_bodies = {key: {} for key in groups}

    def demand(value):
        key = C.canonical(value)
        need(key in demands or len(demands) < caps["demands"], "DELTA_AUTHORING_DEMAND_LIMIT")
        demands[key] = value

    def reference(key, ref):
        if ref[0] == "foundation":
            need(C.name_key(ref[1]) in foundation_names, "DELTA_AUTHORING_UNKNOWN_FOUNDATION")
            return
        owner, name = (key[0], ref[1]) if ref[0] == "local" else (ref[1], ref[2])
        address = owner, C.name_key(name)
        if owner not in modules:
            demand({"kind": "NeedVerifiedDeltaMember", "module": owner, "name": deepcopy(name)})
        elif address not in addresses:
            demand({"kind": "NeedDeclaration", "module": owner, "name": deepcopy(name)})
        else:
            target = addresses[address]
            need(target != key or groups[key]["kind"] == "inductive", "DELTA_AUTHORING_SELF_REFERENCE")
            if target != key: edges[key].add(target)

    def expression(key, value):
        nonlocal work
        pending = [value]
        while pending:
            expr = pending.pop(); work += 1
            need(work <= caps["expression_visits"], "DELTA_AUTHORING_EXPRESSION_WORK")
            tag = expr[0]
            if tag in ("const", "proj"): reference(key, expr[1])
            children = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
                        "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}[tag]
            pending.extend(expr[i] for i in children)

    for key, group in groups.items():
        for d in group["declarations"]:
            expression(key, d["type"])
            hashes = ([d["value_hash"]] if d["kind"] == "definition" else
                      [r["value_hash"] for r in d["meta"]["rules"]] if d["kind"] == "recursor" else [])
            for digest in hashes:
                address = key[0], d["universes"], digest
                if address not in bodies:
                    demand({"kind": "NeedBody", "module": key[0], "name": deepcopy(d["name"]),
                            "universes": d["universes"], "body_hash": digest})
                elif address not in selected_bodies[key]:
                    selected_bodies[key][address] = bodies[address]
                    expression(key, bodies[address])
    report = {"groups": len(groups), "declarations": declarations,
              "counted_expression_visits": work, "selected_input_bytes": stored_bytes,
              "all_session_openings_included": True, "frontend_theorem_ancestor_proof_bytes": 0,
              "onward_uncertified_proof_ancestry_retained": True,
              "fixed_foundation_proof_bodies_included": True,
              "expression_counter_is_not_total_cpu_work": True, "whole_operation_supervision_required": True,
              "warrant_census": session.census()}
    if demands:
        session.require_selection(binding)
        return {"status": "NEED_AUTHORING_CONTEXT_DATA", "demands": [demands[k] for k in sorted(demands)],
                "selection_binding": binding, "cost": report, "mathematical_acceptance": False}
    remaining, ordered, done = set(groups), [], set()
    while remaining:
        ready = [key for key in sorted(remaining) if edges[key] <= done]
        need(ready, "DELTA_AUTHORING_INTERGROUP_CYCLE")
        for key in ready:
            ordered.append({"owner": key[0], "index": key[1], "group": groups[key],
                "bodies": [{"universes": address[1], "digest": address[2], "expression": body}
                           for address, body in sorted(selected_bodies[key].items())]})
        remaining.difference_update(ready); done.update(ready)
    packet = {"schema": CONTEXT_SCHEMA, "foundation": session._verifier._foundation,
              "policy": session._verifier._policy, "foundation_sha256": foundation_sha256,
              "foundation_view": foundation, "imports": ordered,
              "selection_binding": binding, "mathematical_acceptance": False}
    raw = C.canonical(packet)
    need(len(raw) <= caps["data_bytes"], "DELTA_AUTHORING_CONTEXT_OUTPUT")
    report["frontend_packet_bytes"] = len(raw)
    session.require_selection(binding)
    return {"status": "UNTRUSTED_AUTHORING_CONTEXT_READY", "packet": C.parse_json(raw),
            "selection_binding": binding, "cost": report, "mathematical_acceptance": False}


class DeltaSourceOperation:
    """One immutable owner-source selection and one consumed export return."""
    def __init__(self, session, foundation_bytes, foundation_sha256, source, roots,
                 *, limits=None, envelope=None):
        need(type(session) is DeltaImportSession, "DELTA_SOURCE_EXACT_SESSION")
        need(type(source) is str and 0 < len(source.encode("utf-8")) <= 65536, "DELTA_SOURCE_BYTES")
        need(type(roots) is list and 1 <= len(roots) <= 64, "DELTA_SOURCE_ROOT_COUNT")
        for name in roots: C.validate_name(name)
        need(len({C.name_key(n) for n in roots}) == len(roots), "DELTA_SOURCE_DUPLICATE_ROOT")
        self._session = self._origin_session = session
        self._origin_verifier = session._verifier
        self._deadline = session._deadline
        self._closed = self._consumed = False
        self._source_sha = _sha(source.encode("utf-8")); self._roots = deepcopy(roots)
        self._envelope = Envelope() if envelope is None else envelope
        need(type(self._envelope) is Envelope, "DELTA_SOURCE_ENVELOPE")
        self._envelope.validate()
        self._context = prepare_delta_context(session, foundation_bytes, foundation_sha256, limits=limits)
        self._foundation_bytes = foundation_bytes
        self._binding = self._context["selection_binding"]
        self._request = None
        if self._context["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY":
            packet = self._context["packet"]
            boundaries = {C.name_key(name) for name in packet["foundation_view"]["names"]}
            for item in packet["imports"]:
                boundaries.update(C.name_key(C.relocated_name(item["owner"], d["name"]), NATIVE_NAME_LIMITS)
                                  for d in item["group"]["declarations"])
            need(not boundaries.intersection(C.name_key(name) for name in roots), "DELTA_SOURCE_ROOT_BOUND")
            self._request = C.canonical({"schema": REQUEST_SCHEMA, "context": packet, "source": source,
                "roots": self._roots, "source_sha256": self._source_sha, "mathematical_acceptance": False})
        self._active()

    def _active(self):
        need(not self._closed and self._session is self._origin_session
             and self._session._verifier is self._origin_verifier
             and time.monotonic() < self._deadline, "DELTA_SOURCE_CLOSED_ORIGIN_OR_DEADLINE")
        self._session.require_selection(self._binding)

    def prepare(self):
        self._active()
        if self._request is None:
            result = deepcopy(self._context)
        else:
            result = {"status": "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION",
                "request": self._request, "request_sha256": _sha(self._request),
                "cost": deepcopy(self._context["cost"]), "mathematical_acceptance": False}
        self._active()
        return result

    def finish(self, export_bytes):
        self._active()
        need(self._request is not None and not self._consumed, "DELTA_SOURCE_UNCONSUMED_READY_REQUIRED")
        self._consumed = True
        need(type(export_bytes) is bytes and 0 < len(export_bytes) <= 16*MIB, "DELTA_SOURCE_EXPORT_BYTES")
        exported = C.parse_json(export_bytes)
        C.fields(exported, {"schema", "source_sha256", "selection_binding", "roots", "rows",
                            "local_names", "status", "mathematical_acceptance"})
        need(exported["schema"] == EXPORT_SCHEMA and exported["source_sha256"] == self._source_sha
             and exported["selection_binding"] == self._binding and exported["roots"] == self._roots
             and exported["status"] == "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION"
             and exported["mathematical_acceptance"] is False, "DELTA_SOURCE_EXPORT_BINDING")
        packet = self._context["packet"]
        externals = [{"source_name": C.relocated_name(item["owner"], d["name"]),
                      "module": item["owner"], "relative_name": d["name"]}
                     for item in packet["imports"] for d in item["group"]["declarations"]]
        reader = SourceRows(exported["rows"], [], [], limits=NATIVE_NAME_LIMITS)
        names = [reader.name(d["name"]) for row in reader.declarations for d in _records(row)]
        keys = [C.name_key(name) for name in names]
        need(len(set(keys)) == len(keys)
             and sorted(keys) == sorted(C.name_key(name) for name in exported["local_names"]),
             "DELTA_SOURCE_LOCAL_CENSUS")
        need(set(C.name_key(name) for name in self._roots) <= set(keys), "DELTA_SOURCE_ROOT_NOT_CAPTURED")
        local = decode_source(exported["rows"], names, packet["foundation_view"]["names"],
            packet["foundation"], packet["policy"], externals, NATIVE_NAME_LIMITS)
        C.validate_spec(local.spec)
        for (arity, unused), raw in local.bodies.items(): C.validate_expr(C.parse_json(raw), arity)
        actual = {C.name_key(d["name"]): d["kind"] for g in local.spec["groups"] for d in g["declarations"]}
        need(all(actual[C.name_key(name)] in ("theorem", "definition", "opaque", "inductive")
                 for name in self._roots), "DELTA_SOURCE_ROOT_KIND")
        need(not local.claims, "DELTA_SOURCE_LOCAL_ONLY")
        self._active()
        items, binding = self._session.selection()
        need(binding == self._binding, "DELTA_SOURCE_SELECTION_CHANGED")
        for item in items:
            for body in item["bodies"]:
                local.supply_body(body["expression"], body["universes"])
        rows = emit_relation_rows(self._foundation_bytes, local, packet["imports"])
        parents, ranks = [], []
        for item in items:
            parsed = decode_journal(item["journal"])
            need(parsed["module"] != local.module, "DELTA_SOURCE_PARENT_COLLISION")
            parents.append({"journal": list(item["journal"]), "openings": item["openings"]})
            ranks.append(parsed["rank"])
        rank = max(ranks)+1 if ranks else 0
        C.uint(rank, 2**64-1)
        required = set()
        all_groups = [item["group"] for item in packet["imports"]]+local.spec["groups"]
        for group in all_groups:
            for d in group["declarations"]:
                if d["kind"] in ("definition", "opaque"):
                    key = d["universes"], d["value_hash"]
                    if key in local.bodies: required.add(key)
                elif d["kind"] == "recursor":
                    required.update((d["universes"], r["value_hash"]) for r in d["meta"]["rules"])
        bodies = [{"universes": arity, "digest": digest, "expression": C.parse_json(local.bodies[arity, digest])}
                  for arity, digest in sorted(required)]
        image = bytes.fromhex(self._origin_verifier._image)
        words = [int.from_bytes(image[i:i+4], "little") for i in range(0, 32, 4)]
        witness = {"schema": "DMKN_CERTIFIED_MODULES_V2", "image": words, "rank": rank,
                   "local_spec": local.spec, "rows": rows, "parents": parents, "bodies": bodies}
        raw, census = self._session.onward_packet(witness, self._binding, self._envelope)
        result = {"status": "UNTRUSTED_DELTA_PACKET", "packet": raw, "packet_sha256": _sha(raw),
            "summary": C.summarize(local.spec), "local_module": local.module,
            "local_groups": len(local.spec["groups"]), "source_sha256": self._source_sha,
            "roots": deepcopy(self._roots), "parent_selection_binding": self._binding,
            "census": census, "mathematical_acceptance": False}
        self._active()
        return result

    def close(self):
        self._closed = True; self._request = None


class DeltaOwnerPreparation(OwnerPreparation):
    """Reuse original pinned worker, Jobs and aggregate owner controller only.

    No proof/snapshot API is enabled here; author returns a complete untrusted
    delta packet. Only a subsequent actual DeltaVerifier.receive admits it.
    """
    def __init__(self, profile, allowance, output_directory):
        base = Path(__file__).resolve().parents[1]
        extra = {base/name for name in ("delta_claims/authoring.py", "delta_claims/imports.py",
            "delta_claims/claims.py", "delta_claims/receiver.py", "delta_claims/__init__.py",
            "delta/reprepare.py", "delta/receiver.py", "delta/packet.py", "delta/__init__.py",
            "admission/verifier.py", "admission/bindings.py")}
        require(type(profile) is dict and type(profile.get("source_pins")) is list,
                "DELTA_PREPARATION_SOURCE_PROFILE")
        require(extra <= {pin_fields(row) for row in profile["source_pins"]},
                "DELTA_PREPARATION_REQUIRED_SOURCE_PINS")
        super().__init__(profile, allowance, output_directory)

    def author(self, operation, name, *, cpu_seconds, wall_seconds, memory_mib=2048):
        entered = time.monotonic()
        def work(directory):
            uint(cpu_seconds, 1200, 1); uint(wall_seconds, 600, 1); uint(memory_mib, 4096, 64)
            call_deadline = min(self._deadline, entered+wall_seconds)
            require(type(operation) is DeltaSourceOperation, "DELTA_PREPARATION_EXACT_SOURCE_OPERATION")
            operation._active()
            original_session, original_verifier = operation._origin_session, operation._origin_verifier
            original_deadline = operation._deadline
            def source_live():
                require(operation._origin_session is original_session
                    and operation._origin_verifier is original_verifier and operation._deadline == original_deadline,
                    "DELTA_PREPARATION_SOURCE_ORIGIN_CHANGED")
                operation._active()
                require(time.monotonic() < min(call_deadline, original_deadline), "DELTA_PREPARATION_TOTAL_WALL")
            source_live()
            p = self._profile["producer"]
            require((original_verifier._image, original_verifier._foundation, original_verifier._policy)
                    == (p["image_id"], p["foundation"], p["policy"]), "DELTA_PREPARATION_SOURCE_PROFILE")
            ready = operation.prepare()
            if ready["status"] == "NEED_AUTHORING_CONTEXT_DATA":
                return {**deepcopy(ready), "_completion": source_live}
            require(ready["status"] == "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION"
                    and ready["mathematical_acceptance"] is False, "DELTA_PREPARATION_SOURCE_READY")
            raw = ready["request"]
            require(type(raw) is bytes and 0 < len(raw) <= 16*MIB
                    and hash_bytes(raw) == ready["request_sha256"], "DELTA_PREPARATION_REQUEST")
            limits, deadline = self._limits(cpu_seconds, wall_seconds, memory_mib,
                                            min(call_deadline, original_deadline))
            # Retain native export AND full onward proof closure in aggregate storage.
            self._space(len(raw)+96*MIB+operation._envelope.packet_bytes, 18)
            request = directory/"source-request.json"; self._write(request, raw)
            config = {"schema": "DMKN_OWNER_LEAN_WORKER_V1", "worker": self._profile["worker"],
                "executable": self._profile["native_executable"], "lean_root": str(self._lean_root),
                "runtime_pins": deepcopy(self._profile["lean_runtime_pins"]), "request": file_pin(request),
                "output_directory": str(directory/"frontend"), "report_path": str(directory/"worker-result.json"),
                "deadline_monotonic": deadline}
            control = directory/"worker-config.json"
            require(len(encoded(config)) <= 128*1024, "DELTA_PREPARATION_CONFIG_BYTES")
            self._save(control, config); config_pin = file_pin(control)
            pins = {str(request): file_pin(request), str(control): config_pin}
            argv = [p["python"]["path"], "-I", "-S", "-B", self._profile["worker"]["path"],
                    "--config", str(control), "--config-sha256", config_pin["sha256"]]
            self._stage(directory, "author", argv, limits, deadline, pins,
                        (96*MIB+operation._envelope.packet_bytes, 18))
            source_live()
            report = parse(self._A.bounded_read(directory/"worker-result.json", MIB))
            export = self._A.bounded_read(directory/"frontend/EXPORT.json", 16*MIB)
            require(report.get("schema") == "DMKN_OWNER_LEAN_WORKER_RESULT_V1"
                and report.get("status") == "PASS_NATIVE_EXPORT_ONLY"
                and report.get("request_sha256") == pins[str(request)]["sha256"]
                and report.get("executable_sha256") == self._profile["native_executable"]["sha256"]
                and report.get("config_sha256") == config_pin["sha256"]
                and report.get("worker_sha256") == self._profile["worker"]["sha256"]
                and report.get("export_sha256") == hash_bytes(export) and report.get("export_bytes") == len(export)
                and report.get("deadline_monotonic") == deadline and report.get("mathematical_acceptance") is False
                and report.get("native_return_code") == 0 and report.get("native_timed_out") is False
                and report.get("direct_child_reaped") is True and report.get("outer_job_closure_required") is True,
                "DELTA_PREPARATION_WORKER_BINDING")
            child = operation.finish(export)
            require(child["status"] == "UNTRUSTED_DELTA_PACKET"
                    and child["mathematical_acceptance"] is False, "DELTA_PREPARATION_UNTRUSTED_PACKET")
            self._space(len(child["packet"])+MIB, 2)
            source_live(); self._check(pins)
            destination = directory/"delta-packet.json"
            self._write(destination, child["packet"])
            packet_pin = file_pin(destination)
            require(packet_pin["sha256"] == child["packet_sha256"], "DELTA_PREPARATION_FINAL_PACKET_PIN")
            pins[str(destination)] = packet_pin
            source_live(); self._check(pins)
            require(time.monotonic() < deadline, "DELTA_PREPARATION_TOTAL_WALL")
            def completion():
                source_live(); self._check(pins)
                require(time.monotonic() < deadline, "DELTA_PREPARATION_TOTAL_WALL")
            return {"status": "UNTRUSTED_DELTA_PACKET_PREPARED", "child": child,
                "packet": packet_pin, "export": file_pin(directory/"frontend/EXPORT.json"),
                "mathematical_acceptance": False, "_completion": completion}
        return self._call("delta-author", name, work)

    def snapshot(self, *args, **kwargs):
        raise ValueError("DELTA_PACKET_IS_NOT_A_RECEIPT_SNAPSHOT_REQUEST")


