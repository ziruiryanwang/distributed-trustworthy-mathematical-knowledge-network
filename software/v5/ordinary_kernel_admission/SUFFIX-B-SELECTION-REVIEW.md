# Second suffix intake: independent selection review

2026-10-26. `kernel_package_audit`.

**PASS_FOR_ROOT_SELECTION.** Reviewed exact
`experiments/v5-local-checks/std-kernel-suffix-b01.selection.json`, SHA-256
`cc198b16b62623c3ac5803d37a6997243e8f3b219915c0b5c81e3468ffdb326d`.
This is a prelaunch review, not execution or successful part B.

The reviewer read the complete independently audited A outcome
`7ea4ca70d08315abd36975236ec6b5009283b94a936038871f7503eb64078c67`
and root's SUFFIX-A-ADOPTION. A completed both actual CHECKED batches with clean
closure. B selects that actual final root
`674e33cbe441566ea8385e3bb6011b9f2cecaae4b587b50645c975e48c27c95b`.
No parent is guessed, and no redundant status operation is introduced.

Against A's actual saved selection, executable argv changes at exactly three
indices: parent at 37, canonical part-B manifest path at 41, and manifest hash
at 43. The latter is
`a0036d02cc15f0fb5a11d3b02a097870b12b81e963f10db26a9949d6b42b5c5c`.
The previously adopted manifest review covers its exact 429/174 units and
8,899,687/8,867,997 bytes. The actual file rehashes unchanged here; no raw-unit
census or mathematical source review was repeated.

Package/runtime/state/store identities, original materialized unit directory,
public entrypoint, quotas and log ceilings are unchanged. Public limits remain
360 wall / 300 CPU / 1,536 MiB / three processes; outer limits remain 420 wall /
330 Job CPU / 1,792 MiB / four processes. The existing per-operation 60-CPU limit
is unchanged. The named fresh B output directory was absent at review time.

All **three sources and 256 external pins independently rehash**, with zero
mismatches. The source map has exactly A's keys and hashes; only JSON key order
differs. The external map retains all 243 A pins unchanged and adds exactly the
13 files specified by SUFFIX-B-PREPARATION: nine standard A runner/public evidence
files, A outcome and adoption, and its two actual accepted snapshots. No pin is
removed or replaced. The two new snapshot hashes agree with A's audited artifacts:

| Operation directory under `std-kernel-catalog01/operations` | SHA-256 of `chunk.olean` |
|---|---|
| `a0eef708fd11d034016fc2231d5e56c8784b8ad39df675c5e14a99415b4da851` | `41ec2dcb79f902ba46b4e7fe82fc021951ad5ec75e5fc7dd4632689ea2c2cfc5` |
| `8b1a43283e800819bdd240d833c8e0012010adad18360147210980527c00a26f` | `9086d6e0f463505762c8725d3e2fda7827c52ff751ff6f733950ca88495f165a` |

The current package still has exactly its selected 154 files; its census is
unchanged. All earlier runtime pins remain. No mutable database/WAL/SHM file is
pinned. The external map reaches, but does not exceed, the existing 256-pin cap.

Root may select this one operation. Adoption still requires both actual CHECKED
batches, COMPLETE, exact bindings/artifacts and clean closure; any refusal and
its costs remain preserved. This selection launches no contribution or subsequent
publication and establishes no full v5 completion.

Only source/JSON reads, ordinary-file census, comparisons and hashes were used.
No product import, owner/status command, database, native execution or Git
mutation occurred.
