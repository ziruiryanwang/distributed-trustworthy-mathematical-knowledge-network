"""Owner-approved Lean source -> inert portable export -> ordinary admission.

Caller-chosen new definitions/theorems, not a research task or fixture protocol.
Selected acquired mathematics must already be warranted in the protected local
context. The owner supplies immutable, exact-pinned authoring support; neither
paths nor a successful source compiler grant mathematical authority. Source is
executable owner code. Windows Job resource limits are NOT a security sandbox.

The installed admission core alone accepts new complete units. This helper
neither initializes/copies the owner nor publishes to an index or network. Its
fresh evidence/preview files can subsequently be served through existing APIs.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import time

import ordinary_admission as A
import portable_owner_request as R
import portable_candidate as B
import portable_preview as PP

E, P, S, PE, need = A.E, A.P, A.S, A.PE, A.need
MIB = 1024**2
MAX_TARGETS = 32
MAX_TARGET_BYTES = 65536
PROJECT_SCHEMA = "DMKN_ORDINARY_TRUSTED_PROJECT_AUTHORING_V1"


def _project_module(value, *, allow_bridge_import=False):
    need(type(allow_bridge_import) is bool and type(value) is str and 0 < len(value) <= 256,
         "CONTRIBUTION_PROJECT_MODULE_NAME")
    parts = value.split(".")
    # Only an imported top-level bridge may exceed the ordinary component bound.
    # This filename grammar grants no authority to the module's contents.
    bridge = allow_bridge_import and re.fullmatch(r"DMKNBridge_[0-9a-f]{64}", value) is not None
    need(1 <= len(parts) <= 16 and all(0 < len(part) and (len(part) <= 64 or bridge) and
         re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", part) and
         not os.path.isreserved(part) for part in parts),
         "CONTRIBUTION_PROJECT_MODULE_NAME")
    return value


def _project_path(value, code):
    need(type(value) is str and 0 < len(value) <= 32768 and
         not any(ord(char) < 32 for char in value) and os.pathsep not in value,
         code)
    path = Path(value)
    need(path.is_absolute() and ".." not in path.parts and len(path.parts) <= 128,
         code)
    return path


@dataclass(frozen=True)
class TrustedProjectAuthoring:
    """Closed owner-approved authoring selection, never a receiver warrant.

    Only newly authored modules are supported. Imported project code/plugins
    are trusted local executable support, not sandboxed or completely hashed.
    The generated source root is fresh output storage, NOT project_cwd.
    """
    module_name: str
    project_cwd: Path
    project_search_paths: tuple[Path, ...]
    imports: tuple[tuple[str, bool], ...]

    @classmethod
    def from_document(cls, document):
        need(cls is TrustedProjectAuthoring and type(document) is dict and
             set(document) == {"schema", "module_name", "project_cwd",
                               "project_search_paths", "imports"},
             "CONTRIBUTION_PROJECT_FIELDS")
        need(document["schema"] == PROJECT_SCHEMA, "CONTRIBUTION_PROJECT_SCHEMA")
        module = _project_module(document["module_name"])
        cwd = _project_path(document["project_cwd"], "CONTRIBUTION_PROJECT_CWD")
        paths = document["project_search_paths"]
        need(type(paths) is list and 1 <= len(paths) <= 16,
             "CONTRIBUTION_PROJECT_SEARCH_PATHS")
        paths = tuple(_project_path(path, "CONTRIBUTION_PROJECT_SEARCH_PATHS") for path in paths)
        need(len(set(paths)) == len(paths), "CONTRIBUTION_PROJECT_SEARCH_PATHS")
        records = document["imports"]
        need(type(records) is list and 1 <= len(records) <= 64,
             "CONTRIBUTION_PROJECT_IMPORTS")
        imports, seen = [], set()
        for row in records:
            need(type(row) is dict and set(row) == {"module", "meta"},
                 "CONTRIBUTION_PROJECT_IMPORT_FIELDS")
            name = _project_module(row["module"], allow_bridge_import=True)
            need(type(row["meta"]) is bool, "CONTRIBUTION_PROJECT_META")
            need(name not in seen, "CONTRIBUTION_PROJECT_DUPLICATE_IMPORT")
            seen.add(name)
            imports.append((name, row["meta"]))
        return cls(module, cwd, paths, tuple(imports))

    def to_document(self):
        need(type(self) is TrustedProjectAuthoring and isinstance(self.project_cwd, Path) and
             type(self.project_search_paths) is tuple and
             1 <= len(self.project_search_paths) <= 16 and
             all(isinstance(path, Path) for path in self.project_search_paths) and
             type(self.imports) is tuple and 1 <= len(self.imports) <= 64 and
             all(type(row) is tuple and len(row) == 2 for row in self.imports),
             "CONTRIBUTION_PROJECT_DATA")
        document = {"schema": PROJECT_SCHEMA, "module_name": self.module_name,
            "project_cwd": str(self.project_cwd),
            "project_search_paths": [str(path) for path in self.project_search_paths],
            "imports": [{"module": name, "meta": meta} for name, meta in self.imports]}
        # Revalidate direct dataclass construction too; no callbacks or plugins.
        need(type(self).from_document(document) == self, "CONTRIBUTION_PROJECT_DATA")
        return document

    def verify(self, check_budget):
        need(callable(check_budget), "CONTRIBUTION_PROJECT_BUDGET")
        check_budget()
        document = self.to_document()
        for path in (self.project_cwd, *self.project_search_paths):
            check_budget()
            A.C.ordinary(path, directory=True)
        check_budget()
        return document

    def import_bytes(self):
        self.to_document()
        return b"".join(("public " + ("meta " if meta else "") + "import " + name + "\n").encode("ascii")
                        for name, meta in self.imports)

    def module_path(self):
        self.to_document()
        return Path(*self.module_name.split(".")).with_suffix(".lean")


class ContributionError(RuntimeError):
    """Failure with retained acceptance information even if logging fails."""

    def __init__(self, phase, error, accepted=None, native_cpu_seconds=0.0):
        self.report = {"phase": phase, "error_type": type(error).__name__,
            "error": str(error),
            "accepted": json.loads(json.dumps(accepted, allow_nan=False)),
            "native_cpu_seconds": native_cpu_seconds,
            "retention": "CALLER_OWNS_LIFECYCLE_ACCEPTED_STATE_AND_PARTIAL_OUTPUTS_PRESERVED"}
        super().__init__(f"CONTRIBUTION_{phase}: {error}")


def _outputs(output_names):
    need(type(output_names) is list and 1 <= len(output_names) <= MAX_TARGETS,
         "CONTRIBUTION_OUTPUT_COUNT")
    names, keys = [], set()
    for name in output_names:
        key = E.name_key(name)
        need(key not in keys, "CONTRIBUTION_DUPLICATE_OUTPUT")
        keys.add(key)
        names.append(E.strict_json(key))
    need(len(E.canonical_json(names)) <= MAX_TARGET_BYTES, "CONTRIBUTION_OUTPUT_BYTES")
    return names


def _acquired(semantic_id, acquired_targets):
    A.C.hexid(semantic_id)
    need(semantic_id == S.semantic_id(), "CONTRIBUTION_SEMANTICS")
    need(type(acquired_targets) is list and len(acquired_targets) <= MAX_TARGETS,
         "CONTRIBUTION_ACQUIRED_COUNT")
    targets, keys = [], set()
    for row in acquired_targets:
        P.fields(row, ("name", "export_id", "unit_id"), "CONTRIBUTION_ACQUIRED_FIELDS")
        key = E.name_key(row["name"])
        need(key not in keys, "CONTRIBUTION_DUPLICATE_ACQUIRED")
        keys.add(key)
        identity, unit = A.C.hexid(row["export_id"]), A.C.hexid(row["unit_id"])
        name = E.strict_json(key)
        need(S.export_id(semantic_id, unit, name) == identity, "CONTRIBUTION_ACQUIRED_EXPORT_BINDING")
        targets.append({"name": name, "export_id": identity, "unit_id": unit})
    need(len(E.canonical_json(targets)) <= MAX_TARGET_BYTES, "CONTRIBUTION_ACQUIRED_BYTES")
    return targets


def _source(source_body):
    need(type(source_body) is bytes and 0 < len(source_body) <= MIB,
         "CONTRIBUTION_SOURCE_BYTES")
    need(b"\0" not in source_body, "CONTRIBUTION_SOURCE_NUL")
    source_body.decode("utf-8", errors="strict")
    return source_body


def validate_inputs(semantic_id, acquired_targets, source_body, output_names):
    """Pure bounded validation/detachment; not a warrant or source sandbox."""
    targets, names = _acquired(semantic_id, acquired_targets), _outputs(output_names)
    need(not ({E.name_key(row["name"]) for row in targets} &
              {E.name_key(name) for name in names}), "CONTRIBUTION_OUTPUT_IS_ACQUIRED")
    return {"acquired_targets": targets, "source_body": _source(source_body), "output_names": names}


def request_targets(semantic_id, acquired_targets, warranted_symbol):
    """Use exact acquired targets, or genuine protected Eq for basis-only work."""
    need(callable(warranted_symbol), "CONTRIBUTION_WARRANT_CALLBACK")
    selected = _acquired(semantic_id, acquired_targets)
    targets = [[row["name"], row["export_id"]] for row in selected]
    if not targets:
        name = [[0, {"$bytes": [69, 113]}]]  # Eq in the fixed admitted basis.
        targets = [[name, S.basis_symbol_id(semantic_id, S.foundation_id(), name)]]
    for name, identity in targets:
        need(warranted_symbol(name) == identity, "CONTRIBUTION_TARGET_NOT_WARRANTED")
    return targets


def assemble_source(*, source_body, request_directory, semantic_id, context_root,
                    foundation_id, targets_file, candidate_file, authoring_backend=None):
    """Fixed wrapper with exact caller bytes; names travel in bounded JSON.

    This first path wrapper retains the predecessor's explicit ASCII path
    restriction. Lean declaration names themselves may contain UTF-8.
    """
    _source(source_body)
    for value in (semantic_id, context_root, foundation_id):
        A.C.hexid(value)

    def quote(value):
        value = str(value)
        need(value.isascii() and len(value) <= 32768 and
             all(ord(c) >= 32 for c in value), "CONTRIBUTION_LEAN_STRING")
        return json.dumps(value).encode("ascii")

    need(authoring_backend is None or type(authoring_backend) is TrustedProjectAuthoring,
         "CONTRIBUTION_AUTHORING_BACKEND")
    project_imports = b"" if authoring_backend is None else authoring_backend.import_bytes()
    header = (b"module\n\npublic import Init\npublic meta import PortableOwnerConstructCommand\n"
              b"public meta import PortableContributionExportCommand\n" + project_imports + b"\npublic section\n\n"
              b"#ordinary_construct_portable " + b" ".join(quote(value) for value in
              (request_directory, semantic_id, context_root, foundation_id)) + b"\n\n")
    footer = b"\n\n#ordinary_export_contribution " + quote(targets_file) + b" " + quote(candidate_file) + b"\n"
    return header + source_body + footer


def publication_targets(semantic_id, raw_units, output_names):
    """Pure exact target-to-unit mapping. This does NOT establish acceptance."""
    A.C.hexid(semantic_id)
    need(semantic_id == S.semantic_id(), "CONTRIBUTION_SEMANTICS")
    names = _outputs(output_names)
    need(type(raw_units) in (tuple, list) and 1 <= len(raw_units) <= 32,
         "CONTRIBUTION_PUBLICATION_UNIT_COUNT")
    outputs, units, total = {}, set(), 0
    for raw in raw_units:
        need(type(raw) is bytes, "CONTRIBUTION_PUBLICATION_BYTES")
        total += len(raw)
        need(total <= 4*MIB, "CONTRIBUTION_PUBLICATION_BYTE_BOUND")
        item = PE.read_evidence(raw)
        need(item.document["semantic_id"] == semantic_id and item.unit_id not in units,
             "CONTRIBUTION_PUBLICATION_UNIT")
        units.add(item.unit_id)
        for row in item.document["unit"][2]:
            key = E.name_key(row[0])
            need(key not in outputs, "CONTRIBUTION_PUBLICATION_DUPLICATE_NAME")
            outputs[key] = item.unit_id
    result = []
    for name in names:
        unit = outputs.get(E.name_key(name))
        need(unit is not None, "CONTRIBUTION_EXACT_OUTPUT_TARGET")
        result.append({"name": name, "unit_id": unit,
                       "export_id": S.export_id(semantic_id, unit, name)})
    return result


@dataclass(frozen=True)
class AuthoringProfile:
    """Exact immutable owner support, separately adopted from installed core.

    Every helper-directory file is inventoried, not just its first .olean.
    Runtime/system support remains under the installation's existing premise.
    The before/after checks detect ordinary changes; they are not protection
    against a hostile local actor racing immutable owner storage or Python state.
    """
    installation_manifest_sha256: str
    helper_paths: tuple[Path, ...]
    author_worker_script: Path
    file_pins: tuple[tuple[Path, int, str], ...]

    def verify(self, check_budget):
        need(callable(check_budget), "CONTRIBUTION_PROFILE_BUDGET")
        check_budget()
        A.C.hexid(self.installation_manifest_sha256)
        need(type(self.helper_paths) is tuple and 1 <= len(self.helper_paths) <= 8,
             "CONTRIBUTION_HELPER_PATHS")
        helpers = tuple(A.C.ordinary(path, directory=True) for path in self.helper_paths)
        need(len(set(helpers)) == len(helpers), "CONTRIBUTION_HELPER_PATHS")
        worker = A.C.ordinary(self.author_worker_script)
        need(type(self.file_pins) is tuple and 1 <= len(self.file_pins) <= 4096,
             "CONTRIBUTION_PROFILE_PIN_COUNT")
        pins, total = {}, 0
        for pin in self.file_pins:
            check_budget()
            need(type(pin) is tuple and len(pin) == 3, "CONTRIBUTION_PROFILE_PIN")
            path, size, digest = pin
            path = A.C.ordinary(path)
            need(path not in pins and type(size) is int and 0 <= size <= 128*MIB,
                 "CONTRIBUTION_PROFILE_PIN")
            A.C.hexid(digest)
            total += size
            need(total <= 512*MIB, "CONTRIBUTION_PROFILE_TOTAL_BYTES")
            pins[path] = (size, digest)
        # These are the actual imported source modules, not similarly named
        # files in an arbitrary directory. Installed core dependencies are
        # checked by NativeInstallation; require the helper imports to share it.
        required = [Path(__file__).absolute(), worker]
        required.extend(Path(module.__file__).absolute() for module in (R, B, PP, R.V1, PP.P))
        need(all(path in pins for path in required), "CONTRIBUTION_PROFILE_LOADED_SUPPORT")
        need(R.E is E and R.S is S and R.PE is PE and R.V1.E is E and
             B.E is E and B.S is S and B.PE is PE and PP.E is E and PP.PE is PE and PP.P.E is E,
             "CONTRIBUTION_PROFILE_CORE_BINDING")
        pending, entries = [(path, 0) for path in helpers], 0
        while pending:
            directory, depth = pending.pop()
            check_budget()
            with os.scandir(directory) as listing:
                for entry in listing:
                    check_budget()
                    entries += 1
                    need(entries <= 4096, "CONTRIBUTION_HELPER_CENSUS_BOUND")
                    path = Path(entry.path)
                    if entry.is_dir(follow_symlinks=False):
                        need(depth < 8, "CONTRIBUTION_HELPER_DEPTH_BOUND")
                        pending.append((A.C.ordinary(path, directory=True), depth+1))
                    else:
                        path = A.C.ordinary(path)
                        need(path in pins, "CONTRIBUTION_HELPER_UNPINNED_FILE")
        for path, (size, expected) in pins.items():
            check_budget()
            need(path.stat().st_size == size, "CONTRIBUTION_PROFILE_SIZE")
            count, digest = 0, hashlib.sha256()
            with path.open("rb") as stream:
                while block := stream.read(MIB):
                    check_budget()
                    count += len(block)
                    need(count <= size, "CONTRIBUTION_PROFILE_GREW")
                    digest.update(block)
            need(count == size and path.stat().st_size == size and digest.hexdigest() == expected,
                 "CONTRIBUTION_PROFILE_CHANGED")
        check_budget()
        return {"files": len(pins), "bytes": total, "helper_entries": entries}


def contribute_source(owner, parent_root, acquired_targets, source_body, output_names, *,
                      output_directory, profile, parent_deadline, make_budget,
                      account_worker_cpu, check_parent, authoring_backend=None):
    """Author/check several new targets in one already-open protected owner.

    No acquired target is required to occur in a result: utility and the choice
    of research are local decisions. `make_budget` derives each fresh one-use
    operation from the remaining ORIGINAL parent allowance; `check_parent` and
    `account_worker_cpu` are trusted owner callbacks sharing that allocation.
    Caller owns custody/lifecycle. Failure never rolls back accepted mathematics.
    Optional project data changes only source assembly and owner-approved worker
    invocation. Binding, preflight, admission and retention remain one flow.
    """
    need(type(owner) is A.OrdinaryAdmission and type(profile) is AuthoringProfile and
         type(parent_deadline) in (int, float) and math.isfinite(parent_deadline) and
         callable(make_budget) and callable(account_worker_cpu) and callable(check_parent),
         "CONTRIBUTION_OWNER_CONFIGURATION")
    A.C.hexid(parent_root)
    installation, custody = owner.installation, owner.evidence_store
    need(profile.installation_manifest_sha256 == installation.manifest_sha256,
         "CONTRIBUTION_PROFILE_INSTALLATION")
    started, current, output = time.monotonic(), None, None
    phase, accepted, native_cpu = "INPUTS", None, 0.0
    diagnostics = {}

    def check():
        check_parent()
        need(time.monotonic() < parent_deadline, "CONTRIBUTION_PARENT_DEADLINE")
        if current is not None:
            current.check()

    def operation():
        check_parent()
        value = make_budget()
        need(type(value) is A.OperationBudget and not value.claimed and value.worker_cpu == 0 and
             value.deadline <= parent_deadline, "CONTRIBUTION_REMAINING_OPERATION_BUDGET")
        value.check()
        return value

    def save(name, value):
        raw = value if type(value) is bytes else json.dumps(
            value, sort_keys=True, ensure_ascii=True, allow_nan=False, indent=2).encode("ascii")
        P.PortableCatalog._write_fresh(output/name, raw)
        return {"bytes": len(raw), "sha256": A.sha(raw)}

    try:
        current = operation()
        check()
        inputs = validate_inputs(installation.semantic_id, acquired_targets, source_body, output_names)
        acquired, names, body = inputs["acquired_targets"], inputs["output_names"], inputs["source_body"]
        profile_info = profile.verify(check)
        need(authoring_backend is None or type(authoring_backend) is TrustedProjectAuthoring,
             "CONTRIBUTION_AUTHORING_BACKEND")
        project_info = None if authoring_backend is None else authoring_backend.verify(check)
        output = A.C.ordinary(Path(output_directory), directory=True, fresh=True)
        output.mkdir()
        phase = "REQUEST"
        context = owner.catalog.context(parent_root)

        def warranted(name):
            check()
            return context["bindings"].get(E.name_key(name))

        for name in names:
            need(warranted(name) is None, "CONTRIBUTION_OUTPUT_ALREADY_WARRANTED")
        targets = request_targets(installation.semantic_id, acquired, warranted)
        selected_units = {row["export_id"]: row["unit_id"] for row in acquired}
        request_dir, source_dir, build_dir = (output/part for part in ("owner-request", "owner-source", "lean-build"))
        for path in (request_dir, source_dir, build_dir):
            A.C.ordinary(path, directory=True, fresh=True).mkdir()
        fetched = []

        def evidence(name, identity):
            check()
            need(warranted(name) == identity, "CONTRIBUTION_EVIDENCE_NOT_WARRANTED")
            locator = PP.read_locator(E.strict_json(custody.get_locator(
                installation.semantic_id, identity, 4096, check_budget=check)))
            need(locator["semantic_id"] == installation.semantic_id and
                 E.name_key(locator["export_name"]) == E.name_key(name) and
                 S.export_id(installation.semantic_id, locator["unit_id"], name) == identity,
                 "CONTRIBUTION_EXACT_LOCAL_LOCATOR")
            need(identity not in selected_units or selected_units[identity] == locator["unit_id"],
                 "CONTRIBUTION_ACQUIRED_UNIT_CHANGED")
            raw = custody.get_evidence(installation.semantic_id, locator["unit_id"], MIB, check_budget=check)
            item = PE.read_evidence(raw)
            need(item.unit_id == locator["unit_id"] and item.document["semantic_id"] == installation.semantic_id and
                 any(E.name_key(row[0]) == E.name_key(name) for row in item.document["unit"][2]),
                 "CONTRIBUTION_EXACT_LOCAL_EVIDENCE")
            fetched.append({"name": E.strict_json(E.name_key(name)), "export_id": identity,
                            "unit_id": item.unit_id, "bytes": len(raw), "sha256": A.sha(raw)})
            check()
            return raw

        prepared = R.prepare(semantic_id=installation.semantic_id, foundation_id=S.foundation_id(),
            context_root=parent_root, inventory_raw=installation.read("inventory", MIB), targets=targets,
            warranted_symbol=warranted, fetch_evidence=evidence, owner_absent=lambda name: True,
            limits=R.Limits(max_groups=32, max_rows=4096, max_targets=MAX_TARGETS,
                max_group_bytes=MIB, max_payload_bytes=4*MIB, max_acquired_bytes=4*MIB,
                max_acquired_nodes=131072, max_edges=32768))
        header = E.strict_json(prepared.header, E.Limits(max_bytes=MIB))
        bindings = {E.name_key(row[1][0]): row[0] for row in header["basis_rows"]}
        request_pins = {"header.json": save("owner-request/header.json", prepared.header)}
        for index, raw in enumerate(prepared.groups):
            check()
            packet = E.strict_json(raw, E.Limits(max_bytes=MIB))
            for name, mode, identity, payload in packet[1]:
                key = E.name_key(name)
                need(key not in bindings and warranted(name) == identity, "CONTRIBUTION_PREPARED_BINDING")
                bindings[key] = identity
            filename = f"group-{index:05d}.json"
            request_pins[filename] = save("owner-request/"+filename, raw)
        need(all(bindings.get(E.name_key(name)) == identity for name, identity in targets),
             "CONTRIBUTION_PREPARED_TARGET")
        targets_file, candidate = output/"targets.json", output/"candidate.json"
        target_bytes = E.canonical_json(names)
        target_pin = save("targets.json", target_bytes)
        generated = assemble_source(source_body=body, request_directory=request_dir,
            semantic_id=installation.semantic_id, context_root=parent_root,
            foundation_id=S.foundation_id(), targets_file=targets_file, candidate_file=candidate,
            authoring_backend=authoring_backend)
        # Only this fresh generated tree is written, never the approved project.
        source_relative = (Path("OrdinaryProducer.lean") if authoring_backend is None
                           else authoring_backend.module_path())
        source = source_dir/source_relative
        need(source.is_relative_to(source_dir), "CONTRIBUTION_PROJECT_SOURCE_ROOT")
        source.parent.mkdir(parents=True, exist_ok=True)
        source_pin = save("owner-source/"+source_relative.as_posix(), generated)
        request_info = {"parent_root": parent_root, "acquired_targets": acquired,
            "output_names": names, "output_targets": target_pin, "request_files": request_pins,
            "groups": len(prepared.groups), "fetched": fetched,
            "payload_bytes": prepared.payload_bytes, "acquired_bytes": prepared.acquired_bytes,
            "source_body_sha256": A.sha(body), "generated_source": source_pin,
            "authoring_profile": profile_info, "mathematical_acceptance": False}
        if project_info is not None:
            request_info["project_authoring"] = {"configuration": project_info,
                "generated_module_root": str(source_dir), "generated_source": str(source),
                "search_path_order": "PINNED_HELPERS_THEN_PINNED_RUNTIME_THEN_APPROVED_PROJECT"}
        save("REQUEST.json", request_info)
        phase = "AUTHORING"
        check(); current.claim()
        argv = [str(installation.path("python")), "-I", "-S", "-B", str(profile.author_worker_script),
                "--author-worker", str(installation.path("lean")), str(source), str(build_dir),
                os.pathsep.join(map(str, profile.helper_paths)), str(candidate)]
        if authoring_backend is not None:
            authoring_backend.verify(check)
            argv[5] = "--project-author-worker"
            argv.extend((str(source_dir), str(authoring_backend.project_cwd),
                         os.pathsep.join(map(str, authoring_backend.project_search_paths))))
            need(sum(len(argument)+3 for argument in argv) <= 30000,
                 "CONTRIBUTION_PROJECT_ARGV_BOUND")
        supervision = installation._supervisor.supervise(argv, output, output/"authoring-supervision",
            installation._supervisor.limits_checked(current.allowance(parent_deadline)), installation._job_module.Job)
        final_job = supervision.get("final_job")
        if type(final_job) is dict and type(final_job.get("cpu_seconds")) in (int, float):
            charged = final_job["cpu_seconds"]
            need(math.isfinite(charged) and charged >= 0, "CONTRIBUTION_AUTHORING_CPU")
            current.worker_cpu += charged
            native_cpu += charged
            account_worker_cpu(charged)
        save("AUTHORING-SUPERVISION.json", supervision)
        need(A._clean_worker(supervision), "CONTRIBUTION_AUTHORING_NOT_CLEAN")
        need(type(final_job.get("cpu_seconds")) in (int, float), "CONTRIBUTION_AUTHORING_CPU")
        need(A.C.ordinary(output/"authoring-supervision/stderr.txt").stat().st_size == 0,
             "CONTRIBUTION_AUTHORING_STDERR")
        check()
        profile.verify(check)
        need(A.C.read_bounded(source, 2*MIB) == generated, "CONTRIBUTION_SOURCE_CHANGED")
        need(A.C.read_bounded(targets_file, MAX_TARGET_BYTES) == target_bytes,
             "CONTRIBUTION_TARGETS_CHANGED")
        for filename, pin in request_pins.items():
            check()
            raw = A.C.read_bounded(request_dir/filename, MIB)
            need({"bytes": len(raw), "sha256": A.sha(raw)} == pin, "CONTRIBUTION_REQUEST_CHANGED")
        current = operation()  # Same parent ledger, already charged authoring CPU.
        phase = "BINDING"
        bound = B.bind_candidate(A.C.read_bounded(A.C.ordinary(candidate), 4*MIB),
            semantic_id=installation.semantic_id, foundation_id=S.foundation_id(), context_root=parent_root,
            expected_targets=names, prepared_bindings=bindings, warranted_symbol=warranted,
            check_budget=check, limits=B.Limits(max_bundle_bytes=4*MIB, max_units=32,
                max_bindings=4096, max_targets=MAX_TARGETS, max_total_nodes=131072, max_evidence_bytes=4*MIB))
        if bound.status != "READY":
            diagnostics["needs_local_interpretations"] = [E.strict_json(name) for name in bound.missing_names]
            need(False, "CONTRIBUTION_CANDIDATE_NEEDS_INTERPRETATIONS")
        published = publication_targets(installation.semantic_id, bound.raw_units, names)
        items = [PE.read_evidence(raw) for raw in bound.raw_units]
        plans = owner.preflight(parent_root, bound.raw_units, budget=current,
            limits=A.PreflightLimits(max_units=32, max_bytes=4*MIB, max_nodes=131072,
                                     max_names=4096, max_edges=32768))
        if plans.status != "READY":
            diagnostics["missing_dependencies"] = [
                {"name": E.strict_json(name), "export_id": identity} for name, identity in plans.missing]
            need(False, "CONTRIBUTION_PREFLIGHT_NEEDS")
        phase = "ADMISSION"
        try:
            accepted = owner.admit(parent_root, plans, current)
        finally:
            native_cpu += current.worker_cpu
            account_worker_cpu(current.worker_cpu)
        save("ADMISSION.json", accepted)
        need(accepted["status"] == "CHECKED" and accepted["units_checked"] == len(items),
             "CONTRIBUTION_NEW_CHECK_REQUIRED")
        phase = "PUBLICATION_BYTES"
        by_unit = {item.unit_id: item for item in items}
        preview_dir = A.C.ordinary(output/"previews", directory=True, fresh=True)
        unit_dir = A.C.ordinary(output/"evidence", directory=True, fresh=True)
        preview_dir.mkdir(); unit_dir.mkdir()
        previews = []
        for target in published:
            check()
            item = by_unit[target["unit_id"]]
            preview = PP.preview_from_evidence(item.raw, target["name"])
            PP.resolve(preview, item.raw)
            custody.put_preview(preview, before_commit=check)
            filename = "previews/"+target["export_id"]+".json"
            pin = save(filename, preview)
            need(custody.get_preview(pin["sha256"], pin["bytes"], check_budget=check) == preview,
                 "CONTRIBUTION_PREVIEW_CUSTODY_READBACK")
            previews.append({**target, "file": str(output/filename), **pin})
        units = []
        for item in items:
            check()
            filename = "evidence/"+item.unit_id+".json"
            units.append({"unit_id": item.unit_id, "file": str(output/filename), **save(filename, item.raw)})
        result = {"status": "CHECKED_CONTRIBUTION_WITH_DURABLE_PUBLICATION_BYTES",
            "parent_root": parent_root, "local_root": accepted["local_root"],
            "semantic_id": installation.semantic_id, "implementation_id": installation.implementation_id,
            "targets": published, "acquired_targets": acquired, "units": units, "previews": previews,
            "admission": accepted, "authoring_supervision": str(output/"AUTHORING-SUPERVISION.json"),
            "request_groups": len(prepared.groups), "request_acquired_bytes": prepared.acquired_bytes,
            "native_cpu_seconds": native_cpu, "wall_seconds": time.monotonic()-started,
            "claim": "LOCAL_CHECKED_CONTRIBUTION_NOT_INDEX_PUBLICATION_OR_PEER_ACCEPTANCE"}
        check(); save("RESULT.json", result)
        return result
    except BaseException as error:
        failure = ContributionError(phase, error, accepted, native_cpu)
        failure.report.update(diagnostics)
        if output is not None:
            try:
                save("FAILURE.json", failure.report)
            except BaseException as log_error:
                failure.report["failure_log_error"] = {"error_type": type(log_error).__name__, "error": str(log_error)}
        raise failure from error
