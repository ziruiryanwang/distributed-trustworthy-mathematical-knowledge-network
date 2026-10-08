"""Selected owner-local Lean gates. Prepared records are not SQL commits.

No old Node/fixture Store import, global catalog or SQL capability. Source is
cooperative owner-authorized executable input; this is not a source sandbox.
An operator-local configuration binds the installation and writable domains.
"""
from __future__ import annotations

import functools
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import domains as domain_module
from domains import Domains, PYTHON_FLAGS, require_python_profile

MIB = 1024 * 1024
MAX_FILE = 64 * MIB


class CheckingFailure(Exception):
    def __init__(self, code, diagnostics=None, evidence=None, diagnostics_truncated=False):
        super().__init__(str(code)[:2048])
        self.code = str(code)[:2048]
        self.diagnostics = diagnostics or []
        self.evidence = evidence or []
        self.diagnostics_truncated = bool(diagnostics_truncated)


class StageUncertain(Exception):
    def __init__(self, code, stage, evidence=None):
        super().__init__(str(code)[:2048])
        self.code, self.stage, self.evidence = str(code)[:2048], stage, evidence or []


class _StageFailed(CheckingFailure):
    def __init__(self, directory, evidence):
        super().__init__("NATIVE_STAGE_FAILED", evidence=[evidence])
        self.directory = directory


def require(ok, code):
    if not ok:
        raise CheckingFailure(code)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(CheckingFailure("NONFINITE_JSON")))


def read(path, limit=MAX_FILE):
    with Path(path).open("rb") as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, "FILE_BYTE_LIMIT")
    return raw


def write_new(path, raw, domains):
    path = domains.require_write(path)
    require(len(raw) <= MAX_FILE, "PREPARED_FILE_BOUND")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)
        stream.flush()


def file_record(path):
    path = Path(path).resolve(strict=True)
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(read(path))}


def check_file(pin, domains):
    require(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}, "FILE_PIN_FIELDS")
    path = domains.require_read(pin["path"])
    raw = read(path)
    require(type(pin["bytes"]) is int and len(raw) == pin["bytes"] and sha(raw) == pin["sha256"].lower(), "FILE_PIN_CHANGED")
    return path


def check_interpreter(pin):
    """The sole external file-domain exception is this exact interpreter."""
    require(type(pin) is dict and set(pin) == {"path", "bytes", "sha256"}, "PYTHON_PIN_FIELDS")
    path = Path(pin["path"]).resolve(strict=True)
    require(path == Path(sys.executable).resolve(strict=True), "PYTHON_PIN_EXACT_EXECUTABLE")
    raw = read(path)
    require(type(pin["bytes"]) is int and len(raw) == pin["bytes"]
            and sha(raw) == pin["sha256"].lower(), "PYTHON_PIN_CHANGED")
    return path


def module(name, pin, domains):
    path = check_file(pin, domains)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "MODULE_LOADER")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def project(value):
    if type(value) is bytes:
        return {"$bytes": list(value)}
    if type(value) in (list, tuple):
        return [project(item) for item in value]
    if type(value) is dict:
        return {key: project(item) for key, item in value.items()}
    return value


