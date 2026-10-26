# One-payload package plan, not an execution selection

2026-10-26. `practical_library_route`. Source-only assembler complete; no import,
assembly, build, test, product/state opening, network or Git operation was run.
Root owns independent review, finite allocation, actual execution and adoption.

`assemble.py` SHA256:
`8067e7e862e5e3d6abd5513a30197f9bd167552f9223fd49fc0f263a0dec9e3c`.
It exposes `assemble(args)` with the following CLI:

```text
python -I -S -B assemble.py
  --source-root <canonical-root-or-source-snapshot>
  --base-package <approved-multi-source-package>
  --base-assembly <its-adjacent-original-ASSEMBLY.json>
  --output <fresh-disjoint-directory>
  --wall-seconds <finite> --cpu-seconds <finite>
```

`--successor` optionally supplies an explicit reviewed source path; otherwise it
is `source-root/software/v5/ordinary_binding_reuse/baseline_bundle.py`.
`--successor-sha256` defaults to the fixed reviewed `e4b52c2f...fa19b6`; both
the selected value and actual bytes must equal that complete source pin.
Direct `assemble(args)` callers supply `successor=None` and that full hash when
using these defaults, alongside the six required arguments shown above.

The helper, original PROFILE/ASSEMBLY/INSTALLATION and original binder are fixed
to the pins in INTEGRATION.md. The helper provides reviewed low-level file
primitives; its specialized assembler is never called. No product module loads.
Original root, selected sources and destination are checked for ordinary paths,
redirects/links and overlap. The old 154-file map is fully authenticated before
copying and rechecked before committing the new PROFILE; sources are immutable
owner-controlled inputs, not concurrently hostile writable files.

The sole payload substitution is `reference/baseline_bundle.py`. Every copied
file is new/exclusive, size-bounded during copying, flushed and rehashed. All 117
auxiliary roles and 154 total paths remain. Exactly binder plus PROFILE change;
152 files remain exact, including installation and eight historical documents.
PROFILE is committed last. External `ASSEMBLY.json` records the entire output
map and exact inputs; failure retains partial files and never retries or cleans.
A saved receipt alone is not successful process closure or mathematical authority.

Minimal later checks, selected by root: one actual assembly with its complete
two-difference assertions, optionally wrong successor hash and existing-output
refusals before output creation, then one direct unchanged public query preparation
with the new PROFILE in fresh diagnostics. No fake-package suite, native rebuild,
native Std export, archive repack, owner reopen or proof operation is needed.
The current compatibility-map preparer is deliberately not extended and rejects
the changed binder; use explicit public launcher arguments for this load check.

Preserve all frozen packages, archives and failed Std evidence. The source map,
preparer compatibility and fresh distribution remain separate future work, not
claims made by this one development-package overlay.
