# Independent challenge: inspect a candidate before acquiring its proof

2026-10-24. Reviewer: `module_anchor_audit`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Decision

Expose the already implemented, bounded ordinary preview operation through the
public peer API and CLI. This is a small operability improvement with a precise
conditional avoided-cost argument. It does **not** justify a new search profile,
normalization engine, certification campaign, importer, or mathematical trust
mode. Root's `ORDINARY-PREVIEW-SELECTION.md` owns implementation and any subsequent
finite execution; this checkpoint does not commission runtime.

The concrete workflow is: find candidates, inspect a selected formal type, then
decide locally whether to receive and check its evidence. The current public
`find` returns records and locators; `receive` immediately follows its internal
preview with evidence/dependency acquisition and independent admission. The
lower-level `OrdinaryAcquisition.preview` already supports inspection without
an owner, database, custody store, native call or proof-ancestry traversal.

## Existing capabilities, not a new retrieval algorithm

The installed resilient `peer_api.find` is not restricted to exact-type queries.
Its `compile_query` accepts one to eight exact feature conjuncts: declaration
kind, type symbol, result head, binder-domain head and declared-type key, among
the existing supported tags. Only the current public `query.py` preparation
front end emits the exact-type-key query exclusively. A broader wrapper could
expose existing capabilities, but that alone would not establish semantic
applicability, useful selectivity or complete recall.

Conjoining every symbol in a goal is not substitution-complete. A theorem of
type `forall P : Prop, P -> P` may apply after instantiating `P` to a proposition
containing `Eq` and `Nat`, although its stored type need not mention either
constant. Its eventual result head can be a bound variable rather than `Eq`.
Explicit symbol/head anchors can define a useful syntactic candidate family;
they cannot claim to contain every applicable theorem. An agent may choose such
a family without making it a mathematical acceptance rule.

The saved definition-body discriminator already provides a reason not to make a
more elaborate index the next default. It examined three postings instead of
eight, but used 202,790 search-response bytes instead of 103,356; with its
acquisitions the staged path used 215,544 bytes and ten calls. That is useful
optional vocabulary discovery, not a demonstrated full-cost saving. The older
instantiation prototype also uses a distinct codec/profile; its capabilities
must not silently be attributed to the current ordinary package.

## Trust contract for a public preview

The operation must accept one explicit selection containing provider label,
snapshot ID and complete ordinary export record, plus already selected contacts
and a finite allowance. It should return the complete parsed canonical preview,
the original selection, exact byte count and SHA-256, and explicit assurance
facets. A parsed document is JSON-safe; Python raw `bytes` must not leak into a
JSON report. No generated source or executable artifact is needed.

The existing lower-level operation establishes the following relation:

1. The selected record has the expected ordinary schema and namespace.
2. The fetch requests exactly its advertised preview hash and size.
3. The returned raw bytes have exactly that size and hash.
4. The ordinary adapter derives its complete record, including features,
   locator and export identity, from the preview, and requires equality to the
   selected record.

Thus a successful return is **exact preview/record binding**. It is not any of:

- A proof that the advertised type is inhabited or that the declaration exists
  in a valid mathematical environment.
- A proof that this preview agrees with the full evidence. That separate check
  remains `portable_preview.resolve(preview_raw, evidence_raw)` in acquisition.
- Reverification of the record's membership in the named index snapshot. The
  snapshot identifier is a retained selection label in this operation.
- Evidence that the chosen provider covers the entire network, or that a local
  rejection shows the mathematics is false or irrelevant to every future user.

A dishonest provider can consistently advertise false mathematics in its preview
and record. Returning `mathematical_acceptance: false`, no evidence-binding
claim, and no membership-verification claim is essential, not a caveat to hide
in prose. Later unchanged independent admission supplies mathematical warrant.

The preview contains the complete encoded declaration type and exact bindings
for symbols appearing in it. **It does not contain all referenced definition
bodies or their computed meanings.** A caller may still need separate body
inspection to understand an unfamiliar predicate. This command makes existing
type information accessible; it is not a complete semantic explanation or an
applicability decision procedure.

## Resource and state contract

