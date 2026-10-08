# V5 certified modular relation: source-backed implementation decision

2026-10-07. Author: `/root/v4_final_growth_challenge`, now mechanism owner.
Scope: new unused design/model only. No predecessor code, build, proof, runtime,
product, evidence or handoff was modified or executed for this investigation.
Root owns selection; assurance independently challenges the trust boundary.

## Decision

Implement a **new versioned module relation with certified declaration imports
and demand-driven immutable-environment reconstruction**. Do not extend the v4
macro lowerer into a purported kernel importer. Do not use absent definition
bodies as axioms, assign them opaque hints, or make a missing lookup mean false.

The first consequential implementation is a native-only conditional relation,
its parser/identity model and demand controls. It must support a genuinely new
inductive declaration group and branch composition. Its conditional reports
are not mathematical admission until genuine selected parent receipts have
been verified. A new guest/image and actual recursively resolved certificate
come after this relation and its boundary controls pass independent review.

The final intended route is:

```
exact module reference + certificate
  -> authenticate selected declaration/group headers
  -> reconstruct immutable selected environment
  -> check local declarations, stopping with NeedDeclaration/NeedBody if necessary
  -> fetch/authenticate only the demanded records; reconstruct and retry
  -> completed exact witness -> same relation in guest -> resolved module receipt
```

Imported bodies are not re-type-checked merely because they are used. Their
exact declaration and body commitments are certified. Their demanded bodies
still enter conversion, and their type/semantic dependencies still cost work.
All **new local** definition, opaque-value and theorem bodies are checked.
New inductives are checked as complete groups, not admitted as arbitrary recursors.

## What the actual source permits today

Paths below are relative to the canonical project root. These are source facts,
not fresh runtime claims. `native-relation-01/project/guest/src/relation.rs` and
the corresponding `certified-definitions-04` file have the same inspected SHA-256
`69f2d79d803501e007778cbec7fc218087783d42ff41eb49cec8a05f9011a75e`.
Their checker `src/tc.rs` copies likewise share
`522134805c82cb7522aafc2550a3bfc520455f44f893fb18a94acec5fb162c6f`.
This comparison covers those two inspected files, not an asserted complete tree map.

| Existing seam | Exact behavior and consequence |
|---|---|
| `experiments/native-relation-01/project/guest/src/relation.rs:296` | `check` authenticates fixed foundation rows and selected typed parent journals, then parses/checks the packet. It is a conditional relation; source equality does not verify receipts. |
| `relation.rs:385` | Nonfoundation axioms must match selected certified **Prop** interfaces. They are checked as types and separately required to be Prop. This is not a general imported-definition mechanism. |
| `relation.rs:409` | New definitions must be safe, nonopaque, singleton groups, with both type and value F-closed. Their exact body is hashed into identity and the canonical name. |
| `relation.rs:489` and `:509` | A selected definition requires its exact body, and every selected/authenticated/intrinsic definition is passed to `export.check_declar`. Certification currently does not eliminate definition-body rechecking. |
| `relation.rs:454` | The relation rejects output self/cross references and unknown constants. These restrictions, not merely the lowerer's API, prevent general named modules and local theorem chains. |
| `checker/src/env.rs:54` | `Declar` already represents Axiom, Quot, Theorem, Definition, Opaque, Inductive, Constructor and Recursor. A Definition stores an eager `ExprPtr` body and hint. |
| `checker/src/parser.rs:802` | Safe definitions/opaque values, theorem bodies and complete inductive rows are constructible; unsafe/partial definitions are refused. Parser construction is not checking. |
| `checker/src/tc.rs:82` | `check_declar` checks local Definition/Theorem/Opaque values against their declared types. `check_declar_info` checks universe parameters, closed types and their sorts; Theorem requires Prop. |
| `checker/src/env.rs:240` and `util.rs:239` | Immutable environments use an insertion-index cutoff; a declaration cannot refer to a later ordinary declaration. This is useful for local extension safety but must not confuse hidden-later with missing imported data. |
| `checker/src/tc.rs:1138` and `env.rs:322` | Delta reduction inspects declaration kind/hint, then obtains and substitutes the body. Keeping only a type or changing the hint changes behavior before body access. |
| `checker/src/inductive.rs:34` | New inductive checking reconstructs/checks constructors and recursors, including nested specialization. It uses whole mutual-block metadata and temporary environment extensions. |
| `checker/src/parser.rs:429` | Finalization constructs constructor ownership and complete recursor maps. Loading one arbitrary constructor/recursor without its authenticated group is insufficient. |
| `experiments/certified-definitions-04/project/guest/src/main.rs:34` | After the conditional check, the guest calls `env::verify` for every selected parent journal, then commits its journal. Resolved final receipt acceptance remains required outside the guest. |

