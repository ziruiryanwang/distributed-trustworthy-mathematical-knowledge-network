# V5 resumed integration assurance — 2026-10-12

## Explicit implementation resumption after guide delivery

### Actual network01 outcome: independently audited FAIL, no math attempted

Root reports session73832 terminal and reaped. Saved outer RESULT
`09f4ebfc23bec4d773ef7c84b9c35904830ad16d8ba5a4f10a642d73dd2ad279`
and inner RESULT
`367be7f9ae7fe13fd2e3ca3af9f734184d9647d2cbbea76a844b5f7021e67706`
independently establish failure at `NETWORK_NO_LOCATED_INDEX_CONTACT` in reader1.
All 210 selected actual bindings still match, now including the actual Python
snapshot files. Copied selection is exactly1718ca6b; config86dbacee remains
unchanged. No FINALIZATION-FAILED marker exists; the raw outcome is simply FAIL.

Origin built structural custody with13groups/11bodies and no missing committed
values, then reported ADVERTISED_HINT for rendezvous4ae286d8. Reader1 actually
joined the neutral bootstrap but its sole route returned an empty peer list.
There was no descriptor request, HTTP search/acquisition, receipt owner, delta
owner, mathematical check or admission. Reader2 and replica were never created;
origin loss and the typed descriptor-recovery seam were never exercised. An
advertisement status is therefore not evidence of successful distributed lookup.
The exact underlying DHT/topology cause is not established by these records.

All3Node controllers closed with exit0, unchanged role/source pins, successful
5896-file runtime pre/post checks, no channel failure or forced termination.
Their raw stderr reports LOCATION_IPC_CLOSED, zero live transport connections,
zero descriptor-unavailable events and no exhausted transport allowance. Origin
HTTP had0requests/0failures/0active; cleanup errors are empty. Outer Job reports
5total processes,0active,0terminated, direct-child reaped and Job closed, exit1.
No proof or admitted artifact was produced or relabeled.

Actual cost:21.578125 inclusive Job CPU plus separate0.703125 wrapper CPU,
90.4038063 outer wall seconds,533635072B peak Job private commitment. Inner
controller18.015625CPU/88.4697278wall is already inside the outer Job cost.
Bootstrap's first full runtime hashing used69.6194914wall;405seconds remained
before reader1 startup, so the failed empty route is not a deadline exhaustion.
All source/config/evidence stays frozen. No retry, cap renewal or automatic
successor was selected by this audit.

### Aggregate input encoder: source correspondence cleared

`aggregate/input.py`
`5c5d51403bb00234f5843a1b6ca4109195285e292bdcdcc08f07ae94c7b0a226`
matches Rust's DMKNAI01/v1 wire: image/counts, tagged184B-I or192B-A claims,
frontier claim indices/member openings, raw target ModuleIDs, and u32LE-length
witness frames. It checks finite list/wire bounds, unique/used claims, exact
legacy or aggregate frontier binding and duplicate frontier modules. It does
not claim topological validity, new-target validity or mathematical correctness;
the actual Rust relation checks those independently.

`from_legacy_packet` correctly compares canonical summary bytes (the existing
packet parser returns bytes, not a summary dictionary), preserves exact pending
receipt/journal pairs and canonically encoded mathematical witnesses. It does
not validate the receipt-to-journal claim. Real host verification and resolved
guest assumptions remain mandatory. No encoder/test/compile/runtime was run.

### Aggregate host receipt boundary: standalone source clearance

Root's unlinked `aggregate/receipt.rs`
`41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254`
uses the same real-cryptography profile as the retained module host: bounded
fixed-integer bincode with trailing-byte refusal, genuine Succinct Poseidon2
only, no RISC0_DEV_MODE variable, explicit verifier dev-mode=false. The retained
SDK implementation was inspected: verify_with_context performs real integrity
verification and compares the exact ReceiptClaim::ok(image,journal digest),
including successful exit and resolved assumptions, not integrity alone.

Pending claims must be the fixed I member statement or the independently
adopted A aggregate header. Exact pending journal bytes are compared to the
real verified receipt. Final aggregate verification first binds expected
header.A to adopted A, then genuinely verifies that image and exact header.
VerifiedReceipt fields are private and accessors immutable; structural helpers
or serialized success reports cannot construct it through this module's API.
This is not a session/expiry implementation. Consumer adoption/lifetime policy,
hostile-deserialization memory/CPU containment, complete producer resolution,
linking/build/execution and a public aggregate member receiver remain separate.

### Actual network01 source and exact selection: cleared, not yet executed

Reviewed the complete `delta/network_actual.py` successor SHA256
`1d3a7802790186a7ceb929fecc2bcdd99bc72a46049ce23f0f0795b379b4ea2c`
and `network_actual_api.md`
`c4675e6f61284292e672a51c6704ebb68b8b6ae9053759cc53602a4de982ac57`.
Before use, review corrected the missing post-report original-deadline check
and a reader2 local-variable shadowing defect that would have replaced custody
evidence with the last body response. The final source retains operation error
separately when cleanup also fails and uses a FINALIZATION-FAILED override.

The source has two fresh genuine receipt/native owners, not transferred live
handles. Reader2 first obtains the real origin route; only then does the harness
close origin HTTP/Node/stores and start replica from reader1 custody. Reader2's
same channel and prepaid grants charge the stale descriptor and route again.
The first actual returned formal candidate is selected without target/provider
ID injection. Expected retained identities are checked only afterwards. This is
trusted same-process orchestration, not adversarial process isolation.

Both readers reconstruct committed selected groups/bodies from acquired packet
bytes. Reader2 opens its own live DeltaImportSession and reconstructs normal
authoring context using those bytes plus the independently adopted foundation.
This adds no Lean authoring or mathematical-verification call. Independent
read-only inspection of the retained packet found 11 available body hashes and
16 selected declarations, with no missing demanded definition/recursor hash;
this inspection is not a successful context reconstruction or admission test.

Root's exact unlaunched selection:
`1718ca6be75e5971d44f5929f52c00350841352c28bcd6f1251013c92744f636`;
configuration:
`86dbaceea85da39233893f3bc300e1bea1f45f34dad1f29ac0bd2d9b64f74865`.
All 210 independent prelaunch bindings match: 55 canonical sources, 43 outer
pins, 75 owner-runtime mappings (including 55 future snapshot paths checked
against their exact canonical bytes), 28 Node snapshot/source checks, 9 inputs.
Future Python snapshot/output is correctly absent; the 14-file Node snapshot
exists with only the selected entry alias. No unexpected source borrowing is
allowed by the loaded-source closure guard.

The enclosing allocation is 300 CPU seconds, 600 wall seconds, 4096 MiB and
8 active processes. The original workflow is 480 seconds; at most 3 location
children coexist. Each of two admissions reserves 30 receipt plus 2 times 30
native CPU seconds under the same app grant, with 32 requests/32 MiB replies;
18 requests and 1,081,344 reply bytes are prepaid before each reader starts.
Seven root-selected loopback ports are 43171..43177; root's preparation bound
and released them, which is not a guarantee against a later bind race.
The generator and frozen snapshot/supervision runner were read. Clearance is
only for this one finite operation, with no automatic retries or renewed grant.

### Aggregate source and Python/Rust bindings: source clearance only

Read the stable eleven-file aggregate crate, its source controls and API in
full. Production delta construction directly calls the unchanged mathematical
relation; no checker callback can inject a conclusion. Private graph edges are
the exact returned parent journals, with existing-member equality, strict rank,
duplicate/conflicting ModuleID refusal and full backward target closure.
Every claim must support a selected frontier. The guest discharges every exact
typed I/A assumption via real env::verify before committing the 192-byte header.

The header's exact A binding and overflow-checked increasing seal height support
induction over prior aggregates independently of mathematical rank; within one
aggregate, topological checking establishes the new members. This reasoning is
conditional on genuine recursive-receipt soundness and the adopted checker's
conditional extension correctness, not an independent proof of either.
The Merkle construction binds domains, member count/index, exact legacy journal
bytes, ordered level nodes and explicit duplicate-last padding. One selected
member needs only its bounded opening, not all sealed proof witnesses.

