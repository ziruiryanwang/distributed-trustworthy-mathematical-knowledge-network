# Independent candidate-construction source review

2026-10-23. Reviewer: `admission_event_audit`. Source/theory review only; no
compiler, test, consumer, receiver, catalog operation or Git command was run.

**No blocking source finding for the selected finite candidate-construction
slice.** This applies the authority separation in
`AUTHORING-AUTHORITY-REAUDIT.md` without changing the current receiver's
prepared-map and accepted-parent identity requirements or new-proof checks.
Actual build, source use and successor acceptance are not implied.

## Exact reviewed cuts

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/OwnerConstruction.lean` | `94e85e23442c2ec3640bc3b3a8181486fc25026af6536a55035be16187bbe536` |
| `software/v5/ordinary_lean/OwnerConstructCommand.lean` | `bded743c7ce6a76ebbfcc375dac78c4b240555acf246622ed483fe69d4abdffc` |
| `software/v5/ordinary_lean/ConstructExportCommand.lean` | `6328e2a3d2f0588aaddf5f75d6ad56fb10757de3a847bd4efc2b45f795210260` |
| `software/v5/ordinary_lean/SuccessorExport.lean` | `710622c74f2caced586b6fbc15440893c30dc7379379f159d21e829aecb1f788` |
| `software/v5/ordinary_lean/run_owner_consumer.py` | `75f413c3645506649d8793df50fa25f1468cea40b640c0b4dbd04796a57e1eea` |
| `research/cycles/v5-2026-10-22-native-library/Select-OwnerConsumer.ps1` | `3aa44cad7c69ce3a35940d0f32e3283e604928e02993ae4aa9ed23fd2e9ec8a0` |

The new helper and commands were read completely, as were the new exporter
entry point and plan `OWNER-AUTHORING-CLOSURE-PLAN.md`
`b2cb820cfe2dcce8da4e676dd6aef5960c684307879bbcff7e8dd8a2d466ebdb`.
Removing exactly the new `selectedInterpreted` documentation/function block
reconstructs the prior selected `SuccessorExport.lean` text exactly; its old
API and `bundleBytes` are unchanged. The driver delta against consumer03 consists
of the two imports, two command names, explicit construction/source-map labels
and explanatory docstring. Its request verification/copy and proof body remain.
The selector is unchanged from its prior reviewed cut.

## Demand construction and bounds

`makeIndex` checks the entire bounded authenticated request once: identity shape,
unique names, group/row counts, optional-unit name census, target identity,
byte and encoded-node limits. That is a finite request index, not a census of
the owner or global library. It does not require unused labels to exist in the
owner. Optional theorem proof data may still be parsed/count-preflighted because
it exists in this retained request; it is not decoded or checked as a theorem.

Actual `demand` starts from selected targets. An existing safe owner record
immediately stops traversal without body correspondence or dependency scans.
Only missing signature types or full missing concrete/group declarations produce
further demand. References are collected from those actual construction inputs;
unavailable demanded basis names fail explicitly. No private-name blacklist or
silent one-name exclusion was introduced.

The active group set detects cycles; declared generated self-types are exempted
only through the existing allowed-declaration path. Demand depth, unique finite
indexed groups, added names, signatures/checked-unit total, scan nodes, encoded
nodes and bytes are bounded. Constructed dependencies accumulate in local
immutable environments, so a later failure cannot install an earlier prefix.
Concrete declaration scans include the extra scan performed by `checkBatch`.
Kernel heartbeats/recursion remain finite; the external aggregate supervisor
remains necessary for total runtime, not just individual calls.

## Signature versus mathematical authority

A missing singleton theorem row takes only its accepted parameter/type payload.
The helper canonical-roundtrips that type, demands its real type dependencies,
then calls `addDeclCore` with a safe `axiomDecl` and `doCheck := true`. The actual
result must be an axiom with the exact type/universe payload. This checks
well-formedness of a **scratch assumption**, not the theorem's truth. Such names
are separately recorded as `introducedSignatures`; they are never sent through
the receiver's new-declaration admission as axioms.

Missing concrete definitions/opaques/generated groups use full units and the
existing checked-extension path. Partial existing groups refuse, output names
cannot be overwritten, actual generated inventories must match, and new
theorem-unit replay is expressly refused in this path. The preexisting
`CheckedExtension` receiver axiom prohibition remains untouched.

The returned interpretation labels retain exact accepted IDs but intentionally
assert no whole-owner correspondence. Existing safe local definitions can differ
from the receiver; source construction may succeed while receiver checking later
fails. A locally inserted signature's saved authoring `.olean` is not an accepted
snapshot. These are explicit limitations, not hidden exceptions to acceptance.

## Command state and export collision boundary

`#ordinary_construct` reuses the bounded reader, exact expected header IDs and
sequential group census. Its private plain `EnvExtension` is local/nonpersistent
and additionally bound to `mainModule`. Every fallible IO action and diagnostic
precedes the sole final `modifyEnv`. Only a completely successful candidate is
installed; the getter is bookkeeping, not an unforgeable authority token.

