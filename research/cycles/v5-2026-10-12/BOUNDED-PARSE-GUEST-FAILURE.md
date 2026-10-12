# Bounded-parse guest: retained failure and resolver-cache repair

Date: 2026-10-12. Owner: receipt/source-loop lane. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

Status: **source-only successor ready for independent review; no operation02
has been launched by this lane.** This checkpoint preserves the failed first
operation and defines the fresh repair. The original
[guest plan](BOUNDED-PARSE-GUEST-PLAN.md) is historical evidence, not permission
to edit its five now-used files or restart its allocation.

## What failed, and why

The first operation reached only Cargo's offline unit-graph command. Cargo
refused with:

```text
error: failed to download `ark-r1cs-std v0.5.0`

Caused by:
  attempting to make an HTTP request, but --offline was specified
```

The cache selector had conflated **packages producing compiled units** with
**packages whose manifests Cargo must inspect while resolving those units**.
The former is not a sufficient archive input closure for the latter. The
freshly copied359 cache files and38 project snapshot files matched their
selected pins according to independent assurance; copy corruption did not
cause this failure. Author and review both missed the closure distinction.
The observed refusal is therefore a build-cache design error, not a
mathematical-checker regression.

No graph was produced, no compiler command followed, and no ELF, image,
guest execution, receipt or proof exists for operation01.

### Frozen failure evidence

All paths in this table are below
`experiments/v5-local-checks/`.

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| bounded-parse-guest-build-01/RESULT.json |4187|1f97e4d5c3a6f0c9d704970adcc91a128eb237d541fa71365a99690c1c58d8e8|
| bounded-parse-guest-build-01-attempt.json |110|3ea21a5d9200340ec10763da83e42290b68cc6142b87f94a42f2bb5166411af2|
| bounded-parse-guest-build-01/commands/offline-bounded-graph/command.json |2367|024431af99a84c2ff4ea404f5a671174c224c3452c355467c64475b3c8409c55|
| bounded-parse-guest-build-01/commands/offline-bounded-graph/stderr.txt |126|a54f0ca1f3b418c6a04ed5833b4d5f8d9d11daeb525c80fdf4013b8de872767a|

Selection SHA-256:
`be47024a42da96b5d33dcbea8e9ffcc4f2d81be50cc30a1f58ff0b2d4da0e41d`.

The status remains FAIL with
`RuntimeError: UNEXPECTED_CHILD_EXIT offline-bounded-graph`.
Retained costs: **0.75 inclusive worker CPU seconds +19.375 controller CPU
seconds;89.82956409989856 total wall seconds**. The Job closed with0active,
0terminated,7total processes and26,259,456B peak private commit. The final
output census was1144entries,28,369,513B working bytes and13,640,297B archive
bytes. These costs remain charged and appear explicitly in the successor
RESULT's predecessor-failure record; a repair does not erase them.

## Why this repair is a complete bounded decision, not a one-crate retry

The unchanged project/std lock union has220 registry package versions and198
distinct names. The old successful graph has297 compilation units containing
160 distinct registry versions. Read-only examination of the retained seed
and old extracted-source directory inventories established:

| Set | Count | Meaning |
|---|---:|---|
| Locked registry versions |220|Union of the exact project and std locks|
| Compiled registry versions |160|Versions occurring in the297-unit graph|
| Available locked archives |180|Seed archives present with exact lock checksums|
| Old extracted locked packages |173|Exactly173 in both old graph and old compile caches|
| Added available archives |20|Available180 minus compiled160|
| Missing locked archives |40|Absent as archives and as extracted manifests in all three checked caches|

The three read-only inventory locations were:

- `experiments/general-checker-guest-03/prepare-03/cargo-home/registry/src/index.crates.io-1949cf8c6b5b557f`;
- `experiments/v5-local-checks/aggregate-guest-build-01/cargo-home/registry/src/index.crates.io-1949cf8c6b5b557f`;
- `experiments/v5-local-checks/aggregate-guest-compile-01/cargo-home/registry/src/index.crates.io-1949cf8c6b5b557f`.

Both old successful operation caches have exactly173 source-package directories,
with no directory outside the lock union. Those173 are available in the selected
seed. Hence13 resolver-only packages were extracted even though they never
became a compiled unit. Seven other locked archives are available but were not
extracted by those old operations.

The repair chooses **every one of the180 checksum-matching available locked
archives**, not only the first reported missing package or a guessed subset
of13. It does not copy old extracted source trees, the whole524-archive seed,
or unrelated versions. The same198 sparse-index entries and registry config
produce a379-file private cache. Only20 archives and1,898,069B are added.
The archive total becomes15,538,366B; sparse-index bytes remain9,755,696B.
The registry config retains its exact seed pin.

### Exact additional archives

These13 have extracted manifests in both successful old graph/build caches:

