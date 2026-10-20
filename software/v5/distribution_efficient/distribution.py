"""Build/verify a pinned Windows directory release; launch existing bounded SDK.

Trusted local bootstrap, not a signature verifier or hostile-code sandbox.
No package downloads, proof production, subprocess supervisor, or migration.
"""
import time
STARTED_NS, STARTED_CPU = time.monotonic_ns(), time.process_time()
from copy import deepcopy
from contextlib import contextmanager
from contextvars import ContextVar
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
from types import ModuleType

MIB = 1024**2
BASE_SHA = "a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed"
RELATION = "9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e"
FOUNDATION = "d931d114155cf3cf0dc0b868aa88c6d38b8ada8ecafe267a5934934075782481"
POLICY = "5edfd0ee15b141b7304e26c1a39cd11f7f7e721713cf099813ae4f4442fad377"
INPUT_SCHEMA = "DMKN_V5_DISTRIBUTION_INPUT_V1"
RELEASE_SCHEMA = "DMKN_V5_DIRECTORY_RELEASE_V1"
REQUEST_SCHEMA = "DMKN_V5_INSTALLED_REQUEST_V1"
RELEASE_FILE = "V5-RELEASE.json"
ROLES = {"native", "receipt", "aggregate", "image", "frontend", "foundation"}
WRAPPERS = {
    "reader": b"from client.remote_reader import main\n",
    "serve": b"from client.serve_workspace import main\n",
}
README = """# Mathematical commons: pinned Windows directory

This installation supplies the selected v5 SDK and unchanged nested base support.
It is not a declaration that all final-v5 release/security/growth gates passed.
Licensing remains undecided; this file grants no additional license.

Trust bootstrap Python and distribution.py before executing them. Independently
adopt the V5-RELEASE.json SHA-256; hashes alone do not identify a publisher.
Keep installation files immutable; owner data/TLS secrets/state live outside.

Commands (absolute paths, Python -I -S -B, Windows):

  base/receiver/runtime/python/python.exe -I -S -B distribution.py verify RELEASE_SHA
  base/receiver/runtime/python/python.exe -I -S -B distribution.py launch RELEASE_SHA reader REQUEST REQUEST_SHA
  base/receiver/runtime/python/python.exe -I -S -B distribution.py launch RELEASE_SHA serve REQUEST REQUEST_SHA
  base/receiver/runtime/python/python.exe -I -S -B distribution.py launch RELEASE_SHA run REQUEST REQUEST_SHA

REQUEST is canonical/local JSON with schema DMKN_V5_INSTALLED_REQUEST_V1,
name, workspace_root, parameters, limits, output_limits, owner, runtime_mode.
Name is a fresh lowercase run name. workspace_root is an existing directory
disjoint from this installation. limits/output_limits retain client.launch's
finite Windows Job/census schemas. parameters are the ordinary selected SDK
entry's parameters, without runtime_adoption/foundation (injected for reader).
owner is null for reader/serve; run uses {root,entry,sources}, with sources a
relative-path -> {bytes,sha256} map for explicitly trusted local Python code.
runtime_mode is aggregate for reader, atomic or aggregate for run, null for serve.
Trusted run parameters can request release roles at any depth with exact
{"$installed":"runtime_adoption"} or {"$installed":"foundation"} singleton maps.
No automatic trust downgrade is allowed; aggregate configuration does not prove
an aggregate certificate exists. User's strategy chooses its own mathematics.

The launcher creates fresh NAME-request/preparation.json and launch.json outside
the installation, then invokes unchanged client.launch/boot with the original
wrapper clock. Mathematical Workspace data must be a disjoint persistent sibling
of NAME and NAME-request. Existing files are never overwritten; failure leaves
its partial directory for inspection, without retry or allowance renewal.

reader's ordinary parameters: workspace_path,workspace_config,create_workspace,
operation_limits,query. The query has contacts,egress_policy,specs,search_limits,
contact_lifetime_ms,selection,offer,page,packets,admission. Selection is one
provider/partition ordinal/start/candidate ordinal/packet ordinal; it is not a
usefulness ranking. The entry adds schema DMKN_V5_REMOTE_READER_V1. Inspect the
saved read outcome; completed MISS/REFUSED/NEED_SEMANTICS is not READY.

serve's parameters are schema DMKN_V5_WORKSPACE_SERVICE_V1,mode,workspace_path,
workspace_config,bind,tls,service_limits. It serves existing data remotely
read-only but opening/querying may update local metadata and holds an exclusive
workspace lock. It neither admits mathematics nor advertises through DHT.

Runtime profiles are materialized from relative pinned roles at each launch,
so moving the whole installation does not retain obsolete absolute runtime paths.
Launch checks release structure/census and selected SDK/assets; unused nested
base payload hashes are checked by explicit verify, while existing launch/boot
still validate their exact runtime/helper selection. No ambient code is adopted.
Windows OS loader/PATH assumptions remain; resource Jobs are not security
sandboxes. No archive, publishing, cloud, verifier build or proof run is implied.

Build/verify/launch assume owner-controlled local directories remain stable during
one operation. Each operation validates canonical directory ancestry once, then
checks each file's lexical name, nonreparse type and selected bytes independently.
Directory caching is never reused by the next operation; it is not protection
against concurrent filesystem mutation or a hostile filesystem.
"""


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def fields(value, expected):
    need(type(value) is dict and set(value) == set(expected), "DIST_FIELDS")


