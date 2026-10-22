# Exact-packet controls02: two fixture corrections only

2026-10-22, storage_launch_review. Source-only successor; **NOT RUN**.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root owns the separate finite selection and any execution. No product source,
used control, evidence, installation or Git index is changed by this note.

## Preserved failure and bounded decision

Controls01 remains failed: eight attempted, six passed, two errors, no assertion
failures. Group04 constructed an expiring contact with the wrong Endpoint class;
group05's provider quota could not reserve the group route. These are diagnosed
fixture defects, not successful product tests. See the independent actual audit
[EXACT-PACKET-CONTROLS-OUTCOME](EXACT-PACKET-CONTROLS-OUTCOME.md).

The frozen predecessor is `software/v5/exact_packet/controls.py`,34036 bytes,
SHA256 `bd9a48119a3ae428e343a2d6061256026fc530cf0b281bf33e49e554214f2883`.
Its failed evidence directory `experiments/v5-local-checks/exact-packet-controls-01`
is untouched. Passing groups01/02/03/06/07/08 are **not rerun**.

New source `software/v5/exact_packet/controls02.py` imports that exact predecessor
only from the fresh operation's root-owned source snapshot, after exact size/hash
and selection checks. The two inherited test bodies and teardown remain byte-for-
byte the original methods. Only `fixture` is overridden. Its original eight-group
entry point is not invoked; `main` receives the explicit04/05 selection.

## Corrections and why they are sufficient in principle

1. The returned fixture endpoint is reconstructed by the actual
   `OwnerEgressPolicy.endpoint` public API. Its complete dataclass field dictionary
   must remain equal. The inherited expiring-contact constructor now receives
   `transport.http_provider.Endpoint`, matching its policy validation rather
   than the distinct `http_provider_receipts.Endpoint` returned by server start.
   No endpoint equality check, expiry check, policy or acquisition is weakened.
   Source review caught an extra `ca_file` field in the initial unused adapter;
   the corrected adapter passes exactly the four fields accepted by the policy,
   then compares the complete endpoint including `ca_file=None`. No control
   execution or selector preparation preceded that source correction.
2. A fixture-construction-only adapter changes the explicitly supplied provider
   `max_reply_bytes` from8MiB to32MiB and calls the original real provider class.
   It refuses an unexpected predecessor allowance, checks the resulting exact
   provider type and32MiB value, and restores the constructor binding before test
   requests. Dispatch, reservation arithmetic, actual sockets and quotas remain
   real. The `/v5/modules/group` route reserves16MiB before dispatch even when
   the actual group is tiny;32MiB leaves headroom for the other finite replies.
   This is a cumulative/reservation allowance, not32MiB of actual transfer or
   memory. Client limits and all test assertions remain unchanged.

Both corrections apply to the two fresh test fixtures. Group04 does not need a
group-route reservation; assigning the same finite provider ceiling does not
relax its unchanged client-budget assertions. Group05 already builds its own
canonical controller endpoint; field-preserving normalization does not change
that source descriptor. No product behavior is stubbed by either correction.

## Selection, evidence and trust boundary

Root's `Select-ExactPacketControls02.ps1` selects138 source snapshots: the129
base rows, six unchanged exact-packet replacements, root runner, frozen controls
and the fresh controls02 entry. The authoritative base remains
`distribution-managed-storage-01-input.json`,2813368 bytes/SHA256
`a629df82718f6a9d0560cacbfdc459739c15a56a1f2a46dd87929a1db51c22a4`.
The inherited stager still checks and copies exactly129 selected product sources.
No other dependency is introduced. The CLI remains `--output <fresh output>`.

The inherited main retains its selected-loopback-only dialer, real HTTP/SQLite,
subprocess/native-verification refusal guards, isolated interpreter requirement
and fresh-output writer. No receipt is genuine; mathematical acceptance remains
false. This operation is not an installed facade or certificate admission test.

The final report keeps `exact-packet-controls-result.json`, changes only its
metadata to schema `DMKN_V5_EXACT_PACKET_CONTROLS_V2`, identifies exactly04/05,
records both fixture corrections and predecessor failure, and removes the
irrelevant higher-facade scope. Counts, assertions, errors, success calculation,
observations and source census come unchanged from the inherited runner. A fresh
failure remains a failure; no prior result is rewritten or combined into a
fabricated all-eight success.

Prospective success: both inherited groups pass, no forbidden calls or unexpected
loop exceptions occur, real resources close, and the root Job/evidence audit
confirms the exact selected bytes and clean closure. Root's separate controls02
envelope is30 CPU seconds/90 wall seconds/256MiB/one active process; it is not a
new proof campaign. Actual execution and independent outcome audit are pending.
