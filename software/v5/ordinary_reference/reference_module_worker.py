"""One reference-backed build and two rereads inside the caller's single Job.

The protected controller authenticates the reference and exact original snapshot
before this worker. We bind bytes across phases; neither a plan nor these hashes
grants mathematical authority. Original proof requests are never reopened. No
retry, new allowance, owner opening, library compilation or snapshot copy occurs.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import stat
import subprocess
import sys

MIB = 1024**2
REQUEST_SCHEMA = "DMKN_ORDINARY_REFERENCE_MODULE_REQUEST_V1"
PLAN_SCHEMA = "DMKN_ORDINARY_REFERENCE_MODULE_PLAN_V1"
PENDING_SCHEMA = "DMKN_ORDINARY_REFERENCE_MODULE_PENDING_V1"
PENDING_ASSURANCE = "LOCAL_CHECKED_REFERENCE_MODULE_PENDING_REREADS"
REQUEST_FIELDS = {"schema", "semantic_id", "context_root", "foundation_id", "module_name",
    "targets", "unit_ids", "units", "reference_id", "parent_delta_id", "reference_plan_sha256"}
REPORT_FIELDS = {"schema", "assurance", "semantic_id", "context_root", "foundation_id",
    "module_name", "targets", "unit_ids", "reference_id", "parent_delta_id", "reference_plan_sha256",
    "direct_imports", "names", "inventories", "added_names", "added_inventories",
    "matched_unit_indices", "matched_names", "matched_inventories", "units_checked", "units_matched",
    "checking_passes", "basis_rows", "usable_basis_rows", "reference_public_units",
    "reference_public_names", "generated_names", "artifact_parts"}
PLAN_FIELDS = {"schema", "reference_id", "snapshot_id", "support_id", "semantic_id", "foundation_id",
    "implementation_id", "registration_context_root", "parent_delta_id", "original_roots",
    "reference_report", "replay_request", "generated_plan"}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def fields(value, expected, code):
    need(type(value) is dict and set(value) == expected, code)


def hexid(value, *, empty=False):
    need(type(value) is str and ((empty and value == "") or
         (len(value) == 64 and all(c in "0123456789abcdef" for c in value))), "REFERENCE_WORKER_ID")
    return value


def ordinary_path(value):
    need(type(value) is str and 0 < len(value) <= 32768 and
         re.match(r"^[A-Za-z]:[\\/]", value) is not None and
         not any(ord(c) < 32 for c in value) and ";" not in value and
         not any(p in (".", "..") for p in value.replace("\\", "/").split("/")),
         "REFERENCE_WORKER_PATH")
    path = Path(value)
    need(path.is_absolute(), "REFERENCE_WORKER_ABSOLUTE_PATH")
    return path


def pin(path, maximum):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1 and
         not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT and
         0 < info.st_size <= maximum, "REFERENCE_WORKER_BOUNDED_FILE")
    count, digest = 0, hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(min(65536, maximum + 1 - count)):
            count += len(block)
            need(count <= maximum, "REFERENCE_WORKER_FILE_GROWTH")
            digest.update(block)
    need(count == info.st_size, "REFERENCE_WORKER_FILE_SIZE_CHANGED")
    return count, digest.hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "REFERENCE_WORKER_DUPLICATE_JSON")
        result[key] = value
    return result


def read_object(path, expected, maximum):
    need(pin(path, maximum) == expected, "REFERENCE_WORKER_JSON_PIN")
    with path.open("rb") as handle:
        raw = handle.read(maximum+1)
    need((len(raw), hashlib.sha256(raw).hexdigest()) == expected, "REFERENCE_WORKER_JSON_CHANGED")

    def integer(token):
        need(len(token) <= 20 and token.isascii() and token.isdigit() and
             (len(token) == 1 or token[0] != "0"), "REFERENCE_WORKER_UINT64")
        value = int(token)
        need(value <= 18446744073709551615, "REFERENCE_WORKER_UINT64")
        return value

    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object, parse_int=integer,
        parse_float=lambda _: need(False, "REFERENCE_WORKER_FLOAT"),
        parse_constant=lambda _: need(False, "REFERENCE_WORKER_CONSTANT"))
    need(type(value) is dict, "REFERENCE_WORKER_JSON_OBJECT")
    return value


def name_key(value):
    # Full semantic-name validation remains native/controller work. This exact
    # serialization is only for equality/census within already protected plans.
    need(type(value) is list, "REFERENCE_WORKER_NAME_SHAPE")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def module_text(value, *, bridge=False):
    need(type(value) is list and 1 <= len(value) <= 16, "REFERENCE_WORKER_MODULE_NAME")
    parts = []
    for row in value:
        need(type(row) is list and len(row) == 2 and type(row[0]) is int and row[0] == 0,
             "REFERENCE_WORKER_MODULE_COMPONENT")
        fields(row[1], {"$bytes"}, "REFERENCE_WORKER_MODULE_BYTES")
        data = row[1]["$bytes"]
        need(type(data) is list and 1 <= len(data) <= 96 and
             all(type(n) is int and 0 <= n < 128 for n in data), "REFERENCE_WORKER_MODULE_BYTES")
        text = bytes(data).decode("ascii")
        need(re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text) is not None, "REFERENCE_WORKER_MODULE_IDENTIFIER")
        parts.append(text)
    text = ".".join(parts)
    if bridge:
        need(len(parts) == 1 and text.startswith("DMKNBridge_"), "REFERENCE_WORKER_BRIDGE_NAME")
        hexid(text[11:])
    return text


def parts_for(base):
    return (base, Path(str(base)+".server"), Path(str(base)+".private"),
            base.with_suffix(".ir.sig"), base.with_suffix(".ir"))


def selected_reference(plan, request, forbidden):
    """Bind a protected reference, separate generated map and their metadata.

    Original map entries contain paths, not authentication hashes. Their exact
    snapshot identity is a controller prerequisite. Initial actual hashes here
    are immutable-within-operation checks, never independent authentication.
    """
    fields(plan, PLAN_FIELDS, "REFERENCE_WORKER_PLAN_FIELDS")
    need(plan["schema"] == PLAN_SCHEMA, "REFERENCE_WORKER_PLAN_SCHEMA")
    for key in ("reference_id", "snapshot_id", "support_id", "semantic_id", "foundation_id",
                "implementation_id", "registration_context_root"):
        hexid(plan[key])
    hexid(plan["parent_delta_id"], empty=True)
    for key in ("reference_id", "parent_delta_id", "semantic_id", "foundation_id"):
        need(request[key] == plan[key], "REFERENCE_WORKER_REQUEST_PLAN")
    metadata, documents = {}, {}
    for role, maximum in (("reference_report", 32*MIB), ("replay_request", 16*MIB), ("generated_plan", 4*MIB)):
        row = plan[role]
        fields(row, {"path", "bytes", "sha256"}, "REFERENCE_WORKER_METADATA_PIN_FIELDS")
        path = ordinary_path(row["path"])
        need(path not in forbidden and path not in metadata and type(row["bytes"]) is int and
             0 < row["bytes"] <= maximum, "REFERENCE_WORKER_METADATA_ALIAS_OR_BOUND")
        expected = row["bytes"], hexid(row["sha256"])
        documents[role] = read_object(path, expected, maximum)
        metadata[path] = expected
    report, replay, generated = (documents[key] for key in ("reference_report", "replay_request", "generated_plan"))
    need(report.get("schema") == "DMKN_ORDINARY_REFERENCE_BASE_REPORT_V2" and
         report.get("assurance") == "CORRESPONDENCE_REQUIRES_CURRENT_PROTECTED_WARRANTS" and
         report.get("context_root") == plan["registration_context_root"], "REFERENCE_WORKER_REPORT_BINDING")
    for key in ("snapshot_id", "support_id", "semantic_id", "foundation_id"):
        need(report.get(key) == plan[key], "REFERENCE_WORKER_REPORT_IDENTITY")
    roots = plan["original_roots"]
    need(type(roots) is list and 1 <= len(roots) <= 16, "REFERENCE_WORKER_ROOTS")
    root_names = []
    for row in roots:
        fields(row, {"module", "import_all", "is_exported", "is_meta"}, "REFERENCE_WORKER_ROOT_FIELDS")
        need(all(type(row[key]) is int and row[key] == expected for key, expected in
                 (("import_all", 0), ("is_exported", 1), ("is_meta", 0))), "REFERENCE_WORKER_ROOT_FLAGS")
        module_text(row["module"])
        root_names.append(row["module"])
    need(len({name_key(n) for n in root_names}) == len(root_names), "REFERENCE_WORKER_ROOT_DUPLICATE")
    fields(replay, {"schema", "mode", "modules", "artifacts"}, "REFERENCE_WORKER_REPLAY_FIELDS")
    need(replay["schema"] == "DMKN_ORDINARY_BASELINE_ARTIFACT_REQUEST_V1" and
         replay["mode"] == "replay" and replay["modules"] == root_names and
         type(replay["artifacts"]) is list and 1 <= len(replay["artifacts"]) <= 4096,
         "REFERENCE_WORKER_REPLAY_BINDING")
    pins, module_names, total = {}, set(), 0
    forbidden = forbidden | set(metadata)
    for row in replay["artifacts"]:
        fields(row, {"module", "parts"}, "REFERENCE_WORKER_ORIGINAL_FIELDS")
        name = module_text(row["module"])
        need(name not in module_names, "REFERENCE_WORKER_MODULE_DUPLICATE")
        module_names.add(name)
        matrix = row["parts"]
        need(type(matrix) is list and len(matrix) == 2 and all(type(r) is list for r in matrix) and
             len(matrix[0]) == 3 and len(matrix[1]) == 2, "REFERENCE_WORKER_ORIGINAL_PARTS")
        paths = tuple(ordinary_path(p) for p in matrix[0]+matrix[1])
        need(paths[0].suffix == ".olean" and paths == parts_for(paths[0]), "REFERENCE_WORKER_ORIGINAL_LAYOUT")
        for path in paths:
            need(path not in pins and path not in forbidden, "REFERENCE_WORKER_ORIGINAL_ALIAS")
            expected = pin(path, 64*MIB)
            total += expected[0]
            need(total <= 512*MIB, "REFERENCE_WORKER_ORIGINAL_BOUND")
            pins[path] = expected
    need(all(module_text(n) in module_names for n in root_names), "REFERENCE_WORKER_ROOT_MISSING")
    fields(generated, {"schema", "reference_id", "support_id", "delta_id", "modules", "bindings"},
           "REFERENCE_WORKER_GENERATED_FIELDS")
    need(generated["schema"] == "DMKN_ORDINARY_REFERENCE_GENERATED_PLAN_V1" and
         generated["reference_id"] == plan["reference_id"] and generated["support_id"] == plan["support_id"] and
         generated["delta_id"] == plan["parent_delta_id"], "REFERENCE_WORKER_GENERATED_BINDING")
    modules, bindings = generated["modules"], generated["bindings"]
    need(type(modules) is list and len(modules) <= 32 and type(bindings) is list and len(bindings) <= 1024 and
         bool(plan["parent_delta_id"]) == bool(modules) == bool(bindings), "REFERENCE_WORKER_GENERATED_CENSUS")
    imports, generated_total, ids, added = root_names, 0, set(), set()
    for row in modules:
        fields(row, {"delta_id", "module_name", "direct_imports", "added_names", "artifact_parts"},
               "REFERENCE_WORKER_GENERATED_MODULE_FIELDS")
        identity, name = hexid(row["delta_id"]), module_text(row["module_name"], bridge=True)
        need(identity not in ids and name not in module_names and row["direct_imports"] == imports,
             "REFERENCE_WORKER_GENERATED_CHAIN")
        ids.add(identity); module_names.add(name)
        need(type(row["added_names"]) is list and 1 <= len(row["added_names"]) <= 4096 and
             type(row["artifact_parts"]) is list and len(row["artifact_parts"]) == 5,
             "REFERENCE_WORKER_GENERATED_OUTPUTS")
        for value in row["added_names"]:
            key = name_key(value)
            need(key not in added and len(added) < 16384, "REFERENCE_WORKER_GENERATED_NAME_BOUND")
            added.add(key)
        paths, module_total = [], 0
        for part in row["artifact_parts"]:
            fields(part, {"path", "bytes", "sha256"}, "REFERENCE_WORKER_GENERATED_PART_FIELDS")
            path = ordinary_path(part["path"])
            need(path not in pins and path not in forbidden and type(part["bytes"]) is int and
                 0 < part["bytes"] <= 64*MIB, "REFERENCE_WORKER_GENERATED_PART_BOUND")
            expected = part["bytes"], hexid(part["sha256"])
            module_total += expected[0]; generated_total += expected[0]
            need(module_total <= 64*MIB and generated_total <= 256*MIB, "REFERENCE_WORKER_GENERATED_BOUND")
            need(pin(path, expected[0]) == expected, "REFERENCE_WORKER_GENERATED_PART_PIN")
            pins[path] = expected; paths.append(path)
        need(paths[0].name == name+".olean" and tuple(paths) == parts_for(paths[0]),
             "REFERENCE_WORKER_GENERATED_LAYOUT")
        imports = [row["module_name"]]
    if modules:
        need(modules[-1]["delta_id"] == plan["parent_delta_id"], "REFERENCE_WORKER_GENERATED_PARENT")
    realized = set()
    for unit in bindings:
        fields(unit, {"unit_id", "outputs", "realization"}, "REFERENCE_WORKER_GENERATED_UNIT_FIELDS")
        hexid(unit["unit_id"])
        need(unit["realization"] == "added" and type(unit["outputs"]) is list and
             1 <= len(unit["outputs"]) <= 4096, "REFERENCE_WORKER_GENERATED_REALIZATION")
        for row in unit["outputs"]:
            fields(row, {"name", "export_id", "kind", "level_params", "inventory_sha256"},
                   "REFERENCE_WORKER_GENERATED_OUTPUT_FIELDS")
            key = name_key(row["name"])
            need(key in added and key not in realized, "REFERENCE_WORKER_GENERATED_BINDING_CENSUS")
            realized.add(key)
    need(realized == added, "REFERENCE_WORKER_GENERATED_NAMES")
    need(module_text(request["module_name"], bridge=True) not in module_names, "REFERENCE_WORKER_OUTPUT_COLLISION")
    return metadata, pins, imports, report, len(realized)


def main(args):
    need(len(args) == 9 and os.name == "nt" and sys.flags.isolated and sys.flags.no_site and
         sys.dont_write_bytecode and not sys.flags.optimize, "REFERENCE_WORKER_PROFILE")
    lean, source, helper_text, sysroot, inventory, request, plan_path, output, report = args
    lean, source, sysroot, inventory, request, plan_path, output, report = map(ordinary_path,
        (lean, source, sysroot, inventory, request, plan_path, output, report))
    helpers = tuple(ordinary_path(part) for part in helper_text.split(os.pathsep))
    need(1 <= len(helpers) <= 8 and len(set(helpers)) == len(helpers) and
         sum(len(a)+3 for a in args) <= 30000 and lean == sysroot/"bin/lean.exe" and
         all(p.is_file() for p in (lean, source, inventory, request, plan_path)) and
         all(p.is_dir() for p in (sysroot/"lib/lean", output.parent, report.parent, *helpers)),
         "REFERENCE_WORKER_INPUTS")
    pending = report.with_name(report.name+".pending")
    trace_path = report.with_name(report.name+".phases.jsonl")
    parts = parts_for(output)
    fresh = (*parts, report, pending, trace_path)
    limits = {source: MIB, inventory: MIB, request: 4*MIB, plan_path: MIB}
    need(len(limits) == 4 and len(set(fresh)) == len(fresh) and
         not set(fresh).intersection((lean, *limits)) and all(not os.path.lexists(p) for p in fresh),
         "REFERENCE_WORKER_FRESH_OUTPUTS")
    input_pins = {p: pin(p, maximum) for p, maximum in limits.items()}
    plan = read_object(plan_path, input_pins[plan_path], MIB)
    selected = read_object(request, input_pins[request], 4*MIB)
    fields(selected, REQUEST_FIELDS, "REFERENCE_WORKER_REQUEST_FIELDS")
    need(selected["schema"] == REQUEST_SCHEMA and selected["reference_plan_sha256"] == input_pins[plan_path][1],
         "REFERENCE_WORKER_REQUEST_PLAN_PIN")
    metadata, parent_pins, direct_imports, original_report, generated_names = selected_reference(
        plan, selected, set((*fresh, lean, *limits)))

    def unchanged_inputs():
        need(all(pin(p, limits[p]) == value for p, value in input_pins.items()), "REFERENCE_WORKER_INPUT_CHANGED")
        need(all(pin(p, value[0]) == value for p, value in metadata.items()), "REFERENCE_WORKER_METADATA_CHANGED")
        need(all(pin(p, value[0]) == value for p, value in parent_pins.items()), "REFERENCE_WORKER_PARENT_CHANGED")
        need(not os.path.lexists(report), "REFERENCE_WORKER_PREMATURE_REPORT")

    def artifact_pins():
        total, result = 0, {}
        for path in parts:
            value = pin(path, 64*MIB-total)
            total += value[0]; result[path] = value
        return result

    def read_pending(expected):
        value = read_object(pending, expected, 8*MIB)
        fields(value, REPORT_FIELDS, "REFERENCE_WORKER_PENDING_FIELDS")
        need(value["schema"] == PENDING_SCHEMA and value["assurance"] == PENDING_ASSURANCE,
             "REFERENCE_WORKER_PENDING_SCHEMA")
        for key in ("semantic_id", "context_root", "foundation_id", "module_name", "targets", "unit_ids",
                    "reference_id", "parent_delta_id", "reference_plan_sha256"):
            need(value[key] == selected[key], "REFERENCE_WORKER_PENDING_REQUEST")
        need(value["direct_imports"] == direct_imports and value["basis_rows"] == 581 and
             value["usable_basis_rows"] == len(original_report["usable_basis_names"]) and
             value["reference_public_units"] == original_report["public_unit_count"] and
             value["reference_public_names"] == original_report["public_name_count"] and
             value["generated_names"] == generated_names and value["checking_passes"] == 2 and
             type(value["units_matched"]) is int and value["units_matched"] == 0 and
             all(value[key] == [] for key in ("matched_unit_indices", "matched_names", "matched_inventories")),
             "REFERENCE_WORKER_PENDING_CENSUS")
        return value

    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    # This path loads the selected internal tool/support, not the mathematical
    # reference. Native reference imports clear searchPathRef and use exact maps.
    env["LEAN_PATH"] = os.pathsep.join(map(str, (sysroot/"lib/lean", *helpers)))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
    command = [str(lean), "-DElab.async=false", "-R", str(source.parent), "--run", str(source)]
    with trace_path.open("xb") as trace:
        def event(phase, state, exit_code=None):
            row = {"schema": "DMKN_ORDINARY_REFERENCE_MODULE_PHASE_TRACE_V1", "phase": phase,
                   "event": state, "exit_code": exit_code}
            trace.write(json.dumps(row, sort_keys=True, separators=(",", ":")).encode("ascii")+b"\n")
            trace.flush()

        def invoke(phase):
            unchanged_inputs()
            event(phase, "STARTED")
            code = subprocess.call(command+[phase, *map(str, (sysroot, inventory, request, plan_path, output, pending))],
                cwd=Path.cwd(), env=env, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            event(phase, "EXITED", code)
            return code

        code = invoke("build")
        if code != 0:
            return code
        selected_parts = artifact_pins()
        pending_pin = pin(pending, 8*MIB)
        value = read_pending(pending_pin)
        need(type(value["artifact_parts"]) is list and len(value["artifact_parts"]) == 5,
             "REFERENCE_WORKER_OUTPUT_PART_CENSUS")
        for path, row in zip(parts, value["artifact_parts"]):
            fields(row, {"path", "bytes"}, "REFERENCE_WORKER_OUTPUT_PART_FIELDS")
            need(ordinary_path(row["path"]) == path and type(row["bytes"]) is int and
                 row["bytes"] == selected_parts[path][0], "REFERENCE_WORKER_OUTPUT_PART_BINDING")

        def unchanged_outputs():
            need(pin(pending, 8*MIB) == pending_pin and artifact_pins() == selected_parts,
                 "REFERENCE_WORKER_OUTPUT_CHANGED")

        for phase in ("reread-private", "reread-exported"):
            # The next invocation checks every input/parent after the preceding
            # phase and before this phase. Do not hash a large original snapshot
            # twice consecutively at the same transition.
            unchanged_outputs()
            code = invoke(phase)
            if code != 0:
                return code
        value = read_pending(pending_pin)
        value["schema"] = "DMKN_ORDINARY_REFERENCE_MODULE_OUTPUT_V1"
        value["assurance"] = "LOCAL_CHECKED_REFERENCE_MODULE_CONTROLLER_BOUND_IDENTITIES"
        raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                         separators=(",", ":")).encode("ascii")
        need(0 < len(raw) <= 8*MIB, "REFERENCE_WORKER_FINAL_BOUND")
        unchanged_inputs(); unchanged_outputs()
        with report.open("xb") as handle:
            handle.write(raw); handle.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