def digest(value):
    need(type(value) is str and re.fullmatch("[0-9a-f]{64}", value), "DIST_SHA256")
    return value


def row(value):
    fields(value, {"bytes", "sha256"})
    need(type(value["bytes"]) is int and 0 <= value["bytes"] <= 128*MIB, "DIST_FILE_BOUND")
    digest(value["sha256"])
    return value


def relative(value):
    need(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value, "DIST_RELATIVE")
    path = PurePosixPath(value)
    need(path.parts and not path.is_absolute() and path.as_posix() == value
         and len(path.parts) <= 32, "DIST_RELATIVE_SHAPE")
    for part in path.parts:
        need(part not in (".", "..") and not part.endswith((".", " "))
             and not os.path.isreserved(part)
             and not any(ord(c) < 32 or c in ':*?"<>|' for c in part), "DIST_PATH_PART")
    return path.parts


_DIRECTORIES = ContextVar("dmkn_distribution_checked_directories", default=None)


@contextmanager
def path_scope():
    """Fresh directory-only validation cache, for a stable trusted local tree.

    Nested scopes start fresh and restore their caller's scope. No file type,
    freshness, hash, failed check or cached scope crosses an operation boundary.
    This reduces metadata I/O, not the selected content-verification work.
    """
    token = _DIRECTORIES.set(set())
    try:
        yield
    finally:
        _DIRECTORIES.reset(token)


def _directory(path, checked):
    # Full resolution is needed only when first adopting an existing directory.
    # File leaves are separately checked below, never added to this cache.
    for ancestor in reversed((path, *path.parents)):
        key = str(ancestor)
        if key in checked:
            continue
        need(str(ancestor.resolve()) == key, "DIST_CANONICAL_LOCAL_PATH")
        info = ancestor.lstat()
        need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
             "DIST_ORDINARY_ANCESTOR")
        checked.add(key)


def ordinary(value, *, directory=False, fresh=False):
    path = Path(value)
    need(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":"
         and path != Path(path.anchor), "DIST_CANONICAL_LOCAL_PATH")
    for part in path.parts[1:]:
        relative(part)
    checked = _DIRECTORIES.get()
    if checked is None:
        # Standalone callers keep the predecessor's uncached path validation.
        need(str(path.resolve()) == str(path), "DIST_CANONICAL_LOCAL_PATH")
        for ancestor in path.parents:
            info = ancestor.lstat()
            need(stat.S_ISDIR(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
                 "DIST_ORDINARY_ANCESTOR")
    else:
        _directory(path.parent, checked)
    if fresh:
        need(not os.path.lexists(path), "DIST_FRESH_PATH")
    elif directory and checked is not None:
        _directory(path, checked)
    else:
        # Verified canonical ordinary parent + lexical component + nonreparse
        # leaf confines the target without resolving its entire ancestry again.
        # File-map spelling/census and hash binding remain independent checks.
        info = path.lstat()
        need(not getattr(info, "st_file_attributes", 0) & 0x400
             and (stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)),
             "DIST_ORDINARY_TARGET")
    return path


