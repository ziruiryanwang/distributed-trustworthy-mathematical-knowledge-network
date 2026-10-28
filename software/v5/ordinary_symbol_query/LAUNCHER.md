# Bound the entire ordinary operation

`run.py` is the Windows public launcher for one selected package's `owner.py`,
`peer.py` or `query.py`. It puts the Python controller **and its descendants**
inside the already shipped Windows Job supervisor. Direct entrypoints remain
usable when the caller supplies an equivalent outer envelope.

The launcher does not decide mathematical truth. It fixes a practical cost gap:
an entrypoint's `--memory-mib` alone bounds its native workers, not the Python
controller reading inert remote data. The new outer Job includes that controller.

## Invocation

Use the approved runtime and the package's externally approved `PROFILE.json`
SHA-256. Do not substitute an unreviewed package merely because its hashes agree.
For example, adapting these absolute paths to your installation:

```powershell
& 'C:\dmkn-runtime\python\python.exe' -I -S -B 'C:\dmkn\package\run.py' `
  --profile-sha256 APPROVED_PROFILE_SHA256 `
  --python-runtime 'C:\dmkn-runtime\python' `
  --lean-runtime 'C:\dmkn-runtime\lean' `
  --diagnostics 'C:\dmkn-work\find-envelope-01' `
  --wall-seconds 90 --cpu-seconds 60 --memory-mib 1024 `
  --active-processes 6 --stdout-bytes 1048576 --stderr-bytes 1048576 `
  peer -- find --config 'C:\dmkn-input\find.json' `
  --config-sha256 APPROVED_CONFIG_SHA256 --output 'C:\dmkn-work\find-output-01'
```

All launcher flags go before `owner`, `peer` or `query`. After `--`, use the
existing entrypoint's operation-specific arguments, with full option names and
separate option/value tokens. Query has no positional operation. Do not repeat
profile, runtime or allocation flags: the launcher supplies them. Duplicate,
abbreviated, `--name=value`, arbitrary-executable and shell dispatch are refused.
Owner-approved project execution still requires the entrypoint's existing local
approval; this launcher supplies no source approval by itself.

Every cap is explicit. Wall time is 35..3600 seconds; CPU is 4..200000 seconds
(at most 600 for query); private commit is 1..8192 MiB; simultaneous Job processes
are 1..8; stdout and stderr are each 1..8388608 bytes. These are ceilings, not
recommended budgets or promises that a command will fit. Include the controller,
native workers and their supervisors when choosing process/memory limits.

The child receives the same wall/CPU/memory ceiling, but its cooperative budget
does not renew the outer allocation. Outer elapsed wall time starts at launcher
startup, including bootstrap, and is forwarded to unchanged supervision. There
is exactly one child invocation and no fallback, retry or service lease renewal.
For `serve`, the existing finite service configuration remains required; the
outer budget must leave room for its normal cleanup.

## Files and trust boundary

The diagnostic directory must be fresh, with an existing ordinary parent, and
disjoint from the package, both runtime directories, owner catalog/custody/index,
operation output and selected input files/directories. Publish/serve's index path
is obtained from the hash-bound local operation config before any diagnostic
write; that owner config is not remote mathematical evidence. Package and runtimes must
also be pairwise disjoint. Paths must be absolute local-drive paths, without
links, reparse redirects or shared file hardlinks. Entry-specific path and input
validation still runs inside the bounded child. This preflight covers direct CLI
paths plus the selected index, not recursive inspection of project selections.
The child retains its existing checks on project roots and nested local inputs;
approved project code is executable local support, not sandboxed code. The launcher does not open
owner state, inspect remote evidence or acquire locks on the owner's behalf.

Before importing any package module, the launcher checks the selected profile,
the launcher/entry/base-loader bytes, the installation manifest, the selected
Python executable and its two pinned DLLs, and all three supervisor modules.
Only then does it import those exact supervisor source bytes. The child performs
the existing full package/installation verification before processing its inputs.
The currently executing launcher, Python/OS integrity and stable owner-controlled
files remain trust premises; these checks are not self-authentication or a
hermetic attestation of every Python standard-library/runtime file.

The preserved supervisor originally constructed a historical `receiver/` PATH.
For this invocation only, the launcher retains its environment sanitization and
replaces that PATH with the explicit selected Python root, Python `DLLs`, and
Lean `bin` directories. It launches Python and the chosen script by absolute path.
The existing native workers retain their own explicit selected runtime setup.
No supervisor source, Job logic, mathematical policy or state format changes.

## Reading the outcome

The fresh diagnostic directory retains `LAUNCH.json`, `SUPERVISION.json`,
`RUN.json`, and `child/command.json`, `child/stdout.txt`, `child/stderr.txt`.
The operation's separate `--output` directory remains the entrypoint's own.

- Launcher exit zero means the chosen CLI exited zero and its child tree was
  observed closed under the supervisor's checks. It is **not** mathematical
  acceptance; inspect the entrypoint's actual report for that disposition.
- A resource stop, nonzero exit, interrupt or cleanup uncertainty is an
  unsuccessful or unknown operation, **not** a rejected mathematical theorem.
  Earlier commits and partial output may exist. The launcher never rolls back
  state, removes a lock, overwrites diagnostics or restarts automatically.
- Recover through the existing owner/state recovery rules. Preserve child logs
  and reports, especially when the outer Job interrupted inner cleanup.

The Job enforces lifetime-on-close, aggregate private commitment and simultaneous
process limits, with its existing user-CPU control. Wall time, total user+kernel
CPU and log lengths are sampled, so they can overshoot. Failed cleanup may consume
additional time and is reported, not silently counted as a clean completion.
The trusted launcher itself stays outside the child Job: its bootstrap has a
cooperative CPU/time check, existing supervision has its separate sampled wrapper
CPU cap, and total wrapper CPU is reported separately. Do not add nested native
Job CPU to the outer Job CPU: those descendants are already included.

There is no hard disk quota, filesystem/network privilege sandbox, protection
against a hostile same-account process, or safe arbitrary-source execution claim.
The launcher closes a whole-controller resource boundary, not all deployment or
large-network growth requirements. Its focused review and execution evidence
must be adopted separately from these source instructions.

## Reusing a protected authoring ancestor

For `owner -- contribute`, the launcher accepts the optional
`--authoring-frontier-root ROOT_ID` with `--project-authoring` and
`--project-authoring-sha256`. Use the exact lowercase 64-hex identity of the
selected checked ancestor. This limits scratch reconstruction at that protected
ancestor; the contribution is still checked against its actual selected parent.
It does not trust remote theorem claims or bypass admission.

The owner verifies operation/project eligibility and the frontier relationship;
well-formed identity text alone is not authority. Omit the flag to retain the
existing authoring route. All runtime, source-approval, resource and recovery
rules above still apply. This option does not apply to `produce-baseline`, peer
operations or queries.

## Search by a known concept

The query entry additionally accepts --symbol-names with --context-root and the normal owner selection. Supply a JSON list of exact Lean names, or use the companion's prepare-symbol-query action to convert ordinary qualified names. This option is exclusive with --native-type and requires a selected local context. It prepares type-symbol search constraints using that context's exact identities; it performs no native elaboration, peer lookup or mathematical admission. Missing names yield no ready query. The same limits, input-path separation and closure rules apply. Relevance and search coverage remain properties of the selected indexes and query budget.
