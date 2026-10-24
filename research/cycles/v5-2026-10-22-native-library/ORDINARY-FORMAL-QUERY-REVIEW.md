# Ordinary formal-query seam: independent source review

2026-10-23; reviewer `formal_query_audit`. Source/theory review only.

## Disposition

**No blocking source defect found for the specified narrow query seam.** It is
reasonable to select coherent helper assembly and small changed-boundary controls
next. This is not compilation, installed integration, actual discovery, useful
growth, or release acceptance. No product code, tests, native tools, network,
owner state, or databases were executed or changed by this review. Git remains
root-owned. Only this review checkpoint was written.

The user has no existing local Lean project to supply. A fresh controlled project
can establish compatibility but must not be called real-user usefulness evidence.

## Reviewed identity and scope

Paths below are relative to the canonical root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| Source | SHA-256 |
|---|---|
| `software/v5/ordinary_formal_query/OwnerQueryCommand.lean` | `d488268d3e5118dcd121b504f051d3875d7e4d3d52badaf7198c9c86093fe59b` |
| `software/v5/ordinary_formal_query/formal_query.py` | `7901236768784a399f9ae5c56b374d040bce56536b0a47a6ee85093440cabcee` |
| `software/v5/ordinary_formal_query/discovery/ordinary_export_adapter.py` | `3ddbed2156a393b08543a5da88c89b5c5b9c2b4f65689c46fbd7623cec38db0a` |
| `software/v5/ordinary_formal_query/README.md` | `4ed5280b3cdf3cfcd97df0555fb2706b974a3c947e6abaab433b0bea9158ac1b` |
| `research/cycles/v5-2026-10-22-native-library/ORDINARY-FORMAL-QUERY-CONTRACT.md` | `add529b1cdec8831e4526aea37beac00e159f7e1bd3e4fa6bc98aa465d0b1d6e` |

All four selected source files and the contract were read completely; source
hashes above were rechecked at review completion. The next-benefit decision,
existing ordinary codecs/previews/semantics, adapter comparison and relevant
pinned Lean 4.34 APIs were also inspected. This review does not supersede the
separate installed-theorem or saved-runtime audits.

## What the seam establishes in principle

The owner already has a local formal type and knows the portable identities of
its referenced symbols. It can ask for candidates sharing that type's structural
key without possessing a target ExportID or proving the query. The pathway is:

`owner type → closed type AST → exact known symbol bindings → search key`.

This does not require a scratch theorem/axiom, accepted unit, proof exporter,
dependency-closure walk, or new acceptance rule. Unknown portable identities
remain an explicit usability limit: importing a declaration by Lean name does
not by itself reveal the portable SymbolID. Refusing or redirecting an unknown
mapping is preferable to rebuilding ancestry just to search.

### Lean extraction boundary

`withoutModifyingEnv` and `runTermElabM` follow the pinned command-elaboration
pattern. `Term.elabType`, synthetic-metavariable synthesis, instantiation,
`Meta.mkForallFVars ... (usedOnly := true)` and `Meta.check` have the inspected
Lean 4.34 signatures. Closing used section variables retains their dependencies
without adding every unrelated local variable as a premise. The existing codec
rejects open terms, expression/level metavariables, undeclared universe
parameters and malformed parameter lists. `Expr.hasSorry` explicitly refuses a
query containing `sorryAx` before encoding.

The command writes only the schema, ordered universe names and type DAG. It
does not write a theorem name, proof, evidence unit, locator or acceptance flag.
The codec encodes arbitrary name/literal strings as byte arrays in the existing
single-key byte-object format; the remaining strings are fixed ASCII tags.
Thus the inspected array/codec output avoids object-order and string-escape
disagreement with Python's strict canonical JSON vocabulary. Actual native
round-trip validation is still required.

`OriginalExpr` is one of the existing package builder's public source modules;
the builder preserves its body and changes its legacy header to `module` and
public imports/section. The new command's public-meta import/section convention
matches existing owner commands. This supports assembly plausibility, not a
claim that the new command was compiled.

