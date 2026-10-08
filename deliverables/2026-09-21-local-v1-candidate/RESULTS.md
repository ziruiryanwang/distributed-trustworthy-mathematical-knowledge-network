# Local candidate: results and support boundary

2026-09-21. This is the authoritative qualification statement accompanying
source-package02. **Usable local candidate; unchanged decentralized v1 goal
not complete.** No external release occurred and licensing remains undecided.
Start with [START-HERE](START-HERE.md). The source ZIP is immutable; historical
pending labels inside its documentation predate the evidence below. They are
not silently rewritten or treated as new executions.

## Delivered artifact

[math-commons-source.zip](math-commons-source.zip) contains 112 selected source,
documentation and canonical-asset payloads, plus its manifest: 3,637,844 bytes.
SHA-256: `22e673620aa3a6cdba6aa21ef7e56a9dcafa4c1ed296c149f2c8ab24c0f01ff5`.
The adjacent [manifest](SOURCE-MANIFEST.json) identifies each payload; the
[packaging result](PACKAGE-RESULT.json) records packaging, not runtime acceptance.
Its `DEVELOPMENT_SOURCE_PACKAGED_UNQUALIFIED` status is intentionally unchanged.
The operational qualifications below are separate, later evidence.

This is a source distribution, not a preinstalled autonomous researcher or a
copy of all mathematics. It excludes runtimes, node databases and credentials.
The supported tested environment is Windows x64/local NTFS, Lean 4.34.0 and
Python 3.14.6 with standard-library SQLite 3.50.4. Operators provide compatible
complete runtimes and owner-controlled local directories. Other environments
are unqualified, not presumed broken or supported.

## Executed and independently reviewed

| Capability | Evidence and precise scope |
| --- | --- |
| Exact source-request construction | [12 contracts](../../software/qualification/request-builder-contract-01/OUTCOME.md): UTF-8 preservation, framing, bounds and refusal cases. The helper creates files; it neither sends nor accepts mathematics. |
| Finite hosting control | [19 contracts](../../software/qualification/hosting-contract-01/OUTCOME.md): prelaunch reservation, immutable grants, no-repeat reconciliation, failures and exhaustion. Transport is mocked in these contracts. |
| Source packaging | [10 contracts](../../software/qualification/source-package-contract-04/OUTCOME.md), plus [actual archive audit](../../software/qualification/source-package-02/OUTCOME.md): membership, bounds and hashes. Earlier failed allocations remain failed. |
| Fresh shipped workflow | [Integrated01](../../software/qualification/integrated-release-01/OUTCOME.md): extract, compile both support modules, configure/init, use the shipped helper, submit/publish/expose an ordinary definition, deliver actual catalog and bundle in two 10-second sessions, expire, then refuse to restart an exhausted grant. |
| Independent mathematical use | [Baseline A](../../software/qualification/usefulness-consumer-A-01/OUTCOME.md) and [peer-assisted B](../../software/qualification/usefulness-consumer-B-01/OUTCOME.md) both check and publish the exact target below. B independently selects and substantively applies the received proof after its supplier stops. |
| Reciprocal contribution | [Preserved reciprocal test](../../software/qualification/peer-01-h01/OUTCOME.md): actual receiving-side checking and downstream mathematical use, not only HTTP delivery. |
| Custody and bounded continuity | [Replica02](../../software/qualification/replica-native-02/OUTCOME.md): another holder supplies original package bytes after the producer stops; a fresh receiver admits and uses them. |
| Capacity and interrupted operations | [Capacity01](../../software/qualification/capacity-native-01/OUTCOME.md) and [ordinary-abort02](../../software/qualification/ordinary-abort-native-02/OUTCOME.md), alongside earlier narrow peer recovery: scoped continuation with charges retained, not arbitrary crash repair. |

The 41 focused contracts are not 41 end-to-end proofs or an exhaustive security
certification. Integrated01 measured 180.734375 disjoint Job/controller CPU
seconds; helper, observer, other wrapper and agent costs are not fully measured.
Every qualification remains bound to its own exact sources and inputs.
[Cut compatibility](../../software/release/CUT-COMPATIBILITY.md) compares 103
safety-relevant payloads and maps changed paths: the mathematical code, assets
and rebuilt support binaries match the relevant prior cuts. This supplies
compositional coverage, not a claim that every old test ran on the new archive.

## Independent-agent comparison

For arbitrary `A : Type u`, associative `op`, two-sided unit `e`, and nested
lists `chunks`, both agents proved exactly

```text
R A op e (List.flatten chunks) = R A op e (List.map (R A op e) chunks)
```

where `R` is the same checked right-fold definition. Both canonical types have
the same 63 nodes, with no extra assumption or specialization. The endpoint was
ordinary checked submission **and local publication**, not compilation alone.
Local publication does not mean an Internet announcement.