The guest schema currently omits `opaque` despite checker/parser support.
Nonfoundation inductive groups are rejected by the current relation even though
the checker supports them. New profile/schema/journal domains are necessary;
old v4 journals must never be reinterpreted as v5 module certificates.

## Identity: finite names, no hash fixed point, no naming authority

Use three distinct objects:

1. **Module specification**, defining immutable mathematical identities.
2. **Checking witness**, containing new proof/value terms and imported evidence.
3. **Certificate**, attesting the exact relation's successful check of that spec.

The module specification is a bounded canonical structure containing format,
foundation and semantic-policy IDs, exact external declaration references,
ordered local declaration/group descriptors and their expression commitments.
Local references are relative name trees/slots, never the final module hash.
External references are `(ModuleSpecID, relativeDeclarationName)`; foundation
references are tagged and restricted to the exact adopted foundation.

Compute `ModuleSpecID = H(domain, canonical specification)` before relocation.
Relocate a local relative name `r` to `DMKN.Mod.<ModuleSpecID>.r`. Preserve the
relative hierarchical name structure, rather than flattening all names to
unrelated slot strings: the checker derives `.rec` and nested auxiliary names
from inductive names. Rename **all** expression constants, projection type names,
constructor ownership, mutual-member lists, recursor associations/rules and
relevant name-derived metadata consistently. Human source/display aliases are
outside the mathematical identity and may coincide across independent modules.

Local mutual/recursive references hash as relative references. The final name
is inserted only after the hash, so no equation `h = H(...h...)` is required.
Bodies of transparent definitions are committed. Opaque implementation bodies
are committed but not automatically disclosed to downstream conversion.
Theorem witness terms may be separately committed by the checking-witness ID;
the mathematical theorem identity binds its exact interface, not a particular
proof. A proof may not certify itself simply because its identifier is known:
local ordering and strictly descending imported certificate ranks still apply.

Concretely, external references occurring only in a theorem's proof belong to
the checking witness and its imported-receipt set, not the module specification.
Different proofs may therefore preserve ModuleSpecID while changing witness ID,
parent receipts and rank. References inside public types or committed definition/
opaque bodies affect the specification. Reject attempts to import the very
ModuleSpecID currently being constructed as a shortcut around local checking.

Universe parameters are declaration-local ordered binders. The codec may encode
them by positional indices and relocate to fresh fixed parameter names, but it
must preserve order, occurrences, arities and `max`/`imax` expressions exactly.
Do not identify reordered parameters or normalize universes without an explicit
proved/checked translation rule. Constants bind both exact declaration identity
and their ordered universe instantiation. Binder display spelling is not a
license to change binding structure. No semantic hash-equivalence oracle is needed.

The relocation obligation is a concrete structural statement: injective
namespace relocation fixing foundation names, preserving local scope and group
name conventions, commutes with expression substitution and transports checker
judgments. Differential exact-structure controls and native Lean comparison are
required; a content hash alone does not establish this statement.

## Certificate conclusion and ancestry avoidance

A new journal binds at least:

```
relationVersion, admittedImage/policy, FoundationID,
ModuleSpecID, declarationGroupRoot, exportRoot,
rank, exactCheckingWitnessDigest
```

`declarationGroupRoot` is a canonically shaped bounded Merkle map/vector of the
module's declaration/group descriptors. It binds kinds, types, universe binders,
hints/safety, body commitments and whole-group metadata. A descriptor opening
also binds its exact module and relative address. Raw bytes or inclusion alone
do not establish validity: the root must be in an actually verified compatible
module receipt. Publication/export selection is separate from this admitted map.

Select **self-contained module-validity receipts**, not a recursively traversed
manifest chain and not an initially mandatory global environment-root merge.
The guest proves its own safe local extension using exact certified imported
records, and recursively verifies selected parent journals. A cold receiver
verifies the resulting fully resolved receipt once. It does not fetch the
proofs, witnesses or import manifests of the certificate's proof ancestors.

