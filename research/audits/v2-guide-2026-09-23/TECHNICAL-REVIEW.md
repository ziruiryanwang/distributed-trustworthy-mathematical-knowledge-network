# Delivered-v2 guide: technical review checkpoint

2026-09-23. Reviewer assignment: independently extract the delivered source13
facts and audit the new explanatory guide. This is a documentation-only review;
no product, package, installation, experiment, or sealed release bytes are edited
or executed. The canonical workspace guard passed using its documented
process-local PowerShell execution-policy override.

## Authority and scope

Read the canonical `AGENTS.md`, `GOAL.md`, current authoritative section of
`research/NOW.md`, delivered `START-HERE.md`, `QUALIFICATION.md`, and
`HANDOFF-INTEGRITY.md`, and source13 `API.md`, `AGENT-QUICKSTART.md`, `CORE.md`,
and `README.md` passages relevant to this review.

The delivered release is
`deliverables/2026-09-23-v2-local-release`, frozen source13
`product-local/auxiliary-frontend-source-13`. Its integrity disposition is
`PASS_SELECTED_SOURCE13_LOCAL_V2_HANDOFF`. Source14 is an unfinished,
unqualified post-v2 development successor; none of its intended index changes
may be described as delivered-v2 behavior. Frozen source package pages retain
historical development headings; the manifest-bound release report controls
the source cut's actual qualification.

## Checklist for the guide

1. **Agent and owner are different roles.** Agents choose investigations and
   ordinary requests. The cooperative local owner provides runtimes, initializes
   nodes, configures/authorizes peer contacts, funds finite service and resources,
   and controls renewal/recovery. These are authority distinctions inside a
   trusted local-account envelope, not isolation from a hostile local account.
   No bundled autonomous researcher, shared root goal, mandatory global task
   queue, or complete corpus is included.

2. **Private artifact, public candidate, accepted context are distinct.**
   `submit` checks selected owner-authorized Lean source and returns a private
   checked artifact; it neither publishes nor advances the client's context.
   `publish` reauthenticates that artifact and creates a P1 candidate at the
   current snapshot; it grants no reader acceptance. `peer_acquire` validates
   a complete inert package and registers a local candidate/acquisition,
   advancing the P1 snapshot but not the accepted context. `admit` performs
   fresh native checking of 1–4 selected candidates and their dependency union
   with the current context, advancing the accepted head only on success.
   `info` and historical replay/selection/inspection are not fresh checking.
   (Source13 API sections “Formal local operations,” “Peer operations,” and
   “Mathematical and resource interpretation.”)

3. **Sharing does not start a server or transfer acceptance.** `expose` makes
   an immutable view of actual local publications, optionally followed by exact
   custody acquisitions. An acquired-only candidate is not eligible for its
   publication list. `replica_expose` offers retained original bundles under
   custody authority, with no new publication or mathematics. The owner then
   separately authorizes finite `host`/`serve`. Every eventual receiver still
   uses fresh `admit`. Provider disappearance after acquisition does not prevent
   local admission. Availability beyond funded service is not guaranteed.

4. **Names, handles, and identities must not be conflated.** Opaque handles are
   local to node/client/configuration and must be copied from actual responses,
   not fabricated or sent to other nodes. Foundation/definition/proof/group
   content identities are formal typed identifiers, not handles or bare digest
   strings. Returned `leanName` is the receiving Lean spelling; canonical
   `name/reference/type/u` fields are authority. Pretty names cannot safely be
   split on dots. Cryptographic digests bind exact bytes, not authorship,
   licensing, safe execution, theorem equivalence, or mathematical truth.

5. **No central acceptance server or consensus vote is required.** Nodes
   exchange packages and make local, foundation/context-relative checking
   decisions. Selected foundations, kernel, canonical/checking code, local
   runtime and OS remain trusted. TLS authenticates the owner-selected pinned
   endpoint, not theorems. The delivery does not add a blockchain, SNARK or
   global consensus mechanism.

6. **Search is bounded and exact where offered.** Local `find` optionally
   filters the current or historical local snapshot by one exact reference
   occurring in an entry's formal *type*. It is not a body-text search, human
   name search, semantic similarity search, proof unfolding, novelty test or
   theorem-equivalence test. Keys are foundation-relative. Remote `peer_find`
   provides unfiltered immutable pages from an owner-authorized peer. Its
   `complete:true` exhausts only that advertised snapshot, never global
   mathematics. Local and peer snapshots/cursors are distinct; actual handles
   and pagination bounds must be retained.

