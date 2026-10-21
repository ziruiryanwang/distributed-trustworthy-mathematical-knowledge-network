# Remove repeated persisted-policy reads inside one validation phase

2026-10-20, root. Implementation selection, not execution or release adoption.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

The adopted mirror01 outcome c37d3d91 stopped at controller120CPU before the
author worker, after real method discovery/admission/import. Current code already
deduplicates immutable file pins inside `MixedImportSession._live`; do not add
that mechanism again. Its unchanged active callback repeatedly checks both
receipt issuers, which repeatedly reread the same persisted adoption record.
The call graph establishes amplification; the saved clocks do not attribute
an exact number of seconds to individual functions. No RAM experiment or cap
increase is justified. The full final-v5 goal is unchanged.

Select only fresh successors `software/v5/validation_phase/admission/trust.py`
and `admission/pin_phase.py`, based on current114 map995525c5. Core_growth owns
implementation; core_release independently reviews source; adaptive_audit owns
fresh `software/v5/validation_phase/controls.py`; root selectors/integration/Git.
Checkpoints share this canonical cycle directory. All used predecessors remain
immutable; current installation8e93486c is not modified.

## Contract

- Coalesce only persisted `TrustDomain._current` reads within the existing
  synchronous owner-only PP.phase. No caller, await, native worker, network or
  application callback may run inside it. Do not expand that existing boundary.
- Keep all original active callbacks, deadlines, CPU caps, exact classes,
  bindings/registration, source origins, handle identity and sticky denial checks.
  A cached observation is not mathematical acceptance or reusable authority.
- Key observations by exact live domain, retaining its immutable adoption
  generation/identity. A changed generation must not use a cached observation.
  Nested scopes have independent state. No cache survives successful or failed
  exit, nor resumes from a report or previous API operation.
- First use performs a full existing persisted read. Every successful phase must
  freshly reread every observed domain AFTER the original pin final sweep.
  Run the original active callback after each final read, within the scope, so
  finalization costs cannot pass an expired deadline/CPU cap unnoticed. Refuse
  newly encountered domains during finalization. Same-object withdrawal denies
  immediately even on a cache hit. A body/finalization failure never succeeds.
- This intentionally changes disk observation from every nested microguard to
  first-use/final phase boundaries under the already stated trusted stable local
  environment. It does not promise safety against hostile concurrent filesystem
  rollback, cancellation of running workers or revocation of prior returned data.
  Do not describe it as byte-for-byte identical observation timing.

## Focused evidence before integration

Use real temporary TrustDomain records and real `_read` in native-free tests;
issuer shells may test actual liveness without granting mathematical authority.
Count reads deterministically; cover repeated checks, independent scopes/domains,
withdrawal and sticky denial, changed adoption/identity, failed callbacks/body,
pin-sweep changes, final-read clock crossing and scope cleanup. Original pin
conflict/freshness behavior must remain. Do not rerun historical suites.

Root's draft `Select-ValidationPhase01.ps1` is preparation only. A reviewed exact
source map and finite launch decision are required before execution. No automatic
mirror retry or large package rebuild follows. Batch the already reviewed pair
planner with this repair if changed-boundary evidence supports integration.
