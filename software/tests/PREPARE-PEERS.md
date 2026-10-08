# Two-installation PREPARE coordinator

Prospective source, not an executed result. Root alone runs this after independent source and launch review. This coordinator prepares public contexts; it does not start services, author a theorem, submit source, acquire a peer result, publish, or finish the reciprocal experiment.

## Fixed invocation and launch record

```text
python -B -E -s -S software/tests/prepare_peers.py --launch ABS_LAUNCH_JSON
```

The launch contains exactly:

```text
{schema:1, coordinator:FilePin, python:FilePin, source_files:[FilePin,...],
 shared_runtime:{path:ABS_RUNTIME,lean:FilePin},
 ports:{alpha:43171,beta:43172},
 limits:{command_seconds:500,active_wall_seconds:1800,
         observed_cpu_seconds:1800,retained_bytes:1073741824}}
FilePin = {path:absolute_path,bytes:positive_integer,sha256:hex_digest}
```

`source_files` is sorted by product-relative POSIX path. Its exact set is current `py/*.py`, `API.md`, `manage.py`, `build.py`, `assets-lock.json`, and every regular file under `native/` and `assets/`. No tests, old state, runtime, precompiled support, `build/`, qualification output or experiment files are copied. The coordinator itself has its own exact pin and is snapshotted into the evidence directory. Root creates the launch only after all source authors have frozen their cuts. Launch paths and FilePin paths must be absolute; duplicate JSON keys and nonfinite numbers, including overflowing decimal exponents, refuse.

The roots are fixed relative to this script:

```text
software/qualification/peer-01/       new retained evidence
product-local/peer-01/
  alpha/install/                    copied raw product sources/assets
  alpha/build-work/                 new external support-build workspace
  alpha/state/                      independently configured/initialized state
  alpha/scratch/                    public-call supervision evidence
  beta/...                          second independent copy/state/build
```

Both top-level run roots must be absent; creation is exclusive. Existing siblings and failed attempts are never removed. Symlinks/reparse points, special files, duplicate/missing/extra source pins, changed source bytes and inappropriate path domains refuse. Ports are actually bound simultaneously once and then closed; this is a preflight check, not a guarantee/reservation of their future availability. No listening peer service is started.

## Exactly ten public commands

For each installation, in order: run its copied `build.py` once; run its copied `manage.py configure` once; then run `manage.py request` for `init`, `info`, and `find` once each. That is two support-build stage allocations, containing two source compilations each, and two mathematical bootstrap stage allocations. There are no retries, alternate ports, adaptive repairs or theorem-source inputs.

Configuration selects clients `local` and `reviewer`, zero offered theorem packages, and peer alias `other` with the other installation's frozen port. Every executable/support/asset config path must belong to the copied installation, except its explicitly shared external Lean executable. State and scratch are external sibling directories. Config creation is not acceptance. Initialization must return actual checked contexts for both local labels; local `info` must match the initial public description, and local `find` must report an empty P1 snapshot.

The mathematical source pipeline is not invoked. Public author packets contain only these actual initialized descriptions/handles, the empty enumeration, installed command/config locations, the installed `API.md` pin and evidence bindings. They include no chosen theorem, future source, statement interpretation or proof skeleton. A separate authoring/finish phase is not part of this coordinator.

## Shared runtime and evidence scope

Both installations use `software/runtime/lean-4.34.0-windows` as the same explicit external immutable Lean distribution. They do not copy it or consume experimental `.olean` output. Each installation builds its own support from its own copied sources. The launch checks the selected Lean executable before and after; it does not rehash every DLL/runtime library. The full shared runtime is a declared trust premise and its sharing is recorded in the result. This is not independent-host or independent-runtime deployment evidence. A later clean independent runtime/host remains necessary.

Both also use the same selected Python runtime distribution, with its executable pinned but not every standard-library module or dynamic library. These executable pins do not authenticate either full transitive runtime. Separate same-host directories/state are not an OS visibility boundary: the old checkout remains readable even though no configured product dependency points into it.

The coordinator preserves raw source copies, exact command arrays, stdout/stderr, public request bytes, config pins, build/public supervisor receipts, node events, public info/author packets, state seals and final bounded file inventories. It verifies public request/response hashes against the actual node supervisor and event records. Each direct command's initial `result.json` precedes deeper evidence inspection; the final prepare result adds later successful build/public bindings and their observed quiescence. Configure has no independent process-tree observation, and is labeled accordingly. Native command/stage evidence stays in each independently owned local build/state/scratch tree. No database is copied between nodes or directly promoted by the coordinator.

## Bounds and stop semantics

Each direct CLI command has a 500-second maximum, further reduced to the remaining 1,800-second active-wall grant. These are cooperative polling/checkpoint limits, not an outer operating-system resource container. Its redirected stdout/stderr are checked while running against 2 MiB/1 MiB ceilings. Existing build/native runners and public manage supervision provide their already declared inner child process-tree memory/CPU/time limits. The coordinator and its direct build/manage/configure wrappers have no additional OS CPU or memory containment. Root monitors/polls the trusted preparation launch and stops it at the declared wall limit if necessary; that monitoring does not establish full descendant cleanup or a hard total-resource quota. The coordinator is not a replacement process-tree sandbox.

Observed CPU is coordinator process CPU plus each unique build-stage Job and each unique public-node supervisor Job whose final receipts have been successfully bound. The node Job already includes its nested native work, so its bootstrap child Job is not counted again. Direct Python build/manage/configure wrapper CPU, and any Jobs lacking successfully bound final receipts on failure, are unmetered here and explicitly marked; `observed_cpu_seconds <= 1800` is not a claim about complete total CPU. Final reporting/serialization endpoints are stated. Before final records, combined retained evidence/data is limited to 1 GiB with a 16 MiB reporting margin; the final success check additionally includes exact serialized seal/result lengths. The shared external runtime is excluded. Streaming source-copy/file-hash work has count/depth/size bounds. No hard transient filesystem quota is claimed.

Any command failure, timeout, output limit, missing receipt or mismatch stops the whole prepare without retry. The coordinator reaps a direct timed-out process when possible; it does not infer descendant quiescence from that action. On such failure the result says descendant quiescence is unconfirmed and preserves the nested evidence for diagnosis. Completed build/public request work requires the actual retained Job records to report empty process trees. Pending native or request recovery is not attempted.

Success means `PREPARED_TWO_INSTALLATIONS_AWAITING_INDEPENDENT_AUDIT_AND_LOCAL_AUTHORING`, not network completion, successful reciprocal contribution or deployment readiness. Failure artifacts remain under the same exclusively created roots.