def overlap(left, right):
    return left.is_relative_to(right) or right.is_relative_to(left)


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, "DIST_DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def reject(unused):
        raise ValueError("DIST_INTEGER_JSON_REQUIRED")
    return json.loads(raw.decode("utf-8"), object_pairs_hook=pairs,
                      parse_float=reject, parse_constant=reject)


def read(path, maximum=8*MIB):
    path = ordinary(path)
    size = path.stat().st_size
    need(0 < size <= maximum, "DIST_INPUT_SIZE")
    with path.open("rb") as stream:
        raw = stream.read(maximum+1)
    need(len(raw) == size == path.stat().st_size, "DIST_INPUT_CHANGED")
    return raw


def checked_json(path, expected, maximum=8*MIB):
    raw = read(path, maximum)
    need(hashlib.sha256(raw).hexdigest() == digest(expected), "DIST_INPUT_PIN")
    return parse(raw)


def pinned(path, expected):
    path = ordinary(path)
    row(expected)
    need(path.stat().st_size == expected["bytes"], "DIST_PIN_SIZE:"+str(path))
    with path.open("rb") as stream:
        actual = hashlib.file_digest(stream, "sha256").hexdigest()
    need(path.stat().st_size == expected["bytes"] and actual == expected["sha256"],
         "DIST_PIN:"+str(path))
    return path


def absolute_pin(value):
    fields(value, {"path", "bytes", "sha256"})
    ordinary(value["path"])
    return row({key: value[key] for key in ("bytes", "sha256")})


def pin(path):
    path = ordinary(path)
    with path.open("rb") as stream:
        sha = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha}


def file_map(value):
    need(type(value) is dict and 1 <= len(value) <= 20000, "DIST_FILE_COUNT")
    aliases, spelling, total, files, directories = set(), {}, 0, set(), set()
    for name, expected in value.items():
        parts = relative(name)
        key = name.casefold()
        need(key not in aliases, "DIST_CASE_ALIAS")
        aliases.add(key)
        for n in range(1, len(parts)+1):
            prefix = "/".join(parts[:n])
            need(spelling.get(prefix.casefold(), prefix) == prefix, "DIST_DIRECTORY_CASE_ALIAS")
            spelling[prefix.casefold()] = prefix
        row(expected)
        total += expected["bytes"]
        files.add(key)
        directories.update("/".join(parts[:n]).casefold() for n in range(1, len(parts)))
    need(not files.intersection(directories) and total <= 2*1024**3, "DIST_MAP_BOUND_OR_FILE_PARENT")
    return value


def write_new(path, raw):
    ordinary(path, fresh=True)
    with path.open("xb") as stream:
        stream.write(raw)
    need(path.stat().st_size == len(raw), "DIST_OUTPUT_SIZE")


def copy_pinned(source, target, expected):
    source = ordinary(source)
    row(expected)
    need(source.stat().st_size == expected["bytes"], "DIST_COPY_INPUT_SIZE")
    target.parent.mkdir(parents=True, exist_ok=True)
    ordinary(target, fresh=True)
    observed, size = hashlib.sha256(), 0
    with source.open("rb") as incoming, target.open("xb") as outgoing:
        while block := incoming.read(MIB):
            size += len(block)
            need(size <= expected["bytes"], "DIST_COPY_GREW")
            observed.update(block)
            outgoing.write(block)
    need(size == expected["bytes"] == source.stat().st_size
         and observed.hexdigest() == expected["sha256"], "DIST_COPY_PIN")
    pinned(target, expected)


def census(root, expected):
    actual, directories = set(), 0
    for parent, children, names in os.walk(root, followlinks=False):
        ordinary(parent, directory=True)
        directories += 1
        need(directories <= 20000, "DIST_DIRECTORY_BOUND")
        for child in children:
            ordinary(Path(parent)/child, directory=True)
        for name in names:
            path = ordinary(Path(parent)/name)
            actual.add(path.relative_to(root).as_posix())
            need(len(actual) <= 20001, "DIST_CENSUS_BOUND")
    need(actual == set(expected) | {RELEASE_FILE}, "DIST_EXACT_FILE_CENSUS")


def build(input_path, expected, destination):
    with path_scope():
        return _build(input_path, expected, destination)


