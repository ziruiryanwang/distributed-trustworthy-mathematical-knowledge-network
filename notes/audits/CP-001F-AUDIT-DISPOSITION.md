# CP-001F: integration findings and disposition

Date: 2026-09-20. Status: integrated paper/source audit disposition. This is not implementation assurance; final reviewed cuts and qualification boundaries are recorded in the independent audit notes.

## Scope and reviewers

The selected integration is [Operational corpus v3](../../spec/OPERATIONAL-CORPUS-V3.md). Three independently tasked collaborators examined source production/client use, decentralized discovery, and proof composition. They then cross-reviewed sibling mechanisms and root-owned migration/economics/integration notes. The root also independently read selected pinned Lean source and challenged the initial coarse-index design.

The independent review records are:

- [Migration and composition boundary audit](CP-001F-migration-cross-audit.md).
- [Base routing and economics audit](CP-001F-routing-economics-cross-audit.md).
- [V3 integration and exact routing audit](CP-001F-v3-integration-audit.md).

Reviewers' hashes identify actual review cuts. Subsequent repairs are recorded explicitly; the eventual checkpoint manifest binds final bytes. A full note read is distinguished from a source spot-check or a sibling's reported finding. No reviewer ran Lean, built a module, extracted artifacts, executed an exploit, simulated the network or benchmarked the proposed system.

## Concrete findings and selected repairs

| Finding | Evidence or countercase | Selected disposition |
|---|---|---|
| Incomplete public Lean evidence | Module theorem projections can be axiom-shaped; bodies may not have been imported, and the default body accessor omits theorem/opaque values | Explicit global-private full-data collector, complete matched artifact parts, completed records and full body access; no receiver trust in compiled imports |
| Compiler-assisted axiom bypass by name blacklist | Pinned native evaluation can create fresh axiom declarations | Inspect actual complete transitive kinds/axioms against the exact foundation inventory, not a historical forbidden-name list |
| Alias expansion has an avoidable large family | Distinct universe instantiations survive raw DAG sharing and give exponentially many nodes under the literal expansion recipe | Restricted checked opaque proof capsules preserve source polymorphic sharing; no universal proof-complexity or compatibility claim |
| C-BOUNDARY | A fixed external theorem and a new root can share a canonical JudgmentID despite different source names | Require complete retained witness-domain disjointness from exported wrapper judgments; re-plan under all guards or decline; independently reread |
| Uninformative fixed native hints | Fresh conversion checks on a transparent alias chain can repeatedly unfold both sides with equal regular-zero hints | HEIGHT1 derives checked dependency heights; NativeRules code 3/new FoundationID, including reconstructed ordinary bootstrap definitions |
| Connected but undiscoverable useful work | Bridge contacts can be permanently omitted by bounded ranked one-hop responses; uninterested peers do not relay theorem hints | Explicit paid iterative provider-rendezvous layer, finite routing tables, sharded expiring postings and reader traversal |
| R-STOP | The first responsive contact could satisfy the initial nearest-sixteen stopping wording | Require sixteen successes before distance-cutoff completion, otherwise explicit candidate exhaustion; settle relevant in-flight work |
| Coarse catalog is not efficient exact search | With indistinguishable providers and one unknown owner, q probes give q/P uniform success and P worst-case probes | Explicit finite FULL_EXACT target scope and actual fine-key memberships; coarse/structural coverage remains separately scoped |
| F-GROUP-COUNT | Partial/empty groups exceed chosen replica counts; a retired group and its replacement can coexist at one holder | Separate selected, active and total charged lifecycle state; no holder-count bound is applied to unreclaimed retired records; explicit total caps and supplied renewal/placement budgets |
| F-MEMBER-ROOT | Sources must compute expected before/after roots, but the first draft left the holder's map representation optional | Select exact canonical operational map type 0x8023/1, key domain, original-key-bearing leaves, first-differing-bit branches and typed child IDs |
| F-RENEW-PUBLIC | One eligible member could otherwise justify retaining unrelated withdrawn advertisements | Producer renewal guards cover the exact complete member root and relevant current disclosure/retention/incident state; dirty coverage requires revalidation or nondecision |
| Group row ownership and reclamation | Old-group garbage collection or base PUT/DROP could bypass the grouped row's root/version/ownership | Exact old-owner/row-generation deletion fences; base operations reject live group-owned rows; explicit drop/transition for same-holder scope replacement |
| Wire grammar seams | Imprecise contact shapes, status labels or capability direction can yield noninteroperable interpretations | Fixed route/ad contact arrays, reciprocal unchanged HELLO exchanges, allocated capabilities/operations/map types, bounded page/result shapes and numeric subreasons under existing NET result codes |
| M-CACHE | Identical source bytes/witnesses can be translated differently under different capsule/background boundaries | Bind exact TranslationContextID or qualify deterministic independence; candidate cache is not target acceptance; independently reread |
| E-LOAD | Equal deterministic arrivals and service can keep a queue stable | Necessary average balance uses no-greater-than; strict slack is a qualified robust design margin |
| E-RENEW | Group leases can amortize per-record renewal work | Limit rA/tau formula to individual-record leases; charge the actual selected group/membership representation |
| R-AVERAGE | Mean shard occupancy below capacity does not logically force an overflowing shard | State that imbalance can require deeper placement, not that it must; maximum-load assurance is not inferred from an average |

