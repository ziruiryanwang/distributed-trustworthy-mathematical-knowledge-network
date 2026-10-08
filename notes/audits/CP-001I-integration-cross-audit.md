# CP-001I independent integration cross-audit

Date: 2026-09-20. Scope: the proposed V6 selection boundary, precedence, authority composition and evidence claims. The reviewer is independent of the V6 integration author. This is a source-reading and paper-contract audit; no implementation, build, test, executable model, Lean run, extraction or benchmark was performed. No author note, completed module audit or frozen H/earlier file was edited.

## Reviewed cuts

Read [V6](../../spec/OPERATIONAL-CORPUS-V6.md) and the frozen [V5 integration](../../spec/OPERATIONAL-CORPUS-V5.md) in full. Compared V6 against the exact I source contracts and the completed protocol/lifecycle review, and read the repaired local retry policy. The economics comparison is limited to the selected small fixture and its timing/count conditions; this audit does not independently requalify the unrelated larger economic cases. Earlier client/economics audits were inspected for their declared source cuts and dispositions, not treated as reviews of later changes.

| Source | Reviewed SHA-256 |
|---|---|
| `spec/OPERATIONAL-CORPUS-V6.md` | `09DBFA2AED311C8C2192CEB888269E35AC14E83BC68F328E40B5266C38768A7D` |
| `spec/OPERATIONAL-CORPUS-V5.md` | `6C1E723492779ED7238731D5D7D2849D6E6DBFE3F2052DCDD6C68D99F13231B0` |
| `notes/analyses/CP-001I-candidate-service-trust-boundary.md` | `497C105A3EFD4502A8D7107489E8CDB78DC37D0696451C1E4040E3952D88E62F` |
| `notes/analyses/CP-001I-untrusted-search-brokers.md` | `2A404FAE9F79FE7ED40D1430CAF8AB0B0738CE35F53F340A4BA490C2ECB83C1F` |
| `notes/analyses/CP-001I-direct-broker-bindings.md` | `2CE9222631ED95AE0CE7B31C875AA4CD72EA5D0440B7BC1A8E34FB84D7F2EFB2` |
| `notes/analyses/CP-001I-broker-local-retry-policy.md` | `7E859F189A498090D054D5411136FA5569C8F86FCC036B69F6AFFC98615FAABB` |
| `notes/analyses/CP-001I-broker-economics-and-availability.md` | `0E3AFB634128694DC5B5160954BF0EE73BA445E8CC2110F86EFA961DDF092DE2` |
| `research/modules/direct-broker/audits/protocol-audit.md` | `E0539E27BB38AFE341CE1DF0775ABD5D66791F4A9EEE50D4321C47CBEE03CEDE` |
| `research/modules/broker-retry/audits/retry-audit.md` | `71851BF73EAF3847EB9C504D295389B10CA056E957429D308932BADA7B44966A` |

## Selection and precedence

No blocking selection contradiction was found. V6 explicitly selects the known-contact direct subset of BROKER1 and gives the exact direct-binding note precedence over its symbolic/flattened sketches. Thus the symbolic BROKER_FIND form does not compete with the concrete predicate object and ServiceCall arrays. Capability 9, types `0x8125/1` through `0x8128/1`, operations 21 through 23, the token wrapper, value comparison and snapshot retirement all come from one exact selected contract.

The integration expressly leaves broker DHT keys, advertisements, grouped routing and unfamiliar-broker discovery unselected. BROKER1's broad final all-lanes gate is not silently satisfied or used to import those incomplete mechanisms: V6 narrows the selected module and records that choice. Existing native routing remains available under its own unchanged role requirements.

H's qualified native index provider still needs its actual checked, retained and authorized evidence. A metadata-only broker does not acquire that role, advertise native eligibility, open a native read scope or acquire custody merely by copying descriptors. V5's NativeRules code 4/HEIGHT1, exact FoundationID commitments, reconstruction, axiom restrictions, source interpretation, retention and current-use conditions remain intact. The separately negotiated organizational service changes no mathematical schema or foundation commitment.

No central broker, global goal, intention test, political attribution condition, network research assignment or compulsory background retry is introduced. Owner-local research choice remains distinct from remotely disclosed query information.

