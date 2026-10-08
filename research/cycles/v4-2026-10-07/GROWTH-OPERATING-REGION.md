# A concrete useful-accumulation operating region for v4

October 7, 2026. Theory/requirement author: `/root/v4_final_growth_challenge`.
This note uses the actual one-shot `growth-accounting01` result. Its independent
source/outcome audit passes in `experiments/named-library-01/INDEPENDENT-SOURCE-REVIEW.md`,
under "Actual installed-client contracts and finite growth accounting". This
note supplies requirement/theory interpretation; final release adoption belongs
to root. No additional execution is selected here.

## Result

The new representation supports a **real finite payload-capacity improvement**,
not merely an asymptotic or hypothetical positive-amortization claim. The exact
ten positive constructions D0, D1 and FAMILY_1 through FAMILY_8 require:

| Persistent representation of the same endpoints | Mathematical payload |
|---|---:|
| Exact shared module recipes | 19,963 bytes |
| Recipes plus the largest single flattened capsule | 27,609 bytes |
| Every independent self-contained prefix capsule | 53,480 bytes |
| Recipes plus every flattened capsule | 73,443 bytes |

All ten selected lowerings actually completed under the unchanged supported
bounds. Every completed prefix, including the smallest two-root prefix, has a
positive recipe-versus-independent-capsule payload gap. This is not a theorem
count or a claim that the familiar example constitutes new mathematical truth.

**Concrete capacity theorem.** Fix these exact ten formal type/body endpoints,
the selected codec/lowering policy, and a persistent mathematical-payload
allowance of 32 KiB = 32,768 bytes. Suppose the owner preserves the recipe
closure, can reconstruct a requested endpoint through the selected lowerer,
and separately provisions the nonpayload resources below. Then retaining the
recipes and at most one flattened capsule fits this allowance, whereas the
previous protocol retaining every independent self-contained prefix does not.

Proof: the actual exact byte sums give

```
19,963 + 7,646 = 27,609 <= 32,768 < 53,480.
```

Every selected root was actually reconstructed from its exact prefix and bound
to an exact emitted capsule hash/interface. The family therefore supplies the
required reconstruction witnesses, rather than assuming they exist. The
comparison protocol must retain all its designated capsules, whose sum exceeds
the allowance. No kernel/prover timing premise enters this byte inequality.
The comparison does not impose a global retention policy on the network: it
is one explicitly chosen local accumulation policy and finite workload.

With no retained flattened cache, the exact saving is 33,517 payload bytes
(about 62.67%). With one largest capsule retained, it is 25,871 bytes. Keeping all
flattened outputs would erase the saving. These are payload differences, not
whole-disk or whole-route performance percentages. An optimized cross-object
compressor, a local named library already owning the same material, or a policy
retaining only the latest output is not the comparison protocol.

## What was observed, and what is proved compositionally

The one-shot analyzer used the previously exported immutable family and the
adopted installed pure codec/compiler/lowerer. It did not regenerate the family,
run a native checker, generate a proof, open a database, or use the network.
All 10 roots completed once; no refusal or retry occurred. Exact evidence is
`experiments/named-library-01/growth-accounting01/RESULT.json`, with outer
operation evidence in `growth-accounting-outer01/RESULT.json`.

The largest selection had 10 modules, 19,963 raw input bytes, 7,646 output bytes,
125 output expression nodes, 329 emission states, 9 typed instances and 1,279 lowering
work units. Current selected-lowering ceilings are 64 modules, 16 MiB raw input,
4 MiB output, 200,000 compiler nodes/states, 1,000,000 compiler work,
64 module-path depth and 256 emission depth. Passing these ten operations does not
remove any ceiling or promise every request below a byte cap succeeds.

The complete outer record reports 0.546875 inclusive Job CPU seconds plus
0.21875 outer-wrapper CPU seconds, 0.8211856 outer wall seconds, two processes,
zero residual/terminated processes and clean Job closure. Peak recorded Job
private commit was 25,583,616 bytes. These describe this accounting operation;
they are not a matched checking/network speedup. The analyzer's earlier internal
time samples exclude final output serialization/fsync; use the outer totals for
the complete run.

