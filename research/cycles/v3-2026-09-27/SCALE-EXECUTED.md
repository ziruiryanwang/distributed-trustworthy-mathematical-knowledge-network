# Scale redesign: selected contract and actual evidence

Checkpoint: 2026-09-27, approximately20:13 America/Chicago. Goal remains active.
This page consolidates the latest evidence; historical source cuts stay frozen.

## The architectural change

The normal scalable object is an exact mathematical **interface plus a validity
certificate**, not its entire ancestral proof archive. Receiver acceptance and
new contribution must both respect that boundary:

1. Discover a candidate through an untrusted index. Retrieve its exact type,
   universe parameters, semantic/foundation/profile bindings and certificate.
2. Verify the certificate locally under an independently adopted verifier and
   assurance policy. Hashes/signatures or another node's success receipt alone
   do not establish mathematical validity.
3. Use sealed theorem interfaces and fetch only authenticated definitions
   required by the new computation. An old theorem's proof history stays sealed.
4. Check the new inference against these interfaces; recursively compose the
   immediate parent certificates into a certificate for the exact new result.
   The new prover must not require the parents' ancestors either.

Archival proofs, index availability, certificate validity and local usability
are separate states. No central server, global ledger or mandatory root task is
introduced. Every participant can be a prover; each receiver selects and checks
its own exact foundation/profile rather than trusting that participant.

For selected new work with k parents, the target resource dependence is on the
new proof/checking work, k bounded parent certificates and the definitions
actually consulted—not on all historical proof steps H. This does not promise
constant work for a gigantic statement or computation-relevant definition.
The general relation and compatibility obligations are in
[SCALE-DESIGN.md](SCALE-DESIGN.md). Its general Lean implementation is unfinished.

## Actual narrow implementation

The executable experiment implements EQ-DAG1: a finite equational calculus with
four variables, two uninterpreted binary symbols, term depth at most3, at most4
ordered context hypotheses and five inference rules. Its proposition is
`Valid Gamma q`, universally quantified over interpretations satisfying Gamma.
It does not assert that Gamma is true without assumptions.

The same repeated circuit verifies up to two independent immediate parent
certificates, checks their exact common profile/context and strict natural rank
descent, and checks one local mathematical rule. Fresh verifying processes read
only their adopted manifest/profile/verifier and one candidate. Fresh proving
processes read fixed setup assets, one local request and immediate parent
packets. Source inspection and exact application-read records establish this
dataflow; an OS-level filesystem sandbox is not claimed.

The completed finite campaign has9positive contributions,5fresh receiving checks,
8targeted receiver refusals and1invalid TRANS that reached the actual prover and
was refused during witness generation. No invalid certificate was returned in
that last control. Two certificates with different histories and exactly the
same378public fields have the same byte length. All failure evidence is retained.

| Measured item | Observation | Interpretation |
|---|---:|---|
| Each of9certificate packets |149,380bytes|Fixed selected representation, not evidence for unbounded expressiveness.|
| One cold receiver's application reads |152,526bytes in4files|No parent/proving assets or ancestral archive read.|
| Adopted verifier asset |1,905bytes|Not the complete receiver packet/implementation cost.|
| Inner ordinary+cyclic check |4.23–6.20ms over5calls|Excludes loading, decoding, process and supervisor overhead.|
| Inclusive receiver Job CPU |15.625–46.875ms|Coarse process accounting, not a statistical benchmark.|
| Nine producing processes |about5.1–5.6s supervised wall each|Producer work remains substantial; no native speedup inferred.|
| Reusable prover circuit |148,937,522bytes|Read by each fresh producer in this experiment.|
| Setup |24.59375workerCPU,16.3211wall seconds|First refinement stabilized, one helper proof.|

Setup, finite campaign and both native handoff attempts together consumed
116.296875known CPU seconds (workers plus measured controllers),82.4407214active
allocation wall seconds. This excludes prior compiler/backend/native preparation
and idle review intervals. Those costs remain in their own records; this is not
total engineering cost or an end-to-end useful-agent benchmark.

The native handoff initially failed with out-of-memory at4GiB. A separately
selected repair reused Lean's existing post-import environment, with explicit
trust level0 and the unchanged checker, instead of importing the same library
again. Same input bytes; no module rebuild, certificate regeneration or crypto
reverification. It passed at2.224GB peak private commit and1.931s wall. Original
failure remains failed, not overwritten. The source/evidence strongly supports
duplicate-import pressure but does not reconstruct the original allocation stack.

## What the Lean bridge does not establish

The actual native theorem is

    Valid Gamma Jlong -> Valid Gamma R0 -> Valid Gamma K.

It is kernel-checked with no reachable axioms and retains both premises.
Certificates give separate experimental computational assurance for those
premises; they do not become stock Lean proof terms. The Rust prover presently
accepts five-rule recipes, not arbitrary Lean proof terms. Checking this
conditional theorem does not by itself produce K's certificate from Lean code.

The finite relation's correspondence to the general Lean soundness theorem has
been source-reviewed, not mechanically verified. The selected Plonky2 backend
is deprecated; its approximately95/100-bit one-shot estimates do not establish
adequate adaptive-recursion security for a huge network. Consequently this is
**experimental scale-feasibility evidence, not a production trust mode**.

## Next central decision

Do not add networking or count more synthetic joins as mathematical growth.
The next integration must bind actual supported local mathematical checking to
certificate production and export. A typed finite-rule adapter is feasible but
must remain clearly restricted; it cannot close general Lean certification.
See [INTEGRATION-GAP](../../../experiments/certified-equation-interface-01/INTEGRATION-GAP.md)
and [NEXT-CENTRAL-GATE](../../../experiments/scale-equation-01/NEXT-CENTRAL-GATE.md).

Quicker knowledge growth is still unestablished. A credible later comparison
must include setup/proving/acquisition/reuse/export and use a strong direct
native or mathematical baseline, not force it to replay an inflated chain.
For costs Pn+Q*Vn versus Pc+Q*Vc, a receiver saving matters only when it
compensates for extra production/setup cost at the actual reuse volume Q.
Usefulness and independent agent behavior require additional evidence.

## Evidence navigation

- [Application source/relation review](../../../experiments/scale-equation-01/SOURCE-REVIEW.md)
- [Actual build](../../../experiments/scale-equation-01/BUILD-OUTCOME.md)
- [Actual setup](../../../experiments/scale-equation-01/SETUP-OUTCOME.md)
- [Actual certificate campaign](../../../experiments/scale-equation-01/CAMPAIGN-OUTCOME.md)
- [Preserved native failure](../../../experiments/certified-equation-interface-01/HANDOFF-OUTCOME.md)
- [Native repair contract](../../../experiments/certified-equation-interface-02/REPAIR-PLAN.md)
- [Native repair raw result](../../../experiments/certified-equation-interface-02/handoff-02/RESULT.json)
- [Independent native repair outcome](../../../experiments/certified-equation-interface-02/OUTCOME.md)

The independent repair outcome audit passes its stated narrow scope. No public
publication, external deployment, license selection or independently hosted
operation occurred. The delivered v2/native acceptance path remains unchanged.
