# Second efficiency seam: local common-subexpression reuse, not trusted caching

2026-09-27. Read-only proposal by `v3_efficiency` after root's follow-up.
No implementation or execution. Keep immediate source14 review first.

## Recommended smallest follow-up

Within `source_codec.reexport_actual`, compute each rebuilt root closure once:

```text
# Current
require(rebuilt.closure(root) == store.closure(root), ...)
for key in rebuilt.closure(root):
    require(rebuilt.objects[key] == store.objects[key], ...)

# Candidate
rebuilt_keys = rebuilt.closure(root)
require(rebuilt_keys == store.closure(root), ...)
for key in rebuilt_keys:
    require(rebuilt.objects[key] == store.objects[key], ...)
```

The original first and second `rebuilt.closure(root)` calls have the same exact
local Store and root and no intervening mutation: the intervening call only
reads the separate original store. Neither closure mutates a Store. The returned
set is local and not exposed. Retaining that already computed set until its
immediate loop therefore avoids one complete dependency/mutation-check traversal
per root without trusting a stale Store, content-ID-only cache, or peer assertion.
All original-object commitment checks remain; all rebuilt-object commitment
checks still run once before object equality checks. No supplied receipt can
authorize this shortcut and no result survives the local function call.

This addresses a broader pipeline position than raw byte insertion: every
`verify_native` calls `reexport_actual` (admission, bootstrap, publication, both
candidate/inverse checks during submission), and internal inverse reconstruction
also calls it. An admission with six replay roots previously recomputes six
rebuilt closures merely to obtain keys for the immediately following loops.

## Second very small local simplification

In `Checker.submit`, the initial result
`_old_store, _old_roots, plan = self.context(context)` is discarded except its
plan. After the native stage, `self.union(context['packages'])` constructs the
same prior union again before original-context native re-export validation.

Reuse the initial locally held store/roots there instead. Between those points,
source writing, plan creation, subprocess execution, receipt validation and
source-record binding do not receive or mutate that Store. Child processes have
separate memory. The original second union itself uses the same request-local
`package()` cache, so it was not a second read/authentication of external files.
Its make-plan validation is followed immediately by another make-plan inside
`reexport_actual`, which remains unchanged. Thus retaining the already prepared
input union need not eliminate the later original-object/mutation validation.

Do not generalize this to admission in the first patch. Admission's old-context
union versus new-context union are different inputs, requiring ordering, quotas,
inventory-conflict and mutation analysis. Likewise do not pass arbitrary cached
plans to `reexport_actual`: externally supplied/mutable plans cannot authorize
skipping binding checks.

## Evidence and priority limits

The retained old one-package profile has closure 0.5321 instrumented cumulative
seconds, versus 6.4026 reader seconds. This establishes a real traversal path,
not a current six-root estimate; source10's encoder changes and current inputs
make extrapolation unsafe. Current source13 evidence quantifies the total outer
gap, but does not attribute the current cost of these exact repeated unions/
closures. **I cannot honestly establish that this second seam is higher-impact
than byte insertion from existing measurements.** It is low-risk and reaches
multiple full-workflow validations, so it merits a small deterministic comparison
if the first candidate's gain is inadequate.

The valuable existing evidence is enough to choose a candidate without a new
baseline-only profiler. Do not promise a meaningful whole-workflow speedup until
the already-required matched integrated measurement supports it. If the gains
are modest, say so; useful proof-reuse gains are a separate evaluation.

## Exact qualification scope

- Primary closure reuse: only `py/source_codec.py` plus lock binding. Existing
  codec/identity/native policy unchanged; no persistent key or cache format.
- Optional union reuse: only `py/checking.py` plus lock binding and its staged
  file pins. This changes a controller critical path and needs focused tests.
- Differential full `reexport_actual` outputs for real single/multiple roots,
  including received generated group, independent aliases and mismatched actual
  outputs; require equal complete Store/root/plan/closure and same rejection.