The repeated family has a direct typing argument: if a polymorphic operation
maps A to A under the declared parameters, composing it with itself has the
same type. Induction therefore justifies the family at the source level, given
the acquired Iter seed, ordinary type rules and lowering correspondence. The
typed import applications retain declared-type obligations instead of discarding
them. This is not an observed kernel acceptance report for all ten emitted
capsules. Actual accepted reciprocal D1/D2/law use and wrong-signature rejection
are separate integration evidence; neither this note nor the analyzer supplies
their acceptance labels.

## An implementable owner policy

The software already separates immutable recipe custody, selective acquisition,
lowering, local native acceptance and transferable receipts. A participant can
use the following policy without a new central authority or research scheduler.

1. Keep the exact recipe closure for every endpoint promised during the current
   custody epoch. Store admission reserves unique logical bytes and entries;
   use 10 entries or more for this family and a blob allowance of at least 19,963.
   For the 32 KiB example, an allocation of 24 KiB for recipe payload plus 8 KiB for
   at most one retained canonical capsule is sufficient. This is a local
   resource allocation, not a new store schema or a claim that its two parts
   are enforced by one automatic combined quota.
2. Keep exact recipe IDs, adopted policies and whichever frontier/law objects
   are actually needed. Dispose of a reproducible flattened cache only after
   preserving its dependency recipes and required evidence. A hash cannot
   restore lost bytes. The updated operator guide permits recipe-only custody;
   the software does not supply automatic infinite retention or cache eviction.
   Count every persistent canonical capsule copy in the mathematical-payload
   coordinate, including copies inside native artifacts or evidence directories;
   changing its pathname or role does not move it to another budget. The one-cache
   witness permits at most one such copy across all locations. Verification
   workspaces may be separately transient, but must be retired after preserving
   exact recipes and genuinely required warranted evidence. The actual accounting
   experiment retains all outputs for audit and does not execute this retention
   policy or demonstrate automatic eviction.
3. Acquire only the selected missing closure under one operation-wide allowance.
   Retained exact dependencies need not cross the network again. Require a
   completed custody status, not just a successful command envelope, before
   requesting local materialization. A partially acquired closure remains
   partial even if its individual files have good hashes.
4. Lower through the adopted code and check the **exact resulting capsule**.
   Publish custody offers independently of mathematical acceptance; receivers
   never adopt a sender's local checked flag. Recheck locally or verify an
   actual compatible certificate at the required assurance level.
5. Admit new service/checking/certification work only under an explicit finite
   allocation. Preserve failed/expired work and charges. A separate future
   allocation may reuse exact retained custody; it must not pretend the earlier
   attempt was free or automatically renew an expired proof operation.
6. Stop admitting an object before the storage reserve is exhausted, and stop
   advertising a service promise that cannot be funded. Available mathematical
   knowledge is the exact retained/retrievable and warranted capability, not
   the number of expired provider hints.

A 32 KiB mathematical-payload allocation is intentionally a small finite witness,
not a recommended total node configuration. Operators may choose larger finite
allowances. Normal services, installations and cryptographic artifacts are much
larger and must not be hidden outside an advertised **total** budget.

## The rest of the resource vector is explicit

Write the owner's allocation as

```
b = (persistent mathematical payload,
     other persistent storage, transient disk,
     CPU, memory, wall time,
     requests, route events, connections, outgoing service,
     optional certification work).
```

The theorem strictly improves the first coordinate for the fixed comparison.
It does not prove Pareto improvement in every coordinate or positive benefit
under arbitrary monetary/CPU weights. The remaining coordinates have these
implementable conditions:

