# From a local fragment to a funded certified cut

2026-10-06. Independent read-only installed-source investigation; no product
import, proof/checker/compiler execution, network action or funding commitment.
This identifies a concrete existing path, not a new completed certificate. Full
v4 remains unaccepted. Root owns any new finite operation selection.

## Finding

The compact `seal-request` command is only an owner-selected handoff record.
It cannot seal. However, the already extracted full installation at
`product-local/v4-operator-integration-01/commons-v4` contains an actual compatible
V5 contributor, the adopted guest/prover, `prepare-seal`, finite `advance`, final
cold receipt verification and final bundle export. No new trusted service or
central server is needed: any suitably provisioned holder can own this operation.
The full installation is separate from the compact download and is expensive to
adopt; that cost must not disappear from the growth comparison.

| Installed control | Independently read SHA-256 |
|---|---|
| RELEASE-MANIFEST.json | cd25b9b2b671c3901bf42402fd5be11923bb6db13f032c068f6e315c07f990d1 |
| contributor/profile.json | 298d790ec380f50ca45307069fd577908131a0622e57a3aa455813268213bfc7 |
| operator/commons_run.py | 298e89cb5955437fa16cd4bcd2bf1a382f583096b142a0bedde100ee1f9dbaee |
| contributor/cert_workflow.py | e2583d49e11aada754f2a649942ed6561ca19483ef234cfde2f2d709991814a4 |
| contributor/cert_fragments.py | 6e31235baeddaf026f4944c3479f375514a62909953179cf50bbb9bee6df5ae4 |
| contributor/cert_stages.py | 66b3d7a0f2a1542a313cd1daffec008627c89c9a734a35dba83731c790f6dc82 |

These are byte identifications of the retained installation, not a recommendation
to trust a digest received from an arbitrary peer. Adopt the release independently.

## Why current inert/native-fast fragments are source-compatible

The full profile is `DMKN_INSTALLED_CERTIFIED_PROFILE_V5`, profile ID
`dmkn-experimental-certified-definitions-01`, image
`5275d4fb567412d65ec0a9a01fa2fc2e5b12e1825a4ea247ab79880ef153b80a`, foundation
`4eeaab61471a4ab9f93209af9aad66fcb45f6322783b919851d4d95ea33f9f80`.
These mathematical identities match the current native-local lane. The profile
file digest differs because the native-local installation has different executable
roles/assets; profiles themselves are not copied into a received fragment.

Both use `DMKN_BOUNDED_PROOF_FRAGMENT_V1`. The wire consists of exact input,
journal, capsule and certified frontier bundles plus their strict manifest. The
sender's local assurance, backend, executable pin and null/VM segment count are
NOT transferable wire authority. The old full loader therefore does not need to
understand a native-local state record: it loads the inert proof and checks it
again under its own selected guest. Native checking does not enlarge the guest's
language or capacity. An expensive native-valid fragment may still exceed the
sealer's cycle/memory/bytes budget and be refused.

The loader enforces the exact tree, aggregate16MiB bound, fixed mathematical
policy, exact packet/capsule correspondence, at most8 certified interfaces,
rank descent and complete header/frontier equality. `prepare-seal` then enforces
the owner's expected fragment-manifest SHA and expected interface identity. A
structural load is not mathematical acceptance. Every distinct final frontier
receipt is actually verified against its exact full journal.

## The existing state transition, not a stub

1. An owner has durable exact fragment custody and independently adopts the full
   sealer installation. A transport peer or seal-request does not supply authority.
2. A fresh `prepare-seal` operation snapshots those bytes, verifies every actual
   frontier and executes the selected guest once to capture `snapshot.bin`.
   There is no duplicate standalone execute/export pass. The resulting state
   records actual segment/assumption shape and has status READY, not COMPLETE.
3. Explicit finite `advance` invocations consume that SAME operation's original
   allowance/deadline. For n segments and a assumptions, the exact plan is
   segment+lift for each segment, join for segments1..n-1, resolve for each
   assumption, finish, and cold verify: `3*n + a + 1` stages, at most393 under
   n<=128 and a<=8. Dependencies and bytes are rebound on continuation.
4. The final invocation must actually cold-verify the finished receipt and close
   its workers. Only then does `finalize_bundle` require `last_verified=True`,
   bind the singleton capsule/journal and commit the transferable bundle.
5. A downstream holder independently verifies that bundle before adopting it
   as a certified premise. The certificate can replace proof replay behind this
   new cut; it does not erase demanded statement/definition data.

The source requires final verification in the actual completing invocation;
a persisted boolean from a prior process is insufficient. Failed, incomplete,
interrupted or uncertain operations are not automatically resumable. A clean
READY prefix is the authorized continuation case; COMPLETE is terminal.

## Concrete public invocation contract

Use this installation's bundled
`contributor/runtime/python/python.exe -I -S -B` to invoke
`operator/commons_run.py`, not the compact `operator/commons.py`. The full launcher
authenticates its release/profile and only exposes fixed workflow targets. It
injects the adopted profile and profile digest into the child; the owner does
not supply a peer-selected profile override.

