# Installed producer: independent public-launch design review

2026-10-22; reviewer `storage_outcome_audit`. Canonical root only.

Disposition: **the settled contract is implementable in principle and suitable
for the selected fresh source implementation**. This is design approval, not
source approval, runtime qualification, mathematical acceptance or v5 completion.
No product import, constructor, test, proof or packaging operation was performed
by this review. No used source or live U proof evidence was changed or inspected.

## Exact reviewed checkpoints

| Document | SHA-256 |
|---|---|
| `RELEASE-PRODUCER-PUBLIC-LAUNCH.md` | `c0964e4d3b0d078e6a115929cb8eb7fd4481bb12244499eb15711bf5249c4b57` |
| `INSTALLED-PRODUCER-SELECTION.md` | `dbaca172035ada81ae82edcd5d57b2424eb758b9692e9e68299d27ba0d4f8f16` |
| Independent `RELEASE-PRODUCER-SOURCE-COMPATIBILITY.md` | `8e1f418d186682383931cd85c9472ccd3d6bd23b25fb12d25dfd3770f5c31078` |

I read the full design and formal selection, and examined the actual current
distribution launch/materialization/preparation-map paths, client launcher,
generic lifecycle snapshot execution/adoption, retained outer validator, entry
action handling and stage request/lineage checks. The formal selection's exact
thirteen-field grammar governs older exploratory paragraphs in the design.

## Why this is a central, bounded change

The reviewed component solves release-owned artifact adoption, but ordinary
installed operation still has two incompatible identities: the general client
runs copied core sources, whereas resumable production binds stable installed
core origins and profile bytes. It also emits a different actual outer evidence
grammar. A dedicated fixed-action finite launcher resolves those mismatches
without changing the general client loader or receipt mathematics.

This is not a second proof system, scheduler or runtime installation. It reuses
the existing supervisor, native artifacts and generic snapshot/production
semantics. New records describe genuine public executions, not converted
research PASS records. The current receiver remains selected unchanged.

## Findings raised and settled before implementation

### Shared verifier and complete import closure

The first producer union would have overwritten current verifier `ec6474cd`
with historical `9f77bd17`. The source compatibility review establishes the
API/trust/refusal regression and the complete three-module forward-import
closure. The selected design preserves all current130 rows and includes those
three helpers before product import. This finding is resolved in the contract.

### Both generic snapshot validation sites

A new outer launcher alone is insufficient. Existing `snapshot.execute` and
`snapshot.adopt` both call module-global `_selection`, and adoption additionally
calls the old local-check `_local_outer`. The selected fresh source adds a
protected lifecycle selection method, changes both calls to use it, preserves
the old validator as the default, and has the installed subclass choose the
new exact public grammar and outer validator. The entry also checks that same
grammar. No permissive callback, monkey-patch or failed-validation fallback is
allowed. This is the minimum explicit seam; no snapshot algorithm copy is needed.

### Enclosing failure must override inner success

The earlier design lacked an enforceable link from prior inner stage reports
to their enclosing public launch. A stage can save a passing result before its
worker or outer finalization later fails. Existing inner lineage checks alone
do not establish that later closure.

The formal selection now adds `prior_launches`, at most16 exact outer pins in
one-to-one order with the input's `prior_attempts`. Each must bind the actual
action=run selection, profile/allowance, worker report and exact matching inner
production result, with all specified overrides absent. Validation is shallow;
it does not recursively expand each predecessor's predecessor list. The existing
inner scheduler still validates the complete prefix ledger. Unknown or failed
outer closure does not qualify a continuation.

### Request bytes are not completed request production

A generated request file can survive failed enclosing finalization. The selected
thirteenth field, `input_launch`, is therefore mandatory for public run/preflight
and must name a completed action=request outer whose worker report names the
exact selected request pin. It is null for snapshot/request. There is no implicit
path inference or manual-owner bypass inside this public lane. The existing
low-level API remains distinct. This closes the second missing outer link.

### Layout and bounded output union

Initially proposed nested stage output conflicted with the existing request/
preflight requirement that a future stage output's parent already exist while
the future enclosing run directory must be fresh. The selected action output is
instead a fresh disjoint sibling; the generated request remains `RUN/request.json`.
The public census must cover the run and the selected actual action output,
without double counting or omitting either. Request/preflight leave their future
stage output absent. Fixed named failure markers cover the outer run, worker,
actual snapshot/attempt and cited predecessor records, not only an immediate
parent directory or an unrelated-history scan.

