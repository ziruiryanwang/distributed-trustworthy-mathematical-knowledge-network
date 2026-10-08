# Independent scaling-contract review

2026-10-06, `/root/v4_central_reaudit`. Read complete root-owned
`SCALING-CONTRACT.md` and the final clarification delta. Reviewed SHA-256:
`8d250c9f63baf0ba58cbdbbdd9a0741938eb9a806f3bbc8638969396d64f3923`.
This is a conditional source/theory review, not new network runtime evidence.

No remaining theoretical blocker was found within the stated premises:

- The local-ID-path-only trie gives at most257 leaves at256-bit depth, hence
  at most5,140 stored contacts at bucket size20. This is a local memory bound,
  not itself a routing success or logarithmic lookup theorem.
- Logarithmic probe work explicitly assumes O(log N) relevant occupied scales
  with maintained live coverage and bounded probes per scale. Arbitrary256-bit
  keys alone imply neither the probabilistic premise nor favorable delivery.
- Selected interface/new-work/frontier costs are separate from ancestral proof
  history. No historical replay is required at a genuine certified cut, but
  demanded definitions, wide frontiers and local conversion still cost resources.
- Aggregate placement needs at least r*A provider rows under the stated r-replica
  requirement; local hot-key/provider caps add stricter constraints. Hint storage
  is not mathematical correctness, object custody or a replication promise.
- Renewal inequality is a sufficient service condition under bounded scanner
  delay, complete successful service, fair scheduling and delivery. It is not
  automatically enforced by the configured limits or established by a short
  successful loopback test.

Review found that the initial TTL formula needed an explicit homogeneous-TTL
premise: different peers may share a mathematical namespace while selecting
different lease durations. The adopted correction states a common T or uses
`T_remote_min - T_publisher/2` as the available margin. A long publisher interval
cannot guarantee a short-lived remote record. The formula is conservative because
the old remote receipt cannot precede the local publication timestamp, under the
stated nonnegative bounded delivery model. Renewals that fail instead of succeeding
do not satisfy its service premise.

The document also preserves the correct withdrawal distinction: atomic local
intent prevents queued resurrection, but already sent hints can arrive later and
expire relative to receipt. Arbitrary-delay global expiry is not promised.
Intent without an admitted self-provider row needs explicit owner retry.

The selected implementation remains useful only inside a funded service envelope;
resource caps outside that envelope mean explicit incomplete/refusal, not universal
cheap discovery. Independent physical-host and broad adversarial availability
evidence are not inferred from this argument. The actual five-node lifecycle is
separately audited by the scale reviewer, avoiding duplicate campaigns.
