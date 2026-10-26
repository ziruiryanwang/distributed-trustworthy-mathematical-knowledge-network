"""Select one flat-source preparer repair continuation; never execute it."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import time

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LOCAL = ROOT/"experiments/v5-local-checks"
PREFIX = "software/v5/ordinary_current_release/"
PACKAGE = LOCAL/"binding-package01/assembled/package"
PYTHON = Path(r"D:\Python314")
RELEASE = "821796aa5b4996edd3f34babdb3be186d8321e0b3b4208b1e3f18705400caf78"
MIB = 1024**2


def need(ok, code):
    if not ok:
        raise ValueError("CURRENT_SELECT_"+code)


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    for name in ("name", "test-sha256", "bundle-sha256", "preparer-sha256",
                 "prior-source-receipt-sha256", "prior-prebuilt-receipt-sha256"):
        p.add_argument("--"+name, required=True)
    args = p.parse_args()
    need(Path.cwd() == ROOT and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize, "PROCESS")
    need(re.fullmatch(r"current-release-continuation[0-9]{2}", args.name), "NAME")
    need(all(re.fullmatch(r"[0-9a-f]{64}", value) for value in
             (args.test_sha256, args.bundle_sha256, args.preparer_sha256,
              args.prior_source_receipt_sha256, args.prior_prebuilt_receipt_sha256)), "APPROVED_HASHES")
    started, cpu = time.monotonic(), time.process_time()
    sources, external = {}, {}

    def check():
        need(time.monotonic()-started < 60 and time.process_time()-cpu < 30, "ALLOWANCE")

    def pin(path, expected=None):
        check()
        need(path.is_absolute() and ".." not in path.parts, "ABSOLUTE_PATH")
        for ancestor in (*reversed(path.parents), path):
            info = ancestor.lstat()
            need(not stat.S_ISLNK(info.st_mode) and
                 not getattr(info, "st_file_attributes", 0) & 0x400, "REDIRECTED_PATH")
            need(stat.S_ISDIR(info.st_mode) if ancestor != path else
                 stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "PATH_KIND")
        size = path.stat().st_size
        need(0 < size <= 512*MIB, "FILE_BOUND")
        with path.open("rb") as stream:
            value = {"bytes": size, "sha256": hashlib.file_digest(stream, "sha256").hexdigest()}
        need(path.stat().st_size == size and (expected is None or value == expected), "PIN:"+str(path))
        return value

    release_path = ROOT/PREFIX/"release.json"
    need(pin(release_path)["sha256"] == RELEASE, "EXACT_RELEASE")
    release = json.loads(release_path.read_bytes())
    selected = dict(release["build"]["sources"])
    for row in release["companions"].values():
        value = {"bytes": row["bytes"], "sha256": row["sha256"]}
        need(row["source"] not in selected or selected[row["source"]] == value, "SOURCE_ALIAS")
        selected[row["source"]] = value
    for role in ("source", "prebuilt"):
        for name in release["release_support"][role].values():
            value = pin(ROOT/name)
            need(name not in selected or selected[name] == value, "SUPPORT_ALIAS")
            selected[name] = value
    for name in ("tools/Run-V5-Check.py", PREFIX+"test_release.py", PREFIX+"continue_release.py", PREFIX+"select_continue.py",
                 PREFIX+"prepare_selected02.py", PREFIX+"CONTINUATION.md"):
        selected[name] = pin(ROOT/name)
    for name, value in selected.items():
        pin(ROOT/name, value)
        if name.startswith("software/v5/") or name == "tools/Run-V5-Check.py":
            need(value["bytes"] <= 2*MIB, "SOURCE_BOUND")
            sources[name] = value["sha256"]
        else:
            need(name.startswith("software/assets/foundation/"), "EXTERNAL_SOURCE_SCOPE")
            external[str(ROOT/name)] = value["sha256"]
    need(sources[PREFIX+"continue_release.py"] == args.test_sha256 and
         sources[PREFIX+"bundle.py"] == args.bundle_sha256 and
         sources[PREFIX+"prepare_selected02.py"] == args.preparer_sha256, "REVIEWED_SOURCES")
    for name, value in release["prebuilt"]["files"].items():
        external[str(PACKAGE/name)] = pin(PACKAGE/name, value)["sha256"]
    for name, value in release["build"]["runtime_pins"].items():
        if name.startswith("python_runtime/"):
            path = PYTHON/name.split("/", 1)[1]
            external[str(path)] = pin(path, value)["sha256"]
    prior = LOCAL/"current-release-controls01/suite"
    for kind, digest in (("source", args.prior_source_receipt_sha256),
                         ("prebuilt", args.prior_prebuilt_receipt_sha256)):
        path = prior/kind/"RECEIPT.json"
        value = pin(path)
        need(value["sha256"] == digest, "PRIOR_RECEIPT:"+kind)
        external[str(path)] = digest
    need(1 <= len(sources) <= 256 and 1 <= len(external) <= 256 and
         sum(selected[name]["bytes"] for name in sources) <= 16*MIB, "SNAPSHOT_BOUND")
    destination = LOCAL/(args.name+".selection.json")
    need(not os.path.lexists(destination) and not os.path.lexists(LOCAL/args.name), "FRESH_SELECTION")
    selection = {"schema": "DMKN_V5_LOCAL_CHECK_V1", "name": args.name,
        "sources": sources, "runtime_pins": external,
        "argv": [str(PYTHON/"python.exe"), "-I", "-S", "-B",
            "{snapshot}/"+PREFIX+"continue_release.py", "--source-root", str(ROOT),
            "--package", str(PACKAGE), "--release-sha256", RELEASE,
            "--preparer-sha256", args.preparer_sha256,
            "--prior-source-receipt", str(prior/"source/RECEIPT.json"),
            "--prior-source-receipt-sha256", args.prior_source_receipt_sha256,
            "--prior-prebuilt-receipt", str(prior/"prebuilt/RECEIPT.json"),
            "--prior-prebuilt-receipt-sha256", args.prior_prebuilt_receipt_sha256,
            "--output", "{output}/suite"],
        "limits": {"wall_seconds": 180, "cpu_seconds": 90, "memory_mib": 768,
                   "active_processes": 1, "stdout_bytes": 2*MIB, "stderr_bytes": MIB}}
    raw = json.dumps(selection, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=True, allow_nan=False).encode("ascii")
    check()
    with destination.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"status": "PREPARED_NOT_EXECUTED", "selection": str(destination),
        "sha256": hashlib.sha256(raw).hexdigest(), "source_count": len(sources),
        "external_count": len(external)}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
