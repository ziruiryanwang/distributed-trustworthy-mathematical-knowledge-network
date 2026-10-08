# Sample L bundle: independent archive identity audit

Reviewer: `/root/v3_index`; 2026-09-28.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Workspace guard passed. The reviewer did not run a prover, verifier, importer
or receiver, extract any file, or modify the archive or qualified source bundle.

Disposition: **PASS_EXACT_FOUR_FILE_ARCHIVE_IDENTITY_ONLY**.

## Exact artifact

[lemma-L-bundle.zip](lemma-L-bundle.zip) is 223,898 bytes, SHA-256:

```text
d6f2012e152b77e0e51ad189e156769c76ceddc9dd4604c4480fbbeac6f561f9
```

The archive has exactly four root-level entries, each occurring once, with
no directory, extra entry or nonzero external attributes. Each entry was
opened and fully decompressed through a bounded streaming read. Its actual
expanded byte count and independently computed SHA-256 equal the corresponding
regular, non-reparse source file under:

`experiments/certified-verifier-integration-01/receipt-01/bundles/L`.

The source directory itself was checked to contain exactly those four files.
Archive length/hash matched the root's selected pin; the archive hash was
checked again after all stream reads. No changed archive was observed.

| Exact entry name | Expanded bytes | Compressed bytes | SHA-256 |
|---|---:|---:|---|
| `bundle.json` | 680 | 455 | `9ff166b24c197e14e00b877f8aa631ed22d305e7a70ebbd98d625327cfab4902` |
| `capsule.json` | 1,739 | 577 | `c1ac67ddaa6ca8d894403c69326afd3fa477959817973e87d8aa53c23c43d1c6` |
| `journal.bin` | 148 | 153 | `384a17d3a0c54545f7db3bbb33f12c156a2224248c427b178948219cf398e9b6` |
| `receipt.bin` | 223,522 | 222,297 | `5ac187a57279f2fbaeab05dc37cc302541ca006bbb5fd172a22ccde54ab2e4d7` |

Total actual expanded bytes: **226,089**. Files extracted: **0**. Mathematical
runtime calls: **0**. The archive has no enclosing directory: extract these
four files together into a dedicated ordinary bundle directory outside the
receiver installation.

## Relation to actual verification evidence

The source manifest's payload lengths/hashes agree with these exact entries.
The source bundle is the authentic L input qualified in the existing
[receiver outcome audit](../../experiments/certified-verifier-integration-01/RECEIPT-OUTCOME-AUDIT.md).
That separate audit establishes the relocated receiver's positive case and
four selected genuine refusals; those runtime checks were not repeated here.

This archive audit establishes byte identity and packaging only. It does not
independently establish cryptographic soundness, native Lean admission,
recursive premise discharge, broader scale or useful growth. L is the
rank-zero case. The ordinary child certificate remains a separate ongoing
gate at this checkpoint; no child success is inferred from packaging L.
The sample is part of a local internal tentative handoff, not an external
publication or license decision.
