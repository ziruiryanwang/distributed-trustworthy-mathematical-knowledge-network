# Finite hosting source review

Status: source review PASS after two integrity corrections, 2026-09-21.
Reviewer: `package_contract_review`. This is not a runtime qualification or a
release approval. The reviewer did not execute/import product Python, tests,
Lean, a service, or a public CLI.

## Reviewed cut

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `software/py/hosting.py` | 17,811 | `80D574952FA62075AFC82F5C09D8AD536B3665073727D40F7F2F2B3AAF7B869E` |
| `software/tests/test_hosting.py` | 16,904 | `CE3C618F046A38146D256DB6EB373BEAA087788BD3BB1087DCAC9B8D1CB467E4` |
| `software/HOSTING.md` | 4,944 | `ECE04DA3A9FC9581A4A72038F6EF1CC52B2B1C6773D67076481EA984F5256065` |
| `software/manage.py` | 14,706 | `74C78824CFA95E13F62EAA538A4CD98897B3FC382A2061E62250D87DE9CEA11D` |

The integration was checked against the existing `supervise.py`,
`service_worker.py`, and service stop contract. The host command uses the existing
finite loopback worker and Windows Job supervisor; it adds no checker,
mathematical acceptance path, or independent supervision implementation.

## Contract checked

The explicit immutable grant binds one committed view/catalog, configuration,
session maxima and selected source/runtime pins. Fifteen input pins plus the
retained grant fit the existing sixteen-pin transport limit. A nonblocking owner
lock serializes hosting controllers. Each session's full maxima are reserved in
an exclusive fsynced slot before its directory or worker is created; no refund
or automatic authorization renewal occurs.

Before another slot or grant proceeds, every unfinished reservation requires
matching request/envelope evidence, a reaped direct child, an empty and closed
Job, and no cleanup/evidence uncertainty. A matching completed failure halts that
grant. A missing or inconsistent receipt blocks further hosting. A completed
successful slot is never deliberately repeated after controller restart.

The following review findings were corrected by the author:

- Success reconciliation now checks the supervisor's `event.json` file pin,
  in addition to the request/stdout pins and event I/O hashes.
- Restart now requires each completed slot's retained supervisor receipt to
  exist and hash to its terminal marker. This is bounded receipt integrity
  checking, not historical worker execution or a full replay of all output files.

The corrected suite contains **19 synthetic tests**: the original fourteen
reservation/restart/refusal/lock/schema cases, four negative receipt-integrity
cases, and one `manage.main` argument-routing smoke with `invoke_host` mocked.
Original corrupted receipt fixtures are retained by rename, not deleted.

## Qualification boundary

Test source inspection does not establish that the suite passes. The routing
smoke does not exercise the real `invoke_host`, process supervisor or listener.
Root must separately execute the bounded suite and qualify a real finite service,
expiry, retained receipts and no-repeat reinvocation before claiming runtime
hosting behavior.

This remains a cooperative-owner Windows/local-filesystem profile. Per-session
limits are not a hard aggregate controller CPU/disk quota. The 1 MiB evidence
charge is accounting, not reserved disk space. `SESSION_LIMIT` also covers CPU,
connection and byte exhaustion; it does not guarantee the advertised duration.
Readiness is historical. Inter-session listener gaps remain. No permanent daemon,
automatic crash recovery from missing evidence, independent-host availability,
useful mathematical growth, or public-release qualification is established here.
