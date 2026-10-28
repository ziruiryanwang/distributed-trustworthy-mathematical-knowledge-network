# Small public discovery step before theory reuse

2026-10-26. Source/data only; no service, network, product import, owner/catalog
or database call, experiment, state mutation or Git operation occurred. Only this
plan is authored. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**Use one existing public loopback service, one stateless formal find and at most
six stateless previews.** No recipient initialization, repeated Std grounding,
republishing or new harness is needed. This supplies an actual public discovery
path before the separately prepared same-owner theory extension. It does not
make that extension an independent-recipient or autonomous-discovery experiment.

## Actual existing state

Let `L` denote the canonical `experiments/v5-local-checks` directory.
Use the already adopted package `L/kernel-admission-package01/distribution/package`
for this unchanged peer workflow; its PROFILE is
`60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b`.
The pending authoring-frontier controls/package are not a dependency of discovery.
Root may instead select its later adopted successor after verifying the unchanged
peer support; do not silently substitute profiles.

| Binding | Exact existing value |
|---|---|
| index | `L/finite-map-index01` |
| catalog | `L/std-kernel-catalog01` |
| custody | `L/std-kernel-custody01` |
| store ID | `fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7` |
| custody quota input | `software/v5/ordinary_std_intake/custody_limits.json` |
| index latest recorded snapshot | `4c641b21a09a37b31a96fce6c31761c4e312619f26c36fba3407d076f6714c78` |
| index namespace | `d966de54aa32c6cd059ab9553a0968a320594a63561cadf742cca6265858079c` |

The quota is the existing objects4096/exports8192/logical_bytes134217728/
db_pages65536. Reopen the index with exactly its publication limits:
max_objects32, max_postings4096, max_features512, max_snapshots33,
max_logical_bytes16777216, max_db_pages4096; `create:false`. No access_pairs
field was used at creation, so do not add one when reopening.

The adopted saved publication RESULT is
`L/finite-map-publication01/publication/RESULT.json`, SHA-256
`0e3d52235f03daf26707fc7deb18510d4f205f99ea34449a6e08353cdf10aa04`.
Its nine records are the evidence for expected matches below, not a replacement
for actually querying the index. No database inventory was opened here.

## Query and correctly sized finite budget

Supply exactly these three formal conjuncts to search:

```json
[
  {"tag":"object-kind","value":"ordinary-lean-export-v2"},
  {"tag":"declaration-kind","value":"theorem"},
  {"tag":"type-symbol","symbol":{"kind":"portable-symbol","symbol_id":"baa1877cd14b1dc673e5273d7289fac7217bd71ac12087079c32df5503f8d452"}}
]
```

The symbol is the already known exact Std.HashMap binding. No FiniteMapEffects
name, target export ID, target UnitID or complete target type is a search input.
The public query compiler already exists, but this known-symbol query needs no
new query-compilation/native operation. A source/data domain-hash calculation
against the saved records confirms all six theorem records match all conjuncts;
their object-ID prefixes occupy six distinct partitions:0c,35,3d,3f,f5,f7.

This corrects the older RECIPROCAL-PLAN's tentative four-request/two-page budget:
**one offer plus six partition pages requires at least seven requests** on the
normal current data. A page-length cap does not cover all partitions. Proposed
find fields are:

```json
{
  "limits":{"providers":1,"snapshots":1,"requests":9,"pages":8,
            "examined":64,"candidates":16,"bytes":1048576,"wall_ms":20000,"inflight":1},
  "offer":{"max_bytes":262144,"max_expanded_bytes":524288,"max_age_ms":60000},
  "page":{"scanned":8,"matches":4,"bytes":65536,"timeout_ms":500,
          "record_probes":256,"node_reads":8192,"hash_calls":65536,"sql_vm_steps":200000}
}
```

The six expected pages reserve48 scan units. Candidate capacity16 accommodates
per-page reservations even after earlier hits; page.matches4 must not be combined
with an aggregate candidate grant too small for later reservations. Eight pages
reserve at most524288 reply bytes, plus the262144-byte offer, inside1MiB. These
are finite ceilings, not a latency or success guarantee. Leave candidate_mode
absent/default atomic-v1; this tiny existing index needs no new sparse access path.

## Existing public operations

Use the actual package's `peer.py` under the existing Run-V5-Check supervisor,
with Python `D:\Python314\python.exe -I -S -B`, explicit canonical runtime paths,
PROFILE, exact config SHA-256, fresh output and original finite budgets. No new
Python orchestrator is necessary: the root can manage its ordinary process
session and prepare the next small JSON file from saved output.

1. **serve:** config contains index above, host127.0.0.1, port0, tlsnull,
   lease_seconds120, cleanup_seconds15, share_all_custodytrue, exclusivetrue,
   and limits `{max_connections:2,max_requests:16,max_reply_bytes:4194304,
   operation_ms:1000}`. Supply state/quota flags. Proposed peer allowance is
   150wall/30CPU/768MiB, outer180wall/45JobCPU/1024MiB/fourprocesses. Startup
   plus the120-second lease and15-second cleanup must fit the original deadline;
   the existing API checks this. Serving opens the existing owner lock and shares
   the entire selected custody locally; do not run contribution/publication on
   that owner concurrently. Root selects one service, no renewal/retry.
