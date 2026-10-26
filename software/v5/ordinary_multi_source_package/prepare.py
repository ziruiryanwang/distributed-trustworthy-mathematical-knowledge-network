"""Offline, explicit configuration preparation. Never executes the product.

Use --request ABSOLUTE_JSON --output FRESH_ABSOLUTE_DIRECTORY. Report hashes
select bytes, not an author or mathematical warrant. The product rechecks them.
Only the Python standard library is imported; no protected state is opened.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import stat

PROFILE = "97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834"
MIB = 1024**2
CUSTODY = dict(objects=(1, 1000000), exports=(1, 16000000),
               logical_bytes=(1024, 2**40), db_pages=(256, 268435456))
INDEX = dict(max_objects=(1, 1000000), max_postings=(1, 128000000),
             max_features=(1, 1048576), max_snapshots=(1, 1000001),
             max_logical_bytes=(1024, 2**40), max_db_pages=(256, 268435456))
SEARCH = dict(providers=(1, 64), snapshots=(1, 256), requests=(1, 512),
              pages=(1, 4096), examined=(1, 131072), candidates=(1, 256),
              bytes=(1024, 32*MIB), wall_ms=(1, 3600000), inflight=(1, 8))
PAGE = dict(scanned=(1, 4096), matches=(1, 8), bytes=(2048, MIB),
            timeout_ms=(1, 1000), record_probes=(1, 65536), node_reads=(1, 100000),
            hash_calls=(1, 2000000), sql_vm_steps=(100, 10000000))
RECEIVE = dict(requests=(1, 8192), reply_bytes=(1, 1024*MIB), units=(1, 1024),
               unit_bytes=(1, 8*MIB), total_bytes=(1, 64*MIB), missing=(1, 4096),
               preflights=(1, 1025), locator_bytes=(1, MIB))
DIRECTORY = dict(requests=(1, 32), reply_bytes=(1, MIB), max_contacts=(1, 64),
                 max_bytes=(1024, 32768), max_age_ms=(1, 60000), attempt_timeout_ms=(1, 5000))
SERVICE_KEYS = {"host", "port", "tls", "lease_seconds", "cleanup_seconds", "limits"}


def need(ok, code):
    if not ok:
        raise ValueError("KIT_" + code)


def fields(value, names):
    need(type(value) is dict and set(value) == set(names), "FIELDS")


def integer(value, low, high):
    need(type(value) is int and low <= value <= high, "INTEGER")
    return value


def identifier(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None, "IDENTIFIER")
    return value


def string(value):
    need(type(value) is str and 0 < len(value) <= 32768 and
         all(ord(c) >= 32 for c in value) and
         not any(marker in value for marker in ("REPLACE_ME", "APPROVED_", "<", ">")),
         "STRING_OR_PLACEHOLDER")
    return value


def limits(value, bounds):
    fields(value, bounds)
    for key, (low, high) in bounds.items():
        integer(value[key], low, high)
    return value


def sequence(value, maximum, *, empty=False):
    need(type(value) is list and (0 if empty else 1) <= len(value) <= maximum, "LIST_BOUND")
    return value


def name(value):
    """A conservative structural name check, not the product semantic validator."""
    sequence(value, 64)
    size = 0
    for part in value:
        need(type(part) is list and len(part) == 2, "NAME_PART")
        integer(part[0], 0, 1)
        if part[0] == 0:
            fields(part[1], {"$bytes"})
            octets = sequence(part[1]["$bytes"], 4096)
            for octet in octets:
                integer(octet, 0, 255)
            raw = bytes(octets)
            need(raw.decode("utf-8").encode("utf-8") == raw, "NAME_UTF8")
            size += len(raw)
        else:
            integer(part[1], 0, 2**32-1)
    need(value[0][0] == 0 and size <= 4096, "NAME_BOUND")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def export_identity(semantic, unit, original_name):
    # Exact public portable identity formula, not a proof of existence/truth.
    return digest(b"DMKN-ORDINARY-EXPORT-V2\0" + canonical([
        identifier(semantic), identifier(unit), name(original_name)]))


def ordinary_path(value, *, existing=False, directory=False, fresh=False):
    """Inspect path metadata only; never read state directories or their contents."""
    path = Path(string(str(value) if isinstance(value, Path) else value))
    need(path.is_absolute() and ".." not in path.parts and len(path.parts) <= 128 and
         path != Path(path.anchor), "ABSOLUTE_NONROOT_PATH")
    # This kit targets local Windows drives, not UNC/device namespaces.
    need(not str(path).startswith(("\\\\", "//")), "LOCAL_PATH")
    if path.drive:
        need(re.fullmatch(r"[A-Za-z]:", path.drive) is not None, "LOCAL_DRIVE")
    for part in path.parts[1:]:
        need(not part.endswith((".", " ")) and not any(c in part for c in ':*?"<>|') and
             not os.path.isreserved(part), "PATH_COMPONENT")
    missing = False
    for part in (*reversed(path.parents), path):
        try:
            info = part.lstat()
        except FileNotFoundError:
            missing = True
            continue
        need(not missing and not stat.S_ISLNK(info.st_mode) and
             not (getattr(info, "st_file_attributes", 0) & 0x400), "REDIRECTED_PATH")
        if part != path or directory:
            need(stat.S_ISDIR(info.st_mode), "PATH_KIND")
        else:
            need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
    need(not existing or not missing, "MISSING_PATH")
    need(not fresh or missing, "OUTPUT_EXISTS")
    return path


def disjoint(left, right):
    need(not left.is_relative_to(right) and not right.is_relative_to(left), "PATH_OVERLAP")


class Inputs:
    def __init__(self):
        self.bytes = 0
        self.paths = []
        self.pins = []

    def read(self, value, maximum):
        path = ordinary_path(value, existing=True)
        size = path.stat().st_size
        need(0 < size <= maximum and self.bytes+size <= 40*MIB and len(self.paths) < 12, "INPUT_BOUND")
        with path.open("rb") as stream:
            raw = stream.read(maximum+1)
        need(len(raw) == size, "INPUT_CHANGED")
        self.bytes += size
        self.paths.append(path)
        self.pins.append(dict(path=str(path), bytes=size, sha256=digest(raw)))
        return raw

    def json(self, raw):
        # Limit nesting before the decoder allocates recursive containers.
        depth, quoted, escaped = 0, False, False
        for byte in raw:
            if quoted:
                if escaped:
                    escaped = False
                elif byte == 92:
                    escaped = True
                elif byte == 34:
                    quoted = False
            elif byte == 34:
                quoted = True
            elif byte in (91, 123):
                depth += 1
                need(depth <= 64, "JSON_DEPTH")
            elif byte in (93, 125):
                depth -= 1
                need(depth >= 0, "JSON_DEPTH")
        need(not quoted and depth == 0, "JSON_UNTERMINATED")
        def pairs(items):
            result = {}
            for key, value in items:
                need(key not in result, "JSON_DUPLICATE_KEY")
                result[key] = value
            return result
        def constant(_):
            raise ValueError("KIT_JSON_NONFINITE")
        def number(text):
            value = float(text)
            need(math.isfinite(value), "JSON_NONFINITE")
            return value
        return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                          parse_constant=constant, parse_float=number)

    def ref(self, ref, maximum=16*MIB):
        fields(ref, {"path", "sha256"})
        expected = identifier(ref["sha256"])
        raw = self.read(ref["path"], maximum)
        need(digest(raw) == expected, "INPUT_PIN")
        return self.json(raw), raw

    def report(self, ref, operation):
        report, _ = self.ref(ref)
        allowed = (operation,) if type(operation) is str else operation
        need(type(report) is dict and report.get("ok") is True and
             report.get("operation") in allowed and report.get("profile_sha256") == PROFILE and
             type(report.get("result")) is dict and not report.get("close_errors") and
             not report.get("final_budget_error") and not report["result"].get("cleanup_errors"),
             "SUCCESSFUL_SELECTED_REPORT_REQUIRED")
        return report


def contacts(value):
    need(type(value) is dict and 1 <= len(value) <= 64, "CONTACTS")
    for label, row in value.items():
        need(len(string(label).encode("utf-8")) <= 128, "CONTACT_LABEL")
        fields(row, {"host", "port", "tls", "server_name", "ca_file", "ca_sha256"})
        address = ipaddress.ip_address(string(row["host"]))
        need(not address.is_unspecified and not address.is_multicast, "CONTACT_ADDRESS")
        integer(row["port"], 1, 65535)
        need(type(row["tls"]) is bool and (row["tls"] or address.is_loopback), "REMOTE_TLS_REQUIRED")
        if row["tls"] and row["server_name"] is not None:
            need(len(string(row["server_name"])) <= 253 and
                 all(33 <= ord(c) < 127 for c in row["server_name"]), "SERVER_NAME")
        elif not row["tls"]:
            need(row["server_name"] is None and row["ca_file"] is None, "CLEAR_CONTACT_TLS_FIELDS")
        need((row["ca_file"] is None) == (row["ca_sha256"] is None), "CA_PIN_PAIR")
        if row["ca_file"] is not None:
            ordinary_path(row["ca_file"], existing=True)
            identifier(row["ca_sha256"])
    return value


def access_pairs(value):
    if value is None:
        return value  # Explicit null, like omission, selects the product default.
    fields(value, {"pairs", "limits"})
    pairs = sequence(value["pairs"], 8)
    normalized = []
    for pair in pairs:
        need(type(pair) is list and len(pair) == 2, "ACCESS_PAIR")
        left, right = identifier(pair[0]), identifier(pair[1])
        need(left < right, "ACCESS_PAIR_ORDER")
        normalized.append((left, right))
    need(normalized == sorted(set(normalized)), "ACCESS_PAIRS_ORDER")
    limits(value["limits"], dict(max_rows=(1, 16000000), max_logical_bytes=(1024, 2**40)))
    need(len(canonical(value)) <= 4096, "ACCESS_CONFIG_BYTES")
    return value


def index(value, paths):
    optional = {"access_pairs"} if type(value) is dict and "access_pairs" in value else set()
    fields(value, {"path", "limits", "create"} | optional)
    if optional:
        access_pairs(value["access_pairs"])
    need(type(value["create"]) is bool, "INDEX_CREATE")
    path = ordinary_path(value["path"], directory=True, existing=not value["create"], fresh=value["create"])
    ordinary_path(path.parent, existing=True, directory=True)
    paths.append(path)
    limits(value["limits"], INDEX)
    return value


def query_specs(value):
    """Preserve the starter's exact-symbol/kind/key subset; no product import."""
    for spec in sequence(value, 8):
        need(type(spec) is dict, "SPEC")
        if spec.get("tag") == "type-symbol":
            fields(spec, {"tag", "symbol"}); fields(spec["symbol"], {"kind", "symbol_id"})
            need(spec["symbol"]["kind"] == "portable-symbol", "SYMBOL_KIND")
            identifier(spec["symbol"]["symbol_id"])
        elif spec.get("tag") in ("object-kind", "declaration-kind", "declared-type-key"):
            fields(spec, {"tag", "value"})
            if spec["tag"] == "declared-type-key":
                identifier(spec["value"])
            else:
                allowed = {"ordinary-lean-export-v2"} if spec["tag"] == "object-kind" else {
                    "definition", "theorem", "opaque", "inductive", "constructor", "recursor"}
                need(spec["value"] in allowed, "SPEC_VALUE")
        else:
            raise ValueError("KIT_SPEC_NOT_IN_STARTER_SUBSET")
    return tuple(sorted({canonical(spec) for spec in value}))


