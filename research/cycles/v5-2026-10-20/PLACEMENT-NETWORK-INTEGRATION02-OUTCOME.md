# Actual remote-placement integration02: scoped PASS

Independent audit, 2026-10-21. **PASS:** a fresh custodian accepts one actual
remote structural placement, preserves identical replay/status, advertises it,
and supplies goal-only discovery/acquisition after the original source closes.
The reader then genuinely verifies the received succinct I receipt and opens
the selected theorem group under temporary local trust, which is withdrawn.
This is same-host loopback integration evidence, not full v5 acceptance.

Root launched session 75970 exactly once. Audit used read-only files/hashes and
isolated stdlib SQLite queries with `mode=ro`/`query_only=ON`; no product import,
network, proof, verifier rerun, state mutation or old-campaign replay.

## Exact bindings

Evidence root: `experiments/v5-local-checks/placement-network-integration-02`.
The adopted changed-source review is `PLACEMENT-NETWORK-REPAIR02-REVIEW.md`
(`657e799c53f258f53a4e93a729ec023177663d56a3299085e95b23c1b7076bd8`).

Independently compared **129 physical originals and all 129 retained source
snapshots, 25 direct runtime pins, and 123 staged logical files** (121 product
plus two query helpers): every selected hash/size matches. Twenty recorded
pre/post role-file bindings across the two Node roles also match the staged
pins. This is not an independent rehash of the whole transitive runtime corpus.

| Binding | SHA-256 |
|---|---|
| `selection.json` | `87c80fd67a6279c4481faa1dcb2c97fd9e9576c4dea6744fdf1d6cd0fb108f6e` |
| Adjacent `placement-network-integration-02-input.json` | `6e14ba3b8abbce616a8115b7ce3a229242869a3b8861c427c52e3221a2f47f58` |
| `integration-sources.json` | `d4b5877bc6253c3e063fa3b51151dd0726ac84fdbcfce19bdef854d273686d77` |
| Outer `RESULT.json` | `6cbb4ec3e6b01720a4b3b956942aff6989a6259de30a9b881614bf84ee253f81` |
| `placement-network-integration-result.json` | `e888707cf59b40d199e0ad982f25b845792f6c459fa06d4eb4dd70917d526826` |

## Actual placement, replay and source withdrawal

The first response is `RECEIPT_COMMITTED` with `INDEXED_UNADVERTISED` structural
outcome. Its separate route observation is `HINT_DISPATCHED_UNACKNOWLEDGED`,
with one actual add-provider write. Neither observation is mathematical
acceptance or a global availability guarantee. The local placement receipt is
distinct from the later cryptographic mathematical receipt.

Independent comparison confirms exact equality of the first, duplicate and
status response bodies. The three intake requests complete with no error,
uncertain submit or additional placement charge. The durable ledger has one
grant/request/cell and one committed request, recovery unused. Its single
reserved total equals final used funding and the saved response:

`placements=1, index_calls=2, new_cells=1, recovery_passes=1, requests=3,
reply_bytes=517519, storage_bytes=34138740, structural_bytes=17010880,
wire_overhead_bytes=98304`.

These are nonrefundable authorizations, not measured physical costs. The
route journal has one matching run/cell/request row, not another publication
on replay. B's index has one object/22 postings/two snapshots; source A and
reader R each retain zero index objects.

A performs exactly three successful HTTP reads: group, packet offer, packet;
449960 reply-body bytes, 459 request-body bytes, 688 observed header bytes.
Its final counters equal those saved after first placement: replay/status
causes no new source fetch. The reviewed adapter stops A's listener, confirms
no tasks/server remain, and closes A's workspace **before** constructing R's
workspace or invoking its independent goal-only reader. The executed report
reaches `done`, with `source_closed=true`; this is not failure-path cleanup.

## Discovery and exact retained knowledge

R obtains one actual route and one advisory descriptor contact, then two
authenticated search responses: one offer and one verified page. Search uses
one provider/snapshot/page, examines one candidate and returns one unique
record; actual search bodies are 5828 reply bytes/946 request bytes, with 447
header bytes. There is no global-completeness claim, and index-build assurance
remains separate from authentication of the committed snapshot.

R is given the closed binary-congruence formal goal, not A's selected module
ID, theorem name, placement manifest or evidence digest. The actual returned
`CommonsV5.binary_congr` has group index 10 and module
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.
Its complete type hash is
`f2edeb38b850ec7b5a0188be612ee16e2b6d29cf31bc984afffa8ff06ebef82d`,
equal to both the reader's independently constructed goal and admitted type.

Read-only SQLite comparisons independently establish byte equality of A, B
and R's stored group and packet, and equality to the selected fixture opening:

- Group opening: 1595 B,
  `0c74d294730fc2d005a082aba01350e5a9ab54a5aa797036f35d607ce17c900a`.
- Packet: 447887 B,
  `a737e8f650e9d3abb4781bb2c85c0e625ed4573b7170d71aff1799dbb54495e3`.