Wire length is checked before each witness byte-vector allocation. Global
rows/bodies/openings/edges/nodes are bounded; the JSON tree is nevertheless
constructed before the global node census, as the API now states explicitly.
The temporary census tree drops before the unchanged checker parses the frame.
Outer memory/cycle bounds and actual feasibility remain necessary. Test-only
synthetic graph conclusions are not production or cryptographic authority.

Exact reviewed crate hashes:

| File | SHA-256 |
|---|---|
| Cargo.toml | `58d5d9d2ccfde1c060948c9c2ef5978175c809ac187defb8e8c1573a409b9363` |
| lib.rs | `ae71c52390fd47fa3b0cb130b289ff19629bbd8cb976f59c0042e1aabb95c340` |
| header.rs | `642167ddde6a6f134efff58a2ab270916ebe050f7d0f29acf69f8aaa3465a8e8` |
| membership.rs | `25e6a2fa86f4c095dd9bd76ce83de60c55405bc9d52eeec1c668e51c07e04b6d` |
| wire.rs | `2368990cb04186b0e01f3b2075cf7e0505ffaa26f4f2aef6680a342b39f7957d` |
| census.rs | `f6ab62fe777482acb913972a34689eeaec16ed99fedae584cc6b62f6e4ba18df` |
| relation.rs | `0f4e240727511764ef4b86a8185c55eb310b89396dece2e8f12fca055bc3460b` |
| main.rs | `d7b9b93843b683215e0556e585bc5ea241c672fe4c2a89cc07afa41afb81acad` |
| tests.rs | `6a784eb7781284e8560928a5b47089721dadc38ef725f31ba7c3d89d14e089ae` |
| graph_controls.rs | `7a055e63d1a4420ac8187f592342f4574e3604f5eff0a14510cc9526e924bec4` |
| API.md | `90b14c1d415a4f01c80ee4237551d2554b2610c71f4c4f233a19e507d824431e` |

Root's Python `aggregate/bindings.py`
`d749273ef5841afe881407bcb3c2655385dd635bdae12b37e09ca2381a46bcd5`
matches the Rust header/member layout, LE image-word/integer framing, policy,
count/height/rank constraints and domain-separated SHA construction. Canonical
lowercase hex ordering equals Rust digest-byte order. Paths agree for singleton
and odd-width trees; index/count/depth/duplicate-last rules coincide. Python
requires an adopted A when decoding, but performs no cryptographic verification.
No build, test, guest execution, new receipt or public receiver is established
by this source correspondence review. A distinct fully resolved A producer and
receiver, typed frontier/import path and network exposure remain required.

### Recoverable descriptor-unavailability seam: narrow source clearance

Reviewed `node_entry_services_available.mjs` SHA256
`02bbdf1223602aff512ae9cfadcc58f2b5e6efc02e1c1b65b34e3f14ebc75fb2`
and `available_descriptor.py`
`d3b215f59c0b4745562fdc76339a53f22d0fa009932dfecbef4fecfff6743fba`.
No runtime was launched and no outcome is inferred from this source review.

The retained TCP implementation changes an OS connection error's message but
preserves its `code` and `syscall`; transport-manager forwards it, and dial-queue
rethrows one exact error or a nonempty AggregateError of per-address failures.
The locator's `_command` resets busy without aborting the service on such a
failure. Thus an immediate refused TCP connection can reach this narrow seam.
Timeout/abort, authentication, protocol and allowance failures do not acquire
the accepted code/syscall pair; mixed aggregate failures remain terminal.

Recovery requires the original operation, life and locator signals still live,
the locator not stopped and its service deadline unexpired. It returns only a
typed local dial-unavailability observation, never authenticated absence or
nonexistence. Python binds the exact ticket/peer/status, checks the original
deadline, and abandons the ticket at its full reserved reply charge. The same
actual ServiceLocationProcess, WorkflowBudget and grant remain in use; positive
descriptor authentication and validation remain unchanged. All malformed or
other outcomes close the channel. The existing raw transport counters continue
charging failed connection attempts.

Root must use a fresh snapshot with these exact successor Node bytes aliased
as `node_entry_services.mjs` and that successor digest in the original role map;
the frozen predecessor is not modified. This clears only the source seam, not
the complete stale-provider lifecycle or any mathematical/network release claim.

### Actual retained-export repair01: independently audited PASS

Reprepare01 completed exit0. All184 independent bindings match:44 canonical
sources+44 snapshot sources+27 selection runtime+63 actual owner-runtime+6 exact
inputs. Outer RESULT SHA256
`232ef9cb77ffc12d46765fe49d3a428c5e7de6252689d22258fb3c22e6a852a7`;
inner `ae0297103d563c03561e8cc0eb803cdb7756a99d69f0d83dc067943fe1d949d5`.

Independent decoded packet comparison confirms ONLY the final1009-row witness
field changes. All other packet fields, prior witness, genuine receipt frontier,
mathematical spec/body commitments and local proof source are preserved. Exact
new and cold-receiving662,480B packet SHA256 is
`54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1`.
Actual first-delta parent equals the actually verified base journal; actual
second-delta parents equal the actual base and first-delta journals. The fresh
receiver admits unchanged target52c564f8 at rank2, opens its selected group and
exports the exact complete packet. This is genuine local native-delta authority
over a real cryptographic frontier, not a new succinct child certificate.

All three workers and outer Job exit0 with clean closure/reap, zero active/
terminated processes, no termination requests and no cleanup errors. Actual CPU
is0.046875s each; receipt/first/second wall0.7192437/0.1416823/0.1193155s. Outer
inclusive6.625CPU plus separate0.5625wrapperCPU,8.638137wall,peak107,601,920B.
Every final owner is closed with zero live handles. No author, guest, proof or
network call runs. Author01's failure and46.796875CPU+1.171875wrapper cost remain
preserved and charged; this recovery does not rewrite that outcome.

The shared corrected emitter has now been exercised with the retained export.
The new authoring02 live ordinary-source API path itself has not yet executed;
future normal use must select that successor, not the frozen faulty authoring.py.
Network circulation, aggregate certification and full-cost growth remain open.

### Retained-export reprepare01 exact source/selection clearance

Reviewed reprepare_actual.py; required one finalization correction: after writing
RESULT, recheck the original deadline and write overriding FINALIZATION-FAILED
on late/error return, as in prior harnesses. Corrected source
`fcb9af85e264047caf31b4936c8fb93e8ae6da71d4d6db1802e30ba1621b68bc`
is cleared with selection
`d20434664f4e94ff20186c659e71851c76c0ce2e394c08aa68551901e2a425d9`
and config `640c3fb38142b6cc1da0686137544a23c62eb3f20c37f458b61c1b42a16ecb77`.
All140 prospective bindings match:44 sources,27 selection runtime,63 actual-owner
runtime and6 exact inputs. Future snapshot references all map to selected
sources; output absent. Actual failed packet40aac392/export268681e0/request17cc9657
and fixed foundation736792e remain exact inputs, not editable prior evidence.

The harness requires only final witness rows to change, retains the same target
and actual successful ordinary-source export, then independently receives the
complete corrected packet with at most one real receipt and two native checks.
It opens the target, verifies exact re-export, checks final pins and closes all
owners before reporting. Earlier preparation profile contributes immutable receipt
host fields only; no old Producer/Owner source origins are loaded. Outer300CPU/
300wall/2048MiB/cap4, original workflow240wall, per worker30CPU/90wall/1024MiB.
No ordinary author, guest, snapshot, proof or network repeat is selected.

### Aggregate-DAG sealing principle audit: coherent, not implemented evidence

Read full DELTA-SEALING-POLICY.md and coordinated directly with its source author.
No blocking architectural contradiction identified. The proposed header is
indeed192B. Unchanged184B internal journals labeled I denote the existing
conditional module relation; real A receipts and exact Merkle member openings
provide a DISTINCT warrant. They must never be passed off as I receipts or
admitted by the frozen exact-I receiver. Preserving ModuleIDs is compatible with
an explicit new proof-form authority, not a permission to bypass image checks.

