# Remote-placement integration: source composition review

2026-10-21, core_release. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**Final disposition: PASS_SOURCE_COMPOSITION_FOR_EXACT_BOUNDED_INTEGRATION,
not a runtime or release pass.** The initial source was held for three
deterministic adapter setup corrections and one scheduling-sensitive assertion.
All four were reported and corrected before execution; the final exact source
was reread as described below.

I authored the new placement wire, so this is not an independent review of that
wire. This assignment reviews root's independently authored integration and
selection preparer against `PLACEMENT-NETWORK-INTEGRATION-PLAN.md`, including
their composition with existing selected APIs. The separate adaptive_audit
source review owns the product-wire/service judgment. No product import,
execution, network, build, proof, test, Git mutation or root-file edit occurred.

## Initial exact source

| Source | SHA-256 |
|---|---|
| `software/v5/placement_network/integration.py` | `5940798411747998413d404753738111844ced28d1f382c3ee05eaa9c842158b` |
| `research/cycles/v5-2026-10-20/Select-PlacementNetworkIntegration01.ps1` | `076d75cc357a2691e722bafe713c556877241b7cdbc562043a879cb7c03e670a` |

The exact SDK map is the current 114-entry map
`d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0`,
2805479 bytes. Relevant APIs were read at their selected physical paths, not
inferred from older logical predecessors. SHA/JSON inspection and arithmetic
are read-only checks, not execution of the proposed workload.

## Concrete findings

1. **Three request reservations exceed the supplied client outgoing allowance.**
   The initial `outgoing_bytes=65536` is smaller than `3*25600=76800` for submit,
   identical replay and status. The third call deterministically refuses
   `CLIENT_BUDGET`. Use the exact three-request allowance; do not reduce wire
   accounting or renew the grant after a failed call. Incoming needs
   `3*90112=270336` bytes and the original 1 MiB already sufficed.
2. **Structural acquisition requested invalid zero limits.** Selected
   `transport/receipt_client.py` requires positive minimum 1 for
   `verify_attempts`, `verification_input_bytes` and `worker_cpu_seconds`.
   These may be valid finite unused `1,1,1` caps with explicit zero-used checks;
   the separate genuine receipt receiver still owns actual admission. Do not
   change the frozen budget class for this adapter.
3. **Random port acquisition order is not canonical egress-policy order.**
   `test_endpoints` must be sorted unique `(host,port)` pairs. Iterating
   `all_ports.values()` does not ensure sorted ephemeral ports. Sort the values
   when building the policy, preserving the role-to-port map separately.
4. **Whole provider-status equality includes transient cleanup state.**
   `active=len(tasks)` may legitimately change after EOF while a prior handler
   completes closure. Compare stable request/byte/failure/refusal counters to
   establish no repeated fetch; separately require successful provider closure.
   Keep unchanged placement funding/custody/index/route-row assertions.

## Composition supported by source

The scenario uses original supplier A, initially empty custodian B, and fresh
reader R with only two locator children. A has an HTTP custody provider but no
locator. R's existing `reader` role has server-mode DHT enabled, can hold B's
ordinary announcement and is not an index-provider role. B alone registers the
descriptor handler and publishes its dynamically derived cell. Startup means
listening/dial attempted, not routing readiness; existing provide/find queries
use their bounded routing barriers. The actual positive dispatch assertion
and subsequent real discovery, not a sleep or startup label, decide success.

B uses the actual `PlacementService.open/start/issue_token/close` and one owned
Workspace; the submitted token is fixed to A's explicit source and B's intake
endpoint. Replay and status use the same canonical manifest/request identity.
The local receipt remains `INDEXED_UNADVERTISED`; the separate route observation
must be `HINT_DISPATCHED_UNACKNOWLEDGED` with positive dispatch writes. Neither
becomes mathematical authority or a remote DHT acknowledgement.

A's HTTP service and Workspace close before `discover()` is called. That
function receives a fresh R Workspace, R locator, independently generated
closed binary-congruence goal, policy, deadline and report sink. It receives
no answer module ID/name, manifest, packet pin or snapshot. The fixed query
helper constructs the formal type and features without fixture reads. Its
root/fixture independence is an audited function/data-flow boundary inside a
trusted process, not a hostile-process information-flow sandbox.

