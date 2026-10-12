# Exact warrants, shared semantics: public delta and import successor

2026-10-12. Root-selected source/theory work only. No builds, runtime, proof,
network changes or Git by this lane. Canonical root is
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**Current source revision:** the final sections supersede the initial conflict-
only policy: same-J alternate derivations can now be explicitly resolved to one
complete existing/incoming record. No source or control has run in this lane.

## Principle established before implementation

The current legacy journal J is184 exact bytes and includes image, foundation,
policy, ModuleID, group commitment/count and derivation rank. ModuleID M hashes
the semantic summary; it does not include the theorem proof or derivation rank.
Two valid warrants J0 and J1 can therefore share M while differing in rank.

Use two different keys for two different responsibilities:

- **Warrant graph:** full exact J, with its exact already-checked parent Js.
  Every distinct J occupies a node and resource slot. Never substitute a
  same-ModuleID journal or minimize its rank inside an existing witness.
- **Semantic import:** M plus group index, or M plus body identity. Same M
  supplies the same committed declarations/bodies, installed once in the Lean
  frontend. This deduplication does not choose or manufacture a warrant.

An import session retains all needed exact ancestry but requires the caller to
select one explicit already-established J per semantic M for a **new** local
contribution. That selection is immutable within the session. Opened groups and
bodies use M; the new direct parent journal is the selected J. Existing ancestor
witness bytes, ranks, parent lists and checking outcomes remain unchanged.

### Conditional correctness argument

Assume the existing receipt verifier soundly establishes each exact frontier J
and the unchanged native relation correctly establishes a conclusion J from its
exact returned parent journals. Induction over the finite topological exact-J
graph establishes all admitted nodes. Removing the additional prohibition on
repeated M does not change any inductive premise: membership is still exact-J,
every native witness is checked, ranks are still exact, and backward closure
must cover all submitted graph nodes.

For context construction, a selected J commits its semantic summary, and every
selected group/body is authenticated against that commitment. Identical M with
byte-identical summary/opening gives the same installed declaration, independent
of warrant rank. The new witness explicitly names the selected J; it is then
checked independently. No result follows from a semantic ID without its live
exact warrant. Imported theorem validity is not transferred by a saved report.

Aggregate author and independent reviewer confirmed this matches the selected
exact-warrant aggregate-v2 model. The reviewer also requires explicit ambiguity,
complete derivation representation policy and pre-dedup resource charges below.

## Concrete honest mixed-branch case

M0(rank0) and M1(rank1) have identical mathematical interface M; M1 uses a
separate helper H0, not M0 as a forbidden same-module direct parent. C1 uses M0;
C2 uses M1; a later T uses C1 and C2. T's retained ancestor closure contains both
M0 and M1. The old receiver incorrectly rejects that closure by ModuleID.
The successor retains both exact Js; the frontend can install M's declarations
once. If T itself needs an M declaration, it explicitly selects M0 or M1 as an
additional direct warrant for that semantic interface. Neither branch's old
parent J is rewritten. Different ranks alone are not new mathematical knowledge.

## Existing callers and necessary scope