The top receiver must verify actual adoptedA and bind the header's suppliedA to
it; guest parent aggregate headers must agree onA/I/foundation/policy. Computed
seal_height is1+maximum parent aggregate height, with overflow refusal, and is
separate from mathematical rank. Conditional induction on height followed by
the actual finite relation-returned dependency order is valid under real recursive
application/commitment/checker soundness assumptions. Mathematical source sharing
alone is not a formal checker-to-Lean equivalence proof.

Required source obligations communicated: call unchanged relation::check_bytes
DIRECTLY, never a callback allowed to invent checked conclusions; keep pure
aggregate results explicitly conditional until real env::verify premises all
discharge; check unique/unused assumption descriptors and member openings
separately; derive exact graph edges from actual relation journals; require new
designated targets and complete no-extras backwards reachability; enforce exact
encoding/endian/domain hashes/odd-leaf handling/count/index/path depth; validate
frame length against remaining global budgets BEFORE allocation. Actual SDK
receipt-byte and full-resolve limits remain host obligations. No native/mock
control may grant cryptographic or mathematical authority by flag.

A bounded selected member commitment avoids mandatory global-state growth and
sealed-proof downloads. It does not eliminate demanded definition semantics,
future availability, new proof checking, aggregate prover cost or resource
refusal. The single-moduleI route on an uncertified chain genuinely requires
intermediate receipts; batching can remove separate certificate overhead, not
the sum of new mathematical checks. The documented cost model and capacity
inequality are conditional; they establish neither demand nor full-cost network
advantage. A new guest/host/member receiver requires separate exact review and
selected execution evidence; this principle audit authorizes no build or proof.

### Narrow relation-order repair: source clearance only

Reviewed fresh authoring02.py
`9438a5cb6d3a2e8172b0a655e49c13589c351297e7819760e47b5bc331bcbec1`
against the frozen predecessor: exact differences are documentation, importing
the shared emitter, replacing the import/local row-emission block, using its
returned rows, and requiring own/helper source pins. Frontend topological context,
live-origin obligations, full ancestry retention and mathematical gates do not
change. Used authoring.py remains untouched.

Read complete fresh reprepare.py
`af225a6dbfb6c7b5c28f0b8fb43374f06b2c4e139066c1c77ed3d07f6f739195`.
Validated lowercase64hex owner order equals Rust's binary owner ordering; numeric
group-index order and local-spec group order then match unchanged relation
bindings. Duplicate imported keys refuse. The pure retained-export helper decodes
actual local proof material, requires exactly the prior local spec and exact
context-to-parent-opening group map, verifies supplied body commitments, preserves
every other witness/packet field and changes only final witness rows. It neither
loads a saved acceptance flag nor revives an old live handle.

No blocking source finding. Exact fixed foundation and retained input bytes must
be selected/pinned by the forthcoming harness; preparation output remains fully
untrusted until independent cold receiving. No author/proof rerun or checker
weakening is authorized by this review. Actual corrected bridge qualification
and future ordinary authoring02 integration remain separate from source clearance.

### Actual ordinary-source return01: retained FAIL and independent diagnosis

Root session54525 terminated exit1. All262 independent bindings match:43
canonical and43 snapshot source pins,36 selection runtime pins, plus140 actual
owner/profile/runtime/fixture pin-and-size checks. Outer RESULT SHA256
`b9f04f725f58b82597b8376dbffb8b7491449b528e30fdfcd4ff3900cadb79cb`;
inner `cca82866f3cf3255c872f4747551c8b7e9d6e0b460589594f345efbef323c699`.

The original real receipt+first native admission succeeds. One ordinary Lean
author produces126 export rows, one four-universe new theorem and one local
group. Independent read-only traversal of the actual exported proof DAG takes
153 expression visits and confirms exactly two references to the first module's
fold_map_received, not just two occurrences in source text. Export5813B SHA256
`268681e0e4193badaa073be369ac062b678ef65123d152780182c448c2f902b7`;
request63616B `17cc96571235788c335e7426e9060f43c5ec42bc0a299d83756b6b37092daf38`.
Preparation retains complete662,480B packet
`40aac3921a49b144c19cb7310679741abbd82bb7d796f05a5a0beb71ee60649d`,
target52c564f87f31082468557df6eed0a04bc7adf9d28d9614fe6cf173f5633088bf,
with one actual receipt frontier and two deltas. The cold receiver's packet is
identical; both first-delta copies are exact88b71b82. All origin owners close
before cold receiving. Cold real receipt and first delta pass; second delta
refuses at CORRESPONDENCE_DESCRIPTOR_RECORD_MISSING, exit2. No new target is
mathematically admitted and no return handle survives.

**Independent diagnosis:** the relation collects imported groups in a BTreeMap
keyed by `(ModuleID, group_index)` and correspondence matches their ordered
bindings positionally against native group rows. DeltaSourceOperation.finish
instead emits frontend `context.imports` in its dependency-topological order.
Actual decoded native group position1 is base.binary_congr, while the relation
expects base.Tree.below. Other base groups are similarly permuted; owners and
names themselves are correct. The earlier source review missed this ordering
incompatibility. NativeRows.group and the mathematical checker are not the cause;
do not weaken correspondence to accept mismatched groups. A fresh successor
should emit witness imports in exact relation order while leaving frontend
dependency order unchanged. Used authoring source/harness/failed evidence remain
frozen; retained source export can support a separately selected bridge repair,
without repeating ordinary authoring or increasing unrelated limits.

All six worker Jobs and outer Job have clean closure/reap, zero final active/
terminated processes and no cleanup errors. Real receipt CPU0.03125s each;
origin first native0.03125s; cold first and failing second native0.015625s each.
Author Job3.625CPU/6.8725487wall, peak488,300,544B. Enclosing46.796875CPU plus
separate1.171875wrapperCPU,56.0269228wall,peak523,395,072B; do not add its nested
workers/lifetime counters again. No network, guest, snapshot or proof ran.

### Actual delta-network-controls01: scoped PASS

All five new controls pass with zero failures/errors. All88 bindings match:
34 canonical source+34 snapshot source+20 runtime pins. Outer RESULT SHA256
`2557246477e83baac75e31f430778f859747b900389aa594a205fba98686fca9`;
inner `632188e968ef3ea75284d07371c2292ded1f082c331a9178869b4eb4019f62e6`.
Worker0.71875CPU plus wrapper0.328125CPU,1.7805488wall,peak28,286,976B. Exit0,
closed/reaped,zero active/terminated processes,no requested termination or cleanup
errors. This establishes the selected SQLite/structural/loopback-byte controls
only; no positive mathematical authority, crypto/native/Node worker, positive
located handoff or global-network/growth result. Used source/tests are frozen.

### Exact ordinary-source delta-author01 selection clearance

Prospectively cleared selection
`159c8c6f8a5350b3d3d113187fba1126dbc4be761923f03193d162a9455e740b`,
configuration `3a923f554528848fa42415c9db165d99c4b50b77c69e40101025fe700a2bd41f`
and preparation profile
`f03b591c6e9e40346028c35b663d4d2c5daaf9a58ec6eb890810f96c6c984a4b`.
All219 pin/size checks match, covering43 canonical sources,36 selection runtime
pins,60 owner runtime pins,40 preparation-source pins and the additional actual
worker/producer/Lean/input bindings. Future snapshot references all map to exact
selected source bytes. The output root was absent at review. No arbitrary old
same-byte origin is substituted for the worker, Producer, helpers or fixtures.

Maximum work remains two real frontier checks, three native relation calls and
one ordinary Lean author, each with30CPU maxima:180 worker CPU total. Outer
420CPU/420wall/3072MiB/cap4 leaves controller headroom; original workflow360wall,
owner300wall,120controllerCPU, one30CPU author,256MiB/512entries storage. Per-call
90wall/1024MiB and inherited inner cap2 remain. The112MiB-plus-request transient
authoring storage reservation fits. Actual owner runtime pins total86,016,597B.
Known Lean DLL/Init pins do not imply complete hermetic olean/OS closure.
No snapshot, guest, proof or network work is selected by this clearance; actual
success, complete cleanup and substantive new proof reuse await terminal audit.

