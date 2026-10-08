# Consequential-assumption ledger: independent boundary audit

Date: 2026-09-20. Reviewer: `direct_broker_protocol_audit`. Scope: bounded source-organization review of the new [assumption ledger](registry/ASSUMPTIONS.md) against selected V6/I, inherited reconstruction limits, J/VIEWS1 and [INTERFACES](registry/INTERFACES.md). Check consequential omissions or overstatements, failure grades and accidental promotion of identity, review or future runtime evidence into mathematical truth or availability. This is not a new foundational/security audit or independent requalification of every linked source.

Only this audit was written. No selected/frozen contract or author registry was edited. No implementation, executable model, native replay, extraction, test or benchmark was performed. Source reading and document-integrity checks are the evidence grade.

## Exact reviewed cuts

| Artifact | SHA-256 |
|---|---|
| `research/registry/ASSUMPTIONS.md` | `91567D33FBD049FF7368096612C46549BF99FE8C3498C533EA319FDEC2AE7519` |
| `research/registry/INTERFACES.md` | `F900ABB7DB5208CA9A594EA13911A2289930F72542533D19604CFACB2E9E2CF2` |
| `spec/OPERATIONAL-CORPUS-V6.md` | `95FC34057FB5E00D9F453287F396BC935FBA9BEE9EC5F4B5FE24404125F2B5A2` |
| `spec/OPERATIONAL-CORPUS-V5.md` | `6C1E723492779ED7238731D5D7D2849D6E6DBFE3F2052DCDD6C68D99F13231B0` |
| `notes/checkpoints/CP-001I-candidate-only-discovery.md` | `7BA0F39503CC6B98624911D5F6C4BF17305FE9EAD0736A7C2AC520E9750DD600` |
| `notes/checkpoints/CP-001J-unfamiliar-interface-entry.md` | `ED28F31BDC1013DC592B3B7EF6E265444733F81E3FA8009C7B618F0DA07E8F09` |
| `notes/analyses/CP-001I-candidate-service-trust-boundary.md` | `497C105A3EFD4502A8D7107489E8CDB78DC37D0696451C1E4040E3952D88E62F` |
| `notes/analyses/CP-001I-broker-local-retry-policy.md` | `7E859F189A498090D054D5411136FA5569C8F86FCC036B69F6AFFC98615FAABB` |
| `notes/analyses/CP-001I-broker-economics-and-availability.md` | `0E3AFB634128694DC5B5160954BF0EE73BA445E8CC2110F86EFA961DDF092DE2` |
| `research/modules/query-view-expansion/proposal.md` | `2AC5045E20F9B44198BEFBB1048987132A3E7AB2F3DEF08B6AD0695DBBF467A2` |

The complete new ledger was read. V6, the I/J checkpoints and INTERFACES supplied the integration boundary; relevant V5 source-correspondence/bootstrap and I durable-accounting/availability passages supplied targeted checks. The VIEWS1 source retains its separately reviewed exact cut. This table identifies source cuts used, not a claim that every older contract received a fresh full audit.

## AS-AUD-001: acquisition need not finish from one source

Initial status: open organization-level premise precision at `91567D33...`.

AS-08 says that for a promised acquisition/reuse path, "at least one selected source" supplies "the required exact bytes" with enough service before the limits expire. Read as a necessary acquisition premise, that demands one source capable of serving the complete required evidence during the interval. The selected contract also supports a finite compatible union of actual responses.

The [candidate trust boundary](../notes/analyses/CP-001I-candidate-service-trust-boundary.md), acquisition section, expressly permits combining chunks from different sources after exact CID/range/hash and complete-closure checks. The [economics/availability analysis](../notes/analyses/CP-001I-broker-economics-and-availability.md), evidence-availability section, explicitly says acquisition can succeed "without any one source serving every requested byte during the interval." It separately preserves the qualified-source retention contract.