- Exactly one explicit preview attempt; no candidate loop, retry, ancestry,
  dependency locator, evidence request, implicit cache or admission.
- `requests` must equal one. `reply_bytes` is positive and at most the existing
  1 MiB preview ceiling. Reject an advertised preview larger than this grant
  before I/O. The real preview reader still enforces its syntax/DAG/name limits.
- Use the existing `OrdinaryBudget`, including its original parent deadline.
  A composed caller may supply a shared ledger. Narrow that deadline only;
  never refund previous work or replace the ledger after failure.
- A begun HTTP/parse/hash/record-validation failure consumes the one request
  and the full selected reply cap through the existing acquisition settlement.
  Validation refusal before an attempt need not charge a nonexistent fetch.
- Close a network ledger only if this call created it. Preserve the final
  network and HTTP accounting on both success and failure. Existing transport
  cleanup has a separately budgeted best-effort allowance of at most one second.
- Reuse exact contact/TLS validation and before/after pin checks. Peer metadata
  cannot introduce new endpoints, local paths or trust stores.
- Construct acquisition with `local_custody=None`; do not call `_state`, open an
  owner/catalog/custody database, or allocate a native admission operation.
- The CLI must extend every existing `find`-only state-free branch to cover
  `preview`, including configuration fields and output/custody handling, not
  just its final dispatch. Existing other operations stay byte-for-byte or
  source-equivalent unchanged under the selected two-payload successor.

For a rejected candidate, proof acquisition/checking/storage cost is absent.
The preview work depends on the bounded selected type representation and existing
package/contact validation, with no mandatory term proportional to its proof
ancestry or the global corpus. This is not constant-time mathematics: selected
type complexity, parsing, endpoint latency, startup and transport overhead still
cost resources. Cooperative checks remain distinct from hard process isolation.

Separate CLI invocations are separate explicit grants. The new command does not
make an entire multi-command search/inspection/reception session automatically
share one budget. SDK composition can reuse the existing ledger when selected.

## Conditional complete-workflow benefit

Fix candidates `1..n`, a selected subset `S`, the same initial local knowledge,
representation, verifier and cache state, and a stated resource measure. Let
`p_i` be candidate `i`'s preview acquisition/validation cost and `h_i` its
remaining evidence/closure acquisition, checking and retention cost under that
state. For the simple case in which shared cache interactions are absent or
already attributed consistently:

\[
C_{\rm eager}=\sum_i(p_i+h_i),\qquad
C_{\rm inspect}=\sum_i p_i+\sum_{i\in S}(p_i+h_i)+W.
\]

The selected current `receive` refetches its preview; it does not consume the
earlier preview as a validated cache. `W` includes additional command startup,
inspection/decision effort, output and integration overhead. Therefore:

\[
C_{\rm inspect}<C_{\rm eager}
\quad\Longleftrightarrow\quad
\sum_{i\notin S}h_i>\sum_{i\in S}p_i+W.
\]

This is a nonempty benefit region, not an unconditional speedup. If every
candidate is received, repeated previews add cost. If a shared closure becomes
warm under eager reception, use route-specific marginal costs instead of the
displayed additive simplification. Provider service, cold-cache effects, bytes,
CPU and storage should be reported separately or combined with explicit weights.
Wrong rejection may lose useful mathematics and is not covered by a pure cost
inequality.

Against an equally optimized direct SDK workflow, previewing already exists.
This change supplies a usable public route, not a new algorithmic advantage.
Neither query recall nor the meaning of useful growth changes. It removes an
unnecessary forced acquisition in the CLI path while preserving the user's
choice of what to investigate.

## Residual central issue and review scope

Common-library interoperability is still a larger practical constraint. A local
query cannot invent portable bindings for ordinary constants absent from the
admitted basis. The tiny successful approved-project intake does not solve a
large cold Mathlib/Std closure or justify repeating the saved large refusal.
This bounded preview seam should not become another reason to defer that issue
indefinitely, nor should generic importer work be selected without a concrete
workload and favorable whole-cost case.

Source review below will cover only the new API/CLI boundary. Existing metadata
and acquisition mechanisms are reused; no owner/database opening, native run,
network operation, duplicate test or Git mutation was performed for this review.

