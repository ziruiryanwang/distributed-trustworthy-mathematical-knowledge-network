# Independent inert-mirror review

2026-10-26. Disposition: **GO for root's single proposed native-free selection**,
not execution authority, actual success, product adoption or mathematical checking.
Complete contract, helper, runner, source map, README, tests, revised test plan,
EXECUTION and exact selection were read. This reviewer performed only source and
file-pin inspection; no implementation imports, runtime, state or Git mutation.

## Contract finding C1: successful prepare must survive the command boundary

The contract distinguishes a worker return from clean supervised completion,
but does not yet prescribe how `serve` authenticates that distinction. A worker
can write a valid descriptor and then fail, exceed its budget or leave children.
If a later `serve` accepts descriptor existence or its READY field, a failed
preparation can still become publicly ready.

Required resolution was: the supervising parent must promote/seal the exact prepared
selection only after zero exit and whole-Job clean closure, or `serve` must require
an equivalent protected successful outer record bound to that descriptor and its
store configuration. Worker output alone remains a candidate. Preserve partial
output on failure; do not automatically roll back, overwrite or resume it.

**Resolved in selected source.** Core prepare closes stores before DESCRIPTOR and
never writes READY. Parent requires exact clean actual Job completion, binds
worker/report/descriptor/request/software identities, writes diagnostics and
readbacks READY-PENDING, then performs nonoverwriting Windows rename to READY as
the final state action. A precommit failure leaves no READY. Lost response around
the commit is explicitly possibly committed, not rollback. Serving requires exact
operator-selected seal/descriptor bytes and unchanged source/helper selection.
The marker relies on protected local state, not secret cryptographic authority.
All mirror results remain `mathematical_acceptance:false`.

## Complete source review

- Independently matched all 27 selected source/data lengths and SHA-256s to the
  retained investigator extraction; its manifest is `65edf28f...`. The fixed map
  supplies 22 library modules, launcher, inventory and three supervision files.
  Loader order covers actual imports and used lazy HTTP roles, including clients'
  module-store dependency; namespace-package search paths are empty. Unsupported
  body-adapter branches cannot be selected by this prepared ordinary-only index.
  No profile.load, NativeInstallation, admission/catalog or Lean artifact is
  needed. Python/stdlib/OS approval remains a premise; three runtime pins are
  not a hermetic attestation of every dependency.
- Helper validates every manifest batch and aggregate counts; unique outputs,
  basis collisions, exact import IDs and topological closure; exact target rows;
  complete supplied raw units; evidence-derived previews; selected indexing only.
  Its claim is syntactic closure, not generated-group completeness or Lean truth.
- Fresh stores and explicit disclosure precede writes. Conservative physical
  reservation covers databases/journals/metadata; index page size is checked.
  Each index call reserves its entire existing hash ceiling before execution;
  observed partial counters and an authorized upper bound survive exceptions.
  The enclosing original CPU/memory/wall grant is not renewed by per-call limits.
- Prepare closes stores before candidate descriptor output. Serve authenticates
  exact local descriptor/seal, obtains exclusive ACTIVE.lock, checks database
  bounds/sidecars, exact configs/status/snapshot, then enables query_only. It
  starts unchanged Provider with explicit disclosure, endpoint/TLS and finite
  limits. A single lease deadline and cleanup reserve bound normal lifetime.
  Errors still close Provider/stores; uncertain cleanup preserves the lock.
  Per-read content checks and protected immutable-by-policy storage remain
  essential; the descriptor does not make arbitrary peer databases safe.

## Tests, finite selection and honest coverage

The test's fixture module is imported only for existing constructors; its old
suite is not run. Four exact inert units include a three-unit chain ending in a
False claim with a Nat body, and one supplied synthetic group. No mathematical
acceptance of either is expected. Direct prepare forbids network/process entry;
public prepare/service run from the selected source extraction, without a native
installation. Actual API signatures, schemas and codec fixture shape agree.

Selected new controls cover missing/wrong imports, duplicate/basis names, bad
target/disclosure/count/byte/hash reservation, output reuse, late index refusal,
source-map and changed-codec refusal, missing/wrong seal or descriptor, live lock
conflict and changed-snapshot refusal before opening a listener. The positive
path uses genuine OFFER/candidate/preview/evidence calls with no initial target
or snapshot ID; the exact returned false claim remains inert. Whole supplied
group bytes and the unindexed sibling locator are checked locally. The later
index modification is deliberately limited to the newly created synthetic test
fixture after positive service closes; no previous installation is mutated.

The revised TEST-PLAN correctly distinguishes unexecuted/inherited controls:
runtime-pin mutation, undeclared-role changes, manifest/unit mutation and forced
cleanup failure are not separately fault-injected. Neither source review nor
earlier component tests become new runtime results. Keep the test's same-host,
finite-data, positive-discovery scope; this is not broad recall or speedup proof.

The final proposed selection is
`experiments/inert-mirror-controls01-selection.json`, SHA-256
`74f0dfcf92a87d58699c0ff20c280f05cbd63b00c12f8097c25248b1d4b675e6`.
All eight source and 31 external pins independently matched; the output leaf
was absent at review. The existing root supervisor supplies the one outer
180-wall/90-inclusive-Job-CPU/1024-MiB/eight-process allocation. Inner public
60-wall/30-CPU/512-MiB grants do not renew it; private controls and the finite
five-second loopback lease remain inside it. Expected test failures are not
retries or permission to continue after a failed entire selected run.

Reviewed consequential source SHA-256s:

| File | SHA-256 |
|---|---|
| mirror.py | `8b9d5301260b6648190d7e49e9ec488eb5f39419d242808aa84eaca5cd88116e` |
| run.py | `cef9b50b8a98231e7f9e60afb0f9021b7d5f495266b2320957076ab4e1c55bd0` |
| SOURCES.json | `1bc43d4c9896476443d0d6aab95015db7af32bc46a04cfb1624a5c40e638feb9` |
| test_mirror.py | `60600a26f4a49a080dedcbc8a8befbf8c48bbbeddba9d8165a320deae1c670d3` |
| TEST-PLAN.md | `ba3677dff2f141fa4667fbd4d39b5248418b1fca1f0f4dbb9ae758cbba313abd` |

No blocking source/test/selection issue remains in this review. Root must still
select launch explicitly and audit actual saved outcomes before adoption. The
unchanged mathematical receiver is not exercised, bypassed or newly qualified.
