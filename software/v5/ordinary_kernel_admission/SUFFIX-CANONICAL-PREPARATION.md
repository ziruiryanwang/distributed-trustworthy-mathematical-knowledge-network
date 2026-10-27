# Exact-byte manifest successors

Independent review found a deterministic prelaunch defect in the two initial
suffix artifacts: apply_patch emitted a final newline, while ordinary strict
JSON forbids whitespace outside strings. Preserve those files and their review;
no owner, parser experiment or native operation used them.

Select file-only creation of fresh `part-a-canonical.json` and
`part-b-canonical.json` alongside them. Generate sorted compact JSON bytes with
no final newline through a standard-library script using exclusive `xb` output.
This emits data artifacts, changes no source file, imports no product code and
opens no owner database. Require identical row data/cuts/schema/semantic ID to
the independently inspected original manifest. Read back exact bytes and pins.
Do not overwrite the LF originals or copy any raw unit. New exact review/pins
are required before a separate intake selection.
