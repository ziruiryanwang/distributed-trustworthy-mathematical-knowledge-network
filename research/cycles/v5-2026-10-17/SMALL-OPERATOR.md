# Ordinary small-producer operator

2026-10-17, `memo_tests_review`; source implementation only, under
SELECTIVE-FRONTIER-SELECTION. No runtime, product import, test, build, proof or
Git operation. Frozen producer and predecessor evidence remain unchanged.

## Implemented seam

New `software/v5/aggregate_small/operator.py` accepts explicit `preflight` or
`run`, `--profile`, `--profile-sha256`, `--request`, `--request-sha256`, and
`--owner-report`. Use the selected isolated Python with `-I -S -B` and an
enclosing bounded owner; the wrapper does not provide its own process sandbox.
No hardcoded fixture paths, new allowance, automatic continuation or cap change.

Profile/request documents are absolute ordinary non-reparse files, at most
1 MiB each, exact SHA-256 pinned and duplicate-key checked. Imports must resolve
to the same source tree; the real constructor additionally validates all selected
producer, supervisor, build and runtime pins. Owner-report/sentinel are fresh
create-new bounded files separate from source, production output and protected
inputs. Existing parent directories are required; the wrapper creates no folders.

`preflight` invokes the actual `AggregateProducer(profile)` and `_request(request)`
exactly once. It never calls `run`, the native host or prover, and requires the
planned production directory to remain absent. Its report contains the selected
finite stage graph, full-missing-path envelope, prior allowance charges and actual
installation/request pin-byte sums. A valid quote is not funding, memory
sufficiency, receipt verification, proof completion or mathematical admission.

`run` invokes `owner.run(request)` exactly once. The existing producer controls
the requested finite prefix, reservations, first-failure stop and historical
charges. The wrapper references its durable RESULT rather than embedding a
potentially large duplicate. A successful prefix is not a completed certificate.

The wrapper closes an instantiated owner on every path and rebinds documents,
entry/source/installation pins and declared request pins (the complete derived
input map in preflight; the retained producer rebinds it internally during run).
Failure is preserved;
late report-write/rebinding failure writes a separate create-new finalization
sentinel overriding any earlier report. If no safe report location can be
established, it refuses without writing there and returns bounded JSON on stdout.
The outer owner must capture startup/import/constructor/refusal/exit costs.

## Review and next boundary

Source review must verify both no-dispatch preflight and exactly-one-run paths,
report collision/late-failure handling, loaded origins and request pin coverage.
No synthetic constructor is used by this entry point. Any focused controls and
the first real supplied-profile preflight need separate root selection. Actual
profiles/requests await a complete adopted BASE+FIRST capsule; this source does
not turn failed layout02 into usable proof input or qualify final v5.
