"""Native-free launcher controls; root selects execution after source review.

Load exact run.py, exercise real grammar/separation/binding orchestration and
terminal reporting, then double only filesystem/native-supervision effects for
run(). No process, network, protected owner state or package installation is
opened, and no fixture files are created. This does not retest Windows Job internals.
"""
from __future__ import annotations

from copy import deepcopy
from contextlib import ExitStack
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace as NS
from unittest.mock import patch


HERE = Path(__file__).resolve().parent


def need(ok, code):
    if not ok:
        raise AssertionError(code)


def raw(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def main():
    source = (HERE/"run.py").read_bytes()
    spec = importlib.util.spec_from_file_location("_launcher_control_subject", HERE/"run.py")
    entry = importlib.util.module_from_spec(spec)
    exec(compile(source, str(HERE/"run.py"), "exec"), entry.__dict__)
    cases = []

    def passed(label):
        cases.append({"case": label, "status": "PASS"})

    def refuses(label, callback, code):
        try:
            callback()
        except ValueError as error:
            need(str(error) == code, "WRONG_REFUSAL:"+label+":"+str(error))
        else:
            raise AssertionError("EXPECTED_REFUSAL:"+label)
        passed(label)

    for tool, tokens in (("owner", ["--", "produce-baseline", "--approve-local-project"]),
                         ("peer", ["--", "find", "--config", "input.json"]),
                         ("query", ["--", "--native-type", "type.json"])):
        argv, _ = entry.child_arguments(tool, tokens)
        need(argv == tokens[1:], "EXACT_FIXED_DISPATCH")
    passed("all-three-fixed-cli-grammars")
    for label, tool, tokens, code in (
        ("arbitrary-tool", "shell", [], "RUN_CHILD_ARGUMENTS"),
        ("arbitrary-operation", "peer", ["exec"], "RUN_FIXED_OPERATION"),
        ("allocation-override", "peer", ["find", "--cpu-seconds", "600"], "RUN_UNAPPROVED_OPTION_OR_MISSING_VALUE"),
        ("profile-override", "owner", ["status", "--profile-sha256", "0"*64], "RUN_UNAPPROVED_OPTION_OR_MISSING_VALUE"),
        ("abbreviated-option", "peer", ["find", "--conf", "x"], "RUN_UNAPPROVED_OPTION_OR_MISSING_VALUE"),
        ("duplicate-option", "peer", ["find", "--config", "a", "--config", "b"], "RUN_DUPLICATE_OPTION"),
        ("equals-option", "peer", ["find", "--config=a"], "RUN_EXACT_OPTION"),
        ("shell-positional", "peer", ["find", ";"], "RUN_EXACT_OPTION"),
    ):
        refuses(label, lambda t=tool, v=tokens: entry.child_arguments(t, v), code)

    limits = dict(wall_seconds=60, cpu_seconds=30, memory_mib=512,
                  active_processes=4, stdout_bytes=65536, stderr_bytes=65536)
    need(entry.checked_limits(NS(tool="peer", **limits)) == limits, "EXACT_LIMITS")
    for label, key, value, code in (("boolean-cap", "memory_mib", True, "RUN_EXPLICIT_FINITE_LIMITS"),
        ("wall-too-small", "wall_seconds", 34, "RUN_CHILD_MINIMUM_ALLOWANCE"),
        ("process-ceiling", "active_processes", 9, "RUN_EXPLICIT_FINITE_LIMITS")):
        changed = dict(limits); changed[key] = value
        refuses(label, lambda c=changed: entry.checked_limits(NS(tool="peer", **c)), code)
    changed = dict(limits); changed["cpu_seconds"] = 601
    refuses("query-cpu-ceiling", lambda: entry.checked_limits(NS(tool="query", **changed)),
            "RUN_QUERY_CPU_ALLOWANCE")

    # Real lexical path comparisons, with filesystem inspection explicitly doubled.
    base = HERE/"uncreated-control-fixture"
    pkg, pyr, lean = (base/name for name in ("package", "python", "lean"))
    diag, out, index = (base/name for name in ("diagnostics", "output", "index"))
    options = {"output": str(out), "config": str(base/"config.json")}
    with patch.object(entry, "ordinary", lambda value, **_: Path(value)):
        selected = entry.separate_arguments(pkg, pyr, lean, diag, options, (index,))
        need(selected["output"] == out, "SEPARATION_POSITIVE")
        passed("disjoint-direct-and-index-paths")
        for label, d, opt, extra, code in (
            ("diagnostics-in-package", pkg/"logs", options, (), "RUN_WRITABLE_SUPPORT_OVERLAP"),
            ("diagnostics-in-output", out/"logs", options, (), "RUN_DIAGNOSTICS_ARGUMENT_OVERLAP"),
            ("diagnostics-in-index", index/"logs", options, (index,), "RUN_WRITABLE_OVERLAP"),
            ("input-in-output", diag, {"output": str(out), "config": str(out/"in.json")}, (), "RUN_INPUT_WRITABLE_OVERLAP"),
        ):
            refuses(label, lambda d=d, o=opt, e=extra: entry.separate_arguments(pkg, pyr, lean, d, o, e), code)
        config_raw = raw({"index": {"path": str(index), "create": False}})
        with patch.object(entry, "read", lambda *_: config_raw):
            args = {"config": str(base/"config.json"), "config-sha256": sha(config_raw)}
            need(entry.configured_state("peer", ["publish"], args, lambda: None) == (index,),
                 "PINNED_INDIRECT_INDEX")
            passed("pinned-config-index-extracted")
            wrong = dict(args); wrong["config-sha256"] = "0"*64
            refuses("wrong-config-pin", lambda: entry.configured_state("peer", ["serve"], wrong, lambda: None),
                    "RUN_PEER_CONFIG_PIN")
        with patch.object(entry, "read", side_effect=AssertionError("UNNEEDED_CONFIG_READ")):
            need(entry.configured_state("peer", ["find"], {}, lambda: None) == (), "STATEFREE_CONFIG_NOT_READ")
            need(entry.configured_state("owner", ["status"], {}, lambda: None) == (), "OWNER_CONFIG_NOT_READ")
            passed("non-index-command-does-not-read-config")

    # Binding orchestration uses exact real descriptor hashes; byte-reader and
    # file-pin primitive are doubles, not a claim of filesystem tamper testing.
    files = {name: {"bytes": len(name.encode()), "sha256": sha(name.encode())}
             for name in ("run.py", "owner.py", "peer.py", "query.py", "profile.py")}
    roles = {**entry.SUPERVISOR_ROLES, **entry.PYTHON_ROLES}
    manifest = {"schema": "DMKN_ORDINARY_NATIVE_INSTALLATION_V1", "roles": dict(roles),
                "files": {logical: {"bytes": 1, "sha256": "a"*64} for logical in roles.values()}}
    def descriptors(m=manifest):
        manifest_raw = raw(m)
        profile_raw = raw({"schema": "DMKN_ORDINARY_OWNER_PROFILE_V1",
            "installation_manifest_sha256": sha(manifest_raw), "helper_paths": ["authoring/helpers"],
            "author_worker": "author_worker.py", "files": files})
        return manifest_raw, profile_raw
    manifest_raw, profile_raw = descriptors()
    selected_pins = []
    def pin_file(path, pin, check, *, source=False):
        selected_pins.append((path, source)); check()
        return b"source" if source else None
    with ExitStack() as stack:
        stack.enter_context(patch.object(entry, "ordinary", lambda value, **_: Path(value)))
        stack.enter_context(patch.object(entry, "read", lambda path, *_:
            profile_raw if path.name == "PROFILE.json" else manifest_raw))
        stack.enter_context(patch.object(entry, "bound_file", pin_file))
        stack.enter_context(patch.object(entry, "sys", NS(executable=str(pyr/"python.exe"))))
        bound = entry.bind_support(pkg, sha(profile_raw), pyr, lambda: None)
        need(len(selected_pins) == 11 and set(bound["support"]) == set(roles), "ALL_SUPPORT_PINS")
        need({path for path, is_source in selected_pins if not is_source} ==
             {pyr/"python.exe", pyr/"python314.dll", pyr/"python3.dll"}, "RUNTIME_PINS")
        passed("five-entries-three-supervisors-three-runtime-pins")
        refuses("wrong-profile-pin", lambda: entry.bind_support(pkg, "0"*64, pyr, lambda: None),
                "RUN_PROFILE_PIN")
        with patch.object(entry, "sys", NS(executable=str(pyr/"other.exe"))):
            refuses("wrong-running-python", lambda: entry.bind_support(pkg, sha(profile_raw), pyr, lambda: None),
                    "RUN_RUNNING_PYTHON")
        broken = deepcopy(manifest); broken["roles"]["job"] = "other.py"
        bad_manifest, bad_profile = descriptors(broken)
        with patch.object(entry, "read", lambda path, *_:
                          bad_profile if path.name == "PROFILE.json" else bad_manifest):
            refuses("wrong-supervisor-role", lambda: entry.bind_support(pkg, sha(bad_profile), pyr, lambda: None),
                    "RUN_REQUIRED_ROLE:job")
        with patch.object(entry, "bound_file", side_effect=ValueError("CONTROL_PIN_MISMATCH")):
            refuses("entry-pin-failure-propagates", lambda: entry.bind_support(pkg, sha(profile_raw), pyr, lambda: None),
                    "CONTROL_PIN_MISMATCH")

    clean = {"status": "COMMAND_EXITED_ZERO_AND_CLOSED", "child_exit_code": 0,
        "direct_child_reaped": True, "job_closed": True, "cleanup_errors": [],
        "final_job": {"active_processes": 0, "terminated_processes": 0}}
    need(entry.operational_result(clean)["ok"] and
         entry.operational_result(clean)["mathematical_disposition"] == "NOT_INTERPRETED", "CLEAN_NOT_MATH")
    for field, value in (("status", "RESOURCE_LIMIT"), ("child_exit_code", 1),
                         ("job_closed", False), ("cleanup_errors", ["unknown"]), ("final_job", None)):
        changed = deepcopy(clean); changed[field] = value
        need(not entry.operational_result(changed)["ok"], "NONCLEAN_NOT_SUCCESS")
    passed("terminal-claims-never-promote-interruption-or-acceptance")

    class VirtualPath:
        """Only enough path protocol for run dispatch; no filesystem effects."""
        def __init__(self, value): self.path = Path(str(value))
        def __str__(self): return str(self.path)
        def __truediv__(self, tail): return VirtualPath(self.path/tail)
        def absolute(self): return self
        @property
        def parent(self): return VirtualPath(self.path.parent)
        def mkdir(self): calls.append("mkdir")

    args = NS(tool="peer", child_args=["find", "--config", str(base/"config.json")],
        profile_sha256="a"*64, python_runtime=str(pyr), lean_runtime=str(lean),
        diagnostics=str(diag), **limits)
    calls, saved, seen = [], {}, {}
    current_report, failure_mode = deepcopy(clean), None
    job_class = object()
    def old_environment(_): return {"PATH": "historical", "KEPT": "yes"}
    def save_new(path, value):
        if failure_mode == "save-supervision" and str(path).endswith("SUPERVISION.json"):
            raise OSError("CONTROL_REPORT_FAILURE")
        saved[str(path)] = deepcopy(value)
    def supervise(argv, cwd, evidence, passed_limits, job, *, started):
        calls.append("supervise")
        seen.update(argv=argv, cwd=str(cwd), evidence=str(evidence), limits=passed_limits,
                    job=job, started=started, environment=supervisor.child_environment(cwd))
        if failure_mode == "supervisor":
            raise RuntimeError("CONTROL_SUPERVISOR_UNKNOWN")
        return deepcopy(current_report)
    supervisor = NS(limits_checked=lambda value: value, child_environment=old_environment,
                    save_new=save_new, supervise=supervise)
    def bind(*_):
        calls.append("bind")
        if failure_mode == "bind":
            raise ValueError("CONTROL_BIND_FAILED")
        return {"installation_manifest_sha256": "b"*64}
    def load(_):
        calls.append("load")
        return supervisor, job_class
    with ExitStack() as stack:
        for name, value in (("Path", VirtualPath), ("ordinary", lambda value, **_: VirtualPath(value)),
            ("configured_state", lambda *args: ()), ("separate_arguments", lambda *args: None),
            ("bind_support", bind), ("load_supervision", load),
            ("sys", NS(flags=NS(isolated=1, no_site=1, optimize=0), dont_write_bytecode=True))):
            stack.enter_context(patch.object(entry, name, value))
        result = entry.run(args)
        need(result["ok"] and calls == ["bind", "load", "mkdir", "supervise"], "EXACT_BIND_LAUNCH_ORDER")
        need(seen["limits"] == limits and seen["started"] == entry.START_WALL and
             seen["job"] is job_class and seen["argv"][:4] == [str(pyr/"python.exe"), "-I", "-S", "-B"] and
             seen["argv"][4] == str(HERE/"peer.py") and seen["argv"].count("--cpu-seconds") == 1 and
             seen["argv"][seen["argv"].index("--cpu-seconds")+1] == "30", "ORIGINAL_CAP_AND_FIXED_ENTRY")
        need(seen["environment"]["KEPT"] == "yes" and str(pyr) in seen["environment"]["PATH"] and
             str(lean/"bin") in seen["environment"]["PATH"] and
             supervisor.child_environment is old_environment, "SCOPED_SELECTED_ENVIRONMENT")
        need(saved[str(diag/"SUPERVISION.json")] == clean and result["mathematical_disposition"] == "NOT_INTERPRETED",
             "UNMODIFIED_CHILD_REPORT")
        passed("one-fixed-dispatch-original-caps-and-preserved-report")
        for label, mode, report, expected in (
            ("binding-fails-before-import-or-child", "bind", clean, "NO_CHILD_LAUNCHED"),
            ("resource-stop-is-not-math-rejection", None, {**clean, "status": "RESOURCE_LIMIT"}, "OPERATION_INTERRUPTED_OR_UNSUCCESSFUL"),
            ("supervisor-error-is-unknown", "supervisor", clean, "OPERATION_OUTCOME_UNKNOWN"),
            ("report-error-preserves-unknown-effects", "save-supervision", clean, "OPERATION_OUTCOME_UNKNOWN"),
        ):
            calls.clear(); saved.clear(); failure_mode, current_report = mode, report
            result = entry.run(args)
            need(not result["ok"] and result["status"] == expected and
                 result["mathematical_disposition"] == "NOT_INTERPRETED" and
                 supervisor.child_environment is old_environment, "TRUTHFUL_FAILURE:"+label)
            need(calls.count("supervise") == (0 if mode == "bind" else 1), "NO_RETRY:"+label)
            if mode == "bind": need(calls == ["bind"], "BIND_BEFORE_IMPORT")
            passed(label)
    print(json.dumps({"status": "PASS", "scope": "LAUNCHER_CONTRACTS_WITH_DOUBLED_FILESYSTEM_AND_SUPERVISION",
        "run_sha256": sha(source), "cases": cases}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
