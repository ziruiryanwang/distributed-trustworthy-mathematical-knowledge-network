# Easy network checks: source and retained-result review

2026-09-22. Independent read-only PowerShell/JSON/source/hash review; reviewer
ran no Python, product imports, Lean, SQL or tests. The review note is the only
reviewer write. Previously delivered archives remain unchanged.

## Three-case smoke: cleared for bounded execution

Reviewed `run_easy_network.py`, the complete `test_local_network_smoke.py`, reused
fixture/runner sources and relevant transport/Job supervision paths. No blocking
flaw found for this limited test scope. Reviewed SHA-256 identities:

- Runner: `2C49E0624799F6E9655FF8111E9592DAA18642A7CE03B3C33AEB10814380801E`.
- Tests: `C2FF060939286565136984263C36CE1D503D687BE0F585132AA3E2FD70BB275A`
  (8,769 bytes, including the hidden-window creation flag).

The first reviewer clearance accidentally paired the post-change source read
with the earlier `132B7D0867BFB00C497E967D2A996A0576E8CCB7F870D64E2E861F7AAD7277DA`
pin. Root's prelaunch guard refused before creating an allocation or child.
An independent in-memory reversal of only the 93-byte `CREATE_NO_WINDOW` change
reproduced that earlier 8,676-byte digest exactly. Current source was reread and
rehash-confirmed; this is a corrected reviewer bookkeeping error, not a repaired
test result. No historical failure was erased or rerun.

The explicit `load_tests` selects exactly three cases, excluding inherited tests.
The worker refuses skips, failures, wrong counts and selected checker/codec/SQL
imports. Supplier children use hidden windows and inherit the outer process Job;
fixed fixture paths and finite server limits introduce no remote-host dependency.
Natural supplier exit is asserted before successful teardown: forced cleanup
cannot convert a timeout into a passing test. The truncated-response thread has
bounded socket waits, retained failure observations and an asserted join.

The intended discriminators are acquired-byte re-serving after the first
supplier stops; real-socket truncation refusal; and invalid Host rejection
followed by valid discovery. Synthetic CBOR and coherent advertised metadata
are deliberately not mathematical acceptance. Source review is not an executed
smoke result. Scope excludes independent machines, routing/TLS, OS-level hostile
code isolation, meaningful mathematical reuse and scalability.

The fresh-run runner retains source snapshots and binds original source pins at
launch. Its existing outer supervisor supplies 60-second wall, 30-second Job CPU,
512-MiB Job memory and eight-active-process bounds. This is not a hard transient
disk quota. The proof of no native work here is the selected source path plus
recorded zero-stage/import checks, not the service's descriptive boolean alone.

## Existing transport suite: fresh transport-02 outcome PASS

Independently inspected `qualification/transport-02/result.json`, command,
request, event, both streams and supervisor receipt. Recomputed all ten
launch/source pins and all five retained output pins without mismatch; the
receipt pin set equals launch. Event request/response hashes match actual bytes.
The verbose stream names all 18 tests, and the result records 18 passed, zero
errors, failures or skips, and zero native stages.

The receipt records `TRANSPORT_COMPLETE`, exit zero, direct child reaped, final
active count zero and Job closed, with no cleanup error or termination request.
The recorded child PID was absent when checked. Job CPU was 0.296875 seconds;
receipt wall was 0.7018594000255689 seconds; peak Job private commitment was
37,101,568 bytes. Two lifetime Job processes is not evidence of two host machines.

- Result SHA-256: `A47311365EED4DEB1996E363DAA4FB727FC013EF02AE20435533E2F27AB485C8`.
- Receipt SHA-256: `869DEA36BC13C004B77FC387AAB644F43D4D9158A4983B5A56FC1097FC07A13A`.

This fresh result supports the named transport/framing/schema/refusal controls
and an existing real-loopback test. It neither reruns mathematical checking nor
qualifies the new three-case smoke before that separate run occurs.

## Smoke01 failure and narrowly corrected smoke02 source clearance

