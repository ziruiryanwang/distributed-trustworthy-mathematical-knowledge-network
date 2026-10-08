# Minimal typed-row prototype selection proposal

2026-09-30 UTC; `/root/diversity_author`. Source-grounded proposal only.
Canonical guard PASS; AGENTS/GOAL/current NOW and the complete adopted
PROVED-WORK-REDUCTION-DECISION were read. No implementation, import, compiler,
execution, proof, key access, product change or package census occurred.

Disposition: `READY_FOR_SEPARATE_SOURCE_SELECTION_NOT_IMPLEMENTED`.
Select the authenticated Value-to-owned-row seam, not another encoder/parser
redesign. This removes the normalized text allocation and lexical reparse;
whether it materially reduces proved work remains an empirical question.

## Exact source cut and ownership

All paths resolve below
`E:\Distributed Trustworthy Mathematical Knowledge Network` (R).
The actual current Rust project is
`R\experiments\certified-collection-01\build-01\project`, NOT upstream.
Its adopted SOURCE-MAP.json is
`3821fa586cbd3f62b71235e5d402eeac93e3d2c526d585eae3a040f8176c0ffa`:
nine guest leaves and31 checker leaves. Guest Cargo/lock pins are
`2ed9be0f93361a8de6a423d6e184944408cc38c0b9637446fed4947bfd4822d7` /
`571bd711fd7ada6cbe18bb248b66c59d5e9879debdce69d0df1606d4ba442975`.
These and the two edited-baseline leaves were actually rehashed read-only.

Root should select a fresh40-leaf copy at proposed
`R\experiments\certified-typed-row-01\project`, verify it against that exact
map before editing, then allow only:

| Owner | Editable production leaf | Functions/change |
|---|---|---|
| Parser author | checker/src/parser.rs | Owned-row wrapper/decoder; extract go1 decode from shared apply; extract parse_export_file finalization into shared finalize; new owned-row entry |
| Relation author | guest/src/relation.rs | Replace normalized Vec/text reader with exact serialization counter and authenticated owned-row retention/consumption in check |
| Root/test author | New experiment-only probe manifests/sources, fixtures, supervisors, maps/plans | Differential correctness and one execution screen; not installed product files |

Baseline parser SHA is
`5b0eaf937857a17be3c944628855231a58d99c07dd0241cae2d43b70e7343b72`;
relation SHA is
`8f3973c4a27a5f7c7dd52ffad4381920dbdf7ac72f2c56e4372905d7cbf32aa1`.
Keep the other38 leaves exact, particularly main/journal/fixed/foundation,
schema/registry, Cargo/locks, tc.rs and all native checking bodies. Independent
reviewer owns extraction/congruence and final maps; root alone selects builds.

## Representation contract, with no weakened authentication

In parser.rs expose an opaque `OwnedRow(ExportJsonObject<'static>)` with private
fields, constructed only by consuming a serde_json::Value through the existing
Serde row decoder. No native pointers, ExportFile or alleged checked declarations
may enter. Establish DeserializeOwned/owned Cow strings by compilation and
tests; prohibit leaked buffers, transmute and unsafe lifetime shortcuts.

Old go1 remains decode-from-line then shared apply(row, diagnostic). New
parse_owned_rows consumes rows through precisely that apply and the same
finalize. Move existing match/finalization bodies, do not reimplement them.
Its small diagnostic argument accommodates existing unsupported-literal error
messages referencing `line`; private wording may differ, acceptance may not.
Preserve row order, line-number increments, BackRef insertion/duplicate guards,
metadata semver, axiom policy and constructor/recursor association.

Relation check retains initial raw Value parsing, exact metadata and every
schema/digest/support/parent/output check. Authenticate each row first; count
its unchanged compact JSON serialization; only then consume its Value into
OwnedRow. Metadata is included. Retain typed rows until ALL authentication and
the derived permitted-axiom Config are complete; only then build native objects.
Do not simultaneously retain the whole Value collection or normalized text.
Existing bounded raw packet/line/DAG/declaration checks bound retention; invent
no stricter row cap without proving it cannot exclude an old-admissible packet.

Use serde_json::to_writer on a checked-count std::io::Write sink, counting
every emitted UTF-8 byte and one newline per metadata/row. Require the identical
4MiB normalized bound at its existing checkpoints. The fixed metadata is already
below that cap. Overflow/errors refuse. Do not substitute raw length, character
count or an approximate JSON-size formula. Keep hash(original packet), journal,
actual selected check_declar/is_prop calls and main's env::verify/discharge exact.
The obligation is `decode_owned(v) = decode_text(serialize(v))`, including
flattened variants, integers, ignored native fields and ordered arrays. Relation
authentication still constrains fields such as theorem `all` that native decoding
ignores. Initial duplicate-key Value behavior remains unchanged.

