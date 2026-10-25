# Ordinary Lean investigator distribution

This is a **source-only distribution successor**, not a completed v5 release or
an executed build. It consolidates the native-first authoring/checking package
with exact unfamiliar-symbol inspection and advisory authoring-project lookup.
The mathematical checker, native compilation lanes and acceptance policy are
unchanged. No new theory generator, hosted source repository or growth guarantee
is added. Runtime evidence and adoption remain separate from this source recipe.

## Build from a source checkout

Supported profile: Windows x86-64, complete Python 3.14.6 and Lean 4.34.0 runtime
distributions, including Lean's native compiler tools. Supply explicit runtime
roots, an existing output parent and a fresh output directory:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_research_distribution\build.py' `
  --source-root 'C:\commons-source' `
  --python-runtime 'C:\tools\Python314' `
  --lean-runtime 'C:\tools\lean-4.34.0-windows' `
  --output 'C:\commons-builds\investigator-01' `
  --wall-seconds 600 --cpu-seconds 600 --memory-mib 2048
```

These are example finite allowances, not measured requirements or a success
promise. Valid bounds remain 120-3600 wall seconds, 100-3600 aggregate CPU
seconds and 256-8192 MiB. There is no download, automatic retry, renewal or
historical binary input. The caller must approve the builder, checkout and
runtimes; exact hashes identify selected bytes, not their author or safety.

Successful output would contain `package/` and `_build/`. Only `package/` plus
the selected external runtimes are needed for operation. Build inputs, logs,
source maps and generated outputs remain under `_build/` for diagnosis. Its
`BUILD-RESULT.json` reports actual package/profile and native installation
identities; `PROFILE.json` commits last. Failure preserves partial output.

## Public commands and deliberate choices

Run packaged `owner.py`, `peer.py` and `query.py` with Python `-I -S -B`.
The command help lists exact flags. Every operation has explicit package/runtime
selection, fresh output and finite resource limits. A configuration hash binds
the selected configuration, not every dependency or the truth of peer claims.

| Entry | Operations used by an ordinary investigator | Boundary |
|---|---|---|
| `peer.py` | `find`, `preview`, `inspect`, `authoring-offers` | State-free, inert information; reject catalog/custody/store arguments |
| `owner.py` | `produce-baseline` | Explicitly approved compiled local project; no owner state; output is not accepted mathematics |
| `owner.py` | `init`, `status`, `intake-baseline` | Receiver-selected owner policy and independent checking |
| `peer.py` | `receive`, `publish`, `serve` | Selected owner/custody/index context; actual receive checks, publication indexes, serve exposes custody |
| `owner.py` | `contribute`, `extract-std`, `extract-project`, `complete`, `export-module` | Existing narrower checked application/return/materialization routes |

Ordinary Lean projects remain the default rich authoring environment. Selecting
ideas, approving project execution and deciding which results to publish are
investigator decisions. There is no mandatory global research agenda, human-
intention acceptance field, new model service or automatic source execution.

## One complete investigator workflow

The following crosswalk identifies every new input's source. It does not assert
that a suitable project or willing provider always exists.

1. **Select contacts and a query.** An operator supplies reachable contacts and
   their TLS policy; `find` cannot discover an initial trusted contact from nothing.
   A local investigator chooses known-symbol or other supported formal features
   and a bounded search scope. A known symbol can come from an earlier exact
   preview/locally known binding. `query.py` additionally supports its existing
   owner-context query construction. Ordinary package/search tools remain useful.
2. **Select an actual result.** `find` reports `matches` with provider,
   snapshot identity and record. Pass that actual selection to `preview`; do not
   substitute a guessed theorem or assume the provider searched all mathematics.
   Preview binds the declared type and its symbol identities, not its truth.
3. **Inspect unfamiliar laws.** Select `(name, export_id)` from an actual preview
   binding and the provider to query. `inspect` obtains the exact locator and one
   inert declaration unit. It does not traverse dependencies, run native code,
   accept the declaration or install an ordinary Lean interface.
4. **Find an ordinary project, if wanted.** Pass a selected exact export identity
   to `authoring-offers`. A response can suggest repository, full Git commit,
   project directory, module, declaration and toolchain. All are unverified
   claims. Empty/unsupported/truncated is not global absence. Choose a hint or
   an independently obtained project under local retrieval/execution policy.
   The command itself never downloads, checks out, builds or approves anything.
5. **Establish any required exact correspondence.** After independently obtaining
   and explicitly approving a compatible compiled project, use `produce-baseline`
   on the selected structured declaration names. See packaged `PRODUCER.md` for
   project-selection schema, explicit approval and spool bounds. Compare the
   validated bundle's semantic/name/unit/export identities with the selected
   target. The manifest, exact unit files and target rows are public outputs;
   neither a repository name nor a success string supplies this comparison.
   A mismatch means correspondence is unresolved/different, not that the two
   mathematical statements are necessarily inequivalent.
6. **Investigate locally.** Use ordinary Lean definitions, structures, models,
   countermodels and proofs to develop a new concept, extension or bridge.
   Source/execution approval and output validity remain separate. The investigator
   need not complete an inert round trip before every exploratory proof. Drafts
   and unsuccessful hypotheses remain drafts, not accepted global premises.
7. **Return independently checkable work.** Select completed definitions and
   useful connections as well as endpoints. Produce an inert bundle or reuse an
   existing exact bundle. A receiver initializes/selects its own approved state
   and uses `intake-baseline` above its explicit parent root, with exact bundle
   path, manifest and manifest hash. Its actual admission establishes the checked
   closure; producer compilation/export alone does not. Existing native receive
   or contribution/completion routes remain alternatives when supported.
8. **Make the result discoverable.** `publish` uses the actual accepted context
   root and exact `{name, export_id, unit_id}` target rows, validating their local
   binding. The operator selects an index and finite read/storage limits. Targets
   commit separately; preserve partial success. `serve` exposes an existing index
   and all addressable objects in the selected custody under exclusive access,
   explicit disclosure approval, finite lease and TLS requirements. It is not a
   per-target ACL. A provider can optionally supply a separately pinned authoring
   offer map; this does not endorse the linked source or prove availability.

For an ordinary peer client the common flags are `--profile-sha256`,
`--python-runtime`, `--lean-runtime`, `--config`, `--config-sha256`, `--output`,
`--wall-seconds`, `--cpu-seconds`, `--memory-mib`. Stateful peer operations
add the documented `--catalog`, `--custody`, `--store-id`, `--custody-limits`.
Do not add those to the four state-free commands. Configuration field contracts
are enforced by packaged `peer_api.py`; no private-state edits are required.

An authoring-offer query config has exactly `contacts`, `selection`, `limits`:
selection is `{provider, export_id}` and limits are `{requests:1,
reply_bytes:32768, max_offers:8}` or smaller permitted bounds. Contacts use the
existing `{host,port,tls,server_name,ca_file,ca_sha256}` schema. Ordinary names
use the existing structured Lean-name encoding, not guessed dotted strings.
An operator enables optional offers through serve's `authoring_offers` field:
`{path,sha256}` naming a selected immutable canonical map. Omitted/null means
unsupported. The map is bounded to 2 MiB/2048 exact keys/eight offers per key;
the packaged codec defines its precise schema. It is parsed once, not watched.

## Costs, assurance and compatibility

Inspection does not require downloading all ancestral proofs. Independent cold
intake can still require a selected dependency closure; optional generated modules
have narrower realization limits and do not restore all notation, instances,
tactics or other frontend metadata. Ordinary approved project reuse preserves
that frontend but requires its own execution approval. No route is silently
treated as satisfying the stronger properties of another.

Changing a definition or theorem can change its exact identity. No popularity
vote merges meanings; explicit checked bridges can relate different theories.
Discovery is bounded/incomplete. Known-symbol features expose explicit formal
connections, not all analogies or unseen future ideas. Concept development by
independent agents is supported, not guaranteed useful, novel or accelerated.

Native process limits and `loadExts := false` are not a hostile-project sandbox.
Checking final mathematics cannot undo harmful code execution or protect a
checker already tampered with. Source offers confer no execution permission.
No source hosting, license, release authentication, global availability or
worldwide deployment qualification is implied by this source consolidation.

## Exact successor and source-only checkpoint

This recipe derives from `ordinary_native_distribution/build.py` and its exact
source map. Five final Python roles select `ordinary_authoring_offers` sources:
`peer.py`, `peer_api.py`, `profile.py`, `support/transport/http_provider.py` and
`support/transport/ordinary_acquisition.py`. It adds only
`support/transport/authoring_offers.py`. The packaged README becomes this document;
the existing `PRODUCER.md` source is preserved. No product implementation is copied
from an experiment directory or modified by this recipe.

The base builder's 47 inputs remain exact, including its old transport source
inputs even though final transport copies select successors. Thus 78 source/assets
become **81**, plus this builder and its map; 60 direct copies become **61**.
The output contains **142 payloads** plus PROFILE: 28 installation payloads,
112 profiled auxiliary roles and two documents. Relative to the native baseline,
135 payload roles retain their selected sources, six select replacements including
README, and one is new. New native build bytes are not promised byte-identical.

The receiver's eight modules, thirteen authoring modules/five companions, query
module, seven-module extractor lane/two separately linked executables, all native
transforms, runtime pins, base builder pin, sequential scheduling and decreasing
allowance accounting are unchanged. Changes in `build.py` are its description,
source prefix/map pin and exact census constants only. The fresh map is uniformly
formatted JSON; native/base sections retain identical parsed values. Sources and
used predecessor evidence remain untouched.

No compilation, build, test, service, native operation, owner open or Git mutation
was run by this author. Independent source review and root's exact selection are
required before execution. Old accepted state and module anchors are not migrated;
newly built support may have different identities. This closes a source-selection
gap, not the entire v5 goal or empirical/theoretical claims about research growth.
