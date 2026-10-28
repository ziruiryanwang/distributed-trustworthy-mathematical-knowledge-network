# Finite advisory-query controls

Source only; not run. Root owns one selection and actual outcome. Proposed outer
limit: 60 seconds wall, 30 seconds CPU, 512 MiB, one process; the test's own
nonrenewing allowance is 45 wall / 25 CPU. Use isolated `-I -S -B` Python through
the existing whole-operation supervisor. No native, network, database connection
or real catalog opening is permitted; those calls are patched to refuse.

Inputs are an existing selected package/PROFILE (only source and installation
descriptor bytes are read), helper and query source with exact hashes, and a
fresh output below `experiments/v5-local-checks`. The existing package supplies
unchanged core validators and formal-name helpers. No new assembly is needed for
these controls. At completion all selected source/profile/manifest bytes are
rechecked. Root records the final source pins in its selection.

The four groups are:

1. Actual native and legacy record validators on synthetic extensions. Missing
   generated snapshots succeed only through the advisory scope; the original
   validator refuses missing snapshots. Wrong request/operation, duplicate
   binding, non-generated path, bad import-audit hash and bad original-source
   hash refuse. The scope clears after failure; skipped files are not cached as
   verified. Create/import/reserve/commit capabilities refuse. The helper's full
   projection returns only detached advisory data after close.
2. Partial missing names yield no binding-row query from the caller projection.
3. An inert close failure prevents a successful helper result.
4. Advisory input rejects custody arguments and mixed type/symbol modes.

The actual inherited opener, OS lock, activation and selected ancestry are
source-audited, not executed by these controls. In particular, legacy eager
hydration is covered by the unchanged opener's dynamic dispatch argument and
actual legacy record validator control; this is not a real imported-owner test.
Synthetic records have no actual Lean-check event and establish no theorem or
accepted context. The test-only opener interception is not production behavior.

The complete public output lifecycle was previously exercised for symbol queries;
the new caller retains that publication path. A separately selected actual query
checks the new integrated route without repeating service/find/native campaigns.
Do not infer large-context performance from these tiny controls.
