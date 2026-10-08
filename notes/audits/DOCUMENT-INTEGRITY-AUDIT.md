# Document integrity audit

## 1. Audit record

| Field | Value |
|---|---|
| Date | 2026-08-27 |
| Scope | Every Markdown file under the repository root before this audit note was added |
| Pre-audit corpus | 14 files, 3,329 lines |
| Source conversation | `D:\Downloads\ChatGPT-AI and Mathematics Research-20260827-1346.md` |
| Source SHA-256 rechecked | `82F92900EC07B78B80C99C19CDEA0179450DFE0CB4EC0FB0F22FB2A4B9328922` |
| Repository state | Not a Git repository; no commit or machine-generated diff baseline is available |
| Repair policy | Apply only mechanical formatting, encoding, link, trace, and current-name repairs; preserve substantive protocol wording |

## 2. Result

After the mechanical repairs listed below:

- every Markdown file decodes under strict UTF-8;
- no forbidden C0 control character remains other than line endings;
- no common mojibake signature or Unicode replacement character was found;
- all 29 relative Markdown link targets resolved at the time of the check;
- all fenced-code blocks, display-math delimiters, inline-math delimiters, and TeX brace/environment counts balanced under the audit scanner;
- all Markdown table blocks had a stable unescaped-pipe count;
- no heading-level skip or duplicate heading was found within a file.

The apparent strings beginning with code point `U+9225` and a question mark, seen when reading some files with Windows PowerShell 5.1, were terminal-decoding artifacts. `Get-Content` without `-Encoding UTF8` interpreted valid UTF-8 punctuation through the legacy code page. Strict byte decoding and `Get-Content -Encoding UTF8` recover the intended en dashes, em dashes, and quotation marks. The repository files themselves did not contain that mojibake.

## 3. Mechanical repairs applied

1. Restored lost inline TeX delimiters around variables, asymptotic expressions, witness thresholds, morphisms, and scale parameters.
2. Reconstructed a corrupted theorem-relation definition in the supporting evidence-plane specification: a carriage return had replaced the `\r` of `\rho`, and a tab had replaced the `\t` of `\tau`.
3. Removed the resulting control characters and restored `\rho`, `\tau`, `\Gamma`, and `\mathcal E` as explicit mathematical symbols.
4. Normalized the current project name to **DTMKN** in current-document titles and prose. Historical CP-000 and the explicitly historical evidence-plane delivery plan retain **DVMKN**.
5. Added the current cooperation, trustworthiness, operational-identity, and SNARK deferral decisions to [SOURCE-TRACE.md](../SOURCE-TRACE.md), while labeling the succinct-proof papers as literature candidates rather than implementation premises.

Files mechanically changed in this audit:

- `README.md`;
- `spec/COOPERATION-CORE-v0.md`;
- `spec/DVMKN-CORE-v0.md`;
- `security/THREAT-MODEL-v0.md`;
- `security/TRUSTWORTHY-COOPERATION.md`;
- `research/COOPERATION-TESTBED.md`;
- `research/SNARK-ASSESSMENT.md`;
- `research/REUSE-AND-DELIVERABLES.md`;
- `notes/checkpoints/CP-000-concept-baseline.md`;
- `notes/checkpoints/CP-001-cooperative-knowledge-generation.md`;
- `notes/CLAIM-AND-DECISION-LEDGER.md`;
- `notes/SOURCE-TRACE.md`;
- this audit note.

## 4. Reproducible checks

The audit used read-only PowerShell and `rg` checks equivalent to:

