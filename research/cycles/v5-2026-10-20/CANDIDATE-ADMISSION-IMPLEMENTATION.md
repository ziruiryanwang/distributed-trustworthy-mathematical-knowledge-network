# Preserve useful work across a clean terminal-certificate refusal

2026-10-22, root. SOURCE IMPLEMENTATION ONLY; execution requires later selection.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

Root read actual selected I/A receive paths, client action/failure/admission/
staging paths and frozen supervisor166-303, plus independent cleanup challenge
`2d8ccfd815933ad94f34d6a3907432cac30c37c7b8a640be9018d8017d485ad4`.
The independent reviewer found no conceptual blocker. The design author's
source investigation agrees: isolate a new attempt before any staging/import,
not recover an already failed or revoked owner. Its detailed decision is a
supporting checkpoint, not authority to broaden this selection. Root now fully
read its final8da717a0 and adopts the five-file seam with the clarifications below.

## Invariant and API contract

An opt-in attempt may return NOT_ADMITTED only for the same invocation's natural
exit exactly1, empty stdout, no supervisor error, complete unforced cleanup,
independently checked final resource/log/output bounds, unchanged input bytes,
fresh original pins/trust and still-live original deadline. This is nonacceptance,
not a mathematical or cryptographic diagnosis. All reservations remain charged.
Old live registries stay unchanged by nonmutation, never copied/restored.

Every unsafe/uncertain result, changed authority, overrun, binding mismatch or
exception retains a fatal path. No exception-message classification, saved
report authority, implicit retry, new owner, renewed deadline or refund. Existing
strict receive/acquire/admit/stage APIs retain their contracts. Successful
acceptance still follows the existing full binding/handle-issuance path.

- Lower `try_receive` has the same arguments as `receive`: returns the actual
  live handle on success, or `None` only on the complete clean nonacceptance gate.
  Existing `receive` never gains a `None` result. A shared private execution body
  may avoid duplicated launch/binding logic; the opt-in branch precedes success
  binding, with no catch-and-resurrect path. Fatal opt-in exits revoke its owner.
- Public `try_admit_terminal_local`, `try_acquire_terminal`,
  `try_acquire_terminal_exact` expose a structured
  NOT_ADMITTED result or ADMITTED plus the ordinary live warrant. Calls are
  explicit and serialized under the same grant, before selecting a staged token.
  They support terminal-I and terminal-A only. Structurally valid mixed/native
  packets return `UNSUPPORTED_TRIAL_FORM` before any verifier, retaining only
  the already incurred transfer/input/custody charges.
- No new body acquisition, staged replacement, import rollback or automatic
  candidate policy. The agent chooses another variant explicitly. Accepted
  terminal evidence enters existing positive live caches so subsequent ordinary
  staging/import can reuse it without a duplicate verification. No negative cache
  or scan/copy of all previously accepted handles is required.

Clarification to8da717a0: the trial itself must never stage or import, but blanket
`_session is None`/empty `_staged` preconditions are not selected. The actual
terminal-verification path does not mutate either; preserving existing handles,
contexts and selections is the point of this change. Establish noninterference
from the writes, including on positive cache insertion. No selected staged
variant is replaced and no failed reader/client is revived; callers still must
choose how to use a positive warrant through existing import APIs. If authors
find a concrete unavoidable interaction, report it before weakening this
requirement or editing staging/import code. Keep the active client/owner guards.

## Exact fresh source scope and ownership

Base map129: `distribution-exact-packet-01-input.json`/`328c21bb...`.
Also select the tested custody successor e1e35cec at its existing logical key;
it is frozen and must not be edited. New source root `software/v5/candidate_admission/`:

- storage_outcome_audit: new `admission/clean_refusal.py`, successor
  `admission/verifier.py` from origin_phase32289cac, and successor
  `aggregate_claims/aggregate_admission.py` from trust_withdrawal2ef830f8.
  Own lower API/helper contract and concise source checkpoint. Check the complete
  predicates in2d8ccfd8, especially zero-length stdout, nonzero final resource
  checks, I's missing own-output census, post-subprocess pin-phase invalidation,
  and final deadline after all evidence I/O. Keep source-origin/pin requirements.
- storage_integration_adapter: successor `client/workspace_evidence.py` from
  exact_packet3f39d9b5, plus successor `client/managed_owner.py` solely updating
  its exact workspace pin after review. Own minimal public API/README and source
  map. No changes to staged/semantic-reader/atomic/native code are selected.
  Report other actual required explicit pins before expanding source scope.
- storage_launch_review: independent review of actual sources and later controls.
- root: focused controls, source-map/selectors, finite launches, adoption and Git.

This composes130 logical SDK sources (one helper added). Used predecessors stay
immutable; no old-state migration or installation patching. No release rebuild,
cryptographic proof generation or resource-heavy experiment is selected. A later
small real-I refusal/continuation check is justified only for this changed trust/
liveness boundary, not as another growth or global deployment demonstration.

## Pre-execution review refinement

The independent source reviewer found that inherited public action wrappers
finished with a blocking filesystem census and no subsequent liveness check.
Root selects two trial-only wrappers in the already assigned fresh facade:
same entry/fatal cleanup/finally semantics, then active/census/fresh active and
nonblocking original grant/owner deadline plus controller-CPU checks before
return. The three new trial methods use these wrappers; strict APIs and frozen
base files do not change. Tests must cover expiry during that final census.

The efficiency rationale is avoided loss of already checked work, not an
unconditional speedup: if clean-refusal probability is q, discarded-work cost
is W and extra clean-guard cost is H, expected local savings in a stated workload
require q E[W | clean refusal] > E[H]. This is a conditional accounting model,
not a measured claim, and excludes any separately chosen retry costs. The
source property is stronger than the cost claim: nonacceptance performs no
prior-registry/context/selection writes regardless of network size. Checking
this new attempt's bounded outputs does not scan all mathematical knowledge.
