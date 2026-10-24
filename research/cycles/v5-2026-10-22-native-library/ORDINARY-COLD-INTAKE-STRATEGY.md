# Cold library intake: practical decision and safe incremental contract

2026-10-24. Source/theory investigation by `cold_intake_strategy`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No compilation, experiment, catalog/database opening, network operation or Git
mutation was performed. This note is a design contract, not runtime evidence or
authority to implement a new onboarding lane.

## Decision now

**Finish the thin, explicitly approved local-project extraction adapter and its
prospective capacity checks first. Do not build a generic cold-import scheduler
in this step.** Keep its same-parent completion rule unchanged. The separate
`ORDINARY-PROJECT-INTAKE-NATIVE.md` owns the exact request/schema contract; this
note does not duplicate or replace it.

The immediate benefit is narrow but real: a contributor with a compatible local
project can supply a missing complete declaration without reauthoring the
retained contribution, buying a certificate or trusting a peer binary. Early
remaining-capacity checks avoid extraction already known to exceed the public
completion envelope. The improvement reuses the existing exporter, binder,
independent receiver and approved-runtime selection.

This decision is **not** a claim that small completion accommodates ordinary
libraries generally. The user has no external local project to supply, so no
external-user benefit has been measured. Stop investing in this seam once its
new boundary is resolved; do not turn controlled compatibility into a claim of
broad deployment or useful growth. A genuine large-cold path is possible under
the conditions below, but it is not a cheap loop around the present command.

For users who need most of a common library and already approve its code,
conventional pinned-library sharing remains the practical starting workflow.
The commons must earn its added extraction/checking/discovery cost, not assume
that conventional libraries lack caching or incremental compilation.

## What the existing sources and evidence establish

| Boundary | Existing mechanism and limitation |
|---|---|
| Small retained completion | `ordinary_library_package/library_completion.py::complete_candidate` validates the original consumer, supplements exactly its missing names, and binds one ordered composite against the **same** protected parent. Public callers select 32 combined units, 4 MiB combined input, 131072 encoded nodes and 4096 names/bindings. |
| Original request recovery | `ordinary_library_support02/retained_preparation.py::reconstruct_preparation` requires exact request/header parent, hashes, target names and protected symbol identities. It is not a rebase function. |
| Candidate binding | `ordinary_lean/portable_candidate.py::bind_candidate` preserves claimed IDs, permits explicitly unclaimed names to acquire protected local interpretations, rejects existing-output collisions, and validates ordering even when it returns `NEEDS_LOCAL_INTERPRETATIONS`. |
| Checked delta admission | `ordinary_lean/ordinary_admission.py::_plan/admit` derives exact dependency order, rejects conflicting imports/exports and partially present groups, reuses exact complete units, and checks the remaining new units above one protected context. Its bounded core supports at most 1024 units/64 MiB per call; that is a ceiling, not a selected runtime budget. |
| Protected continuation | `ordinary_lean/portable_catalog.py::context/reserve_extension/_commit_checked` validates a one-parent chain, forbids shadowing, binds the actual new worker event, and atomically promotes an extension. There is no arbitrary-branch merge or unverified snapshot adoption. |
| Current extraction | The selected controller is `ordinary_extractor_binding/library_extraction.py`, not its older support-tree counterpart. It still produces one supplement for one original parent. Widening its approved module selection does not add resumable extraction or batching. |

Historical ReadFootprint evidence is already sufficient to show the scale
mismatch. `PORTABLE-LOCAL-IMPORT-REVIEW.md` records 2852 evidence files totaling
49,499,157 bytes, with a largest file of 970,480 bytes. The historical
`ADMISSION-RECOVERY-OUTCOME.md` records successful prefix-preserving admission
in 1024/1024/804-unit batches and independently inspected dependency bindings.
Its combined admission/recovery cost was 271.15625 known CPU seconds, including
the original failed attempt. This is evidence for that old selected closure and
support, not a benchmark or compatibility guarantee for a new public importer.
Its narrowly analyzed historical diagnostics do not relax today's clean-worker
policy. Do not rerun it merely to prove that batching can work.

At most 32 units per batch would require at least `ceil(2852/32) = 90` batches,
even before byte/node restrictions or reserving consumer capacity. The present
completion method does not authorize those batches. A new public lane may choose
a larger bounded core envelope, but must justify it explicitly rather than
silently lifting the ordinary contribution limits.

## Conditional batching theorem

