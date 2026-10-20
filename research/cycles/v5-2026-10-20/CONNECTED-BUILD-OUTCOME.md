# Connected installation: independent saved-build audit

2026-10-20, `core_release`. Canonical guard passed. Saved evidence, exact maps
and selected changed-file hashes only; no build, import, test, service, RAM work
or Git operation repeated.

**Disposition: PASS for the exact file-only connected installation.**

Installation: `product-local/v5-distribution-connected-01/Mathematical Commons v5`.
Release manifest SHA-256:
`69d9456eb53135061bc68a8d657ae0f25bc71013cd9c8d2cd5f571c4c7996ef5`.
The saved builder reports `DIRECTORY_CREATED_AND_EXACTLY_VERIFIED` with 9,851
payload files and 842,219,712 bytes (the manifest is outside that payload count).

## Map and binding findings

- Original and saved plans both match
  `9484fda5bc1b6a2648d4d06b73be443ca361adee8f3d73210655efc07cffdab1`.
  Both source pins match originals and snapshots; all 22 runtime/input pins match.
- Compared with distribution03, exactly four existing payloads change: README,
  builder, workspace-evidence alias and staged-workspace alias. No file is removed.
- Exactly 5,900 payloads are added: the 5,896 fixed-manifest Node/overlay rows,
  the advertised-service wrapper, semantic-reader helper, advertised-service
  implementation and acquisition-resilience transport. Every optional base row
  matches the retained catalogue; there is no unexplained base addition/change.
- All 106 installed SDK manifest bindings match the selected input's lengths,
  hashes and logical paths. The eight non-base changed/added files were also
  independently hashed from disk and match. The new wrapper is precisely the
  selected import of `client.serve_advertised.main`.
- All other retained manifest fields are structurally unchanged, apart from
  schema, base role, input identity, SDK map and the explained preparation-source
  map. All 85 preparation source pins exactly correspond to installed v5 Python
  SDK rows. Assets, foundation/policy/relation, Lean support and runtime roles
  have no unexplained change.

The reviewed exact builder's successful path performs full copied-file hash
checks, final directory census and full installed readback before returning
success. This audit verifies that saved outcome and its exact source/output
bindings, rather than redundantly reading all 842 MB again. No independent
second full-file traversal is claimed.

## Outcome and cost

The command exited zero, direct child was reaped, Job closed, final active
processes were zero, and no cleanup error or termination request occurred.
Worker CPU was 31.796875 seconds; wrapper CPU was 0.796875 seconds; known whole
CPU was **32.59375 seconds**. Wall time was **177.61060529993847 seconds**, within
the original 120 CPU / 300 wall seconds / 128 MiB / two-process envelope.
Stderr was empty. No allowance was renewed.

| Saved evidence | SHA-256 |
|---|---|
| `experiments/v5-local-checks/distribution-connected-build-01/RESULT.json` | `775c7b6ff2230581eca8f8646e949c207415368ca037bab117d14b76310b3e09` |
| `command/stdout.txt` | `469937b96abfed30fc0625a59c4f79da0fc53a9df810b4471b95ada71d0947b1` |

This establishes the byte-verified optional-role installation. It does not
establish actual advertised service, mathematical admission, independently
hosted operation, useful-growth advantage or completed v5. The separate
installed-service adapter review remains the next integration boundary.