If a demanded type/body names an ancestor module O, the receiver obtains O's
own resolved module receipt and the exact descriptor opening. It does not claim
that an arbitrary hash is certified merely because M once imported something.
This costs one certificate per distinct **semantically demanded** module unless
already verified locally. O's proof ancestors remain hidden. Signature or
conversion closure can therefore extend through several modules; it is not
silently equated with proof-history-independent constant work.

Why independently certified O can be joined: all references are immutable
module-qualified identities under one policy/foundation. M's receipt certifies
that its referenced imported identities had compatible validity warrants when
M was checked. O's independent receipt establishes the same immutable semantic
descriptor. There is no mutable global name whose meaning differs between M
and O. This compatibility/weakening argument is an explicit soundness obligation,
not an assumption that any two independently consistent axiom sets can be unioned.

The alternative of having every receipt commit a transitive admitted-environment
root would permit membership against that root, but adds authenticated union,
conflict, update and witness-cost mechanisms. It is unselected for the first
implementation. A raw Merkle root would not eliminate those costs or prove
validity. The selected scheme needs no globally current environment or ledger.

The new image must verify only the explicitly adopted parent-image/profile
policy. Old-image bridging, if desired, is a separate explicit adapter theorem
and relation—not acceptance based on similar journal fields. The image identifier
in a public header is not self-authentication. Root/verifier adoption pins the
actual image, as in the existing trust chain. Format/policy identifiers in the
module specification do not require embedding that specification's own hash.

## Exact import/extension/merge relation

Let F be the adopted foundation; W the finite authenticated witness environment;
I its imported declaration groups; and L the ordered local extension groups.

The relation accepts only after:

1. Decode the bounded canonical spec/witness; verify exact IDs, group openings,
   role census, namespace relocation and complete syntactic reference bindings.
2. For every imported record, bind the exact compatible module journal and
   descriptor opening. Guest receipt assumptions or actually verified native
   receipt tokens—not persisted sender flags—supply its validity premise.
3. Build one immutable selected environment from F, I and L with fresh ordinary
   cutoffs and exact atomic group boundaries. Equal qualified identities coalesce
   only for identical authenticated records. Different modules' same human names
   remain distinct. Foundation shadowing and mismatched identity are refused.
   Imported records are visible as certified external declarations independently
   of consumer insertion order; all loaded imports precede the new local cutoffs.
   Looking into an imported body's own certified context must not accidentally
   inherit that imported record's temporary insertion position as a validity
   cutoff. Missing imported dependencies demand more data; genuinely later local
   declarations remain unavailable. No imported record is installed under a new
   local declaration's identity to change its role.
4. Skip body checking only for records bearing the exact authenticated imported
   role. Ordinary new declarations cannot acquire that role through a tag or
   duplicate-name trick. All local values and every new inductive group undergo
   actual checking in the correct preceding/local-mutual environment.
5. Every absent data access is a demand/refusal, never a normal semantic answer.
   Demand expansion may add authenticated records or bodies, but cannot change
   any prior record, kind, hint, type, universe parameter, local ordering or
   group boundary. No replacement underneath existing typechecker caches occurs.
6. On success bind the exact module, final witness and output roots. For a
   transferable claim, recursively discharge all actual parent assumptions and
   verify the final receipt against the adopted image/policy.

Native conditional success without genuine parent verification is diagnostic
only. A caller may not forge a module import token from a JSON status field.
Imported bytes must remain bound to the invocation's verified journal set.

The intended soundness statement is conditional on the adopted checker relation,
foundational assumptions, canonical/relocation correspondence, hash binding and
recursive-proof soundness: accepted modules constitute compatible conservative
extensions of F, and accepted local theorems hold in their exact union. It is
not yet a machine-proved equivalence between Nanoda and all Lean behavior.

## Demand mechanism: preserve semantics and avoid intrusive mutable lifetimes

Choose immutable reconstruction over an in-checker network callback. The current
`Env` and `TcCtx` borrow arena-backed immutable declarations; mutating/fetching
into that arena during inference would affect many signatures, lifetimes and
cache invariants. No network I/O belongs inside the trusted guest.

### Required distinction

```
Known(record, bodyPresentOrCommittedAbsent)
NeedDeclaration(exact qualified identity)
NeedBody(exact qualified identity, committed body digest)
KnownNotVisible(local cutoff violation)
InvalidReference(no such authenticated module member)
```

