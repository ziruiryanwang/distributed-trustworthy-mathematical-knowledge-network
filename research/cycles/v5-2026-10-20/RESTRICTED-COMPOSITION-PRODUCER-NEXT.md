# RC production: minimum ordinary-owner and receiver seam

2026-10-21, core_release. Source-only trace. No used file, installation, trust
policy or state was changed; no build, runtime or proof was launched. This note
does not select those operations. Root owns the current RC native build work.

## Consequential conclusion

**The receiver is mostly reusable; the missing producer seam is larger than
two build-adoption overrides, but does not require a new proving scheduler.**

Use the existing finite aggregate stage scheduler and the installed terminal-A
receipt/member/import path. Add RC-specific pure preparation, actual-build/image
adoption and a narrow snapshot-owner successor. Do not alter mixed-delta packet
semantics, replay ancestor proofs, build another receiver or copy a distribution
before the RC lane has a worthwhile same-target execution result.

The authoritative installed source map is `sdk_sources` in
`experiments/v5-local-checks/distribution-terminal-i-01-input.json`, SHA
`d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`.
It contains114logical files. It includes ordinary `production/producer.py`, but
**does not include** aggregate_small, aggregate_lifecycle or prover_memory
producer packages. Those are source-side facilities, not already shipped public
aggregate-production APIs. The current SDK can consume terminal A members;
changing its aggregate image alone cannot turn its I producer into RC production.

## Existing seams and exact incompatibilities

| Existing source | Reusable mechanism | Actual RC obstruction |
|---|---|---|
| `aggregate_small/producer.py` | Exact stage graph, finite allowances, inherited charges, checkpoint custody, resolved receipt finish | `_adopt_host_build` hardcodes old one-link schemas/source sets/names; `_adopt_image` hardcodes proof-memo four-crate build/assembly schemas |
| `aggregate_lifecycle/producer.py` | Ordinary prepare/snapshot/request/preflight/run lifecycle with composite profile identity | `prepare` calls old `prepare_mixed_seal`; constructor/source closure and `_snapshot` bind the old snapshot module |
| `aggregate_lifecycle/snapshot.py` | Exact staging, bounded native invocation, actual capsule/session adoption, cleanup | `_config` reparses an old mixed packet; `execute` requires exact old PreparedSeal type; `adopt` recomputes using the same old parser |
| `aggregate_claims/prepare_mixed.py` | Backward target closure, expected J/H/member opening calculation | Calls mixed packet parser and old aggregate encoder |
| `aggregate_claims/input.py` | Counts/claim/frontier/membership checks and binary record layout | Emits `DMKNAI02`/version2 and accepts old ordinary witness payloads, not selected RC framing |
| `prover_memory/producer.py` and `adoption.py` | Example of a narrow explicit adoption successor with whole-runtime source pins | Stage-only override; exact five-step allocation-build schema/SOURCE digest and preserved old aggregate image, not a generic RC adoption facility |
| `aggregate_geometry/layout_owner.py` | Snapshot-only owner without proof dispatch | Still aliases old image adoption, old prepare function and its own geometry build; not a drop-in RC producer |

In particular, subclassing LifecycleProducer and overriding only
`_adopt_host_build`/`_adopt_image` would still reject RC preparation inside
`snapshot._config`. Monkey-patching its imported parser or rewriting retained
reports into old schemas would bypass the intended source/profile boundary.

## Small concrete source addition

If the root selects public RC production after the economics gate, add the
following small source family under `software/v5/restricted_composition/`.
These are proposed files/contracts, not existing implementation claims.

| Fresh file | Minimum responsibility |
|---|---|
| `__init__.py` | Export the selected producer/preparation API only |
| `prepare.py` | Pure bounded RC submission parser, `DMKNRC01` encoder, exact target closure/J/H/member preparation; no native or receipt calls |
| `adoption.py` | Adopt actual RC snapshot/stage build records and actual guest-build/image assembly records; exact roles, source/library edges, finalization and image bindings |
| `producer.py` | RC composite profile and ordinary owner; subclass retained AggregateProducer for stage scheduling; use new preparation/snapshot/adoption paths |
| `snapshot.py` | Narrow successor of lifecycle snapshot, replacing packet/type/config/result schemas and recomputation with RC preparation; retain actual capsule/receipt/session checks |
| `operator.py` | Small owner-facing entry for prepare/preflight/snapshot/run; one explicit finite request, not automatic proof funding or retries |