Output is an explicitly owner-selected absolute fresh path, with exclusive
creation and no overwrite. Parent-directory symlinks and concurrent local
filesystem interference are not fully excluded. That is acceptable only within
the documented trusted owner-local boundary, not as a peer-selected output-path
API. Owner macros/imports can execute code, and environment restoration does not
undo external effects. Resource limits are not a hostile-source sandbox.

### Key agreement and invariance

Let `N(T,B)` be the rooted expression tree represented by a validated DAG `T`,
with constant/projection names replaced by their exact binding `B`, binder labels
erased, and universe labels replaced by their declared ordered positions. All
other retained fields are unchanged. This is a mathematical description for
the argument, not an implementation that expands the DAG.

The key hashes each node's tag, retained fields and already computed child
hashes. Induction over backward DAG edges gives:

- Equal normalized nodes have equal hashes, regardless of their numeric node
  indices or whether equal subexpressions were shared.
- Hence equal `N(T,B)`, selected semantics, profile and universe arity produce
  equal keys. Binder/universe-label renaming preserves a key when the ordered
  universe positions and all other fields are preserved.
- Conversely, recovering different normalized inputs from the same key would
  require a collision at the root or some differing descendant hash. This is a
  cryptographic search-filter assumption, not a mathematical equality theorem.

Query and preview paths invoke the same private key routine after their own
bounded syntax/binding validation. Semantic ID is checked against the selected
ordinary semantics, which already binds the foundation. Binder annotations,
level instances, ordered universe arity/positions, let flags, literals,
projection symbol/field and expression tags remain in the key. There is no
normalization by reduction, instantiation, premise permutation or proof-body
traversal. Definitionally equal formulations can miss.

All public entry points reparse bounded raw bytes. The complete sorted binding
census must equal the exact reference census, rejecting omissions, extras,
duplicates and order errors. Caller-supplied associations may still be false:
they are search inputs only. The parser need not itself prove the query or reject
every untrustworthy named constant; only the owner command promises its explicit
`sorry` refusal. Neither successful parsing nor key equality warrants a result.

### Index and acceptance separation

The successor adds one required type-key feature, a helper dependency, stricter
limit preflight and a new feature revision/profile namespace. Record/locator
and exact evidence binding remain unchanged. Generic record validation imports
`discovery.ordinary_export_adapter`; a coherent assembly must replace that exact
module and supply `formal_query` plus the existing ordinary helper closure.
Dropping the new adapter into an old isolated assembly is not sufficient.

Old index snapshots must not be silently treated as new-profile snapshots.
Reindexing, storage and maintenance are real costs. Adding a required feature
can exhaust the existing finite feature cap for a previously maximal record;
that is a profile/resource refusal, not mathematical invalidity. Search remains
advisory; native checking and warranted dependency matching remain indispensable.

## Cost and claim limits

The bottom-up key pass is linear in supplied DAG nodes/edges and retained field
bytes and does not expand a shared tree or replay proof ancestry. Its
`key_node_visits` counts only level/expression visits, not physical CPU or whole
query cost. Parsing, validation, name encoding and sorted reference census add
work; do not describe the entire operation as strictly linear in node count.

The native final-byte check occurs after elaboration and serialization. A small
query can require expensive elaboration/type conversion, and intermediate work
can exceed final-output size. Finite process CPU, memory and wall limits remain
necessary. The command's node/byte limits also do not guarantee acceptance by
every stricter downstream profile; downstream refusal is explicit and safe.

An exact bucket can be very large. This seam proves neither efficient general
semantic discovery nor complete global coverage. It also does not instantiate
the project's full-cost benefit inequality. Ordinary `#check`, Loogle-style
search or package sharing can be cheaper; the ordinary comparator must receive
the same query facility. Stop or redirect if exact contract formulation or
unknown-symbol mapping makes this route less useful than those alternatives.