| Existing path | Current behavior | Fresh successor consequence |
|---|---|---|
| `delta/receiver.py::receive` | Graph already keyed J, but separate ModuleID set forbids honest variants | Remove only that extra exclusion; preserve exactJ duplicate refusal and full checking/budgets |
| `members`, `describe_member`, `open_member_group` | `describe_member(handle,M)` returns first matching M | New exact-J lookup; separate variants enumeration. No first-entry selection |
| `delta/authoring.py` and `authoring02.py::DeltaImportSession` | `_nodes[M]`; merges require same old payload/rank | Fresh nodes keyed J; semantic stores remain M-keyed; explicit immutable `select_warrant(J)` |
| `prepare_delta_context` | Assumes one semantic item perM and emits relocated names based onM | Preserve one selected semantic item perM; no duplicate frontend declaration |
| `DeltaSourceOperation::finish` | Parent list derives from session items | Fresh selected items carry exact selectedJ; original native rank/direct-parent constraints remain |
| `onward_packet` | Transitive closure indirectly reconstructed through M keys | Traverse and emit exactJ ancestry without rewriting parent bytes |
| `DeltaOwnerPreparation` | Exact class/source pinning and source-operation lifetime checks | Fresh classes/pins required; unchanged worker and supervision semantics |
| `authoring/imports.py`, `context.py`, `source.py`, `acquisition.py`, `module_dependency.py` | Receipt-only ImportSession deliberately chooses one receipt perM; exact class checks | Remain unchanged. They cannot silently accept new delta or aggregate authority |
| `delta/actual.py`, `author_actual.py`, `network_actual.py`, `network_actual02.py`, retained continuation | Frozen callers use old module lookup/session classes | Stay frozen, not automatically upgraded or rerun. Future root integration must select new API explicitly |

`delta/reprepare.py::emit_relation_rows` stays useful: canonical relation group
order is semantic(ownerM,index), not warrant rank. Its older recovery function's
ModuleID collision rules are not a general new variant API and are not changed.

## Public API and conservative representation policy

Fresh package is `software/v5/delta_claims/`; old delta bytes stay frozen.
Native packet wire remains `DMKN_NATIVE_DELTA_PACKET_V1`: genuine legacy I
receipts plus ordinary native witnesses. This work does **not** reinterpret an
aggregate membership opening as an I receipt. Future aggregate frontiers need
their separately designed live authority path.

Receiver exposes exact warrant facts including the accepted witness/receipt
payload digest. That digest binds the corresponding packet entry to a live
established J; it is metadata, not mathematical authority by itself.

    receiver.members(handle) -> every exactJ warrant
    receiver.variants(handle, module) -> all matching exactJ facts
    receiver.describe_member(handle, exact_journal) -> one exactJ fact
    receiver.open_member_group(handle, exact_journal, opening)

Session interface:

    session.use_handle(handle) -> target exactJ
    session.variants(module) -> available exactJ facts
    session.select_warrant(exact_journal) -> semantic ModuleID
    session.open_group(module, opening)
    session.supply_body(module, universes, expression)

No implicit choice is made even when there is only one candidate. Repeating the
same choice is idempotent; replacing it in a live session refuses. A new session
may make a different explicit choice. Operation selection hashes include exact
selected Js, packet identities and semantic data, so later additions/selections
cannot mutate an already prepared child or silently change its context.

One exactJ may also have different complete proof/receipt representations.
This initial session retains one complete representation and accepts exact
duplicates only if form, payload and parent-list bytes are identical. A different
representation of an existing exactJ yields a typed representation conflict;
the caller can use a separate session or make a separately reviewed explicit
representation selection. Do **not** union different parent edge sets, pick the
first unknown proof, or splice claims from distinct derivations. Supporting all
representation alternatives is deliberately distinct from supporting rank variants.

Counts and submitted-byte charges occur before deduplication. DistinctJ records
count against warrant storage even when M is shared. Context diagnostics report
unique semantic modules separately from retained warrant records; neither is a
useful-growth measurement. Failed and repeated calls remain charged.

## Existing single-witness restrictions remain

The unchanged native `modules/receipt/src/relation.rs` maps direct parents byM,
requires one exact parent J perM, and refuses parent.module==child.module.
The successor must not bypass those rules by changing ranks, importing duplicate
M declarations under fabricated names, or rewriting a retained witness.

Thus mixed variants across different ancestor branches are supported, but a new
single witness naming two direct Js for the sameM is not. Selecting one valid
warrant for identical semantic declarations is an explicit new-contribution
choice, not a theorem that arbitrary old witness parent substitutions are valid.
If a mathematical interface would need genuinely distinct meanings under the
same M, it is a semantic commitment conflict, not a rank-variant case.

## Minimal source changes and tests to draft

