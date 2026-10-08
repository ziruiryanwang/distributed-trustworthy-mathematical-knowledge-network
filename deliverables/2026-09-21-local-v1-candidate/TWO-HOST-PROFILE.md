# Proposed two-host operator profile — not yet executed

This profile specifies a concrete next deployment test for the unchanged
loopback-only application. No second host was available for qualification.
These instructions neither configure SSH nor authorize remote connections.
Operators must supply their own authorized hosts, accounts, verified host keys,
compatible runtimes and local storage. No central service is required.

## Topology and trust

| Host | Its own application listener | Its configured receiving alias | Local SSH forward |
| --- | --- | --- | --- |
| Alpha | 127.0.0.1:43111 | beta=43112 | 43112 to Beta's 43112 |
| Beta | 127.0.0.1:43112 | alpha=43111 | 43111 to Alpha's 43111 |

Each host independently extracts/verifies the candidate, builds support,
configures fresh state/scratch and initializes its own node. The archive's
QUICKSTART commands illustrate the two configurations; run the corresponding
configuration on each host, not both against one shared database. Keep local
handles, database and scratch evidence local. Use the same selected foundation
and compatible supported runtime profile; remote receipt copies are not trust.

The same local/remote application port is intentional: the HTTP profile checks
the exact `Host: 127.0.0.1:<server-port>` field. A differently numbered local
forward is not compatible with this profile. Ports must be free before launch.

After independently authenticating the SSH host keys, an operator can establish
the corresponding forward. These commands contain placeholders, not known hosts:

```powershell
# On Alpha: its local beta alias reaches Beta's loopback application.
ssh -N -T -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=yes -L 127.0.0.1:43112:127.0.0.1:43112 BETA_ACCOUNT@BETA_HOST

# On Beta: its local alpha alias reaches Alpha's loopback application.
ssh -N -T -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=yes -L 127.0.0.1:43111:127.0.0.1:43111 ALPHA_ACCOUNT@ALPHA_HOST
```

Do not disable host-key checking to bypass an error. SSH implementations,
authentication, remote access policy and forwarding permissions are outside
this package. Keep application HTTP loopback-only. SSH authenticates a route;
it does not make a theorem valid or turn a catalog into a complete global index.

## Required deployment acceptance trace

1. Alpha independently submits, publishes and exposes a result, then serves its
   committed view under an explicit finite grant. Beta discovers and acquires it
   through its own configured alias. Retain both hosts' source/runtime pins and
   bounded request/service evidence, including failures and incomplete transfers.
2. Stop Alpha's service and forward. Beta freshly admits the acquired package,
   builds a nontrivial checked contribution using its exact receiving names,
   and publishes it. Audit actual reachable proof dependencies, not import counts.
3. Reverse the roles: Beta exposes/serves the contribution; Alpha acquires,
   freshly admits and uses it. No shared filesystem, borrowed acceptance state,
   manual promotion or indispensable third endpoint is allowed.
4. Demonstrate one supported continuity case: a fresh third node, or a fresh
   replacement Alpha state in distinct directories, reacquires a retained
   replica and freshly checks/uses it after the original producer is offline.
   Do not erase the original node to simulate this condition.
5. Verify finite session expiry, no silent renewal, clean worker shutdown,
   byte corruption refusal and honest resource accounting. Report separately
   software checking cost, network cost and operator/agent overhead.

This trace is a future qualification gate, not a statement that it has run.
No independent-host availability, bandwidth or failure-recovery result can be
inferred from same-host loopback evidence.

## Bounded continuity policy

Preserve committed canonical packages through independently retained custody
copies. An unavailable node can be replaced by a freshly configured node that
reacquires those exact packages and performs normal local admission. This
recovers retained mathematical knowledge; it does not restore the old node's
handles, private unpublished work, accounting history or acceptance status.
The existing same-host replica experiment demonstrates a bounded version of
this pattern on its preserved source cut; current-cut coverage is separately
identified in the delivery results.

If local state is pending, use only the documented supported recovery operation
with its original evidence. Nonempty SQLite sidecars, missing original receipts
or damaged state can deliberately block in-place recovery. Never clear them,
edit the database/configuration, reset counters or invent a retry ID to force
progress. Retain the old state and use a fresh-state reconstruction workflow
only when sufficient independently held packages actually exist.

No protocol can reconstruct bytes after every custody copy has been lost.
This candidate has no whole-network inventory, automatic replication guarantee,
general backup/restore command or used-state migration. Those limits must remain
visible to operators rather than being disguised as permanent knowledge storage.
