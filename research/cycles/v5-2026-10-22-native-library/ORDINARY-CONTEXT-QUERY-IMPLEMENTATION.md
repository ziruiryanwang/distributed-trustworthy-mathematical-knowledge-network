# Context-bound query: source implementation checkpoint

2026-10-23, `usable_v5_next`. Root selected only fresh
`software/v5/ordinary_query_context/query.py` under contract
`e4db149a864a9f7a3103a92549c5a1ed64621361d8b43f5a6e0a65571e001b67`.
No runtime, product import, database opening, native call, experiment, package
assembly or Git mutation by this author. Independent review precedes execution.

Source SHA-256:
`449b5fea77f4c19cfbde47346ea255ae1277a1cf53e3030a6baa9de3f8659af6`.
Preserved predecessor:
`ordinary_query_package/query.py`,
`886bdfd61dbc613411379b5c298fb61492feeae1215beabc783d4d5537110d57`.

## Exact delta and public behavior

- The old `bootstrap_owner` is unchanged. The old `run` body is unchanged as
  `run_manual`; valid manual inputs retain their output bytes/fields/flow.
- New `binding_mode` validates manual/context exclusivity and the complete
  owner-option tuple before state opening, for CLI and programmatic dispatch.
- Parser adds `--context-root` as an alternative to `--bindings`, with required
  context-only `--catalog`, `--custody`, `--store-id`, `--custody-limits`.
- `resolve_context_bindings` is a small pure function over Q's actual reference
  order and the supplied mapping. It validates present IDs, reports all missing
  names and returns no partial binding bytes. It iterates only query references.
- `run_context` validates existing paths/limits/ADOPTION and uses real
  OrdinaryStore/OrdinaryAdmission reopen APIs. The explicit selected root must
  match semantic, foundation and implementation IDs. No native/custody transfer/
  admission/anchor work is called.
- Owner and custody are both closed in the finally path, even after an error.
  Any close error suppresses success. Owner reopening can settle abandoned
  reservations; this is disclosed, not labeled database-read-only.
- After successful closure, new BINDINGS/QUERY/SPECS files are written into a
  fresh directory. The context-mode RESULT is fsynced to a pending file and
  published last by fresh Windows rename. Failures retain partial bytes; rename
  uncertainty preserves the attempted result hash. No retry or deletion.
- Unknown-reference output is structured and leaves the output directory absent.
  Output explicitly says `SELECTED_RECEIVER_CONTEXT_NOT_PROJECT_EQUIVALENCE`.

No owner.py/profile.py/core helper was changed. The local-anchor support descriptor
does not include query.py, so replacing only that payload is compatible with the
same selected support; full package PROFILE must still be regenerated/verified.
Actual support-ID comparison belongs to later integration, not this source claim.

## Accounting and boundaries

The original query allowance covers loading, opening, resolution, closure and
output preparation. Catalog reconstruction and artifact hashing remain real
costs; existing context methods have no per-iteration parent budget callback.
Before/after checks and an enclosing supervisor remain necessary. Native/worker
CPU is zero. The saved result's sampled cost, like the preserved manual path,
precedes writing/publishing that result itself; an outer supervisor supplies
whole-operation finalization accounting. No result claims hard RSS/disk bounds.

The pure helper has no owner authority. Actual authority/eligibility comes only
from the live selected owner context; the query remains nonauthoritative search
data either way. No proof of source-project semantic equivalence or search result
truth is claimed. General project-library extraction is separate work.

## Next minimum evidence

Reviewer `module_anchor_audit` has this exact unused source. Root owns selection
of focused pure/CLI/lifecycle controls and, if cleared, one saved-input real-owner
mapping call. Reuse the existing query extraction/search/module-consumer evidence;
no Lean recompilation, service lease, mathematical contribution or native anchor
rerun is necessary to validate this Python-only seam.

## Focused controls authored, not executed

Root selected source-only controls after source-clearing the entry above.
`software/v5/ordinary_query_context/controls.py`, 19,174 bytes, SHA-256
`bd253397494a63faa6139222667f78789ba7124f301df62f0eaed9ab2592f549`,
is ready for independent review. No runtime, import of product source, native call,
database opening or test execution has been performed by this author.

