"""Sequential local module construction and rereads inside ONE selected Job.

The controller pins the full runtime/helper profile before and after execution;
those protected inputs must not change concurrently. This worker additionally
binds exact native source/request/inventory and generated artifacts between the
three phases. These hashes are not an adversarial filesystem sandbox. Each Lean
process exits before the next starts, releasing imported compacted regions.
There is no retry, per-phase grant, timer renewal, compilation or owner opening.
"""
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess
import sys


MIB = 1024**2
PENDING_SCHEMA = "DMKN_ORDINARY_MODULE_PENDING_V1"
PENDING_ASSURANCE = "LOCAL_CHECKED_MODULE_PENDING_REREADS"
REPORT_FIELDS = {"schema", "assurance", "semantic_id", "context_root", "foundation_id",
    "module_name", "targets", "unit_ids", "names", "inventories", "units_checked",
    "checking_passes", "basis_rows", "artifact_parts"}


def need(condition, code):
    if not condition:
        raise ValueError(code)


def pin(path, maximum):
    metadata = path.lstat()
    need(stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1 and
         not getattr(metadata, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT and
         0 < metadata.st_size <= maximum, "MODULE_WORKER_ORDINARY_BOUNDED_FILE")
    count, digest = 0, hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(min(65536, maximum + 1 - count)):
            count += len(block)
            need(count <= maximum, "MODULE_WORKER_FILE_GROWTH")
            digest.update(block)
    need(count == metadata.st_size, "MODULE_WORKER_FILE_SIZE_CHANGED")
    return count, digest.hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "MODULE_WORKER_JSON_DUPLICATE")
        result[key] = value
    return result


def read_pending(path, expected_pin):
    need(pin(path, 8*MIB) == expected_pin, "MODULE_WORKER_PENDING_CHANGED")
    with path.open("rb") as handle:
        raw = handle.read(8*MIB+1)
    need((len(raw), hashlib.sha256(raw).hexdigest()) == expected_pin,
         "MODULE_WORKER_PENDING_READ_CHANGED")
    value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                       parse_constant=lambda _: need(False, "MODULE_WORKER_JSON_CONSTANT"))
    need(type(value) is dict and set(value) == REPORT_FIELDS and
         value["schema"] == PENDING_SCHEMA and value["assurance"] == PENDING_ASSURANCE,
         "MODULE_WORKER_PENDING_REQUIRED")
    return value


