# Evaluator snapshot: independent saved-outcome audit

2026-10-20, core_release. **PASS for one completed execution capsule, not a
certificate or production GO.** No experiment/checker/proof was rerun.
Scope and assumptions remain those in [launch review](EVALUATOR-SNAPSHOT-LAUNCH-REVIEW.md)
and [mathematical binding review](EVALUATOR-SNAPSHOT-REVIEW.md).

Evidence root: `experiments/v5-local-checks/evaluator-snapshot-01`.
Selection `1bafa8de8d1c6ec8013ae22d3f5d0b27e3f8d3662249b88765998433a437cf73`
and config `e2130424c923a05f7305d252a0a4cd5b5ece793679161a36b8a2eaf811ef5250`
match saved inputs. All eight current/snapshot source pins match; runner final
rebinding and closure passed. Saved argv contains only prepare and snapshot,
using the selected unchanged host/image, exact witness and genuine BASE receipt.

Independent byte checks establish the 50,021-byte frame contains exactly the
50,017-byte accepted witness `8b840844`, with correct length prefix. The complete
184-byte journal equals the prior actual native conclusion byte-for-byte:
`e1b67f57ac9612a20b33231c2b71b2bd9260e6f4eb50fa9d0d761cd80408fbed`.
Both host calls exited zero. The reviewed host's successful snapshot branch
requires exact guest halt/journal and actual verified parent assumptions;
its output reports **51 segments, one assumption**, schema 3, binding
`ed0cee6bf8db60809e7c7b1d28b5c25e8b574b2ef98eeaaef053ce8335c331f9`.

Capsule: **10,004,276 bytes**, independently rehashed and schema-prefix checked,
SHA-256 `bda2fcf63908711953f701f7a802834b85287e77b456269277ee95d833107164`.
This audit does not deserialize every segment or promote the capsule/log into
portable mathematical authority. Later proving must validate its bound state;
final receiving must verify a genuine final receipt. No new receipt exists.

Original 2^25 cycle / po18 selection remains unchanged. Exactly two host calls,
zero proof calls, no retry or renewal. Outer exit zero, reaped direct child,
zero final active processes, closed Job, no cleanup error/termination request.
Known total CPU: **2.1875 seconds** = 1.828125 Job + 0.359375 total wrapper;
saved wall: **2.1157676 seconds**. Inner/supervision figures are not additive.

| Saved file | SHA-256 |
|---|---|
| RESULT.json | df8cacb701c32f7c233e43c51461206992b99bc9da776a75f22dd7784fffa947 |
| evidence/RESULT.json | 74182c5e14bdff01d1b486c00100012d70e201bb4c06e17228479b2ba7a0a0b0 |
| evidence/method.frame | fdd11d92b8c3f2f7479e3874018ba806612c1c66e0411ec3f555cb5e2bde3b0a |

The existing remaining complete graph is **154 host calls**: 51 segment + 51
lift + 50 join + one resolve + one finish. This is not a proof-time bound or
funding authorization. **Production remains DEFER**: the actual native-only
alternative costs 0.03125 Job CPU / 0.1229064 wall seconds, and no reuse demand
justifies the additional certification cost yet. Preserve this capsule without
reexecution; proceed to a higher-payoff core software obligation. Full v5 is open.