## Smallest decision-changing follow-up

Root, not this review, selects execution. Avoid a broad campaign.

1. Compile only the coherent new helper boundary, then extract one independently
   authored natural contract: close used/dependent section variables, omit an
   unused variable, and preserve an explicit universe order. Refuse an unresolved
   universe/metavariable or `sorry`; inspect actual JSON with the real parser.
2. Pure controls establish query/preview agreement without copying the returned
   target type into the query; alpha-label/shared-DAG invariance; and intended
   nonmatches for binder annotations, universe positions/arity/structure,
   symbol IDs, let flags, literals and projection fields.
3. Refusal controls cover missing/extra/duplicate bindings, malformed/open/orphan
   or oversize syntax, wrong semantics/profile and attempted limit relaxation.
4. Verify namespace separation, coherent adapter selection and unchanged exact
   candidate/evidence binding. Then consider at most one actual discover/use
   discriminator if the workflow still has plausible whole-cost benefit.

Passing these establishes compatibility of this interface only. It is not a
reason to claim sustained growth or fund increasingly elaborate exact search
without evidence of a practical user's saved work.

## Addendum: prospective pure controls and selection

Source review of `query_controls.py`
`11f99eee82cbbcde951dad12caa648361d7de45f4319c429c638274347a5f8b2`
and `ORDINARY-FORMAL-QUERY-CONTROLS.md`
`af1663a8330173d33013c1da4f9159a427560ee0f19f0e0ec826a03c589329dd`:
**no blocking source defect found; clear for root's selected pure run.**

- All 42 cases were traced against the actual APIs: 22 positive metadata
  relationships and 20 exact refusals. The independently written base/preview
  DAGs are closed, fully reachable, and have the same retained structure and
  11 level/expression visits. The shared/expanded DAG cases retain reachability;
  duplicate nodes are permitted at this syntax-only boundary. They do not claim
  canonical native evidence or well-typed mathematics.
- Structural changes reach their intended key fields. Missing/extra/duplicate/
  reversed bindings, open roots, orphan expressions/universes and explicit small
  bounds reach the specified refusal strings in the inspected validation order.
  No false expectation of semantic typing was found. The let-flag and application
  examples are deliberately inert syntax fixtures, not Lean validity claims.
- The eight actual modules are preverified and executed from retained bytes,
  with a correctly named empty-path ephemeral package for the real relative
  adapter callback. The adapter case checks real feature inclusion, the new
  namespace descriptor, V3 validation and exact preview resolution. No alternate
  key implementation, Store, native or network path supplies the outcome.
- The harness reports only successful completion after an exact case census and
  source rereads. Its internal clocks and external-call tripwires are not an OS
  sandbox. Failure remains failure; no automatic retry exists.

Selection `experiments/v5-local-checks/ordinary-formal-query-controls-01.selection.json`
`07c1b58a60a89d7272117f53419ee58fa3b874dd7de3bd1f7de52d1ef57fca02`
matches the harness interface, all ten selected source hashes, three explicit
Python runtime pins, `-I -S -B`, snapshot inputs and fresh `controls` output.
Its 45-wall/25-CPU/512-MiB/two-process outer profile contains the harness's
35-wall/20-process-CPU checks. This was a selection-consistency glance, not a new
audit of the unchanged supervisor or runtime binaries. No execution occurred.

These finite controls do not cover native elaboration, every invalid field,
older-snapshot migration, real lookup, mathematical admission or useful growth.
Their deliberately narrow scope is appropriate for this changed boundary.

## Addendum: saved pure-control outcome

**PASS for the selected pure query/preview/adapter metadata controls.** Reviewed
only retained data under
`experiments/v5-local-checks/ordinary-formal-query-controls-01`; nothing reran.

