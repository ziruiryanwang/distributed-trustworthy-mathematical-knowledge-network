"""Prepare exact file-only distribution inputs; no product import, build or copy."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
CHECKS = ROOT/"experiments/v5-local-checks"
NAME = "distribution-01"
MIB = 1024**2
BASE_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
REMOTE_SHA = "68af53270016f920822942cef153948eeacdca81b501dc461a1b8dec2a756483"


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def pin(path):
    need(path.is_absolute() and path.resolve() == path and path.is_file()
         and all(not part.is_symlink() and not part.is_junction()
                 for part in (path, *path.parents)), "ORDINARY_INPUT_PATH")
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while chunk := stream.read(MIB):
            count += len(chunk)
            need(count <= 512*MIB, "INPUT_FILE_BOUND")
            digest.update(chunk)
    need(count == path.stat().st_size, "INPUT_FILE_SIZE_CHANGED")
    return {"path": str(path), "bytes": count, "sha256": digest.hexdigest()}


def verify(row):
    need(type(row) is dict and set(row) == {"path", "bytes", "sha256"},
         "EXACT_PIN_FIELDS")
    need(pin(Path(row["path"])) == row, "SELECTED_INPUT_CHANGED:"+row["path"])
    return deepcopy(row)


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTION")
    need(len(sys.argv) == 2 and len(sys.argv[1]) == 64
         and all(c in "0123456789abcdef" for c in sys.argv[1]),
         "REVIEWED_DISTRIBUTION_SOURCE_SHA_REQUIRED")
    remote_path = CHECKS/"client-remote-check-01-plan.json"
    need(pin(remote_path)["sha256"] == REMOTE_SHA, "RETAINED_REMOTE_PLAN_CHANGED")
    remote = json.loads(remote_path.read_bytes())
    reader = remote["parameters"]["reader"]
    adoption = reader["runtime_adoption"]
    need(remote["owner_entry"] == "remote_check.py" and len(remote["sources"]) == 103,
         "EXACT_REMOTE_SOURCE_BASIS")
    base = Path(remote["installation_root"])
    manifest = pin(base/"RELEASE-MANIFEST.json")
    need(manifest["bytes"] == 1070384 and manifest["sha256"] == BASE_SHA,
         "EXACT_NESTED_BASE_MANIFEST")
    files = json.loads(Path(manifest["path"]).read_bytes())["files"]
    need(len(files) == 6652 and sum(row["bytes"] for row in files.values()) == 235662448,
         "EXACT_BASE_PAYLOAD_MAP")

    sdk = {}
    for key, expected in remote["sources"].items():
        if key == "owner/remote_check.py":
            continue
        role, relative = key.split("/", 1)
        need(role in ("v5", "portable") and not Path(relative).name.startswith("test_"),
             "SDK_NOT_FIXTURE_OWNER")
        row = pin(Path(remote["source_roots"][role])/relative)
        need({name: row[name] for name in ("bytes", "sha256")} == expected,
             "RETAINED_SDK_SOURCE_CHANGED:"+key)
        sdk[key] = row
    need(len(sdk) == 102, "EXACT_SDK_SOURCE_COUNT")

    template_pin = verify(adoption["preparation_profile"])
    need(template_pin["bytes"] == 21137 and template_pin["sha256"] ==
         "f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b",
         "EXACT_PREPARATION_TEMPLATE")
    template = json.loads(Path(template_pin["path"]).read_bytes())
    producer, wire = template["producer"], reader["workspace_config"]["wire_profile"]
    need(template["schema"] == "DMKN_V5_PREPARATION_PROFILE_V1"
         and producer["schema"] == "DMKN_V5_PRODUCER_PROFILE_V1"
         and producer["supervisor_manifest"] == manifest
         and producer["host"] == adoption["receipt"]
         and producer["image_id"] == wire["relation_image"]
         and producer["foundation"] == wire["foundation"]
         and producer["policy"] == wire["policy"]
         and adoption["aggregate"]["image"] == wire["aggregate_image"],
         "EXACT_RETAINED_PROFILE_ROLES")
    assets = {name: verify(row) for name, row in {
        "native": adoption["native"], "receipt": adoption["receipt"],
        "aggregate": adoption["aggregate"]["executable"], "image": template["image"],
        "frontend": template["native_executable"], "foundation": reader["foundation"],
    }.items()}
    lean_root = Path(template["lean_root"])
    lean = {}
    for source in template["lean_runtime_pins"]:
        path = Path(source["path"])
        need(path.is_relative_to(lean_root), "RETAINED_LEAN_ROOT")
        key = path.relative_to(lean_root).as_posix()
        need(key not in lean, "DUPLICATE_LEAN_ROLE")
        lean[key] = verify(source)
    need(set(lean) == {"bin/libc++.dll", "bin/libInit_shared.dll",
        "bin/libleanshared.dll", "bin/libleanshared_1.dll",
        "bin/libleanshared_2.dll", "lib/lean/Init.olean"},
        "EXACT_SIX_LEAN_RUNTIME_FILES")
    need(sum(row["bytes"] for row in lean.values()) == 212510976, "LEAN_BYTE_CENSUS")
    distribution = pin(ROOT/"software/v5/distribution/distribution.py")
    need(distribution["sha256"] == sys.argv[1], "REVIEWED_DISTRIBUTION_SOURCE_CHANGED")
    value = dict(schema="DMKN_V5_DISTRIBUTION_INPUT_V1", base_root=str(base),
        base_manifest=manifest, sdk_sources=sdk, preparation_template=template_pin,
        assets=assets, aggregate_image=adoption["aggregate"]["image"],
        lean_runtime=lean, distribution_source=distribution)
    output = CHECKS/(NAME+"-input.json")
    need(not output.exists(), "FRESH_DISTRIBUTION_INPUT")
    raw = json.dumps(value, sort_keys=True, indent=2).encode("utf-8")+b"\n"
    need(len(raw) <= MIB, "DISTRIBUTION_INPUT_BOUND")
    with output.open("xb") as stream:
        stream.write(raw)
    print(json.dumps({"input": pin(output), "sdk_sources": len(sdk),
        "base_payload_files": len(files), "external_assets": len(assets),
        "lean_files": len(lean), "copied": False, "product_imports": 0,
        "executed": False}))


if __name__ == "__main__":
    main()
