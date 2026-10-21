# Finding general results from a local goal

This optional index profile adds one small conclusion fingerprint to each
declaration. It can suggest a general theorem from a concrete instance of its
conclusion without knowing that theorem's name or complete parameter telescope.
It is a candidate filter, not a prover, unifier or mathematical acceptance rule.

The owner chooses 1..3 expression-child paths of at most 12 edges. Paths must be
distinct and sorted by compact JSON bytes; an empty path observes the root.
Changing paths means another namespace and charged reindexing, not migration.
Use the matching explicit conclusion-fingerprint workspace schema. Do not combine
this profile implicitly with the pair or whole-type-pattern profiles.

```python
from discovery.conclusion_fingerprint import (
    FINGERPRINT_PROFILE_SCHEMA, conclusion_spec, goal_queries,
)

profile = {"schema": FINGERPRINT_PROFILE_SCHEMA, "paths": [["arg"]]}
source_spec = conclusion_spec(codec, module_id, universes, declaration_type, profile)
alternatives = goal_queries(codec, local_module_id, universes, closed_goal, profile)
# Each alternatives[i] is ONE ordinary query's singleton spec list.
# Select and fund desired alternatives through the existing adaptive-query API.
```

The adapter indexes source_spec automatically; callers do not authorize postings
by supplying it. Source declaration syntax is checked before stripping all leading
forall parameters. Their occurrences become STAR, including paths below them.
Other observations preserve expression shape, local binder positions and exact
constant symbols. Constants ignore universe arguments; sorts ignore levels;
projection metadata and binder annotations are not fingerprinted. There is no
beta/delta/iota/zeta/eta reduction, symbol transport or definitional equality.

For a local goal with context Gamma, pass its complete closed `forall Gamma, g`
codec wrapper and `context_binders=len(Gamma)`. The whole wrapper is validated
before exactly that many leading foralls are removed. Remaining foralls belong
to g. Internal binder variables and Gamma variables are distinguished; final
Gamma-variable observations force STAR because source fingerprints cannot contain
those context tokens. A path below a rigid context variable still observes ABSENT.
With context_binders=0, the supplied goal must be closed and is not stripped.
No metavariable or arbitrary local-context inference is provided.

For dimension d, the helper emits at most 2^d <= 8 separate query alternatives,
often fewer with context variables. It adds no result-head, symbol, declaration
kind or other conjunct automatically. Adding one yourself narrows coverage.
Compile each selected alternative through the actual workspace adapter, then use
ordinary direct or located next-query calls. Acquire desired evidence before
rotation; candidate/staging handles retire, while genuine warrants retain their
original authority. Generating eight alternatives does not fund eight operations.
Goal generation is bounded local caller computation: this helper returns no cost
report and does not debit a search/acquisition ledger. Source extraction, by
contrast, adds its measured structural-work count to the adapter's existing work
limit. Both paths retain whole-input validation and their explicit syntax bounds.

If the source type and closed goal wrapper both pass the stated validation and
resource bounds, use the same profile and exact rigid symbol identities, and the
goal is a well-scoped raw capture-avoiding instance of that source conclusion,
its generated keys include that source's fingerprint key, subject to the stated
hash assumptions. This does not prove the instance exists, satisfies dependent
parameter types, discharges assumptions or gives a true theorem. A syntactically
scoped context wrapper is not a kernel-checked context. Actual mathematics still
passes the unchanged admission and application checks.

Complete input handling uses the existing bounded codec and occurrence-counting
preflight before whole-expression encoding; oversized, open, cyclic or malformed
inputs fail rather than produce partial keys. Each publication adds one required
posting and still obeys the existing 128-feature cap. Large wildcard buckets can
remain unhelpful, and failed searches consume ordinary budgets. This mechanism
does not promise semantic equivalence, global recall, bounded posting-list size
or a measured useful-growth improvement. Existing ordinary profiles stay intact.
