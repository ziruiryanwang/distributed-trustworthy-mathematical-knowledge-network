# Ordinary peer package

This v5 candidate adds direct-contact discovery and sharing to the
[persistent ordinary owner](../ordinary_package/README.md). It reuses the existing
Lean checker, custody and index. Certificates are not required. It is not yet a
final public release: source review, file-only assembly, six focused pure
controls and the actual nine-command reciprocal CLI workflow passed their
independent audits. The broader release obligations below remain open.
License undecided.

## What the commands mean

| Command | Result | What it does not establish |
|---|---|---|
| `find` | Candidates from selected index providers | Mathematical truth, global completeness or absence |
| `receive` | Acquire selected evidence and its missing dependencies, then check locally | Trust in the provider's own acceptance flag |
| `owner.py contribute` | Check a caller-written extension against an explicit local parent | Safe execution of arbitrary downloaded Lean source |
| `publish` | Add exact accepted local targets to a local index | Remote publication or another mathematical check |
| `serve` | Expose the selected custody and index for a finite lease | Permanent availability, remote writes or research coordination |

Peers exchange inert declarations, not executable source or native snapshots.
Local source must be owner-approved. Cold ordinary acquisition can still require
the missing proof dependency closure. Previously checked local mathematics is
reused under its protected local warrant. No client needs the whole network's
contents, but that is not a constant-cost claim for a large selected context.

## Assemble without rebuilding Lean

Build a base package as described in the ordinary-owner README, or select an
existing exact base. Then run the trusted source assembler:

```text
<Python>/python.exe -I -S -B <repository>/software/v5/ordinary_peer_package/assemble.py
  --source-root <repository>
  --base-package <base-package> --base-profile-sha256 <base-profile-hash>
  --python-runtime <Python> --lean-runtime <Lean>
  --output <fresh-successor-directory> --wall-seconds 60 --cpu-seconds 40
```

Every path is absolute. The assembler verifies the supported base, copies only
its selected payload, replaces the adjacent profile loader and adds six Python
files. It never copies owner state or builds native modules. `PROFILE.json` is
committed last. Keep the returned profile hash. Native installation identity
remains unchanged, so an existing compatible owner can reopen without migration
or initialization. Do not modify the original package in place.

The locally assembled candidate's profile is
`06649545f962e8ca95b21ab1c87626444bdc06c16e5191b96a8f27e7766505e5`.
It contains 117 runtime files (36,680,265 bytes), plus an assembly receipt.
Explicit supported runtimes are still required; this is not a hermetic build.
A profile hash selects bytes, not an unknown publisher's authenticity.

## Common invocation

```text
<Python>/python.exe -I -S -B <package>/peer.py <find|receive|publish|serve>
  --profile-sha256 <selected-hash>
  --python-runtime <Python> --lean-runtime <Lean>
  --config <owner-config.json> --config-sha256 <config-file-hash>
  --output <fresh-result-directory>
  --wall-seconds 120 --cpu-seconds 90 --memory-mib 1536
```

Except for `find`, also select the same existing `--catalog`, `--custody`,
`--store-id` and `--custody-limits` used by `owner.py`. Do not initialize the owner
again. The unchanged `owner.py` entry still supplies init/status/contribute.

Configuration is explicit bounded JSON. The exact field and limit contracts are
in [the coordinator notes](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PEER-IMPLEMENTATION.md)
and [CLI notes](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PEER-CLI.md).
There are no implicit contacts, latest branches, renewed grants or retries.

The intended sequence is:

1. Find using formal feature specifications and a finite contact/search budget.
2. Select a returned `{provider, snapshot_id, record}` and an exact local parent.
   Receive binds the preview to evidence, obtains missing dependencies and runs
   independent admission. Keep its returned local root and target identities.
3. Contribute owner-written source using those acquired targets through the
   existing owner command. Keep its new root and targets.
4. Publish those targets from that exact checked context into a selected local
   index. This can create a fresh index only when explicitly configured.
5. Serve the existing index/custody for a finite lease, with cleanup reserve.

## Important operating limits

Serving exposes **every addressable object in the selected custody**, including
inert objects that are not indexed or locally accepted. Both `share_all_custody`
and `exclusive` must explicitly be true. The CLI holds the ordinary owner lock
through service shutdown. Other public commands using that same owner cannot
mutate it meanwhile. Do not point unrelated catalogs or uncontrolled programs at
the same custody/index. There is no per-object access control or hidden filtering.

Contacts use literal IPs. Plaintext is permitted only on loopback; remote contacts
require verified TLS. Owner-selected CA files are hash-pinned, or null explicitly
selects system CAs. Server certificate/key bytes remain local owner selections.
The present search is fail-fast: a bad provider can end the call, with earlier
matches and costs retained. It is not automatic resilient failover. Pagination
and candidate proofs do not establish that the whole mathematical corpus was
searched, or that skipped ranges contain no matches.

Each command has one original resource allowance. API composition must also share
one network ledger; a prepaid search allocation is never renewed for receipt.
Windows Jobs constrain native workers but are not a hostile-source sandbox.
Controller limits are cooperative: hard whole-process/service bounds require an
external supervisor. `--memory-mib` is not a hard cap on the controller's memory.

`READY.json` means the finite listener is open, not that knowledge was accepted.
`RESULT.json` and stdout record terminal outcomes. Preserve failures: admission
or some index publications may already have committed before reporting fails.
A failed command does not imply rollback. Reopening an owner may settle abandoned
operations during recovery; operational schema rejection can occur after that
reopen. Profile/config-hash rejection happens before owner opening.

## Evidence and remaining release work

The [independent outcome](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PEER-OUTCOME.md)
records exactly what has run. File-only assembly took 4.04 elapsed seconds and
1.91 known inclusive CPU seconds, with compiled bytes unchanged; that is an
assembly observation, not a mathematical-growth or comparative performance result.
The six pure controls also loaded the successor profile in a fresh process and
passed in 1.36 elapsed seconds / 1.19 known CPU seconds. They use explicit mocks
and perform no native checking or peer communication; see the outcome's scope.

The [public reciprocal outcome](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-PEER-RECIPROCAL-OUTCOME.md)
records nine actual commands: publish, initialize a genuinely new receiver,
serve, discover, receive, contribute offline, publish, serve and discover again.
The receiver checked a theorem and its missing definition, then used that theorem
twice in a new checked proof after the supplier stopped. The final cold client
discovered the new export; it did not independently accept it. Original owner
files stayed unchanged. Both services and all processes closed cleanly.

The complete run cost 87.63 elapsed seconds (including 60 seconds of service
leases) and 30.81 known inclusive CPU seconds. A preceding plan was rejected
before any product command because it exceeded the supervisor's process-count
ceiling; its failure remains recorded. These are workflow observations, not a
net-benefit comparison with optimized ordinary library sharing.

Large-scale relevance, selected-context costs, ordinary project/editor integration,
full-cost benefit against optimized package sharing, resilient provider operation,
independent hosting and public-release assurance still need justified solutions.
This interface is a practical integration step toward v5, not a substitute for
those requirements or permission to publish externally.