| Package/version | Archive bytes |
|---|---:|
|ark-r1cs-std@0.5.0|103859|
|bit-vec@0.8.0|24132|
|embedded-io@0.4.0|12901|
|embedded-io@0.6.1|13133|
|getopts@0.2.23|21409|
|proptest@1.11.0|207859|
|rand_chacha@0.9.0|18258|
|rand_xorshift@0.4.0|10262|
|rand@0.9.5|100216|
|rustc_version@0.4.1|12245|
|unarray@0.1.4|12895|
|unicode-width@0.2.1|279344|
|valuable@0.1.1|28679|

These7 are also available and locked but were not extracted there:

| Package/version | Archive bytes |
|---|---:|
|adler2@2.0.1|13366|
|fnv@1.0.7|11266|
|memchr@2.7.5|97603|
|miniz_oxide@0.8.9|67132|
|rand_core@0.9.3|24543|
|windows_x86_64_msvc@0.52.6|832564|
|windows-targets@0.52.6|6403|

Every digest is read from the pinned seed map and independently required to
equal its parsed lock checksum. For example ark-r1cs-std0.5.0 is
`941551ef1df4c7a401de7068758db6503598e6f01850bdb2cfdb614a1f9dbea1`.
The runtime CACHE-SELECTION record will expose the exact20 name/version,
path, size and digest rows; these are not accepted on name alone.

### Exact40 missing versions and scope limit

```text
addr2line@0.25.0
bitflags@1.3.2
block@0.1.6
cc@1.2.0
core-foundation@0.9.4
core-foundation-sys@0.8.7
core-graphics-types@0.1.3
dlmalloc@0.2.9
errno@0.3.14
foreign-types@0.5.0
foreign-types-macros@0.2.4
foreign-types-shared@0.3.1
fortanix-sgx-abi@0.5.0
gimli@0.32.0
hermit-abi@0.5.2
libredox@0.1.25
linux-raw-sys@0.12.1
malloc_buf@0.0.6
metal@0.29.0
objc@0.2.7
object@0.37.1
rand@0.9.1
redox_users@0.5.3
r-efi@5.3.0
r-efi@6.0.0
r-efi-alloc@2.1.0
rustix@1.1.5
unwinding@0.2.7
wasi@0.11.1+wasi-snapshot-preview1
wasip2@1.0.4+wasi-0.2.12
windows_aarch64_gnullvm@0.52.6
windows_aarch64_msvc@0.52.6
windows_i686_gnu@0.52.6
windows_i686_gnullvm@0.52.6
windows_i686_msvc@0.52.6
windows_x86_64_gnu@0.52.6
windows_x86_64_gnullvm@0.52.6
windows-sys@0.59.0
wit-bindgen@0.57.1
zerocopy-derive@0.8.59
```

This exact missing set is enforced by the pure selector. It is **not a claim
that the entire lock union is available**. These versions were inactive for
the retained successful target/profile/features in the examined old operations;
that fact does not justify another target or feature combination. The successor
must still obtain the exact unchanged297-unit graph under offline/locked
resolution. Any demand for an unavailable package fails closed; no online
fallback, unrecorded seed addition, or one-package retry is authorized.

### Pinned basis

| Basis | SHA-256 |
|---|---|
|prepare-03/CARGO-HOME.json|474c01d941c61e37e744bd0bdd74e2193c46cc3b3ff320fcef449230570f3ab4|
|aggregate-guest-build-01/project/software/v5/aggregate_guest/Cargo.lock|13381f3226dfb40e766fda448adaa4a75f407da0d31114964d1278991a6f1b7c|
|general-checker-guest-02/prepare-01/std-candidate/lib/rustlib/src/rust/library/Cargo.lock|207129d8edc2cb762f8556dce440012854d28ca2d8774852fb00ee0a32191fc5|
|aggregate-guest-build-01/commands/offline-aggregate-graph/stdout.txt|2cc441345c1cf3cc16e9dd21cca1bf2130319dbfa1124ad3ddb1d6507f2f4609|
|aggregate-guest-compile-01/SOURCE-MAP.json|75c710e3ee13f63cb6ef44da8656caa53c300bf649317d2b5669d8b9cde06ce0|

## Exact fresh source successor

Only two new files were implemented under
`software/v5/bounded_parse_guest/`:

| New file | Bytes | SHA-256 |
|---|---:|---|
|cache_resolver.py|7693|afb71f3f19acd90cf6b731e3fa62ff65f382d372e478b8dd75599a34d2565b83|
|build_resolver.py|27749|ad8182636c7b87a54bfcf41fbf66983a45f8aaf02f00c1010485d6d990651e8e|

The pure selector uses TOML parsing, enforces lock checksum consistency,
compiled160 subset, available180, exact20 additions including byte counts,
missing40,198 sparse entries and379total files. It has no filesystem,
subprocess or project-import behavior. It returns selected file pins and a
bounded explanation record. The controller separately runs frozen
`graph.canonical_graph` on the retained graph; it uses the new selector,
**not** frozen `graph.cache_inputs`, for cache construction.

