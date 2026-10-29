# Selected next question: an owner-operated location layer

2026-10-28, root. Read DECISION89a7ad83 and CHALLENGE914924c5 in full. Adopt their
exact-export identity, bounded acquisition and whole-cost arguments. The challenge
correctly blocks treating a static map or an unchanged DHT wrapper as the solution.
This note selects a concrete operator model for a source feasibility decision;
it does not select implementation, a service launch, a public pilot or a new test.

## Roles and responsibility

Use independently operated, voluntarily participating custody/routing nodes.
Each operator approves its own source/runtime, bootstrap peers, listening/announced
address, endpoint policy, custody scope, key quotas and finite maintenance grant.
There is no mandatory operator, designated gateway, global membership vote or
mathematical trust in a routing peer. A light reader starts with a small chosen
set of replaceable HTTP gateways and needs no inbound listener or Node process.

The candidate backend is the **existing maintained DHT**, with a distinct ordinary
export identity domain. The operator advertises only deliberately selected keys
from its own approved custody. No arbitrary remote registration/write API is part
of this model. A gateway accepts bounded exact-key read requests and queries its
own already budgeted routing service; it does not accept a client's grant as
authority to increase its own capacity or renew maintenance.

An operator may combine custody, routing and gateway roles, but no reader is
required to do so. Addresses and operators need not be globally enumerated by a
reader. Reachable participating peers, adequate routing tables, admitted replicas,
registered key coverage and a live holder are explicit success assumptions.
Sybil/eclipse resistance, global absence and guaranteed availability are not
consequences of exact-byte mathematical checking. The user's primarily cooperative
network model permits investigating this conditional operating regime.

## Publication and continuity

New advertisements must be derivable from newly appended unit outputs, including
support-only exports, without reading or reexporting the earlier proof corpus.
The mathematical query is (SemanticID, ExportID); locator/evidence validation
remains unchanged. A failed advertisement leaves undiscoverable valid custody.
A stale advertisement may cause a paid unavailable attempt; it creates no warrant.
Serving and advertising are distinct resource commitments, with explicit horizons.

Fixed quotas apply per operator. Price first publication, duplicate publication,
expiry, withdrawal, restart/recovery, and periodic renewal. The existing repeated
published-key scan must either be replaced by a justified incremental invariant
or retained under an explicitly defended finite scope. Do not remove quota checks
or hide startup/recovery scans. An unlimited-key, forever-on daemon is not selected.

## Exact decision required before implementation

Trace the smallest complete source cut for: append-delta advertisement preparation,
ordinary DHT role/descriptor/intent validation, finite operator lifecycle, read-only
HTTP gateway and same-budget located receive with expiry preserved before every
dial. Reuse existing module boundaries rather than cloning the entire old certified
application. Identify the actual durable count/expiry APIs before proposing a fix.
Separate protocol work from arbitrary public deployment and independent hardware
evidence; neither is selected locally.

Compare this concrete model against one cheaper modification: optional grouped
membership and direct-import location hints attached to already known contribution
bundles. Grouping can reduce renewal multiplicity, but its membership production,
coverage, overlap and lookup costs must be counted. Current artifacts do not supply
that route unchanged. Do not build both alternatives speculatively. A finite bound
or a source-level impossibility can settle the choice without an experiment.

The implementation decision must name which workflow/coverage improves, give
resource bounds for publishers, gateways and readers, and identify the evidence
that could change the choice. If the existing stack cannot support this model
economically, choose the cheaper grouping modification or explicitly retain known
supplier sets. Avoid a succession of passing map demos that leaves the same open
dependency-location problem untouched.

Assignments: operable_scale_decision owns SOURCE-FEASIBILITY.md for this exact
operator model; query_scaling owns GROUPING-ALTERNATIVE.md as the competing source/
cost argument, without redoing the general challenge. Root reconciles and selects
any implementation. Both work under this canonical folder with explicit canonical
shell workdir and absolute edits. No product sources or used evidence may change.
