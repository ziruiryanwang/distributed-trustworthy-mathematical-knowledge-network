# Post-handoff continuity triage: finite nodes are not a global stopping rule

2026-09-23. Read-only product/evidence inspection by
`post_handoff_continuity_gap`; canonical workspace guard passed. Source09,
used installations and the delivered candidate remain frozen. No product
imports, tests, processes, services, private-key reads or state changes occurred.
Only this checkpoint was authored. Product line citations below refer to
`product-local/stage-census-source-09/`; they are inspected source, not new
execution evidence.

## Recommendation

**Do not select migration, unbounded renewal or another exhausted-node transfer
test next. Prioritize the measured complete-workflow efficiency discriminator.**
Existing source09 behavior already supplies bounded mathematical succession
without transferring acceptance or preserving node identity/history. Actual
source07 and source09 installed runs have served committed views after their
ordinary request and native-stage authorizations were exhausted. Repeating that
case would not discriminate a new central obstruction.

There are real remaining lifecycle limitations: unexposed material can be
stranded by irreversible admission exhaustion; there is no supported garbage
collection/backup/restore; one sufficiently large proof closure cannot be made
acceptable by starting a fresh node. These are not solved. However, this review
finds no evidence that they prevented the selected real reciprocal workload,
whereas its finite cost is already directly measurable. Do not convert every
deliberately finite bound into an automatic v1 feature requirement.

## Separate three meanings of continuation

1. **Continue the same node below its lifetime bounds:** explicit owner renewal
   adds requests/stages/bytes/metadata allowance without resetting usage.
2. **Continue selected mathematics on a fresh compatible node:** serve a
   committed exposure, acquire its exact bytes and freshly admit there. New
   handles, budgets, configuration and acceptance belong to the receiver.
3. **Continue arbitrary mathematics forever at bounded cost:** neither of the
   above establishes this. Availability, resource supply, compatible foundations
   and a tractable selected proof closure remain premises.

For compatible A/B, a committed view V on healthy nonpending A plus supplied
finite service/receiver resources permits the implemented path
`serve_A(V) -> find_B -> acquire_B -> admit_B`. Only the last accepted response
is mathematical acceptance at B. The path has no positive ordinary-credit
precondition at A. Iterating such a path is an operating strategy, not a proof
of indefinite availability, affordable growth or universal mathematical coverage.

## Actual evidence already closes the proposed exposed-result exit test

The earlier [continuation triage](2026-09-23-continuation-triage.md) recommended
a new five-request exhausted-credit exit test. That recommendation is now
superseded by existing executed evidence, not commissioned again:

| Actual retained allocation | Observed exhaustion before service | Decisive result |
| --- | --- | --- |
| [Source07 aggregate result](../../experiments/aggregate-custody-01/integration-01/RESULT.json), `holder_pre_service_status` | used = authorized = 6 requests / 1 stage; remaining requests/stages = 0; 152 MiB reservation headroom | Actual installed holder service after both original suppliers stopped; fresh receiver admission of both exact roots. [Independent audit](../../experiments/aggregate-custody-01/INTEGRATION-OUTCOME-AUDIT.md), especially lines 87–109. |
| [Source09 mixed result](../../experiments/stage-path-census-01/integration-01/RESULT.json), `producer_pre_service_status` | remaining requests/stages = 0; 200 MiB reservation headroom | Actual installed service of one publication plus one custody entry, followed by fresh receiver admission of both. [Independent audit](../../experiments/stage-path-census-01/INTEGRATION-OUTCOME-AUDIT.md), lines 103–125. |

Root operation results retain their original pending-audit labels; the separate
passing audits supply their scoped dispositions. These runs do not consume all
4096 lifetime requests or prove recovery from metadata corruption, disk failure,
pending work or incompatible semantics. Those distinctions must remain explicit.

## Limit matrix and existing responses

| Boundary | Actual implementation | Consequence and existing route |
| --- | --- | --- |
| Ordinary authorization | `py/storage.py:392` reserves before preparation; requests and reserved bytes are independent checks at lines 403–405. Stages are separately charged at `:459`. | Initial exhaustion is not irreversible if owner-supplied renewal remains possible. Failed admitted work stays charged. |
| Lifetime authorization | `py/capacity.py:13`, `py/storage.py:487`: 4096 requests, 256 stages, 64 GiB cumulative reserved authorization, 64 grants; metadata caps up to 256 MiB. | A node eventually cannot accept additional research work. Renewal never resets usage or raises these ceilings. The network need not preserve one node forever. |
| Context list | `py/checking.py:243` enforces at most the configured 5–16 packages; `:490` appends selected package records. | It limits one selected context, not all stored results. `select_context` (`py/node.py:285`) permits returning to a historical context and branching, while retaining old knowledge. It does not trim one genuine dependency closure. |
| Closure itself | `py/source_codec.py:16` has 64 MiB / 8192 objects / 256 units / 1024 exports; `py/checking.py:243` forms a complete union. Wire has additional 16 MiB payload / 18 MiB bundle limits (`py/peer_wire.py:19`). | A proof whose necessary closure exceeds a supported bound is refused even on a fresh node. Packaging the latest derived root can avoid retaining every historical package-list entry, because `source_codec.py:939,955` exports/requires exact transitive root closure; it cannot erase necessary mathematical dependencies. No broad-library capacity claim follows. |
| Catalog and provider | At most 8192 provider entries (`py/storage.py:741`), and a managed view at most 256 entries / 64 MiB combined bundles (`py/peer_wire.py:20–23`). | These are local ceilings, not a global ledger limit. Select a bounded useful subset; independent nodes may retain different subsets. No single-view whole-corpus promise exists. |
| Contacts | 16 configured-plus-added contacts (`py/storage.py:582`), append-only aliases. | Known-peer operation grows only to this bound in one node. Compatible fresh nodes may choose new contacts. This is not wide-network discovery/rotation qualification. |
| Hosting journal | `HOSTING.md:72` bounds one journal to 128 grants / 4096 slots. | `manage.py:192` separately provides an explicitly authorized finite `serve` session and does not consult that journal or reserve ordinary work. This does not refund a spent journal slot or establish automatic uptime. |
| Exhausted ordinary credits with a view | `py/service_worker.py:74` reads committed view authority through `ReadOnlyControl`; `py/inspect_context.py:26` verifies initialized/nonpending state without requiring positive remaining credits. | The actual exhausted-credit transfer above succeeds. Service still needs intact config/control/view/runtime/identity bytes and physical supply. |

