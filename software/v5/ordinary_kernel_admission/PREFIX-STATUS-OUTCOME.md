# Independent actual retained-prefix status audit

Disposition: **PASS_SELECTED_PREFIX_CURRENT_LOCAL_CONTEXT**.

Saved run: `experiments/v5-local-checks/std-kernel-prefix-status01`.
The reviewer used saved-file reads, hashes and JSON comparisons only. No product
import, owner/status invocation, database access, native execution or Git change
was performed. This audit concerns the status operation already completed by
root; it launches no continuation.

All **three current/snapshotted source pairs** and **232 external pins** match
selection `7c262debd658e1c6443dd9cd1e8b211e1704303b0422a3e1b3487b18d70b1084`.
Original and saved selection bytes have that same hash. The current package's
complete 154-file census still equals its selected map. The outer recorded argv
equals the selection after the two prescribed placeholder substitutions; public
LAUNCH and SUPERVISION argv agree. Public RUN and outer stdout JSON agree.

## Confirmed current context

The owner returned `ok=true`, operation `status`, `LOCAL_OWNER_OPEN`, and the
exact selected catalog/custody paths and quotas. Its PROFILE is
`60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b`;
public RUN binds installation manifest
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.

| Binding | Actual value |
|---|---|
| Store | `fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7` |
| Implementation | `86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea` |
| Semantic ID | `9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7` |
| Foundation | `884f408f0e7d647a1b72714cfa78685804dea9e07289a67176692cfbfe2c8282` |
| Basis | `4d7cc70e515293b3037a8fa34f60fa97fe082196e005aa7cd894204464ca5f2b` |
| Selected prefix | `c3d0f6209f42abdc98a6975a358545b0d61701e849b6ed0a3e69bdc1b7f400f6` |
| Context | 1,743 names; two modules; 2,820,152 artifact bytes |

The bounded root inventory contains **exactly two entries**: this basis with
empty parent and this prefix with the basis as parent. `has_more=false` and
`next_after_root=null`. Thus the expected inventory is complete for this
observed local catalog, with no additional committed root reported. The selected
context is non-null and has every expected identity and count.

Custody reports **2,048 objects / 2,192 exports / 28,559,972 logical bytes**, all
within the unchanged 4,096 / 8,192 / 134,217,728 quotas. Its semantic ID matches
the selected context and `mathematical_acceptance=false`. These are the public
stored-counter observations, not an independent audit of every database row.
Retained custody from the unsuccessful second batch does not establish a second
accepted mathematical context. Custody put precedes native admission and retains
its inert objects when admission later fails.

## Immutable artifacts and closure

Both pinned snapshots remain exact:

| Relative operation path below `std-kernel-catalog01` | Bytes | SHA-256 |
|---|---:|---|
| `operations/7816507ebfdacca0e8de26d1100226c7d9a6c37fad07229373a491e39bef7bc8/chunk.olean` | 669,968 | `627f13203ff33d4134daad615a81c53238a037a6ec74e8155816788fb3132bc5` |
| `operations/f1b41c5c66464e8f181b21061a3c4a2d70638953c43a1069a6471b089053113c/chunk.olean` | 2,150,184 | `1959cf9a4dbc022d9dd1d9b93d5e178d507d0d1b592da03a7b87ce03ceef96b1` |

Public and outer supervision both report COMMAND_EXITED_ZERO_AND_CLOSED, exit
zero, direct child reaped, Job closed, zero final active processes, no cleanup
errors and no termination request. Both stderr files are empty; there are no
owner close errors. Public RUN is `ok=true` / CLI_EXITED_ZERO. The owner reports
**zero worker CPU**, consistent with the reviewed status route launching no
Lean checking worker. Status verifies retained bindings and snapshot bytes; it
does not replay the prefix's proofs.

Whole runner wall time is **2.4383179 seconds**. Inclusive outer Job CPU is
**1.140625 seconds**, plus **1.0625 seconds** wrapper CPU, totaling
**2.203125 known CPU seconds**. Public Job CPU 0.984375 and owner controller CPU
0.9375 are nested observations, not additional charges. Outer peak aggregate
private commit is 51,404,800 bytes; public peak is 32,260,096 bytes. The unchanged
outer 60-wall/20-CPU/768-MiB and public 35-wall/10-CPU/512-MiB envelopes completed
without exhaustion.

## Evidence and interpretation

| Saved evidence | SHA-256 |
|---|---|
| `RESULT.json` | `9a83a1367d436134542d7f81d8a6f37821454a260c8a354bffe6d12a571de383` |
| `owner-status/LAUNCH.json` | `e239e2880497f5695e8806920b57198ac7752a8f6048afa90459776c766a208e` |
| `owner-status/RUN.json` | `9450fb899323f54e95dc4a6c0480ac79efc59a2833275145becf39e7972b87d7` |
| `owner-status/SUPERVISION.json` | `81d9603032bb737609c747cdae9fc97d54c80b74a927ba82d36ed14f421b849d` |
| `owner-status/child/stdout.txt` | `b0cff75ca06c31df9db448617880e6acf23c7920954651d420e15f35af42283e` |
| `command/stdout.txt` | `fadf363bab03830df738cff1bfaa3954282ab35a4d85c3f9890731199b5219cd` |

This is new evidence that the selected prefix is currently a usable protected
local context. It does not assert database-byte preservation: ordinary recovery
was permitted by the reviewed operation. Nor does it prove that custody data is
mathematically accepted, provide a peer-transferable certificate or complete the
full baseline intake. The failed intake and its historical
`possible_unreported_commit=true` remain unchanged. Root may use this result to
select a separately reviewed finite suffix operation; no suffix execution or
budget renewal follows automatically from this audit.