Two fresh, no-history agents received the same vocabulary, target and API
documentation, with randomized order A then B. Each had 45 minutes, at most
24 post-onboarding requests, two submissions and 600 observed disjoint Job CPU
seconds. Neither received a replacement trial or root mathematical repairs.

| Post-onboarding observation | A: local baseline | B: peer access |
| --- | ---: | ---: |
| Endpoint | Passed | Passed |
| Ordinary requests | 2 | 5 |
| Native stages | 1 | 2 |
| Charged byte allowance | 144 MiB | 352 MiB |
| Public Job CPU | 114.015625 s | 100.484375 s |
| Separate serving Job CPU | None | 0.15625 s |
| Endpoint elapsed time | 375.9354725 s | 652.6888854 s |
| Submitted source | 2,159 bytes | 1,217 bytes |
| Canonical proof nodes | 216 | 229 |

B selected the append/fold law from seven catalog entries, acquired its exact
package, freshly admitted it locally, and used its fully applied proof as an
argument to `Eq.trans` in the checked induction step. The audit follows reachable
proof nodes and exact package/source/native/publication bindings. Mere imports
or catalog claims are insufficient. A constructed the auxiliary proof itself.

Onboarding additionally charged four requests, three stages and 416 MiB per arm;
observed Job CPU was 174.5 s for A and 174.640625 s for B. Thus total public Job
CPU was 288.515625 s and 275.125 s respectively; B's separate service adds
0.15625 s once. Vocabulary preparation (167.953125 s), producer02
(320.78125 s) and corpus preparation (20.390625 s) are additional measured
preparation costs, not free inputs or silently amortized marginal work. Failed
preparations and incomplete accounting remain in their original records.

**No speedup inference:** B's observed Job CPU was lower but elapsed time was
longer. Deliberate service-cost waiting, operator delays, one sample per arm and
unmeasured model/wrapper work prevent causal or general efficiency conclusions.
Shorter source did not produce a smaller canonical proof. Charged allowances
are not measured disk consumption. The first service setup failed before launch;
the disclosed pre-dispatch correction retained identical corpus and budgets.
See the [comparison](../../software/qualification/usefulness-consumers-01/COMPARISON.md)
for the complete accounting interpretation.

This is one practical success of optional discovery/reuse/contribution within
prospective bounds. It is not novel mathematics, sustained accumulation or
exponential growth. B's contribution was locally published, not sent back to A
in this trial; reciprocal exchange is supported by the separate test above.

## Trust and operational contract

- Acceptance is relative to the selected Lean foundation and permitted axioms.
  The checker, codec, local OS/filesystem and runtimes remain trusted. This is
  neither unconditional truth nor a formal proof of the entire implementation.
- Received packages are inert bounded data and require fresh local admission.
  Hash identity, a peer's success, custody and popularity do not grant acceptance.
  The owner-authorized Lean source path executes code; it is **not** a sandbox
  for arbitrary hostile source or a hostile local filesystem account.
- Agents choose their own investigations. There is no mandatory research queue,
  shared root goal, natural-language translation or human-intention predicate.
  The tested foundation is a selected library slice, not arbitrary mathlib.
- Discovery enumerates bounded catalogs; at most two configured peer aliases
  are supported. Services bind literal loopback and use finite explicit grants.
  This is not a global index, automatic routing mesh or permanent daemon.
- Resource authorizations and context sizes are finite. Renewal preserves all
  charges and does not guarantee physical storage. Preserve original request
  bytes and receipts; an unknown outcome is not permission to start a new retry.
- A fresh node can reconstruct **selected available mathematics** from surviving
  compatible custody packages and recheck it. This does not restore private
  drafts, local handles/history, arbitrary damaged state, all former knowledge
  or bytes whose every copy is lost. No general backup/restore, used-state
  migration, in-place upgrade or garbage-collection claim is made.

## Remaining decision and software gate

The independent [readiness audit](../../software/release/READINESS-AUDIT.md)
closes bounded useful-reuse and source-cut coverage. The principal remaining
software qualification is **separately operated deployment**: no second machine
was available, and every executed exchange used one host. The concrete
[two-host profile](TWO-HOST-PROFILE.md) specifies authenticated forwarding,
independent checking, contribution back and conditional reconstruction, but is
explicitly unexecuted. No new centralized service is required by that design.

Licensing and external publication are intentionally left to the owner; this
handoff grants neither. Broader libraries, larger networks, retrieval quality
and sustained useful growth need later evidence. They are not secretly passed,
nor must usefulness heuristics become mathematical axioms before a bounded v1.

The full raw evidence remains under the project's `product-local` and
`software/qualification` directories; the source ZIP alone does not contain it.
Linked outcome notes are review reports, not independent reproductions. The
goal stays active, and this candidate is not relabeled completed global v1.
