# Native context-03: source-delta and exact-launch review

2026-09-21. PASS: no unresolved pre-execution blocker found for this exact source
cut and fresh allocation-03 launch. No Python/Lean import, compilation, product execution or database query
was performed. Only source/text reads and inert file/JSON/hash inspection were
used. This is not execution success or a mathematical dependency result.

## Reviewed source cut

Paths are relative to `software/` unless the preserved product root is named.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `tests/run_context_native_03.py` | 15700 | `19f569e813833372c8de2392d1c7722ade4e598bd39380e8d731415b28b1516c` |
| `tests/context_native_worker_03.py` | 23216 | `cc67f1341ead057438e3078aade12215ef0f98499ad49a89c0b0cc67f53a3b39` |
| `tests/scenario_profile.py` | 4619 | `b8b3e1b1c1485de80ae9fb2371c32771a4f8505fc90d580e021442f227fbcf6a` |
| `drafts/CONTEXT-NATIVE-03.md` | 4838 | `057231124dd4f7e9bd13be0f3b0eeb40701eef4c6a853f408a40221981eb6bc1` |

The complete new worker and coordinator were read. Their deltas were compared
against the reviewed allocation-02 files. A separate exact text transformation
check confirms the worker differs only by its fresh DATA root, preserved PRODUCT
root/source-copy selection and the three `noncomputable` prefixes.

The coordinator now selects all product inputs and the outer `run_stage`,
`supervise`, and `domains` modules from
`product-local/context-native-02/install`. Its ordered pin list, import search
path and loaded-module origin checks all use that preserved root. The unchanged
test-only scenario adapter still comes from `software/tests`; harness and Lean
runtime paths remain under `software`. This avoids mixing the mutable v3
development helpers into the v2 native discriminator. Snapshots still bind the
six selected Python source inputs before import.

## Preserved product and source-profile correction

The product inventory was independently enumerated using the same root-file,
direct-Python, recursive-native/asset rule and ordinal POSIX-relative ordering.
All 98 files / 3,434,601 bytes match allocation-02's recorded relative identities,
lengths and SHA-256 values. No product-file mismatch or reparse point was found.
Old build outputs and state are excluded; the worker must rebuild support in its
fresh installation. No source falls back to the mutable development product.

The preserved outer module hashes are:

| Preserved product file | SHA-256 |
| --- | --- |
| `py/run_stage.py` | `3c84f507dbb788827dbd50de2d0d7552e4f72bd615f425cfd5f1da278ac5a5be` |
| `py/supervise.py` | `e5f35c0a88602757ecb7ff899f923f940b588e11e2a7c9c36d51fdbb2dfcac1b` |
| `py/domains.py` | `a3f44cce31ddd79056f0683de17d46712bfd46c99dfe71fac56e27dd1deb59c9` |

X/Y/Z keep the same universe declarations, binders, types, root names and
mathematical bodies. Z still substitutes only the exact returned X identifier
at its two composition application sites. `noncomputable def` is a principled
source-profile correction: the reviewed Lean source suppresses optional code
generation while retaining a safe definition, and the existing capture/screen
and native `doCheck := true` replay remain unchanged. The separate source-only
diagnosis is `drafts/CONTEXT-NONCOMPUTABLE-REVIEW.md`. No unsafe foundation axiom,
alternate proof, checker weakening or successful native02 X identity is assumed.

## Unchanged bounds and acceptance obligations

The exact success path remains fourteen installed CLIs, ten ordinary requests,
six receiver stages and eighteen pipeline commands, plus one support-build stage
with two compilations. Reserved receiver grants total 848 MiB / 889,192,448 bytes.
These are not actual retained bytes or OS-process counts.

The requested outer test profile remains sixteen processes, 450 wall seconds,
450 Job CPU seconds and 6144 MiB, with 65,536-byte stdout/stderr/event limits.
Product public-eight/native-one profiles are unchanged. Retained endpoint bounds
remain 1 GiB / 16,384 files / 32,768 entries. Existing Job containment, cleanup,
failure-prefix retention, source/receipt/command/plan bindings, CPU preservation
before optional report persistence, and quiescent census remain unchanged.
Nested CPU is counted once inside the outer Job. Coordinator observations and
unmetered startup/final persistence remain separate; no exact auxiliary-PID
maximum or hard transient filesystem quota is claimed.

The worker retains exact metadata deltas, refusal-before-native checks, indexed
stage/request assignments, X submission/reception description equality,
historical selection/refusal replay, and prior rows/files/charges preservation.
There is no automatic retry, fixture repair, additional stage, refund, migration
or reuse of old acceptance evidence.

The strongest planned result is still `PASS_PENDING_DEPENDENCY_AUDIT`.
Operational outcome audit and independent canonical audit are required after
execution. The latter must bind exact source capture and inverse replay, distinct
X/Y package identities and branch closures, and two substantive X applications
in Z's reachable value. Shared constant DAG nodes need not be duplicated.
Native02 remains a failed immutable prefix; this correction does not rewrite it.

Even a pass establishes only this fixed local regression, not discovery, useful
growth, v3 renewal qualification, networking, independent hosts or usable-v1
completion.

## Exact launch

Reviewed `qualification/context-native-launch-03.json`: 44,180 bytes,
SHA-256 `fdd8b2dda543e0cb18d57b15eee4a0732bf9531d9d476991941c6094132b6985`.
All eight ordered source/runtime pins match their exact actual paths, byte
lengths and hashes, totaling 283,024 bytes. Their roles are Python, coordinator,
worker, scenario adapter, preserved runner, preserved supervisor, preserved
domains and Lean. The finalized launch itself becomes the ninth supervisor pin.

All 98 ordered product rows have the exact field sets and preserved-product
absolute paths, and match actual file lengths/hashes and allocation-02 relative
identities/hashes. Launch schema, top-level field set, exact limits and retained
bounds match the reviewed coordinator. No pin or allowance was substituted.

At final review both `product-local/context-native-03` and
`software/qualification/context-native-03` are absent. Selected input paths and
the existing fresh-root parent ancestries show no reparse point. These checks
do not prevent later trusted-owner mutation; the coordinator/worker still must
perform their pinned preflight and preserve any failed prefix.

Root may consider one execution of this exact allocation if those premises and
identities remain unchanged. No broader execution, retry or qualification is
implied by this source-and-launch disposition.
