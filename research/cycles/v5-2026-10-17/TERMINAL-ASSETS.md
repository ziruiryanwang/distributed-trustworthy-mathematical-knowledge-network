# Genuine terminal adapter: selected assets and real owner construction

2026-10-17. Author `v5_growth_decision`; scope is only fresh
`software/v5/client/terminal_assets.py`. No execution, imports, test, build,
proof, network or Git mutation. Independent review required before use.

Current source:19,562bytes, SHA-256
`ac81eb61db88112619aea7ed90dc3645a98e1def368c75045622747a2768a445`.
After source review, a requested inert `receipt_identity` field was added so
the strategy binds actual carried receipt bytes/hash to the selected asset,
not merely to the same H. No other source behavior changed by this addition.

## API shared with strategy

`Assets(context)` exposes immutable bytes `foundation`, `header`, scalar
`foundation_sha256`, `aggregate_image`, and owner-selected `ports`/`calls` data.
`receipt_identity` is the inert `{bytes,sha256}` of the exact supplied receipt.
Methods: `configuration()`, `grant_limits("B"|"C")`,
`owners(workspace,grant,phase)`, `origin_material()`, `author_input()`,
`expected_journals()`, `expected_second_spec()`.

`calls["admit"]` contains native_cpu_seconds, receipt_cpu_seconds, wall_seconds,
memory_mib; `calls["author"]` contains cpu_seconds, wall_seconds, memory_mib.
These are selected allocations, not measured duration claims.

`origin_material()` returns exactly:

```text
terminals: [{module: ModuleID, packet: bytes}, ...]  # BASE and FIRST only
groups: [{module: ModuleID, opening: authenticated_group}, ...]
bodies: [complete DMKN_MODULE_BODY_V1 response, ...]
first_export_name: [["s","OwnerV5"],["s","fold_map_received"]]
```

This origin has12 groups/11 unique bodies; the consumer fetches only its own
demands. FIRST witness rows/proofs are stripped. The origin has structural
custody only, no accepted mathematics. `author_input()` returns source string
and roots, to be called only after B's genuine acquisition. Evaluator-only
`expected_journals()` has uppercase BASE/FIRST/SECOND byte values;
`expected_second_spec()` reads the retained corrected reference only after
authoring and returns its local interface, not a witness equality obligation.
Phase separation is enforced by the trusted strategy, not a hostile sandbox.

## Future exact parameters, no default receipt

The future launch's parameters are exactly:

```text
schema: DMKN_V5_TERMINAL_ACTUAL_OWNER_V1
assets: map of {path,bytes,sha256} pins
ports: {bootstrap,origin_location,replica_location,readerB,readerC,
        origin_http,replica_http}
allocation: {B_wall_seconds,C_wall_seconds,controller_cpu_seconds,
             receipt_cpu_seconds,native_cpu_seconds,author_cpu_seconds,
             admission_wall_seconds,author_wall_seconds,
             admission_memory_mib,author_memory_mib}
```

`assets` exact keys are base_bundle, foundation, first_input, source, roots,
reference_packet, header, derivation, aggregate_host, preparation_host, native,
image, frontend, profile, and **receipt**. All but receipt have exact retained
length/hash constants in the source; receipt has no default and must be a
separately root-selected file <=8MiB. There is no capsule, I-receipt or fabricated
fallback. Actual A verification is performed later by B/C, never inferred from
these structural pins. H2 and both single-sibling member paths are independently
bound using existing `B.bind_member`; exact J hashes are checked.

The A receiving host is the existing
`experiments/v5-local-checks/small-aggregate-snapshot-host-build-01/small_aggregate_host.exe`,
6,630,400bytes/hash
`a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05`.
Its source `aggregate_small/aggregate_host.rs:verify` dispatches
`receipt::verify_aggregate` and emits the exact schema/status/fields consumed by
`aggregate_claims.admission_binding.bind_output`. No new host is compiled.
The I module host retained by the preparation profile is only the existing
preparation/supervision constructor dependency; **no I consumer owner or I
verification call** is made.

## Resource and identity boundary

Configuration:32MiB packet/8MiB receipt ceiling, one A claim/two frontiers/one
delta/two edges, bounded semantic stores/index. Each B/C grant:256 public calls,
256MiB submitted input,128 acquisition requests/128MiB reply, one verification
submission,32MiB verification input,16MiB semantic import data. B permits two
direct sources; C one mixed source; both permit3 members/one receipt. Requested
wall/controller/call CPU and memory come from the future finite root allocation.
The sum of the two actual A reservations plus one native/one author reservation
must fit outer CPU; each selected call memory must fit outer memory. This subset
check does not reserve setup/provider/controller headroom; root's whole plan must.

B acquisition CPU is one A; total worker CPU adds one author. C acquisition/total
CPU is one A plus one native. Single mixed-verification CPU is capped at600s by
the existing public acquisition interface. A operation cap is1, mixed cap1 for
both (B never calls mixed receive), preparation cap1 only at B. All owners are
constructed after reserve, under the same grant deadline, with exact A-only
owner pairing. Failed construction attempts cleanup of every constructed owner
and preserves all cleanup exceptions. Successful operation transfers ownership.

The preparation profile is rebased from its pinned retained template to the
actual selected launcher snapshot; digests originate in `context.source_sha256`.
Both actual A/native owner maps include selected source pins, enforce128-entry/
512MiB ceilings, and retain their own required runtime closure. No automatic
source authorization from newly observed hashes and no dynamic source-path
fallback. Actual ordinary/resilient client checks remain intact.

Root still needs the genuine receipt and exact resource/launch selection. This
source does not satisfy that prerequisite, run the gate, or claim growth/release.