The original tiny same-statement alias cycle was already documented in CP-001D. This checkpoint does not misrepresent its rediscovery as new work. New contributions are the cost-qualified expansion family, explicit restricted capsule recipe and repaired canonical-background guard, together with the separate source-backed hint issue.

## Independently checked source facts

The producer investigation read the relevant pinned Lean module visibility, serialization/import, asynchronous completion, body-access, String and native-evaluation source paths, with immutable URLs in its [note](../analyses/CP-001F-lean-producer-client-path.md). Limited pinned mathlib native-linter evidence is not a global compatibility measurement.

The composition investigator read the actual lazy-delta hint comparison, checked insertion path, universe parameter/arity checks and polymorphic singleton definition. It distinguished a concrete conversion-step family from wall-clock performance and confirmed that unused declared universe parameters do not invalidate its paper family merely by being absent from the theorem type.

The root independently reread the pinned source portions `AddDecl.lean:113–127`, `Environment.lean:1858–1872`, `2180–2182`, `2433–2448`, `Meta/Native.lean:31–87`, `Declaration.lean:17–40`, `kernel/type_checker.cpp:1026–1047` and `kernel/environment.cpp:192–222`. These confirm the public/full-evidence distinction, actual native axiom generation, lazy unfolding branch, and fresh checked insertion. They are not a complete kernel audit.

The routing author inspected immutable libp2p Kademlia and IPNI specification revisions as engineering precedents. Other reviewers did not claim independent reproduction of that source investigation. The chosen local accounting, exact mathematical keys and native truth boundary are this project's own specified adaptations.

## Claims deliberately not made

- A checked transformed target is not automatically semantically equivalent to its old-foundation source.
- A scoped routing receipt is not guaranteed present remote storage, public current knowledge, a global nearest-node proof, or a native theorem verdict.
- Four authenticated replicas are not four established independent failure domains.
- A finite exact-index scope does not cover an arbitrarily large library or solve unknown-lemma relevance.
- Restricted capsules do not prove universal inexpensive joining of proof-dependent nominal contexts.
- Native source review and corrected foundation selection do not supply a tested bootstrap, adapter or executable image.
- Counted queues and safe refusal do not by themselves demonstrate useful autonomous accumulation.
- New IDs produced by wrappers or foundation re-expression are not automatically new mathematical insights.

These are not excuses to leave a discovered concrete contradiction unresolved. The table above separates repaired defects from real restricted scope and still-required evidence.

## Remaining substantive work

The main adequacy questions are practical full-evidence export and content-renamed replay over broad Lean developments; affordable composition beyond the proven eligible capsule slice; structural candidate recall when exact judgment IDs are not known; sustainable fine-index/custody/migration resource supply; and end-to-end checked reuse under realistic diversity, growth and faults.

The concept now specifies more of the path and the conditions under which it works. Those remaining questions are not all mathematical impossibility claims, nor are they solved by a larger collection of qualification checkboxes. They require further targeted design/source analysis and, only when authorized, actual implementation and qualification. The goal remains active.

## Preservation and verification

Frozen CP-001/1A, CP-001C, CP-001D and CP-001E manifests were independently checked during this work: respectively 18, 11, 15 and 18 rows match their stored lengths and SHA-256 values. No frozen file was edited.

Final checkpoint verification must also check all new files' strict UTF-8 decoding, local Markdown links, balanced code fences and mathematical delimiters, and exact final manifest rows. These are document-integrity checks only, not protocol executions or evidence that every unknown defect has been excluded.
