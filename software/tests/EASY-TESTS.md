# Easy local network tests

These tests need one Windows machine and the project's selected Python runtime,
not another computer, a VM, a Lean build, a network account or an API key. They
operate on synthetic inert packages and test transport, not mathematical truth.
The independent Lean proof/reuse results remain separate evidence.

Run from a development checkout containing `software/tests` and `software/py`.
The immutable source-package02 release archive does not include the test suite.
Use fresh two-digit run suffixes: an existing allocation is refused, not erased.

```powershell
# Example fresh run names; choose other unused suffixes if these already exist.
& 'D:\Python314\python.exe' -B -E -s -S 'software/tests/run_transport.py' --run transport-03
& 'D:\Python314\python.exe' -B -E -s -S 'software/tests/run_easy_network.py' --run local-network-smoke-03
```

The first command runs 18 framing, corruption, refusal and real-loopback
controls. The second runs three additional scenarios:

- Receive bytes from one child-process supplier, let it stop normally, and
  receive the same bytes from another supplier built from the received copy.
- Drop a real socket transfer before its advertised body finishes; require
  refusal and connection closure, with partial data preserved.
- Send an invalid Host header, then a valid request; require rejection of the
  first, service of the second and natural shutdown at the connection quota.

The existing Windows Job supervisor bounds each suite to 60 wall seconds,
512 MiB private commit and eight active processes. CPU ceilings are 60 seconds
for the original suite and 30 seconds for the three new tests. Supplier workers
have 10-second sessions and two-connection quotas; forced cleanup cannot pass
as natural shutdown. Parent preparation and final reporting are outside the
worker Job. Limits are not a complete machine/agent cost measurement.

Results, stdout/stderr, request/response hashes and quiescence receipts are kept
under `software/qualification/<run-name>`. New smoke runs also snapshot their
test/product sources and retain each supplier's command, output and lifecycle.
Never delete a failed run to reuse its name or treat receipt absence as success.

These are actual localhost sockets and, in the supplier cases, separate OS
processes. They do not model independent physical hosts, arbitrary packet loss,
all hostile traffic, mathematical admission, or long-term availability. Passing
them is useful local evidence without making those broader claims.
