# Bounded ordinary Lean investigator distribution

This is a **source-only distribution successor**, not a completed v5 release or
an executed build. It preserves the native-first authoring/checking workflow, unfamiliar-symbol
inspection and advisory authoring-project lookup. This successor adds an explicit
receive dependency policy and a supported whole-operation resource launcher.
The mathematical checker, native compilation lanes and acceptance policy are
unchanged. No new theory generator, hosted source repository or growth guarantee
is added. Runtime evidence and adoption remain separate from this source recipe.

## Build from a source checkout

Supported profile: Windows x86-64, complete Python 3.14.6 and Lean 4.34.0 runtime
distributions, including Lean's native compiler tools. Supply explicit runtime
roots, an existing output parent and a fresh output directory:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_bounded_operations\build.py' `
  --source-root 'C:\commons-source' `
  --python-runtime 'C:\tools\Python314' `
  --lean-runtime 'C:\tools\lean-4.34.0-windows' `
  --output 'C:\commons-builds\bounded-investigator-01' `
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

Use packaged `run.py` with the approved Python `-I -S -B` to launch the fixed
`owner`, `peer` or `query` entrypoint inside a finite whole-operation Windows Job.
[LAUNCHER.md](LAUNCHER.md) gives exact flags, path requirements, resource claims
and interrupted-operation handling. Direct scripts remain available only when
the caller supplies an equivalent external envelope; their memory option alone
does not constrain the Python controller. A configuration hash selects bytes,
not a trusted provider or the truth of peer claims.

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

A receive configuration now also requires an explicit `dependency_policy`.
`selected-unit-only` checks the selected unit against the chosen grounded parent
and returns `NEED_GROUNDED_PREMISES` if prerequisites are missing, without fetching
ancestor locators or proofs. `bounded-closure` explicitly permits the former
bounded acquisition behavior. Missing/invalid policy refuses before network I/O.
See [RECEIVE-POLICY.md](RECEIVE-POLICY.md). This is an intentional local-config
change; existing receive configurations must select a policy.

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

Inspection does not require downloading all ancestral proofs. Strict receive can refuse missing prerequisites before ancestor retrieval, but
does not make cold acceptance cheap. Explicit bounded-closure receive or cold
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

The public launcher supplies OS Job process/private-memory controls and sampled
wall/aggregate-CPU/log checks. It does not impose filesystem/network privilege
isolation or a hard disk quota. Native limits and `loadExts := false` are likewise
not a hostile-project sandbox.
Checking final mathematics cannot undo harmful code execution or protect a
checker already tampered with. Source offers confer no execution permission.
No source hosting, license, release authentication, global availability or
worldwide deployment qualification is implied by this source consolidation.

## Exact successor and source-only checkpoint

The clean-source recipe derives from the frozen ordinary_research_distribution.
Only peer_api.py, profile.py and this README replace existing final roles;
run.py, LAUNCHER.md and RECEIVE-POLICY.md are added. The base builder's 47 inputs,
all native source lanes, transforms, runtime pins, installed checker and
mathematical acceptance rules remain unchanged. There is no state migration.

The source map has 84 source inputs plus its builder and map, 64 direct copies,
and 145 payloads plus PROFILE: 28 installation payloads, 113 profiled auxiliary
roles and four documents. Native output identity follows the actual build;
equal sources do not guarantee byte-identical linker timestamps.

This document describes a source recipe. Current execution/adoption evidence
belongs to the separate review checkpoint. A source build is not mathematical
acceptance, independent security review or a completed worldwide v5 release.
Neither change establishes research acceleration. Approved ordinary Lean
projects and independent investigators remain the route for developing new
concepts, models, theories and checked connections.
