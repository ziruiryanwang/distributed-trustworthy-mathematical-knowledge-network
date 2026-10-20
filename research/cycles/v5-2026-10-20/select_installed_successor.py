"""Stage fresh requests with unchanged mathematics/limits; never launch them."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(r"E:\Distributed Trustworthy Mathematical Knowledge Network")
OLD = ROOT/"product-local/v5-distribution-02"
NEW = ROOT/"product-local/v5-distribution-03"
INSTALL = NEW/"Mathematical Commons v5"
MIB = 1024**2
BASIS = {
    "reader": ("controls/relocated-remote-01-request.json",
               "dce01a835daec6f7f80f1977d7c1d90b4a79a4f1d30ab75cbe276a38aae8b23e",
               "caller-data", "controls"),
    "contributor": ("contributor-controls/installed-contribution-01-request.json",
                    "49c8817e41e585143954f45b0871e0b0cee0caffcdd5d55742e842c511ea65fb",
                    "contributor-data", "contributor-controls"),
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def ordinary(path, *, directory=False, fresh=False):
    need(path.is_absolute() and path.resolve() == path
         and all(not item.is_symlink() and not item.is_junction()
                 for item in (path, *path.parents)), "ORDINARY_CANONICAL_PATH")
    need(not path.exists() and path.parent.is_dir() if fresh
         else (path.is_dir() if directory else path.is_file()), "PATH_STATE")
    return path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path, maximum=8*MIB):
    ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "INPUT_BOUND")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size == path.stat().st_size, "INPUT_CHANGED")
    return raw


def checked(path, digest):
    raw = read(path)
    need(sha(raw) == digest, "ADOPTED_INPUT_CHANGED")
    return json.loads(raw)


def write(path, raw):
    ordinary(path, fresh=True)
    need(0 < len(raw) <= MIB, "STAGED_BOUND")
    with path.open("xb") as stream:
        stream.write(raw)
    need(read(path) == raw, "STAGED_READBACK")
    return {"path": str(path), "bytes": len(raw), "sha256": sha(raw)}


def relocate(value):
    if type(value) is dict:
        return {key: relocate(item) for key, item in value.items()}
    if type(value) is list:
        return [relocate(item) for item in value]
    if type(value) is str and value.startswith(str(OLD)+"\\"):
        return str(NEW)+value[len(str(OLD)):]
    return value


def main():
    need(Path.cwd() == ROOT and sys.flags.isolated and sys.flags.no_site
         and sys.dont_write_bytecode, "CANONICAL_ISOLATED_SELECTOR")
    need(len(sys.argv) == 4 and sys.argv[1] in BASIS, "MODE_RELEASE_AND_INPUT_SHA_REQUIRED")
    mode, release_sha, input_sha = sys.argv[1:]
    for value in (release_sha, input_sha):
        need(len(value) == 64 and all(ch in "0123456789abcdef" for ch in value), "SHA256")
    release = checked(INSTALL/"V5-RELEASE.json", release_sha)
    selected = checked(ROOT/"experiments/v5-local-checks/distribution-03-input.json", input_sha)
    need(release["schema"] == "DMKN_V5_DIRECTORY_RELEASE_V2"
         and release["base_role"] == "mathematical-client-v1"
         and release["build_input_sha256"] == input_sha, "EXACT_RELEASE_BASIS")
    need(set(release["sdk_sources"]) == set(selected["sdk_sources"])
         and all(release["files"][release["sdk_sources"][key]]
                 == {name: row[name] for name in ("bytes", "sha256")}
                 for key, row in selected["sdk_sources"].items()), "EXACT_SDK_MAP")
    entry = read(INSTALL/"distribution.py")
    need(release["files"]["distribution.py"] == {"bytes": len(entry), "sha256": sha(entry)},
         "INSTALLED_ENTRY_PIN")
    basis_path, basis_sha, data_name, controls_name = BASIS[mode]
    old = checked(OLD/basis_path, basis_sha)
    new = relocate(deepcopy(old))
    # Every scalar except the explicit old allocation root remains identical.
    need(new["limits"] == old["limits"]
         and new["parameters"]["operation_limits" if mode == "contributor" else "reader"]
         == relocate(old["parameters"]["operation_limits" if mode == "contributor" else "reader"]),
         "UNCHANGED_OPERATION")
    data, controls, operations = NEW/data_name, NEW/controls_name, NEW/"operations"
    ordinary(INSTALL, directory=True)
    for path in (data, controls):
        ordinary(path, directory=True, fresh=True)
    if operations.exists():
        ordinary(operations, directory=True)
    else:
        ordinary(operations, directory=True, fresh=True)
        operations.mkdir()
    for path in (operations/new["name"], operations/(new["name"]+"-request")):
        ordinary(path, directory=True, fresh=True)
    workspace = Path(new["parameters"]["workspace_path"] if mode == "contributor"
                     else new["parameters"]["reader"]["workspace_path"])
    ordinary(workspace, directory=True, fresh=True)
    data.mkdir()
    controls.mkdir()
    for name, expected in old["owner"]["sources"].items():
        need(name == old["owner"]["entry"] and Path(name).name == name, "SINGLE_RETAINED_OWNER")
        raw = read(Path(old["owner"]["root"])/name, MIB)
        need({"bytes": len(raw), "sha256": sha(raw)} == expected, "RETAINED_OWNER_CHANGED")
        write(data/name, raw)
    pins = ([old["parameters"]["packet"]] if mode == "reader" else
            [old["parameters"]["input"]["packet"], old["parameters"]["source"]])
    for pin in pins:
        raw = read(Path(pin["path"]), MIB)
        need(len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], "RETAINED_DATA_CHANGED")
        target = Path(relocate(pin["path"]))
        need(target.parent == data, "STAGED_DATA_SCOPE")
        write(target, raw)
    raw = json.dumps(new, sort_keys=True, indent=2).encode("utf-8")+b"\n"
    need(str(OLD).encode("utf-8") not in raw.replace(b"\\\\", b"\\"),
         "OLD_ALLOCATION_REFERENCE")
    request = write(controls/(new["name"]+"-request.json"), raw)
    print(json.dumps({"request": request, "release_sha256": release_sha,
        "prior_request_sha256": basis_sha, "limits_unchanged": True, "executed": False,
        "argv": [str(INSTALL/"base/receiver/runtime/python/python.exe"), "-I", "-S", "-B",
                 str(INSTALL/"distribution.py"), "launch", release_sha, "run",
                 request["path"], request["sha256"]]}))


if __name__ == "__main__":
    main()
