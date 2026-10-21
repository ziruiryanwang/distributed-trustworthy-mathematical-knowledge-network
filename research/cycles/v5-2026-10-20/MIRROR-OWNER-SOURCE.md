# Finite ordinary method-circulation owner

2026-10-20, core_release. Implements root's MIRROR-OWNER-SELECTION using the
current installed 114-source map, without adding a product mechanism. Source
reading and hashing only: no import, constructor evaluation, candidate parsing,
compilation, test, native/proof execution, networking, build or Git mutation.
Independent source review and root's exact finite selection precede any launch.

## Source identity

| Source | SHA-256 |
|---|---|
| `software/v5/examples/mirror_method/owner.py` | `43c3a2eeebcccdfa05c00855887068d98084755e6c5169168dab3787d3208978` |
| New `MirrorInvolution.lean.in` in that directory | `8fbe6639b2040a7be73ca620e799dd6404beba7402bd6ed01ff99639df9d89f7` |
| Unchanged `MirrorInjectivity.lean.in` | `9021d2150caefc7dd85844995ad63e4403237c6804701cc49df6919b9dd5a5f3` |
| Unchanged `method_query.py` | `0ddbc8dac7e60180f3f9aad3216873158d8b2722a9d31c48112e20262298c642` |
| Existing `software/v5/examples/contribution.py` | `ce82e170e1fad04beeb0be8722c89d748e381762b4957dfaf7b5850e2a57495c` |

The readable fixed-target `MirrorInvolution.lean` and all reviewed predecessor
bytes remain unchanged. The new template has one whole-reference METHOD_REF
token, no evaluator address/name fallback. Mathematical source arguments and
initial query independence are in MIRROR-INDEPENDENT-REVIEW.md.

## Finite ABI

Installed ordinary owner entry `owner.py`, synchronous `main(context)`, calls
`asyncio.run(run(context))` and returns 0 only for `COMPLETED`.
Use the installed public distribution run workflow with aggregate runtime mode
and authoring enabled through the ordinary runtime. Three BOOT owner sources:
`owner.py`, `contribution.py`, `method_query.py`. The installed wrapper permits
only Python owner sources, so the two templates are separately pinned input
files, not new wrapper features or BOOT source entries.

Exact parameter fields:

- `schema = DMKN_V5_MIRROR_METHOD_OWNER_V1`.
- `action = explicit-temporary-adoption-and-method-circulation`.
- `runtime_adoption`, `foundation`: matching installed author-enabled adoption
  and pinned foundation; the public wrapper can inject its ordinary sentinels.
- `packet`: pinned retained evaluator packet for provider fixture seeding only.
- `first_template`, `second_template`: ordinary `{path,bytes,sha256}` pins;
  bounded `read_pin` (64KiB each), strict UTF-8. Exact approved template identity
  comes from the reviewed selector, not a hardcoded hash in owner.py.
- `workspace_config`: existing evidence workspace shape below.
- `provider_workspace_path`, `first_workspace_path`, `second_workspace_path`:
  distinct fresh ordinary paths, disjoint from installation/run/source roots.
- `first_domain_path`, `second_domain_path`: distinct fresh ordinary paths,
  also disjoint from all three workspaces; both domain IDs are distinct hex64
  values in `first_domain_id`, `second_domain_id`.
- `first_operation_limits`, `second_operation_limits`, `author_limits`,
  `admission_limits`: exact prospectively fixed dictionaries below.

All destinations and both operation allocations are validated before the first
operation. The second domain/runtime/grant are instantiated only at the second
phase, after first success and closure. Thus its same-process controller clock
does not overlap the first operation. A first failure stops the second, never
creates a retry or reserve renewal.

## Existing API composition

The constructor freezes and saves both BASE/codec-derived exact-type query
alternatives **before any packet bytes are read**. Provider fixture seeding uses
the existing pure `_semantic_plan` extractor: it puts verified structural group
openings, committed available bodies and the raw packet into fresh stores, and
indexes the sole root theorem. This is data preparation, not an issuer.

The receiver function gets only its client, one explicit loopback endpoint and
the frozen query alternatives; no provider-private packet path, root or method
name. It reserves one two-generation envelope, uses ordinary full authenticated
pages and compares a returned descriptor's exact type with the independently
constructed query. A finite miss does not become global absence. Unsupported
partition scope or metadata refusal stops; there is no third query or retry.

The same SemanticReader stages one offered packet, chooses demanded internal
member journals from its actual staged inventory, resolves declarations/rules,
and finishes once with fresh ordinary admission. Interface-only mode preserves
the Tree inductive group's computation rules. `finish` receives only the staged
root as an admission key, not every internal member. Before rendering, the
admitted root and acquired group/descriptor must still match the actual locator.

Every string name component must pass the codec and the narrow ASCII identifier
grammar; each resulting Lean component, including DMKN/Mod/module, is quoted.
The method reference is rendered from the actual admitted module/name. The
second template requires exactly ten module-token occurrences. Both render paths
refuse any remaining token. No arbitrary peer Lean text is interpolated.