`env.rs:get_old_declar` currently returns `None` for both missing entries and
entries beyond the cutoff. These must not be conflated. A hidden later local
declaration is not fetchable missing data. A missing imported record does not
prove the name denotes no declaration, and an absent body does not prove two
terms unequal. Ordinary local self/forward-reference attempts still fail.

For imported transparent definitions, extend the checker representation with a
certified missing-body state while retaining **Definition** semantics and the
exact hint. `get_applied_def` must still recognize it as a definition. On an
actual `get_declar_val`/delta demand, absence returns `NeedBody` or halts; it must
not return the ordinary nondefinition `None`, invent an opaque hint, or install
an axiom. New local definitions may never have absent bodies.

Imported opaque declarations retain Opaque kind and their certified header.
The current checker never unfolds Opaque through `get_declar_val`; absence of its
private implementation is therefore not the same case as a transparent demand.
New opaque declarations still require their full value when originally checked.

Certified Prop theorem import can retain the existing separately justified
sealed-Prop interface substitution. This is not generalized to definitions.
The descriptor preserves theorem identity/kind even if the checked-environment
adapter uses an internal certified-Prop stub. Its soundness relies on the actual
certified theorem and Lean proof irrelevance. The current checker otherwise
allows Theorem delta unfolding with an opaque hint; the adapter must not pretend
that a missing theorem proof is an arbitrary missing definition body. This
specific substitution needs independent review and correspondence controls.

### Finite host loop

```
W := authenticated headers required by local syntax and selected interface types
repeat under one cumulative CPU/bytes/rounds/requests/deadline allocation:
    reconstruct fresh immutable environment and empty checker caches from W
    run native conditional preflight
    if Checked: retain exact completed W and result; stop
    if Need(k):
        fetch bounded exact descriptor/body/group opening for k
        verify module receipt and binding before granting imported authority
        extend W monotonically; reject unchanged/repeated unsatisfied demand
    otherwise: return Refused
```

The guest consumes completed W, not this host's success flag or demand transcript.
It reruns the same successful mathematical relation. Any demand still missing
halts/refuses and creates no accepted journal. A dishonest preflight can waste
resources or omit needed data, but cannot cause guest success through omission.

One feasible implementation is a typed `Demand` result propagated through checker
accessors. A native-only typed unwind caught at the outer preflight boundary may
reduce invasive return-type edits, while guest absence panics/aborts. However,
the current guest release profile explicitly has `panic = "abort"`; do not rely
on guest unwinding or catching arbitrary native panics as successful demands.
The exact error mechanism is an implementation selection after source review.
All other panics/errors remain refusal. No synthetic sentinel expression is valid.

This mechanism can redo earlier checking after a new demand. With d demanded
records it may cost much more than one final pass, potentially quadratic in an
adversarial chain. Charge every attempt; batch statically knowable type/group
dependencies before retry; cache immutable authenticated data but not unchecked
mathematical success. A full lazy accessor may become justified if measured
restart cost is central. Do not advertise optimal locality from this first seam.

## Supported declaration kinds and hazards

| Kind | First selected design | Hazard that must remain explicit |
|---|---|---|
| Foundation declarations/axioms/quotient primitives | Exact existing F; no new arbitrary axiom or Quot export. | Reserved names and primitive behavior cannot be replaced by a lookalike module. |
| Safe Definition | New body checked; imported header/body commitment certified; actual unfolding demands exact body. | A certificate cannot remove demanded computation. Hint changes, body substitution and self recursion must refuse. |
| Theorem | New proof checked as Prop; imported exact certified Prop interface has no ancestral proof replay. | Statement may demand semantic definitions. Proof irrelevance does not authenticate its statement or assumptions. |
| Opaque value | Add missing guest schema support; check new value; import certified opaque interface without private body replay. | Opaque is a declaration kind, not permission to relabel a transparent definition. |
| Nonrecursive/recursive/mutual inductive group | Admit complete safe atomic types/constructors/recursors; use actual `check_inductive_declar` for new groups. Import complete certified group metadata/rules. | Positivity, constructor ownership, recursor equations, K flag, universe restrictions and mutual completeness cannot be checked by testing types alone. |
| Nested inductive group | Checker contains a full specialization/reconstruction path; plan source support, then targeted qualification before release claim. | `_nested` naming, auxiliary recursor maps and injected temporary declarations require relocation and whole-group fidelity. Do not claim coverage just because a variant exists. |
| Safe recursive functions | Accept actual kernel terms produced through recursors/well-founded encodings and checked ordinary ordering. | Do not admit arbitrary cyclic value equations or bypass cutoffs because Lean source said `termination_by`. Imported certificate must attest the actual compiled declarations. |
| Unsafe/partial/plugin code | Refuse in mathematical relation. | Source elaboration/tactics may be useful external producers but need hostile-code isolation; a well-typed certificate does not sandbox their execution. |

