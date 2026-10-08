# Independent preimplementation review: remote transport v1

Reviewed 2026-09-23 against the selected editable
`product-local/integrated-frontend-source-03` (not historical `software/` or a
used installation). Initial contract SHA-256:
`456e9166f3c004153dab21f00aba03003d8231e2f645b0a457e79fb810d5b899`.
Root's source-grounded clarifications were reviewed at SHA-256
`cd294c889db4870a4710903b32261befbef2f26a98f30b9ac265520d6996d43f7`.
The two final wording corrections were reviewed at SHA-256
`f9e6f36b57886c258690985af811813825ecb657751b3b86eba6046dd60f5afd`.
No product code, service, key material or network endpoint was changed or
used by this audit.

## Verdict

**Dispatch-ready for a new, separately allocated implementation
cut, not qualified software.** The core choice—explicit IPv4 endpoints and
exact leaf-DER-pinned TLS 1.3 before any HTTP—fits the current peer and owner
boundaries. Configuration version 5 with SQLite physical schema 4 is coherent;
the latter is checked by `py/storage.py:199–225`. The clauses below are exact
implementation obligations, not reasons for another general architecture
loop. The amended contract now states the three raw network-entry key sets
and the actual time boundary for key/view mutation checks. The source-derived
tests can be frozen against those terms.

## Decision-critical seams

1. **Strict shape and secret boundary.** Current `manage.py:40–115` produces
   schema-4 loopback peers; `py/node.py:53–100` and
   `py/domains.py:54–58` strictly reject any other config version. The revised
   contract now pins a normalized TLS listener to exactly
   `{profile,bind_host,port,certificate,private_key,certificate_sha256}` with
   exact `{path,bytes,sha256}` PEM-file records and a *separate* leaf-DER
   digest. Conversion of input `certificate_file`/`private_key_file` must
   precede state creation. `load_config` may check locator shape but must not
   read identity bytes; only configure and the selected service worker do so.
   Validate every path component for reparse/alternate-stream hazards before
   canonicalization, rather than merely resolving away an alias. For exact
   parser tests, the contract now states raw entry key sets: TLS peer
   `{profile,host,port,certificate_sha256}`, loopback peer
   `{profile,host,port}` with host exactly `127.0.0.1`, and TLS listener
   `{profile,bind_host,port,certificate_file,private_key_file}`.

2. **Pin before first request, per connection.** Current
   `py/peer_service.py:109–146` connects to `127.0.0.1` and sends HTTP at line
   123. The TLS branch must instead receive the entire endpoint (currently
   `py/peer_node.py:185–214` passes only port), connect only to its numeric
   configured IPv4 address, complete deadline-bounded TLS 1.3, check selected
   ALPN and exact leaf DER digest, *then* reach `_send`. A failed pin cannot
   fall back to the loopback branch. `peer_find` may call `_get` twice; its
   bounded event must contain two separate public endpoint/phase records,
   initialized `pin_verified:false,http_request_started:false`. These flags
   and the socket-double test must establish the ordering per attempt, not
   infer it from an aggregate success. The added event shape is now explicit
   in the contract.

3. **Fixed TLS failures must be fixed before broad wrappers.** Without local
   mapping, `ssl.SSLError` (an `OSError`) could reach raw string emitters at
   `py/peer_node.py:150–154`, `py/node.py:393–396,439–446`,
   `py/service_worker.py:139–143`, and `manage.py:259–263` (or retained
   stderr). The amended contract correctly requires reduction at TLS/config
   helpers to fixed codes and no raw exception text/events. Include post-
   handshake TLS I/O faults in that review; existing `_recv/_send` at
   `py/peer_service.py:38–60` currently collapse generic `OSError` to
   `PEER_UNAVAILABLE`. An outer worker/supervisor failure remains unknown,
   never fabricated into a terminal TLS refusal.

4. **Host peer refusal versus local fatal fault.** Current
   `py/peer_service.py:257–306` increments accepted connections before
   request parsing but catches every wire/IO fault as `last_error` and
   continues. Current `py/hosting.py:158–203` regards any `last_error` as a
   failed slot and only accepts loopback bind identity. TLS needs the amended
   split: bad handshakes/remote syntax are charged peer refusals and may be
   followed by a valid client in the same finite session; missing/changed
   *local* selected view bytes, identity faults, quota/supervisor uncertainty
   are `fatal_error` and halt. A post-readiness fatal fault must not be
   reported as a normal successful owner session. For schema-2 TLS grants,
   derive `{profile,bind_host,port,certificate_sha256}` from the immutable
   listener in current config and compare exact readiness and terminal
   observations; hosting never reopens a private key. Preserve the schema-1
   legacy `last_error` rule. `py/hosting.py:66–84,120–138,251–300` shows the
   strict grant, request, journal and precharge points.

5. **Finite resource and native-checking boundaries are compatible.** Existing
   client outer envelope is 120 seconds/1024 MiB (`manage.py:139–145`), owner
   service is at most 360 seconds with 120 CPU seconds/256 MiB and 128
   connections (`manage.py:173–184`), and the service clock starts before
   view authentication (`py/service_worker.py:67–119`). The TLS handshake must
   fit inside both the per-connection 30-second and remaining service clocks.
   `py/peer_service.py:65–92,187–197` counts plaintext HTTP, not TLS record or
   handshake bytes; the contract correctly disclaims a hard link-byte quota.
   `py/hosting.py:25–26,322–324` has 15 input pins and the grant adds one,
   reaching `py/supervise.py:122`'s 16-pin ceiling: keep first-slice helpers
   inside pinned `peer_service.py` and never add a private-key file to generic
   supervisor pins. `py/peer_node.py:211–228` still performs inert package
   checking after transfer; fresh Lean admission remains a distinct receiver
   operation. TLS/acquisition alone cannot satisfy the mathematical gate.

## Final wording resolution and gate boundary

Contract acceptance gate 3 now locates a key-change refusal before TLS context
setup or the next session, and selected-view faults at their local read/recheck
points. It explicitly excludes instantaneous revocation of an already loaded
TLS context following a mid-session disk-key change. The strict raw shapes now
appear at contract lines 84–88. A post-readiness local fatal must halt and fail
owner hosting, not be classified as an expected peer refusal. These corrections
close the review's two remaining textual conditions; implementation and the
predeclared gates still need their own evidence.

Passing this review authorizes only implementation and the predeclared local
tests in the contract. It does **not** establish TLS qualification, independent
host operation, long-lived key rotation, Internet availability, efficient
knowledge growth, licensing, or the full release goal.
