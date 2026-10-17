# Genuine terminal gate: implementation-ready adapter split

2026-10-17. Source-only assignment from root; no runtime, proof, imports or Git
mutation. Canonical guard passes. This closes missing glue for the existing
GENUINE-TERMINAL-GATE, not a new release goal. **Final A remains absent.**

## Decision and minimum new files

No adequate adapter already exists. Reuse `client/launch.py` and `client/boot.py`
unchanged, with one fresh `DMKN_V5_CLIENT_LAUNCH_V1` owner entry. Reuse actual
`Workspace`, issuers, preparation, structural stores, provider and location APIs.
Root can parallelize only these two new source files:

1. `client/terminal_assets.py`: pinned input/adoption/configuration and
   genuine owner construction; separate author.
2. `client/terminal_strategy.py`: `main(context)` strategy, origin seed,
   discovery, semantic-demand resolution, author/publication, cold C and cleanup;
   separate author. Root owns the eventual exact launch selector and a small
   exported-proof inspector if needed.

Suggested inter-file contract (ordinary immutable data, never minted authority):

```text
Assets(context)
  .foundation: bytes; .foundation_sha256: str
  .aggregate_image: str; .header: bytes; .ports: dict
  .configuration(): exact evidence-workspace config
  .grant_limits(phase: "B" | "C"): finite grant dict
  .owners(workspace, grant, phase): transferred CommonsClient
  .origin_material(): {terminals, groups, bodies, first_export_name}
  .author_input(): (source_text, roots)  # called only after B acquisition
  .expected_journals(): {BASE, FIRST, SECOND}  # evaluator, not chooser
  .expected_second_spec(): dict  # evaluator after author call, not author input
```

`origin_material` may use retained BASE/FIRST witness data only to derive
structural interfaces/body records. Its output contains no FIRST proof rows,
SECOND witness, receipt authority or verifier handle. The strategy's initial
chooser receives only formal query/bootstrap/grant, not this assets object.
This is trusted phase separation within one process, not hostile-code isolation.

Root's proposed inspector contract is
`inspect_author(prepared, source, roots, grant, *, envelope, aggregate_image,
expected_header, expected_target_journal, expected_frontier_journals,
required_proof_module, required_proof_name, foundation_bytes)`. It checks actual output/source
binding, exact local interface/J and FIRST proof use, returns inert audit facts,
and performs no native admission or fixed-row-count comparison. Root adopts
independent review's additional pure current-export-to-witness re-emission
comparison, using the unchanged emitter and exact foundation/context bindings;
this does not compare to historical witness bytes or replay parent proofs.

## Reuse map; do not launch historical harnesses

| Existing source | Reuse |
|---|---|
| `client/launch.py`, `client/boot.py` | Exact snapshots, guarded source origins, enclosing Job, finite outputs and closure. No new supervisor. |
| `client/actual_assets_atomic.py` | Data-pin checks, installed-runtime rebasing and preparation-profile construction pattern. Its `Assets.owners` is I-only and cannot be used unchanged. |
| `client/actual_owner03.py` | Node/bootstrap/provider/find/page flow, cleanup, exported-source inspection pattern. Its seed, cold-local path and `inspect_author` are not this gate; the latter hardcodes three universes while SECOND has four. |
| `client/actual_resume_owner.py` | Capture terminal client reports once, before later phases inflate lifetime CPU observations. No prior mutable workspace reuse. |
| `mixed_network/reciprocal_actual.py` | Structural BASE/FIRST extraction and bounded provider-publication status semantics only. Do not import it: it mutates `sys.path`, uses older direct imports, starts by authoring, and requires 3 A + 2 native checks. |
| `client/workspace_resilient.py` | Ordinary evidence workspace with same-grant safe search refusal; use after root adopts its pending focused controls. Otherwise root explicitly selects evidence predecessor, not a hidden fallback. |
| `evidence_network.packet.pack_terminal`, `evidence_network.transport.CompositeProvider` | Two-form exact envelopes and provider. Do not use I-only/mixed-only providers or fake issuers. |

## Exact current H2, not historical H3

Under `experiments/v5-local-checks/selected-frontier-layout-01/evidence/`:

- `header.bin`: 192 bytes, SHA-256
  `49dd845edaec83f5b0cba5af38653f768e51ed95a4bb6ea7824c10bdd1c3169e`.
- `selection-derivation.json`: SHA-256
  `1750785cbde497cbd60f371203ce67cbf35844aaf9422782b65f03c2d1561941`.
  Use its `selected_header`, `members` and `omitted_descendant`, never its
  historical `old_synthetic_header`/`previous_actual_header` fields.
