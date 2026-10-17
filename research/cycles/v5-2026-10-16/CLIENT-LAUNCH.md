# Ordinary finite client launcher

2026-10-16. Root selected only `software/v5/client/launch.py` and `boot.py` for
source implementation; the facade author owns `workspace.py` and `API.md`.
No runtime, test, proof generation, deployment or Git mutation is authorized by
this checkpoint. The fixed release manifest remains
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.

## Reuse the existing containment boundary

The launcher imports the exact manifest-pinned `operator/commons.py`, `domains.py`
and `run_stage.py` bytes, then calls the existing `commons.supervise` with the
existing `run_stage.Job`. That supervisor creates the child suspended, assigns it
to its bounded Windows Job and only then resumes it. All client source census,
snapshot creation, package imports, workspace/owner setup and strategy execution
occur in the child after that point. No second supervision engine is introduced.

There is an unavoidable small trusted outer bootstrap: interpreter startup,
bounded plan/manifest reads, supervisor source adoption, creation of the fresh
run directory and the call that creates the Job. Root explicitly accepts this
trusted-wrapper boundary. Wall time starts at the first launcher clock sample;
bootstrap CPU is capped and reported separately from child Job CPU. Interpreter
startup before that sample is unmeasured, not zero. The wrapper is not claimed
to have been inside the child's Job. Supervisor cleanup and uncertain-closure
semantics remain unchanged; failures never become successful client operations.

The child is the fixed adopted embedded Python with `-I -S -B`; no arbitrary
executable, shell, interpreter flag, environment overlay, remote manifest or
remote command is accepted. The owner strategy is a pinned **trusted local Python
script** with `main(context)`, not peer-provided executable knowledge. A zero exit
or launcher report grants no mathematical authority.

## One owner plan, one fresh run

The exact, externally hash-bound owner plan contains fixed fields:

- Schema and a simple run name.
- Canonical installation and workspace roots.
- Canonical original source roots `v5`, `portable`, and `owner`.
- Exact relative source-file size/SHA-256 map, including both launcher files,
  the 21-file portable `location` closure and the owner script.
- One relative owner entry and bounded JSON parameters.
- The existing supervisor's six finite limits and finite final output-census
  limits. Snapshot file/byte ceilings are independent fixed implementation caps.

All launcher-created outputs are fresh descendants of `workspace/name`:

```text
workspace/name/
  command/          existing supervisor reports/stdout/stderr
  sources/
    portable/location/...
    v5/...
    owner/...
  work/             owner/client/location operation outputs
  BOOT-RESULT.json  nonauthoritative source/origin/lifecycle report
  RESULT.json       nonauthoritative outer closure report
```

`sources` and `work` are disjoint siblings. Location adopts the mathematical
workspace below `work`, never the
whole run or whole allocation workspace, for the fresh-operation configuration.
Root also selected the persistent configuration below. Neither weakens
source/runtime/workspace disjointness. Original source roots and installation
must not overlap the fresh run.

### Two supported owner layouts

The boot context's `workspace_root` is the **allocation parent**, not automatically
the mathematical `Workspace.root`. `location_workspace` is a fresh default, not
a mandatory persistent location. Root explicitly selected these two uses:

```text
Fresh local operation:
  mathematical Workspace.root = context.location_workspace / "commons"
  location adoption.workspace = mathematical Workspace.root

Persistent mathematical commons:
  mathematical Workspace.root = context.workspace_root / "commons"
  location adoption.workspace = mathematical Workspace.root
```

The persistent path must be disjoint from `context.run`, all source roots and
installation, and is explicitly selected in trusted owner strategy parameters.
It is a sibling of each fresh run, never their parent. In both modes, reserve
`grant = workspace.reserve(limits, outer_deadline=context.deadline)` before
constructing mathematical owners; put their outputs plus location state/evidence
under the fresh `grant.directory`. Each location service remains create-only.
Persistence belongs to the mathematical store/ledger, not a false claim that
the existing location node can resume its old state.