def _build(input_path, expected, destination):
    value = checked_json(input_path, expected)
    fields(value, {"schema", "base_root", "base_manifest", "sdk_sources", "preparation_template",
                   "assets", "aggregate_image", "lean_runtime", "distribution_source"})
    need(value["schema"] == INPUT_SCHEMA, "DIST_INPUT_SCHEMA")
    output = ordinary(destination, directory=True, fresh=True)
    base = ordinary(value["base_root"], directory=True)
    base_pin = value["base_manifest"]
    absolute_pin(base_pin)
    need(Path(base_pin["path"]) == base/"RELEASE-MANIFEST.json" and base_pin["sha256"] == BASE_SHA,
         "DIST_FIXED_BASE_MANIFEST")
    nested = checked_json(base_pin["path"], BASE_SHA)
    base_files = file_map(nested["files"])
    template_pin = value["preparation_template"]
    absolute_pin(template_pin)
    template = checked_json(template_pin["path"], template_pin["sha256"], MIB)
    fields(template, {"schema", "producer", "image", "worker", "native_executable", "lean_root",
                      "lean_runtime_pins", "source_pins"})
    need(template["schema"] == "DMKN_V5_PREPARATION_PROFILE_V1", "DIST_PREPARATION_SCHEMA")
    producer = template["producer"]
    fields(producer, {"schema", "supervisor_manifest", "host", "python", "python_dll",
                      "source_pins", "runtime_pins", "image_id", "foundation", "policy"})
    need(producer["schema"] == "DMKN_V5_PRODUCER_PROFILE_V1"
         and (producer["image_id"], producer["foundation"], producer["policy"])
         == (RELATION, FOUNDATION, POLICY) and producer["supervisor_manifest"] == base_pin,
         "DIST_PREPARATION_FOUNDATION")
    digest(value["aggregate_image"])
    need(value["aggregate_image"] not in ("00"*32, RELATION), "DIST_AGGREGATE_IMAGE")
    fields(value["assets"], ROLES)
    need(value["assets"]["receipt"] == producer["host"]
         and value["assets"]["image"] == template["image"]
         and value["assets"]["frontend"] == template["native_executable"], "DIST_TEMPLATE_ROLES")
    source_pin = value["distribution_source"]
    absolute_pin(source_pin)
    source_identity = {key: source_pin[key] for key in ("bytes", "sha256")}
    pinned(source_pin["path"], source_identity)
    # A bounded owner may execute an exact source snapshot. Adopt byte identity,
    # not the builder's original folder; installed launch origin stays unchanged.
    pinned(Path(__file__).resolve(), source_identity)
    files, copies, sources, roles = {}, {}, {}, {}
    def select(name, path, expected_row):
        relative(name)
        need(name not in files and not overlap(output, Path(path)), "DIST_OUTPUT_INPUT_OVERLAP")
        files[name] = row(deepcopy(expected_row))
        copies[name] = ordinary(path)
        return {"path": name, **files[name]}
    for name, expected_row in base_files.items():
        select("base/"+name, base.joinpath(*relative(name)), expected_row)
    select("base/RELEASE-MANIFEST.json", base_pin["path"], absolute_pin(base_pin))
    need(type(value["sdk_sources"]) is dict and 1 <= len(value["sdk_sources"]) <= 141, "DIST_SDK_COUNT")
    for name, item in value["sdk_sources"].items():
        parts = relative(name)
        need(len(parts) >= 2 and parts[0] in ("v5", "portable")
             and Path(parts[-1]).suffix in (".py", ".mjs")
             and not name.startswith(("v5/location/", "v5/portable_runtime/")), "DIST_SDK_PATH")
        expected_row = absolute_pin(item)
        need(expected_row["bytes"] <= 2*MIB, "DIST_SDK_FILE_BOUND")
        selected = select("sdk/"+name, item["path"], expected_row)
        sources[name] = selected["path"]
    required = {"v5/client/launch.py", "v5/client/boot.py", "v5/client/workspace.py",
                "v5/client/runtime.py", "v5/client/remote_reader.py", "v5/client/serve_workspace.py",
                "v5/authoring/worker.py", "v5/production/producer.py", "v5/production/__init__.py"}
    need(required <= set(sources), "DIST_SDK_REQUIRED")
    for role, item in value["assets"].items():
        selected = select("assets/"+role+"/"+Path(item["path"]).name,
                          item["path"], absolute_pin(item))
        roles[role] = selected["path"]
    old_lean = ordinary(template["lean_root"], directory=True)
    need(type(value["lean_runtime"]) is dict and 1 <= len(value["lean_runtime"]) <= 128,
         "DIST_LEAN_RUNTIME")
    original_lean = {Path(item["path"]).relative_to(old_lean).as_posix(): item
                    for item in template["lean_runtime_pins"]}
    need(len(original_lean) == len(template["lean_runtime_pins"])
         and original_lean == value["lean_runtime"], "DIST_EXACT_LEAN_RUNTIME")
    lean = [select("assets/lean/"+name, item["path"], absolute_pin(item))
            for name, item in value["lean_runtime"].items()]
    select("distribution.py", source_pin["path"], absolute_pin(source_pin))
    def base_role(item):
        absolute_pin(item)
        path = Path(item["path"])
        need(path.is_relative_to(base), "DIST_TEMPLATE_BASE_ROLE")
        name = path.relative_to(base).as_posix()
        expected_row = {key: item[key] for key in ("bytes", "sha256")}
        need(base_files.get(name) == expected_row, "DIST_TEMPLATE_BASE_PIN")
        return {"path": "base/"+name, **expected_row}
    def role_pin(role):
        name = roles[role]
        return {"path": name, **files[name]}
    relative_profile = {
        "schema": template["schema"], "image": role_pin("image"),
        "worker": {"path": sources["v5/authoring/worker.py"], **files[sources["v5/authoring/worker.py"]]},
        "native_executable": role_pin("frontend"), "lean_root": "assets/lean",
        "lean_runtime_pins": lean,
        "source_pins": [{"path": name, **files[name]} for key, name in sources.items()
                        if key.startswith("v5/") and key.endswith(".py")],
        "producer": {"schema": producer["schema"], "supervisor_manifest":
            {"path": "base/RELEASE-MANIFEST.json", **files["base/RELEASE-MANIFEST.json"]},
            "host": role_pin("receipt"), "python": base_role(producer["python"]),
            "python_dll": base_role(producer["python_dll"]),
            "runtime_pins": [base_role(item) for item in producer["runtime_pins"]],
            "source_pins": [{"path": sources["v5/production/"+name],
                            **files[sources["v5/production/"+name]]}
                           for name in ("__init__.py", "producer.py")],
            "image_id": RELATION, "foundation": FOUNDATION, "policy": POLICY}}
    generated = {"README.md": README.encode("utf-8"),
                 **{"owners/"+name+".py": raw for name, raw in WRAPPERS.items()}}
    for name, raw in generated.items():
        need(name not in files, "DIST_GENERATED_COLLISION")
        files[name] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    manifest = {"schema": RELEASE_SCHEMA, "base_manifest_sha256": BASE_SHA,
        "files": files, "sdk_sources": sources, "roles": roles,
        "aggregate_image": value["aggregate_image"], "preparation": relative_profile,
        "build_input_sha256": expected}
    validate_manifest(manifest)
    need(not overlap(output, base) and not overlap(output, ordinary(input_path)), "DIST_OUTPUT_SCOPE")
    output.mkdir()
    for name, path in copies.items():
        copy_pinned(path, output.joinpath(*relative(name)), files[name])
    for name, raw in generated.items():
        target = output.joinpath(*relative(name))
        target.parent.mkdir(parents=True, exist_ok=True)
        write_new(target, raw)
    raw = encode(manifest)
    need(len(raw) <= 8*MIB, "DIST_RELEASE_SIZE")
    write_new(output/RELEASE_FILE, raw)
    verify_release(output, manifest, full=True)
    return {"status": "DIRECTORY_CREATED_AND_EXACTLY_VERIFIED", "root": str(output),
            "manifest_sha256": hashlib.sha256(raw).hexdigest(), "files": len(files),
            "bytes": sum(item["bytes"] for item in files.values()), "mathematical_acceptance": False}


