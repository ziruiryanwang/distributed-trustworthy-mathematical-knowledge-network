# Independent continuation review: reuse the retained controls03 archive

2026-10-26. Disposition: **GO for one root-selected native-free continuation at
the exact pins below.** This is source/selection approval, not an executed pass.
Controls03 remains failed; its narrow successful pack and all unrun checks are
separately recorded in `OUTCOME-AUDIT.md`. No product source, packaged guide,
archive, old test, runner or prior evidence is changed by this successor.

## Reviewed identities

- `test_bundle02.py`: SHA-256
  `17cd0c44568ac347c4013b1e1564afb7bd92441ced4de5dae08fda3af6dcb66a`.
- `experiments/workflow-source-continuation04-selection.json`: SHA-256
  `0e7c7e2ff68711c8682f76ee1344626d0c99458ae9b5cd6db7cc6f7dad5fadaf`.
- Unchanged product `bundle.py`: SHA-256
  `ceae62463c13dccd3a58faea0b8548d1454e09de3877b8058303dd51619b10c7`.
- Unchanged runner `tools/Run-V5-Check.py`: SHA-256
  `44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.
- Retained controls03 `suite/packed/source.zip`: SHA-256
  `46913cfd1c957720a673ec4a41f770bbcd10a489a04c176ca7bdbcbae5e39c49`.
- Retained controls03 `suite/packed/RECEIPT.json`: SHA-256
  `a807b5d365439457c3b2194838f6e5887ac5d71f19c3be6ee4308c6d2f0250a3`.

The review read the complete successor, its exact diff against the preserved
used test, the continuation explanation and runner, and compared the complete
old/new selection maps. All 154 selected source pins and all 159 external pins
were checked against current files read-only. Proposed output
`experiments/v5-local-checks/workflow-source-continuation04` was absent at review.
No product/test module was imported and no run, extraction or pack was started.

## Test-only delta and argument

The complete diff has only the following changes:

1. `census` obtains metadata with
   `Path(item.path).stat(follow_symlinks=False)` instead of cached
   `DirEntry.stat(follow_symlinks=False)`. The regular-file, symlink/reparse,
   single-link, membership, directory census and byte checks remain unchanged.
   This addresses the diagnosed Windows metadata false refusal without deleting
   a safety predicate. Fresh owner-controlled output and absence of concurrent
   replacement remain premises; this is not a new race-resistant sandbox.
2. The original public pack command, base-manifest copy and just-created receipt
   read are replaced by explicit reads of the retained pack directory. That
   directory must be absolute and resolved. Its receipt must name that exact
   directory. The archive must match the explicit selected hash.
3. The original complete archive metadata, receipt, manifest, all 143 base
   payloads and ten canonical companion mappings are checked again before fresh
   extraction. This rechecks inexpensive input binding; it does not reproduce
   the source archive or repeat a product operation.
4. Two required CLI arguments supply the retained pack directory and archive
   hash. The group and top-level scope labels now explicitly identify retained
   archive continuation, not a new pack.

Everything after extraction remains unchanged: one relocated public verifier,
unchanged-tree comparison, selected operational file/link closure, nine manifest
refusals, two bootstrap helper refusals and the fresh extra-member fixture.
The check against a base-manifest hash instead of the union hash still refuses.
The helper sentinels remain inert unless an unapproved helper were wrongly
executed; the test requires refusal at the prior length/hash check.

The old stdout/receipt equality assertion is no longer executed because this
continuation produces no pack stdout. The preceding independent failure audit
already verified that retained equality, and this selection pins the exact
receipt and archive externally before and after execution. The successor still
validates their schema, status, path, counts, lengths, hashes, base association
and exact content projection. This is sufficient for the selected reuse route;
it is not a generalized untrusted-receipt parser or archive import API.

## Selection and limits

Relative to controls03 the selection changes only:

- The fresh run name and corresponding output route.
- The old test snapshot row/argv path to the new test and its exact hash.
- Two new external rows for the retained ZIP and receipt.
- The two explicit retained-input CLI options.

All other source/runtime hashes, argv values and limits are identical. The
unchanged runner permits these 154 source entries under `software/v5` plus
itself; the two foundation inputs remain external pins, not disallowed source
snapshot rows. The source count, aggregate source size and external count stay
within the runner bounds. The test uses the selected canonical utility and
source mappings, not an entirely mirrored pack source, as previously disclosed.
Its protected-input premise and before/after external hash checks remain.

Bounds: 120 wall seconds, 60 inclusive Job CPU seconds, 384 MiB, four concurrent
processes, 2 MiB stdout and 1 MiB stderr. The unchanged test horizon is 110 wall
seconds / 45 controller CPU seconds. Exactly one successful child CLI is planned:
the relocated public verifier. Other new checks are bounded in-process file/API
controls. There is no pack, native build, mathematics, service, network,
publication, deletion, old-output write or automatic retry.

Root must select execution explicitly, preserve the terminal result and obtain
an actual-outcome audit of the newly reached checks. A future pass would close
this source-distribution continuation only; it would not relabel controls03,
establish independent-host usability, or complete the full v5 objective.