## Source identities consulted

All paths below are relative to the canonical root; SHA-256 identifies the exact
consulted unchanged source, not a mathematical correctness certificate.

| Source | SHA-256 |
|---|---|
| `software/v5/transport/ordinary_acquisition.py` | `e69bd0f33829e4709fdc1a7c3afe4150704dfeabfe30243195b379945081e826` |
| `software/v5/ordinary_resilient_package/peer_api.py` | `656e7c3ccfff7613bf04fdec9d1a3656a49a803ad2f5662916db9e86bbe4b95d` |
| `software/v5/ordinary_formal_query/discovery/ordinary_export_adapter.py` | `3ddbed2156a393b08543a5da88c89b5c5b9c2b4f65689c46fbd7623cec38db0a` |
| `software/v5/ordinary_peer_package/peer.py` | `c1e88338408f59a26d70d27d9c9968b7b6192f6d0ac6b99121ad19e5f78e1930` |

Prior actual body-discovery evidence is recorded in
`ORDINARY-BODY-DISCOVERY-OUTCOME.md`; it was not replayed.

## Selected API and facade source review

**PASS for the selected additive source boundary**, not execution or package
qualification. The reviewed API SHA-256 is
`8b96e3bf7b7d5e3401b682f8eebc62a1d63421b9c4108dd94567db5f4d09c84f`;
the reviewed CLI SHA-256 is
`bf90809c35eb0a2cbc827d678bded411d8187dcfe2ba52223d443e2ce439e26d`.
Both are under `software/v5/ordinary_preview_package/`.

The API diff is solely the appended `preview` function. All old operations and
shared helpers remain unchanged. The new exact config shape is
`contacts/selection/limits`; the selected triple is validated and detached.
The preview size is checked against the one-request grant before any fetch.
The real adapter and acquisition helper are used with `local_custody=None`,
inside the original network deadline. There is exactly one awaited fetch and
no owner, database, native, evidence or locator operation. The full parsed
preview is returned with exact raw hash/length; raw Python bytes are not returned
in the new public report. The report preserves all three false authority facets.

The existing `_network` helper either creates a new ledger or narrows a supplied
ledger's deadline. The function closes only a ledger it created. The inherited
fetch settlement runs even on cancellation or malformed replies; the API catches
the failure and returns it through `PeerFailure` with final network/acquisition
accounting. A later output/allowance failure does not renew or erase charges.
The final type parse is bounded by the unchanged preview profile and followed by
live allowance/pin checks.

The CLI diff adds one operation and shares `state_free` with `find` at all four
relevant gates: state-argument validation, state-path resolution, adoption marker
and custody-limit reads, and actual owner/custody opening. Consequently preview
does not open a store and then call itself read-only. It does import the unchanged
pinned owner helper for package bootstrap/allowance, which is distinct from
opening an owner. Dispatch explicitly selects both preview and serve; an unknown
operation cannot fall through to service startup. Existing report, fresh-output,
config/profile/runtime and allowance handling remain unchanged.

The reviewed README initially has SHA-256
`f5f182e8e2067028d62dca77079c2f378e0f87db417270d0f2c86717ece63241`.
Its contract agrees with the sources, including no symbol bodies, no evidence or
membership warrant, later duplicate preview cost and cooperative memory limits.
One editorial correction was requested: replace "three prior find-only state
boundaries" with "all prior find-only state boundaries". That wording does not
affect the reviewed runtime code. Root owns focused controls and the subsequent
exact two-payload assembly; no installed behavior is inferred from this review.

## Focused controls and selector review

**Source-cleared; not executed by this reviewer.** Root's new
`ordinary_preview_package/controls.py` has SHA-256
`5a9ec390a99b1e6688964f508ff8cb93c069d581d293e84dffec990bcf9262d7`;
`select_controls.py` has SHA-256
`4af2e8cf39da0c34934b19baf0a56f417863018a27af1a00043053c29f630fe9`.

The controls load the selected current package once without owner state, then
load the new API and facade from the immutable selected-source snapshot. The
actual ordinary preview parser, record extractor/resolver, budget, acquisition
helper and type-document encoding are used. Only HTTP exchange is doubled in
the API cases. That double checks the exact route and complete request
schema/hash/size, returns selected fixture bytes or explicitly named corrupt
responses, and does not hide real network behavior behind a pass label.