Parent/boot output census covers only the fresh run. Persistent custody,
indexes and grant outputs are bounded by the Workspace's store quotas and
per-grant census, **not** falsely counted in the launch run census or in a hard
disk quota. No whole persistent-workspace scan is added to each operation.
Trusted owner code remains responsible for selecting these disjoint scopes;
this is not filesystem isolation against that owner code.

## Exact loading and original time

The outer bootstrap verifies only the small fixed bootstrap closure. The child
verifies the complete selected embedded-Python file census and hashes, checks all
source pins, writes a fresh bounded source snapshot and verifies it. Source maps
cannot contain `.pyc`/`.pyo` or native Python-extension payloads. The child refuses
preloaded selected package names; `location` has the explicit regular-package
initializer. Its initial selected import order is portable overlay, then retained
v5 source snapshot, then the already checked standard-library paths.

A narrow import-origin guard compiles selected Python source bytes directly and
refuses unselected filesystem origins. This prevents bytecode-cache or omitted
package fallback; it is not a sandbox against the trusted owner strategy. The
actual imported `__file__` origins, sources and selected runtime are rechecked at
finalization. Helpers dynamically adopted by mathematical owners remain governed
by their own exact pin checks and do not gain authority from this loader.

`context.started` and `context.deadline` derive from the original outer monotonic
clock samples passed unchanged to boot. No new wall allowance begins after
snapshot or owner setup. Owner code must construct subordinate grants with that
same upper deadline (or a smaller remaining integer allowance). The outer Job
and supervisor still bound all descendants even when a local API has a shorter
deadline. Construction of mathematical owners occurs only in `main(context)`.

## Important limits

- Hard Job containment is resource containment, not hostile-code isolation.
- Output entry/byte census is bounded final evidence, not a filesystem disk
  quota. Existing stdout/stderr limits are sampled by the unchanged supervisor;
  owner/client output quotas retain their own enforcement. Oversized final
  outputs fail rather than being silently called successful.
- OS libraries, trusted owner filesystem and bootstrap interpreter startup are
  not claimed hermetic or cryptographically attested by this wrapper.
- This launcher does not choose a research goal, provider, theorem, proof budget,
  certificate policy, or automatic retry. Those are explicit local strategy.
- The unchanged mathematical owners remain the only source of live acceptance
  handles. No saved success JSON is an acceptance credential.

Review and root-selected changed-boundary controls must precede use. The source
map must cover the actual client import closure, not a guessed subset; old proof
campaigns are neither needed nor renewed by this launcher.

## Source implementation checkpoint

The two selected files are implemented. This author did not execute, import,
compile or test them. Independent source reviewer `v5_growth_decision` inspected
the inherited supervisor and identified one concrete namespace coupling: loading
`domains` in boot would conflict with the actual ReceiptVerifier's tagged module
loader. Boot now loads only the exact supervisor; the mathematical owner loads
its own exact `domains`/Job modules normally. The outer launcher may load them
in its separate interpreter. No source/class gate is weakened.

The ordinary owner entry is synchronous `main(context)` and must return integer
zero explicitly; it may call `asyncio.run` itself. A registered private module
supports ordinary dataclass/function definitions in that pinned strategy source.
The launcher copies the exact owner plan to fresh `run/plan.json` before dispatch;
boot checks that origin and unchanged hash. Source copy and all client setup stay
inside the already attached child Job.

Parent success requires actual zero-exit/closed supervisor outcome, a matching
boot-completion record, and absence of a boot-failure marker. Thus an accidental
`sys.exit(0)` before boot finalization cannot silently pass. The raw supervisor
record is preserved separately from wrapper-binding failures. Final parent
census checks the quiescent run, then checks again after writing `RESULT.json`;
an overrun creates `FINALIZATION-FAILED.json` and returns failure.

