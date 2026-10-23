# Ordinary-project proof return: narrow direct-import compatibility

2026-10-23, `retained_preparation`. Source-only implementation checkpoint.
Canonical workspace guard passed. No code or control execution, owner/database
opening, native work, package assembly or Git mutation by this author.

## User workflow and selected decision

An owner has a locally generated proof-complete bridge module and uses it in a
normal pinned Lean project. The existing trusted-project `contribute` backend
should author a fresh declaration using that module and independently check the
returned proof in the same warranted parent. Do not build a new proof-export
protocol, require a shim module or generate a cryptographic certificate.

Direct configuration was previously impossible: generated bridge names have
75 characters; the project-import grammar limited every component to 64. This
was established from source before selecting an experiment. The return rationale,
receiver-identity argument and whole-cost limits are in the existing
[export/return seam](ORDINARY-PROJECT-EXPORT-SEAM.md).

## Exact successor delta

New source: `software/v5/ordinary_project_return/ordinary_contribution.py`.
Predecessor: the unchanged, used `ordinary_project_package/ordinary_contribution.py`.

| File | SHA-256 |
|---|---|
| Preserved predecessor | `b8eefe6af368d8a7f5c498d563a12b31416c48c877ea471361eadd2a56a90b31` |
| New helper | `09394f523417406aefcad0b47d06fa2d7782940bec3bb5094975f08b68f94ca8` |
| New pure controls | `2e754900c73f6b64e58d59cae545f79932369e0a3c87ff33feffda292753180a` |

The helper changes only the name validator and its import call site:

- `_project_module(value, *, allow_bridge_import=False)` adds a boolean-checked
  internal option. No configuration field can set this option.
- With that option enabled, the full string may be exactly
  `DMKNBridge_[0-9a-f]{64}`. It must still satisfy ASCII-identifier/reserved-name,
  total-length and component-count rules. Full matching makes this a single
  component, not an exception for a long component nested inside another name.
- Only the `imports` loop passes `True`. Generated output module names, ordinary
  validation and direct dataclass revalidation keep the original <=64 bound.
- Ordinary short names that resemble the bridge prefix remain legal. No existing
  short-name grammar is removed just because the spelling resembles a bridge.

All source assembly, path/search order, count limits, owner/context/evidence
handling, semantic identities, checking, resource accounting and admission code
remain unchanged. Recognizing a filename does not authenticate module contents.

## Focused controls, not yet executed

`software/v5/ordinary_project_return/project_controls.py` loads the exact selected
package once and requires the helper hash above. It exposes the established CLI:

```text
--package <absolute-selected-package> --profile-sha256 <exact-hash>
--python-runtime <absolute-root> --lean-runtime <absolute-root>
--output <existing-root-allocated-output-directory>
```

One original 50-wall/30-CPU-second allowance covers loading and all four groups:

1. Exact 75-character bridge import, closed configuration round trip, unchanged
   output module path and exact source-header insertion before construction.
2. Import-only scope: default/output/direct-dataclass paths still refuse the long
   name; no user field or nonboolean option opens a new validation mode.
3. Wrong prefix/hex case/length, suffixes, dotted wrappers, injection characters
   and ordinary bound overruns refuse; existing short names and exact old bounds pass.
4. Existing closed fields, explicit meta flag, duplicate/import-count/search-count
   limits and path constraints still apply when a bridge is imported.

Only inert configuration and source-byte functions are exercised. Guards reject
real process, database, network, owner, custody, contribution or admission calls.
No module is compiled or loaded into Lean and no mathematical warrant is supplied.
The report is `PROJECT-RETURN-CONTROLS.json`; passing would qualify this narrow
configuration seam, not actual normal-project return or whole v5.

## Package replacement map and next evidence

The minimal successor of the selected public module package replaces only
`authoring/py/ordinary_contribution.py` with the new helper and updates that
payload's entry in the regenerated `PROFILE.json`. Existing owner/loader/worker,
native helpers, module exporter, installation manifest and mathematical IDs stay
unchanged. Controls are external test source, not additional product payload.
Root owns exact assembly/selection and independent review before any execution.

After this syntax-only boundary is qualified, the distinct consequential check is
one fresh public contribution importing the actual local bridge, preserving exact
parent import IDs and receiving real new-proof admission. Check that already
supplied targets introduced no scratch signatures. Do not replay earlier module
build tests or call an imported precompiled theorem a new current-module output.
Creating a bridge solely for one contribution may add cost; the practical benefit
is a return path from normal project work that already needs the paid module.

## Independent return-theorem analysis (2026-10-23)

`retained_preparation` is assigned the public native harness/theorem review;
the separate reviewer owns selectors, helper controls and package-map review.
This section is read-only source/theory analysis, not execution clearance for an
unfinished harness or a claim that the theorem was admitted.

The proposed new theorem `CommonsReturnExample.mapFour` has independent types
`a : Type u`, `b : Type v`, functions `f : a -> a`, `g : b -> b`, `h : a -> b`
and assumption `step : forall y, h (f y) = g (h y)`. Write `T f x` for the
existing `applyTwice f (applyTwice f x)`. The conclusion is `h (T f x) = T g (h x)`.

The explicit equality proof has the following endpoints, with no new axiom:

1. `congrArg h (applyFour_eq a f x)` gives `h (T f x) = h (f^4 x)`.
2. `step (f^3 x)` gives `h (f^4 x) = g (h (f^3 x))`.
3. `congrArg g (step (f^2 x))` gives the next equality to `g^2 (h (f^2 x))`.
4. `congrArg (fun z => g (g z)) (step (f x))` gives `g^3 (h (f x))`.
5. `congrArg (fun z => g (g (g z))) (step x)` gives `g^4 (h x)`.
6. `Eq.symm (applyFour_eq b g (h x))` gives `T g (h x)`.

