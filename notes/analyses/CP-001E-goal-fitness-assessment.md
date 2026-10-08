# CP-001E: goal-fitness assessment beyond a safe small prototype

Date: 2026-09-19  
Status: Ongoing concept amendment; CP-001D remains frozen

The previous turn was progress: it produced a new detailed specification, adversarial reviews, and an integrity-checked checkpoint. That does not prove the ultimate goal achieved. This turn tests the design against efficient reciprocal accumulation by a very large, diverse, indefinitely operating network, rather than treating safe refusal of difficult workloads as sufficient success.

## Requirements and authoritative evidence

The user's requirements are interpreted at their original scope. This table distinguishes design evidence from production evidence instead of weakening the requested outcome to what already exists.

| Requirement | Current evidence | Assessment and next action |
|---|---|---|
| Independently check contributions before relying on them | CP-001D specifies exact native Lean data, but its old kernel pin contains subsequently fixed soundness defects | Old pin withdrawn from deployment candidacy; corrected Lean 4.34.0 foundation selected for fresh qualification in the security audit |
| Local investigators can both reuse and contribute | Explicit local-client path and a nontrivial three-generation mathematical paper chain | Paper-level path exists; real library ergonomics and repeated-use cost are not established |
| No central theorem server or mandatory root goals | Direct peers, offline archives, independent local authority; no corpus research scheduler | Selected architecture supports this; discovery still requires actual contacts and supplied service |
| No human-intention layer or unsolved-mathematics registry | Corpus records actual statements/evidence; investigators choose privately | Preserved scope; optional formal expression retrieval must remain ephemeral service, not a task registry |
| Very large and diverse agent population | Bounded directories, local indexes and full selected closures | Resource safety alone is insufficient; repeated-list, transfer and search-prefix bottlenecks require amendments |
| Efficient meaningful accumulation | Bounded proof alternatives, local usage observations, cost diagnostics and exploration | Defensible heuristics, not demonstrated useful-growth performance; ranking cannot recover undiscovered candidates |
| Autonomous long-term preservation | Local maintenance, pins, replicas, exact archives and renewable local policy | Requires actual durable custodianship and supplied capacity; warm-cache-only deployments can lose everything |
| Formal rigor without requiring every heuristic to be optimal | Conditional arguments and explicit empirical gates | Correct separation; neither zero findings nor a source API proves implementation correctness |
| Markdown checkpoints and subagent audits | Frozen CP-001D manifest and recorded cross-reviews | Satisfied for that checkpoint; new amendments require their own integration and review |
| No implementation yet | New work consists of Markdown and read-only source inspection | Preserved; no generated prototype or executable conformance result is claimed |

## Confirmed design countercases

### Repeated transitive metadata

CP-001D explicitly serializes a judgment's transitive semantic-reference set and a replay's transitive declaration/witness lists. Across a growing chain of individually small results, retaining each prefix can repeat a quadratic number of references. Hashing whole flat lists does not automatically share their common internal contents.

This is avoidable representation overhead, not a theorem that Lean proof checking inherently needs quadratic work. A proposed amendment must also avoid recomputing every old declaration under a fresh global replay key; smaller serialized lists alone do not establish efficient warm reuse.

The [native scaling analysis](CP-001E-native-scaling.md) owns exact families, the selected representation, incremental cache authority, and migration rules.

### The default transfer envelope can reject an ordinary small-byte closure

Take 16384 missing objects of 2 KiB each: 32 MiB payload, within CP-001D's default object-count and total-byte limits. If each needs one manifest call and one chunk call, there are 32768 paid service calls.

The provider's 32-offers/second default, even with a full burst of 64, gives a lower bound

\[
(32768-64)/32=1022\ \text{seconds}.
\]

Two inbound control frames per paid call under the 64-frames/second default give the same order of bound. At 100 ms round-trip latency, two round trips per call and four concurrent calls give a concurrency lower bound of approximately

\[
32768\cdot 2\cdot0.1/4=1638.4\ \text{seconds}.
\]

Both exceed the 900-second default transfer allowance. For comparison, 32 MiB divided by the sustained 8-MiB/second application rate is four seconds; this is not the strict token-bucket lower bound. With a full initial 16-MiB burst, the payload envelope alone gives only \((32-16)/8=2\) seconds. Neither calculation includes metadata, link latency, checking, or other bottlenecks. These are conditional arithmetic bounds/estimates for that explicit trace, not measured throughput. Local shared chunks, fewer missing objects, larger allowances, or different service policy can change the trace.

