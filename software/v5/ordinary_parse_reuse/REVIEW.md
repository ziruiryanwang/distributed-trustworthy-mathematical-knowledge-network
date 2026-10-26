# Independent parse-reuse source and focused-control review

2026-10-26. Reviewer: current_acceptance_challenge. Canonical project root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`. This review performs
source/data inspection only. No product import, control, native operation,
installation, selector, benchmark or Git mutation was run by the reviewer.

## Disposition

**PASS_SOURCE_AND_EXACT_FOCUSED_SELECTION**, for the exact files below and the
finite native-free controls in TEST-PLAN. Root may select that one reviewed run.
This is not a test outcome,
installation adoption, rich-Std intake clearance or v5 completion.

| File | Bytes | SHA-256 |
|---|---:|---|
| ordinary_admission.py | 41372 | 98c88eb0e7ea5e101f6ccd8e94b56a0cc248167c317a0440ba00dc86f503cd9a |
| baseline_intake.py | 17024 | 9b243232603206b3a0925f639a0b8b1a6cbf0de8ca093ad4aa3642c595ff1142 |
| DESIGN.md | 10082 | 709e79c6e7070f160d2e6aae23f6d7ff705885c41983ada0402c15c862388706 |
| controls.py | 33123 | 493927df959935b042504204a0ddfcd06933fb4adb0437159a5eed9c6e5628ee |
| TEST-PLAN.md | 8599 | b3b4381edadb7809a2a84c08c0d2483a88f816ff9dfadb2364222885be1a137d |
| select_controls.py | 7232 | 4bc027bfdc8e4d8849c38105db9ff93eb17af3c10d9de8da0787ca19cc6f83d1 |

These are the author's final pins, independently reread/hashed by this reviewer.
The complete source diffs were compared against the exact current-release
predecessors: admission `9653a710a089393d189830a26aa8dd0723ee75859ce577d9713dae569b5e8575`
and intake `b5a17aa580f8d9cfdeaaded7d93c2b12ad6e19e5018bf5e7c087cb56760069d8`.
Their equality to the adopted actual build was independently checked earlier in
this assignment. Used predecessors remain unchanged.

## Core argument

The private planner is the old algorithm with an additional return projection;
its finite raw-byte checks, strict portable parsing, semantic and name binding,
missing imports, duplicate handling, complete-group reuse, import lineage and
topological order are unchanged. The map is constructed from that invocation's
strict parses, keyed by each item's own immutable raw bytes. Public `_plan` and
`preflight` still return only the raw-only, nonauthoritative Preflight.

Actual admission obtains the real current parent and freshly invokes this
planner on the supplied `plan.raw_units`. It does not accept the caller's status,
order, reused IDs, missing list or attached parsed metadata. The same private
parsed values generate names, ordered identities and canonical native unit JSON.
Only immutable raw/order/ID/JSON values and bounded name subtrees survive into
`_execute`; the parsed map and ordered Evidence aliases are explicitly dropped
before staging, catalog or native callbacks.

The new `_execute` keyword is private, not an input to the public API. Its shape,
exact ordered raw tuple, native JSON byte bound and domain-separated raw hashes
are checked before the unchanged grant/request/parent bindings. Raw equality
alone would not establish JSON correspondence: that implication comes from the
closed, read-only internal construction above. Hostile Python introspection or
monkeypatching is outside the existing owner-process model, not prevented by an
underscore. The basis path still uses the existing call and requires no prepared
extension. Repository search found no other extension callers needing migration.

Unchanged `_stage` still independently parses, puts real inert custody bytes and
compares exact readback. Unchanged catalog reservation reparses and binds the
actual ordered units. Native decoding/checking and exact report/artifact checks
remain mandatory. The post-grant `finally` still abandons a clean failed event
or quarantines an uncertain native lifetime. Neither preflight nor a hash grants
mathematical authority.

Baseline metadata planning uses its own fresh map for binding and custody-cost
projections, and drops it after each batch. The concrete
`_custody_increment -> OrdinaryStore._export_locators -> read_locator` source
chain was inspected: it reads without mutating/storing Evidence, and detaches
locator names through encoding/strict decoding. The explicit loop-row reset
removes a possible full declaration/proof-DAG alias; retained names do not point
back to containing trees. This is a source ownership argument, not an assumption
that the frozen Evidence dataclass makes its document immutable.

## Cost, memory and failure boundary

The fresh successful path removes three admission projections and two baseline
projections: eight to five strict portable reads within the admission workflow,
thirteen to eight across full intake. The claim is an operation-count reduction,
not a CPU/wall speedup or a different checking policy. For the retained closure
the eliminated parse-input volume is 224,564,215 bytes; hashing, JSON encoding,
I/O, database and native work remain.

The old planner already retained one finite batch. The new map adds references,
not a global or prior-call cache. Native serialization overlaps that one batch
temporarily; its Python representation overhead is not bounded in MiB merely by
the raw size. Admission releases proof trees before native execution, and metadata
planning releases each batch before the next. Exceptions can retain one bounded
frame until its traceback is released. Existing hard outer resource containment
is still necessary; maximum-sized admissible input is not promised to finish.

Serialization now occurs before custody staging/reservation. Allocation or
encoding failure can therefore happen earlier with fewer side effects. DESIGN
states this explicitly; normal projections remain byte-equivalent, but identical
failure timing is not claimed. This cannot promote a false root or erase existing
state. There is no allowance renewal or retry.

## Focused tests and pre-execution corrections

The complete final control source and plan were read. The eleven groups compare
real predecessor/successor parsers and controller flow over three genuine small
retained V2 units, using explicit catalog/custody/native doubles. They cover:
raw-only plan equivalence, reverse/duplicate/mixed/reused cases, fresh-call
parsing, missing/conflicting imports, exact native projections, the two count
reductions, forged public metadata, changed raw/current parent, private immutable
projection binding, five failure/cleanup paths, per-batch lifetime, full two-batch
intake counts and preservation of a first confirmed synthetic prefix when the
second actual reread changes.

The exact production custody schema/durability and native mathematical event are
not simulated claims. The store double includes one real strict read only to
model the unchanged validation boundary; its locator format is synthetic. The
real `reserve_extension` projection runs, but reservation and commit authority
are doubles. Subprocess, sockets, database opening and real owner/catalog opening
are blocked. The model writes only its fresh result, not its virtual owner paths.

Two deterministic test errors were found and repaired before any execution:

- The old baseline retains its last Evidence loop alias across batches. The
  zero-prior-batch lifetime/peak requirement now applies to the successor, while
  predecessor projection/count equality is still checked.
- The first fixture has no imports. Import mutations now use the genuinely
  importing second fixture and preserve the intended conflicting-parent path.

Weak references test Evidence-wrapper release, not arbitrary dictionary subtree
lifetime. TEST-PLAN now explicitly relies on the source ownership review for the
latter. No broader memory or hostile-process claim is drawn from small fixtures.

The selector reads PINS/FIXTURES by AST literal extraction without importing
tests or product code. It binds the final controls hash supplied by root, the two
fixed successor hashes, seven source snapshots and fifteen external pins
(nine package modules, three units and three Python runtime files), checks fresh
canonical paths and rechecks pins before its exclusive selection write. It does
not launch. Its proposed runner envelope is 60 wall / 45 inclusive Job CPU
seconds, 512 MiB, one process and 1 MiB per log, with inner 45 wall / 30 CPU.

## Next boundary

The actual generated selection at
`experiments/v5-local-checks/parse-reuse-controls01.selection.json`, SHA-256
`5e9e52158134af517da07edd22f816b51326864c03ddfadeeb887457aa890b85`, was read
completely. Its seven source and fifteen external hashes were independently
recomputed and all matched. Command, exact run name/output, isolation flags and
all six resource limits agree with the reviewed plan; its run directory was
absent at that check. The selector has generated a selection, not executed it.

Adopt only
the saved actual outcome: all eleven groups, exact counts/projections, no
forbidden operation, matching stdout/result, empty stderr and clean closed Job.
Do not treat this source review as an already passed test. A failure is retained,
not retried from this allocation. File-only installation source is separately
reviewed in PACKAGE-REVIEW.md; real native initialization/intake remains held.
