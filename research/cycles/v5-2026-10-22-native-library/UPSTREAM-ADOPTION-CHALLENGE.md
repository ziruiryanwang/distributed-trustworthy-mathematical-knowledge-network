# Upstream adoption challenge: retire code, not just move cost

2026-10-24. `package_continuation`, read-only architectural/source review.
Read UPSTREAM-VALIDATION-REUSE and GROWTH-DEFAULT-ARCHITECTURE-AUDIT completely;
checked current selected 4.34 semantics, installation/catalog binding, codecs,
checked-extension and snapshot sources. Relied on the coordinated pinned upstream
source inspections rather than downloading those complete files again. Only this
checkpoint was edited. No tests, builds, upgrade, installation, state opening or
Git mutation.

## Verdict

**The upstream opportunity is real, chiefly as reduced implementation and
maintenance burden, not an established checking-speed improvement. Prefer its
native data model for a new, narrowly bounded cold-validation adapter; do not
translate every result through our old V2 interchange or replace the existing
warm owner by an upstream process exit code.** Preserve the current 4.34 lane
unchanged while that source boundary is decided.

Upstream already provides generic export, parsing and kernel replay. Recreating
those in another new protocol is unnecessary if a thin local policy guard can
express the required assurance. But generic derivability under supplied axioms
is not our exact-foundation claim; source-supported policy differences cannot
be hidden behind the upstream project's name. Native package authoring/API and
receiver assurance should remain separate, as the default-architecture audit
recommends.

The current clean facade can close as optional-lane source cleanup. This review
does not justify investing in its next package merely because that is possible.

## First-pass replacement and retirement map

Here “replace” means avoid maintaining the analogous implementation in a new
upstream-native validation lane, not delete frozen old code or change old IDs.

| Current responsibility | What pinned upstream can supply | What genuinely retires, and what does not |
|---|---|---|
| Expression/name/level serialization and declaration parsing: OriginalExpr, OriginalDecl, corresponding Python wire validators | LeanExport Basic/Parse/Json | A new lane can avoid a second bespoke expression/declaration wire codec. If it must emit/read old V2 bytes, those codecs/validators remain and translation is additional work. |
| Generic selected closure export: OrdinaryExport, BaselineExporter and extraction plumbing | `dumpEnv` recursively exports selected dependencies and groups | Generic traversal/serialization can be delegated. Receiver-relative frontier cuts, exact old seed comparisons and our existing framed missing-proof exchange are not supplied. Do not claim all current exporter code disappears. |
| Reconstruction/kernel replay: CheckedExtension and fresh cold checking | Lean.Replay plus LeanChecker from-export | Generic replay/generated-constructor checks can be reused. Axiom/primitive policy, target coverage, exact input/outcome binding and finite caller bounds remain our responsibility. The current code already calls Lean's kernel, so upstream is not replacing a separately implemented theorem prover. |
| One-time basis validation and repeated local use: BootstrapSupport, LocalSnapshot, protected roots/anchors | Fresh replay can contribute to the initial validation event | No inspected upstream persistent warranted-frontier protocol replaces warm snapshots/anchors. Exact old records are not portable upstream receipts. A future local cache must bind its own actual event; no claim of warm incremental validation follows from fresh replay. |
| Reconstructing ordinary modules from checked declarations: module export/exposure/anchor helpers | Normal approved Lean packages remain the API plane | Default package-native work can avoid demanding this reconstruction at all. Upstream inert export does not preserve frontend registrations or prove that arbitrary later imported binary/plugin bytes are the validated declarations. |
| Resource control, exact policy/version binding, local outcome records, discovery/custody | Some source-execution isolation in Linux lake check; no equivalent whole project protocol | Keep bounded control and assurance distinctions. Existing discovery/custody concepts still apply, but current V2-specific ID/index code cannot silently interpret upstream records. No new index is warranted just to explore the validator. |

This is a substantive reduction only if the new primary path consumes upstream
records directly and leaves the historical custom lane as an unchanged fallback
where needed. Two actively expanded equivalent codecs, connected by a bidirectional
translator and two cache migrations, would increase maintenance. A separate
candidate backend is useful for evaluating a replacement; permanent feature parity
between both is not an assumed product requirement.

## The 4.34 to 4.35 boundary is real

The currently installed `ordinary_semantics.py` binds both foundation and semantic
contracts to exact Lean revision `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b`, the
fixed 456-unit/581-name seed and inventory, and exact expression/declaration
contracts. Its implementation parser accepts only
`LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR`. Unit/export IDs derive from those
semantics; local roots additionally derive from implementation/store/parent.

`NativeInstallation.open` pins selected kernel/runtime/native-support bytes.
`PortableCatalog._open` requires exact stored implementation agreement.
`LocalSnapshot.checkRestored` rejects unexpected module metadata/import layouts.
These are source-enforced refusals, not conjectures about whether a newer binary
might happen to load an old file.

Consequences:

- A 4.35-based adapter is a **new project-supported validation boundary**, not a
  justified in-place update of current owners under the present contracts.
  Reusing the old semantic ID would require a separate correspondence argument
  that has not been supplied; it is not a shortcut selected here.
  Upstream 4.35 itself is not thereby called unsupported; this project has not
  qualified its integration or platform boundary.
- Existing warm state remains useful under its old pinned installation. Preserve
  it; do not modify adoption markers, substitute new runtimes or relabel old
  results. A later independently rechecked result may be accepted by a new lane,
  but that is a new event, not free cache migration.
