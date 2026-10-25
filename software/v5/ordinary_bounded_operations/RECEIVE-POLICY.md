# Explicit receiving dependency policy

2026-10-24. Source successor of
`software/v5/ordinary_authoring_offers/peer_api.py`. This note specifies the
changed local API contract, not a new certificate or mathematical acceptance rule.
The predecessor remains unchanged. Source review and selected execution are
separate gates; this note alone claims neither has passed.

## The consumer chooses before acquisition

Every `receive` configuration must include exactly one string field:

```json
"dependency_policy": "selected-unit-only"
```

The other supported value is `"bounded-closure"`. There is no default. Old
configurations lacking the field fail `PEER_RECEIVE_FIELDS`; other types or values
fail `PEER_RECEIVE_DEPENDENCY_POLICY`. These checks precede owner/custody checks,
contact-file reads, operation creation and network acquisition within `receive`.
An outer CLI may already have loaded its package/configuration and opened local
state before calling this API; the guarantee is not zero local CLI startup I/O.

Both policies retain the existing explicit parent root, exact selection binding,
unit/byte/request/missing-frontier/preflight limits and original operation grant.
Neither policy allows a provider's claim to replace independent admission.

## Selected-unit-only

1. Validate the requested parent context before peer I/O.
2. Acquire the selected preview and selected whole declaration unit. Bind their
   exact mathematical identities using the unchanged acquisition/preview checks.
3. Run the real owner's existing preflight on that unit and the explicit parent.
4. If preflight is `READY`, call the unchanged `owner.admit`. Admission independently
   checks its actual plan again; the policy creates no admission bypass.
5. If preflight needs premises, stop acquisition before the first ancestor locator
   or evidence request. Do not call `owner.admit`.

After normal cleanup and final allowance checking, step 5 returns:

- `status: "NEED_GROUNDED_PREMISES"`;
- `admission: null`, `mathematical_acceptance: false`, and
  `local_acceptance_available: false`;
- `acceptance_facet: "NO_LOCAL_ACCEPTANCE_MISSING_PREMISES"`;
- the checked `dependency_policy`, `parent_root` and selected `target`;
- `grounded_premises_needed`, containing exact encoded names and export identities
  from the owner's bounded preflight, plus the retained frontier/acquisition costs.

This status is a successful diagnosis of nonacceptance, not a proof that the
selected result is false. The list is the selected unit's current missing frontier,
not a claim that these premises exist elsewhere or exhaust their transitive
dependencies. No automatic retry, parent change, grant renewal or closure fallback
occurs. A caller may make a later separately authorized choice using its actual
available context and budget.

If the selected frontier exceeds its original cap, the existing
`PEER_MISSING_FRONTIER_BOUND` error takes precedence. It still occurs before any
ancestor request. The selected whole unit may contain multiple declarations or a
large proof; strict mode is not a theorem-interface-only download. Existing
grounded-parent inspection/restoration and successful admission costs remain.

## Bounded-closure

This explicit selection retains the predecessor's finite recursive acquisition:
preflight, locate missing exact premises, acquire missing units under all aggregate
limits, and preflight again. Only `READY` reaches unchanged admission. Every bound
still applies, including preflight iteration and no-progress refusal. This mode
is useful when a consumer consciously grants the work needed to ground a small
missing closure; it does not guarantee cheap cold acceptance in a huge network.

For either successful admission policy, `CHECKED` means new local native acceptance;
`REUSED_LOCAL_ACCEPTANCE` means existing local acceptance without a new check.
Both expose the selected target and policy. Earlier exact-byte custody is only
inert storage, not acceptance.

## Cleanup and partial effects

The strict missing-premise branch does not return early. It executes the existing
operation CPU accounting, owned-ledger close, acquisition/network reporting and
final original-allowance check. Shared ledgers remain caller-owned, their deadlines
can only narrow, and no grant is replenished. Cleanup, accounting, or final-budget
failure produces the ordinary `PeerFailure`/`FAILED` report rather than a clean
nonacceptance outcome. The policy, bound target and known frontier remain available
in that partial report when they were reached.

Selected preview/evidence bytes may already have entered inert local custody when
strict mode refuses missing premises. Those effects and charges are not rolled
back or hidden. If admission already returned an accepted result and a later check
fails, the original implementation's retained `admission` report is preserved;
`FAILED` must not be interpreted as reversal of a local mathematical commit.

## Scope of the improvement

Numeric caps previously limited work but did not express a prohibition on ancestry
retrieval: even a one-unit cap could permit an ancestor locator request. The new
policy expresses that prohibition directly. It is a predictable-cost refusal
boundary, not a solution to cheap successful arbitrary cold verification. No wire
format, semantic identity, Lean checker, imported foundation, global ledger or
trust mode changes. Hard controller resource containment still requires the
selected whole-operation launcher or an equivalent external process envelope.