The fourteen API cases cover exact success; tampered hash, HTTP failure and
cancellation; a different well-shaped snapshot label with no membership claim;
matching-digest malformed preview syntax; complete record feature mismatch;
oversize/extra-request/absent-provider/bad-snapshot zero-fetch refusals; and
shared prepaid accounting, last-request use and exhausted-budget refusal without
renewal. Generic failure cases promise refusal only; only feature mismatch and
exhaustion pin exact error codes. They do not prove every possible failure code
or malformed input is handled, nor actual HTTP/TLS correctness.

One explicit facade-bootstrap double then exercises dispatch through the real
new CLI, followed by refusal of each of its four forbidden state arguments.
The existing package was already genuinely loaded before this double. The test
forbids database connection, subprocess creation, owner/custody opening, evidence
and locator methods. No claim of actual packaged bootstrap, independent-host
operation, native checking or mathematical acceptance follows. A successful
run would contain nineteen named cases, not nineteen native/network experiments.

The selector uses only immutable package/runtime pins from the exact prior
project-intake selection, plus the saved real preview. It excludes owner state
and old harness inputs, snapshots the three new source files, itself and the
existing runner, and requires fresh selection/output destinations. Its finite
envelope is 60 wall seconds, 35 CPU seconds, 768 MiB and two processes; the
control's internal bound is 45 wall seconds and 25 controller CPU seconds.
No compiler or live service is launched by the selector. The earlier template,
current profile, helper and fixture hashes were independently read and match:

- Selection: `2f298613971e2ffbb33c818061195a5ac4d7fd7359d38a9ed3b7c0497b857dfe`.
- Profile: `aab7e2460c0879d0fbb2b570470984efe2a66c4a932f5725ce563a1df7c2530f`.
- Builder helper: `49b922ddcd93c63f5c21e96f9daa4a7930d967f361c79c789744beb2810989f5`.
- Preview: `362292c8237bd4cf0f9127ed5575723f188b51efa7ab0a784ac0bf1c1489193c`.

Root retains launch selection and saved-outcome adoption. No prior passing
campaign was repeated for this source clearance.

## Saved focused-controls outcome

**PASS for the selected real-validation/inert-transport boundary.** Saved run:
`experiments/v5-local-checks/ordinary-preview-controls-01`. This independent audit
read saved JSON, source snapshots and file hashes only; it did not replay tests,
load product modules, open owner/database state or invoke native/network code.

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `d004f858e9042f5a3d44fec01edf1a370e69bae2262e959e4c8bedf2305fc3a7` |
| Outer `RESULT.json` | `0f124f69e1e626df7745bbd9786119fe2f92f179d823e3150ef4984b9f6c59c4` |
| `controls/RESULT.json` | `b1e248d9d88f52e014436373affe610df2724a8325c7f0cc752312fb7081ec6b` |
| `controls/facade/RESULT.json` | `a01e4eb6adf465d1eb94f031e63047ab375e385a28e539a77a0ace7fec75132b` |
| `command/stdout.txt` | `ec736ed94bdd9fb06fd34b9b3c1a7417d97908c2dbf37df465729d573fe27703` |

All 152 runtime pins and five selected source snapshots independently match.
The outer result binds the actual selection; the actual command names the exact
saved package, fixture and fresh output. All nineteen named cases are present.
There are ten inert exchange calls and zero forbidden-side-effect calls.

All four API successes contain the complete parsed 1,351-byte fixture preview,
independently compared to the saved fixture, with matching advertised/returned
hash and all three authority facets false. The alternate valid snapshot label
survives unchanged and still has membership verification false. The successful
facade result similarly has null catalog/custody/store fields, a single charged
preview, false mathematical acceptance and no worker CPU.