Write `K0` for an authenticated owner-local accepted context under fixed
semantics/foundation/policy and supported checking implementation. Let `U` be a
finite dependency-ordered sequence of **whole** portable declaration units.
Each unit includes its complete permitted declaration records and exact imported
symbol IDs. These are inert evidence until checked.

Partition `U` into consecutive batches `B1,...,Bm`. Require:

1. Every external reference of a unit in `Bj` is supplied by `K(j-1)` or an
   earlier whole unit in `Bj`, with the exact expected symbol ID. No missing
   name, placeholder axiom or provisional success flag may close the boundary.
2. No output overwrites an existing name. An already accepted unit may be skipped
   only when all its outputs have the exact unit-derived identities and its
   complete imports are present with their exact identities. A partially present
   inductive/generated group is refused, not repaired by splitting the group.
3. The unchanged receiver checks all new units under the selected permitted
   axioms and declaration policy. Unsupported/unsafe/partial declarations and
   malformed generated records refuse normally. Foundation and semantic
   identities remain fixed; no new trust mode appears between batches.
4. Only the live, clean, correctly bound checking event followed by durable
   catalog promotion constructs `Kj`. The next batch uses that actual protected
   descendant, not a manifest's proposed result or a peer-provided snapshot.

Then, conditional on the existing kernel/controller/owner-storage assumptions,
every accepted `Kj` is a valid extension of `K0`. All previous name-to-identity
bindings remain unchanged. The proof is induction: batch 1 is checked in the
warranted base; each later batch refers only to the previously warranted prefix
and earlier declarations checked within that batch. No circular justification
crosses an unaccepted boundary.

This yields **prefix safety**, not all-or-nothing acceptance of the whole import.
Failure of batch `j` leaves the accepted prefix through `j-1` usable and charged.
It does not warrant the missing suffix or final consumer.

For fixed exact portable evidence, changing admissible partition boundaries does
not change its unit/export IDs: those identities bind the unit and imports, not
the owner's batching choice. Local context roots and generated module layouts
can differ with batching and must not be equated. Mathematical validity also
does not imply equivalent performance or identical frontend import behavior.

## Retaining the original consumer across a checked descendant

Let `C0` be the exact retained candidate and `R0` its authenticated original
request at `K0`. Let `Km` be a verified descendant obtained by actual admission.
The existing APIs intentionally refuse calling `bind_candidate(C0, context=Km)`:
`C0` and `R0` still identify `K0`. Rewriting those retained files or weakening
their context check would hide an interpretation change.

A separately selected future continuation operation can preserve the files and
derive a **new, explicitly authorized binding wrapper** as follows:

1. Authenticate `C0`, `R0`, selected original targets and original preparation
   files; recover and validate their claims against protected `K0`, not `Km`.
   Preserve these exact source bytes and their hashes.
2. Establish from protected catalog records that `K0` is an ancestor of `Km` in
   the same eligible lineage. Matching names or matching foundation alone is
   insufficient. Independent branches are not automatically eligible.
3. Preserve every original claimed symbol ID. Previously unclaimed names that
   already resolved at `K0` retain those interpretations by nonshadowing. For
   each genuinely missing name, record the exact newly selected symbol ID from
   `Km`. No name-only semantic-equivalence claim is made.
4. Require the unchanged consumer outputs to remain absent in `Km`; also reject
   dependency outputs that collide with consumer outputs during planning when
   possible. The original targets, declaration records, universe parameters and
   canonical complete-unit bytes remain unchanged.
5. Bind a derived wrapper against `Km` using the existing binder and the original
   prepared claims. The wrapper records the original candidate/request hashes,
   origin and destination roots, exact resolved-name map, unchanged canonical
   unit hashes and its own identity. It is a new local interpretation artifact,
   not a replacement original request and not mathematical acceptance.
6. Run ordinary preflight/admission under `Km`. Return the exact accepted
   statement and identities under the resulting interpretation. There is no
   need to re-elaborate the original source merely to preserve its provenance;
   there is still a need to independently check the complete consumer units.

The consequent judgment is `Gamma(Km) |- rho(p) : rho(T)`. It is not a theorem
that the source project's entire semantics equals `Gamma(Km)`. That distinction
is already present in the owner-local unclaimed-name policy and does not appeal
to human intention. Formal validity of the accepted statement remains decisive.

