"""Preparation-only seven-package fixture; see PREPARE-USEFULNESS-CORPUS.md."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

MIB = 1024 * 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def safe(value, missing=False):
    path = Path(value)
    require(path.is_absolute() and ".." not in path.parts and not str(path).startswith("\\\\"), "absolute local path required")
    for current in (path, *path.parents):
        if missing and current == path:
            require(not os.path.lexists(current), "output already exists")
            continue
        info = current.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400, "reparse path refused")
    require(path == path.resolve(), "noncanonical path")
    return path


def pin(path, maximum=512 * MIB):
    path = safe(path)
    require(path.is_file() and path.stat().st_size <= maximum, "file bound/type")
    digest, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            size += len(block)
            require(size <= maximum, "file grew beyond bound")
            digest.update(block)
    return {"bytes": size, "sha256": digest.hexdigest()}


def scan(root, maximum=512 * MIB, count=65536):
    root = safe(root)
    require(root.is_dir(), "directory required")
    result, size, directories = {}, 0, 0
    def walk_error(error):
        raise error
    for directory, folders, names in os.walk(root, followlinks=False, onerror=walk_error):
        directories += 1
        require(directories <= 2 * count + 64, "directory count bound")
        for name in folders:
            require(safe(Path(directory) / name).is_dir(), "directory type")
        for name in names:
            require(len(result) < count, "file count bound")
            path = Path(directory) / name
            record = pin(path, maximum - size)
            size += record["bytes"]
            result[path.relative_to(root).as_posix()] = record
    return result


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    def reject(value):
        raise ValueError("noninteger JSON number")
    return json.loads(raw, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def save(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    require(Path(value.__file__) == path, "module origin mismatch")
    return value


def project(value):
    if type(value) is bytes:
        return {"$bytes": list(value)}
    if type(value) in (list, tuple):
        return [project(item) for item in value]
    if type(value) is dict:
        return {key: project(item) for key, item in value.items()}
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("install", "output", "pins", "pins-sha256"):
        parser.add_argument("--" + name, required=True)
    parser.add_argument("--package", action="append", required=True)
    args = parser.parse_args()
    require(all((sys.flags.dont_write_bytecode, sys.flags.ignore_environment, sys.flags.no_user_site, sys.flags.no_site)), "run with -B -E -s -S")
    require(len(args.package) == 7, "exactly seven packages required")
    install, output, pins = safe(args.install), safe(args.output, True), safe(args.pins)
    packages = [safe(path) for path in args.package]
    require(len(set([install, *packages])) == 8, "distinct input directories required")
    for source in [install, pins, Path(__file__), Path(sys.executable), *packages]:
        require(output != source and output not in source.parents and source not in output.parents, "output overlaps input")
    pin_record = pin(pins, 16 * MIB)
    require(pin_record["sha256"] == args.pins_sha256.lower(), "frozen manifest digest mismatch")
    with pins.open("rb") as stream:
        raw_pins = stream.read(16 * MIB + 1)
    require(len(raw_pins) <= 16 * MIB, "pin manifest byte bound")
    require(hashlib.sha256(raw_pins).hexdigest() == pin_record["sha256"], "manifest changed")
    frozen = strict(raw_pins)
    require(set(frozen) == {"schema", "output", "python", "helper", "install", "packages"} and type(frozen["schema"]) is int and frozen["schema"] == 1, "pin schema")
    require(Path(frozen["output"]) == output and len(frozen["packages"]) == 7, "frozen selection mismatch")
    def verify_inputs():
        require(pin(pins, 16 * MIB) == pin_record, "pin manifest changed")
        for key, path in (("python", Path(sys.executable)), ("helper", Path(__file__))):
            require(frozen[key] == {"path": str(path), **pin(path)}, key + " pin mismatch")
        for record, path in zip([frozen["install"], *frozen["packages"]], [install, *packages]):
            require(set(record) == {"path", "files"} and Path(record["path"]) == path, "input path mismatch")
            require(record["files"] == scan(path, 512 * MIB if path == install else 17 * MIB, 8193), "input file map mismatch")
        require(sum(p["bytes"] for record in frozen["packages"] for p in record["files"].values()) <= 64 * MIB, "aggregate package bound")
    verify_inputs()
    required = {"py/source_codec.py", "py/codec.py", "py/symbol_index.py", "py/peer_wire.py", "assets/foundation/seed-verified.json"}
    require(required <= set(frozen["install"]["files"]), "installed analysis inputs missing")
    require(not any(name.lower().endswith((".pyc", ".pyo")) for name in frozen["install"]["files"]), "bytecode cache refused")
    require(all(frozen["install"]["files"][name]["bytes"] <= MIB for name in required), "analysis input byte bound")
    S = module("corpus_source", install / "py/source_codec.py")
    S.configure_codec(install / "py/codec.py")
    M = module("corpus_symbols", install / "py/symbol_index.py")
    W = module("corpus_wire", install / "py/peer_wire.py")
    seed = S.C.from_projection(S.strict_json((install / "assets/foundation/seed-verified.json").read_bytes()))
    foundation = S.C.to_projection(S.Store(seed).foundation)
    output.mkdir(exist_ok=False)
    save(output / "input-pins.json", raw_pins)
    (output / "packages").mkdir()
    offers = []
    for number, (source, record) in enumerate(zip(packages, frozen["packages"]), 1):
        destination = output / "packages" / f"{number:02d}"
        destination.mkdir()
        for relative, expected in record["files"].items():
            path = destination / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with safe(source / relative).open("rb") as stream:
                raw = stream.read(expected["bytes"] + 1)
            require({"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()} == expected, "copy source changed")
            save(path, raw)
        require(scan(destination, 17 * MIB, 8193) == record["files"], "copy mismatch")
        store, root = S.read_package(destination, seed)
        value = M.describe_root(S, store, root)
        require(value["status"] == "OK", "unsupported/invalid metadata: " + str(value.get("reason", "")))
        formal = project({"replay": root, "native_ref": value["native_ref"], "semantic_target": value["semantic_ref"],
                          **{key: value[key] for key in ("universe_arity", "type_dag", "descriptor", "descriptor_id", "symbols", "trace")}})
        require(len(encoded(formal)) <= MIB, "formal metadata byte bound")
        offers.append({"package": {"path": str(destination), "manifest_sha256": pin(destination / "manifest.json")["sha256"]},
                       "descriptor_id": S.C.to_projection(value["descriptor_id"]), "formal_metadata": formal,
                       "symbols": [key.hex() for key in value["row"].symbol_keys]})
    require(len({encoded(offer["formal_metadata"]["replay"]) for offer in offers}) == 7, "duplicate roots")
    catalog = W.build_view(output / "view", foundation, offers)
    require(W.load_view(output / "view")["catalog"] == catalog and len(catalog["entries"]) == 7, "view roundtrip mismatch")
    save(output / "offers.json", encoded(offers))
    verify_inputs()
    for number, record in enumerate(frozen["packages"], 1):
        require(scan(output / "packages" / f"{number:02d}", 17 * MIB, 8193) == record["files"], "final copy mismatch")
    result = {"status": "CORPUS_FIXTURE_PREPARED_NOT_MATH_ACCEPTANCE", "mathematicalAcceptance": False, "native_stages": 0,
              "entries": 7, "pin_manifest": {"path": str(pins), **pin_record}, "output_files_excluding_result": scan(output)}
    save(output / "result.json", encoded(result))
    complete = scan(output)
    result_pin = complete.pop("result.json")
    require(complete == result["output_files_excluding_result"], "output changed during finalization")
    print(json.dumps({"status": result["status"], "result": {"path": str(output / "result.json"), **result_pin}}, sort_keys=True))


if __name__ == "__main__":
    main()
