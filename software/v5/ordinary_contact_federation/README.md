# Ordinary Lean investigator with optional contact discovery

This successor adds `peer directory-find` and `peer directory-serve` for bounded,
one-hop specialist-provider suggestions. See [CONTACTS.md](CONTACTS.md) for the
actual configurations, trust boundaries and commands. Both are state-free; the
existing mathematics and native support are unchanged. This layer does not
establish complete discovery, accelerated growth or final-v5 release readiness.

The build instructions below describe the preserved fair baseline. For this
successor, select that baseline and its ASSEMBLY.json, then apply the separately
approved contact overlay using `ordinary_contact_federation/assemble.py`,
`OVERLAY.json` and their exact hashes. Its required arguments are --source-root,
--base-package, --base-profile-sha256, --base-receipt, --base-receipt-sha256,
--overlay, --overlay-sha256, --output, --wall-seconds and --cpu-seconds.
It copies native bytes without rebuilding and commits the fresh PROFILE last.
Use that NEW PROFILE for all subsequent commands. The old kit's approved-profile
list does not include this successor; use the explicit command documented above.

## Preserved baseline capabilities

This package adds bounded provider scheduling to the ordinary Lean investigator.
It preserves native-first authoring, independent mathematical checking, unfamiliar
definition inspection and ordinary-project reuse. It is not an autonomous theory
generator or evidence of accelerated mathematical discovery. The full v5 release
goal remains open; adoption and runtime results belong to separate checkpoints.

## Build or reuse a selected baseline

Supported runtime profile remains Windows x86-64, Python 3.14.6 and Lean 4.34.0.
First build the bounded investigator using the source checkout's
`software/v5/ordinary_bounded_operations/build.py` and its README, or select an
already built compatible package. Select its exact PROFILE and external
`_build/BUILD-RESULT.json` hashes. Do not edit the original package. Then run:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_fair_search\assemble.py' `
  --source-root 'C:\commons-source' `
  --base-package 'C:\commons-builds\bounded-investigator-01\package' `
  --base-profile-sha256 'REPLACE_WITH_SELECTED_PROFILE_SHA256' `
  --base-build-receipt 'C:\commons-builds\bounded-investigator-01\_build\BUILD-RESULT.json' `
  --base-build-receipt-sha256 'REPLACE_WITH_SELECTED_RECEIPT_SHA256' `
  --output 'C:\commons-builds\fair-investigator-01' `
  --wall-seconds 120 --cpu-seconds 90
```

Replace both hash placeholders with the independently selected exact values.
The output directory must be absent and its parent must already exist. Bounds
are examples, not a success promise: 10-600 wall seconds and 5-600 CPU seconds.
This file-only assembly imports no product code, runs no compiler and contacts
no provider. It copies every selected native byte unchanged; compatible fresh
builds use their own explicit manifests rather than historical binary pins.
The operator must approve the baseline, receipt, overlay source and runtime.
Hashes bind bytes; they do not authenticate an author or certify safety.

Output is `package/` plus an external `ASSEMBLY.json`. Success requires a zero
exit and a matching `ASSEMBLED_NOT_ADOPTED` receipt. Partial output is retained
on failure, without automatic retry. PROFILE commits last inside the package;
its presence alone does not prove successful assembly. The assembler makes
cooperative time checks; an enclosing owner Job is needed for enforced process
containment. It assumes immutable owner-approved storage, not concurrent hostile
writers. Preserve the build/assembly receipts for later selection and diagnosis.

## Use the package

Use packaged `run.py` with the approved Python `-I -S -B`, the new exact
`--profile-sha256` from the assembly receipt and the selected external runtimes.
[LAUNCHER.md](LAUNCHER.md) documents whole-operation limits and exact command
flags. [PRODUCER.md](PRODUCER.md) documents approved compiled-project export.
[RECEIVE-POLICY.md](RECEIVE-POLICY.md) documents explicit dependency policies.
Existing configuration shapes are unchanged. A helper kit pinned to a predecessor
PROFILE must not silently be used as if it selected this successor.

| Public entry | Operations | What the result establishes |
|---|---|---|
| peer | find, preview, inspect, authoring-offers | Bounded inert discovery information, not mathematical acceptance |
| owner | produce-baseline | An exact inert export from an explicitly approved local project |
| owner | init, status, intake-baseline | Receiver-selected context and actual independent checking |
| peer | receive, publish, serve | Selected acquisition/checking, indexing and finite custody exposure |
| owner | contribute, extract-std, extract-project, complete, export-module | Existing narrower checked construction/materialization routes |

The practical loop is: choose contacts and a formal query; find and preview an
actual result; inspect unfamiliar definitions; optionally query advisory
authoring-project offers; independently approve and obtain a compatible ordinary
Lean project; investigate definitions, models, countermodels and connections
locally; export selected completed work; have a receiver check it; publish exact
accepted targets and serve selected custody. Actual target identities come from
public outputs, not guessed names or private-state edits. Peer advertisements
never authorize source execution. Draft hypotheses remain drafts. There is no
required global research agenda, human-intention acceptance field or model API.

State-free find/preview/inspect/authoring-offers reject owner catalog/custody/store
arguments. Stateful operations require their explicit approved context. Receive
must select `selected-unit-only` or `bounded-closure`; the former can report
`NEED_GROUNDED_PREMISES` without fetching ancestry, while the latter explicitly
permits bounded dependency acquisition. Cold acceptance may still require a
dependency closure. Publication and serving do not guarantee perpetual custody.

## What changes in search

Find retains one original SearchSession and one prepaid outer budget. It offers
each selected provider once, then requests at most one page per active provider
per round. No grant renewal, retry, replacement session or concurrent request is
introduced. Asynchronous attempts are capped at five seconds and further narrowed
by residual time and queued opportunities, with a one-second closure reserve.
Only recognized failures with observed clean settlement can yield to another
provider. Uncertain connection cleanup, cancellation and unknown local failures
remain fatal; earlier verified matches and charges remain visible.

This reduces first-provider starvation when grants and local/cleanup costs permit
later attempts. It does not guarantee reaching every provider: small aggregate
budgets can end earlier. Synchronous CA loading, JSON/proof work and OS scheduling
are not preempted by the attempt timer. Offering all providers first can delay
the first hit. Query semantics, positive-record verification, coverage claims,
wire format and mathematical admission rules do not change. Partial results are
not global absence or completeness claims.

## Exact scope and remaining limits

The selected 148-file fair baseline becomes 150 files: eight existing payloads
are replaced and contact_directory.py plus CONTACTS.md are added. PROFILE is
regenerated last and contains 116 auxiliary roles. Changed source is peer.py,
peer_api.py, run.py, profile.py, http_provider.py, fair_exchange.py and
fair_search.py; README is the eighth replacement. All 28 installation payloads,
native helpers and other three documents are unchanged. Absolute deadline
propagation prevents transport-local timing from renewing the original horizon.
No state migration, new mathematics policy, foundation, cryptography or native
compilation is added.

Ordinary Lean authoring permits agents to invent definitions and develop theories;
this transport/checking infrastructure does not guarantee their novelty, value or
speed. Learned selection and exact proof acceptance remain distinct. Search is
bounded and incomplete. Ordinary source approval, OS resource limits and final
proof checks are not a hostile-source security sandbox. Public deployment still
requires its own license, maintenance, security and operational decisions.