2. **find:** wait for its actual READY.json. Define one contact label `a` with
   READY host/port/tls, server_namenull, ca_filenull, ca_sha256null; tls is the
   returned Boolean, not serve's null configuration. Set providers `["a"]`,
   specs above and the complete limits/offer/page above. State flags are forbidden.
   Proposed peer45wall/15CPU/512MiB, outer60wall/20JobCPU/768MiB/threeprocesses.
   Retain its exact result, including offers, matches, provider_errors, termination,
   search/network counters and coverage flags.
3. **preview:** for each returned match being considered, copy exactly
   `{provider,snapshot_id,record}` into `selection`, reuse the actual contact, and
   set `limits:{requests:1,reply_bytes:65536}`. No target identity is invented or
   supplied independently of the find result. At most six previews, preferably
   serially or at most two concurrently, fit the service's16-request envelope:
   find's selected9 plus six previews is15. Each public preview has its own
   original finite peer35wall/8CPU/384MiB and outer45wall/12JobCPU/512MiB/
   threeprocesses envelope. Every failed attempt consumes its grant; no automatic
   replacement. All six current previews total only32,038 actual object bytes.
4. Wait for that same service to report LEASE_FINISHED, quiescenttrue, clean
   provider/index/owner/custody closure and clean outer reaping. Only then may
   the same-owner frontier contribution start. The service ending is intentional,
   not a license to infer remote availability afterward.

The original operator kit documents these exact public operations and safely
copies find selections for preview. Its frozen original compatibility map does
**not** cover this package. Even the newer ordinary_current_release selector's
recorded noncompiled map differs at `reference/baseline_intake.py`; the frontier
successor differs at additional paths. Do not run a known-incompatible selector,
override its profile constant or extend its compatibility map for this one call.
Direct closed JSON configs plus the existing peer CLI are already supported and
avoid a new helper or compatibility project. No config or launch was created here.

## Selection from returned formal types

`find.result.matches[i]` supplies provider, snapshot_id and the complete record.
The record binds object_id/object_sha256/object_bytes, formal features and a
locator containing semantic_id, export_name and unit_id. It is candidate metadata.
Preview success must be PREVIEW_BOUND_NOT_ACCEPTED with the exact retained
selection, preview_sha256/preview_bytes and a preview containing semantic_id,
unit_id, export_name, header and type_bindings. These are enough for a reader to
interpret the universally quantified formal type and identify referenced concepts.

Select the type expressing universal-output nonemptiness iff initial nonemptiness
or a Boolean summary, and the type providing an execution returning the input
when that summary is false. Returned declaration names may help navigation, but
select by the actual types; no search decision is conditioned on a preloaded
nonempty_iff/zero_effect_witness ID. If a concept is unfamiliar, a later explicitly
selected inspect can use a returned type_bindings pair; it is not needed merely
to obtain these two theorem triples and is outside this finite15-request plan.

Derive each selected acquired triple from its actual preview and matched record:
name=preview.export_name, unit_id=preview.unit_id, export_id=record.object_id.
Check their equality to the already prepared frontier acquired-targets file as
an **after-the-fact integration check**. That file was authored from local evidence
and is not itself discovery evidence. This source plan knows the expected answers;
the operation demonstrates unknown-ID formal search inputs and public retrieval,
not a blinded experiment or independent mathematical invention.

## Coverage, failure and claim boundaries

The present public find returns verified positive committed records and explicitly
INCOMPLETE_SEARCH, even when all selected contacts finish. Expect termination
SELECTED_CONTACTS_FINISHED_NO_COMPLETENESS_CLAIM on the ordinary successful path;
global_complete and verified_scan_coverage remainfalse. Inspect actual recorded
snapshot IDs and require the current final snapshot above when no further
publication intervenes. Do not convert a provider cursor or six matching records
into a proof of global or within-corpus completeness.

An unavailable/slow provider, stale offer, bad proof or exhausted grant gives a
charged refusal/incomplete outcome, with retained partial candidates where allowed.
No returned target means no discovery result, not theorem nonexistence. There is
only one provider in this bounded step, so it does not establish failover or global
availability. Do not add a failure campaign or second provider for this question.
Preview binds bytes to the returned record but grants no mathematics and does not
reverify snapshot membership. The subsequent independently checked contribution
still uses the already protected local parent; discovery neither imports Lean
binaries nor licenses received source execution.

Adopt only the actual public-query/preview bridge if it succeeds. Charge server,
search, previews and failures in addition to the existing contribution/publication
and later extension. No causal speedup, independent recipient acceptance, scalable
recall benchmark, autonomous theory formation or complete v5 follows from this step.
