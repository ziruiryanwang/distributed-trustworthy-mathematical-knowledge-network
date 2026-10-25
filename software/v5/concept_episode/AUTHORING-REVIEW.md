# Independent standard-project source review

2026-10-24. **GO for root's one bounded standard Lake build; source review only.**
No build, compiler, owner operation, network access or Git mutation was performed
by this reviewer. Root owns exact execution selection, archive creation and
adoption. This does not qualify new export identities or complete v5.

## Final selected files

The three final added files were read completely after the artifact-cache setting
was added. The two retained source files were hash-checked and their imports and
modern module headers inspected. Their contents are unchanged.

| File | SHA-256 |
|---|---|
| lakefile.toml | c54f0d8ef96b8ca2d6b45c43be612501eefbc19aca87e7472e2f213466f165f5 |
| lean-toolchain | 8733782dc070a99b312039cda424f601b80f3be6f6f512627da5ba25adc27632 |
| AUTHORING.md | 3df4ba42f3c088fe6307402d73a6c0763f7de44f6b24bf1f27d6e585e1c7223c |
| TheoryA.lean | d2391e4a1a69d1ce57274ed011cd16734457e8239d2831a8e6eddd3349cbd9d9 |
| TheoryB02.lean | d1397331c7b633fec21558189c2eaa45b76642c49d5ca3f359a01f6e623c5bb4 |

## Configuration and dependency closure

The declarative TOML defines package repair_concepts and library RepairConcepts,
with that library as the default target. Explicit roots are exactly TheoryA and
TheoryB02. The selected Lean 4.34 Lake source confirms omitted globs default to
one exact glob per root, with local imports recursively built; its TOML decoder
recomputes that default after decoding roots. Therefore no RepairConcepts.lean
umbrella file is required, and the preserved failed TheoryB.lean is not selected
by a wildcard or imported dependency.

TheoryA starts with `module`, `public import Init`, `public section`;
TheoryB02 uses the same modern structure and imports TheoryA. Their transitive
external mathematical imports are entirely provided by the compatible complete
Lean runtime. There are no requires entries, remote dependencies, custom scripts,
Lake hooks, external generated inputs or links to an old experiment. The five
selected files plus the approved complete runtime are the input closure for this
specific ordinary build; this does not assert closure for arbitrary future edits.

PackageConfig confirms enableArtifactCache=false explicitly disables the package's
local artifact-cache use instead of relying on a cache miss. A fresh five-file
snapshot and --no-cache additionally exclude local prior build outputs and build-
cache downloads. Invoke the actual selected runtime's lake.exe, not an elan shim,
and avoid unrelated Lean/Lake path overrides. The toolchain label alone is not a
retained runtime or a proof that one is installed.

Root and reviewer independently inspected the selected CLI: --offline affects
new/init, not build. The final guide and revised decision correctly omit that
flag and explain offline sufficiency through the empty external dependency set
and local complete runtime. Neither --no-cache nor this source audit is network
isolation or a hostile-source sandbox.

## Identity and evidence boundaries

The historical B-SETUP.json names corrected B as logical module TheoryB and
selects explicit old TheoryA artifacts. This standard project instead builds
logical TheoryB02. The guide explicitly preserves that distinction; equal source
bytes do not warrant equal private names, compiled artifacts or export identities.
The quoted historical receiver root matches ACCEPTANCE-AUDIT.md and is explicitly
not an acceptance token for the new build or another receiver.

The MyTheory example imports the actual public root and requires investigators to
add their own root deliberately. It imposes no global research task. Source/code
approval, native authoring, exact export correspondence and independent mathematical
admission remain separate. No historical-novelty, research-speedup, guaranteed
creativity, independent availability or public-release claim is made.

## Marginal value and stopping rule

One bounded Lake build is justified because standard module selection/import
setup is genuinely different from the experiment-specific B setup. It should
compile only the two retained roots and their supported runtime imports in the
fresh snapshot, with no retries or budget renewal. The selected maximum is
90 wall seconds / 60 CPU seconds / 1,024 MiB / eight processes. Root owns the
actual command, runtime pins and output location.

That build checks continuation infrastructure, not a new mathematical episode,
export/admission correspondence or growth speed. Once its output is audited and
the exact five Git blobs are archived/bound, stop this boundary. No repeated A/B
creation, export, intake, discovery or product build is needed for this change.
Archive entries must exclude failed TheoryB, private state, logs and .lake outputs;
full compatible runtime retention remains separate. Licensing and external
publication remain undecided and unperformed.

## Exact prospective selection review

Root's experiments/concept-lake-source-01-selection.json has SHA-256
2f40662c9575ef31c7f9bbb96d1c600bfc0839a6e1633acdc1a196d397506b02.
All six selected source pins (five project files plus the existing runner) and
12 named runtime pins independently match. The target output did not exist at
review. No Lean/Lake/elan-prefixed environment override was present in the
reviewing shell; immutable normal owner environment remains a premise.

The argv invokes the pinned real lake.exe with --no-cache, explicit -d pointing
inside the fresh source snapshot, and build RepairConcepts. The existing runner
accepts the pinned executable and selected snapshot argument, binds sources before
execution and verifies their continued equality afterward. The exact requested
90/60/1024/eight-process limits and finite logs are present. This uses no helper,
new harness, old .lake tree or product binary. The 12 file pins are explicitly
partial, not a hermetic toolchain proof.

**GO for this selection once, without renewal or retries.** This remains a
pre-execution review; a clean terminal result and output audit are still required.

## Actual standard-project build audit

