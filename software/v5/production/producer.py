"""Relocatable Windows producer. Reports/checkpoints are not admission handles.

Only the local owner supplies profile, requests, budgets and predecessor pins.
The unchanged real host verifies cryptographic objects when consuming them and
fully verifies its final receipt. This module never treats saved JSON as proof.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import time

MIB = 1024**2
HEX = r"[0-9a-f]{64}"
KINDS = ("segment", "lift", "join", "resolve", "finish")
COMMON = {"memory_mib": 4096, "active_processes": 2,
          "stdout_bytes": MIB, "stderr_bytes": MIB}
STAGE_CEILINGS = {"segment": (1800, 600), "lift": (600, 600),
                  "join": (600, 600), "resolve": (600, 600), "finish": (300, 600)}
SOURCE_NAMES = ("producer.py", "__init__.py")


class ProductionError(ValueError):
    pass


def require(ok, why):
    if not ok:
        raise ProductionError(why)


def fields(value, names):
    require(type(value) is dict and set(value) == set(names), "EXACT_FIELDS")


def uint(value, maximum, minimum=0):
    require(type(value) is int and minimum <= value <= maximum, "INTEGER_LIMIT")
    return value


def number(value):
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0, "FINITE_NONNEGATIVE_COST")
    return value


def digest(value):
    require(type(value) is str and re.fullmatch(HEX, value), "SHA256_FORMAT")
    return value


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def reject(_):
        raise ProductionError("NONFINITE_JSON")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=reject)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)+"\n").encode()


def hash_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def pin_fields(value, maximum=128*MIB):
    fields(value, ("path", "bytes", "sha256"))
    require(type(value["path"]) is str and Path(value["path"]).is_absolute(), "ABSOLUTE_PIN_PATH")
    uint(value["bytes"], maximum, 1); digest(value["sha256"])
    return Path(value["path"])


def file_pin(path):
    size = path.stat().st_size
    require(0 < size <= 128*MIB, "FILE_SIZE")
    h, seen = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while block := stream.read(MIB):
            seen += len(block); require(seen <= 128*MIB, "FILE_GREW")
            h.update(block)
    require(seen == size, "FILE_SIZE_CHANGED")
    return {"path": str(path), "bytes": seen, "sha256": h.hexdigest()}


def stage_key(kind, index):
    require(kind in KINDS, "STAGE_KIND"); uint(index, 127)
    return kind+":"+str(index)


def graph(segments, assumptions):
    """Deterministic ordered graph; finish has the complete segment vector."""
    uint(segments, 128, 1); uint(assumptions, 8)
    result = []
    for i in range(segments):
        result.append((stage_key("segment", i), ()))
        result.append((stage_key("lift", i), (stage_key("segment", i),)))
        if i:
            left = stage_key("lift", 0) if i == 1 else stage_key("join", i-1)
            result.append((stage_key("join", i), (left, stage_key("lift", i))))
    prefix = stage_key("lift", 0) if segments == 1 else stage_key("join", segments-1)
    for i in range(assumptions):
        result.append((stage_key("resolve", i), (prefix,)))
        prefix = stage_key("resolve", i)
    result.append(("finish:0", tuple(stage_key("segment", i) for i in range(segments))+(prefix,)))
    return result


def missing_plan(segments, assumptions, available):
    nodes = graph(segments, assumptions); edges = dict(nodes)
    require(set(available) <= set(edges)-{"finish:0"}, "CHECKPOINT_OUTSIDE_GRAPH")
    required = set()
    def visit(key):
        if key in available or key in required:
            return
        required.add(key)
        for parent in edges[key]:
            visit(parent)
    visit("finish:0")
    return [(key, dependencies) for key, dependencies in nodes if key in required]


def checkpoint_header(raw_header, byte_count, binding, key):
    """Pinned bincode fixed-width envelope only; this is NOT crypto verification."""
    require(len(raw_header) >= 60 and struct.unpack_from("<I", raw_header)[0] == 5, "CHECKPOINT_SCHEMA5")
    require(raw_header[4:36].hex() == binding, "CHECKPOINT_CAPSULE_BINDING")
    n = struct.unpack_from("<Q", raw_header, 36)[0]
    require(1 <= n <= 7 and len(raw_header) >= 56+n, "CHECKPOINT_KIND_LENGTH")
    kind = raw_header[44:44+n].decode("ascii")
    index = struct.unpack_from("<I", raw_header, 44+n)[0]
    payload = struct.unpack_from("<Q", raw_header, 48+n)[0]
    require(kind != "finish" and stage_key(kind, index) == key
            and payload > 0 and 56+n+payload == byte_count, "CHECKPOINT_LAYOUT_OR_KEY")


def clean(record):
    return (record.get("status") == "COMMAND_EXITED_ZERO_AND_CLOSED"
        and record.get("child_exit_code") == 0 and record.get("direct_child_reaped") is True
        and record.get("job_closed") is True and record.get("cleanup_errors") == []
        and record.get("termination_requested") is False
        and record.get("final_job", {}).get("active_processes") == 0
        and record.get("final_job", {}).get("terminated_processes") == 0)


def closure_known(record):
    final = record.get("final_job")
    return (type(final) is dict and record.get("direct_child_reaped") is True
        and record.get("job_closed") is True and record.get("cleanup_errors") == []
        and final.get("active_processes") == 0)


class Producer:
    """One local owner; no remote-controlled construction or automatic retries.

    A run is one finite attempt. A new run requires a fresh request/output path;
    same-lineage predecessor charges remain spent. close() prevents further runs.
    """
    def __init__(self, profile):
        require(os.name == "nt" and sys.flags.isolated and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize, "WINDOWS_ISOLATED_OWNER_REQUIRED")
        fields(profile, ("schema", "supervisor_manifest", "host", "python", "python_dll",
                         "source_pins", "runtime_pins", "image_id", "foundation", "policy"))
        require(profile["schema"] == "DMKN_V5_PRODUCER_PROFILE_V1", "PROFILE_SCHEMA")
        self.profile = parse(encoded(profile)); profile = self.profile
        self._profile_raw = encoded(profile)
        self._closed = False; self._busy = False; self._attempt_open = False; self._history = {}
        self._last_call_failure = None
        for name in ("image_id", "foundation", "policy"):
            digest(profile[name])
        manifest = pin_fields(profile["supervisor_manifest"], 8*MIB)
        require(file_pin(manifest) == profile["supervisor_manifest"], "SUPERVISOR_MANIFEST_PIN")
        self._manifest_raw = manifest.read_bytes(); held = parse(self._manifest_raw)
        require(type(held) is dict and type(held.get("files")) is dict, "MANIFEST_FILES")
        self._install = manifest.parent; self._pins = {str(manifest): profile["supervisor_manifest"]}

        def load(name, relative):
            row = held["files"].get(relative); fields(row, ("bytes", "sha256"))
            uint(row["bytes"], 4*MIB, 1); digest(row["sha256"])
            path = self._install / relative
            p = {"path": str(path), **row}; require(file_pin(path) == p, "SUPERVISOR_SOURCE_PIN")
            self._pins[str(path)] = p
            if name in sys.modules:
                module = sys.modules[name]
                require(getattr(module, "_dmkn_admission_source_pin", None) == row["sha256"]
                    and Path(getattr(module, "__file__", "")) == path, "LOADED_MODULE_COLLISION")
                return module
            raw = path.read_bytes(); spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec); sys.modules[name] = module
            try:
                exec(compile(raw, str(path), "exec"), module.__dict__)
            except BaseException:
                del sys.modules[name]; raise
            module._dmkn_admission_source_pin = row["sha256"]
            return module

        # Same exact identities as admission; same-process composition is safe.
        self._A = load("_dmkn_v5_admission_supervisor", "operator/commons.py")
        load("domains", "receiver/helpers/domains.py")
        self._Job = load("_dmkn_v5_admission_job", "receiver/helpers/run_stage.py").Job
        source = profile["source_pins"]
        require(type(source) is list and len(source) == 2, "EXACT_PRODUCER_SOURCES")
        require({pin_fields(x) for x in source} == {Path(__file__).resolve().parent / x for x in SOURCE_NAMES},
                "ACTUAL_PRODUCER_SOURCE_PATHS")
        runtime = profile["runtime_pins"]
        require(type(runtime) is list and len(runtime) <= 128, "RUNTIME_PIN_COUNT")
        for p in [profile["host"], profile["python"], profile["python_dll"], *source, *runtime]:
            path = pin_fields(p)
            require(str(path) not in self._pins or self._pins[str(path)] == p, "CONFLICTING_PIN")
            self._pins[str(path)] = dict(p)
        require(sum(p["bytes"] for p in self._pins.values()) <= 512*MIB, "RUNTIME_BYTE_ENVELOPE")
        require(Path(sys.executable).resolve() == Path(profile["python"]["path"])
            and Path(profile["python_dll"]["path"]) == Path(sys.executable).parent / "python314.dll", "ADOPTED_PYTHON")
        self._check(self._pins)

    def _check(self, pins):
        require(encoded(self.profile) == self._profile_raw, "OWNER_PROFILE_MUTATED")
        for path, p in pins.items():
            self._A.absolute(path)
            require(file_pin(Path(path)) == p, "PIN_CHANGED:"+path)

    def _add_pin(self, pins, p):
        pin_fields(p)
        for table in (self._pins, pins):
            require(p["path"] not in table or table[p["path"]] == p, "CONFLICTING_ROLE_PIN")
        pins[p["path"]] = dict(p)

    def _read(self, p, maximum=MIB):
        path = pin_fields(p, maximum); self._A.absolute(path)
        require(file_pin(path) == p, "INPUT_PIN_CHANGED")
        return self._A.bounded_read(path, maximum)

    def _checkpoint(self, row, session):
        fields(row, ("key", "file"))
        require(type(row["key"]) is str, "CHECKPOINT_KEY")
        path = pin_fields(row["file"], 64*MIB); self._A.absolute(path)
        require(file_pin(path) == row["file"], "CHECKPOINT_PIN")
        with path.open("rb") as stream:
            checkpoint_header(stream.read(64), row["file"]["bytes"], session["binding"], row["key"])
        return path

    def _request(self, request):
        fields(request, ("schema", "allowance_id", "session", "checkpoints", "output_directory",
            "stage_limit", "budget", "prior_attempts", "carried_external_costs"))
        require(request["schema"] == "DMKN_V5_PRODUCER_REQUEST_V1", "REQUEST_SCHEMA")
        digest(request["allowance_id"]); require(len(encoded(request)) <= MIB, "REQUEST_BYTES")
        session = request["session"]
        fields(session, ("image", "frame", "expected", "capsule", "parents", "binding",
                         "cycles", "po2", "segments", "assumptions"))
        digest(session["binding"]); uint(session["cycles"], 1 << 28, 1); uint(session["po2"], 20, 12)
        graph(session["segments"], session["assumptions"])
        require(type(session["parents"]) is list and len(session["parents"]) <= 8, "PARENT_COUNT")
        require(session["assumptions"] <= len(session["parents"]), "ASSUMPTION_COUNT")
        inputs = {}
        for name, maximum in (("image",64*MIB),("frame",16*MIB+4),("expected",184),("capsule",64*MIB)):
            p = session[name]; pin_fields(p, maximum); self._add_pin(inputs,p)
        for p in session["parents"]:
            pin_fields(p, 64*MIB); require(p["path"] not in inputs, "DUPLICATE_PARENT_PATH"); self._add_pin(inputs,p)
        self._check(inputs)
        expected = self._read(session["expected"], 184)
        require(len(expected) == 184 and expected[:12] == b"DMKNM002\x02\0\0\0"
            and expected[12:44].hex() == self.profile["image_id"]
            and expected[44:76].hex() == self.profile["foundation"]
            and expected[76:108].hex() == self.profile["policy"], "ADOPTED_EXPECTED_JOURNAL")
        with Path(session["capsule"]["path"]).open("rb") as stream:
            require(stream.read(4) == struct.pack("<I", 3), "CAPSULE_SCHEMA3")
        rows = request["checkpoints"]; require(type(rows) is list and len(rows) <= 391, "CHECKPOINT_COUNT")
        inventory = {}
        for row in rows:
            self._checkpoint(row, session); require(row["key"] not in inventory, "DUPLICATE_CHECKPOINT_KEY")
            inventory[row["key"]] = row["file"]; self._add_pin(inputs,row["file"])
        nodes = missing_plan(session["segments"], session["assumptions"], inventory)
        uint(request["stage_limit"], 392, 1)
        b = request["budget"]
        fields(b, ("worker_cpu_seconds", "controller_cpu_seconds", "wall_seconds", "output_bytes", "output_entries", "stages"))
        for name, lo, hi in (("worker_cpu_seconds",1,250000),("controller_cpu_seconds",1,3600),
                ("wall_seconds",1,86400),("output_bytes",70*MIB,2*1024*MIB),("output_entries",16,8192)):
            uint(b[name],hi,lo)
        fields(b["stages"], KINDS)
        for kind, maximum in STAGE_CEILINGS.items():
            fields(b["stages"][kind], ("cpu_seconds","wall_seconds"))
            uint(b["stages"][kind]["cpu_seconds"],maximum[0],1)
            uint(b["stages"][kind]["wall_seconds"],maximum[1],1)
        carried = request["carried_external_costs"]
        fields(carried, ("worker_cpu_seconds", "controller_cpu_seconds", "wall_seconds", "scope"))
        for key in ("worker_cpu_seconds","controller_cpu_seconds","wall_seconds"):
            number(carried[key])
        require(type(carried["scope"]) is str and 1 <= len(carried["scope"]) <= 1024, "CARRIED_SCOPE")
        identity = {k: session[k] for k in ("binding","cycles","po2","segments","assumptions")}
        identity.update({k: {n: session[k][n] for n in ("bytes","sha256")}
                         for k in ("image","frame","expected","capsule")})
        identity["parents"] = [{n: p[n] for n in ("bytes","sha256")} for p in session["parents"]]
        session_id = hash_bytes(encoded(identity))
        prior_pins = request["prior_attempts"]
        require(type(prior_pins) is list and len(prior_pins) <= 16, "PRIOR_ATTEMPT_COUNT")
        require(request["allowance_id"] not in self._history
            or self._history[request["allowance_id"]] == prior_pins, "LIVE_ALLOWANCE_HISTORY_MISSING")
        prior_cpu = 0; prior_controller = 0; prior_wall = 0; seen = set(); prior_bytes = 0
        for i, pin in enumerate(prior_pins):
            path = pin_fields(pin,MIB); prior_bytes += pin["bytes"]
            require(str(path) not in seen and prior_bytes <= 8*MIB, "PRIOR_LEDGER_BOUND")
            seen.add(str(path)); old = parse(self._read(pin))
            require(old["schema"] == "DMKN_V5_PRODUCER_ATTEMPT_V1"
                and old["session_id"] == session_id and old["allowance_id"] == request["allowance_id"]
                and old["prior_attempts"] == prior_pins[:i]
                and old["budget"] == b and old["carried_external_costs"] == carried,
                "COMPLETE_SAME_ALLOWANCE_LINEAGE")
            require(old["closure_accounting_known"] is True and old["final_binding_validated"] is True
                and not (path.parent / "FINALIZATION-FAILED.json").exists(), "PRIOR_REQUIRES_OWNER_RECOVERY")
            for row in old["retained_checkpoints"]:
                require(inventory.get(row["key"]) == row["file"], "PRIOR_SUCCESS_MUST_BE_RETAINED")
            prior_cpu += number(old["worker_cpu_charge_this_attempt"])
            prior_controller += number(old["controller_cpu_seconds"])
            prior_wall += number(old["wall_seconds"])
            self._add_pin(inputs,pin)
        require(sum(p["bytes"] for p in inputs.values()) <= 512*MIB, "SESSION_INPUT_ENVELOPE")
        output = self._A.absolute(request["output_directory"], directory=True, fresh=True)
        for protected in [self._install, *map(Path,self._pins), *map(Path,inputs)]:
            require(not self._A.overlap(output, protected), "OUTPUT_OVERLAP")
        return session_id, expected, inputs, inventory, nodes[:request["stage_limit"]], output, (prior_cpu,prior_controller,prior_wall)

    def run(self, request):
        require(not self._closed and not self._busy, "PRODUCER_CLOSED_OR_BUSY")
        started, cpu_started = time.monotonic(), time.process_time()
        self._busy = True; self._last_call_failure = None
        try:
            request = parse(encoded(request))
            return self._run(request, started, cpu_started)
        except BaseException as error:
            self._last_call_failure = {"scope":"RUN_REFUSAL_OR_INTERRUPTION_OBSERVATION_NOT_DURABLE_BUDGET_LEDGER",
                "controller_cpu_seconds":time.process_time()-cpu_started,
                "wall_seconds":time.monotonic()-started,"attempt_directory_created":self._attempt_open,
                "error":type(error).__name__+": "+str(error)[:2000]}
            if self._attempt_open:
                self._closed = True
            raise
        finally:
            self._busy = False

    def _run(self, request, started, cpu_started):
        session_id, expected, inputs, inventory, nodes, output, prior = self._request(request)
        session, budget = request["session"], request["budget"]
        require(prior[0] < budget["worker_cpu_seconds"] and prior[1] < budget["controller_cpu_seconds"]
            and prior[2] < budget["wall_seconds"], "ALLOWANCE_EXHAUSTED")
        deadline = started + budget["wall_seconds"]-prior[2]
        def active():
            require(time.monotonic() <= deadline
                and prior[1]+time.process_time()-cpu_started <= budget["controller_cpu_seconds"], "ATTEMPT_DEADLINE_OR_CONTROLLER_CPU")
        def rebind():
            active(); self._check(self._pins); self._check(inputs); active()
        rebind(); output.mkdir(); self._attempt_open = True
        self._A.save_new(output / "request.json", request)
        self._A.save_new(output / "profile.json", self.profile)
        controls = [file_pin(output/"request.json"),file_pin(output/"profile.json")]
        for p in controls:
            self._add_pin(inputs,p)
        report = {"schema":"DMKN_V5_PRODUCER_ATTEMPT_V1", "status":"FAIL", "session_id":session_id,
            "allowance_id":request["allowance_id"], "budget":budget, "prior_attempts":request["prior_attempts"],
            "carried_external_costs":request["carried_external_costs"], "worker_cpu_charge_this_attempt":0,
            "closure_accounting_known":True, "proof_stage_calls":0, "guest_execute_calls":0,
            "mathematical_admission":False, "application_receipt_created":False,
            "stages":[], "retained_checkpoints":[], "final_binding_validated":False,
            "control_documents":controls,
            "authority":"PRODUCER_ARTIFACTS_NOT_ADMISSION_HANDLES"}
        def census(reserve=0, reserve_entries=0):
            size, count = 0, 0
            for directory, dirs, names in os.walk(output, followlinks=False):
                for name in dirs+names:
                    active(); p = Path(directory)/name
                    self._A.absolute(p,directory=name in dirs); count += 1
                    require(count+reserve_entries <= budget["output_entries"], "OUTPUT_ENTRY_LIMIT")
                    if name in names: size += p.stat().st_size
                    require(size+reserve <= budget["output_bytes"], "OUTPUT_BYTE_LIMIT")
            return {"bytes":size,"entries":count}
        try:
            for key, dependencies in nodes:
                active(); rebind(); census(70*MIB,10)
                kind, index_text = key.split(":"); index = int(index_text)
                limits = {**COMMON, **budget["stages"][kind]}
                require(prior[0]+report["worker_cpu_charge_this_attempt"]+limits["cpu_seconds"]
                    <= budget["worker_cpu_seconds"], "NEXT_STAGE_RESERVATION_EXCEEDS_ALLOWANCE")
                limits["wall_seconds"] = min(limits["wall_seconds"], math.floor(deadline-time.monotonic()))
                require(limits["wall_seconds"] >= 1, "STAGE_DEADLINE")
                stage_dir = output / (kind+"-"+index_text); stage_dir.mkdir()
                artifact = stage_dir / ("receipt.bin" if kind == "finish" else "proof.checkpoint")
                deps = [inventory[d] for d in dependencies]
                require(sum(session[n]["bytes"] for n in ("image","frame","expected","capsule"))
                    +sum(p["bytes"] for p in session["parents"]+deps) <= 512*MIB, "HOST_TOTAL_READ_LIMIT")
                argv = [self.profile["host"]["path"],"stage",session["image"]["path"],session["frame"]["path"],
                    session["expected"]["path"],str(session["cycles"]),str(session["po2"]),kind,index_text,
                    str(artifact),str(len(session["parents"])),*[p["path"] for p in session["parents"]],
                    session["capsule"]["path"],*[p["path"] for p in deps]]
                reservation = {"schema":"DMKN_V5_PRODUCER_RESERVATION_V1", "session_id":session_id,
                    "allowance_id":request["allowance_id"],"stage":key,"limits":limits,"argv":argv,
                    "dependencies":deps,"worker_reserved":limits["cpu_seconds"]}
                self._A.save_new(stage_dir / "reservation.json", reservation)
                report["worker_cpu_charge_this_attempt"] += limits["cpu_seconds"]
                report["proof_stage_calls"] += 1
                stage = {"schema":"DMKN_V5_PRODUCER_STAGE_V1","stage":key,"status":"FAIL"}
                try:
                    active()
                    process = self._A.supervise(argv,self._install,stage_dir/"command",limits,self._Job)
                except BaseException as error:
                    process = {"status":"SUPERVISOR_RAISED_UNCERTAIN","final_job":None}
                    stage["supervisor_error"] = type(error).__name__+": "+str(error)[:2000]
                stage["process"] = process
                known = closure_known(process)
                if known:
                    actual = number(process["final_job"]["cpu_seconds"])
                    report["worker_cpu_charge_this_attempt"] += actual-limits["cpu_seconds"]
                    stage["worker_cpu_charge"] = actual
                else:
                    report["closure_accounting_known"] = False
                    self._closed = True
                    stage["worker_cpu_charge"] = limits["cpu_seconds"]
                try:
                    require(known and clean(process), "STAGE_FAILED_OR_UNCERTAIN")
                    require(prior[0]+report["worker_cpu_charge_this_attempt"] <= budget["worker_cpu_seconds"], "AGGREGATE_WORKER_CPU")
                    p = file_pin(artifact); require(p["bytes"] <= 64*MIB, "OUTPUT_FILE_BOUND")
                    line = self._A.bounded_read(stage_dir/"command/stdout.txt",MIB).decode("ascii").strip()
                    if kind == "finish":
                        marker = ("REAL_SUCCINCT_CHECKPOINT_FINISHED image_id="+self.profile["image_id"]+
                            " rank="+str(int.from_bytes(expected[176:184],"little"))+
                            " groups="+str(int.from_bytes(expected[172:176],"little"))+
                            " receipt_bytes="+str(p["bytes"])+" parents="+str(len(session["parents"]))+
                            " segments="+str(session["segments"])+" binding="+session["binding"])
                    else:
                        self._checkpoint({"key":key,"file":p},session)
                        marker = ("REAL_PROOF_CHECKPOINT_NOT_APPLICATION_CERTIFICATE kind="+kind+" index="+index_text+
                            " checkpoint_bytes="+str(p["bytes"])+" segments="+str(session["segments"])+
                            " assumptions="+str(session["assumptions"])+" binding="+session["binding"])
                    require(line == marker, "EXACT_HOST_OUTPUT")
                    rebind(); active(); census()
                    stage.update(status="PASS_BOUND_HOST_STAGE",artifact=p)
                except BaseException as error:
                    stage["error"] = type(error).__name__+": "+str(error)[:2000]
                self._A.save_new(stage_dir/"RESULT.json",stage)
                report["stages"].append(file_pin(stage_dir/"RESULT.json"))
                require(stage["status"] == "PASS_BOUND_HOST_STAGE", "FIRST_FAILURE_STOPS")
                active(); census()
                self._add_pin(inputs,p)
                if kind == "finish":
                    report["receipt"] = p; report["application_receipt_created"] = True
                else:
                    inventory[key] = p
            rebind(); active()
            report["status"] = "PASS_FINISHED_RECEIPT_ARTIFACT" if report["application_receipt_created"] else "PASS_SELECTED_PREFIX_ONLY"
        except BaseException as error:
            report["error"] = type(error).__name__+": "+str(error)[:2000]
        try:
            rebind(); active()
            report["final_binding_validated"] = True
        except BaseException as error:
            report.update(status="FAIL",final_binding_error=type(error).__name__+": "+str(error)[:2000])
        report["retained_checkpoints"] = [{"key":k,"file":v} for k,v in sorted(inventory.items())]
        report.update(controller_cpu_seconds=time.process_time()-cpu_started,wall_seconds=time.monotonic()-started,
            prior_allowance_worker_charge=prior[0],prior_allowance_controller_cpu=prior[1],prior_allowance_wall=prior[2],
            accounting="THIS_ATTEMPT_JOB_CHARGE_PLUS_PRE_FINAL_REPORT_CONTROLLER;SUPERVISOR_NESTED;UNKNOWN_CHARGE_IS_RESERVATION_NOT_PROVEN_CPU_BOUND",
            measurement_exclusions="PROCESS_STARTUP_EXIT_AND_POST_OBSERVATION_TAILS;OUTPUT_LIMIT_SAMPLED_NOT_FILESYSTEM_QUOTA")
        self._A.save_new(output/"RESULT.json",report)
        try:
            active(); census()
        except BaseException:
            self._A.save_new(output/"FINALIZATION-FAILED.json",{"status":"POST_REPORT_LIMIT_FAILED"})
            raise ProductionError("FINALIZATION_FAILED")
        self._history[request["allowance_id"]] = request["prior_attempts"]+[file_pin(output/"RESULT.json")]
        self._attempt_open = False
        return report

    def close(self):
        require(not self._busy, "PRODUCER_BUSY")
        self._closed = True

    def report(self):
        """Includes measured refused preflight calls that had no safe output path."""
        return {"closed":self._closed,"busy":self._busy,"last_call_failure":self._last_call_failure,
            "authority":"LOCAL_OPERATION_OBSERVATION_NOT_PROOF_OR_COMPLETE_PROCESS_COST"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile",required=True); parser.add_argument("--profile-sha256",required=True)
    parser.add_argument("--request",required=True); parser.add_argument("--request-sha256",required=True)
    args = parser.parse_args()
    def document(name, expected):
        digest(expected); p=Path(name)
        require(p.is_absolute() and 0 < p.stat().st_size <= MIB, "OWNER_DOCUMENT_PATH_BOUND")
        raw=p.read_bytes(); require(len(raw)<=MIB and hash_bytes(raw)==expected,"OWNER_DOCUMENT_PIN")
        return parse(raw)
    owner=Producer(document(args.profile,args.profile_sha256))
    try:
        result=owner.run(document(args.request,args.request_sha256)); print(json.dumps(result),flush=True)
        return 0 if result["status"].startswith("PASS_") else 1
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
