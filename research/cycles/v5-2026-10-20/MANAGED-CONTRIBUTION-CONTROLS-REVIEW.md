# Private-credential controls and preparation selector review

2026-10-21, support_screen. **PASS, SOURCE ONLY.** The four-group controls and
their preparation-only selector have no remaining source-level blocker within
the selected network-free helper scope. This is not a test result, actual grant
issuance, installed contribution or execution authorization.

## Exact reviewed artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/managed_contribution/credential_controls.py` | 20603 | `c274f8f5b71a58a38b7c2eae5e8b10b94d12f82c6e8233461f1a008880b5d09b` |
| `research/cycles/v5-2026-10-20/Select-ManagedContributionControls01.ps1` | 6420 | `466f678b3a3da9690ef3b2d80a11745e689dd9edd0d7c7b4ccdcc2860cb84b21` |
| `research/cycles/v5-2026-10-20/MANAGED-CONTRIBUTION-CONTROLS-SOURCE.md` | 9647 | `47ddc1b257576f113088bf0d3f472e59ccf89802fc0fa164ccc7d7159ae823d9` |

All three were read completely. The helper is the separately reviewed12374-byte
`7116e2d9161cbb828203bc7eff1e7dd90c1cab7d6e860a6e16801ffb6ecb37f0`;
the immutable implementation review remains `MANAGED-CONTRIBUTION-REVIEW.md`
at `86840438a5920c19e27654b6d30d4c0c4a0bc7e1f5bd6fdb88ca1d1deba0028f`.

## Concrete controls argument

- The selected loader validates the adopted126 SDK map and pinned release,
  overlays only the exact new helper snapshot, then checks the resulting127
  source rows, imported origins and final hashes. Canonical cwd, installed
  isolated/no-site/no-bytecode Python and exact outer snapshot location are
  required. The selected manifest has no zero-byte source rows or two-component
  root-level module rows that would invalidate the loader's size/prefix checks.
- Group1 checks a nonmutating positive preflight and seven refusals covering
  both overlap directions, exact overlap, relative paths, absent protection,
  unadopted confidentiality and existing target preservation.
- Group2 has15 related reader refusals: pin extent/digest, canonical/duplicate/
  partial/oversized bytes, token-ID mismatch, unexpected metadata/scope, and
  independently supplied release/profile/runtime/session/plan/generation
  bindings. Malformed synthetic input bytes remain preserved.
- Group3 returns actual idle `PlacementClient` instances, not fabricated client
  objects. It checks independent contact/egress and four caller caps, both
  earlier-caller and earlier-original deadlines, and ten refusals. The explicit
  three-tick clock injection reaches expiry after genuine client construction
  and requires that actual client to be closed. It is labeled a simulation;
  no request, timer sleep or new deadline allowance is used.
- Group4 checks sanitized error fields, suppression of a deliberately injected
  secret-bearing I/O exception, and rejection of an arbitrary service before
  issuance or destination creation. The two facade refusals do not purport to
  exercise post-issuance failures or grant-charge persistence.
- Process/system launch, socket/connect/listen, service start/issuance and
  deletion calls are guarded and recorded as failures. Fixtures are fresh and
  retained under the output. The deterministic public token is a nonissued
  parser fixture, not an authentic secret or OS-protected credential. It is
  excluded from the final bounded result. Raw unittest output may contain
  synthetic fixture values on failure; no genuine credential exists here.

The exact helper requires a real started service for positive publication.
Avoiding a fabricated service is correct: the network-free suite cannot
qualify actual issuance, partial authentic output or durable charges. Those
remain source-reasoned boundaries and separately selected ordinary integration
obligations, not missing assertions silently reported as passed. The author
checkpoint and result schema disclose this limitation explicitly.

## Preparation selector argument

The fixed installed126 release is
`8fcf2c971029c8ad0787ec8da0891be178a95b80999f8bccc262e077009701a2`;
its build input is
`4a9bfd78afd328d629ee6ad967f7f9378034db86cdee86bef751c5c50e6778a1`.
The selector binds and compares installed/source byte-hash rows. It selects
only18 Python runtime rows from adopted lifecycle selection
`aac5291b234e237e19f75e934fbb8ecf39971027743b85c206035f2f837b4007`,
then adds release/build/basis:126+18+3=147 runtime pins. Direct metadata
inspection confirms the18-row prefix selection. No old Node/fixture/service
state or mathematical runtime is selected.

The exact two-key caller map must use controls `c274f8f5...` and helper
`7116e2d9...`; the helper's embedded extent/digest is additionally asserted.
The unchanged runner is the third snapshot, at
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
The new selection/input-name/allocation must be absent. Only the bounded
selection JSON is exclusively created/flushed; no output allocation is made
and no runner is invoked. The result says `executed=false` and provides the
actual selection digest. Limits are30 CPU seconds,60 wall seconds,256 MiB,
two active processes and1 MiB per output stream. Root must separately adopt
the exact source pins and generated selection before any launch.

## Review and qualification boundary

The author reports one authorized stdlib AST parse of the unchanged controls
and a zero-error PowerShell parse; the reviewer did not repeat either parse.
This review used source reads, metadata inspection and small-file hashes only.
No product import, control execution, selector invocation, secret read,
installation, issuance, service, deletion, mathematical work or Git operation
was performed. Prospective PASS requires exactly four tests with no failures,
errors, skips or forbidden calls plus final source/origin rebinding; only a
later independently inspected actual run can establish that result.

Windows ACL confidentiality, hostile same-account isolation, cross-host/reboot
freshness, authentic publish-failure charge persistence, mathematical acceptance
and complete-v5 qualification remain outside this review and these controls.