def search_settings(value):
    keys = {"limits", "offer", "page"}
    if type(value) is dict and "candidate_mode" in value:
        keys.add("candidate_mode")
    fields(value, keys)
    if "candidate_mode" in value:
        need(type(value["candidate_mode"]) is str and value["candidate_mode"] in ("atomic-v1", "sparse-v2"),
             "CANDIDATE_MODE")
    limits(value["limits"], SEARCH)
    limits(value["offer"], dict(max_bytes=(1024, MIB), max_expanded_bytes=(1024, MIB), max_age_ms=(1, 3600000)))
    limits(value["page"], PAGE)
    return value


def advisory_endpoint(value):
    """Inert registered hint syntax, never a permission to contact its host."""
    fields(value, {"host", "port", "tls", "server_name"})
    address = ipaddress.IPv4Address(string(value["host"]))
    need(str(address) == value["host"], "CONTACT_CANONICAL_IPV4")
    server_name = value["server_name"]
    if server_name is not None:
        need(type(server_name) is str and 1 <= len(server_name) <= 253 and server_name == server_name.lower() and
             all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
                 for label in server_name.split(".")), "CONTACT_TLS_NAME")
    contacts({"hint": {**value, "ca_file": None, "ca_sha256": None}})
    return canonical(value)


def egress(value):
    fields(value, {"schema", "mode", "public_ports", "test_endpoints"})
    need(value["schema"] == "DMKN_V5_OWNER_EGRESS_V1" and
         value["mode"] in ("public-ipv4", "loopback-test"), "EGRESS_SCHEMA")
    ports = sequence(value["public_ports"], 16, empty=True)
    for port in ports:
        integer(port, 1, 65535)
    need(ports == sorted(set(ports)), "EGRESS_PORT_ORDER")
    pairs = []
    for row in sequence(value["test_endpoints"], 16, empty=True):
        fields(row, {"host", "port"})
        need(row["host"] == "127.0.0.1", "EGRESS_TEST_LOOPBACK_ONLY")
        pairs.append((row["host"], integer(row["port"], 1, 65535)))
    need(pairs == sorted(set(pairs)), "EGRESS_TEST_ORDER")
    need((value["mode"] == "public-ipv4" and ports and not pairs) or
         (value["mode"] == "loopback-test" and pairs and not ports), "EGRESS_MODE")
    return value