The begun tamper, HTTP, cancellation, matching-hash malformed syntax and feature
mismatch cases each charge 1,351 bytes, leave zero pending requests and close
their owned ledger. Actual diagnostics include `ORDINARY_PREVIEW_EXACT_BYTES`,
`ORDINARY_ACQUISITION_HTTP_STATUS`, `JSON_LEXICAL_TOKEN` and
`ORDINARY_PREVIEW_RECORD_BINDING`; cancellation is conservatively reported as
`PEER_OPERATION_FAILED`. The four early validation cases make zero exchange
calls. All four forbidden facade state arguments fail with
`PEER_OPERATION_STATE_ARGUMENTS`, before output creation or exchange.

The shared ledger retains its prepaid search and advances from two requests /
2,702 charged bytes to three requests / 4,053 charged bytes. The next call fails
with `ORDINARY_AGGREGATE_BUDGET`, leaves those counts unchanged and makes zero
new exchange calls. All three shared-operation reports leave the ledger open,
with no pending reservation. The selected test's own final closure is separate.

The command exits zero, direct child is reaped, Job closes with zero active or
terminated processes and no cleanup error. Outer wall time is
**1.5381855997256935 seconds**. Known inclusive CPU is **1.359375 seconds**:
0.828125 Job CPU plus 0.53125 outer wrapper CPU; separately reported inner
supervision CPU is zero. Peak Job private commit is 29,143,040 bytes. Stderr is
empty. These costs are for the complete finite control run, not ordinary remote
preview latency or an amortized user benefit measurement.

This pass does not qualify actual HTTP/TLS, the forthcoming assembled package's
bootstrap, search recall, applicability, useful growth, native mathematics or
worldwide deployment. The selected current package and all used evidence remain
unchanged. Any new integration boundary belongs to a separate root selection.

## File-only assembly and clean-recipe source review

**Source-cleared; no assembly/build executed by this reviewer.** The selected
new files are under `software/v5/ordinary_preview_package/`:

| File | SHA-256 |
|---|---|
| `assemble.py` | `7be8f6ea6f84d4789b8492d20d2c7eb0b799503ac80b9f629229068ec88c45d7` |
| `select_assembly.py` | `fcce660bab3c2f9e4bad73251f1a8123b4a9cbc2542aea2bc1cd3c0d3936e16a` |
| `build.py` | `c0cf85148668f2382a1dd66356b01c1f5c9d60f1e6ae3a7e91b05c01cd31a99d` |
| `source-map.json` | `f567b842b7e74a3167dcb7dd999fa7d3030c7faa062cd9c365a7a373126252fa` |
| Corrected/extended `README.md` | `0bc1a282e70fdf0a75a177ed77692b9bd2b4ed7abcb012b72f291aa6b0addb6d` |

The assembler requires exact current base profile `aab7e246...` and receipt
`3dfa9092...`, retained owner/loader identities and explicit reviewed replacement
hashes. It loads the old pinned package for validation without opening owner
state. The allowed delta is exactly `peer.py` plus `peer_api.py`: two changed,
132 unchanged, zero added runtime payloads, total 134. Installation and all
native artifacts are copied unchanged. No subprocess, native build, catalog,
custody or network operation is requested.

Input paths are checked through the preserved path validators. Output must be
fresh and disjoint from base/runtime roots; selected inputs cannot lie inside
it. Copies use bounded streaming, exclusive creation, hash/length verification
and flush/fsync. All predecessor payloads and descriptors are rechecked, as are
new sources and output payloads. The new profile changes only its auxiliary
file map; installation identity stays exact. The assembly receipt is written
before the profile's final rename. A failure preserves partial files and an
explicit failure record; it never edits an existing package or owner.

The selector imports only locally selected definition-only helpers, collects
the exact base/profile/installation/runtime and source pins, verifies explicit
replacement hashes and emits a fresh selection. The actual assembler runs from
the selected snapshot and checks equality to its pinned canonical source. The
inner allowance is 60 wall/40 CPU seconds; outer selection is 90 wall/50 CPU
seconds, 512 MiB and two active processes. Those bounds authorize only this
finite file operation if root selects it, not a renewed old campaign.

