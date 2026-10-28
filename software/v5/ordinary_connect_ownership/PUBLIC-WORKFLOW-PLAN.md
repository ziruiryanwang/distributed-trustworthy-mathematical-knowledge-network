# Fresh public workflow for owned-connect settlement

2026-10-28, query_scaling. Source-only under SELECTION.md and root's explicit
two-slot approval. No sockets, product imports, runtime, tests or Git performed.
The used registration-refresh runner, its plan and public01 failure stay frozen.
New package/PROFILE and any launch remain root's separate exact selections.

## Why this run differs

Public01 reached its first refreshed READY, returned A and observed natural
registrar exit. It then failed on UnsettledTransportError during a stopped-port
request; it did not reach cycle two. Its saved error did not distinguish reset
from timeout and did not establish a leak. Neither an unchanged rerun nor
accepting that exception would establish the selected owned-connect behavior.

The fresh runner retains four public children and the A-to-B byte-identical
policy discriminator. It additionally puts one approved unavailable feed before
the live library feed. This directly tests the reason for the transport change:
a safely settled failed connection can permit later selected work under the
original bounded grant. No mathematical server, index, owner, proof or native
operation is added.

## Exact source and unchanged fixture

`public_workflow.py` SHA256:
`007e77eeec09c705d7d8f9ef1432b646962d8a6db17d205fe5497c550d496a58`.
It is a fresh successor of the preserved runner
`ordinary_registration_refresh/public_workflow.py`,
`b909464655b479b22bc106177dd889af82fbc7240641a40fb35972654081ec46`.

The same old helper provides only file/CLI/loader/result functions:
`ordinary_contact_federation/test_public.py`,
`98f3eb0b60e95bcdadca280c636c65ddaa2b6be47793ea43c264ab20abef7879`.
The old scenario is never called. The fresh original 100-second/45-own-CPU
envelope is assigned once before operations; no allowance is renewed.

The unchanged actual shared-carrier query is
`ordinary_finite_map_refinement/find-config02.json`,
`eec3a9399a341e2bd1e604c87f123819f099d53864ba99c2e110b9f36f8518c6`.
Its object-kind, theorem-kind and exact Std.HashMap portable-symbol specs remain
unchanged, as does namespace
`d966de54aa32c6cd059ab9553a0968a320594a63561cadf742cca6265858079c`.
The runner validates that namespace using the explicitly selected new package.

## Minimal two-slot sequence

Three inert loopback acceptance observers represent A, B and out-of-scope C.
They supply no application data; any learned-endpoint connection fails the run.
A separate local socket reserves an OS-assigned port without listening. Keep it
bound until the first library feed announces READY, preventing that feed's port=0
allocation from taking the registrar port. Then close it and require an invalid
descriptor before constructing or launching the refresh configuration. Finally
also closes it on early launch failure; reserved_socket_closed records the actual
descriptor observation, not an assumed cleanup. That numeric endpoint
is preapproved once as both the registrar's fixed listener and the first feed
slot. It is not a learned endpoint. In cycle two it is the observed closed prior
registrar endpoint. No new service child is introduced by this selection.

Each cycle runs one public `directory-serve` library feed and one public
`directory-refresh-serve`, using the selected package's ordinary run.py launcher.
The feed origin stays fixed. Cycle one advertises A and C; cycle two advertises
only B. Registrar config bytes and their saved hash stay identical across cycles:

- First slot: preapproved closed registrar origin, max_contacts 1, max_bytes 32,768.
- Second slot: live library origin, max_contacts 2, max_bytes 32,768.
- Both scopes allow only A/B; egress allows A/B/C so C is rejected by scope.
- Two requests / 65,536 bytes are prepaid once per invocation. No retry, new
  grant, arrival-order selection or silent quota increase occurs.

