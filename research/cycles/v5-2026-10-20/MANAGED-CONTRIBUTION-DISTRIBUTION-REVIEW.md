# Managed-contribution distribution selector review

2026-10-21, support_screen. **PASS, SOURCE ONLY.** No source-level blocker was
found in the preparation-only selector for the exact reviewed successor below.
This does not authorize execution or establish a successful build/installation.
Root retains preparation, finite launch, adoption and Git ownership.

## Exact reviewed scope

`research/cycles/v5-2026-10-20/Select-ManagedContributionDistribution01.ps1`:
5992 bytes, SHA-256
`2e83c316afd241e8570aa958116273e2e969aa4d4500fb86d971c4b7b348fd85`.

The entire selector was read. Its exact baseline input, build-selection,
unchanged builder and independent composition-review pins were checked directly.
The earlier composition review remains a separate immutable checkpoint:
`MANAGED-CONTRIBUTION-REVIEW.md`, SHA-256
`86840438a5920c19e27654b6d30d4c0c4a0bc7e1f5bd6fdb88ca1d1deba0028f`.
The selector's caller must supply that reviewed composition digest and these
exact reviewed successor digests, not arbitrary syntactically valid hashes:

- Owner: `75c0e8a93c26594d459e716cf55dc6c982b1df079eeaed7834a1347fe4a40d09`.
- Private helper: `7116e2d9161cbb828203bc7eff1e7dd90c1cab7d6e860a6e16801ffb6ecb37f0`.

## Source argument

1. The canonical workdir is explicit. The pinned126-source input
   `4a9bfd78afd328d629ee6ad967f7f9378034db86cdee86bef751c5c50e6778a1`
   must have the expected schema/base role, the old owner digest and no helper.
   Every baseline source is byte/hash checked before the new map is made.
2. The only map changes are replacement of `v5/client/managed_owner.py` and
   addition of `v5/client/private_credentials.py`. The final assertions require
   127 SDK rows and106 v5 preparation rows:125 unchanged plus two selected rows.
   No installed predecessor or used source is edited.
3. The builder remains `software/v5/body_location/distribution.py`, SHA-256
   `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
   The pinned prior build selection
   `ac19b479647dfd39ee4f78df7699305dde90467e89bd832b24bd1ed05cac9a03`
   supplies the same selected Python/runtime/basis closure. The old build-input
   runtime row is replaced by the newly generated input digest; other rows are
   rehashed. For this exact basis the count remains29. No second builder or
   product import/loader is introduced.
4. The unchanged runner is pinned at
   `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
   Future builder arguments retain isolated/no-site/no-bytecode Python and bind
   the exact new input digest. The finite envelope is120 CPU seconds,600 wall
   seconds,128 MiB,two active processes and1 MiB per log stream.
5. The new input, selection, installation parent and outer allocation must all
   be absent before writing. JSON is bounded and exclusively created/flushed;
   the installation parent is fresh. Preparation writes only those new objects
   and returns their actual digests with `build_executed=false`. It does not
   invoke the runner/builder, issue credentials, start services or delete data.

The selector's fresh paths are
`experiments/v5-local-checks/distribution-managed-contribution-01-input.json`,
`experiments/v5-local-checks/distribution-managed-contribution-build-01-selection.json`
and `product-local/v5-distribution-managed-contribution-01/Mathematical Commons v5`.
Partial preparation is retained and will cause a subsequent freshness refusal;
there is no overwrite, cleanup or retry branch.

## Evidence boundary

This review used source/manifest inspection and bounded read-only hashes only.
No selector invocation, product import, AST parse, build, test, secret read,
service, mathematical runtime, installation mutation or Git operation occurred.
The reviewer did not perform a new complete large-payload sweep; the selected
unchanged builder retains its actual verification responsibility. Root must
inspect the generated maps/digests, separately select any one build and obtain
an actual build/output audit before adopting an installation. Contributor and
installed-orchestration review are separate, still distinct from this pass.
