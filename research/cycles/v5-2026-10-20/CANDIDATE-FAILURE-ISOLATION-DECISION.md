# Candidate-failure isolation: minimum implementation decision

2026-10-22. Author: `storage_integration_adapter`. **Source decision only; no implementation, execution or adoption.**

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

Add an explicit, opt-in **terminal-certificate trial before staging or importing**. A carefully settled unsuccessful verifier call may return `NOT_ADMITTED` normally, with no new warrant and without destroying earlier live warrants. The caller may then explicitly choose another candidate under the **same original owners, grant, counters and deadline**.

Do not catch ordinary admission exceptions and continue. Do not restore revoked owners. Do not add staged rollback, mixed/native transactions, automatic retries, implicit new grants or certificate-negative caching in this slice. Keep existing `receive`, `acquire`, `acquire_exact`, staged-reader and import failure semantics fail-closed.

This is a central availability improvement: an untrusted but structurally transferable bad receipt need not destroy unrelated verified work. It is not weaker mathematical acceptance or evidence that the rejected statement is false.

## Exact baseline and inspected boundaries

Use the actual129 SDK map `experiments/v5-local-checks/distribution-exact-packet-01-input.json`, SHA-256 `328c21bb585881d654f1a23f1704fbaa277ee865f7adb1250cf6c19b85647561`. The separately selected offer-enumeration custody successor `e1e35cecd8f40154a98e40cb1a5a2cca1d8c376966e57ef529c7c878bdd6c634` widens metadata count 8 to 64; it does not implement rejection recovery.

| Logical module | Selected source under `software/v5/` | Relevant behavior |
|---|---|---|
| `admission/verifier.py` | `origin_phase/admission/verifier.py` (`32289cac`) | I handle inserted only after successful process, exact output binding and final deadline checks, lines165-233. Ordinary failure does not itself blanket-revoke; outer client does. |
| `aggregate_claims/aggregate_admission.py` | `trust_withdrawal/aggregate_claims/aggregate_admission.py` (`2ef830f8`) | A handle inserted only at final success; any exception revokes all old handles/members, lines175-252. |
| `client/workspace_atomic.py` | `continuing_context/client/workspace_atomic.py` (`32e3b95e`) | Action wrappers fail the client on escaped exceptions, lines94-120. I admission/cache/accounting lines468-483. |
| `client/workspace_mixed.py` | `client/workspace_mixed.py` (`eb4e9374`) | Failure clears warrants/caches and closes original owners, lines245-259. A admission/cache/member selection lines310-342. |
| `client/workspace_evidence.py` | `exact_packet/client/workspace_evidence.py` (`3f39d9b5`) | Exact target binding lines433-469; offered/exact acquisition lines657-730. |
| `client/workspace_staged.py` | `exact_packet/client/workspace_staged.py` (`5d96c8cb`) | One staged packet per module; admission token is consumed before verification. |
| `client/semantic_reader.py` | `exact_packet/client/semantic_reader.py` (`253b0ffb`) | Escaped errors fail reader; closing a reader does not erase client staging. |
| `mixed_claims/receiver.py` | `incremental_native/mixed_claims/receiver.py` (`54365699`) | Nested claim handles/cache can change before overall mixed acceptance; entered failure revokes mixed owner. |
| `mixed_claims/imports_atomic.py` | `continuing_context/mixed_claims/imports_atomic.py` (`45b08286`) | Pure-data import session, not persistent native checker, but extending invalidates old view and sequential source insertion precedes final materialization. |

The selected pin helper is `standalone_validation/admission/pin_phase.py` (`ac7ed228`), not the older adjacent helper. Independent detailed process-predicate challenge is [CANDIDATE-REFUSAL-CLEANUP-CHALLENGE.md](CANDIDATE-REFUSAL-CLEANUP-CHALLENGE.md), SHA-256 `2d8ccfd815933ad94f34d6a3907432cac30c37c7b8a640be9018d8017d485ad4`; fully read for this decision.

## Exact proposed public behavior

Owner-level API: `try_receive` with the same arguments as existing `receive`. It returns an explicit outcome containing either the ordinary new live owner handle or `NOT_ADMITTED` without a handle. The outcome comes from that invocation, never from caller-supplied/saved reports. Share the existing positive checking body; do not create a second mathematical acceptance implementation.

