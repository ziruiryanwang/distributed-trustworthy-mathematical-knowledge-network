"""Prospective one-shot launch binding and current-handle crash quiescence.

Trusted fixed worker, private enrolled root, no external writers/restores or
out-of-Job launchers. Not a hostile Python boundary or a supervisor-loss remedy.
The only recovery caller is the scoped exact Job adapter below, before close.
"""
from copy import deepcopy
import ctypes as C
from ctypes import wintypes as W
import hashlib
import os
import secrets
import time

from discovery import formal_features as F
from discovery.discovery_store import ordinary
from . import codec as P
from . import reclaim as R

SCHEMA = "DMKN_V5_SUPERVISED_SESSION_V1"
OWNERSHIP = "PRIVATE_FIXED_WORKER_NO_EXTERNAL_WRITERS_OR_OUT_OF_JOB_LAUNCHERS_V1"
MAX_SESSION = 16384
_KEY = object()
OPERATOR_SHA = "6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9"
JOB_SHA = "bdd2cbc28258f49ef08b678ba54b437ff541ef4deb0af4aa36795d2baa19b028"
_FIELDS = ("schema", "number", "nonce", "binding", "profile_sha256", "command_sha256",
           "limits", "run_deadline_ns", "recovery_deadline_ns", "cleanup_seconds",
           "bind_calls", "recovery_calls", "owner_cpu_seconds", "state", "worker")


def _kernel():
    F.need(os.name == "nt", "SUPERVISED_WINDOWS_REQUIRED")
    k = C.WinDLL("kernel32", use_last_error=True)
    k.GetCurrentProcess.argtypes = []; k.GetCurrentProcess.restype = W.HANDLE
    k.GetProcessId.argtypes = [W.HANDLE]; k.GetProcessId.restype = W.DWORD
    k.GetProcessTimes.argtypes = [W.HANDLE] + [C.POINTER(W.FILETIME)]*4
    k.GetProcessTimes.restype = W.BOOL
    k.WaitForSingleObject.argtypes = [W.HANDLE, W.DWORD]
    k.WaitForSingleObject.restype = W.DWORD
    return k


def _process_identity(handle=None):
    k = _kernel(); handle = k.GetCurrentProcess() if handle is None else handle
    created, exited, kernel, user = (W.FILETIME() for unused in range(4))
    pid = k.GetProcessId(handle)
    F.need(pid != 0 and k.GetProcessTimes(handle, C.byref(created), C.byref(exited),
                                         C.byref(kernel), C.byref(user)),
           "SUPERVISED_EXACT_PROCESS_QUERY_FAILED")
    return {"pid": int(pid), "created": int(created.dwLowDateTime) |
            int(created.dwHighDateTime) << 32}


def _check_worker(value):
    F.fields(value, ("pid", "created"))
    F.uint(value["pid"], 1, 2**32-1); F.uint(value["created"], 1, 2**64-1)


def _binding(manager):
    manager._active()
    root = ordinary(manager.root)
    # Same path/marker bytes alone do not identify the enrolled filesystem.
    entries = [(root, "directory"), (root/"manager.json", "file"),
               (root/"generations.sqlite", "file"), (root/"owner.lock", "file"),
               (root/"slot-0", "directory"), (root/"slot-1", "directory")]
    R._small(root/"manager.json", manager._marker)
    return {"root": str(root), "epoch": manager.config["epoch"],
            "config_sha256": P.digest(manager._raw), "marker_sha256": P.digest(manager._marker),
            "identities": [R._identity(R._info(path, kind)) for path, kind in entries]}


def _stable(session):
    return P.digest(F.compact({key: value for key, value in session.items()
                               if key not in ("state", "worker")}))