First contribution uses existing `contribute_from_context` once for mirror and
involution V. The old context is not reopened. First client/workspace/service
close and its domain is withdrawn. The second provider reopens the first
workspace as ordinary structural custody; no first trust or warrant is restored.
V's actual published identity is an explicit known-dependency input, not authority.

A fresh second owner queries/acquires/admit/imports V and checks both mirror and
involution descriptors. Expected raw V types use **local** mirror references;
only the discovery type hash relocates under V's actual identity. Injectivity
then uses an external V reference and the existing source helper once. Both
outputs' intended descriptor shapes/types are checked in published custody.

The service closes before native admission/authoring, with no subsequent network
charge increase. Each owner must report one import session, one author call,
two admission submissions and one publication attempt. No unsupported assertion
about receipt cache behavior is made. Existing native evidence remains essential.

## Exact bounded proposal

Workspace/config basis:
`experiments/v5-local-checks/interface-view-actual-01-inputs/plan.json`.
Keep its index/module/packet/store limits and default discovery profile. Packet
envelope is the same except `edges=8`; retain `deltas=3`, `claims=1`,
`frontiers=1`, packet16MiB, receipt8MiB, witness16MiB, openings4096, bodies8192,
rows250000, nodes500000, depth128. The DAG is BASE I frontier -> M -> V -> W;
the last packet needs three ordinary native deltas, not the old one-delta cap.

| Allocation | First agent | Second agent |
|---|---:|---:|
| Wall seconds | 210 | 210 |
| Controller CPU seconds | 120 | 120 |
| Worker reservation seconds | 95 | 115 |
| Acquisition worker suballocation | 50 | 70 |
| Client calls | 192 | 256 |
| Input / output | 64MiB / 128MiB | 64MiB / 128MiB |
| Output entries | 1024 | 1024 |

Both acquisition dictionaries: requests128, reply32MiB, verify_attempts2,
verification_input64MiB; worker values as above. Both import dictionaries:
max_sources1, max_members8, max_receipts1, max_calls8192, submitted32MiB,
data8MiB. Helper: modules8/names64/groups64/bodies64/steps256/data8MiB.

Author:45CPU/90wall/768MiB. Each admission:10nativeCPU/10receiptCPU/60wall/
512MiB. First worst prospective admission reservations are20+30=50; second
30+40=70. Author45 then gives worker95/115. These are reservation maxima,
not runtime measurements or additive total CPU claims.

Each query: providers1/snapshots1/requests3/pages2/examined8/candidates4/
bytes384KiB/inflight1/wall90s. First envelope sums additive caps for two queries;
the second has one. Full page: examined4/matches2/bytes128KiB/timeout1000ms/
node_reads50000. Offer maximum128KiB expanded256KiB; no more than two nonempty
partitions are traversed per finite query. HTTP: connections2/requests128/
reply64MiB/operation5000ms. Each phase uses one absolute service/acquisition
deadline of at most90s, including clean stop, bounded by grant/outer margins.

Combined outer envelope: **300CPU/600wall/1024MiB/4 active processes**, with
1MiB stdout/stderr. The outer total is deliberately stricter than the sum of
per-owner controller and worker maxima (450CPU); a run may exhaust the outer
before those maxima. No resubmission follows automatically. Sequential native
workers preserve the selected existing memory caps; there is no RAM experiment.

## Retained inputs and evidence

Current map `distribution-body-custody-01-input.json`, SHA-256
`995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be`, identifies
114 SDK sources; installed release is
`8e93486cadb5806d6470d7a8920803a9a4bad39260dd72f3be3498f699eeeb1e`.
Do not depend on the uninstalled pair planner.

Retained M packet (498641 bytes), SHA-256
`efc96de9cafea117baad14cfd160f42c2a3ad41bf9cb4e6a2dc18a7dad3ffc1b`:

`product-local/v5-distribution-interface-01/evaluator-commons/operations/121800ebd03cd37174e81c1d1bbed5f5e0aec4715d968612db9d7f6f1ba7dad3/preparation/author-1/mixed-packet.json`.

Foundation23313 bytes, SHA-256
`736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`.

The owner exclusively retains `first-queries.json`, `second-queries.json`, both
generated Lean sources, both raw published packets, two full phase reports and
a compact aggregate report in `context.location_workspace`. Full ordinary
native/authoring/publication evidence remains in each new workspace operation.
The aggregate records separately pinned template/input provenance and BOOT owner
hashes. No opaque context/candidate/warrant is serialized. Successful and failed
cleanup/withdrawal are explicit; no state is deleted.

## Claim boundary

If later executed successfully, this supports unknown-ID exact-contract method
discovery, actual interface reuse, a distinct operation/law contribution and
fresh onward injectivity use. It does not establish full-cost speedup, global
recall, new succinct-frontier production, independent hosting, permanent custody
or final v5. Root owns finite execution, actual audit, adoption and integration.
