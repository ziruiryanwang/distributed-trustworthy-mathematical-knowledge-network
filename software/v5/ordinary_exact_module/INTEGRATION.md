# Exact installed module controller and anchor integration

2026-10-26. Source-only implementation under `CONTRACT.md`; no Python imports,
tests, native checks, assembly, owner-state access or source installation have
been performed by this assignment. Actual equality for the retained AllClosure
closure remains unknown. Root owns selection and runtime; `REVIEW.md` is the
independent source assessment.

## Frozen predecessors and footprint

The fresh successors start from these unchanged files under
`software/v5/ordinary_module_anchor`:

| File | SHA-256 |
|---|---|
| module_export.py | `85f9a2b5695dd90dd888bd3868f51a41904cb0b2d0d14335abe0b65d5182b65c` |
| anchor_store.py | `a244eaf2764b6a51f4006447eebe3b69529a46bf376f999804a99f23661a929e` |
| OrdinaryModule04.lean | `901e4fc06351f6ad658eba9b5ea23ab644648646c8567fc035b057aa1883cfe8` |

The planned product overlay still replaces exactly three payloads: the two
Python successors in this folder and the separately owned `OrdinaryModule.lean`.
The worker, closure collector, receiver, identities, fixed basis, resource limits,
native helper artifacts, report field census and report schema remain unchanged.
The default predecessor package remains
`experiments/v5-local-checks/transport-release-handoff01/suite/assembled/package`,
with PROFILE SHA-256
`b047d4492da79e363fcd154144a6d9088a93100fde7aac3c385f3a296a41dad7`.

## Controller and private commit changes

`module_export.POLICY` becomes
`ORDINARY_EXACT_INSTALLED_PUBLIC_MODULE_V2`. `validate_partition` retains sorted,
distinct, exact-integer in-range matched indices, at least one unmatched unit,
and exact request-derived counts, names and full inventories in original order.
Its matched-unit validation delegates to `anchor_store.matched_realization`.
There is no incoming realization-label field or new report schema.

The shared classifier uses the existing inert bounded unit codec before checking:

- Definitions: tag 0, one kind-1 row, singleton `all`, exact name, parameters,
  type, body, reducibility hint including height, and `all` correspondence.
- Theorems: preserved tag 1, one kind-2 row, singleton `all`, exact descriptor
  type/proof correspondence; returns `installed-singleton-theorem`.
- Opaques: tag 2, one safe kind-3 row, singleton `all`, exact descriptor/body
  correspondence and zero unsafe flag.
- Groups: tag 3 with only kinds 4/5/6; exact descriptor type/constructor census,
  parameter lists/types, parameter count, ordered inductive `all` and constructor
  lists, constructor owner/index, recursor `all`, and rule references/field counts.
  No fixed number of constructors or recursors is invented.

Definition, opaque and generated groups return `installed-exact-nontheorem`.
These are protected request-shape/coherence checks, not proofs of installed
matching. In particular, absence of a generated recursor cannot be diagnosed by
counting these names alone. The accepted complete-unit and every-sibling warrant
premises, native exact kernel/frontend comparisons, descriptor reconstruction,
atomic presence, public comparisons and prefix semantic scans remain necessary.

`Store._commit_generated` independently rechecks the original reservation's exact
request bytes, decodes every selected unit, and derives its tag from that protected
unit plus the validated matched index partition. It never uses report-supplied
family labels. The existing check that at least one unit is added remains, now
also rejected early by matched-index validation. That index validation checks
types before set construction, so malformed/unhashable indices close cleanly.

## Persisted interpretation and refusal

The reduced stored unit schema admits `installed-exact-nontheorem` only for a
single kind-1/3 output or kinds 4/5/6 with at least one kind-4 output. The old
singleton-theorem tag remains restricted to one kind-2 output. Names, export and
unit identities, level parameters, inventory hashes, complete ordered outputs,
and added/matched partition remain unchanged. Reduced metadata does not become a
standalone completeness or acceptance token.

Support identity already binds the policy, controller, store, native source,
worker, collector, selected owner/profile path and native helper bytes. The new
policy/source bytes therefore deliberately make predecessor anchors incompatible.
`_record` still requires exact support equality; `load` still checks current
context binding for every output and all five artifact hashes. There is no
migration, relabeling, saved-report adoption or recovery API. Old closed records
may remain stored while a new cold export is selected, but explicit reuse of an
old-support anchor refuses. A refusal does not rewrite its record or artifacts.

The record and plan schema names remain V1 because the compatibility authority
is exact support identity, not a schema-name-only fallback. Native plan reading
has the corresponding new family case. At least one actually added declaration,
both new-declaration kernel passes, both fresh private/exported rereads and the
protected pending-report binding remain mandatory.

## Verification boundary

`test_controls.py` and `TEST-PLAN.md` describe the prospective focused native-free
controls. They do not repeat the old sidecar storage suite. Root must separately
review/select execution, the three-payload overlay and any actual mixed module
operation. Passing inert tests cannot qualify installed declaration equality,
public visibility, Lean checking, module importability, query usability, or v5.