### Complete-packet custody/network source review

Exact structural-controls selection84b83dfdef0dd8d11851bbc89c4be7888af838a2b7c0ea4204f1678f9aecfaf9
is prospectively cleared:34 source and20 runtime pins all match; fresh output
absent. The transitive imported controller/workflow/parser graph is included,
but no Node child, native checker or cryptographic verifier is constructed.
Only the five new controls run under30CPU/60wall/512MiB/cap2, in output disjoint
from delta-author01. The old packet suite is not rerun. Outcome audit is pending.

Read the complete source, including the previously truncated transport middle,
and the revised prospective handoff. Source-cleared exact SHA256 values:

- custody.py `4304e529a15e9249d8ba43f5390e94082d0baad1c55db6fb5b74b4160a1fa27c`.
- transport.py `18c1abda1dca45cd8f5e86c09c4e1b8d5b13d4472931173a1db4a080c0c71d40`.
- test_network.py `39d8c9d28fab9ab1e0a2f0a7852a94f02565deabd64d1f15a7a484d6b019f23e`.
- network_api.md `688fac0a8539b61aed288d1d6a784b4a20250cd96f9d4760a606580f3bde47d4`.

Distinct packet profiles/stores/routes preserve the receipt ABI and never turn
structural custody into mathematical admission. The composite provider actually
serves a formal index and selected semantic groups/bodies, so advertising the
existing index role is legitimate; generic custody-only routing is not claimed.
Packet digests, target summaries, quotas and atomic packet/offer writes are
checked. Cross-database commits remain non-atomic; readback establishes current
selected custody, not future retention or availability of every future body.

Review identified that the first `from_search` draft merely required a nonempty
external prepaid ledger. Its replacement uses exact `DeltaLocatedHandoff`:
the actual fresh reader channel is checked before start, the actual existing
workflow is constructed from exact grants, complete route+descriptor+search
request ceilings and descriptor/search reply capacity are prepaid prospectively,
and the original channel/workflow/budget/adapter/policy/query/deadline identities
remain bound. Only one originating search and one acquisition handoff are issued.
Export acquisition requires a candidate actually seen by that search. Contact
expiry/egress is rechecked. The original reader must remain open/unfailed until
the workflow completes, not be closed immediately after obtaining contacts.

Admission reserves the SUM of all frontier and delta CPU maxima under the same
acquisition budget before actual receiving. Original deadlines, exact live
DeltaVerifier identity and post-admission semantic/packet readback are checked;
failed finalization revokes the verifier. Nested reservations are constraints,
not separate actual costs. The inherited600CPU per-admission budget remains.
Application budgets do NOT measure all DHT wire, bootstrap/provider/controller
CPU or framing costs; those still need separate evidence and enclosing Jobs.
Owner Python is trusted; this is not an adversarial-process sandbox.

The five new controls are source-cleared, UNRUN at this review: wire/authority
separation; SQLite reopen/dedup/corruption; transaction/target/profile/quota
refusals; actual bounded loopback byte acquisition and supplier-offline readback;
and unoffered/duck-authority refusals. Their zero-row synthetic packet is
deliberately invalid mathematics and cannot grant admission. They do not test a
positive actual prospective handoff, DHT discovery or real delta admission.
Root must separately select finite exact execution; no old suite is repeated.

### Actual native-delta admission01: independently audited PASS

Root session95240 terminated exit0. Independently checked82 pins:12 canonical
sources,12 retained snapshot sources,27 runtime/input pins and31 exact actual
owner pins; no mismatch. Outer RESULT SHA256
`8faee6c64f9769c807f22138c177c5aad1b8a04b955db78bcfd01d85a6f77132`;
inner `40ff77e5cef75870b79041236488d7297c08035c1405ab0ddb361f0f3fd8c91d`.

The actual host fully verifies base receipt850c33b2 under the adopted image and
policy. The native driver's sole parent journal is byte-equal to that actual
frontier output. Its actual113,220B child input is exactly88b71b82; its computed
184B child journal equals retained expected07734789. The real receiver admitted
child4adbc049, opened child and base groups, exposed the correct distinct two
member proof forms and exported the exact560,792B complete packet SHA256
`a6a1fc259a154a82c489b536ee5bee91b22cf476d8da8fe9d0f12732a07ee3b8`.
This is real conditional-native-plus-certified-frontier admission, not a saved
report substituting for mathematical authority or a newly minted child receipt.

Packet-cap and missing-frontier controls perform no native/receipt work. The
negative native witness differs from the positive bytes ONLY by the unique
theorem proof reference1200 becoming type reference770. The checker reaches its
actual definitional-equality assertion, which the driver catches and returns
as REFUSED (`CHECKER_PANIC_OR_UNRESOLVED_DEMAND`), exit2. This establishes genuine
native refusal without claiming that every such generic refusal proves falsity.
It is not a timeout: closure/reap pass, no termination was requested, and final
active/terminated counts are zero. The earlier positive handle is revoked; every
owner is finally closed with zero live handles. The fabricated handle also refuses.

Actual worker CPU is0.03125s each for real receipt, positive native and negative
native; their wall times are0.7318819/0.9369466/0.1371026s. Enclosing Job CPU8.125s
already includes all workers and controller activity; add only separate outer
wrapper0.46875s, not overlapping lifetime counters. Outer wall10.7333411s, peak
private commit94,916,608B. No cleanup errors, guest, proof, source author or
network calls. This closes only the selected real admission/changed-boundary
gate, not ordinary delta composition, network circulation, net growth or v5.

### Ordinary-source two-delta return harness: source clearance

Read all of `delta/author_actual.py`, SHA256
`a9897ec4a4380cf5b34404ac4a1cbae0b35d4764ea783d22ad5bd3e08d0a17a9`,
the exact DeltaFoldMapTwice source/root fixture and its called public delta
authoring/preparation methods. No blocking source finding. The harness imports
the retained first delta through an actual cold receipt plus native relation;
creates one four-universe ordinary-source theorem using that first theorem twice;
inspects the actual exported proof/value closure for at least two first-theorem
occurrences; and retains exact first witness plus the new witness above the same
genuine base receipt. The returned packet remains untrusted until admitted.

Every originating operation/session/preparation/delta/frontier owner is closed
before a distinct cold recipient verifies the full packet, opens the new group
and exports identical onward bytes. Final owner reports follow cleanup; cleanup,
deadline, source/runtime/configuration changes and late reporting failures override
success. Maximum two receipt calls, three native checks and one ordinary Lean
author; no network, guest, snapshot, sealer or new negative campaign.

This is source clearance only. Exact future-snapshot helper paths (`actual.py`,
`authoring/receipt_integration.py`, this harness and their actual imported graph)
must be included in both applicable profile and runtime selections; inherited
same-byte paths are not sufficient. Root owns the finite configuration/launch.
Actual mathematical success and any full-cost benefit remain unestablished here.

### Driver02 actual audit and exact delta-actual01 clearance

Driver02 completed compile-only PASS. Independently checked all 196 current
bindings: 11 canonical files, 11 retained source snapshot files and 174 runtime/
evidence pins, with no mismatch. The seven compiler warnings are unused imports,
functions or constants, not compilation errors. The executable is 1,713,152B,
SHA256 `37a0af1b08e7176fb0d387b3e8439266d7c2c0befe5b08bc3cdd4c90c62d3e40`.
RESULT SHA256 is `e655d48f89b102e3e41285e6c8dc6594e81b6954f0efcc3b0e2452ff7be99879`.
Compiler exit0; final Job has zero active/terminated processes, no cleanup
errors, and observed exit of the exact selected owned VCTIP helper. Worker CPU
43.59375s plus outer controller CPU2.265625s; the latter includes main controller
CPU, so do not add it twice. Outer wall50.5353079s; peak worker commit746,483,712B.
Report-writing/exit tails retain their explicit accounting exclusions. No
mathematical native check, guest, proof, network or dependency rebuild occurred.