## Composition of the selected claims

| Seam | Integration result |
|---|---|
| Listing versus evidence | The five observed-event stages keep metadata listing, scoped exact reads, complete acquisition, reusable checked evidence and checked application/contribution distinct. None is silently promoted into the next. |
| Descriptor and source authority | Candidate identity remains exact descriptor `d`; lead edits preserve it, and leads visibly bind the same R. Capability 9 does not supply native 3+7+8 collection support, foundation adoption, source export authority or generic CAS access. |
| Mutation and withdrawal | V6 preserves one authority-writer comparison/no-op/change/acknowledgment transaction. It explicitly selects value-CAS and permits ABA, rather than claiming a stronger revocation fence. Quiescent withdrawal depends on settling restoring intents. |
| Search progress | The shortest-token posting, immutable authorized roots and inclusive unprocessed boundary preserve the reviewed non-skipping prefix argument. END concerns only the local posting above the original boundary, under an honest broker; it supplies neither Byzantine completeness nor global absence. |
| Snapshot and delivery lifetimes | Reserved slots and retiring roots count until actual release. END closes scan claims; incomplete or orphan snapshots can last to expiry. A separately authorized immutable reply can survive ordinary query retirement. The exact direct note controls disclosure and admission-seal cancellation. |
| Retry identity and work | Observation identity is distinct from the stable retry obligation. TRY_ONE remains a planner ticket consumed by one dispatcher, exact settlement is idempotent, and cache eviction cannot erase spending or fences. Broker errors do not become native-source failures merely because the roles share a NodeID. |
| Retry progress limits | At most 32 visits, 128 lead inspections, 32 reserved trials, one trial in flight and eight existing calls per tranche remain subordinate to parent resources and horizons. One-hour cooldown and fixed-lead circular-selection claims do not become scheduled work, wall-time fairness or eventual source recovery. |
| Safety claim | The arbitrary-transcript claim preserves the implication from each completed native acceptance. It does not assert equality of accepted sets, relevance, availability or unchanged investigator outcomes. |
| Reciprocal contribution | The path retains actual evidence, compatible checking/application and independently funded publication/custody premises. A successful lookup or application does not automatically publish another artifact. |

The optional local retry mechanism is available to an already admitted investigator. It is not an amendment to the wire protocol or a remote request to create new investigation authority. The surrounding parent-resource requirement prevents the broker stage and each eight-call native tranche from obtaining independent free copies of one budget.

## Timing, counts and economic grade

V6's small fixture is no stronger than the repaired sources. It preserves spaced reservation starts, the at-most-66-second complete slot residence, the selected at-most-60-second created-snapshot lifetime, the absence of preexisting/unrelated slot users and the need to qualify actual timing and resources. The occupancy conclusion is `ceil(66 / 8.64) = 8`; it does not assume that any page reaches END or its caller. The defeating 600-second case correctly remains 1152 starts/day with eight slots.

The numerical summary matches the reviewed small-fixture calculation: 10000 new queries, no continuations, 192 publication submissions for two source leads per 96 new targets, and 400 additional paid mutation executions total 10592, below 20000. The corresponding broker CPU is 3192 seconds within 3600, and the stated traffic is 10.76708984375 GiB within 16 GiB. Unused execution-count headroom does not promise extra queries, continuations or resource supply. No close operation is assumed.

The 18-GiB native-stock difference is conditional on the attained 4096-target endpoint and actual shared-core/increment assumptions. V6 identifies it as avoided discretionary canonical native stock, not net fleet storage or authority to delete promised custody. Eight metadata/search copies do not become eight evidence sources. The large ungrouped-routing stress case is a defeating extrapolation, not an implicitly selected high-capacity deployment.

### I-INT-001: minor mutation-count wording precision

At the initial reviewed V6 cut, the phrase “at most400 further paid mutations/failures” is less precise than the economics source. The 400 allowance is for additional mutation executions, including failed/conflicting mutations and mutation retries. Failed new queries are already inside the 10000 new-query bound; the fixture does not fund 400 extra query retries or their snapshot reservations through this category.

Requested wording: “at most 400 further paid mutation executions, including failed/conflicting mutations and mutation retries.” This is a summary precision, not an independently discovered protocol defect or a blocking contradiction under V6's explicit exact-source precedence. It should be resolved in the final integration text to avoid implying a broader workload.

