# Actual owner-request preparation: independent outcome audit

2026-10-23. Reviewer: `admission_event_audit`.

**PASS for actual protected-context request preparation, not owner use or a new
mathematical acceptance event.** Root's actual operation terminated successfully
and the saved request matches its selected accepted source evidence. This audit
did not rerun preparation, Lean, admission, recovery, or any test campaign. Its
only computation was read-only inspection, hashing and independent reconstruction
of the saved request from existing data. The source/catalog were not modified.

## Exact operation

Directory: `experiments/v5-local-checks/ordinary-owner-prepare-01`.

| File | SHA-256 |
|---|---|
| `selection.json` | `725dcc3d86fd22102ca7c01376392d39f9e93193086e53fc8173d484814bf413` |
| `RESULT.json` | `6c0e135e75e7eac25bfd2d805edb111f8d6cdc9f11226e267eb131e3aa2ce974` |
| `PREPARE-RESULT.json` | `dc59498dcd8f056902edcac06cc5570ec1c0373f888893dbb2b2b1789fb98f79` |

All four actual immutable source snapshots match the selected hashes, including
`owner_request.py` at `b6f39083728304c49f99cd8c223b5e44b3fa89a4c6a1092ec7eefdeddabfcd17`
and `run_owner_prepare.py` at
`6d32ce6b617f733c9605b30d175d4a1a274a11892c2c5ea46cd8f2d6b8a4cb1d`.
The generic request source is unchanged from the independent source review.
The runner implements the recommended `materialized_units <= 1024` preflight.

The actual supervisor result has exit zero, direct child reaped, Job closed,
zero active/terminated processes, no requested termination and no cleanup
errors. Stderr is empty; stdout is the preparation summary, not Lean output.
Recorded cost is 13.5625 worker Job CPU seconds plus 0.234375 wrapper CPU
seconds, 54.2564839 outer wall seconds and 93,335,552-byte peak Job private
commit. The selected bound was 120 CPU / 180 wall seconds / 256 MiB.
The Job's total-process counter is 2; this is not a claim about simultaneous
processes or evidence that a Lean worker ran. The selected script has no native
worker invocation.

## Protected context and exact source locations

The fixed source is the previously adopted local recovery context, not a peer
database or the present preparation's success flag:

```text
context 4d70ddd613bbbfe5e9312ea403e64a95a0a2239842a19d90bf0c044847929026
profile fd23ae289706e5a3277a3c4304de83d65498755dd014b234810e79539f5c8219
basis   cb8f9c2db2b5b53984be1ce8b5f540024264a1e2db41fc7226c594ee1f022299
DB SHA  bcb94ff9695f4d360205eaf8f81151f1cf70437c0e6c434b48f6993d893980e9
```

The actual runner hashes that fixed DB before and after use and opens SQLite
with `mode=ro&immutable=1`. It checks withdrawal before/after, traverses the
four-root accepted chain, checks root/profile/basis identity and no name
overwrites, and hashes each selected local snapshot to its already adopted
record. It obtains 3622 accepted name-to-symbol bindings. The audit separately
opened that same exact DB read-only, reconstructed the four-root chain/bindings,
and confirmed the DB digest was unchanged and withdrawal absent afterwards.
The previous independent recovery acceptance audit is reused, not repeated.

Evidence locations are restricted to the original admission's 2852 numbered
files. The fixed recovery manifest has SHA-256
`4af119ba2ae759634529f01093555ba45bdf420307ab057f61b2085f16f23bef`.
The runner checks every file against that manifest, computes each evidence's
domain-separated unit ID and each export ID, and requires all those names/IDs
to match the adopted context. Selected fetches recheck exact file hashes and
then enter the unchanged strict evidence reader. There is no fallback to an
unwarranted path, arbitrary database, or name-only match.

## Independent saved-request reconstruction

The audit directly checked all 388 request files against `request_files` hashes
and lengths, their exact file census, canonical group bytes and total bytes.
It independently read the original numbered evidence, matched the pinned
manifest, derived export IDs, reconstructed each selected group's rows and
optional unit from that actual evidence, and compared the complete stored
packet for equality. No call to `owner_request.prepare` was made.

All 387 groups matched unique original evidence units. Every source import ID
matched the protected binding map. Semantic references of each prepared group
were either members of that same atomic generated group or already present in
the earlier prepared groups/fixed basis. For all three missing ordinary units,
their full construction imports were also present earlier. All requested target
identities occur in the resulting correspondence map.

Actual request census:

| Item | Actual value |
|---|---:|
| Fixed basis rows | 581 |
| Basis theorem rows reduced to interfaces | 132 |
| Selected groups / selected original evidence files | 387 |
| Group rows | 517 |
| Theorem-interface group rows | 57 |
| Exact-semantic group rows | 460 |
| Complete generated groups carrying unit data | 54 |
| Total correspondence names including basis | 1098 |
| Planned missing ordinary units | 3 |
| Request files | 388 |
| Exact request payload | 4,978,899 bytes |
| Selected original evidence | 5,800,278 bytes |
| Reported selected serialized evidence nodes | 122164 |
| Fixture-wide evidence-map setup | 49,499,157 bytes |

The three missing ordinary units are:

- `group-00205.json`: `DMKN.ReadFootprint.Avoids`.
- `group-00385.json`: `DMKN.ReadFootprint.ReadsOnly`.
- `group-00386.json`: `DMKN.ReadFootprint.readsOnly_insertMany`.

Their complete construction units are retained. Existing theorem interface rows
omit proof bodies; generated units retain their necessary group/computation
data. The 57 theorem-interface group rows include the missing target theorem,
whose construction proof is separately present in its optional unit.

## What this result does and does not establish

The actual prepared artifact is bound to an independently accepted context and
contains the selected semantic closure, rather than another request to replay
the entire accepted proof ancestry. That is real progress toward ordinary
source reuse. It does not prove that these presumed-existing declarations are
present in the target owner project: the runner's presence hint is the stated
fixture assumption, and the Lean helper must check actual membership/semantics.

Preparation still reads full retained evidence for selected groups. Its initial
49.5 MB map construction scans all 2852 fixture evidence files; this is explicitly
one-time local setup, **not** scalable unknown-ID search or an installed persistent
object index. Do not describe the selected-evidence number as the full preparation
cost, or claim proof-body-free acquisition merely because interface rows omit
theorem proofs.

The runner is conditional local integration with fixed adopted identities and
owner-storage immutability, not a peer admission API or hostile-input sandbox.
No owner environment was changed, no theorem was used by Lean, no new catalog
root was admitted, and no reciprocal result or growth advantage was established.
Next useful evidence remains actual ordinary owner use and independently checked
successor contribution, after the separate helper compilation boundary is solved.
