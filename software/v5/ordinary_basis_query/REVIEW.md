# Independent source and selection review: basis-only query companion

2026-10-26. **GO for the exact controls01 selection; source GO for the exact
public01 selection only after root adopts clean controls.** This is a review
decision, not an actual test pass or v5 completion. No unresolved correctness
blocker was found in the final reviewed source. Root owns execution/adoption;
preserve and stop on any failure, with no retry or allowance renewal.

The review read the complete CONTRACT, query implementation, README,
IMPLEMENTATION, test source and TEST-PLAN, plus the relevant existing launcher,
owner/bootstrap/profile loader, native query command, semantic IDs and formal
query/discovery adapter. All review work was read-only except this checkpoint.
No product/test import, compilation, extraction, owner initialization, service,
network, repack, old-source edit or Git mutation occurred.

## Reviewed source identities

Paths are relative to this directory except the unchanged runner.

| File | SHA-256 |
|---|---|
| `CONTRACT.md` | `bfd342e4524b142f26f0df32137a7aedec1138842abacd31e212f0ddab253975` |
| `query.py` | `a3d0e7d4ec7da30296c0349a67d63d90d1fc611e22e2b4cfb69e7a6ff5a8a68a` |
| `README.md` | `c692d26e042dee0c9de4b79daa0f0018c863d4ddc471ff1383f220053ae4076d` |
| `IMPLEMENTATION.md` | `0a921aa72a6f669affc140069ea3710656293848a57880a7cf9c6d6cd5b72cb7` |
| `test_query.py` | `c2fb010137343b3324181476e5bc2ad972085fc9fc2f38231871c4f4891194ad` |
| `TEST-PLAN.md` | `655db5f358d4b98880fdb8e45e7ba03592df0c09d6b9dfa03f69a17621a0dc87` |
| `tools/Run-V5-Check.py` | `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651` |

## State-free binding argument

The new capability is preparing an exact-type search hint from an approved local
expression, without first proving a theorem or opening mathematical state.
It is not a new acceptance mode.

Let `N` be the exact reference census returned by the existing native-type parser
and `B` the unique-name set of the exact pinned 581-name inventory. The code first
requires the selected semantic module/ID and inventory hash, then checks all of
`N` against `B`. If any reference is missing, it raises `UnknownVocabulary`
before deriving any basis-symbol ID. Otherwise, in the parser's existing reference
order, it produces

`[name, basis_symbol_id(selected_semantics, selected_foundation, name)]`.

These are declared search identities, **not warrants that a basis was checked**.
The fixed descriptor/inventory hashes select an interpretation; they do not prove
foundation correctness or checker/runtime correspondence. The implementation
performs no basis native initialization, owner/catalog/custody opening, declaration
admission or proof-body checking. The requested type need not be inhabited.

Elaboration uses the approved selected runtime and already built fixed Init/query
helper environment. That support correspondence and protected immutable storage
are trust premises. The inventory filter prevents silently assigning a fixed
basis identity to an arbitrary foreign-project name; there is no foreign project
or caller-selected import/search-path interface. Approved syntax can itself run
macros/tactics/commands with account permissions, so the documentation correctly
does not claim hostile-source isolation or derive source approval from a hash.

`formal_query.bind_native_type` and `query_spec` remain unchanged. The worker
uses the already loaded discovery adapter's `namespace_for` and `compile_query`,
with shared-query module identity checked. There is no copied namespace formula,
new feature profile or guessed portable ID. This preserves the existing exact
structural-key interpretation, not arbitrary unification, equivalence or global
semantic-search completeness.

## Execution, output and failure boundary

The parent requires explicit local approval, strict bounded config/query JSON,
exact input hashes, finite integer limits and ordinary/fresh/separated paths.
It checks the actual installed contact launcher hash
`47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39`
before importing it and reuses its existing support binder and supervisor.
It does not add operations to that launcher's public allowlist.

The fixed child follows the existing owner bootstrap and complete package/profile
loader before one Lean command. Loading support is not opening an owner. Fixed
imports, quoted universes, a quoted fresh AST output path and sanitized runtime
paths bind this invocation. Native stdout/stderr inherit the supervised worker's
logs, avoiding unmonitored extra native log files. There is no native helper build
or second extraction path.

