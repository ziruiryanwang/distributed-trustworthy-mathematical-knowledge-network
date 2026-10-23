# Complete a contribution whose library dependencies were missing

This successor adds `owner.py complete` to the project-aware ordinary package,
including the [discovery-resilience change](../ordinary_resilient_package/README.md).
It is an integration step toward v5, not the completed public release. Source
review, file-only assembly and seven focused native-free control groups passed.
Actual completion qualification is separate. The license remains undecided.

## Purpose and boundary

A source contribution can elaborate successfully yet reference imported library
results absent from its selected commons context. Instead of reauthoring it,
retain its inert `candidate.json` and supply complete inert declarations for the
genuinely missing names. `complete` checks the supplement and the original new
declarations together through the same receiver as ordinary contribution.

The supplement is not an assumption list or a compiler-success receipt. Its
definitions/theorems must contain the required bodies/proofs. Its selected targets
must equal the candidate's actual missing set. All existing boundary identities
must match the protected selected parent. Supplemental units precede the original
units, whose canonical contents and claimed identities are preserved.

No provisional supplemental result is installed as an accepted fact to make the
consumer pass. Only one actual combined native admission can establish acceptance.
Neither a correct hash nor a well-formed plan establishes mathematical validity.

This command **does not yet generate the supplement**. The existing private
installed-library extractor is being integrated separately. It does not import
an arbitrary project, run Lake, download dependencies or execute peer source.
Current support is explicit inert completion, not full Lean-project interoperability.

## CLI

Use the same runtime, catalog, custody, store ID, resource and profile arguments
as [the ordinary owner](../ordinary_package/README.md), with operation `complete`.
Add these arguments, using absolute paths:

```text
--parent-root <the-original-selected-local-root>
--candidate <retained-candidate.json> --candidate-sha256 <exact-hash>
--supplement <complete-missing-declarations.json> --supplement-sha256 <exact-hash>
--prepared-bindings <original-prepared-map.json> --prepared-bindings-sha256 <exact-hash>
--output-names <original-target-names.json>
--output <fresh-result-directory>
```

`prepared-bindings` is a JSON array of `[structured-name, exact-export-id]` pairs
from the original authenticated preparation, not a peer's name-to-ID guess.
The original contribution retains its preparation in `owner-request/header.json`
and numbered group files; a public conversion helper is not yet included.
Output names use the same structured Lean-name encoding as `contribute`.
Do not pass source, acquired-target or project-authoring flags to `complete`.

All three input hashes and basic data bounds are checked before opening the owner.
Semantic candidate checking occurs after open; normal recovery may therefore
settle an interrupted earlier operation before a later semantic refusal.
There is no automatic choice of latest parent or silent rebase.

The current public profile permits at most 32 new units/targets, 4 MiB combined
candidate-plus-supplement input, 4 MiB evidence, 131,072 expression nodes and
4,096 selected names. These are finite local operation limits, not a claim that
arbitrary imported mathematics has a small closure. A larger operation requires
an explicit future interface decision, not silent cap renewal.

On success, keep the returned `local_root`, exact target IDs and evidence/previews.
Existing publication and serving commands can use them. An error after admission
may still leave checked mathematics committed; the report retains that acceptance.
Do not infer rollback from a failed terminal report. Original input files are not
rewritten, and successful prior authoring is not rerun.

## Source and assembly

`library_completion.py` is a pure planner reusing the existing binder twice;
`completion_api.py` connects it to existing preflight, admission and retention.
The second bind uses the real protected parent, never a fabricated accepted map.
Repeated bounded parsing/checking is accounted work, not a zero-cost conversion.

The file-only assembler layers over the project-aware/resilient package. Two
entrypoint files change and two Python helpers are added; 114 payloads, including
the native checker, project authoring and peer implementation, remain unchanged.
No Lean rebuild or owner-state copying is performed.

The assembled profile is
`82ca3a098fd7a51a4c0246bbddf8003d01557374411b5361fd5c7b3d7f6b9680`.
It has 118 payloads totaling 36,705,510 bytes, plus PROFILE and ASSEMBLY metadata.
Assembly took 3.84 wall seconds / 2.016 known CPU seconds and closed cleanly.
External supported Windows Lean 4.34.0/Python 3.14.6 runtimes remain required.
This is not a hermetic or cross-platform distribution claim.

The seven control groups exercise the real pure planner and explicit mocked
coordinator/CLI boundaries, not Lean acceptance. They passed in 1.56 wall seconds
/ 1.344 known CPU seconds with clean closure. The first harness failed before
any group because its CLI loop shadowed a helper; that failed run and its cost
remain preserved, and a minimal separate harness corrected it. No product
change or repeated native proof campaign was needed.

See the [independent source/assembly review](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-COMPLETION-AND-FAILURE-REVIEW.md)
and [planner invariant](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-LIBRARY-COMPLETION-IMPLEMENTATION.md).
Scratch authoring modules with assumed handles remain unsuitable for distribution
as ordinary proof-complete Lean libraries. Conventional package sharing is still
preferable when it serves the same assurance/usefulness endpoint more cheaply.
