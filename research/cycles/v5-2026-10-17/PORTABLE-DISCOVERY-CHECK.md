# Actual portable descriptor-unavailability path

2026-10-17; read-only source investigation by `memo_tests_review`.
Canonical guard passed. No product source, runtime, test, proof or Git mutation.
Only this checkpoint is new.

## Decision

**Do not implement another descriptor-recovery wrapper or repeat its tests.**
The actual portable location selection already supports a narrowly classified
unavailable descriptor TCP connection while preserving the same ordinary client,
reader process, workflow, grant and accounting. The terminal adapter reaches
that existing path. Treating the older nonportable entry as this launch's entry
would produce a false missing-feature finding.

This is a source-level decision, not new runtime evidence. The new terminal
integration remains unexecuted and still requires genuine A plus exact launch
review. Its separate60-second contact-lifetime constraint remains unchanged.

## Exact chain

- `client/boot.py:140` places the pinned portable tree before the v5 tree in
  the actual import path. `terminal_strategy.node` selects
  `context.sources_portable/location`, with the launcher's source hashes.
- `portable_runtime/location/controller_services.py` starts that selected
  `node_entry_services.mjs`, using the portable V2 source map and explicit
  adopted workspace. The similarly named nonportable entry is not substituted.
- `node_entry_services.mjs:60` recognizes only actual `Error` values whose
  syscall is `connect` and code is ECONNREFUSED, EHOSTUNREACH, ENETUNREACH or
  ETIMEDOUT, or bounded nonempty AggregateErrors whose every member qualifies.
  It does not classify arbitrary error text, protocol/authentication failures,
  cancellation or exhausted budgets as ordinary unavailability.
- At `node_entry_services.mjs:163`, the descriptor-only recovery additionally
  requires un-aborted command/service/locator signals, a live locator and its
  unchanged deadline. It sends an IPC **OK** result containing
  DESCRIPTOR_UNAVAILABLE, exact ticket/peer, TCP_CONNECT_UNAVAILABLE and
  mathematical_acceptance=false. It does not replace the process or grant.
- `portable_runtime/location/controller.py:178` validates the original IPC
  sequence and OK status, then returns its result. Consequently the typed
  unavailability result does not enter its exception/kill branch.
- `portable_runtime/location/available_descriptor.py:25` validates the exact
  typed reply and original channel/deadline. It abandons the same ticket once,
  returns normally with authenticated_peer=None and global_complete=false, and
  never adopts a contact from an unavailable peer.
- `client/workspace_atomic.py:34` imports this available-descriptor helper.
  Its inherited `find`, at544, appends each result and adds contacts only for
  ADOPTED_ADVISORY_CONTACTS. The loop therefore proceeds to the next already
  routed peer after a typed unavailable result. Evidence/resilient clients
  inherit this method; neither needs a second recovery implementation.

## Same allowance, with a finite conditional opportunity

`WorkflowBudget.begin_descriptor` at125 charges one original descriptor request
and its serialized request bytes. `abandon_descriptor` at173 removes the pending
ticket via `_take` and charges its full reserved reply ceiling. No refund or
replacement ticket is issued. The location/search envelope was already prepaid
into acquisition by `delta/transport.py:197`. Node command/transport counters
and original service lifetime are likewise retained.

For the terminal adapter, one route returns at most four peers and at most four
descriptor attempts. Location reply capacity is2MiB+32768, including the2MiB
search allocation; four4096-byte abandoned descriptors fit within that original
capacity. If a later selected peer returns a valid descriptor before the
unchanged deadline, it can provide contacts for the same one-shot search. If no
valid contact survives, find reports NO_CONTACTS_IN_SELECTED_ROUTE_PLAN and the
terminal gate fails honestly; this does not establish mathematical absence.

Invalid descriptor bytes, wrong authenticated peer, malformed IPC, deadline or
budget exhaustion, cancellation and other unclassified errors remain fail-stop.
This narrow result is not general provider-outage recovery. It also does not
extend contact freshness during later A verification or semantic retrieval.

## Inspected portable identities

Paths below are relative to `software/v5`.

| Source | SHA-256 |
|---|---|
| portable_runtime/location/controller.py | 4dc0824d758e72fce591dbd9dddb9e487bcd0506cfaf4a71e894b0166b84e064 |
| portable_runtime/location/controller_services.py | 8591c49dba300a84d1e4b60f3ee1550be5eefd06b22867cf84d5b1080497e595 |
| portable_runtime/location/available_descriptor.py | d3b215f59c0b4745562fdc76339a53f22d0fa009932dfecbef4fecfff6743fba |
| portable_runtime/location/workflow.py | 0e0eafd11ff601ac069aa95e5b9de3608f3d77c7f9864cf5709d900d4c25c57e |
| portable_runtime/location/node_entry_services.mjs | 2eae8676469da5ef34fb88539d67774fc3dd115a6662cf24d169046e224fc346 |
| portable_runtime/location/maintained_roles.mjs | 9824559f55eca9b1e56786c14cbe090b74904d1786a915f124dc4101b0aa9683 |
| client/workspace_atomic.py | 01eefed1804ec5f296aebfcc12441dd283cd77c9bac8f8d5b02e8a4becc5e8c1 |

No claim about a newly observed sequence, sound mathematics, positive growth or
independent hosting follows from this read-only inspection.