The controller is a mechanically adapted successor of frozen build.py:
entrypoint/schema, exact source count, failure lineage and cache-selector call
change; supervision, command construction, graph comparison, artifact checks
and finalization are retained. It explicitly binds the predecessor FAIL,
command,stderr,selection,attempt and costs. It requires all inherited36 source
pins equal the failed selection (32Rust +3manifests +graph.py).

The source set is38 files, with39 in the fresh project snapshot after the
unchanged Cargo.lock is added:

- Unchanged32 Rust sources.
- Unchanged3 manifests.
- Unchanged graph.py.
- New cache_resolver.py and build_resolver.py.
- Cargo.lock is unchanged and added only to the snapshot.

The old build.py is not copied or imported. All five originally used files
remain byte-for-byte frozen; read-only rehash after successor creation confirms:

| Frozen file | Bytes | SHA-256 |
|---|---:|---|
|Cargo.toml|751|7eaa23cdc5aaf4c8fd1b8e1924a1cb4f702d7af8d04cdd06a33df23dfa5c0ad1|
|module/Cargo.toml|570|0435d18fdfb878290b291e62978643975fe2887c79873f50d6d4fa7332dba15c|
|checker/Cargo.toml|438|56364af430400d805de9be09d842b70e2f3bc3de9a14ff8082b18bcbcc1ff543|
|graph.py|8668|090744c1b479474399912c2180e8cca8e1e12afe050689f6c310af4c57136c87|
|build.py|24272|514b5f743ee7acef21c02719d98aa2b910e67a4966231527a1d4b83ac450f584|

## Prospective controller contract

This document is not a launch clearance. Root must select the final reviewed
source map and independent assurance must clear that exact selection.

Entrypoint:

```text
D:\Python314\python.exe -I -B -S <canonical-root>\software\v5\bounded_parse_guest\build_resolver.py <selection-path> <selection-sha256>
```

Selection schema: `DMKN_V5_BOUNDED_PARSE_RESOLVER_GUEST_BUILD_V1`.

The same six keys remain:
schema,name,sources,limits,native_comparison,
authorizes_guest_build_and_owned_telemetry_cleanup.
Name is now **exactly** `bounded-parse-guest-build-02`; its run directory
and attempt must both be absent. The sources map has exactly38 entries.
Native-comparison binding remains the exact8960B RESULT with digest
`ddd411125b809fda24be93280329f6d7b7bd3d4b32ac5cbd71beab46e4948a20`.

Result schema:
`DMKN_V5_BOUNDED_PARSE_RESOLVER_GUEST_BUILD_RESULT_V1`.

Successful status remains:
`PASS_BOUNDED_PARSE_EXACT_GRAPH_GUEST_BUILD_ONLY`.

Commands remain exactly:

1. offline-bounded-graph: same locked/offline target/profile/build-std command
   plus --unit-graph -Zunstable-options, then unchanged exact graph comparison.
2. build-bounded-guest: same base command plus -vv --message-format=json.

The artifact object retains user_elf,elf_headers,link_map. There is no change
to artifact interpretation, ELF location pattern or the graph-comparison
status. New RESULT fields are predecessor_failure and resolver_cache_selection.
A new CACHE-SELECTION.json records the same cache-selection explanation.
These schema changes must be recognized by the unused assembly adapter;
they do not authorize assembly or image execution.

### Unchanged finite limits and closure

| Resource | Limit |
|---|---:|
|Inclusive worker CPU, shared across both commands|480s|
|Shared worker phase wall|600s|
|Worker Job memory|4096MiB|
|Active Job processes|8|
|Ordinary controller CPU|70s|
|Total controller CPU including finalization reserve|90s|
|Total wall from same initial clock|780s|
|Fresh run output|3GiB /32768entries|
|Per-command combined logs|32MiB|

The native Job's CPU cap is user time; retained InclusiveJob.stats additionally
checks **kernel+user** at every existing phase poll and finalization. Final
stats remain obtainable for clean failure evidence even after a cap is exceeded.
No budget counter resets between graph/build or before finalization.

The private CARGO_HOME/target/TEMP/profile, exact selected input hashing before
and after, unchanged32Rust/source/native-comparison lineage,982SDK/2192std/
27compiler file maps,98host-tool/link pins, rustfmt/clang/link helpers,
Python/helper-chain pins, ancestor/private Cargo-config absence checks,
fresh-run-only census and prohibition of unexpected archives all remain.
No retained cache is changed. No broad SDK/history/runtime census is added.
The failure evidence increases the small read-only input map; it does not add
a second build or new executor.

Finalization still closes the Job, requires quiescence, rebinds all selected
inputs including copied project/cache and failure evidence, exclusively saves
RESULT/attempt, and emits an overriding FINALIZATION-FAILED marker on late
budget failure. No partial pass licenses proving.

The supported conclusion after a future successful reviewed run would be only
a newly compiled guest ELF with the selected graph. It would not establish
image success, semantic correspondence, cryptographic certification, improved
guest cost, deployability or full v5 completion.