Copy the used receiver and corrected authoring02 into fresh package paths;
change only exact-warrant graph/member metadata, explicit session selection,
ancestry lookup and new source/profile identity. Reuse unchanged strict parser,
native checker, receipt owner, context reconstruction/emitter and worker limits.
No source-level checker injection or new accepting callback is introduced.

Draft inert tests for exactJ alternatives, missing exact parent despite another
sameM variant, ambiguous/incorrect lookup, immutable explicit selection,
one-copy semantic groups, complete old-parent preservation, repeated-byte charge,
sameJ alternate representation refusal and single-witness duplicateM refusal.
Fabricated fixtures are bookkeeping controls, not genuine receipts/admission.
Actual mixed-branch native/receipt qualification requires a later root-selected
finite operation and independent outcome audit; no such runtime is authorized here.

## Source draft complete; independent review requested

The fresh implementation consists of the exact-J receiver, inert packet/fact
binding helper, explicit-selection import session and corrected-source authoring
adapter. All receiver handle tuple accesses were inspected after adding exact
representation metadata. The old native relation, parser, actual receipt owner,
corrected canonical-row emitter and ordinary-source worker remain unchanged.
The API explains both rank variants and the separate same-J representation limit.

Nineteen draft controls in `software/v5/delta_claims/test_claims.py` cover exact
identity/rank variants, retained old parents, missing exact ancestry, tampered
copied facts, same-summary frontiers matched by actual evidence digest, exact
receiver lookup, old-vs-new authority classes, required immutable selection,
semantic opening deduplication, pre-dedup repeated charges, warrant capacity,
failed-acquisition costs and merge atomicity, representation conflicts, selection
invalidation after new acquisition, changed live inventory, unchanged onward
ancestor witness bytes and the unchanged direct-parent/rank constraints.

These are conspicuously synthetic fixtures with fake receipt bytes/empty rows;
test-only object construction and method patches bypass verification. **No test
has run.** Even success would establish bookkeeping only, not any mathematical
or cryptographic admission. No old end-to-end scenario is duplicated.

| Fresh file under `software/v5/delta_claims/` | Bytes | SHA-256 |
|---|---:|---|
| `__init__.py` | 246 | `dc919d97068cea9d267b07368d238e4ce7a5689d20439ac5e6d69f7f76bb4987` |
| `receiver.py` | 21395 | `7731f712902b5c5e0869a51c913b335428309760df604768293f7ab58c301bfd` |
| `claims.py` | 3228 | `c880964241e5b0f492ab332b2c694896b3b6efdc638e014b25148bd6410e6564` |
| `imports.py` | 12310 | `74b963e72a39df72eac5bba505cadc529c4c4a948041a6965a1278afa0834a16` |
| `authoring.py` | 22831 | `cc62ebd697d8137f021dbf79feb4e39e41639a8c5864c041da40838469bbc290` |
| `test_claims.py` | 15154 | `a74f5a8cb158e014c28dc825983d9d4043b4994eab23206723210c3bf68524f2` |
| `API.md` | 8439 | `23c9266519af758ee3555b7e6ff21faec72d9988d3a37c5102c55e393834c0c7` |

### Source-selection closure

The receiver's required pins include new `receiver.py`, `__init__.py` and
`claims.py`; frozen `delta/packet.py`, `delta/__init__.py` and its eagerly
imported `delta/receiver.py`; plus the existing admission bindings/verifier,
codec and production controller files. The actual native executable is still
required. Existing owner profiles retain their own transitive source/runtime
requirements; this list does not replace them.

The authoring owner additionally requires every fresh product file including
`imports.py` and `authoring.py`, plus `delta/reprepare.py` and the unchanged
owner/authoring/native worker closure required by the superclass. The synthetic
test source belongs only to a separate root-selected control operation; it must
not be trusted as a product authority module. Constructing an import session
directly occurs inside the adopted local controller, not as remote code execution.