The fixed manifest's selected embedded-Python subtree has 584 files totaling
30,459,330 bytes (largest file 6,778,592 bytes), read from manifest metadata only.
The child validates exact actual census and each pin under finite tree bounds;
this metadata inspection was not a runtime test or performance measurement.

Stable initial review targets:

| Payload | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/client/launch.py` | 13,578 | `523a3031da86457037af3c41f87425cd406e5fe3fcf6a2edb2d87eff9b59ef78` |
| `software/v5/client/boot.py` | 12,565 | `76cdcd42379d61c5fe37dc86a23363687c084c56887302dcdd922aa9b089ce2b` |

Exact whole-client source closure, coupled facade tests and actual contained
execution still require root selection. No preexisting campaign was repeated.

## Exact ordinary invocation and plan

Once the source selection is reviewed and executed successfully, the ordinary
invocation shape is:

```text
<installation>/receiver/runtime/python/python.exe -I -S -B <v5-source-root>/client/launch.py <absolute-owner-plan.json> <plan-SHA256>
```

All paths in the owner plan are absolute ordinary canonical local Windows paths.
The working directory does not select an installation or code root. The exact
plan schema is:

```text
{
  "schema": "DMKN_V5_CLIENT_LAUNCH_V1",
  "name": "a-new-owner-run",
  "installation_root": "<fixed-release installation>",
  "workspace_root": "<allocation parent>",
  "source_roots": {
    "v5": "<retained v5 root containing client/launch.py and boot.py>",
    "portable": "<portable_runtime root containing location/>",
    "owner": "<trusted local strategy source root>"
  },
  "sources": {
    "v5/client/launch.py": {"bytes": "<integer>", "sha256": "<exact digest>"},
    "v5/client/boot.py": {"bytes": "<integer>", "sha256": "<exact digest>"},
    "v5/client/workspace.py": {"bytes": "<integer>", "sha256": "<exact digest>"},
    "owner/strategy.py": {"bytes": "<integer>", "sha256": "<exact digest>"},
    "<every other selected dependency and all 21 portable/location files>": "<exact pin>"
  },
  "owner_entry": "strategy.py",
  "parameters": {},
  "limits": {
    "cpu_seconds": "<integer, 1..86400>",
    "wall_seconds": "<integer, 1..3600>",
    "memory_mib": "<integer, 1..4096>",
    "active_processes": "<integer, 1..8>",
    "stdout_bytes": "<integer, 1..8388608>",
    "stderr_bytes": "<integer, 1..8388608>"
  },
  "output_limits": {
    "bytes": "<integer, 67108864..2147483648>",
    "entries": "<integer, 1024..32768>"
  }
}
```

This is a field-shape illustration, not executable example JSON: replace marked
integer/digest/path slots and supply the complete exact dependency map. Source
limits are 512 files, 2 MiB per file and 64 MiB total. Relative paths have at most
32 components and cannot encode aliases, traversal or case-fold collisions.
`v5/location` and `v5/portable_runtime` copies are refused; only the single
`portable/location` package supplies canonical location classes. No bytecode or
native Python extension may appear in the source snapshot. Installed standard
library extensions remain governed by the fixed runtime manifest.

The strategy script is a single selected entry executed as a registered private
module and may import selected SDK packages and the fixed standard library.
The original owner source directory is **not** added to Python's search path.
Additional strategy helpers must be deliberately integrated into the selected
source closure; arbitrary local-directory fallback is not supported.

`context` exposes immutable fields `installation`, `workspace_root`, `run`,
`location_workspace`, `sources_v5`, `sources_portable`, `sources_owner`,
`started`, `deadline`, `limits`, `parameters`, and `source_sha256`, plus
`remaining_seconds()`. Map fields are read-only top-level views. Source pins can
be extracted into ordinary dictionaries when the existing exact-type owner
constructors require them. They are adoption inputs, never remote authority.
