# CP-001E: V2 mathematics, foundation, and identity audit

Date: 2026-09-20. Status: independent bounded paper audit; no implementation, bootstrap extraction, build, replay, or exploit execution. No frozen CP-001D artifact was edited.

## Reviewed revisions and scope

- [Integrated V2 specification](../../spec/OPERATIONAL-CORPUS-V2.md), initial full read: SHA-256 `A7FD9EB3BF55D46CAF1EDF10F986099BF7BA7F7F0D1867BD4C441139BC893A09`; repaired revision read in full: `4A55F9BFB5698E1E0116AD127999CBB424EE672A62144CD8E3B64F91118862E4`.
- [Native scaling amendment](../analyses/CP-001E-native-scaling.md), identity/representation, width, replay, cache/environment, incident and migration sections: `2CDFD32A0282E6100C15DB1233FB163F0966CA520A3B5A4EF370C24A606BC537`.
- [Foundation security note](../analyses/CP-001E-foundation-security-audit.md), including qualification and new-source migration: `C7393FBF236A2C4DDE41E32597B6733D9D4B04481B1F8BF46CC11D7B542EDFE7`.
- Frozen mathematical contract, targeted inherited SeedProfile, term/group/opaque shapes, generated names, Module and NativeRefutation behavior. The earlier [source cross-audit](CP-001E-foundation-cross-audit.md) supplies the independently inspected source evidence and its limitations.

This audit covers mathematical identity, typed-schema incompatibility, foundation-authority boundaries, witness closure, and native-check cache inheritance. It is not a fresh exhaustive audit of NET2 allocation/concurrency, discovery extraction, or custody transitions.

## Registry separation

The V2 registry consistently assigns schema 2 to the changed foundation and to every contributed mathematical object family: terms, definitions, groups, opaques, contexts, judgments, proofs, replays, modules, and opposing-evidence records. Frozen schema-1 payloads retain their old interpretation. Typed content addressing commits to both the type and schema, so equal payload bytes under different schemas do not denote the same ContentID absent a content-binding failure.

SeedProfile remains `0x0002/1` because its self-contained descriptor grammar is retained. Its actual new source commit and descriptor/export bytes change its identity. NativeRules and ReservedNames occupy new types `0x0003/1` and `0x0004/1`; the two trie types are also new. Thus the surviving schema-1 allocations are not implicit permission to import old theorem/term/definition records.

The explicit V2 rule disabling mixed legacy mathematical closures overrides the native-scaling note's possible qualified same-foundation reader extension. This is a genuine initial-profile restriction, not an unresolved choice left to an implementation. A new term cannot name an old schema-1 definition merely because its printed type or content digest looks familiar. Native references must be checked as full typed IDs and under the same FoundationID, including refs in inline group DAGs and trie leaves; those are ordinary consequences of the V2 registry and closure rules.

An empty reference/witness trie can have the same ContentID across different foundations because it contains no native meaning. This sharing is safe only because its containing SemanticContext/Replay binds the exact FoundationID and every nonempty native reference receives the schema/foundation checks. A shared syntactic trie node is not a cross-foundation checking certificate.

## No foundation hash cycle or peer-controlled adoption

The dependency order is acyclic: SeedProfile contains its source/inline bootstrap descriptors without a FoundationID; NativeRules contains fixed rules/features/axiom paths; ReservedNames names SeedProfile; Foundation then commits to all three. Bootstrap-local names do not name the not-yet-created FoundationID. Group-local recursive references likewise retain their bounded local indexes, not recursive content-address preimages.

The new interpretation artifacts describe a locally qualified foundation. Receipt of a well-hashed NativeRules or ReservedNames object is not activation authority. In particular, a peer cannot add an axiom name, remap a primitive, remove a forbidden native name, select a different seed signature, or install an old checker by submitting a newly hashed table. It produces a different, unsupported foundation until a separate explicit local qualification/adoption process exists. The first candidate remains the particular source and practical feature set selected in the root security note.

Names of the three allowed axioms alone are not their mathematical signatures. Their exact seed descriptors, source binding, native reconstruction rules, and local qualification provide the necessary signatures and behavior. Likewise, `String.ofList` is a source-specific bootstrap obligation, not permission to treat any declaration bearing that text as the primitive.

The actual new bootstrap and interpretation byte inventories have not been instantiated. V2 states this rather than assigning invented digest values or claiming the candidate is already ACTIVE. That is consistent with a concept-only artifact.

## Meaning versus selected evidence

The direct reference set is recomputed solely from telescope/conclusion syntax; proof-only dependencies remain in the selected replay, not statement identity. Typed group member selectors and universe instantiations remain committed in the statement terms. The direct set's smaller footprint therefore does not forget which native member/application was asserted.

