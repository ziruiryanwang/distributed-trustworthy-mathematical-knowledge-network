# Preparation-only corpus: independent source review

2026-09-21. **PASS for bounded source compatibility**, not an execution
allocation, runtime success, sharing grant or mathematical acceptance.

Reviewed completely:

- `prepare_usefulness_corpus.py`: 9,543 bytes; SHA-256
  `526F410CFF8BD7EBFB90CCC23A87A8E622DC6AB084B700AC55B5A1F3C6D0E43D`.
- `PREPARE-USEFULNESS-CORPUS.md`: 5,761 bytes; SHA-256
  `293C388EA19978FFAEBC98BDB7FD874708AEF38DF3FDCB00C9FF5BB0D0EB9C8A`.

No material source blocker was found under the documented quiescent,
owner-controlled filesystem assumptions. The following contracts were checked
against the actual audited vocabulary01 installation, not inferred APIs:

- Full installation and package file maps, selected path bindings, helper and
  executable pins are checked before installed-module imports and again before
  completion. Added, removed or changed files therefore fail map equality.
  Each copied package is rechecked both immediately and at completion.
- `source_codec.read_package` checks foundation, typed content addresses,
  inventories, exact root object closure and `make_plan` structure. Its codec
  loader retains the hardcoded codec SHA-256 check. These are structural checks,
  not native mathematical acceptance.
- Metadata comes from each copied package via `symbol_index.describe_root` and
  matches all nine `Checker.metadata` fields, notably
  `semantic_target = semantic_ref`; descriptor and indexed symbol keys are
  derived from that same result. Distinct replay roots are required.
- Existing `peer_wire.build_view` and `load_view` check manifest commitments,
  framing/content digests, catalog roundtrip, seven-entry count and profile
  bounds. Neither constructor nor helper creates native proof evidence.
- Fresh nonoverlapping output, exclusive writes, path/reparse checks, bounded
  maps and reads, final output census, and the result/stdout two-level pinning
  form a finite preparation contract. Failure retains partial output; there is
  no automatic resume, retry, deletion, service or publication operation.

The author and reviewer coordinated a documentation-only correction: freeze a
random permutation of all seven packages before pinning/dispatch, without a
systematic lemma position. The implementation preserves the frozen CLI order
and required no change. Random order alone is not a complete consumer-blinding
design; consumer visibility and evaluator-only records remain separate gates.

Before any run, root must bind the actual seven independently qualified input
packages, complete installation map, frozen order, output path and supervisor
limits in a prospective allocation. Root must separately establish permission
to share selected bytes. Success requires an authenticated exit-zero receipt,
complete final pin checks, quiescence and resource accounting. The helper's
generous refusal ceilings do not replace that allocation's tighter limits.
File maps do not pin empty directories, ACLs, Python libraries or DLLs, and are
not hostile-race isolation. Receiver admission remains fresh and local; prior
producer evidence, metadata and availability cannot be borrowed as acceptance.

Reviewer performed only read-only PowerShell/.NET source inspection and hashes
plus this Markdown note. No Python import/execution, compilation, Lean, SQL or
product CLI was run. One initial diagnostic search guessed a nonexistent
`peer_package.py` path; actual contracts were then read from `peer_wire.py` and
the installed codec/checker sources.
