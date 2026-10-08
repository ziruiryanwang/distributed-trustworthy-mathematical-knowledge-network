"""Fixed five-layer, native-free process shape; only the reviewed driver runs it."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1]
RUN = SOURCE / "qualification/scenario-shape-01"
LEGACY = SOURCE.parent / "experiments/lean-operation-integration/lifecycle_node_02.py"
CODE = (SOURCE / "tests/run_scenario_shape.py", Path(__file__).resolve(),
        SOURCE / "tests/scenario_profile.py", SOURCE / "py/run_stage.py",
        SOURCE / "py/supervise.py", LEGACY, SOURCE / "py/domains.py")
ROLES = ("worker", "wrapper", "node", "runner", "leaf")
FLAGS = ["-B", "-E", "-s", "-S"]
LIMITS = {"wall_seconds": 20, "cpu_seconds": 15, "memory_mib": 512,
          "active_processes": 16, "stdout_bytes": 65536, "stderr_bytes": 65536,
          "event_bytes": 65536, "request_bytes": 1024,
          "case_seconds": {"shape-timeout": 8}}
ALLOCATION = {"calls": 2, "wall_seconds": 40, "job_cpu_seconds": 30,
              "native_stages": 0}
RETAINED = {"bytes": 8 * 1048576, "files": 128, "entries": 256}


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def read(path, bound=65536):
    with Path(path).open("rb") as stream:
        raw = stream.read(bound + 1)
    require(len(raw) <= bound, "READ_BOUND")
    return raw


def pin(path):
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        require(not ancestor.is_symlink()
                and not getattr(ancestor.lstat(), "st_file_attributes", 0) & 0x400,
                "REPARSE_POINT")
    raw = read(path, 16 * 1048576)
    return {"path": str(path.resolve(strict=True)), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def save(path, value):
    """Exclusive, atomically published barriers; readers never see partial JSON."""
    raw = encode(value)
    require(len(raw) <= 65536, "SAVE_BOUND")
    path, temporary = Path(path), Path(str(path) + ".writing")
    require(not path.exists(), "NEW_RECORD_REQUIRED")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.rename(path)


def load_runtime(launch):
    require(set(launch) == {"schema", "pins", "limits", "allocation", "retained"}
            and type(launch["schema"]) is int and launch["schema"] == 1
            and encode(launch["limits"]) == encode(LIMITS)
            and encode(launch["allocation"]) == encode(ALLOCATION)
            and encode(launch["retained"]) == encode(RETAINED), "EXACT_LAUNCH")
    require(launch["pins"] == [pin(sys.executable), *[pin(path) for path in CODE]],
            "EXACT_ORDERED_SOURCE_PINS")
    names = ("run_stage", "supervise", "domains", "scenario_profile", "lifecycle_node_02")
    require(not any(name in sys.modules for name in names), "RUNTIME_PRELOADED")
    sys.path.insert(0, str(LEGACY.parent))
    sys.path.insert(0, str(SOURCE / "py"))
    import run_stage
    import supervise
    import domains
    import scenario_profile
    import lifecycle_node_02
    require(run_stage.domain_module is domains, "RUNNER_DOMAINS_MODULE_IDENTITY")
    for module, path in ((run_stage, CODE[3]), (supervise, CODE[4]), (run_stage.domain_module, CODE[6]),
                         (scenario_profile, CODE[2]), (lifecycle_node_02, LEGACY)):
        require(Path(module.__file__).resolve() == path, "EXACT_MODULE_ORIGIN")
    return SimpleNamespace(stage=run_stage, supervisor=supervise,
                           profile=scenario_profile, diagnostic=lifecycle_node_02)


def await_file(path, child=None):
    deadline = time.monotonic() + 12
    while not path.exists() and time.monotonic() < deadline:
        require(child is None or child.poll() is None, "CHILD_EXITED_BEFORE_BARRIER")
        time.sleep(0.01)
    require(path.exists(), "BARRIER_DEADLINE")
    return json.loads(read(path))


def child_command(args, role, parent):
    return [sys.executable, *FLAGS, str(CODE[1]), "--config", str(args.config),
            "--state", str(args.state), "--request", str(args.request),
            "--event", str(args.event), "--role", role, "--parent", str(parent)]


def observe(runtime, job, requested):
    stage = runtime.stage
    limits = stage.ExtendedLimits()
    if not job.k.QueryInformationJobObject(job.handle, 9, stage.C.byref(limits),
                                          stage.C.sizeof(limits), None):
        raise stage.C.WinError(stage.C.get_last_error())
    return {"requested_active_processes": requested,
            "active_process_limit_readback": limits.BasicLimitInformation.ActiveProcessLimit,
            "before": stage.Job.stats(job),
            "members": runtime.diagnostic.job_processes(job),
            "after": stage.Job.stats(job)}


def main():
    parser = argparse.ArgumentParser()
    for name in ("config", "state", "request", "event"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--role", choices=ROLES, default="worker")
    parser.add_argument("--parent", type=int, default=0)
    args = parser.parse_args()
    require(os.name == "nt" and sys.dont_write_bytecode and sys.flags.ignore_environment
            and sys.flags.no_site and sys.flags.no_user_site, "WINDOWS_STARTUP_PROFILE")
    raw = read(args.request, 1024)
    request = json.loads(raw)
    require(request in ({"mode": "normal"}, {"mode": "timeout"})
            and raw == encode(request), "EXACT_REQUEST")
    mode, role = request["mode"], args.role
    directory = RUN / "cases" / ("shape-" + mode)
    require(args.state.resolve() == RUN / "reserved-state"
            and args.request.resolve() == directory / "request.json"
            and args.event.resolve() == directory / "event.json", "FIXED_PATHS")
    runtime = load_runtime(json.loads(read(args.config)))
    binding = {"mode": mode, "request_sha256": hashlib.sha256(raw).hexdigest(),
               "native_stages": 0}
    require((role == "worker" and args.parent == 0)
            or (args.parent > 0 and os.getppid() == args.parent), "ACTUAL_PARENT")
    save(directory / ("actual-" + role + ".json"),
         dict(binding, role=role, pid=os.getpid(), parent=args.parent))
    job, child = None, None
    try:
        if role == "leaf":
            release = await_file(directory / "release.json")
            require(mode == "normal" and release == binding, "EXACT_RELEASE")
        else:
            next_role = ROLES[ROLES.index(role) + 1]
            if role in ("wrapper", "runner"):
                job = runtime.stage.Job(30, 256, active_processes=8 if role == "wrapper" else 1)
            command = child_command(args, next_role, os.getpid())
            creationflags = subprocess.CREATE_NO_WINDOW | (0x4 if job is not None else 0)
            save(directory / ("command-" + next_role + ".json"),
                 {"argv": command, "cwd": str(CODE[1].parent), "shell": False,
                  "creationflags": creationflags})
            child = subprocess.Popen(command, cwd=CODE[1].parent, stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False,
                close_fds=True, creationflags=creationflags)
            save(directory / ("launched-" + next_role + ".json"),
                 dict(binding, role=next_role, parent=os.getpid(), pid=child.pid))
            if job is not None:
                job.attach_resume(child)
            actual = await_file(directory / ("actual-" + next_role + ".json"), child)
            require(actual == dict(binding, role=next_role, pid=child.pid, parent=os.getpid()),
                    "ACTUAL_CHILD_BINDING")
            if role == "runner":
                save(directory / "leaf-job.json", dict(binding, observation=observe(runtime, job, 1)))
            if role == "wrapper":
                await_file(directory / "leaf-job.json", child)
                for name in ROLES[1:]:
                    await_file(directory / ("launched-" + name + ".json"), child)
                # This process belongs only to the outer Job. NULL queries that
                # current Job; its separate public Job handle contains the node.
                current_job = SimpleNamespace(k=job.k, handle=None)
                shape = dict(binding, null_handle_queries_wrapper_containing_job=True,
                             wrapper_pid=os.getpid(), public=observe(runtime, job, 8),
                             outer=observe(runtime, current_job, 16))
                save(directory / "shape.json", shape)
                if mode == "normal":
                    save(directory / "release.json", binding)
            code = child.wait(timeout=20)
            require(code == 0, "CHILD_NONZERO")
        complete = dict(binding, role=role, pid=os.getpid(), direct_child_reaped=child is not None,
                        child_pid=child.pid if child else None, returncode=child.returncode if child else None)
        if job is not None:
            deadline = time.monotonic() + 2
            while job.stats()["active_processes"] and time.monotonic() < deadline:
                time.sleep(0.01)
            complete["final_job"] = job.stats()
            require(complete["final_job"]["active_processes"] == 0, "LOCAL_JOB_NOT_QUIESCENT")
            job.close()
            complete["job_closed"] = True
            job = None
        save(directory / ("complete-" + role + ".json"), complete)
        if role == "worker":
            reply = encode({"status": "NATIVE_FREE_SHAPE_COMPLETE", "native_stages": 0})
            save(args.event, dict(binding, response_sha256=hashlib.sha256(reply).hexdigest(),
                                  shape=pin(directory / "shape.json")))
            sys.stdout.buffer.write(reply)
        return 0
    finally:
        try:
            if job is not None:
                job.kill()
        finally:
            try:
                if child is not None:
                    if child.poll() is None:
                        child.kill()
                    child.wait(timeout=2)
            finally:
                if job is not None:
                    job.close()


if __name__ == "__main__":
    raise SystemExit(main())