Replay fixes one proof per needed judgment, including its own proof root where applicable. Complete traversal derives the expected witness map and declarations; equality against the submitted canonical map forbids both omitted and extra choices. Cycles are rejected before unsupported environment insertion. Bound native recursion within one checked inductive group remains distinct from a cross-object theorem-support cycle.

The V2 Module and same-context opposing-evidence records use their inherited practical shapes with the new IDs. No new replay root type or remote authority is created for NativeRefutation. It remains a locally derived checked relation attached to a negative proof replay, not a proof of underivability or an unconditional assertion that a conditional positive theorem is false.

## No old acceptance or mismatched-witness inheritance

The reviewed V2 contract explicitly prohibits old acceptance-cache inheritance across foundation source changes. Successful checking must bind the exact typed root, witness map, FoundationID, checker image, adapter, interpretation, ABI and semantic options. Storing the same bytes on disk or selecting a larger resource budget supplies none of those missing checks.

The inherited native amendment also prevents a subtler mismatch: an actual native environment containing theorem witness A cannot be described as the replay selecting B solely because A and B prove the same JudgmentID. The selected baseline reconstructs or branches an environment compatible with the exact witness choice. Child certificates must have compatible full witness maps; conflicting assignments cannot be silently unioned.

The distinction between historical native acceptance and current reliance remains explicit. Recovered identical bytes can restore availability if the old checking basis is still locally trusted. A checker/foundation incident instead blocks current reliance until the affected qualification and evidence are re-established. Full incident support includes representation trie/context/replay objects as well as declarations. A stale or foreign positive flag is not a local certificate.

Consequently, no direct route from “old checked object,” “peer-supplied rule table,” or “same theorem statement under another proof selection” to V2 ACCEPT was identified in the reviewed contract. This is a paper interface finding, not a proof that a future implementation cannot contain such a route.

## Conformance clarifications: repaired and reread

The local qualification rule already prevents peers from choosing inconsistent profiles. For a more mechanically checkable registry, the reviewer nevertheless requested these explicit cross-record assertions from the owner:

- `Foundation.kernelSourceCommit = SeedProfile.sourceCommit`.
- `ReservedNames.SeedProfileID = Foundation.SeedProfileID`.
- NativeRules' family agrees with Foundation's family, and its selected rule code, feature vector, and allowed-axiom name paths have one specified exact canonical representation/order.
- Typed-reference validation is applied inside set/map leaves and inline native descriptors, not just top-level records.

These clarify derivation/validation of local release artifacts and prevent misleading composite descriptors. No exploitable peer-authority bypass was demonstrated from their abbreviated original wording.

The owner added the first three assertions explicitly. The reviewer reread the revised registry: source-commit equality, exact SeedProfileID equality, native-family equality, canonical sorted duplicate-free features/axiom paths, and agreement of the exact permitted seed axiom declarations/types are now requirements. The fixed family/rule code/features and inherited exact axiom schemes remain bound by the locally selected reconstruction contract; checking familiar names alone is explicitly insufficient. The fourth item is enforced by the existing all-reference schema/foundation rule together with the inherited inline-descriptor and trie-leaf type checks; it is not an exception left to a top-level-only implementation. No clarification remains pending within this audit scope.

The same full reread checked adjacent schema changes for mathematical-boundary conflicts. The NET2 schema bump now explicitly applies only to reused NET1 types; newly allocated export/advisory types retain their declared schema 1. Raw chunks/manifests remain byte objects, not executable or mathematical authority. The export starting-point bytes require exact CID/type checks rather than trusting a root hint. Advisory pages now require exact FoundationID agreement for all resolved mathematical targets/interfaces/replay hints, and narrow structure/rewrite activation to checked native cases. None enables mixed legacy native closures or imports an old acceptance certificate. Detailed transport accounting and client-operation completeness remain with their separate reviewers.

## Disposition

No unresolved contradiction was identified in the reviewed mathematical schema/foundation/cache boundary. The broad schema bump and initial prohibition of mixed legacy closures are coherent. The conformance clarifications above are repaired and reread at the final reviewed specification hash. Still-unperformed practical qualification includes actual bootstrap derivation, adapter correspondence, exact generated native inventory, axiom footprint, compiled-image/runtime behavior, representative library replay, adversarial native inputs, and cache/recovery execution.

This audit does not qualify a deployable image, complete a kernel-soundness proof, or establish that the selected source has no unknown defects. It supports the conceptual separation necessary for reliable decentralized reuse without author reputation or a consensus ledger deciding mathematical truth.