def validate(manager):
    manager._active()
    row = manager.db.execute("SELECT session_sequence,session FROM meta WHERE id=1").fetchone()
    F.need(row is not None, "SUPERVISED_SESSION_CENSUS")
    number, raw = row
    F.uint(number, 0, manager.config["max_sessions"], "SUPERVISED_SESSION_CENSUS")
    if raw is None:
        F.need(number == 0, "SUPERVISED_MISSING_SESSION")
        return None
    session = F.strict(bytes(raw), MAX_SESSION); F.fields(session, _FIELDS)
    F.need(session["schema"] == SCHEMA and session["number"] == number and number > 0,
           "SUPERVISED_SESSION_SCHEMA_OR_SEQUENCE")
    for key in ("nonce", "profile_sha256", "command_sha256"): F.hexid(session[key])
    F.need(session["binding"] == _binding(manager), "SUPERVISED_ENROLLED_ROOT_CHANGED")
    F.fields(session["limits"], ("cpu_seconds", "memory_mib", "active_processes",
                                 "wall_seconds", "stdout_bytes", "stderr_bytes"))
    for value in session["limits"].values(): F.uint(value, 1, 2**53-1)
    F.uint(session["limits"]["active_processes"], 1, 8)
    F.uint(session["run_deadline_ns"], 1, 2**63-1)
    F.uint(session["recovery_deadline_ns"], session["run_deadline_ns"]+1, 2**63-1)
    F.uint(session["cleanup_seconds"], 25, 60)
    F.need(session["recovery_deadline_ns"]-session["run_deadline_ns"] ==
           session["cleanup_seconds"]*1000000000, "SUPERVISED_ORIGINAL_CLEANUP_BOUND")
    F.need(session["bind_calls"] == 2 and session["recovery_calls"] == 2
           and session["owner_cpu_seconds"] == 5, "SUPERVISED_FIXED_REGISTRY_ACTION_CAPS")
    F.need(session["state"] in ("RESERVED", "BOUND", "QUIESCED"), "SUPERVISED_SESSION_STATE")
    if session["state"] == "RESERVED":
        F.need(session["worker"] is None, "SUPERVISED_RESERVED_WORKER")
    else: _check_worker(session["worker"])
    return session


def validate_run(manager, record):
    if record["runs"] == 0:
        F.need("session" not in record and "quiescence" not in record,
               "SUPERVISED_UNRUN_BINDING")
        return
    facet = record.get("session")
    F.fields(facet, ("number", "nonce", "session_sha256", "worker", "slot",
                     "generation", "sequence", "run"))
    F.uint(facet["number"], 1, manager.config["max_sessions"])
    for key in ("nonce", "session_sha256", "generation"): F.hexid(facet[key])
    _check_worker(facet["worker"])
    F.need((facet["slot"], facet["generation"], facet["sequence"], facet["run"]) ==
           (record["slot"], record["generation"], record["sequence"], record["runs"]),
           "SUPERVISED_STORED_RUN_JOIN")
    if record["run_state"] == "QUIESCED_UNCLEAN":
        F.need(record.get("quiescence") == {"schema": "DMKN_V5_EXACT_JOB_QUIESCENCE_V1",
               "session_sha256": facet["session_sha256"], "nonce": facet["nonce"],
               "worker": facet["worker"]}, "SUPERVISED_STORED_QUIESCENCE")
        F.need("closure_sha256" not in record, "SUPERVISED_NOT_ORDERLY_CLOSED")
    else:
        F.need("quiescence" not in record, "SUPERVISED_UNEXPECTED_QUIESCENCE")


def _save_session(manager, session):
    raw = F.compact(session); F.need(len(raw) <= MAX_SESSION, "SUPERVISED_SESSION_BOUND")
    manager.db.execute("UPDATE meta SET session_sequence=?,session=? WHERE id=1",
                       (session["number"], raw))


def run_binding(session, record):
    return {"number": session["number"], "nonce": session["nonce"],
            "session_sha256": _stable(session), "worker": deepcopy(session["worker"]),
            "slot": record["slot"], "generation": record["generation"],
            "sequence": record["sequence"], "run": record["runs"]}


class _WorkerJoin:
    def __init__(self, key, manager, session):
        F.need(key is _KEY, "SUPERVISED_JOIN_ISSUER")
        self.manager = manager
        self.session = deepcopy(session)


def join_current_worker(manager, profile_sha256):
    manager._call(); F.hexid(profile_sha256)
    F.need(manager._worker_session is None and not manager._handles,
           "SUPERVISED_WORKER_ALREADY_JOINED")
    session = validate(manager)
    F.need(session is not None and session["state"] == "BOUND"
           and session["profile_sha256"] == profile_sha256,
           "SUPERVISED_NO_CURRENT_BOUND_WORKER")
    F.need(time.monotonic_ns() < session["run_deadline_ns"], "SUPERVISED_RUN_EXPIRED")
    F.need(_process_identity() == session["worker"], "SUPERVISED_NOT_CURRENT_DIRECT_WORKER")
    manager._worker_session = _WorkerJoin(_KEY, manager, session)
    return {"number": session["number"], "nonce": session["nonce"],
            "worker": deepcopy(session["worker"]), "mathematical_acceptance": False}


