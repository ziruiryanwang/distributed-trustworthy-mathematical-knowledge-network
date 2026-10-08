# Supporting Evidence Profile v0 traceability matrix

This table maps each security property to its assumptions, mechanism, test, and residual limitation. A requirement is not satisfied merely because a mechanism exists.

| ID | Property | Principal assumptions | Mechanism/invariant | Evidence Profile v0 test | Residual risk |
|---|---|---|---|---|---|
| SEC-01 | Exact typed binding | Collision resistance; injective canonical profile; sound parser | Version/type domain-separated CID; COSE subject binding | Golden vectors, one-byte and typed mutation, differential fuzzing | Hash, codec, or parser-class failure |
| SEC-02 | Conditional local derivability | Sound checker and logic; exact resolved environment | Recipient replay; axiom/TCB report; fail closed | Clean-machine replay; invalid proof and altered statement tests | Kernel/compiler/hardware bug; unsound axioms; semantic mismatch |
| SEC-03 | Referential closure | Resolver follows only immutable references | Logical and proof dependency roots; no mutable names | Dependency substitution, missing blob, version drift, path confusion | Incomplete dependency extraction or unavailable archive |
| SEC-04 | Assertion authenticity | EUF-CMA signatures; correct identity/key binding | COSE signatures; issuer/verifier key epochs | Forgery, replay, wrong-predicate, wrong-subject, rotation tests | Key compromise; false but authentic assertion |
| SEC-05 | Append-only correction | Honest object retention or mirror | Immutable objects; signed challenge/supersede/withdraw events | Retraction and restoration across mirrors | Some operators may censor later correction events |
| SEC-06 | Fork accountability | Conflicting views eventually meet an honest monitor | SCITT/VDS receipts; stored checkpoints; gossip/cross-log | Deliberate split-view simulation and portable proof validation | Isolated permanent views remain undetected |
| SEC-07 | Rollback/freeze resistance | Client retains state; freshness source/policy | Monotone pinned checkpoints; explicit recovery epoch | Rollback, stale view, offline recovery tests | First contact and clock/freshness trust |
| SEC-08 | Typed epistemic integrity | Correct schema/UI implementation; evidence verifier | Separate dimensions and candidate/attested/certified status | UI/API invariant and bridge-evidence negative tests | Humans may still overinterpret labels |
| SEC-09 | Failure containment | Recorded dependency/attestation graph is complete | Reverse-dependency impact; policy recomputation; alternative proofs | Mutate high/low-level dependency; compare expected closure | Undeclared dynamic dependencies; expensive global recomputation |
| SEC-10 | Availability/exit | Declared replica threshold; at least one honest reachable mirror | OCI/CAS mirror, export, archive policy, optional erasure coding | Remove primary; restore from mirror; independent import | Hash/receipt without payload; widespread coercion or format loss |
| SEC-11 | Resource/abuse safety | Enforced isolation and accounting | Size/cost declarations; quotas; time/memory/network limits | Archive/build/proof bombs, recursive graph, high-rate submissions | Economic denial of service; curator centralization |
| SEC-12 | Governance safety | Enforced versioning and authority separation | Timelock, key epochs, forkability, old-profile support | Unauthorized upgrade, emergency rollback, old-object replay | Capture, fragmentation, ossification |
| SEC-13 | Confidentiality, later | Defined adversary and leakage budget; correct cryptography | AEAD, hiding commitments, threshold custody, precise ZK/MPC/PIR profile | Not an Evidence Profile v0 claim | Metadata/query leakage, fair exchange, endpoint compromise |

## Evidence-state trace

| Evidence dimension | Mechanical basis | What it establishes | What it does not establish |
|---|---|---|---|
| Formal derivability | Local kernel replay | Exact claim derives in exact declared environment, conditional on checker soundness | Informal meaning, axiom consistency, novelty, significance |
| Reproduction | Independent execution attestation | Another identified run obtained a stated result | Independent failure domains or mathematical truth by count |
| Provenance | Signed PROV-like assertions and measured events | Identified keys asserted or observed a process | Moral authorship, originality, causal completeness |
| Transparency | SCITT statement/receipt and VDS evidence | Identified assertion was registered in a particular service/history | Accuracy, completeness, global time, payload availability |
| Semantic alignment | Typed relation plus evidence | Exact proposed relation, context, translation, and evidence level | Universal semantic identity unless certified under stated theory |
| Novelty | Corpus-relative search report | No specified relation found by a procedure in a named snapshot | No one knew or proved it elsewhere |
| Availability | Mirror/archive checks | Object recoverable under a measured policy at a time | Future persistence without continued resources |
| Significance | Identified editorial/community assessment | A group made a judgment under a process | Objective or permanent importance |