Client-level APIs: `try_acquire_terminal` and `try_acquire_terminal_exact`. Their names explicitly limit scope. Keep existing candidate/entry, exact-journal expectation and receipt CPU/wall/memory arguments; omit optional body acquisition in this minimum. Successful result is `ADMITTED` plus the ordinary same-client warrant; unsuccessful result is `NOT_ADMITTED` without any warrant. The result identifies the attempted packet digest/size and is local operational data, not portable authority.

Preconditions: no import session (`_session is None`), no existing staged packet selection (if the staged subclass is used, its `_staged` must be empty), and the ordinary live candidate/owners/grant. Previously verified warrants may exist. This is a **pre-stage trial**, not recovery after `reader.finish` or `admit_staged` has failed.

Use the existing offered versus exact transfer distinction and exact custody readback. Structural packet inspection identifies the evidence form. A structurally valid `mixed` packet returns `UNSUPPORTED_TRIAL_FORM` before any verifier call; it does not silently fall back to destructive mixed admission. Transfer/input/custody charges remain. Malformed packets, missing offered membership, mismatched identities and corrupt custody are still errors, not ordinary rejection.

For terminal I/A, use the same summary, exact journal, policy, opening and member bindings as ordinary acquisition. A successful result must pass every existing final warrant/opening/journal check. A terminal-A trial must check member binding **before** entering the A verifier, as existing `admit_aggregate_member` does; it must not accept an invalid membership after a good aggregate receipt. Positive cache hits retain their existing live-owner/exact-byte validation and charges. A member selection failure after positive A verification remains fatal.

After one success, ordinary `import_context` can consume the returned warrant. A later staged/reader path may reuse positive receipt authority under existing cache rules, but current staging can transfer the packet again. Do not claim this slice removes that transfer or authorizes stage-cache changes. `NOT_ADMITTED` inserts no receipt/packet/aggregate cache entry.

## The narrow recoverable outcome

Use conservative **exit code exactly integer 1 plus actual empty stdout**. This is safe nonacceptance, not proof invalidity: a clean environmental refusal can also exit1. Crash codes and success-looking output followed by failure are outside this initial branch. No host-source interpretation of stderr is required.

All independent challenge conditions are mandatory, summarized here:

1. The actual in-memory process result belongs to this invocation and exact original argv/cwd/limits; schema/authority match. No report loading or exception-message classification.
2. `COMMAND_FAILED`, strict integer exit1, no `error` field, no service stop; ordinary stdout file is actually empty. The supervisor's `bounded_read` rejects empty files, so do not use that helper to test emptiness.
3. Direct child reaped, Job closed, no cleanup errors, no termination requested; final active/terminated counts both strict integer0 and a real observed Job with at least one total process.
4. Independently recheck finite/nonnegative final user/kernel/total CPU, total consistency, wall-through-cleanup, wrapper CPU, peak private commit and actual log lengths against the selected limits. Supervisor final reclassification is zero-success-only, so `COMMAND_FAILED` alone is insufficient. Observed memory bounds do not prove that no allocation was denied.
5. Exact input receipt/header reread; fresh ordinary own-output directory and bounded byte/entry census including request, process and refusal evidence. For I add the missing own-attempt census, e.g. `len(receipt)+1MiB` and32 entries; A already reserves/checks an analogous envelope. I's existing finite operation/input caps bound accumulated attempt envelopes; the client grant's existing aggregate output census still gates return. This is not a hard filesystem quota or a claim that I already reserves owner-level aggregate output bytes.
6. Fresh post-process original source/pin/trust/profile checks, no pin phase spanning the subprocess. Complete any final phase sweep before exposing a result. No prior registry reconstruction.
7. All reservation charges remain; original effective call/owner/client deadlines and controller bounds hold after **all** possibly blocking evidence, census and validation work. No late I/O after final guards. Final client action-wrapper validation remains mandatory and can still fail the whole operation.

An observed overrun, timeout, forced termination, supervisor error, uncertainty, input/output drift, trust withdrawal, source drift, expired deadline or cancellation is fatal. The branch makes no claim about the *cause* of a clean nonacceptance. Known unsafe resource/cleanup states cannot be mislabeled as ordinary misses.

## Minimal source scope: four replacements plus one helper, no new runtime

