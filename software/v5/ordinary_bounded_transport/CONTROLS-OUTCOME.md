# Bounded transport controls01: independent saved-output audit

2026-10-25. Reviewer: `concept_software_bridge`. Canonical guard PASS.

Disposition: **PASS for the six selected loopback transport controls**. The
saved evidence supports bounded pre-handshake ownership, finite failed-attempt
charging, prompt unfinished-client shutdown and an unchanged inert preview
exchange on the selected runtime. Root owns adoption. This is not assembly,
public-wrapper, mathematical acceptance, independent-host or full-v5 readiness.

Read-only saved JSON/text and file-hash inspection only: no product import,
test rerun, socket, native execution, state/database access or Git mutation.
The disposable private key was not read, copied or printed.

## Exact execution and bindings

Evidence root, relative to the canonical project:
`experiments/v5-local-checks/bounded-transport-controls01`.

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `a6475ecd1abb79121a1d7c2c596239e5f372ec3b1181ef7775d58ecf002cff43` |
| outer `RESULT.json` | `99e6d6698fd62527fbbc358adf6dfeb74d167aeb1e360c98a2c0b196b76962ba` |
| `suite/RESULT.json` | `8eb67066c8d4df244ec8ca73230bf1f4a5543b1780961b2baf90fe335b8cb08e` |
| `command/stdout.txt` | `b4f0260e9abac74e10307394251e658aeb8e2507c82bb2b5d23b90727085f376` |
| `command/command.json` | `4733525dad76deda3785453f8d9dc7fae11d37865bc201acf8f36798c4c38e27` |

All three source pins match both the immutable snapshots and current selected
source files; all 29 explicit runtime/support pins independently rehash correctly.
The original prospective selection has the same digest as the saved selection
and outer result. Selected provider is
`9288996fa1d4e737f500043cddfc1c7935d9b7830ac6638596b6f7f278f2add7`;
selected harness is
`c80d8b43778360857a885303c63a96110c80a8c9beb5fcd885d3bf94654722de`.
These equal the reviewed prelaunch bytes.

The actual command argv equals the selection after expanding only snapshot/output
placeholders, uses isolated Python `-I -S -B`, and selects the pinned candidate,
sparse package/profile and PowerShell binary. The command cwd is canonical.
Command limits equal the outer result's limits. Stdout is exactly the suite
report after Windows CRLF normalization; the one-byte length difference is its
final newline encoding. Command stderr and disposable-certificate stderr are
empty. There is no missing group or success inferred solely from process exit.

## Actual observations and assertion support

The complete selected harness was read. Its observation wrapper delegates to
the real `loop.connect_accepted_socket`; it records actual socket objects and
checks prior unclosed sockets before each conversion. It does not fabricate
provider counters, successful TLS, dispatch replies or closure. Its common stop
assertion requires no listener, no tracked tasks, every observed raw socket's
`fileno() == -1`, zero active records and zero reserved reply bytes. Six groups
are appended only after their specific assertions succeed.

| Group | Actual retained witness |
|---|---|
| Pending TLS, K=1 | While the first raw client stalls, the second TCP client waits in the OS queue: one accepted attempt, one handshake, zero HTTP requests. After closing the first, the second conversion starts with zero earlier raw sockets open; the first has `fileno == -1`. Stop cancels the second handshake; both actual sockets close. Stop takes 0.015497 s. |
| Failed handshakes pay | Two malformed TLS clients yield two real `SSLError` events, two paid accepted attempts, two handshake failures and zero HTTP requests. The listener is no longer accepting and admission is exhausted. The executed third-connection assertion refuses successful connection/conversion; only two sockets were observed, both closed. |
| Incomplete HTTP header | A real handler has begun under `operation_ms=60000`. Stop takes 0.000303 s, not the application timeout; actual client EOF/reset is required before the group is recorded. The one observed raw socket closes. |
| Incomplete TLS header | The same trace follows a genuinely successful verified TLS handshake. Stop takes 0.000465 s with actual client EOF/reset and raw closure. |
| Unchanged ordinary preview | Real `exchange`/dispatch retrieves exactly 437 bytes over verified TLS from the fresh inert store. SHA-256 is `cb1381c1e16b7586ed716838e4878d33986451c30ba4429b86327623e4e8b287`; one request and exactly 437 reply bytes are charged. Parsed acceptance remains false. |
| Idle accept stop | No socket is accepted; stop takes 0.000192 s and leaves no listener/task or active/reserved state. |

Across all groups, all seven observed accepted raw sockets end at `fileno == -1`.
No conversion begins with an earlier observed raw socket still open. The common
stop limit was two seconds, and no explicit failed stop was retried into a pass.
The first group's reset/cancellation and second group's TLS failures are the
intended transport events, not failed mathematical claims or hidden suite failures.

The positive case's pre-stop snapshot briefly reports one cleanup-pending record
even after raw closure; final status is zero. This is consistent with retaining
the slot until both task completion and raw closure, not evidence of a leaked
connection or permission to ignore outstanding work.

Independent byte checking of `SYNTHETIC-PREVIEW.json` after removing its single
saved LF reproduces the exact 437-byte reply digest. Its name is explicitly
`SyntheticTransportUnprovedClaim`; neither storage nor transport makes it a
warrant. No owner catalog, compiler, theorem admission or existing state is used.

The freshly generated public test certificate rehashes to
`369f0084ffc94f7d3eeddc0400ea62cf1bc4dc3a9046a8aabff305d2b2dc5b6b`.
Generator output is the expected sole creation marker, exit is zero and the
child is reaped. The source uses an output-local one-day certificate with SAN
and server-auth extensions, a normal verifying client context and no certificate
store modification; there is no `CERT_NONE` or hostname-check bypass. The
disposable identity is not an operator identity or public distribution asset.

## Inclusive cost and closure

The outer result reports `COMMAND_EXITED_ZERO_AND_CLOSED`, direct child reaped,
Job closed, zero final active processes, no termination request and no cleanup
errors. Suite cleanup errors are also empty. Cumulative process count is four;
this is not a measured peak-concurrency statistic.

Known measured CPU is **1.375 seconds**: 1.171875 inclusive Job CPU plus 0.203125
outer-wrapper CPU. Do not add the nested 0.3125 harness CPU or 0.015625 supervision
subinterval again. Total outer wall is **3.2574433 seconds**; command wall through
cleanup is 3.2139348 seconds. Peak Job private commitment is 58,191,872 bytes.
The one disposable certificate child is included, not an uncharged external step.

These fit the original 60-wall/30-CPU-second, 768-MiB, four-active-process envelope
and 1-MiB-per-log limits. Observed stdout is 6,234 bytes; stderr is zero. No retry,
allowance renewal or broader campaign occurred.

## Limits and next boundary

This is finite loopback evidence on the selected Python 3.14.6/OpenSSL runtime,
supporting the separately reviewed ownership invariant. It is not a proof for
every scheduler/cancellation interleaving, arbitrary runtime failure, OS queue
size, network saturation, client fairness, global availability or exploit absence.
The short measured stop times are observations, not universal latency promises.
Resource containment is not a hostile-code sandbox.

Assembly and public-wrapper integration require their own exact selection and
saved outcomes; this audit does not borrow them from direct Provider tests.
The static `source_only_until_root_selection` field in the suite does not erase
the actual recorded root selection, nor does its success imply automatic adoption.
Preserve this used source/evidence; no unchanged test rerun is recommended.