Root executed concept-lake-source-01 once. **PASS for the selected ordinary Lake
build.** This reviewer inspected saved results, traces and hashes without rerun.
All six snapshot source pins (the five project files plus runner) and 12 named
runtime pins match the selected values. The five project inputs remain unchanged.
Generated files occur only in the fresh snapshot, not the canonical source tree.

Stdout explicitly reports Built TheoryA (721 ms), Built TheoryB02 (630 ms), and
successful completion of four jobs. Stderr is **119 bytes, not empty**: exactly
the ordinary informational messages that no previous manifest existed, a fresh
one was created, and the toolchain was already up to date. No compile error or
warning appears in those logs. The resulting lake-manifest.json has an empty
packages array and names repair_concepts.

Actual generated setup/trace files confirm package repair_concepts, modern
isModule=true and logical names TheoryA and TheoryB02. A's local import-artifact
map is empty; B02's only explicit map is TheoryA's newly built public/server/IR
companions inside this same snapshot. Both setups have empty plugins and dynlibs.
The traces select the current runtime and local snapshot source/output paths;
no old experiment artifact path appears. The expected complete local Init
toolchain remains an external premise, not a freshly rebuilt or fully pinned
dependency tree.

The snapshot project contains its five inputs, the generated manifest and 32
Lake build files (38 files total). Only TheoryA and TheoryB02 have generated
module outputs: .olean, .olean.server, .olean.private, .ir, .ir.sig and .ilean,
plus normal hashes/traces/generated C/setup files. Failed TheoryB.lean and a
TheoryB.olean output are absent. This confirms the standard roots rather than
silently reusing historical B-SETUP's logical module identity.

The outer command exited zero, child reaped, Job closed, zero active processes,
four total processes and no cleanup errors or termination request. Job CPU is
1.65625 seconds, runner CPU separately 0.40625 seconds; peak Job private commit
510,668,800 bytes. Wall through cleanup is 2.4435187001 seconds and runner total
wall 2.6274778000 seconds, within the original 90/60/1024/eight-process limits.
No allocation renewal or retry occurred. This is not a research speedup result.

Evidence is under experiments/v5-local-checks/concept-lake-source-01:

| Evidence | SHA-256 |
|---|---|
| selection.json | 2f40662c9575ef31c7f9bbb96d1c600bfc0839a6e1633acdc1a196d397506b02 |
| RESULT.json | c29fc5b7ca2a042be04c0dd9d20a062a7b0264882a511477269c69084f427ae5 |
| project lake-manifest.json | 4828793e221be80a91df94e235ac49901ddb5fa5af2dfe1b97ca919513ec0c7f |
| generated TheoryA.olean | 345a87d1b82d41221960ce4e40a48c36c2bc856eb9dbb6c5df731f0dcb2342fd |
| generated TheoryB02.olean | 61e368f3c6efd5eb98d02a29ddd4cb306ff400b2bd5b4c9e01a065c399e60084 |
| generated TheoryA.setup.json | c5dbc8f067e422cfe62d9fabb9c7521a85c6ac5cbd51ab02b3a5b49572a824ae |
| generated TheoryB02.setup.json | 948fa4c3d8ebfc5e1a4755df54f207557687af734f6457aa740d9941dc98b499 |

Here project means sources/software/v5/concept_episode; generated setup files
are under .lake/build/ir and module artifacts under .lake/build/lib/lean.
This establishes standard-project buildability and source-based continuation
infrastructure, not new commons export identity/correspondence, admission,
creative novelty or independent availability. Exact five-file Git archive
binding remains root's separately selected next boundary; no recompilation is
needed to audit those bytes.

## Exact Git archive audit

Root created the ordinary Git archive after source commit
d41e746b21d1fd074d4bb3bdb5211075f8eb19ff. **PASS for exact five-file source handoff
binding.** This reviewer read the ZIP entries in memory without extraction or
execution and used read-only Git tree inspection; no Git mutation occurred.

Archive: product-local/concept-authoring-source-01/repair-concepts-source.zip,
7,806 bytes, SHA-256
35de621253de0cd3ac4eeeafabd0f4a44477e50d78fc4227f4c85d8426729b3f.
The ZIP has exactly five unique file entries under repair-concepts/ plus one
empty directory entry. The names are precisely the five selected source files;
no failed TheoryB, build output, database, secret or extra path is present.

For each uncompressed entry, SHA-256 matches the successfully built source
snapshot and the selected source pin above. Its independently computed Git blob
identity (SHA-1 over the standard blob header and raw entry bytes) matches the
100644 regular-file entry in that exact committed subtree:

| File | Bytes | Committed Git blob |
|---|---:|---|
| AUTHORING.md | 5,620 | 17b6efed38d7e06c2e3a075bfc03d2b30b416b23 |
| TheoryA.lean | 5,724 | c9f7fba2115dfae99bb164bcfe4414b8729b1084 |
| TheoryB02.lean | 7,401 | bfffd1d54bc5f423a6520ea70f548cb32d9f0dcd |
| lakefile.toml | 160 | 2da2ba4d45a65027515058975ad0e32e746e222a |
| lean-toolchain | 25 | 12359f928f18e4a89ebd1444a0310b025931b17d |

The executed build used the runner's fresh source snapshot, **not a ZIP
extraction**. Entry-byte equality binds the archive payload to those built inputs;
it does not constitute an extraction test. No recompile is needed for this
binding audit. The archive remains local, unlicensed for public release pending
the user's decision, and dependent on separately retained compatible runtime.
No new mathematical acceptance identity, novelty, speedup, source hosting or
independent availability follows. The selected build-and-archive boundary is
complete; do not repeat prior episodes or builds for another pass.