`selectedInterpreted` validates the finite label and introduced-name sets without
looking up unused labels. The existing scheduler serializes complete new units;
only actual reached boundary references are then required to exist safely and
be either imported or tracked as introduced by this construction. Otherwise
`NEW_LOCAL_BOUNDARY_COLLISION` refuses: a newly authored declaration cannot
silently become an old import. The installed Lean `isImportedConst` definition
was checked: it consults the environment's declaration-to-module map, not the
name's spelling or namespace. This origin check is an export discipline, not a
substitute for receiver checking.

`#ordinary_export_constructed` additionally requires same-module construction
state, a current-module actual theorem, a name absent from the interpretation
boundary and a nonempty newly serialized closure. It writes only a bounded inert
bundle at a fresh absolute output path and does not mutate the environment.
Signature names stop at existing accepted IDs rather than becoming axiom units.
Existing generated group boundaries remain conservative; genuinely new groups
still require full atomic construction/export.

## Receiver and practical limitations

The final controller still checks every reached import against both the exact
prepared map and the actual protected parent; it then checks complete new units
through the unchanged worker and commits only after the reviewed clean actual
event. A forged/mistaken construction label, mismatched local meaning or local
assumption does not bypass this. The new commands reuse the old inert bundle
schema without changing its assurance label or claiming proof transport.

The finite 833-label adapter can refuse an imported theorem used by a new local
proof if that theorem is outside the selected prepared map, even if it exists
elsewhere in the accepted parent. Such a refusal would identify a catalog
coverage/export seam, not justify downloading every hidden proof. No worldwide
lookup complexity, cheap arbitrary cold onboarding or guaranteed local-to-receiver
compatibility is established by this source review.

The next useful gate is the actual unchanged substantive consumer proof followed
by independent successor checking. Do not repeat old projection, matcher,
basis-admission or certificate campaigns merely because this new helper exists.

## Focused syntax successor and author checkpoint

Root's subsequent `OwnerConstruction.lean` cut
`04f605717af3b907195756455c2ec645e37e20ce9897c0510f47d7da24895ed3`
changes only `makeIndex`'s return record to explicit assignments for the same
eight fields. A direct comparison against the selected helper01 snapshot
`94e85e23...` reconstructs the new text by exactly that replacement (allowing
line-ending representation in the comparison). No demand, signature, semantic,
limit or environment rule changed. The source review therefore covers this
syntax-only successor; it is not a claim of its build outcome.

The completed `OWNER-CONSTRUCT-COMMANDS.md`
`e2c5aa583dd2e91444c148aa09e8735982f1ad7a335b840f909a498b40c59cf6`
was then read completely. Its source/API, local-state, reached-boundary and
unchanged-receiver descriptions agree with the reviewed code. No additional
runtime or acceptance claim follows from that checkpoint.
