# Renewal controls02: independent selector correction review

2026-10-22, storage_outcome_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**PASS_CHANGED_BOUNDARY_SELECTION_COMPATIBILITY.** Read complete selector02
and its complete diff against used01; parsed PowerShell syntax without execution.
Exact selector SHA-256:
`d2be66dccd3a9534e378d90e582b9f36ef4f759ec65ac9357f6b54291b536a58`.
This review builds on actual failure audit b562efe2 and controls02 source review
4f7825d4, not on an assumption that the failed controls01 imported successfully.

## Verified agreement

The only functional selector changes are the new02 run/output name, controls02.py
source/argv, two explicitly pinned pure helper additions, and135->137 census.
The unrelated comment changes do not affect execution. All runtime/fixture,
source-origin/path/freshness checks and resource limits are unchanged.

The four caller-provided hashes must be:

- InitSha: `b35e61684e93de713a5ee2df159f6ef8c162650367ebf5095e1f837b83e36cdc`.
- SourceSha: `fc5902f778fa37b484a4ab50d0594a1d5a0afe8b91896928bf321cce64dac019`.
- OwnerSha: `2bae25aecfd5935674a540d79580531334179ecce7a1e00ca6171d858fde87ac`.
- ControlsSha: `0b3a775d7e5ba6fe0b5232e83d88b0d5446fd4f9cffac80e92d2579fed6f017b`.

Hardcoded prepare_mixed2d03b635/inputd40b611e pins exactly match the two helper
files reviewed in4f7825d4. These augment the test snapshot only; the immutable
130-source SDK map remains unchanged. The137 physical sources reconstruct the
136 logical files expected by controls02. The updated argv names that same
controls02 entry, and the fixture remains019219ca. No old controls.py is dispatched.
Source bytes rise only by13470 over the previous1784377-byte set:1797847 bytes,
well within the wrapper's16MiB total bound. No new executable is selected.

Runtime remains the previously reviewed30-entry baseline plus current map and
fixture, exactly32. Caps remain30CPU/90wall/256MiB/one active process/1MiB per
log. Preparation creates only one new JSON with CreateNew; it launches nothing.
Selection and output paths were absent at this review. Syntax parsing passed.

## Required outcome

No selector, test suite, import probe, product operation or proof was run. Root
must inspect the resulting137-source/32-runtime selection and exact argv/caps
before a fresh bounded execution. Success still requires all six test groups
actually running, correct explicit-inert evidence, source preservation and clean
terminal closure. A future failure remains failed and charged, without automatic
rerun. No mathematical admission, genuine renewal, completed proof or full-v5
acceptance follows from this source-selection review. No blocking finding.
