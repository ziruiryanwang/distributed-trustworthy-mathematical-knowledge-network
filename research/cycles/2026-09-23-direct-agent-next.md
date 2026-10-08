# Next central test: an agent directly uses the existing local CLI

2026-09-23, America/Chicago. Prospective implementation note, **not launch
clearance**. No node, service, consumer, or proof submission was started for
this note. Keep frozen U1 and its negative outcome unchanged. The evaluator's
chosen target is one test question, not a network-wide task list or protocol
root goal.

## Decision

For a first self-service proof-authoring test, **do not build a new agent
protocol**. Package 02 already has the necessary local interface:
[`make_request.py`](../../software/make_request.py) creates an exact UTF-8
request file from an agent-authored source file, and
[`manage.py request`](../../software/manage.py) sends that exact file and
returns a structured reply. The agent can run both commands itself. The
latter already uses `supervise.Transport` for the public worker
(`manage.py:120–159`): ordinary calls have 450-second wall/CPU and 6,144-MiB
enclosing-Job limits, peer calls 120-second wall/CPU and 1,024 MiB; native
stages have the configured 4,096-MiB/300-second profile. Thus the key missing
evidence is direct agent use of checked mathematics, not a missing command
transport or a global coordinator. The `import Init` frontend has passed a
separate trivial capture probe under a 4-GiB Job, but full product and
nontrivial peer-dependent outcomes remain separate gates.

## Reuse, not replay

Use the freshly packaged source cut
`product-local/lean-frontend-package-02/math-commons-source.zip`, archive
SHA-256 `45088860e9e34cb4e099923db3f1d57ca019f3352ca63d6f67e2bef57cbe3152`,
manifest SHA-256
`d31c2aefe97559c0db22f6fd883dc20e26fa07165668e3d6dd470046e00ea682`.
The extracted, support-built install at
`product-local/lean-frontend-integration-02/install` may be reused read-only
if its ongoing integration closes and its complete installed source/build
pins are still unchanged; otherwise freshly extract/build that same archive
into a new install. Never modify an install already bound to node state.
Its `native/AgentClient.lean` SHA-256 is
`3843e9baa335e772db21ac127121b276426c4117f1ab508c21f30c04c15f185d`.
The [package audit](../../experiments/lean-frontend-integration-02/PACKAGE-AUDIT.md)
verified source/ZIP/extraction/build continuity, not this test's endpoint.