The exact delta-actual01 selection
`f9315f53a9d515ea4f2fd6ac2c33ef0dbdf3ac4a93d5b8ce914663a5b971344c`
and config `7f5b305b1c2977157f90052de965e6831d9641015ba1364532fc921cd6983868`
are prospectively cleared. All 70 checks match:12 canonical sources,27 runtime/
input pins and31 owner runtime pins mapped from exact future snapshot paths.
The output root did not exist at review. Reread the complete actual.py; it
extracts producer configuration fields from the earlier preparation profile
only and never instantiates Producer or OwnerPreparation, so it does not load
the old source-pin origins. The current imported graph and adopted supervisor
manifest remain separately pinned.

Outer budget300CPU/300wall/3072MiB/cap4; original operation wall240; native and
receipt reservations30CPU each. The reviewed one-receipt/two-native maximum,
real clean native negative and final closure requirements remain unchanged.
This clears root selection of one operation, not any assertion of runtime
mathematical success, scalable network operation, growth benefit or release.

### Delta ordinary-source authoring successor: source review only

The separate actual-receiver harness `delta/actual.py` is source-cleared at
`960773b95e1a7cf5f273174f938bcd1c67cef1715b6717494c6993b34e8bebe4`.
It binds retained ordinary-source child88b71b82/expected journal07734789/base
receipt850c33b2, with no source authoring or guest/proof repeat. It selects one
genuine cold frontier admission and one native child admission, opens target and
base member interfaces, exports exact complete onward bytes, rejects a fabricated
handle, then reuses the SAME verified frontier for a native ill-typed-proof
refusal (only actual theorem row value1200 changes to type term770). It requires
nonzero native exit with clean closure, not timeout, and observes prior-handle
revocation. Separate packet-cap/missing-frontier refusals must invoke no worker.
Maximum actual mathematical calls: one receipt and two native checks, although
conservative reservation accounting is intentionally larger and failed native
cost is separate from observed-success worker CPU.

Review corrected the pre-close evidence snapshot ambiguity: final primary
owners/receipt_owner reports now follow close; separately labeled before_closure
preserves the old observation. Cleanup errors and expired original deadline
override success, including after final report write. This is source clearance
only; exact built-native/config/runtime selection and actual evidence remain
root-owned prerequisites.

Read the complete fresh authoring.py33,655B
`bf3f266c0ba2e3ebd2079bb33fac067e88f1309172bc3985a2a92c034e58627e`
and authoring_api.md5,657B
`d7da7e974d5a1b7682a9e6445affdb1ef628093e55903a9924790b36405e1d71`,
then compared the actual frozen context/source/NativeRows/model/OwnerPreparation
APIs they call. No blocking source defect identified; no code executed.

DeltaImportSession requires the exact live originating DeltaVerifier and real
registered VerifiedDelta handles. Parsed packet payloads must match the actual
accepted member inventory, exact journal and proof form. Multi-handle composition
conservatively rejects alternative journals, receipt/witness bytes or forms for
the same module. Opened group commitments and supplied semantic body hashes are
bound; the session's operation selection includes original packet identities.

The ordinary frontend receives only selected interfaces and needed semantics,
plus the fixed foundation, through the unchanged request schema. Its absence of
ancestor theorem proofs does not imply their disappearance from onward evidence.
SourceOperation decodes actual export declarations, checks census/root/source/
selection bindings, emits native rows through actual NativeRows.group methods,
and forms a complete untrusted child witness. It does not insert a fake receipt
or an ImportClaim with invented receipt authority into existing receipt-only APIs.

Onward construction traverses exact parents into the accepted closure, includes
every required uncertified ancestor once, preserves actual receipt frontiers,
orders delta witnesses by checked rank and appends the child last. Unneeded
branches may be pruned; missing required material refuses. The same aggregate
packet parser applies; a larger optional Envelope cannot override the narrower
canonical/native codec domain. Child acceptance still requires independent
native/receipt verification, not successful source preparation.

DeltaOwnerPreparation reuses original owner allowances, worker/config/process
bindings and failure accounting. It reserves storage for native export plus full
packet, pins the final saved packet, and uses the original _call completion
callback after report writing/census and before return to revalidate the live
source origin, bindings and deadlines. snapshot() explicitly refuses. Its local
profile must include the actually loaded authoring successor and transitive
source closure. No actual native author run, second-delta admission, reciprocal
network return or v5 release follows from this source-only clearance.

### Native-delta source and build-proposal review

**Actual build01 FAIL; compatibility-review miss preserved.** The single selected
build exited1 with Rust E0432: retained native-library01 has no
`nanoda_lib::parser::decode_corresponded_owned_row`, required by current relation
source. Its preserved parser snapshot contains `parse_owned_rows` but not the
new owned decoder. Thus the earlier hash/overflow/source review did **not**
establish API compatibility; this reviewer should have compared the library's
actual compiled source snapshot with the relation's imports before clearance.
No native_delta.exe exists. All eleven build snapshot pins match. Root and the
source owner now investigate an actually compatible retained x86_64 checker or
a separately selected fresh build; no rerun, budget widening or fallback to an
older relation is implied.

Actual evidence independently checked: build RESULT
`5aeb9c2729feea819d4400a8206308737fa303ca2a55dcc1a807e644f35d8bb0`,
attempt `e7f39f21fa13fb213b9f4357ac0b56a0d89488dfa0bb0fe002f9df21f2d37f72`,
stderr `bfc149a0bc647aa75f248544334095fea152120697781010231d98a77fee4539`.
One command, no guest/proof calls; Job closed with zero active/terminated and no
cleanup errors or telemetry cleanup. Worker0.734375 CPU, peak629,358,592B;
inclusive controller1.703125 CPU and total observed8.0823074 wall. Main and
attempt controller CPU are the same enclosing cost, not additive. Raw failure
is retained even though process containment and evidence closure succeeded.

Separately, the nine structural controls' exact selection
`c8cc86ce63e63daecc421ce90e7c80362eb50a3e207813faecae1969eb066ae1`
was reviewed before launch:12 source+3 runtime pins independently match, fresh
output,30CPU/45wall/512MiB/cap2. Updated test source
`d16c545bd084c10a9183ba7c65c61b840e9a45f66841119efaf36b15a842d1eb`
adds the fractional telemetry regression to the existing ninth group; its
finite-float local report passes while mathematical JSON refuses decimals.
No positive authority/native/cryptographic call is made by these tests. This
was launch clearance only; terminal outcome is now independently reviewed below.

**Actual delta-packet-controls01 PASS (structural only):** all nine named tests
pass with zero failures/errors in retained stderr and inner RESULT. The updated
fractional-telemetry case is included.27 independent post-run hash checks
(12 canonical sources+12 snapshot sources+3 runtime pins) match. The sole Job
exits0, closes/reaps, ends with zero active/terminated, no termination request or
cleanup errors. Worker0.46875 CPU plus enclosing wrapper0.265625 CPU (do not add
its included0.015625 supervision CPU again),1.1253214 wall, peak24,547,328B.
Outer RESULT `df2023331f82673a8d68844fe4d2cf9d98500c69f3d12b555f6e3977ec283ded`;
inner RESULT `a1c7876e53e5baec0e6d73ba7f64cb9bbee49edc7a6cea4dac45adb9826f452b`.
No native/checker/proof call or positive authority exists. Used packet/receiver/
test bytes are frozen; no passing campaign repetition is warranted.