- Saved outer selection is the selected `07c1b58a…` operation. Actual argv,
  canonical cwd, snapshot inputs and limits agree with it. All ten snapshot and
  original source hashes match selection; all eight report module paths/hashes
  match those actual snapshots. The coherent real adapter, not a replacement
  fingerprint engine, supplied the feature/namespace/resolution result.
- Report and parsed stdout agree. There are exactly 42 recorded outcomes:
  22 positive relationships and 20 exact expected refusals, matching the reviewed
  census. Query/preview agreement reports 11 key-node visits; the adapter case
  retains `UNPROVED_METADATA_ONLY` and the overall mathematical-acceptance flag
  is false. No native or discovery-network operation is claimed.
- All 134 retained raw-fixture hashes independently match their UTF-8 bytes.
  The 66,879-byte fixture envelope hashes to
  `eafc880d6c4bd267ab7919369b1e069ed490bac762e201ea987c8704a158f0e4`,
  exactly as reported. The 9,776-byte report is
  `ec6aff57c7fb491f2db3ce27f30b3f2a52eb9d23e3c22f43312ed634d99cfc2b`.
- Outer result `921daf087a4c63a93fd66b9549c0e04905eb2df8e4682634309ba8f57539f9b8`
  records exit 0, direct child reaped, zero active processes, closed Job,
  no cleanup errors and empty stderr. Wall time is 0.6243837 seconds. Known
  inclusive Job CPU is 0.25 seconds plus 0.109375 wrapper CPU = 0.359375 seconds;
  the 0.140625 inner-controller CPU is already included, not added again.
  Peak Job-private commit is 23,572,480 bytes.

Adopt this small changed-boundary result without repeating it. Native query
elaboration/actual JSON compatibility, installation and practical use remain
separate gates. The full v5 goal is not completed by these metadata controls.

## Addendum: two-call native discriminator source review

**No blocking source defect found; clear for the exact selected native boundary.**
Read complete `native_query_check.py`
`45c2a50b8d6a423846fe884ae5b42e1e55d25cad5f401593ceb36d234679971f`,
`QueryNativeFixture.lean`
`91e58051c4e32886a420fc3aad71971b53e8e52bad70b7ceadec846a02d18795`
and `ORDINARY-FORMAL-QUERY-NATIVE.md`
`fead16a5bdfa6e5d90e0c04971f93e18d36b4dd80fd5d80ce5db8173899a4a62`.
No native operation or Python product code was executed by this review.

- The test wrapper calls the real `#ordinary_type_query`. Pinned Lean 4.34
  exposes `Environment.constants` and `SMap.foldStage2`; the latter folds only
  local `map₂`, ignoring imported `map₁`. Its callback reads names, not bodies.
  Comparing the before/after name arrays tests no persistent local declaration
  insertion during this invocation, not a general proof of absence of effects.
- The independent query is pointwise equality of arbitrary dependent functions,
  with no asserted truth, theorem name or proof. `runTermElabM` plus used-only
  closure predicts `{A}`, then `B`, `f`, `g` and the inner explicit `a`; the unused
  Nat variable is absent. Types need only sorts, bound variables and `Eq`, giving
  the asserted exact reference census and explicit `[u,v]` parameter list.
- The two calls compile the new helper and fixture, reusing the retained public
  `OriginalExpr` companions. The source/path substitutions are bounded, fresh
  and owner-local. The actual native JSON then enters the real selected query
  parser, exact binder/census checks, fixed-basis `Eq` identity and query spec.
  No proof ancestry, source exporter, owner Store or network lookup is invoked.
- Input/compiled-output pins, zero diagnostics, five companions per module,
  clean process closure and final resource checks are required. Actual child
  Job CPU is charged once; unknown accounting fails while retaining its grant.
  Query-spec computation precedes the final pin/budget check. Final reporting
  is still covered by the outer supervisor. Partial files remain preserved.