Six pure/mode groups use the actual six preserved Q/helper modules and the
unchanged context entry; all seven source hashes are checked before execution
and rechecked afterwards. They cover exact ordered projection despite reverse
map insertion and unrelated malformed metadata; all and partly missing names
with no partial binding bytes; malformed selected IDs/map/callback; zero-reference
syntax; per-reference/final allowance calls and propagated exhaustion; and two
valid modes plus 32 refused incomplete/mixed option combinations before dispatch.

The saved four-reference public01 query provides a more discriminating fixture
than the one-reference native02 output. The selected raw fixtures under
`experiments/v5-local-checks/ordinary-query-public-01/public/` are:

| Fixture | Bytes | SHA-256 |
|---|---:|---|
| `query-local/native-type.json` | 373 | `226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480` |
| `fixtures/known-bindings.json` | 451 | `0ebd5b6de9942a1f9359e23c4d7a36219d30bd71af69c73813de8cfd03d95f2f` |
| `query-prepared/QUERY.json` | 1,035 | `eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a` |

The ordered resolution must reproduce the saved binding bytes and the actual Q
construction must reproduce the previously saved manual QUERY byte-for-byte.
This does not rerun the previous query campaign or native02, whose failed harness
status remains unchanged.

Five additional cases call actual `run_context` with **explicit inert owner,
custody, profile, path and adapter doubles**. They test sequencing, not real
owner state: both handles close before writing; missing references produce no
output; both close failures are reported and suppress publication; and a rename
that completes then raises preserves the attempted RESULT hash with UNKNOWN.
Success writes only fresh scratch files. The lifecycle cases are expressly not
evidence for real lock/recovery/path validation, selection authority, discovery,
mathematical acceptance or real-owner accounting. On independent review of the
unused initial controls (`6f036529...`), one context-root mismatch case was added:
`QUERY_CONTEXT_IDENTITY` must refuse before output while still closing both
opened handles. This cheaply covers an earlier-exception path. The suite now
has eleven groups. Socket, subprocess and SQLite
entry points are disabled throughout product-source loading and all controls.

Proposed finite execution (root selection still required): inner 35 wall / 20 CPU
seconds; outer 60 wall / 35 CPU seconds, 512 MiB, two processes. Arguments:

```text
D:\Python314\python.exe -I -S -B <selected-controls.py>
  --helpers <canonical-software/v5/ordinary_lean>
  --formal-query <canonical-software/v5/ordinary_formal_query/formal_query.py>
  --fixtures <canonical-experiments/v5-local-checks/ordinary-query-public-01/public>
  --output <fresh-child-of-selected-run>
```

The selected/snapshotted controls must have exact `query.py` beside them;
the script pins that sibling to `449b5fea...`. Root alone owns selection,
supervised execution, saved-outcome adoption, assembly and the one subsequent
minimal real-owner integration. This author has not selected or launched any run.

Independent reviewer `module_anchor_audit` source-cleared the final
`bd253397...` eleven-group controls after checking the added mismatch case.

Root then assigned a source-only selector. New
`software/v5/ordinary_query_context/select_controls.py`, 4,965 bytes, SHA-256
`801f45e186d39ad04b95cda7fdbd47ad8077572346f8cb9392234671c0414851`,
prepares fresh `ordinary-context-query-controls-01.selection.json` only when
root invokes it. It follows the existing pinned builder/finite runner pattern,
snapshots runner/selector/controls/query together, pins the actual helpers and
three preserved fixtures, and takes only the exact three Python runtime pins
from the pinned native02 selection. No Lean runtime, module artifact, owner state
or unrelated package payload is used by this pure/inert control. The runner's
explicit-runtime, non-hermetic scope remains unchanged. Its intended command is
the CLI above with `{output}/controls` as the fresh child. Selector source review,
its invocation and the bounded control launch remain root-owned; none occurred
as part of this source-only assignment.

## One actual context-query integration authored, not executed

Root next selected source-only `integration.py` and `select_integration.py` in
the same fresh context-query folder. Source pins at submission for review:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `integration.py` | 16,055 | `c51ef8c55d7b95f8170e72127d639fbff579fc85ab3d0053464a6dfa7483dd65` |
| `select_integration.py` | 6,137 | `c3a739564feba537e4fb4723536fda527200d4ff1423f879671fe7109f2fdb88` |

