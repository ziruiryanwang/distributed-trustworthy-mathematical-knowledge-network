"""Internal synchronous reuse of immutable owner-installation pin checks.

Only a trusted, non-yielding validation phase may use this helper. The local
runtime/filesystem is owner-controlled and stable during that phase; this is
not protection against hostile concurrent mutation or an acceptance cache.
Successful pins are sampled on first use and again before successful exit.
No result survives the phase. Nested phases remain independent by default;
only an explicitly registered original owner may borrow an enclosing phase.
Persisted local trust is likewise checked on first touch and freshly after the
pin sweep. Intermediate trust reads are coalesced, not binding/denial checks.
Successful absolute module-origin resolutions are also reused only in this
scope, then freshly resolved after all trust/pin checks. Relative inputs stay
fresh on every call because their interpretation also depends on the cwd.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

from admission import trust as T


class PinPhaseError(RuntimeError):
    pass


_CURRENT = ContextVar("dmkn_internal_pin_validation_phase", default=None)
_ORIGIN_PHASE = ContextVar("dmkn_internal_origin_validation_phase", default=None)


class _PinPhase:
    __slots__ = ("active", "records", "borrowers", "open")

    def __init__(self, active, borrowers):
        self.active = active
        self.records = {}
        self.borrowers = borrowers
        self.open = True


class _PinView:
    __slots__ = ("phase", "active", "open")

    def __init__(self, state, active):
        self.phase = state
        self.active = active
        self.open = True

    def require_open(self):
        if not self.open or not self.phase.open:
            raise PinPhaseError("PIN_PHASE_CLOSED")

    def guard(self):
        self.require_open()
        self.active()


class _OriginPhase:
    __slots__ = ("records", "finalizing", "open")

    def __init__(self):
        self.records = {}
        self.finalizing = False
        self.open = True


def check_origin(module_file, expected):
    """Compare a current module-file string with its original absolute origin.

    Never invoke active here: the phase's active callback calls this helper.
    The caller still checks the module object's identity and current __file__
    type every time. Only successful exact argument pairs enter the phase.
    Relative inputs always resolve afresh, even after a previous success.
    """
    if (type(module_file) is not str or not isinstance(expected, Path)
            or not expected.is_absolute()):
        raise PinPhaseError("ORIGIN_PHASE_INTERNAL_ARGUMENT")
    path = Path(module_file)
    state = _ORIGIN_PHASE.get()
    if state is None:
        return path.resolve() == expected
    if not state.open:
        raise PinPhaseError("ORIGIN_PHASE_CLOSED")
    key = module_file, expected
    if key in state.records:
        if path.is_absolute():
            return True
    elif state.finalizing:
        raise PinPhaseError("ORIGIN_PHASE_NEW_ORIGIN_DURING_FINALIZATION")
    valid = path.resolve() == expected
    if valid:
        state.records[key] = True
    return valid


@contextmanager
def _origin_phase(active):
    """Outer scope for the already trusted non-yielding validation phase.

    Original guards enclose final fresh origin observations. Disk observation
    granularity changes, not module/binding checks. Concurrent hostile path
    rollback and authority escaped before scope completion are not supported.
    """
    state = _OriginPhase()
    token = _ORIGIN_PHASE.set(state)
    try:
        yield
        # Trust and pin finalization have completed. At ordinary top-level exit,
        # active makes fresh unscoped trust reads; nested exit restores the outer
        # trust scope. Do not claim two total trust reads for the composite phase.
        state.finalizing = True
        for module_file, expected in tuple(state.records):
            active()
            if Path(module_file).resolve() != expected:
                raise PinPhaseError("ORIGIN_PHASE_FINAL_ORIGIN_CHANGED")
            active()
    finally:
        state.open = False
        state.records.clear()
        _ORIGIN_PHASE.reset(token)


def _expected(pin):
    if (type(pin) is not dict or set(pin) != {"bytes", "sha256"}
            or type(pin["bytes"]) is not int or pin["bytes"] < 0
            or type(pin["sha256"]) is not str or len(pin["sha256"]) != 64
            or any(char not in "0123456789abcdef" for char in pin["sha256"])):
        raise PinPhaseError("PIN_PHASE_EXACT_PIN")
    return pin["bytes"], pin["sha256"]


def check_pin(checker, path, expected):
    """Return an exact pin comparison; only successful immutable pins are reused."""
    state = _CURRENT.get()
    if state is None:
        return checker(path) == expected
    state.require_open()
    active, records = state.guard, state.phase.records
    active()
    if not isinstance(path, Path) or not path.is_absolute() or not callable(checker):
        raise PinPhaseError("PIN_PHASE_INTERNAL_ARGUMENT")
    exact = _expected(expected)
    prior = records.get(path)
    if prior is not None:
        original_checker, original_exact = prior
        if original_checker is not checker:
            raise PinPhaseError("PIN_PHASE_CHECKER_CONFLICT")
        if original_exact != exact:
            raise PinPhaseError("PIN_PHASE_EXPECTED_CONFLICT")
        active()
        return True
    # Snapshot expected values before calling the trusted checker. A failed
    # comparison is not cached, so a subsequent call must actually check again.
    valid = checker(path) == {"bytes": exact[0], "sha256": exact[1]}
    active()
    if valid:
        records[path] = checker, exact
    return valid


@contextmanager
def phase(active, *, borrowers=()):
    """Bracket one synchronous owner-only phase, with fresh successful-exit sweep.

    Do not span an await, a subprocess, network I/O, or a user callback. Every
    original deadline/profile/authority check remains at its original call site;
    active is also called before/after each reused or fresh pin and final sweep.
    Borrowers is an immutable original-owner identity snapshot, never peer data.
    Default/nested phases are independent even when an enclosing phase exists.
    """
    if not callable(active):
        raise PinPhaseError("PIN_PHASE_ACTIVE_CALLBACK")
    if type(borrowers) is not tuple or any(owner is None for owner in borrowers):
        raise PinPhaseError("PIN_PHASE_BORROWER_IDENTITIES")
    state = _PinPhase(active, borrowers)
    view = _PinView(state, active)
    try:
        # Keep the phase live until pin, trust AND origin finalization finish.
        with _origin_phase(view.guard):
            with T._validation_phase(view.guard):
                view.guard()
                token = _CURRENT.set(view)
                try:
                    yield
                    view.guard()
                    for path, (checker, exact) in state.records.items():
                        view.guard()
                        if checker(path) != {"bytes": exact[0], "sha256": exact[1]}:
                            raise PinPhaseError("PIN_PHASE_FINAL_PIN_CHANGED")
                        view.guard()
                    view.guard()
                finally:
                    _CURRENT.reset(token)
    finally:
        # Both root and borrowed copied-out contexts must refuse after closure.
        view.open = state.open = False
        state.records.clear()


@contextmanager
def borrow_or_phase(active, *, owner):
    """Internal validation-only borrow by an explicitly registered original owner.

    A matching live enclosing state owns the sole successful-exit sweep. Its
    caller must not expose any usable result before that sweep completes, and
    must revoke the original borrower if deferred finalization fails. Every
    borrowed pin visit also invokes this call's own original active/deadline
    guard. No authorization is inferred from another arbitrary caller's phase.
    """
    if not callable(active):
        raise PinPhaseError("PIN_PHASE_ACTIVE_CALLBACK")
    current = _CURRENT.get()
    if current is not None:
        current.require_open()
    if current is None or not any(owner is original for original in current.phase.borrowers):
        with phase(active):
            yield
        return

    def guarded():
        current.guard()
        active()

    view = _PinView(current.phase, guarded)
    token = _CURRENT.set(view)
    try:
        view.guard()
        yield
        view.guard()
    finally:
        view.open = False
        _CURRENT.reset(token)