**Fresh native-library02 selection cleared:** exact proposal and copied selection
`7941f68e3615e7bb1119aa0083ce0cc73525e4b8e978f72ab4e596ba446b2cae`.
All27 source and68 retained runtime pins independently match. The26 actual checker
files additionally match both guest05's compiled source snapshot and its
SOURCE-MAP.checker entries; guest selection5da04eb9/mapdf3d2f88 hashes match.
Current parser7a183a1c exports the required owned decoder and parse_owned_rows;
current lib.rs exports parser/module/correspondence modules. This comparison
addresses the actual earlier source/API mismatch, without changing checker code.
The direct rlib-only argv is exactly library01's previous argv (eight retained
externs, overflow=yes/panic=unwind/opt2). Fresh output,90CPU/120wall/2048MiB/cap4;
no linker, Cargo, guest, proof or dependency rebuild. This is prospective build
clearance, not a compiled artifact or universal native/guest equivalence. Driver02
must bind the actual successfully built rlib hash in a separate fresh selection.
The source owner, not this reviewer, performed the disjoint retained-library
census; no duplicate census was run.

**Actual library02 PASS; driver02 prospectively cleared.** Independent actual
review rehashed122 canonical/snapshot/runtime inputs with zero mismatch. Compile
exit0, no stderr, closed/reaped Job, zero final active/terminated, no cleanup
errors.42.53125 worker CPU+1.03125 wrapper CPU,14.1900198 wall, peak444,993,536B.
Actual rlib11,303,166B:
`ba6d0db2e614c2bb032ca5d92d97d31a7ebfe87f85fa6cce6fe5549483b7c651`;
RESULT `916e05e1118a28b289cd2224a06df2fe5a15f30c85be58f8b692ea03add53600`.
No native driver or theorem check follows from this library build alone.

Fresh driver02 source500c6b35 equals reviewed build01 source under only documented
docstring/output/attempt/proposal/self-path replacements (exact byte comparison
after substitutions). Selection
`031f526e5b8077652e85d6b7ffbb84ff8e9db1549f40359345f46e03f5545d66`
binds proposal
`b0d037459b950c3cbabd1c2554aebf1fe9611820598d370eb40f4d69e700885d`.
All183 proposal pins (nine sources+174 runtime/evidence entries) independently
match. The only compiler argv change is the actual new library02 path; its rlib,
RESULT and selection are pinned. Output and attempt are fresh; original
240CPU/300wall/3072MiB/six-active bounds and reviewed telemetry cleanup remain.
One fresh root launch is cleared; failed driver01 remains failed and preserved.

**Exact build01 selection cleared before its failed launch:** final driver
`b84db1f4ff776b3a3fcd0a4396af3a4ea7e50bb28bdb27dfa107b9c38797347d`
and selection
`4b7b64c22f93f207dd60cb2967d46db2e3ca0db57335a8555168d81e4dd91139`
bind the unchanged proposal below. Complete helper lifecycle review confirms
the exact factory installs240CPU/3072MiB/six active despite the adopted Phase
constructor's default call shape. Phase wall240 is within total300; combined
logs1MiB and controller60CPU/output1GiB8192entry sampled bounds remain finite.
Owned VCTIP cleanup validates exact Job membership/image/hash only after direct
compiler exit0; unknown descendants refuse. All final close errors override PASS.
Seven helper hashes, D:\Python314 executable/DLL and VCTIP hash independently
match; output and attempt paths were fresh. Eleven snapshot sources preserve
the relation's source-relative paths. Review requested explicit final-write/exit
tail scope labels, now present in both main and enclosing attempt reports. No
claim of fully hard wall/disk enforcement follows. This clears one compile-only
launch by root, not a runtime success or mathematical admission.

Independent complete source review finds no blocking defect in the new driver,
packet parser and owner receiver, including the actual-closure member API. This
is source clearance for separately selected build/controls, not an executed
positive admission. Exact reviewed implementation hashes:

- native.rs: `66d5c58a99cccab4ffe1c53264fd1ae1eb0941c15dcadff0a54ef2844caa664e`.
- packet.py: `3ebd338998acefa7808695ec4a0f5320d15a6893b8c339243af21afad456c0f3`.
- receiver.py: `418708346600bff17d2a8425fb9ca322d8eeb9e6a0ad97a6d63c5637bd4df120`.
- test_packet.py: `f7b1279b6d9b34dac385b5b1bbb4eb9224eca7b71c3cb59d688006bcc425c27c`.

The native driver calls unchanged relation3625bc9c, encodes its computed journal,
then checks its own image/foundation/policy even for zero-parent witnesses. It
returns computed exact parent journals with explicit conditional-only status.
The owner obtains frontiers only through the exact originating ReceiptVerifier,
checks complete journal-byte equality rather than ModuleID/rank alone, and adds
each computed conclusion only after all parent premises have already been
established. Strict exact rank and topological order prevent circular support.
No-extras/reachability use that actual checked graph. Immutable packet bytes,
same-call input digest, runtime/source pins, original deadlines and real live
frontier handles are rechecked before final promotion. Saved JSON cannot mint
authority; the opaque VerifiedDelta registry is distinct from VerifiedModule.

Members are drawn from retained tuple(graph), not a remote inventory. Their
copied descriptions/openings remain under the one accepted closure handle and
its originating live frontiers; no fabricated receipt handles are introduced.
The complete original packet is retained for a cold onward receiver. Aggregate
packet/receipt/witness/node/depth/row/edge/opening/body budgets prevent replacing
an ancestry limit by a depth-only bound. Attempts, input bytes and conservative
worker reservations survive failures; observed-success CPU is explicitly partial.
Operational telemetry uses the finite-float local parser, separate from strict
integer-only mathematical input and native output.

The nine source-reviewed structural controls create no positive authority and
make no native or cryptographic calls. Actual selected-child acceptance, wrong
frontier/target/proof/body refusal, a second delta and final-lifetime controls
still need concrete evidence. The fixed native parser may impose a smaller
supported domain than optional larger Envelope ceilings; those cases refuse
conservatively, not complete more cheaply. Jobs are resource containment, not
hostile-source isolation, and output sampling is not a hard disk quota.

Build proposal
`bdd23d50c7e45906e84cda6167f1ea6bf73c25a6b4cfae31924674998258d021`
was independently rehashed:9 sources plus172 retained runtime inputs, zero
mismatches. Its65-argument direct rustc invocation targets x86_64 Windows,
overflow-checks=yes/panic=unwind, reuses existing dependencies and checker rlib,
and does not rebuild dependencies, execute a guest or produce a proof. The
retained native-library01 selection also compiled the checker rlib itself with
overflow-checks=yes/panic=unwind; final-link flags alone would not establish that.
Proposed finite build limits240 CPU/300 wall/3072MiB/six active are not enlarged.

The proposal is **not a launch selection**. Root's fresh supervisor must use
reviewed exact owned VCTIP cleanup and finite-float telemetry, preserving the
prior generic build's failed descendant lifecycle instead of repeating it.
Actual compiler/dependency/architecture correctness remains in the receiver TCB;
shared relation source is not a proof of native/guest semantic equivalence.
Current cryptographic profile2 still requires real receipt parents and cannot
seal an arbitrary uncertified delta DAG merely because native checking passed.

### Actual receipt/source integration01: successful prefixes, failed snapshot

Independent terminal review of root session93713 is complete. The overall raw
operation remains **FAIL / exit1**; this is not a child admission or completed
integration. All 37 selected sources were rehashed in both canonical and frozen
snapshot locations, plus all 33 runtime/input pins: **107 checks, zero mismatches**.
Selection6efbbc8e/profilecd7a4bfa/config8199b31a remain unchanged.

The genuine fresh host receive returned `REAL_MODULE_RECEIPT_VERIFIED`, fully
resolved, profile2/current image04/current foundation and policy, rank0, exact
base module2b54d3be. Both copied receipt files (receive and parent-0) equal the
223,594B final base receipt850c33b2. Same-call binding and the reviewed live
verifier/session path support actual base admission, not merely saved receipt
production. All authority was closed at the end (zero verifier live handles).

