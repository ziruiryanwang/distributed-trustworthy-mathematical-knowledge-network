"""Selected original-source reuse and new inert export in one owner process.

The prepared request is authenticated local controller input, not a peer warrant.
The selected mode constructs a candidate in the owner's ordinary environment;
it does not assert whole-owner semantic correspondence. Acquired theorem
signatures and any compiled authoring artifact are not receiver acceptance.
This builds no prerequisite and never imports the producer module. It retains
the substantive existing consumer proof body verbatim. A successful source
compile/export is NOT independent receiver acceptance or a growth measurement.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT / "experiments/v5-local-checks"
LEAN = ROOT / "software/runtime/lean-4.34.0-windows/bin/lean.exe"
PREPARE = LOCAL / "ordinary-owner-consumer-02"
PREPARE_SHA = "09477faa163f9e2a6071d479552367650a41ac13218f70d66f8159740cb04d23"
PROFILE = "fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219"
CONTEXT = "4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026"
BASIS = "cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299"
TARGET = "DMKN.ReadFootprint.Consumer.snapshot_predicate_applyBatches"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_request():
    raw = (PREPARE / "PREPARE-RESULT.json").read_bytes()
    need(sha(raw) == PREPARE_SHA, "ADOPTED_PREPARATION_PIN")
    manifest = json.loads(raw)
    need(manifest["profile_id"] == PROFILE and manifest["context_id"] == CONTEXT,
         "ADOPTED_REQUEST_CONTEXT")
    directory = PREPARE / "owner-request"
    files = manifest["request_files"]
    need(type(files) is dict and len(files) == 388, "REQUEST_FILE_COUNT")
    need({p.name for p in directory.iterdir()} == set(files), "REQUEST_FILE_CENSUS")
    total = 0
    for name, expected in files.items():
        need(name == "header.json" or re.fullmatch(r"group-[0-9]{5}\.json", name),
             "FIXED_REQUEST_FILENAME")
        path = directory / name
        need(path.resolve() == path and path.is_file() and path.stat().st_size <= 8388608,
             "REQUEST_PATH_OR_BOUND")
        with path.open("rb") as stream:
            data = stream.read(8388609)
        need(len(data) <= 8388608 and
             {"bytes": len(data), "sha256": sha(data)} == expected, "REQUEST_FILE_PIN")
        total += len(data)
        need(total <= 67108864, "REQUEST_TOTAL_BOUND")
    need(total == 4549204, "ADOPTED_REQUEST_PAYLOAD")
    return directory, manifest, raw


def reuse_prepared_request(output, original_directory, manifest, manifest_raw):
    """Reuse the adopted projection byte-for-byte; do not recalculate its closure."""
    request = output / "owner-request"
    request.mkdir()
    files = manifest["request_files"]
    for name, expected in files.items():
        with (original_directory / name).open("rb") as stream:
            raw = stream.read(8388609)
        need({"bytes": len(raw), "sha256": sha(raw)} == expected, "REUSED_REQUEST_COPY_PIN")
        with (request / name).open("xb") as stream:
            stream.write(raw)
    with (output / "PREPARE-RESULT.json").open("xb") as stream:
        stream.write(manifest_raw)
    print(json.dumps({"phase": "REUSED_ADOPTED_PROJECTED_REQUEST", "manifest_sha256": PREPARE_SHA,
                      "payload_bytes": manifest["payload_bytes"]}), flush=True)
    return request, files


def verify_projected(directory, files):
    need({p.name for p in directory.iterdir()} == set(files), "PROJECTED_FILE_CENSUS")
    for name, expected in files.items():
        path = directory / name
        need(path.resolve() == path and path.stat().st_size == expected["bytes"],
             "PROJECTED_PATH_OR_SIZE")
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        need(digest == expected["sha256"], "PROJECTED_FILE_CHANGED")


def main():
    source = Path(__file__).resolve().parent
    output = Path(sys.argv[1])
    previous = [Path(part) for part in sys.argv[2].split(os.pathsep)]
    need(len(sys.argv) == 3 and Path.cwd() == ROOT and
         source.parents[2] == output / "sources" and output.is_relative_to(LOCAL),
         "SELECTED_SNAPSHOT_INVOCATION")
    need(1 <= len(previous) <= 8 and all(p.is_absolute() and p.is_relative_to(LOCAL)
         and p.resolve() == p and p.is_dir() for p in previous), "SELECTED_HELPER_PATHS")
    original_request, manifest, manifest_raw = verify_request()
    request, request_files = reuse_prepared_request(output, original_request, manifest, manifest_raw)
    verify_projected(request, request_files)
    original = (source / "examples/ReadFootprintConsumer.lean").read_bytes()
    first, separator, body = original.partition(b"\n")
    need(separator and first.rstrip(b"\r") == b"import examples.ReadFootprint",
         "EXACT_ORIGINAL_CONSUMER_HEADER")
    owner_source = output / "owner-source"
    build = output / "lean-build"
    owner_source.mkdir()
    build.mkdir()
    # JSON string quoting agrees with Lean for these bounded ASCII paths/IDs.
    quote = lambda value: json.dumps(str(value), ensure_ascii=True)
    header = ("module\n\npublic import Std.Data.ExtHashMap.Lemmas\n"
              "public import OwnerConstructCommand\npublic import ConstructExportCommand\n\n"
              "public section\n\n"
              f"#ordinary_construct {quote(request)} {quote(PROFILE)} {quote(CONTEXT)} {quote(BASIS)}\n")
    footer = f"\n#ordinary_export_constructed {TARGET} {quote(output / 'consumer-export.json')}\n"
    generated = header.encode() + body + footer.encode()
    target = owner_source / "AcquiredReadFootprintConsumer.lean"
    with target.open("xb") as stream:
        stream.write(generated)
    source_map = {"original_sha256": sha(original), "retained_body_sha256": sha(body),
                  "generated_sha256": sha(generated), "requested_target": TARGET,
                  "producer_imported": False, "prepared_request_sha256": PREPARE_SHA,
                  "construction_mode": "receiver-interpreted-candidate",
                  "whole_owner_correspondence_claimed": False, "receiver_policy_changed": False}
    with (output / "CONSUMER-SOURCE-MAP.json").open("x", encoding="utf-8") as stream:
        json.dump(source_map, stream, indent=2)
    env = dict(os.environ)
    for key in ("LEAN_PATH", "LEAN_SYSROOT", "LEAN_SRC_PATH"):
        env.pop(key, None)
    env["LEAN_PATH"] = os.pathsep.join(map(str, [build, *previous]))
    argv = [str(LEAN), "-DElab.async=false", "-R", str(owner_source),
            "-o", str(build / "AcquiredReadFootprintConsumer.olean"), str(target)]
    start = time.monotonic()
    with (output / "consumer.stdout.txt").open("xb") as stdout, \
         (output / "consumer.stderr.txt").open("xb") as stderr:
        result = subprocess.run(argv, cwd=ROOT, env=env, stdout=stdout, stderr=stderr, timeout=120)
    step = {"argv": argv, "exit_code": result.returncode, "wall_seconds": time.monotonic() - start}
    print(json.dumps(step), flush=True)
    verify_request()
    verify_projected(request, request_files)
    need(result.returncode == 0, "OWNER_CONSUMER_COMPILE_OR_EXPORT_FAILED")
    exported = output / "consumer-export.json"
    need(exported.is_file() and 0 < exported.stat().st_size <= 67108864, "SUCCESSOR_EXPORT_REQUIRED")
    with exported.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    report = {"status": "PASS_OWNER_SOURCE_USE_AND_INERT_SUCCESSOR_EXPORT", "step": step,
              "export_bytes": exported.stat().st_size, "export_sha256": digest,
              "claims": "NOT_RECEIVER_ACCEPTANCE_DISCOVERY_OR_GROWTH_EVIDENCE"}
    with (output / "CONSUMER-RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)
    print(json.dumps(report), flush=True)


if __name__ == "__main__":
    main()
