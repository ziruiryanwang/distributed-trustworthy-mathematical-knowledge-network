# Independent ordinary A-capable client review

Reviewer: `v5_growth_decision`,2026-10-16. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source/evidence inspection only: no product imports, tests, native/proof calls,
Git operations or product edits. Root owns implementation/runtime selections.

## Design disposition

Read complete `PUBLIC-A-CLIENT-SEAM.md`,15096 bytes, SHA-256
`56d0981a4cfc7ae306ca7109b95636e6c799371d700842ec96efa45999ee2558`,
and relevant actual APIs: full atomic workspace, aggregate admission, mixed
custody/transport, mixed import/admission authority paths, retained receipt
constructor and acquisition-budget/handoff/closure mechanics.

**Design supports source implementation.** Mandatory actual A with optional
actual I is already supported by the underlying exact mixed APIs. There is no
reason to fabricate an I authority or require its otherwise unused lifecycle.
The new workspace/profile is separate from unchanged I-only source and state.
No new mathematical checker or generic plugin mechanism is needed.

The actual seam remains narrower than standalone remote A-member discovery:
the existing mixed packet requires a delta and targets its final delta. Direct
A member admission supplies the local bootstrap; ordinary substantive extension
produces the existing wire form. The design explicitly preserves that limit and
does not propose wrapper theorems or assert that this alone completes v5.

## Decisive source-review obligations

1. **Concrete specialization, not swapped imports.** The frozen base has lexical
   references to its I-only classes/schema. Review every inherited call. In
   particular, new `Workspace.open/operation/status`, client construction,
   `_active`, optional-I admission/report/close, all warrant dispatch, context
   dispatch, `resolve` and both packet parse paths require correct treatment.
   Base `find` may be reused only because both handoff names are the **same**
   `DeltaLocatedHandoff` class; this does not make `FrontierAcquisition` and
   `MixedAcquisition` interchangeable. Do not monkeypatch frozen globals.
2. **Immutable owner/profile origin.** Require actual exact types, fixed I/F/P,
   explicit A, and the exact delta owner tuple `(optional_I,A)`. Bind actual
   owner identities as well as profile values throughout the client lifetime.
   A pristine report uses `live_aggregates/live_members/member_calls`, not the
   I owner's `live_handles`. Deadline/cap checks must not invent an unavailable
   I-construction timestamp or silently extend an original deadline.
3. **Member-specific authority and cache.** Receipt-level reuse is keyed by A,
   actual owner profile, exact H and receipt digest/length, and revalidates the
   real live aggregate. Member reuse additionally binds exact J, index and
   ordered siblings. Use `describe_member`, never an aggregate fact masquerading
   as a module. Normalize `journal`, `aggregate_header` and each sibling byte
   string explicitly for comparison; original bytes remain verification inputs.
   Copied/deserialized/foreign tokens must fail registry membership.
4. **Conserved resources.** Every actual direct I/A or mixed admission uses the
   same existing `AcquisitionBudget` before issuer work. The per-owner CPU caps
   are nested constraints, not fresh disjoint allowances. A receipt cache hit
   needs no new native verification reservation but still charges submitted
   inputs/member work. Preparation remains the separate, preallocated share;
   failures do not refund or renew grants. Existing600-CPU per-admission and
   original query/deadline limits remain. Controller/member/output costs remain
   bounded and observed, without claiming a filesystem or hostile-code sandbox.
5. **Revocation and close.** Every exit invalidates local tokens/contexts/caches
   appropriately. Closing mixed acquisition/delta does not close independent A
   or I issuers, so the new client must explicitly close them. Preserve cleanup
   poisoning, persisted uncertain tails and owner-transfer-on-success only.
   Reopening persistent custody reconstructs data, never trusted handles.
6. **No semantic shortcuts.** Existing atomic imports, demanded bodies and
   exact whole-J resolution stay unchanged. Direct A membership does not supply
   definition bodies. Publication/custody/index state remains structural data;
   all mathematical use depends on freshly live issuer authority.

Baseline `workspace_atomic.py` remains SHA-256
`01eefed1804ec5f296aebfcc12441dd283cd77c9bac8f8d5b02e8a4becc5e8c1`.
Aggregate admission source is
`a6a7e8041674de60fff198ed8522b1c28e0662bbf1f8acce8fe3eee60ab03561`;
atomic imports `8d5e77ea1a239c10bd745a2860080d4ea6c91e52f4da32c7f18562ca755c0ba8`;
mixed receiver `d292a966469402a24282e40377c8ac9c929504e38de7862aa9a6bd1b3ad3fb00`.

## Evidence separation and next step