7. **The checking pipeline remains substantive.** Submission elaborates local
   source, captures the selected declaration and closure, compiles canonical
   objects, performs fresh native replay, inverse export, and a second fresh
   replay. Source syntax/parser success alone is insufficient. Shared imported
   declarations must match checked inventory; new external library material
   must be captured with its full dependency closure. Unsupported constructs,
   unsafe declarations and additional axioms refuse. Peer data does not contain
   source programs or owner execution plans. Local Lean source itself is
   executable authorized input, not hostile-source sandboxed.

8. **V2's group-root result is narrow but real.** An inductive group can be
   published directly, without a wrapper theorem. Public type/index metadata
   concerns its first original type, not a distinct entry for every member.
   Admission exposes checked constructor/main-recursor/auxiliary-recursor
   receiving names, types and universe arities within the existing 256-reference
   cap. Theorem/definition descriptions remain root-only. Source13 repairs
   frontend visibility for already-checked recursors, preserving exact kernel
   and frontend binding checks; it introduces no axiom or replacement recursor.

9. **Publication is narrower than successful submission.** Source13's public
   type metadata/index accepts only variable, sort, constant, application,
   lambda and Pi nodes (tags 0–5). Literal, let and projection type nodes refuse
   with `CANDIDATE_TYPE_FRAGMENT:NATIVE_SYNTAX_OUTSIDE_TYPE_FRAGMENT`, including
   after `submit` succeeds. Actual Count continuation changed only `1` to
   `Nat.succ Nat.zero` in the theorem statement, then freshly submitted it.
   Count definitions/proof were unchanged, but formal type encoding/content
   identity changed. The old literal-bearing artifact remains unpublished.
   There is no automatic normalization or guarantee of a cheap supported
   rewriting for every refused type.

10. **Evidence must be stated at its actual scope.** Source13's original
    exercise established substantive main/auxiliary use but failed publication.
    The separately audited source-only continuation passed publication, reverse
    pinned-TLS transfer and fresh receiving admission after the sender stopped.
    Original plus continuation: 16 attempted/15 successful ordinary requests,
    seven native stages, two publications. Including source13 preparation and
    retained failure, measured enclosing/disjoint Job CPU is 627.71875 seconds.
    Nested Job CPU must not be added again; controller/model/audit CPU is not
    included unless separately measured. These are engineering workload costs,
    not a per-theorem performance or agent-speedup estimate.

11. **Finite capacity has separate constraints.** Request credits, native
    stage credits, reserved-byte authorization, metadata headroom and actual
    disk supply are different. Failed work remains charged. Contexts hold at
    most 16 packages including five common packages; `admit` selects at most
    four candidates and checked descriptions fit 256 references. Default
    fresh-node authorization is 128 requests/16 stages/4,096 MiB reserved bytes/
    32 MiB metadata. The retained exercise instead had 12 requests/4 stages/
    1,024 MiB per node. Final A has 5 requests/1 stage/456 MiB remaining; B has
    3/0/312 MiB. B's zero stages is consumed experiment capacity, not a fresh
    product default. Owner renewal preserves prior usage and has lifetime caps.

12. **Operational outcome and replay require care.** `make_request.py` writes
    exact request bytes but does not send them. `manage.py request` sends them.
    Success requires actual structured status/acceptance flags, not an exit
    code alone. The same request ID plus identical bytes replays its historical
    terminal result without redoing work; different bytes conflict. Unknown
    outcome may follow a committed operation. Retain original IDs/bytes/state/
    evidence, and use only supported owner recovery. No automatic retry, general
    power-loss recovery, damaged-state repair or general backup/restore is
    supplied. `status` consumes no ordinary request/stage credit but writes
    supervisory evidence in scratch; it does not freshly check old mathematics.

13. **Installation is fresh and environment-specific.** Windows x64,
    PowerShell 7, fixed local NTFS/non-reparse directories and cooperative
    exclusive ownership are required. Supply complete Lean 4.34.0 Windows and
    the qualified Python 3.14.6 distribution with SQLite 3.50.4, OpenSSL 3.5.7,
    TLS 1.3/ALPN. Always use Python `-B -E -s -S`. The archive contains 114
    source payloads plus its manifest, no runtimes/prebuilt support/initialized
    nodes/private identities/experiment outputs. Check exact package hashes and
    all payload lengths/hashes; build once, then require actual init acceptance.
    Resolve the real `pwsh`, replace illustrative paths consistently, and use
    fresh installation/build/state/scratch paths. No migration or bound-install
    overlay is supported. Default free-space sample is at least 5 GiB + 64 MiB,
    excluding runtimes/build/second-node needs; it is not an OS reservation.

