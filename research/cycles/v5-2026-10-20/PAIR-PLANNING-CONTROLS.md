# Focused pair-planning controls: source handoff

2026-10-20. Author: core_growth. Source-only; not parsed, imported or executed.
Root owns review, selection, launch, outcome adoption and Git. No product source
or used evidence was changed. The independent review remains required.

## Exact inputs and invocation

Runner: `software/v5/pair_planning/controls.py`, 34,964 bytes, SHA-256
`9678a2a3e661f5a6c460ec8c61da03144134360567bf6fc40b09216f79f5a312`.

The source basis is the 114-entry `sdk_sources` map in
`experiments/v5-local-checks/distribution-body-custody-01-input.json`, SHA-256
`995525c5cbf2746718cbf583a3e3e401bc56c2f88d1cef8664ffeb1b644454be`.
All original map byte counts and hashes are checked before staging. Exactly
three logical entries are replaced by the following reviewed-candidate paths:

| Relative source under `software/v5/pair_planning/` | SHA-256 |
|---|---|
| `discovery/module_export_adapter.py` | `c7fde37659753a9238506d399e0be5c44ebb5e3a012b5a681dfa1a1551884fd1` |
| `client/direct_contacts.py` | `1f4224808ceb65feff3fd80353a3dbea3923e2ad091e7c435193fd82f4dc54c8` |
| `client/located_queries.py` | `4ffb84789deefb524f7f290b2a8879e3b9a1eadc0febf53ad2f5e1a3e168c66a` |

Two additional staged logical files produce 116 total, not 116 new products:

- `v5/discovery/_pair_planning_baseline.py` is the exact original adapter selected
  by the basis map. It supplies unchanged-default comparison, not another run.
- `v5/client/test_direct_contacts.py` uses
  `software/v5/client/test_direct_contacts.py`, 23,990 bytes, SHA-256
  `5707cc9c334ca602fe41b56079e5725be30c5c21cc6b2c7591c77b0c9953906b`.
  Only fixture constructors/helpers are called. No inherited test method runs.

The wrapper/source snapshot must preserve original relative source paths under
`software/v5`; the runner resolves its source root from its own absolute path.
It reads the exact basis map at its canonical location. Required argv is:

```text
python.exe -I -S -B <absolute selected controls.py> --output <fresh existing output directory>
```

The working directory must be the canonical root. Output must be an existing,
resolved absolute path under canonical `experiments/`; selected-code and test
subdirectories must not preexist. The terminal report is `controls-result.json`,
schema `DMKN_V5_PAIR_PLANNING_CONTROLS_V1`. It names all selected methods, exact
source copies, observations and assertion failures. Imports/staging failing
before the report are failures, not an empty success.

## Nine changed-boundary controls

1. Four existing profile modes preserve namespaces, record bytes and default
   compilation; nonpair plans introduce no features.
2. All seven nonempty profiles over three possible atomic pairs, all seven
   nonempty queries and all eight structural export patterns yield 392 exact
   predicate comparisons. Eligible keys are independently derived from profile
   atoms. Enriched and legacy predicates equal the intended atomic conjunction.
3. Four atoms/all six pairs fit eight wire keys; eight atoms/eight pairs expose
   the cap with seven legacy keys, one added and six omitted. All 127 nonempty
   legacy route subsets remain usable. Returned plan mutation is isolated.
4. Empty/raw-hash/nested-pair/nine-spec inputs and modified profile state refuse.
5. A real codec/adapter/SQLite Store corpus contains 193 exact committed exports:
   96 with the first canonical pair, 96 with only its missing third atom, and one
   with all three. IDs are actual codec hashes and partitions are their actual
   first bytes, not invented postings. Real summaries and ordinary authenticated
   pages are verified with `Coverage.accept`. Both queries must return the same
   singleton with complete committed-anchor coverage. Enrichment must examine
   exactly one record and fewer than legacy, with no partition's anchor count
   increased. Larger summary bytes are explicitly reported, not hidden.
6. Actual direct factory default/opt-in calls bind the selected immutable query
   and exact query digest; the original grant, owners, ledger and prepayment
   remain. Defaults omit planner metadata and opted-in metadata does not alias.
7. Actual located factory default/opt-in calls preserve the original legacy
   route hash and same reader, use one locate/descriptor sequence, and retain
   original budgets/owners. Metadata is isolated from caller mutation.
8. A settled no-contact result retains its opted-in plan without replacement
   search/acquisition, a new generation or reallocation.
9. Both factories reject `1`, `"yes"` and `None` as the opt-in before allocation
   or reader start. Ordinary fail-stop/cleanup still executes.

## Scope and cost

The exported objects are structurally valid canonical descriptors/openings;
their illustrative theorem types are **not kernel-checked mathematical claims**.
This test addresses index planning and factory binding, not mathematical growth.
Mathematical issuers and channel start/command/close are explicit inert fixtures;
the stores, budgets, grant bookkeeping, protocol parsers, envelope and session
classes are real. Inert substitution does not establish location authentication.

No Lean, proof, Node, socket, subprocess or old test campaign is selected.
The socket class is preserved while its constructor is blocked, avoiding the
previous Proactor class-substitution defect. Async loop exceptions fail cleanup.
Current-source workspace schema and generation-row shapes were checked before
handoff. The old direct fixture is adapted to current body/origin invariants.

The proposed single Python-only outer envelope is 45 CPU seconds, 90 wall
seconds, 384 MiB and two processes. This is a prospective bound, not a measured
cost claim. Store limits bound objects/postings/features/snapshots and database
pages; normal query pages use fixed work and byte limits. A cap failure does not
authorize another run or a larger envelope. No source build or installation is
needed to discriminate this change. Root's selector must pin its own snapshot
and runner in addition to the 116 logical staging entries.

Even a passing result establishes neither global search completeness nor total
cost dominance: extra authenticated summaries can outweigh saved scans. It
tests the already argued finite predicate preservation and anchor-count
dominance while reporting that overhead. It is not a growth workload or final
v5 qualification.