def service_settings(request, paths):
    address = ipaddress.ip_address(string(request["host"]))
    need(not address.is_unspecified and not address.is_multicast, "SERVE_ADDRESS")
    integer(request["port"], 0, 65535)
    integer(request["lease_seconds"], 1, 3600)
    integer(request["cleanup_seconds"], 10, 60)
    limits(request["limits"], dict(max_connections=(1, 8), max_requests=(1, 1000000),
                                  max_reply_bytes=(1024, 2**40), operation_ms=(1, 60000)))
    if request["tls"] is None:
        need(address.is_loopback, "REMOTE_TLS_REQUIRED")
    else:
        fields(request["tls"], {"cert_file", "cert_sha256", "key_file", "key_sha256"})
        for prefix in ("cert", "key"):
            paths.append(ordinary_path(request["tls"][prefix+"_file"], existing=True))
            identifier(request["tls"][prefix+"_sha256"])
    return {key: request[key] for key in SERVICE_KEYS}


def report_state(report, state):
    need(all(report.get(key) == state[key] for key in state), "REPORT_STATE_MISMATCH")


def completed_intake(result):
    need(type(result) is dict and result.get("status") == "BASELINE_INTAKE_COMPLETE", "COMPLETE_INTAKE")
    identifier(result.get("manifest_sha256"))
    identifier(result.get("selected_root"))
    root = identifier(result.get("local_root"))
    batches = sequence(result.get("batches"), 64)
    for position, batch in enumerate(batches):
        fields(batch, {"batch", "status", "local_root", "units_checked"})
        need(type(batch["batch"]) is int and batch["batch"] == position and
             batch["status"] in ("CHECKED", "REUSED"), "INTAKE_BATCH_STATUS")
        identifier(batch["local_root"])
        integer(batch["units_checked"], 0, 1024)
    need(batches[-1]["local_root"] == root, "INTAKE_FINAL_ROOT")
    return root