## Operable contract obligations

### Initialization and immutable identity

The V4 distribution exposes exact descriptor/template roles and three producer
artifacts, preserving the six consumer roles. The relative template has no
back-reference to the manifest that pins it. The owner supplies the release
digest; materialization inserts that manifest/descriptor identity and absolute
installed paths, producing a fresh external profile without constructing a
producer or dispatching a host.

The new public profile schema/domain prevents accidental old-lineage adoption.
Core origins remain `ROOT/sdk/v5`; only the pinned entry is copied per operation.
The profile does not contain its own document path or transient run paths, so
different external destinations can hold identical profile bytes. Existing
snapshot evidence nevertheless retains its exact original profile-document
pin. Relocation deliberately gives a new operational identity; it is not an
allowance migration.

### Fixed command and truthful evidence

The thirteen selection fields are
`schema,name,action,release,profile,input,entry,run_directory,runtime_pins,limits,output_limits,prior_launches,input_launch`.
The helper derives one fixed command using the actual saved selection digest;
the selection never contains an argv with its own unknown hash. All four actions
bind selection path and digest. No caller chooses an executable, plugin or
arbitrary command.

Successful outer adoption requires exact command/cwd/limits, terminal Job closure,
the action-specific worker report and exact output pins, unchanged inputs/code,
bounded output census, original clocks and absent overriding markers. The parent
writes a final failure override if finalization fails after saving its result.
Only run dispatches proof stages. Snapshot remains an execution-capsule operation,
request remains data construction and preflight remains inspection. No operational
result grants mathematical acceptance or funds an implicit next attempt.

### Stable source loading and host assumptions

The worker must validate the complete selected product closure before importing,
compile exact held source bytes at the installed origins, reject preloaded or
unselected product modules, and check actual origins and bindings afterward.
Reading a file before and after an ordinary loader runs is not equivalent to
executing the checked bytes. The shared contract is stdlib-only at import so
the parent need not import product code or construct the producer outside its Job.

The complete Python-runtime census/origin rule must be explicit in source; the
16 selected non-source runtime pins are only a repeated-rebind subset, not a
hermetic dependency proof. Python startup, owner-controlled installation, local
filesystem and OS/DLL assumptions remain explicit. No security-sandbox claim
follows from Job limits or held-byte loading.

### Counts and resource accounting

The agreed source projection is internally consistent:

| Quantity | Selected projection | Relevant limit |
|---|---:|---:|
| Unique SDK names | 144 = 130 +12 +2 | Explicit fresh distribution cap144 at build and validation |
| Preparation Python source rows | 123 = 109 +12 +2 | 128 unchanged |
| Producer core modules | 31 = 27 +3 +1 shared contract | Exact selected set |
| Pre-import core/helper/entry roles | 33 = 31 +2 | Exact selected set |
| Support runtime rows | 49 = 31 +2 +16 | 128 unchanged |
| Repeated-rebind installation pins | 60 = 56 +3 +1 | 64 unchanged |
| Outer runtime digest map | Actual count to derive | 256 unchanged |

The parent-only launcher is release-pinned and rebound separately, not hidden
inside the core31 count. Prior outer/selection/worker metadata adds bounded
transient reads and must be explicitly bounded in the helper. Actual assembly
must verify every projected count and byte sum. Do not drop a required source
to meet a limit; do not inflate the historical256 limit to import old build logs.

The outer Job CPU already includes producer and native descendants. Whole-call
known CPU is that inclusive measurement plus disjoint parent process CPU, not
plus the inner native CPU a second time. Original public wall clocks survive
the distribution-to-launcher transition and final report I/O. Startup exclusions
and uncertain closure are recorded honestly. Outer per-call costs are additional
operational records; the existing inner allowance's immutable carried-cost field
is not silently rewritten on every continuation.

## Source review and smallest subsequent checks

The next independent review is `INSTALLED-PRODUCER-SOURCE-REVIEW.md`. It must
verify these contracts in the actual fresh source, especially shallow explicit
provenance, full named marker precedence, preserved receiver bytes and both
protected snapshot call sites. A design pass does not authorize execution.

After source review, root may select narrow changed-boundary controls for exact
materialization, origin/import closure, public schema/command/provenance refusal,
output relationships and finalization. A later installed snapshot/request can
test the actual public path when suitable mathematical input exists. No host
rebuild, second heavy proof, repeated broad campaign or live allowance migration
is needed to test this adapter's design.