Root proposes the tighter facade-only scope below, under `software/v5/candidate_admission/`. It is sufficient if the facade shares its terminal helper between ordinary and trial paths, rather than implementing two different positive authority/accounting paths. Select fresh successors only; predecessor bytes are used/frozen.

1. **New `admission/clean_refusal.py`:** one shared nonauthoritative clean-refusal predicate/output checker for the two real owners, with strict origin/symbol/source pins. It consumes only the direct same-call invocation result, never saved reports. This helper does not issue handles or recreate owners.
2. **`admission/verifier.py`:** shared private verification implementation for old `receive` and new opt-in `try_receive`; narrowly constructed clean-nonacceptance path through the helper; same positive binding; missing I own-attempt output census. No new public constructor/configuration scope.
3. **`aggregate_claims/aggregate_admission.py`:** matching opt-in path through the same helper. A's normal clean-nonacceptance return must happen **inside** its operation before the existing revocation catch. All escaped exceptions still revoke. No member creation on nonacceptance.
4. **`client/workspace_evidence.py`:** two explicit terminal-trial APIs and private I/A admission helpers; route both ordinary terminal and trial terminal admission through these helpers. Override ordinary direct `admit_receipt`/`admit_aggregate_member` in this facade if necessary so the selected evidence client has one positive cache/accounting/member path. Port the narrow predecessor rules exactly; the old atomic/mixed base files stay frozen. Keep pre-stage guards, no trial bodies, explicit unsupported mixed outcome, and all positive exact-journal/final opening checks. Do not weaken `_action`/`_async_action` globally or change mixed packet/native verification.
5. **`client/managed_owner.py`:** update only the embedded selected `workspace_evidence.py` source pin required by managed composition. The selected SDK map/support/writer identity must be regenerated by root; no old managed-state identity reuse.

No changes to hosts, cryptographic images, supervisor, wire protocol, transport, storage schema, `workspace_atomic`, `workspace_mixed`, `workspace_staged`, `semantic_reader`, mixed verifier or import session are selected by this recommendation. Runtime owner construction signatures need not change. Root owns final source-map selection, implementation authorization and deployment/test allocations.

## Preservation argument and bounded controls

Let `H` be the old authority registries, `L` the live original-owner invariant, and `U` the monotone resource ledger. The normal-return nonacceptance branch must establish:

`(H,L,U) -> (H,L,U + charged_attempt, NOT_ADMITTED)`.

Establish `H'=H` by branch non-mutation before any new handle/cache/import publication, not copying or scanning all old handles. The only lasting changes are charged counters and ordinary untrusted custody/evidence. No new derivation was admitted, so earlier derivations remain warranted under the same still-live profile. For success, use the unchanged acceptance relation; for any failed final guard, retain existing revocation/poisoning semantics. This relies on the existing trusted owner process/OS/filesystem model; Windows Jobs are not a hostile-code security sandbox.

Small source/control obligations, not a new broad campaign:

- Preserve one prior genuine/live warrant, cleanly refuse a terminal candidate, then explicitly accept a valid alternative and use both positive warrants. Same owners/grant/deadline; no refunded counters. Separate focused I/A controls exercise each issuer branch without rerunning all crypto tests.
- Exact-journal mismatch, invalid A membership, bad opening, malformed packet, changed custody and final client-census failure remain fatal, even after a child completed cleanly.
- Table-driven predicate negatives cover each independent challenge clause, especially bool exit values, crash exit, nonempty stdout, final-only CPU/log/wall overrun, no Job, errors, killed descendants, input/pin/trust drift and late evidence I/O.
- Old APIs retain fail-stop behavior; unsupported mixed trial calls no verifier; trial after staging/import is refused; no stage rollback/revival exists.
- Existing positive cache hits remain exact/live; rejected candidates create no positive or negative authority cache; fresh alternatives consume remaining original budget.

The already available fallback is an explicit fresh operation after a **clean** close and a new grant. It loses old live handles/context and may repeat verification; an uncertain workspace cannot reopen. This remains distinct from the proposed in-operation trial and is not a hidden retry policy.

This decision closes the source-design question sufficiently to select a bounded implementation. It does not establish runtime qualification, general candidate isolation, broad adversarial isolation or final-v5 completion.
