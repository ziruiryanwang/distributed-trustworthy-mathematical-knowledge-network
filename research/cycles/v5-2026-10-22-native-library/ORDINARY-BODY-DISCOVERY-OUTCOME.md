# Definition-body discovery: saved outcome audit

2026-10-23. Independent reviewer: `admission_event_audit`. Saved evidence only;
no test replay, product import, Lean call, catalog mutation or Git operation.

## Decision

**PASS for the selected finite metadata/index discriminator; no overall
efficiency win established.** Both search stages together examined three
postings versus eight for the exact preceding broad query, but returned
**202,790 search bytes versus 103,356**: about 1.96 times as many. Additional
definition evidence and body-index maintenance also cost resources. Keep this
as an optional specialized query route, not an established default or a general
speedup. This is useful decision evidence precisely because the narrower posting
scan does not automatically imply lower complete-workflow cost.

## Exact evidence and execution boundary

Run: `experiments/v5-local-checks/ordinary-body-discovery-controls-01`.

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `10fe8b0435c5a7a4134ff23af5cb256035bb6aee5f1989b9f3c66fa26dddb9dd` |
| `RESULT.json` | `197925c7adbd0732eaa84399bce943049eaa943e92402be9e8f688beb5e3966a` |
| `command/stdout.txt` | `5597e4e1699cfb0a8c76459f47305efa7657fd73f58c95593dd6df696892579d` |
| `command/stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

All 13 retained source hashes match the selection, including the independently
reviewed check `29a55fe0` and adapter `310980b1`. All five selected external pins
(three Python runtime files and two retained actual producer evidence files)
also match. The result binds the exact selection hash and its command matches
the selected inputs and fresh store path. This is not a hermetic runtime proof.

The command exited zero and closed cleanly: direct child reaped, Job closed,
zero remaining active processes and no cleanup errors. Stdout is 4,161 bytes;
stderr is empty. Full reported wall time is **1.1245459001511335 seconds**.
Known inclusive CPU is **0.765625 seconds**: 0.6875 Job CPU plus 0.078125 outer
wrapper CPU; the separately reported inner supervision CPU is zero. Peak Job
private commit is 18,690,048 bytes. The selected outer envelope was 30 CPU
seconds, 60 wall seconds, 256 MiB and two processes. The source contains no
Lean subprocess, network service or mathematical admission operation.

## What actually passed

All four selected groups reported PASS. The local formal query was printed
before the first publisher read. The retained Stable trace reports eight
generated alternatives, 13 path visits, 58 total unit nodes and structural
work 74. The compact shared-DAG control reports 82 body nodes, 170 total unit
nodes and structural work 173. These structural counters are not CPU costs.

The real local Store integration held nine definition records and nine method
records. It attempted only the first, most-specific query; seven other
alternatives were not attempted. Stage one returned actual Stable and the
intentional P/Q collision. Both full definitions were acquired and resolved;
both learned symbols were queried at stage two. One second-stage search was
empty; the other returned the actual method. Its preview and retained full
evidence were bound without mathematical acceptance. The comparator returned
eight theorem candidates under the exact theorem-kind/forall-domain conjunction.

| Charged bucket | Calls | Examined postings | Returned bytes |
|---|---:|---:|---:|
| First-stage body search | 3 | 2 | 48,217 |
| Both second-stage symbol searches | 3 | 1 | 154,573 |
| Both definition evidence acquisitions | 2 | 0 | 5,760 |
| Method preview acquisition | 1 | 0 | 1,677 |
| Method full-evidence cross-check | 1 | 0 | 5,317 |
| Broad comparator search | 9 | 8 | 103,356 |
| Total selected check | 19 | 11 | 318,900 |

Totals agree with the final event and remain within the one 64-call/8 MiB/
120-second internal ledger. The selected staged path plus acquisitions used
215,544 returned bytes and ten calls. The comparator's row includes search only,
not acquisition or proof attempts for all eight candidates; neither route has a
matched whole-workflow cost measurement here. Costs of both collision branches
are present, not silently dropped.

Body metadata incurred a separate index: nine objects, nine postings, seven
features, ten snapshots and reported logical size 37,638 bytes. Its saved SQLite
file is 94,208 bytes. The method index reports nine objects, 47 postings, 22
features, ten snapshots and logical size 165,711 bytes; its file is 352,256 bytes.
These are finite fixture storage observations, not a marginal production
maintenance estimate. Index creation and all controls are included in the
overall command time but not separated into matched route timings. File sizes
were inspected without opening or modifying either database.

## Supported and unsupported conclusions

The implemented hint can learn an unknown definition's exact symbol from an
independently spelled local property and use that symbol to narrow existing
theorem discovery. It tolerates an intentional false candidate without
confusing feature resolution with mathematical truth. Source and saved output
retain `mathematical_acceptance: false` throughout.

The run does not establish semantic applicability, mathematical novelty,
complete recall, global corpus coverage, network transport behavior, an
amortized useful-growth advantage or full v5 readiness. Synthetic decoys are
unproved metadata. Actual retained producer evidence is reused inertly, not
rechecked. Do not repeat the passed native reciprocal loop or invest in search
proof/serialization optimization merely to turn this small posting win into
a headline. The next consequential work is usable generic contribution and
then cost-aware choice among existing discovery routes under realistic use.
