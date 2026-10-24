"""Two-payload file successor: native long paths and context-bound query preparation."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
PREFIX = "software/v5/ordinary_module_anchor_package/"
BASE = ROOT/"experiments/v5-local-checks/ordinary-module-anchor-assembly-02/package"
BASE_PROFILE = "5e7e9a6b8679864e52f93f7704f58591799406a3226343e05ce0c01a85cc7be9"
BASE_RECEIPT = "0685b54054e6f53892ad03795444c8a7447da2b1d6acff4f80b32d1284bad0f2"
SOURCE = "software/v5/ordinary_module_anchor/OrdinaryModule03.lean"
LOGICAL = "module/OrdinaryModule.lean"
QUERY = "software/v5/ordinary_query_context/query.py"
QUERY_SHA = "449b5fea77f4c19cfbde47346ea255ae1277a1cf53e3030a6baa9de3f8659af6"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError(code)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    parser.add_argument("--native-sha256", required=True)
    args = parser.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "ANCHOR_REPAIR_CONTEXT")
    started, cpu = time.monotonic(), time.process_time()
    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 40,
             "ANCHOR_REPAIR_ALLOWANCE")
    old_source = ROOT/PREFIX/"assemble.py"
    with old_source.open("rb") as stream:
        raw = stream.read(2*MIB+1)
    need(hashlib.sha256(raw).hexdigest() ==
         "1c426a2ce3484448effe5dee559d52cf0c43650fcfd2f50946aba97e05c6481d",
         "ANCHOR_REPAIR_HELPER_PIN")
    spec = importlib.util.spec_from_file_location("_anchor_repair_helper", old_source)
    S = importlib.util.module_from_spec(spec)
    exec(compile(raw, str(old_source), "exec"), S.__dict__)
    B = S.bootstrap(ROOT/S.BUILDER, "_anchor_repair_builder", S.BUILDER_SHA)
    output = B.ordinary(args.output, directory=True, fresh=True)
    need(output.is_relative_to(ROOT/"experiments/v5-local-checks") and
         not output.is_relative_to(BASE) and not BASE.is_relative_to(output), "ANCHOR_REPAIR_OUTPUT")
    owner = S.bootstrap(BASE/"owner.py", "_anchor_repair_owner",
        "a17f7905f479929bf55f3ddbe8f857de9d48e528a132e4c27f2a000d1adb028d")
    loader = owner.bootstrap(BASE, BASE_PROFILE, check)
    runtimes = {"python_runtime": Path(r"D:\Python314"),
                "lean_runtime": ROOT/"software/runtime/lean-4.34.0-windows"}
    loaded = loader.load(BASE, BASE_PROFILE, runtimes, started+60, check_parent=check)
    need(B.pin(BASE/"ASSEMBLY.json", check, 2*MIB)["sha256"] == BASE_RECEIPT,
         "ANCHOR_REPAIR_BASE_RECEIPT")
    old = loaded.descriptor
    installed_raw = loader.bounded(BASE/"installation/INSTALLATION.json", 2*MIB)
    installed = loader.owner_json(installed_raw)
    selected = {name: (BASE/name, pin) for name, pin in old["files"].items()}
    for name, pin in installed["files"].items():
        loader.relative(name)
        if name.split("/", 1)[0] not in runtimes:
            selected["installation/"+name] = (BASE/"installation"/name, pin)
    selected["installation/INSTALLATION.json"] = (BASE/"installation/INSTALLATION.json",
        {"bytes": len(installed_raw), "sha256": old["installation_manifest_sha256"]})
    replacement = B.pin(ROOT/SOURCE, check, 2*MIB)
    need(replacement["sha256"] == args.native_sha256 and replacement != selected[LOGICAL][1],
         "ANCHOR_REPAIR_NATIVE_PIN")
    selected[LOGICAL] = (ROOT/SOURCE, replacement)
    query_pin = B.pin(ROOT/QUERY, check, 2*MIB)
    need(query_pin["sha256"] == QUERY_SHA and query_pin != selected["query.py"][1],
         "ANCHOR_REPAIR_QUERY_PIN")
    selected["query.py"] = (ROOT/QUERY, query_pin)
    replacements = {LOGICAL: replacement, "query.py": query_pin}
    need(len(selected) == 134 and len(old["files"]) == 106 and
         len({name.casefold() for name in selected}) == 134, "ANCHOR_REPAIR_CENSUS")
    need(sum(pin["bytes"] for _, pin in selected.values()) <= 768*MIB, "ANCHOR_REPAIR_BYTES")
    for name, (path, expected) in selected.items():
        loader.relative(name)
        need(B.pin(path, check, 128*MIB) == expected, "ANCHOR_REPAIR_INPUT")
    output.mkdir()
    for name, (path, expected) in sorted(selected.items()):
        check()
        target = output/name
        target.parent.mkdir(parents=True, exist_ok=True)
        B.ordinary(target.parent, directory=True); B.ordinary(target, fresh=True)
        digest, size = hashlib.sha256(), 0
        with path.open("rb") as inp, target.open("xb") as out:
            while block := inp.read(MIB):
                check(); size += len(block)
                need(size <= expected["bytes"], "ANCHOR_REPAIR_COPY_BOUND")
                digest.update(block); out.write(block)
            out.flush(); os.fsync(out.fileno())
        need({"bytes": size, "sha256": digest.hexdigest()} == expected and
             B.pin(target, check, 128*MIB) == expected, "ANCHOR_REPAIR_COPY_PIN")
    for name, (path, expected) in selected.items():
        need(B.pin(path, check, 128*MIB) == expected and B.pin(output/name, check, 128*MIB) == expected,
             "ANCHOR_REPAIR_FINAL_PIN")
    descriptor = dict(old, files=dict(old["files"], **replacements))
    profile_raw = loaded.A.E.canonical_json(descriptor)
    receipt = {"status": "ASSEMBLED_NOT_ADOPTED", "base_profile_sha256": BASE_PROFILE,
        "base_assembly_sha256": BASE_RECEIPT, "profile_sha256": hashlib.sha256(profile_raw).hexdigest(),
        "installation_manifest_sha256": old["installation_manifest_sha256"],
        "implementation_id": loaded.installation.implementation_id, "files_excluding_profile": 134,
        "added": [], "changed": sorted(replacements), "unchanged": sorted(set(selected)-set(replacements)),
        "changed_or_added": replacements, "native_source": SOURCE, "query_source": QUERY,
        "assembler": B.pin(Path(__file__).resolve(), check, 2*MIB),
        "claim": "TWO_PAYLOAD_PATH_AND_CONTEXT_QUERY_NO_NATIVE_OWNER_OR_STATE_OPERATION"}
    B.save_json(output/"ASSEMBLY.json", receipt)
    B.fresh_bytes(output/".PROFILE.pending", profile_raw)
    check(); B.ordinary(output/"PROFILE.json", fresh=True)
    (output/".PROFILE.pending").rename(output/"PROFILE.json")
    print(json.dumps(receipt, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