B serves five reader HTTP requests with no failures: 455788 reply-body bytes,
1403 request-body bytes and 1135 header bytes. R's shared acquisition reports
nine charged requests including six prepaid location/search slots, 720296
charged reply bytes, no pending reservation and **zero verification attempts
or worker reservations consumed during structural acquisition**. Actual group
transfer is 1595 B; offer/packet responses total 448365 B. The route allowance is
not an observed DHT-byte measurement.

## Genuine mathematical admission and owner closure

The successful network cleanup precedes the separate received-I verifier call.
Actual saved executable stdout reports `REAL_MODULE_RECEIPT_VERIFIED`,
`fully_resolved=true`, `mathematical_admission=true`, rank 0 and
`succinct-poseidon2`. This audit checked the actual native process report,
stdout, request, received bytes and same-call binding, not only the exit code
or owner summary.

The 223594 B receipt hashes to
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`
in the selected input, stored received file, executable output, request,
binding and mathematical result. Native journal bytes equal the selected 184 B
journal and the reported mathematical journal. Module/summary bindings match.
The owner then opens the acquired group with that live handle and confirms
membership of the exact returned declaration. No ancestral proof replay,
new Lean/native theorem check or proof production is added in this workflow.

Verifier accounting records one attempt, 10 reserved CPU seconds, 223594
submitted bytes and one live handle before close; afterward it is closed with
zero live handles. The saved support's 148 roles match the actual selected
sources/runtime/supervisor/adapter bindings. Independently reconstructed
support ID is
`f93c46aa58c7f04a17bb3aff05e4a43fb08bf1e4244fecff4560d28da85d0181`.
The withdrawal marker binds this ID, the same domain, and the exact adoption
file hash. Temporary trust is withdrawn, not reusable live policy.

B's service reports `CLOSED`, with all six role/store closure flags true and
no cleanup errors. Both Node roles report closed/returncode 0, no channel
failure or forced termination; each uses three commands. B's complete final
runtime validation still takes 7.2918821s, beyond the former seven-second
wrapper, and now finishes within the selected original close allocation.
Its 6s native teardown and all runtime/role checks remain unchanged. R's final
runtime validation takes 7.5593174s. Both actual censuses are 5896 files and
130118221 B. These are recorded runtime validations, not new audit experiments.

The client/acquisition diagnostic snapshots intentionally precede their
source-enforced `close()`/`finally` calls and therefore show `closed=false`;
they are not post-close observations. Final reader workspace closure is true.
Outer and nested verifier supervisors both report reaped children, closed
Jobs, zero active/terminated processes and no cleanup errors.

## Costs and scope

Original outer limits remain 150 CPU/300 wall seconds, 512 MiB and six processes.
Outer Job CPU 34.359375s plus wrapper CPU 0.796875s gives **35.15625 known CPU
seconds**; wall 42.653352700173855s, supervised wall 42.4244336001575s. Peak Job
private commit 299376640 B; six total processes. Wrapper-supervision 0.203125s
and nested verifier costs are already contained and must not be added again.
The nested verifier's own process report records 0.015625 Job CPU seconds,
0.7034088s supervised wall and 13ms inner verification; these are different
scopes, not interchangeable overall verification latency. Outer logs are empty.

No source/execution allowance was renewed. Failed01 remains a failure with
its original costs; these variable runtime timings do not establish a speedup.
This run qualifies the corrected remote-placement/source-offline discovery/
received-I admission composition for one retained theorem. It does not create
a new mathematical extension, prove net full-cost growth, test retention repair
or sustained churn, qualify public TLS/independent hosts, install a distribution,
or establish full v5 readiness. No passing campaign should be repeated merely
to increase evidence count.

## Additional durable evidence hashes

Paths are under this run's evidence root.

| Evidence | SHA-256 |
|---|---|
| `received-i/process.json` | `3255d4060cf8f630709772241eac6de979fdbbb18a77fc4e99b19d3ba3257761` |
| `received-i/command/stdout.txt` | `1b6236bda564c7b0a7ce8bc124d2a2be4cc8b9712f5e98a7061bdf8f18636515` |
| `received-i/binding.json` | `e5c8607453b99b6fa2c7ef1cc30420bf946ebc21c475d87dfc312507e7c4e27e` |
| `reader-trust/ADOPTION.json` | `393d958ffaec2fdb9e2c453cdd438bb40a43d160ea9799c9001aa46137867c9c` |
| `reader-trust/WITHDRAWN` | `060aefb01b2b75b5c554ca64228a305023cb79590550bd35817577d76248c08c` |
| `custodian-workspace/placement.sqlite` | `9328c3f83df9b8d57af480d4249a8c68f634354db302d3bf375923fb08115ee9` |
| `custodian-workspace/placement-routes.sqlite` | `eaef9bd13643c1ea80af90831329de34c317d4fd0001f95d42101d39577ad841` |
| B and R `modules/modules.sqlite` | `1aaa887d9aacf9d7a4a5786ffaee402a584e27c1ace796a8f9fc8985e246833b` |
| B and R `packets/evidence-packets.sqlite` | `cbb5fb22d57d05581b6c82d87a1d3fdba15a408dbaa1da936da4bd142fac9202` |
| `custodian-workspace/index/discovery.sqlite` | `808799e2e785d76ad1a128044a44b92f8a0d5633a5acf832b4a847227130cc28` |
