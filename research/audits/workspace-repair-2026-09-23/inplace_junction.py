"""Set one guarded NTFS junction on an *existing empty* directory.

The self-test uses only a fresh disposable child of this audit directory.
No directory is removed or moved by this helper. A held-open cwd was observed
to fail a relative write after in-place conversion, so the actual legacy-root
mode is disabled. Retained actual-mode code is for review only.
"""
from __future__ import annotations

import argparse
import ctypes
from ctypes import wintypes
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys


AUDIT = Path(__file__).resolve().parent
CANONICAL = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
LEGACY = Path(r"E:\Distributed Verifiable Mathematical Knowledge Network")
TEST = AUDIT / "inplace-junction-test-01"
TAG_MOUNT_POINT = 0xA0000003
FSCTL_SET_REPARSE_POINT = 0x000900A4
FSCTL_GET_REPARSE_POINT = 0x000900A8
FILE_ATTRIBUTE_DIRECTORY = 0x10
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
GENERIC_WRITE = 0x40000000
FILE_SHARE_ALL = 0x7
OPEN_EXISTING = 3
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
kernel32.GetFileAttributesW.argtypes = [wintypes.LPCWSTR]
kernel32.GetFileAttributesW.restype = wintypes.DWORD
kernel32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD,
    wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD,
    wintypes.HANDLE]
