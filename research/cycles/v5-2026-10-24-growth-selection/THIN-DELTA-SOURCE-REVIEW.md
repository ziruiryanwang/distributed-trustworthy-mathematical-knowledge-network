# Thin delta materializer: independent source review

2026-10-24. `thin_delta_audit`. Canonical guard passed. Source-only review;
no compiler, native import, test, package, protected state or Git mutation.

## Verdict

**PASS for the exact source correction; GO for root to select a bounded next
integration/compilation boundary.** No blocking changed-source finding. This
does not establish compilation, actual materialization, fresh registration,
ordinary-project use, general compatibility or final-v5 readiness.

A standalone syntax build is optional, not a required extra campaign. The
existing worker executes the source through Lean for actual materialization;
root may include compilation in the separately reviewed useful boundary rather
than pay for a duplicative syntax-only run. This review authorizes no launch.

## Exact reviewed identities and delta

| Source | SHA-256 |
|---|---|
| `ordinary_thin_delta/ReferenceModule.lean` | `026839805f72f8ae9bab99cc4401d878206052ff090175a64bc039405b186c91` |
| Preserved `ordinary_reference/ReferenceModule.lean` | `6660c657e10b7f34bcb2ecc1c32361c34075ff137197be9d87bb54780e03303e` |
| `ordinary_thin_delta/CONTRACT.md` | `44e245ef7141de9b059c423b9de0508204e5834df53b41ca31c4df138d15edb0` |
| Pinned Lean 4.34 `Lean/Environment.lean` | `ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86` |

Read the entire fresh source and contract. The line-ending-normalized diff
contains exactly three explanatory comment lines and replacement of the old
unconditional `!env.header.isModule` refusal with:

```lean
if env.header.isModule != publicView then
  fail "IMPORTED_ENVIRONMENT_MODE_MISMATCH"
```

The source uses the same condition on one line. No parser, import flags,
declaration rule, budget, output format, record check or control flow elsewhere
changed. The predecessor was not edited. Actual byte hashes above, rather than
the normalized comparison, identify the two distinct sources.

## Why this is the correct mode distinction

Pinned `Environment.lean:2308` defaults `finalizeImport.isModule` to
`level != .private`. The public `importModules` call at lines 2438-2449 forwards
the requested level without overriding that default. Private inspection thus
has enclosing `header.isModule = false`; exported inspection has true.
This does not determine each imported artifact's own modern-module flag.

The fresh materializer has exactly two `checkBaseHeaders` call sites:

- `importBase` at line 506 supplies `level != .private` immediately after its
  actual import; `run` invokes this separately for private and exported views.
- `reread` at line 602 supplies the same expression after importing the actual
  generated artifact. CLI dispatch supplies only `.private` or `.exported`.

Thus the new equality checks the actual supported import contract. It does
not weaken exported mode to permit a private map. No caller-supplied plan field
chooses this Boolean, and neither the header nor either constant map is mutated.

`setExporting` is a no-op on non-module environments, but that is not a bypass
here: private record/inventory inspection uses false, while public checking
uses a separately imported exported environment with the requisite true header.
The parked special source-authoring path is not repaired by this source.

## Safety and realization obligations retained

- `checkBaseHeaders` still requires every imported module's `isModule`, exact
  per-view original module order, generated chain/order and output suffix.
  `checkModuleHeader` still binds modern generated headers, exact direct imports,
  constant inventories and unique module identity.
- The base request/plan retains exact registered identities and the explicit
  artifact map. `searchPathRef` is empty; plugins and extension loading are off.
  Names alone and native digest labels are not independent base authority.
- `checkBaseRecords` inspects both frontend and kernel maps against the distinct
  registered projections. The new guard does not turn private availability into
  a public frontier or invent a signature-only proof warrant.
- Decoding permits only the registered usable/public/generated frontier and
  earlier new declarations. Collision checks inspect actual private records.
  Both `CheckedExtension.checkBatch` calls remain; its `addDeclCore` has checking
  enabled and rejects unsupported/unsafe/sorry dependencies under its policy.
- `OwnerRebind.exposeAdded` exposes actual new checked recursors and prefixes;
  it does not build a public base from private records. The writer comes from
  the separately checked exported environment, not from private inspection.
- New inventories are checked against both actual maps before writing. Both
  fresh rereads retain exact output/base/header/inventory checks. A failed
  public projection or missing private-only proof dependency still refuses.

The unchanged registered-import preservation argument is reused from
ORDINARY-REFERENCE-DELTA-CONTRACT, not proved anew. Compact metadata checks rely
on exact protected artifacts and current registered correspondence; they do not
become independent mathematical acceptance merely because this guard passes.

## Remaining integration boundary

`reference_registration.support_descriptor` includes the delta native source.
This change requires a new exact support binding and genuine fresh registration
under it, unless a separate migration is justified. The old registration or a
saved matcher report must not be relabeled. The logical installed role remains
`reference/ReferenceModule.lean`; this source directory alone is not an install.

No additional inevitable materialization failure was identified in this narrow
source review. This is not a claim that every later stage will pass: actual
public-frontier proof compatibility, fresh output serialization/imports and
ordinary consumer use still require their selected integration evidence. The
growth payoff is avoiding duplicate bases/new producer execution for the stated
warm compatible workflow, not a measured speedup or general cold-ancestry result.
