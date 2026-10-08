# Offline source packager: independent source review

2026-09-21. **SOURCE PASS after the path-preflight correction described below.**
No remaining source-level blocker was found for the narrowly scoped, cooperative-
filesystem development packager. Execution, archive outcomes and installation are
not qualified by this review. Root may proceed to the separately reviewed bounded
contracts and fresh source-package allocation; this is not authorization for an
external publication or a product-release claim.

The auditor read source/documentation and selected Python standard-library source,
enumerated selected paths, and independently hashed current selected files. No
builder/product execution, imports, AST processing, SQL, ZIP operation or source
edit was performed. This review note is the only audit write.

## Reviewed cut and selection

| Selected file | Bytes | SHA-256 |
| --- | ---: | --- |
| `release/package_source.py` | 14,011 | `8062fe2b4d9cc75279f512fc288727617ccc4017dea1b74f5a1a10fd2286e837` |
| `release/README.md` | 8,181 | `DCCCDD525B118C21D5BF558F175D480F7276A1E226F21AA86DD6C5E8BBA9E90F` |
| `assets-lock.json` | 18,914 | `887230fc0a0bb52350cf5c0b3e2233ab015eda1649d634a3e15cf740c8fc0492` |

The current selection is exactly **108 distinct files, 3,555,524 bytes**; maximum
individual size is 823,690 bytes. Its membership is two entry points, nineteen
Python modules, three Lean sources, seventy-five assets, the asset lock, five
operator documents, the two release files and one quickstart. The actual
quickstart is `drafts/OPERATOR-QUICKSTART.md`, renamed inside the package to
`QUICKSTART.md`; the alternate top-level source does not exist at this observation.
This is a current mutable-source measurement, not reuse of a historical native
qualification manifest and not the final future package's identity.

All **81 asset-lock rows** match actual file sizes and hashes: six specifically
named code/native files and seventy-five assets. Duplicate JSON keys/rows, boolean
or noninteger counts, missing mandatory files and paths outside the fixed narrow
shape refuse. The five common-package names are fixed; lock-controlled objects
can only be lowercase hexadecimal CBOR basenames in their object directories.
The lock is itself packaged and reread against the initial lock observation.
It is an owner-selected integrity commitment, not an authenticated remote trust
root or a claim that packaging verifies CBOR mathematics.

The actual `py`, `native` and `assets` sets match the allowlists. Their directories,
the source ancestors and selected release/draft directories contain no observed
reparse substitutions. The tool checks exact selected-tree membership rather than
recursively accepting arbitrary contents. Other top-level directories are not
traversed; runtime, build, test, experiment, state and scratch trees are excluded.
Selected owner-authored text is not automatically free of secrets, licenses or
absolute paths; the README correctly requires content review before sharing.

## Finding closed before execution

The initial builder, SHA-256
`d3d46f51f4c8d9521e9dafdebb31f302133e9d1d9dbe2d6cf631401c6589c055`,
used lexical `Path.is_relative_to` on input spellings while permitting extended
Windows anchors. For example, ordinary `E:\tree\software` and extended
`\\?\E:\tree\software\package` can refer to nested locations but compare under
different anchors. The advertised containment check therefore lacked the needed
namespace normalization. This source finding was reported immediately; no
reproduction run or directory creation was performed by the auditor.

Root's reviewed correction requires an ordinary drive-letter anchor before path
access, rejects root/traversal/reserved/colon/trailing-space-or-dot components,
checks original existing ancestors before resolution, strictly resolves source
and output parent, revalidates the resolved namespace/ancestors, and constructs
the absent output from that parent and the original single basename. Containment
is then compared in those resolved names. The original builder entrypoint is also
checked for reparse ancestors before its strict resolution and comparison with
the selected source builder. Failure evidence uses the selected canonical output.

Reading the selected Python's `pathlib.resolve` and `ntpath.realpath` confirms that
strict Windows resolution uses `_getfinalpathname`; for ordinary inputs the
extended prefix is stripped only after confirming the nonprefixed spelling has
the same final path. A resolved UNC/device spelling is refused by the reapplied
drive guard. This closes the identified namespace-spelling bypass within the
trusted stable-filesystem profile. It is not a proof against hostile concurrent
mount changes, pathname races or every Windows filesystem alias; platform alias
behavior still belongs in bounded contract evidence where available.

## Safety and byte-identity assessment

- Output must be absent with an existing checked parent and outside the source.
  `mkdir` creates no parents and accepts no existing allocation. Every file write
  uses exclusive creation. There is no deletion, replacement or retry cleanup.
  Post-creation errors retain partial files and attempt a new failure marker.
- Selected reads reject links/reparse ancestors and nonregular/empty files.
  Metadata identity/size/timestamps/attributes are checked before opening, on the
  opened handle before/after reading, and afterward at the path. Post-ZIP source
  checks compare bytes and observations again. These are change-detection samples,
  not an atomic snapshot or adversarial isolation.
- Per-input 2-MiB, lock 64-KiB, 128-source-file and 16-MiB aggregate limits are
  explicit. Selected directory enumeration, path depth and manifest size are
  bounded. ZIP verification reads at most 18 MiB. Fixed/allowlisted bounded
  member names and stored compression keep archive overhead bounded. These are
  algorithmic compatibility limits, not OS quotas or a wall-clock deadline.
- Sorted paths, exact captured bytes, stable canonical JSON, fixed ZIP timestamps,
  regular-file 0644 attributes, empty comments/extra fields and stored compression
  remove intended host/time/random variation under the selected Python profile.
  No absolute source/output path is dynamically added to the manifest/result.
  Content already present in a selected document remains unchanged.
- ZIP verification requires the exact ordered member list, no archive comment,
  expected file lengths/compression/timestamps and exact member bytes; a second
  bounded archive read checks byte stability. The external manifest is written
  from the same byte string as the embedded manifest. The result is written last
  and binds archive/manifest hashes and counts. Attributes are fixed at writing;
  their output equality remains an appropriate independent contract assertion.
- The manifest does not hash itself: the result binds the manifest, whose rows
  bind the selected payloads. ZIP membership adds exactly that manifest to the
  selected source rows. This avoids a circular identity requirement.

A final marker is neither a signature nor a durable directory transaction. A
process/power failure can leave a partial marker; consumers must require complete
parseable bytes and verify all referenced hashes. Hard links and a writer racing
the final observation are explicitly outside isolation guarantees. Failure to
persist the failure marker is reported separately, without deleting evidence.

## Claims and qualification handoff

The success name is honestly `DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED`. Packaging
has no Lean execution, product import, database operation, dependency download,
signature, license selection, runtime inclusion or external publication. The
README and included quickstart correctly distinguish same-host current-source
instructions from historical source-cut outcomes, arbitrary peer-source safety,
fresh-operator qualification and v1 readiness. Excluded historical links are
identified as such rather than represented as package-local evidence.

The next contracts should establish exact membership/hash/count/metadata and
determinism on inert selected inputs, plus refusal and unchanged-output evidence
for reused output, bad namespaces/overlap/reparse paths, missing/extra selected
files, lock corruption, bounds, ambiguous quickstart and observed source change.
A separately allocated actual-source run must bind its own current source hashes;
neither synthetic contracts nor this source review establish its result. Fresh
extraction/build/operator execution and exact-manifest integrated product
qualification remain subsequent release work. Do not translate source-package
success into mathematically useful growth or decentralized-network readiness.
