"""Ordinary Lean authoring over a live mixed exact-warrant session.

Mechanical successor of the reviewed exact-J context/source adapter. The same
pure traversal, canonical emitter, owner worker and native relation are reused.
Only exact session/operation gates, fixed basis, liveness and onward packet form
change. Every produced witness/packet remains UNTRUSTED until real admission.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
from pathlib import Path
import time

from authoring.context import DEFAULT_LIMITS, SCHEMA as CONTEXT_SCHEMA, _foundation as _decode_foundation, _records
from authoring.source import REQUEST_SCHEMA, EXPORT_SCHEMA, NATIVE_NAME_LIMITS
from modules import codec as C
from delta.reprepare import emit_relation_rows
from modules.source_rows import SourceRows, decode_source
from modules.receipt.witness import decode_journal
from preparation.owner import OwnerPreparation
from production.producer import MIB, encoded, parse, file_pin, pin_fields, hash_bytes, require, uint
from .packet import Envelope, need


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


from .imports_atomic import (MixedImportSession, _context_limits, _decode_context_foundation, _build_context)
from .interface_projection import project_frontend_context


def _foundation(raw, pin, session):
    need(type(session) is MixedImportSession, "MIXED_FOUNDATION_EXACT_SESSION")
    session._live()
    result = _decode_context_foundation(raw,pin,session._basis)
    session._live()
    return result


def prepare_mixed_context(session, foundation_bytes, foundation_sha256, *, limits=None):
    """Retained unsealed route, using the same extracted pure context algorithm."""
    need(type(session) is MixedImportSession, "MIXED_AUTHORING_EXACT_SESSION")
    caps = _context_limits(limits)
    need(type(foundation_bytes) is bytes and len(foundation_bytes) <= caps["data_bytes"],
         "MIXED_AUTHORING_FOUNDATION_INPUT")
    items,binding = session.selection()
    foundation,work = _foundation(foundation_bytes,foundation_sha256,session)
    ready = _build_context(items,binding,foundation_bytes,foundation_sha256,
                           foundation,work,session._basis,session.census(),caps,
                           definition_mode=session._definition_mode)
    session.require_selection(binding)
    return ready


class MixedSourceOperation:
    """One immutable owner-source selection and one consumed export return."""
    def __init__(self, session, foundation_bytes, foundation_sha256, source, roots,
                 *, limits=None, envelope=None, view=None):
        need(type(session) is MixedImportSession, "MIXED_SOURCE_EXACT_SESSION")
        need(type(source) is str and 0 < len(source.encode("utf-8")) <= 65536, "MIXED_SOURCE_BYTES")
        need(type(roots) is list and 1 <= len(roots) <= 64, "MIXED_SOURCE_ROOT_COUNT")
        for name in roots: C.validate_name(name)
        need(len({C.name_key(n) for n in roots}) == len(roots), "MIXED_SOURCE_DUPLICATE_ROOT")
        self._session = self._origin_session = session
        self._origin_basis = session._basis
        self._deadline = session._deadline
        self._closed = self._consumed = False
        self._source_sha = _sha(source.encode("utf-8")); self._roots = deepcopy(roots)
        self._envelope = Envelope() if envelope is None else envelope
        need(type(self._envelope) is Envelope, "MIXED_SOURCE_ENVELOPE")
        self._envelope.validate()
        self._view = view
        if view is None:
            need(not session._sealed,"MIXED_SOURCE_SEALED_VIEW_REQUIRED")
            self._context = prepare_mixed_context(session,foundation_bytes,foundation_sha256,limits=limits)
        else:
            session.require_view(view)
            need(type(foundation_bytes) is bytes and foundation_bytes == session._view_payload[4]
                 and foundation_sha256 == session._view_payload[3],"MIXED_SOURCE_VIEW_FOUNDATION")
            need(limits is None,"MIXED_SOURCE_SEALED_CONTEXT_LIMITS_FIXED")
            self._context = session.view_context(view)
        self._foundation_bytes = foundation_bytes
        self._binding = self._context["selection_binding"]
        self._request = None
        self._frontend_projection = None
        if self._context["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY":
            packet = self._context["packet"]
            boundaries = {C.name_key(name) for name in packet["foundation_view"]["names"]}
            for item in packet["imports"]:
                boundaries.update(C.name_key(C.relocated_name(item["owner"], d["name"]), NATIVE_NAME_LIMITS)
                                  for d in item["group"]["declarations"])
            need(not boundaries.intersection(C.name_key(name) for name in roots), "MIXED_SOURCE_ROOT_BOUND")
            # The frontend is an untrusted proposal generator. Keep the original
            # authenticated packet above for finish()/emit_relation_rows; only
            # this separate request view may replace deferred definitions.
            frontend_packet = packet
            if packet.get("definition_mode", "eager") == "interface-only":
                frontend, self._frontend_projection = project_frontend_context(self._context)
                frontend_packet = frontend["packet"]
            self._request = C.canonical({"schema": REQUEST_SCHEMA, "context": frontend_packet, "source": source,
                "roots": self._roots, "source_sha256": self._source_sha, "mathematical_acceptance": False})
        self._active()

    def _active(self):
        need(not self._closed and self._session is self._origin_session
             and self._session._basis is self._origin_basis
             and time.monotonic() < self._deadline, "MIXED_SOURCE_CLOSED_ORIGIN_OR_DEADLINE")
        if self._view is not None:
            self._session.require_view(self._view)
            need(self._binding == self._session._view_payload[2],"MIXED_IMPORT_SELECTION_CHANGED")
        else:
            self._session.require_selection(self._binding)

    def prepare(self):
        self._active()
        if self._request is None:
            result = deepcopy(self._context)
        else:
            result = {"status": "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION",
                "request": self._request, "request_sha256": _sha(self._request),
                "cost": deepcopy(self._context["cost"]), "mathematical_acceptance": False}
            if self._frontend_projection is not None:
                result["frontend_projection"] = deepcopy(self._frontend_projection)
        self._active()
        return result

    def finish(self, export_bytes):
        self._active()
        need(self._request is not None and not self._consumed, "MIXED_SOURCE_UNCONSUMED_READY_REQUIRED")
        self._consumed = True
        need(type(export_bytes) is bytes and 0 < len(export_bytes) <= 16*MIB, "MIXED_SOURCE_EXPORT_BYTES")
        exported = C.parse_json(export_bytes)
        C.fields(exported, {"schema", "source_sha256", "selection_binding", "roots", "rows",
                            "local_names", "status", "mathematical_acceptance"})
        need(exported["schema"] == EXPORT_SCHEMA and exported["source_sha256"] == self._source_sha
             and exported["selection_binding"] == self._binding and exported["roots"] == self._roots
             and exported["status"] == "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION"
             and exported["mathematical_acceptance"] is False, "MIXED_SOURCE_EXPORT_BINDING")
        # Never use the frontend projection as authenticated declarations.
        packet = self._context["packet"]
        externals = [{"source_name": C.relocated_name(item["owner"], d["name"]),
                      "module": item["owner"], "relative_name": d["name"]}
                     for item in packet["imports"] for d in item["group"]["declarations"]]
        reader = SourceRows(exported["rows"], [], [], limits=NATIVE_NAME_LIMITS)
        names = [reader.name(d["name"]) for row in reader.declarations for d in _records(row)]
        keys = [C.name_key(name) for name in names]
        need(len(set(keys)) == len(keys)
             and sorted(keys) == sorted(C.name_key(name) for name in exported["local_names"]),
             "MIXED_SOURCE_LOCAL_CENSUS")
        need(set(C.name_key(name) for name in self._roots) <= set(keys), "MIXED_SOURCE_ROOT_NOT_CAPTURED")
        local = decode_source(exported["rows"], names, packet["foundation_view"]["names"],
            packet["foundation"], packet["policy"], externals, NATIVE_NAME_LIMITS)
        C.validate_spec(local.spec)
        for (arity, unused), raw in local.bodies.items(): C.validate_expr(C.parse_json(raw), arity)
        actual = {C.name_key(d["name"]): d["kind"] for g in local.spec["groups"] for d in g["declarations"]}
        need(all(actual[C.name_key(name)] in ("theorem", "definition", "opaque", "inductive")
                 for name in self._roots), "MIXED_SOURCE_ROOT_KIND")
        need(not local.claims, "MIXED_SOURCE_LOCAL_ONLY")
        self._active()
        items, binding = self._session.selection()
        need(binding == self._binding, "MIXED_SOURCE_SELECTION_CHANGED")
        for item in items:
            for body in item["bodies"]:
                local.supply_body(body["expression"], body["universes"])
        rows = emit_relation_rows(self._foundation_bytes, local, packet["imports"])
        parents, ranks = [], []
        for item in items:
            parsed = decode_journal(item["journal"])
            need(parsed["module"] != local.module, "MIXED_SOURCE_PARENT_COLLISION")
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
        image = bytes.fromhex(self._origin_basis.image)
        words = [int.from_bytes(image[i:i+4], "little") for i in range(0, 32, 4)]
        witness = {"schema": "DMKN_CERTIFIED_MODULES_V2", "image": words, "rank": rank,
                   "local_spec": local.spec, "rows": rows, "parents": parents, "bodies": bodies}
        raw, census = self._session.onward_packet(witness, self._binding, self._envelope)
        result = {"status": "UNTRUSTED_MIXED_DELTA_PACKET", "packet": raw, "packet_sha256": _sha(raw),
            "summary": C.summarize(local.spec), "local_module": local.module,
            "local_groups": len(local.spec["groups"]), "source_sha256": self._source_sha,
            "roots": deepcopy(self._roots), "parent_selection_binding": self._binding,
            "census": census, "mathematical_acceptance": False}
        self._active()
        return result

    def close(self):
        self._closed = True; self._request = None


class MixedOwnerPreparation(OwnerPreparation):
    """Reuse original pinned worker, Jobs and aggregate owner controller only.

    No proof/snapshot API is enabled here; author returns complete untrusted
    mixed packet material. Only a subsequent actual MixedDeltaVerifier.receive admits it.
    """
    def __init__(self, profile, allowance, output_directory):
        base = Path(__file__).resolve().parents[1]
        extra = {base/name for name in ("mixed_claims/authoring.py", "mixed_claims/imports.py",
            "mixed_claims/receiver.py", "mixed_claims/packet.py", "mixed_claims/__init__.py",
            "delta_claims/receiver.py", "delta_claims/claims.py", "delta_claims/__init__.py",
            "delta/reprepare.py", "delta/receiver.py", "delta/packet.py", "delta/__init__.py",
            "aggregate_claims/__init__.py", "aggregate_claims/aggregate_admission.py",
            "aggregate_claims/admission_binding.py", "aggregate_claims/bindings.py",
            "admission/verifier.py", "admission/bindings.py",
            "mixed_claims/authoring_atomic.py", "mixed_claims/imports_atomic.py",
            "mixed_claims/interface_projection.py")}
        require(type(profile) is dict and type(profile.get("source_pins")) is list,
                "MIXED_PREPARATION_SOURCE_PROFILE")
        require(extra <= {pin_fields(row) for row in profile["source_pins"]},
                "MIXED_PREPARATION_REQUIRED_SOURCE_PINS")
        super().__init__(profile, allowance, output_directory)

    def author(self, operation, name, *, cpu_seconds, wall_seconds, memory_mib=2048):
        entered = time.monotonic()
        def work(directory):
            uint(cpu_seconds, 1200, 1); uint(wall_seconds, 600, 1); uint(memory_mib, 4096, 64)
            call_deadline = min(self._deadline, entered+wall_seconds)
            require(type(operation) is MixedSourceOperation, "MIXED_PREPARATION_EXACT_SOURCE_OPERATION")
            operation._active()
            original_session, original_basis = operation._origin_session, operation._origin_basis
            original_deadline = operation._deadline
            def source_live():
                require(operation._origin_session is original_session
                    and operation._origin_basis is original_basis and operation._deadline == original_deadline,
                    "MIXED_PREPARATION_SOURCE_ORIGIN_CHANGED")
                operation._active()
                require(time.monotonic() < min(call_deadline, original_deadline), "MIXED_PREPARATION_TOTAL_WALL")
            source_live()
            p = self._profile["producer"]
            require((original_basis.image, original_basis.foundation, original_basis.policy)
                    == (p["image_id"], p["foundation"], p["policy"]), "MIXED_PREPARATION_SOURCE_PROFILE")
            ready = operation.prepare()
            if ready["status"] == "NEED_AUTHORING_CONTEXT_DATA":
                return {**deepcopy(ready), "_completion": source_live}
            require(ready["status"] == "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION"
                    and ready["mathematical_acceptance"] is False, "MIXED_PREPARATION_SOURCE_READY")
            raw = ready["request"]
            require(type(raw) is bytes and 0 < len(raw) <= 16*MIB
                    and hash_bytes(raw) == ready["request_sha256"], "MIXED_PREPARATION_REQUEST")
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
            require(len(encoded(config)) <= 128*1024, "MIXED_PREPARATION_CONFIG_BYTES")
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
                "MIXED_PREPARATION_WORKER_BINDING")
            child = operation.finish(export)
            require(child["status"] == "UNTRUSTED_MIXED_DELTA_PACKET"
                    and child["mathematical_acceptance"] is False, "MIXED_PREPARATION_UNTRUSTED_PACKET")
            self._space(len(child["packet"])+MIB, 2)
            source_live(); self._check(pins)
            destination = directory/"mixed-packet.json"
            self._write(destination, child["packet"])
            packet_pin = file_pin(destination)
            require(packet_pin["sha256"] == child["packet_sha256"], "MIXED_PREPARATION_FINAL_PACKET_PIN")
            pins[str(destination)] = packet_pin
            source_live(); self._check(pins)
            require(time.monotonic() < deadline, "MIXED_PREPARATION_TOTAL_WALL")
            def completion():
                source_live(); self._check(pins)
                require(time.monotonic() < deadline, "MIXED_PREPARATION_TOTAL_WALL")
            return {"status": "UNTRUSTED_MIXED_DELTA_PACKET_PREPARED", "child": child,
                "packet": packet_pin, "export": file_pin(directory/"frontend/EXPORT.json"),
                "mathematical_acceptance": False, "_completion": completion}
        return self._call("mixed-author", name, work)

    def snapshot(self, *args, **kwargs):
        raise ValueError("MIXED_PACKET_IS_NOT_A_RECEIPT_SNAPSHOT_REQUEST")