## Small differential source and oracles

Propose experiment-only `probe-old/{Cargo.toml,Cargo.lock,src/main.rs}` and
`probe-new/{Cargo.toml,Cargo.lock,src/main.rs}`. Both use the retained guest
dependency identities/lock; their explicit Nanoda and relation paths select
respectively the frozen project and fresh candidate. Share one small probe
source recipe; no new dependencies/dev-dependencies, production manifest edit
or Risc0 guest entrypoint in the host probe. Compile offline host-target probes
into fresh external targets. A missing cached host dependency stops selection,
not a network fetch or weaker hashing substitution.

Use exact retained A/B/AB packets and parent-free headers from PREPARED.json /
collection framing-01. Freeze at most24 additional packet mutations BEFORE
execution. Cover normalized-count/Unicode escapes, raw duplicate keys, integer
widths, native decoder unknown-field/BackRef/variant behavior, DAG gaps/duplicate
nodes, universe order, reserved support drift, theorem all, output references,
and the two genuine invalid-member proof inputs. Identify which reach adaptation;
host-preflight refusals are not adapter coverage. Isolate each old/new case in
its own process because BackRef refusal can exit rather than unwind.

Required positive oracle: exact old/new Journal bytes with the SAME test image
field, interfaces/rank/raw packet hash; identical selected-check completion.
Require equal normalized byte count against actual old serialized bytes, equal
typed decoded rows on admitted fixtures, and matching relevant construction
observations (ordered declaration names/roles, universes, DAG/census and groups).
Every old-invalid case must remain invalid at its selected boundary. Mutations
must have fixed expected old outcomes, not post-hoc acceptance agreement alone.
Retained bad-proof cases must actually reach proof rejection. No mock receipt
or host probe becomes cryptographic acceptance. Host differentials plus a
reviewed shared-body extraction are both necessary; neither proves all inputs.

## Build feasibility and single retained-AB work screen

Use the inherited offline toolchain/SDK/build-std/seed and normalized295-unit
production graph, but a NEW build adapter must support the parser overlay:
old build.py allows only four guest overlays and assumes checker unchanged.
Do not edit/reuse that used adapter or old target. Production roots/features/
dependency graph must remain identical after path normalization; test crates
have separately reviewed host graphs. New source maps explain exactly2/40
production leaf changes, not an entire SDK/ZIP requalification.

Prospective separate envelopes: native differential stage300treeCPU/600wall,
1GiB/8active/128cumulative,64MiB output/2048entries; fresh guest cross-build
1800treeCPU/1800wall/4GiB/8active/1024cumulative,16GiB combined storage;
root CPU/memory separately selected (build:300CPU/512MiB). These are exposures,
not guarantees. Prior guest build took349.37wall/264.72 knownCPU with0.945GB peak
Job memory and413 cumulative processes: plausible local feasibility, not a new
measurement. Preserve failures and any explicitly selected telemetry cleanup.

After source/differential/build audit, separately assemble using the retained
driver/kernel and fresh ELF; no backend rebuild. Reframe the exact retained AB
packet with only the newly assembled image in header/journal. One execute call:
`execute <new-image> <new-AB-frame> <new-AB-journal> 67108864 18`, using held
collection host-build-01 driver. Select120treeCPU/240wall/1GiB/8active,64MiB
outputs plus separately pinned input storage and root90CPU/256MiB. Record actual
exit/marker/Job closure and all setup costs; no proof/verify fallback or retry.

Compare against RETAINED AB17301504 padded/15609378 nonpadding/15411179
instructions/66segments; do not rerun that baseline. Continue only if padded
rows<=15571353 AND segments<66, all non-image journal fields agree, bounds/checks
are unchanged and memory remains in the prospectively selected cap. A failure
stops this candidate without threshold/workload adjustment. Trace saving does
not imply proportional proof-CPU or useful-growth saving.

## Image/migration stop gate

Any changed compiled guest/library yields a NEW image; journal layout/foundation
are intentionally unchanged, not an old receipt relabeling. Existing parent
journals and env::verify require SAME image; source04 namespace also includes
image words. Keep old software/receipts/stores/cursors intact. Before any proof
or adoption choose and cost disjoint lanes, genuine recertification or a separately
specified bridge; include availability, reindexing/announcements and maintenance.
No bridge or new profile/package is selected here. Prototype source work begins
only on root's new explicit selection; sealed v3 and prior evidence stay frozen.