**Counterexample to permissive rebasing:** a candidate has unclaimed `q : Nat`
and proves `q = q`. Two unrelated contexts define `q := 0` and `q := 1`; both
can check the unchanged proof term, but they do not provide the same definition
or symbol identity. A successful final check is not evidence that an arbitrary
parent substitution preserved the original interpretation. Likewise, replacing
an explicitly claimed ID just because a name matches defeats exact dependency
identity even when some resulting theorem remains valid. The explicit descendant
and immutable-claims conditions avoid both errors.

## Operational contract a real cold lane would need

These requirements explain why the next thin adapter should not silently grow
into a generic scheduler:

- **Bounded evidence source.** A single giant JSON array parsed before batching
  is not bounded-memory onboarding. Obtain a finite pinned manifest/spool of
  individually bounded units, or a bounded streaming exporter with cumulative
  byte/node/name/edge limits. The controller must check evidence identities,
  dependency order and declared counts; the manifest itself grants no trust.
  Selected units must actually supply the required missing closure. Importing
  arbitrary unrelated material is not completion of the original request.
- **Whole-unit ceiling.** One oversized inductive/recursive unit cannot be made
  valid by arbitrary slicing. Refuse it with a clear unsupported resource result
  or separately design a larger bounded lane; do not add temporary axioms.
- **Extraction is a separate bottleneck.** Existing private imports can load the
  selected modules' transitive artifact environment. Admission batching does not
  bound that import's memory, enable missing private proof data, or make the
  existing exporter stream. One exporter repeatedly traversing the same closure
  for successive batches can erase the intended savings.
- **Nonrenewing session budget.** Bound total planned/accepted units, extracted
  bytes, spool/durable storage, batches, worker launches, CPU and wall time.
  Per-batch caps alone permit unbounded aggregate work. Failed extraction,
  refused batches and abandoned reservations remain counted. A later explicit
  continuation receives a new declared allowance; it does not erase past cost.
- **Durable progress and unknown commit.** Save immutable plan and batch-input
  identities. Treat catalog promotion as the linearization point. After a crash,
  inspect authoritative protected state: a fully committed exact batch advances
  the cursor; an uncommitted batch does not; uncertainty/corruption quarantines
  the operation. A saved `READY`, report or stale cursor cannot manufacture a
  successful native event. Use a new grant for an authorized retry and retain the
  old failure. Do not recheck an already accepted exact prefix.
- **Support and storage changes.** Revalidate current support eligibility,
  original ancestry and immutable snapshots before resuming. Corrupt artifacts
  or an unsupported implementation migration do not become valid through a
  progress ledger. Preserve the prefix and refuse until an explicit recovery
  procedure is selected. Do not relabel locally checked snapshots as portable
  warrants for another owner.
- **Atomicity and concurrency.** Serialize this owner's mutations using the
  existing owner lock. A remote event or another accepted branch cannot silently
  move the selected parent. Keep the same lineage until deliberate completion;
  branch merging is a separate contract.

The current catalog already limits roots, operations, names, selected artifacts
and plan bytes. Its default limits include 4096 roots, 8192 operations, 1048576
names and 4 GiB total artifacts. A cold plan must fit all these cumulative
constraints, including retained failed reservations, not only its batch inputs.
Raising defaults is not part of this recommendation.

## Cost and comparator: batching does not make cold trust free

For `m` batches, write `L(Kj)` for validating/loading the accepted context,
`V(Bj)` for checking the new complete units, `D` for extraction/transfer and `H`
for orchestration and storage. A defensible accounting model is

`T = D + sum_j [L(K(j-1)) + V(Bj)] + H`.

The checked prefix is not re-proved, but present catalog context construction
walks the selected chain, builds its bindings and checks retained artifact
eligibility. Fresh native workers load the selected context. If context load
cost grows linearly in accepted units and batches hold `b` units, that term can
grow as `Theta(n^2/b)` in a simplified equal-unit model. This is a warning under
stated assumptions, not a measured complexity bound for Lean. Ninety tiny
batches are therefore not automatically preferable to a few separately bounded
ones. Incremental authoring module anchors do not remove this cold-import term.

Compare three workflows honestly:

1. **Approved pinned ordinary library:** artifacts/caches and the local compiler
   are trusted according to the user's normal development policy. Often lowest
   cost for a large common background, but not independent receiver checking of
   malicious peer material merely because hashes match.
2. **Independently checked local library:** pay a cold check once, retain its
   protected results, then check deltas. A conventional local library offered the
   same checker, representation and cache is entitled to the same amortization.
