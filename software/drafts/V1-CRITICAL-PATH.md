# Critical path to a usable v1 mathematical commons

2026-09-21. Independent, read-only product-design assessment after the bounded
reciprocal, controls and transfer-recovery audits, while historical-context
selection is being qualified. This note proposes priorities; it neither changes
the implemented protocol nor certifies the development tree. Only this Markdown
file was authored. No product execution, import, database query or code edit was
performed. Historical qualification cuts remain unchanged.

## Decision in brief

Later evaluation clarification: root selects the principle in
[matched endpoints](USEFULNESS-MATCHED-ENDPOINT.md). Comparative speedup is
required to claim comparative efficiency, not as a universal release condition.
Useful v1 capability requires independently demonstrated nontrivial reuse and
contribution within a prospectively acceptable practical envelope, with a
matched local comparison and all costs reported. This supersedes interpreting
the illustrative benefit threshold below as a mandatory win. No benchmark has
been commissioned or passed by this clarification.

Finish the small context-selection discriminator already underway. Then make
one node capable of continuing useful work without throwing away its state:
select an explicit operating envelope, implement renewable authorization with
real metadata/storage headroom, and make ordinary interrupted operations
reconcilable. In parallel, establish a measured formal-retrieval baseline and
prepare a real two-host deployment. Add explicit exact-byte replica sharing;
otherwise the present publication rule makes the originating producer a
necessary supplier even when another node already holds the result.

Do not make sophisticated usefulness ranking, a global index, consensus,
cryptographic identity infrastructure, SNARKs, or complete formal verification
prerequisites for these capabilities. Conversely, do not call another finite
reciprocal example a usable v1 while lifetime credits, a stranded pending slot,
or a fixed contact configuration still force a healthy operator to start over.

The immediate product question is not whether every component has a theorem.
It is whether an independently operated agent can discover, check, use, retain,
share and extend formal knowledge through documented interfaces, repeatedly and
at a measured cost, within an honest supported envelope.

## Evidence used and current boundary

This assessment reads [the current goal](../../GOAL.md),
[continued operation](CONTINUED-OPERATION.md), the
[renewal proposal](CAPACITY-RENEWAL.md) and
[review](CAPACITY-RENEWAL-REVIEW.md), [API](../API.md),
[peer wire contract](../PEER.md), [core](../CORE.md),
[recovery contract](../RECOVERY.md), [context proposal](CONTEXT-SELECTION.md),
and pertinent `manage.py`, `py/storage.py`, `py/node.py`, `py/checking.py`,
`py/peer_node.py`, source-codec and native-interface code. The requested
continued-operation note is under `software/drafts/`, not `software/`.

The [H01](../qualification/peer-01-h01/OUTCOME.md) and
[controls](../qualification/peer-01-controls/OUTCOME.md) audits support a real
same-host reciprocal loop and bounded controls. The
[recovery outcome](../qualification/recovery-01/OUTCOME.md) qualifies one genuine
interrupted transfer under its declared profile. None qualifies independent-host
operation, sustained capacity, useful-growth efficiency or general crash
recovery. Some documentation introductions retain earlier historical status;
the linked outcome scopes, not a stale heading or mutable-source existence,
determine which behavior has executed.

### Properties to preserve while making the prototype practical

For a node N, keep these predicates separate:

- `Have_N(x)`: N has the bytes required by an exact artifact/closure identity.
- `Offer_N(x)`: N explicitly makes those bytes discoverable and retrievable.
- `Accept_N(F, Gamma, x)`: N's selected checking path accepted x relative to
  the explicit foundation F and context Gamma.
- `Useful_N(x, W)`: an empirical or heuristic assessment for local workload W.

Neither `Offer` nor `Useful` implies `Accept`. An older acceptance receipt does
not imply current `Have`. Offering someone else's artifact need not create a
new theorem or assert authorship. A changed locator need not change mathematical
identity. These distinctions are more important than making every module formal.

The acceptance guarantee remains conditional on the selected Lean/kernel,
reconstruction, explicit foundations, hashes and trusted local runtime. Ranking
and popularity cannot introduce axioms, waive dependency validation, or turn a
resource refusal into mathematical falsity. Each agent chooses its work; test
workloads are project evaluations, not a network-wide research agenda.

## Current choices that obstruct an operable v1