kernel32.CreateFileW.restype = wintypes.HANDLE
kernel32.DeviceIoControl.argtypes = [wintypes.HANDLE, wintypes.DWORD,
    wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
kernel32.DeviceIoControl.restype = wintypes.BOOL
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL


def fail_win32(label: str) -> None:
    code = ctypes.get_last_error()
    raise OSError(code, f"{label}: {ctypes.FormatError(code).strip()}")


def exact_path(path: Path, expected: Path) -> None:
    if os.path.normcase(os.path.abspath(path)) != os.path.normcase(os.path.abspath(expected)):
        raise ValueError(f"WRONG_EXACT_PATH: {path}")


def ordinary_directory(path: Path, *, empty: bool) -> None:
    info = path.lstat()
    attributes = kernel32.GetFileAttributesW(str(path))
    if attributes == 0xFFFFFFFF:
        fail_win32("GetFileAttributesW")
    if not stat.S_ISDIR(info.st_mode) or not (attributes & FILE_ATTRIBUTE_DIRECTORY):
        raise ValueError(f"NOT_DIRECTORY: {path}")
    if attributes & FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError(f"ALREADY_REPARSE_POINT: {path}")
    if empty:
        with os.scandir(path) as entries:
            if next(entries, None) is not None:
                raise ValueError(f"DIRECTORY_NOT_EMPTY: {path}")


def reparse_buffer(target: Path) -> bytes:
    target_text = str(target)
    substitute = ("\\??\\" + target_text).encode("utf-16-le")
    display = target_text.encode("utf-16-le")
    path_buffer = substitute + b"\0\0" + display + b"\0\0"
    data_length = 8 + len(path_buffer)
    if data_length > 16376:
        raise ValueError("REPARSE_BUFFER_TOO_LARGE")
    return struct.pack("<LHHHHHH", TAG_MOUNT_POINT, data_length, 0,
                       0, len(substitute), len(substitute) + 2, len(display)) + path_buffer


def set_junction(link: Path, target: Path) -> dict:
    ordinary_directory(link, empty=True)
    ordinary_directory(target, empty=False)
    if os.path.splitdrive(link)[0].casefold() != os.path.splitdrive(target)[0].casefold():
        raise ValueError("DIFFERENT_DRIVES")
    handle = kernel32.CreateFileW(str(link), GENERIC_WRITE, FILE_SHARE_ALL,
        None, OPEN_EXISTING,
        FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_BACKUP_SEMANTICS, None)
    if handle == ctypes.c_void_p(-1).value:
        fail_win32("CreateFileW(directory)")
    try:
        # Recheck after opening the directory. NTFS additionally enforces the
        # empty-directory condition for mount-point reparse data.
        ordinary_directory(link, empty=True)
        payload = reparse_buffer(target)
        source = ctypes.create_string_buffer(payload)
        returned = wintypes.DWORD()
        if not kernel32.DeviceIoControl(handle, FSCTL_SET_REPARSE_POINT,
                source, len(payload), None, 0, ctypes.byref(returned), None):
            fail_win32("FSCTL_SET_REPARSE_POINT")
        output = ctypes.create_string_buffer(16384)
        if not kernel32.DeviceIoControl(handle, FSCTL_GET_REPARSE_POINT,
                None, 0, output, len(output), ctypes.byref(returned), None):
            fail_win32("FSCTL_GET_REPARSE_POINT")
        data = output.raw[:returned.value]
        tag, length, _, sub_offset, sub_length, print_offset, print_length = struct.unpack_from(
            "<LHHHHHH", data, 0)
        names = data[16:8 + length]
        substitute = names[sub_offset:sub_offset + sub_length].decode("utf-16-le")
        display = names[print_offset:print_offset + print_length].decode("utf-16-le")
        if tag != TAG_MOUNT_POINT or substitute != "\\??\\" + str(target) or display != str(target):
            raise ValueError("READBACK_TARGET_MISMATCH")
        return {"tag": hex(tag), "substitute": substitute,
                "print_name": display, "returned_bytes": returned.value}
    finally:
        kernel32.CloseHandle(handle)


def recovered_manifest_intact() -> None:
    manifest = json.loads((AUDIT / "BEFORE.json").read_text(encoding="utf-8"))
    exact_path(Path(manifest["canonical_root"]), CANONICAL)
    exact_path(Path(manifest["unexpected_root"]), LEGACY)
    recovered = AUDIT / "recovered"
    ordinary_directory(recovered, empty=False)
    for entry in manifest["files"]:
        relative = entry["relative_path"]
        if not relative.startswith("experiments/") or ".." in Path(relative).parts:
            raise ValueError("INVALID_MANIFEST_RELATIVE_PATH")
        stored = recovered / relative
        peer = CANONICAL / relative
        for path, expected in ((stored, entry["sha256"]),
                               (peer, entry["canonical_peer_sha256"])):
            data = path.read_bytes()
            if len(data) != entry["bytes"] and path == stored:
                raise ValueError(f"RECOVERED_SIZE_CHANGED: {relative}")
            if hashlib.sha256(data).hexdigest().casefold() != expected.casefold():
                raise ValueError(f"RECOVERED_OR_PEER_HASH_CHANGED: {relative}")


def self_test() -> dict:
    if TEST.exists():
        raise ValueError("TEST_ALLOCATION_ALREADY_EXISTS")
    TEST.mkdir()
    target = TEST / "target"
    link = TEST / "held-open-link"
    target.mkdir()
    link.mkdir()
    (target / "sentinel.txt").write_text("target-only\n", encoding="utf-8")
    child_code = (
        "import sys; print('READY', flush=True); command=sys.stdin.readline().strip(); "
        "open('relative-created.txt','w',encoding='utf-8').write('held-cwd\\n') if command=='GO' else None; "
        "print('DONE:'+command, flush=True)"
    )
    child = subprocess.Popen([sys.executable, "-B", "-E", "-s", "-S", "-c", child_code],
        cwd=link, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True)
    ready = child.stdout.readline().strip()
    if ready != "READY":
        child.communicate("SKIP\n", timeout=15)
        raise RuntimeError("HELD_CWD_CHILD_NOT_READY")
    try:
        result = set_junction(link, target)
    except Exception:
        child.communicate("SKIP\n", timeout=15)
        raise
    stdout, stderr = child.communicate("GO\n", timeout=15)
    target_write = target / "relative-created.txt"
    if child.returncode != 0:
        raise RuntimeError(f"HELD_CWD_CHILD_FAILED: {child.returncode}: {stderr}")
    if (link / "sentinel.txt").read_text(encoding="utf-8") != "target-only\n":
        raise RuntimeError("NEW_PATH_DID_NOT_RESOLVE_TARGET")
    return {"status": "TEST_FSCTL_SET_COMPLETED_NOT_ACTUAL_REPAIR",
            "test_directory": str(TEST), "link": str(link), "target": str(target),
            "held_child_stdout": ready + "\n" + stdout,
            "held_child_stderr": stderr, "relative_write_in_target": target_write.exists(),
            "readback": result}


def actual() -> dict:
    exact_path(AUDIT, CANONICAL / "research/audits/workspace-repair-2026-09-23")
    ordinary_directory(CANONICAL, empty=False)
    exact_path(LEGACY, Path(r"E:\Distributed Verifiable Mathematical Knowledge Network"))
    ordinary_directory(LEGACY, empty=True)
    recovered_manifest_intact()
    result = set_junction(LEGACY, CANONICAL)
    if (LEGACY / "AGENTS.md").read_bytes() != (CANONICAL / "AGENTS.md").read_bytes():
        raise RuntimeError("POSTSET_CANONICAL_SENTINEL_MISMATCH")
    return {"status": "ACTUAL_INPLACE_JUNCTION_SET_NEW_LOOKUPS_ONLY", "link": str(LEGACY),
            "target": str(CANONICAL), "readback": result}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--actual", action="store_true")
    parser.add_argument("--confirm-exact-existing-directory", action="store_true")
    parser.add_argument("--acknowledge-held-cwd-risk", action="store_true")
    args = parser.parse_args()
    if args.actual:
        parser.error("actual legacy-root mode disabled after held-cwd relative write failed EINVAL")
    print(json.dumps(self_test() if args.self_test else actual(), sort_keys=True))


if __name__ == "__main__":
    main()