The complete clean recipe was reviewed by exact diff against the frozen
approved-project predecessor. Only its documentation, own source prefix and
source-map hash change. The map changes only the two peer source paths/pins and
their direct-copy destinations. Its 71 selected sources, 54 direct copies,
native lanes, transforms, runtime pins, owner/module support and acceptance
installation are otherwise unchanged. No full compiler rerun is warranted by
these two Python payload changes. Source completeness and file-only assembly
remain separate from actual new packaged entrypoint qualification.

The corrected README now says "all prior" state boundaries and explains the
file-only route without claiming a run. Its example grants are not measured
resource requirements. Earlier frozen controls/source evidence remains intact.

## Saved assembly01 outcome

**PASS for the exact file-only successor**, not public-operation qualification.
Run: `experiments/v5-local-checks/ordinary-preview-assembly-01`.

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `80b0a92e99bd0667d4ba5165d420b045b22daef217742aad4169c2281554212e` |
| Outer `RESULT.json` | `f921c73ef2aaa2fd4fd260690ae845736605b4e4a2b2dfe9e0d103d8b882ddb5` |
| `package/PROFILE.json` | `ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f` |
| `package/ASSEMBLY.json` | `6e09d2b255d8321bd522291276e03f10729cbc4f57536a57b29b63ab67a528bc` |

All 149 runtime pins and six source snapshots independently match. Every one
of the 134 output payloads matches its descriptor hash and byte length. Comparing
actual bytes to the previous package finds exactly `peer.py` and `peer_api.py`
changed, 132 payloads unchanged and no additions. The output has 136 files:
134 payloads plus the two descriptors. The new profile's non-file fields are
unchanged, including the installation-manifest identity. All 54 direct-copy
entries in the 71-source clean recipe match the actual new package bytes.

The actual command uses the reviewed assembler and replacement hashes. It exits
zero, its direct child is reaped, its Job closes with zero active/terminated
processes, and no cleanup error is reported. Outer elapsed time is
**4.249872999731451 seconds**. Known inclusive CPU is **2.3125 seconds**:
1.78125 Job CPU plus 0.53125 outer wrapper CPU, with zero separately reported
inner supervision CPU. Peak Job private commit is 27,787,264 bytes. The receipt
records 38,067,255 copied payload bytes. No native compiler or owner operation
was selected or executed by this file-only assembler.

This saved-data audit did not rerun assembly, import product code or open state.
The preview CLI's actual new-package bootstrap/transport path remains a separate
small integration boundary. No native reciprocal/checking campaign is needed
to reconfirm unchanged mathematics for these two Python-only replacements.

## Packaged public-call source review

**Source-cleared for the two-call boundary only.** New
`ordinary_preview_package/public_check.py` SHA-256 is
`0b5fa2e87694e854ce7e6f7c00b533273496a36fa0ac084305bc21b5feebdf55`;
`select_public_check.py` is
`082212b250a97474ad86c4ee7d78474a45e690bf34fd94a579e8c1451fc14df7`.
No call was executed by this reviewer.

This harness addresses a genuinely new integration boundary: the actual newly
assembled public CLI's bootstrap and preview over ordinary loopback HTTP. It
does not repeat native admission, index search, custody serving or mathematical
reciprocity. It pins the exact new package/receipt, retained 1,351-byte preview,
runtimes and selected support; it holds/rechecks all package files and created
config/result bytes. Its synthetic snapshot label is expressly not discovery
membership evidence.

One bounded static responder accepts at most two loopback connections: first
the exact saved preview, then a same-length hash-corrupt reply. It validates the
exact route, HTTP version, four permitted request headers and canonical request
body. It emits only permitted response headers, omitting the standard library's
default Date/Server headers. Socket reads have a one-second timeout; server loop
deadline, thread stop/join and socket closure are explicit. The responder is
test infrastructure, not a proposed network provider or hostile-source sandbox.

The real public commands omit all owner/custody arguments. Expected exits are
zero and one. Success must reproduce the exact full canonical fixture and its
selection; refusal must specifically report `ORDINARY_PREVIEW_EXACT_BYTES`.
Both must retain false authority facets, exactly one 1,351-byte charged attempt,
zero pending reservation and closed owned ledger. Output directories may contain
only the public `RESULT.json`; the responder must report exactly the two intended
requests and close cleanly.