def validate_manifest(manifest):
    fields(manifest, {"schema", "base_manifest_sha256", "files", "sdk_sources", "roles",
                      "aggregate_image", "preparation", "build_input_sha256"})
    need(manifest["schema"] == RELEASE_SCHEMA and manifest["base_manifest_sha256"] == BASE_SHA,
         "DIST_RELEASE_SCHEMA")
    digest(manifest["build_input_sha256"])
    digest(manifest["aggregate_image"])
    need(manifest["aggregate_image"] not in ("00"*32, RELATION), "DIST_AGGREGATE_IMAGE")
    files = file_map(manifest["files"])
    need(RELEASE_FILE not in files and {"distribution.py", "README.md", "owners/reader.py",
         "owners/serve.py", "base/RELEASE-MANIFEST.json"} <= set(files), "DIST_FIXED_FILES")
    need(files["base/RELEASE-MANIFEST.json"]["sha256"] == BASE_SHA, "DIST_BASE_PIN")
    fields(manifest["roles"], ROLES)
    for role, name in manifest["roles"].items():
        relative(name)
        need(name.startswith("assets/"+role+"/") and name in files, "DIST_ROLE_SCOPE")
    sources = manifest["sdk_sources"]
    need(type(sources) is dict and 1 <= len(sources) <= 141, "DIST_SOURCE_COUNT")
    for name, path in sources.items():
        parts = relative(name)
        need(len(parts) >= 2 and parts[0] in ("v5", "portable") and path == "sdk/"+name
             and path in files and files[path]["bytes"] <= 2*MIB
             and Path(parts[-1]).suffix in (".py", ".mjs"), "DIST_SOURCE_MAP")
    def check_tree(value):
        if type(value) is dict:
            if "path" in value:
                fields(value, {"path", "bytes", "sha256"})
                relative(value["path"])
                need(files.get(value["path"]) == {key: value[key] for key in ("bytes", "sha256")},
                     "DIST_PROFILE_FILE_ROLE")
            else:
                for item in value.values():
                    check_tree(item)
        elif type(value) is list:
            need(len(value) <= 128, "DIST_PROFILE_LIST_BOUND")
            for item in value:
                check_tree(item)
    profile = manifest["preparation"]
    fields(profile, {"schema", "producer", "image", "worker", "native_executable", "lean_root",
                     "lean_runtime_pins", "source_pins"})
    need(profile["schema"] == "DMKN_V5_PREPARATION_PROFILE_V1"
         and profile["lean_root"] == "assets/lean", "DIST_RELATIVE_PREPARATION")
    p = profile["producer"]
    fields(p, {"schema", "supervisor_manifest", "host", "python", "python_dll", "source_pins",
               "runtime_pins", "image_id", "foundation", "policy"})
    need(p["schema"] == "DMKN_V5_PRODUCER_PROFILE_V1"
         and (p["image_id"], p["foundation"], p["policy"]) == (RELATION, FOUNDATION, POLICY)
         and p["supervisor_manifest"]["path"] == "base/RELEASE-MANIFEST.json"
         and p["host"]["path"] == manifest["roles"]["receipt"]
         and profile["image"]["path"] == manifest["roles"]["image"]
         and profile["native_executable"]["path"] == manifest["roles"]["frontend"]
         and profile["worker"]["path"] == "sdk/v5/authoring/worker.py", "DIST_PROFILE_ROLE_BINDING")
    check_tree(profile)
    need(all(item["path"].startswith("assets/lean/") for item in profile["lean_runtime_pins"]),
         "DIST_LEAN_ROLE_SCOPE")
    need(all(item["path"].startswith("base/") for item in
             [p["python"], p["python_dll"], *p["runtime_pins"]]), "DIST_PYTHON_ROLE_SCOPE")
    return manifest


