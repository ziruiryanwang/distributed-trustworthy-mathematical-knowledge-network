# Ordinary Lean investigator with optional selective discovery

This successor adds optional provider-local pair access paths and an explicitly
selected sparse V2 search protocol. See [SPARSE-SEARCH.md](SPARSE-SEARCH.md) for
configuration, costs and limits. It retains `peer directory-find` and
`peer directory-serve` for bounded one-hop provider suggestions, documented in
[CONTACTS.md](CONTACTS.md). Mathematical checking and native support are unchanged.
Neither layer establishes complete discovery, accelerated growth or final-v5
release readiness. Review/test adoption is recorded separately from these sources.

The build instructions below describe the preserved fair baseline. Apply the
approved contact overlay to that fair package first, using the source checkout's
`software/v5/ordinary_contact_federation/assemble.py` and its `OVERLAY.json`.
Alternatively, select an already assembled compatible contact package and receipt.
Then apply THIS sparse successor with
`software/v5/ordinary_sparse_access/assemble.py` and its own `OVERLAY.json`.
Each overlay takes its immediate predecessor package and ASSEMBLY.json, not the
original native build receipt. Required arguments are --source-root,
--base-package, --base-profile-sha256, --base-receipt, --base-receipt-sha256,
--overlay, --overlay-sha256, --output, --wall-seconds and --cpu-seconds.
It copies native bytes without rebuilding and commits the fresh PROFILE last.
Use the final sparse assembly's NEW PROFILE for all subsequent commands. Select
all source/overlay/receipt hashes independently; the old kit's approved-profile
list does not include this successor. No historical kit approval transfers.

## Preserved baseline capabilities

The preserved fair baseline added bounded provider scheduling to the investigator.
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
Existing configurations remain valid; opt-in additions are in SPARSE-SEARCH.md.
A helper kit pinned to a predecessor
PROFILE must not silently be used as if it selected this successor.

| Public entry | Operations | What the result establishes |
|---|---|---|
| peer | find, preview, inspect, authoring-offers | Bounded inert discovery information, not mathematical acceptance |
| peer | directory-find, directory-serve | Advisory one-hop contacts and subsequent bounded search, not mathematical acceptance |
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
V1 wire format and mathematical admission rules do not change. Sparse V2 changes
only the explicitly selected positive-search traversal/accounting protocol.
Partial results are
not global absence or completeness claims.

## Exact scope and remaining limits

The selected 150-file contact baseline becomes 152 files: ten existing payloads
are replaced, and pair_access.py plus SPARSE-SEARCH.md are added. PROFILE is
regenerated last and contains 117 auxiliary roles. The replacements are peer.py,
peer_api.py, profile.py, http_provider.py, fair_exchange.py, fair_search.py,
search_session.py, discovery_store.py, candidate_query.py and this README.
All 28 installation payloads, native helpers and other four documents are
unchanged. Existing contact discovery and original deadlines are retained.
There is no state migration, new mathematics policy, foundation, cryptography
or native compilation. Enabled physical indexes require a fresh explicit config.

Ordinary Lean authoring permits agents to invent definitions and develop theories;
this transport/checking infrastructure does not guarantee their novelty, value or
speed. Learned selection and exact proof acceptance remain distinct. Search is
bounded and incomplete. Ordinary source approval, OS resource limits and final
proof checks are not a hostile-source security sandbox. Public deployment still
requires its own license, maintenance, security and operational decisions.

## Optional selective two-feature search

Providers and readers may opt into the sparse V2 discovery path described in
[SPARSE-SEARCH.md](SPARSE-SEARCH.md). It preserves ordinary mathematical checking
and atomic positive proofs. The index is a fresh, owner-selected capacity
investment, not automatic migration or a claim of complete global discovery.