| Present choice and source | Consequence | Smallest consequential remedy |
|---|---|---|
| `manage.configure`: 128 requests, 16 stages, 4 GiB conservative reservations; `ControlStore.reserve/stage` consume these monotonically | Eventually even a healthy node cannot do new work. An `info` request consumes one request and the ordinary 8-MiB reservation | Versioned cumulative authorization separate from consumption; owner grants reachable at logical exhaustion; a bounded observation/status path |
| `storage.py`: 4096-byte pages, 8192-page cap; request replies up to 1 MiB and records up to 2 MiB; no administrative reserve | Logical credits do not ensure that an ordinary terminal response or grant record fits | Select/measure an envelope and reserve terminal/admin headroom; reject new work before violating that reserve; support deliberate physical expansion or explicitly bounded exhaustion |
| Context package list at most 16, including five common packages; `admit` unions with the current head | A sequence of unrelated investigations fills the working context | Qualify historical-head selection first; keep the corpus separate from a proof context. Do not claim that selection enlarges one genuine dependency closure |
| A single global `meta.active`; recovery only for selected native-free peer operations; nonempty SQLite sidecars refuse | One interrupted `submit`, `admit`, selection or transaction can strand all ordinary work | One common status/reconciliation contract for supported operations, including native-worker quiescence and legitimate database recovery |
| `find` is append-sequence pagination, not query search; peer discovery downloads a whole catalog of at most 32 entries | Finding an unknown useful lemma scales toward enumeration; a larger corpus may be invisible behind view limits | Public exact-ID lookup plus bounded formal filtering; then snapshot-consistent paged/incremental remote metadata. Choose ranking from measurements |
| `expose` requires a local publication marker; acquired entries are ineligible; `publish` accepts a locally submitted artifact | Possession/admission of an imported result is not enough to share its exact bytes. A forced wrapper theorem would create duplication | Explicit owner-authorized replica custody/exposure, distinct from creating a mathematical publication or acceptance |
| At most two immutable contacts, literal loopback transport, manually issued finite service sessions | Contacts cannot evolve; service is not independently hosted across machines or persistently available | Versioned mutable owner contact records; a documented multi-host transport profile and restartable hosting with durable resource authorization |
| Reconstructed source environment is not an ordinary Lean project with all notation/tactics; unsupported syntax has already caused failure | An agent can know the formal theorem yet fail at the interface | A precise capability profile and directly usable formal vocabulary/type/body interface, with conformance tests and normal example clients |
| Absolute installation/state paths and exact runtime/source/config pins are retained in records | Editing config or moving a used state is not a valid upgrade or relocation | Publish supported compatibility/backup/upgrade boundaries; fresh installs and explicit mathematical export/readmission are acceptable first, not silent in-place migration |

Windows-only support, selected Lean 4.34.0 and an explicit finite language
fragment are not themselves blockers to a bounded v1. They are blockers to
claims of arbitrary-platform or all-Lean-library support. A single local writer
is likewise acceptable initially if work is bounded, busy responses are clear,
interrupted work is reconcilable, and agents can operate separate nodes.

## Dependency-ordered milestones

The table specifies product outcomes, not a requirement to build another large
experimental coordinator for each row. Preparatory work can proceed in parallel;
the dependencies concern what a completion claim requires.

| Milestone | Depends on | Exit evidence |
|---|---|---|
| A. Small-context continued investigation | Existing acceptance path | A real package-bound refusal, explicit historical selection, fresh successful admission/use, preserved earlier records and charges; no reclassification of selection as acceptance |
| B. Continuing local operation | Chosen v1 envelope; A for the repeated-use workload | Exhaust a deliberately small real allowance, renew it through the public owner interface, continue native work, reconcile supported interruptions, and preserve exact old replies/charges |
| C. Useful, affordable formal retrieval and reuse | Existing core; B before prolonged measurement | A fixed heterogeneous corpus and independently authored consumers, compared with local-library/enumeration baselines; stage-separated costs, failures and genuine downstream dependencies reported |
| D. Exact-byte replication and independent hosting | Explicit custody/acceptance separation; B for ongoing operation | Producer A publishes, B retains and explicitly serves the same identity, A stops, C acquires from B and freshly checks/uses it; actual separate hosts and no required central endpoint |
| E. Release candidate | A–D integrated in one declared supported cut | A new operator installs from the release package, follows documentation without research-internal plans, repeats the supported workflows, and obtains reviewed failure/resource behavior |

