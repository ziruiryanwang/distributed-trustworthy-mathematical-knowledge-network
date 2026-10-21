# Independent exact-custody integration source review

2026-10-20, core_release. Read-only source review of root's transport, facade,
reader and builder changes, plus the capability helper's integration paths.
No code imports, parsing, tests, native runs, network, build, installation or
Git operations. Runtime and adoption remain root's separate decisions.

**GO by source for the root-owned four-source boundary and corrected helper.**
The concrete lifecycle finding below is corrected in the final helper identity
recorded in its disposition. No execution, full v5 or mathematical qualification
follows this source review.

## Exact reviewed root sources

Paths relative to `software/v5/body_location/`:

| File | SHA-256 |
|---|---|
| `transport/acquisition_resilience.py` | `0dc12c02a5e8e8b2d4add4b32c030d036e94459260f58878f731a9e7e59f577e` |
| `client/workspace_evidence.py` | `fa636e2c75c9cd599732d7cb1e5a8fd8b2c5d42afc05e64ab6e67edbee92ff99` |
| `client/semantic_reader.py` | `17a3da541ac6f55914e4f4aee1da140dbc2b4cf1b96139bd34bb16503b950383` |
| `distribution.py` | `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813` |

The helper initially reviewed was `body_custody.py` at
`a780be385fe32841bbe5b7da3c24db6487e8fc99f3df47f8dcc9ca8f5c0c1ead`;
its separately authored response to the lifecycle finding is not silently
covered by that identity. The release/provider eight-source boundary has its
own independent `EXACT-CUSTODY-ROUTING-REVIEW.md`.

## Same-owner transport and settlement

The refactor factors existing contact capture into `_owners` and `_capture`.
The ordinary binder still requires an exact accepted private contact class,
identity in both original maps, the original budget and original egress policy.
It adds only the genuine `client.located_queries._Contact`, not arbitrary
subclasses. This corrects the previously recorded genuine-contact rejection.

The new binder accepts only the exact pool-issued `_BodyAttempt`. Its private
membership, active attempt state, context and endpoint identity are checked;
no callback is passed through a public API. It does not add Q to original index,
search or acquisition contacts. Both binders use `_attempt_body`, including
the same HTTP framing, commitment validation, original outer and structural
accounting, and fatal malformed-data/uncertain-cleanup behavior.

The actual selected declaration helper imports this transport's `_binding` and
`_unchanged`. Their signatures/captured fields remain compatible; an ordinary
declaration bound has no `attempt` key, so it retains the ordinary branch and
gains the exact located-contact correction without new body-token authority.

Token selection precedes `AcquisitionBudget.begin`; facade `finally` spends it
on every exit. If `begin` refuses, no nonexistent ticket is settled. After a
successful begin, the shared engine's `finally` settles even if the structural
gate or subsequent validation fails. Structural reservations decrement only
when entered. The existing grant may refuse before begin; local hint expiry is
checked after begin and again at endpoint validation, so it cannot dial without
its ordinary charged reservation. A normal404/503 consumes the token and
retains staged mathematics. No replacement allowance or automatic retry exists.

## Facade, reader and source origins

The facade initializes optional pool identities before inherited dynamic
liveness/reporting use, then checks exact origin identity. Its new methods use
the existing serialized action decorators, existing byte charge, original
grant and selected owner source pins. Required pins are taken from the actual
mathematical owners and compared for agreement, never freshly invented by
hashing arbitrary code.

Local imports of `semantic_reader` and `located_queries` occur after workspace
construction, avoiding their reverse import through `workspace_validated`.
The helper's top-level imports do not import the final validated client; its
exact-class imports are delayed until reserve/demand operations. The builder
requires the new helper and shared attempt source. Runtime preparation already
collects the selected SDK source map into owner pins. No new runtime artifact
or cryptographic build is required by this source change.

Each new reader operation uses one existing `_call` and one facade action. The
same pending demand, original candidate/descriptor, selected member, query and
acquisition identities are checked. The capability path does not call or relax
`_selected_supplier`. Successful returned data is committed and read back only
outside recoverable transport handling, then staged in the same reader. Failed
reader steps/close remove its capabilities; successful staging removes tokens
for the now-fulfilled body during prune. Query retirement is detected through
the retained original search/acquisition identities and closed generation.

The builder extends explicit `serve-advertised` schema selection to V3 while
retaining V1/V2 and the original installed-root injection. Selected SDK map
identity, exact file copying, immutable install paths and launcher checks stay
unchanged. The provider itself owns the exact new V3 field validation.

## Capability lifecycle finding and disposition

The initial helper checked `channel_failed` and client cleanup uncertainty but
not an already-known nonzero child return code or `forced_termination`. Thus a
hint could remain usable despite a known unexpected locator death. This is
different from the explicitly permitted clean locator-only expiry.

The helper author added those failure checks and prune invalidation in source
`ce5916d173df3b9f3e5abe7a63b3774594a4a5e7d5caf0f34a77ea1b8809af08`.
One related precise case remains requested: `_close_core` can fail during its
final origin/source-pin verification after the child returned0, without setting
those flags. A nonnull close task must be known completed, uncancelled and
successful before it can justify continued hint use; pending/failed/cancelled
cleanup must not count as clean. This is a read-only state check, not a fresh
health/network operation.

Final disposition: reread helper
`d4ad056417996b37b50463037a72217a4dbca8aedab18d18c8c5b0a24d23e89c`.
Its shared `_uncertain_channel` checks flags, known returncode and the existing
close task without awaiting or restarting it. Pending/cancelled/exceptional
close state invalidates in both pool.check and demand pruning; completed clean
cleanup remains permitted. The two concrete cases are resolved by source.
No remaining changed-boundary source blocker identified; targeted controls
still must check actual implementation behavior.

Expired issued entries may be retained as bounded inert tombstones so attempted
consumption still follows the agreed begin-before-predial-expiry accounting.
They are not usable live hints; the helper now separately reports unexpired
issued hints. Cumulative issuance limits cap tombstone retention. This does
not renew expiration or permit a second attempt.

## Required focused evidence

Controls should exercise genuine exact located contacts for both body and
declaration; unknown/cross-reader/changed-demand/reused tokens; before/after-begin
expiry and capacity refusal; clean404/503 versus corrupt200 and uncertain
cleanup; unchanged contact maps and mathematical staging; V3 readback failure
before service; shared two-role counters/IPC; and the lifecycle correction.
No broad rerun or proof campaign is needed for these changed source boundaries.
