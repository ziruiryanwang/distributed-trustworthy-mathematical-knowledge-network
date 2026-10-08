# Source trace

## 1. Prior conversation

The design input supplied by the user is:

`D:\Downloads\ChatGPT-AI and Mathematics Research-20260827-1346.md`

SHA-256:

`82F92900EC07B78B80C99C19CDEA0179450DFE0CB4EC0FB0F22FB2A4B9328922`

The file was read on 2026-08-27. It is a conversation export, not a peer-reviewed or authoritative source. It contains mojibake in some punctuation and names. Its predictions, web-search snippets, absence claims, 2026 preprints, company announcements, faculty details, legal comments, and market claims are not premises of Core v0 unless separately verified.

Relevant design regions by line number in that immutable source:

- lines 1977–2646: global mathematical knowledge-network vision;
- lines 4421–5160: proof packages, local verification, transparency, dependency impact, and phased prototype;
- lines 6525–7485: research lineage, proof-carrying research objects, provenance, federation, and agent messages;
- lines 7487–8382: typed theorem alignment and false-equivalence risk;
- lines 8419–9104: selective decentralization, federation, credible exit, and polycentric governance;
- lines 10131–10781: private/ZK knowledge claims and their limits;
- lines 10782 onward: proposed reading map.

## 2. Independently checked current standards

These primary standards were fetched from the RFC Editor on 2026-08-27 and their titles/status were checked directly:

