# CP-001F Markdown checkpoint manifest

Date: 2026-09-20  
Algorithm: SHA-256  
Included: 12 specification, analysis, audit and checkpoint documents  
Excluded: this manifest and the intentionally mutable CURRENT-DESIGN.md navigation page

## Scope

This freezes the v3 complete-evidence, proof-composition, provider/fine-index routing and foundation-migration concept, with source evidence and independent paper audits. It is not a software release, executed conformance result, security certification or completion of the ultimate goal.

Future substantive changes require an additive checkpoint or explicitly recorded amendment. Frozen earlier snapshots remain unchanged. Intermediate hashes in review notes identify actual review cuts; this table binds final checkpoint bytes.

## Artifact hashes

| Repository-relative path | Bytes | SHA-256 |
|---|---:|---|
| `notes/analyses/CP-001F-dissemination-and-routing.md` | 44424 | `57ea2ff2473cc2afd3fd68c2b7ea1fe84046de765d97bc6706441ee2a4b83f05` |
| `notes/analyses/CP-001F-exact-routing-coverage.md` | 31124 | `8367743a6708c7caef5478965859e3907a2d80b62f9fc774c518092a4b9dde7f` |
| `notes/analyses/CP-001F-foundation-evolution-and-migration.md` | 22434 | `c56b83b0fc99b9b8d174fcef1d0246d31dc9b03a763bfc5e35add0c2b991a45a` |
| `notes/analyses/CP-001F-lean-producer-client-path.md` | 25916 | `8bcd6a84d9fd121fb11294af3df5878c4f6ec08f5ce9985cc1603baa8a439983` |
| `notes/analyses/CP-001F-operability-and-index-economics.md` | 16121 | `03a7db93fdff03989c877f75459ee063c26c4f3a960a4ed626f013a7027b6725` |
| `notes/analyses/CP-001F-proof-identity-composition.md` | 31979 | `47422562b1099f485bd08bcc6f16b3333b83bb073ef9649e8b8a7c56752057db` |
| `notes/audits/CP-001F-AUDIT-DISPOSITION.md` | 10428 | `646f6cee154e4df1b1b18c99e0716a57b31baa2773538e2a8555cde8def084ef` |
| `notes/audits/CP-001F-migration-cross-audit.md` | 15637 | `bd97fe3ed2705e108d07db17e5cc07f54e0ed7c526db7cfbf17c85b30ee4d62f` |
| `notes/audits/CP-001F-routing-economics-cross-audit.md` | 19985 | `637a733d27e937ecb1073829432450f05e658534b7df85a580541869981e06cd` |
| `notes/audits/CP-001F-v3-integration-audit.md` | 19001 | `d0321964b97cb6084fcd8eff63ce139861ce1e370617044488443f953edf614b` |
| `notes/checkpoints/CP-001F-complete-evidence-and-unfamiliar-reuse.md` | 5155 | `a59542072f9f0096db28f7e08102ec2c3b1acda2225129549bffd4107c61b4ab` |
| `spec/OPERATIONAL-CORPUS-V3.md` | 23676 | `16c58e09530359cce106881e0436d9001c6671fb2dc8f59b17b912a35de669e1` |

## Verification boundary

Compare every row against its actual stored length and SHA-256 digest. Check strict UTF-8 decoding, replacement/control characters, local Markdown links, code fences and mathematical delimiters across these files, this manifest and CURRENT-DESIGN.md. Verify the older CP-001/1A, CP-001C, CP-001D and CP-001E manifests separately.

These checks establish document integrity only. They do not establish native soundness, executable correspondence, library-export compatibility, practical discovery performance, group-lease implementation correctness, custody durability or absence of unknown defects. No implementation, Lean replay, build, executable model, network execution, exploit or benchmark forms part of this checkpoint.
