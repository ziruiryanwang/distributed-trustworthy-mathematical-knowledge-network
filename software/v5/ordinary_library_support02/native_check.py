"""One selected three-command ordinary-library check; never a product entrypoint.

Requires outer Windows Job 240 wall /160 CPU /2048 MiB /8 processes. The
original harness allocation is 210 wall /140 CPU, with a 190-second work
window. Each of exactly three public calls has at most 75 wall /40 CPU /
1024 MiB, derived from the remaining original allowance. No retry, build,
init, network, product API import or fourth status command is performed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import stat
import subprocess
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
OLD = LOCAL/"ordinary-peer-reciprocal-02"
PYTHON = Path(r"D:\Python314\python.exe")
LEAN = ROOT/"software/runtime/lean-4.34.0-windows"
MIB = 1024**2
STORE = "23421e020e9fe30b3aec293b6567996285af72fc16f54b311b71ffb113367167"
PARENT = "944e4275cce3ca23dbee05a0dca03771186335bc87def4f6365023eabb6bfc14"
IMPLEMENTATION = "fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df"
SEMANTIC = "9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7"
PREVIOUS_SHA = "c484d96cddf0a4e3985116a7632dabecbcac0386870926cd13a5bdc707282d5a"
OLD_ARTIFACTS = (
    "55cbddc0310a3d93ae4e2c555baa83e0ada1536b0290bf24f95b33d02f448bfe",
    "99303d20602ddd2932ed1fa693f5f29cf3ad91f4698f171e6192cec4d66241bb",
    "f156ac506d2a64dc89c344ead48a3f970834f1602d957a11b2de982a072693f2")
BODY = b"""theorem CommonsLibraryExample.add_zero (n : Nat) :
    Nat.add n Nat.zero = n := Nat.add_zero n