New inductives are essential to root's proposed syntax/fold/fusion workload and
are **not** deferred behind an F-closed substitute. The first actual case should
include a new list-like syntax group with its constructor/recursor semantics,
not merely theorem wrappers around the old foundation.

Atomic group loading may carry more metadata than one queried constructor needs.
That is charged selected semantic work, not a scan of all mathematics. More
fine-grained certified recursor openings would be a separate audited optimization.

## Exact first implementation map

All listed edits require a fresh root-selected v5 source copy. Never edit the
inspected used predecessors. Suggested ownership is mechanism author for the
following relation/checker seam; root for installers/controller integration;
assurance for independent controls/review.

| Fresh equivalent source | Consequential edit |
|---|---|
| New `module_codec` / `module_manifest` | Versioned canonical relative-reference descriptors, group/spec commitments, descriptor openings, namespace relocation and bounded shape checks. Root selects language/location before implementation. |
| `guest/src/journal.rs` | New module conclusion/domain/profile; exact imported module selections and strict rank descent. Do not reuse v4 kind constants as if they certified arbitrary declarations. |
| `guest/src/relation.rs` | Authenticate imported/local roles, map exact module identities, construct selected environment, skip only certified imported checking, check all local groups and bind exact conclusion. Replace F-closed-only and no-cross-output restrictions with checked ordered/module rules. |
| `guest/schema.json` and fixed policy | Support exact local/import descriptors and safe Opaque/group records. Preserve relevant metadata currently omitted/ignored by parser in explicit canonical commitments. |
| `checker/src/env.rs` | Body-presence representation preserving kind/hint; exact missing-vs-cutoff distinction; demand accessors. No unchecked definition-to-axiom conversion. |
| `checker/src/tc.rs` | Recognize certified absent Definition bodies in delta; new local declaration checks cannot skip values. Route lookup failures to exact demands and preserve existing inference/conversion semantics. |
| `checker/src/parser.rs` / `util.rs` | Parse authenticated stubs only through a role-bound entry point; reconstruct arena/cutoff/group maps; distinguish imported from new without trusting input flags. |
| `checker/src/inductive.rs` and raw lookup sites | Preserve whole-group checking/temporary extensions; inspect and close direct `declars.get` bypasses. Never mistake missing group data for a checked smaller group. |
| New native module preflight adapter | Conditional diagnostic output `Checked/Need/Refused`; bind exact witness. Native import authority separately gated by real verified receipt set in public controller. |
| `guest/src/main.rs` | Same relation consumes final finite witness; recursive `env::verify` for actual selected imported module receipts; commit new module conclusion. No fetch/retry/network in guest. |

Relevant direct lookup sites include `tc.rs:96,104,116`,
`inductive.rs:9,13,45,54`, parser finalization at `parser.rs:456`, and
`EnvLimit::ByName` lookup in `env.rs:251`. A patch only to `get_declar_val` is not
a complete demand implementation. Pretty-printer lookups are not mathematical
acceptance but should not accidentally become hidden source dependencies.

The exact fresh copy/source inventory, pseudocode data schema, finite limits
and implementation ownership must be adopted by root before editing code.
No whole kernel rewrite, global ledger, mutable naming registry, new routing
system or unproved optimizer is needed to decide this seam.

## Decisive controls and stop conditions

Before any expensive certificate generation, native/model controls should show:

- New inductive syntax group plus fold/fusion checks under the selected relation.
- Two independently authored modules with the same human names merge via distinct
  qualified identities; one exact shared import coalesces without reinterpretation.
- An imported transparent body is absent and unused: local checking can succeed
  without body work; a demanded body instead yields NeedBody, never success or
  ordinary inequality from the missing case. Supplying exact certified bytes
  reproduces the complete-environment result.
