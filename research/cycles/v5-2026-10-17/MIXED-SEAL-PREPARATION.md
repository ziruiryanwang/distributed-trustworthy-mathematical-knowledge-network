# Minimal generic mixed-evidence seal preparation

Root selection: implement only fresh aggregate_claims/prepare_mixed.py under
this contract, owned by memo_tests_review. Root owns a fresh focused test module;
v5_growth_decision independently reviews. No frozen dependency edits, native
calls or proof funding. Root read the full contract before this selection.

2026-10-17, `memo_tests_review`. Source/theory contract only. Canonical guard
passed; root AGENTS applies. No imports, runtime, implementation, tests or Git.

## Proposed selection

Add only fresh `software/v5/aggregate_claims/prepare_mixed.py` and its focused
test file after root authorizes them. Do not modify frozen parsers, encoders,
producer, guest, receipt policy or fixture adapters. This is the missing pure
conversion seam, not a second production workflow or automatic seal scheduler.

```python
prepare_mixed_seal(raw: bytes, target_journal: bytes, *,
                   adopted_image: str, envelope: mixed_claims.packet.Envelope
                   ) -> PreparedSeal
```

The caller explicitly supplies the existing immutable mixed packet, one exact
184-byte native target J, locally adopted A image and finite existing envelope.
No path, fetch callback, verifier, source compiler, network, grant or output
directory is accepted. A target may be an earlier native ancestor of the packet's
last delta: the helper selects its necessary closure, not an easier statement.
Multi-target optimization and union of independently supplied packets are deferred.

Return a frozen, tuple/bytes-only data record containing input SHA/length, exact
target J, wire bytes, expected 192-byte H, ordered candidate parent claims
`(tag, statement, receipt_bytes)`, byte-sorted selected member Js, target index
and membership siblings, selected original claim/frontier/delta indices and
selected witness SHA/lengths. Include finite size/count census. This avoids
duplicating whole witnesses outside the wire or inventing a live warrant.
All fields are **untrusted preparation**, even when computed from a valid input.

## Reuse these exact functions

- `mixed_claims.packet.parse_packet(raw, envelope, aggregate_image=A)` once:
  existing count/shape/profile/rank/membership/backward-closure checks; returns
  claims, frontiers and `(canonical_witness_bytes, parents, summary, rank)`.
- `delta_claims.claims.expected_journal(summary, rank, B.RELATION_IMAGE)` and
  `aggregate_claims.bindings.member_journal`: derive and validate exact node keys.
- `delta.packet.require_closure(target, graph)`: validate the selected induced
  graph after traversal. Do not copy a second relation/witness parser.
- `aggregate_claims.input.encode`: existing DMKNAI02 framing, exact I/A tags,
  index/path checks, finite wire/count bounds and newly checked target constraint.
- `aggregate_claims.bindings.commitment/opening/bind_member/decode_header`:
  existing v2 membership and profile binding. Reuse their exact domains/order.

`input.from_legacy_packet` stays unchanged. It supplies only I frontiers and
requires separately supplied journals; mixed input already carries exact I/A
claims and member openings, so round-tripping through that converter would lose
information and duplicate work. `frontier_snapshot.derive` stays a retained
fixture adapter, not imported into the generic helper.

## Deterministic algorithm and preservation contract

1. Validate byte types, exact target and adopted A; parse the entire supplied
   mixed packet with the existing envelope. The parser already rejects duplicate
   exact warrants/claims, missing/forward edges, wrong ranks and unused original
   material. Do not salvage a malformed omitted descendant through a second,
   weaker parser. Parsing is structural, not proof or receipt verification.
2. Build at most48 nodes: certified frontiers have no serialized parent edges;
   each native delta uses its parser-returned exact parent-J tuple. Require the
   requested target to be a native node. Unknown J, same ModuleID/different J,
   already-certified frontier, and terminal-only input refuse explicitly.
3. Traverse backward from that target with a bounded visited set. Keep exactly
   the reachable native nodes and frontiers. Keep original delta topological
   order and original relative frontier order. No parent edge may be removed
   from a retained witness. Distinct exact Js are never merged by ModuleID.
4. Keep only claims referenced by retained frontiers, in original claim order;
   remap their integer indices consecutively. Preserve each retained tag,
   statement, receipt bytes, member J/index/path exactly. Several frontiers from
   one A share its one original claim/receipt, not copied receipts per member.
   Do not replace a native node by an unrelated receipt or optimize derivations.
5. Pass retained **parser-returned witness bytes unchanged** to `input.encode`,
   with `targets=[target_journal]`. These are the existing parser's canonical
   named-record encoding; do not claim byte identity with arbitrary whitespace
   substrings of the original packet JSON. Pin both raw input and selected
   canonical witness hashes. The caller's already canonical exported packets
   use the same representation.
6. Sort all selected exact Js by full bytes, matching Rust `Graph`'s BTreeMap.
   Compute the expected root with `B.commitment`; rank is their maximum;
   seal height is `1 + max(retained A parent heights, default=0)`, checked for
   u64 overflow. I claims do not increase parent seal height. Construct H using
   the fixed B relation-image/foundation/policy and adopted A, then validate it
   with `decode_header` and the target opening with `bind_member`.
