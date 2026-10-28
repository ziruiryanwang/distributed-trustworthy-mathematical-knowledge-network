# Read a formal candidate before acquiring its proofs

The offline viewer turns a saved `preview` report into a readable formal type
and exact symbol table. It needs no mathematical owner, Lean process, network
connection or proof closure. It is useful when a search finds an unfamiliar
declaration and ordinary source is not already available.

The displayed type is a claim. Only the existing independent receipt/checking
route can accept the mathematics. The viewer neither rechecks the report's
network history nor establishes that the type agrees with an actual proof.

## Use

Keep `view_preview.py` and `render.py` together. Select the approved package and
the saved report explicitly. Use an absolute fresh output directory whose parent
exists; no existing file is overwritten. For example, in PowerShell:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons\preview\view_preview.py' `
  --package 'C:\commons\package' `
  --profile-sha256 'APPROVED_PACKAGE_PROFILE_SHA256' `
  --report 'C:\commons-work\preview-01\RESULT.json' `
  --report-sha256 'SELECTED_SAVED_REPORT_SHA256' `
  --output 'C:\commons-work\view-01'
```

These are placeholders. The current local package selection is recorded in
`../ordinary_reply_capacity/ADOPTION.md`. The viewer reads only five approved
codec source files from that package. It does not validate the package's native
artifacts or approve a different toolchain. A digest identifies selected bytes;
it does not authenticate who produced them.

On success, read `TYPE.txt` and `VIEW.json`. The latter retains the input digests,
semantic/unit/export identities, original report PROFILE and selected current
PROFILE. An older report can be displayed with unchanged compatible codecs;
its historical claims remain historical data.

`TYPE_DISPLAY_COMPLETE` means the entire type and its reference legends fit
the fixed display limits. `TYPE_DISPLAY_INCOMPLETE` writes only `VIEW.json`,
including the reason and original root-node index. It writes no partial type
or partial symbol table. Inspect the original data or approved source in that
case; there is no automatic larger retry. Malformed or internally inconsistent
reports are refused before an output directory is created.

## Read the notation

All applications and universe arguments are explicit. `Sort(succ(u))` retains
its exact level expression; the viewer does not reconstruct notation such as
arrows, infix operators or inferred implicit arguments. The text is formal
display syntax, not promised compilable Lean source.

`#bN` denotes a fresh binder occurrence and `#uN` a declared universe parameter.
`#cN` refers to row N of the original `type_bindings` table. That index can help
select a binding for the existing inspection operation, but not all rows denote
ordinary exported declarations: some are fixed-basis symbols. Scope follows
the encoded de Bruijn indices, even when names repeat or DAG nodes are shared.

Exact names in the legend preserve typed segments and Unicode without
normalization. Printable names in the type are hints only. A full name containing
one segment `A.B` differs from the two segments `A` and `B`. Unusual characters
are escaped visibly, including control and bidirectional characters.

See `CONTRACT.md` for the scope and resource argument and `SPECIMEN.md` for a
hand-derived example with twelve outer binders. This interface improves access
to encoded types; no measured research acceleration follows from display alone.
