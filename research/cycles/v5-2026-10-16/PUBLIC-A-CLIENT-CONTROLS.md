# Public aggregate client: focused control source

Author checkpoint, 2026-10-16. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Status: **source authored and statically checked; NOT RUN**. No Python import,
syntax compilation, test, native process, proof, build or network operation was
performed by this assignment. Root owns source adoption and any later finite
launch. Independent review is still required. Full v5 is not completed by these
controls.

## Selected boundary

Selection: `PUBLIC-A-CLIENT-SELECTION.md`; design: `PUBLIC-A-CLIENT-SEAM.md`.
The new public client makes the existing aggregate member authority reachable
through the same operation-local workflow as optional I and mixed-delta
admission. These controls distinguish the new integration contracts without
repeating the completed cold I or atomic-import suites.

The decisive invariants are:

- Only the selected A owner, optional I owner and their exact mixed verifier
  compose the client. Persistent configuration selects the mixed profile;
  neither a saved report nor a foreign live warrant substitutes for an owner.
- One acquisition allowance bounds all direct A, I and mixed admissions.
  Issuer suballocations do not mint additional client allowance.
- A receipt cache is local to one live owner/profile and binds exact receipt
  digest, length and header. Member selection still binds exact journal,
  index and ordered membership path on every call.
- Failure revokes the client and closes the originally transferred issuers,
  including when public owner attributes have been replaced. A later successful
  close does not erase a prior cleanup uncertainty.
- An aggregate member dispatches to the existing atomic import seam; standalone
  aggregate custody is not silently presented as a mixed delta packet.

## Exact candidate bytes

