"""Internal synchronous reuse of immutable owner-installation pin checks.

Only a trusted, non-yielding validation phase may use this helper. The local
runtime/filesystem is owner-controlled and stable during that phase; this is
not protection against hostile concurrent mutation or an acceptance cache.
Successful pins are sampled on first use and again before successful exit.
No result survives the phase, and nested phases have independent state.
"""
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path


class PinPhaseError(RuntimeError):
    pass


_CURRENT = ContextVar("dmkn_internal_pin_validation_phase", default=None)


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
    active, records = state
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
def phase(active):
    """Bracket one synchronous owner-only phase, with fresh successful-exit sweep.

    Do not span an await, a subprocess, network I/O, or a user callback. Every
    original deadline/profile/authority check remains at its original call site;
    active is also called before/after each reused or fresh pin and final sweep.
    """
    if not callable(active):
        raise PinPhaseError("PIN_PHASE_ACTIVE_CALLBACK")
    active()
    records = {}
    token = _CURRENT.set((active, records))
    try:
        yield
        active()
        for path, (checker, exact) in records.items():
            active()
            if checker(path) != {"bytes": exact[0], "sha256": exact[1]}:
                raise PinPhaseError("PIN_PHASE_FINAL_PIN_CHANGED")
            active()
        active()
    finally:
        # A body failure skips finalization, never returns a successful phase,
        # discards all cached results, and restores any independent outer scope.
        _CURRENT.reset(token)
