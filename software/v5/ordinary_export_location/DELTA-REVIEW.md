# Advertisement delta: independent source review

2026-10-28, growth_design_audit. **PASS for the pure proposal boundary.** No
runtime, module import, database, network, owner or native experiment was run.
This does not qualify publication, the operator, or the complete location path.

Reviewed `advertisement_delta.py`, SHA-256
`6c67a896bfe97256125dc417bbc97b2e8feb41ac2da89074f471a8dfbc02cd34`.
The selected baseline reader is the current package's
`reference/baseline_bundle.py`, SHA-256
`e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6`;
its manifest reader and the existing portable evidence/identity definitions were
read at their relevant boundaries. Final operator packaging must pin that
ordinary codec closure, as for other pure roles.

## Identity and coverage argument

`manifest()` binds the supplied canonical manifest to its caller-selected hash
and current SemanticID. The reused reader rejects duplicate UnitIDs and fixes
the ordered unit census, raw sizes and hashes. `prepare()` requires that exact
number and aggregate size of raw byte strings; each ordered entry is checked
against its raw hash/size and the portable parser's recomputed UnitID/SemanticID.
Consequently, a proposal row's name comes from an actual parsed declaration of
that exact unit. Its ExportID is recomputed from that SemanticID, UnitID and name.

Iteration is over every declaration in every supplied unit, not the contribution
report's target list. Support-only exports are therefore included in all-output
mode. Explicit-subset mode accepts at most 4,096 distinct syntactically valid
ExportIDs and requires exact equality with the discovered selected set; unknown
IDs cannot disappear silently. Output order is the manifest/declaration order.
Duplicate selected identities refuse. Reported omitted count is the actual
scanned declaration count minus selected rows, not a claim about the rest of the
commons. An over-cap all-output selection refuses rather than truncating.

**No additional mathematical or target-list input binding is needed for these
inert proposals.** The manifest hash, exact ordered unit pins, current semantic
binding and returned row identities already identify the supplied input and
selection result. The proposal's own canonical bytes can be hashed when persisted.
Binding an earlier human target, owner acceptance report or source project would
not establish current custody and is not required to derive an export location.

The approved custodian endpoint and current service grant deliberately are not
in this pure artifact. The later owner-controlled publication path must select
them explicitly, validate the proposal input, then perform the selected exact
locator readback and compare SemanticID, ExportID, UnitID and name before issuing
the corresponding publish command. This artifact has no authority to supply an
endpoint or waive that readback.

## Bounds and limits of this pass

The supplied evidence is bounded to 256 units and 8 MiB. Each unit is parsed once;
aggregate nodes/import edges and at most 65,536 declaration visits are checked.
At most 4,096 rows are retained; incremental proposal-byte accounting is followed
by a bound on the complete canonical document of 2 MiB. The manifest parser also
retains its finite manifest and batch ceilings. Budget callbacks occur before
manifest work, around each parse, per declaration and before returning. These
are byte/structure/cooperative-work bounds, not process-memory isolation.

This helper does not reproduce every native baseline batch-construction bound
or check mathematical derivability. Neither is needed to compute advisory
locations from bounded, valid portable syntax. The output explicitly records
`custody_checked=false`, `published=false`, `mathematical_acceptance=false` and
an inert-identity assurance. It performs no effects before or after return, so
an exception cannot leave a partially published set.

Small changed-boundary controls can later cover all-output versus subset,
support-only inclusion, wrong unit order/pin, unknown selection, output caps and
budget refusal using retained evidence. A repeated Lean or certificate campaign
would not add evidence about this helper.