3. **Commons selective reuse:** pay discovery, extraction, transfer, independent
   missing-closure checking and service cost; benefit when avoiding enough
   reconstruction or discovery effort and reusing the retained checked frontier.

No advantage follows from counting accepted theorems or charging the baseline
repeated proof replay while allowing the commons caches. Nor can approved package
binaries be offered as a zero-cost replacement under a stricter independent
checking policy. The useful compromise is explicit: large cold imports remain
an opt-in bounded expense; warm reuse is the default incremental path.

## Smallest useful next decision

Proceed with the reviewed thin project selection and early quotas; retain its
small completion limits and same-parent semantics. Reuse saved evidence for
unchanged boundaries. One controlled non-Std compatibility discriminator, only
if separately selected, can test the changed importer; it cannot establish the
economic value of a general cold lane.

Before selecting generic incremental onboarding, name a real required missing
closure, its available evidence source, the assurance policy preventing ordinary
pinned-library reuse, and an acceptable total cold budget. The minimum future
implementation is a bounded facade over existing admission plus the explicit
descendant-binding adapter above, not a new checker, global scheduler or
certificate protocol. If evidence extraction cannot produce that closure within
the same budget, the facade alone does not solve the workflow.

The next full-cost claim must concern a genuine discover/reuse/contribute loop
with retained background, against an equally optimized local-library comparator.
This design note settles the safety principle and implementation boundary; it
does not claim that cold onboarding, globally scalable discovery or v5 release
is finished.

## Selected thin controller implementation

After the strategy conclusion, root selected source implementation in
`ORDINARY-PROJECT-INTAKE-SELECTION.md`, adopting the exact native contract
`9463907393807d77c1a16f1fbe1dbefad29fb06df56c9348a25ae94d5135d339`.
The fresh controller is
`software/v5/ordinary_project_extraction/library_extraction.py`, SHA-256
`f11b2f4d5597118671af27f5738487fd3bcce69702d68091f6dbf9ed9bb694d1`.
Its predecessor remains unchanged at
`28ff83c5a8561b9f5250e9be08b34744aedd23757765feb174e1504d700308aa`.

The implementation adds only the selected same-parent seam:

- `selected_modules(modules, *, installed_std=True)` preserves default Std-only
  identifiers. The non-Std grammar is reachable through the explicitly selected
  project mode, not an implicitly broadened Std request.
- `selected_project(raw, expected_sha256, check)` checks the explicit local
  canonical document and hash, exact fields, ordinary Windows raw path grammar,
  existing non-reparse directories, path duplicates, and module identifiers. It
  returns the validated document with original path spellings and checked Path
  objects separately; those spellings are not replaced in request/metadata.
- `extract_retained` accepts the exact exclusive-mode signature in the adopted
  contract. Project roots are included in output/support overlap checks and
  checked again after native work. The existing facade still owns catalog and
  custody separation.
- Remaining unit/byte/encoded-node capacities derive from the same retained
  candidate after its real binder validation. Nonpositive capacity refuses before
  the native call. Project mode sends the exact nine-field request and retains
  `project-selection.json`, its pin, the selected roots/modules and capacities.
  Std keeps its original six-field request and success metadata; exhausted
  encoded-node capacity now also refuses early rather than awaiting completion.
- The existing protected lookup exchange, single CPU-accounting `finally`,
  native executable pin, full supplemental validation and unchanged combined
  completion planner remain in use. No acceptance, rebase, cold scheduler,
  decoder, shared Lean helper or receiver change was added.

Source inspection completed and the fresh file was handed to the independent
reviewer. No syntax execution, controls, compilation, owner opening, experiment,
package adoption or Git operation was performed by this assignment. The original
strategy-only note hash before this implementation appendix was
`d2a510cbf2bb0c44a18bb9ccdced550e70dfbc7e6cf111b9aa25a2bc53f13c5a`;
the final checkpoint hash is reported separately.

During the later integration-source assignment, the actual already-paid public
module name was found to have 75 bytes (`DMKNBridge_` plus 64 hex characters).
Root therefore explicitly selected project-only module component capacity 96,
preserving Std's 64-byte rule. The corrected controller is now
`cd79d9050fbc80a94faef845ddf99fe7d1b8ba5e376048aa4a7698f06f396061`.
The exact original contract and preceding source hash above remain historical;
no used source, compiled artifact or old outcome was rewritten. The associated
finite source-only plan is `ORDINARY-PROJECT-INTAKE-INTEGRATION.md`.
