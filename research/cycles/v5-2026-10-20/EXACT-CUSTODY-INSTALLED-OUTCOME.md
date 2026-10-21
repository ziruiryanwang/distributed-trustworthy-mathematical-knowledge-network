# Installed exact custody01: independent failure audit

2026-10-20, `adaptive_audit`. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

**FAILED, preserved and charged.** The owner adapter fails at `q-start` with
`StructureError: JSON_DECODE`. The selected three-role, same-reader body
acquisition/admission/import boundary is **not qualified**. P and Q actually
started and closed normally; R, the reader, mathematical issuers and temporary
trust domain were never created. This is a narrow adapter parser mismatch,
not evidence of a product mathematical failure or resource exhaustion.

Operation, relative to `product-local/v5-distribution-body-custody-01`:
`custody-integration01-operations/installed-exact-custody-01`.
Root supplied terminal notice for session95388 before this review began.
Only saved evidence, source and read-only file comparisons were used. No
runtime, import, reproducer, test, selector, proof or build was executed here.

## Exact identities and source evidence

| Artifact | SHA-256 |
|---|---|
| Selected request | `dc3238e67e7f99312cd739ce37962a658c7bc9dd08c933263fd878113fb66821` |
| `plan.json` | `f99db4f32d82f3ca748cb5eaf603c90a234b2d379095cd31a4280e9d6806da2e` |
| Owner adapter, source/request copy/snapshot | `d3ca25ce8426a7efdd5cf4071b19436ee4722a1d34e438d5e36f0ea4554791ab` |
| Outer `RESULT.json` | `620d006bc6aa7275b6efe16f7bbbce81b5b7e746926b54a897a420e5ca199ce7` |
| `BOOT-FAILED.json` | `00698c5e9f27b0c3c240a3b1c42af6b079975ee9f789fea5066adbe0e2023ddd` |
| `command/stdout.txt` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `command/stderr.txt` | `ef488ff4d6a35c19b6490e885e0c9e4ece60d9be638f0d651af148ad30595a36` |
| `work/exact-custody-installed-result.json` | `30f69485fc40762a8df706175152369aca175190c9c4c44c39ea5fd5d7a5e312` |
| `work/q-service/service-ready.json` | `d7a8fcd325b9a2c9401ba0dc47629d43b611c6274ba28799ddfa812a77af2a42` |
| `work/q-service/service-result.json` | `092e66c838949073cb6ff858539665a8ef819207f0633deb3b842c26bb96b887` |

The exact release remains
`8e93486cadb5806d6470d7a8920803a9a4bad39260dd72f3be3498f699eeeb1e`;
its prior build audit `9d527a47` and structural controls are reused, not repeated.

The plan has exactly **115 selected source files / 1,435,227 bytes**: all 114
installed SDK sources plus the owner adapter. Independent hashes and lengths
agree for every source and saved snapshot; all SDK entries match the selected
release map. The snapshot census has no extra or missing file. Both P/Q saved
Node source maps agree with all 14 selected MJS source hashes and point to the
actual run snapshot. Their role pre/post pins agree. The retained packet is
658,554 bytes, SHA-256 `6998ba92d064c8ce790192a434655d4b99bf0e7018f422ec24be757de55db2eb`;
foundation is 23,313 bytes, SHA-256
`736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`.
Both were independently rehashed and size-checked.

There is **no successful `BOOT-RESULT.json`**. The nonzero owner return happens
before the boot code's final imported-origins/snapshot/runtime report. The exact
snapshots and pinned-loader source establish the selected code boundary, but
must not be relabeled as a successful actual BOOT-origin report or six-module
live-issuer assertion. Those later assertions were not reached.

## Precise failure cause, without rerunning it

The adapter reads Q's operational readiness document with
`modules.codec.parse_json`. Its saved readiness file is complete JSON containing
fractional clock values, including `deadline: 2210785.6237987` and
`outer_deadline: 2210979.5085862`.

The exact snapshotted mathematical codec deliberately sets
`parse_float=bad_number`; that raises `NONINTEGER_JSON_NUMBER`, which its decoder
wraps as `JSON_DECODE`. The ready assignment therefore fails before `q_ready`
is retained in the owner report. This source/data incompatibility is sufficient
to explain the saved primary failure; no timed reproducer or memory investigation
is necessary. A mathematical canonical codec is the wrong parser for this local
operational clock document. The service writer is synchronous on the same event
loop, so no partial-write race is required to explain this outcome.