Selection `ordinary-formal-query-native-01.selection.json`
`1eb9f8018a882842446c0749f09a424c57a1b3bf9df0388233fe9137a705a422`
has the five expected source hashes, isolated interpreter/argv and fresh output.
Its 156 runtime pins were compared as data and are exactly identical to the
retained relocated-smoke selection. Outer 90-wall/60-CPU/2048-MiB/eight-process
limits contain the stated inner 80-wall/50-CPU/1536-MiB allowance and two bounded
calls. The existing runtime profile and supervisors are reused, not requalified
by this consistency review. This gate establishes extraction compatibility only;
actual lookup, downstream use, benefit and full v5 release remain separate.

## Addendum: native01 failure, preserved

The selected native01 run **failed** on its first compile. My preceding source
clearance missed Lean's resolution of unqualified `liftIO` to
`Lean.Elab.Command.liftIO : IO α → CommandElabM α` inside the `TermElabM`
callback. The actual diagnostic is a type mismatch, not a resource failure.
This corrects the earlier source plausibility assessment; do not treat that
assessment as compilation evidence or relabel native01 as a passing query test.

Independent saved-data inspection verified all five source snapshots and 16
input pins. There is one failed native call, no `OwnerQueryCommand.olean`, no
fixture invocation and no `query.json`. Outer and inner records show exit 1,
clean reaping/Job closure, zero active or terminated processes, and no cleanup
errors. Outer wall is 5.6851941 seconds; known inclusive CPU is 2.703125 Job +
1.640625 wrapper = 4.34375 seconds. The inner 2.46875 CPU is already included.
Outer result is
`eb01e2733f01c8f36de68de6863b2f1d35b69a7324bf6e04d0ce9ddd067d2d20`;
native result is
`acdc695794d9b1301d388c747000273e8466965c5529d3fbb1aa0cf2251fc71f`.
All failed artifacts remain untouched. No runtime was executed by this audit.

The first unused successor proposal used `liftM (m := TermElabM)`. Review caught
that `m` in `liftM := @MonadLiftT.monadLift` is the source monad, while `n` is
the target (`Init/Prelude.lean:3942–3949`). That proposal is not cleared as an
explicit IO-to-TermElabM repair: it would rely on an additional implicit lift.
Use `liftM (m := IO) (n := TermElabM)` to state the intended operation directly.
The pinned `MonadLift IO CoreM` instance and MetaM/TermElabM transformer chain
support that operation. Any final successor needs its own exact hashes and
root selection; native01 is not retried or overwritten.

### Final unused native02 correction

The ambiguous proposal was corrected before any execution. **Clear the narrow
source delta** at command02
`f71bb36f23edff62b8e48fde803e159a93e1ec5f62541d11d357c59e79971992`,
harness02
`4e19868999a078246be8e7a7e269f50e27e50b2b128b586c118cd6b60a883837`,
selection02
`56b4cd0613f3753040f903386469d78f6b1ef6d6a6169a496da46e30da6430cd`.

Exact text comparison confirms only the intended product line changes to
`liftM (m := IO) (n := TermElabM) <| ...writeType...`. `TermElabM` is exported
by `Lean.Elab.Term`; its target name is available through the existing opens.
The harness differs only in the new command pin, command source filename and
snapshot source filenames; generated logical module names and both native calls
are unchanged. All five selection source pins match current files; the same 156
runtime pins, fixture and original finite limits are retained. No execution or
successful compilation is claimed by this final delta review.

## Addendum: native02 partial success, whole run failed

**Native02 remains FAILED.** Saved outer result
`d4d326d36146279fe9ecf254eb1b3f51c5f8ae95392696830e43c5eeb7fd3f70`
and native result
`cdbb4cbddd4b78cbc16df7fb115c974c0adbd887a9616f133e67f9ade3cf582f`
were inspected without rerunning any product operation.

Both selected Lean calls exited zero with clean closure, no termination or
cleanup errors, and all four native stdout/stderr files empty. All ten generated
companions exist and are nonempty. The generated command source has the exact
selected `f71bb36f…` bytes; the generated fixture is exactly its selected template
with the single fresh output-path substitution. Its declaration-name assertion
therefore ran successfully. All five snapshot hashes and 16 initial input pins
were independently rechecked.

