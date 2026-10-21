# Installed boundary01: request rejected before owner execution

Root retained this tool-captured failure; the launcher did not write its normal
Job result because `read_plan` failed before the child supervisor was entered.

- Release: `769506990ea10be5c6ce812e5cfd457922f4955ad4831bcdbc9d7a9ec9561108`.
- Request: `9f991f1be08f59489e31736e222c4084f9e5c740db7f029429d8e35771284228`.
- Tool command chunk `bf5fc5`, exit code 1, reported wall 5.126559 seconds.
- Final traceback: `client/launch.py:141`, `read_plan`,
  `ValueError: CLIENT_OUTPUT_LIMITS`.
- Failed predicate: `SOURCE_TOTAL <= output["bytes"] <= 2*1024**3`.
  The retained launcher sets `SOURCE_TOTAL = 64*1024**2`; our request chose
  `32*1024**2`. The 1,024-entry bound was legal.
- No owner, mathematical issuer, Job experiment, native checker or network
  operation was reached. No CPU measurement is available for this outer failure;
  do not assign it zero cost or invent an enclosing Job pass.
- The staged `integration-operations/installed-discovery-boundary-01-request`
  directory and request/source remain untouched. The intended run and commons
  paths were not created. No package defect was demonstrated.

Both root and source review missed the existing output floor. The correction is
one fresh request selected by `Select-DiscoveryInstalled02.ps1`: change only its
name, structural workspace target and output-byte ceiling to 64 MiB, retaining
the same adapter, package, time/process/memory limits, owner data and semantics.
Output bytes are a filesystem allowance, not a request for more RAM. No product
rebuild or component test repetition is warranted by this request error.
