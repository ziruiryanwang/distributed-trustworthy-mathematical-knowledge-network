"""Owner-source preparation/return binding, without autonomous process launch.

Lean exports and this module's output remain untrusted prover data. The live
session is rechecked; only real final receipt verification admits mathematics.
"""
from copy import deepcopy
from dataclasses import replace
import hashlib
import time

from modules import codec as C
from modules.source_rows import SourceRows, decode_source
from .context import prepare_context, require_live_selection, _records
from .imports import ImportSession

REQUEST_SCHEMA = "DMKN_OWNER_LEAN_AUTHORING_REQUEST_V1"
EXPORT_SCHEMA = "DMKN_OWNER_LEAN_AUTHORING_EXPORT_V1"
NATIVE_NAME_LIMITS = replace(C.DEFAULT_LIMITS, max_name_parts=C.DEFAULT_LIMITS.max_name_parts+3)


class SourceOperation:
    """One same-session source/roots/context selection and one export return.

    The owner must run only its authorized source under its original supervised
    process allocation. This object neither launches a process nor grants an
    execution allowance; returned JSON flags cannot prove that a process ran.
    """
    def __init__(self, session, foundation_bytes, foundation_sha256, source, roots, *, limits=None):
        C.require(type(session) is ImportSession, "SOURCE_EXACT_SESSION")
        C.require(type(source) is str and 0 < len(source.encode("utf-8")) <= 65536, "SOURCE_OWNER_BYTE_LIMIT")
        C.require(type(roots) is list and 1 <= len(roots) <= 64, "SOURCE_ROOT_COUNT")
        for name in roots: C.validate_name(name)
        C.require(len({C.name_key(name) for name in roots}) == len(roots), "SOURCE_DUPLICATE_ROOT")
        self._session, self._closed, self._consumed = session, False, False
        self._origin_session, self._origin_verifier = session, session._verifier
        self._deadline = session._deadline
        self._source, self._roots = source, deepcopy(roots)
        self._source_sha = hashlib.sha256(source.encode("utf-8")).hexdigest()
        self._context = prepare_context(session, foundation_bytes, foundation_sha256, limits=limits)
        self._foundation_bytes = foundation_bytes  # validated immutable bytes
        self._binding = self._context["selection_binding"]
        self._request = None
        if self._context["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY":
            packet = self._context["packet"]
            boundaries = {C.name_key(name) for name in packet["foundation_view"]["names"]}
            for item in packet["imports"]:
                boundaries.update(C.name_key(C.relocated_name(item["owner"], d["name"]), NATIVE_NAME_LIMITS)
                                  for d in item["group"]["declarations"])
            C.require(not boundaries.intersection(C.name_key(name) for name in roots), "SOURCE_ROOT_ALREADY_BOUND")
            request = {"schema": REQUEST_SCHEMA, "context": packet, "source": source,
                       "roots": self._roots, "source_sha256": self._source_sha,
                       "mathematical_acceptance": False}
            self._request = C.canonical(request)
        self._active()

    def _active(self):
        C.require(not self._closed, "SOURCE_OPERATION_CLOSED")
        C.require(self._session is self._origin_session
                  and self._session._verifier is self._origin_verifier
                  and time.monotonic() < self._deadline, "SOURCE_ORIGIN_OR_DEADLINE_CHANGED")
        require_live_selection(self._session, self._binding)

    def prepare(self):
        self._active()
        if self._request is None:
            result = deepcopy(self._context)
            self._active()
            return result
        result = {"status": "OWNER_SOURCE_REQUIRES_SUPERVISED_LEAN_AND_FINAL_RELATION",
                  "request": bytes(self._request), "request_sha256": hashlib.sha256(self._request).hexdigest(),
                  "cost": deepcopy(self._context["cost"]), "mathematical_acceptance": False}
        self._active()
        return result

    def finish(self, export_bytes):
        self._active()
        C.require(self._request is not None and not self._consumed, "SOURCE_READY_UNCONSUMED_OPERATION_REQUIRED")
        self._consumed = True  # Malformed/failed returns consume this exact operation too.
        C.require(type(export_bytes) is bytes and 0 < len(export_bytes) <= 16*1024**2, "SOURCE_EXPORT_BYTE_LIMIT")
        exported = C.parse_json(export_bytes)
        C.fields(exported, {"schema", "source_sha256", "selection_binding", "roots", "rows",
                            "local_names", "status", "mathematical_acceptance"})
        C.require(exported["schema"] == EXPORT_SCHEMA
                  and exported["source_sha256"] == self._source_sha
                  and exported["selection_binding"] == self._binding
                  and exported["roots"] == self._roots
                  and exported["status"] == "OWNER_FRONTEND_EXPORT_REQUIRES_INDEPENDENT_RELATION"
                  and exported["mathematical_acceptance"] is False, "SOURCE_RETURN_BINDING")
        packet = self._context["packet"]
        foundation_names = packet["foundation_view"]["names"]
        externals = [{"source_name": C.relocated_name(item["owner"], d["name"]),
                      "module": item["owner"], "relative_name": d["name"]}
                     for item in packet["imports"] for d in item["group"]["declarations"]]
        # Derive the local census from actual returned declaration rows, then
        # demand agreement with the exporter's report; neither is trust authority.
        reader = SourceRows(exported["rows"], [], [], limits=NATIVE_NAME_LIMITS)
        local_names = [reader.name(d["name"]) for row in reader.declarations for d in _records(row)]
        keys = [C.name_key(name) for name in local_names]
        C.require(len(set(keys)) == len(keys)
                  and sorted(keys) == sorted(C.name_key(name) for name in exported["local_names"]),
                  "SOURCE_RETURN_LOCAL_CENSUS")
        C.require(set(C.name_key(name) for name in self._roots) <= set(keys), "SOURCE_ROOT_NOT_CAPTURED")
        local = decode_source(exported["rows"], local_names, foundation_names,
                              packet["foundation"], packet["policy"], externals, NATIVE_NAME_LIMITS)
        # Only native absolute names gain the fixed three relocation parts.
        # Reapply unchanged protocol limits to every emitted relative name/term.
        C.validate_spec(local.spec)
        for (arity, unused), raw in local.bodies.items(): C.validate_expr(C.parse_json(raw), arity)
        actual = {C.name_key(d["name"]): d["kind"]
                  for group in local.spec["groups"] for d in group["declarations"]}
        C.require(all(actual[C.name_key(name)] in ("theorem", "definition", "opaque", "inductive")
                      for name in self._roots), "SOURCE_ROOT_KIND")
        self._active()
        image = bytes.fromhex(self._session._verifier._image)
        words = [int.from_bytes(image[i:i+4], "little") for i in range(0, 32, 4)]
        result = self._session.make_request(local, C.parse_json(self._foundation_bytes), words)
        result = {**result, "source_sha256": self._source_sha, "roots": deepcopy(self._roots),
                "local_module": local.module, "local_groups": len(local.spec["groups"]),
                "parent_selection_binding": self._binding, "mathematical_acceptance": False}
        self._active()
        return result

    def close(self):
        self._closed = True
        self._request = None
        # Session/verifier lifetimes remain owned by the existing workflow.
