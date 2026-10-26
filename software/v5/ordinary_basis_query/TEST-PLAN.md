# Focused basis-query wrapper checks

2026-10-26. Owner: `cold_start_workflow`. Contract read in full; canonical guard
passed. SOURCE ONLY: no test, product import, compiler/native process, owner
initialization, catalog/custody access, network operation or Git mutation has
occurred. Root selects execution only after independent source review. The only
assigned files are this plan and `test_query.py`; implementation belongs to
`service_lifecycle` and independent review to `update_trust_lifecycle`.

## Decision and scope

Test the new input/execution/output boundary, not the already tested query
elaborator, query-key semantics, owner admission or search. The control suite
uses the actual selected stateless codecs and fixed inventory where appropriate;
synthetic supervision reports are explicitly operational test data and supply
no mathematical acceptance. No catalog, custody, accepted root, theorem evidence
or acceptance fixture is created or supplied.

The public extraction is a separately selected mode. It must execute exactly
one invocation of the new public companion and one Lean extraction, with no
fallback or retry. Control execution alone must never start a subprocess.
The script must be run with the selected isolated Python and canonical cwd;
every output leaf is fresh and all retained failures remain untouched.

## Eight focused control groups

1. **Strict query input and fixed source generation.** Reject duplicate JSON
   keys, malformed encoding/JSON, unsupported fields, wrong scalar/container
   types, duplicate/invalid universe identifiers, empty/oversized type text and
   excessive universes. Check the generated fixed imports/universe order/query
   command and safely quoted output path. Owner-approved term text is executable
   Lean syntax, not a hostile-code sandbox; tests must not assert injection
   filtering that the contract does not promise.
2. **Config, approval and finite limits.** Require exact config fields and
   digest shapes, reject unsupported raw argv/project/import/executable options,
   boolean numeric limits and out-of-range/missing allowances. Missing explicit
   local-query approval must fail before child launch. These are new wrapper
   validation checks, not another supervisor test suite.
3. **Actual fixed-basis interpretation.** Load only the package's hash-selected
   stateless ordinary evidence/semantics/preview/formal-query modules. Use an
   existing retained actual native query AST as inert data, or a labeled minimal
   type-only AST where needed; derive expected exact bindings independently
   from retained known basis identities. Require only referenced fixed-inventory
   names, exact ordering, existing semantic/foundation IDs and unchanged
   `formal_query` QUERY/SPECS output semantics. No owner/context loader is used.
4. **Unsupported vocabulary and inventory binding.** A well-formed inert AST
   referencing a nonbasis name must refuse/report it before producing usable
   hints or deriving a guessed ID. A different name with plausible local meaning
   is not authorized by a matching context label. Tampered fixed inventory bytes
   must fail. Keep the unknown-name fixture separate from genuine native output.
5. **Freshness, pins and path separation.** Existing output and overlaps with
   selected source/config/runtime/package refuse; mismatched config/query/source
   pins refuse before a child can run. Preserve pre-existing bytes. Exercise the
   actual wrapper path/binding helpers with bounded temporary files, not a fake
   accepted installation or copied historical state.
6. **Closure uncertainty.** Explicitly synthetic child reports
   exercise clean zero-exit/reaped/closed/no-active-process success versus nonzero
   exit, active/terminated children, cleanup error, termination request, missing
   or nonfinite accounting. Boolean zero/CPU values are not accepted as numeric
   observations. This is a predicate control, not a repeat of actual Job tests.
7. **Original allowance accounting.** Reject missing, renewed or mismatched
   child limits, over-limit wall/CPU/log observations, boolean/negative log sizes
   and missing/nonfinite wrapper accounting. Child CPU must not be added twice
   to its containing Job total; wrapper CPU stays separately identified.
8. **Parent terminal gate and publication.** Inert `setup`/`supervise` doubles
   use real bounded file readers, `candidate_pins`, `recheck_inputs` and final
   publication code. Check one fixed worker argv/original deadline, successful
   synthetic closure versus unclean reports, boolean native exit, changed output
   pins, changed input bytes, failed support rebind and missing/extra native
   artifacts. Explicit fsync/readback faults on `RESULT.pending.json` must leave
   that pending file and no `RESULT.json`. A WORKER candidate alone is never a
   successful terminal marker. All fixtures are labeled synthetic, not native
   ASTs or accepted installations. No subprocess is used.

The source is complete against `strict_json`, `validate_query`, `source_text`,
`validate_config`, `basis_bindings`, `make_hints`, `clean_supervision`, `setup`,
`candidate_pins`, `recheck_inputs` and `parent`. The prelaunch group loads the
exact installed launcher once under a test-owned module name, then checks every
intercepted duplicate-load request's name/path/hash before returning it. This
avoids accidental PRELOADED_SOURCE refusals masking intended path boundaries.
No owner loader, acceptance/state API or real supervisor is called by controls.
The valid prelaunch case does execute the real read-only support binding.
Broad reinvention of codecs, path frameworks or Job behavior is excluded.

