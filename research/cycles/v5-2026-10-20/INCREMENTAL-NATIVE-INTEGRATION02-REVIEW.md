# Integration02: narrow source correction review

2026-10-21, adaptive_audit. **GO for root's fresh bounded02 selection.** No
runtime, product import, test, proof or Git mutation. Used01 remains unchanged
and failed; its actual failure audit is `18f258cc`.

Reviewed fresh adapter `software/v5/incremental_native/integration02.py`,16068
bytes, SHA-256 `ea0269008128f774199d28c185cb4494564cac85cca88b2778307530ba9728ce`.
Read-only whole-file diff against used01 `d6445354` confirms only:

- Add `MAP_BYTES = 2805479`.
- Require the pinned map row to have both exact `MAP_SHA` and `MAP_BYTES`.
- Use that exact byte ceiling for its pin and read.

The failure audit independently read the actual map/input-row size2,805,479
and exact hash `d3519be1`; this change fixes that concrete preflight mismatch.
It does not permit arbitrary enlarged source/packet/proof objects or alter
product code, mathematical input, owner authority, checker limits or assertions.
The source note `c8f75e08` also records the remaining existing input bounds;
none uses the former map ceiling for a larger selected artifact.

Reviewed selector02 SHA-256
`ca3bf379bacec3008f40f5f9810d0412ad5ff99e7c62537a476fa6240e33bc1e` by complete
diff against reviewed selector01 `7a44b17e`. Only the adapter source/argv name
and fresh operation02 name change. All exact inputs/source counts/runtime pins,
CreateNew/freshness checks and90CPU/180wall/512MiB/four limits remain. It creates
new input/selection/output paths and cannot overwrite01. The selector passes
the same compatible closed schema to adapter02.

All unchanged constructor, pin-map, current-premise/native-hit, description and
cleanup reasoning remains in integration source review `636c65a4`; it is not
retested or relabeled as actual success here. Root must select and inspect the
new operation separately. Another failure would remain failure, without renewed
budget or hidden repair. No mathematical or growth outcome follows from GO.
