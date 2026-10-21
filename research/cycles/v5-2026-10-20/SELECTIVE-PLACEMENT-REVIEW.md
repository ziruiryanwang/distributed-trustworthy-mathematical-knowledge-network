# Independent selective-placement review

2026-10-21, core_growth. Reviewed SELECTIVE-PLACEMENT-CONTRACT SHA-256
`59ecc15abf6a2e7197fd83927794f5872637387042a2d00c4d0ecde34be2d3be` against
the actual current 114-source map, input `d3519be1`. Source inspection only:
no imports, tests, runtime, implementation or Git changes.

**GO for this mechanism, subject to the small implementation-blocking
clarifications below.** Do not start from the unclarified restart or two-slot
body-locator interpretation. No fundamental mathematical-acceptance or
placement-reachability defect was found in the bounded design.

## Necessary corrections before implementation selection

1. **Separate persistent service identity from live runtime authority.** A
   persisted service epoch identifies the operator/configuration/credential
   domain; it is not a reusable monotonic deadline or a resurrected service
   grant. Restart requires a fresh explicit local owner grant. For the first
   slice, existing publisher tokens become status-only after restart or their
   write expiry: they may read the exact bounded outcome while its generation
   remains retained, but cannot authorize new submissions. An identical old
   request returns its saved phase/status without executing, renewing retention,
   adding a ledger row or replenishing funding. Unfinished work is reconciled
   only by explicit owner selection, against its original reservation and
   retention end. Omit old-token new-write readoption in this first slice. This
   needs no second token protocol. Otherwise a lost reply/crash either destroys
   useful idempotent status or inadvertently revives expired write authority.
2. **Select the actual two-endpoint-compatible locator mode.** The selected
   `body_location/portable/location/maintained_roles.mjs` accepts up to four
   endpoints in V1, but line 62 explicitly limits body-enabled V2 index
   providers to one. Use the existing V1 index-only locator for the two
   generation slots. Direct committed group/body HTTP service still works;
   independent V2 body-location services remain separate. Do not silently feed
   two endpoints to the current V2 configuration or claim newly advertised body
   routes. No JavaScript protocol redesign is needed for this first mode.
3. **Correct the selected located-query source.** The current logical
   `v5/client/located_queries.py` resolves to
   `software/v5/pair_planning/client/located_queries.py`, SHA-256
   `4ffb84789deefb524f7f290b2a8879e3b9a1eadc0febf53ad2f5e1a3e168c66a`,
   not the table's predecessor path. Its route-subset checks and cumulative
   generation allocations still support the proposed mode unchanged.
4. **Specify the exact-custody short circuit before the remote-offer gate.**
   A fresh remote packet acquisition must be authorized by the existing bounded
   source offer. A successful bounded local commitment/readback may instead
   satisfy custody without fetching or fabricating a new offer. This matters
   for cross-store reconciliation after the source disappears. A saved intake
   phase alone is not that readback, and corruption is not a missing-object
   cache miss. Exact duplicate request status never performs either path.
5. **Make the horizon domain explicit:** accept only
   `now < requested_retention_end <= generation_retirement_not_before`, with
   admission still before its close time and within the token's permitted
   horizon. Use the documented clock-error policy before reclamation. A past
   retention end must not receive a positive new-placement acknowledgement.

Root explicitly agreed to corrections 1-3 while this review was being written.
The author can revise the still-unexecuted draft with its original hash retained
in a revision note, then root selects exact implementation ownership.

## Current source supports the proposed seam

The selected fingerprint implementation validates at most three paths and
enumerates at most eight goal alternatives. Its source observer returns STAR
when a path encounters a telescope parameter, including before missing-child
handling. The contract's no-structure-changing-reduction applicability condition
therefore supports its coordinate-wise coverage proof; it does not establish
general Lean applicability. The selected pair-planning adapter binds that
fingerprint profile into its namespace and derives the source feature from the
committed opening. The proposed cell must use the compiled feature ID, not a
publisher's claimed raw label.

The selected `terminal_i/evidence_network/transport.py` has a real direct
`declaration` path, genuine offer tracking, exact packet custody and no verifier
argument. No synthetic discovery result or mathematical grant is necessary.
`ModuleStore` and inherited packet transactions already have before-COMMIT
callbacks and exact readback. Packet storage is keyed by digest, so many exports
of one target module need not store its packet repeatedly.