14. **Release does not establish the broader claims.** Evidence uses two
    nodes on one machine. Independent physical hosts, Internet deployment,
    arbitrary Lean/mathlib and external recursive/inductive constructs,
    hostile local owners, broad scaling, permanent retention and sustained
    useful or exponential knowledge growth remain unqualified. The license is
    undecided and external publication/deployment/redistribution permission is
    not asserted. The local v2 handoff is complete; the broader commons goal
    remains active.

## Completed guide review

Disposition: **PASS_STATIC_V2_GUIDE_WITH_TWO_NONBLOCKING_CLARIFICATIONS**.

Read the complete 900-line
`deliverables/2026-09-23-v2-guide/GUIDE.md`, 46,875 bytes, SHA-256
`52ff403318c9ca14bdf69eb333b99eaa8a0899ecfe217b8f6b45a46210f55445`.
The review found no material false claim in the release selection, trust
boundary, operation semantics, publication restriction, cost/accounting
figures, or limits of the actual same-host evidence. No product command or
test was run. The CLI example was checked statically against the frozen
`make_request.py` parser/request construction, `manage.py` parser, source13
API and release startup instructions. Its `find` flags, default provider,
`status`/`request` invocation and required Python flags agree. Its paths and
handle are correctly labeled deployment-specific placeholders; creating a
request is correctly distinguished from sending it.

The guide correctly distinguishes private checked artifacts, public candidates,
accepted contexts, acquisition/custody, catalog snapshots and finite owner-funded
serving. It does not promote source14, original failed runs, build success,
transport identity or historical replay into stronger mathematical evidence.
Direct group publication is accurately described, without inventing wrapper
theorems or automatic reader acceptance. The external-string-literal caveat
was checked against source13's native replay refusal
`INITIAL_EXTERNAL_STRING_LITERAL_UNSUPPORTED`.

Two clarifications were sent to the root author with the original guide lines:

1. **Lines 305–307, reverse lifecycle.** The story jumps from Bob's publication/
   exposure to Alice's acquisition. Add Bob's operator starting separately
   authorized finite service before Alice acquires, mirroring the forward
   direction. The surrounding operation table already states that exposure
   does not start serving; this makes the example self-contained.
2. **Lines 374–377 or 488–497, group search scope.** Explicitly state that a
   directly published group's public type/index is its first original type,
   not an index of every constructor/recursor/member. Receiving admission
   supplies the checked member interfaces. Existing text makes no false claim
   but does not expose this relevant search limitation.

These are documentary clarifications, not evidence of a broken CLI or false
v2 qualification claim. This review is not a new mathematical/product test,
an execution check of the template, or a new release qualification. Only this
owned review file was edited; the guide and sealed release were not edited.

## Final changed-paragraph check

Final disposition: **PASS_FINAL_STATIC_DELIVERED_V2_GUIDE**.

Root held the revised guide unchanged for this targeted check. Final guide:
`deliverables/2026-09-23-v2-guide/GUIDE.md`, 942 lines, 48,747 bytes, SHA-256
`24f1ec19fd515c052a1268032ca487e7015885fc401f9e97a4a0850afce27965`.
This final disposition combines the complete earlier read with review of the
explicitly changed paragraphs; it does not claim a duplicate whole-guide
review or any product execution.

Both clarifications are correctly resolved: lines 311–314 give Bob's operator
a separate authorized finite service before Alice's acquisition, and lines
536–539 distinguish first-original-type indexing from the complete checked
receiving member interface. There are no outstanding technical findings.

The first-use API, LLM, kernel and native-checking glosses, “distinct milestones”
heading and recorded-version snapshot explanation preserve the interface and
trust boundaries. Lines 458–473 correctly distinguish source12's checked
auxiliary recursor from its missing source-frontend visibility, and source13's
repair of that existing binding from any new axiom or relaxed checking rule.

The added teaching reductions at lines 424–435 and revised statement wording
at line 446 agree with the actual retained `CountPublishable.lean` definitions
and `And.intro`/`Eq.refl` proof. They remain explicitly teaching notation, not
an executed new workload or a claim to discover a deep new theorem. This final
check added no new authority for source14, broader native support, global
discovery, independent-host operation or useful growth. Only this review
checkpoint was edited.
