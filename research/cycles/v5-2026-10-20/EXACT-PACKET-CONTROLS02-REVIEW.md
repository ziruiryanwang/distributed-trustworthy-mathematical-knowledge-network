# Exact-packet controls02: independent source and selection review

2026-10-22. Reviewer: `storage_outcome_audit`. **PASS_SOURCE_REVIEW_ONLY; NOT RUN.**

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Root owns execution, adoption, installation and Git. This review neither launches
tests nor changes frozen product, predecessor source or evidence.

## Exact reviewed inputs

| Input | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/exact_packet/controls02.py` | 5699 | `b3e0411e88f3321e4eb96e7867f115ae632bc94f84dc6ebee7e8c02d2f052846` |
| `EXACT-PACKET-CONTROLS02.md` | 5202 | `71a714eecbbf485a28fa6e2c65c6454e8c62ba546a21e60782f97d4cc96f4b5c` |
| `Select-ExactPacketControls02.ps1` | 5035 | `14639ab3afcbd6ccced4cddc7a8d2323b31412df095492c4ba6299583f936981` |
| Frozen `software/v5/exact_packet/controls.py` | 34036 | `bd9a48119a3ae428e343a2d6061256026fc530cf0b281bf33e49e554214f2883` |

The adapter, note and selector were read completely. The original control source
and six selected product replacements were already reviewed in
[EXACT-PACKET-SOURCE-REVIEW](EXACT-PACKET-SOURCE-REVIEW.md). Their used bytes remain
unchanged. The predecessor's two errors and six passes remain as recorded in
[EXACT-PACKET-CONTROLS-OUTCOME](EXACT-PACKET-CONTROLS-OUTCOME.md).

## Review findings and disposition

The initial, unused controls02 draft (`6eee6a0e...`) incorrectly passed all five
endpoint dataclass fields to `OwnerEgressPolicy.endpoint`, whose exact schema
accepts only `host`, `port`, `tls`, `server_name`. Reviewer and author independently
identified this before selection or execution. Root confirmed the bytes were
unused and authorized correction. **That draft never received a passing review.**

The reviewed successor passes exactly those four contact fields to the real
policy API, then compares the complete resulting endpoint dictionary, including
`ca_file=None`, with the original. This fixes class identity without weakening
the actual expiring-contact endpoint comparison or changing its address/policy.

The fixture temporarily adapts only the `CompositeProvider` constructor's
`max_reply_bytes`: it requires the predecessor's 8 MiB value and invokes the real
class with 32 MiB. It restores the binding before requests and checks the exact
resulting provider type/value. This accommodates the unchanged group route's
16 MiB pre-dispatch reservation. Dispatch, HTTP, quota accounting and client caps
are not replaced or disabled.

Only the fixture method is overridden. The two inherited test methods, assertions
and teardown remain the original 04/05 methods. The original module is loaded
from the fresh source snapshot after exact size/hash checks. Its own `__file__`
still refers to the frozen snapshot, matching the inherited stage check.
Explicit replacement of `SELECTED` selects only 04 and 05; the six passing groups
cannot be run through this entry point. The output wrapper changes explanatory
metadata, not pass/failure calculations, observations or assertions, and keeps
the original fresh-file writer.

The selector differs from reviewed controls01 only in its fresh operation name,
controls02 entry and inclusion of the exact frozen predecessor dependency. It
retains the original runtime/map pins and finite envelope: 30 CPU seconds,
90 wall seconds, 256 MiB, one active process, 1 MiB logs. Its 138 source entries
resolve to the same 129 logical SDK modules (six replacements, 123 unchanged),
plus outer sources. It prepares selection data; execution is separately owned
by root. No product guard, mathematical admission path or old allocation changes.

## Boundary of the pass

There is no remaining source blocker in this narrow fixture-only correction.
This is not evidence that either test has passed. Actual outcome must independently
establish exactly two tests, no failures/errors/forbidden calls/unexpected loop
exceptions, exact source selection, and clean aggregate closure. Payload receipt
bytes are inert, so no mathematical acceptance or installed-facade claim follows.
No rerun of the six successful controls, proof generation or full-v5 claim is
authorized by this review.