Both first-slot outcomes must be SETTLED_UNAVAILABLE with one of the existing
CONNECTION_REFUSED, CONNECTION_RESET or ATTEMPT_TIMEOUT reasons, followed by the
second slot's ADVISORY_CONTACTS outcome. Both refreshes correctly remain
incomplete because the first feed failed. Cycle one's library row reports one
scope rejection; cycle two reports none. Both serve exactly one contact.

The direct existing X.exchange/CD.read_reply reader gets A, then after natural
first registrar exit makes one stopped-port request, then gets B from cycle two.
The stopped-port result must be an actual SettledRefusal with one of the same
three known reasons. UnsettledTransportError, cancellation and unknown errors
remain failures; the runner never reclassifies them. Exactly three reader
attempts and four public child commands are permitted.

Every reader attempt is saved in the in-memory report before awaiting exchange.
An unexpected exception preserves phase (`awaiting_exchange` or outcome
validation), elapsed duration and at most six chained exception records, each
with type, errno, winerror, a bounded message and cause/context link. The
transport has no public phase attribute; the runner does not invent one.
Raw child RESULT/diagnostic files remain preserved if a public command fails.

## Finite timing and closure

Keep 4,000 ms refresh attempt ceilings, 6,000 ms request-start source age,
2,000 ms minimum service, thirty-second requested registrar lease and ten-second
cleanup. The library feed lease is sixteen seconds, giving room for the initial
bounded unavailable attempt plus startup and the live feed request. It is not
renewed. READY must show 2,000..6,000 ms remaining, two selected slots, false
refresh completeness and exactly one retained contact/route.

Observe each registrar's natural process exit by READY.remaining_ms plus ten
seconds cleanup and three seconds wrapper reporting, strictly below the
requested thirty-second lease. Feed exit is bounded by sixteen plus ten plus
three seconds after observed feed READY. All children also retain their original
45-second public command allowance. Same-origin feed and registrar rebinds are
attempted only once after clean prior exits. A collision/bind refusal is preserved
as failure; no alternate port or automatic retry is selected.

Require public results, nested supervision, zero active processes/reserved bytes,
quiescence and no cleanup errors for all four commands. Each refresh ledger must
close with exactly two charged requests / 65,536 bytes and no pending request.
Each public feed and registrar should serve one request. All three learned-endpoint
observers must record zero connections and close. The failed known-feed attempts
are intentionally separate from learned-endpoint dial counts. Any forced cleanup
is a failed workflow, and the outer Job remains the descendant containment.

## Later exact launch selection

Proposed fresh output:
`experiments/v5-local-checks/connect-ownership-public01/suite`.
Root should select a single Run-V5-Check operation named `connect-ownership-public01`
after the new transport source controls and package binding pass. Its argv must
run `{snapshot}/software/v5/ordinary_connect_ownership/public_workflow.py` using
approved `D:\Python314\python.exe -I -S -B`, with explicit `--package`,
`--profile-sha256`, `--python-runtime D:\Python314`,
`--lean-runtime E:\Distributed Trustworthy Mathematical Knowledge Network\software\runtime\lean-4.34.0-windows`
and `--output {output}/suite`. Package/PROFILE have no default or inherited old
selection. Root must bind their actual new values and receipt before launch.
All subprocesses use the canonical root as cwd and save exact COMMAND.json files.

Retain outer 110 wall / 60 inclusive Job CPU seconds, 1,024 MiB, eight active
processes and 1 MiB stdout/stderr. Each public command remains 45 wall / 25 CPU
seconds, 512 MiB, three processes and 1 MiB stdout/stderr. Each direct reader has
two seconds absolute exchange time plus the existing one-second close bound and
32,768 response bytes. Helper reads/reports remain <=2 MiB; READY <=64 KiB.
Do not add nested CPU measures to the outer inclusive total.

This is a changed transport/maintenance composition check, not another complete
discovery or mathematical campaign. Owned-connect controls establish the
pre-transfer seam; this workflow exercises real later-feed progress and policy
replacement. Loopback services remain one-host simulations, not public TLS,
independent-host operation, liveness or final-v5 acceptance evidence.
