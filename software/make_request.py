"""Create one ordinary request file without contacting or importing the node.

Use Python -B -E -s -S. See AGENT-QUICKSTART.md. Owner-controlled local paths
are required; path checks are not a sandbox against concurrent hostile writers.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

SOURCE_MAX = 65536
REQUEST_MAX = 131072
LABEL = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")
ROOT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*\Z")


def require(ok, code):
    if not ok:
        raise ValueError(code)


def local_path(value, *, output=False):
    path = Path(value)
    require(path.is_absolute() and path != Path(path.anchor) and ".." not in path.parts
            and not str(path).startswith("\\\\"), "ABSOLUTE_LOCAL_NONROOT_PATH_REQUIRED")
    for part in path.parts[1:]:
        require(not part.endswith((".", " ")) and ":" not in part
                and not getattr(os.path, "isreserved", lambda _: False)(part), "UNSUPPORTED_PATH_COMPONENT")
    if output:
        require(not os.path.lexists(path), "OUTPUT_ALREADY_EXISTS")
    for current in ((path.parent, *path.parent.parents) if output else (path, *path.parents)):
        info = current.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
                "LINK_OR_REPARSE_PATH_REFUSED")
        require(stat.S_ISDIR(info.st_mode) if output or current != path else stat.S_ISREG(info.st_mode),
                "PATH_KIND_REFUSED")
    return path


def opaque(value):
    require(type(value) is str and 0 < len(value.encode("utf-8")) <= 256
            and not any(ord(char) < 32 for char in value), "BOUNDED_OPAQUE_HANDLE_REQUIRED")
    return value  # Deliberately no trimming, lookup, selection, or authentication.


def parser():
    result = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    commands = result.add_subparsers(dest="operation", required=True)
    for name in ("info", "submit", "publish", "peer-find", "peer-acquire", "admit"):
        command = commands.add_parser(name, allow_abbrev=False)
        command.add_argument("--client", required=True)
        command.add_argument("--request-id", required=True)
        command.add_argument("--output", required=True)
        if name in ("submit", "admit"):
            command.add_argument("--context", required=True)
        if name == "submit":
            command.add_argument("--source-file", required=True)
            command.add_argument("--root", required=True)
        elif name == "publish":
            command.add_argument("--artifact", required=True)
            command.add_argument("--snapshot", required=True)
        elif name == "peer-find":
            command.add_argument("--peer", required=True)
        elif name == "peer-acquire":
            command.add_argument("--remote", required=True)
        elif name == "admit":
            command.add_argument("--candidate", action="append", required=True)
    return result


def prepare(args):
    require(LABEL.fullmatch(args.client) and args.client != "owner", "LOCAL_CLIENT_LABEL_REQUIRED")
    require(LABEL.fullmatch(args.request_id), "REQUEST_ID_REQUIRED")
    fields, source_pin = {}, None
    if args.operation in ("submit", "admit"):
        fields["context"] = opaque(args.context)
    if args.operation == "submit":
        require(len(args.root) <= 256 and ROOT.fullmatch(args.root), "DECLARATION_ROOT_REQUIRED")
        source = local_path(args.source_file)
        with source.open("rb") as stream:
            raw = stream.read(SOURCE_MAX + 1)
        require(0 < len(raw) <= SOURCE_MAX, "SOURCE_BYTE_LIMIT")
        require(not raw.startswith(b"\xef\xbb\xbf"), "SOURCE_UTF8_BOM_REFUSED")
        text = raw.decode("utf-8", errors="strict")
        fields.update(source=text, root=args.root)
        source_pin = {"path": str(source), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    elif args.operation == "publish":
        fields = {"artifact": opaque(args.artifact), "snapshot": opaque(args.snapshot)}
    elif args.operation == "peer-find":
        require(LABEL.fullmatch(args.peer), "PEER_ALIAS_REQUIRED")
        fields = {"peer": args.peer}
    elif args.operation == "peer-acquire":
        fields = {"remote": opaque(args.remote)}
    elif args.operation == "admit":
        require(1 <= len(args.candidate) <= 4 and len(set(args.candidate)) == len(args.candidate),
                "ONE_TO_FOUR_DISTINCT_CANDIDATES_REQUIRED")
        fields["selected"] = [opaque(value) for value in args.candidate]
    request = {"client": args.client, "request_id": args.request_id,
               "op": args.operation.replace("-", "_"), "args": fields}
    raw = (json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False) + "\n").encode("utf-8")
    require(len(raw) <= REQUEST_MAX, "REQUEST_BYTE_LIMIT")
    return raw, source_pin


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        require(sys.dont_write_bytecode and sys.flags.ignore_environment and sys.flags.no_site
                and sys.flags.no_user_site, "RUN_WITH_B_E_s_S")
        output = local_path(args.output, output=True)
        raw, source_pin = prepare(args)
        with output.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        result = {"status": "REQUEST_FILE_CREATED_NOT_SENT", "sent": False,
                  "request": {"path": str(output), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}}
        if source_pin is not None:
            result["source"] = source_pin
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"status": "REQUEST_FILE_CREATION_FAILED_NOT_SENT", "sent": False,
                          "error": type(error).__name__, "detail": str(error)[:512]}, sort_keys=True), file=sys.stderr)
        return 1  # A partial exclusively created file, if any, is retained.


if __name__ == "__main__":
    raise SystemExit(main())
