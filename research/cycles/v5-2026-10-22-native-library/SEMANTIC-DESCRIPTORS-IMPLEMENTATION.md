# Semantic and implementation descriptor source checkpoint

2026-10-23. Author: `preview_boundary_review`. Root-selected source-only work.
No runtime, tests, build, Git mutation, catalog migration or acceptance occurred.

## Implemented scope

Only two fresh source files were added under `software/v5/ordinary_lean`:

| File | SHA-256 |
|---|---|
| `ordinary_semantics.py` | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| `semantic_identity_checks.py` | `9614df54f8bc66ab4d5086aa94eef46cd738466d38bdecdfff474e6d2ba972b4` |

The existing evidence reader, preview, catalog, controller, Lean codecs and
actual V1 recovery remain unchanged. These helpers are not integrated into an
accepted/public V2 route.

`ordinary_semantics.py` supplies exact canonical foundation/semantic descriptor
bytes and IDs, a bounded implementation-claim descriptor and ID, proposed V2
portable evidence/export/basis-symbol identities, and a separate planned local
materialization-root identity. It reuses `ordinary_evidence`'s canonical JSON,
bounded raw reader, unit census, name grammar and hex validation; it does not
introduce another expression codec or kernel.

## Exact contract, not an arbitrary profile label

F binds the current seed/inventory digests, 456-unit/581-name census, exact
upstream Lean revision and explicit initialization/projection rules. S binds F,
that upstream revision, the ordinary formats and their exact retained format
document digests, plus explicit canonical-byte and checked-extension policy.

The document references are fixed values, not hashes recomputed from whatever
files happen to be installed. Updating a controller or binary cannot silently
change S. The retained documents include historical status/default-limit prose;
their format/projection sections are the interpretation references, not evidence
that a build or a formal metatheory has been proved. Recognition of these exact
descriptors remains separate from actual foundation/checker justification.

The semantic-name policy explicitly matches `ExprCodec.requireSemanticName`
and the checked extension's additional `sorryAx` rule: string root, forbidden
root prefixes, forbidden root names, and exact forbidden component paths.
The two-component name `Lean.reduceNat` is represented as `["Lean","reduceNat"]`,
not confused with one string component containing a dot. The restriction applies
to semantic declaration/reference names, not inert binder labels.

F/S readers accept only the current exact selected descriptor bytes, after
bounded canonical parsing. Changed seed/rules or extra implementation fields
are refused. A future semantic contract is a separately selected revision,
not a permissive field update accepted by this reader.

## Implementation and local-root boundary

I contains S and separate exact commitments for kernel, adapter, basis receiver,
controller and snapshot support, plus platform and honest non-hermetic scope.
Those support manifests are not resolved or adopted by this pure module.
Recognized OS/architecture strings are syntactic claims, **not** tested platform
support. Only the current `LEAN_4_34_MODULEDATA_NO_EXTENSIONS_NO_IR` snapshot
format is recognized; serializer-format upgrades/migration are not implemented.

The planned local root binds S, I, owner-store identity, basis/extension kind,
parent and request hash under its own domain. Basis requires an empty parent;
extension requires a valid parent ID. A root hash is not a committed warrant
and authorizes no snapshot load. Exact artifact bytes, eligible parent lineage
and actual clean checking still belong to the future protected catalog event.

V2 unit identity hashes the exact bounded inert envelope with `semantic_id`,
and export/basis identities have fresh domains. There is no implementation ID
in these preimages. Identity helpers can hash a syntactically valid claim under
an unknown S, as content-addressing must be distinguishable from adoption;
the implementation-descriptor reader rejects an S outside its selected contract.
No helper migrates V1 identities or claims the unknown contract is supported.

## Self-review and proposed focused checks

Source self-review is complete. No blocking issue found in the assigned pure
identity scope. The small test source proposes four marker groups:

1. Exact F/S determinism; changed foundation and implementation-field injection
   refused; noncanonical final newline refused.
2. Identical inert evidence has identical portable IDs with distinct synthetic
   platform/support manifests, while I and planned local roots differ; owner
   store identity also distinguishes local roots.
3. Changing the advertised S changes portable unit/export/basis IDs without
   making that S a recognized implementation contract.
4. V1 envelope/domain separation, exact dependency census, and basis/extension
   parent rules prevent implicit relabeling.

The final-newline expected marker was verified by reading `strict_json`:
outside strings, LF is neither a bracket/numeric token nor comma/colon, so its
lexical branch raises `EvidenceError("JSON_LEXICAL_TOKEN")` before JSON parsing.
No test was run to obtain that observation.

Fixtures are synthetic inert declarations and synthetic support digests. Even
a future passing run establishes only these identity/shape discriminators, not
mathematical checking, platform support, migration or deployment readiness.
Root owns independent review, finite execution selection and adoption. The next
coherent V2 catalog/preview/index integration must still preserve the local
warrant and snapshot lineage described in `PROFILE-IDENTITY-SEPARATION.md`.
