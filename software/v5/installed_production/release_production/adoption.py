"""Validate an owner-adopted release component, without reopening build history.

This is operative-subset validation of an externally pinned V3 file map, not
full distribution verification, publisher authentication or mathematical trust.
No host, compiler, subprocess, network operation or owner construction occurs.
"""
from pathlib import Path, PurePosixPath
import os
import stat
from types import SimpleNamespace

from production import producer as P
from aggregate_lifecycle import producer as L
from aggregate_claims import bindings as B

DESCRIPTOR_SCHEMA = "DMKN_RELEASE_AGGREGATE_ARTIFACTS_V1"
MANIFEST_SCHEMA = "DMKN_V5_DIRECTORY_RELEASE_V4"
IMAGE_ID = "9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865"
SOURCE_MODULES = (*L.SOURCE_MODULES, "release_production",
                  "release_production.producer", "release_production.adoption",
                  "admission.pin_phase", "admission.trust", "admission.clean_refusal",
                  "release_production.launch_contract")
INSTALLATION_PIN_LIMIT = 64
ARTIFACTS = {
    "stage_host": {"bytes": 68039168,
        "sha256": "263841ae256af217de2c00452c7f0688a2e9e58e6aa6d95457d5118aef04ff3c"},
    "snapshot_host": {"bytes": 6630400,
        "sha256": "a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05"},
    "guest_image": {"bytes": 1868700,
        "sha256": "0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46"},
}


def _relative(value):
    P.require(type(value) is str and 0 < len(value) <= 1024 and "\\" not in value,
              "RELEASE_RELATIVE_PATH")
    path = PurePosixPath(value)
    P.require(path.parts and not path.is_absolute() and path.as_posix() == value
              and len(path.parts) <= 32, "RELEASE_RELATIVE_SHAPE")
    for part in path.parts:
        P.require(part not in (".", "..") and not part.endswith((".", " "))
                  and not os.path.isreserved(part)
                  and not any(ord(c) < 32 or c in ':*?"<>|' for c in part),
                  "RELEASE_RELATIVE_COMPONENT")
    return path.parts


def ordinary(value, *, directory=False):
    """Canonical ordinary local file/directory; stable owner filesystem assumed."""
    P.require(type(value) in (str, Path) or isinstance(value, Path), "RELEASE_PATH_TYPE")
    path = Path(value)
    P.require(path.is_absolute() and len(path.drive) == 2 and path.drive[1] == ":"
              and path != Path(path.anchor) and str(path.resolve(strict=True)) == str(path),
              "RELEASE_CANONICAL_PATH")
    for part in path.parts[1:]:
        _relative(part)
    for candidate in (path, *path.parents):
        info = candidate.lstat()
        P.require(not getattr(info, "st_file_attributes", 0) & 0x400
                  and not stat.S_ISLNK(info.st_mode), "RELEASE_REPARSE_PATH")
        expected_directory = directory if candidate == path else True
        P.require(stat.S_ISDIR(info.st_mode) if expected_directory else stat.S_ISREG(info.st_mode),
                  "RELEASE_PATH_KIND")
    return path


def _document(pin, maximum):
    path = P.pin_fields(pin, maximum)
    ordinary(path)
    P.require(P.file_pin(path) == pin, "RELEASE_DOCUMENT_PIN")
    raw = path.read_bytes()
    P.require(0 < len(raw) <= maximum and len(raw) == pin["bytes"]
              and P.hash_bytes(raw) == pin["sha256"], "RELEASE_DOCUMENT_CHANGED")
    value = P.parse(raw)
    P.require(type(value) is dict, "RELEASE_DOCUMENT_OBJECT")
    return value


def _row(value):
    P.fields(value, ("bytes", "sha256"))
    P.uint(value["bytes"], 128*P.MIB); P.digest(value["sha256"])