- H2 has BASE index0 and FIRST index1, maximum rank1, seal height1.
  The sole BASE sibling is
  `d252447b00492ac63faef9eb216a24e47bbc7c49f9779974526ab3fab5cc71fd`;
  the sole FIRST sibling is
  `673bc1dab0b85887bc07944bff2d88eec07aa89d6abad984d1901c1ac7dffccf`.
- Exact J_BASE/J_FIRST are unchanged; J_SECOND is `omitted_descendant`, not
  an aggregate member. Adopted A remains
  `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`.

Final receipt must be a fresh **root-adopted real resolved A/H2** pin, at most
8 MiB. Do not give the consumer the capsule or upstream I receipt. Preflight
both terminal JSONs and eventual mixed envelope against selected caps; no public
cap increase to accommodate an oversized result. Retained asset pins in the
gate remain valid, including source/roots and corrected reference packet.

## Root correction: demand-only semantics, not reference-proof equality

Root explicitly selected this correction during this review: do not fetch unused
`binary_congr` merely to reproduce the old 1009-row witness. That reference was
built with all11 BASE groups. Demand-only context may legitimately change proof
rows, parent openings, bodies, packet bytes and witness count. Preserve the
historical reference; no passing evidence is rewritten.

Keep exact J_SECOND and canonical `local_spec` equality, rank2, and an actual
exported proof edge to FIRST. Do **not** require whole-witness equality or1009
rows. Proof-representation equality was never mathematical identity.

Source reason J is expected unchanged: `SourceRows.reference` resolves external
names to `[external, ModuleID, relative_name]`, not imported table positions;
`SourceRows.module` omits nonlocal declarations. Its theorem declaration has
`value_hash=None` and keeps the proof separately. `codec.summarize/module_id`
commit the local interface, not the external context or theorem proof.
`MixedSourceOperation.finish` selects rank `max(parent ranks)+1`; selecting the
same BASE/FIRST Js keeps rank2. `expected_journal` encodes that summary/rank/I.
The retained explicit source uses unchanged names/types and no target-selecting
typeclass or notation search. An unexpected changed exported local interface
must still fail exact comparison; this argument is not permission to normalize
away an actual difference. Native C independently checks the newly emitted proof.

## Concrete strategy and semantic-demand resolver

1. O: fresh evidence workspace/stores, no mathematical owner. Put two terminal
   packets, authenticated BASE groups/body responses and FIRST's sole opening
   through public structural store methods. Index only FIRST's theorem. Start
   one neutral location bootstrap and O's evidence CompositeProvider; publish
   actual formal features. Publication is a hint, not success or authority.
2. B: fresh workspace/grant/owners. Use the gate's theorem/Eq/BASE.fold query;
   `find -> search_offer -> search_page -> resolve -> packet_offers -> acquire`.
   Choose by returned formal candidate, with no `expected_exact_journal` on this
   initial unknown-ID acquire. Evaluator then requires kind A-member/J_FIRST.
   Try only returned configured contacts within the original finite budget;
   classified safe search refusals may continue, not metadata/admission errors.
3. Start `import_context` with FIRST warrant, its exact J and returned opening,
   no semantic bodies. Each non-READY result provides explicit demands:
   - `NeedVerifiedMixedMember`: resolve that module/name via
     `resolve_declaration(origin_candidate, module, name, max_bytes=...)`, obtain
     packet offers and acquire its genuine terminal; only BASE is permitted
     in this selected gate. Require exact J_BASE. Same live A/H2 uses one actual
     receipt check total at B, but still pays exact membership and transfer.
   - `NeedDeclaration`: same exact-name route; reuse returned candidate/opening
     by `(module, name)`, and deduplicate actual group by `(module,index)`.
   - `NeedBody`: use the matching descriptor candidate, resolving it first if
     necessary; `acquire_body(candidate, body_hash, max_bytes=...)`. Deduplicate
     by `(module,universes,digest)`. Convert full response to import row
     `{module,universes,expression}`; verify against the actual requested digest.
   Accumulate only acquired rows; call `extend_context` with new rows/warrants/
   selected Js and replace the old returned context token. A finite monotone
   progress check refuses repeated already-satisfied demands. Cap unique data
   at11 BASE groups/11 bodies plus FIRST group; never request theorem proof.
4. Only after READY release source/roots. `author` exactly once, using the current
   sealed returned context. Inspect actual source-request/export bindings,
   canonical local spec, four-universe target and exported FIRST proof reference;
   require exactly one A claim, two BASE/FIRST frontiers, one rank2 SECOND delta,
   no native FIRST witness and no SECOND A frontier. Compare target spec/J only
   against retained corrected data after authoring closes.
