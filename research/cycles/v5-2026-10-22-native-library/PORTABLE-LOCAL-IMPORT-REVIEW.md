# One-time portable local import: independent source review

2026-10-23. Reviewer: `admission_event_audit`. Source-only: no importer, tests,
native runtime, SQLite connection, accepted-state mutation or Git operation run.

## Disposition and exact cut

No blocking authority or compatibility defect found in the final source below,
conditional on the explicitly adopted original checking lineage and same-checker
interpretation. The implementation supplies a concrete metadata transition, not
a mechanism for trusting a peer's snapshots. Root still owns the exact source
manifest, implementation/support selection, finite controller and actual run.

| Source/context | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/legacy_catalog_import.py` | `0b0a9a36829482a880b291977259ddae786d680fa9970777f339f7827f6e9f35` |
| `PORTABLE-LOCAL-IMPORT-IMPLEMENTATION.md` | `daced024aff7c3942589fb66437430c6513e0547e2bca5ae6ff63b40ea2e3003` |
| `software/v5/ordinary_lean/portable_catalog.py` | `2d0e91b2920abb69304b920a676da202a5e2444ddec37805d19e953b69eebf35` |
| `software/v5/ordinary_lean/legacy_identity_translation.py` | `59c8f3549e775e5922902b0e6d9b2fcedfd2d3c10ab0f052b191c6906c09eb3f` |
| `PORTABLE-SUPPORT-CORRESPONDENCE.md` | `ade45957f49d7078c46819dd020cda5c63d19d879571f4b958d6b5ede6386fba` |

The complete initial importer and every final changed region were read, along
with the complete implementation handoff, catalog/translation sources and
correspondence context. The retained original `native-admission/PROFILE.json`
and the original support-domain construction were also inspected. This review
reuses the already completed catalog and pure-translation audits rather than
rerunning their controls or rechecking accepted proofs.

## Why this is a justified local transition

The caller must select the already adopted successor catalog at the explicitly
restricted owner-local path. The input manifest is trusted controller selection,
not self-authenticating evidence. The importer takes the source owner lock,
opens SQLite read-only (without calling `LocalCatalog.open`), rejects journal/
WAL/SHM sidecars and active reservations, and validates the exact marker and
database pins. It reconstructs the full selected basis-first chain, original
profile/root formulas, committed-operation linkage, source record hashes and
actual snapshot bytes. Extra committed branches, omitted roots, duplicate
evidence paths and inconsistent final-root selection refuse.

Correspondence requires exact equality of original, new implementation and
selected descriptor support. The retained original PROFILE must be present;
its kernel/adapter/basis-receiver domain hashes are recomputed. Every named
support-map leaf must resolve to a selected actual file with the same basename,
size and SHA-256, already byte-verified. Snapshot support is derived specifically
from the retained BasisSnapshot/LocalSnapshot source and compiled maps. This
does not claim a hermetic toolchain or prove checker correctness from hashes.
The original actual checking event and adopted source-to-S argument remain
independent premises, explicitly retained rather than manufactured by a PASS file.

The exact fixed seed and inventory hashes are checked before their JSON is
interpreted. All 581 original basis bindings must equal the reconstructed fixed
inventory mapping, not merely have the right cardinality. For each later batch,
the unchanged pure translator checks every imported old ID against the current
old prefix and pairs it with its portable ID. Complete raw declaration units
and names remain unchanged. The complete ordered original outputs and original
batch hash must match the accepted record before its translated root is added.
Therefore the name-pair invariant is preserved by induction; metadata renaming
does not require replay of the already checked proof terms.

## Activation and preservation

New evidence remains inert. Independent snapshot copies are chunk-hashed and
read back; old snapshots and exact original record bytes are retained unchanged.
V2 roots use the separate legacy-root domain and retain original embedded module
names and parent names. Original check support and translation support are
recorded separately. No native process or new native checking event is invented.

The source lock remains held through the catalog's single activation transaction.
Its two source rechecks verify every accumulated selected source/support/evidence
pin, including files read during translation, plus withdrawal and sidecar state.
The same nonrenewing deadline applies. Failure leaves a fresh destination in
retained quarantine, or requires explicit inspection after an uncertain commit;
there is no retry, source recovery or dual-store promotion. All failed original
operation history remains untouched in the archival source.

After activation, V2 is the sole operational authority. Owners must apply any
retained-support withdrawal to V2; the importer does not install a permanent
watch on the old catalog. Protected owner/OS state and no unauthorized rollback
remain assumptions, as in the catalog contract.

## Practical boundary caught before any run

The first source default allowed only 64 MiB per input file, while the actual
adopted `libleanshared.dll` is **70,414,848 bytes**, exceeding 67,108,864. This
would have predictably refused complete actual-support validation. The reviewer
flagged it before runtime; the author changed the final per-file default to
128 MiB and documented why. Hashing/copying still uses 1 MiB chunks, so that
acceptance cap does not allocate a 128 MiB buffer or enlarge a Lean process.
No failing experiment or weaker support check was needed.

The final source also avoids an unnecessary initial all-file rehash. The two
activation rechecks still each make a linear SHA pass over selected inputs.
`max_input_bytes` counts unique selected input bytes, not total physical reads:
CPU/I/O cost and the two additional passes must remain visible in whole-operation
accounting. All passes share the original deadline; no proof checking occurs.

## Remaining integration obligations

This is not an executed import or public deployment qualification. Root's driver
must select the exact currently adopted source/database/ordered evidence, resolve
the retained support leaves (using preserved source snapshots where current
development files changed), bind current controller support to the actual source
assembly, and enforce finite process/memory/CPU limits. Missing or incompatible
input refuses rather than silently falling back to replay or a weaker premise.

Use the small changed-boundary storage/import controls and one actual import,
then a small genuinely new native extension using the imported parent's actual
module plan. The old successful basis/library checking, pure translation and
seven-unit reciprocal loop do not need another run. This change removes local
identity fragmentation; it does not by itself solve cold full-context loading,
arbitrary branch merging, world-scale discovery or sustained useful growth.

## Concrete selectors and one-unit native handoff review

Root subsequently supplied the concrete import selector/driver and extension
selector; the importer author supplied the one-unit native controller. Their
complete sources were read, including the final controller's changed chunked
support-pin loop and nonrenewing grant/worker deadline checks. No selector,
importer, test or worker was executed by this review.

| Additional source | SHA-256 |
|---|---|
| `select_portable_import.py` | `901cf63b743edd55e017c16db45a4e23658f561c6e0c6df26f5adb6fb35b1cb2` |
| `run_portable_import.py` | `da335e8dafa5322f62e9f4b3cc066c96d8c99f861419257de41cd73b99cf9d4d` |
| `run_portable_extension.py` | `5ac9bfd2c11541810ef376ea042de30d8bcf2275130a5e006f5caa76684ba0c8` |
| `select_portable_extension.py` | `656a5ae7048b607f443c5665408744a094d15bbed5cd3b2b0a48620125b4daa2` |
| `PORTABLE-NATIVE-HANDOFF.md` | `6f777ea460dccd98fb5b8b5f3ed29f6e2d285e190f836723a03debf120ce11a7` |

Python paths are under `software/v5/ordinary_lean`; the handoff is in this cycle.
No blocking source/path/compatibility defect found at these cuts. Actual import
and actual extension remain distinct root selections, with the latter dependent
on an independently adopted successful import and its concrete data manifest.

### Avoiding a second migration

The initial implementation identity commits the selected controller source map.
A new native controller added only afterward would not belong to that immutable
commitment. Root and reviewer identified this before import. The final import
selector now includes `run_portable_extension.py` in the initial source map.
The later extension selector/controller requires its six executing current
sources to match that preserved map and recomputes I's controller-support digest.
The new file-only extension selector chooses inputs but is not falsely claimed
as an executing native admission controller inside the original map. No marker
relaxation, undeclared supporting executable or second migration is needed for
this selected handoff.

### Concrete file/cardinality preflight

Read-only filesystem inspection found five exact `chunk.olean` files and one
empty retained failed-operation directory
`7160c6db37d6548f76f6fa319131ca50c8428147f85f278697a9613eddf1abcb`,
consistent with the source-tree allowance. All fifteen selected supervision,
worker-report and nested-command paths exist. The retained original selection
hash is `ab2f655448242587880129e62cca4bc5dc74638c1e8699e30b4a9f67e26fce5f`;
the successor result hash is
`188110017e34f123f2a6b6fe9b6eb4df7dcd3d9ace888dd0beec9669a9de28a6`,
matching the selector's adopted pins. No database connection was needed here.

The original 2852 evidence files total 49,499,157 bytes; the largest is 970,480
bytes. The selector's basis/1024/1024/804/7 schedule therefore selects all 2859
units in their original order, with the last seven from the independently
accepted successor. It resolves old support sources from their preserved
snapshot instead of substituting current edited development files. Manifest
pins keep the outer runner below its 256-runtime-pin limit; the importer then
checks the fully enumerated actual evidence/support files itself.

The import driver checks its snapshotted controller map against I, shares one
155-second monotonic deadline, calls the importer once, and actually reopens
the ACTIVE result and compares all five original module names and 3629 bindings.
Its selected outer limit is 120 CPU seconds / 180 wall seconds / 512 MiB.
No saved result is supplied as a new kernel-checking event.

### Exact changed native boundary

The extension selector requires an actual completed import, captures its exact
tree and locates the target evidence through the audit's unique output entry.
The controller independently checks that relationship and the target's portable
UnitID/export against the protected context. It preserves the target theorem's
type and universe parameters, constructs a one-constant proof of the alias,
and resolves the complete new unit's imports against the accepted prefix.

The exact copied imported parent is experiment preservation, not a peer store.
The original stays locked during copying; full pin/tree checks precede and
follow it. Only the copied database receives a new operation. The original
worker sources, compiled module directory censuses, kernel binaries, supervisor
and Python runtime remain pinned. Large binary hashes use 1 MiB reads, not
whole-DLL allocation. No helper rebuild or accepted-proof replay is selected.

One live grant binds the new unit, actual imported parent module and full plan.
The retained worker receives that plan and checks exactly one complete new
unit. Only its actual clean supervised exit, immutable input rechecks and exact
module/parent/name/unit-count/size report permit `_commit_checked`. The controller
then checks the complete 3630-name map, six-module plan, new `native-check`
origin, and exact reopen. Grant/worker allowances cannot extend the original
controller deadline; error paths retain and charge staging, not retry it.

The extension's selected ceiling is 90 CPU seconds / 120 wall seconds / 1536 MiB
/ three enclosing processes. The new theorem is deliberately an alias: it is
an exact compatibility discriminator, not novel mathematics or growth. Whole-
store copy/hash and repeated selected-file checks remain explicit test costs;
this review does not promote them to a scalable per-contribution product policy.
