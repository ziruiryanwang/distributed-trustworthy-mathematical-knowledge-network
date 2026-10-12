# Aggregate implementation integration desk

The goal is working v5, not a new guide or an aggregate-only release. This is a
mutable implementation checkpoint. All six release obligations remain open.

## Adopted design and exact source status

The independently reviewed Rust relation calls the unchanged conditional module
checker for every new witness, verifies exact graph premises, and exports one
bounded member commitment. The guest discharges all exact I/A SDK claims before
commit. The separate seal-height induction handles recursion; module rank handles
mathematical dependency order. See AGGREGATE-IMPLEMENTATION and
DELTA-SEALING-POLICY for the argument, limits and source hashes.

Root added these narrow integration sources, independently source-reviewed:

| File under software/v5/aggregate | SHA-256 | Role |
|---|---|---|
| bindings.py | d749273ef5841afe881407bcb3c2655385dd635bdae12b37e09ca2381a46bcd5 | Inert exact header/member binding, cross-language source correspondence |
| input.py | 5c5d51403bb00234f5843a1b6ca4109195285e292bdcdcc08f07ae94c7b0a226 | Bounded DMKNAI01 encoder and legacy packet adaptation; exact receipt pairs remain pending |
| receipt.rs | 41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254 | Standalone host module performing real typed I/A verification; not linked or executed |

No aggregate guest image, aggregate receipt or public aggregate authority exists.
The new receipt helper is not in lib.rs or the guest. A native structural pass
must never be mistaken for a cryptographic assumption discharge.

## Efficient next integration sequence

1. Compile only thin relation/aggregate/test/driver layers over retained checker
   library02 and existing dependencies. No checker rebuild or Cargo resolution.
2. Run narrow changed-boundary controls once, using the retained corrected
   two-delta packet. Independently compare Rust headers/roots/openings with Python.
   Real relation calls remain conditional; synthetic A is not an adopted image.
3. Inspect actual cost bottlenecks before selecting a guest feasibility screen.
   The prior one-child cycle refusal forbids inferring cheap proving from cheap
   native timings. Root deliberately does not implement a large speculative host
   or fund a full proof before that decision.
4. A justified execution screen should retain a reusable coherent execution
   capsule, with a new aggregate-specific binding/schema. An eventual staged
   producer must not repeat successful execution just to collect a capsule.
5. Producer stage resolution and final verification must use actual typed claims
   and the adopted A. A new aggregate member receiver needs live owner-bound,
   revocable authority; old exact-I receivers stay unchanged.
6. Add aggregate-frontier support through an explicit new delta/import path.
   Existing ModuleIDs/groups/bodies are unchanged. Incoming aggregate receipts
   and selected openings replace sealed witnesses, never saved success flags.

## Separate discovery defect exposed by actual operation

Network actual01 stopped with an empty first provider route before any receipt
or native check. All closures and210 bindings were independently audited; failure
remains retained. ADVERTISED_HINT did not establish remote record placement.
Source inspection shows asynchronous identify/routing admission, an explicitly
bypassed empty-routing-table barrier, and discarded provide events. The evidence
does not distinguish which startup race occurred. A fresh event-based readiness
and publication-observability successor is selected source-only, preserving
original finite deadlines, neutral bootstrap and no private holder list. Do not
replace this diagnosis with arbitrary sleeps or a larger timeout.

## Growth claim discipline

Aggregate sealing can remove intermediate application receipts, not the checking
or proving of the new mathematics. Its economic adoption still needs a feasible
full-cost region against optimized local and ordinary shared-library routes.
Selective funding must include failures, availability and service work. Native
CPU, symbolic batch formulas, usage counts and membership proofs alone do not
establish a positive growth margin or make an unserved certificate available.
