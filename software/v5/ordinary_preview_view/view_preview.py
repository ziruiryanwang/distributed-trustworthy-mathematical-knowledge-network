"""Render one explicitly selected saved formal preview, entirely offline.

Only the five pinned inert codecs and adjacent renderer execute. Report contents
select no paths, code or limits. A display is never mathematical acceptance.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import stat
import sys

MIB = 1024**2
RENDERER_SHA = "3b525d8e42709249196062733290486516b40c7cc1c320e9f3d005718a874352"
CODECS = (
    ("ordinary_evidence", "installation/py/ordinary_evidence.py", "fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6"),
    ("ordinary_semantics", "installation/py/ordinary_semantics.py", "ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915"),
    ("portable_evidence", "installation/py/portable_evidence.py", "f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8"),
    ("ordinary_preview", "authoring/py/ordinary_preview.py", "0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6"),
    ("portable_preview", "authoring/py/portable_preview.py", "b78dd54340b7b55e4359769d6784f7f225ba304457ce880ce2760717e865550d"),
)


def need(condition, code):
    if not condition:
        raise ValueError(code)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def identifier(value):
    need(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value), "VIEW_DIGEST")
    return value


def ordinary_path(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and ".." not in path.parts, "VIEW_ABSOLUTE_PATH")
    for part in (*reversed(path.parents), path):
        if fresh and part == path:
            need(not part.exists(), "VIEW_OUTPUT_EXISTS")
            continue
        info = part.lstat()
        need(not stat.S_ISLNK(info.st_mode) and
             not getattr(info, "st_file_attributes", 0) & 0x400, "VIEW_REDIRECTED_PATH")
    if not fresh:
        info = path.stat()
        need(stat.S_ISDIR(info.st_mode) if directory else
             stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "VIEW_PATH_KIND")
    return path


def read(path, cap):
    path = ordinary_path(path)
    need(0 < path.stat().st_size <= cap, "VIEW_INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(cap + 1)
    need(0 < len(raw) <= cap, "VIEW_INPUT_BOUND")
    return raw


def strict_report(raw):
    """Bound outer JSON depth/numbers; the existing codec validates the preview."""
    depth, quoted, escaped = 0, False, False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            need(depth <= 64, "VIEW_JSON_DEPTH")
        elif byte in (93, 125):
            depth -= 1
            need(depth >= 0, "VIEW_JSON_DEPTH")

    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, "VIEW_JSON_DUPLICATE")
            out[key] = value
        return out

    def integer(token):
        need(len(token) <= 20, "VIEW_JSON_INTEGER")
        return int(token)

    def floating(token):
        need(len(token) <= 64, "VIEW_JSON_FLOAT")
        value = float(token)
        need(math.isfinite(value), "VIEW_JSON_FLOAT")
        return value

    def constant(_token):
        raise ValueError("VIEW_JSON_NONFINITE")

    return json.loads(raw, object_pairs_hook=pairs, parse_int=integer,
                      parse_float=floating, parse_constant=constant)


@contextmanager
def selected_modules(package):
    """Hash captured source before execution; restore temporary import slots."""
    sources = []
    for name, relative, pin in CODECS:
        path = package / relative
        raw = read(path, MIB)
        need(digest(raw) == pin, "VIEW_CODEC_PIN:" + name)
        sources.append((name, path, raw))
    renderer_path = Path(__file__).absolute().parent / "render.py"
    raw = read(renderer_path, MIB)
    need(digest(raw) == RENDERER_SHA, "VIEW_RENDERER_PIN")
    sources.append(("_ordinary_preview_view_render", renderer_path, raw))
    sentinel = object()
    previous = {name: sys.modules.get(name, sentinel) for name, _, _ in sources}
    loaded = {}
    try:
        for name, path, raw in sources:
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            exec(compile(raw, str(path), "exec", dont_inherit=True), module.__dict__)
            loaded[name] = module
        yield loaded
    finally:
        for name, old in previous.items():
            if old is sentinel:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old


def view_selected(package, profile_sha256, report, report_sha256, output):
    package = ordinary_path(package, directory=True)
    report = ordinary_path(report)
    output = ordinary_path(output, fresh=True, directory=True)
    source_dir = Path(__file__).absolute().parent
    need(not output.is_relative_to(package) and not package.is_relative_to(output)
         and not output.is_relative_to(source_dir) and not source_dir.is_relative_to(output)
         and not report.is_relative_to(output), "VIEW_OUTPUT_OVERLAP")
    profile_sha256, report_sha256 = identifier(profile_sha256), identifier(report_sha256)
    profile_raw = read(package / "PROFILE.json", 2*MIB)
    need(digest(profile_raw) == profile_sha256, "VIEW_PROFILE_PIN")
    profile = strict_report(profile_raw)
    need(type(profile) is dict and profile.get("schema") == "DMKN_ORDINARY_OWNER_PROFILE_V1",
         "VIEW_PROFILE_SCHEMA")
    report_raw = read(report, 2*MIB)
    need(digest(report_raw) == report_sha256, "VIEW_REPORT_PIN")
    doc = strict_report(report_raw)
    need(type(doc) is dict and doc.get("operation") == "preview", "VIEW_REPORT_OPERATION")
    original_profile = identifier(doc.get("profile_sha256"))
    result = doc.get("result")
    need(type(result) is dict and result.get("operation") == "preview", "VIEW_RESULT_OPERATION")
    selection = result.get("selection")
    need(type(selection) is dict and type(selection.get("record")) is dict, "VIEW_RECORD")
    record = selection["record"]
    need(record.get("schema") == "DMKN_FORMAL_FEATURE_RECORD_V3" and
         record.get("kind") == "ordinary-lean-export-v2", "VIEW_RECORD_SCHEMA")
    with selected_modules(package) as modules:
        E, P = modules["ordinary_evidence"], modules["portable_preview"]
        raw = E.canonical_json(result.get("preview"))
        view = modules["_ordinary_preview_view_render"].render_preview(raw, codec=P, evidence=E)
        locator = P.read_locator(record.get("locator"))
        expected = {"schema": P.LOCATOR_SCHEMA, "semantic_id": view["semantic_id"],
                    "unit_id": view["unit_id"], "export_name": result["preview"]["export_name"]}
        need(locator == expected and record.get("object_id") == view["export_id"],
             "VIEW_RECORD_IDENTITY")
        need(type(record.get("object_bytes")) is int and
             record["object_bytes"] == len(raw) == result.get("preview_bytes") and
             type(result.get("preview_bytes")) is int and
             record.get("object_sha256") == digest(raw) == result.get("preview_sha256"),
             "VIEW_RECORD_BYTES")
        need(doc.get("semantic_id") == view["semantic_id"], "VIEW_REPORT_SEMANTICS")
    need(read(package / "PROFILE.json", 2*MIB) == profile_raw and
         read(report, 2*MIB) == report_raw, "VIEW_SELECTED_INPUT_CHANGED")
    view.update(schema="DMKN_OFFLINE_FORMAL_PREVIEW_VIEW_V1",
                report_sha256=report_sha256, selected_profile_sha256=profile_sha256,
                original_report_profile_sha256=original_profile,
                consistency="SAVED_RECORD_INTERNAL_CONSISTENCY_ONLY",
                mathematical_acceptance=False, network_reverified=False,
                evidence_bound=False, package_authenticated=False)
    encoded = json.dumps(view, ensure_ascii=True, sort_keys=True, allow_nan=False,
                         indent=2).encode("ascii") + b"\n"
    need(len(encoded) <= 2*MIB, "VIEW_RESULT_BOUND")
    # Every input was processed before creating the destination. Failures leave
    # no apparently successful view. No existing output can be overwritten.
    output.mkdir()
    with (output / "VIEW.json").open("xb") as stream:
        stream.write(encoded)
    if view.get("view_text") is not None:
        need(view["status"] == "TYPE_DISPLAY_COMPLETE", "VIEW_PARTIAL_TEXT")
        with (output / "TYPE.txt").open("xb") as stream:
            stream.write(view["view_text"].encode("ascii"))
    return {"status": view["status"], "output": str(output),
            "report_sha256": report_sha256, "preview_sha256": digest(raw),
            "mathematical_acceptance": False}


def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, "VIEW_ISOLATED_PYTHON_REQUIRED")
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    for name in ("package", "profile-sha256", "report", "report-sha256", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    result = view_selected(Path(args.package), args.profile_sha256, Path(args.report),
                           args.report_sha256, Path(args.output))
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, allow_nan=False))


if __name__ == "__main__":
    main()
