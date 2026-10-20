# Installed connected service 01: independent failure audit

2026-10-20, `core_release`. Read-only saved-evidence/source audit; no rerun,
import, runtime launch, full runtime scan, RAM work or Git action.

**Disposition: FAILED before provider boot at a test request-contract mismatch.**
Preserve the used adapter, installation, request, allocation and failure. The
public serving/discovery boundary is not qualified by this attempt.

## Exact cause and actual extent

The actual installed `distribution.py launch ... serve-advertised` command
reached installed `client.launch.read_plan` and raised `CLIENT_OUTPUT_LIMITS`.
The adapter selected output bytes `32 * 1024**2 = 33,554,432`, but the retained
launcher requires `SOURCE_TOTAL = 64 * 1024**2 = 67,108,864` as its minimum.
This is an output-census allowance, not RAM consumption. The earlier source
review missed this fixed lower bound; its clearance did not establish contract
compatibility. No product bug or insufficient-PC-resource conclusion follows.

The distribution wrapper created its request/launch control files. The provider
run directory does not exist, so boot, provider Node, service READY, route
publication, descriptor acquisition and HTTP queries never occurred. The
adapter's `CHECK_PUBLIC_ENDED_BEFORE_READY` is the downstream symptom.

The reader Node did start. It received one stop command and closed with return
code zero, `channel_failed:false` and `forced_termination:false`. Its exact
5,896-file runtime pre/post checks completed (2.6495068 / 2.6192619 wall seconds;
2.625 / 2.5625 CPU seconds) and its five role-source bindings remained identical.
The saved `real_node_roles:2` is a hard-coded intended count, not an observed
count: only one Node role ran in this failed attempt. No two-role claim is adopted.

## Evidence and original envelope

Original and saved selections both match
`0e77f95323b772f0b4e8add0d0a8335bd3675c55d74a27035a96f4cccca08434`.
Both source pins match originals and snapshots; all 39 selected runtime/input
pins match. All 67 reported reader import origins belong to the exact installed
SDK and their current file hashes match the adopted release. No mismatch found.
The unchanged release is `69d9456eb53135061bc68a8d657ae0f25bc71013cd9c8d2cd5f571c4c7996ef5`.

The outer command failed with exit 1, but direct child was reaped, Job closed,
final active processes were zero, and no cleanup error, forced termination or
supervisor termination request occurred. Worker CPU was 10.8125 seconds;
wrapper CPU was 0.34375 seconds; known total CPU was **11.15625 seconds**.
Wall time was **19.25792900007218 seconds**. The original 120 CPU / 600 wall
seconds / 512 MiB / six-process limits were not renewed. The adapter retained
its exact 570-second deadline span and reported 18.8413219 wall seconds.

| Saved evidence under `experiments/v5-local-checks/installed-connected-service-01` | SHA-256 |
|---|---|
| `RESULT.json` | `cd06ef97fe9e893fda68ec69df54dbcaaab9eed3d93f454e6b56abdf5c9c96eb` |
| `evidence/actual-result.json` | `af3ddc12853fd178af6a471c845d16bbdcb6fa01c69c3b3c8df1573d056c5fe1` |
| `evidence/public-stderr.txt` | `fc28e65548d8da7917a820064e7bf3c29c52450e795f87dff06a858551f9773d` |

## Complete request-boundary recheck and smallest correction

The saved public plan has 107 selected sources / 1,202,336 bytes, including
the exact 21-file portable closure and selected built-in owner. Its schemas,
source roots, disjoint output paths, entry, parameter field sets and integer
limits align with `distribution._launch`, `client.launch.read_plan`, fixed
supervisor limits and `serve_advertised._parameters`. Entries 4,096 are within
the 1,024..32,768 bounds; the only identified static request violation is the
output-byte minimum. The remaining 100 CPU / 390 wall seconds / 384 MiB /
three-process public envelope fits the retained contracts.

The provider loopback endpoint/listen/bootstrap are in the fixed allowlist;
atomic workspace configuration is unchanged from the successfully created
fixture. Provider 120-second active lifetime and 150-second location ceiling,
10-second operation/health windows, TTL/reprovide relation and 16 reserved
commands within 24 match the documented constraints. Exact launch/boot/result
paths and cleanup assertions were also rechecked. This is source reasoning,
not evidence that downstream runtime necessarily succeeds.

The smallest prospective successor changes the test's output allowance to
64 MiB, uses fresh operation/evidence identities, and distinguishes planned
from actually started role counts. It needs no product rebuild, proof run,
RAM investigation, integrity weakening or larger time/CPU/process envelope.
Root must separately select any such fresh successor; this audit does not
restart the failed operation or relabel it as a pass.
