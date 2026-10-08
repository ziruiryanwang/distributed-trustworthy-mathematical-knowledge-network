# Next contact/hosting slice: authenticated loopback forwarding

## Read-only local tooling observation, 2026-09-21

Root found existing `C:\Program Files\OpenSSH\ssh.exe` and `sshd.exe`.
The client reports `OpenSSH_for_Windows_10.0p2 Win32-OpenSSH-GitHub,
LibreSSL 4.2.0`; the existing `sshd` service reports Running/Automatic.
SHA-256 client: `6890C128C86CC2C38AAD9FCB32A82B851FF3D38C714A1F656B8E445D7CD5E1C6`;
server: `D66150486D472B8748CAE2D6F5078A210DAE91621447974BDE028F077A4EF90C`.
This was only command/version/hash/service-state inspection: no SSH connection,
credential/key read, server configuration change, listener change or deployment.
The existing service is not a project-owned service or evidence of a second
controlled host. The earlier question about a second host remains unanswered.

## Prospective profile

2026-09-21; source-only proposal. Read GOAL, PEER, manage/node/peer-service and
replica proposals. No import, network probe, service/config change or deployment.

## Recommendation and boundary

Qualify one `ssh-loopback-v1` operator deployment profile: independent hosts,
existing finite serve/request commands and direct authenticated SSH forwarding.
Deliver an install/run recipe and bounded conformance workflow, not a new wire
protocol or automatic tunnel manager. SSH tooling and authorized hosts remain
to be selected; none is assumed here.

Interpret the current at-most-two configured loopback aliases as **transport
slots**, not permanent supplier identities. An operator can retarget a slot
without editing its immutable application configuration or discarding state.
This supports serial contact evolution, not more than two simultaneous routes
or automatic discovery.

Indispensable: independent supply, deliberate routes, bounded grants, retained
failures and fresh receiver checking. Identity/history registries, relay, DHT,
consensus and attribution are not prerequisites. This is not complete v1.

## Tunnel versus direct endpoint

| Choice | Benefit | Additional obligation |
| --- | --- | --- |
| Direct SSH; both application ends loopback | Existing bounded wire/package interfaces; authenticated encryption; no common relay | Operator credentials, pinned host key, reachable SSH endpoint, forwarding permissions and lifecycle |
| Native non-loopback endpoint | No forwarding setup or fixed slots | New endpoint/bind policy, address restrictions, DNS/rebinding, authentication/privacy, exposure controls and qualification |

Prefer forwarding. Independently pin the SSH host key; refuse unknown/changed
keys. Use a restricted forwarding-only account limited to the remote loopback
port. Expose neither shell/arbitrary forwarding nor the local owner API. SSH
credentials authorize transport access, never Lean acceptance or authorship.

**Port constraint:** the client sends HTTP
`Host: 127.0.0.1:p`, and the server requires its own bound port in that field.
An unmodified SSH tunnel must therefore forward local port p to remote
loopback port p. Unequal ports refuse. Reserve nonconflicting selected ports.

## Supplier changes and necessary history

Let E be the recorded entry containing foundation-relative root/descriptor,
manifest digest, bundle digest/length and metadata. Changing the SSH supplier
behind a fixed slot cannot replace the selected bytes with different bytes
while satisfying E, conditional on hash security and correct local validation.
A new supplier can satisfy an old selection by serving that exact bundle, even
if its current catalog differs: acquisition requests the selected bundle hash,
not a fresh catalog. Missing/altered bytes must refuse; coherent new lies still
face local structural rederivation and fresh Lean admission.

An old remote record binds a selected entry to a slot, **not** the later
supplier's identity. Preserve immutable entry/request/candidate/custody bindings;
do not rewrite old records or attribute unsigned catalogs to an SSH host. The replica
helper's configured-endpoint check remains satisfied because the local slot
address is unchanged; intact frozen views need no old SSH connection.

Before retargeting, finish/reconcile in-flight work, stop the old tunnel and
verify process/listener release, then authenticate the new target. Record a
bounded session manifest: slot/ports, host/key fingerprint, start/stop outcome
and service grant reference; no secrets. This supports diagnosis, not acceptance.

## Decisive evidence and remaining hosting gap

Controls: same-port success; unequal-port refusal; unknown/changed SSH
key refusal; tunnel interruption with retained charge and normal recovery;
slot retarget to exact replica succeeds while changed bytes/absent bundle
refuse; no private/source/SQLite route; no acceptance from metadata; old
acquisition and frozen-view bindings survive route changes without config edit.
Measure tunnel resources separately: existing application Jobs do not contain
operator SSH processes or prove their quiescence.

External evidence requires separately administered supported hosts: independent
installation, direct authenticated forwarding, acquisition, fresh admission,
substantive contribution and reciprocal use. Include producer-offline replica
supply, changed-key/disconnection controls, costs and receipts. Three directories
or SSH endpoints on one machine are not independent-host evidence.

Keep current serve grants finite (public wrapper: at most 360 seconds, 128
requests, 256 MiB). Every restart requires a new explicit owner grant; tunnel
reconnection grants no service budget. Do not label manual sessions permanent
hosting. Unattended restart across multiple sessions needs a later finite
cumulative authorization/accounting slice; no generic scheduler is included
here. The trusted local filesystem, package limits, source/receiver separation
and fresh acceptance boundary remain unchanged.
