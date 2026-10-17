# Generic selected-target sealing lifecycle

Status: **SOURCE IMPLEMENTATION SELECTED; no runtime, funding or migration.**
Owner: `memo_tests_review`; root selects implementation/operations. Date: 2026-10-17.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

Root read/adopts this design and selects a fresh `software/v5/aggregate_lifecycle`
package: `__init__.py`, `producer.py`, `snapshot.py`, `API.md`; author may combine
the two Python modules if that reduces duplication. Reuse frozen support APIs;
no old source edits or native rebuild. Root owns focused controls/selection;
v5_growth_decision independently reviews. Implement the ordinary programmatic
API first; an explicit operator CLI follows that stable contract. Source only.

## Decision: reuse the mathematics; replace the fixture adoption seam

The native `aggregate_small/aggregate_host.rs::snapshot` already accepts bounded valid
wire and zero to eight genuine ordered I/A receipts. It derives H with the actual
relation, verifies typed pending claims, executes unchanged A, and requires exact
halted H, resolved claim and complete segments. No guest/host/checker rebuild is needed.

The actual blocker is `aggregate_small/producer.py::_snapshot` (lines786–850): its
exact configuration/result schemas describe the historical `COST_SCREEN`; configuration
has only image/build/output fields, no packet, target or arbitrary preparation request.
The retained `frontier_snapshot.py` also hardcodes BASE/FIRST, one receipt and fixture
paths. A generic script must **not impersonate that screen or rewrite its records**.
Reuse `_adopt_host_build` and the actual five-record snapshot/stage build chains.

## Smallest public owner contract

Prefer one fresh lifecycle module with an explicit new profile and snapshot schema;
reuse the pure helper, retained owner machinery and operator path/pin helpers.
Expose these phases (names are proposed API, not existing implementations):

1. `prepare(packet_bytes, exact_J, envelope)` calls `prepare_mixed_seal`.
2. `snapshot(prepared, pinned_inputs, limits, fresh_output)` performs one bounded
   layout and returns pinned **untrusted** capsule/session evidence, never a receipt.
3. `production_request(snapshot, allowance, budget, inventory, prior, fresh_output)`
   creates an ordinary finite stage request without starting or renewing anything.
4. `preflight/run(request)` reuse the scheduler; one funded prefix, with `close/report`.

`prepared` is inert data, not a mathematical or source-provenance capability. At
snapshot entry rederive it from the pinned original packet/target/envelope and compare
the complete immutable value; do not trust a manually constructed dataclass. Pin the
original packet and envelope, exact J, helper/source identities, wire, expected H,
ordered `(tag,statement,receipt)` list and member opening. Materialize unchanged parent
bytes as distinct indexed files in claim order, including A claims. No sorting by
receipt hash, deduplication of merely equal module IDs or receipt substitution is allowed.
Re-derivation is a preparation cost, not a replay of ancestral mathematical proofs.

The stable profile binds A/I/F/P, image adoption, snapshot/stage builds, supervisor,
all imported source pins and ceilings. Requests bind preparation, geometry/inputs
and fresh output. A successful snapshot also binds actual session/capsule digests,
segments, assumptions, exact native output, command, clean enclosing owner result,
diagnostics and final input/output rebinding. Keep failures and partial files inert.

## Minimal successor, not another producer rewrite

A fresh explicitly versioned `LifecycleProducer` may derive from the frozen owner:
invoke its existing constructor with the exact retained base profile; extend its
pin map with the fresh lifecycle/helper sources and actual snapshot build records;
assign a domain-separated composite profile ID binding the full immutable lifecycle
profile; replace only snapshot-evidence adoption. Reuse inherited stage planning,
manifest checks, full-path quotes, reservations, lineage, dispatch and closure.
Keep the inherited base profile bytes unchanged; never monkeypatch module globals.
The new immutable profile must be rebound too.

Its snapshot-evidence object can keep the same five pin roles (`result`, `outer`,
`selection`, `configuration`, `command`) while explicitly adopting **new schemas**.
The retained internal stage-request/attempt grammar may remain unchanged because
its graph/accounting semantics are unchanged; the composite profile ID separates
all fresh lineages. This is an explicit successor entry point, not an old owner
silently accepting new reports. Source/constructor/close review is required before
implementation adoption. One module can dispatch snapshot/preflight/run; no per-seal
fixture adapters or old attempted allowance migration.

Keep installation stable across prefixes: evidence snapshots are not installed source.
Changed helper/profile/build identity requires fresh adoption and lineage.

## Bounds and repeated reciprocal use

Enforce the intersection of the mixed/helper and producer bounds **before layout**:
wire≤16MiB, claims≤8, each receipt≤1MiB, members≤48, po18, cycles≤2^26,
segments≤256, capsule≤96MiB; also the owner's actual 20MiB fixed-input, 512MiB
read and full output/census limits, including records and image. A raw32MiB mixed
packet fitting its parser does not imply a feasible producer session. Native output
and outer ownership must establish actual completion; no fallback cap increase.

After finish, the ordinary client independently verifies the actual A/H receipt,
selects exact J with its opening, and only then substitutes that representation.
Retain demanded group/body semantics separately; `export_evidence`, public custody
and publication expose the same J. A new native tail can refer to that live A member;
its next mixed packet enters this same preparation path. Rank and seal height remain
distinct, and the helper rejects height overflow. No ancestor witness is fetched
merely to validate the certified premise. Missing demanded semantics still refuse.

Selective renewal is an owner decision. Price preparation, repeated native preflight,
layout, proof, failed search and custody in the selective-certification inequality.
This is repeatable capability, not positive growth. Cross-review: `v5_growth_decision`
supports the boundary with stable installation/profile and full-cost accounting.

## Consequential next evidence only

Before any real launch: focused refusal checks for forged preparation, parent
reordering, changed target/build/helper, limits, partial snapshot and cross-profile
continuation; one synthetic repeated-I/A lifecycle checks owner plumbing, not proofs.
Then reuse the first genuine A and public reciprocal gate already being prepared.
A later A→tail→A renewal needs fresh selection, not repeated I-only campaigns; v5 stays open.
