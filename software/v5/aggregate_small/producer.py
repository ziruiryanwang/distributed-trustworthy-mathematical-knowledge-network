"""Bounded po18 aggregate stage orchestration, never mathematical admission.

Compose the retained pinned loader and pure helpers only. No legacy module
workflow, guest execution, automatic retry, funding, build or receipt promotion.
The owner must reserve/record this controller externally, including constructor
and preflight refusal and final-report/exit tails. Saved JSON is bookkeeping,
not a tamper-proof budget ledger or cryptographic authority.
"""
from __future__ import annotations

import math
import os
from pathlib import Path
import re
import struct
import subprocess
import time

from production import producer as P

MIB = P.MIB
require, fields, uint, number = P.require, P.fields, P.uint, P.number
digest, parse, encoded, hash_bytes = P.digest, P.parse, P.encoded, P.hash_bytes
pin_fields, file_pin = P.pin_fields, P.file_pin
PREFIX = "DMKN_V5_SMALL_AGGREGATE_PRODUCER_"
SOURCE_NAMES = ("producer.py", "__init__.py")
FILE_LIMIT = 64*MIB
CAPSULE_LIMIT = 96*MIB
PARENT_LIMIT = MIB
ARTIFACT_LIMIT = MIB//2
LOG_LIMIT = 64*1024
SEGMENT_LIMIT, ASSUMPTION_LIMIT = 256, 8
HOST_CALL_LIMIT = 3*SEGMENT_LIMIT+ASSUMPTION_LIMIT
CHECKPOINT_LIMIT = HOST_CALL_LIMIT-1
READ_LIMIT = 512*MIB
FIXED_INPUT_LIMIT = 20*MIB
ADMIN_LIMIT = 128*MIB
ADMIN_RECORD_LIMIT = 64*1024
MANIFEST_LIMIT = 256*1024
MANIFEST_LIMITS = {"segment": 2*1024, "lift": 4*1024, "join": 6*1024,
                   "resolve": 4*1024, "finish": MANIFEST_LIMIT}
MANIFEST_SCHEMA = "DMKN_AGGREGATE_DEPENDENCIES_V1"
STAGE_CEILINGS = {"segment": (1200, 240), "lift": (250, 150),
                  "join": (250, 150), "resolve": (600, 600), "finish": (300, 120)}
TAIL_BYTES, TAIL_ENTRIES = 2*MIB, 2
STAGE_FIELDS = {"cpu_seconds", "wall_seconds", "memory_mib", "active_processes",
                "stdout_bytes", "stderr_bytes", "output_bytes"}
ATTEMPT_FIELDS = {
    "schema", "status", "profile_id", "session_id", "allowance_id", "budget",
    "prior_attempts", "carried_external_costs", "worker_cpu_charge_this_attempt",
    "closure_accounting_known", "host_calls_attempted", "prover_stages_attempted",
    "reported_proof_stage_calls", "guest_execute_calls", "mathematical_admission",
    "application_receipt_created", "stages", "retained_checkpoints",
    "final_binding_validated", "control_documents", "authority", "error",
    "final_binding_error", "receipt", "controller_cpu_seconds", "wall_seconds",
    "prior_allowance_worker_charge", "prior_allowance_controller_cpu",
    "prior_allowance_wall", "prior_allowance_output_charge",
    "prior_allowance_entry_charge", "output_charge_this_attempt",
    "entry_charge_this_attempt", "accounting", "measurement_exclusions", "full_path_envelope"}


def stage_key(kind, index):
    require(kind in P.KINDS, "STAGE_KIND")
    uint(index, SEGMENT_LIMIT-1)
    require((kind != "finish" or index == 0)
            and (kind != "resolve" or index < ASSUMPTION_LIMIT)
            and (kind != "join" or index >= 1), "STAGE_INDEX")
    return kind+":"+str(index)


def split_key(key):
    require(type(key) is str and len(key) <= 16 and key.count(":") == 1, "STAGE_KEY")
    kind, text = key.split(":")
    require(text.isascii() and text.isdecimal(), "CANONICAL_STAGE_INDEX")
    index = int(text)
    require(stage_key(kind, index) == key, "CANONICAL_STAGE_KEY")
    return kind, index


def graph(segments, assumptions):
    """Same ordered complete-composite DAG, with explicit finite N256/M8."""
    uint(segments, SEGMENT_LIMIT, 1); uint(assumptions, ASSUMPTION_LIMIT)
    result = []
    for index in range(segments):
        result.append((stage_key("segment", index), ()))
        result.append((stage_key("lift", index), (stage_key("segment", index),)))
        if index:
            left = stage_key("lift", 0) if index == 1 else stage_key("join", index-1)
            result.append((stage_key("join", index), (left, stage_key("lift", index))))
    prefix = stage_key("lift", 0) if segments == 1 else stage_key("join", segments-1)
    for index in range(assumptions):
        result.append((stage_key("resolve", index), (prefix,)))
        prefix = stage_key("resolve", index)
    result.append(("finish:0", tuple(stage_key("segment", i) for i in range(segments))+(prefix,)))
    require(len(result) == 3*segments+assumptions <= HOST_CALL_LIMIT, "BOUNDED_STAGE_GRAPH")
    return result


def missing_plan(segments, assumptions, available):
    nodes = graph(segments, assumptions); edges = dict(nodes)
    require(set(available) <= set(edges)-{"finish:0"}, "CHECKPOINT_OUTSIDE_GRAPH")
    required, pending = set(), ["finish:0"]
    while pending:
        key = pending.pop()
        if key in available or key in required:
            continue
        required.add(key)
        require(len(required) <= HOST_CALL_LIMIT, "FINITE_STAGE_WALK")
        pending.extend(reversed(edges[key]))
    return [(key, dependencies) for key, dependencies in nodes if key in required]


def dependency_manifest(session, key, dependencies):
    """Exact host-consumed dependency data, never proof or mathematical authority."""
    kind, _ = split_key(key)
    edges = dict(graph(session["segments"], session["assumptions"]))
    require(key in edges and type(dependencies) is list
            and len(dependencies) <= SEGMENT_LIMIT+1, "MANIFEST_STAGE_OR_COUNT")
    for row in dependencies:
        fields(row, ("key", "file"))
        split_key(row["key"])
        path = pin_fields(row["file"], ARTIFACT_LIMIT)
        require(len(str(path).encode("utf-16-le"))//2 <= 512
                and "\0" not in str(path), "MANIFEST_PATH_BOUND")
    require(tuple(row["key"] for row in dependencies) == edges[key], "EXACT_ORDERED_DEPENDENCIES")
    digest(session["session_binding"]); digest(session["capsule_binding"])
    value = {"schema": MANIFEST_SCHEMA, "session_binding": session["session_binding"],
             "capsule_binding": session["capsule_binding"], "stage": key,
             "dependencies": dependencies}
    require(len(encoded(value)) <= MANIFEST_LIMITS[kind], "MANIFEST_BYTE_LIMIT")
    return value