def _files(value):
    P.require(type(value) is dict and 1 <= len(value) <= 20000, "RELEASE_FILE_MAP_BOUND")
    files, parents, spelling, total = set(), set(), {}, 0
    for name, row in value.items():
        parts = _relative(name); _row(row)
        key = name.casefold()
        P.require(key not in files, "RELEASE_CASE_ALIAS")
        files.add(key); total += row["bytes"]
        for n in range(1, len(parts)+1):
            prefix = "/".join(parts[:n])
            P.require(spelling.get(prefix.casefold(), prefix) == prefix,
                      "RELEASE_DIRECTORY_CASE_ALIAS")
            spelling[prefix.casefold()] = prefix
        parents.update("/".join(parts[:n]).casefold() for n in range(1, len(parts)))
    P.require(not files.intersection(parents) and total <= 2*1024**3,
              "RELEASE_FILE_MAP_TOTAL_OR_PARENT")


def load(release, source_pins, support_profile):
    """Return exact operative pins/roles from an explicitly adopted V3 container.

    The caller supplies the manifest digest in release.manifest; neither this
    function nor the descriptor infers that trust from freshly read bytes.
    Unselected manifest payloads are not opened or claimed to have been checked.
    """
    P.fields(release, ("root", "manifest", "descriptor"))
    root = ordinary(release["root"], directory=True)
    P.require(type(release["root"]) is str, "RELEASE_ROOT_STRING")
    manifest_pin, descriptor_pin = release["manifest"], release["descriptor"]
    P.require(P.pin_fields(manifest_pin, 8*P.MIB) == root/"V5-RELEASE.json",
              "RELEASE_MANIFEST_LOCATION")
    manifest = _document(manifest_pin, 8*P.MIB)
    P.require(manifest.get("schema") == MANIFEST_SCHEMA and "files" in manifest,
              "RELEASE_V3_CONTAINER")
    files = manifest["files"]; _files(files)
    P.require("V5-RELEASE.json" not in files, "RELEASE_MANIFEST_SELF_REFERENCE")
    pins = {manifest_pin["path"]: dict(manifest_pin)}

    def bind(pin, maximum=128*P.MIB):
        path = P.pin_fields(pin, maximum)
        P.require(path.is_relative_to(root), "RELEASE_SELECTED_PATH_ESCAPE")
        relative = path.relative_to(root).as_posix(); _relative(relative)
        P.require(files.get(relative) == {key: pin[key] for key in ("bytes", "sha256")},
                  "RELEASE_SELECTED_FILE_MAP")
        ordinary(path)
        P.require(P.file_pin(path) == pin, "RELEASE_SELECTED_FILE_CHANGED")
        P.require(pin["path"] not in pins or pins[pin["path"]] == pin,
                  "RELEASE_CONFLICTING_PIN")
        pins[pin["path"]] = dict(pin)
        return dict(pin)

    def relative_pin(pin):
        P.fields(pin, ("path", "bytes", "sha256"))
        path = root.joinpath(*_relative(pin["path"]))
        return {"path": str(path), "bytes": pin["bytes"], "sha256": pin["sha256"]}

    bind(descriptor_pin, P.MIB)
    descriptor = _document(descriptor_pin, P.MIB)
    P.fields(descriptor, ("schema", "foundation", "policy", "relation_image",
                          "aggregate_image", "roles", "sources"))
    P.require(descriptor["schema"] == DESCRIPTOR_SCHEMA
              and descriptor["foundation"] == B.FOUNDATION
              and descriptor["policy"] == B.POLICY
              and descriptor["relation_image"] == B.RELATION_IMAGE
              and descriptor["aggregate_image"] == IMAGE_ID,
              "RELEASE_EXACT_MATHEMATICAL_PROFILE")
    P.fields(descriptor["roles"], ARTIFACTS)
    roles = {}
    for name, row in descriptor["roles"].items():
        absolute = relative_pin(row)
        P.require({key: absolute[key] for key in ("bytes", "sha256")} == ARTIFACTS[name],
                  "RELEASE_EXACT_SELECTED_ARTIFACT:"+name)
        roles[name] = bind(absolute)
    P.require(len({row["path"] for row in roles.values()}) == 3,
              "RELEASE_DISTINCT_ARTIFACT_ROLES")
    P.fields(descriptor["sources"], SOURCE_MODULES)
    P.require(type(source_pins) is list and len(source_pins) == len(SOURCE_MODULES),
              "RELEASE_CORE_SOURCE_COUNT")
    expected_sources = {}
    for name, row in descriptor["sources"].items():
        relative = name.replace(".", "/")
        expected = "sdk/v5/"+(relative+".py" if "." in name else relative+"/__init__.py")
        P.require(type(row) is dict and row.get("path") == expected,
                  "RELEASE_LOGICAL_SOURCE_ROLE:"+name)
        pin = bind(relative_pin(row), P.MIB)
        expected_sources[pin["path"]] = pin
    P.require(len(expected_sources) == len(source_pins)
              and len({P.pin_fields(row, P.MIB) for row in source_pins}) == len(source_pins)
              and all(expected_sources.get(row["path"]) == row for row in source_pins),
              "RELEASE_EXACT_CORE_SOURCE_PINS")
    P.fields(support_profile, ("schema", "supervisor_manifest", "host", "python", "python_dll",
                              "source_pins", "runtime_pins", "image_id", "foundation", "policy"))
    P.require(support_profile["schema"] == "DMKN_V5_PRODUCER_PROFILE_V1"
              and support_profile["host"] == roles["stage_host"]
              and support_profile["image_id"] == IMAGE_ID
              and support_profile["foundation"] == B.FOUNDATION
              and support_profile["policy"] == B.POLICY,
              "RELEASE_SUPPORT_ROLES")
    P.require(type(support_profile["source_pins"]) is list
              and len(support_profile["source_pins"]) == 2
              and type(support_profile["runtime_pins"]) is list
              and 1 <= len(support_profile["runtime_pins"]) <= 128,
              "RELEASE_SUPPORT_PIN_LISTS")
    for row in [support_profile["supervisor_manifest"], support_profile["host"],
                support_profile["python"], support_profile["python_dll"],
                *support_profile["source_pins"], *support_profile["runtime_pins"]]:
        bind(row)
    supervisor = _document(support_profile["supervisor_manifest"], 8*P.MIB)
    P.require(type(supervisor.get("files")) is dict, "RELEASE_SUPERVISOR_FILE_MAP")
    support_root = Path(support_profile["supervisor_manifest"]["path"]).parent
    for relative in ("operator/commons.py", "receiver/helpers/domains.py", "receiver/helpers/run_stage.py"):
        row = supervisor["files"].get(relative); _row(row)
        bind({"path": str(support_root/relative), **row}, 4*P.MIB)
    runtime = {row["path"]: row for row in support_profile["runtime_pins"]}
    P.require(len(runtime) == len(support_profile["runtime_pins"])
              and all(runtime.get(path) == row for path, row in expected_sources.items()),
              "RELEASE_CORE_RUNTIME_BINDING")
    P.require(len(pins) <= INSTALLATION_PIN_LIMIT
              and sum(row["bytes"] for row in pins.values()) <= 512*P.MIB,
              "RELEASE_INSTALLATION_BOUND")
    # Rebind the two authority-carrying documents after payload reads. The
    # constructor/ordinary owner separately rebinds the complete operative set.
    P.require(_document(manifest_pin, 8*P.MIB) == manifest
              and _document(descriptor_pin, P.MIB) == descriptor,
              "RELEASE_ADOPTION_DOCUMENT_CHANGED")
    return SimpleNamespace(root=root, pins=pins, roles=roles,
        descriptor=descriptor, manifest_pin=dict(manifest_pin),
        descriptor_pin=dict(descriptor_pin))