- Missing type declaration, wrong body hash, wrong module receipt/root, stale
  kind/hint, swapped universe parameters, partial inductive group, counterfeit
  recursor rule, local forward/self reference and circular parent rank all refuse.
- A new unproved theorem or incorrect local definition cannot be mislabeled as
  an import; synthetic journals cannot create public mathematical acceptance.
- A deliberately increasing demanded chain stops cleanly at the cumulative
  budget/round ceiling, retaining every attempt and emitting no accepted artifact.
- All parent receipt identities and selected declaration openings are bound to
  the final native/guest witness. Receiver failure never publishes success.

Native structural controls and a conditional successful relation are necessary,
not sufficient release evidence. Actual new image build, recursively resolved
receipt production, fresh cold receiving, hostile-input containment, independent
checker correspondence and public reciprocal use remain subsequent obligations.

Stop/redesign if implementing demanded imported definitions requires pretending
their bodies are axioms, or if checking one selected local extension necessarily
loads every imported proof/manifest ancestor. Stop any blanket full-Lean claim
until actual supported declaration/group and foundation coverage is justified.
The mechanism is intended to remove mandatory proof-history work and undemanded
transparent-body work—not all selected semantic work or arbitrarily hard conversion.

## Implementation checkpoint: actual source, central gates still open

### Current receipt-wrapper slice

Root adopted the actual native positives7/7 and independent controls7/7. This
qualifies the conditional native seam, including the new Tree group, imported
theorem proof omission, genuine missing-body demand and false-new-proof refusal;
it does not qualify certificates. The exact 413-row/22-declaration zero-axiom
foundation is adopted under D06. Build lifecycle failures remain failures even
where a produced executable was separately selected for diagnostics.

`software/v5/modules/receipt/` now supplies the source-only real wrapper:
strict canonical hashing, exact foundation/semantic-policy binding, a new
216-byte module journal, parent/group/body authentication, same-row native
correspondence and checking, and guest `env::verify` for every parent statement.
Independent review found no static blocker in the eight core files. The native
CLI, producer helper and disjoint cross-language control runner are additional
source for root-selected bounded compilation and binding diagnostics. Their
API/build map is in receipt/README.md and NATIVE-BUILD-PLAN.md. No new guest
image, resolved receipt or mathematical admission is claimed by this checkpoint.

Root owns actual FoldFusion new-policy fixture reconstruction through
PrepareReceiptWorkload; this lane owns only `witness.make_input` and journal
decoding. Assurance owns independent full-relation boundary vectors. This
separation avoids a duplicated fixture generator or duplicate math campaign.
The semantic policy excludes receipt-performed state and image identity; old
conditional-policy ModuleIDs are not reinterpreted. Final receiving must pin
the adopted actual image and verify a non-Fake, non-dev, fully resolved receipt.

Root next selected SOURCE implementation of the concrete crypto integration.
`receipt/src/bin/module_host.rs` now supplies actual strict receipt handling,
new-profile framing and a single-execution coherent proving capsule over the
retained segment/lift/join/resolve backend. The capsule and checkpoints remain
untrusted witnesses; final full application verification binds adopted image,
exact journal/witness and empty assumptions. Host/receiver source is not yet a
compiled/qualified program. Reviewer identified and source corrected a real
Segment.po2 usize/u32 comparison mismatch before any build.

`receipt/build_guest.py` and `guest_graph.py` implement a source-only finite
offline guest preparation/build path: exact selected revised checker/source,
root-only Cargo lock rename, and full normalized graph equality except the
new root/library unit/edge. All external package versions/features/profiles/
edges remain bound. Root selects actual compilation separately under
GUEST-BUILD-PLAN; there is no guest/proof launch by this lane.

Independent reviewer completed host/build/graph source review with no remaining
blocker after the po2 comparison and Cargo-URI expectation corrections. Exact
root-requested guest-build01 selection is now prepared at
`experiments/v5-local-checks/guest-build-01-selection.json`, SHA256
`5ef8613f79c7ddb47704fa0930dfaaa854b3df32f15f2cc78ea44338202d8f6a`.
It binds39source files/515056bytes,eight adopted preparation records and the
reviewed finite1800CPU/wall,4096MiB,eight-process,16GiB profile. Required runner
interpreter is the held `D:\Python314\python.exe` with `-B -I -S`, not an
arbitrary relocated Python. Root retains review/launch authority; no guest or
proof run was launched by this lane.

