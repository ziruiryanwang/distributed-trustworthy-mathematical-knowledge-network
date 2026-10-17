# Actual client mathematics and import review

2026-10-16. Independent reviewer: `memo_tests_review`.

## Disposition

**PASS for the proposed mathematics and inspected source boundary.** The seed
fusion theorem and consumer paired-fold projection have valid mathematical
arguments using the retained foundation and base module. The owner inspects the
actual root theorem's exported proof closure, rather than treating a textual
name or a constant anywhere in an export as evidence of reuse. No blocking
mathematical/source finding was identified.

This is not executed Lean elaboration, native acceptance, actual reciprocal
operation, growth benefit, cryptographic assurance or launch clearance. No
project module was imported, no native process/test was run, no Git mutation
was made, and no previously used evidence was changed. PowerShell was used only
to read source/data and compute file identities. Root owns selection and runtime;
the separate lifecycle reviewer owns operational/resource inspection.

## Reviewed identities

Paths below are relative to the sole canonical root,
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/client/actual_owner.py` | 22521 | `2f2f07aa6ac91618120b210abec99ddbef4818332bd2d7915e6b0c837efc1016` |
| `software/v5/client/actual_assets.py` | 10738 | `0cef5f4e8ff7590d52f51d73f3fa42ca23ab4ace4a75eeff16dd0df49f68ef87` |
| `software/v5/authoring/AuthorLean.lean` | 42799 | `00f90c7f449d1228227d89fc251283061ccfa59791e5bd563e058b3d41f1f78e` |
| `software/v5/modules/source_rows.py` | 15320 | `60c7255d9bf65236d684a77e2890c00567dba5bc2f72b81d13c933af237913f4` |
| `software/v5/authoring/context.py` | 10243 | `a6d0b794204fb92dd43b7b63d38cd4f4dd15dff5d7f33d0254c4f1cbc1650541` |
| `software/v5/mixed_claims/authoring.py` | 23676 | `8b09cb1b8f0466a5049ed53f7b28098b6022234e3681786b2f4a9f542cd83e1b` |
| `experiments/v5-local-checks/receipt-prepare-01/prepared/base/bundle.json` | 53769 | `09e4f3bbc045ef25ba0378ee000bdd36bd1d57423f60b696dafc57a48595c926` |
| `experiments/v5-local-checks/receipt-prepare-01/prepared/foundation.json` | 23313 | `736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c` |

The inspected ordinary-owner source was fresh/unexecuted at this review. Later
source edits require a changed-boundary review, not silent transfer of this
disposition. The argument also used the retained source blueprint
`software/v5/workloads/FoldFusion.lean`; the proposed operation does not import
that blueprint or borrow its saved proof output.

## Exact mathematical boundary

The selected base module is
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.
Its actual bundle declares:

- `Tree`, `Tree.leaf`, `Tree.node`, `Tree.rec`;
- `Tree.below`, `Tree.brecOn.go`, `Tree.brecOn`, `Tree.casesOn`;
- `fold.match_1`, `fold._f`, `fold`;
- `map._f`, `map`; and
- `binary_congr`.

All names are under `CommonsV5`. There is no base `fusion` or
`project_summary`. A fresh local `ClientV5` theorem is therefore an extension,
not republication of either theorem already in the admitted base. This does not
claim novelty in mathematics or in other participants' libraries.

The retained foundation's decoded declaration census includes `Eq`, `Eq.refl`,
`Eq.rec`, `Eq.trans`, `Eq.casesOn`, `Eq.ndrec`, `Eq.symm`, `rfl`, `HEq`, `PUnit`,
`PProd`, `Prod`, their constructors/recursors, and **both `Prod.fst` and
`Prod.snd`**. Product and both projections have two universe parameters. There
is no `congrArg` declaration in this census. The plan's suggestion that using
a lambda avoids a missing named `Prod.fst` dependency is unnecessary: the named
projection is already present. The proposed lambda is nevertheless valid.
This documentation correction was sent to the plan author; no extra test is
needed for it.

## Why the two proofs are valid

Let `fold l n` interpret a tree by mapping leaves with `l` and combining child
interpretations with `n`. Given functions `h : B -> C`, `leafB`, `leafC`,
`nodeB`, and `nodeC`, assume

\[
h(\operatorname{leafB}(x))=\operatorname{leafC}(x),\qquad
h(\operatorname{nodeB}(x,y))=
\operatorname{nodeC}(h(x),h(y)).
\]

The seed theorem asserts

\[
h(\operatorname{fold}(\operatorname{leafB},\operatorname{nodeB},e))=
\operatorname{fold}(\operatorname{leafC},\operatorname{nodeC},e).
\]

Structural induction on `e` proves it. The leaf case is precisely the first
assumption after unfolding `fold`. In the node case, the second assumption
gives the first equality; imported `binary_congr nodeC ihl ihr` substitutes the
two induction hypotheses; `Eq.trans` composes them. No associativity,
commutativity, extensionality, classical choice or additional axiom is required.
The source explicitly chooses `Tree.rec`, reducing reliance on elaborator
eliminator-selection metadata for the reconstructed inductive.

For projection, instantiate fusion with the intermediate algebra `B × C`,
paired leaf map, componentwise paired node map, target algebra `B`, and
`h = fun pair : B × C => pair.1`. The leaf and node preservation obligations
reduce by beta reduction and product projection; each is `rfl`. This yields
the stated equality of the first projection of the paired fold with the
`B`-only fold. The intermediate universe is `max v w`, and the target universe
is `v`; polymorphic fusion admits this instantiation. Both generated theorem
types genuinely use all three declared universe parameters.

The owner has explicit `autoImplicit false`, `noncomputable section`, and
`universe u v w`. The source contains no numeric/string literals, `simp`,
`congrArg`, or new axioms. Product notation is supported by the pinned Init
frontend and retained foundation. Exported `.proj` expressions have an explicit
representation in both the native exporter and `SourceRows` decoder.

The theorem supplies a reusable equality; it does **not** by itself prove an
operational saving or compel a consumer to avoid calculating the second
component. A later rewrite/optimization strategy and an explicit resource model
are needed for that claim. This operation is a reciprocal-use gate, not the
full-cost growth comparison.

## Import and actual-use evidence

`prefix()` opens the exact relocated base namespace. `projection_source()`
validates the discovered module digest and directly applies
`DMKN.Mod.«<discovered>».ClientV5.fusion`; it does not declare an axiom, copy the
seed proof, or receive the seed ModuleID as a search input. Consumer discovery
uses the known base `fold` export and formal theorem/`Eq` features. After
candidate resolution it checks the returned relative method name and binds
the acquired warrant to that discovered ModuleID.

The consumer takes the exact base/fusion journals from the acquired warrant's
members and openings/bodies from `semantic_material(warrant)`. It does not take
the original base bundle as its authoring input. Both modules' selected groups
and their transparent semantic dependencies are supplied, rather than only a
public `fold` declaration whose auxiliary definitions are unavailable.

The existing context builder checks references and body commitments, produces
typed missing-data demands, and orders imported groups by dependencies. The
native frontend checks foundation descriptors against pinned Init and installs
imported definitions with their bodies. Imported theorem interfaces become
temporary frontend axioms **inside untrusted preparation**; that is not a new
mathematical acceptance mode. The final mixed/native relation must discharge
their admitted parents. The exporter skips imported boundary declarations and
rejects newly introduced local axioms.

`inspect_author()` binds the source bytes, requested roots, export, produced
packet and decoded local spec. It starts from the selected theorem's actual
`env.local_proofs[Address.of(env.module, root)]`, reads its proof body, and follows
local proof/value dependencies with finite visit/declaration limits. It requires
the exact external base `binary_congr` edge for the seed and exact acquired
fusion edge for the successor. It separately checks the root theorem's type
references the base `Tree` and `fold` and has three universe parameters.

The decoder validates the name/level/expression index domains, backreferences,
name-role partition, local declaration census and expression expansion limits
before this traversal. The proof inspection therefore does not mistake an
unrelated export row, name-table entry or source-text occurrence for proof use.
Its traversal includes type subterms inside a proof expression: it establishes
the reported proof-closure reference, not a general theorem of semantic
indispensability. For these fixed source terms, projection is visibly a direct
application of the acquired fusion result, so this distinction is not a blocker.

Both preparation and this inspection explicitly return non-authority. Actual
seed admission occurs at the fresh consumer; successor admission occurs on
the cold client. A passing inspection alone cannot substitute for either.

## Remaining actual checks, without duplicate experiments

The smallest selected client operation must still establish:

1. Successful elaboration/export of these exact generated sources under the
   pinned frontend and imported reconstructed context.
2. Native acceptance of the acquired seed and retained successor, with the
   declared actual proof-reference inspections passing.
3. Successful publication, packet-only semantic reconstruction, fresh owner
   admission and service cleanup, as judged by the lifecycle/actual reviewers.

There is no reason to launch a separate mathematics-only test first: these
checks belong to the one integrated operation already proposed. The cold phase
is fresh client/owner authority in the same Python process/host, as its source
correctly states. Native delta ancestry above I is still checked at reception;
zero ancestor theorem-proof bytes in ordinary frontend import does not imply
constant cold verification cost for arbitrarily long unaggregated chains.
Affordable frontier advancement and full-v5 release remain open.

## Actual operation 01: preparation failure, no mathematics reached

Root requested a terminal-only inspection of the existing
`product-local/v5-client-owner-runs/client-actual-01` output. Its plan identity is
`dad9f1d436c71f836d467fe14713d38e975563bd067836996eb292ec0d9b60d2`.
The saved owner/assets snapshots exactly match the two source identities above.
No launch or rerun was performed by this reviewer.

**Disposition: FAIL before any mathematical operation.** `RESULT.json` records
`COMMAND_FAILED`, child exit 1. `BOOT-FAILED.json` records
`CLIENT_BOOT_OR_OWNER_FAILED` with `StructureError: EXACT_RECORD_FIELDS`.
The actual traceback reaches `Strategy.__init__ -> Assets.__init__` at
`C.fields(params["assets"], RETAINED)`. The selected codec requires its second
argument to be a set of field names; the supplied `RETAINED` object is a dict.
Thus `set(value) == names` is false even though the plan's asset names are the
expected eight names. This is an adapter schema-validation defect, not a
mathematical rejection or evidence of bad input mathematics.

The failure precedes asset receipt/bundle loading, `Strategy.run`, seed workspace
creation, finite-grant construction, owner construction, receipt verification,
source authoring and native delta admission. The output's `work` directory is
empty. There is no source-request, exported Lean proof, owner actual-result or
fresh mathematical acceptance evidence to audit. Consequently **zero client
receipt/native/author calls were reached**, and neither proposed theorem has
executed evidence from this operation. The earlier mathematical argument is
unchanged; its source-only disposition did not establish executable adapter
correctness.

Exact retained outcome identities:

| Relative to `client-actual-01` | Bytes | SHA-256 |
|---|---:|---|
| `RESULT.json` | 2253 | `342303c66d75ac3d7987d7ad72eae74b4640417d498f12a742d3ecf8b8bf448c` |
| `BOOT-FAILED.json` | 87 | `c99ab7e76b9858a8a895eec36c74935906186f7044aff90a1f227da8ecf44bc9` |
| `command/stderr.txt` | 1830 | `3ac74b9eee0d5e714f89879ab0c441f771d204f9d4593a718ecf4c180834aaa4` |

The operational result reports direct child reaped, final active processes zero,
no termination requested, and no cleanup errors. Lifecycle adoption and any
fresh successor selection remain root's/separate reviewer's responsibility.
No actual proof-reference check passed; do not relabel this operation as a
mathematics or reciprocal-use pass.

## Actual operation 02: genuine I admission, source namespace refusal

Root requested a terminal-only mathematical inspection of
`product-local/v5-client-owner-runs/client-actual-02`, with seed operation
`32e6ddf7d813b557cc208294db3a4725d0a08a4da149c6c6fd1713d3252c273b`.
This reviewer ran no software/test and changed no product or failed evidence.

**Disposition: seed I admission reached; no new theorem export or reciprocal
use.** The saved receipt stdout records `REAL_MODULE_RECEIPT_VERIFIED`,
`fully_resolved=true`, the exact base ModuleID and selected receipt SHA-256
`850c33b2...6e5d47`. Its binding record is
`SAME_CALL_BINDINGS_VALIDATED_BEFORE_HANDLE`. The client report records one
admission submission, one import session, one author call, zero publication
attempts and zero mixed-delta admission attempts. This narrow actual I result
does not make the overall failed operation pass.

The source worker invoked the selected native frontend, which returned 1 without
timeout. Its result is `WORKER_NATIVE_REFUSED`, `export_bytes=null`,
`export_sha256=null`, with direct child reaped. Native stderr is
`OWNER_AUTHORING_FAILED AUTHOR_OWNER_SOURCE_REJECTED`. The source diagnostics
explicitly include the unknown namespace
`DMKN.Mod.«2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e».CommonsV5`
at the `open` command, followed by unknown `Tree`, `fold`, and `Tree.rec` uses.
No actual proof dependency could be inspected because there was no export.

The actual request contains all fourteen expected base declarations, owned by
the exact base ModuleID, and the intended seed source. It includes `Tree`,
`Tree.rec`, `fold`, `binary_congr` and their auxiliary definitions; this is not
an empty/missing semantic context. The native source installs and checks
frontend-visible exact constants before elaborating this source. These facts
support the separate author's namespace-registration diagnosis; they do not
constitute an executed test of an alternative source spelling.

Replacing the failed `open`/short-name references with their exact fully
qualified relocated constants is mathematically conservative: it changes name
resolution, not the imported declaration, theorem statement, homomorphism
assumptions, structural-induction argument or universe parameters. In
particular, `Tree`, `Tree.rec`, `fold` and `binary_congr` must all select this
same base owner; acquired fusion must still select the discovered owner.
The declaration names `ClientV5.fusion`/`ClientV5.project_summary` and the
actual exported-proof dependency checks should remain unchanged. This is
source-level justification of that proposed repair, not runtime selection or
a prediction that later boundaries will pass.

Exact retained mathematical outcome identities, relative to the seed operation:

| File | Bytes | SHA-256 |
|---|---:|---|
| `receipt-1/command/stdout.txt` | 1535 | `1b6236bda564c7b0a7ce8bc124d2a2be4cc8b9712f5e98a7061bdf8f18636515` |
| `receipt-1/binding.json` | 412 | `59302332508bb840f72a3366b8a6fa20c91c8800c8200a0010c7de24f855bb2d` |
| `preparation/author-1/source-request.json` | 61239 | `64aa3d0a5efde807d2bf4736524426f566cd8665027b4203c2164464cb2ce065` |
| `preparation/author-1/worker-result.json` | 787 | `8ad8fb1e027a8960a6b08da026968e0a5a8bc50f1452839a29c413c663e84f21` |
| `preparation/author-1/author-command/stdout.txt` | 7003 | `277cc9575000904a70ce6dc521dce9acd813a4b35c755e827ebcbfb7094f0ecc` |
| `preparation/author-1/author-command/stderr.txt` | 52 | `071d1528425682b874c8779a24ea375a0c73a726de4fcb0c8a3f5d38718eca28` |

No consumer, cold re-admission, publication or new mathematical result follows.
Preserve the failed authoring call and its charges. Root and the lifecycle
reviewer own total accounting, source-successor selection and any next launch.

## Actual operation 03: seed and acquired native result verified; loop fails later

Root requested a terminal-only audit of
`product-local/v5-client-owner-runs/client-actual-03`. Seed operation is
`4898246455cde36d15d11631b263a7a4fe9bb8d6c18d920504e72f038ca8490b`; consumer operation is
`a92a87348962d44907fc9853005485dba2bf097f76dd9697c434b254f5dcf0e9`.
Only read-only saved-data/source inspection was performed. No project module was
imported and no theorem, test, native check or receipt verification was rerun.

**Disposition: scoped positive mathematical evidence for the newly authored
fusion seed and its checked acquisition; overall reciprocal operation FAIL.**
The overall error is `DeltaError:MIXED_CONTROLLER_CPU`. Consumer author calls
and publication attempts are both zero. There is no paired-fold projection,
cold successor admission or completed two-way loop from this operation.

### Actual seed theorem, not a text-only use claim

The successful source uses fully qualified exact base names, without the failed
namespace `open`. Its UTF-8 source SHA-256 independently recomputes to
`e75d0679c8e7a882543bc1baf60e8148483e8cc86dd225c3c4737f768ae95ebf`, matching
the actual export. The worker reports native return 0, no timeout,
`PASS_NATIVE_EXPORT_ONLY`, and a 14,224-byte export with hash
`240512aa4eb5a77c9aa95efc20e93a15b8a082a5a032384c3adb3d861b09a6dc`.

Independent PowerShell data-only inspection reconstructed the export's name
and expression index maps and traversed the selected declaration's actual
type/value roots, checking referenced expression indices point backward. The
330 rows contain exactly one local theorem `ClientV5.fusion`, with universe
parameters `u`, `v`, `w`; no local helper theorem substitutes for it.

- Statement expression root 67 reaches 68 distinct expression nodes. Its
  constants are precisely foundation `Eq` and exact base `CommonsV5.Tree/fold`.
- Proof expression root 295 reaches 272 distinct expression nodes. Its reached
  constants include exact base `binary_congr`, `Tree.rec`, `fold`, `fold._f`,
  `Tree.below`, `Tree.leaf/node`, and foundation `Eq`, `Eq.trans`, `PProd`,
  `PProd.mk`, `PUnit`, `PUnit.unit`.

The imported `binary_congr` reference is therefore in the actual proof reachable
from this theorem's value, not merely in source text or an unrelated export row.
The reviewed structural-induction argument now has successful source-export
evidence under the selected frontend. The source is the full generic fusion
statement already analyzed above; this is not a closed example or reflexivity
wrapper. Frontend success remains untrusted preparation until the receiver's
actual mathematical boundary is satisfied.

### Exact publication and acquired mathematical check

The seed reports local publication of module
`b42957064314b6667bf05cd3eec27ce39b925491c756a69f23a739d39ebb9f94`, export
`ClientV5.fusion`, publication ID
`1573252331936645f052074a5506189fbbd2162160d93d7617d208d4af8d3a75`.
The seed's saved `mixed-packet.json` and consumer's acquired `delta/1/packet.json`
have independently equal length 554,165 and SHA-256
`92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f`.
The packet has one I claim, one frontier, one delta and one edge. Local publication
and indexing alone do not establish its truth.

At the consumer, the actual native checker exits 0 with clean child closure and
`CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION` for the 105,541-byte delta input,
hash `2cdef224538a722c56674a5e89387c8aac3dcea8caeb1cc9d1142ab28b2f0858`.
Independent byte comparisons establish:

1. Its sole required parent journal equals the freshly verified base I journal.
   Consumer receipt stdout is `REAL_MODULE_RECEIPT_VERIFIED`, fully resolved,
   for the exact base module and retained receipt hash `850c33b2...6e5d47`.
2. Its target journal equals the saved mixed binding's exact target journal.
   Decoded target ModuleID is `b4295706...ebb9f94`, with rank 1.
3. The mixed result binds the same packet hash and records
   `MIXED_BOUND_BEFORE_LIVE_PROMOTION`. The client proceeds through acquisition
   to its subsequent import-context request before the controller refusal.

Thus the genuine premise and actual native delta conclusion were combined on
the consumer path; a saved frontend or publication report was not substituted
for them. All handles are closed by terminal cleanup. The saved binding/result
is evidence of that execution, not a transferable acceptance credential.

The seed context reports zero frontend ancestor theorem-proof bytes. This does
not erase the new native delta witness checked at acquisition, nor prove
bounded cold cost for arbitrary unsealed ancestry. This one discovered result
also supplies no broad-search recall or useful-growth measurement.

### Exact outcome files and stopping point

Within the seed's `preparation/author-1` directory:

| File | Bytes | SHA-256 |
|---|---:|---|
| `source-request.json` | 61778 | `a5440640e3657fe7d817f2f76d6d295828cbf43ea65236130c9299ebf90ed9d9` |
| `worker-result.json` | 838 | `9bcd0794f2ee4032388997edf981d473dbea5bcff0b67d85b5e4a8bcefc261d0` |
| `frontend/EXPORT.json` | 14224 | `240512aa4eb5a77c9aa95efc20e93a15b8a082a5a032384c3adb3d861b09a6dc` |

Within the consumer's `delta/1` directory:

| File | Bytes | SHA-256 |
|---|---:|---|
| `packet.json` | 554165 | `92bbe15b0c8cfcba805efe86939009a9c0c53148e1c9fbd708d48fc6e0fe507f` |
| `native-0/stdout.txt` | 1520 | `06cfbfe9265c2a6b0d84d6c501816c2be63f1794a59973eb21e2648c6213e203` |
| `RESULT.json` | 1090 | `ddfecd90c13dfc9b298e1967b781ac321462489be2cf56bf05a097024cd72284` |

The run's `work/actual-result.json` is 106,892 bytes, hash
`f06d047dc44354bd1cedc98a86f9104a2b94323ed9cb9c952ba512c1d7184e58`.
It records consumer controller observation 97.875 seconds against a 90-second
controller allowance, one acquired native check and one newly begun import
session, but zero consumer author/publication calls. That counter does not by
itself identify which internal operation consumed the excess; separate source
analysis should locate the consequential work before any budget change.

Preserve and reuse this seed's successful artifacts if a fresh continuation is
selected. Do not author it again merely to get a whole-loop PASS. Any later live
receiver must still obtain authority through its appropriate actual admission
path; persistent packet bytes and this audit do not restore a closed warrant.
Root and the lifecycle reviewer own aggregate costs, termination adoption and
any next source/runtime selection. Operation 03 remains failed.
