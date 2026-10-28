# A known mathematical name becomes a search constraint

This change serves an investigator who knows a concept in a checked local
environment but does not know the names or statements of useful remote results.
For example, `FiniteMapRefinement.Context` can select interfaces involving that
exact datatype. It does not assert which matching interface is useful.

The mathematical and networking implementations stay the same. The query entry
projects requested names from the explicitly selected local environment into
the already supported portable-symbol search constraints. The operator companion
provides a simple qualified-name input. If any requested name is absent, no
usable query is emitted. Searching a different environment can correctly yield
different identifiers for the same printed name.

The completed ordinary-source investigation does not show that this input gap
caused the index to go unused. Its five-module corpus was small enough to read.
This change addresses an independently observed API gap; it is not evidence of
faster discovery or a reason to require network searches in every investigation.

## Source and package selection

All predecessors and completed evidence remain unchanged. The successor query
is based on `ordinary_query_context/query.py`; the launcher changes only its
query option allowlist and input-path treatment for `--symbol-names`. Native
checking, admission, indexing and peer search retain their existing code.

Root selects a file-only assembly against the current portable build:

- Base: `experiments/v5-local-checks/current-distribution-build01/distribution/package`.
- PROFILE: `d5e56dd3bb2d1a531abeaabf06aea1864a7037c88a2035749230574455d7d4b0`.
- Build receipt: its sibling `_build/BUILD-RESULT.json`, SHA-256
  `08ef24292afc45b7cfae7075c0ea2231f45ea88e02cc05bca2dd263f95612863`.
- Changed payloads: `query.py`, `run.py`, `LAUNCHER.md`, and their resulting
  `PROFILE.json`. The other 150 package files must remain byte-identical.

The assembler checks the complete selected base receipt, profile and file map,
copies into a fresh destination, checks inputs again, and publishes the new
profile last. It imports only existing pinned file helpers. It does not compile
Lean, open a mathematical store or accept mathematics. Native outputs are reused
from the completed source build. A final payload-map pin and independent source
review are required before the selected assembly is executed.

The compact source-build recipe can select these three successor sources using
the same builder and native lanes. This does not call for recompiling unchanged
Lean support merely to qualify a Python input change.

## Targeted verification

First check the changed pure functions and report transformations: name syntax,
bounded counts, duplicates, exact context identities, all-or-nothing resolution,
legacy exact-type dispatch, and the launcher's new input path. Preserve the
existing context-opening and close-before-output behavior.

Then use the assembled public package for two short local queries against the
already checked B environment, with no new mathematical preparation:

1. Resolve the familiar `FiniteMapRefinement.Context` name and produce ordinary
   `type-symbol` constraints.
2. Request that name together with a missing name; require a diagnostic and no
   usable query output, rather than silently searching for only the known name.

After those calls close, one finite local service/find pair may use the positive
query report against B's existing index. This checks the new public input handoff
to actual matching records. It does not repeat the theory, its intake or a
reciprocal proof campaign. It is an integration test, not a discovery experiment.
Numeric launch allowances and fresh paths are recorded before each execution.

The same implementation and foundation identities are retained, so existing B
state remains eligible for the product's normal compatibility checks. Old reports
are never relabeled with the new PROFILE. The new query preparation permits an
explicit context root; the runtime verifies that root against actual local state.

The whole goal remains active, local and unpublished. Large-context metadata
hydration, useful search selectivity and comparative research benefit are distinct
questions; this change cannot be used to claim they are solved.
