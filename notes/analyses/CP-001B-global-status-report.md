# CP-001B source analysis: global-status semantics

| Field | Value |
|---|---|
| Date | 2026-08-28 |
| Role | Independent distributed-status analysis |
| Mode | Read-only analysis; no repository edits |
| Used by | `CP-001B` |

## Conclusion

No decentralized node can possess the instantaneous status of an open, continuously changing network. DTMKN should define **receiver-local, query-relative status at a named scoped frontier**, plus conditional eventual discovery.

For an exact unsigned judgment \(x\), raw evidence state is

\[
\operatorname{state}_{P_i}(x)=
\left(
\mathbf 1[(\textsf{SUPPORTS},x)\in K_{P_i}],
\mathbf 1[(\textsf{REFUTES},x)\in K_{P_i}]
\right).
\]

This yields neither, support only, refutation only, or both. A separate exact `RelianceQuery` is accepted only through \(\operatorname{Stable}_{P_i}(q;A_i,O_i)\). Validation outcome, strict reliance, availability, and freshness are orthogonal dimensions.

## Frontier result

A frontier must bind a named authenticated shard/membership configuration, exact key/subscription predicate, and authenticated checkpoint/cursor for each relevant shard. “Processed through the frontier” can mean only that every committed record in mechanically enumerable declared coverage has been verified and applied. It does not cover:

- events after the checkpoint;
- omitted or uncommitted facts;
- cells/shards outside scope;
- private or withheld results;
- semantic relations that no complete mechanical predicate recognizes;
- present availability of referenced payloads.

Merkle roots commit to records under a root. They do not prove publication completeness, theorem truth, causal consistency of an arbitrary checkpoint vector, or data availability.

## Convergence result

Separate:

1. same-authority crash-fault immutable-fact convergence;
2. same-authority deterministic materialized-view convergence when facts, closures, schemas, evaluator/checker results, policy, overrides, and freshness epoch agree;
3. inter-cell candidate discovery, after which independent cells may legitimately disagree.

Conditional discovery additionally assumes a correct fair non-omitting home, reconstructible responsive providers, eventual message delivery, stable configuration or safe handoff, bounded work, positive receiver service share, admitted load within the service envelope, and terminating checking.

## Partition result

A node that receives no messages cannot distinguish “no counterexample was published” from “a counterexample was published behind the partition.” Therefore no finite global update bound exists without synchrony assumptions. Critical queries must return incomplete/stale/unknown dimensions when required coverage cannot be obtained.

## Invalidation result

A remote challenge is a candidate. After local checking and admission, the receiver atomically publishes changed local facts, conservative dirty seeds, and a new reliance epoch. Old cached acceptance survives only after its exact tree is checked under the current epoch and the epoch is reread unchanged. Cross-cell correction remains eventual and conditional.

## Ledger result

The theorem object store, discovery index, local materialized reliance view, checkpoint/event history, and resource-control ledger have different consistency requirements. A blockchain of theorem payloads is unnecessary. Narrow consensus is useful only for genuinely shared mutable state; it cannot make theorem status globally current across a partition.

