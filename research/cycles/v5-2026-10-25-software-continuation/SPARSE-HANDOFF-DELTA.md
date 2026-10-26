# Smallest coherent contact-and-sparse handoff delta

2026-10-25. `ordinary_routing_gap`. Bounded source reasoning only. The canonical
guard passed. No implementation, package build, archive, experiment, product
import, state edit or general deployment audit was performed. The prior
`ordinary_source_bundle/ADOPTION.md` remains adopted and unchanged; its completed
source-closure/archive controls should not be repeated.

## Decision

**Prefer one fresh successor source handoff after a narrow operator-kit update,
not a packaging-only relabel of the old kit.** Reuse the existing build and
three file-only overlays; do not introduce a combined compiler, installer or
generic dependency resolver. Direct public commands already provide the new
product operations, so there is no reason to block current testing on the kit.
But a handoff advertised as an integrated investigator workflow must close the
actual configuration/report handoff gaps below before shipping it as such.

Keeping the additions separate is temporarily honest and usable for an operator
following `CONTACTS.md` and `SPARSE-SEARCH.md`. It is not the best final handoff:
the compact source archive omits their inputs, and the selected-package kit
explicitly rejects their profiles. Merely putting all files in another ZIP
would not make those interfaces cooperate.

## Existing source closure and dependency chain

The adopted compact handoff has 105 payloads: 84 bounded-build source inputs,
the fixed builder and source map, six fair-overlay inputs, eight operator-kit
files, two authoring-offer reference documents and three bundle documents/tools.
Its 3.05 MiB ZIP excludes runtimes, private state and historical experiments.
`bundle.py` hard-codes this exact census, fixed source pins and entrypoints; it
does not discover arbitrary later overlays. This was an intentional safety
boundary, not a missing wildcard to enable now.

The actual current build path is:

```text
unchanged bounded build + its BUILD-RESULT
  -> unchanged fair assemble + fair ASSEMBLY
  -> contact assemble + contact ASSEMBLY
  -> sparse assemble + sparse ASSEMBLY
  -> final PROFILE selected for all commands and compatible kit preparation
```

Both new assemblers import the unchanged fair assembler's bounded file helpers
under its exact hash. Contact accepts the fair layout and fixed noncompiled
source pins. Sparse requires the contact layout and a matching immediate-parent
receipt including the contact assembler identity. Native installation bytes are
copied, not rebuilt at either stage. Fresh native builds can use their own
selected build/profile/receipt identities; historical generated binary hashes
are not the only accepted build.

The additional exact source closure is small and explicit:

- Contact: ten mapped payload sources/documents, `assemble.py`, `OVERLAY.json`.
- Sparse: twelve mapped payload sources/documents, `assemble.py`, `OVERLAY.json`.

Those 26 paths are not in the old 105-payload archive. Retain the already included
fair helper/assembly sources and bounded build inputs; they are real dependencies,
not redundant research debris. No prior installation, receipt, experiment tree,
native output or test suite needs to become an archive payload. New build and
assembly receipts are generated outputs, supplied sequentially at use time.

A fresh bundle utility needs an explicit updated allowlist/count/entrypoint
selection and guide for these additions plus the chosen kit successor. The old
utility's hard-coded 102 known/105 payload counts must not be bypassed by relaxing
its census. Preserve the old utility and archive; select the new finite version
separately. Do not claim a final payload count until the kit source set is chosen.

## Packaging alone leaves an unserved prepared workflow

The current `ordinary_operator_kit/prepare_selected.py:known_layout` recognizes
only exact ordinary and fair-search variants. It uses a pinned compatibility
map and rejects other layouts with `SELECT_UNKNOWN_INTERFACE`. This is stronger
than a historical PROFILE allowlist: replacing only a profile constant or
passing the new profile hash does not select contact/sparse.

Even a map-only extension is insufficient:

| Existing helper boundary | Consequence for the new workflow |
|---|---|
| `prepare.py` find action permits exactly the original fields | `candidate_mode` cannot be prepared; sparse mode is not selectable through this kit |
| `index` requires exactly path/limits/create | `access_pairs` cannot be prepared for publish/serve |
| No directory-find/directory-serve action | Initial unknown-provider discovery requires manual direct CLI configuration |
| `selected_match` calls `Inputs.report(..., "find")` | A real successful directory-find report cannot feed prepared preview/receive |