Concrete distinction: two qualified sources may each retain the complete replay while their actual admitted responses during an interval cover complementary portions. If the receiver obtains the entire exact closure through those compatible authorized responses within its aggregate budget, acquisition can succeed even though neither source individually served it all. Conversely, several partial observations that leave one required object uncovered are not complete acquisition or complete custody.

Minimal repair: require a finite selected source set whose actual authorized, compatible responses jointly cover the complete required evidence within the actual aggregate resources and deadlines. One sufficient source is a special case. Explicitly preserve the existing complete-retention obligations of any source claiming qualified-native status; union acquisition is not permission for a partial custodian to claim that role.

This finding concerns an overstated liveness premise, not a native acceptance defect or a need to change selected protocols. It supplies neither a new source-contact allowance nor a presumption that partial responses can always be combined.

## Other boundary checks

The twelve-row grouping makes the consequential boundaries visible without creating a rival specification. AS-01 through AS-05 separate binding/decoder trust, operational authentication, adopted native basis, faithful actual checking/current use and source correspondence. Correctly checked target mathematics is not promoted to faithful source import; abstract proof irrelevance is not promoted to unchanged executable conversion. A compromised or dishonest operational identity is not itself a proof of a false theorem while the actual acceptance boundary remains intact.

AS-06 and AS-09 retain durable owner accounting, atomic settlement, uncertainty fences, qualified clock origins, all-times resource stock and the distinction between numeric caps and actual supply. Recovery/clock failures may stop progress; resetting allowances is not an allowed repair. The permitted value-CAS ABA case is not mislabeled as persistent withdrawal. The I stock-time countercase remains arithmetic under explicit premises, not measured throughput.

AS-07 through AS-10 separate possession/custody, future service, failure-domain assumptions and exact scoped discovery. Multiple keys, old receipts, listed metadata or successful partial reads do not establish future availability or independent redundancy. Missing routes or truncated features may defeat recall without proving global absence. AS-11 preserves actual application checking and the preservation/image/reflection distinction. AS-12 keeps usefulness and sustained growth empirical, with cold costs and failures retained rather than removed from the success denominator.

The opening and closing qualifications correctly state that local enforceability is conditional on implementation/integrity, finite tests do not prove general assumptions, and paper review is not runtime qualification. No consequential premise family missing from the assigned V6/I/J/interface organization scope was identified beyond AS-AUD-001's precision issue. This is not a claim that the ledger exhausts every inherited TCB or environmental assumption.

## Initial disposition

Repair AS-AUD-001 in the author-owned ledger and identify the new exact cut for focused rereview. No other concrete finding remains in this bounded organization scope at the initial cut. Review closure, if recorded later, will bind the repaired bytes and will not certify future registry edits or prove that any listed assumption actually holds.

## Repaired-cut rereview and closure

Re-read the complete twelve-row ledger at held SHA-256 `26EFE1EBF9CEE44A5CC5CF7C7007112B2D598D6435237AD15E03A4FE797F8F2E` on 2026-09-20. The historical table and initial finding above retain the original reviewed cut.

**AS-AUD-001: closed at the repaired cut.** AS-08 now requires actual compatible exact CID/range responses from a finite selected source set, together with admissible retained local bytes, to cover the complete required closure within the aggregate caller allocation and each source's grants/deadlines. It explicitly makes one sufficient source a special case. Failure of one source defeats the promised path only when the remaining admitted compatible union cannot complete it.

The row explicitly retains qualified native sources' full-retention obligations and does not turn metadata brokers into custodians. It neither extends the existing finite contact/work allowances nor treats complementary partial observations as complete coverage before every required object is obtained. Its proposed future evidence now includes the precise multi-source success case as well as coverage gaps, authority changes and budget/deadline failures. No runtime result is claimed.

No remaining concrete finding was identified within this bounded organization, failure-grade and source-boundary scope at the repaired cut. This is scoped paper/source-review closure, not proof of the listed premises, native/runtime qualification, an exhaustive inherited-assumptions inventory or independent recertification of VIEWS1. Only this audit was edited during the rereview; frozen contracts remain unchanged by this reviewer.