## Evidence and disposition

V6 correctly distinguishes the earlier client/economics reviews from the later exact direct-service and retry audits. In particular, the earlier economics audit reviewed `F5E82...`; the amended snapshot timing and operation-count conditions are covered by the completed direct protocol review at the later economics cut, not falsely attributed to the earlier audit. Historical proposal wording in those older reviews does not itself allocate or select a wire profile.

The document remains an integration candidate until the root's explicit selection process. Its statements do not pretend that candidate numeric allocations have already been deployed. It expressly leaves implementation, executed native reconstruction, extraction, actual queue/memory behavior, useful yield, throughput and broad library interoperability unperformed. The active overall project goal is not marked complete by this checkpoint.

At the reviewed cuts, no blocking conceptual contradiction was found in the proposed selection or composition. I-INT-001 records the one minor summary clarification requested. This audit supports selection only at the bounded paper-contract grade stated by the sources, not a deployment, performance or universal useful-growth claim.

## Exact-cut closure

Independently reread the complete revised V6 integration candidate at SHA-256 `6943AB0F8C06F907663F58D856FD1D7DC4F7CE1E76DD5AD7766D7C25AF6556C2`. The exact underlying I contracts and completed module audits remain the cuts listed above.

I-INT-001 is closed. The integration now explicitly includes failed new queries inside the 10000 new-query count and describes the separate 400 allowance as paid mutation executions, including failed/conflicting mutations and mutation retries. The revised summary neither adds query attempts nor changes the audited operation, CPU, traffic or snapshot occupancy accounting. The accompanying typography changes do not change selection or authority.

No unresolved finding from this bounded integration review remains at this exact candidate cut. The known-contact subset, explicit direct-binding precedence, exclusion of broker routing, preservation of H native/foundation obligations, optional local retry, conditional capacity claims and distinction between reviewed paper contracts and unperformed execution are coherent.

This closure concerns the reviewed integration candidate. Later editorial selection headers, checkpoint/disposition links or manifests must identify their actual delta and final bytes; the hash above does not purport to cover uninspected future changes. Any substantive change in the selected contracts or claims needs a new bounded review.

## Final selected-cut closure

Read the final selected V6 in full at SHA-256 `95FC34057FB5E00D9F453287F396BC935FBA9BEE9EC5F4B5FE24404125F2B5A2`, the [audit disposition](CP-001I-AUDIT-DISPOSITION.md) at `E95FFB32A495F90E7B87DD62347863D014EB457EA01A9B4480D6B9AD37C85D69`, and the [checkpoint](../checkpoints/CP-001I-candidate-only-discovery.md) at `6F33AB4405601881CCDEA40FCBEF0BA53616FB5C4B1CF1AD7123083D480F2C4E`.

A non-mutating text/digest check reversed exactly the four selection passages enumerated in the disposition. The reconstructed bytes hashed to the independently reviewed candidate `6943AB0F8C06F907663F58D856FD1D7DC4F7CE1E76DD5AD7766D7C25AF6556C2`. This verifies that the final V6 delta is confined to the stated opening status/links, explicit optional selection wording, table heading and final closure/historical-header paragraph. No grammar, mechanism, resource premise or quantitative claim changed.

The disposition accurately records the repaired source cuts and the different scopes of the earlier economics review, later independently reviewed temporal/count repair, protocol review, retry review and integration review. It does not convert authoring or a historical review into independent approval of an unreviewed amendment. The checkpoint retains the conditional capacity and native-stock premises, the unchanged native trust/custody boundary, and the absence of executed qualification or a completed overall project goal.

The next query-view investigation is expressly outside this selected I scope. This review does not certify that new mechanism or independently re-audit the separately summarized reciprocal paper example. Pending manifest links are references to the root's subsequent integrity-freeze step; this audit does not claim that the manifest already exists or that its final file set has been verified.

No blocking contradiction or unresolved finding from this bounded integration review remains at these final selected cuts. Selection is supported at the declared concept/paper-contract grade only; actual execution, native interoperability, timing, memory, useful yield and growth remain unperformed qualification work.