def parent(inputs, ref, state):
    raw, _ = inputs.ref(ref)
    operation = raw.get("operation") if type(raw) is dict else None
    need(operation in ("init", "intake-baseline", "receive"), "PARENT_OPERATION")
    need(raw.get("ok") is True and raw.get("profile_sha256") == PROFILE and
         not raw.get("close_errors") and not raw.get("final_budget_error"), "PARENT_SUCCESS")
    report_state(raw, state)
    result = raw.get("result")
    need(type(result) is dict and not result.get("cleanup_errors"), "PARENT_RESULT")
    if operation == "init":
        need(result.get("status") == "INITIALIZED_LOCAL_OWNER" and
             type(result.get("basis")) is dict and
             result["basis"].get("status") == "CHECKED", "PARENT_INITIALIZED")
        root = result["basis"].get("local_root")
    elif operation == "intake-baseline":
        root = completed_intake(result)
    else:
        admission = result.get("admission")
        need(result.get("status") in ("CHECKED", "REUSED_LOCAL_ACCEPTANCE") and
             result.get("local_acceptance_available") is True and type(admission) is dict and
             admission.get("status") in ("CHECKED", "REUSED"), "PARENT_CHECKED_RECEIVE")
        root = admission.get("local_root")
    return identifier(root)


def selected_match(inputs, request):
    # The original operation and report bytes remain unchanged and hash-pinned.
    # Learned contact hints are deliberately not inspected or adopted here.
    report = inputs.report(request["find_report"], ("find", "directory-find"))
    result = report["result"]
    need(result.get("status") == "INCOMPLETE_SEARCH" and
         result.get("operation") == report["operation"], "FIND_STATUS_OR_OPERATION")
    matches = sequence(result.get("matches"), 256)
    selected = matches[integer(request["match_index"], 0, len(matches)-1)]
    fields(selected, {"provider", "snapshot_id", "record"})
    need(selected["provider"] in request["contacts"], "SELECTED_CONTACT")
    identifier(selected["snapshot_id"])
    record = selected["record"]
    fields(record, {"schema", "namespace", "kind", "object_id", "object_sha256", "object_bytes", "features", "locator"})
    need(record["schema"] == "DMKN_FORMAL_FEATURE_RECORD_V3" and record["kind"] == "ordinary-lean-export-v2",
         "ORDINARY_RECORD")
    for key in ("object_id", "object_sha256", "namespace"):
        identifier(record.get(key))
    integer(record.get("object_bytes"), 1, MIB)
    features = sequence(record["features"], 128)
    for feature in features:
        identifier(feature)
    need(features == sorted(set(features)), "FEATURE_ORDER")
    locator = record["locator"]
    fields(locator, {"schema", "semantic_id", "unit_id", "export_name"})
    need(locator["schema"] == "DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2" and
         record["object_id"] == export_identity(locator["semantic_id"], locator["unit_id"], locator["export_name"]),
         "LOCATOR_EXPORT_BINDING")
    need(len(canonical(record)) <= 16384, "RECORD_BOUND")
    return selected