Every call takes this common outer syntax (placeholders require explicit owner
choices; this document does not select a run):

```text
operator/commons_run.py
  --manifest ABS_FULL_RELEASE/RELEASE-MANIFEST.json
  --manifest-sha256 ADOPTED_FULL_RELEASE_SHA
  --target workflow --evidence ABS_FRESH_EVIDENCE
  --cpu-seconds OUTER_CPU --wall-seconds OUTER_WALL
  --memory-mib OUTER_MEMORY --active-processes OUTER_PROCESSES
  --stdout-bytes LOG_BOUND --stderr-bytes LOG_BOUND
  -- CHILD_ACTION_AND_ARGUMENTS
```

Preparation child arguments:

```text
prepare-seal --run ABS_FRESH_OPERATION --fragment ABS_HELD_FRAGMENT
  --expected-manifest-sha256 EXACT_FRAGMENT_MANIFEST_SHA
  --expected-interface EXACT_FORMAL_INTERFACE_ID
  --cpu-budget-seconds OPERATION_ALLOWANCE --deadline-utc FINITE_UTC_DEADLINE
```

Continuation child arguments, with a NEW outer evidence directory each time:

```text
advance --run ABS_EXISTING_READY_OPERATION --max-new-stages FINITE_COUNT
```

`advance` deliberately accepts no new operation budget/deadline. An operator must
inspect the previous closed record, stage progress and remaining reserves before
calling it. The outer exit marker means clean command closure, not mathematical
success; read the actual child status and final receipt verification evidence.
Do not move/copy a partial operation to simulate a new allowance or silently
reset a failed campaign. Root must separately select any new campaign.

## Funding and costs that cannot be hidden

The installed full profile has operation CPU ceiling120000seconds, invocation
controller charge600seconds, invocation wall7200seconds, operation deadline at
most86400seconds ahead,4GiB memory,8active processes,12GiB working-byte ceiling,
8192entries, guest2^26cycles and segment exponent19. Ordinary proof-stage worker
CPU reserve is1800seconds; finish/verify reserve300seconds. Each stage reserves
600seconds of deadline room, irrespective of hoped-for fast completion.

These are caps/reservations, NOT a claim that a typical seal consumes those CPU
amounts or succeeds under them. The product records measured workers separately
from conservative charges. Outer inclusive Job CPU includes the inner controller
and workers; do not add its nested worker figures again. The disjoint outer
wrapper CPU is an additional cost. Full adoption, snapshot, all proof stages,
failed attempts, final verify, distribution and custody belong in a seal quote.

The implementation checks `charged + next_worker_reserve <= operation_allowance`
and enough deadline remains BEFORE starting a stage. A reserve stop in advance
can return READY with no new stage. Blindly calling advance again does not obtain
funding: it consumes another600second controller charge without progress. Stop
on no progress/insufficient original reserve and make a deliberate new decision;
do not claim liveness from repeated successful CLI exits. Choosing too small a
preparation allowance can leave a useful snapshot that cannot economically finish.

There is no enforced global payer market, shared escrow, automatic subsidy or
cross-owner CPU transfer. In the current operable route, the sealer's actual owner
funds local execution and custody from resources it controls. Multiple independent
owners can do so without a central authority, but willingness and future capacity
are positive operating assumptions, not consequences of theorem truth.

## What has actually passed, and what remains conditional

`experiments/certified-seal-01/SEAL-OUTCOME.md` independently audits one genuine
source-free prepare-seal on the original first fragment. Exact child bytes,
genuine parent verification and snapshot passed. It had n=41,a=1, READY,
zero completed proof stages and no final bundle. Whole Job17.625seconds and
disjoint controller0.484375seconds were reported; conservative operation charge
601.96875seconds. This is preparation evidence, not a full new seal or a typical
economics calibration.

Current native-fast fragments have source-level compatibility through unchanged
inert wire and mathematical policy. This note does not add an executed
native-fast-to-completed-seal case. The existing final stages supply a concrete
mechanism; successful capacity/economics for any newly selected artifact still
require justified bounds or actual outcome. Prior genuine certificates remain
real evidence, not a license to mark every future seal successful.

## Consequence for sustained growth

The recurrent-cut model in rollover-policy-01/THEORY.md requires funded,
successful cuts before unsealed replay reaches its cap. This full path identifies
who executes that requirement and what software steps do it. It does not prove
that every chain or workload can pay. If its next seal is unfunded, incompatible
or cannot fit, the honest result is defer/refuse, not unlimited ancestral replay
and not a fictitious certificate. Native local speed improves the rent term;
it neither zeroes the buy term nor measures guest segments.

A future compact source-free sealer could remove full-authoring adoption overhead
without changing the relation. That is a separate consequential engineering
selection; no need to launch another expensive proof solely to describe this
already present path. Do not call the compact request stub a completed integration
or conceal the separate full installation from a deployability claim.