def current_worker(manager, outer_deadline=None):
    manager._active(); join = manager._worker_session
    F.need(type(join) is _WorkerJoin and join.manager is manager,
           "SUPERVISED_CURRENT_WORKER_JOIN_REQUIRED")
    session = validate(manager)
    F.need(session == join.session and session["state"] == "BOUND"
           and _process_identity() == session["worker"], "SUPERVISED_WORKER_BINDING_CHANGED")
    F.need(time.monotonic_ns() < session["run_deadline_ns"], "SUPERVISED_RUN_EXPIRED")
    if outer_deadline is not None:
        F.need(outer_deadline*1000000000 <= session["run_deadline_ns"],
               "SUPERVISED_RUN_DEADLINE_EXTENSION")
    return session


class _Launch:
    def __init__(self, key, manager, session):
        F.need(key is _KEY, "SUPERVISED_LAUNCH_ISSUER")
        self.root, self.config = manager.root, deepcopy(manager.config)
        # Carry the verified current binding, not a config-derived adoption flag.
        self.writer_profile_sha256 = manager._writer_profile
        self.session = deepcopy(session)
        self.job_created = False
        self.bound = False
        self.outcome = {"status": "UNKNOWN", "reason": "LIVE_QUIESCENCE_NOT_OBSERVED"}


def _open_launch(launch, calls):
    from .lifecycle import ManagedGenerations
    F.need(type(launch) is _Launch, "SUPERVISED_EXACT_LAUNCH")
    deadline = launch.session["recovery_deadline_ns"]/1000000000
    F.need(time.monotonic() < deadline, "SUPERVISED_RECOVERY_EXPIRED")
    return ManagedGenerations.open(launch.root, launch.config, deadline=deadline,
                                  writer_profile_sha256=launch.writer_profile_sha256,
                                  calls=calls, cpu_seconds=launch.session["owner_cpu_seconds"],
                                  _launch=launch)


def expect_open(manager, launch):
    """Before any open-time rewrite, require the current exact private launch."""
    F.need(type(launch) is _Launch and time.monotonic_ns() < launch.session["recovery_deadline_ns"],
           "SUPERVISED_EXACT_UNEXPIRED_LAUNCH")
    F.need(validate(manager) == launch.session, "SUPERVISED_OPEN_SESSION_MISMATCH")


def _same(manager, launch):
    session = validate(manager)
    F.need(session is not None and _stable(session) == _stable(launch.session),
           "SUPERVISED_SESSION_REPLACED")
    return session


def _bind_process(launch, worker):
    F.need(not launch.bound and time.monotonic_ns() < launch.session["run_deadline_ns"],
           "SUPERVISED_LAUNCH_ALREADY_BOUND_OR_EXPIRED")
    _check_worker(worker)
    manager = _open_launch(launch, launch.session["bind_calls"])
    try:
        manager._call()
        def bind():
            session = _same(manager, launch)
            F.need(session["state"] == "RESERVED" and session["worker"] is None,
                   "SUPERVISED_BIND_ONCE")
            session["worker"] = deepcopy(worker); session["state"] = "BOUND"
            _save_session(manager, session)
        manager._transaction(bind)
    finally:
        manager.close()
    # Ambiguous COMMIT or failed owner close cannot arm resume.
    launch.session["worker"] = deepcopy(worker); launch.session["state"] = "BOUND"
    launch.bound = True