This is exactly one proposed public query CLI invocation, using the existing
protected synthetic owner and original selected context
`94827b21912710d45d0a459d089b741d39a15caf9b60847b5f0553be7457cece`.
The native AST and baseline binding/query/spec/result files are reused, not
recompiled or reconstructed through another manual campaign. The positive
boundary must reproduce BINDINGS, QUERY and SPECS byte-for-byte and preserve
the prior search namespace, features, profile and content hash fields (except
the intentionally new package-profile identity). Query remains nonauthoritative.

The harness pins/rechecks the existing public01 463-entry immutable map,
including the predecessor 252-entry evidence, and the selected package/runtime.
It checks the exact semantic/foundation/implementation/context/store tuple,
four bound references, zero worker CPU, a clean **single-process** query Job,
stdout agreement with the success marker published after both actual closes,
and direct release/reacquisition of the catalog byte-range owner lock. Custody
owns a SQLite connection, not an `owner.lock`; clean process-tree closure covers
handle release without inventing a custody lock or opening a second owner.

Owner reopening may settle old RESERVED operations; mutable database bytes
are intentionally excluded from the immutable-file claim. The source has no
native, extraction, search, admission, certificate, compilation or retry path.
Root requested only the positive case: no naturally all-missing saved query was
selected, and the focused pure/inert controls already cover that refusal.

Both package path and the exact PROFILE/ASSEMBLY hashes are mandatory selector
arguments. Root's planned assembly03 was superseded before native execution by
the guarded-native assembly04 direction; this harness does not assume03 or
alter it. The context-query payload stays exact `449b5fea...`. It accepts the
fixed 134-payload profile and a hash-selected receipt with the native payload
changed, optionally alongside query.py, but no added payloads.

Planned fresh name: `ordinary-context-query-integration-01`; outer 120 wall /
60 CPU seconds, 768 MiB, three processes; harness 90 / 45, 512 MiB; exactly one
query child with at most 45 wall / 15 CPU seconds and one process. The actual
query's cooperative budget is five wall seconds and one CPU second smaller.
All accounting starts at harness boot, and unknown child CPU charges the full
grant before stopping. Root must schedule sequentially with other owner work.

The author has **not** executed the selector, controls or integration, opened
the owner/database, compiled source, changed Git or generated any selection.
Independent source review and root's exact finite selection remain prerequisites.

## Actual integration01: failed harness, successful query, saved-only completion

2026-10-23 Chicago / 2026-10-24 UTC. Root executed the selected integration
once against package04, PROFILE
`b0802fbe33b08bbf57e8050a18e96c2b1d277a75ba53192e51b487d34a3682a9`.
Selection `9e98495421047955361ad37b506bf18504d97e12e28f2ce86c409e42ce9e2516`;
snapshots still match `integration.py` `c51ef8c5...` and selector `c3a73956...`.
**The original enclosing harness remains FAILED** at
`CONTEXT_INTEGRATION_NO_CHILD_WORKERS`. No source/result was edited and no query
was repeated. This paragraph separately completes saved-file checks, not the
original campaign or its false process-count assumption.

The query subprocess itself exited zero and returned the post-finally success
marker. Inner supervision records clean direct-child reap/Job closure, zero
final active or terminated processes, no termination request or cleanup errors,
0.875 inclusive child Job CPU seconds and 0.9713682997971773 wall seconds through
cleanup. Query-reported worker CPU is zero. The enclosing harness used
2.4893621001392603 wall seconds; outer measured Job CPU was 2.078125 and wrapper
CPU 0.53125, for 2.609375 known inclusive CPU seconds. Failed outer exit1 was
also cleanly reaped/closed. Nested CPU is not added again.

### Why the source assertion was unjustified

The observed cumulative `final_job.total_processes` is **2**, not the asserted
1. Reinspection of the exact pinned supervisor (`commons.py` `6ea16154...`) and
Job implementation (`run_stage.py` `bdd2cbc2...`) establishes only:

- `supervise` performs one explicit `subprocess.Popen` for the selected argv,
  creates it suspended and calls `attach_resume`;
- `attach_resume` assigns that process handle to the Job and resumes it;
- `stats` copies Windows `JOBOBJECT_BASIC_ACCOUNTING_INFORMATION.TotalProcesses`
  directly; the wrapper does not synthesize this count or subtract overhead.