Keep `AggregateProducer` unchanged and pinned. The new owner can reuse its
stage methods through inheritance, preserving its exact two-file source pins
and base profile, while its outer composite profile binds all new source files.
Model this on lifecycle's composite identity: request/allowance continuation
must use the same full profile identity. Override the adoption and snapshot
methods intentionally; do not expose caller-controlled verifier callbacks.
Use a fresh `DMKN_RC_PRODUCER_PROFILE_V1` wrapper and fresh RC snapshot schemas;
the actual stage-request grammar need not change if its session fields remain
exactly the existing image/wire/header/capsule/parent bindings.

The package/source installation must contain the inherited aggregate_small and
production closure plus the new RC closure and required shared codecs/bindings.
This is a selected add-on or later distribution addition, not an edit to the
current immutable114-file installation. An initially separate producer entry
can emit an ordinary terminal packet for the already installed SDK. Folding
every action into CommonsClient is not required to establish that working path.

## Pure preparation contract

Take an explicit bounded submission with receipt claim table, frontier member
openings, topologically ordered six-field RC deltas and one exact target J.
Use a new submission schema, such as `DMKN_RC_SUBMISSION_V1`. Do not send these
uncertified RC frames through the old mixed-delta parser or label them native
I receipts. No network task list or human-intention field is involved.

Preparation must:

1. Accept only genuine-claim *slots*: tag0 fixed-I J, or tag1 H for the selected
   same RC aggregate image. Receipt bytes here remain untrusted pending witnesses;
   their actual application verification belongs to the host/guest path.
2. Enforce exact fixed-I semantic image/F/P, ordinary theorem descriptors,
   declared RC frame limits, exact parent-J/rank relationships, no duplicate
   claim/node/module/group and no old-A frontier substitution. Reuse existing
   group commitments/J/header/membership helpers where applicable.
3. Compute the target's backward closure and unique required receipt claims;
   derive expected J from module summary/rank using the existing helper, then
   expected H from sorted exact-J members and parent seal heights. This is
   structural prediction, not mathematical acceptance.
4. Emit fresh `DMKNRC01`/version1 aggregate bytes and an immutable prepared
   record containing wire/header, ordered receipt bytes, target member opening,
   selected indices and byte/count census. The selected native/guest RC relation
   must independently reproduce the exact H. No Python-only checker result
   may replace that check.
5. Keep preparation pure and bounded. The limits should describe RC data,
   not claim to consume old mixed-envelope `rows`/`bodies` fields. Unsupported
   inputs refuse; a general-lane fallback is a separate explicit operation.

Source checking may refuse before inference, but expected H preparation must
not be described as trusted merely because every hash is internally consistent.
The existing same-image graph protocol and full receipt verification are what
discharge the conditional mathematical premises.

## Actual build and image adoption contracts

Three distinct artifact roles must not be conflated:

- **Native RC controls/build:** the current three native compiles establish a
  possible native checker/control binary only. They produce no guest image,
  cryptographic snapshot host, stage prover or portable certificate.
- **RC guest/image:** compiled from the same selected RC relation/census/wire
  closure, with real verify-every-pending-claim entry and H commitment. Its actual
  assembled image identity must be bound to the guest source/build/artifact
  records, not supplied as a desired old image or inferred from an output log.
- **RC snapshot and stage hosts:** fresh links must use the selected RC aggregate
  relation. Both existing host paths run `relation::check_bytes(wire)` during
  execution/preflight. Old binaries therefore cannot parse RC wire just because
  the command line names a new image. Host source and crypto backend can be
  reused if their APIs remain compatible; executables are still new artifacts.

`adopt_host_build(role)` should recognize only the exact finalized RC build
schema/root/source map/commands/outputs for that role, require clean completion
and no finalization override, and prove the new-library edges in each link.
Do not reuse the current native-controls build result as evidence for either
cryptographic host. Pinned retained dependencies can be reused; no backend
rebuild is implied by changing the application relation.