The harness reuses the native installation's already-loaded supervisor and Job
modules after exact role-path checks, avoiding a second domains-module import.
It grants at most 40 wall/12 CPU seconds per child and at least enough to satisfy
the CLI's 35-second minimum; each process is separately supervised with two active
processes. Its original inner total is 75 wall/32 CPU seconds and 512 MiB;
the selected outer bound is 90 wall/40 CPU seconds, 768 MiB and four active
processes. Actual child CPU replaces its reserved grant only when known; unknown
CPU retains the full charge and fails instead of renewing work. Cleanup requires
zero remaining/terminated processes, not an unjustified cumulative-process-count
equality. An outer Job remains responsible for whole-tree containment.

The selector writes fresh selection/output identities and pins immutable
package/runtime/fixture/support sources only. It opens no catalog, database,
socket, compiler or child. Root's actual finite selection and saved-result audit
remain required. A passing loopback result would still not qualify remote TLS,
independent hosting, search completeness, relevance or useful-growth advantage.

## Saved public01 outcome

**PASS for the selected packaged preview and exact tamper-refusal boundary.**
Run: `experiments/v5-local-checks/ordinary-preview-public-01`.

| Saved artifact | SHA-256 |
|---|---|
| `selection.json` | `613e28c8da5fde5d5e570e46d52bfe94cb56b6fa2b0c6037f26592095796c5c7` |
| Outer `RESULT.json` | `6fb5cb5b1de2ccbb777cad0818de09947a79b5f69d108f5b88f306e67491b6f6` |
| `public/PUBLIC-CHECK-RESULT.json` | `14d230d969251053d5adb280982748d3f22338c318412361cc2330f064220d83` |
| `public/IMMUTABLE-FILES.json` | `868a0282fa53ce29fa92aa81dca0b0571e071ea03bfa91acf6ad4ddc7ba32835` |
| `public/SERVER.json` | `1bd2f5c3b57aba3249ec4f5617860f19af6bedce74e9f672d2a795ea5911aa00` |

All 148 runtime pins, four source snapshots, 148 pre-call held inputs and 152
final held files independently match. Every pre-call entry remains in the final
map unchanged. The actual command selects package profile `ab04e724...` and
receipt `6e09d2b2...`. Both public stdout documents equal their saved CLI result
files and the harness's retained per-call results.

The exact call exits zero and returns the complete parsed fixture, independently
compared to the saved preview, with matching 1,351-byte size/hash and unchanged
selection. The public result has null owner/catalog/custody selection. The
tampered call exits one with `ORDINARY_PREVIEW_EXACT_BYTES`, no returned preview
and no mathematical acceptance. Both keep mathematical acceptance, evidence
binding and snapshot-membership verification false; each charges one request
and 1,351 reply bytes, closes its owned ledger and leaves no pending reservation.

The static responder records exactly two connections and the intended exact/
tampered replies, each 1,351 bytes. Both requests have the same expected preview
hash/size/schema and 148-byte request body. Each CLI observes one completed HTTP
response, 1,351 reply bytes and 225 total header bytes; failed-attempt counts are
zero/one respectively. The responder reports no errors, its socket is closed
and its thread is not alive. No evidence, locator, index or native operation is
part of this two-call sequence.

Both supervised children are reaped, their Jobs close with zero active or
terminated processes, and stderr/cleanup errors are empty. Their known CPU is
0.75 and 0.765625 seconds. The entire selected run takes
**4.068215699866414 wall seconds** and **3.6875 known inclusive CPU seconds**:
3.1875 outer Job CPU plus 0.5 outer wrapper CPU. The child figures are already
included and must not be added again. Peak outer Job private commit is
58,105,856 bytes. The outer cumulative process count is six, not six simultaneous
processes; the selected active-process bound is four. No native worker CPU is
reported by either public command.

The independent audit is saved-data/hash inspection only. This closes the
selected Python-interface/package/loopback integration seam without rerunning
proof or native campaigns. It does not turn a static metadata responder into
an independently hosted index/custodian, establish mathematical truth from a
preview, prove broad usefulness or finish deployable v5. Further work should
return to higher-payoff common-library and complete-workflow questions, not
polish this now-passing preview mechanism indefinitely.