5. B `publish` authored packet/SECOND export through the ordinary client; require
   LOCALLY_PUBLISHED, actual readback and no partial intent. Start B's provider
   from its held stores; no private insertion. Stop/reap O HTTP/location before
   creating C. Close B's mathematical client and capture its report once, while
   its workspace stores can continue serving. No B native SECOND admission.
6. C: separate fresh workspace/grant/owners, same neutral query/bootstrap, no B
   warrant or target ID supplied to chooser. Repeat bounded public discovery;
   stale O contacts can receive only already selected same-session refusal
   handling. Acquire SECOND; evaluator requires kind mixed/J_SECOND and exact
   B-published bytes. This incurs one independent A check and one native check.
7. Stop/reap B provider/location. While C's own warrant remains live, use
   `semantic_material`, `describe(...)[members]` and `import_context` with its
   acquired mixed closure. Require READY/no demands and unchanged HTTP counters
   after provider loss. No second author or third cold verification. Close all
   clients/stores/nodes, preserving failure records and exact resource reports.

## Real owners, source pins and resource shape

Reserve first; then construct `AggregateReceiptVerifier`, `MixedDeltaVerifier`
with `legacy_verifier=None, aggregate_verifier=that_same_A`, and (B only)
`mixed_claims.authoring_atomic.MixedOwnerPreparation`. Call workspace.operation
with `receipt_owner=None`. Every owner starts after its grant and its deadline
is at most grant.deadline. Construction failure closes only constructed owners;
successful operation transfers them to the client. No manual handle injection.

Rebase preparation profile exactly as `actual_assets_atomic` does, retaining its
real installed frontend/Lean image/runtime identities. The A verification
executable must be a selected real A `verify A receipt H` host, not I's host or
the proof stage command. Its retained small snapshot host is an available
candidate; root selects the exact executable/build pin. Mixed native executable
is the retained relation checker, unchanged. No rebuild is required for consumers.

Pin imported v5 files to the launcher's actual snapshot, using selected hashes
from `context.source_sha256`, never authorize code using hashes discovered at
runtime. Start with the95-file evidence-client source selection, remove control
owner/test-only rows, add the two new files and resilience sources, and close
actual imports. Keep the portable location source map exactly as launcher
requires; no second `v5/location` import tree. Each issuer pin map stays <=128
entries/512MiB; split source responsibility across A/native maps if necessary,
without omitting either owner's required closure. Client-required source union
must contain atomic/mixed/evidence/resilient and evidence-network origins.

Finite operation counts are fixed now; timing allowances remain root's later
exact selection. B: acquisition verify_attempts1, A operations1, no actual native
delta receive, preparation operations1. C: acquisition verify_attempts1 (one
mixed envelope), A operations1, mixed operations1, no preparation. Both require
a pristine mixed owner even when B never calls it; its configured positive cap
is not an additional actual check. Per-phase import capacity must hold at least
B's2 sources/2 members/1 receipt and C's1 source/3 members/1 receipt. All nested
caps obey current public suballocation rules. Exactly2 A/1 author/1 native and
zero I/guest/proof calls are final assertions, not source-assumed outcomes.

Original grant input allowance must include repeatedly submitted envelopes,
receipts, context batches and live-source binding charges—not merely net network
bytes. Avoid submitting all accumulated data on every incomplete-context step:
imports retain prior rows, and only new rows/warrants need adding. Use a finite
resolver-step/request cap and no renewal. A byte/CPU plan must account for actual
final receipt size before runtime; no invented verifier timing from absent A.

## Finite outputs and cost record

One new launcher run: original plan, immutable sources, normal bootstrap/result
records, `work/origin`, `work/B`, `work/C`, bounded location channels and native
owner subdirectories, and one bounded `terminal-result.json`. No recursive
copy of old experiments or global ledger. Reuse launch output/census ceilings;
choose finite aggregate bytes/entries and process slots covering simultaneous
bootstrap/provider/reader plus the ordinary bounded native child tree.

Report call counts, exact H/Js/receipt and transferred packet hashes, source and
returned group/body identities, author/native proof-edge evidence, READY status,
provider-loss closure, refusals, partial outcomes and original caps. Whole Job
CPU plus outer-wrapper CPU is the known total; nested A/native/author controller
measurements explain it and must not be added again. Include hashing/setup,
provider/index/storage work. Record physical HTTP payload/header scopes separately
from charged acquisition/input/issuer bytes and explicitly unknown DHT/partial
traffic. Close-time client reports are captured once. Upstream proof production
and historical failures remain separate retained costs, not zero or rerun costs.

This makes the new terminal route executable once genuine A is available. It
does not itself establish full-cost growth advantage, huge-network completeness,
independent hosting, hostile-input isolation or final v5 readiness. No additional
synthetic regression suite or repeat of the I-only campaign is commissioned.