The separate module-host-metadata01 selection was read and its five direct
extern paths AND hashes matched to the adopted collection host LINK-INPUTS.
It uses host serde-c8458b918a5c64a0 and serde_json-9fcbc8f7ff06ebf5, which are
required for SDK Receipt/Segment serialization. Two host dependency search
paths and all shared journal/hash/policy/commitment source files are selected;
Nanoda is deliberately not a host/receiving dependency. This is a selection
inspection, not compiler success or a second toolchain census.

Root's actual module-host-metadata01 failed with a typed SDK boundary:
`InnerAssumptionReceipt::Succinct` requires `SuccinctReceipt<Unknown>`, while
verified public receipts supply `SuccinctReceipt<ReceiptClaim>`. Actual failure
is retained: exit1,0.53125JobCPU,zero active processes. The mutable host source
now uses the SDK's exact `into_unknown()` conversion, retaining all seal/hash/
parameter fields and the claim digest, with an explicit digest-equality guard.
Source SHA is `07f35f5ea4772641fe900d5b6551e4fb6c087cb6609674d21126c476a221b102`.
Fresh metadata02 selection SHA is
`3a2541a71becec1393a1f24621190bc246aeb1017d0930058f0425a1ebf833c8`;
argv/runtime pins/finite limits are unchanged, only name and repaired source
pin differ. Root owns its review/launch. Guest selection is unaffected because
the native host source is deliberately excluded from that build.

Metadata02 subsequently PASSED actual compilation with zero diagnostics and
clean closure, 0.484375 Job CPU seconds. This qualifies Rust metadata only, not
an executable or receipt. Guest-build01 failed before commands/source snapshot
at an inherited census metadata bug: `pruned_aliases` is a list, not a numeric
budget counter. Its 48.96875 controller CPU and 178.9271316 wall seconds remain
charged. The repaired adapter sums only the three validated integer counters
and retains alias metadata independently; it does not weaken alias checking.
Adapter SHA256 is
`1f8b7cd8fac046297120af9393b02bc6469ed4d7854125c432b7dfa38cc96d38`.
Fresh guest02 selection SHA256 is
`86e38250bf1f4241f081ab13893e0eacce9e41411d70d204c46722171a707113`.
All other source/preparation pins and limits are unchanged. Root launched this
independently reviewed fresh attempt; no successful guest is claimed here.

`receipt/build_host.py` now adapts the retained successful collection linkage
to the exact new five-source/five-direct-extern host. Its finite lifecycle
allows cleanup only of exact Job-owned VCTIP processes with their reviewed
image path/SHA; unknown descendants refuse. No backend rebuild is selected.
Independent review cleared the seven-source host01 selection SHA256
`761d12fe9c8b310018f41bf018d619084ecffa5a410c9402dc4b3f409fdadf12`.
Root launched it with the unchanged finite 600 worker-CPU/phase-wall seconds,
900 allocation-wall seconds, 4096 MiB, eight processes and 12 GiB storage.
Actual host01 subsequently passes independent review: compiler exit0, no
diagnostics or telemetry cleanup, zero active Job processes. Exact executable
is 66,621,952 bytes with SHA256
`e3b357bb719db9c3e02fa65fde704e0cbd4dd73f48ee0157a6bf1e55dc5c9190`.
Its result SHA256 is
`47c9c31aeaa30edd0c294f10ec90020bad702ec24157305498395edee76133d5`;
122.015625 Job CPU +20.296875 controller CPU and 241.1658761 wall seconds are
charged. This is an actual linked host, not guest/receipt success.

Root separately authorized exact post-hoc recovery of guest01's pre-repair
adapter under `experiments/v5-local-checks/guest-build-01-recovery/`. Recovered
build_guest.py is 14,038 bytes, SHA256
`64987882ed2a6a34c99cbe98cd1c9e273a2055b84708d275e400fb77af9dbfec`,
matching original selection01. RECOVERY.md explicitly distinguishes later
reconstruction from an original launch snapshot; failed result/current02 bytes
were not modified and the recovered script was not executed.

