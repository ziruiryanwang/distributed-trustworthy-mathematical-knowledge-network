"""One-payload file-only syntax successor; preserve failed assembly and owner state."""
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
BASE = ROOT/"experiments/v5-local-checks/ordinary-module-anchor-assembly-01/package"
BASE_PROFILE = "8404d56996180520c88f98f3fec61100809bde59297b983de686fede8958ac93"
BASE_RECEIPT = "03520b9bb3fef53d78671af07269dafc327d06a23f604053128eeded538cc339"
SOURCE = "software/v5/ordinary_module_anchor/OrdinaryModule02.lean"
LOGICAL = "module/OrdinaryModule.lean"
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
    descriptor = dict(old, files=dict(old["files"], **{LOGICAL: replacement}))
    profile_raw = loaded.A.E.canonical_json(descriptor)
    receipt = {"status": "ASSEMBLED_NOT_ADOPTED", "base_profile_sha256": BASE_PROFILE,
        "base_assembly_sha256": BASE_RECEIPT, "profile_sha256": hashlib.sha256(profile_raw).hexdigest(),
        "installation_manifest_sha256": old["installation_manifest_sha256"],
        "implementation_id": loaded.installation.implementation_id, "files_excluding_profile": 134,
        "added": [], "changed": [LOGICAL], "unchanged": sorted(set(selected)-{LOGICAL}),
        "changed_or_added": {LOGICAL: replacement}, "native_source": SOURCE,
        "assembler": B.pin(Path(__file__).resolve(), check, 2*MIB),
        "claim": "ONE_PAYLOAD_SYNTAX_REPAIR_NO_NATIVE_OWNER_OR_STATE_OPERATION"}
    B.save_json(output/"ASSEMBLY.json", receipt)
    B.fresh_bytes(output/".PROFILE.pending", profile_raw)
    check(); B.ordinary(output/"PROFILE.json", fresh=True)
    (output/".PROFILE.pending").rename(output/"PROFILE.json")
    print(json.dumps(receipt, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