def _commit_quiescence(launch, observe):
    F.need(type(launch) is _Launch and launch.bound, "SUPERVISED_UNBOUND_RECOVERY")
    observe()
    manager = _open_launch(launch, launch.session["recovery_calls"])
    try:
        manager._call()
        def commit():
            session = _same(manager, launch)
            F.need(session["state"] == "BOUND" and session["worker"] == launch.session["worker"],
                   "SUPERVISED_RECOVERY_SESSION_MISMATCH")
            # This callback owns the still-open exact Job and direct HANDLE.
            # Reobserve inside the transaction; a caller JSON never reaches here.
            observe()
            changed = []
            for record in manager._records():
                if record is None or record["runs"] == 0: continue
                expected = run_binding(session, record)
                if record["session"] != expected:
                    F.need(record["run_state"] not in ("RESERVED", "LIVE", "CLOSING", "UNKNOWN"),
                           "SUPERVISED_UNRELATED_UNCLOSED_RUN")
                    continue
                if record["run_state"] == "CLOSED": continue
                F.need(record["run_state"] in ("RESERVED", "LIVE", "CLOSING", "UNKNOWN"),
                       "SUPERVISED_RECOVERY_RUN_STATE")
                record["run_state"] = "QUIESCED_UNCLEAN"
                record.pop("closure_sha256", None)
                record["quiescence"] = {"schema": "DMKN_V5_EXACT_JOB_QUIESCENCE_V1",
                    "session_sha256": expected["session_sha256"], "nonce": session["nonce"],
                    "worker": deepcopy(session["worker"])}
                # Phase, failure/retirement intent, horizons and every charge stay.
                manager._save(record); changed.append(record["slot"])
            session["state"] = "QUIESCED"; _save_session(manager, session)
            return changed
        changed = manager._transaction(commit)
    finally:
        manager.close()
    launch.outcome = {"status": "QUIESCED", "unclean_slots": changed,
                      "orderly_close_claim": False, "mathematical_acceptance": False}


def _pin(module, expected):
    path = ordinary(module.__file__, directory=False)
    F.need(path.stat().st_size <= 1048576, "SUPERVISED_SOURCE_BOUND")
    with path.open("rb") as stream: raw = stream.read(1048577)
    F.need(len(raw) <= 1048576 and hashlib.sha256(raw).hexdigest() == expected,
           "SUPERVISED_SOURCE_PIN")


