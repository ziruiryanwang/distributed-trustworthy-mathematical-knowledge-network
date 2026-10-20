# Demand-driven checking: defer the ordinary continuation

**DEFER implementation now.** Typed diagnostic `NeedBody` exists, but a safe
ordinary end-to-end continuation is not a small addition over the installed
interface candidate. No code, runtime, build, RAM inquiry or Git action occurred.
Active map inspected: interface distribution `V5-RELEASE.json`, `c249d086`.

## Exact existing boundary

- `modules/native/checker/src/bin/module_preflight.rs` catches typed `Demand` and
  returns `NEED` with a native name-table index and optional body digest. Its
  process exits zero on NEED, **not** mathematical acceptance. It needs an
  already formed native-row request; it is not a Lean elaborator service.
- The retained diagnostic binary is outside the installed role. It uses the
  earlier checker library; unchanged demand semantics were established by the
  separate native-negative applicability review, not binary identity.
- Installed `delta/native.rs` catches unresolved demands as generic
  `CHECKER_PANIC_OR_UNRESOLVED_DEMAND`, exit2. It does not emit a typed demand.
- Installed `runtime_efficient/mixed_claims/receiver.py::receive` checks process
  cleanup/exit before binding a conditional conclusion; every failure revokes
  its handles/cache. Public client action failure marks the operation FAILED.
  Parsing a diagnostic string cannot safely turn that terminal state live again.
- `workspace_atomic.py::extend_context` rejects a READY selection with
  `CLIENT_READY_CONTEXT_SEALED`. `SemanticReader` already resolves structural
  declaration/body demands before finishing; that is not missing functionality.

## The obstacle before native checking

The interface-only frontend substitutes a rigid opaque declaration for a
missing ordinary definition. If elaboration needs its reduction, particularly
a hidden type alias, Lean can reject before exporting any native witness.
`authoring/worker.py` returns a failure, not a bound semantic demand; the
preparation owner closes. Native preflight therefore cannot diagnose every
ordinary source-conversion need. Repeating it after a frontend failure has no
input and does not repair this gap.

## What a real extension would require

A separate non-admitting, bounded preflight owner could use the old diagnostic
binary on an already exported witness. Its demand must bind exact input bytes,
native index -> authenticated module/name, universe arity and committed hash.
An explicit supplier request would then use existing acquisition/custody APIs.
But a new immutable-context revision, final-witness re-emission and fresh final
native admission are still necessary; the current consumed/sealed context is
not renewable authority. Every attempted stage and failed search stays charged.
With d sequential demands, stateless preflight can cost (d+1) full passes rather
than one; current binaries expose no resumable checker state. This is narrower
than general source elaboration and needs explicit success/workload evidence.

## Higher-payoff disposition

Keep current fail-closed final admission. A knowledgeable local strategy can
already supply a selected committed body **before** READY import, in
interface-only mode, retaining demanded type/rule closure without requiring
every other ordinary-definition body. This is explicit selection, not automatic
kernel-guided discovery. Do not duplicate SemanticReader or add another planner.
Finish the already selected substantive evaluator-method discriminator; another
toy application would add little. General demand continuation is potentially
more valuable, but first needs a demonstrated workload and a principled frontend
demand boundary. Existing typed native diagnostics alone do not justify a GO.