`receipt/assemble_guest.py` and IMAGE-ASSEMBLY-PLAN are source-reviewed for a
separate actual-success-only assembly step. The adapter requires the exact
closed successful new guest result/ELF, retained qualified assembler and
kernel, checks all pins before and after, and reports file SHA separately from
actual image ID. It executes no guest and creates no certificate. The actual
assembly selection awaits the new guest's successful result and exact pins;
review is conditional on root's bounded 120-second/1-GiB/two-process outer Job.
Output caps in this adapter are checked after capture, so this outer process
containment remains necessary. No old failed or used evidence is rewritten.

Guest02 subsequently PASSED the full actual build and final rebinding. Exact
new user ELF is 1,402,284 bytes, SHA256
`d8a767b911f008a8f30590f6465f6b58c6273e95b8993b36a75d8ad070119fca`;
RESULT SHA256 is
`ddfc4395e06b7f0ffb258169a746ec4d8283cab00be9d21a810715c6cdba11ee`.
Its Job closes with zero active processes; 209.5625 Job CPU +216.046875
controller CPU and 422.9368438 wall seconds are charged. Exact graph comparison
allows only the renamed root plus one library unit/edge (296 rather than295
units). Root reaped/adopted the result; independent actual audit passed. The
reviewed cleanup policy terminated one exact owned/hash-pinned VCTIP process,
PID21784, and observed its exit. Final closure is clean, not unassisted.
No guest execution, certificate or image adoption follows from compilation.

Actual artifact pins now permit `module-image-assembly-01-selection.json`,
SHA256 `7a412d6499608226c6f381f9c04dbed865a076e93cb3c5b546b84afaaed3e0e0`.
All three source/seven runtime pins were rebound; output is fresh. Selection
uses the reviewed 120 CPU/120 wall seconds, 1024 MiB, two-process outer Job.
It awaits exact independent selection review/root launch; this lane does not
launch it. Fresh output is `experiments/v5-local-checks/module-image-assembly-01`.

### Narrow public offer integration source

Root additionally assigned this lane a bounded entry-path harness while the
base execution screen proceeds. `software/v5/transport/offer_integration.py`
copies the exact retained compressed DB `0871e195...d4d0fea`, derives namespace
and symbolic theorem/equality features from the prior old-policy bundle, then
makes exactly two real HTTP calls: offer without any known/injected snapshot
ID, followed by a page using only the authenticated offer's SID and first
nonempty partition plan. No index status/SID is inspected by the consumer and
no direct summary query supplies a hidden bootstrap. Returned records are
authenticated index candidates, explicitly not mathematical acceptance.

The single shared session permits two requests, one provider/snapshot/page,
32 examined rows, eight candidates, 139264 reply bytes and 15 seconds. The
harness requires actual candidates, exact client/server request/reply/header
accounting, one charged snapshot slot and no leaked provider/client reservation.
Original index/bundle bytes are rebound after clean provider shutdown. Existing
summary helper code is reused unchanged; no rebuild/failover/Lean/proof test is
repeated. The fresh outer selection is
`experiments/v5-local-checks/offer-public-integration-01-selection.json`, SHA256
`72f13c0e1c80694503c2a3e8e9c73e14f1fecb599c65e33c0089e7e7b5723587`.
Fifteen source/twenty runtime pins match, with 45 CPU/90 wall seconds, 1024 MiB
and two processes. Independent source/selection review and root launch are
pending at this checkpoint; this is not an actual passing result.

The evolving implementation is `software/v5/modules/`, with detailed source and
trust boundaries in its API and `native/CHECKPOINT.md`. Root launched the
15-contract structural model and eight native-row bridge controls once; these
are not mathematical tests. The first revised native checker source snapshot
passed metadata compilation with no diagnostics; it has not thereby run.

The source now includes owner-aware source→codec→native translation, original-
kind body demands, conditional import/new roles, and independent Rust raw-row
descriptor correspondence. New correspondence compares full inductive metadata
before parser loss, exact body expressions and qualified names/universes; it
returns explicit **undischarged** hash equations and cannot authenticate receipts.
The same-input diagnostic CLI then parses/checks those rows, binding exact
matched import/local roles. Actual linked/native workload controls, genuine
hash/receipt/guest integration and public reciprocal use remain separate gates.

Review corrected a real nested fresh-name probing regression without weakening
semantic missing-record demands. Review also removed quadratic descriptor-to-
group scanning. Root's actual Tree workload is nonnested; neither source repair
nor compiler success qualifies nested-inductive runtime behavior. No frozen v4
or predecessor source/evidence has been edited or rerun by this lane.
