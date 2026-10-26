# Find a conditional theorem without knowing its complete type

This optional search mode helps with one specific problem: the goal is known,
but a useful remote theorem has additional parameters and hypotheses that the
caller does not yet know how to formulate. It adds a small necessary-condition
filter to the existing portable index. It does **not** prove applicability, solve
the remaining hypotheses, or replace ordinary Lean search.

For example, a user working with repair schedules may ask:

```lean
run [r, s] x = run [s, r] x
```

A general theorem about schedules with the same fixed states can help, but its
full type may also mention order structure, closure and safety assumptions.
Those assumptions are not recoverable by simply replacing the goal's arguments
with variables. A type preview can introduce that vocabulary; the user still
has to acquire the mathematics and discharge its assumptions in Lean.

## How the filter works

For the raw curried form `Eq A (op x y) (op y x)`, the two fixed paths examine
the first argument of the right operand and the first argument of the left
operand. On commutativity these are `y` and `x`; on reflexivity
`op x y = op x y` they are both `x`.

A theorem whose two positions are the same parameter cannot instantiate, as
raw syntax, to a goal whose corresponding terms differ. The provider derives
this constraint from the exact advertised type. The consumer compares its two
goal terms and submits **one** ordinary feature query. Provider extraction adds
at most two postings per theorem; it reads no proof or proof ancestry.

The comparison preserves portable symbol identities, universe instances, binder
indices and expression structure. It ignores display names. It does not unfold
definitions, reduce expressions, use local equalities or decide mathematical
equivalence. Two syntactically different expressions may be equal in Lean.

The public values are `equal` and `separate`. `separate` also covers absent
paths, so it is not a proof of inequality. An `equal` query is nonselective:
every theorem in this profile gets that feature. Unconstrained and unrelated
theorems also survive a `separate` query. This is a small additional filter,
not a general matching engine. Prefer exact generalized queries, known symbols,
or an already approved Lean/Loogle environment when they are more selective.

## Prepare and search

Use an approved fresh correlation package. Keep the ordinary query workflow:
produce the desired closed formal type with the existing OwnerQueryCommand,
then resolve its referenced symbols either through `--bindings` or through the
existing `--context-root` workflow. Do not guess portable symbol identities.

Add this optional value argument to the existing supervised `query` entry:

```text
--conclusion-context-binders N
```

`N` is the exact number of leading foralls introduced to close the local context,
not the number of premises in a remote theorem. Explicit `0` selects correlation
search with no context wrapper. Omitting the option keeps exact whole-type
search. It is independent of `--context-root`, which chooses symbol bindings.
Do not strip every leading forall automatically: a forall can belong to the
goal itself.

Use the resulting single-element `SPECS.json` in the ordinary finite `peer find`
or `directory-find` operation, with explicit contacts and the original aggregate
budgets. The matching fresh `prepare_selected.py` accepts the new spec; the old
kit correctly rejects the unknown interface. No new network operation or OR
query is introduced. Results are still incomplete positive candidate metadata.

You may add supported kind/symbol/head constraints yourself. For the schedule
example the already known `run` symbol is useful. Do not automatically require
every symbol in a specialized goal: substitution can introduce symbols absent
from a general theorem, excluding a useful result.

Then follow the unchanged sequence:

1. Inspect and bind the candidate's exact preview.
2. Acquire its exact portable evidence and check it under local policy.
3. Inspect unfamiliar definitions and apply the theorem in an approved local
   Lean environment, proving all remaining obligations.
4. Check and contribute the resulting extension through the existing workflow.

Search, profile hashes and membership proofs do not grant mathematical authority.
Neither this helper nor an index provider executes remote Lean source.

## Installation and existing data

The source recipe is the existing bounded-build -> fair -> contact -> sparse ->
transport route, followed by this file-only overlay. It changes exactly three
runtime roles: the ordinary export adapter, query entry and supervised launcher's
query-option allowlist. Lean support, mathematical acceptance and peer protocols
stay byte-identical. A new PROFILE identifies the changed support.

The assembler takes explicit absolute source/base/output paths, the approved base
PROFILE and receipt hashes, and an exact four-payload overlay manifest. It creates
a fresh package and commits PROFILE last. It does not compile or approve native
artifacts. Do not edit an existing installation or weaken a profile check.

The discovery namespace changes. Create a fresh bounded index and republish only
selected locally accepted exports; do not relabel an old index or snapshot. Old
packages and indexes remain available unchanged. Reindexing and running multiple
namespaces cost real resources. Existing owner/snapshot compatibility rules still
apply; this guide does not authorize state migration or a reset of allowances.

The existing 128-feature limit is unchanged. If the full inherited plus required
correlation features do not fit, publication refuses for this profile rather
than silently omitting a key. Such a refusal says nothing about mathematical
validity. Other profiles, existing indexes and direct library tools remain options.

## What is and is not guaranteed

For supported validated syntax, if a goal is a capture-avoiding raw instance of
a theorem's conclusion, its correlation key occurs among that theorem's derived
keys. This narrow statement does not promise that the provider has the theorem,
will return it honestly, or can find it within any arbitrary budget. Added
conjuncts require their own coverage assumptions. Paths requiring reduction or
different vocabulary are outside this raw-instance guarantee.

Query equality uses two bounded structural-key passes over the supplied DAG when
both endpoints exist. It never expands that DAG into a tree. Input validation,
all node/byte hashing, provider indexing, reindexing, holding, unsuccessful queries,
partition fanout, candidate inspection and local application still cost work.
The theorem alone establishes no useful-growth rate or overall performance gain.

Source and focused integration status are recorded beside this guide. Until an
explicit reviewed outcome adopts the fresh package, it is a source candidate,
not a replacement for the existing handoff. Everything remains local and
unpublished; no license, external trial or worldwide-readiness claim is implied.