def supervise(manager, *, profile, argv, cwd, evidence, limits, operator_module,
              job_module, cleanup_seconds=25, stdin_bytes=None, serve_seconds=None):
    """Consume a manager owner; launch once using the exact frozen supervisor.

    profile binds the root-selected immutable trusted worker/source map. Caller
    must load the pinned modules through the adopted loader (no monkeypatches).
    Registration precedes Popen; exact worker binding precedes Assign+Resume.
    Registry actions use the original cleanup deadline and five CPU seconds
    each, not a renewed service lease. Guards are sampled, not hard wall limits.
    This function never retries a launch.
    """
    from .lifecycle import ManagedGenerations
    F.need(type(manager) is ManagedGenerations and not manager._handles
           and manager._worker_session is None, "SUPERVISED_EXACT_IDLE_MANAGER")
    manager._call()
    F.fields(profile, ("sha256", "ownership")); F.hexid(profile["sha256"])
    F.need(profile["ownership"] == OWNERSHIP, "SUPERVISED_OWNERSHIP_PREMISE")
    _pin(operator_module, OPERATOR_SHA); _pin(job_module, JOB_SHA)
    A, J = operator_module, job_module
    limits = A.limits_checked(deepcopy(limits))
    F.uint(limits["active_processes"], 1, 8, "SUPERVISED_FROZEN_JOB_PROCESS_BOUND")
    F.uint(cleanup_seconds, 25, 60)
    F.need(manager._cpu_cap-(time.process_time()-manager._cpu_start) >= 10,
           "SUPERVISED_PREALLOCATED_OWNER_CPU_REQUIRED")
    F.need(type(argv) is list and 1 <= len(argv) <= 128
           and all(type(v) is str and 0 < len(v) <= 32768 and "\0" not in v for v in argv),
           "SUPERVISED_COMMAND_BOUND")
    cwd = ordinary(cwd); evidence = ordinary(evidence, fresh=True)
    F.need(not evidence.is_relative_to(manager.root) and not manager.root.is_relative_to(evidence),
           "SUPERVISED_EVIDENCE_ROOT_OVERLAP")
    F.need(stdin_bytes is None or type(stdin_bytes) is bytes and 0 < len(stdin_bytes) <= 1048576,
           "SUPERVISED_STDIN_BOUND")
    F.need(serve_seconds is None or type(serve_seconds) is int
           and 1 <= serve_seconds <= limits["wall_seconds"]-15 and stdin_bytes is None,
           "SUPERVISED_FINITE_SERVICE_LEASE")
    started_ns = time.monotonic_ns()
    run_deadline = started_ns+limits["wall_seconds"]*1000000000
    recovery_deadline = run_deadline+cleanup_seconds*1000000000
    F.need(recovery_deadline <= manager._deadline*1000000000,
           "SUPERVISED_PREALLOCATED_CLEANUP_REQUIRED")
    command = {"argv": argv, "cwd": str(cwd), "evidence": str(evidence),
               "stdin_sha256": None if stdin_bytes is None else hashlib.sha256(stdin_bytes).hexdigest(),
               "serve_seconds": serve_seconds}
    F.need(len(F.compact(command)) <= 65536, "SUPERVISED_COMMAND_BOUND")
    def reserve():
        old = validate(manager)
        F.need(old is None or old["state"] == "QUIESCED", "SUPERVISED_PRIOR_SESSION_UNRESOLVED")
        number = 1 if old is None else old["number"]+1
        F.need(number <= manager.config["max_sessions"], "SUPERVISED_SESSION_CAP")
        F.need(all(r is None or r["run_state"] in ("NONE", "CLOSED", "QUIESCED_UNCLEAN")
                   for r in manager._records()), "SUPERVISED_PRIOR_RUN_UNKNOWN")
        session = {"schema": SCHEMA, "number": number, "nonce": secrets.token_hex(32),
            "binding": _binding(manager), "profile_sha256": profile["sha256"],
            "command_sha256": P.digest(F.compact(command)), "limits": limits,
            "run_deadline_ns": run_deadline, "recovery_deadline_ns": recovery_deadline,
            "cleanup_seconds": cleanup_seconds, "bind_calls": 2, "recovery_calls": 2,
            "owner_cpu_seconds": 5, "state": "RESERVED", "worker": None}
        _save_session(manager, session)
        return session
    session = manager._transaction(reserve)
    launch = _Launch(_KEY, manager, session)
    manager.close()  # Failure or ambiguous commit forbids launch.

    class BoundJob(J.Job):
        def __init__(self, seconds, memory_mib, active_processes=1):
            F.need(not launch.job_created, "SUPERVISED_ONE_JOB_ONLY")
            launch.job_created = True
            self._ready = False; self._sealed = False; self._attached = False
            self._recovery_attempted = False; self._direct = None; self._direct_handle = None
            self._job_handle = None
            super().__init__(seconds, memory_mib, active_processes=active_processes)
            self._job_handle = self.handle
            self._ready = True

        def attach_resume(self, process):
            F.need(self._ready and not self._sealed and not self._attached,
                   "SUPERVISED_ATTACH_ONCE")
            self._attached = True
            self._direct = process; self._direct_handle = int(process._handle)
            worker = _process_identity(self._direct_handle)
            F.need(worker["pid"] == process.pid, "SUPERVISED_POPEN_HANDLE_IDENTITY")
            _bind_process(launch, worker)
            # Original containment assignment and resume are unchanged.
            super().attach_resume(process)

        def _observe(self):
            F.need(self._ready and self._sealed and launch.bound and self.handle
                   and self.handle == self._job_handle
                   and self._direct is not None and int(self._direct._handle) == self._direct_handle,
                   "SUPERVISED_CURRENT_HANDLES_REQUIRED")
            F.need(time.monotonic_ns() < session["recovery_deadline_ns"],
                   "SUPERVISED_ORIGINAL_CLEANUP_EXPIRED")
            F.need(_process_identity(self._direct_handle) == launch.session["worker"],
                   "SUPERVISED_DIRECT_HANDLE_CHANGED")
            # Popen.wait can return a cached returncode; additionally wait on the
            # exact still-owned kernel handle itself. Zero timeout never extends cleanup.
            F.need(_kernel().WaitForSingleObject(self._direct_handle, 0) == 0,
                   "SUPERVISED_DIRECT_WAIT_NOT_SIGNALED")
            self._direct.wait(timeout=0)
            F.need(self.stats()["active_processes"] == 0, "SUPERVISED_JOB_NOT_QUIESCENT")

        def close(self):
            # Frozen Job.__init__ dynamically calls close on partial failure.
            # State exists before super().__init__; that path never recovers.
            self._sealed = True
            try:
                if self._ready and launch.bound and not self._recovery_attempted:
                    self._recovery_attempted = True
                    _commit_quiescence(launch, self._observe)
            finally:
                super().close()

    report = A.supervise(deepcopy(argv), cwd, evidence, limits, BoundJob,
                         started=started_ns/1000000000, stdin_bytes=stdin_bytes,
                         serve_seconds=serve_seconds)
    report["session_recovery"] = deepcopy(launch.outcome)
    return report