The descriptor contact originates in actual located-peer processing with the
existing authenticated private Node channel. Search uses the returned snapshot
offer and verified page. The selected record supplies the export locator;
the retrieved opening's full type/universes are matched against the independent
goal. Packet identity is learned from the same provider's typed offer, then
exact bytes are acquired and retained. The later equality to A's packet is a
postcondition, not an input to selection. No private index row is fed to R.

After all network services close, R's acquired receipt is passed to the real
`ReceiptVerifier.receive` once with an explicitly created temporary trust
domain, selected checker executable and source/runtime pins. `describe` must
bind the actual same-call journal and module; `open_group` checks the acquired
opening against that live handle and requires the discovered declaration in
the returned group. Historical bundle labels cannot mint a handle. Verifier
closure and trust withdrawal are required. No new proof, native-delta check,
frontend authoring or synthetic issuer is involved.

## Source and resource accounting

- Physical source snapshot: 114 current map files, one selected runner,
  eight qualified product replacements/additions, two owner helpers,
  three network modules and the integration adapter: **129**.
- Product logical staging: 114, four replacements, four added local-placement
  modules and three added network modules: **121**, plus two owner helpers.
- Explicit outer runtime pins: 18 Python runtime files, supervisor manifest,
  checker executable, three fixture files, exact current map and owner input:
  **25**. This is not a claim of hermetic OS/DLL closure.
- Receiver pin map: 100 original Python modules, seven new product Python
  modules, two owner helpers, 18 Python runtime files and checker executable:
  **128**, exactly the selected receiver's allowed maximum. Additional Python
  files cannot be silently inserted into that map without revisiting the cap.
- Existing Node adoption separately verifies its 5896-file runtime/overlay
  closure and selected JS sources before/after use. It is not an unpinned
  executable merely because those transitive rows are absent from the outer
  25 directly named runtime pins.

The selector refuses preexisting run/input/selection paths, verifies exact
inputs, snapshots source hashes and writes only new owner selection files.
It does not execute the adapter. The current map's exact 2805479-byte bound
avoids the already diagnosed predecessor map-size failure.

The prospective outer allocation remains 150 CPU seconds, 300 wall seconds,
512 MiB, six active processes, and 1 MiB stdout/stderr. The network roles stop
before the single receipt verification. Original finite service, Node, search,
acquisition and receiver allowances remain distinct; nested CPU must not be
added again to the same measured outer Job CPU. No allowance is renewed after
an uncertain action, no old campaign is rerun, and no full distribution is copied.

## Evidence boundary

Any execution still requires root's exact reviewed-source selection and the
separate product/control gates. A successful future outcome would establish
one real same-PC loopback remote-placement/replay/source-withdrawal/goal-only
discovery/receipt-admission composition. It would not establish public TLS,
independent hosting, arbitrary theorem search, whole-network completeness,
full-cost growth, new theorem authorship, service rollover or final v5 release.

## Corrected-source disposition

Root's corrected adapter is **31253 bytes**, SHA-256
`d71925cd57b2d3b438081bf340984bca272a409b89fec50931ea6fd86c449305`.
The selector remains **8133 bytes**, SHA-256
`076d75cc357a2691e722bafe713c556877241b7cdbc562043a879cb7c03e670a`.

I reread the final adapter, checked its hash and verified:

- Client allowances are exactly `3*90112` incoming and `3*25600` outgoing.
- Structural acquisition has valid `1,1,1` verification caps and explicitly
  requires all three corresponding usage counters to remain zero.
- Loopback endpoint policy iterates `sorted(all_ports.values())`.
- Duplicate no-fetch comparison retains only cumulative `requests`,
  `request_bytes`, `reply_bytes`, `header_bytes`, `failures`, `refused`;
  successful source closure is still separately required.

No further source-composition blocker was found in the assigned scope. This
permits root to consider the exact source for its separately recorded finite
selection once the independent product/control gates are satisfied. It is not
authority to launch here, a prediction that the DHT returns the desired result,
or permission to repeat a failed campaign. All initial findings remain above
rather than being erased from the review trace.