def verify_release(root, manifest, *, full):
    # Even the final verification nested inside build revalidates directories.
    with path_scope():
        return _verify_release(root, manifest, full=full)


def _verify_release(root, manifest, *, full):
    validate_manifest(manifest)
    census(root, manifest["files"])
    for name, expected in manifest["files"].items():
        if full or not name.startswith("base/") or name == "base/RELEASE-MANIFEST.json":
            pinned(root.joinpath(*relative(name)), expected)
    base = checked_json(root/"base/RELEASE-MANIFEST.json", BASE_SHA)
    need({name[5:]: value for name, value in manifest["files"].items()
          if name.startswith("base/") and name != "base/RELEASE-MANIFEST.json"} == base["files"],
         "DIST_EXACT_NESTED_BASE_MAP")


def materialize(root, value):
    if type(value) is dict:
        if "path" in value:
            return {**value, "path": str(root.joinpath(*relative(value["path"])))}
        return {key: str(root/"assets/lean") if key == "lean_root" else materialize(root, item)
                for key, item in value.items()}
    if type(value) is list:
        return [materialize(root, item) for item in value]
    return value


def substitute(value, roles, depth=0):
    """Two explicit local-owner placeholders, not arbitrary code/path lookup."""
    need(depth <= 64, "DIST_PARAMETER_DEPTH")
    if type(value) is dict:
        if "$installed" in value:
            fields(value, {"$installed"})
            need(type(value["$installed"]) is str and value["$installed"] in roles,
                 "DIST_PARAMETER_ROLE")
            return deepcopy(roles[value["$installed"]])
        return {key: substitute(item, roles, depth+1) for key, item in value.items()}
    if type(value) is list:
        return [substitute(item, roles, depth+1) for item in value]
    return value


