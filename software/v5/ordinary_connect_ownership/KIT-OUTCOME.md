# Owned-connect kit: saved packing and relocation outcome

2026-10-28, growth_design_audit. **PASS for the selected local archive,
extraction and inert preparer integration.** This audit read/hash-checked saved
artifacts only. It did not rerun the packer, import product code, execute the
preparer, open owner/database state, contact a peer, run Lean or mutate Git.

The source basis is KIT-REVIEW.md
`3c455f266ba2e69a1b2de6cd4288867ba412ae1365cf08442f7bc35cab0b7e25`.
Actual software/transport behavior is separately covered by OUTCOME.md
`5f61e1cb0405eac3cc2451b90d9a83267bb07a336d8a23691e74ba3843951d88`.
This packaging pass adds neither new mathematical acceptance nor independent
hosting/public-deployment evidence. Root owns adoption and version control.

## Exact archive and extracted bytes

Run: `experiments/v5-local-checks/connect-kit-pack01`.
The current candidate extraction is `packed/commons` beneath that run; the
adjacent archive is `packed/commons-local.zip`.

| Artifact | SHA-256 |
|---|---|
| Pack selection | `3305d476e963866f91cb194bae11bb2d414164af8ba8cd6d1e0a0bd6eebbb020` |
| Pack outer result | `d1560b33205a6f4ba1faeab48afb925c90c769044a97ae6a508456c41e5a6660` |
| Archive, **43,046,969 bytes** | `fab6080ff60d1845e92bb0815d4a908517819449eddd93ca36459515bfe4b058` |
| KIT-MANIFEST.json, 38,494 bytes | `f67dcfac7d27f319f899665b50d044deb7d6035622209e71c5761efe73006e0d` |
| External RECEIPT.json | `06daf9ee12308bf6fb47904ca81c183b60d21c9cbac35107bac5953333ed6e5f` |
| Reviewed source-file selection | `d333020c179de78efe87425f9bfbe92983153f99a82f86868c2f822ff90075b7` |

I independently recomputed the archive hash and length, streamed/hash-checked
all 267 ZIP entries, and rehashed every one of the 266 extracted payload files.
All sizes and hashes match the manifest and reviewed source selection. The
additional entry/file is KIT-MANIFEST.json itself. Archive entry names have no
duplicates; the extracted census is exactly 267 files, so no payload is missing
and no extra file is silently included.

The payload division remains **160 package files + 93 mapped sources + current
map/build recipe + 11 companions = 266**. Package PROFILE is
`d8eb8e4bfa4845ad44673ee037c739973dc5d03f89ed38ee80979c47888fa3cb`;
installation identity remains
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
The exact selected utility `1884f367...`, helper `b5d211a8...`, source map
`80d46cbe...` and builder `55794245...` match their reviewed roles. This reuses
the already audited source closure and package; it does not repeat its software
or mathematical audits.

The receipt reports `PACKED_AND_RELOCATED_LOCAL_KIT` and its nested verification
reports `VERIFIED_LOCAL_KIT_BYTES`, 266 payload files and the same PROFILE.
The manifest retains Windows x86-64 / Python 3.14.6 / Lean 4.34.0 as external
requirements and `UNDECIDED_LOCAL_ONLY` license status. Runtime distributions,
mathematical state, proof outputs and credentials are not bundled. Digests bind
bytes; they do not authenticate a publisher or remove the trusted-code premise.

## Relocated offline preparation

Run: `experiments/v5-local-checks/connect-kit-relocation01`.

| Artifact | SHA-256 |
|---|---|
| Relocation selection | `62c5ae4a61219c53ffddcb9666cab16ce661a0fad6f663ddfc5930a8b451bb5f` |
| Relocation outer result | `0cd5c85e71875f713a88111c3199fc4333162d2ea8716bac3647591c5bf1e558` |
| `checks/RESULT.json` | `b3c7c9be68c7b9a464bbc5a0c733171a7f270fdb2ed395a51a452193e932a2e4` |
| Saved checker source | `24b2e8fcab6814c4e8a8d437c3a77a5a9fcc3ef8f34ac59d79b62e75e0685cf0` |
| Prepared config | `463c3aee55ded3338098dca9f092b6532cd05c501f412deda3db601c6cb758f9` |

The checker source is the exact reviewed successor whose sole change from the
earlier directory-kit checker was PROFILE. It selected this new extraction by
manifest hash and invoked its offline `operator/prepare_selected.py` once, from
the extracted kit's directory. The saved result is
`PASS_RELOCATED_DIRECTORY_FIND_PREPARATION`, with child exit zero, empty child
stderr, 50 known noncompiled roles and false mathematical acceptance.

The actual 654-byte config hashes to the retained authentic config identity
above. It therefore preserves the previously obtained formal specs and search
configuration exactly. The saved arguments select entry `peer`, action `find`,
the new PROFILE and that exact config hash; `requires_launcher` remains true.
The preparer receipt reports zero product commands executed and no protected
state opened. The requested `unexecuted-find` output does not exist.

This demonstrates that the relocated wrapper's new compatibility pin accepts
the selected direct-source layout and produces the intended inert handoff. It
does not execute that find operation, establish a currently live provider at a
retained address, approve native artifacts or validate mathematics. The checker
appropriately reports zero native/network calls and no owner opened.

Across the pack and relocation runs, all six selected source-snapshot references
and all six runtime-pin references match. Repeated supervisor/runtime pins are
included in those counts. The source selection ties back to the static review;
the explicit runtime pins retain their existing nonhermetic-runtime limitation.

## Closure and cost

Both outer records are `COMMAND_EXITED_ZERO_AND_CLOSED`: exit zero, direct child
reaped, Job closed, zero final active processes, no requested termination and
no cleanup errors. Outer stderr is empty for both; the saved inert child stderr
is also empty. The relocation checker observed its one child exit before saving
success. No bound failure or forced cleanup is hidden by the pass flags.

| Stage | Inclusive child Job CPU | Separate wrapper CPU | Known total CPU | Wall through report | Peak Job private commitment |
|---|---:|---:|---:|---:|---:|
| Pack/extract/verify | 1.9375 s | 0.125 s | 2.0625 s | 6.4318917 s | 147,230,720 bytes |
| Inert relocated preparation | 0.21875 s | 0.078125 s | 0.296875 s | 0.4235770 s | 32,333,824 bytes |
| Combined | | | **2.359375 s** | **6.8554687 s** | Not additive |

The preparer child is already included in the relocation Job. Supervisor
subcounters are within their wrapper totals; no nested counter is added twice.
The selected pack envelope was 90 wall seconds, 45 Job CPU seconds, 512 MiB,
one concurrent process and 1 MiB per output stream. Relocation used 60 wall
seconds, 30 Job CPU seconds, 512 MiB, four concurrent processes and the same
stream ceilings. Lifetime process counts are not concurrent counts.

The local candidate is coherent at these exact identities and ready for root's
adoption decision. Used predecessor kits, the failed refresh workflow and all
source/evidence remain preserved. No release, license choice or external
publication occurred as part of this audit.