def main(args):
    need(len(args) == 8 and os.name == "nt" and sys.flags.isolated and
         sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,
         "MODULE_WORKER_PROFILE")
    lean, source, helpers_raw, sysroot, inventory, request, output, report = args
    paths = tuple(map(Path, (lean, source, sysroot, inventory, request, output, report)))
    helpers = tuple(Path(part) for part in helpers_raw.split(os.pathsep))
    need(1 <= len(helpers) <= 8 and len(set(helpers)) == len(helpers) and
         all(p.is_absolute() and ".." not in p.parts for p in (*paths, *helpers)),
         "MODULE_WORKER_PATHS")
    lean, source, sysroot, inventory, request, output, report = paths
    need(lean == sysroot/"bin/lean.exe" and all(p.is_file() for p in
         (lean, source, inventory, request)) and all(p.is_dir() for p in
         (sysroot/"lib/lean", output.parent, report.parent, *helpers)),
         "MODULE_WORKER_INPUTS")
    need(sum(len(value)+3 for value in args) <= 30000, "MODULE_WORKER_ARGV_BOUND")
    pending = report.with_name(report.name+".pending")
    trace_path = report.with_name(report.name+".phases.jsonl")
    parts = (output, Path(str(output)+".server"), Path(str(output)+".private"),
             output.with_suffix(".ir.sig"), output.with_suffix(".ir"))
    fresh = (*parts, report, pending, trace_path)
    need(len(set(fresh)) == len(fresh) and all(not os.path.lexists(p) for p in fresh) and
         not set(fresh).intersection((lean, source, inventory, request)),
         "MODULE_WORKER_FRESH_OUTPUTS")
    limits = {source: MIB, inventory: MIB, request: 4*MIB}
    need(len(limits) == 3, "MODULE_WORKER_INPUT_ALIAS")
    input_pins = {path: pin(path, maximum) for path, maximum in limits.items()}

    def unchanged_inputs():
        need(all(pin(path, limits[path]) == expected for path, expected in input_pins.items()),
             "MODULE_WORKER_INPUT_CHANGED")
        need(not os.path.lexists(report), "MODULE_WORKER_PREMATURE_FINAL_REPORT")

    def artifact_pins():
        total, result = 0, {}
        for path in parts:
            value = pin(path, 64*MIB-total)
            total += value[0]
            result[path] = value
        return result

    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(("LEAN", "PYTHON")) and key.upper() != "PATH"}
    env["LEAN_PATH"] = os.pathsep.join(map(str, (sysroot/"lib/lean", *helpers)))
    env["PATH"] = os.pathsep.join((str(Path(sys.executable).parent), str(lean.parent)))
    command = [str(lean), "-DElab.async=false", "-R", str(source.parent), "--run", str(source)]
    # Every descendant inherits the SAME enclosing Job. subprocess.call waits
    # for this phase's process; no new supervisor or allowance is constructed.
    with trace_path.open("xb") as trace:
        def event(phase, state, exit_code=None):
            row = {"schema": "DMKN_ORDINARY_MODULE_PHASE_TRACE_V1", "phase": phase,
                   "event": state, "exit_code": exit_code}
            trace.write(json.dumps(row, sort_keys=True, separators=(",", ":")).encode("ascii")+b"\n")
            trace.flush()

        def invoke(phase, arguments):
            unchanged_inputs()
            event(phase, "STARTED")
            code = subprocess.call(command+[phase, *map(str, arguments)], cwd=Path.cwd(),
                env=env, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            event(phase, "EXITED", code)
            return code

        code = invoke("build", (sysroot, inventory, request, output, pending))
        if code != 0:
            return code
        unchanged_inputs()
        selected_parts = artifact_pins()
        pending_pin = pin(pending, 8*MIB)
        pending_value = read_pending(pending, pending_pin)
        rows = pending_value["artifact_parts"]
        need(type(rows) is list and len(rows) == 5, "MODULE_WORKER_PART_COUNT")
        for path, row in zip(parts, rows):
            need(type(row) is dict and set(row) == {"path", "bytes"} and
                 type(row["path"]) is str and Path(row["path"]) == path and
                 type(row["bytes"]) is int and row["bytes"] == selected_parts[path][0],
                 "MODULE_WORKER_PENDING_PART_BINDING")

        def unchanged_outputs():
            need(pin(pending, 8*MIB) == pending_pin and artifact_pins() == selected_parts,
                 "MODULE_WORKER_PHASE_OUTPUT_CHANGED")

        for phase in ("reread-private", "reread-exported"):
            unchanged_inputs()
            unchanged_outputs()
            code = invoke(phase, (sysroot, request, output, pending))
            if code != 0:
                return code
            unchanged_inputs()
            unchanged_outputs()

        # Pending evidence stays retained. Only now may an overall success report
        # exist; the controller still validates it independently before MODULE.json.
        value = read_pending(pending, pending_pin)
        value["schema"] = "DMKN_ORDINARY_MODULE_OUTPUT_V1"
        value["assurance"] = "LOCAL_CHECKED_MODULE_CONTROLLER_BOUND_IDENTITIES"
        raw = json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                         separators=(",", ":")).encode("ascii")
        need(0 < len(raw) <= 8*MIB, "MODULE_WORKER_FINAL_REPORT_BOUND")
        unchanged_inputs()
        unchanged_outputs()
        with report.open("xb") as handle:
            handle.write(raw)
            handle.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