"""


def need(condition, code):
    if not condition:
        raise ValueError(code)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      allow_nan=False, separators=(",", ":")).encode("ascii")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def ordinary(path, directory=False):
    need(path.is_absolute() and ".." not in path.parts, "LIBRARY_CHECK_ABSOLUTE_PATH")
    for part in (path, *path.parents):
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "LIBRARY_CHECK_REDIRECT")
    info = path.lstat()
    need(stat.S_ISDIR(info.st_mode) if directory else
         stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "LIBRARY_CHECK_PATH_KIND")
    return path


def read(path, maximum=4*MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 <= size <= maximum, "LIBRARY_CHECK_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size, "LIBRARY_CHECK_FILE_CHANGED")
    return raw


def save(path, value):
    ordinary(path.parent, directory=True)
    raw = value if type(value) is bytes else canonical(value)
    need(len(raw) <= 16*MIB, "LIBRARY_CHECK_OUTPUT_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    return {"bytes": len(raw), "sha256": digest(raw)}


def name(text):
    return [[0, {"$bytes": list(part.encode("ascii"))}] for part in text.split(".")]


def retained_input_paths():
    """Explicit immutable selections; never catalog/custody databases or locks."""
    return [OLD/"RECIPROCAL-RESULT.json", OLD/"B-catalog/ADOPTION.json",
            OLD/"B-custody-limits.json", *(OLD/"B-catalog/operations"/identity/"chunk.olean"
                                          for identity in OLD_ARTIFACTS)]


def retained_map():
    result, total = {}, 0
    for path in retained_input_paths():
        raw = read(path, 32*MIB)
        total += len(raw)
        need(total <= 64*MIB, "LIBRARY_CHECK_RETAINED_TOTAL")
        result[str(path)] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def clean_native(path, extraction=False):
    report = json.loads(read(path, MIB))
    final = report.get("final_job")
    need(report.get("status") == ("EXTRACTED_AND_CLOSED" if extraction else
                                 "COMMAND_EXITED_ZERO_AND_CLOSED") and
         report.get("child_exit_code") == 0 and report.get("direct_child_reaped") is True and
         report.get("job_closed") is True and report.get("cleanup_errors") == [] and
         report.get("termination_requested") is False and type(final) is dict and
         final.get("active_processes") == 0 and final.get("terminated_processes") == 0 and
         type(final.get("total_processes")) is int and final["total_processes"] >= 1,
         "LIBRARY_CHECK_NATIVE_CLOSURE")
    cpu = final.get("cpu_seconds")
    need(type(cpu) in (int, float) and math.isfinite(cpu) and cpu >= 0,
         "LIBRARY_CHECK_NATIVE_CPU")
    if extraction:
        need(report.get("threads_joined") is True and report.get("accounting_complete") is True and
             report.get("job_attach_resume_completed") is True and
             report.get("native_cpu_seconds") == cpu, "LIBRARY_CHECK_EXTRACTION_CLOSURE")
    return report


class Run:
    def __init__(self, package, profile, output):
        self.started, self.cpu_started = time.monotonic(), time.process_time()
        self.deadline, self.cleanup_deadline = self.started+190, self.started+210
        self.package, self.profile, self.output = package, profile, output
        self.live, self.calls, self.cleanup, self.charged_cpu = {}, [], [], 0.0

    def check(self):
        need(time.monotonic() < self.deadline and
             time.process_time()-self.cpu_started+self.charged_cpu < 140,
             "LIBRARY_CHECK_ORIGINAL_ALLOWANCE")
        for row in self.live.values():
            need(row["stdout"].stat().st_size <= 4*MIB and row["stderr"].stat().st_size <= MIB,
                 "LIBRARY_CHECK_LIVE_LOG_BOUND")

    def collect(self, label, expected_missing=False, validate=True):
        row = self.live[label]
        need(row["process"].poll() is not None, "LIBRARY_CHECK_CHILD_STILL_LIVE")
        row["process"].wait()
        for handle in row["handles"]:
            handle.close()
        del self.live[label]
        event = {"operation": label, "returncode": row["process"].returncode,
                 "wall_seconds": time.monotonic()-row["started"],
                 "charged_cpu_seconds": row["cpu_cap"], "result": None}
        self.calls.append(event)
        charge = row["cpu_cap"]
        try:
            raw, errors = read(row["stdout"]), read(row["stderr"], MIB)
            event.update(stdout_sha256=digest(raw), stderr_sha256=digest(errors))
            result = json.loads(raw)
            event["result"] = result
            cost = result["cost"]
            values = (cost["controller_cpu_seconds"], cost["worker_cpu_seconds"])
            need(all(type(value) in (int, float) and math.isfinite(value) and value >= 0
                     for value in values), "LIBRARY_CHECK_CHILD_COST")
            detail = result.get("detail", {})
            missing = (result.get("ok") is False and row["process"].returncode == 1 and
                result.get("phase") == "CONTRIBUTE" and result.get("accepted") is None and
                detail.get("phase") == "BINDING" and detail.get("accepted") is None and
                detail.get("error") == "CONTRIBUTION_CANDIDATE_NEEDS_INTERPRETATIONS" and
                detail.get("needs_local_interpretations") == [name("Nat.add_zero")])
            normal = result.get("ok") is True and row["process"].returncode == 0
            if not errors and not result.get("close_errors") and (normal or expected_missing and missing):
                charge = sum(values)
            if validate:
                need(not errors and not result.get("close_errors") and result.get("operation") == label and
                     (missing if expected_missing else normal), "LIBRARY_CHECK_PUBLIC_COMMAND:"+label)
                if not expected_missing:
                    need(result["implementation_id"] == IMPLEMENTATION and
                         result["profile_sha256"] == self.profile and result["store_id"] == STORE,
                         "LIBRARY_CHECK_SELECTED_OWNER")
            return result
        finally:
            event["charged_cpu_seconds"] = charge
            self.charged_cpu += charge

    def call(self, operation, extra, expected_missing=False):
        self.check()
        need(not self.live and len(self.calls) < 3 and
             operation == ("contribute", "extract-std", "complete")[len(self.calls)],
             "LIBRARY_CHECK_EXACT_SEQUENCE_NO_RETRY")
        wall = min(75, math.floor(self.deadline-time.monotonic())-5)
        cpu = min(40, math.floor(140-(time.process_time()-self.cpu_started)-self.charged_cpu)-1)
        need(wall >= 35 and cpu >= 4, "LIBRARY_CHECK_REMAINING_CHILD_GRANT")
        argv = [str(PYTHON), "-I", "-S", "-B", str(self.package/"owner.py"), operation,
            "--profile-sha256", self.profile, "--python-runtime", str(PYTHON.parent),
            "--lean-runtime", str(LEAN), "--wall-seconds", str(wall), "--cpu-seconds", str(cpu),
            "--memory-mib", "1024", "--catalog", str(OLD/"B-catalog"),
            "--custody", str(OLD/"B-custody"), "--store-id", STORE,
            "--custody-limits", str(OLD/"B-custody-limits.json"), "--parent-root", PARENT, *extra]
        save(self.output/(operation+".command.json"), {"argv": argv, "wall_cap": wall,
            "cpu_cap": cpu, "memory_mib": 1024, "parent_seconds_remaining": self.deadline-time.monotonic()})
        stdout_path, stderr_path = self.output/(operation+".stdout"), self.output/(operation+".stderr")
        stdout, stderr = stdout_path.open("xb"), stderr_path.open("xb")
        started = time.monotonic()
        try:
            process = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
        except BaseException:
            stdout.close(); stderr.close()
            raise
        self.live[operation] = {"process": process, "handles": (stdout, stderr), "cpu_cap": cpu,
            "stdout": stdout_path, "stderr": stderr_path, "deadline": started+wall, "started": started}
        while process.poll() is None:
            self.check()
            need(time.monotonic() < started+wall+1, "LIBRARY_CHECK_CHILD_DEADLINE")
            time.sleep(0.05)
        result = self.collect(operation, expected_missing=expected_missing)
        self.check()
        return result

    def close(self):
        # Only terminate processes launched here; enclosing Job owns whole-tree closure.
        for label, row in list(self.live.items()):
            try:
                if row["process"].poll() is None:
                    row["process"].terminate()
                    self.cleanup.append({"operation": label, "action": "TERMINATED_EXACT_CHILD"})
                row["process"].wait(timeout=max(0.1, min(5, self.cleanup_deadline-time.monotonic())))
                self.collect(label, validate=False)
            except BaseException as error:
                self.cleanup.append({"operation": label, "error_type": type(error).__name__, "error": str(error)})
                if row["process"].poll() is None:
                    row["process"].kill()
                for handle in row["handles"]:
                    handle.close()


def pinned(path, pin, maximum=4*MIB):
    raw = read(path, maximum)
    need(pin == {"bytes": len(raw), "sha256": digest(raw)}, "LIBRARY_CHECK_RETURNED_PIN")
    return raw


def actual_proof_use(completion, directory):
    """Inspect returned checked bytes, not metadata-only or text-name occurrence."""
    units = {}
    for item in completion["units"]:
        path = directory/"evidence"/(item["unit_id"]+".json")
        need(Path(item["file"]) == path, "LIBRARY_CHECK_EVIDENCE_PATH")
        raw = pinned(path, {key: item[key] for key in ("bytes", "sha256")})
        need(digest(b"DMKN-ORDINARY-EVIDENCE-V2\0"+raw) == item["unit_id"], "LIBRARY_CHECK_UNIT_ID")
        doc = json.loads(raw)
        need(doc["semantic_id"] == SEMANTIC, "LIBRARY_CHECK_EVIDENCE_SEMANTICS")
        descriptor = doc["unit"][1]
        need(descriptor[0] == 1 and len(descriptor) == 6, "LIBRARY_CHECK_THEOREM_DESCRIPTOR")
        units[canonical(descriptor[1])] = (item["unit_id"], doc)
    wanted, library = name("CommonsLibraryExample.add_zero"), name("Nat.add_zero")
    need(set(units) == {canonical(wanted), canonical(library)}, "LIBRARY_CHECK_EXACT_TWO_THEOREMS")
    supplier_id, supplier = units[canonical(library)]
    consumer_id, consumer = units[canonical(wanted)]
    supplied_export = digest(b"DMKN-ORDINARY-EXPORT-V2\0"+canonical([SEMANTIC, supplier_id, library]))
    need([library, supplied_export] in consumer["imports"], "LIBRARY_CHECK_EXACT_SUPPLEMENT_IMPORT")
    proof_nodes = consumer["unit"][1][4][2]
    need(any(node[0] == 2 and node[1] == library for node in proof_nodes), "LIBRARY_CHECK_PROOF_REFERENCES_LEMMA")
    need(not any(row[0] == library for row in supplier["imports"]), "LIBRARY_CHECK_NO_SELF_IMPORT")
    target = completion["targets"]
    need(len(target) == 1 and target[0]["name"] == wanted and target[0]["unit_id"] == consumer_id and
         target[0]["export_id"] == digest(b"DMKN-ORDINARY-EXPORT-V2\0"+canonical([SEMANTIC, consumer_id, wanted])),
         "LIBRARY_CHECK_CONSUMER_PUBLICATION")
    need(len(completion["previews"]) == 1, "LIBRARY_CHECK_PREVIEW_COUNT")
    preview = completion["previews"][0]
    path = directory/"previews"/(target[0]["export_id"]+".json")
    need(Path(preview["file"]) == path, "LIBRARY_CHECK_PREVIEW_PATH")
    pinned(path, {key: preview[key] for key in ("bytes", "sha256")})
    return {"supplier_unit_id": supplier_id, "supplier_export_id": supplied_export,
            "consumer_unit_id": consumer_id, "consumer_export_id": target[0]["export_id"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("package", "profile-sha256", "output"):
        parser.add_argument("--"+option, required=True)
    args = parser.parse_args()
    package, output = Path(args.package), Path(args.output)
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and
         not sys.flags.optimize and Path(sys.executable) == PYTHON, "LIBRARY_CHECK_PYTHON")
    ordinary(package, directory=True); ordinary(output, directory=True)
    need(package.is_relative_to(LOCAL) and output.is_relative_to(LOCAL) and
         all(not output.is_relative_to(other) and not other.is_relative_to(output) for other in (OLD, package)),
         "LIBRARY_CHECK_DISJOINT_OUTPUT")
    run = Run(package, args.profile_sha256, output)
    report = {"status": "FAILED", "phase": "INPUTS", "calls": run.calls,
        "claim": "PUBLIC_MISSING_LIBRARY_COMPLETION_NOT_GROWTH_OR_GENERAL_LIBRARY_SUPPORT",
        "outer_job_required_for_final_tree_quiescence": True}
    preserved = None
    try:
        profile_raw = read(package/"PROFILE.json", 2*MIB)
        need(digest(profile_raw) == args.profile_sha256, "LIBRARY_CHECK_PROFILE_PIN")
        previous_raw = read(OLD/"RECIPROCAL-RESULT.json", 2*MIB)
        need(digest(previous_raw) == PREVIOUS_SHA, "LIBRARY_CHECK_PREVIOUS_PIN")
        previous = json.loads(previous_raw)
        need(previous["status"] == "PASS_PUBLIC_CLI_RECIPROCAL_SEAM" and previous["B_basis"] == PARENT,
             "LIBRARY_CHECK_EXISTING_BASIS")
        adoption = json.loads(read(OLD/"B-catalog/ADOPTION.json", MIB))
        need(adoption["store_id"] == STORE and adoption["implementation"]["semantic_id"] == SEMANTIC,
             "LIBRARY_CHECK_EXISTING_ADOPTION")
        preserved = retained_map(); save(output/"PRESERVED-BEFORE.json", preserved)
        save(output/"CallerBody.lean", BODY); save(output/"acquired.json", [])
        save(output/"outputs.json", [name("CommonsLibraryExample.add_zero")])
        save(output/"modules.json", [name("Std.Data.Internal.List.Defs")])
        contribution, extraction, completion = (output/part for part in ("contribution", "extraction", "completion"))
        report["phase"] = "EXPECTED_MISSING_LIBRARY"
        first = run.call("contribute", ("--source", str(output/"CallerBody.lean"),
            "--acquired-targets", str(output/"acquired.json"), "--output-names", str(output/"outputs.json"),
            "--output", str(contribution)), expected_missing=True)
        authoring = clean_native(contribution/"AUTHORING-SUPERVISION.json")
        need(first["detail"]["native_cpu_seconds"] == authoring["final_job"]["cpu_seconds"] and
             first["cost"]["worker_cpu_seconds"] == authoring["final_job"]["cpu_seconds"],
             "LIBRARY_CHECK_FAILED_AUTHORING_FULLY_CHARGED")
        need(json.loads(read(contribution/"FAILURE.json", MIB)) == first["detail"], "LIBRARY_CHECK_FAILURE_RETAINED")
        candidate_raw, request_raw = read(contribution/"candidate.json"), read(contribution/"REQUEST.json", MIB)
        report["expected_refusal"] = first["detail"]
        report["phase"] = "EXTRACTION_ONLY"
        extracted = run.call("extract-std", ("--retained-contribution", str(contribution),
            "--retained-request-sha256", digest(request_raw), "--retained-candidate-sha256", digest(candidate_raw),
            "--library-modules", str(output/"modules.json"), "--output", str(extraction)))["result"]
        need(extracted["status"] == "EXTRACTED_COMPLETION_INPUTS_NOT_ACCEPTED" and
             extracted["mathematical_acceptance"] is False and extracted["parent_root"] == PARENT and
             extracted["missing_targets"] == [name("Nat.add_zero")] and
             extracted["supplemental_units"] == 1 and extracted["consumer_units"] == 1,
             "LIBRARY_CHECK_INERT_EXACT_EXTRACTION")
        supervision = clean_native(extraction/"EXTRACTION-SUPERVISION.json", extraction=True)
        need(extracted["native_cpu_seconds"] == supervision["native_cpu_seconds"] ==
             run.calls[-1]["result"]["cost"]["worker_cpu_seconds"], "LIBRARY_CHECK_EXTRACTION_CPU")
        pins = extracted["pins"]
        for key, filename in (("candidate", "candidate.json"), ("targets", "targets.json"),
                ("prepared_bindings", "prepared-bindings.json"), ("extraction_request", "request.json"),
                ("supplement", "supplement.json")):
            pinned(extraction/filename, pins[key])
        need(read(extraction/"candidate.json") == candidate_raw and
             json.loads(read(extraction/"targets.json")) == [name("CommonsLibraryExample.add_zero")],
             "LIBRARY_CHECK_RETAINED_CANDIDATE_AND_TARGETS")
        report["phase"] = "COMBINED_NATIVE_ACCEPTANCE"
        completed = run.call("complete", ("--candidate", str(extraction/"candidate.json"),
            "--candidate-sha256", pins["candidate"]["sha256"], "--supplement", str(extraction/"supplement.json"),
            "--supplement-sha256", pins["supplement"]["sha256"], "--prepared-bindings", str(extraction/"prepared-bindings.json"),
            "--prepared-bindings-sha256", pins["prepared_bindings"]["sha256"],
            "--output-names", str(extraction/"targets.json"), "--output", str(completion)))["result"]
        # Retain acceptance before checking further test assertions: failure is not rollback.
        report["admission"] = completed.get("admission")
        admission = completed["admission"]
        need(completed["status"] == "CHECKED_COMPLETION_WITH_DURABLE_PUBLICATION_BYTES" and
             completed["parent_root"] == PARENT and completed["local_root"] != PARENT and
             admission["status"] == "CHECKED" and admission["units_checked"] == len(completed["units"]) == 2 and
             admission["local_root"] == completed["local_root"] and completed["semantic_id"] == SEMANTIC and
             completed["candidate_sha256"] == digest(candidate_raw) and
             completed["supplement_sha256"] == pins["supplement"]["sha256"], "LIBRARY_CHECK_NEW_CHECKED_COMPLETION")
        operation = Path(admission["operation_directory"])
        need(operation.parent == OLD/"B-catalog/admission-calls", "LIBRARY_CHECK_ADMISSION_OPERATION")
        admission_supervision = clean_native(operation/"supervision-result.json")
        need(admission["retained_unit_ids"] == [item["unit_id"] for item in completed["units"]],
             "LIBRARY_CHECK_ADMITTED_EXACT_RETURNED_UNITS")
        need(completed["native_cpu_seconds"] == admission["worker_cpu_seconds"] ==
             admission_supervision["final_job"]["cpu_seconds"] ==
             run.calls[-1]["result"]["cost"]["worker_cpu_seconds"], "LIBRARY_CHECK_ADMISSION_CPU")
        report["actual_proof_use"] = actual_proof_use(completed, completion)
        need(read(contribution/"candidate.json") == candidate_raw and
             read(contribution/"REQUEST.json", MIB) == request_raw and
             read(package/"PROFILE.json", 2*MIB) == profile_raw, "LIBRARY_CHECK_INPUTS_UNCHANGED")
        run.check()
        report.update(status="PASS_PUBLIC_MISSING_LIBRARY_COMPLETION", phase="COMPLETE",
                      local_root=completed["local_root"], source_sha256=digest(BODY))
    except BaseException as error:
        report.update(error_type=type(error).__name__, error=str(error))
    finally:
        run.close()
        if run.cleanup or run.live:
            report["status"] = "FAILED"
        report["cleanup"] = run.cleanup
        if preserved is not None:
            try:
                after = retained_map(); save(output/"PRESERVED-AFTER.json", after)
                need(after == preserved, "LIBRARY_CHECK_PRIOR_BRANCH_ARTIFACTS_CHANGED")
                report["prior_branch_artifacts_preserved"] = True
            except BaseException as error:
                report.update(status="FAILED", preservation_error=str(error))
        report.update(wall_seconds=time.monotonic()-run.started,
            charged_child_cpu_seconds=run.charged_cpu, harness_cpu_seconds=time.process_time()-run.cpu_started,
            cost_scope="Original expected refusal is charged. Outer Job aggregate is authoritative; do not add child receipts twice.")
        if report["wall_seconds"] >= 210 or run.charged_cpu+report["harness_cpu_seconds"] >= 140:
            report.update(status="FAILED", final_budget_error="LIBRARY_CHECK_ORIGINAL_ALLOWANCE")
        save(output/"LIBRARY-NATIVE-RESULT.json", report)
        print(json.dumps({"status": report["status"], "calls": len(run.calls), "wall_seconds": report["wall_seconds"]}), flush=True)
    return 0 if report["status"] == "PASS_PUBLIC_MISSING_LIBRARY_COMPLETION" else 1


if __name__ == "__main__":
    raise SystemExit(main())