The point is still material: default safety limits do not by themselves yield an efficient working path for many small mathematical objects. A bounded bundled-transfer amendment must reduce paid per-object round trips without weakening disclosure, accounting, crash handling, or full-object identity checks. The [exchange scaling analysis](CP-001E-exchange-scaling.md) owns that amendment.

### Safe pagination can systematically hide reusable mathematics

At the NET1 hard maximum of 262144 retained roots, a broad all-match posting list needs 4096 pages of 64 results. Two sequential round trips per page at 50 ms already imply about 409.6 seconds, exceeding the default 120-second cursor lifetime. Even the 16384-root default requires 256 pages, approximately 25.6 seconds in this idealized round-trip calculation.

Restarting every timed-out scan from the beginning can repeatedly expose the same prefix. A client-side learned ranker cannot retrieve candidates that never reach it. More selective formal indexes, bounded diversified seeks/samples, and plural source routing are operational needs, not guarantees of universal mathematical relevance.

The [agent reuse analysis](CP-001E-agent-reuse-and-discovery.md) owns a formal-client baseline and its expressly versioned optional query extensions.

### Global freshness can defeat unrelated warm reuse

If a status evaluation requires an unchanged global reliance epoch for duration T, unrelated commits can force repeated retries. Under an illustrative Poisson model with commit rate \(\lambda\), the no-change probability is \(e^{-\lambda T}\); fresh idealized attempts require \(e^{\lambda T}\) trials on average. At \(\lambda=100\) per second and T=0.05 seconds this is approximately 148.4 trials.

This is a model countercase, not a measured workload. It motivates retaining the global epoch as an observation label while validating exact relevant evidence/policy/protection guards at the final local transaction. Broad unknown incidents must still fail closed. A relevance optimization may not turn an old snapshot into a current observation by relabeling it.

### Correctness plus expiry is not durable growth

An honest network can check every new result and later expire every copy. Fixed finite redundancy likewise does not prove indefinite survival under stationary nonzero loss hazards.

The [preservation analysis](CP-001E-preservation-over-unbounded-time.md) derives those limitations and selects explicit locally funded collection custodianship, with scoped maintenance and handoff conditions. This is a prerequisite for a deployment's durable-accumulation claim, not a new global mathematical authority.

## Existing library evidence changes the qualification target

Read-only official source inspection found a mathlib release exactly matching Lean v4.22.0, at commit 79e94a093aff4a60fb1b1f92d9681e407124c2ca. Its complete repository-tree response contains 6726 Mathlib Lean source blobs totaling 77,230,502 source bytes.

The [source evidence note](CP-001E-source-scale-evidence.md) records the immutable references, filters, and limits of this observation. Source bytes are not native closure bytes; no cap violation or replay performance was inferred.

The next release qualification should therefore use actual exact library slices, not merely claim that a compatible library might someday exist. Source tactic imports and elaborator conveniences do not become receiver-side executable dependencies.

## Amendment boundaries

CP-001E must say which changes:

- preserve mathematical object identity and only change service policy;
- introduce a new transport operation without changing native meaning;
- change canonical mathematical representation and therefore require new schema-bound IDs;
- remain optional external-client heuristics;
- require new locally authorized preservation commitments.

A limit increase must not silently weaken logical rules. Conversely, a pure CPU/byte allowance change should not needlessly rename all mathematics. Unsupported profile transitions remain explicit. Frozen CP-001D objects and observations retain their original interpretation.

## Completion status

These countercases contradict any claim that CP-001D alone has already established efficient goal-scale operation. Separately, the [foundation-security audit](CP-001E-foundation-security-audit.md) establishes that its historical Lean pin is unsuitable as the selected deployment candidate. The architectural boundary of independently checking inert evidence remains appropriate, but it requires a corrected checker and fresh qualification, not a disclaimer that the known-vulnerable checker is assumed sound. The proper next action is to integrate those repairs and adversarially review the amended paths.

The project remains at concept/specification stage. No implementation is started, and the ultimate goal is not marked complete.
