# Dedicated hosting burden: current package and existing pure alternative

2026-10-28, growth_design_audit. Manifest arithmetic and selected startup-source inspection only.
No runtime/tree scan, native hash pass, benchmark, owner/database open or Git action.
Numbers are selected-file bytes, not RAM, installed totals, downloads or latency improvements.

**Conclusion:** Python-only hosting already exists and is adopted in
[ordinary_inert_mirror02](../ordinary_inert_mirror02/ADOPTION.md). The worthwhile
question is carrying current incremental-host behavior into that lighter role,
not inventing another host. The integrated host currently requires substantial
irrelevant Lean support: 36,911,142 packaged bytes plus 212,588,544 explicitly
pinned external Lean bytes, even though it starts no mathematical worker.

## Exact current census

Current integrated entrypoint is [incremental-host ADOPTION](../ordinary_incremental_host/ADOPTION.md).
K denotes `experiments/v5-local-checks/incremental-kit-pack01/packed/commons`.
The kit's package is **K/package**, not K itself. Counts sum `KIT-MANIFEST.json.files`
rows, cross-referenced to PROFILE/INSTALLATION; no payload enumeration or rehashing.

| Selection | Files | Bytes |
|---|---:|---:|
| Complete kit payloads, excluding its manifest | 266 | 43,004,375 |
| `package/` payload subset | 160 | 39,642,332 |
| `package/authoring/helpers/` Lean compiled helpers | 70 | 21,200,496 |
| `package/authoring/bin/` two exporter executables | 2 | 1,577,472 |
| `package/installation/lean-lib/` native `.olean` modules | 8 | 13,954,288 |
| `package/installation/lean-src/` worker/helper source | 8 | 130,051 |
| `package/module/OrdinaryModule.lean` | 1 | 48,835 |
| **Disjoint packaged Lean/native categories above** | **89** | **36,911,142** |
| `package/installation/foundation/` seed + inventory, separate | 2 | 1,547,864 |

The highlighted categories are 93.11% of package payload bytes. They exclude the
foundation files, Python source, metadata, guides, and kit build/source companions.
Dropping all highlighted categories leaves 2,731,190 package bytes before any
role-specific source changes; this is arithmetic, not a proposed complete release.

`INSTALLATION.json.files` separately pins these external runtime attachments:

| Attachment selection | Files | Bytes |
|---|---:|---:|
| Lean `bin/lean.exe` and five runtime DLLs | 6 | 212,588,544 |
| Python `python.exe`, `python314.dll`, `python3.dll` | 3 | 6,958,752 |

Lean's selected subset is 202.740 MiB: executable 83,456; libInit_shared.dll
28,345,856; libc++.dll 1,659,392; libleanshared.dll 70,414,848;
libleanshared_1.dll 52,662,272; libleanshared_2.dll 59,422,720 bytes.
External attachments are outside the package census; their sum with the highlighted
categories is 249,499,686 disjoint bytes. Full Lean libraries/development files are
outside this pin census: no installed-total estimate follows. Python stdlib/SQLite/TLS
also exceed its three pins and remain necessary.

## Why an inert command still requires them

Current HOSTING.md requires Windows/Python/Lean roots. `run.py:248` authenticates
launcher support and the three Python pins; `run.py:330` also requires a Lean
directory, adds its bin path and forwards it to every host child. It does not
execute Lean. `host.py:143` calls the full `profile.load` before configuration.

`profile.py:184-242` authenticates all 122 PROFILE payloads (23,703,479 bytes),
checks helper directory censuses, loads authoring and owner-related modules and
calls `NativeInstallation.open`. `ordinary_admission.py:158-277` validates the
full native support relation, requires both runtime roots, then hashes **all 36**
installation-manifest entries (235,396,198 bytes including both external pinsets).
Its `_verify` streams their bytes; there is no native checking subprocess here.
The loader's AuthoringProfile.verify rehashes PROFILE pins, and host finalization
calls it again. These are repeated reads, not additional installed bytes. They
do not prove host data's mathematics and are unnecessary in principle for an
independently pinned pure-host implementation. This is a dependency observation,
not a measured latency claim or permission to bypass current package checks.

## Existing lighter baseline and the actual missing seam

Mirror02 selects 27 pure source/data files, **1,212,995 bytes**, including inventory
(823,690 bytes). No Lean, native build, PROFILE/INSTALLATION or owner is required.
Three Python pins total 6,958,752 bytes. These figures exclude companion files and
the rest of its selected investigator source distribution; they are a loader
selection, not a claim of a standalone 1.2-MB installed application.

Mirror02's actual public prepare, unknown-ID search, exact retrieval, finite
service and stale-snapshot refusal passed. The original mirror's failed service
remains historical; use repaired mirror02. It prepares a finite bundle with
syntactic import closure against the basis and seals a particular data snapshot.
It has no supported append/update operation; changing that snapshot invalidates
its descriptor. Current integrated host instead initializes once, appends selected
partial bundles, and serves under a stable **configuration** descriptor with
current snapshot metadata. Its legal partial-commit prefixes support growth
without rebuilding a whole closed generation. Those are the capabilities to retain.

Reuse the established pure loading/supervision approach where compatible, with a
small explicit compatibility decision for incremental state and incomplete bundles.
Do not promise that the unchanged static mirror accepts new handoff deltas or that
removing Lean confers portability beyond the selected Windows/Python profile.
Seed/inventory removal is a separate dependency decision; the existing pure mirror
deliberately keeps inventory, so it is not included in the certain Lean savings.

Pins checked on these small manifests: KIT `efeb28150e429f6bcb0e41db2070183b21fd1395c426aca317dd62b31593eecd`;
PROFILE `e8d33500db4c0a5ce89b2dfb51c3e1f9ec8f12063bbc58fe5e4eb23c2b6dfb13`;
INSTALLATION `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`;
mirror SOURCES `1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9`.