The actual query is 649 bytes, SHA-256
`fa1965b1c69bcbe479e66e65d19bbea710fde294ce2e00e603c0636207735ef5`,
ending in byte 93 (`]`), not a newline. Inspection finds four universe nodes,
21 expression nodes, parameters `[u,v]`, sole constant reference `Eq`, and outer
binders `A` implicit followed by `B,f,g,a` explicit. The executed source checks
the real query parser, parameter/reference census and these binders before the
inventory read. The retained query's bounded closed/reachable structure agrees
with those checks; no theorem proof or returned candidate supplied it.

The observed `EvidenceError: JSON_LEXICAL_TOKEN` is explained by the following
fixed-support inventory read. Its 823,690 raw bytes hash to the selected
`c81800abbe3f421b2e3d3687e864946e9c0dd43a97a118034c79376f7cdba1b0`
and end in byte 10 (LF). `ordinary_evidence.strict_json` rejects whitespace
outside strings, including this final LF. That strict reader is appropriate for
the canonical query envelope but was the wrong unadapted reader for this retained
support-file encoding. The failed run did not produce `bound-query.json` or reach
its final pin/budget check. Do not describe it as an overall passing native test.

Known whole-run cost is 4.3129556 wall seconds and 2.59375 outer Job + 1.421875
wrapper = 4.015625 CPU seconds. The two inner Job charges, 1.046875 and 1.125,
are included rather than added again. Outer exit is 1 with clean closure.

The five command companions are identified below for a separately selected
saved-output continuation, **not yet adopted as completed package inputs**:

| Companion | Bytes | SHA-256 |
|---|---:|---|
| `OwnerQueryCommand.olean` | 85512 | `0dcf8f7ba86ef053001876d1dfe70245bc494cddc6b8c3d8e5ac5069c82da4e2` |
| `OwnerQueryCommand.olean.private` | 204000 | `6264acaefd4796dacb162e1ad2448709a5bedcccc64c63fcaf0fcf1779cfccb5` |
| `OwnerQueryCommand.olean.server` | 1856 | `f9aaec7c95b2f81462f0faab5ee53c1125f17c9a5d7367bea9c8576fc421fcfe` |
| `OwnerQueryCommand.ir` | 73384 | `ad8627e47bf8bbcfc5401dac6316f2c91792214b184df1c3f825c5c32cb42866` |
| `OwnerQueryCommand.ir.sig` | 176 | `8777e7153d3ce8e581d31c625e4c515d886132f6e63ec95ea201045859bcf948` |

Economical continuation: preserve native02, verify its exact saved query,
compiled outputs and original inventory hash, then use a documented adapter for
the inventory's known single terminal LF **in memory only** before its bounded
metadata parse. Do not trim arbitrary query/evidence input, weaken their strict
reader, rewrite the inventory or recompile successful modules. Complete the
known-basis `Eq` binding and real query spec in a fresh pure operation, recheck
all retained pins and record a separate result. Exact compiled-artifact adoption
should follow that successful saved-output review, not precede it.

## Addendum: pure saved-output continuation source clearance

**No blocking defect found; clear the selected pure postcheck.** Read complete
`native_query_finish.py`
`40b2b17e0c536c1987199970f5db795ab9d9e1826c95d2075636fcfa46fc0dd3`,
its exact retained support module
`8d0238e312bca697b7d74d01785581bfc5954f45942cb134a369a108ca4f80a1`,
and the selected supervisor's operational `strict` reader. No code executed.

The continuation requires the exact failed outer/native results, 17 pinned saved
files, original five source/snapshot identities, 156 runtime pins and 16 initial
inputs. It checks outer exit 1, both inner zero exits, clean closures, actual
command/log bindings, generated source substitution and absence of earlier bound
query outputs. The exact saved stdout is the required 22-byte failed-status line
with CRLF. There is no opportunity to substitute another successful native run
or silently label the old run successful.