| Resource | Required policy and supported mechanism |
|---|---|
| SQLite/index/owner/overlay storage | Fund separately from raw module blobs. Existing store page and metadata ceilings bound admission. The database minimum is 256 pages; page accounting is not a 19,963-byte whole-store claim. |
| Native artifacts, receipts, laws, runtime and evidence | Reserve their actual selected bytes separately. Count retained capsule copies if they remain. A fresh audit may retain every output for reproducibility even though a normal operator chooses recipe-only persistence. |
| Materialization | Use actual selected-root byte/state bounds plus an enclosing finite CPU/memory/wall allowance. The observed 120 CPU-second / 180 wall-second / 512 MiB accounting allocation completed; it does not qualify identical bounds for all later native checks. |
| Checking and conversion | Allocate per operation, supervise the entire process tree, accept only a real successful exact report. Demanded semantic computation is not eliminated by a ModuleID. No general linear checking bound is asserted. |
| Acquisition | Current absolute ceilings are 128 modules, 512 edges, 64 MiB counted byte events, 512 requests, 8192 route progress events and 60 seconds; lower owner choices and per-node operation deadlines also apply. This family needs ten unique descriptors, but actual route/failure/service costs are additional. Custody success can exceed the stricter later lowering envelope, so check both. |
| Maintained service | Fund provider renewal, outgoing requests, finite connection capacity and retained copies. Reachable compatible contacts and at least one available selected custodian or prior local custody are necessary. These are service conditions, not cryptographic guarantees. |
| Optional certificates | The existing source-free prepare/advance/final-verification route uses actual prepared segment/assumption counts and explicit full remaining-stage funding. Native acceptance does not supply a receipt. If funding, stage capacity or deadline is insufficient, refuse/defer certification and retain the correct lower assurance label. |

An owner who wants a single scalar cost can choose nonnegative weights w and
compare `w dot cost` for both full routes, including setup, maintenance, failures,
checking and original certificate costs. This result does **not** determine the
sign of that full weighted difference. It determines a nonempty finite
payload-feasibility interval with actual reconstruction, which was previously
only an asymptotic possibility.

## End-to-end support theorem and its boundary

Let a finite set of operations satisfy all of the following: adopted exact
code/policy and sound checking assumptions; canonical ID-bound recipe custody;
selected acquisition with reachable providers or prior local custody; sufficient
finite per-stage allocations; correct source-to-output lowering; and actual
successful checking or compatible receipt verification before accepted reuse.
Let providers fund their stated service epochs and recipients retain needed
bytes beyond a supplier's shutdown.

Then independent agents can acquire a construction, reuse it in a new recipe,
check its exact result, contribute it and let another agent repeat the same
steps, without an indispensable central server or whole-corpus storage/scan.
Proof is composition of the implemented custody, lowering, checking and peer
interfaces with their explicit statuses and exact bindings. A failed stage
does not entail success of its successors; incomplete results preserve that
distinction. The real reciprocal integration gate establishes actual instances
of this composition, while its source contract covers the general conditional
claim. Its observed outcomes must be cited separately before final adoption.

For the concrete family and retention policy, this composition can use the
strictly smaller payload allowance proved above. That is a substantive
software-supported accumulation capability: more of the specified warranted or
subsequently checkable constructions remain reconstructible under the fixed
payload limit. It is not the assertion that each extra ModuleID is inherently
valuable, that every research project accelerates, or that production data must
grow exponentially. Independent demand determines which capabilities merit
local retention; it never determines mathematical validity.

The network-size conclusion is likewise conditional and structural. No selected
operation needs a census of all M global objects or all theorem-proof ancestors.
Routing/load/coverage, demanded transparent semantics, finite selection limits
and certification costs still matter. The repaired remote continuation path
addresses permanent first-page blindness at an already reached provider; it
does not imply complete global recall under partitions, capped provider search
or hostile identity multiplication.

## Release claim this evidence supports

V4 can claim an implemented reusable semantic-library boundary, exact bounded
reconstruction, trustworthy-checking integration when its actual gate passes,
and a demonstrated finite payload-capacity advantage for a stated useful
construction family and prior-protocol baseline. The acquired algebraic law
supplies an additional reusable mathematically warranted algorithm transformation;
its operation-count advantage is a theorem, not this run's evaluation benchmark.

This is materially stronger than publishing named toy objects or an inequality
with an unknown sign. It is still not a claim of unrestricted Lean compatibility,
Internet-wide measured reliability, universally cheap search/proving, guaranteed
availability, global novelty detection or a universal positive research-growth
rate. These are not silently added gates, and the concrete v4 achievement must
not be inflated into them.