The original wall start and child deadline are carried through; five seconds are
reserved for parent finalization. Child CPU/memory/process/log bounds come from
the unchanged supervisor/Job. Parent work is bounded cooperatively and reported
separately. Clean completion requires exact zero exit, reaping, closed Job, zero
active/terminated descendants, no termination request/cleanup errors, coherent
selected limits and finite within-limit observations. Sampling/cleanup overshoot
and post-execution rather than hard disk caps remain disclosed.

Only generated source, AST and `.olean` are mandatory native outputs. The four
known ancillary suffixes are optional; every actual allowed artifact is hashed
and unlisted native entries refuse. The parent rechecks candidate pins, original
inputs and launch support after clean child closure. Worker output is explicitly
only a candidate. A complete fsynced/read-back pending report, followed by the
original-allowance check and Windows nonoverwriting rename, publishes the terminal
result. No partial pending file is a successful marker. This is not a claim of
power-loss-durable directory metadata or adversarial same-account race safety.

Full package/runtime validation remains inside the bounded worker. Later helper
and launch-support rechecks retain the existing immutable-runtime premise; this
review does not demand or claim a new full-runtime scan after every operation.

## Concrete findings resolved before use

- A direct success `RESULT.json` write could previously leave a success-looking
  file after a write/readback error. The final code publishes via validated pending
  bytes and nonoverwriting rename; targeted fault controls cover this boundary.
- Mandatory compiler ancillary files were an unnecessary assumption. The final
  allowlist distinguishes required outputs from the four permitted optional ones.
- Namespace/features now come directly from the existing installed adapter.
- Test expectations now match quoted universe identifiers. Repeated prelaunch
  controls reuse only the exact pinned launcher object after checking the intended
  import request, preventing stale-module refusals from masking real path checks.

## Focused tests and exact selections

The eight controls cover new query/config/source generation, prelaunch paths and
approval, fixed-basis binding, unknown vocabulary, synthetic closure, allowance
accounting and terminal publication. Actual stateless codecs and a retained AST
are used for binding; synthetic ASTs/reports/files are explicitly labeled and
create no accepted mathematics. Native/network/database entrypoints are trapped
in controls. The parent doubles exercise real candidate-pin, input-recheck and
publication functions, including pending fsync/readback faults. The private
worker, full native loader and actual Lean invocation are not qualified by mocks.

Public mode independently calls the new public companion once with
`forall (p q : Prop), And p q -> And q p`, requires the exact `And` reference
census, reparses the actual AST and recomputes bindings/QUERY/SPECS with the existing
codecs. It requires terminal/supervision/output agreement. Its namespace/features
check is worker-to-parent correspondence, supported by the reviewed direct
existing-adapter calls, not a second implementation of the namespace algorithm.

Exact prospective selection hashes:

- `experiments/basis-query-controls01-selection.json`:
  `a2294a66c2321b0c398f6690dc2965fe645243ca08427f7037253665c20b2281`.
- `experiments/basis-query-public01-selection.json`:
  `7aafc8f00605eeee4e141119b9f80e1cc2a390a19241cf112a93ba778a48f064`.

Both use the same seven source snapshots, all independently checked against the
hashes above. Public has the unchanged 163 external package/Python/Lean pins from
the service-plan selection; controls adds only the exact retained native AST
(`226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480`).
All 164/163 external pins match current files. Both fresh output roots were absent.
Test and companion run from the selected snapshot; explicit canonical workdir and
package/runtime arguments match the existing runner and the tested public grammar.

Outer limits for each: 120 wall seconds / 60 inclusive CPU seconds / 1280 MiB /
six active processes / 4 MiB stdout / 1 MiB stderr. Public inner original limits:
60 wall / 30 inclusive child CPU / 768 MiB / four active processes / 1 MiB per
log; its supervised child wall allowance is 55 seconds. The harness is separately
bounded by its 105-wall/40-controller-CPU cooperative checks. Nested CPU is an
included observation, not an extra charge.

Root should execute controls once, audit clean results, then separately select
the single public extraction. Stop this seam after its saved-outcome check. No
owner initialization, richer-project frontend, source archive repack, networking,
growth experiment or broad regression campaign follows from this review. Full
usable/deployable v5 and the user's local/unpublished boundary remain unchanged.
