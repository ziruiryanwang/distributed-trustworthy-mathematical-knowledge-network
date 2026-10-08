# Source10 support and evidence

2026-09-23. **Locally qualified source10 successor:** independent disposition
`PASS_SELECTED_SOURCE10_INSTALLED_ENCODER_NOT_WHOLE_V1`.
Exact package identities are in [START-HERE.md](START-HERE.md). This is a narrow
source09 successor, not a new whole-release validation or a perfect release.
The adjacent [HANDOFF-INTEGRITY.md](HANDOFF-INTEGRITY.md) separately decides
the final file-delivery gate; absent, failed or mismatched means incomplete.

## Change and evidence boundary

The complete [source map](../../experiments/short-header-01/SOURCE-MAP.md) records
114 payloads: 111 unchanged, exactly three changed, no additions or removals.

| Changed payload | Bytes | SHA-256 |
| --- | ---: | --- |
| `py/codec.py` | 23,024 | `1906a39f819f6c3aa3a4f3d8eae10b00bf02040a339efc532b42155b4d7d6bcf` |
| `py/source_codec.py` | 53,215 | `9188b1e7bc90f73bfcb0335cd892ce3e57504e6ab67a1e512134845da43adf4a` |
| `assets-lock.json` | 18,915 | `965ffe1d475fbd4fc485259bf0a807583246f2e0ce520a55767b5e46f2b84915` |

Only short-header encoding and its loader/lock bindings change. The inherited
[source09 scope and limitations](../2026-09-23-v1-local-candidate/RESULTS.md)
remain applicable. Earlier reciprocal reuse, contact, custody, recovery and
mixed-catalog evidence is preserved, **not rerun wholesale on source10**.
Unchanged-code comparison supports focused testing, not automatic release proof.

## Observed gates and evidence

| Gate | Disposition |
| --- | --- |
| Isolated encoder correctness | Audited PASS: twelve differential groups, zero failures/errors/skips, clean closure; no native checking or network. |
| Component performance | Audited PASS: 24 reads, two alternating baseline/candidate pairs, exact complete outputs. |
| Fresh source10 package/support build | Audited PASS for exact package/build and clean closure; no mathematical acceptance. |
| Installed loader/lock controls | Audited PASS: six cases, including both crossed-loader refusals and installed new/new Beta package/plan equality; no native acceptance. |
| Actual installed Compose publication, transfer and fresh receiver admission | Independent `PASS_SELECTED_SOURCE10_INSTALLED_ENCODER_NOT_WHOLE_V1`; exact canonical bytes, new staged codec pair, fresh native acceptance and clean closure. |
| Final copied-artifact/document integrity | Separate required adjacent report; consult its exact checked scope and disposition. |

Actual preparation [result](../../experiments/short-header-01/preparation-01/RESULT.json):
4,350 bytes, SHA-256 `edb4a00b6277919009b0ec3b3c4e68d25b5cd1b418e0fcf01ebaf9b41116476a`.
Fresh installed [build receipt](../../product-local/short-header-integration-10/install/build/build-receipt.json):
3,193 bytes, SHA-256 `939b9f175a1970aaa53d65bfbdefa61875f34debcfe55c42ad9bf9628854b570`.
Independent [preparation/binding audit](../../experiments/short-header-01/PREPARATION-BINDING-OUTCOME.md):
8,656 bytes, SHA-256 `d169de3ed0a4df93dee0128791fd0fdb0c5145f134c23ce1b5f014a3ff995dad`;
disposition `PASS_SELECTED_SOURCE10_PREPARATION_AND_BINDINGS_NOT_INSTALLED_MATH_ACCEPTANCE`.
Both allocations closed cleanly; neither initialized nodes or granted native acceptance.

Actual installed [result](../../experiments/short-header-01/integration-01/RESULT.json):
91,268 bytes, SHA-256 `80f64383e0c4fd56c7f7a8dbafa34d31ffd63b80fc4453f7419084087db245bb`;
[inputs](../../experiments/short-header-01/integration-01/INPUTS.json):
58,266 bytes, SHA-256 `1b27ad645e3a4aa00cdbf22441f674cc53cf55d6824d71ba99a46c66e544e970`.
The independent [installed outcome audit](../../experiments/short-header-01/INTEGRATION-OUTCOME.md)
is 8,059 bytes, SHA-256 `58e81db586f43e5569b812db28ebc87edd5d5b305c89d548e1d6a330e054e681`.
It confirms eight requests/four mathematical stages, no replay or renewal,
identical candidate/inverse/producer/receiver Compose package bytes, and fresh
native receiver acceptance after actual TLS service stopped. Submission and
admission retain distinct one-root/six-root replay contexts with the same
definition and foundation. Both nodes and service closed cleanly. The frozen
raw result's pending-audit label remains historical; this audit supplies the
completed scoped disposition, not a rerun or rewritten machine result.

## Measured improvement, correctly scoped

The independently audited [qualification](../../experiments/short-header-01/OUTCOME.md)
and [benchmark](../../experiments/short-header-01/BENCHMARK-OUTCOME.md) compare
the actual package reader on five shipped packages plus the retained Beta
package. Every arm uses fresh Stores; complete Store/root/plan outputs agree.
There is no profiler or discarded sample. Median paired candidate/baseline
ratios are **0.688461 CPU** and **0.679034 wall**: approximately **31.2% less CPU
and 32.1% less elapsed time for that selected reader workload**.

Two pairs do not estimate a population; host/order variation is visible.
These percentages do not describe native checking, whole-node/agent/network
cost, mathematical usefulness or growth. No new mathematical authorship is
claimed by replaying known Compose source in the installed integration.

Component workers consumed **85.953125 Job CPU seconds**; the six-binding worker
separately consumed **5.109375**. Preparation used **31.359375 Job CPU seconds**
and **56.2131261 wall seconds**. Audited installed integration reports
**158.15625 main + 0.53125 service = 158.6875 disjoint Job CPU seconds**, with
**159.8781085 wall seconds**; preparation plus integration is **190.046875 CPU
seconds**. Different workloads are not a before/after comparison. Nested receipts
and timed reader calls are not added again; model/controller/reviewer costs
are excluded. These costs qualify neither whole-workflow speedup nor usefulness.

## Unchanged foundations, safety and practical limits

Receiver-local Lean checking is relative to the selected foundational axioms,
canonical policy, trusted implementation/runtimes and cooperative owner/OS.
Certificate pinning authenticates an owner-selected endpoint, not mathematical
truth. No SNARK, blockchain ledger or centralized acceptance service is added.
Config 6 / physical database 5, wire/catalog 2 and stage-plan 2 remain selected;
use fresh installations/state, not in-place migration.

The foundation inventory and five common packages are unchanged. General
mathlib interoperability, arbitrary external inductive/recursive families,
instance/notation reconstruction and every Lean construct are not qualified.
Contexts remain limited to sixteen packages including the five common ones;
admission selects at most four. Catalog/contact/storage/CPU bounds still apply.
Search is bounded local filtering or selected-peer enumeration, not complete
global discovery. Finite hosting and conditional custody do not promise
permanent retention. General backup/restore and used-state migration are absent.

Preserve all predecessor failures and costs. No second-host, public-Internet,
sustained useful growth, exponential accumulation or broad scaling claim
follows. Licensing remains undecided; no external publication/deployment or
redistribution permission is supplied. The full project goal remains open.