The actual native author returned zero and exported526 rows / one local theorem.
An independent read-only traversal of the saved export expression DAG, separate
from the harness census, finds the admitted relocated `binary_congr` in the
theorem proof and Tree/fold/map in its statement. Its canonical child has one
group and1355 rows, module
`4adbc049e4d1e29ec045d64c7dba9e27bdd506dfa6c7fb707f022be40439e742`.
Only committed imported interfaces/needed semantics were supplied; imported
theorem proof ancestry is absent, while fixed foundation proof data remains a
separate supplied input. Ordinary-source authoring is genuine selected-interface
reuse; it is still not independent child mathematical admission.

Host preparation returned `PREPARED_ONLY_NOT_CERTIFIED`, rank1. The sole parent
journal in the retained child input equals the full184-byte journal from actual
base receiving. Expected child journal is184B, profile2/current image, one group,
rank1; the frame is retained113,224B. Snapshot then exited1 with precisely
`Session limit exceeded: 33557665 >= 33554432`. No child.snapshot capsule exists,
no child receipt/proof was created, and no child handle was granted. This is a
clean cycle-limit refusal, not evidence that the child relation passed or that
an additional3,233 cycles would suffice to complete it. Do not rerun receipt
admission/authoring or enlarge/restart this failed snapshot by implication.

All four inner stages and the outer Job report zero final active processes,
reaped direct children, closed Jobs, no termination request and no cleanup errors.
The real positive author fits unchanged concurrent cap2 (total process count3).
Selected observations: receive0.015625 CPU/1.8135803 wall; author4.15625 CPU/
30.398877 wall; prepare0.109375 CPU/0.6890074 wall; snapshot2.125 CPU/1.5943692 wall.
The enclosing Job costs13.515625 CPU, peak521,482,240B; outer measured wall is
44.0268633 seconds. Outer wrapper1.0 CPU is separately recorded. The13.515625
already contains the inner worker/controller costs; do not add them again.
Owner allowance closes with2 calls,6.390625 charged worker CPU and known closure.

Retained audit anchors (SHA256):

- Outer RESULT: `76f6fae8a4dbb3aa8f188736933617a050f4ac4867e9d6ca47426c783837adea`.
- Inner RESULT: `54c48e050860bafb98cbe20b16f173f122e1ad3b3c0e134cad3cde26dbfd4282`.
- Actual export: `36278b75e0a12a0cf92d40510730503a49e2285b316ded674c10af0bd7621d2d`.
- Actual source request: `72208ac51a8794b888ac6d37d3f443175753e66c2c9e2fb3e0f42e4bc75d5f10`.
- Child frame: `dade9928001af41562d5471187fd9d149805e98bd6efdd06511b5e6a5a4c9fea`.
- Expected journal: `07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da`.

Disposition: adopt only the successful real-receipt/imported-source/preparation
prefixes and the clean failed snapshot evidence. Retained child input/frame are
untrusted reusable data for a separately selected native-delta path. Full v5,
independent child admission, onward reciprocal circulation and full-cost growth
remain open. No runtime was launched by this reviewer.

Root has now relayed the user's explicit resumption of real v5 implementation.
The guide/pause paragraphs below are historical. This reviewer again owns only
independent source/preflight review and this checkpoint; root alone selects and
runs finite operations or mutates Git. The still-unrun receipt integration author
is finalizing the harness. No frozen owner/worker source is edited by this lane.

### Process-envelope reassessment

Do not infer a required cap of three from a total-process count of two. The
retained base-production audit also records two total processes for direct host
stages, whose command is a single native executable with no Python worker in
that Job. The worker-control harness has no deliberate real Popen outside its
mocked native calls. The source does not identify an additional process or prove
that it overlaps the native worker child. A source successor raising the cap is
therefore not selected merely on speculation.

Recommended discriminator, if root selects it: unchanged worker plus unchanged
native frontend, exact runtime pins, same cap two, one tiny deliberately malformed
owner request under a fresh short finite allocation. A parser-specific native
refusal with direct reaping, no deadline/Job process termination and final active
zero would establish the actual worker/native launch shape fits the current cap.
It need not redo a mathematical control or receive any certificate. The expected
nonzero child outcome must be distinguished from process-limit failure. This is
a proposal, not runtime clearance or an executed result.

### Initial draft findings sent to author

Validate all later-phase finite limits before spending real cold-admission work;
protect producer host/Python/runtime pin paths in output-overlap preflight too;
retain original deadline through final report writes (with a failure override
if needed). Actual imported-source paths and full source closure must match the
root's immutable selection. Final source review awaits the author's corrections.

### Stable receipt-loop source review

Read all of the corrected 21,755B `authoring/receipt_integration.py`, SHA256
`f0d2697fc6e769d93643c2bfd1b1917e324408540aa5a862775fa316e47f4702`.
**No remaining source blocker found for the selected integration scope.** This
is source clearance only: the cap-two worker discriminator and exact complete
source/runtime/profile/enclosing resource selection remain required before root
chooses a launch.

The harness prevalidates all later grants, constructs the exact adopted owner
profile before spending receipt work, protects all producer/runtime/source input
paths, and starts every local lifetime within one nonrenewing outer wall bound.
It invokes actual receive once, carries the exact live handle/receipt into the
same ImportSession, opens the pinned current semantic bundle, captures the actual
prepared request, and uses the same SourceOperation for ordinary authoring. It
then inspects actual exported proof-value closure for imported binary_congr plus
the Tree/fold/map statement interfaces; it does not rely on source spelling.

The sole exact real parent receipt/journal passes unchanged to the existing
parent-aware snapshot API. Result types explicitly remain untrusted child/prover
data, not child mathematical admission. Input pins are rebound, owner/session/
verifier closure is attempted, failures/unknown accounting retained, and a late
final-report write produces a failure override/nonzero exit. Output and work
accounting retain sampled limits and exclude final tails rather than claiming
hard quotas or double-counting nested controller CPU. The enclosing Job must
also be large enough for actual nested worker/native processes and CPU.

### Actual cap-two probe: failed harness, sufficient retained launch evidence

Prospective clearance was for harness
`8261679860ff393f4f718fb967224c1c8e6fc7e67e7f96a3ea72d7c392ce831b`
under selection
`b0254716a6fa7b1a2cadba67456d6a9d8da580992a59c3ae65f30e1941fc26f5`.
Review required the actual BASE cwd/environment (not project-root cwd), explicit
final resource bounds despite expected nonzero status, and exact worker-report
bindings. All three snapshot source and 24 runtime pins matched before launch.

The root's one selected run ended **raw harness FAIL**. The harness called the
adopted integer-only `supervisor.strict` reader on operational telemetry that
contains floating wall/deadline values. It raised NONINTEGER_JSON_NUMBER after
the inner process and worker report had already been saved. This preflight miss
is preserved, not repaired in used source or relabeled as a passing campaign.
The inner harness RESULT was never written. No native output/export exists.

Read-only independent evaluation of **all ten originally encoded predicates**
against those retained artifacts gives true: expected worker refusal, same-call
worker binding, actual native parser reached, native reaped, no timeout, exact
worker diagnostic, no mathematical promotion, clean whole-Job closure, all inner
resource limits, and unchanged inputs. Additionally checked exact deadline
equality and the unchanged inner active-process cap of two. Rehashed every
snapshot source/runtime pin after the run with zero mismatches.

The actual native stderr is `OWNER_AUTHORING_FAILED AUTHOR_REQUEST_SCHEMA`.
Worker records code 1, `WORKER_NATIVE_REFUSED`, direct reaping and no timeout.
The inner Job records 0.78125 CPU seconds, 6.5493266000412405 wall seconds,
28,655,616 peak private-commit bytes, total processes 3, final active 0,
terminated 0, no requested termination, no cleanup errors, direct reaping and
closed Job. These satisfy unchanged 10 CPU / 20 wall / 512MiB / cap-two limits.
Total process count is therefore demonstrably not the concurrent process cap.
The identity of the additional sequential/transient process remains unproven.

**Disposition: sufficient posthoc evidence for this actual worker/native launch
envelope only.** Do not rerun this already observed boundary or widen the cap
merely to obtain a green harness report. Actual positive authoring is still a
separate integration endpoint. The failed run remains charged: enclosing Job
1.453125 CPU plus outer wrapper 0.6875 CPU, 8.306573099922389 outer wall. Inner
Job/controller costs are contained in that enclosing Job and are not additive.