The product already returns top-level `matches` from directory-find, together
with advisory learned contacts and nested search accounting. The new product
`find` also returns its compiled namespace/features and selected mode. These
are usable public data, not a reason to read private Store tables. Existing
preview/receive configuration already accepts an explicitly selected candidate
and owner-selected contacts. Thus the missing seam is inert preparation and
selection, not another transport API or mathematical acceptance rule.

## Minimal kit successor to select next

Use a fresh directory/version; preserve all used old kit bytes and its adoption
manifest. The minimum code changes are three successor files, with small
matching documentation/example/selection records:

1. **`prepare.py` successor.** Retain existing offline path/input/output/report
   bounds and all mathematical-authority disclaimers. Accept optional strict
   `candidate_mode` in direct find and forward it unchanged. Accept the exact
   optional static `index.access_pairs` configuration for publish/serve. Add
   directory-find preparation using the existing public fields and limits;
   directory-serve is another direct bounded configuration case, not a daemon.
   Let candidate selection consume either successful find or directory-find
   reports from the selected profile, preserving their actual operation name
   and unchanged exact record/snapshot checks. Do not manufacture a fake find
   report or rewrite historical evidence to reuse the old branch.
2. **`prepare_selected.py` successor.** Pin the fresh preparer and compatibility
   map; recognize the final known contact+sparse auxiliary layout explicitly.
   Do not infer approval from a caller-supplied arbitrary PROFILE. Keep the
   no-product-import and no-native-approval boundary. The final layout has 45
   noncompiled auxiliary roles plus the same 72 native roles, versus the old
   fair kit's 43 plus 72. Verify the actual selected file bytes as before.
3. **Fresh `compatibility.json`.** Pin the final known noncompiled sources,
   including contact_directory and pair_access plus their replacements. Native
   roles remain constrained by the known shape but separately approved by the
   actual package loader/operator. Do not edit the old map or its old wrapper
   hash to silently broaden approval.

Add a concise new selected-package guide and machine-readable request examples
for the integrated path. A new selected-kit manifest must start source-only and
record only later actual evidence; it cannot inherit the old twelve-control
adoption label merely because most code is reused. Unchanged authoring-offer
and original operation guides may remain references, with a clear new entry
page rather than a copied documentation hierarchy.

**Important contact boundary:** directory suggestions are not persistent dial
authority. A later prepared preview/receive request should require the operator
to supply/approve its explicit contacts for that new bounded operation. Do not
silently convert expired learned hints into permanent trusted contacts, inherit
directory CA files, or automatically execute subsequent commands. The kit can
validate the selected result without deciding what to research or authorizing
remote source execution.

This is small enough to serve the real user workflow; a generic schema registry,
automatic environment migration or new operator platform is not justified.
If even this narrow update is deferred, label new-path kit support unavailable
and retain the direct CLI examples rather than claiming complete integration.

## Smallest verification boundary, once separately selected

Do not rebuild native support or rerun the old source-bundle nineteen controls.
The decision-changing check is a tiny inert preparation chain using a selected
new profile and genuine public report shape: directory-find result -> explicitly
approved contact/candidate -> preview/receive configuration, plus sparse find
and pair-enabled publish/serve forwarding. Check wrong profile/schema, forbidden
fields, absent explicit contact approval and unchanged predecessor defaults.
Preparation executes no product or mathematics and must not invent a success
report. A separately selected public command check already planned for sparse
mode remains the place to exercise actual dispatch.

Only after this source/API seam is reviewed should a new file-only source
handoff be selected. Its changed-boundary verification checks inclusion of the
26 overlay inputs and chosen kit, unchanged baseline pins, exact census and
usable relocation/build-chain paths. This does not repeat the old archive's
qualification or establish a native rebuild from extraction. Packaging remains
delivery plumbing, not proof of useful growth, hostile-source isolation or
worldwide release readiness.
