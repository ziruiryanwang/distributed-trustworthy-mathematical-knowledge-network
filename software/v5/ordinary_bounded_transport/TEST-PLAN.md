# Bounded transport: prospective six-group control plan

2026-10-25. SOURCE ONLY, not an execution request or result. Root must select
the exact final provider/test/runtime pins after independent review. Existing
sparse/provider/custody/native campaigns are not repeated.

## Fixed scope

One test process verifies the selected sparse profile/installation manifests and
loads only thirteen exact unchanged Python support files plus the separately
pinned fresh `http_provider.py`. There is no package/native loader or Lean
runtime check. Empty in-memory namespace paths prevent unlisted lazy imports.
No candidate replaces files in the frozen package. All network endpoints are
loopback and use ephemeral OS-assigned ports. One fresh tiny inert custody
database contains one synthetic unproved preview; no existing database or
accepted mathematical state is opened. No Lean/compiler/prover is executed.

A single selected PowerShell 7 child generates a **fresh disposable test-only**
RSA certificate/key using the existing offline .NET CertificateRequest mechanism.
It writes only `disposable-tls/test-cert.pem` and `test-key.pem` under fresh output,
with localhost/IP SAN and one-day lifetime. It touches no certificate store,
operator identity or old test key. The key is not printed or included in a
public/source bundle. A normal verifying client trusts this exact test
certificate; no `CERT_NONE`/hostname-check bypass is used for positive TLS.
Root must pin the PowerShell binary as well as Python and source inputs.

## Decisive groups

| Group | Actual witness and observation |
|---|---|
| Pending TLS slot cap | With K=1, hold one raw client before TLS and connect a second into the OS queue. A transparent wrapper around the **real** `connect_accepted_socket` records each raw socket. Only one conversion may start until the first raw socket's actual `fileno` becomes -1. Stop while the second handshake remains pending and observe both sockets closed. |
| Failed handshakes pay | Two actual malformed TLS clients consume `max_requests=2` as accepted-attempt allowance without becoming HTTP requests. Observe each raw socket close, the listener stop accepting, and no third successful connection/conversion. |
| HTTP prompt stop | Open a real plaintext loopback client, send an incomplete HTTP header and enter a 60-second operation. `stop` must close it within the fixed two-second test bound, with actual client EOF/reset and raw-socket closure. |
| TLS prompt stop | Same incomplete-header trace after a genuine successfully verified TLS handshake. No waiting for the 60-second application timeout. |
| Ordinary positive route | Retrieve the exact synthetic preview from a real fresh `OrdinaryStore` over verified TLS through unchanged `dispatch` and `exchange`. Exact bytes/digest/count, one paid request, no mathematical acceptance. |
| Idle accept stop | Stop an idle listening provider while it awaits acceptance; observe no accepted raw socket, no owner task/listener left and prompt closure. |

The transport wrapper only observes and delegates the real conversion. It does
not fake a successful handshake, `Provider.status`, dispatch result, socket
closure or mathematical authority. The queued TCP connection is deliberately
not counted as an accepted application socket. Kernel listen backlog, external
flood resistance and global network availability are not measured.

## Finite resource envelope and failure handling

Proposed unchanged single-run ceiling: outer 60 seconds wall / 30 CPU seconds /
768 MiB private commitment / 4 processes / 1 MiB per log. The harness has its
own original 50-second wall / 25 CPU-second cooperative checks; the one key
generation child is limited to 12 seconds and included in the outer Job.
No nested native CPU is added. Each wait has a finite deadline, and tests use
six distinct short service lifetimes rather than a daemon or renewal.

Output is a fresh directory. The script saves a final `RESULT.json` on success
or failure, including actual per-group observations, transport counters,
certificate identity, cleanup errors and harness CPU. Root's existing runner
records whole-tree CPU, memory, wall and closure independently. Retain failed
results and generated test artifacts; no automatic retry, old-state mutation,
source rewrite or certificate-store cleanup occurs.

Provider closure must be observed, not inferred solely from counters. At every
group end: all observed accepted raw sockets have `fileno == -1`, no provider
listener/tasks remain, active count and reply reservation are zero. Client
writers are closed and awaited. On an unsuccessful explicit stop, the harness
does not silently rerun that stop as a fresh success; outer containment remains
the last resource boundary and an uncertain outcome remains a failure.
Fresh store population and TLS-context setup are inside that cleanup scope.
Cleanup errors remain in the report without replacing an earlier test/setup
exception; if cleanup alone fails, the run fails explicitly.

## Source review and selection boundary

The provider author has independently read the direct harness and identified the
setup-cleanup gap, corrected before execution. The final candidate provider is
`9288996fa1d4e737f500043cddfc1c7935d9b7830ac6638596b6f7f278f2add7`;
the direct harness is
`c80d8b43778360857a885303c63a96110c80a8c9beb5fcd885d3bf94654722de`.
Root must read the completed independent REVIEW and exact runtime/source pins
before selection. No runtime passing claim follows from this plan or source
inspection. A later assembly/public-wrapper control, if selected, is separate
and should test only that changed binding, not all historical routes.
