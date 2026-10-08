# CP-001B source analysis: continual learning versus exact external memory

| Field | Value |
|---|---|
| Date | 2026-08-28 |
| Role | Independent continual-learning analysis |
| Mode | Read-only analysis; no repository edits |
| Used by | `CP-001B` |

## Conclusion

Continual training and an indexed external corpus are complementary, not alternative authority mechanisms. The external content-addressed evidence corpus is exact memory; model parameters are fallible, lagging priors for retrieval, planning, conjecturing, and proof generation.

The authority boundary is

\[
\operatorname{Accept}_i(q,e)
\Rightarrow
\operatorname{Stable}_{P_i(e)}
\bigl(q;A_i(e),O_i(e)\bigr).
\]

Model parameters may propose an artifact or evidence tree but cannot be an epistemic premise in acceptance.

## What weights can and cannot do

Weights can usefully encode:

- mathematical language and stable abstractions;
- tactic, premise, and decomposition priors;
- retrieval ranking and query reformulation;
- compressed recurring proof patterns.

Weights cannot reliably provide:

- an enumerable exact theorem set;
- exact CIDs, contexts, assumptions, or environment versions;
- current challenges, withdrawals, or closure availability;
- precise per-theorem correction or deletion;
- a freshness or completeness certificate.

## Threat analysis

Online or federated learning adds:

- poisoning and backdoors;
- formally valid but semantically vacuous training examples;
- catastrophic forgetting and cross-domain regression;
- stale associations that survive attempted unlearning;
- common-mode failures across agents sharing one checkpoint;
- benchmark leakage and Goodhart effects;
- trainer/checkpoint supply-chain compromise;
- Byzantine gradient or update attacks;
- rollout divergence and weak reproducibility.

Robust gradient aggregation does not establish mathematical validity. Learned components require privilege separation from checkers, policy, admitted evidence, protected indexes, and retention roots.

## Hybrid protocol

1. Publish new work as immutable typed artifacts.
2. Update bounded exact/structural descriptor indexes.
3. Retrieve exact task-relevant CIDs and closures.
4. Let a frozen/versioned model propose plans or proofs.
5. Check and admit through the ordinary receiver-funded path.
6. Build immutable training manifests only from selected checked artifacts and typed failures.
7. Train new checkpoints or adapters offline.
8. Use sealed prospective evaluations, per-domain noninferiority, canaries, and rollback.
9. Treat every learned checkpoint as an untrusted artifact.

Online local adaptation may be tested for proposal or ranking quality. It must not change acceptance semantics or protected incident service.

## Experimental result

Compare frozen external retrieval, periodically adapted retrieval, online proposal/ranking adaptation, weights-only proposal profiles, and hybrids under identical checking and resource accounting. Exact model/data/code roots and temporal cutoffs are required. Training, evaluation, rollout, rollback, and amortized storage costs must be charged.

The central design rule is:

> External checked memory supplies addressability, freshness, correction, and replay; learned weights supply compression and heuristics.