def content(pin):
    pin_fields(pin)
    return {k: pin[k] for k in ("bytes", "sha256")}


def header(raw, support, relation_image):
    """Structural v2 binding only; native relation/receipt checks are authoritative."""
    require(len(raw) == 192 and raw[:12] == b"DMKNA002\x02\0\0\0", "AGGREGATE_HEADER_V2")
    require(raw[12:44].hex() == support["image_id"]
            and raw[44:76].hex() == relation_image
            and raw[76:108].hex() == support["foundation"]
            and raw[108:140].hex() == support["policy"], "AGGREGATE_HEADER_PROFILE")
    require(support["image_id"] not in ("0"*64, relation_image), "DISTINCT_AGGREGATE_IMAGE")
    uint(int.from_bytes(raw[172:176], "little"), 48, 1)
    require(int.from_bytes(raw[184:192], "little") > 0, "POSITIVE_SEAL_HEIGHT")


def checkpoint_header(raw, byte_count, binding, key):
    """Unauthenticated 71-byte maximum envelope, not SDK payload verification."""
    require(len(raw) >= 52 and raw[:12] == b"DMKNAP01\x01\0\0\0", "AGGREGATE_CHECKPOINT_V1")
    require(raw[12:44].hex() == binding, "CHECKPOINT_CAPSULE_BINDING")
    n = struct.unpack_from("<Q", raw, 44)[0]
    require(1 <= n <= 7 and len(raw) >= 64+n, "CHECKPOINT_HEADER_EXTENT")
    kind = raw[52:52+n].decode("ascii")
    index = struct.unpack_from("<I", raw, 52+n)[0]
    payload = struct.unpack_from("<Q", raw, 56+n)[0]
    require(kind in P.KINDS[:-1] and stage_key(kind, index) == key
            and payload > 0 and 64+n+payload == byte_count, "CHECKPOINT_LAYOUT_OR_KEY")


def stage_output(raw, key, session, support, artifact, manifest, dependencies):
    """Exact single JSON object; bool is deliberately not accepted as integer."""
    result = parse(raw)
    kind, index = key.split(":")
    finish = kind == "finish"
    expected = {
        "schema": "DMKN_SMALL_AGGREGATE_PROOF_STAGE_V1",
        "status": "REAL_AGGREGATE_RECEIPT_FINISHED" if finish else
                  "REAL_AGGREGATE_CHECKPOINT_NOT_APPLICATION_RECEIPT",
        "kind": kind, "index": int(index), "aggregate_image": support["image_id"],
        "header_sha256": session["expected"]["sha256"],
        "capsule_binding": session["capsule_binding"],
        "session_binding": session["session_binding"], "segments": session["segments"],
        "assumptions": session["assumptions"], "output_bytes": artifact["bytes"],
        "output_sha256": artifact["sha256"], "application_receipt_created": finish,
        "guest_execute_calls": 0, "proof_stage_calls": 0 if finish else 1,
        "mathematical_admission": False,
        "dependency_manifest": manifest, "dependency_keys": list(dependencies)}
    fields(result, expected)
    pin_fields(result["dependency_manifest"], MANIFEST_LIMITS[kind])
    require(type(result["dependency_keys"]) is list
            and all(type(x) is str for x in result["dependency_keys"]), "DEPENDENCY_KEY_TYPES")
    require(all(type(result[k]) is type(v) and result[k] == v for k, v in expected.items()),
            "EXACT_AGGREGATE_STAGE_OUTPUT")
    return result


def stage_argv(host, adopted_image, session, key, artifact, manifest):
    kind, index = key.split(":")
    pin_fields(manifest, MANIFEST_LIMITS[kind])
    argv = [host, "stage-manifest", adopted_image, session["image"]["path"],
            session["wire"]["path"], session["expected"]["path"],
            str(session["cycles"]), str(session["po2"]), kind, index, str(artifact),
            str(len(session["parents"])), *[p["path"] for p in session["parents"]],
            session["capsule"]["path"], manifest["path"], str(manifest["bytes"]), manifest["sha256"]]
    require(len(argv) == 16+len(session["parents"])
            and all(type(x) is str and "\0" not in x for x in argv), "MANIFEST_ARGV_SHAPE")
    require(len(subprocess.list2cmdline(argv).encode("utf-16-le"))//2+1 <= 32767,
            "WINDOWS_COMMAND_LINE_LIMIT")
    return argv