The selected `instantiation_discovery/discovery/discovery_store.py` lacks the
new owner's callback: `admit` has its own 30-second budget, and both duplicate
and fresh branches COMMIT after only its internal `_guard`. A minimal successor
must invoke the intake owner's deadline/grant guard immediately before **both**
COMMIT paths. It must preserve transaction rollback and source-byte validation;
an outer asyncio timeout is not a substitute for the synchronous guard.

Current served workspaces hold an exclusive owner lock and immutable
configuration. Use the writable real Store, not the read-only projection. One
serialized intake slot plus bounded ordinary read service is adequate for this
scope. Existing publication commands already support publish/withdraw and a
fixed endpoint descriptor; the new runner must reserve dynamic cell capacity
up front and serialize commands with health/stop. It cannot inherit the old
fixed-route command calculation unchanged.

## Retention, security and coverage findings

Two generation slots, nondecreasing retirement times, a durable increasing
generation sequence and a floor for retired generations can bound active data
and obsolete request metadata. Advance the floor only after the relevant
generation's promises and handlers end; never reuse a snapshot identity. A
crash before the floor is durable must not permit root deletion followed by
recreation from an old token. The receipt ledger must retain original
reservations across partial database commits; reconciliation may finish exact
work, never reset its costs. A manager must count immutable index history and
both generation copies, not just live payload sums.

Actual long-run finite-disk operation still needs reclamation at explicitly
managed paths. A preserve-only initial implementation is safe only if it refuses
at its total quota; it must not be described as sustained rollover. No project
evidence or arbitrary peer-named path is eligible for this policy.

The two bootstrap roles are correctly distinct. A DHT descriptor is not write
permission; willing operators issue their own bounded grants. Source endpoint,
CA, egress and executable choices remain local. Current HTTP supports numeric
endpoint addresses, verified TLS and optional local server-name/CA adoption;
an IP endpoint using its IP as the TLS name requires a matching IP SAN. It does
not become authenticated HTTPS because the overlay uses Noise. The old HTTP
route allowlist and header parser do not themselves provide placement intake:
use an explicitly closed new handler/client, not a global write switch or an
Authorization-header assumption unsupported by current parsing. A fixed bounded
request envelope over the new verified-TLS route is sufficient; a new broad
authentication framework is not needed.

The reachability theorem is correctly conditional on selecting a provider that
actually holds the export and completing its authenticated intervals. Capping
r contacts per cell does **not** give provider-subset recall as the network
grows. Nor does a hot cell become selective because each individual store has
a quota. Keep REFINE_OR_INCOMPLETE and advertised/acknowledged/observed evidence
levels distinct. This feature removes mandatory global scanning from its
selected path; it does not solve universal large-network recall.

## Smallest coherent implementation group

Start with the actual bounded reserve/pull/index/acknowledge transaction, not a
new directory or a calculator. Approximately three new modules plus one narrow
successor are a reasonable first source group:

- A closed request/grant/outcome codec with independently derived cell binding.
- A bounded generation/request ledger with persistent reservations, idempotent
  status, the restart rule above, and exact locally issued live service grants.
- One serialized structural placement controller composing existing acquisition,
  custody readback, index admission and durable route intent. Keep reconciliation
  explicit and finite; no retry worker or unbounded queue.
- The discovery Store successor adding the before-COMMIT guard on both branches.

This first group exposes an owner-local callable transaction, enabling focused
failure/restart/dedup controls before network/service orchestration. Its honest
endpoint is `INDEXED_UNADVERTISED` until actual route dispatch; do not call it
completed remote placement. The next integration uses that same controller in
one closed submit/status TLS handler and the two-slot V1 advertised runner, not
a second competing workflow. The existing read-side custody/index protocols
and mathematical receivers should remain unchanged.

The genuinely new boundary is a durable, capability-budgeted result ordinary
publishers can request and later query, with exact evidence retained and
query-derived reachability. A manual operator silently editing index/routes,
or returning a DHT hint as custody ACK, would not satisfy it. The retained
three-role source-withdrawal example is a suitable later narrow integration;
no new certificate production or repeated mirror workload is justified.

These corrections support source implementation without further speculative
research. They do not establish net growth benefit, independent hosting,
successful physical reclamation or v5 release completion.