Prepare C's corpus, queries and cost instrumentation now; do not wait for B's
implementation to decide what usefulness will mean. Prepare D's host/runtime
and transport contract now; do not wait for sophisticated ranking or worldwide
peer discovery. A short two-host feasibility check may precede B, but cannot
substitute for D's continuing-operation evidence. The critical serial work is
currently A followed by B, not another variation of the completed positive loop.

### B: select an envelope, not an illusion of unlimited capacity

Use the reviewed renewal invariant with consumed vector U and authorized vector
A: ordinary reservation requires `U + charge <= A`; a fresh owner grant adds
nonnegative d to A and never reduces U. Grant replay returns its old bytes and
does not add d twice. Both ordinary-request and native-stage byte charges count.
Grants change no proof, head, publication, acceptance policy or foundation.

The present finite system has a simple inevitability: if each new operation
consumes at least q positive reservation bytes and A is fixed, at most
`floor((A_bytes - U_bytes) / q)` further such reservations can succeed. Request
and stage caps impose independent ceilings. Increasing a numerical parser limit
or resetting state does not answer this problem.

Make these decisions before implementing renewal:

1. A fresh versioned store with bounded authorization/grant records, exact
   integer arithmetic and immutable initial grants; no accidental migration of
   preserved nodes. Expose reviewed initial limits so tiny real saturation
   tests do not need hundreds of native stages.
2. A finite supported physical/metadata envelope and early admission guard.
   Account for a pending operation's maximum remaining visibility/terminal
   writes, rollback-journal needs, and an administrative grant/status record.
   The 32-MiB hard DB cap is not a reserve. A measured conservative reserve is
   acceptable under an explicit filesystem-capacity premise; a free-space
   observation is not a guarantee against unrelated writers or hardware loss.
3. A bounded owner observation path that still reports status at ordinary
   quota exhaustion. Do not casually exempt existing `find`: it creates local
   candidate/cursor handles. A genuinely read-only `status`/`info` contract can
   avoid a permanent ledger row per poll while retaining bounded CPU/output
   and physical diagnostic costs.
4. A realistic qualification horizon declared before the run: candidate and
   accepted-context counts, operations by class, grant count, largest supported
   closure, DB pages, retained bytes, and maximum per-operation costs. It must
   cross initial exhaustion and multiple continuations, not only grant once
   and terminate. Pick numeric values from pilot costs, not from wishful
   billion-agent capacity assertions.

The current exact-four-digit stage-path recognition supplies an independent
ceiling: raising stage authorization beyond IDs 0–9999 requires revising and
testing its consumers. Similarly, the 8192-entry cap, record/reply size ceilings,
package limits and fixed DB cap do not disappear when request credits renew.
An envelope must check all of these jointly.

For the first envelope, conservative no-refund reservation and retained
historical evidence can remain. That is simpler than premature garbage
collection. But the release must say how an owner increases real capacity or
stops safely at its declared boundary; finite storage plus indefinitely growing
retained history cannot provide indefinite growth. Archival/compaction becomes
necessary when measured storage demand justifies it, with an explicit dependency,
historical-replay and availability contract. Do not design that subsystem merely
to avoid choosing a credible first envelope.

#### Supported interruption is part of continuing operation

The peer recovery audit is valuable but deliberately narrow. Generalize by
operation class, not by erasing the guard against native uncertainty:

- A committed request returns its original terminal bytes; output loss is not
  rollback and is not a reason for automatic new-ID retries.
- An uncommitted request can become an explicit terminal interruption only
  after its original complete worker tree is authenticated quiescent and the
  visibility/ledger state is reconciled under writer exclusion. Native-stage
  rows and all consumed resources remain charged and retained. No directory
  alone becomes accepted mathematics.
- Every supported operation must have either a demonstrated bounded recovery
  path or a concrete documented restore/revalidation procedure. Merely saying
  "blocked forever" for ordinary process cancellation is not usable v1 behavior.
  Fatal disk corruption or total evidence loss may remain outside the profile.
- A nonempty legitimate rollback journal is not automatically malicious data.
  If process interruption inside a transaction is supported, integrate and
  qualify SQLite's legitimate recovery after quiescence; never delete sidecars
  to make a check pass. Power-loss/filesystem durability is a distinct claim.

This calls for a reusable state/status contract and a small failure matrix,
not immediate concurrent writers, distributed transactions or automatic
re-execution of unknown mathematical work.

### C: usefulness and efficiency must become measured product properties