The first executed smoke remains **FAILED: one failure, two passes**. Its first
supplier completed two responses, exited zero naturally at its request quota,
and was reaped. The subsequent offline probe returned `TRANSFER_TIMEOUT`, while
the test demanded only `PEER_UNAVAILABLE`; therefore supplier B was never
started. The real-socket truncation and hostile-Host cases passed. This failed
run does not establish completed supplier turnover.

Independently verified all nine frozen source-snapshot pins and five recorded
output pins. Its receipt is `TRANSPORT_NONZERO_EXIT`, worker exit one, direct
child reaped, final active count zero, Job closed, no terminated processes and
no termination request. Retained lifecycle reports independently show both
started suppliers exiting zero without cleanup or forced termination. Job CPU
was 0.359375 seconds and receipt wall 2.6469408000120893 seconds. The truncation
thread report records client close, no error and no surviving thread.

Compared the complete current test against the frozen smoke01 snapshot. The
only delta admits the two documented unavailable error codes and retains the
observed code, no-returned-catalog fact and supplier exit code. The original
natural-exit assertion remains mandatory. `peer_service._get` explicitly maps
connect `socket.timeout` to `TRANSFER_TIMEOUT` and other connect `OSError` to
`PEER_UNAVAILABLE`; demanding just one was an over-specific test assumption.
The revised test does not accept a successful catalog or a still-running
supplier, change product code, relax resource limits or retroactively pass
smoke01.

Fresh smoke02 source execution is cleared with test SHA-256
`613E7A439ED1FE3A4F3CEF9253C66E96DC3D0F192D48BE80B47E168B02E1781C`.
Runner SHA-256 remains `2C49E0624799F6E9655FF8111E9592DAA18642A7CE03B3C33AEB10814380801E`.
This renewed clearance is still source review, not a smoke02 outcome. All
smoke01 sources, fixture reports and failure evidence remain preserved.

## Fresh smoke02 outcome PASS

The separately executed `local-network-smoke-02` passed all three named tests
with zero errors, failures, skips, selected forbidden imports or native stages.
Recomputed all eleven source/config/interpreter pins, nine source snapshots and
five output pins without mismatch; receipt/launch pin sets and event I/O bindings
agree. Both historical smoke01 failure and its source cut remain unchanged.

All three supplier lifecycles record natural exit zero, no cleanup path and no
forced termination. Suppliers A and B each served two connections/two responses;
A's subsequent offline probe returned `TRANSFER_TIMEOUT`, no catalog, with its
exit code still zero. The original package's three files equal both acquired
copies byte-for-byte (six direct comparisons). A and B served identical 628-byte
bundles, SHA-256
`0A8CBF028457CA0EAE0E692846371725CDA1E73D6610E81F9D9E74CCBBE83732`.
Source and execution order establish that B used the first acquired package
after A had exited, not a concurrently available original supplier.

The truncated HTTP body is 627 bytes; its client closed, responder thread ended
and no responder errors occurred. The hostile-Host request received zero bytes;
the same supplier then provided valid discovery, reporting two connections,
one response and `HTTP_PROFILE_REFUSED` as its last error. All observed
root/supplier PIDs were absent at audit time.

The supervisor records `TRANSPORT_COMPLETE`, exit zero, direct child reaped,
final active count zero, Job closed and no termination or cleanup error. Job CPU
was 0.515625 seconds; receipt wall was 2.9070863000233658 seconds; peak Job private
commitment was 55,250,944 bytes. Eight lifetime processes, with a sampled peak of
four active, is a process-tree observation on one host, not eight suppliers or
independent hosts. Disjoint Job CPU across transport02 and both smoke attempts
is 1.171875 seconds; this excludes wrapper, review and earlier project work.

- Smoke02 result SHA-256: `0D7233E2A766DE63F8FC16FA77CBCAC258E18C1C4FC9141320597EDAF8F91DBC`.
- Smoke02 receipt SHA-256: `80C20CEC474CD3078797D443CAD5671369AF33271E56DE45DEFE5B01399E81FC`.

This supplies actual local process-turnover and refusal evidence under the
stated synthetic-byte profile, not new mathematical or separate-host evidence.