`adopt_image` should bind actual guest-source snapshot, build selection/result,
artifact, assembler selection/result and output image, including any enclosing
owner record required by those actual build formats. The image must match the
producer support image and each H. Do not fabricate proof-memo schema records.
An adopted source/image association is a local trust decision, not a proof that
the checker implements Lean correctly; the reviewed refinement remains needed.

The finite scheduler can retain po18 stages, assumption resolution, same-call
final resolved receipt verification, original allowance charges and saved-failure
semantics. Selecting a new image does not renew old failed/unfinished budgets.

## Receiver: likely zero code and zero verifier-rebuild change

Installed logical files resolve to these physical sources:

| Logical role | Selected physical source |
|---|---|
| client runtime/support/trust binding | `trust_withdrawal/client/runtime.py` |
| aggregate receipt owner | `trust_withdrawal/aggregate_claims/aggregate_admission.py` |
| terminal/member admission and publication | `terminal_i/client/workspace_evidence.py` |
| terminal packet and custody profile | `terminal_i/evidence_network/{packet,custody}.py` |
| authoring/import view | installed mixed-claim interfaces; continuing-context successors are separately selected, not silently installed |

The installed aggregate executable is retained
`small-aggregate-snapshot-host-build-01/small_aggregate_host.exe`, SHA
`a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05`.
Its `verify ADOPTED_A RECEIPT EXPECTED_HEADER` path is image-parametric and
calls `receipt::verify_aggregate`; it does **not** parse delta wire. That routine
requires a genuine succinct Poseidon2 receipt, dev-mode false, full resolved
application verification under the supplied adopted image, exact H bytes and
H's internal image binding. Therefore a receiver rebuild is not indicated by
the RC wire change alone. One actual new-receipt check is still necessary before
claiming runtime compatibility with this retained binary.

Use a fresh runtime adoption `{aggregate:{executable: existing_pin,image:A_RC}}`,
derive its exact support manifest and explicitly adopt a new TrustDomain. The
current runtime keeps its ordinary preparation producer tied to fixed I; leave
that unchanged. RC certificate production is the separate owner above, not a
replacement for the SDK's general Lean authoring profile. Workspace custody/wire
configuration must also name A_RC, producing a different profile identity.
Do not overwrite old workspace/trust records or reinterpret old-A receipts.

The current header/J encoding and terminal packet remain unchanged. After a
real certificate is available, the ordinary route is:

```text
admit_aggregate_member(real receipt, exact H, target J, opening)
  -> live A-member warrant -> export_evidence
  -> retain_semantics(selected group openings, no theorem proof bodies)
  -> ordinary terminal publication/discovery/acquisition
  -> same-call receipt verification and group opening
  -> MixedImportSession.use_aggregate_member -> local extension.
```

The producer may structurally package a terminal packet first, but the receiver
must obtain authority from its own real receipt verification, not from producer
stdout or saved native conditional results. The imported theorem's proof ancestry
is not fetched. The selected interface/group openings remain necessary.

## Remaining gates in the order that changes decisions

1. Complete the current RC source/control review and native same-J/W comparison.
   This decides correctness/refinement, not economic superiority.
2. Compare the **same** selected target and genuine parent frontier through RC
   and the best general route, using the same guest/proof-output semantics.
   If there is no consequential benefit, do not fund a new producer campaign.
3. If justified, select the actual guest/image and two host links, then add the
   small preparation/adoption/snapshot owner above with focused changed-boundary
   controls. Existing stage/network suites need not be repeated wholesale.
4. Produce one actual final A_RC receipt. Independently verify it with the
   existing image-parametric receiver, publish/import the exact target through
   ordinary APIs, and make a second RC contribution from that member. No mock
   or uncertified FIRST result may stand in for either boundary.

No real RC guest image, corresponding hosts, preparation owner, certificate or
new-image runtime adoption is established by the current native build work.
Those are exact missing inputs, not an instruction to launch them now. This
plan preserves the final-v5 goal and reuses its existing costly mechanisms.