Review the newly selected source and distinguishing proof-free controls only.
Synthetic interactions can test dispatch, keying, charging and revocation, not
issue mathematical authority or stand in for a genuine A receipt. The actual
new-client A-member-to-extension-to-cold-recipient gate remains necessary once
a compatible real receipt exists; combine it with, rather than repeat, the
unrun old fixture integration. Existing actual I reuse is already evidence.

No implementation or runtime pass is asserted by this design review.

## Fixed-target sealing: transport premise currently missing

Read the existing `AFFORDABILITY-NEXT.md` and `DELTA-SEALING-POLICY.md`; their
benefit and rent-or-buy arguments require an **available target-preserving
post-seal receiving route**, not merely a successfully produced certificate.

Counterexample: targetX is one native delta over an already-I-certified baseB.
A successful aggregate certifies bothB andX. Replacing X's witness by its exact
A-member opening would leave zero deltas, which the current mixed parser rejects
(`1 <= len(deltas)`). Packet custody targets `witnesses[-1]`; actual mixed
admission also requires its requested summary to equal that last delta. Keeping
X as both certified frontier and delta repeats exactJ and is rejected. Keeping
X as a native delta over certifiedB is possible but still downloads/checks X's
witness: the intended removal of X's own cost has not happened. Search/index
semantics can describe X, and direct aggregate admission can verify supplied
bytes, but current public custody/offer/acquisition cannot connect those parts
for a standalone certified target. A known unrelated descendant is neither
guaranteed to exist nor a target-preserving substitute.

This does **not** invalidate ancestor sealing: when the requested target remains
an unsealed descendant, its proper ancestors can be replaced by A frontiers in
the existing mixed wire. Nor does it disprove the conditional growth theorem.
It means the complete-route margin must use that actually deliverable rewrite.
For the stated simple chain model, retaining the final target as a native delta
adds its receiving cost at the checkpoint; under equal per-node costc this adds
`lambda*c/k` to the displayed per-contribution expression. One must not use its
old checkpoint service termv as if a bare target were remotely available.

Smallest deployable alternative: a separately typed, bounded **selected terminal
evidence envelope** containing real A receipt, exactH, exactJ,index,ordered
siblings, with independent semantic openings/bodies served by existing stores.
Structurally bind its advertised ModuleID and exact locally adopted A/F/P; use
the existing real aggregate verifier and member selection for admission. Reuse
opaque byte custody/HTTP machinery with explicit profile/schema gates and the
same acquisition budget. Do not reinterpret A as I, relax the mixed parser's
last-delta contract, accept provider success flags or add a wrapper theorem.
Existing cryptographic semantics suffice; the missing work is typed publication,
location/acquisition and authority handoff. Exact format/source is not selected.

Priority: finish the already-selected A-client source/control review. Before
spending the **actual public-A campaign** as evidence for fixed-target sealing
benefit, select either this small terminal route or explicitly retain an
ancestor-only comparator and margin. Prefer integrating terminal dissemination
into that one future genuine-A campaign, avoiding a later repeat. This gap does
not block source authoring or a justified proof-capability investment; it does
block claiming the full fixed-target network benefit from lastdelta-only APIs.

## Initial product source review and correction

Read complete initial `client/workspace_mixed.py` at30701 bytes/SHA-256
`0607e8d6e1fb45f930d405de6b635741d560c3298a5caa7b1e9338e7552c7f55`.
Root found, and this reviewer independently confirmed, a transferred-owner
cleanup defect: `_active` detected owner-attribute substitution, but `_fail`,
`close` and reporting still used mutable current attributes. A replacement could
be closed while the original transferred issuer remained alive.

Revised source31054 bytes/SHA-256
`eb4e9374707b3e3f03b7e60ad91fd0fd30a3872d3e9fb59fe3f93c039338acbd`
closes the original frozen owner tuple, not an untransferred replacement, and
reports original-owner accounting. The import session retains its ordinary
client-owned lifetime. Cleanup errors poison the workspace; all local warrants,
member/receipt/packet caches and contexts are revoked. Focused controls must
distinguish this original-owner guarantee. No execution preceded the correction.

The same revision factors pure `_bind_fact` checks so `_issue` does not
immediately perform a duplicate live describe; `semantic_material` likewise
does not duplicate the inherited I/mixed check. The live issuer check remains,
including exact fact normalization, source/profile and evidence binding. This
is removal of duplicate calls, not use of a saved-report authority shortcut.

The full implementation review finds no other blocking source issue:

| Boundary | Reviewed implementation |
|---|---|
| Storage and inheritance | Separate schema/mixed PacketStore; no old open/constructor call; explicit operation/status overrides; neutral grant/lock/history/publication mechanics inherited unchanged. |
| Optional I | Exact A/delta mandatory, optional exact I; actual delta tuple and I/F/P/A bound; direct I refuses when absent; report/cleanup handle absence. |
| Source/profile lifetime | Actual configured owner identities and profiles frozen; source paths belong to selected pins/import origins; handoff alias identity is checked rather than globals patched. |
| Direct A reuse | Exact header/profile/image/receipt-digest/length cache; real live aggregate revalidation; every member call uses actual `select_member` with exact J/index/ordered siblings. No receipt-only member token reuse. |
| Member snapshots | Known byte fields become canonical inert lists for comparison; original receipt/header/J/path bytes remain issuer inputs. New kind dispatches to `describe_member` and `use_aggregate_member`. |
| Resource accounting | One shared AcquisitionBudget reserves all actual direct/mixed admissions; authoring remains disjoint; submitted A bytes/index/path and repeated calls charged; existing deadline/member/output limits preserved. |
| Network and semantics | MixedAcquisition uses same grant/profile and actual mixed verifier; both parser paths use selected A; atomic materialization, demanded bodies and authoring remain unchanged. |
| Shutdown | Original transferred owners explicitly closed even after acquisition cleanup failure; cleanup uncertainty persists and prevents new grants. No persisted token restoration. |

Direct member admission intentionally relies on the issuer's exact member cache,
not a second client member cache: selecting another member reuses crypto receipt
authority but still invokes charged exact membership selection. This satisfies
the design without confusing two members of one receipt. No new theorem/wrapper,
proof production, standalone A network format or positive growth claim appears.

**Product source review supports the corrected candidate**, pending the final
API/implementation checkpoint and distinguishing control-source/selection review.
No test, product import or mathematical authority was produced by this review.

## Final API and focused-control source review

Read complete `API-MIXED.md`,8978 bytes/SHA-256
`4a809b43d32e7fc5888ce9dda7e994817610006bc1d0a338bc83963786b3383c`,
and `PUBLIC-A-CLIENT-IMPLEMENTATION.md` at SHA-256
`17be4c05e830d24f94e2841bb7ac37c6cd06ab96364839f20bdc63a80a6132a2`.
The API accurately distinguishes direct local A admission, remote last-delta
targets, missing semantic material, trusted owner construction and persistent
cleanup uncertainty. Its inherited/overridden method map agrees with source.
No further product/API blocking issue was found in the selected seam.

Read all16 focused controls in `client/test_workspace_mixed.py`,29962 bytes,
SHA-256 `478de57908ebffc98093f0139f83e0a06a9609383f237cec4466086736eb0c3e`,
and complete `client/mixed_control_owner.py`,1323 bytes/SHA-256
`02b06e69237ad6da091ea9368992cc3ee6286fcaab27a187ce6db56be6283c80`.
These exercise the real workspace/configuration/storage/grant/client/budget and
pure member bindings, with explicitly fabricated exact-class issuer instances.
Receipt/native acceptance, constructor/install checks and one semantic-import
dispatch are synthetic. No product test mode or genuine mathematical authority
is thereby established.

The initial14-control draft lacked a regression for the concrete original-owner
cleanup defect. Root and this reviewer requested it; two additions now cover
all four substituted owner attributes and persistent cleanup uncertainty. They
require original owners closed, A aggregate/member registries empty, old member
unusable, replacement untouched, original report dispatch, and no new grant
after an injected cleanup error even when final close later succeeds. These
are new changed-boundary controls, not repetitions of old passing campaigns.

Other controls distinguish A-required/I-optional profiles, owner/image pairing,
pristine/cap/deadline/source-pin refusals, exact two-member receipt reuse,
different receipt/header cache keys, wrong membership openings, shared I/A/mixed
acquisition charges, absent-I refusal, changed profile, foreign/expired handles,
same-owner import dispatch, fresh reopen without warrants, and refusal of a
zero-delta packet. Fixtures' actual pure methods and report/state fields were
checked against existing issuer source. No blocking fixture mismatch was found.

Read root's `Select-PublicAClientControls01.ps1`: it verifies all retained pins
against exact prior plan `e92a408dbd99d6893a7588d8f8151e879a18b62bbcc4439be37694a5ac2f4233`,
removes only five unused helpers/tests plus the prior owner, adds the new mixed
client/test/owner, and retains30CPU/90wall/512MiB/two-process bounds. Preparing
this plan does not launch it. Exact generated-plan review remains separate.

**Source disposition:** corrected product/API and16 focused synthetic controls
support one separately selected finite run. This is not a runtime pass, actual
A import/reuse evidence, economical proof-production evidence or full v5.

