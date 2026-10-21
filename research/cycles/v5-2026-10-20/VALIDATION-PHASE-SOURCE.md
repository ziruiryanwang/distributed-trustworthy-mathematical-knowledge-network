# Synchronous trust-validation phase: source checkpoint

2026-10-20, core_growth. Implements root's
[selection](VALIDATION-PHASE-SELECTION.md), following the
[controller diagnosis](MIRROR-CPU-CAUSE.md). **Source only: no product imports,
parsing/compilation, tests, native execution, installation or adoption.**
Root owns finite launches and final acceptance. Core_release reviews this source;
adaptive_audit owns the independent focused controls.

## Exact sources

| Role | Canonical-root-relative path | SHA-256 |
|---|---|---|
| Preserved trust predecessor | `software/v5/trust_withdrawal/admission/trust.py` | `a60fd123845c7cd732967f995363b3132ebab1522cd90870ab728e6a54dd83ee` |
| Fresh trust successor | `software/v5/validation_phase/admission/trust.py` | `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0` |
| Preserved pin predecessor | `software/v5/runtime_efficient/admission/pin_phase.py` | `4b302fc472ced49a7681deb019c20a92674353d9adf109949cba7d3034b0deca` |
| Fresh pin successor | `software/v5/validation_phase/admission/pin_phase.py` | `76b54eb04fa2a66ec598b8c6d668e675d8bd483809f8fa66448fa7319b82a9ce` |

Both predecessors' hashes were rechecked after the new files were written and
are unchanged. Only the two assigned fresh product paths were edited. New files
use LF; no baseline line endings were normalized. Exact unified differences
appear below.

## API and invariants

The private `trust._validation_phase(active)` is a context manager, used only
inside the existing `PP.phase`. It is installed **before** PP's original initial
active callback. The callback's trust observations therefore belong to the same
scope; there is no extra uncached entry read. Existing initial/body/final pin
callbacks and exact file checks remain at their original logical positions.

`TrustDomain._current` now has an uncached ordinary route and a scoped route.
The original complete persisted checking body is moved unchanged to
`_fresh_current`; `_read`, create/open/bind/check/withdraw, registration and
identity-return operations are unchanged. Scoped records key exact domain
objects and snapshot path/raw/directory-key/record-key/identity values.
Every hit checks denial and generation; the ordinary binding check still runs
afterward. A read/phase-generation failure latches denial.

Successful scope exit is ordered:

1. PP's original final file-pin sweep and active callback finish.
2. PP restores its pin context.
3. For each previously observed domain: check cached generation/denial, perform
   unconditional fresh persisted validation, check generation again, then invoke
   the original active callback while the trust scope is still installed.
4. Clear/close trust state and restore the previous context.

The final callback detects a resource/deadline crossing during the final read.
Its existing-domain checks do not cause more disk reads. An unseen domain during
finalization refuses explicitly as `TRUST_PHASE_NEW_DOMAIN_DURING_FINALIZATION`.
Other new failures are `TRUST_PHASE_GENERATION_CHANGED`,
`TRUST_PHASE_CLOSED`, and `TRUST_PHASE_ACTIVE_CALLBACK`.
Original persisted-read, registration and denial errors remain.

Nested scopes do not inherit observations. All exits close/clear scope state in
`finally`; an outer scope is restored, never replaced by an inner cache.
A copied context retaining a closed scope cannot use it as a valid cache.
Body exceptions do not reach the success sweep, so no phase success is returned;
fresh-read failures preserve the existing sticky denial.

Under the established trusted stable-owner/non-yielding phase contract, one
successful phase with `q` repeated checks across `d` distinct domains changes
`q` full persisted reads to exactly `2d`. A nested scope contributes separately.
All authority/profile/resource checks remain. This is an operation-count
argument, not an unmeasured speedup or full-workload completion claim.

The scope is not safe across await, native subprocess, network, user callback,
new public action or authority escape. It intentionally changes persisted-policy
observation to first/final phase reads; hostile transient mutation/rollback and
recall of earlier returned data remain outside the local trust model.

## Exact trust diff