Start with the formal information already available: exact typed IDs, foundation,
kind, universe arity, type structure and dependency/symbol references. Expose
exact lookup and one bounded structural/lexical filter path over versioned
metadata. Reuse existing internal descriptor lookup and symbol information;
do not start with a global semantic-equivalence solver. Search indexes are
rebuildable candidate-selection data, not acceptance authority.

Use a corpus containing independently chosen definitions, composable theorems,
unrelated distractors, exact duplicates and alternative presentations. Consumers
must not be handed the answer's exact identifier; include one real interoperability
case beyond the worked G/H family within the declared fragment. All queries and
answers may be formal. No human-intention field, natural-language gateway or
central task list is required by this evaluation.

Compare the same consumers, initial libraries, total budgets and downstream
formal challenges under at least a local-library/enumeration baseline and the
network retrieval path. Report completion rate, time/cost to first checked
usable dependency, completed downstream contributions, actual dependency use,
duplicate transfer/storage burden, and failure/refusal rates. Include producing,
indexing, checking and retaining shared knowledge where relevant; state cold
onboarding and any amortization horizon separately. A receiving-agent saving is
not necessarily a network-wide saving. If agent compute is unmetered, do not
claim a complete compute comparison.

Predeclare a practical benefit criterion before observing results: for example,
more completed downstream work at the same total budget, or comparable completion
with lower end-to-end cost. Do not turn raw theorem count, hash novelty, HTTP
success, or two references in a source file into evidence of meaningful growth.
No finite workload establishes universal mathematical importance or exponential
growth. An inconclusive comparison is an inconclusive result, not a reason to
retroactively weaken the baseline.

Local successful-use frequency, recent retrieval success, closure size, estimated
checking cost, embeddings or an LLM can rank candidates. Treat them as fallible,
replaceable policies. Popularity reports from other nodes are hints; a popularity
score cannot discharge a proof obligation. Retain bounded exploration so today's
usage does not automatically suppress unfamiliar mathematics. Sophisticated
ranking is justified only if it improves the measured retrieval bottleneck.

Profile before changing proof technology. G02's admission Job measured 22.046875
CPU seconds, with 4.671875 nested native CPU already included; the difference
is not proof of one specific bottleneck, but it makes kernel-only acceleration
an unsupported first remedy. The controls duplicate used 7.78125 Job CPU seconds
and 64 MiB of conservative allowance with zero native stages. Measure repeated
package validation/copying, context reconstruction, process setup and native work
separately. Reuse authenticated immutable selected data where justified; never
replace the required receiver check with an untrusted peer's cache claim.

### D: mathematical identity must survive a change of custodian

Current `peer_node.reuse` recognizes an exact existing offer. Nevertheless,
`expose` insists on `require_published`, whereas received offers are not locally
published and ordinary `publish` consumes a source-submitted artifact. Local
admission does not by itself create that publication marker. Therefore current
rules do not implement an exact-result replica service.

Add a minimal explicit owner choice to retain and share a selected inert package
or candidate, with independently bounded resource authorization. The original
typed IDs and canonical bytes remain unchanged; local custody/sharing records
must not manufacture a new mathematical theorem, origin claim, or acceptance
receipt. Acquiring bytes remains private by default: explicit sharing is not
automatic exposure of all acquired state or source/evidence files.

An owner may share a hash/framing/closure-validated inert candidate **without**
claiming it has been natively accepted. Requiring every cache/relay to prove it
would conflate custody with mathematical authority. If policy elects to serve
only locally admitted results, that is an optional local gate, not the meaning
of replication. In either case a consumer's own normal acceptance path remains
mandatory before trusted mathematical use. Bad metadata, invalid proofs and
missing dependencies remain possible and must be handled explicitly.

The decisive availability test has three roles: A creates x; B retains and
explicitly offers the same x; A goes offline; C obtains x from B and freshly
checks/uses it. This checks a real change of supplier, not a new wrapper theorem.
Roles may be combined for a preparatory test, but independent-host deployment
claims require actual separately operated environments. No central ledger is
needed to tell C what bytes x denotes. Hashes do not ensure that any holder
continues to exist; durable availability is conditional on funded storage and
reachable holders.

For multi-host transport, the smallest initial profile may use an explicitly
configured authenticated tunnel to the existing loopback service, or a reviewed
direct TLS endpoint profile. A tunnel preserves the inert payload boundary but
is a real deployed dependency whose routing, host authentication, disconnection,
quotas and setup must be documented/tested. It does not qualify a public-facing
HTTP server or secretly authorize deployment to another machine. No indispensable
central relay is allowed in the demonstrated architecture.

