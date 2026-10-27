# Reuse above an installed library

This optional contribution setting avoids reconstructing already installed
library declarations while preparing a new proof. It is intended for an agent
that has a checked local parent containing received mathematics and an approved
Lean project that already imports an ancestor library, such as Std.

The ordinary contribution command gains one option:

```text
--authoring-frontier-root CHECKED_ANCESTOR_ROOT
```

Supply it together with the existing `--project-authoring` descriptor and its
`--project-authoring-sha256`. Keep the usual `--parent-root`, acquired target
triples, source body, output names and finite budget. The ancestor must belong
to this owner and its checked module plan must be an exact prefix of the parent
plan. The parent itself is also a permitted boundary. Without the new option,
the previous preparation protocol is unchanged. Other commands reject it.

For example, if the parent contains Std plus a received theory, select the
owner's checked Std root and approve a local project importing Std. Acquired
definitions above that boundary are reconstructed from their retained inert
evidence. Names encountered at the boundary are expected to exist in the
approved project. Their portable proof bodies are not fetched to traverse older
ancestry. Only names actually reached by preparation are recorded.

The expectation can be wrong. A demanded name missing from the approved Lean
environment causes that authoring attempt to fail, without a hidden fallback
or renewed budget. A same-name local definition can also have different semantics.
Successful authoring therefore does not grant mathematical acceptance: the
exported candidate is rebound and checked against the exact protected parent
before it can become an accepted contribution. This final check is mandatory.

The setting does not restore the original project's notation, instances or
elaborator extensions. Approved local imports remain executable support, and
peer source or binaries are never approved by selecting a boundary. Existing
budgets still apply, including 32 fetched groups, 4096 combined names, 1 MiB per
header/group and 4 MiB total request payload. Snapshot validation, installed
library imports and checking the new proof still cost resources.

The retained request uses `DMKN_OWNER_REQUEST_V3` and records the selected root
and reached name/identity labels. Completion validates the retained bindings
against the current protected parent. This metadata is an interpretation record,
not a certificate that the approved project has equivalent semantics.

Current validation status is recorded in EXECUTION.md and the actual outcome
notes. Source review and a successful helper build alone are insufficient to
claim the new workflow has passed its mathematical controls.