```powershell
$repo = 'E:\Distributed Trustworthy Mathematical Knowledge Network'
rg --files -g '*.md' $repo
rg -n --glob '*.md' 'DVMKN|DTMKN|Distributed Verifiable|Distributed Trustworthy' $repo
rg -n --glob '*.md' `t $repo
rg -n --pcre2 --glob '*.md' '[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]' $repo
Get-FileHash -LiteralPath 'D:\Downloads\ChatGPT-AI and Mathematics Research-20260827-1346.md' -Algorithm SHA256
```

Additional PowerShell scanners:

- decoded every file with a throwing `System.Text.UTF8Encoding` instance;
- enumerated every character to reject non-line-ending C0 controls;
- resolved each non-URL Markdown link relative to its containing file;
- tracked code fences and `\[`/`\]` display blocks;
- checked per-line `\(`/`\)` balance outside code fences;
- counted braces and `\begin`/`\end` inside display blocks;
- checked table pipe counts and heading structure;
- searched for unrendered parenthesized mathematical tokens and common encoding artifacts.

These are deterministic structural checks, not a proof that every mathematical formula expresses the intended concept.

## 5. Unresolved substantive inconsistencies

The following were not mechanically changed because each affects protocol meaning or versioned identity.

### DI-01 — `UNKNOWN` validation state is inconsistent (P0)

[CP-001](../checkpoints/CP-001-cooperative-knowledge-generation.md) and the [testbed](../../research/COOPERATION-TESTBED.md) define validation results as `ACCEPT | REJECT | ERROR | UNKNOWN`, and the cooperation core says incomplete execution may yield `UNKNOWN`. However, the evidence-state enumerations in CP-001 and [Cooperation Core v0](../../spec/COOPERATION-CORE-v0.md) use `UNCHECKED | ACCEPT | REJECT | ERROR` and omit `UNKNOWN`.

Required disposition: decide whether `UNKNOWN` is distinct from `UNCHECKED`; then use one total state machine and specify its transitions. Collapsing them silently would conflate “not run” with “ran but could not decide or complete.”

### DI-02 — P0 closure predicates are not equivalent (P0)

The core and trustworthy-cooperation documents require typed-CID validity, contract match, exact-context match, resolved closure, base acceptance, grounded support, accepted composition, and absence of a locally established defect. The “P0 acceptance state” in [COOPERATION-TRACEABILITY.md](../COOPERATION-TRACEABILITY.md) lists only exact context, evidence-contract satisfaction, grounded support, and absence of a defect.

Required disposition: either make the traceability predicate a named abstraction that formally implies the omitted checks, or reproduce the normative predicate exactly. A traceability matrix must not accidentally describe a weaker acceptance rule.

### DI-03 — Materialized-view domains vary (P0)

The cooperation core uses \(V_{P_i}(A_i,O_i)\), trustworthy cooperation uses \(V_P(A_i)\), and CP-001 states convergence using \(V_P(F_i)\) and \(F^*\) without defining \(F_i\). These may be intended abstractions, but no projection between the domains is stated.

Required disposition: define one fact/object/availability state space and explicit projections. Then state convergence over the same domain used by the implementation.

### DI-04 — Receive/quarantine/admit notation mixes stage and set semantics (P1)

Several documents write \(R_i\supseteq Q_i\supseteq A_i\), while describing \(R_i\) as a bounded receive buffer and \(A_i\) as durable facts. At a time instant, a durable admitted fact may outlive the buffer element from which it came, so literal set inclusion need not hold unless these are cumulative historical sets or logical classes rather than storage contents.

Required disposition: use a transition relation for operational stores, or explicitly define the symbols as cumulative classification sets and introduce separate bounded queue state.

### DI-05 — Priority ledger overstates identity deferral (P1)

Claim C-015 says “identity, provenance, history, attribution, and transparency are P2 overlays,” while C-021/C-022 and the current security design make ephemeral operational identity, scoped authorization, revocation, and minimal failure-domain metadata P0 when necessary. The user's current instruction defers political attribution, not every identity function.

Required disposition: narrow C-015 to political attribution and rich historical provenance, with an explicit exception for P0 operational identity and control evidence.

### DI-06 — DVMKN-to-DTMKN protocol-identifier migration remains (P1)

The current project name is **Distributed Trustworthy Mathematical Knowledge Network (DTMKN)**. The file `spec/DVMKN-CORE-v0.md` and its internal `DVMKN` profile name, domain-separation string, predicate name, filename, and incoming links remain. These are not all cosmetic: changing a domain-separation string changes content identifiers and conformance vectors.

Required disposition: rename the supporting specification and links only with an explicit profile-version decision. Either preserve `DVMKN` as a documented legacy wire-profile identifier or introduce a new `DTMKN` tag and migration rule. CP-000 and the explicitly historical reuse plan may retain DVMKN as the former working name.

### DI-07 — Two different artifacts are called “Core v0” (P1)

The current cooperation protocol and the historical/supporting evidence-plane protocol both use “Core v0.” This makes phrases such as “Core v0 requirement” ambiguous across the threat model, old traceability matrix, delivery plan, and current testbed.

Required disposition: reserve `DTMKN Cooperation Core v0` for the P0 artifact and rename the other profile, for example `DTMKN Evidence Profile v0` or explicitly `Legacy DVMKN Evidence Core v0`.

### DI-08 — Traceability scope is ambiguous (P1)

`notes/TRACEABILITY.md` maps the historical evidence-plane security properties, whereas `notes/COOPERATION-TRACEABILITY.md` maps the current P0 cooperation properties. The generic filename and README label “Requirement traceability matrix” do not identify the former as historical/supporting.

Required disposition: rename or label the evidence-plane matrix explicitly and make the current cooperation matrix the primary requirement index.

### DI-09 — External succinct-proof references remain quarantined (P2)

The SNARK assessment lists four feasibility references. Their bibliographic strings are now traced, but primary URLs, canonical metadata, versions, local hashes, and exact imported propositions have not yet been independently recorded. They must not become normative premises until that source work is done.

## 6. Link-check caveat after the pending profile rename

All relative targets resolved before any rename of `spec/DVMKN-CORE-v0.md`. If that file becomes `spec/DTMKN-EVIDENCE-v0.md` or another name, update and rerun checks for at least:

- `README.md`;
- `notes/checkpoints/CP-000-concept-baseline.md`;
- any new audit or specification links introduced during the rename.

## 7. Audit conclusion

The repository has no detected byte-encoding, control-character, relative-link, Markdown-structure, or TeX-delimiter defect after the listed repairs. The remaining risks are semantic specification inconsistencies, not presentation defects. DI-01 through DI-03 should be resolved before treating the acceptance and convergence rules as frozen; DI-06 must be resolved before publishing stable identifiers or conformance vectors.

## 8. CP-001 resolution addendum

The preceding counts and findings are an immutable record of the first integrity pass. Subsequent substantive protocol work resolved DI-01 through DI-08 as follows; the final repository checks and hash manifest supersede the first pass for current file counts and hashes.

| Finding | Status | Resolution evidence | Remaining obligation |
|---|---|---|---|
| DI-01 | RESOLVED | The Cooperation Core and CP-001 use `UNCHECKED \| ACCEPT \| REJECT \| UNKNOWN(reason) \| ERROR(reason)` with explicit semantics. `UNCHECKED` is pre-attempt, `UNKNOWN` is bounded nondecision/unavailability, and `ERROR` is unexpected untrustworthy execution failure. | Freeze reason-code vectors in CP-002. |
| DI-02 | RESOLVED | [Cooperation Core section 5](../../spec/COOPERATION-CORE-v0.md) and the [cooperation traceability predicate](../COOPERATION-TRACEABILITY.md) both quantify over the same exact finite signed evidence tree and tree-level contract check. | Implement one shared predicate and differential tests. |
| DI-03 | RESOLVED | Current convergence and noninterference statements use \(V_P(A,O)\): locally admitted immutable facts plus locally available exact object closure under policy \(P\). | Preserve this domain in the materialized-view API. |
| DI-04 | RESOLVED | The core, security document, and CP-001 describe \(R\to Q\to A\) as transitions among distinct stores, explicitly not nested sets. | Model crash points in the executable state machine. |
| DI-05 | RESOLVED | Claim C-015 and CP-001 now make required operational principals P0 while deferring political attribution and rich provenance/history. | Do not let political reputation enter theorem closure. |
| DI-06 | RESOLVED PRE-FREEZE | The supporting specification is [DTMKN Evidence Profile v0](../../spec/DTMKN-EVIDENCE-PROFILE-v0.md). Decision D-023 and [SOURCE-TRACE section 7](../SOURCE-TRACE.md) record that the domain tag changed before any frozen vectors or deployed objects existed. | Any later tag change needs a versioned migration and new vectors. |
| DI-07 | RESOLVED | `DTMKN Cooperation Core v0` names the P0 cooperation protocol; `DTMKN Evidence Profile v0` names the supporting evidence/transparency profile. | Keep names distinct in APIs and reports. |
| DI-08 | RESOLVED | README identifies [COOPERATION-TRACEABILITY.md](../COOPERATION-TRACEABILITY.md) as primary and [TRACEABILITY.md](../TRACEABILITY.md) as the supporting Evidence Profile matrix; the latter's title and columns carry that scope explicitly. | A future filename rename is cosmetic and must preserve links. |
| DI-09 | OPEN / INTENTIONAL | Recent succinct-proof references remain quarantined and are not normative P0 premises. | Verify primary metadata, versions, hashes, and imported propositions before P1 use. |

The substantive audit disposition, including formal-protocol and scale findings, is maintained separately in [CP-001-AUDIT-DISPOSITION.md](CP-001-AUDIT-DISPOSITION.md).

## 9. CP-001A final validation addendum

The amended concept corpus was revalidated after the autonomy-first, execution-claim, metering, crash-time, capability-amplification, reliance-publication, Evidence Profile, and local-finalization/outbox repairs. The validation scope is every Markdown file under the repository root; the byte manifest excludes only itself to avoid self-reference.

| Check | Final pre-freeze observation |
|---|---|
| Corpus | 19 Markdown files, including the manifest |
| Strict text integrity | Every file decodes as strict UTF-8; no forbidden C0/DEL character, tab, Unicode replacement character, or scanned mojibake signature occurs |
| Markdown structure | 60 relative file links resolve; 44 table blocks have consistent unescaped-pipe counts; every code fence and heading hierarchy is balanced |
| TeX structure | 740 inline/display math blocks have balanced delimiters and unescaped braces; every scanned `begin`/`end` environment is properly nested |
| Parser | Pandoc 3.10 parses every file as GFM without error |
| Schema residuals | No obsolete one-field meter-basis schema, split epoch-before-state publication rule, generic cross-store atomic-finalization summary, capability-without-control-record summary, or execution-state regression transition remains |
| Required anchors | Root/child absent-parent tags, `RESERVED -> RUNNING -> FINALIZED`, per-component accounting, crash-safe receiver time, finite capability action records, atomic reliance tuple publication, strict native validation bases, exact attestation/replay binding, and nonauthorizing outbox boundaries are all present |
| Source trace | The source-conversation SHA-256 remains `82f92900ec07b78b80c99c19cdea0179450dfe0cb4ec0fb0f22fb2a4b9328922` |

The scanner is deterministic but deliberately syntactic. Its pass does not establish state-machine refinement, cryptographic soundness, checker correctness, useful mathematical efficacy, federation reliability, or any positive coordination effect. Those remain CP-002 proof, implementation, fault-injection, and empirical obligations.