```diff
diff --git a/software/v5/trust_withdrawal/admission/trust.py b/software/v5/validation_phase/admission/trust.py
index d101c5d..d426553 100644
--- a/software/v5/trust_withdrawal/admission/trust.py
+++ b/software/v5/validation_phase/admission/trust.py
@@ -8,6 +8,8 @@ and power-loss durability beyond the filesystem's guarantees are not claimed.
 """
 from __future__ import annotations
 
+from contextlib import contextmanager
+from contextvars import ContextVar
 import hashlib
 import os
 from pathlib import Path
@@ -24,6 +26,50 @@ SUPPORT_LIMITS = C.Limits(max_bytes=MAX_SUPPORT_BYTES)
 RECORD_LIMITS = C.Limits(max_bytes=MAX_RECORD_BYTES)
 
 
+_VALIDATION_PHASE = ContextVar("dmkn_internal_trust_validation_phase", default=None)
+
+
+class _ValidationPhase:
+    __slots__ = ("records", "finalizing", "open")
+
+    def __init__(self):
+        self.records = {}
+        self.finalizing = False
+        self.open = True
+
+
+@contextmanager
+def _validation_phase(active):
+    """Internal disk-read reuse inside one trusted synchronous pin phase.
+
+    No await, process/network dispatch, user callback, public action or authority
+    escape is permitted. Disk observations occur on first touch and successful
+    exit, not every intermediate guard. The owner/filesystem must be stable
+    during the phase; hostile concurrent mutation/rollback is not covered.
+    Original binding, denial and active checks remain uncached. Nested scopes
+    are independent; no cached observation remains usable after either exit.
+    """
+    C.require(callable(active), "TRUST_PHASE_ACTIVE_CALLBACK")
+    state = _ValidationPhase()
+    token = _VALIDATION_PHASE.set(state)
+    try:
+        yield
+        # PP.phase has completed its original final pin sweep before reaching
+        # this point. No previously unseen domain may join the final sweep.
+        state.finalizing = True
+        for domain in tuple(state.records):
+            domain._current()  # cached generation/denial check, never skipped
+            domain._fresh_current()  # unconditional original complete disk read
+            domain._current()  # generation still exact after that read
+            # Charge finalization's CPU/wall tail to the original live guards.
+            # Its already observed domains use this scope, avoiding recursion.
+            active()
+    finally:
+        state.open = False
+        state.records.clear()
+        _VALIDATION_PHASE.reset(token)
+
+
 def _manifest(value):
     C.fields(value, {"schema", "identities", "roles"})
     C.require(value["schema"] == SUPPORT_SCHEMA, "TRUST_SUPPORT_SCHEMA")
@@ -179,7 +225,40 @@ class TrustDomain:
         self._current()
         return self
 
+    def _generation(self):
+        C.require(type(self._identity) is dict
+            and set(self._identity) == {"domain_id", "support_id", "adoption_sha256"},
+            "TRUST_PHASE_GENERATION_CHANGED")
+        return (self._path, self._raw, self._directory_key, self._record_key,
+            tuple(self._identity[name] for name in
+                  ("domain_id", "support_id", "adoption_sha256")))
+
     def _current(self):
+        try:
+            C.require(type(self) is TrustDomain and not self._denied,
+                      "TRUST_DENIAL_LATCHED")
+            state = _VALIDATION_PHASE.get()
+            if state is None:
+                self._fresh_current()
+                return
+            C.require(state.open, "TRUST_PHASE_CLOSED")
+            generation = self._generation()
+            prior = state.records.get(self)
+            if prior is not None:
+                C.require(generation == prior, "TRUST_PHASE_GENERATION_CHANGED")
+                return
+            C.require(not state.finalizing,
+                      "TRUST_PHASE_NEW_DOMAIN_DURING_FINALIZATION")
+            self._fresh_current()
+            C.require(self._generation() == generation,
+                      "TRUST_PHASE_GENERATION_CHANGED")
+            state.records[self] = generation
+        except BaseException:
+            self._denied = True
+            raise
+
+    def _fresh_current(self):
+        # Original persisted validation, deliberately unable to use the phase.
         try:
             C.require(type(self) is TrustDomain and not self._denied,
                       "TRUST_DENIAL_LATCHED")
```

## Exact pin-phase diff

```diff
diff --git a/software/v5/runtime_efficient/admission/pin_phase.py b/software/v5/validation_phase/admission/pin_phase.py
index e8cdd5d..46910ae 100644
--- a/software/v5/runtime_efficient/admission/pin_phase.py
+++ b/software/v5/validation_phase/admission/pin_phase.py
@@ -5,11 +5,15 @@ runtime/filesystem is owner-controlled and stable during that phase; this is
 not protection against hostile concurrent mutation or an acceptance cache.
 Successful pins are sampled on first use and again before successful exit.
 No result survives the phase, and nested phases have independent state.
+Persisted local trust is likewise checked on first touch and freshly after the
+pin sweep. Intermediate trust reads are coalesced, not binding/denial checks.
 """
 from contextlib import contextmanager
 from contextvars import ContextVar
 from pathlib import Path
 
+from admission import trust as T
+
 
 class PinPhaseError(RuntimeError):
     pass
@@ -65,19 +69,23 @@ def phase(active):
     """
     if not callable(active):
         raise PinPhaseError("PIN_PHASE_ACTIVE_CALLBACK")
-    active()
-    records = {}
-    token = _CURRENT.set((active, records))
-    try:
-        yield
+    # Install trust scope before the original entry guard: issuers checked by
+    # that guard share the phase's first read. Its final sweep follows the final
+    # pin sweep below and invokes active after each fresh persisted trust read.
+    with T._validation_phase(active):
         active()
-        for path, (checker, exact) in records.items():
+        records = {}
+        token = _CURRENT.set((active, records))
+        try:
+            yield
             active()
-            if checker(path) != {"bytes": exact[0], "sha256": exact[1]}:
-                raise PinPhaseError("PIN_PHASE_FINAL_PIN_CHANGED")
+            for path, (checker, exact) in records.items():
+                active()
+                if checker(path) != {"bytes": exact[0], "sha256": exact[1]}:
+                    raise PinPhaseError("PIN_PHASE_FINAL_PIN_CHANGED")
+                active()
             active()
-        active()
-    finally:
-        # A body failure skips finalization, never returns a successful phase,
-        # discards all cached results, and restores any independent outer scope.
-        _CURRENT.reset(token)
+        finally:
+            # A body failure skips finalization, never returns a successful phase,
+            # discards all cached results, and restores any independent outer scope.
+            _CURRENT.reset(token)
```
