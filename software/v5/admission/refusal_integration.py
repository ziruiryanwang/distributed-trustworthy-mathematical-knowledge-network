"""One actual malformed-receipt refusal through the new public adapter.

No successful receipt, guest execution, proof production or network request.
The second attempted call must refuse from aggregate budgets before any child.
"""
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from admission.bindings import journal
from admission.verifier import ReceiptVerifier

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
BASE = ROOT / "product-local/v4-library-commons-02/commons-v4"
MANIFEST_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
HOST = ROOT / "experiments/v5-local-checks/module-host-build-02/module_host.exe"
HOST_SHA = "5d5e738f125b189ae424e4b94076b2e6660239a714c4f6ffab341a881136cb74"
JOURNAL = ROOT / "experiments/v5-local-checks/module-base-execute-01/evidence/base.expected-journal"
JOURNAL_SHA = "18d6f4837b81681649f0b80046be2a9510d32019e8508190bb799d466c3344d5"
IMAGE = "d9572ba4c2336c1544cae3fba652cc66f47b70144c4051d3a57dd2e25af161bb"


def sha(path):
    with path.open("rb") as stream: return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()+b"\n"
    with path.open("xb") as stream: stream.write(raw)


def main():
    C.require(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
              and sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 2,
              "CANONICAL_ISOLATED_REFUSAL_CHECK")
    output = Path(sys.argv[1])
    C.require(output.is_absolute() and output.resolve() == output and not output.exists()
              and output.is_relative_to(ROOT / "experiments/v5-local-checks"), "FRESH_REFUSAL_OUTPUT")
    C.require(sha(HOST) == HOST_SHA and sha(JOURNAL) == JOURNAL_SHA, "RETAINED_HOST_JOURNAL_PINS")
    expected = journal(JOURNAL.read_bytes())
    C.require(bytes.fromhex(IMAGE) == b"".join(word.to_bytes(4, "little") for word in expected["image"]),
              "FIXTURE_ACTUAL_IMAGE")
    output.mkdir()
    result = {"status": "FAIL", "schema": "DMKN_PUBLIC_ADMISSION_REFUSAL_TEST_V1",
              "guest_executions": 0, "proof_calls": 0, "network_calls": 0,
              "mathematical_admissions": 0, "scope": "ACTUAL_MALFORMED_RECEIPT_REFUSAL_ONLY"}
    verifier = None
    try:
        verifier = ReceiptVerifier(supervisor_manifest=BASE / "RELEASE-MANIFEST.json",
            supervisor_manifest_sha256=MANIFEST_SHA, executable=HOST,
            runtime_pins={str(HOST): {"bytes": 66654208, "sha256": HOST_SHA}},
            image_id=IMAGE, foundation=expected["foundation"], policy=expected["policy"],
            operations=1, submitted_bytes=1024, reserved_cpu_seconds=15, wall_seconds=45)
        C.require(verifier.report()["attempts"] == 0, "EMPTY_ADMISSION_START")
        malformed = b"\xff\xff\xff\xff"
        try:
            verifier.receive(malformed, expected["summary"], output / "receive",
                             cpu_seconds=15, wall_seconds=30, memory_mib=512)
        except ValueError as error:
            C.require(str(error) == "ADMISSION_VERIFIER_REFUSED", "EXACT_REAL_VERIFIER_REFUSAL")
        else: raise AssertionError("malformed receipt admitted")
        process = json.loads((output / "receive/process.json").read_bytes())
        C.require(process["status"] == "COMMAND_FAILED" and process["child_exit_code"] != 0
                  and process["direct_child_reaped"] is True and process["job_closed"] is True
                  and process["cleanup_errors"] == [] and process["termination_requested"] is False
                  and process["final_job"]["active_processes"] == 0
                  and process["final_job"]["terminated_processes"] == 0, "CLEAN_ACTUAL_REFUSAL_PROCESS")
        C.require(process["argv"] == [str(HOST), "receive", IMAGE,
                    str(output / "receive/receipt.bin"), expected["module"]], "EXACT_RECEIVE_COMMAND")
        C.require((output / "receive/receipt.bin").read_bytes() == malformed
                  and not (output / "receive/binding.json").exists(), "NO_ACCEPTANCE_EVIDENCE")
        first = verifier.report()
        C.require(first["attempts"] == 1 and first["submitted_bytes"] == 4
                  and first["reserved_cpu_seconds"] == 15 and first["live_handles"] == 0,
                  "FAILED_CALL_CHARGED_NO_HANDLE")
        try:
            verifier.receive(malformed, expected["summary"], output / "forbidden-second",
                             cpu_seconds=15, wall_seconds=30, memory_mib=512)
        except ValueError as error:
            C.require(str(error) == "ADMISSION_AGGREGATE_BUDGET", "NO_HIDDEN_BUDGET_RENEWAL")
        else: raise AssertionError("second receipt process authorized")
        C.require(not (output / "forbidden-second").exists() and verifier.report() == first,
                  "SECOND_ATTEMPT_MADE_NO_PROCESS_OR_STATE")
        C.require(sha(HOST) == HOST_SHA and sha(JOURNAL) == JOURNAL_SHA, "RETAINED_INPUTS_UNCHANGED")
        result.update(status="PASS", actual_verifier_invocations=1,
                      second_attempt="REFUSED_BEFORE_PROCESS", accounting=first, process=process)
    except BaseException as error:
        result.update(error={"type": type(error).__name__, "message": str(error)[:1000]})
    finally:
        if verifier is not None:
            verifier.close(); result["closed_accounting"] = verifier.report()
        save(output / "RESULT.json", result)
    print(json.dumps({key: result.get(key) for key in ("status", "actual_verifier_invocations", "error")}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__": raise SystemExit(main())