Provide owner-controlled versioned contact replacement. Old remote selections
must remain bound to their selected endpoint/version or fail explicitly; assigning
an alias to a new contact must not reinterpret an old request. Endpoint identity
helps routing/resource safety but does not prove mathematical correctness.
Standard transport authentication suffices initially; political attribution is
not on this path.

Hosting must also outlive a manually managed ten-minute demonstration session.
A normal supervisor/service command may restart bounded workers under explicit
durable owner authorization, retaining aggregate accounting and stopping at
exhaustion. It must not replenish resources by silently resetting a worker's
counter. Continue serving committed immutable views independently of local
research work. Add bounded snapshot-consistent catalog pages or explicitly
selected view sets; eventual update observations suffice. A global instantaneous
"whole-system status" is not a prerequisite or a promised asynchronous-network
property. Whole-corpus replication at every participant is unnecessary.

### E: the release must be independently usable

A new operator should need documented installation/build/configuration commands,
not hand-built research plans, copied experiment receipts, hidden root-side
promotion or knowledge of internal canonical encodings. Provide a small normal
agent client/example using returned exact formal names/types/body data, request
IDs, status/replay semantics and standard peer operations. This is not a
natural-language formalization service or a mandatory proof strategy.

Declare the supported foundations, Lean/runtime versions, platform, syntax and
declaration fragment, context/closure/resource limits, source trust boundary and
expected failure modes. Add syntax/type/body round-trip conformance examples so
an independently written agent can produce a valid submission without discovering
missing notation through repeated paid failures.

Keep code/data versioning explicit. The first release can support fresh stores
only and preserve old installations for historical evidence; it need not solve
every migration. It still needs an honest way to retain/export mathematical
artifacts for a new installation and freshly check them under its compatibility
policy. A path change, restored old database, or changed config must never be
presented as preserving all historical request/accounting commitments without a
separately established migration/restore contract. Actual external publication,
license choice, host access and spending remain deliberate owner decisions.

## Reduce test overhead without reducing the acceptance boundary

Keep one small shared supervisor/receipt interface and a reusable outcome reader;
make scenario files mostly data plus a short sequence of public operations.
The current move toward a small context-contract coordinator is appropriate.
Reuse frozen valid inert artifacts for orthogonal tests, and exercise resource
boundaries with small supported initial allocations. Do not repeatedly rebuild
two producers or generate new mathematics just to test a metadata transition.

Use native-free unit/model/transition tests for parsing, integer bounds,
authorization, snapshot paging, replay, contact changes and transaction outcomes.
Label synthetic database/receipt fixtures as such. Retain one minimal genuine
native-backed discriminator for each mathematical or execution claim, one real
transport interruption when that behavior changes, and a compact release-level
end-to-end suite across the integrated cut. A changed layer should rerun its
affected contracts and one connecting workflow, not every historical experiment.

Preserve failed launches, actual child counts, charges and final cleanup records.
Count enclosing and nested CPU without double counting; distinguish missing
measurement from zero cost. Share hashes/inventories for immutable fixtures and
checkpoint once per run rather than scanning global history on every request.
Do not reduce overhead by omitting receiver checking, suppressing failures,
fabricating native evidence, or trusting a supervisor exit code as proof of
quiescence. Independent review remains important, but review the actual changed
boundary rather than requiring a new bespoke 50-KiB orchestrator for each case.

## What can wait, and what cannot

**Can wait:** worldwide DHT discovery; blockchain consensus; a mandatory global
catalog or research agenda; reward/attribution systems; universal semantic
deduplication; SNARK acceleration; complete mathlib or multi-platform support;
optimal usefulness ranking; arbitrary concurrent writers. Exact duplicate
detection plus explicit unsupported-variant handling is an acceptable first
policy if its rejection rate is measured and it does not erase alternatives.

**Cannot wait for a usable-v1 claim:** recurring local work within the declared
envelope; state-preserving exhaustion handling; supported ordinary interruption
reconciliation; useful formal discovery and independently consumable source
interfaces; exact-byte custody/replication; actual multi-host operation without
a required central service; measured total costs; and a tested normal install/run
path. Formal safety arguments, tested operational guarantees and heuristic utility
claims should stay separately labeled throughout.
