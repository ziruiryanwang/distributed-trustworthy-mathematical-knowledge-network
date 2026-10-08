# CP-001B source analysis: distributed storage and indexing

| Field | Value |
|---|---|
| Date | 2026-08-28 |
| Role | Independent storage/index analysis |
| Mode | Read-only analysis; no repository edits |
| Used by | `CP-001B` |

## Conclusion

DTMKN should expose a logical global corpus without requiring a physical global copy. Let

\[
\mathcal C(t)=\bigcup_i\operatorname{Published}_i(t).
\]

No node, index, blockchain, or model must materialize this union. If a class contains \(U\) bits that must be exactly reconstructible, aggregate retained information has worst-case lower bound \(\Omega(U)\). The system must pay for exact storage, retain an exact recomputation recipe, or permit expiration.

## Retention result

Separate raw output, bounded quarantine, admitted metadata, reusable native evidence closure, replicated/erasure-coded closures, archival objects, recomputable objects, derived indexes, and expiring provider records. “Generated” and “valid” do not imply “durably stored.” Stable strict reuse requires the exact current closure to be locally available.

Garbage collection should mark from receiver-authorized retention roots, traverse dependency manifests, use grace epochs, and preserve in-flight pins. Content-addressed chunking and Merkle-DAG manifests deduplicate shared formal environments and dependencies.

## Index result

Use layered indexes:

1. CID to provider records;
2. exact judgment/goal/context/environment keys;
3. symbols, type heads, normal forms, assumptions, and dependency shapes;
4. receiver-derived reverse dependencies;
5. interest/subscription shards;
6. optional embeddings as candidate rankers.

The mandatory laws are

\[
\operatorname{IndexHit}(k,c)\not\Rightarrow\operatorname{Valid}(c)
\]

and

\[
\operatorname{NoHit}(k)\not\Rightarrow\operatorname{Nonexistent}(k).
\]

Every accepted use resolves to an exact CID, obtains the required closure, and passes receiver-local checking.

## Scaling result

For generation rate \(\lambda\), schema/admission/retention fractions, unique retained payload bytes \(u\), descriptor bytes \(m\), payload durability overhead \(\rho\), and descriptor-home replication \(h\), durable stock depends on both publication rate and retention survival. Finite-lived tiers have stock proportional to rate times mean lifetime; only an indefinitely surviving fraction forces asymptotically linear cumulative growth. Repair bandwidth is traffic, not resident stock.

All-results-to-all-nodes dissemination has aggregate cost linear in both node count and publication rate. The intended architecture uses bounded metadata homes, direct content-addressed payload transfer, hot caches, cold archives, and explicit retention contracts.

## Whole-system status result

An exact instantaneous global status is impossible in an asynchronous partitionable network. Checkpoints can commit to scoped shard histories, but do not establish theorem truth, current payload availability, or completeness of unpublished information. Ordinary agents need bounded task-relevant shard frontiers, relevant deltas, incident notifications, and on-demand objects—not every theorem.

## Recommended implementation slice

- chunked five-cell CAS;
- exact/structural/dependency indexes;
- bounded descriptor homes and Merkle anti-entropy;
- retention activations, provider audits, repair, and garbage collection;
- scoped status/frontier API;
- partition, index-poisoning, provider-loss, hot-key, GC-race, and valid-junk tests.