The inventory is bound both by its installation manifest and `S.INVENTORY`, then
read unchanged using the existing operational JSON reader that permits its LF.
No normalization, rewrite or relaxation of `E.strict_json` occurs. The real
strict query parser and known-basis symbol/key helpers run on the actual saved
query. The source rechecks the binder/reference contract and 581-row fixed basis,
requires exactly one `Eq` row, and writes only fresh bindings/query/report files.

Support imports are from exact verified bytes; imported modules have inert
top-level declarations. No support `main`, compiler, owner, database or network
call is used. Subprocess/socket/database entry points are additionally blocked
as tripwires, not a sandbox. All held input bytes are rehashed before output;
fresh query/binding pins are reported. The report retains `original_run_status:
FAILED`, `acceptance: false` and `native_calls_performed: 0`. Compiled artifacts
are only eligible for independent review and root adoption, not mathematical
authority from this report alone.

Selection `ordinary-formal-query-postcheck-01.selection.json`
`2f10e6eeb2316106cfb37f705c85e75b95dc3f651684c9f9188d554113b5907e`
matches both snapshot source hashes, three unchanged Python pins, isolated argv
and fresh `postcheck` output. Outer 45-wall/25-CPU/512-MiB/two-process limits
enclose internal 35-wall/20-process-CPU checks. This is a fresh pure continuation,
not a retry of either successful native compile or the failed whole operation.

## Addendum: saved postcheck outcome and exact artifact eligibility

**PASS for the separate saved-native-query postcheck.** No rerun was performed
by this audit. The actual selection, argv and output are consistent with source
clearance above. Both new source snapshots and their current originals match;
all 193 report-held input paths were independently length/hash verified. Fresh
bound-query and bindings bytes match their reported lengths/hashes. Saved command
argv/cwd/limits agree with the outer result, stdout is the one postcheck PASS
line, and stderr is empty.

The real query helpers accepted the saved 649-byte native query, exact `[u,v]`
parameters and `A1,B0,f0,g0,a0` binders, and produced the selected-semantics
known-basis `Eq` binding. The 956-byte bound query is
`91dc89dc17e17f01b8b081e05be65afbafe6407faf6e2230c12f14703cc22edf`;
96-byte bindings are
`7b218838c14908ef5b79ebd0362fd74b04bc4600dc4857dcbd01bbfb9ff78c7c`.
Its `declared-type-key` is
`7f7601e62e607449371c61fcc3c6d0ddc0c4963a52d1daab1be58b39e4d0528c`.
There was no new native call, theorem proof, acceptance or search operation.

The report still declares `original_run_status: FAILED`, and both original
failure results retain their audited hashes. This completion does not rewrite
native02. Jointly, the two successful saved native calls and this postcheck now
support root adoption of exactly the five command companions listed in the
native02 addendum for a separately selected compatible assembly. They do not
qualify that assembly or arbitrary helpers, platforms, theorem search or growth.

Postcheck report hash:
`73fc37e92c211487a4cd65acc26f90f9323a333c66c8877ff14e487031bc3b25`.
Outer result hash:
`0feafa4a167a91d36dcf99c3448ef1ce9854feebb252b070125445199cc03701`.
Exit is zero with clean reaping/Job closure, zero active/terminated processes and
no cleanup errors. Recorded operation cost is 1.9144335 wall seconds and
1.6875 outer Job + 0.078125 wrapper = 1.765625 known CPU seconds; inner
1.546875 CPU is included. Peak Job-private commit is 36,143,104 bytes.

The adjacent invocation note records an earlier relative-selector launcher
rejection. The unchanged runner's absolute-path check precedes selection reading,
run creation and child launch, consistent with that note. This was a corrected
launcher argument, not a repeated native/query workload. Its separately unmeasured
launcher overhead is not claimed in the recorded operation totals above.