def public(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        try:
            self.checkpoint()
            result = method(self, *args, **kwargs)
            self.checkpoint()
            return result
        except StageUncertain:
            raise
        except Exception as error:
            if self.pending_stage is not None:
                raise StageUncertain("STAGE_OUTCOME_UNCERTAIN:" + str(error), self.pending_stage, list(self.completed)) from error
            if isinstance(error, CheckingFailure):
                if not error.evidence:
                    error.evidence = list(self.completed)
                raise
            raise CheckingFailure("SELECTED_CHECK_FAILED:" + type(error).__name__ + ":" + str(error),
                                  evidence=list(self.completed)) from error
    return wrapped


class Checker:
    def __init__(self, config: dict, work_dir: Path, allocate_stage: callable):
        require_python_profile()
        self.config, self.files = config, config["files"]
        self.domains = Domains.from_config(config)
        self.work_dir = self.domains.require_work(work_dir)
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.allocate_stage = allocate_stage
        self.started, self.child_seconds = time.monotonic(), 0.0
        self.pending_stage, self.completed = None, []
        self.metrics = {"source_module_loads": 0, "seed_reads": 0, "canonical_package_reads": 0,
                        "canonical_package_bytes": 0, "evidence_reads": 0, "stage_allocations": 0,
                        "pipeline_children": 0, "package_cache_hits": 0}
        self.packages = {}
        self.evidence_cache = set()
        limits = config.get("limits", {})
        self.package_limit = limits.get("packages", 16)
        self.byte_limit = limits.get("canonical_bytes", 64 * MIB)
        self.inprocess_seconds = limits.get("inprocess_seconds", 120)
        self.source_limit = limits.get("source_bytes", 65536)
        require(all(type(x) is int and x > 0 for x in (self.package_limit, self.byte_limit,
                self.inprocess_seconds, self.source_limit)) and self.package_limit <= 16
                and self.byte_limit <= 64 * MIB and self.source_limit <= 65536, "SELECTED_LIMIT_PROFILE")
        needed = {"seed", "inventory", "source_codec", "codec", "symbol_index", "agent_client",
                  "core_olean", "bootstrap_olean", "checking", "runner", "lean", "domains"}
        require(needed <= set(self.files), "CHECKING_CONFIG_FILES")
        for name in needed:
            check_file(self.files[name], self.domains)
        require(check_file(self.files["checking"], self.domains) == Path(__file__).resolve()
                == self.domains.install / "py" / "checking.py", "CHECKER_SELF_PIN")
        require(check_file(self.files["runner"], self.domains) == self.domains.install / "py" / "run_stage.py", "RUNNER_PIN_DOMAIN")
        require(check_file(self.files["domains"], self.domains) == Path(domain_module.__file__).resolve()
                == self.domains.install / "py" / "domains.py", "DOMAINS_SELF_PIN")
        self.domains.require_lean(self.files["lean"]["path"])
        self.S = module("operation_integration_source", self.files["source_codec"], self.domains)
        self.S.configure_codec(check_file(self.files["codec"], self.domains))
        self.M = module("operation_integration_symbols", self.files["symbol_index"], self.domains)
        self.metrics["source_module_loads"] += 1
        self.seed = self.S.C.from_projection(self.S.strict_json(read(check_file(self.files["seed"], self.domains))))
        self.metrics["seed_reads"] += 1
        self.python_pin = file_record(sys.executable)

    def checkpoint(self):
        require(time.monotonic() - self.started - self.child_seconds <= self.inprocess_seconds, "INPROCESS_TIME_LIMIT")

    def read_package(self, path):
        path = self.domains.require_package(path)
        self.metrics["canonical_package_reads"] += 1
        begin = time.monotonic()
        try:
            store, root = self.S.read_package(path, self.seed)
            require(store.total_bytes <= self.byte_limit, "SELECTED_PACKAGE_BYTES")
            self.metrics["canonical_package_bytes"] += store.total_bytes
            return store, root
        finally:
            self.metrics["package_read_wall_seconds"] = self.metrics.get("package_read_wall_seconds", 0.0) + time.monotonic() - begin

    def package(self, entry):
        require(type(entry) is dict and set(entry) == {"path", "manifest_sha256"}, "PACKAGE_PIN_FIELDS")
        require(type(entry["path"]) is str and type(entry["manifest_sha256"]) is str
                and re.fullmatch(r"[a-fA-F0-9]{64}", entry["manifest_sha256"]), "PACKAGE_PIN_TYPES")
        try:
            path = self.domains.require_package(entry["path"])
        except (OSError, ValueError) as error:
            raise CheckingFailure("SELECTED_BYTES_REFUSED", [{"phase": "selected-package-path",
                                  "type": type(error).__name__, "detail": str(error)[:2048]}]) from error
        key = (str(path), entry["manifest_sha256"].lower())
        if key in self.packages:
            self.metrics["package_cache_hits"] += 1
            return self.packages[key]
        require(len(self.packages) < 32, "SELECTED_PACKAGE_CACHE_COUNT")
        try:
            require(sha(read(path / "manifest.json", 16 * MIB)) == key[1], "SELECTED_MANIFEST_BINDING")
            value = self.read_package(path)
        except (OSError, ValueError, CheckingFailure) as error:
            raise CheckingFailure("SELECTED_BYTES_REFUSED", [{"phase": "selected-package-bytes",
                                  "type": type(error).__name__, "detail": str(error)[:2048]}]) from error
        require(sum(x[0].total_bytes for x in self.packages.values()) + value[0].total_bytes <= 64 * MIB, "SELECTED_CACHE_BYTES")
        self.packages[key] = value
        return value

    def import_package(self, entry):
        store, root = self.package(entry)
        destination = self.domains.require_write(self.work_dir / "packages" / entry["manifest_sha256"].lower())
        if not destination.exists():
            self.S.export_package(store, root, destination)
        copied = {"path": str(destination), "manifest_sha256": sha(read(destination / "manifest.json", 16 * MIB))}
        saved, saved_root = self.package(copied)
        require(saved_root == root and saved.closure(root) == store.closure(root), "PACKAGE_COPY_BINDING")
        return copied

    def union(self, packages):
        require(type(packages) is list and 1 <= len(packages) <= self.package_limit, "CONTEXT_PACKAGE_COUNT")
        inputs = [self.package(package) for package in packages]
        joined, roots = self.S.Store(self.seed), []
        for store, root in inputs:
            for ref, payload in store.objects.values():
                joined.add(ref[1], ref[2], payload)
            for key, inventory in store.inventories.items():
                require(key not in joined.inventories or self.S.same(joined.inventories[key], inventory), "INCOMPATIBLE_INVENTORY")
                joined.inventories[key] = inventory
            if root not in roots:
                roots.append(root)
        require(joined.total_bytes <= self.byte_limit, "CONTEXT_CANONICAL_BYTES")
        plan = self.S.make_plan(joined, roots)
        require(len(encoded(plan)) <= MAX_FILE, "CONTEXT_PLAN_BYTES")
        return joined, roots, plan

    def metadata(self, store, root):
        value = self.M.describe_root(self.S, store, root)
        require(value["status"] == "OK", "CANDIDATE_TYPE_FRAGMENT:" + value.get("reason", ""))
        formal = project({"replay": root, "native_ref": value["native_ref"],
                          "semantic_target": value["semantic_ref"], "universe_arity": value["universe_arity"],
                          "type_dag": value["type_dag"], "descriptor": value["descriptor"],
                          "descriptor_id": value["descriptor_id"], "symbols": value["symbols"], "trace": value["trace"]})
        require(len(encoded(formal)) <= MIB, "FORMAL_METADATA_BYTES")
        return value, formal

    def evidence(self, items):
        require(type(items) is list and 1 <= len(items) <= 16, "SELECTED_EVIDENCE_COUNT")
        for item in items:
            key = sha(encoded(item))
            if key in self.evidence_cache:
                continue
            self.metrics["evidence_reads"] += 1
            require(item["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE", "FAILED_EVIDENCE_NOT_ACCEPTANCE")
            require(type(item["files"]) is list and len(item["files"]) <= 4096, "SELECTED_EVIDENCE_FILES")
            for pin in item["files"]:
                check_file(pin, self.domains)
            check_file(item["plan"], self.domains)
            check_file(item["receipt"], self.domains)
            directory = self.domains.require_work(item["directory"])
            require(Path(item["plan"]["path"]) == directory / "plan.json"
                    and Path(item["receipt"]["path"]) == directory / "stage.json", "EVIDENCE_RECEIPT_PATH")
            receipt = strict(read(item["receipt"]["path"], MIB))
            require(receipt["stage"] == str(item["stage"]) and receipt["status"] == item["status"], "EVIDENCE_STAGE_BINDING")
            self.validate_receipt(directory, strict(read(item["plan"]["path"])), item["plan"]["sha256"])
            self.evidence_cache.add(key)

    def context(self, context):
        require(context.get("kind") == "context", "CONTEXT_KIND")
        self.evidence(context["evidence"])
        store, roots, plan = self.union(context["packages"])
        require(plan == context["plan"], "CONTEXT_PLAN_CHANGED")
        return store, roots, plan

    def stage(self, purpose, extra, steps):
        self.checkpoint()
        lease = self.allocate_stage(purpose)
        require(type(lease) is dict and set(lease) == {"id", "directory", "seconds", "memory_mib", "bytes"}, "STAGE_LEASE_FIELDS")
        require((type(lease["id"]) is int and lease["id"] >= 0) or type(lease["id"]) is str, "STAGE_LEASE_ID_TYPE")
        require(re.fullmatch(r"[A-Za-z0-9_-]{1,64}", str(lease["id"])), "STAGE_LEASE_ID")
        require(type(lease["directory"]) is str and type(lease["seconds"]) is int
                and 1 <= lease["seconds"] <= 300 and type(lease["memory_mib"]) is int
                and 1 <= lease["memory_mib"] <= 4096 and type(lease["bytes"]) is int
                and 1 <= lease["bytes"] <= 512 * MIB, "STAGE_LEASE_LIMITS")
        directory = self.domains.require_stage(lease["directory"], self.work_dir)
        require(not directory.exists(), "NEW_REQUEST_STAGE_REQUIRED")
        self.pending_stage = dict(lease)
        self.metrics["stage_allocations"] += 1
        preparation = self.domains.require_write(self.work_dir / ("prepare-" + str(lease["id"])))
        preparation.mkdir(parents=True, exist_ok=False)
        inputs = []
        for key, name in (("agent_client", "native/AgentClient.lean"), ("core_olean", "lib/AgentReplayCore.olean"),
                          ("bootstrap_olean", "lib/BootstrapSupport.olean"), ("inventory", "inventory.json"),
                          ("seed", "seed.json"), ("source_codec", "source_codec.py"), ("codec", "codec.py"),
                          ("checking", "checking.py"), ("domains", "domains.py")):
            inputs.append({**self.files[key], "as": name})
        for name, value in extra.items():
            if isinstance(value, Path):
                pin = file_record(value)
            else:
                path = preparation / name
                write_new(path, value if type(value) is bytes else encoded(value), self.domains)
                pin = file_record(path)
            inputs.append({**pin, "as": name})
        plan = {"schema": 2, "domains": self.domains.as_dict(), "domains_source": self.files["domains"],
                "request_directory": str(self.work_dir), "stage_directory": str(directory), "stage": str(lease["id"]),
                "expected_runner_sha256": self.files["runner"]["sha256"], "lean": self.files["lean"],
                "python": self.python_pin, "seconds": lease["seconds"], "memory_mib": lease["memory_mib"],
                "bytes": lease["bytes"], "inputs": inputs, "steps": steps}
        path = preparation / "execution-plan.json"
        write_new(path, encoded(plan), self.domains)
        plan_hash = sha(read(path))
        command = [sys.executable, *PYTHON_FLAGS, str(check_file(self.files["runner"], self.domains)), "--directory", str(directory),
                   "--stage", str(lease["id"]), "--expected-plan-sha256", plan_hash, str(path)]
        start = time.monotonic()
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
        finally:
            self.child_seconds += time.monotonic() - start
        require(len(result.stdout) <= MIB and len(result.stderr) <= MIB, "RUNNER_STREAM_LIMIT")
        write_new(preparation / "runner.stdout", result.stdout, self.domains)
        write_new(preparation / "runner.stderr", result.stderr, self.domains)
        self.validate_receipt(directory, plan, plan_hash, allow_failure=True)
        receipt = strict(read(directory / "stage.json", MIB))
        require(receipt["stage"] == str(lease["id"]), "ALLOCATED_STAGE_RECEIPT_BINDING")
        succeeded = receipt["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
        require(result.returncode == (0 if succeeded else 1), "RUNNER_EXIT")
        pins = [file_record(directory / "stage.json"), file_record(directory / "plan.json")]
        pins += receipt["outputs"] + [row[field] for row in receipt["steps"] for field in ("stdout", "stderr")]
        pins += [{key: row[key] for key in ("path", "bytes", "sha256")} for row in receipt["inputs"]]
        evidence = {"directory": str(directory), "plan": file_record(directory / "plan.json"),
                    "receipt": file_record(directory / "stage.json"), "files": pins,
                    "status": receipt["status"], "stage": lease["id"]}
        self.metrics["pipeline_children"] += len(receipt["steps"])
        self.completed.append(evidence)
        self.pending_stage = None
        if not succeeded:
            raise _StageFailed(directory, evidence)
        return directory, evidence

    def validate_receipt(self, directory, plan, plan_hash, allow_failure=False):
        require(type(plan.get("schema")) is int and plan["schema"] == 2
                and plan["domains"] == self.domains.as_dict(), "STAGE_PLAN_DOMAINS")
        directory = self.domains.require_stage(directory, plan["request_directory"])
        require(str(directory) == plan["stage_directory"], "STAGE_PLAN_DIRECTORY")
        require(plan["domains_source"] == self.files["domains"], "STAGE_PLAN_DOMAINS_PIN")
        check_file(plan["domains_source"], self.domains)
        require(plan["lean"] == self.files["lean"] and plan["python"] == self.python_pin
                and plan["expected_runner_sha256"].lower() == self.files["runner"]["sha256"].lower(), "STAGE_PLAN_TOOL_PINS")
        receipt = strict(read(directory / "stage.json", MIB))
        require(receipt["stage"] == plan["stage"] and receipt["domains"] == plan["domains"]
                and receipt["request_directory"] == plan["request_directory"], "STAGE_DOMAIN_BINDING")
        succeeded = receipt["status"] == "STAGE_COMMANDS_COMPLETED_NOT_MATH_ACCEPTANCE"
        require(succeeded or (allow_failure and receipt["status"] == "STEP_FAILED"), "NATIVE_STAGE_FAILED")
        require(not (directory / "ACTIVE.lock").exists(), "STAGE_QUIESCENCE_UNCONFIRMED")
        require(receipt["accounting_root"] == str(directory) and receipt["retained_bytes_scope"] == "SELECTED_STAGE_ONLY", "STAGE_ACCOUNTING_BINDING")
        require(receipt["expected_plan_sha256"].lower() == plan_hash.lower()
                and sha(read(directory / "plan.json")) == plan_hash.lower()
                and strict(read(directory / "plan.json")) == plan, "STAGE_PLAN_BINDING")
        for field in ("runner", "plan", "lean"):
            check_file(receipt[field], self.domains)
        check_interpreter(receipt["python"])
        require(Path(receipt["runner"]["path"]) == directory / "run_stage.py"
                and Path(receipt["plan"]["path"]) == directory / "plan.json", "STAGE_FILE_PATH")
        require(receipt["runner"]["sha256"].lower() == self.files["runner"]["sha256"].lower(), "STAGE_RUNNER_PIN")
        require(Path(receipt["lean"]["path"]) == Path(self.files["lean"]["path"])
                and receipt["lean"]["sha256"].lower() == self.files["lean"]["sha256"].lower(), "STAGE_LEAN_PIN")
        require(Path(receipt["python"]["path"]).resolve() == Path(self.python_pin["path"])
                and receipt["python"]["bytes"] == self.python_pin["bytes"]
                and receipt["python"]["sha256"].lower() == self.python_pin["sha256"].lower(), "STAGE_PYTHON_PIN")
        final = receipt["final_job"]
        require(final["active_processes"] == 0 and final["terminated_processes"] == 0, "CHILD_NOT_QUIESCENT_OR_LIMIT_TERMINATED")
        require(receipt["execution_endpoint"]["children_quiescent"] is True
                and receipt["execution_endpoint"]["selected_output_census_complete"] is True, "STAGE_ENDPOINT_INCOMPLETE")
        require(receipt["stage_wall_seconds"] <= plan["seconds"] and final["cpu_seconds"] <= plan["seconds"], "STAGE_TIME_BOUND")
        require(final["peak_job_private_commit_bytes"] <= plan["memory_mib"] * MIB
                and receipt["selected_stage_bytes_at_execution_endpoint"] <= plan["bytes"]
                and receipt["limits"]["selected_stage_staging_bytes"] == plan["bytes"], "STAGE_RESOURCE_BOUND")
        require(len(receipt["steps"]) == len(plan["steps"]) if succeeded else 1 <= len(receipt["steps"]) <= len(plan["steps"]), "STAGE_STEP_COUNT")
        require(len(receipt["inputs"]) == len(plan["inputs"]), "STAGE_INPUT_COUNT")
        runtime = self.domains.lean_runtime
        def expand(value):
            return value.replace("$RUN", str(directory)).replace("$RUNTIME", str(runtime))
        for expected, actual in zip(plan["inputs"], receipt["inputs"]):
            check_file({key: actual[key] for key in ("path", "bytes", "sha256")}, self.domains)
            require(actual["bytes"] == expected["bytes"] and actual["sha256"].lower() == expected["sha256"].lower(), "STAGE_INPUT_PIN")
            require(Path(actual["path"]) == directory / "input" / expected["as"]
                    and Path(actual["source"]) == Path(expected["path"]).resolve(), "STAGE_INPUT_PATH")
        for number, (step, actual) in enumerate(zip(plan["steps"], receipt["steps"])):
            executable = receipt["lean"]["path"] if step["kind"] == "lean" else str(Path(sys.executable))
            argv = [executable] + (["-j", "1", "-M", str(plan["memory_mib"])] if step["kind"] == "lean" else []) + [expand(value) for value in step["argv"]]
            require(actual["command"] == argv and Path(actual["cwd"]) == Path(expand(step.get("cwd", "$RUN"))), "STAGE_ACTUAL_COMMAND")
            require(actual["lean_path"] == [expand(value) for value in step.get("lean_path", [])], "STAGE_LEAN_PATH")
            require(actual["index"] == number and actual["status"] == "EXITED", "STAGE_CHILD_STATUS")
            expected_exit = step.get("expected_exit", 0)
            require((actual["exit_code"] != expected_exit) if not succeeded and number == len(receipt["steps"]) - 1
                    else actual["exit_code"] == expected_exit, "STAGE_CHILD_EXIT")
            for field in ("stdout", "stderr"):
                check_file(actual[field], self.domains)
                require(Path(actual[field]["path"]) == directory / ("%02d.%s.log" % (number, field)), "STAGE_LOG_PATH")
        require(type(receipt["outputs"]) is list and len(receipt["outputs"]) <= 4096, "STAGE_OUTPUT_COUNT")
        for pin in receipt["outputs"]:
            check_file(pin, self.domains)
        actual_outputs = []
        for index, path in enumerate((directory / "out").rglob("*"), 1):
            require(index <= 4096 and path.resolve().is_relative_to(directory), "STAGE_OUTPUT_DOMAIN")
            if path.is_file():
                actual_outputs.append(str(path))
        require(sorted(pin["path"] for pin in receipt["outputs"]) == sorted(actual_outputs), "STAGE_OUTPUT_CENSUS")

    def native_step(self, arguments):
        return {"kind": "lean", "label": "selected-native", "lean_path": ["$RUN/input/lib"], "cwd": "$RUN/input/native",
                "argv": ["-R", "$RUN/input/native", "--run", "$RUN/input/native/AgentClient.lean", *arguments], "expected_exit": 0}

    def installed_references(self, plan):
        values = [[0, index] for index in range(len(self.seed[2]))]
        for row in plan["batch"]:
            if row["kind"] != 3:
                require(row["kind"] in (0, 1, 2, 4), "PLAN_KIND")
                values.append([{0: 1, 1: 7, 2: 4, 4: 2}[row["kind"]], row["id"]])
            else:
                for index, pair in enumerate(row["types"]):
                    values.extend([[3, row["id"], [0, index]], [3, row["id"], [2, index]]])
                    values.extend([3, row["id"], [1, index, constructor]] for constructor in range(len(pair[1])))
        return values

    def verify_native(self, directory, number, store, roots, plan, references):
        log = directory / ("%02d.stdout.log" % number)
        actual = self.S.read_record(log, b"ACTUAL_BATCH_JSON ")
        self.S.reexport_actual(store, roots, actual)
        description = self.S.read_record(log, b"AGENT_CLIENT_DESCRIPTION_JSON ")
        require(description["foundation"] == plan["foundation"] and description["replays"] == plan["replays"], "DESCRIPTION_CONTEXT")
        require([row["reference"] for row in description["rows"]] == references, "DESCRIPTION_REFERENCES")
        return description

    def describe(self, purpose, store, roots, plan, references):
        require(type(references) is list and 1 <= len(references) <= 256, "DESCRIPTION_REFERENCE_COUNT")
        available = {encoded(value) for value in self.installed_references(plan)}
        require(len({encoded(value) for value in references}) == len(references)
                and all(encoded(value) in available for value in references), "DESCRIPTION_REFERENCE_BINDING")
        step = self.native_step(["--describe", "$RUN/input/plan.json", "--inventory", "$RUN/input/inventory.json", "--requests", "$RUN/input/refs.json"])
        directory, evidence = self.stage(purpose, {"plan.json": plan, "refs.json": references}, [step])
        return self.verify_native(directory, 0, store, roots, plan, references), evidence

    @public
    def bootstrap(self, packages: list[dict]) -> dict:
        require(type(packages) is list and 1 <= len(packages) <= self.package_limit, "BOOTSTRAP_PACKAGE_COUNT")
        copied = [self.import_package(value) for value in packages]
        store, roots, plan = self.union(copied)
        references = [[0, 0]] + [value for value in self.installed_references(plan) if value[0] != 0]
        description, evidence = self.describe("bootstrap", store, roots, plan, references)
        return {"kind": "context", "packages": copied, "plan": plan, "description": description, "evidence": [evidence]}

    @public
    def offer(self, package: dict) -> dict:
        copied = self.import_package(package)
        store, root = self.package(copied)
        value, formal = self.metadata(store, root)
        return {"package": copied, "descriptor_id": self.S.C.to_projection(value["descriptor_id"]),
                "formal_metadata": formal, "symbols": [key.hex() for key in value["row"].symbol_keys]}

    @public
    def admit(self, context: dict, offers: list[dict]) -> dict:
        self.context(context)
        require(type(offers) is list and 1 <= len(offers) <= 16, "SELECTED_OFFER_COUNT")
        packages, references = list(context["packages"]), []
        for offer in offers:
            store, root = self.package(offer["package"])
            value, formal = self.metadata(store, root)
            require(self.S.C.to_projection(value["descriptor_id"]) == offer["descriptor_id"]
                    and formal == offer["formal_metadata"]
                    and [key.hex() for key in value["row"].symbol_keys] == offer["symbols"], "ACQUIRED_DESCRIPTOR_MISMATCH")
            if offer["package"] not in packages:
                packages.append(offer["package"])
            ref = self.S.C.to_projection(value["native_ref"])
            if ref not in references:
                references.append(ref)
        store, roots, plan = self.union(packages)
        description, evidence = self.describe("admit", store, roots, plan, references)
        return {"kind": "context", "packages": packages, "plan": plan, "description": description, "evidence": [evidence]}

    def source_record(self, directory, source_pin, root):
        actual = self.S.read_record(directory / "00.stdout.log", b"AGENT_CLIENT_SOURCE_JSON ")
        raw = read(check_file(source_pin, self.domains), self.source_limit)
        require(Path(actual["path"]) == directory / "input/source.lean" and actual["bytes"] == len(raw)
                and actual["source"].encode("utf-8") == raw
                and actual["root"] == self.S.C.to_projection(self.S.C.name_path(root)), "SOURCE_CAPTURE_INPUT_BINDING")

    def submission_steps(self, source_root):
        first = self.native_step(["--check-source", "$RUN/input/plan.json", "--inventory", "$RUN/input/inventory.json",
                                  "--source", "$RUN/input/source.lean", "--root", source_root])
        def worker(action, capture, output):
            return {"kind": "python", "label": action, "argv": [*PYTHON_FLAGS, "$RUN/input/checking.py", "_worker", action,
                    "$RUN/input/job.json", capture, output]}
        return [first, worker("capture", "$RUN/00.stdout.log", "$RUN/out/candidate"),
                self.native_step(["--describe", "$RUN/out/candidate/plan.json", "--inventory", "$RUN/input/inventory.json", "--requests", "$RUN/out/candidate/refs.json"]),
                worker("inverse", "$RUN/02.stdout.log", "$RUN/out/inverse"),
                self.native_step(["--describe", "$RUN/out/inverse/plan.json", "--inventory", "$RUN/input/inventory.json", "--requests", "$RUN/out/inverse/refs.json"])]

    @public
    def submit(self, context: dict, source_utf8: bytes, source_root: str) -> dict:
        _old_store, _old_roots, plan = self.context(context)
        require(type(source_utf8) is bytes and len(source_utf8) <= self.source_limit, "OWNER_SOURCE_BYTE_BOUND")
        source_utf8.decode("utf-8", errors="strict")
        require(type(source_root) is str and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*", source_root), "OWNER_SOURCE_ROOT")
        source_path = self.work_dir / "owner-source.lean"
        write_new(source_path, source_utf8, self.domains)
        source_pin = file_record(source_path)
        job = {"domains": self.domains.as_dict(), "domains_sha": self.files["domains"]["sha256"],
               "packages": context["packages"], "root": source_root, "source_sha": source_pin["sha256"],
               "source_codec_sha": self.files["source_codec"]["sha256"], "codec_sha": self.files["codec"]["sha256"]}
        steps = self.submission_steps(source_root)
        try:
            directory, evidence = self.stage("submit", {"plan.json": plan, "source.lean": source_path, "job.json": job}, steps)
        except _StageFailed as error:
            receipt = strict(read(error.directory / "stage.json", MIB))
            if len(receipt["steps"]) != 1:
                raise
            self.source_record(error.directory, source_pin, source_root)
            log = error.directory / "00.stdout.log"
            summary = self.S.read_record(log, b"AGENT_CLIENT_DIAGNOSTICS_JSON ")
            require(summary["hasErrors"] is True, "SOURCE_FAILURE_WITHOUT_DIAGNOSTICS")
            lines = [self.S.strict_json(line[len(b"AGENT_CLIENT_DIAGNOSTIC_JSON "):]) for line in read(log).splitlines()
                     if line.startswith(b"AGENT_CLIENT_DIAGNOSTIC_JSON ")]
            require(lines and len(lines) == summary["emitted"], "SOURCE_DIAGNOSTIC_BINDING")
            selected, size = [], 0
            for line in lines[:64]:
                length = len(encoded(line))
                if size + length > MIB // 2:
                    break
                selected.append(line)
                size += length
            require(selected, "DIAGNOSTIC_ROW_BOUND")
            raise CheckingFailure("SOURCE_REJECTED", selected, error.evidence,
                                  summary["truncated"] or len(selected) < len(lines)) from error
        self.source_record(directory, source_pin, source_root)
        inherited, inherited_roots, _ = self.union(context["packages"])
        self.S.reexport_actual(inherited, inherited_roots, self.S.read_record(directory / "00.stdout.log", b"ACTUAL_BATCH_JSON "))
        candidate, inverse = directory / "out/candidate/package", directory / "out/inverse/package"
        s1, r1 = self.read_package(candidate)
        p1 = self.S.make_plan(s1, [r1])
        refs = strict(read(directory / "out/candidate/refs.json"))
        self.verify_native(directory, 2, s1, [r1], p1, refs)
        s2, r2 = self.read_package(inverse)
        p2 = self.S.make_plan(s2, [r2])
        require(r1 == r2 and p1 == p2, "SUCCESSOR_INVERSE_BINDING")
        description = self.verify_native(directory, 4, s2, [r2], p2, refs)
        package = self.import_package({"path": str(inverse), "manifest_sha256": sha(read(inverse / "manifest.json"))})
        return {"kind": "artifact", "package": package, "root": self.S.C.to_projection(r2),
                "source_sha256": source_pin["sha256"], "source_root": source_root, "source": source_pin,
                "description": description, "evidence": [evidence], "actual": str(directory / "04.stdout.log")}

    @public
    def publication(self, artifact: dict) -> dict:
        require(artifact.get("kind") == "artifact", "ARTIFACT_KIND")
        require(type(artifact["evidence"]) is list and len(artifact["evidence"]) == 1, "ARTIFACT_SINGLE_SUBMISSION_STAGE")
        self.evidence(artifact["evidence"])
        check_file(artifact["source"], self.domains)
        require(artifact["source_sha256"].lower() == artifact["source"]["sha256"].lower(), "ARTIFACT_SOURCE_BINDING")
        evidence = artifact["evidence"][0]
        directory = Path(evidence["directory"]).resolve(strict=True)
        require(Path(artifact["actual"]) == directory / "04.stdout.log"
                and any(pin["path"] == artifact["actual"] for pin in evidence["files"]), "ARTIFACT_ACTUAL_BINDING")
        execution_plan = strict(read(evidence["plan"]["path"]))
        require(execution_plan["steps"] == self.submission_steps(artifact["source_root"]), "ARTIFACT_COMPLETE_SUBMISSION_PLAN")
        self.source_record(directory, artifact["source"], artifact["source_root"])
        store, root = self.package(artifact["package"])
        require(self.S.C.to_projection(root) == artifact["root"], "ARTIFACT_ROOT_BINDING")
        value, formal = self.metadata(store, root)
        plan = self.S.make_plan(store, [root])
        description = self.verify_native(directory, 4, store, [root], plan,
                                         [self.S.C.to_projection(value["native_ref"])])
        require(description == artifact["description"], "ARTIFACT_FINAL_DESCRIPTION_BINDING")
        return {"package": artifact["package"], "descriptor_id": self.S.C.to_projection(value["descriptor_id"]),
                "formal_metadata": formal, "symbols": [key.hex() for key in value["row"].symbol_keys]}


def internal_worker(action, job_path, log_path, output_path):
    require_python_profile()
    job_path = Path(job_path).resolve(strict=True)
    base = job_path.parent
    job = strict(read(job_path, MIB))
    domains = Domains.from_record(job["domains"])
    require(job["domains"] == domains.as_dict(), "WORKER_DOMAINS_BINDING")
    plan_path = domains.require_read(base.parent / "plan.json")
    plan_raw = read(plan_path)
    plan = strict(plan_raw)
    require(type(plan.get("schema")) is int and plan["schema"] == 2
            and plan["domains"] == domains.as_dict(), "WORKER_PLAN_DOMAINS")
    stage = domains.require_stage(base.parent, plan["request_directory"])
    require(str(stage) == plan["stage_directory"] and base == stage / "input"
            and job_path == base / "job.json" and Path(__file__).resolve() == base / "checking.py"
            and Path(domain_module.__file__).resolve() == base / "domains.py", "WORKER_STAGE_INPUT_BINDING")
    receipt = strict(read(stage / "stage.json", MIB))
    require(receipt["stage"] == plan["stage"] and receipt["domains"] == plan["domains"]
            and receipt["request_directory"] == plan["request_directory"]
            and receipt["expected_plan_sha256"].lower() == sha(plan_raw), "WORKER_AUTHENTICATED_PLAN")
    require(type(plan["inputs"]) is list and 1 <= len(plan["inputs"]) <= 64, "WORKER_INPUT_COUNT")
    for name in ("checking.py", "domains.py", "job.json", "source_codec.py", "codec.py", "seed.json"):
        entries = [entry for entry in plan["inputs"] if entry["as"] == name]
        require(len(entries) == 1, "WORKER_SNAPSHOT_INPUT_BINDING")
        check_file({"path": str(base / name), "bytes": entries[0]["bytes"],
                    "sha256": entries[0]["sha256"]}, domains)
    require(sha(read(base / "domains.py")) == job["domains_sha"].lower()
            == plan["domains_source"]["sha256"].lower(), "WORKER_DOMAINS_PIN")
    source = module("integration_worker_source", {"path": str(base / "source_codec.py"),
                    "bytes": (base / "source_codec.py").stat().st_size, "sha256": job["source_codec_sha"]}, domains)
    require(sha(read(base / "codec.py")) == job["codec_sha"].lower(), "WORKER_CODEC_PIN")
    source.configure_codec(base / "codec.py")
    seed = source.C.from_projection(source.strict_json(read(base / "seed.json")))
    require(action in ("capture", "inverse"), "WORKER_ACTION")
    output = domains.require_write(output_path)
    expected_output = "candidate" if action == "capture" else "inverse"
    expected_log = "00.stdout.log" if action == "capture" else "02.stdout.log"
    require(output == stage / "out" / expected_output
            and domains.require_read(log_path) == stage / expected_log, "WORKER_OUTPUT_LOG_BINDING")
    output.mkdir(parents=True, exist_ok=False)
    if action == "capture":
        require(sha(read(base / "source.lean")) == job["source_sha"].lower(), "WORKER_SOURCE_PIN")
        require(type(job["packages"]) is list and 1 <= len(job["packages"]) <= 16, "WORKER_PACKAGE_COUNT")
        for package in job["packages"]:
            path = domains.require_package(package["path"])
            require(sha(read(path / "manifest.json")) == package["manifest_sha256"].lower(), "WORKER_INHERITED_MANIFEST_PIN")
        inherited, roots = source.merge_packages(seed, [package["path"] for package in job["packages"]])
        capture = source.read_record(log_path, b"SOURCE_CAPTURE_JSON ")
        require(capture["roots"] == source.C.to_projection([source.C.name_path(job["root"])]), "WORKER_CAPTURE_ROOT")
        compiler = source.SourceCompiler(seed, capture, inherited, roots)
        compiler.all()
        root = compiler.replay(source.C.name_path(job["root"]))
        store = compiler.store
    elif action == "inverse":
        store, root = source.read_package(base.parent / "out/candidate/package", seed)
        store = source.reexport_actual(store, [root], source.read_record(log_path, b"ACTUAL_BATCH_JSON "))
    else:
        raise CheckingFailure("WORKER_ACTION")
    source.export_package(store, root, output / "package")
    plan = source.make_plan(store, [root])
    source.write_json(output / "plan.json", plan)
    typed_root = store.get(root, 0x15, 3)[1]
    require(typed_root[0] in (1, 4), "WORKER_ROOT_KIND")
    ref = [7, typed_root[1]] if typed_root[0] == 4 else [1, typed_root[1]]
    source.write_json(output / "refs.json", source.C.to_projection([ref]))


if __name__ == "__main__":
    try:
        require(len(sys.argv) == 6 and sys.argv[1] == "_worker", "INTERNAL_WORKER_ARGUMENTS")
        internal_worker(*sys.argv[2:])
    except BaseException as error:
        sys.stderr.write((type(error).__name__ + ": " + str(error))[:2048] + "\n")
        raise SystemExit(1)