| Retained item | SHA256 |
|---|---|
| Outer failed RESULT | `b700bf6fd2d7844ef8d99a7d1d8290ba5937ae2b52d7ac36a0f7fe204f71f111` |
| Inner process | `1a295c7d8d4bbfa7ca830d7bd229993432940add46abdda440b603841300053a` |
| Worker report | `bbeaf282a4e3882c9259fb3dde067ad722b0f190d664b571830dc7e7b1596263` |
| Worker config | `651d4708bf0a6c7b70e738eed104b8159bb74eba83d079126424d180c17fc46d` |
| Native stderr | `f254442a5f0cd4e1657162086b97a8ac42381718cb0ec903a71a82da06063bf3` |

Source reinspection confirms receipt_integration and OwnerPreparation use
`production.producer.parse`: duplicate keys and nonfinite JSON constants reject,
ordinary finite decimal telemetry is allowed. Their mathematical object readers
remain separately integer-restricted. The probe's specific reader bug is not
inherited by the pending positive integration path.

### Exact genuine receipt/source/snapshot selection clearance

Independently cleared the following bytes after full source and pin review:

- `receipt-source-integration-01-selection-draft.json` SHA256
  `6efbbc8e43a8704b3f8650ec9b21f589180ecd671e6d21c18152109db994b659`.
- Profile SHA256
  `cd7a4bfac290a717f20af1a00d8e6f1a87939ea8ba7d3203b38d21bea291e56e`.
- Configuration SHA256
  `8199b31aadb0ddce3ca0ba683679b793b3bfac404bd0cdce28a4b58ff552f36e`.

All 37 source and 33 runtime/input pins match actual current files; the future
output does not yet exist at review. The profile's 34 Python files cover the
read local import graph (including transport/discovery dependencies transitively
imported by ImportSession). Namespace packages without an initializer require no
invented initializer. The actual Producer/Owner/worker source paths are the exact
future snapshot paths, not same-byte files imported from another location.
Supervisor helpers are additionally adopted through the pinned release manifest.

Known Lean runtime pins include the five shared DLLs and Init.olean, not a claim
of complete hermetic transitive olean/OS dependency closure. Host03/image04,
current-policy semantic bundle, exact final base receipt, foundation and the
ReceivedFoldMap source/roots all match the selected identities.

The outer allowance is 600 CPU / 600 wall / 4096MiB / six active processes.
Integration wall is 540; owner/session wall is 480 clamped to the original
remaining time. Owner stages reserve 30+15+240=285 worker CPU against 300;
controller lifetime CPU is 120. One receive reserves 30 separately. The selected
1MiB receipt-session cap exceeds the actual 223,594B receipt. Native authoring,
prepare and snapshot remain separate finite stages with unchanged inner cap two.
Snapshot is one execution with unchanged 2^25 cycles/po2=18; no warmup or proving.

**Clearance scope:** root may select this one cold-base receipt → same live
ordinary-source operation → one real-parent child snapshot attempt. No new
child certificate, fresh child receiving, network loop or final v5 release is
implied, and no automatic retry or renewed allowance is cleared. All mathematical
and operational outcome claims still require the saved actual evidence.

**Assignment redirected before runtime:** root clarified that the latest actual
human request was the full theoretical architecture guide followed by a pause.
The integration findings below are preserved as source-only notes, not current
implementation/preflight authority. No runtime, source successor or integration
selection was launched. The completed guide review is GUIDE-ASSURANCE-REVIEW.md.

## Scope and current disposition

Independent source/selection review of the genuine cold-receipt → live imported
interfaces → ordinary Lean author → parent-aware child snapshot path. The root
owns all runtime selections, launches, adoption and Git. This reviewer runs no
proofs/tests and changes no used implementation or evidence. Base-production
outcome review belongs to the separate BASE-PRODUCTION-AUDIT assignment.

Canonical workspace guard passed. Read the canonical AGENTS/GOAL/NOW and current
WORK selection; older pause/live entries are history after explicit resumption.
Full v5 remains unfinished. This note is not public deployment qualification.

## Source-derived obligations

1. `ReceiptVerifier.receive` must really invoke the adopted host with the actual
   final receipt and exact image/module/foundation/policy. Saved reports, expected
   journals, snapshots and synthetic handles are not substitutes. `ImportSession`
   must use the exact live originating verifier and exact receipt bytes.
2. Open the current `receipt-prepare-01` semantic bundle, not the old-policy fold
   bundle. Bind its summary to the actual receipt. Open groups and supply only
   committed bodies using public session methods. Foundation proof bytes are a
   fixed separate input; zero imported-theorem ancestry is not zero foundation.
3. The same `SourceOperation` must remain bound to its original session, verifier,
   deadline and selection through native return, `finish`, report/census and
   public return. Existing source and preparation controller enforce these
   boundaries, including final callback and overriding late-failure marker.
4. Actual exported local proof data must reference the admitted module's
   `binary_congr`, and the intended Tree/fold/map interfaces. Source text alone
   is insufficient to prove actual reuse. Derive local IDs/counts from export.
5. `OwnerPreparation.snapshot` serializes exact untrusted child input and separate
   exact parent receipt bytes; the host independently reverifies the parents.
   Its frame/journal/profile/rank/openings and returned capsule/assumption census
   must bind. A capsule is not a final receipt or positive child handle.
6. Final child certification/cold admission, return discovery/availability and
   complete-workflow economics remain distinct unfinished endpoints. Do not
   promote this integration into those claims.

## Process-cap compatibility — unresolved before launch

The frozen preparation controller's `_limits` fixes two active Job processes.
Its author stage starts a Python worker that starts one native frontend. Prior
`author-worker-controls-01/RESULT.json` reports total processes **2** despite all
native Popen calls being mocked; actual `author-lean-controls-01` reports total
processes **7** for the Python runner and five sequential native invocations.
These observations support an additional process but do not establish its
identity, overlap duration or maximum active count.

Read-only review of adopted `operator/commons.py::supervise` finds a direct
`CREATE_SUSPENDED | CREATE_NO_WINDOW` launch, assignment and resume; it contains
no explicit helper launch. The selected Python executable is the normal 106,208B
Python 3.14.6 executable, with no visible `pyvenv.cfg` at its runtime root. This
does not eliminate Windows/runtime helper behavior. No probe was launched.

**Do not clear cap two solely from the intended process graph.** Root may select
one bounded process-tree discriminator, or a separately frozen minimal successor
with explicit author cap three while retaining all other CPU/wall/memory/output/
binding/closure limits. Existing owner source is used/frozen and cannot be edited
in place. A larger cap alone would not establish hermeticity or a sandbox.

## Pinning and environment

- Owner/Producer minimum source lists are not a complete dependency closure. The
  integration selection must pin all actual imported v5 modules and the adopted
  supervisor/runtime inputs separately.
- Producer validates actual imported `producer.py` and `__init__.py` paths, not
  merely hashes at another copy. Owner likewise binds sibling worker and required
  preparation/authoring/module paths. Runtime selection must match actual import
  locations, including any immutable integration snapshot.
- Worker reconstructs operation-local LEAN_SYSROOT and prefixes selected Lean bin;
  its inherited path comes from the adopted supervisor. Known DLL pins do not
  prove a complete OS/olean dependency closure. Owner source remains trusted code,
  not hostile input contained by Job resource limits.
- One outer controller CPU observation already includes nested supervision CPU;
  do not add that CPU twice in whole-workflow economics. Worker Jobs are separate
  costs. Lifetime CPU includes idle owner work; original deadlines do not renew.

## Deferred until explicit resumption

A fresh `authoring/receipt_integration.py` draft is retained unreviewed, unrun
and unadopted. No implementation or runtime assignment remains live. A later
explicit resumption must separately select its full source/profile review and
any finite execution; none is cleared or assumed successful by the findings
above. The current assignment ends with the guide review and requested pause.
