# Core implementation selection

2026-10-20. Final deployable v5 remains the goal. No memory census, compiler,
layout, or cryptographic proof run is selected. The completed builds and all
previous evidence remain untouched.

## Selected: isolate invalid discovery replies

Concrete obstacle: `search_resilience._send` calls `SearchSession.accept` on a
200 reply outside recovery; the ordinary client's decorator then destroys live
warrants/context on any invalid metadata. A hostile or mistaken index can
therefore prevent reaching an honest alternative within the same grant.

Implement a fresh validation-only metadata gate plus transport successor in
`software/v5/transport/search_validation.py`, reusing existing bounded exchange,
ticket reservation/settlement, and exact owner checks. Validate only the current
reply and touched snapshot/partition. Do not copy the entire session, extend
budgets/deadlines, retry automatically, or change mathematical admission.

Expected input-validation errors within the pure gate return a typed rejection.
Local liveness/deadline errors must escape that classification. For rejection,
abandon the original ticket once at its full reservation; promote no summary,
candidate or coverage. For success, invoke unchanged `accept` outside the
recovery catch. Double metadata verification is an explicit initial tradeoff:
bounded extra local validation rather than a risky rewrite of stateful commit.
Unexpected exceptions and all actual commit failures remain fail-stop.

`core_search` owns the helper, its focused tests, and SEARCH-DECISION.md.
Root owns `client/workspace_validated.py`, a thin successor preserving staging
and all mathematical owners, integration, runtime selection and Git.
`core_release` independently challenges the new boundary after its client
construction proposal. No prior suite is rerun merely to collect green checks.

Changed-boundary validation should cover invalid offer/candidate/coverage,
invalid-first then honest response with unchanged live context and budgets,
no metadata promotion, conservative settlement, and fatal deadline/local/commit
errors. Tests must be lightweight and not invoke a prover or native checker.

## Next deployment seam under decision

The actual ordinary client factory is tied to fixed experiment inputs and
phase names. `core_release` proposes the smallest release-owned configurable
constructor using existing owners, exact source pins and operation grants.
`core_growth` confirms that another generic benefit calculator would duplicate
the retained model and cannot invent absent provider/comparator costs; it will
instead test the selected factory. Root must record its exact source scope
before implementation.

Root now selects the proposed minimal release-owned constructor:
`core_release` owns fresh `software/v5/client/runtime.py` and RUNTIME.md;
`core_growth` owns fresh `software/v5/client/test_runtime.py` and the concise
test/result section in GROWTH-DECISION.md. Existing actual/terminal assets and
profiles stay unchanged. The API takes explicit locally adopted pinned
preparation/runtime data and the launcher's selected source map; it must not
infer authority by hashing arbitrary current files. Math receipts, theorem IDs,
ports and fixture phase names are not construction inputs. Support explicit
I-only atomic or A/evidence/staged modes through the exact existing owners,
without downgrading A to I when unavailable. Enforce original grant sublimits,
source closure, earlier deadlines and fail-closed cleanup on construction error.
No native/proof run is selected; root reviews sources and selects only the new
cheap constructor-boundary controls. Optional proof generation and security
policy remain outside this factory.

## Selected first runtime: search validation

Root has read the helper, facade and eight-control test source; independent
core_release source review supports the boundary after moving the local coverage
summary invariant outside the recoverable catch. Select exactly one run of
`search-validation-controls-01-selection.json`, SHA-256
`532600e0e9c6e288c4df10682a133d5a9003d368bcef5d4556ea8888a1a962b6`.
The existing runner snapshots 83 selected sources and checks 19 runtime/data
pins. Limits: 30 CPU seconds, 90 wall seconds, 256 MiB, two processes.
Only eight new controls run; one two-connection IPv4 loopback case, no external
endpoint, native checker, prover or compiler. Used source/test/selection bytes
freeze; preserve any failure without relabeling or automatic retry.

Search01 terminated before any tests: the selected source map omitted the
existing inert fixture `transport/test_search_resilience.py`. This is root's
selection error, not a test or product pass. Retain its raw failure (0.703125
Job CPU seconds plus 0.34375 outer-wrapper CPU; clean closure). Root selects
fresh02 with only that pinned fixture added; product and test bytes stay exact.
The known imported fixture is read, not its old test suite executed. Root also
read the new runtime test source and selects its separate first run with the
same 30 CPU/90 wall/256 MiB envelope, adding the required authoring worker source
as inert pinned data. Both operations use existing supervision, no native proof.