## Exact finite selection review

Read complete generated `experiments/v5-local-checks/public-a-client-controls-01-plan.json`,
30271 bytes/SHA-256
`97ccdfe728f4fc38cdbdfa3459c26ca5dc2ab07ed2fd72b2af94bbb8fef72593`.
Independent read-only pin comparison confirms89 selected source files,
1011606 bytes, no size/hash mismatch and no changed retained source against
the exact atomic02 predecessor. The only additions are mixed client/test/owner;
the only removals are the five unused helpers/tests and prior owner listed by
the selector. The new owner entry calls only the16 selected controls. No old
test suite, real verifier constructor, native/Lean/prover, Node service or
network acquisition is called by this selected owner.

The actual public launcher/bootstrap were read completely. They retain the
fixed release-manifest binding, exact snapshot/source/import-origin checks,
single original deadline, enclosing Job and final closure/census requirements.
Source roots stay canonical; the fresh output is
`product-local/v5-client-owner-runs/public-a-client-controls-01`, observed absent
at review. It is disjoint from the installation and all source roots. The test
only writes ordinary fresh workspaces beneath that operation's `work` directory.

Verified actual fixed manifest SHA-256
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`,
all584 Python runtime files and three launcher helpers:587 pins,30536285 bytes,
no hash mismatch, missing runtime file or extra runtime file. The selected
portable source closure and import strategy are unchanged; the test and its
package-relative imports are present in the selected snapshot map. No product
import or execution was used to obtain these results.

Limits remain30 child CPU seconds,90 original wall seconds,512MiB,two processes,
1MiB stdout and stderr each; final output census caps128MiB/4096 entries.
The existing separately observed wrapper CPU/startup/finalization limitations
are not silently included in child CPU or called a security sandbox. Test grant
reservations are deliberately synthetic values, not permission to spend those
CPU amounts outside the30CPU enclosing Job.

**Launch disposition: exact selection supports one root-owned finite synthetic
control run.** This review does not launch it, predict success or authorize any
genuine receipt/proof campaign. Preserve the exact used bytes and audit actual
saved outcomes, including outer/final binding, after termination.

## Independent actual outcome audit

Audited only saved evidence under
`product-local/v5-client-owner-runs/public-a-client-controls-01`; no rerun,
product import or execution by the reviewer. Read outer `RESULT.json`,
`BOOT-RESULT.json`, exact `command.json`, complete stderr and inner
`work/mixed-controls/RESULT.json`. All16 selected tests report `ok`, with zero
errors/failures/skips; the selected list matches the reviewed owner/test source.
The source-defined synthetic acceptance and one import-routing stub remain
explicit in the actual result, not upgraded to genuine A authority.

Both original and copied plan retain SHA-256
`97ccdfe728f4fc38cdbdfa3459c26ca5dc2ab07ed2fd72b2af94bbb8fef72593`.
Independently compared all89 original source files and all89 snapshots to
selected lengths/hashes: no mismatch. Snapshot census is exact. All68 recorded
import origins belong to selected snapshot files, including the new mixed
client/test, frozen atomic base and mixed-network APIs. The bootstrap's final
runtime/source/origin/plan checks completed. No `BOOT-FAILED.json` or
`FINALIZATION-FAILED.json` exists; no output reparse entry was observed.

The actual public launcher records `COMMAND_EXITED_ZERO_AND_CLOSED`, exit0,
direct child reaped, Job closed, zero active/terminated processes, no termination
request, no cleanup errors and no final binding error. Command limits and exact
original90-second clock interval match the selected plan. Peak sampled Job
private commit is42201088 bytes. Known new CPU is2.4375 Job plus0.484375 wrapper
= **2.921875 seconds**; wrapper-inclusive measured wall is **3.9273728 seconds**.
Interpreter startup before the clock and the final reporting tail retain their
recorded limits; nested supervision CPU is not added a second time.

Reported pre-outer-result census is492 entries/4029073 bytes. Independent final
read-only census is493 entries/4031367 bytes: the difference is the outer
2294-byte `RESULT.json` itself, within selected128MiB/4096-entry bounds. These
are observed censuses, not a hard filesystem quota.

**Independent outcome disposition: PASS for the selected synthetic public-A
client controls and their exact source/import/operational closure.** Root may
adopt this narrow evidence and preserve all used source/plan/results. Do not
repeat the16 controls absent a newly changed boundary. This establishes the
tested dispatch, cache/member binding, shared budget, revocation/reopen and
original-owner cleanup behavior with synthetic issuers. Genuine A production,
actual A-member semantic reuse, standalone certified-target network transport,
economic benefit and the complete deployable v5 remain open.