- Deliberately corrupted original or rebuilt values must still refuse before
  success. Counting control should show two rebuilt closure calls per root fall
  to one, never zero, and every object still gets equality checked.
- For union reuse, verify unchanged exact stage steps, plan bytes, returned
  artifacts/evidence and retained failure behavior; instrument union count
  separately from timed measurements.
- Keep all existing native passes/failed runs; combine a chosen tested change
  into one fresh v3 candidate rather than rebuilding for every small patch.

These are common-subexpression eliminations within a single controlled execution,
not an unverified immutable-Store claim. Exact-key persistent plan caching might
save more, but would require binding all object/inventory/foundation bytes and
policy plus mutation invalidation; it is not the low-risk deadline recommendation.

## Root-proposed stronger plumbing: return the plan the reader just validated

The existing `read_package` finishes with `make_plan(store, [root])` and then
discards the result. `Checker.submit` calls `read_package(candidate)` followed
immediately by `make_plan(candidate_store, [root])`, and repeats that pair for
the inverse package. Root proposes returning the first computation instead.

Recommended interface shape:

```text
read_package_with_plan(path, seed):
    ... exactly the original reader body ...
    plan = make_plan(store, [root])
    return store, root, plan

read_package(path, seed):
    store, root, _ = read_package_with_plan(path, seed)
    return store, root
```

The original two-result API remains intact for all old callers. A corresponding
Checker method applies the same package domain guard, metrics, total-byte check
and finally-block accumulated timing. Its legacy two-result wrapper must not
double-count reads or accidentally invoke both readers. Submission then directly
uses the returned `p1`/`p2`, removing the two adjacent recomputations. Nothing
between return and first plan use receives or mutates that Store or plan.

`verify_native` calls `reexport_actual(store, roots, actual)` and checks the
description; static inspection confirms reexport only reads the original Store
and creates a distinct `rebuilt = Store(store.seed)`. Its generated-object
insertions and inventory writes target the rebuilt Store. It does not mutate
the original object dict, inventory dict, plan or roots. Therefore retaining
the reader-returned plan through `verify_native` and comparing candidate/inverse
plans does not introduce stale-plan acceptance. Existing reexport recomputation,
object guards and full native checks remain in place.

This is a strict dataflow result, not a cache keyed merely by a root. Do not
place the new plan in an arbitrary mutable Store attribute and reuse it later
after caller edits. The three-result caller owns immediate consumption only.
No files are skipped and no valid-input/bound/failure check is removed. The
canonical plan is still generated once at the original reader boundary.

Add focused controls for exact two-versus-three-result correspondence and plan
equality, unchanged read/count/byte metrics, malformed-package refusal parity,
and deterministic `make_plan` call-count reduction at the two submit seams.
Existing trusted-reader input immutability assumptions suffice. Required source
scope is `source_codec.py`, `checking.py`, and their root-owned lock rows.

### Preserve repeated path checks when retaining the earlier submission union

The old second `self.union` starts by invoking `self.package(entry)` again.
Those cache hits still perform entry-shape/hash-string validation and current
resolved-path/domain/directory checks. Merely deleting them would change path
refusal behavior even though it does not add a mathematical trust boundary.
Preserve those cheap checks before reusing the initial union.

For an exact-output-equivalence contract covering changed path resolution, bind
the initial ordered input selection to the package-cache entries actually used;
after the stage, resolve/validate each entry again. Reuse only if both ordered
entries and resolved cache selections are unchanged. Otherwise use the original
union path (or make changed selection an explicitly documented refusal rather
than silently using the old Store). Checking only textual path equality is not
enough: `Domains.require_package` resolves paths, and its existing implementation
can distinguish different in-domain resolved targets. No platform/reparse threat
assumption should be silently expanded by this optimization.

If that additional bookkeeping distracts from deadline value, keep the original
second union for v3 and take the simpler reader-plan/closure reuse first. They
do not cross a subprocess wait or repeat filesystem resolution, so their
equivalence argument is narrower and easier to test.