1. [RFC 9943, *An Architecture for Trustworthy and Transparent Digital Supply Chains*](https://www.rfc-editor.org/rfc/rfc9943), IETF Standards Track, June 2026.
2. [RFC 9942, *CBOR Object Signing and Encryption (COSE) Receipts*](https://www.rfc-editor.org/rfc/rfc9942), IETF Standards Track, June 2026.
3. [RFC 9162, *Certificate Transparency Version 2.0*](https://www.rfc-editor.org/rfc/rfc9162), Experimental, December 2021; it obsoletes RFC 6962.

RFC 9943 is especially material. Its security sections explicitly state that:

- registration identifies/authenticates an issuer statement but the issuer may be wrong;
- VDS order need not equal statement-issuance order;
- issuers may register selectively;
- privacy and metadata leakage require deployment analysis;
- key-compromise recovery is deployment-sensitive;
- multiple independent transparency services and relying-party policy are expected.

DTMKN specializes this architecture for mathematical evidence rather than claiming that SCITT supplies storage, discovery, theorem checking, semantic fidelity, or universal non-equivocation.

## 3. Stable primary foundations to verify and snapshot for CP-001

The following are architecture inputs, but CP-001 should record exact version identifiers and local snapshot hashes before normative dependence:

### Formal systems and mathematical knowledge

- Lean 4 system and language documentation;
- Mathlib source and exact selected commits;
- OMDoc/MMT module systems and interface-theory work;
- Math-in-the-Middle interoperability architecture;
- Dedukti and proof-translation literature;
- LCF-style small-kernel architecture;
- relevant SAT/SMT proof-certificate formats for later adapters.

### Encoding, provenance, and supply chain

- RFC 8949, CBOR;
- STD 96 / RFC 9052 family, COSE;
- W3C PROV-DM / PROV-O;
- The Update Framework (TUF);
- in-toto;
- SLSA provenance specification;
- OCI image/distribution and ORAS artifact specifications;
- reproducible-build and Nix/Guix documentation.

### Distributed transparency and verification

- RFC 9943/9942 SCITT and receipts;
- RFC 9162 Certificate Transparency v2;
- CONIKS/key-transparency work;
- transparency witness, checkpoint gossip, and cross-logging literature;
- TLA+/Apalache;
- Tamarin or ProVerif;
- Alloy and fault-injection methods.

## 4. Quarantined recent references

The source conversation names numerous 2025–2026 systems, benchmarks, papers, and company results. They may be valuable literature candidates, but this checkpoint does not assert their existence, results, novelty, dataset sizes, or performance. Before use, record:

1. canonical title and authors;
2. primary publisher or repository URL;
3. version/date and persistent identifier;
4. local snapshot SHA-256;
5. exact proposition imported into DTMKN reasoning;
6. whether the work is peer reviewed, a preprint, documentation, or a company claim;
7. independent replication or criticism if available.

This quarantine prevents a fast-moving AI-mathematics literature from silently becoming an unstable foundation for protocol guarantees.

## 5. Evidence discipline

Every future checkpoint should label substantive claims as `DEFINITION`, `DERIVED`, `EXTERNAL`, `EMPIRICAL`, `HYPOTHESIS`, or `SPECULATION`. External claims cite primary sources; empirical claims include commands, environments, raw outputs, and hashes; hypotheses include explicit falsifiers. Agreement among agents or reviewers is not evidence by itself.

## 6. Current concept-generation decision trace

The user's 2026-08-27 corrections establish the current priority order:

- the first outcome is actually producing or reusing useful mathematics efficiently and accepting it reliably;
- agents may pursue independent local goals and learn from earlier artifacts without any shared root goal, campaign, sponsor, global budget, or common stopping rule;
- coordination remains important but is secondary and must demonstrate marginal value beyond passive typed reuse after its full overhead is charged;
- trustworthiness is also P0 because accepted work must not inherit false or malicious premises;
- operational identity may be P0 when needed for authenticated control, scoped authority, resource admission, revocation, or failure-domain measurement;
- political attribution, credit, prestige, ownership, and global discovery priority are secondary;
- SNARKs or related succinct arguments should be used only where their exact relation and measured system economics justify them.

The corresponding internal design decisions are recorded in:

- [CP-001A](checkpoints/CP-001A-autonomy-first-cooperation.md): autonomy-first amendment, primary property, zero-scope trace, optional coordination, and staged deliverable;
- [CP-001](checkpoints/CP-001-cooperative-knowledge-generation.md): cooperation-first project definition, two-plane architecture, and P0 deliverable;
- [Cooperation Core v0](../spec/COOPERATION-CORE-v0.md): receive/quarantine/admit lifecycle, grounded support, protocol, invariants, and liveness assumptions;
- [Trustworthy cooperation](../security/TRUSTWORTHY-COOPERATION.md): receiver-local evidence rule, operational-identity boundary, bounded adversary, and hostile-input controls;
- [SNARK assessment](../research/SNARK-ASSESSMENT.md): native-checking baseline, exact succinct-verification relation, break-even model, and deferral criteria;
- [Technology reuse map](../research/COOPERATION-TECHNOLOGY-REUSE.md): conservative NOW/EVALUATE/LATER/REJECT-P0 mapping with primary-source classes and implementation caveats;
- [Research and reuse testbed](../research/COOPERATION-TESTBED.md): base-efficacy, reliability, reuse, coordination, federation, baselines, workloads, and fault injection.

These documents make project `DEFINITION`, `DERIVED`, and `HYPOTHESIS` claims; they are not independent external evidence. In particular, least-fixed-point grounded support and receiver-local admission are design rules derived from the stated fault model, while improved useful-knowledge yield, scalability, and the succinct-verification break-even point remain empirical hypotheses.

The succinct-verification feasibility references named in the assessment—zkPi (CCS 2024, DOI `10.1145/3658644.3670322`), recursive proof-carrying data (STOC 2013, DOI `10.1145/2488608.2488623`), Nova (CRYPTO 2022, DOI `10.1007/978-3-031-15985-5_13`), and IACR ePrint `2022/206`—are literature candidates, not current implementation premises. Before normative use, record canonical metadata, primary URLs, versions, local snapshot hashes, and the exact imported proposition under the discipline in section 4.

## 7. Pre-freeze name/profile migration

Decision `D-023` adopts **Distributed Trustworthy Mathematical Knowledge Network (`DTMKN`)** as the current name, reserves **DTMKN Cooperation Core v0** for the P0 protocol, and renames the supporting object/transparency document **DTMKN Evidence Profile v0**.

The supporting profile's domain-separation tag changed from the former pre-freeze string `DVMKN` to `DTMKN`. This would change content identifiers in an implementation. At this checkpoint there was no frozen schema, conformance vector, published object, or implementation dependency, so the project chose a clean pre-CP-002 migration rather than a legacy wire alias. Any later tag change requires an explicit version/migration rule and new conformance vectors.

The independent protocol, scale, security, technology, and document audits are internal critical analyses, not external evidence. Their counterexamples justify design constraints; their agreement does not establish empirical performance or implementation correctness.

## 8. Post-audit design refinements

Internal counterexample review after the initial CP-001 draft produced five additional `DERIVED` constraints:

1. matching policy roots and authentication do not make an independently operated cell honest, so inter-cell exchange is always candidate-only and receiver-re-admitted;
2. a public or reusable bearer-like demand ticket permits theft and concurrent check-then-spend, so P0 uses non-spendable offers, authenticated scoped tickets, atomic candidate-bound reservations, and exact settlements;
3. separate same-polarity dependency closures cannot express ordinary mixed-polarity refutation, so justifications use signed heads and prerequisites in one grounded least fixed point;
4. membership of a root judgment loses path-dependent axiom, checker, reviewer, and diversity constraints, so stable reliance checks the exact finite evidence tree against the receiver's exact query contract;
5. concurrent quarantine and release facts are order-dependent without explicit predecessors, so reliance overrides use acyclic exact-ID supersession and incomparable actions resolve fail-closed.

These are protocol derivations from concrete attack/interleaving traces, not external empirical claims. The formal re-audit conditionally passed the revised Markdown specification; implementation, model checking, fault injection, and useful-yield experiments remain outstanding.

## 9. Autonomy-first amendment trace

The later user correction does not reject cooperation. It changes the dependency direction:

\[
\text{effective mathematical work}
\rightarrow
\text{trustworthy reusable artifacts}
\rightarrow
\text{optional passive sharing}
\rightarrow
\text{optional active coordination}.
\]

The reverse implication is invalid: a functioning coordination layer does not establish effective mathematical work.

Internal autonomy and evaluation audits derived these additional constraints:

1. `coordinationScopeRef` is optional for every base work/publication path and excluded from native proof validity;
2. a bounded `PublicationHint` may affect only expendable discovery state and quota-charged nonamplifying relay until a receiver selects it and reserves resources;
3. standalone work uses a receiver-issued grant → ticket → reservation path; sibling tickets reserve their full allocations from the grant, while optional global sharing needs escrow or narrow consensus only for that spend state;
4. a finite receiver-owned `serviceClassID`, not a sender-created goal/topic/scope, determines queue shares;
5. routing uses domain-separated exact object, goal, environment, or receiver-approved interest keys rather than campaign homes;
6. the mandatory workload contains zero coordination scopes and demonstrates staggered cross-cell reuse of earlier independent work;
7. participant-visible execution \(E\), sealed future inputs \(S_{\mathrm{probe}}\), and observer metadata \(M\) are separated, with required protocol-projection noninterference when only \(M\) changes;
8. base solving, reliability, local memory, passive cross-cell reuse, typed-infrastructure value, active coordination, optional programs, and decentralization overhead are distinct estimands;
9. a negative coordination result is a valid mechanism-level finding and does not invalidate a successful local research/validation core.

These are `DEFINITION` or `DERIVED` project claims. Whether the selected agents solve useful tasks, typed reuse adds value, coordination helps, or the architecture scales remains `HYPOTHESIS` until the preregistered testbed runs.

## 10. Post-amendment adversarial trace

Three independent post-edit audits supplied concrete counterexamples. Their corrections are internal design derivations, not empirical evidence:

1. a grant identifier inside several independently bounded tickets does not conserve the grant; ticket issuance must reserve the full ceiling and redemption allowance atomically from the grant;
2. releasing a child ticket's full reservation without charging its actual spend to the parent recycles capacity; terminal child accounting must transfer actual spend and consumed redemptions first;
3. a work-item-only `Close` predicate contradicts standalone evidence reuse; stable reliance is defined over an exact receiver-local `RelianceQuery`, with work-item closure only a derived convenience;
4. portable work content cannot carry receiver authority; `WorkAdmissionRecord` separately binds issuer-qualified budget, admission scope, service class, priority, replication, and retention decisions;
5. subscribed hint discovery and a zero-forwarding flood gate are contradictory; bounded authenticated subscription/home-shard relay is allowed, while payload work remains reservation-gated;
6. active coordination cannot be compared fairly if it also receives a stronger local solver, and an optional program cannot be isolated if it receives extra resources; local engines and componentwise arm-wide ceilings are matched;
7. reuse interference invalidates task-family bootstrap units; blocks are entire independent workload instances or genuinely disconnected components, and fixed-suite versus workload-population inference is stated explicitly;
8. “benefit” is decomposed into yield superiority, resource Pareto improvement under noninferiority, and reliability/resilience improvement under noninferiority.

The auditors initially returned `FAIL` on the affected draft. The dispositions are recorded in the audit ledger and must be rechecked against the final hashes; agreement among the auditors still does not establish implementation correctness or useful-knowledge acceleration.
