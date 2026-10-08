"""One selected real guest execution, before any cryptographic proof allocation.

Owner-only cost screen, run inside the selected Windows Job supervisor. This is
not a public verifier, hostile-source sandbox, or module-admission authority.
The host prepares the framed input; this adapter independently checks its bytes
and journal before executing the exact adopted image once. No parent receipts
are permitted in this first base-module screen.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from modules.receipt.witness import decode_journal


def pinned(path, digest, maximum):
    path = Path(path)
    C.require(path.is_absolute() and path.is_file() and 0 < path.stat().st_size <= maximum,
              "SELECTED_FILE_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum + 1)
    C.require(len(raw) <= maximum and hashlib.sha256(raw).hexdigest() == digest, "SELECTED_FILE_HASH")
    return raw


def save(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def main():
    parser = argparse.ArgumentParser()
    for key in ("host", "host-sha", "image", "image-sha", "image-id", "input", "input-sha", "output"):
        parser.add_argument("--" + key, required=True)
    parser.add_argument("--cycles", type=int, required=True)
    parser.add_argument("--po2", type=int, required=True)
    args = parser.parse_args()
    C.require(re.fullmatch(r"[0-9a-f]{64}", args.image_id) is not None, "ADOPTED_IMAGE_ID")
    C.require(args.cycles == 2**25 and args.po2 == 18, "EXACT_EXECUTE_SCREEN_LIMITS")
    paths = ((args.host, args.host_sha, 128 * 1024**2),
             (args.image, args.image_sha, 64 * 1024**2), (args.input, args.input_sha, 2**20))
    for path, digest, maximum in paths:
        pinned(path, digest, maximum)
    raw = pinned(args.input, args.input_sha, 2**20)
    request = C.parse_json(raw)
    C.require(request["parents"] == [] and request["rank"] == 0, "BASE_WITHOUT_PARENTS_ONLY")
    module = C.module_id(request["local_spec"])
    out = Path(args.output)
    C.require(out.is_absolute() and not out.exists(), "FRESH_SCREEN_EVIDENCE")
    out.mkdir()
    report = {"schema": "DMKN_MODULE_EXECUTION_SCREEN_V1", "status": "FAIL",
              "mathematical_admission": False, "proof_calls": 0, "guest_execute_calls": 0,
              "module_id": module, "image_id": args.image_id, "cycles_cap": args.cycles,
              "segment_po2": args.po2, "calls": []}

    def call(label, argv, timeout):
        try:
            result = subprocess.run([args.host, *argv], capture_output=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired as error:
            stdout, stderr = error.stdout or b"", error.stderr or b""
            save(out / (label + ".stdout"), stdout[:2**20])
            save(out / (label + ".stderr"), stderr[:2**20])
            report["calls"].append({"command": label, "status": "TIMEOUT",
                                    "stdout_bytes": len(stdout), "stderr_bytes": len(stderr)})
            raise
        save(out / (label + ".stdout"), result.stdout[:2**20])
        save(out / (label + ".stderr"), result.stderr[:2**20])
        report["calls"].append({"command": label, "exit_code": result.returncode,
                                "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr)})
        C.require(len(result.stdout) <= 2**20 and len(result.stderr) <= 2**20, "SCREEN_OUTPUT_BOUND")
        C.require(result.returncode == 0, "HOST_COMMAND_FAILED:" + label)
        return result.stdout

    try:
        frame, expected = out / "base.frame", out / "base.expected-journal"
        prepared = C.parse_json(call("prepare", ["prepare", args.image, args.input,
                                                 str(frame), str(expected)], 30))
        C.require(prepared["status"] == "PREPARED_ONLY_NOT_CERTIFIED"
                  and prepared["mathematical_admission"] is False, "PREPARATION_NOT_AUTHORITY")
        image_bytes = bytes.fromhex(args.image_id)
        words = [int.from_bytes(image_bytes[i:i+4], "little") for i in range(0, 32, 4)]
        request["image"] = words
        payload = C.canonical(request)
        C.require(frame.stat().st_size == 4 + len(payload)
                  and frame.read_bytes() == len(payload).to_bytes(4, "little") + payload,
                  "EXACT_REPINNED_FRAME")
        C.require(expected.stat().st_size == 216, "EXPECTED_JOURNAL_BOUND")
        journal = expected.read_bytes()
        parsed = decode_journal(journal)
        C.require(parsed["image"] == words and parsed["module"] == module
                  and parsed["summary"] == C.summarize(request["local_spec"])
                  and parsed["rank"] == 0 and parsed["witness"] == C.hash_value("module-witness", request),
                  "INDEPENDENT_EXACT_EXPECTED_JOURNAL")
        C.require(prepared["image"] == words and prepared["module"] == module
                  and prepared["rank"] == 0 and prepared["witness"] == parsed["witness"],
                  "PREPARATION_OUTPUT_BINDING")
        report["guest_execute_calls"] = 1
        actual = call("execute", ["execute", args.image, str(frame), str(expected),
                                   str(args.cycles), str(args.po2)], 150).decode("utf-8").strip()
        pattern = (r"EXECUTED_ONLY_NOT_A_CERTIFICATE image_id=([0-9a-f]{64}) rank=(\d+) groups=(\d+) "
                   r"parent_bytes=(\d+) parents=(\d+) segments=(\d+) rows=(\d+) padded_rows=(\d+) "
                   r"padding_rows=(\d+) instructions=(\d+)")
        match = re.fullmatch(pattern, actual)
        C.require(match is not None and match[1] == args.image_id, "ACTUAL_EXECUTION_RECORD")
        keys = ("rank", "groups", "parent_bytes", "parents", "segments", "rows", "padded_rows",
                "padding_rows", "instructions")
        metrics = dict(zip(keys, map(int, match.groups()[1:])))
        C.require(metrics["rank"] == metrics["parents"] == metrics["parent_bytes"] == 0
                  and metrics["groups"] == parsed["group_count"]
                  and 1 <= metrics["segments"] <= 128, "EXECUTION_SCOPE")
        report.update(status="PASS_REAL_GUEST_EXECUTION_ONLY", metrics=metrics,
                      input_frame_bytes=frame.stat().st_size, expected_journal_sha256=hashlib.sha256(journal).hexdigest())
    except BaseException as error:
        report.update(status="FAIL", error={"type": type(error).__name__, "message": str(error)[:2000]})
    try:
        for path, digest, maximum in paths:
            pinned(path, digest, maximum)
    except BaseException as error:
        report.update(status="FAIL_FINAL_BINDING", binding_error=str(error)[:2000])
    save(out / "RESULT.json", C.canonical(report))
    print(json.dumps(report), flush=True)
    return 0 if report["status"] == "PASS_REAL_GUEST_EXECUTION_ONLY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
