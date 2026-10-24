# Inspect a candidate before acquiring its proofs

This source successor adds `peer.py preview` to the ordinary peer interface.
It lets an agent inspect one unfamiliar candidate's complete formal type and
referenced-symbol identities before deciding whether to download its proof
closure and check it. Referenced definitions' bodies are not included, and a
preview does not establish whether the theorem applies to the agent's work.

The implementation reuses the existing preview/record verifier. It adds no
index, checker, certificate requirement or mathematical acceptance rule. Only
`peer.py` and `peer_api.py` are intended to change in a freshly assembled package;
existing owners, custody and installed packages remain untouched. Source review,
19 focused controls, file-only assembly and the two-call real-HTTP integration
passed independent review. The selected development package is
`experiments/v5-local-checks/ordinary-preview-assembly-01/package`, profile
`ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f`.
Do not run the loose source entry as if it were an assembled package.

## Practical workflow

1. Use `find` to obtain candidate records from explicitly selected providers.
2. Choose one exact `{provider, snapshot_id, record}` from the result and pass it
   to `preview`. Read the returned canonical type and symbol identities.
3. If the candidate looks irrelevant, stop without acquiring its evidence or
   opening any local mathematical owner state.
4. If it looks promising, use the existing `receive` with that same selection,
   an explicit local parent root and a separately selected receipt budget.
   Only independent admission establishes local mathematical acceptance.

`receive` still fetches its own preview. The two-command path therefore pays
for that preview twice; this interface does not claim a preview cache. Savings
are conditional: avoided proof acquisition/checking for rejected candidates
must exceed inspection and extra-command costs. This is not a proof of useful
growth, and an optimized ordinary-library comparison also gets previewing.

## Preview configuration

The JSON object has exactly three keys: `contacts`, `selection`, and `limits`.
Use the existing selected contact map without referrals or automatic expansion.
Each contact label maps to exactly:

```text
{host, port, tls, server_name, ca_file, ca_sha256}
```

Hosts are literal IP addresses. Plain HTTP is loopback-only; remote contacts
require verified TLS. Optional values are explicit JSON `null`. `ca_file` and
`ca_sha256` are both null for system CAs, or both supplied for a selected,
hash-pinned CA file. The selected provider label must be in `contacts`.

`selection` has exactly `provider`, `snapshot_id`, and `record`. Copy the full
selection, including the complete record, from the earlier discovery result;
do not replace it with a theorem name or object hash. The snapshot identity is
retained context, not authority: this command does not reverify index membership.

`limits` has exactly these two integer fields:

```json
{"requests":1,"reply_bytes":1048576}
```

`requests` must equal one. `reply_bytes` may be any positive integer up to
1,048,576 bytes (1 MiB), and must cover the record's advertised preview object
size. An advertised oversize is refused before network I/O. A validation failure
may make zero requests; otherwise only the selected preview is requested, with
no retry, candidate loop, dependency locator or evidence fetch.

## Packaged CLI invocation

After a separately reviewed fresh package has been assembled, invoke its entry
with its actual profile hash, supported runtimes and an exact config-file hash:

```text
<Python>/python.exe -I -S -B <package>/peer.py preview
  --profile-sha256 <selected-profile-hash>
  --python-runtime <Python> --lean-runtime <Lean>
  --config <preview-config.json> --config-sha256 <config-file-hash>
  --output <fresh-result-directory>
  --wall-seconds 120 --cpu-seconds 30 --memory-mib 512
```

This is one logical command; all file and directory paths must be absolute.
Like `find`, `preview` forbids `--catalog`, `--custody`, `--store-id`, and
`--custody-limits`. It does not read an adoption marker or open an owner/custody
store. The selected package and runtime identities are still checked, but no
native compiler or mathematical admission runs. The displayed resource limits
are an example caller grant, not measured costs or a required experiment.

Success is written to the fresh output directory's `RESULT.json` and stdout.
The result contains the detached original `selection`, full parsed `preview`,
`preview_sha256`, `preview_bytes`, namespace and network/acquisition accounting.
Its status is `PREVIEW_BOUND_NOT_ACCEPTED`, with these explicit false fields:

- `mathematical_acceptance`
- `evidence_bound`
- `snapshot_membership_reverified`

The binding means that the returned bytes reproduce the complete advertised
record, not that the mathematics is true. A well-bound preview can advertise a
false result. It is inert data, not source to execute or an instruction to obey.
Neither success nor failure establishes global search completeness, novelty,
semantic applicability or absence of useful mathematics.

## Budgets and implementation checkpoint