The package-list distinction matters. A chain does not inherently consume one
per-context package slot per historical step: after selecting an earlier small
context, admitting the latest complete successor can import its earlier
dependencies inside that one package. This follows from exact root-closure
packaging; it is not a newly executed long-chain performance claim. Conversely,
many genuinely independent roots or large recursive closures may still exceed
the selected profile. Increasing a counter is not evidence of affordable support.

## Genuine residual egress gap

An honest operator can spend the last irreversible ordinary allowance before
creating a committed view for a desired result. For example, a successful
`submit` consumes the last research request and returns a private artifact;
the later `publish` and `expose` each need another ordinary reservation.
Likewise a last successful acquisition can lack its later `replica_expose`.

This follows from `py/node.py:365` (every fresh operation reserves first),
`:351` (submission returns an artifact without publication), and
`py/peer_node.py:368,451` (exposure creation). `manage.py:244` has no public
export/import/restore command. At a hard request/byte/metadata boundary with no
remaining suitable grant, existing owner `serve` cannot invent a missing view.
Private filesystem bytes may still exist; this is an absent supported egress
workflow, not destruction of mathematics or impossibility of forensic recovery.

The existing bounded operating policy is to expose/replicate selected results
while admission headroom remains, then select a fresh node when necessary.
That policy is imperfect for mistakes or unexpected resource failure, and no
automatic reserve-for-egress rule is implemented. But it handles the planned
loop without SQL migration or carrying another node's accepted flag.

Do not commission a new egress mechanism solely to eliminate this disclosed
edge before measuring the normal loop. If it later becomes selected, test the
actual case with retained genuine mathematics **without a view** and a genuinely
irreversible supported boundary; successful previously committed-view service
is not evidence for that different case. No such test or feature is selected here.

## Retained bytes: cost issue, not yet a demonstrated continuation failure

`py/checking.py:233` writes normalized packages into request-local work;
submission preserves candidate and inverse stage outputs (`:528–577`);
peer acquisition preserves incoming and normalized material
(`py/peer_node.py:237–254`); exposure creates another immutable bundled view
(`:392`). Exact descriptor reuse (`:273`) avoids duplicate provider entries,
but it does not undo already received bytes, erase stages, refund reservations
or garbage-collect historical views. There is no public prune command in the
complete `manage.py` parser.

Thus logical corpus size, unique useful root count, conservative reserved
bytes and retained physical/logical file bytes are different quantities. A
succession can relocate a selected closure and allow an old owner to cease
service, but this software does not supply a qualified deletion plan for the
old installation/state/evidence. We must preserve experimental evidence; that
research policy is not itself a required product-level eternal-retention design.

Whether actual copying/checking/retention amplification is the urgent obstacle
requires measurement of the complete selected workflow, not inference from
counts or the mere absence of GC. Root is examining exactly that evidence.
Prefer a resulting measured bottleneck decision to adding lifecycle mechanisms
without a decision-changing workload.

## Inspected identity pins and scope

| File | SHA-256 |
| --- | --- |
| source09 `py/storage.py` | `278d14744b311a686bcb40a6836346b24f5180766258e09cdb1e3577f740ee6d` |
| source09 `py/checking.py` | `13afa1fa31f58f273c0364b9679fd56400587f2977ea24bddd85aad9471f840b` |
| source09 `py/peer_node.py` | `8e66b840b1d1e56034f49c337da8d06cc35c508fbe79209b077bd891d16ce894` |
| source09 `py/service_worker.py` | `8014ee4c8acdc74f7d2ff5b9dbae2920564f8c6bf9678b5a6011dd9ae23b0528` |
| source07 aggregate `integration-01/RESULT.json` | `cfb436c50d3eb6f71f840a63f6d12ea12b6ce8f829fbd64c8f329083a6037053` |
| source07 aggregate `INTEGRATION-OUTCOME-AUDIT.md` | `3abba0e628118793bca594bc56f80217cf4b071f683a1844051d8280fea43573` |

Hashes identify inspected bytes, not correctness. This is a bounded technical
priority judgment, not new qualification, full-goal completion or a licensing/
publication decision. The broader goal remains active under root's authority.
