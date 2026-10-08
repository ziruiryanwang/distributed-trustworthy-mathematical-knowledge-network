"""Read-only inventory and exact raw-blob audit for the initial local Git baseline.

No repository mutations. JSON goes to stdout; never print file contents/secrets.
This deliberately checks the conservative initial scope, not future release scope.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TOP = {"software", "tools", "research", "notes", "spec", "security", "deliverables"}
FORBIDDEN = {"runtime", "build", "release", "qualification", "node_modules", "target",
             ".lake", ".venv", "venv", "__pycache__", ".git"}
SECRET = re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"
                    rb"|sk-proj-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}")
MAX_FILE = 5 * 1024 * 1024
MAX_TOTAL = 100 * 1024 * 1024


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, timeout=60)


def disk_record(name):
    parts = PurePosixPath(name).parts
    if not parts or any(p in ("..", ".") for p in parts) or name.startswith("/"):
        raise ValueError("Unsafe Git path")
    if len(parts) == 1:
        if not (name.endswith(".md") or name in (".gitignore", ".gitattributes")):
            raise ValueError("Unselected root file: " + name)
    elif parts[0] not in TOP or any(p in FORBIDDEN for p in parts[1:]):
        raise ValueError("Unselected directory: " + name)
    cursor = ROOT
    for part in parts:
        cursor = cursor / part
        info = cursor.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("Link/reparse point: " + name)
    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_FILE:
        raise ValueError("Nonregular/oversize file: " + name)
    raw = cursor.read_bytes()
    if len(raw) != info.st_size:
        raise ValueError("Concurrent size change: " + name)
    if SECRET.search(raw):
        raise ValueError("Credential marker; inspect privately: " + name)
    return {"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    if Path.cwd().resolve() != ROOT or git("rev-parse", "--show-toplevel").decode().strip().replace("\\", "/") != ROOT.as_posix():
        raise ValueError("Wrong canonical workdir/repository")
    mode = sys.argv[1]
    if mode == "inventory":
        if git("ls-files", "-z"):
            raise ValueError("Initial inventory requires empty index")
        names = sorted(n.decode("utf-8") for n in git("ls-files", "--others", "--exclude-standard", "-z").split(b"\0") if n)
        if len(names) != len(set(n.casefold() for n in names)):
            raise ValueError("Duplicate/case-colliding paths")
        entries = [disk_record(n) for n in names]
        total = sum(e["bytes"] for e in entries)
        if not entries or total > MAX_TOTAL:
            raise ValueError("Empty/oversize scope")
        print(json.dumps({"schema": 1, "scope": "initial-source-only-local-baseline",
                          "files": len(entries), "bytes": total, "entries": entries}, indent=2))
        return
    if mode != "check" or len(sys.argv) != 3:
        raise ValueError("Use inventory or check MANIFEST")
    manifest = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    expected = {e["path"]: e for e in manifest["entries"]}
    index = {}
    for record in git("ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        meta, name = record.split(b"\t", 1)
        filemode, oid, stage = meta.split()
        if filemode != b"100644" or stage != b"0":
            raise ValueError("Nonregular/conflicted index mode")
        name = name.decode("utf-8")
        if name in index:
            raise ValueError("Duplicate index path")
        index[name] = oid
    if set(index) != set(expected):
        raise ValueError("Exact staged path set differs from pre-stage manifest")
    with subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT,
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
        try:
            for name in sorted(expected):
                entry = expected[name]
                if disk_record(name) != entry:
                    raise ValueError("Disk bytes changed since inventory: " + name)
                proc.stdin.write(index[name] + b"\n")
                proc.stdin.flush()
                header = proc.stdout.readline().split()
                if header != [index[name], b"blob", str(entry["bytes"]).encode()]:
                    raise ValueError("Unexpected raw Git blob framing: " + name)
                blob = proc.stdout.read(entry["bytes"])
                if len(blob) != entry["bytes"] or proc.stdout.read(1) != b"\n":
                    raise ValueError("Truncated raw Git blob: " + name)
                if hashlib.sha256(blob).hexdigest() != entry["sha256"]:
                    raise ValueError("Staged raw bytes differ: " + name)
            proc.stdin.close()
            if proc.wait(timeout=10) != 0:
                raise ValueError("Git blob reader failed")
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait(timeout=10)
    print(json.dumps({"status": "PASS", "files": len(expected), "bytes": manifest["bytes"],
                      "exact_path_set": True, "regular_modes_only": True,
                      "pre_post_disk_sha256_equal": True, "raw_staged_sha256_equal": True,
                      "reparse_points": 0, "credential_markers": 0}))


if __name__ == "__main__":
    main()