Search02 also stopped before tests: the borrowed fixture's own
`discovery/test_candidate_query.py` import was missing. Retain that terminal
failure (0.796875 Job CPU + 0.375 wrapper CPU, clean closure). Rather than another
guessed closure, root compared the entire selected map against the old passing
search fixture plan: exactly this one predecessor source was absent. Select
fresh03 as their conflict-checked exact union (85 sources). The actual new
product/test files remain unchanged; no prior tests have run or passed here.

## Adopted small controls; next real-owner boundary

Root read/adopts SEARCH-REVIEW and RUNTIME-REVIEW actual outcomes: search03
passed eight controls and runtime01 passed eleven, with exact source/runtime
bindings and clean closure. Their stated inert-owner limits remain. No repeated
campaign follows.

Select source-only `software/v5/client/runtime_check.py` under core_search:
an ordinary trusted-owner example for the existing boot/launcher, taking explicit
runtime/config/grant and pinned receipt/bundle/foundation inputs. It uses the
new RuntimeProfile, actual atomic Workspace and exact original issuers to
admit one retained I receipt, describe its warranted module, and prepare the
selected semantic import; then it closes all owned state. No fixed theorem ID,
fixture phase, provider or receipt is built into the code. No authoring,
proof generation, native delta, or socket work is needed. This validates new
factory-to-real-owner integration, not another reciprocal campaign.

Root owns exact plan/launch selection; core_release independently reviews this
small integration before any execution. Reuse the previous actual source
closure rather than the synthetic test closure. A later run must retain all
failure costs and bind real receipt verification output; existing certificates
are inputs, never a saved acceptance report loaded as authority.

Success in these seams is not final v5 completion. Genuine recurring
certification, full reciprocal operation, justified full-cost growth and public
deployment/security obligations remain open. They are not waived to avoid an
expensive experiment.

Root read/adopts ORDINARY-REVIEW and selects exactly one invocation of
`client-runtime-check-01-plan.json`, SHA-256
`8eea1d8ff69ee381517643db3fdbcec41149ffceaaf66326d88fd11bd25dc8b6`.
It has 88 exact sources, the retained six asset pins, and the reviewed
60 CPU second / 180 wall second / 256 MiB / four-process outer ceiling.
The original finite receipt subcall is 5 CPU seconds / 30 wall seconds /
128 MiB. This is fresh verification and semantic import, not proof generation.
Use the retained installed Python and unchanged launch.py; freeze selected
source/plan bytes on invocation and preserve any terminal failure.

The one selected real integration terminated successfully: 4.75 enclosing Job
CPU seconds plus 0.390625 wrapper CPU, 15.64936 wall seconds, and 106,299,392-byte
peak Job private commit. Its actual saved-outcome review is pending. No rerun.

## Next selected source: ordinary retained-workspace service

Root read/adopts NEXT-CORE's concrete operability argument. Select
`software/v5/client/serve_workspace.py` plus `SERVING.md` under core_search,
and focused `test_serve_workspace.py` under core_growth. Root owns integration,
actual finite selections and Git; core_release reviews the new source boundary.
Use existing launcher/boot and typed CompositeProvider implementations unchanged.
Expose an existing, explicitly selected persistent workspace read-only through
the existing bounded HTTP service, with finite lifetime and guaranteed attempted
cleanup. No mathematical owners or proof generation are constructed.

Support the existing explicit atomic/mixed/evidence/staged/validated modes;
select the corresponding exact workspace/store/provider types without fallback.
Validate canonical, disjoint input/output paths and configuration before service
startup. Never create a missing workspace or modify an old frozen evidence
workspace for a test: a prospective genuine-data test uses a fresh structural
copy/import under a separate selection. The service exclusively owns its opened
workspace; concurrent separate publishing is not claimed.

Bind/TLS policy, request/reply/concurrency ceilings and transport stay unchanged.
Optional location composition may reuse existing ServiceLocationProcess with
explicit original-deadline limits and bounded caller-supplied routes; do not
build a new route planner or enumerate the corpus. If this optional wiring
expands the entry materially, defer it and expose the usable HTTP entry first.
On partial startup or shutdown errors, attempt every component cleanup, preserve
the primary failure, and never report clean success from uncertain cleanup.
The returned endpoint/counters are operational data, not mathematical authority.

Changed-boundary tests cover exact existing-workspace selection, mode/profile
refusals, finite lifetime, clean shutdown/reopen and partial startup cleanup.
Reuse pure stores/loopback and existing location doubles; no cryptographic,
Lean, native, compiler, cloud or public network run is selected by this entry.
Do not rerun old protocol suites. Keep this a small usable product entry, not
another experimental orchestration framework.