Root owns exact selection, integration, runtime, any controls and Git. This
compatibility repair is necessary for independently developed branches; it is
not evidence of useful growth, aggregate scalability or a complete v5 release.

## Adopted next source revision: explicit same-J whole-derivation choice

Before any runtime, root and reviewer adopt the following strengthening. The
conservative same-J refusal above is a sound default but not an adequate endpoint
for independently produced valid proofs with the same interface and rank.
Earlier source hashes identify the unrun initial draft, not the final revision.

`use_handle(handle, resolutions={exact_J: "existing" or "incoming"})` will require
exactly one directive for each same-J representation conflict between current
selected records and this accepted handle. Missing, extra or malformed directives
refuse atomically. No caller may supply a new proof/edge set through a directive.
Only one complete already-established record is selected for each J; original
payload and exact parent list move together. The other packet remains live and
available for a later explicit reacquisition/choice within budgets.

### Why selecting another derivation of the SAME J is sound

An unchanged native child witness cites its parent J, not a digest of the parent's
particular proof. By construction both complete representations establish the
same image/foundation/policy/semantic commitment/rank. Choosing the other complete
representation therefore preserves the child's exact premise. This does **not**
permit substituting a different-rank J for the same semantic ModuleID.

Let the chosen-record graph contain one record for each exact J. A selected receipt
record is an independently verified terminal. A selected native record retains
all and only its checked exact parent Js. Every edge has strictly smaller rank,
because its original checker established the exact max-parent-plus-one rule.
Every selected parent remains in the union of established records. Induction on
rank therefore establishes each chosen J, even if its chosen parent representation
came from another accepted packet. No cycle, edge union or new proof appears.
For onward emission, traverse only the selected target parents' chosen records;
prune other stored records and emit original native payloads unchanged.

### State and preparation binding obligations

Choice is an atomic local transaction after full exact directive validation and
final liveness checks. Failed calls still consume submitted bytes/call allowance
but do not change stored handles, graph, semantic inventory or selections.
An incoming choice replaces one full record; existing choice preserves it.
Repeated packet submission must not bypass conflict handling, since a previous
explicit choice may have retained the other packet's representation.

Prepared-operation selection binds every chosen graph record's exact J, form,
evidence digest, exact parents and supplying packet identity, not only direct
imports. A monotone representation revision also binds it, so switching A-to-B
and back to A cannot revive a prepared source operation. This detects an
ancestor-only choice change even when all selected frontend declarations and
direct parent Js are unchanged. Semantic deduplication remains independent.

## Revised source ready for independent review (still UNRUN)

`imports.py` implements the explicit directive map above. A repeated packet goes
through the same conflict computation, rather than taking the old early-return
path. The exact set of conflicting Js must match directive keys; values are
only `existing` or `incoming`. Chosen-record ancestor closure is checked without
edge union. All state maps and revision are prepared in locals, then committed
together after the final live inventory and owner checks; no post-mutation
liveness call can create a failed partial merge. Submitted bytes/calls remain
charged on refusal.

`selection()` now commits the complete chosen graph: exact Js, proof forms,
payload digests, exact parent tuples, supplying packets and monotone representation
revision. Revision increases when any existing chosen record is replaced, so an
A-to-B-to-A reversal cannot revive an earlier source-operation binding.

There are now **25 draft synthetic controls**, adding explicit existing/incoming
selection, pruning an unused branch without edge union, exact directive validation,
repeated-packet conflict enforcement, an ancestor-only switch/back preparation
invalidation and failed-final-liveness atomicity. The latter representation test
selects a descendant module while switching only its T ancestor's derivation.
All controls remain unrun and have no real proof authority.