Outer stderr is the complete 941-byte boot traceback ending in
`CLIENT_OWNER_NONZERO_OR_INVALID_RESULT`. That is the consequence of the owner's
failed return, not a replacement diagnosis. `BOOT-FAILED.json` reports the same
wrapper failure; the precise primary error remains in the owner result.

## What actually ran, and what did not

P's seeded store has 13 groups / 16 declarations / 10 bodies / 3 modules, one
indexed export and one retained packet. Q has one group/declaration/body/module
and no index or packet. The selected P body row is absent and Q's exact body
read-back succeeds. These are structural observations, not mathematical warrants;
P's retained packet still contains the body in another representation.

P's loopback HTTP/V1 location service starts. Q's actual V3 advertised service
boots to P, reads its selected body, and dispatches one body-route hint under
the exact configured body domain. The recorded dispatch has eight events and
`HINT_DISPATCHED_UNACKNOWLEDGED`; it does not prove remote placement. No index
route is advertised by Q. Q completes its original **90-second** service,
four health observations, and clean normal shutdown. Its standalone saved result
equals the embedded owner-report result.

P and Q each received **zero HTTP requests**. There was no reader query,
descriptor acquisition, one-use capability, body GET, same-reader closure,
receipt verification, native admission or imported context. The report stops
before P's selected index publication and before trust/client setup. The requested
R workspace and trust-domain paths are absent on disk. `domain_created=false`
and `domain_withdrawn=false` mean **no domain existed to withdraw**, not a leaked
active adoption. Likewise the false reader/client/nodes-completed flags reflect
unreached success milestones, not by themselves failed cleanup of a live R.

Consequently no conclusions about preserved reader ownership/maps/deadlines,
prepaid body/query budgets, Q's one GET, retained mathematics acceptance or
no-ancestral-proof-byte import can be drawn from this run. No new proof or
authoring work occurred. The wrapper's `mathematical_acceptance=false` remains
correct.

## Actual closure and diagnostic scope

P's recorded raw stderr is exactly 884 bytes and one terminal JSON line. Decoding
its saved hex yields the same semantic object as the retained parsed terminal:
`LOCATION_IPC_CLOSED`, sequence 1, zero active transport connections and no
mathematical acceptance. Its channel has exit 0, closed=true, channel_failed=false,
forced_termination=false, actual runtime pre/post reports and equal role pins.
P HTTP has active=0, requests=0, failures=0 and reserved reply bytes=0; its HTTP
and workspace closure flags are true.

Q's public result is PASS with location/HTTP/workspace closed and no cleanup
errors. Its location channel has exit 0, closed=true, channel_failed=false,
forced_termination=false, actual runtime pre/post reports and equal role pins;
final public location status is STOPPED with zero active transport connections.
Its reported raw-child stderr count is **884 bytes**. The public API does not
expose those raw bytes: this audit does not claim empty or independently parsed
Q stderr. That predeclared observation limit is unchanged. No R log exists,
because no R child was created.

The outer Job confirms child exit 1, direct child reaped, Job closed, active
processes 0, total processes 4, terminated processes 0, no cleanup errors, no
termination request and no final supervisor error. Peak private Job commit is
**307,253,248 bytes**. The owner report also has no cleanup error. Closure passes
within this failed operation; it does not change FAILED into qualification.

## Charged cost and disposition

- Inclusive Job CPU: **32.484375 seconds** (15.4375 user + 17.046875 kernel).
- Separate outer-wrapper CPU: **6.65625 seconds**.
- Known total CPU: **39.140625 seconds**.
- Outer wall: **123.0908789 seconds**.

Bootstrap CPU 5.921875 seconds is included in outer-wrapper CPU; nested
supervision CPU 0.640625 is likewise not additional to it. Child
wall-through-cleanup 122.98438700009137 seconds is nested. Pre-clock interpreter
startup is explicitly unmeasured, not zero. Original ceilings remain
150 CPU / 300 wall seconds / 512 MiB / six processes and 1 MiB per log. The run
did not exhaust these limits and no cap extension follows from the failure.

Preserve01, its source, state and full charge. The central installed boundary
remains unqualified. A fresh source-reviewed adapter successor may correct only
the operational parser and use fresh paths; the failed allocation must not be
restarted, rewritten or relabeled. Root owns any subsequent selection. No product
rebuild, mathematical-codec weakening, trust adoption or v5-release claim is
justified by this audit.
