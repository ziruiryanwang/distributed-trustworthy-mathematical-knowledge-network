# Ordinary reference matcher05: actual public capabilities

## Selection and preserved baseline

Root selected only a fresh source successor after the one exported-view census
completed. Both actual views had 60 missing names and 153 axiom-shaped records
among 590 observed names. The fixed basis accounted for 59 missing private
helpers; the selected private `hidden_low` theorem was also absent. The public
`flip_low` theorem was axiom-shaped in both views. `Flag`, its generated group,
`casesOn`, the matcher and exposed `flip` retained their original record kinds.
Those observations establish shapes, not exact semantic correspondence.

Fresh source: `software/v5/ordinary_baseline/OrdinaryReferenceBase05.lean`.
It imports the unchanged, already built `BaselineArtifactCore04` helper. Source04
remains byte-identical at SHA-256
`c7c0636b7252a3f62d277bb7497a14f7686b7ec61fdd722d6bb05dbba0ca5b19`.
No build, native operation, source export, snapshot copying, owner registration,
package operation or Git mutation is selected or performed by this author.

The independent semantic argument and audit belong to
`ORDINARY-REFERENCE-DELTA-CONTRACT.md`; this note records the implementation and
schema. Root owns `reference_report02.py`. Cold-intake owns the later narrow
three-command matcher build and retained-input continuation adapters.

## Exact changed relation

Private matching is preserved: the full fixed 581-name foundation is compared
to the pinned legacy inventory; each selected complete ordinary unit is decoded
with the existing allowed-declaration policy, compared to its exact private
frontend and kernel records, and checked for closed private dependencies.

`MatchedUnit.singletonAbstract` replaces the theorem-only eligibility bit.
Only a safe definition, theorem or opaque descriptor whose exact output array
is `[own name]` and original `all` metadata is `[own name]` qualifies. Public
axiom-shaped views must match the exact original name, ordered universe names
and encoded type. They receive a distinct projection label; they are never
reported as full computational records. Every non-axiom public record still
requires exact ordinary inventory equality. Inductive, constructor and recursor
records cannot use singleton abstraction. Existing foundation axioms/quotient
primitives retain their explicit exact original policy.

The source now includes name and actual view in public record mismatch and
abstraction failures. It emits a `PUBLIC_BASIS_COMPLETE` phase before traversing
selected public units, making future failures distinguishable from basis work.

## Public basis availability and closure

For each fixed name, matcher05 validates the private frontend against the exact
private kernel original, then independently checks each present public frontend
and public kernel record. An absent public record is reported as absent, never
manufactured as an axiom. A mismatching present record refuses even when it
would later be excluded from the usable basis.

The existing semantic scanner collects the union of both actual public records'
dependencies. Full records contribute their bodies and rules; axiom-shaped
abstract interfaces contribute only their actual types. Inductive metadata,
constructor owners, recursor rules and implicit literal roots remain scanned.
A dependency outside the fixed basis refuses under this deliberately conservative
profile; selected later units do not retroactively justify a foundation record.

Let `C` be the names present in both views, and `D(n)` this union of dependencies.
Start with `U = C`. In fixed inventory order, remove a name whenever
`D(n)` is not contained in the current `U`. Repeat until no removal occurs.

This returns the greatest dependency-closed subset of common availability:

1. At termination every retained name's dependencies are retained.
2. If `T` is any closed subset of `C`, no deletion can remove a member of `T`:
   its dependencies were members of `T` and are preserved inductively.
3. Every changing round removes at least one fixed-basis name, so there are at
   most 581 counted rounds. The final unchanged pass is not counted.

This preserves supported cycles; it is not an acyclicity requirement on
mathematical declaration dependencies. Selected public-unit traversal may stop
only at this `usable_basis`; a private-basis name removed by the construction
causes an explicit refusal if required by a selected public interface.

The private, basis and selected-public scans share the existing aggregate
20,000,000-node and 262,144-edge ceilings. Public basis records are compared and
scanned once per view; the deletion loop reuses only finite dependency sets.

## V2 report contract agreed with root

Request schema and fields are unchanged. Report schema becomes
`DMKN_ORDINARY_REFERENCE_BASE_REPORT_V2`. Every old top-level field remains,
including separate frontend/kernel projections on selected public outputs,
`checked_units=0` and `added_names=[]`. Five new fields are:

- `public_basis`: exactly 581 rows in fixed inventory order.
- `usable_basis_names`: the surviving names in that same order.
- `basis_scan_nodes`, `basis_edges`: added scanner work, excluding private and
  selected-public work; all three categories sum to the aggregate ceiling.
- `basis_pruning_rounds`: changing rounds only, between zero and 581.

Every basis row has exactly `name`, `kind`, `level_params`, `projection`,
`kernel_projection`. A projection is `full`, `erased_singleton_theorem`,
`abstract_singleton_definition`, `abstract_singleton_opaque`, or `absent`.
The last label is legal only for basis rows. The two row projections already
encode availability, so no redundant availability-name arrays are added.

Important legacy-format distinction: fixed seed inventory field 2 is a universe
**count**, not ordered names. The report emits actual original ordered names
through `DeclCodec.paramsJson original.levelParams`. Root's binder checks their
shape, uniqueness, bounds and count against that legacy field; the live matcher
establishes exact equality between original and actual record views. It must not
compare the array directly to the old integer or pretend the old inventory
authenticated particular binder spellings.

The report is conditional correspondence evidence only. It is not portable
proof authority, and parsing it alone does not establish the greatest-subset
computation. A later protected registration must bind the selected live event,
original artifact/support identities and current complete private warrants.
Future delta decoders must authorize only this usable basis and registered
nonbasis frontier, not silently retain permission for all 581 private names.

## Source review status

The initial source-only implementation is complete and self-reviewed for the
new fields, actual Lean `Std.HashSet.erase`/`Array.filter` APIs, existing compiled
record-layout patterns and report grammar (no boolean/null additions). The
independent reviewer is checking the semantic relation and primitive dependency
details. Final source hash and clearance follow that review. No build or runtime
success is claimed here.

### Final source candidate and primitive-closure correction

Final source candidate SHA-256:
`ec8248e4f96e9dd39bc78cb3e89ac0c5057d17f459dc152555d84678a5444c09`
(602 lines). Root selected one additional source-only closure correction after
the author's and independent auditor's source inspection: every quotient record
adds all fixed `BootstrapProbe.quotNames` and `Eq` to its semantic dependency
set. The earlier all-581-public-presence requirement had supplied those primitive
dependencies implicitly; a partial usable basis must record them explicitly.
No quotient computation rule, signature, axiom policy or private warrant changes.

The author checked `BootstrapProbe.Scan.refs`, `Std.HashSet.erase`,
`Array.filter`, original codec field layouts and the report assembly against
pinned source. The newly added records use the same compiled04 newline/comma
layout patterns. No Lean parser/compiler was launched for this source check;
independent semantic clearance and the fresh retained-core three-command build
remain separate gates.