class AggregateProducer:
    """One finite owner. Profiles/requests are local decisions, never peer data.

    Profile: schema, support_profile (retained Producer loader profile),
    source_pins (this package's two files), relation_image, host_build,
    image_adoption and explicit stage_memory_ceiling_mib. host_build contains
    pinned result/attempt/selection/
    source_map/command records. image_adoption contains pinned result/outer/
    selection/guest_build/guest_selection/guest_source_map/artifact records. These are actual
    selected build formats, not invented replacement adoption reports.

    Every stage budget explicitly chooses all STAGE_FIELDS below retained
    ceilings. output_bytes includes all retained attempts on the allowance;
    per-stage output_bytes is the selected artifact bound. Conservative final
    report/sentinel space stays charged. External costs remain separately
    disclosed, not added twice to nested inclusive Job measurements.
    """
    def __init__(self, profile):
        fields(profile, ("schema", "support_profile", "source_pins", "relation_image",
                         "host_build", "image_adoption", "stage_memory_ceiling_mib"))
        require(profile["schema"] == PREFIX+"PROFILE_V1", "PROFILE_SCHEMA")
        uint(profile["stage_memory_ceiling_mib"], 8192, 1)
        require(len(encoded(profile)) <= MIB, "PROFILE_BYTES")
        self.profile = parse(encoded(profile))
        self._raw = encoded(self.profile)
        self.profile_id = hash_bytes(self._raw)
        self._closed = False; self._busy = False; self._attempt_open = False
        self._history = {}; self._last_call_failure = None
        self._support = P.Producer(self.profile["support_profile"])
        self._A, self._Job, self._install = self._support._A, self._support._Job, self._support._install
        supervisor_memory = self._A.CEILINGS["memory_mib"]
        require(type(supervisor_memory) is int
                and self.profile["stage_memory_ceiling_mib"] <= supervisor_memory,
                "ADOPTED_SUPERVISOR_MEMORY_CEILING")
        self._pins = dict(self._support._pins)
        digest(self.profile["relation_image"])
        sources = self.profile["source_pins"]
        require(type(sources) is list and len(sources) == 2, "EXACT_AGGREGATE_SOURCES")
        require({pin_fields(p) for p in sources} ==
                {Path(__file__).resolve().parent/n for n in SOURCE_NAMES}, "ACTUAL_AGGREGATE_SOURCE_PATHS")
        for pin in sources:
            self._add(self._pins, pin)
        self._adopt_build()
        self._adopt_image()
        require(sum(p["bytes"] for p in self._pins.values()) <= READ_LIMIT, "INSTALLATION_BYTE_ENVELOPE")
        self._check(self._pins)

    @property
    def support(self):
        return self.profile["support_profile"]

    def _add(self, table, pin, maximum=128*MIB):
        pin_fields(pin, maximum)
        for existing in (self._pins, table):
            require(pin["path"] not in existing or existing[pin["path"]] == pin, "CONFLICTING_ROLE_PIN")
        table[pin["path"]] = dict(pin)

    def _check(self, pins):
        require(encoded(self.profile) == self._raw, "AGGREGATE_PROFILE_MUTATED")
        self._support._check(pins)

    def _read(self, pin, maximum=MIB):
        return self._support._read(pin, maximum)

    def _records(self, container, names, table):
        fields(container, names)
        result = {}
        for name in names:
            self._add(table, container[name], 2*MIB)
            result[name] = parse(self._read(container[name], 2*MIB))
        return result

    def _no_override(self, pins):
        for pin in pins:
            path = Path(pin["path"]).parent / "FINALIZATION-FAILED.json"
            require(not path.exists(), "FINALIZATION_OVERRIDE")

    def _local_outer(self, outer, selection, selection_pin, outer_pin):
        fields(outer, ("authority", "result", "runtime_scope", "schema", "selection_sha256",
                       "wall_seconds", "wrapper_cpu_seconds"))
        fields(selection, ("schema", "name", "sources", "runtime_pins", "argv", "limits"))
        require(outer["schema"] == "DMKN_V5_LOCAL_CHECK_RESULT_V1"
                and selection["schema"] == "DMKN_V5_LOCAL_CHECK_V1"
                and outer["selection_sha256"] == selection_pin["sha256"]
                and P.clean(outer["result"]), "ADOPTED_CLEAN_OUTER_SELECTION")
        require(outer["result"]["limits"] == selection["limits"], "OUTER_SELECTED_LIMITS")
        argv = selection["argv"]
        require(type(argv) is list and all(type(x) is str for x in argv), "OUTER_SELECTED_ARGV")
        output = Path(outer_pin["path"]).parent
        snapshot = str(output/"sources")
        # Match Run-V5-Check.py's ordered literal substitutions exactly.
        # It expands {snapshot}, then {output}; it does not expand {root}.
        selected_argv = [x.replace("{snapshot}", snapshot).replace("{output}", str(output)) for x in argv]
        require(outer["result"]["argv"] == selected_argv,
                "OUTER_EXACT_SELECTED_ARGV")
        number(outer["wall_seconds"]); number(outer["wrapper_cpu_seconds"])

    def _adopt_build(self):
        host = self._adopt_host_build(self.profile["host_build"], self._pins, "stage")
        require(host == self.support["host"], "ADOPTED_STAGE_HOST_EXECUTABLE")

    def _adopt_host_build(self, pins, table, role):
        require(role in ("stage", "snapshot"), "HOST_BUILD_ROLE")
        r = self._records(pins, ("result", "attempt", "selection", "source_map", "command"), table)
        result, selection = r["result"], r["selection"]
        fields(result, ("schema", "status", "selection_sha256", "limits", "retained_command_sha256",
                        "retained_result_sha256", "runtime_pin_count", "runtime_pin_bytes", "backend_rebuilds",
                        "relation_rebuilds", "checker_rebuilds", "host_calls", "guest_calls", "proof_calls",
                        "network_calls", "authority", "executable", "job", "commands", "controller_cpu_seconds",
                        "wall_seconds", "output_census", "sampled_peaks", "accounting"))
        fields(selection, ("schema", "name", "authorizes_compile_only", "sources", "runtime_pins", "limits"))
        schema = "DMKN_V5_SMALL_AGGREGATE_"+role.upper()+"_HOST_BUILD"
        require(selection["schema"] == schema+"_V1"
                and selection["authorizes_compile_only"] is True
                and result["schema"] == schema+"_RESULT_V1"
                and result["status"] == "PASS_SMALL_AGGREGATE_"+role.upper()+"_HOST_ONE_LINK_ONLY"
                and result["selection_sha256"] == pins["selection"]["sha256"]
                and result["limits"] == selection["limits"], "ADOPTED_SMALL_HOST_BUILD")
        fields(r["attempt"], ("status", "result_sha256"))
        require(r["attempt"] == {"status": result["status"], "result_sha256": pins["result"]["sha256"]}
                and result["job"]["active_processes"] == result["job"]["terminated_processes"] == 0
                and len(result["commands"]) == 1 and result["commands"][0]["argv"] == r["command"]
                and r["source_map"] == selection["sources"], "BUILD_RECORD_CHAIN")
        command_record = result["commands"][0]
        require(command_record["status"] == "COMMAND_COMPLETED" and command_record["exit_code"] == 0
                and command_record["cleanup_errors"] == [], "BUILD_COMMAND_CLEAN_COMPLETION")
        for name in ("backend_rebuilds", "relation_rebuilds", "checker_rebuilds", "host_calls",
                     "guest_calls", "proof_calls", "network_calls"):
            require(type(result[name]) is int and result[name] == 0, "BUILD_SCOPE")
        source = "stage_host.rs" if role == "stage" else "aggregate_host.rs"
        expected = {"software/v5/aggregate_small/build_"+role+".py",
                    "software/v5/aggregate_small/"+source, "software/v5/aggregate/receipt.rs"}
        fields(r["source_map"], expected)
        build_root = Path(pins["result"]["path"]).parent
        require(type(selection["name"]) is str
                and re.fullmatch("small-aggregate-"+role+"-host-build-[0-9]{2}", selection["name"])
                and build_root.name == selection["name"], "EXACT_SMALL_BUILD_NAME")
        for relative, pin in r["source_map"].items():
            fields(pin, ("bytes", "sha256"))
            self._add(table, {"path": str(build_root/"source"/relative), **pin}, MIB)
        host = result["executable"]
        pin_fields(host, 128*MIB if role == "stage" else 8*MIB)
        executable = "small_aggregate_stage_host.exe" if role == "stage" else "small_aggregate_host.exe"
        require(host["path"] == str(build_root/executable), "SMALL_BUILD_EXECUTABLE_PATH")
        self._add(table, host, 128*MIB if role == "stage" else 8*MIB)
        command = r["command"]
        require(type(command) is list and all(type(x) is str for x in command)
                and command.count(str(build_root/"source/software/v5/aggregate_small"/source)) == 1
                and command.count(host["path"]) == 1, "EXACT_BUILD_COMMAND_OUTPUT_SOURCE")
        self._no_override(pins.values())
        return host

    def _adopt_image(self):
        pins = self.profile["image_adoption"]
        r = self._records(pins, ("result", "outer", "selection", "guest_build", "guest_selection",
                                "guest_source_map", "artifact"), self._pins)
        self._local_outer(r["outer"], r["selection"], pins["selection"], pins["outer"])
        result = r["result"]
        fields(result, ("artifact_record", "assembler_calls", "authority", "exit_code", "guest_build_result",
                        "guest_executions", "image", "image_id", "image_id_origin", "logs",
                        "mathematical_admission", "proof_calls", "schema", "selection_sha256", "status"))
        require(result["schema"] == "DMKN_V5_PROOF_MEMO_IMAGE_ASSEMBLY_RESULT_V1"
                and result["status"] == "PASS_NEW_AGGREGATE_IMAGE_ASSEMBLY_ONLY"
                and result["image_id"] == self.support["image_id"]
                and type(result["assembler_calls"]) is int and result["assembler_calls"] == 1
                and type(result["exit_code"]) is int and result["exit_code"] == 0
                and type(result["guest_executions"]) is int and result["guest_executions"] == 0
                and type(result["proof_calls"]) is int and result["proof_calls"] == 0
                and result["mathematical_admission"] is False
                and result["guest_build_result"] == pins["guest_build"]
                and result["artifact_record"] == pins["artifact"], "ADOPTED_IMAGE_ASSEMBLY")
        guest = r["guest_build"]
        fields(guest, ("accounting", "artifact", "authority", "cargo_calls", "checker_compiles", "commands",
                       "compiler_calls", "control_outer_result_sha256", "control_outer_status", "controller_cpu_seconds",
                       "dependency_compiles", "functional_control_result_sha256", "functional_controls_disposition",
                       "graph_commands", "guest_calls", "image_assembly_calls", "job", "limits", "network_calls",
                       "output_census", "outputs", "prior_build_result_sha256", "prior_source_map_sha256", "proof_calls",
                       "sampled_peaks", "schema", "selection_sha256", "source_snapshot", "status", "wall_seconds"))
        require(guest["schema"] == "DMKN_V5_PROOF_MEMO_FOUR_CRATE_BUILD_RESULT_V1"
                and guest["status"] == "PASS_PROOF_MEMO_FOUR_CRATE_COMPILES_ONLY"
                and guest["selection_sha256"] == result["selection_sha256"]
                and guest["selection_sha256"] == pins["guest_selection"]["sha256"]
                and guest["artifact"] == r["artifact"]
                and guest["job"]["active_processes"] == guest["job"]["terminated_processes"] == 0,
                "ADOPTED_GUEST_SOURCE_BUILD_CHAIN")
        outer_argv = r["outer"]["result"]["argv"]
        require(outer_argv.count("--guest-result") == outer_argv.count("--guest-result-sha256") == 1
                and outer_argv[outer_argv.index("--guest-result")+1] == pins["guest_build"]["path"]
                and outer_argv[outer_argv.index("--guest-result-sha256")+1] == pins["guest_build"]["sha256"],
                "ASSEMBLY_OUTER_EXACT_GUEST_BUILD")
        selection, sources = r["guest_selection"], r["guest_source_map"]
        fields(selection, ("schema", "name", "adapters", "production_sources", "retained_artifacts",
                           "authorizes_four_compiles_and_retained_artifact_adoption", "limits"))
        fields(sources, ("source_snapshot", "project", "compiler_read_sources", "adapters"))
        require(selection["schema"] == "DMKN_V5_PROOF_MEMO_FOUR_CRATE_BUILD_V1"
                and selection["authorizes_four_compiles_and_retained_artifact_adoption"] is True
                and sources["source_snapshot"] == guest["source_snapshot"]
                and sources["project"] == selection["production_sources"]
                and sources["adapters"] == selection["adapters"]
                and type(sources["project"]) is dict and 1 <= len(sources["project"]) <= 256
                and type(sources["compiler_read_sources"]) is dict
                and all(sources["project"].get(k) == v for k,v in sources["compiler_read_sources"].items()),
                "GUEST_SOURCE_MAP_BUILD_BINDING")
        # Source map and build are both independently owner-pinned. Source
        # correspondence is an adoption obligation, not inferred from an ELF hash.
        self._image = result["image"]
        self._add(self._pins, self._image, FILE_LIMIT)
        self._no_override(pins.values())

    def _request(self, request):
        fields(request, ("schema", "allowance_id", "session", "checkpoints", "output_directory",
                         "stage_limit", "budget", "prior_attempts", "carried_external_costs"))
        require(request["schema"] == PREFIX+"REQUEST_V1", "REQUEST_SCHEMA")
        digest(request["allowance_id"])
        require(len(encoded(request)) <= MIB, "REQUEST_BYTES")
        session = request["session"]
        fields(session, ("image", "wire", "expected", "capsule", "parents", "session_binding",
                         "capsule_binding", "cycles", "po2", "segments", "assumptions", "snapshot_evidence"))
        digest(session["session_binding"]); digest(session["capsule_binding"])
        uint(session["cycles"], 1 << 26, 1)
        require(type(session["po2"]) is int and session["po2"] == 18, "SMALL_SEGMENT_GEOMETRY")
        graph(session["segments"], session["assumptions"])
        require(type(session["parents"]) is list and len(session["parents"]) == session["assumptions"],
                "EXACT_PARENT_ASSUMPTION_COUNT")
        inputs = {}
        for name, maximum in (("image", FILE_LIMIT), ("wire", 16*MIB), ("expected", 192), ("capsule", CAPSULE_LIMIT)):
            self._add(inputs, session[name], maximum)
        require(session["image"] == self._image, "EXACT_ADOPTED_IMAGE")
        for pin in session["parents"]:
            require(pin_fields(pin, PARENT_LIMIT) not in set(map(Path, inputs)), "DUPLICATE_PARENT_PATH")
            self._add(inputs, pin, PARENT_LIMIT)
        self._check(inputs)
        expected = self._read(session["expected"], 192)
        header(expected, self.support, self.profile["relation_image"])
        with Path(session["wire"]["path"]).open("rb") as stream:
            prefix = stream.read(44)
        require(prefix[:12] == b"DMKNAI02\x02\0\0\0" and prefix[12:44] == expected[12:44], "WIRE_V2_ADOPTED_IMAGE")
        with Path(session["capsule"]["path"]).open("rb") as stream:
            prefix = stream.read(44)
        require(prefix[:12] == b"DMKNAS01\x01\0\0\0"
                and prefix[12:44].hex() == session["session_binding"], "COMPLETE_CAPSULE_SESSION_PREFIX")
        self._snapshot(session, expected, inputs)
        require(sum(pin["bytes"] for path,pin in inputs.items()
                    if path != session["capsule"]["path"]) <= FIXED_INPUT_LIMIT,
                "FIXED_SESSION_INPUT_ENVELOPE")
        rows = request["checkpoints"]
        require(type(rows) is list and len(rows) <= CHECKPOINT_LIMIT, "CHECKPOINT_COUNT")
        inventory = {}
        for row in rows:
            self._checkpoint(row, session)
            require(row["key"] not in inventory, "DUPLICATE_CHECKPOINT_KEY")
            inventory[row["key"]] = row["file"]
            self._add(inputs, row["file"], ARTIFACT_LIMIT)
        nodes = missing_plan(session["segments"], session["assumptions"], inventory)
        uint(request["stage_limit"], HOST_CALL_LIMIT, 1)
        budget = request["budget"]
        fields(budget, ("worker_cpu_seconds", "controller_cpu_seconds", "wall_seconds",
                        "output_bytes", "output_entries", "stages"))
        for key, lo, hi in (("worker_cpu_seconds", 1, 500000), ("controller_cpu_seconds", 1, 7200),
                           ("wall_seconds", 1, 172800), ("output_bytes", 4*MIB, 2304*MIB),
                           ("output_entries", 16, 8192)):
            uint(budget[key], hi, lo)
        fields(budget["stages"], P.KINDS)
        for kind, ceilings in STAGE_CEILINGS.items():
            selected = budget["stages"][kind]
            fields(selected, STAGE_FIELDS)
            uint(selected["cpu_seconds"], ceilings[0], 1)
            uint(selected["wall_seconds"], ceilings[1], 1)
            for key, maximum in P.COMMON.items():
                upper = (self.profile["stage_memory_ceiling_mib"] if key == "memory_mib"
                         else LOG_LIMIT if key in ("stdout_bytes", "stderr_bytes") else maximum)
                uint(selected[key], upper, 1)
            uint(selected["output_bytes"], ARTIFACT_LIMIT, 1)
        carried = request["carried_external_costs"]
        fields(carried, ("worker_cpu_seconds", "controller_cpu_seconds", "wall_seconds", "scope"))
        for key in ("worker_cpu_seconds", "controller_cpu_seconds", "wall_seconds"):
            number(carried[key])
        require(type(carried["scope"]) is str and 1 <= len(carried["scope"]) <= 1024, "CARRIED_SCOPE")
        # Exact profile includes all actual source/runtime/adoption pins. Session
        # content identity preserves ordered parents and adopted screen identity.
        identity = {k: session[k] for k in ("session_binding", "capsule_binding", "cycles", "po2", "segments", "assumptions")}
        identity.update({k: content(session[k]) for k in ("image", "wire", "expected", "capsule")})
        identity["parents"] = [content(pin) for pin in session["parents"]]
        identity["snapshot_evidence"] = {k: content(v) for k,v in session["snapshot_evidence"].items()}
        session_id = hash_bytes(encoded(identity))
        prior_pins = request["prior_attempts"]
        require(type(prior_pins) is list and len(prior_pins) <= 16, "PRIOR_ATTEMPT_COUNT")
        require(request["allowance_id"] not in self._history or self._history[request["allowance_id"]] == prior_pins,
                "LIVE_ALLOWANCE_HISTORY_MISSING")
        prior = [0, 0, 0, 0, 0]
        seen, prior_bytes = set(), 0
        for i, pin in enumerate(prior_pins):
            path = pin_fields(pin, MIB)
            prior_bytes += pin["bytes"]
            require(str(path) not in seen and prior_bytes <= 8*MIB, "PRIOR_LEDGER_BOUND")
            seen.add(str(path))
            old = parse(self._read(pin))
            fields(old, ATTEMPT_FIELDS)
            require(old["schema"] == PREFIX+"ATTEMPT_V1" and old["profile_id"] == self.profile_id
                    and old["session_id"] == session_id and old["allowance_id"] == request["allowance_id"]
                    and old["prior_attempts"] == prior_pins[:i] and old["budget"] == budget
                    and old["carried_external_costs"] == carried, "COMPLETE_SAME_ALLOWANCE_LINEAGE")
            require(old["status"] in ("FAIL", "PASS_SELECTED_PREFIX_ONLY")
                    and old["closure_accounting_known"] is True and old["final_binding_validated"] is True
                    and old["application_receipt_created"] is False and old["receipt"] is None
                    and not (path.parent/"FINALIZATION-FAILED.json").exists(), "PRIOR_REQUIRES_OWNER_RECOVERY")
            retained = old["retained_checkpoints"]
            require(type(retained) is list and len(retained) <= CHECKPOINT_LIMIT, "PRIOR_INVENTORY_BOUND")
            for row in retained:
                fields(row, ("key", "file"))
                pin_fields(row["file"], ARTIFACT_LIMIT)
                require(inventory.get(row["key"]) == row["file"], "PRIOR_SUCCESS_MUST_BE_RETAINED")
            for j, key in enumerate(("worker_cpu_charge_this_attempt", "controller_cpu_seconds", "wall_seconds")):
                prior[j] += number(old[key])
            prior[3] += uint(old["output_charge_this_attempt"], budget["output_bytes"])
            prior[4] += uint(old["entry_charge_this_attempt"], budget["output_entries"])
            self._add(inputs, pin, MIB)
        self._check(inputs)
        require(sum(pin["bytes"] for pin in inputs.values()) <= READ_LIMIT, "SESSION_INPUT_ENVELOPE")
        output = self._A.absolute(request["output_directory"], directory=True, fresh=True)
        for protected in [self._install, *map(Path, self._pins), *map(Path, inputs)]:
            require(not self._A.overlap(output, protected), "OUTPUT_OVERLAP")
        envelope = self._envelope(session, budget, inventory, nodes, prior)
        return session_id, inputs, inventory, nodes[:request["stage_limit"]], output, prior, envelope

    @staticmethod
    def _envelope(session, budget, inventory, nodes, prior):
        sizes = {key: pin["bytes"] for key,pin in inventory.items()}
        base = sum(session[k]["bytes"] for k in ("image", "wire", "expected", "capsule"))
        base += sum(pin["bytes"] for pin in session["parents"])
        cpu, wall, retained, entries, largest = 0, 0, 0, 0, base
        for key, dependencies in nodes:
            kind = key.split(":")[0]
            selected = budget["stages"][kind]
            largest = max(largest, base+sum(sizes[d] for d in dependencies)+MANIFEST_LIMITS[kind])
            cpu += selected["cpu_seconds"]
            wall += selected["wall_seconds"]
            retained += selected["output_bytes"]+selected["stdout_bytes"]+selected["stderr_bytes"]+2*MIB+MANIFEST_LIMIT
            entries += 9
            sizes[key] = selected["output_bytes"]
        return {"missing_host_calls": len(nodes), "missing_prover_stages": len(nodes)-1,
                "selected_worker_cpu_envelope": cpu, "new_output_envelope": retained+4*MIB,
                "selected_worker_wall_envelope": wall,
                "new_entry_envelope": entries+4, "maximum_host_read_envelope": largest,
                "existing_checkpoint_bytes": sum(pin["bytes"] for pin in inventory.values()),
                "full_path_fits_requested_envelopes":
                    prior[0]+cpu <= budget["worker_cpu_seconds"]
                    and prior[2]+wall <= budget["wall_seconds"] and largest <= READ_LIMIT
                    and prior[3]+retained+4*MIB <= budget["output_bytes"]
                    and prior[4]+entries+4 <= budget["output_entries"],
                "scope": "CONSERVATIVE_REQUEST_LIMITS_NOT_COST_PREDICTION_OR_FUNDING"}

    def run(self, request):
        require(not self._closed and not self._busy, "AGGREGATE_PRODUCER_CLOSED_OR_BUSY")
        started, cpu_started = time.monotonic(), time.process_time()
        self._busy = True; self._last_call_failure = None
        try:
            return self._run(parse(encoded(request)), started, cpu_started)
        except BaseException as error:
            self._last_call_failure = {
                "scope": "RUN_REFUSAL_OR_INTERRUPTION_OBSERVATION_NOT_DURABLE_BUDGET_LEDGER",
                "controller_cpu_seconds": time.process_time()-cpu_started,
                "wall_seconds": time.monotonic()-started, "attempt_directory_created": self._attempt_open,
                "error": type(error).__name__+": "+str(error)[:2000]}
            if self._attempt_open:
                self._closed = True
            raise
        finally:
            self._busy = False

    def _run(self, request, started, cpu_started):
        session_id, inputs, inventory, nodes, output, prior, envelope = self._request(request)
        session, budget = request["session"], request["budget"]
        require(prior[0] < budget["worker_cpu_seconds"] and prior[1] < budget["controller_cpu_seconds"]
                and prior[2] < budget["wall_seconds"] and prior[3] < budget["output_bytes"]
                and prior[4] < budget["output_entries"], "ALLOWANCE_EXHAUSTED")
        deadline = started+budget["wall_seconds"]-prior[2]
        administrative = {}

        def active():
            require(time.monotonic() <= deadline
                    and prior[1]+time.process_time()-cpu_started <= budget["controller_cpu_seconds"],
                    "ATTEMPT_DEADLINE_OR_CONTROLLER_CPU")

        def rebind():
            active()
            require(sum(pin["bytes"] for path,pin in inputs.items()
                        if path not in administrative) <= READ_LIMIT, "ACTIVE_SESSION_INPUT_ENVELOPE")
            require(sum(pin["bytes"] for pin in administrative.values()) <= ADMIN_LIMIT,
                    "ACTIVE_ADMINISTRATIVE_INPUT_ENVELOPE")
            self._check(self._pins); self._check(inputs)
            self._no_override(self.profile["host_build"].values())
            self._no_override(self.profile["image_adoption"].values())
            self._no_override(session["snapshot_evidence"].values())
            self._no_override(self._snapshot_build_pins.values())
            self._no_override(request["prior_attempts"])
            active()

        def save_admin(path, value, maximum):
            raw = encoded(value)
            require(len(raw) <= maximum, "ADMINISTRATIVE_RECORD_BOUND")
            self._A.save_new(path, value)
            pin = file_pin(path)
            require(pin["bytes"] == len(raw) and pin["sha256"] == hash_bytes(raw),
                    "EXACT_SAVED_ADMINISTRATIVE_BYTES")
            self._add(administrative, pin, maximum)
            require(sum(p["bytes"] for p in administrative.values()) <= ADMIN_LIMIT,
                    "ACTIVE_ADMINISTRATIVE_INPUT_ENVELOPE")
            self._add(inputs, pin, maximum)
            return pin

        rebind(); output.mkdir(); self._attempt_open = True
        controls = [save_admin(output/"request.json", request, MIB),
                    save_admin(output/"profile.json", self.profile, MIB)]
        report = {
            "schema": PREFIX+"ATTEMPT_V1", "status": "FAIL", "profile_id": self.profile_id,
            "session_id": session_id, "allowance_id": request["allowance_id"], "budget": budget,
            "prior_attempts": request["prior_attempts"], "carried_external_costs": request["carried_external_costs"],
            "worker_cpu_charge_this_attempt": 0, "closure_accounting_known": True,
            "host_calls_attempted": 0, "prover_stages_attempted": 0, "reported_proof_stage_calls": 0,
            "guest_execute_calls": 0, "mathematical_admission": False, "application_receipt_created": False,
            "stages": [], "retained_checkpoints": [], "final_binding_validated": False,
            "control_documents": controls, "receipt": None, "error": None, "final_binding_error": None,
            "authority": "PRODUCER_ARTIFACTS_NOT_ADMISSION_HANDLES", "full_path_envelope": envelope}

        def census(reserve=0, reserve_entries=0):
            size, count = 0, 0
            for directory, dirs, names in os.walk(output, followlinks=False):
                for name in dirs+names:
                    active(); path = Path(directory)/name
                    self._A.absolute(path, directory=name in dirs); count += 1
                    if name in names:
                        size += path.stat().st_size
                    require(prior[4]+count+reserve_entries <= budget["output_entries"], "OUTPUT_ENTRY_LIMIT")
                    require(prior[3]+size+reserve <= budget["output_bytes"], "OUTPUT_BYTE_LIMIT")
            require(prior[4]+count+reserve_entries <= budget["output_entries"]
                    and prior[3]+size+reserve <= budget["output_bytes"], "OUTPUT_RESERVATION_LIMIT")
            return size, count

        try:
            for key, dependencies in nodes:
                rebind()
                kind, index_text = key.split(":")
                selected = budget["stages"][kind]
                limits = {k:v for k,v in selected.items() if k != "output_bytes"}
                # Artifact + two logs + small command/reservation/result records;
                # preserve separate final report/sentinel space on every call.
                stage_reserve = selected["output_bytes"]+limits["stdout_bytes"]+limits["stderr_bytes"]+2*MIB+MANIFEST_LIMIT
                census(stage_reserve+TAIL_BYTES, 9+TAIL_ENTRIES)
                require(prior[0]+report["worker_cpu_charge_this_attempt"]+limits["cpu_seconds"]
                        <= budget["worker_cpu_seconds"], "NEXT_STAGE_RESERVATION_EXCEEDS_ALLOWANCE")
                limits["wall_seconds"] = min(limits["wall_seconds"], math.floor(deadline-time.monotonic()))
                require(limits["wall_seconds"] >= 1, "STAGE_DEADLINE")
                dependencies_pins = [inventory[d] for d in dependencies]
                manifest_value = dependency_manifest(session, key,
                    [{"key": dependency, "file": pin}
                     for dependency,pin in zip(dependencies, dependencies_pins)])
                require(sum(session[n]["bytes"] for n in ("image", "wire", "expected", "capsule"))
                        +sum(p["bytes"] for p in session["parents"]+dependencies_pins)
                        +len(encoded(manifest_value)) <= READ_LIMIT,
                        "HOST_TOTAL_READ_LIMIT")
                stage_dir = output/(kind+"-"+index_text); stage_dir.mkdir()
                artifact = stage_dir/("receipt.bin" if kind == "finish" else "proof.checkpoint")
                manifest_pin = save_admin(stage_dir/"dependencies.json", manifest_value, MANIFEST_LIMITS[kind])
                argv = stage_argv(self.support["host"]["path"], self.support["image_id"],
                                  session, key, artifact, manifest_pin)
                reservation = {"schema": PREFIX+"RESERVATION_V1", "profile_id": self.profile_id,
                    "session_id": session_id, "allowance_id": request["allowance_id"], "stage": key,
                    "limits": limits, "artifact_byte_limit": selected["output_bytes"], "argv": argv,
                    "dependency_manifest": manifest_pin, "dependency_keys": list(dependencies),
                    "worker_reserved": limits["cpu_seconds"],
                    "output_bytes_reserved": stage_reserve, "output_entries_reserved": 9}
                reservation_pin = save_admin(stage_dir/"reservation.json", reservation, ADMIN_RECORD_LIMIT)
                report["worker_cpu_charge_this_attempt"] += limits["cpu_seconds"]
                stage = {"schema": PREFIX+"STAGE_V1", "stage": key, "status": "FAIL",
                         "reservation": reservation_pin}
                invoked = False
                try:
                    active()
                    report["host_calls_attempted"] += 1
                    report["prover_stages_attempted"] += int(kind != "finish")
                    invoked = True
                    process = self._A.supervise(argv, self._install, stage_dir/"command", limits, self._Job)
                except BaseException as error:
                    process = ({"status": "SUPERVISOR_RAISED_UNCERTAIN", "final_job": None} if invoked else
                        {"status": "RESERVED_NOT_LAUNCHED", "final_job": {"active_processes": 0, "cpu_seconds": 0},
                         "direct_child_reaped": True, "job_closed": True, "cleanup_errors": []})
                    stage["supervisor_error"] = type(error).__name__+": "+str(error)[:2000]
                stage["process"] = process
                known = P.closure_known(process)
                if known:
                    try:
                        actual = number(process["final_job"]["cpu_seconds"])
                    except (KeyError, ValueError, TypeError):
                        known = False
                if known:
                    report["worker_cpu_charge_this_attempt"] += actual-limits["cpu_seconds"]
                    stage["worker_cpu_charge"] = actual
                else:
                    report["closure_accounting_known"] = False; self._closed = True
                    stage["worker_cpu_charge"] = limits["cpu_seconds"]
                try:
                    require(known and P.clean(process), "STAGE_FAILED_OR_UNCERTAIN")
                    require(prior[0]+report["worker_cpu_charge_this_attempt"] <= budget["worker_cpu_seconds"],
                            "AGGREGATE_WORKER_CPU")
                    self._A.absolute(artifact)
                    require(0 < artifact.stat().st_size <= selected["output_bytes"], "SELECTED_OUTPUT_FILE_BOUND")
                    pin = file_pin(artifact)
                    require(pin["bytes"] <= selected["output_bytes"], "SELECTED_OUTPUT_FILE_BOUND")
                    stdout = self._A.bounded_read(stage_dir/"command/stdout.txt", limits["stdout_bytes"])
                    result = stage_output(stdout, key, session, self.support, pin, manifest_pin, dependencies)
                    report["reported_proof_stage_calls"] += result["proof_stage_calls"]
                    if kind != "finish":
                        self._checkpoint({"key": key, "file": pin}, session)
                    rebind(); census(TAIL_BYTES, TAIL_ENTRIES)
                    stage.update(status="PASS_BOUND_HOST_STAGE", artifact=pin, bound_stdout=result)
                except BaseException as error:
                    stage["error"] = type(error).__name__+": "+str(error)[:2000]
                stage_pin = save_admin(stage_dir/"RESULT.json", stage, ADMIN_RECORD_LIMIT)
                report["stages"].append(stage_pin)
                require(stage["status"] == "PASS_BOUND_HOST_STAGE", "FIRST_FAILURE_STOPS")
                census(TAIL_BYTES, TAIL_ENTRIES)
                self._add(inputs, pin, ARTIFACT_LIMIT)
                if kind == "finish":
                    report["receipt"] = pin; report["application_receipt_created"] = True
                else:
                    inventory[key] = pin
            rebind()
            report["status"] = "PASS_FINISHED_RECEIPT_ARTIFACT" if report["application_receipt_created"] else "PASS_SELECTED_PREFIX_ONLY"
        except BaseException as error:
            report["error"] = type(error).__name__+": "+str(error)[:2000]
        try:
            rebind(); census(TAIL_BYTES, TAIL_ENTRIES)
            report["final_binding_validated"] = True
        except BaseException as error:
            report.update(status="FAIL", final_binding_error=type(error).__name__+": "+str(error)[:2000])
        report["retained_checkpoints"] = [{"key": k, "file": v} for k,v in sorted(inventory.items())]
        try:
            size, count = census(TAIL_BYTES, TAIL_ENTRIES)
            report.update(controller_cpu_seconds=time.process_time()-cpu_started, wall_seconds=time.monotonic()-started,
                prior_allowance_worker_charge=prior[0], prior_allowance_controller_cpu=prior[1], prior_allowance_wall=prior[2],
                prior_allowance_output_charge=prior[3], prior_allowance_entry_charge=prior[4],
                output_charge_this_attempt=size+TAIL_BYTES, entry_charge_this_attempt=count+TAIL_ENTRIES,
                accounting="INCLUSIVE_WORKER_JOB_CHARGE_PLUS_PRE_FINAL_REPORT_CONTROLLER;UNKNOWN_CHARGE_IS_RESERVATION_NOT_CPU_BOUND;OUTPUT_TAIL_STAYS_RESERVED",
                measurement_exclusions="CONTROLLER_STARTUP_EXIT_POST_OBSERVATION_TAILS;OUTPUT_CENSUS_SAMPLED_NOT_QUOTA;OUTER_OWNER_MUST_CLOSE_BOUNDARIES")
            fields(report, ATTEMPT_FIELDS)
            require(len(encoded(report)) <= MIB, "ATTEMPT_REPORT_BYTES")
            self._A.save_new(output/"RESULT.json", report)
            rebind()
            census()
            require(file_pin(output/"RESULT.json")["bytes"] <= MIB, "FINAL_REPORT_BOUND")
        except BaseException as error:
            self._closed = True
            self._A.save_new(output/"FINALIZATION-FAILED.json", {
                "status": "FINALIZATION_FAILED", "overrides_result": True,
                "error": type(error).__name__+": "+str(error)[:2000]})
            raise P.ProductionError("FINALIZATION_FAILED") from error
        self._history[request["allowance_id"]] = request["prior_attempts"]+[file_pin(output/"RESULT.json")]
        self._attempt_open = False
        return parse(encoded(report))

    def close(self):
        require(not self._busy, "AGGREGATE_PRODUCER_BUSY")
        self._closed = True
        self._support.close()

    def report(self):
        return {"closed": self._closed, "busy": self._busy, "last_call_failure": self._last_call_failure,
                "authority": "LOCAL_OPERATION_OBSERVATION_NOT_PROOF_OR_COMPLETE_PROCESS_COST"}

    def _checkpoint(self, row, session):
        fields(row, ("key", "file"))
        require(type(row["key"]) is str, "CHECKPOINT_KEY")
        split_key(row["key"])
        path = pin_fields(row["file"], ARTIFACT_LIMIT)
        self._A.absolute(path)
        require(file_pin(path) == row["file"], "CHECKPOINT_PIN")
        with path.open("rb") as stream:
            checkpoint_header(stream.read(71), row["file"]["bytes"], session["capsule_binding"], row["key"])

    def _snapshot(self, session, expected, inputs):
        pins = session["snapshot_evidence"]
        r = self._records(pins, ("result", "outer", "selection", "configuration", "command"), inputs)
        self._local_outer(r["outer"], r["selection"], pins["selection"], pins["outer"])
        result = r["result"]
        fields(result, ("actual_result", "aggregate_image", "capsule", "configuration_sha256", "cycles",
                        "diagnostic", "diagnostic_mode", "exit_code", "host_calls", "mathematical_admission",
                        "output_census_before_result", "proof_calls", "schema", "scope", "segment_po2",
                        "status", "wall_seconds_before_final_report", "host_build"))
        require(result["schema"] == "DMKN_SMALL_AGGREGATE_COST_SCREEN_RESULT_V1"
                and result["status"] == "PASS_ONE_AGGREGATE_EXECUTION_CAPSULE_ONLY"
                and result["aggregate_image"] == self.support["image_id"]
                and result["cycles"] == session["cycles"] and result["segment_po2"] == session["po2"]
                and type(result["exit_code"]) is int and result["exit_code"] == 0
                and type(result["host_calls"]) is int and result["host_calls"] == 1
                and type(result["proof_calls"]) is int and result["proof_calls"] == 0
                and result["mathematical_admission"] is False
                and result["capsule"] == session["capsule"]
                and result["configuration_sha256"] == pins["configuration"]["sha256"], "ADOPTED_COMPLETE_SCREEN")
        actual = result["actual_result"]
        expected_result = {
            "schema": "DMKN_SMALL_AGGREGATE_SNAPSHOT_RESULT_V1", "status": "UNTRUSTED_AGGREGATE_EXECUTION_CAPSULE_RETAINED",
            "aggregate_image": self.support["image_id"], "header": list(expected),
            "capsule_path": session["capsule"]["path"], "capsule_bytes": session["capsule"]["bytes"],
            "capsule_sha256": session["capsule"]["sha256"], "capsule_binding": session["capsule_binding"],
            "session_binding": session["session_binding"], "segments": session["segments"],
            "assumptions": session["assumptions"], "mathematical_admission": False,
            "proof_calls": 0, "guest_execute_calls": 1}
        fields(actual, expected_result)
        require(all(type(actual[k]) is type(v) and actual[k] == v for k,v in expected_result.items()),
                "EXACT_SNAPSHOT_RESULT")
        require(all(type(x) is int for x in actual["header"]), "SNAPSHOT_HEADER_BYTES")
        cfg = r["configuration"]
        fields(cfg, ("schema", "image_result", "image_result_sha256", "aggregate_image", "output", "host_build"))
        require(cfg == {"schema": "DMKN_SMALL_AGGREGATE_COST_SCREEN_V1",
                       "image_result": self.profile["image_adoption"]["result"]["path"],
                       "image_result_sha256": self.profile["image_adoption"]["result"]["sha256"],
                       "aggregate_image": self.support["image_id"],
                       "output": str(Path(pins["result"]["path"]).parent),
                       "host_build": result["host_build"]}, "SCREEN_CONFIGURATION_BINDING")
        snapshot_host = self._adopt_host_build(result["host_build"], inputs, "snapshot")
        self._snapshot_build_pins = parse(encoded(result["host_build"]))
        outer_argv = r["outer"]["result"]["argv"]
        runtime = r["selection"]["runtime_pins"]
        require(type(runtime) is dict and outer_argv[-1] == pins["configuration"]["sha256"]
                and runtime.get(outer_argv[-2]) == pins["configuration"]["sha256"],
                "SCREEN_OUTER_CONFIGURATION_BINDING")
        command = r["command"]
        fields(command, ("argv", "authority", "timeout_seconds"))
        argv = command["argv"]
        require(type(argv) is list and len(argv) == 12+len(session["parents"])
                and all(type(x) is str for x in argv), "SNAPSHOT_COMMAND_SHAPE")
        require(argv[1:] == ["snapshot", self.support["image_id"], session["image"]["path"],
                session["wire"]["path"], session["expected"]["path"], str(session["cycles"]), str(session["po2"]),
                result["diagnostic_mode"], session["capsule"]["path"], result["diagnostic"]["path"],
                str(len(session["parents"])), *[p["path"] for p in session["parents"]]],
                "SNAPSHOT_COMMAND_EXACT_SESSION_AND_PARENT_ORDER")
        for pin in [session["image"], *session["parents"]]:
            require(runtime.get(pin["path"]) == pin["sha256"], "SCREEN_SELECTED_INPUT_PIN")
        self._A.absolute(argv[0])
        require(argv[0] == snapshot_host["path"] and file_pin(Path(argv[0])) == snapshot_host
                and runtime.get(argv[0]) == snapshot_host["sha256"], "SCREEN_SELECTED_HOST_PIN")
        self._add(inputs, snapshot_host, 8*MIB)
        self._no_override(pins.values())
        self._no_override(self._snapshot_build_pins.values())

