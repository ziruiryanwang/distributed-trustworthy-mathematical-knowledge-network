"""One exact old-I prepare/execution capsule; no proof, retry or new producer lane.

Run only through the selected finite outer Job. Saved native admission fixes
expected bytes, not portable authority; the real host checks the genuine parent
receipt and guest conclusion. The existing host may normalize the image field,
so byte-identical prepared payload and independently retained J are mandatory.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C
from modules.receipt.witness import decode_journal

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
MIB, CYCLES, PO2 = 1024**2, 2**25, 18
IMAGE = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
BASE = "2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e"
MODULE = "bbf0845d2622374699a93a9d8ccc6e565dd1c985e72441ec0eeae41bb03fc0c5"
J_SHA = "e1b67f57ac9612a20b33231c2b71b2bd9260e6f4eb50fa9d0d761cd80408fbed"
PINS = {
    "host": "74a58215351a641d9efbbffbc389b5faea350c46f5c1e1a48bf76cf77b99d6c9",
    "image": "d76f623bb1de5c840fd2ef9c1ac35fc6aba2de74cda0f62c11c161f6973da31f",
    "witness": "8b84084486b0aadceb9ee353a28654b2777e297a726693135c575d5c50e85f5a",
    "receipt": "850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47",
    "accepted_result": "adc7fe79bf6870c01c00df4fdd68567129b3d20217c938a4b125d8b7616ac9e3",
}


def ordinary(value, fresh=False):
    path = Path(value)
    C.require(path.is_absolute() and path != Path(path.anchor) and path.resolve() == path,
              "CANONICAL_NONROOT_PATH")
    for item in ((path.parent if fresh else path), *path.parents):
        C.require(not item.is_symlink() and not item.is_junction(), "ORDINARY_PATH")
    C.require(not os.path.lexists(path) if fresh else path.exists(), "FRESH_OR_PRESENT_PATH")
    return path


def read(path, maximum=MIB):
    path = ordinary(path)
    C.require(path.is_file() and 0 < path.stat().st_size <= maximum, "READ_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    C.require(0 < len(raw) <= maximum and len(raw) == path.stat().st_size, "READ_CHANGED")
    return raw


def pin(path):
    path = ordinary(path)
    size = path.stat().st_size
    C.require(path.is_file() and 0 < size <= 128*MIB, "PIN_BOUND")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    C.require(path.stat().st_size == size, "PIN_CHANGED")
    return {"path": str(path), "bytes": size, "sha256": digest}


def save(path, raw):
    ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def main():
    started = time.monotonic()
    C.require(os.name == "nt" and Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
        and sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 3,
        "SELECTED_ISOLATED_OUTER_JOB_REQUIRED")
    configuration = ordinary(sys.argv[1]); cfg_raw = read(configuration)
    C.require(hashlib.sha256(cfg_raw).hexdigest() == C.digest_string(sys.argv[2]), "CONFIG_PIN")
    cfg = C.parse_json(cfg_raw)
    C.fields(cfg, {"schema", "host", "image", "witness", "receipt", "accepted_result", "output"})
    C.require(cfg["schema"] == "DMKN_EVALUATOR_SNAPSHOT_SCREEN_V1", "CONFIG_SCHEMA")
    def rebind():
        C.require(time.monotonic()-started < 200 and read(configuration) == cfg_raw, "ORIGINAL_DEADLINE_OR_CONFIG")
        for name, digest in PINS.items():
            C.fields(cfg[name], {"path", "bytes", "sha256"})
            C.require(cfg[name]["sha256"] == digest and pin(cfg[name]["path"]) == cfg[name], "INPUT_PIN:"+name)
    rebind()
    raw = read(cfg["witness"]["path"]); witness = C.parse_json(raw)
    accepted = json.loads(read(cfg["accepted_result"]["path"]))
    expected = bytes(accepted["checked_output"]["journal"]); journal = decode_journal(expected)
    words = [int.from_bytes(bytes.fromhex(IMAGE)[i:i+4], "little") for i in range(0, 32, 4)]
    C.require(accepted["status"] == "COMPLETED" and accepted["client_closed"] and accepted["workspace_closed"]
        and not accepted["cleanup_errors"] and hashlib.sha256(expected).hexdigest() == J_SHA
        and journal["module"] == MODULE and journal["rank"] == 1 and journal["image"] == words,
        "EXACT_INDEPENDENTLY_ACCEPTED_JOURNAL")
    C.require(raw == C.canonical(witness) and len(raw) == 50017 and len(witness["rows"]) == 697
        and witness["schema"] == "DMKN_CERTIFIED_MODULES_V2" and witness["image"] == words
        and witness["rank"] == 1 and C.summarize(witness["local_spec"]) == journal["summary"]
        and len(witness["parents"]) == 1 and len(witness["bodies"]) == 2, "EXACT_UNCHANGED_WITNESS")
    parent = bytes(witness["parents"][0]["journal"]); parent_j = decode_journal(parent)
    C.require(parent == bytes(accepted["parent"]["journal"]) and parent_j["module"] == BASE
        and parent_j["image"] == words and parent_j["rank"] == 0
        and [x["index"] for x in witness["parents"][0]["openings"]] == [0, 10], "EXACT_BASE_PARENT")
    output = ordinary(cfg["output"], fresh=True)
    C.require(output.parent.is_dir() and output.is_relative_to(ROOT/"experiments/v5-local-checks"), "OUTPUT_SCOPE")
    for name in PINS:
        C.require(not Path(cfg[name]["path"]).is_relative_to(output), "OUTPUT_DISJOINT_INPUTS")
    output.mkdir(); save(output/"configuration.json", cfg_raw)
    frame, expected_path, capsule = output/"method.frame", output/"method.expected-journal", output/"method.snapshot"
    report = {"schema": "DMKN_EVALUATOR_SNAPSHOT_SCREEN_RESULT_V1", "status": "FAILED",
        "host_calls": 0, "proof_calls": 0, "mathematical_admission": False, "new_receipt": False,
        "cycles": CYCLES, "po2": PO2, "accepted_journal_sha256": J_SHA, "capsule": None, "error": None}
    def command(label, argv, timeout):
        C.require(label in ("prepare", "snapshot"), "CLOSED_COMMAND_SET")
        rebind(); report["host_calls"] += 1
        save(output/(label+"-command.json"), C.canonical({"argv": argv, "timeout_seconds": timeout}))
        environment = {key: value for key, value in os.environ.items() if not key.upper().startswith("RISC0_")}
        with (output/(label+"-stdout.txt")).open("xb") as stdout, (output/(label+"-stderr.txt")).open("xb") as stderr:
            result = subprocess.run(argv, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, timeout=min(timeout, 195-(time.monotonic()-started)),
                check=False, creationflags=subprocess.CREATE_NO_WINDOW)
        report[label+"_exit_code"] = result.returncode
        C.require((output/(label+"-stdout.txt")).stat().st_size <= MIB
            and (output/(label+"-stderr.txt")).stat().st_size <= MIB and result.returncode == 0, "HOST_COMMAND_FAILED:"+label)
        rebind(); return read(output/(label+"-stdout.txt"))
    try:
        host, image = cfg["host"]["path"], cfg["image"]["path"]
        prepared = C.parse_json(command("prepare", [host, "prepare", image, cfg["witness"]["path"], str(frame), str(expected_path)], 30))
        C.require(read(frame) == struct.pack("<I", len(raw))+raw and read(expected_path, 184) == expected,
                  "NO_IMAGE_OR_WITNESS_RELABELING_EXACT_ACCEPTED_J")
        C.require(prepared == {"status": "PREPARED_ONLY_NOT_CERTIFIED", "image": words,
            "module": MODULE, "rank": 1, "mathematical_admission": False}, "EXACT_PREPARE_REPLY")
        text = command("snapshot", [host, "stage", image, str(frame), str(expected_path), str(CYCLES), str(PO2),
            "snapshot", "0", str(capsule), "1", cfg["receipt"]["path"]], 150).decode("utf-8").strip()
        match = re.fullmatch(r"REAL_EXECUTION_SNAPSHOT_NOT_APPLICATION_CERTIFICATE schema=(\d+) snapshot_bytes=(\d+) segments=(\d+) assumptions=(\d+) binding=([0-9a-f]{64})", text)
        C.require(match is not None, "SNAPSHOT_REPLY")
        schema, size, segments, assumptions = map(int, match.groups()[:4]); capsule_pin = pin(capsule)
        C.require(schema == 3 and 0 < size <= 64*MIB and capsule_pin["bytes"] == size
            and 1 <= segments <= 128 and assumptions == 1, "COMPLETE_CAPSULE_CENSUS")
        with capsule.open("rb") as stream:
            C.require(stream.read(4) == struct.pack("<I", 3), "CAPSULE_SCHEMA")
        report.update(status="COMPLETE_EXECUTION_CAPSULE_NOT_CERTIFICATE", capsule=capsule_pin,
            session={"image": cfg["image"], "frame": pin(frame), "expected": pin(expected_path),
                "capsule": capsule_pin, "parents": [cfg["receipt"]], "binding": match[5], "cycles": CYCLES,
                "po2": PO2, "segments": segments, "assumptions": assumptions},
            production_graph={"segments": segments, "segment_calls": segments, "lift_calls": segments,
                "join_calls": segments-1, "resolve_calls": 1, "finish_calls": 1, "total_calls": 3*segments+1})
    except BaseException as error:
        report["error"] = type(error).__name__+": "+str(error)[:2000]
    try:
        rebind()
        if report["capsule"] is not None: C.require(pin(capsule) == report["capsule"], "FINAL_CAPSULE_CHANGED")
        if frame.exists(): C.require(read(frame) == struct.pack("<I", len(raw))+raw, "FINAL_FRAME_CHANGED")
        if expected_path.exists(): C.require(read(expected_path, 184) == expected, "FINAL_J_CHANGED")
        entries, total = 0, 0
        for directory, dirs, files in os.walk(output, followlinks=False):
            for name in dirs+files:
                path = ordinary(Path(directory)/name); entries += 1
                if name in files: total += path.stat().st_size
                C.require(entries+1 <= 160 and total+MIB <= 128*MIB, "OUTPUT_CENSUS")
    except BaseException as error:
        report.update(status="FAILED", final_error=type(error).__name__+": "+str(error)[:2000])
    report["wall_seconds_before_final_report"] = time.monotonic()-started
    save(output/"RESULT.json", json.dumps(report, sort_keys=True, separators=(",", ":"), allow_nan=False).encode())
    print(json.dumps(report), flush=True)
    return 0 if report["status"] == "COMPLETE_EXECUTION_CAPSULE_NOT_CERTIFICATE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