No recorded PID/creation lineage identifies the second counted process. Thus
**launcher overhead is not established**, and neither count1 nor count2 is
independent evidence of the absence of descendants or native execution. A
cumulative count is not a simultaneous-active count. The grant's active-process
limit1 and terminal active0/terminated0 remain separately recorded observations.
The earlier prose about a "single-process" Job described the rejected harness
assertion, not an established result. Its claim is superseded by this paragraph.

The retained earlier `ORDINARY-EXCHANGE-CONTROLS02.md` had already documented the
same unjustified expectation and explicitly left lineage unexplained. This
author's new harness repeated that avoidable assumption; it is not a product
failure or a reason to rerun the successful public query. Future assertions must
use actual closure/accounting semantics and source call boundaries, not treat an
aggregate OS counter as an execution trace. No new process-census experiment is
selected, because the saved operation and unchanged product source suffice for
the current query-usability decision.

### Separately authorized saved-file postcheck

Root authorized bounded direct PowerShell reads/hashes and one later lock
observation, avoiding another harness or selection. With a 60-second check bound,
the author checked all **463** entries of the pinned prior public01 immutable
map, totaling **300,807,647 bytes**; every length and SHA-256 still matches. The
read-only checking command completed in 1.4499348 seconds. It also established:

- Actual BINDINGS (451 bytes), QUERY (1,035 bytes) and SPECS (104 bytes) equal
  their preserved manual fixtures **byte-for-byte**.
- Actual stdout is exactly saved RESULT bytes plus one LF; output contains
  exactly BINDINGS/QUERY/SPECS/RESULT and no subdirectory or pending marker.
- All seven baseline hash/key/namespace/features/spec fields match. The selected
  semantic/foundation/implementation/context/store tuple and reference_count4
  match exactly; the new package-profile hash is correct.
- The public reply retains `mathematical_acceptance:false`, the selected-local-
  context interpretation boundary and zero reported worker CPU.
- Inner success and clean closure coexist with, and do not relabel, the enclosing
  harness's preserved failed status.

The independent reviewer subsequently reported the same saved-output agreement,
all159 runtime pins/four snapshots and all463 prior immutable files unchanged.
No further duplicate scan is needed.

### Later catalog-lock observation, not original-harness evidence

At **2026-10-24T02:11:27.1326056Z**, after root explicitly authorized this narrow
check, the author opened the existing catalog `owner.lock` with read/write access
and sharing, acquired `[0,1)` with .NET `FileStream.Lock`, released it and closed
the stream. The file was one NUL byte both before and after: **zero byte writes,
zero owner reopenings and zero database openings**. This establishes release at
that later observation; the original failed harness never reached its lock check.
It does not reconstruct the process lineage, validate custody by reopening it or
turn the earlier harness into a pass. Custody has no analogous owner.lock file.

### Preserved saved-output identities

Paths below are relative to
`experiments/v5-local-checks/ordinary-context-query-integration-01/`.

| Saved artifact | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` (failed enclosing run) | 2,302 | `be583f3aa8bcedca38f551b9a9e5faef24c5287a4c8953d1cc7e90459811f17d` |
| `integration/INTEGRATION-RESULT.json` (failed assertion) | 5,212 | `5c228d9966f2e1bfad1bc8c911bae3a84c2d8069afaf65436c23489d87d9ca6f` |
| `integration/CALL-SUPERVISION.json` | 4,504 | `e6c5d13a0d9aecdec91cbe5f1585de3177911ccf7b952a56c5df7a1cef175149` |
| `integration/query/RESULT.json` (successful public query) | 1,641 | `1f1a4e9d61ca1c8853d0ef7f9ee0954de4edc6f9555da449a6b3cd71e16f3909` |
| `integration/call/stdout.txt` | 1,642 | `b35975cee2e8dd7889402ed13b68fd3307f2c637b6e1c83f433e0246097e5555` |
| `integration/call/stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Binding/query/spec identities remain exactly those in the earlier fixture table.
This is narrow evidence for a usable selected-context query adapter, not new
mathematical acceptance, measured growth, search recall, source-project semantic
equivalence, a full release or proof of a particular OS process-lineage cause.