- Backporting a fork of new exporter/parser code to 4.34 is not automatically
  cheaper: it makes us maintain compatibility patches and weakens the maintenance
  argument. No such backport is established or recommended here.
- Keeping the supported old runtime while evaluating new source does not require
  downloading another runtime now. The version cost is a later adoption cost,
  not a reason to run an upgrade experiment before the contract is settled.

The inspected 4.34 `LeanChecker.lean` already offers compiled-module replay and
fresh replay, but describes itself as an environment-hacking detector, not an
external verifier. Its presence does not supply the newly integrated inert
export/parse/lake-check path or justify treating imported peer artifacts as safe.

## Costs and API compatibility: no free cold or warm path

The current checked-extension code is a small policy wrapper over `addDeclCore`,
not an independent kernel. It requires positive heartbeat/recursion bounds,
forbids new axioms/unsafe/partial declarations, checks all references, rejects
overwrites and compares actual generated inventories. Replacing its call with
Replay while reconstructing all these checks is not a large proven saving.
Generic codec/closure infrastructure is the stronger retirement candidate.

Both current cold export and the inspected upstream exporter serialize a selected
proof closure. Upstream also scans imported constants for recursor information;
fresh replay repeats that closure's checking. There is no ancestry-free cold
verification or amortization theorem merely from changing libraries. Calling
lake check on every theorem application would turn a one-time adoption cost into
a repeated charge. A protected local reuse event is separate from trusting a
remote validator's report, and a new policy/toolchain epoch can invalidate its use.

Likewise, inert upstream declarations do not restore notation, simp databases,
class/instance registration or arbitrary executable elaboration support. Normal
approved packages preserve those interfaces. Mathematical checking and approval
to execute their binaries/plugins are separate decisions; neither an input hash
nor a successful inert check establishes every subsequent package execution's
behavior. Keep that boundary explicit rather than rebuilding all frontend
metadata in another interchange layer.

The migration is worthwhile when avoided codec/replay maintenance and new-library
compatibility work exceed wrapper upkeep, toolchain/platform adoption and any
required retained-lane support. This is a conditional engineering benefit region,
not measured throughput. No unique advantage over Git is required: ordinary
packages can carry the mathematics while our useful layer manages receiver-local
assurance and replaceable discovery/availability.

Linux bubblewrap in the reviewed CLI does not give the current Windows product
hostile-source isolation. Using `--from-export` can avoid the source-build phase,
but parsing/output handling still needs bounded process/input control. Do not
disable a sandbox to turn that platform difference into apparent release proof.

## Root's concrete cold contract: supported in principle

The subsequently appended seven-step relation in UPSTREAM-VALIDATION-REUSE is
read and incorporated. It binds input/version/policy/targets, bounds parsing,
rejects unsafe/partial or unpermitted axiom entries, anchors canonical foundation
records, performs fresh replay, compares actual results and commits only after
clean closure. Its conditional soundness sketch addresses the logical gaps in
bare CLI success. Replay returning an actual kernel environment makes the
post-check conceivable without building a second kernel. This is not a proof
that every honest upstream export passes its proposed equality relation.

The principal remaining maintenance risk is Step 6: requiring all old inventory
and proof-witness conventions could recreate the machinery we intend to retire.
Use no stronger field equality than the advertised new claim requires. An exact
export-byte hash identifies consumed bytes; it is not automatically a canonical
semantic object ID. Selected theorem derivability and checked definition/
computation meaning can be warranted without inheriting every compiler-bookkeeping
or proof-representative identity promise. Where exact proof witness or generated
record identity *is* advertised, its actual correspondence must be established.
Do not weaken a claimed field silently or borrow old V2 IDs. Root's explicit
permission to reject or narrow unsupported identity claims is important here.

## One decisive smallest next source task

**Resolve Step 6's compatibility relation on the pinned upstream data model:**
trace `dumpEnv -> parse -> fresh replay -> actual ConstantInfo` for supported
declaration kinds, focusing only on normalization, mutual/nested groups and
fields retained or reconstructed. Produce a small field-preserved/normalized/
unsupported decision table and the minimal comparison contract justified by it.
This can reveal immediately whether a thin guard suffices or whether it would
rebuild OriginalDecl-style inventory infrastructure. The guard/policy is already
specified by root; do not commission another generic contract-writing round.

Prefer upstream's existing generated-record/comparator operations where their
relation matches the public claim. No serializer, V2 bridge, new index, warm-state
importer, executable adapter, toolchain upgrade or benchmark is selected. If
normalization requires a small explicit mathematical projection, state it; if
preserving the proposed claim requires reproducing export/replay or the entire
old environment model, reject that substitution rather than expand the task.

This focused source task determines whether the new backend actually retires
custom maintenance. It is more consequential than another successful cold
fixture, whose success alone cannot settle the representation contract.

## Evidence scope

Upstream claims use the two coordinated reviews at immutable commit
`eb6cafb7290e8bd5f2937522d8d804f58f02bafc`; no fresh runtime success is inferred.
Current source checks use the selected producer installation's semantics,
admission, catalog and LocalSnapshot files. Source OriginalExpr/OriginalDecl/
CheckedExtension hashes were matched to that installation; the latter is
`4c3f3d600eda6319dd6d4578797e16ae6dc0ab81cf97ca4d7bce014081463ea1`.
No claim of upstream insecurity for its documented contract, public deployment,
performance improvement, automatic migration or completed v5 is made.