def launch(expected, command, request_path, request_sha):
    with path_scope():
        return _launch(expected, command, request_path, request_sha)


def _launch(expected, command, request_path, request_sha):
    need(command in ("reader", "serve", "run"), "DIST_COMMAND")
    root = ordinary(Path(__file__).resolve().parent, directory=True)
    manifest = checked_json(root/RELEASE_FILE, expected)
    verify_release(root, manifest, full=False)
    executable = root/"base/receiver/runtime/python/python.exe"
    need(os.name == "nt" and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize and Path(sys.executable).resolve() == executable,
         "DIST_INSTALLED_ISOLATED_PYTHON")
    request = checked_json(request_path, request_sha, MIB)
    fields(request, {"schema", "name", "workspace_root", "parameters", "limits", "output_limits",
                     "owner", "runtime_mode"})
    need(request["schema"] == REQUEST_SCHEMA and type(request["name"]) is str
         and re.fullmatch("[a-z0-9][a-z0-9-]{0,63}", request["name"]), "DIST_REQUEST_SCHEMA")
    workspace = ordinary(request["workspace_root"], directory=True)
    need(not overlap(workspace, root), "DIST_STATE_INSTALLATION_DISJOINT")
    controls = ordinary(workspace/(request["name"]+"-request"), fresh=True, directory=True)
    run = ordinary(workspace/request["name"], fresh=True, directory=True)
    need(type(request["parameters"]) is dict, "DIST_PARAMETERS")
    parameters = deepcopy(request["parameters"])
    sources = {name: manifest["files"][path] for name, path in manifest["sdk_sources"].items()}
    if command == "run":
        owner = request["owner"]
        fields(owner, {"root", "entry", "sources"})
        owner_root = ordinary(owner["root"], directory=True)
        relative(owner["entry"])
        need(type(owner["sources"]) is dict and 1 <= len(owner["sources"]) <= 64
             and owner["entry"] in owner["sources"] and owner["entry"].endswith(".py"),
             "DIST_TRUSTED_OWNER_SELECTION")
        need(not overlap(run, owner_root) and not overlap(controls, owner_root), "DIST_OWNER_OUTPUT_OVERLAP")
        for name, expected_row in file_map(owner["sources"]).items():
            need(name.endswith(".py") and expected_row["bytes"] <= 2*MIB, "DIST_OWNER_SOURCE_BOUND")
            pinned(owner_root.joinpath(*relative(name)), expected_row)
            sources["owner/"+name] = expected_row
        entry = owner["entry"]
    else:
        need(request["owner"] is None, "DIST_BUILTIN_OWNER_ONLY")
        owner_root, entry = root/"owners", command+".py"
        sources["owner/"+entry] = manifest["files"]["owners/"+entry]
        schema = "DMKN_V5_REMOTE_READER_V1" if command == "reader" else "DMKN_V5_WORKSPACE_SERVICE_V1"
        need(parameters.get("schema", schema) == schema, "DIST_ENTRY_SCHEMA")
        parameters["schema"] = schema
    if command == "serve":
        need(request["runtime_mode"] is None, "DIST_SERVICE_NO_RUNTIME_OWNER")
    else:
        mode = request["runtime_mode"]
        need(mode in ("atomic", "aggregate") and (command != "reader" or mode == "aggregate"),
             "DIST_EXPLICIT_ISSUER_MODE")
        if command == "reader":
            need("runtime_adoption" not in parameters and "foundation" not in parameters,
                 "DIST_RELEASE_RUNTIME_PARAMETERS_RESERVED")
    # Check the mathematical workspace scope before creating control data.
    if "workspace_path" in parameters:
        data = Path(parameters["workspace_path"])
        need(data.is_absolute() and not overlap(data, controls) and not overlap(data, run)
             and not overlap(data, root), "DIST_MATHEMATICAL_DATA_SCOPE")
    need(time.process_time()-STARTED_CPU <= 30 and time.monotonic_ns()-STARTED_NS < 120*10**9,
         "DIST_PRELAUNCH_LIMIT")
    controls.mkdir()
    write_new(controls/"request.json", encode(request))
    if command != "serve":
        profile_path = controls/"preparation.json"
        write_new(profile_path, encode(materialize(root, manifest["preparation"])))
        def selected(role):
            name = manifest["roles"][role]
            return {"path": str(root.joinpath(*relative(name))), **manifest["files"][name]}
        adoption = {
            "schema": "DMKN_V5_CLIENT_RUNTIME_V1", "preparation_profile": pin(profile_path),
            "native": selected("native"), "receipt": selected("receipt"),
            "aggregate": None if request["runtime_mode"] == "atomic" else
                {"executable": selected("aggregate"), "image": manifest["aggregate_image"]}}
        if command == "reader":
            parameters.update(runtime_adoption=adoption, foundation=selected("foundation"))
        else:
            parameters = substitute(parameters,
                {"runtime_adoption": adoption, "foundation": selected("foundation")})
    plan = {"schema": "DMKN_V5_CLIENT_LAUNCH_V1", "name": request["name"],
        "installation_root": str(root/"base"), "workspace_root": str(workspace),
        "source_roots": {"v5": str(root/"sdk/v5"), "portable": str(root/"sdk/portable"),
                         "owner": str(owner_root)}, "sources": sources, "owner_entry": entry,
        "parameters": parameters, "limits": request["limits"], "output_limits": request["output_limits"]}
    plan_path = controls/"launch.json"
    plan_raw = encode(plan)
    write_new(plan_path, plan_raw)
    plan_sha = hashlib.sha256(plan_raw).hexdigest()
    # Load only exact release-adopted source. Preserve the FIRST public wrapper
    # clocks: preparing a plan must not silently renew the original allowance.
    launcher = root/"sdk/v5/client/launch.py"
    expected_row = manifest["files"]["sdk/v5/client/launch.py"]
    pinned(launcher, expected_row)
    source = read(launcher, 2*MIB)
    need(hashlib.sha256(source).hexdigest() == expected_row["sha256"], "DIST_LAUNCH_SOURCE_CHANGED")
    module = ModuleType("_dmkn_installed_client_launch")
    module.__file__ = str(launcher)
    sys.modules[module.__name__] = module
    exec(compile(source, str(launcher), "exec", dont_inherit=True), module.__dict__)
    module.STARTED_NS, module.STARTED_CPU = STARTED_NS, STARTED_CPU
    sys.argv = [str(launcher), str(plan_path), plan_sha]
    return module.main()


def main():
    need(os.name == "nt", "DIST_WINDOWS_ONLY")
    args = sys.argv[1:]
    if len(args) == 4 and args[0] == "build":
        print(json.dumps(build(*args[1:]), sort_keys=True), flush=True)
        return 0
    if len(args) == 2 and args[0] == "verify":
        root = ordinary(Path(__file__).resolve().parent, directory=True)
        manifest = checked_json(root/RELEASE_FILE, args[1])
        verify_release(root, manifest, full=True)
        print(json.dumps({"status": "EXACT_DIRECTORY_VERIFIED", "mathematical_acceptance": False}), flush=True)
        return 0
    if len(args) == 5 and args[0] == "launch":
        return launch(*args[1:])
    raise ValueError("USAGE: build INPUT SHA OUTPUT | verify RELEASE_SHA | launch RELEASE_SHA reader|serve|run REQUEST SHA")


if __name__ == "__main__":
    raise SystemExit(main())