`Eq.trans` composes these endpoints. Exponents here abbreviate explicit nested
function application in the source, not a numeral/power library dependency.
The selected installed inventory was independently decoded as inert JSON and
contains `Eq`, `Eq.trans`, `Eq.symm` and `congrArg`; their universe arities are
respectively 1, 1, 1 and 2. No additional library lemma is evident in this proof.
Both uses of `applyFour_eq` must bind the same existing ExportID despite different
type instantiations; `applyTwice` must retain its original definition ExportID.

This is a nonvacuous conditional transport result across two potentially different
types, but its easy derivation is not evidence of global novelty or growth benefit.
The prospective harness must still check exact evidence/import IDs, fresh local
admission, zero introduced scratch signatures for the supplied target, actual
supervised outcomes and preservation of earlier artifacts. Native source/runtime
compatibility and costs are not proved by this algebraic argument.

## Independent public-return harness disposition (2026-10-23)

Reviewer: `retained_preparation`. **Source review clears**
`software/v5/ordinary_project_return/public_native_check.py` at SHA-256
`5c9d1d3bc7cf66e3aaa5ca46845a78508127e81aa3b1a28e98de95ff59159290`.
No tests, Lean execution, owner opening, package assembly or Git operation was
performed by this reviewer. Root still owns exact selection; a source clearance
is not an executed pass. The separate reviewer owns the selector/package map and
pure import controls, so those are not independently requalified here.

### Mathematical and identity boundary

The equality-chain argument above applies to the exact source body in this
harness. The acquired theorem and transparent definition retain respectively
ExportIDs `0447787d07c5ada8730972d027bc25c5927e7c6552ef99c8fe4bdcda23285a6b`
and `b5054e3c29436f1fe8d175b47df405405f76683d7c1e27531d9e597f2e55ee02`.
Both the emitted candidate boundary and final evidence import map must contain
these exact bindings. The requested/returned parent must be
`84dd6a9cf7ece45c4820ab3c28fc50ec072168c77e3cef9b890183bff5af9e13`;
the new checked root must differ. The selected acquired UnitID is also passed
through the public request and compared by the existing custody/evidence path.
The existing locally generated module manifest, native report, five artifact
parts, semantic/foundation IDs and unchanged installation are pinned before use.

`OriginalDecl.encodeDescriptor` represents a theorem as tag 1 with its proof DAG
at descriptor index 4. `OriginalExpr.encode` places expression nodes at DAG index
2; constants have tag 2, exact name and a universe-instance vector. Therefore
`unit[1][4][2]` is the intended proof-node array. The two uses of `applyFour_eq`
at independent universes `u` and `v` yield two distinct interned constant nodes.
Counting these nodes establishes two distinct constant instantiations, **not** a
general count of application occurrences or proof size. The constant name and
its exact imported ExportID are checked separately.

The old bridge's imported declarations are not being relabeled as a new theorem.
The exporter requires current-module targets, excludes existing interpretation
labels and exports a complete fresh unit. The public contribution path binds that
unit to the authenticated parent, preflights its dependencies and calls actual
new-unit admission. The harness requires `CHECKED`, exactly one checked/retained
unit, equality of result and saved admission, exact complete evidence bytes, a
theorem descriptor/inventory row, recomputed UnitID/ExportID linkage and a preview
that resolves against those evidence bytes.

### Ordinary-project reuse and reporting

The generated source imports the already-paid bridge before construction.
`OwnerConstruction.demand` leaves an existing safe record in place; it does not
insert a substitute assumption in that branch. The inspected command actually
prints the signature array, so the harness's exact
`introducedNames=0 introducedSignatures=#[] checkedUnits=0` assertion matches its
format. The generated source bytes, owner-approved project configuration and
actual `--project-author-worker` supervisor argv are also checked. The selected
supervisor really records `argv`; the portable candidate schema really uses
`context_root` and `stats.source_records_enumerated`. No assumption that request
preparation contains all three bridge proof units is made.

Review found one reporting-only defect in initial harness `479dbf4e...`: an owner
close failure can change an otherwise successful response to `ok=False` while
retaining admission inside `result`, without adding top-level `accepted`.
The author changed only admission-summary extraction to prefer nested admission
when present and otherwise use top-level `accepted`. The revised lines and exact
hash above were reread. The full public response remains preserved before later
assertions, and no failure is interpreted as rollback. This correction does not
change the selected product's acceptance or close behavior.

### Cost, preservation and claim limit

There is one public `contribute` invocation; there is no module re-export,
initialization, certificate, networking or automatic retry. The original inner
150-wall/90-CPU allowance derives decreasing child grants, charges the whole CLI
Job once, and conservatively charges its reservation if final CPU is unavailable.
Nested authoring/admission charges are diagnostic, not added again. The separately
selected outer 180-wall/110-CPU/2048-MiB/eight-process envelope remains authoritative
for aggregate containment. Both public and authoring outcomes must close cleanly.
Sixteen prior result/adoption/chunk/module pins are compared before and after,
including on ordinary failure; selected package/source-input pins are also checked.

A successful execution would establish the specific normal-project-to-checked-
contribution return path using a preexisting paid module. It would not establish
general mathematical novelty, a growth advantage, arbitrary hostile-source safety,
all Lean-library compatibility, independent-host deployment or finished v5.