Before any agent dispatch, the operator creates new, absent state/scratch,
request and agent-source directories on the same NTFS volume; a proposed
separate root is `product-local/direct-agent-s1-01`. Call installed
`manage.py configure` with one `local` client, `--context-packages 16`,
`--initial-requests 16`, `--initial-stages 10`,
`--initial-reserved-mib 2048`, `--initial-metadata-mib 32`, the pinned Lean
4.34.0 runtime, and one independently checked loopback peer alias/port for
setup. Then use one new owner `init` request. The S1 plan's finite ledger
arithmetic still applies: at most seven operator setup requests and four
stages, followed by six agent `submit`, one `publish`, two `info` requests and
six more stages; 16 requests/10 stages, maximum 1,464 MiB logical
authorization under those request classes. Confirm fresh physical supply
(at least the plan's 3,136 MiB sample under its 2,048-MiB grant), actual
product charges, and setup/agent aggregate limits; logical authorization is
not a disk or memory reservation.

Operator-only setup, using **new** handles and request IDs, follows the
four-call `init → R submit → R publish → R admit` route evidenced in
[U1 B onboarding](../../experiments/useful-reuse-u1/ARM-B-ONBOARDING-INDEPENDENT-AUDIT.md).
The R source may be the pinned 207-byte
`software/drafts/UsefulnessVocabulary.lean`, SHA-256
`b3d65406fa204268f74bb3cbdcd623991127aa5d3ccc06595c63890f9fd9e48a`,
but no old request/handle/state is copied. Require the fresh checked R
reference, body and complete package to match the independent oracle
manifest SHA-256
`b761e063e52c785f097a1308047da5cb453335a989ff80f9a208785675152133`.
Then serve the unchanged
[`treatment-view-02`](../../experiments/useful-reuse-u1/treatment-view-02)
static fixture (catalog SHA-256
`998f61e775ad5c0cb2353d648ee39b2e041a0056748f12edbc7776c9bf69b360`)
for **setup only**. Its existing `peer_service.py --view --port --ready`
entrypoint supports this; adapt the independently reviewed
`service_supervisor_u1arm_enabled.py` pattern to fresh paths, current
package/source pins and a short bounded session. Do not execute that
U1-specific wrapper unchanged or give the fixture/service to the consumer.
The operator sends one new `peer_find`, selects the intended P by pinned
formal reference/package rather than name/display text, uses the newly
returned remote for `peer_acquire`, and freshly `admit`s exactly that
candidate. Require checked R and P in the resulting context and a current
P1 snapshot; stop and reap the service before agent dispatch. This excludes
unknown-result discovery and delayed availability, which need later tests.

## Direct no-history agent phase

Start one agent with no inherited conversation history. Its frozen packet
contains only current checked context/P1 handles, formal R/P receiving names
and types from its own node replies, the exact formal target statement,
installed package-02 `API.md` and `AGENT-QUICKSTART.md` pins, permitted Lean
library source root, its own writable source/request paths and finite budgets.
The evaluator retains
[`TARGET-TYPE-FREEZE.json`](../../experiments/useful-reuse-u1/TARGET-TYPE-FREEZE.json),
SHA-256 `c2491177e88bdc752437e40e04da8051aeb4cb93b2c6ec49c20aa6e6c16ac1f9`,
but does not expose that oracle, U1 proof attempts/diagnostics, S1 plans or
fixture files. The agent may choose when/how to search library docs or prove;
the system prescribes no proof strategy.

For each independently authored version, the agent writes a new UTF-8 `.lean`
file, then itself runs installed `make_request.py submit --client local
--request-id NEW_ID --context CURRENT --source-file ABS_FILE --root ASCII_ROOT
--output NEW_JSON`, followed by installed `manage.py request --config
ABS_CONFIG --request NEW_JSON`, using Python `-B -E -s -S`. It reads its own
structured reply and diagnostics, never treating CLI exit zero or a capture
summary alone as acceptance. On known `SOURCE_REJECTED`, it may author the
next file/ID within six charged attempts. On `accepted:true`, it itself uses
`make_request.py publish` with the returned artifact and then-current P1
snapshot, then `manage.py request` again. The helper's output is
`REQUEST_FILE_CREATED_NOT_SENT`; only the second command spends a product
credit. Each request/source file and direct reply remains immutable and
auditable. An unknown/pending transport outcome stops; no fresh ID as a
surrogate retry. Allow at most two `info` calls and separately bounded
read-only `inspect` calls if preauthorized. No operator relays, repairs or
constructs an agent request.

The positive endpoint remains stringent: product `submit accepted:true`,
complete canonical theorem type equal to the hidden frozen target, a
root-reachable proof-producing use of the exact freshly admitted P reference,
and ordinary `publish status:OK` of that artifact. Independently audit the
source/request bytes, context, native stages, artifact/package/proof DAG,
P use, publication binding, full resource charges and failed attempts.
`make_request.py` accepts ASCII/dotted roots, while checked P receiving names
can be quoted Lean names inside source; the agent must use exact returned
names, not guessed handles. A successful direct proof lacking P is not a
passing reciprocal-use endpoint.

## Costs, limitations, and next decision

U1 B's four cold R-onboarding calls cost 290.671875 enclosing-Job CPU seconds;
its P admission cost 35.6875 seconds. Those are historical costs, not a
prediction for the new frontend. New `import Init` trivial source capture
used 9.96875 Job CPU seconds and 2.489 GiB peak within 4 GiB, but nontrivial
proofs can still fail capacity, capture language or native replay. Count
operator setup, service, all failed submissions, direct agent/model work and
retained evidence. A direct agent on the shared machine is a **cooperative
information-boundary test**, not OS-enforced protection against reading other
files or running unauthorized commands; review the tool/file trace and do
not claim adversarial isolation. No second host or license is available, and
no external publication is authorized.

If this authoring-first self-service endpoint passes, the existing CLI is
operable for this bounded task. It does **not** yet establish decentralized
return, unknown-result discovery, long-delay retrieval or sustained useful
growth. The next central gate is a fresh receiver independently discovering,
acquiring, admitting and using the new publication after the original
supplier has stopped, under measured finite resources. A global ledger,
attribution policy or new agent scheduler is not required for this test.