def producer(inputs, ref):
    report = inputs.report(ref, "produce-baseline")
    result = report["result"]
    need(result.get("status") == "PRODUCED_INERT_BASELINE_NOT_ACCEPTED" and
         report.get("mathematical_acceptance") is False and
         result.get("mathematical_acceptance") is False, "PRODUCER_COMPLETE_INERT")
    fields(result.get("manifest"), {"bytes", "sha256"})
    integer(result["manifest"]["bytes"], 1, 2*MIB)
    identifier(result["manifest"]["sha256"])
    identifier(result.get("semantic_id"))
    for target in sequence(result.get("targets"), 1024):
        fields(target, {"name", "export_id", "unit_id"})
        name(target["name"])
        identifier(target["export_id"])
        identifier(target["unit_id"])
        need(target["export_id"] == export_identity(result["semantic_id"], target["unit_id"], target["name"]),
             "PRODUCER_EXPORT_BINDING")
    return result


def prepare(request_path: Path, output_path: Path):
    inputs = Inputs()
    request = inputs.json(inputs.read(request_path, MIB))
    need(type(request) is dict and type(request.get("action")) is str, "ACTION")
    action = request["action"]
    output = ordinary_path(output_path, directory=True, fresh=True)
    ordinary_path(output.parent, directory=True, existing=True)
    files, paths, args = {}, [], [action]
    entry = "owner" if action in ("init", "produce-baseline", "intake-baseline") else "peer"
    state = request.get("state")
    stateful = action in ("init", "receive", "intake-baseline", "publish", "serve")
    if stateful:
        fields(state, {"catalog", "custody", "store_id"})
        identifier(state["store_id"])
        for key in ("catalog", "custody"):
            path = ordinary_path(state[key], directory=True, existing=action != "init", fresh=action == "init")
            ordinary_path(path.parent, existing=True, directory=True)
            paths.append(path)
            args += ["--"+key, state[key]]
        disjoint(paths[0], paths[1])
        files["custody-limits.json"] = limits(request.get("custody_limits"), CUSTODY)
        args += ["--store-id", state["store_id"], "--custody-limits", str(output/"custody-limits.json")]
    state_keys = {"state", "custody_limits"} if stateful else set()
    output_keys = set() if action in ("init", "intake-baseline") else {"operation_output"}
    if output_keys:
        path = ordinary_path(request.get("operation_output"), directory=True, fresh=True)
        ordinary_path(path.parent, existing=True, directory=True)
        paths.append(path)
        args += ["--output", request["operation_output"]]
    common = {"action"} | state_keys | output_keys
    if action == "init":
        fields(request, common)
        # State creation is the later product's task, not ours.
        need(not paths[0].exists() and not paths[1].exists(), "INIT_STATE_EXISTS")
    elif action == "find":
        optional = {"candidate_mode"} if "candidate_mode" in request else set()
        fields(request, common | {"contacts", "providers", "specs", "limits", "offer", "page"} | optional)
        contacts(request["contacts"])
        providers = sequence(request["providers"], 64)
        need(len(set(providers)) == len(providers) and all(p in request["contacts"] for p in providers), "PROVIDERS")
        query_specs(request["specs"])
        search_settings({key: request[key] for key in {"limits", "offer", "page"} | optional})
        config = {key: request[key] for key in {"contacts", "providers", "specs", "limits", "offer", "page"} | optional}
    elif action == "directory-find":
        keys = {"contacts", "directories", "specs", "routes", "directory", "egress", "search"}
        fields(request, common | keys)
        contacts(request["contacts"])
        directories = sequence(request["directories"], 8)
        need(all(type(item) is str and item in request["contacts"] for item in directories) and
             len(set(directories)) == len(directories), "DIRECTORY_SEEDS")
        wanted = set(query_specs(request["specs"]))
        routes = sequence(request["routes"], 8)
        compiled = [query_specs(route) for route in routes]
        need(len(set(compiled)) == len(compiled) and all(set(route) <= wanted for route in compiled) and
             len(routes)*len(directories) <= 32, "DIRECTORY_ROUTES")
        limits(request["directory"], DIRECTORY)
        need(request["directory"]["reply_bytes"] >= request["directory"]["max_bytes"], "DIRECTORY_REPLY_ALLOCATION")
        search_settings(request["search"])
        egress(request["egress"])
        config = {key: request[key] for key in keys}
    elif action == "directory-serve":
        fields(request, common | {"entries"} | SERVICE_KEYS)
        entries = sequence(request["entries"], 2048)
        seen = set()
        for row in entries:
            fields(row, {"specs", "endpoints"})
            key = query_specs(row["specs"])
            need(key not in seen, "DIRECTORY_DUPLICATE_KEY")
            seen.add(key)
            endpoints = [advisory_endpoint(endpoint) for endpoint in sequence(row["endpoints"], 16)]
            need(len(set(endpoints)) == len(endpoints), "DIRECTORY_DUPLICATE_ENDPOINT")
        config = dict(entries=entries, **service_settings(request, paths))
    elif action in ("preview", "receive"):
        extra = {"parent_report", "dependency_policy"} if action == "receive" else set()
        acquisition_fields = {"acquisition_sources", "attempt_timeout_ms", "finalization_reserve_ms"}
        acquisition = acquisition_fields if action == "receive" and acquisition_fields & set(request) else set()
        fields(request, common | {"contacts", "find_report", "match_index", "limits"} | extra | acquisition)
        contacts(request["contacts"])
        if acquisition:
            sources = sequence(request["acquisition_sources"], 8)
            need(all(type(item) is str and item in request["contacts"] for item in sources) and
                 len(set(sources)) == len(sources), "ACQUISITION_SOURCES")
            integer(request["attempt_timeout_ms"], 1, 60000)
            integer(request["finalization_reserve_ms"], 1, 60000)
        selected = selected_match(inputs, request)
        bounds = RECEIVE if action == "receive" else dict(requests=(1, 1), reply_bytes=(1, MIB))
        limits(request["limits"], bounds)
        config = dict(contacts=request["contacts"], selection=selected, limits=request["limits"])
        if action == "receive":
            policy = request["dependency_policy"]
            need(policy in ("selected-unit-only", "bounded-closure"), "DEPENDENCY_POLICY")
            need(request["limits"]["unit_bytes"] <= request["limits"]["total_bytes"], "RECEIVE_BYTES")
            config.update(parent_root=parent(inputs, request["parent_report"], state), dependency_policy=policy)
            config.update({key: request[key] for key in acquisition})
        else:
            need(selected["record"]["object_bytes"] <= request["limits"]["reply_bytes"], "PREVIEW_BYTES")
    elif action in ("inspect", "authoring-offers"):
        extra = {"binding_index"} if action == "inspect" else set()
        fields(request, common | {"contacts", "preview_report", "limits"} | extra)
        contacts(request["contacts"])
        report = inputs.report(request["preview_report"], "preview")["result"]
        need(report.get("status") == "PREVIEW_BOUND_NOT_ACCEPTED" and
             type(report.get("preview")) is dict and type(report.get("selection")) is dict, "PREVIEW_STATUS")
        preview, selection = report["preview"], report["selection"]
        need(preview.get("schema") == "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2" and
             selection.get("provider") in request["contacts"], "PREVIEW_PROVIDER")
        own_export = export_identity(preview.get("semantic_id"), preview.get("unit_id"), preview.get("export_name"))
        need(type(selection.get("record")) is dict and selection["record"].get("object_id") == own_export,
             "PREVIEW_EXPORT_BINDING")
        selected = dict(provider=selection["provider"])
        if action == "inspect":
            bindings = sequence(preview.get("type_bindings"), 4096)
            binding = bindings[integer(request["binding_index"], 0, len(bindings)-1)]
            need(type(binding) is list and len(binding) == 2, "TYPE_BINDING")
            selected.update(name=name(binding[0]), export_id=identifier(binding[1]))
            bounds = dict(requests=(2, 2), reply_bytes=(1, 9*MIB), locator_bytes=(1, MIB), unit_bytes=(1, 8*MIB))
            limits(request["limits"], bounds)
            need(request["limits"]["locator_bytes"]+request["limits"]["unit_bytes"] <= request["limits"]["reply_bytes"],
                 "INSPECT_BYTES")
        else:
            selected["export_id"] = own_export
            limits(request["limits"], dict(requests=(1, 1), reply_bytes=(1, 32768), max_offers=(1, 8)))
        config = dict(contacts=request["contacts"], selection=selected, limits=request["limits"])
    elif action == "produce-baseline":
        fields(request, common | {"project_search_paths", "modules", "output_names", "approve_local_project", "spool_mib"})
        need(request["approve_local_project"] is True, "EXPLICIT_LOCAL_PROJECT_APPROVAL")
        for path in sequence(request["project_search_paths"], 16):
            paths.append(ordinary_path(path, directory=True, existing=True))
        for module in sequence(request["modules"], 16):
            name(module)
            for part in module:
                need(part[0] == 0 and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", bytes(part[1]["$bytes"]).decode("utf-8")) is not None,
                     "MODULE_NAME")
        for target in sequence(request["output_names"], 1024):
            name(target)
        integer(request["spool_mib"], 144, 256)
        files["project.json"] = dict(schema="DMKN_ORDINARY_TRUSTED_PROJECT_EXTRACTION_V1",
            project_search_paths=request["project_search_paths"], modules=request["modules"])
        files["names.json"] = request["output_names"]
        args += ["--project-production", str(output/"project.json"), "--project-production-sha256",
                 digest(canonical(files["project.json"])), "--approve-local-project", "--output-names",
                 str(output/"names.json"), "--spool-mib", str(request["spool_mib"])]
    elif action == "intake-baseline":
        fields(request, common | {"parent_report", "producer_report", "bundle_directory", "manifest"})
        root = parent(inputs, request["parent_report"], state)
        produced = producer(inputs, request["producer_report"])
        manifest, raw = inputs.ref(request["manifest"], 2*MIB)
        fields(manifest, {"schema", "semantic_id", "batches"})
        need(manifest["schema"] == "DMKN_ORDINARY_BASELINE_BUNDLE_V1" and
             manifest["semantic_id"] == produced["semantic_id"] and
             produced["manifest"] == dict(bytes=len(raw), sha256=digest(raw)), "MANIFEST_BINDING")
        sequence(manifest["batches"], 64)
        bundle = ordinary_path(request["bundle_directory"], directory=True, existing=True)
        need(Path(request["manifest"]["path"]) == bundle/"manifest.json", "BUNDLE_MANIFEST_LOCATION")
        # Exact bundles may move between machines. Never follow or require the
        # producer's old output paths; the caller selected this local location.
        paths.append(bundle)
        args += ["--parent-root", root, "--bundle-directory", str(bundle), "--bundle-manifest",
                 request["manifest"]["path"], "--bundle-manifest-sha256", digest(raw)]
    elif action == "publish":
        fields(request, common | {"producer_report", "intake_report", "target_indices", "index", "max_unit_bytes", "max_total_bytes"})
        produced = producer(inputs, request["producer_report"])
        accepted = inputs.report(request["intake_report"], "intake-baseline")
        report_state(accepted, state)
        result = accepted["result"]
        root = completed_intake(result)
        need(result.get("manifest_sha256") == produced["manifest"]["sha256"], "COMPLETE_INTAKE_BINDING")
        choices = sequence(request["target_indices"], 64)
        for choice in choices:
            integer(choice, 0, len(produced["targets"])-1)
        need(len(set(choices)) == len(choices), "DUPLICATE_TARGET")
        targets = [produced["targets"][i] for i in choices]
        need(len({canonical(t["name"]) for t in targets}) == len(targets), "DUPLICATE_TARGET_NAME")
        integer(request["max_unit_bytes"], 1, 8*MIB)
        integer(request["max_total_bytes"], 1, 64*MIB)
        config = dict(index=index(request["index"], paths), context_root=root, targets=targets,
                      max_unit_bytes=request["max_unit_bytes"], max_total_bytes=request["max_total_bytes"])
    elif action == "serve":
        fields(request, common | {"index", "share_all_custody", "exclusive"} | SERVICE_KEYS)
        need(request["share_all_custody"] is True and request["exclusive"] is True, "EXPLICIT_WHOLE_CUSTODY_DISCLOSURE")
        index(request["index"], paths)
        need(request["index"]["create"] is False, "SERVE_EXISTING_INDEX")
        config = dict(index=request["index"], share_all_custody=True, exclusive=True,
                      **service_settings(request, paths))
    else:
        raise ValueError("KIT_UNSUPPORTED_ACTION")
    if entry == "peer":
        files["config.json"] = config
        args += ["--config", str(output/"config.json"), "--config-sha256", digest(canonical(config))]
    # Report-contained paths are never followed. All paths above came from the
    # explicit request. Keep kit writes out of inputs, operation outputs/state.
    for path in (*inputs.paths, *paths):
        disjoint(output, path)
    # Only operational directories need pairwise separation. Project search
    # paths may intentionally share an ancestor; their explicit output may not.
    if action != "produce-baseline":
        for i, path in enumerate(paths):
            for other in paths[i+1:]:
                disjoint(path, other)
    else:
        for path in paths[1:]:
            disjoint(paths[0], path)
    files["arguments.json"] = dict(entry=entry, arguments=args, profile_sha256=PROFILE,
        requires_launcher=True, mathematical_acceptance=False,
        authority="INERT_LOCAL_PREPARATION_PRODUCT_RECHECKS_STATE_AND_MATHEMATICS")
    encoded = {key: canonical(value) for key, value in files.items()}
    need(sum(map(len, encoded.values())) <= 4*MIB, "OUTPUT_BOUND")
    receipt = dict(schema="DMKN_OPERATOR_KIT_PREPARATION_V1", action=action, profile_sha256=PROFILE,
        inputs=inputs.pins, files={key: dict(bytes=len(raw), sha256=digest(raw)) for key, raw in encoded.items()},
        mathematical_acceptance=False, commands_executed=0, protected_state_opened=False,
        note="PUBLIC_REPORTS_ARE_UNTRUSTED_CONVENIENCE_NOT_AUTHENTICATION_OR_WARRANTS")
    # Fail before the first write for every validation error. OS failures later
    # preserve partial output; nothing deletes, overwrites, retries or rolls back.
    ordinary_path(output, directory=True, fresh=True)
    output.mkdir()
    for filename, raw in encoded.items():
        with (output/filename).open("xb") as stream:
            stream.write(raw)
    with (output/"RECEIPT.json").open("xb") as stream:
        stream.write(canonical(receipt))
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(canonical(prepare(args.request, args.output)).decode("utf-8"))


if __name__ == "__main__":
    main()