7. Return the immutable plan and exact selection census. Changing target or
   pruning changes H/wire and later capsule/session identity, never the target
   J, foundation, policy, checker or retained witness semantics. No I/A
   certificate is created or transferred as local mathematical authority.

**Why the cut is safe in principle:** if the unchanged native relation accepts
every retained witness and every retained pending receipt is genuinely verified,
induction along the preserved topological order establishes each selected node.
Certified frontiers provide the exact premises; each new conclusion retains all
its original exact parents. The target is therefore unchanged. The helper only
selects the candidate subgraph; it cannot establish those acceptance premises.

An A frontier's ancestor proofs need not be reacquired: the packet already holds
its receipt, exact H/J and membership path. The existing native snapshot host
calls `relation::check_bytes`, compares the actual derived H, and verifies each
ordered pending I/A receipt before guest execution. It later requires exact
halted-session H and assumption resolution. This remains the authority boundary.
Required definition bodies/openings stay in retained witnesses or separately
acquired semantic custody; a certificate never makes missing bodies available.

## Bounds and integration

Use the caller's existing envelope without widening it: maxima include32 MiB
packet,16 MiB witness,8 MiB total receipts,16 deltas,32 frontiers,8 claims,
128 edges,48 total members and6 membership siblings. Traversal/storage indices
are bounded by these counts. `input.encode` additionally enforces **16 MiB total
wire including overhead**; witness bytes alone do not establish wire feasibility.
Height/rank overflow and output-size excess refuse, never truncate or fallback.
Caller/outer owner still bounds parser CPU and peak memory; the byte limits are
not a proof of a particular resident-memory bound.

No file writes occur here. A separately selected owner stages wire/H and exact
parent receipts, pins them, obtains a fresh real execution capsule, then uses the
existing operator's profile/request preflight/run. `aggregate_small`'s stricter
1 MiB per-parent/96 MiB capsule/po18/N256/2^26 limits still apply: generic encoding
success is not admission to that producer. The helper must not silently narrow
the math protocol to this one machine's resource profile.

The existing `client.export_evidence` provides mixed bytes. After real receipt
verification, existing `admit_aggregate_member` / exact-terminal admission,
`import_context` resolution, `retain_semantics`, `publish` and `reconcile` provide
onward use. Keep needed original semantic material before replacing publication
with a terminal. A generic snapshot-adoption wrapper is a later small owner seam,
not permission to copy another fixture or launch a proof in this helper.

## Minimum changed-boundary controls, no new proof campaign

1. Whole-last-target preparation agrees byte-for-byte with direct existing
   `input.encode` from the same parsed rows; selected earlier FIRST agrees with
   retained BASE+FIRST wire/H/witness identities when fed matching mixed evidence.
2. Branch pruning retains every selected parent, omits unrelated descendants,
   preserves topological order, and remaps a nonzero original claim index.
3. Mixed I+A parents and several selected members of one A preserve claim order,
   share its receipt once and derive height from retained A claims only.
4. Unknown J, same ModuleID/wrong rank, existing frontier and terminal-only input
   refuse; no new wrapper theorem or target substitution is synthesized.
5. Wrong A/F/P, invalid membership, missing/forward parent, duplicate exact node
   or unused original material reuse existing parser refusals.
6. Selected parent height=u64 max refuses; omitted high-height claims do not
   affect the selected header. Wire overhead, receipt/count/edge limits and
   mutation of returned container state have explicit boundary controls.
7. Structurally well-formed but false proof/forged receipt data may still prepare:
   output must remain untrusted. Actual rejection belongs to unchanged native/
   cryptographic gates; do not claim pure tests establish it or rerun those suites.

Synthetic inert I/A openings are sufficient for pure selection tests and must
be labeled synthetic. Reuse saved real bytes for identity comparisons; no new
native/guest/proof campaign is needed to test this deterministic conversion.
Root must separately select exact implementation and any finite controls.

## Actual focused result adopted

Root selected `mixed-seal-preparation-controls-01`, plan1e730111, once. All eight
tests pass; independent audit confirms42original/snapshot source bindings,
21runtime pins,20loaded source origins and clean closure. Known1.046875CPU and
1.2815069wall seconds. The real-input comparison reproduces selected FIRST wire,
header and witness identities; no native, guest, proof or receipt verification
was run. Helper2d03b635 and testsf9b3a92e are used/frozen. Generic lifecycle
adoption and actual certification remain separate central work.

## Source implementation checkpoint

Root selected the helper only; implemented `aggregate_claims/prepare_mixed.py`.
The function signature above is unchanged. `PreparedSeal` holds `adopted_image`,
`input_sha256`, `input_bytes`, `target_journal`, `wire`, `expected_header`,
`parents`, `members`, `target_index`, `target_siblings`, `selected_claim_indices`,
`selected_frontier_indices`, `selected_delta_indices`, `witnesses`, `census`,
`status` and `mathematical_admission=False`. All nested values are bytes, tuples,
scalars or frozen dataclasses. `ParentClaim` fields are `tag/statement/receipt`;
`SelectedWitness` fields are `input_index/journal/bytes/sha256`.
`SealCensus` records input packet/witness bytes, wire/receipt bytes, maximum parent
receipt size and selected claims/frontiers/deltas/members/edges. No full witness
duplication outside the wire. Root owns tests; no imports, tests, native calls or
Git operations were performed by this author. Frozen dependencies stay unchanged.