| Current fresh file | Bytes | SHA-256 |
|---|---:|---|
| `__init__.py` | 246 | `dc919d97068cea9d267b07368d238e4ce7a5689d20439ac5e6d69f7f76bb4987` |
| `receiver.py` | 21395 | `7731f712902b5c5e0869a51c913b335428309760df604768293f7ab58c301bfd` |
| `claims.py` | 3228 | `c880964241e5b0f492ab332b2c694896b3b6efdc638e014b25148bd6410e6564` |
| `imports.py` | 14453 | `216f3ce48543ff4638c7112aa16d6dc430f7bc9a04f6927a7d036b81ddee137f` |
| `authoring.py` | 22831 | `cc62ebd697d8137f021dbf79feb4e39e41639a8c5864c041da40838469bbc290` |
| `test_claims.py` | 20982 | `f719bfcaf0e658dac8eeb76b7cce8b365a8da5567563cd37b812af062881860c` |
| `API.md` | 10125 | `abf2fc482658aad9005fc248aa3fb95540d2c69620f9d9c6b3f352a7d5dd06b2` |

No test/build/native/frontend/network/proof or Git operation has been performed
by this subagent. All changes are confined to fresh `delta_claims/` and this
checkpoint. Existing aggregate work and frozen predecessor files are unchanged.
Independent source review is requested before root selects any bounded controls.

## Independent source clearance and finite control-selection proposal

Independent assurance read all seven final files and reported source PASS to
root: complete-record choice, exact conflict directives, graph/revision binding
and atomicity match the argument; all25 controls are explicitly synthetic.
Root instructed keeping these files unchanged. A nonblocking documentation
precision note remains: the API's statement that "all API calls" consume the
allowance refers to operations using `_begin`; `census`, `close` and inert helper
functions do not consume that counter. No runtime or mathematical pass follows
from this source review.

Fresh source-only selector proposal:
`research/cycles/v5-2026-10-12/Select-DeltaClaimControls01.ps1` (6094 bytes,
SHA-256 `bcd410dca0116881b0be34919b3479211beb2a2545e705c9af0eb5bd9330c20d`).
**The selector has not been executed by this subagent.** Root alone may run it,
inspect its resulting exact selection and launch the retained bounded runner.

It proposes a fresh `delta-claim-controls-01` output and create-new selection,
one isolated `-I -S -B` Python worker, and25 synthetic unit controls with30 CPU
seconds,60 total wall seconds,512 MiB,2 active processes and1 MiB per log.
There is no nested mathematical worker, authoring, receipt verification, network,
build or proof operation. Successful output would be `Ran 25 tests`/`OK` in the
retained unittest stderr together with clean outer Job closure, not certification.

The source snapshot has18 files: seven exact reviewed fresh artifacts; ten
transitive/eager Python dependencies; and the unchanged `Run-V5-Check.py`.
The old `delta/__init__.py` eagerly imports old `receiver.py`, which imports
admission verifier and production controller, so those are explicitly included.
Fresh `authoring.py` and API are retained snapshot context but not imported or
exercised by these controls. This check cannot qualify ordinary-source authoring.

Provenance is pinned to the successful earlier native-free packet selection
`c8cc86ce63e63daecc421ce90e7c80362eb50a3e207813faecae1969eb066ae1` and the prior
Python runtime selection `84b83dfdef0dd8d11851bbc89c4be7888af838a2b7c0ea4204f1678f9aecfaf9`.
The resulting21 runtime pins are18 previously pinned Python/DLL files under the
frozen release's `receiver/runtime/python`, its supervisor release manifest and
the two provenance selection files. No old network fixture or mathematical
executable is selected. Explicit runtime pins remain nonhermetic: they do not
prove the complete operating-system/stdlib installation trustworthy.

Source inspection of `test_claims.py` confirms no `receive`, real verifier/producer
constructor, supervisor, socket, network or ordinary-source author invocation.
`SyntheticOwner` uses `object.__new__` and test-only patched owner methods; group
opening executes only hash/structure validation. The deliberate wrong-class
session constructor rejects before touching any verifier. All25 tests use local
fabricated mathematical data, and frozen production modules have no import-time
worker launch. The existing outer runner is the only process supervisor.