The listed topics are executed in order 1, 2, 5, 3, 4, 6, 7, 8. This keeps
prelaunch checks inside the implementation's original bootstrap allowance.

## Source-ready harness invocation

Use the selected Python with `-I -S -B`, explicit canonical cwd and an outer
finite Job selected by root. The harness's own cooperative ceiling is 105 wall
seconds / 40 CPU seconds, without renewal. Exact invocation grammar:

```text
PYTHON -I -S -B ABS/test_query.py --mode controls|public
  --source ABS/query.py --source-sha256 HEX
  --package ABS --python-runtime ABS --lean-runtime ABS --output FRESH_ABS
  [--native-fixture ABS]
```

Controls require the retained native fixture; public mode rejects that option.
The retained fixture is
`experiments/v5-local-checks/ordinary-query-public-01/public/query-local/native-type.json`,
SHA256 `226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480`.
Each mode creates its own fresh root and `TEST-RESULT.json`; failures and every
partial file are retained. There is no test retry, cleanup deletion or fallback.
Successful synthetic parent fixtures are nested under `terminal-ready` and
unambiguously labeled synthetic in the control report; they cannot be used as
real query output.

Selection source needs: pin this harness and the new companion; retain contract,
plan and implementation/readme/review identities for source audit; reuse the
163-file package/Python/Lean immutable input map below. Controls additionally pin
the retained AST. Harness-created query/config bytes are deterministic from this
source and selected absolute arguments; their hashes are recorded before public
execution in `PUBLIC-INVOCATION.json`. This is source readiness, not launch approval.

## One proposed public extraction

Use the actual default package:

`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`

PROFILE:
`b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`.
Installation manifest:
`32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.

Root can reuse the already enumerated immutable external input map in
`experiments/service-plan-controls01-selection.json`: 154 actual package files,
three Python files and six Lean files. Its identity selection is reusable input
data, not permission to rerun the service-plan test. Root additionally pins the
new query/test/contract/plan sources and explicit query/config input selection.
No native helper build or new package assembly is required.

Proposed owner-authored query input, not yet executed:

```json
{"universes":[],"type":"forall (p q : Prop), And p q -> And q p"}
```

This is a formal question, not a theorem declaration, proof or claimed new
mathematics. Read-only inventory inspection confirms `And` is in the fixed
basis. The actual native AST should reference exactly `And`; the codec will
determine and validate that census. Do not insert dummy declarations or call
`owner contribute` to obtain query syntax.

Proposed child allocation: 60 wall seconds, 30 inclusive child CPU seconds,
768 MiB private commitment, four active processes and 1 MiB per log. Proposed
outer test envelope: 120 wall seconds, 60 inclusive CPU seconds, 1280 MiB and
six active processes, with bounded logs. Final values must match reviewed
implementation bounds and root's exact selection; no allowance renews on
failure. A separate native-free controls envelope can be smaller. These are
finite ceilings, not measurements or a performance claim.

Required actual observations:

- New companion public argv/config/query hashes and current package/runtime
  identities match selection; no owner/catalog/custody arguments or path exists.
- One fixed worker and one Lean process use only the selected runtime and
  already compiled helpers. Generated source contains the selected question,
  fixed imports and the fixed fresh native-output path.
- Native extraction exits zero; actual whole child tree is reaped/closed with
  zero active/terminated processes, no termination request or cleanup error.
- Reparse actual AST with the existing codec; exact basis bindings correspond
  to its actual reference census. QUERY equals binding that AST with those
  bindings; SPECS equals the existing query spec on that QUERY. Report/output
  hashes and the terminal marker agree only after final binding checks. The
  required native artifact is Query.olean; the four known ancillary suffixes
  may be absent but are bound when present. No unselected native file is allowed.
  Namespace/features must agree between WORKER and terminal RESULT; exact query
  and spec semantics are independently recomputed with the selected codecs.
- Successful terminal claim is ready search input, explicitly no mathematical
  acceptance. No owner initialization, proof admission, provider, network query,
  support rebuild, project import or publication occurred.
- All original source/runtime/package and retained prior evidence remain exact.
  Report outer inclusive CPU and wrapper CPU once, without adding nested worker
  or Lean CPU again. Retain every partial output and failure.

The native mode should not run a second extraction for a negative control.
Prelaunch refusals and uncertain-supervision logic belong in the native-free
groups. If the actual invocation fails, preserve it and stop; source diagnosis
and any later fresh selection belong to root.

## Reused evidence and stop

Reuse the 42 formal-query/preview controls, the existing compiled native command
and its preserved first harness failure/postcheck, eleven context-binding
controls plus actual context integration, and
`research/cycles/v5-2026-10-22-native-library/ORDINARY-QUERY-PUBLIC-OUTCOME.md`.
Their positive claims do not become a new run under this wrapper, but they remove
any reason to rebuild the helper or repeat query/search/mathematics campaigns.

Independent review checks the complete wrapper, these controls and the exact
later selection. After the one changed-boundary extraction and saved-output
review, stop this seam. No richer-project frontend recovery, filter backend,
growth result, external deployment or source archive repack follows.
