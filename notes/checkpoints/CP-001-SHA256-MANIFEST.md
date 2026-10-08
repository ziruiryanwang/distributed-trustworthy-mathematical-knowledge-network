# CP-001/CP-001A Markdown SHA-256 manifest

## 1. Scope

| Field | Value |
|---|---|
| Checkpoint | `CP-001` as amended by `CP-001A` |
| Date | 2026-08-27 |
| Snapshot frozen | `2026-08-27T19:57:49-05:00` |
| Algorithm | SHA-256 |
| Included | Every Markdown file under the repository root after final substantive audit edits |
| Excluded | This manifest itself, so verification has no self-reference |
| Included file count | 18 |
| Source conversation | `D:\Downloads\ChatGPT-AI and Mathematics Research-20260827-1346.md` |
| Source conversation SHA-256 | `82f92900ec07b78b80c99c19cdea0179450dfe0cb4ec0fb0f22fb2a4b9328922` |

## 2. Artifact hashes

| Repository-relative path | Bytes | SHA-256 |
|---|---:|---|
| `notes/audits/CP-001-AUDIT-DISPOSITION.md` | 36565 | `c219aab89b883f40854df686e8abefff810caf1446c4a8fcdbe451ef9ed1da5e` |
| `notes/audits/DOCUMENT-INTEGRITY-AUDIT.md` | 15769 | `d09002492fdbed8631a6f04558f61c80c1a6765312fce79b50c0d5889725276b` |
| `notes/checkpoints/CP-000-concept-baseline.md` | 20220 | `304445c3a9ec347482e3433549a260e9a5c9199c826aee7b0be6b77da609d862` |
| `notes/checkpoints/CP-001A-autonomy-first-cooperation.md` | 44201 | `0934768dcd88de0771df1abea4dba9467e44799c08477641440e54418841deba` |
| `notes/checkpoints/CP-001-cooperative-knowledge-generation.md` | 45945 | `6faefeb991af7caea2ce5cb60e0bb8870cde6d3a79e2fa9402a315b50eb7c925` |
| `notes/CLAIM-AND-DECISION-LEDGER.md` | 36774 | `a0f646ad73e8283b2bacb46478c7d5ed0706441d75df5a47da948bdc0019a4b7` |
| `notes/COOPERATION-TRACEABILITY.md` | 17486 | `a3ee18f4f0511dddfc4f3f43cfb8e5ecf48a7a3a0bf8db32649ec17e060b9d96` |
| `notes/SOURCE-TRACE.md` | 14715 | `abfa662abebdc3def8719727d9ac1bbc9b159a66ba71c3663466560e544ebdc2` |
| `notes/TRACEABILITY.md` | 5174 | `58f8b01b641155c5c84a05127ae82c1ac37c2e4264020afa9b344852326750a6` |
| `README.md` | 8331 | `2ed25a0c3ad3b34d1c59d5a553b28f52c97349f67441ab60dec1b6734035707b` |
| `research/COOPERATION-TECHNOLOGY-REUSE.md` | 142205 | `4945e7f3a1f8cb51db125990ce2517e6e96e691157cccae1e3c954264be73f0e` |
| `research/COOPERATION-TESTBED.md` | 71272 | `0b035247dacc65f42ef893561bd0f3ae4e770e8000f95753d25da90c460218fd` |
| `research/REUSE-AND-DELIVERABLES.md` | 12673 | `44ce59342ab4101f2b5235aa5b79f208250504585f82bb3cb461acaa3fa5f1ae` |
| `research/SNARK-ASSESSMENT.md` | 11317 | `2a5e11a1df0cfb60485dc3798c4dac888752308b3e8a917ef8ab9a78d7128481` |
| `security/THREAT-MODEL-v0.md` | 15019 | `1ed4fb49489d73bd0c9f85c016c30fb8a3cafe2a7786be08c71dd0d2fb30f9fe` |
| `security/TRUSTWORTHY-COOPERATION.md` | 36884 | `029edbe11248f931b1bce9979a5c6b11e931b4ef262ab1c25211112ef46edc5e` |
| `spec/COOPERATION-CORE-v0.md` | 100162 | `00c9549aa02b9272510a7948fe1a4103a026b0a566f072cd560e9eb5080a2375` |
| `spec/DTMKN-EVIDENCE-PROFILE-v0.md` | 19781 | `47d436a3e24d5754760b4be853f486c4ec44fc45e9bd33e07c25ea35824fd4dc` |

## 3. Verification

From the repository root, recompute the same set with:

```powershell
$checkpointRoot = (Get-Location).Path
$manifestPath = Join-Path $checkpointRoot 'notes\checkpoints\CP-001-SHA256-MANIFEST.md'
Get-ChildItem -LiteralPath $checkpointRoot -Recurse -File -Filter '*.md' |
  Where-Object { $_.FullName -ne $manifestPath } |
  Sort-Object { $_.FullName.Substring($checkpointRoot.Length + 1).Replace('\', '/') } |
  ForEach-Object {
    $relativePath = $_.FullName.Substring($checkpointRoot.Length + 1).Replace('\', '/')
    $digest = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    [pscustomobject]@{ Path = $relativePath; Bytes = $_.Length; SHA256 = $digest }
  }
```

The manifest authenticates exact bytes only. It does not prove the specifications correct, the cited systems implemented, or the empirical hypotheses true.