All paths in this table are relative to the canonical root. Hashes are SHA-256.

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/client/test_workspace_mixed.py` | 29,962 | `478de57908ebffc98093f0139f83e0a06a9609383f237cec4466086736eb0c3e` |
| `software/v5/client/mixed_control_owner.py` | 1,323 | `02b06e69237ad6da091ea9368992cc3ee6286fcaab27a187ce6db56be6283c80` |
| Reviewed product `software/v5/client/workspace_mixed.py` | 31,054 | `eb4e9374707b3e3f03b7e60ad91fd0fd30a3872d3e9fb59fe3f93c039338acbd` |

The frozen inherited atomic client is unchanged. These hashes describe the
source reviewed here, not an execution or mathematical acceptance result.

## Sixteen selected controls

`mixed_control_owner.main(context)` executes exactly `SELECTED` in this order.
Each method has a short `cNN` evidence directory so Windows path length does not
depend on prose method names. All fixture directories remain below
`context.location_workspace/mixed-controls`; no temporary directory elsewhere
and no old test helper are used.

| # | Method suffix after `test_` | Distinguishing assertion |
|---:|---|---|
| 1 | `required_A_optional_I_and_persistent_profile` | A-only and I+A construct exact mixed storage; old workspace schema is refused. |
| 2 | `wrong_owner_image_pairing_and_missing_A_refuse_before_transfer` | Missing A, wrong image, wrong identity pairing and unselected I refuse before ownership transfer or verifier invocation. |
| 3 | `pristine_A_and_original_suballocations_are_required` | Used A member accounting, oversized CPU/member storage, late owner deadline and missing required source pin refuse before transfer. |
| 4 | `same_live_receipt_two_members_normalizes_exact_facts` | One receipt submission supports two exact members; repeated exact membership returns the issuer-local member token; all byte-valued fact fields normalize correctly. |
| 5 | `receipt_cache_binds_exact_header_and_receipt_bytes` | Changed header or receipt bytes cannot reuse the prior aggregate admission. |
| 6 | `wrong_member_path_cannot_hit_receipt_cache_and_fail_closes_owners` | Invalid path is rejected before another receipt submission; all transferred owners close and local warrants/caches disappear. |
| 7 | `direct_A_mixed_and_I_share_one_admission_budget` | Direct A reserves 10 CPU units; one-claim/one-delta mixed admission reserves 20; subsequent I cannot exceed the common 30-unit allowance and never reaches synthetic receive. Mixed packet semantics use the selected A image. |
| 8 | `missing_I_owner_has_no_fallback` | Direct I admission without an I owner refuses, closes A and does not reinterpret I as A. |
| 9 | `cache_cannot_survive_owner_profile_change` | Changed issuer profile revokes the client before a cache can hide it. |
| 10 | `substitution_closes_original_owners_not_untransferred_replacement` | Separate receipt/A/delta/preparation attribute substitutions close the original four owners; original A handles, members and cache are empty; original member no longer describes; replacement is never closed; report still reflects original accounting. |
| 11 | `failed_cleanup_remains_uncertain_after_later_successful_close` | Injected first A close failure remains `CLEANUP_INCOMPLETE` after the second close succeeds; workspace remains poisoned and cannot issue another grant. |
| 12 | `foreign_warrant_refuses_without_reusing_foreign_authority` | Another client's token causes local refusal without closing or borrowing the foreign authority. |
| 13 | `closed_or_expired_A_issuer_revokes_cached_warrant` | Cached warrant does not outlive a closed or expired A issuer. |
| 14 | `A_member_import_dispatch_uses_same_three_owners` | Exact selected member token/receipt and the same I/A/delta owners reach the import seam; this uses an explicit routing stub, not semantic materialization. |
| 15 | `orderly_close_and_reopen_restore_no_A_authority` | Closure revokes tokens; SQLite reopening restores only untrusted records; a fresh client rejects the old token. This is not a cold genuine-I or genuine-A gate. |
| 16 | `standalone_A_is_not_silently_a_mixed_packet` | Removing the required child delta from a structurally valid mixed packet is refused by actual custody/parser before verifier work. |

## Real versus synthetic components

Real production code exercised if selected: the new workspace/client, inherited
operation grants and serialized entry points, real SQLite storage, shared
`AcquisitionBudget`, packet structural parsing, exact aggregate header/member
bindings, aggregate member registry/cache/descriptions/revocation, client fact
normalization, profile/source-origin checks, report persistence and closure.

`SyntheticOwners` deliberately allocates exact issuer classes with `__new__`
without calling their production constructors. Native receive, installation
validation and issuer active checks are replaced in the fixture. Exact classes
permit testing the actual public constructor's identity/suballocation logic;
they do not simulate or establish an authentic installed owner. Client-side
origin, profile, resource and lifetime checks are not patched.

The A fixture retains actual pure `select_member`, `describe_aggregate`,
`describe_member`, report and close methods. Its fake receive directly creates
`VerifiedAggregate` and records fabricated receipt data. The I fixture likewise
fabricates `VerifiedModule`; the mixed fixture parses real packet structure but
fabricates `VerifiedMixedDelta` and records an empty verified-frontier list. It
therefore does not test mixed receipt discharge or native mathematical checking.
Synthetic receives record their calls but do not independently implement the
production issuers' whole admission validation or resource enforcement.

The optional preparation fixture is an inert exact-class object used only to
test ownership/suballocation/cleanup. Control 14 replaces `MixedImportSession`
with an explicit inert routing stub. No imported declaration is materialized,
no Lean process runs and no authoring or proof output is produced.

The test image is the inert value `7a` repeated 32 times. Receipt and foundation
bytes explicitly say `SYNTHETIC`. Structurally valid journal/member commitments
do not make these receipts authentic. All claimed verifier/proof/native counts
in the control report are zero. A later genuine A gate remains necessary.

## Source closure and execution prerequisites

The owner imports only stdlib `json`, `unittest` and the selected new test module.
The test's direct non-stdlib imports are:

```text
admission.verifier
aggregate_claims.bindings
aggregate_claims.aggregate_admission
client.workspace_atomic
client.workspace_mixed
delta_claims.claims
mixed_claims.authoring_atomic
mixed_claims.packet
mixed_claims.receiver
mixed_network.custody
modules.codec
```

Transitive production imports and package initializers must come from the same
prospectively reviewed selected source snapshot. In particular, do not copy
only these direct imports or allow an unselected working-directory helper on
`sys.path`. Root's existing mixed/atomic/network closure selection can supply
that closure; this checkpoint does not authorize loading an older test suite.

Each fixture computes current source hashes only for the six explicitly
required client origin pins: `client/__init__.py`, `client/workspace_atomic.py`,
`client/workspace_mixed.py`, `mixed_network/__init__.py`,
`mixed_network/custody.py`, `mixed_network/transport.py`. This serves the real
client origin checks within synthetic owners. It is not a replacement for the
outer launcher's exact source manifest or actual issuers' larger installation
and runtime pin requirements.

There are 29 physical workspace fixtures, 30 operation grants, and one additional
reopening of an existing workspace; all counts are prospective source-derived
counts, not measured output. Each fixture sets finite storage and grant bounds.
The launcher must independently bound aggregate CPU, wall time, process/memory,
output entries and output bytes for the whole suite, not multiply grants into
new outer authority. The maximum fixture grant output allowance is 128 MiB,
but these controls create no verifier command output. Source quotas are not a
measured total or a proof of sufficient outer allocation.

Expected result file is `mixed-controls/RESULT.json`, with selected names,
tests/errors/failures/skips and explicit synthetic scope. Raw unittest output,
outer resource/cleanup evidence and preserved databases remain available for
independent outcome review. A pass may qualify these changed-boundary controls
only; it cannot be promoted into genuine aggregate acceptance, real semantic
import, growth advantage, network performance or full v5 release readiness.

No prior used source, test evidence, installation, Git index or allocation was
changed by this assignment.