Each CLI invocation has one explicit finite allowance. At the API seam,
`await preview(loaded, config, allowance, network_budget=...)` can share the
existing aggregate network ledger: it consumes remaining capacity, never renews
it after failure, and leaves a caller-supplied ledger open. An internally created
ledger is closed by this call. Retain charged failures and terminal reports.
Controller limits remain cooperative and require an external supervisor for
hard whole-process limits; `--memory-mib` is not a hard controller memory cap.

The CLI is a minimal additive successor of
`../ordinary_peer_package/peer.py`. Its source-candidate SHA-256 is
`bf90809c35eb0a2cbc827d678bded411d8187dcfe2ba52223d443e2ce439e26d`;
the unchanged predecessor's SHA-256 is
`c1e88338408f59a26d70d27d9c9968b7b6192f6d0ac6b99121ad19e5f78e1930`.
All prior find-only state boundaries now apply to both `find` and `preview`.
Dispatch is explicit for every operation, including `serve`; unknown operations
cannot fall through to service startup. Bootstrap, profile/config pins,
allowance, reporting and existing operation semantics are otherwise preserved.
The focused controls used real preview validation with inert transport. The
subsequent public integration used the actual assembled CLI over a bounded
loopback static responder: one correct 1,351-byte preview, then one same-length
tampered reply. The correct preview returned its complete type; tampering refused
with `ORDINARY_PREVIEW_EXACT_BYTES`. Each call charged one request and 1,351 reply
bytes, including the refusal. No owner, native checker or evidence operation ran.
This is not a full provider, TLS, relevance or growth benchmark. Full deployable
v5 remains unfinished.

The actual two-call check took 4.0682 wall seconds and 3.6875 known inclusive CPU
seconds, including its enclosing supervision. These are complete test costs,
not a user speedup. See the
[saved independent review](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-DISCOVERY-NEXT-CHALLENGE.md).

## File-only packaging and clean source recipe

`assemble.py` selects the approved-project intake package by its exact profile
`aab7e2460c0879d0fbb2b570470984efe2a66c4a932f5725ce563a1df7c2530f`
and assembly receipt
`3dfa9092062be83fad2b27d327c76b28ea5a0603ea244e78624884d8e00380a3`.
It requires explicit `--peer-sha256` and `--peer-api-sha256` reviewed replacement
hashes; these are not inferred from whichever source files happen to exist.
The exact delta is two changed runtime files, zero additions and 132 unchanged
files. Copies are streamed, predecessor and selected bytes are rechecked, and
`PROFILE.json` is committed last. No native build or state operation is involved.

```text
<Python>/python.exe -I -S -B <repository>/software/v5/ordinary_preview_package/assemble.py
  --source-root <repository> --base-package <selected-approved-project-package>
  --base-profile-sha256 aab7e2460c0879d0fbb2b570470984efe2a66c4a932f5725ce563a1df7c2530f
  --peer-sha256 <reviewed-peer-hash> --peer-api-sha256 <reviewed-peer-api-hash>
  --python-runtime <Python> --lean-runtime <Lean>
  --output <fresh-package-directory> --wall-seconds 60 --cpu-seconds 40
```

`select_assembly.py` writes, but does not launch, the finite local supervisor
selection. Its required arguments are `--name`, `--peer-sha256` and
`--peer-api-sha256`; the base package path is the retained
`experiments/v5-local-checks/ordinary-project-extraction-build-01/integration/package`.
The selection pins that package, receipt, runtimes, new sources and selected
assembler. Outer limits are 90 wall seconds, 50 CPU seconds, 512 MiB and two
active processes. Actual execution still requires root's separate selection.

For source-complete distribution, `build.py` and `source-map.json` are successors
of the approved-project recipe. The map still selects 71 sources and 54 direct
copies; only the two peer source paths and pins change. All native lanes,
transforms, runtime pins, owner/module support and acceptance installation remain
unchanged. The recipe itself changes only its description, own path prefix and
map hash. It has not been run: a redundant full compiler campaign is not needed
for this file-only change.

Source-only review pins (2026-10-24):

- `assemble.py`: `7be8f6ea6f84d4789b8492d20d2c7eb0b799503ac80b9f629229068ec88c45d7`
- `select_assembly.py`: `fcce660bab3c2f9e4bad73251f1a8123b4a9cbc2542aea2bc1cd3c0d3936e16a`
- `build.py`: `c0cf85148668f2382a1dd66356b01c1f5c9d60f1e6ae3a7e91b05c01cd31a99d`
- `source-map.json`: `f567b842b7e74a3167dcb7dd999fa7d3030c7faa062cd9c365a7a373126252fa`

These pins identify candidate source bytes, not a passed runtime or release gate.
