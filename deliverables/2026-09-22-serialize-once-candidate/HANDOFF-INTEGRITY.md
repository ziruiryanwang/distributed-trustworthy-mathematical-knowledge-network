# Handoff integrity

2026-09-22. Root compared all three delivered package files with their originals
in `product-local/serialize-once-package-01`; byte lengths and SHA-256 match.
The tested installation was a fresh extraction of this exact archive. Independent
source review verified all 112 payloads and the generated manifest against the
archive and extracted files, and all 81 asset-lock rows against actual payloads.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| math-commons-source.zip | 3,638,034 | `3cd159228f1e5a655203e8f4d68e3436b5b015ad21b5a4b89e950d1ab906061e` |
| SOURCE-MANIFEST.json | 20,052 | `78ec60d3aaa4da7442a82756487632a7ed22a284e243821266480f7632c9f63e` |
| PACKAGE-RESULT.json | 455 | `c4bc65b81163688476742b0f14c7e34faed98594ee95842a4e3a9f2855c1e2e0` |
| Retained native integration result | 35,684 | `14ef9a798961240ad9384f6936038fc77829642296264751f740a06ca088f53c` |

The original delivered ZIP remains 3,637,844 bytes with SHA-256
`22e673620aa3a6cdba6aa21ef7e56a9dcafa4c1ed296c149f2c8ab24c0f01ff5`.
No old install, source snapshot, failure record or resource charge was replaced.

These hashes identify exact bytes; they are neither a publisher signature nor
a license grant. Packaging alone does not establish mathematical acceptance.
The companion [results](RESULTS.md) distinguish native qualification, synthetic
negative controls, prior-cut evidence and remaining support limits.

Root's final document check decoded 15 associated notes/navigation files as
strict UTF-8 and resolved 266 local file links without a missing target. It did
not certify anchors or remote URLs. The independent operational reviewer also
cross-checked the separate canonical audit's retained equality and
publication/admission/inspection claims; no promotion blocker remained.
All qualification scripts, launch inputs and machine results retain their
executed hashes. Original pending-audit machine labels remain unchanged.
