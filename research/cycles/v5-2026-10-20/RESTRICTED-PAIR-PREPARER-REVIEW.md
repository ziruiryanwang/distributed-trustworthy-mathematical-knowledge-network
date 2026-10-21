# Same-target RC/general preparer: independent source review

2026-10-21, growth. Disposition: **PASS for this pure preparation boundary**.
This is neither an actual paired execution nor a proof/cost/growth result.
No product import, test, compiler, guest, proof or Git operation was performed.

Reviewed all 9,380 bytes of
`software/v5/restricted_composition/prepare_execution.py`, SHA-256
`fd184d7be0ca6eaa139a4b79764ac435c9e2036fea9116d591701d85a192e71d`,
and the author's execution-preparation checkpoint `ce8cb856`. Also inspected
the retained fixture generator, original-witness emitter path, native control
runner/differential, aggregate encoder/bindings, RC wire/census/aggregate
reading, and relevant unchanged snapshot-host preflight/verification logic.

## The comparison being prepared

Let `f` be the exact four-field fixture saved by the adopted native controls.
Let `R = f.first` and `W = f.first_witness`. The selected fixture generator
`b6f2014319b97b94b04ac9a8caf4068031f7f0e4a854a00aff596d6c47b9e51d`
constructs `W` by emitting the actual proof expressions of `R` into the
original row representation, using the same local specification, image,
rank and opened parent declarations. It does not choose a cheaper alternate
proof for the RC arm or reconstruct a new comparator here.

The preparer binds the full raw fixture digest, extracts these saved values,
requires `R` to equal the generator's exact first context-transport frame,
and explicitly compares the shared W/R fields. That first frame has four
universes, sixteen binders and the three intended binary-congruence uses.
It selects neither the second theorem nor the earlier historical FIRST.

The native differential additionally checks both relations and requires equal
complete conclusion journals and ordered parent journals. That equality alone
would not prove identical proof syntax: the exact-proof correspondence comes
from the pinned fixture generator and its emitted saved `W`. The caller must
therefore bind `fixture_sha256` and `fixture_bytes` to the adopted inner control
report and retain its selected generator/source lineage. A caller-chosen hash
is not adoption. This obligation is explicit in the pure API and must be
checked again in the enclosing matched-pair adapter's review.

## Exact wire and header correspondence

There is one genuine fixed-I base receipt, one exact base frontier, one newly
checked delta and one new target. Parent journal and receipt SHA-256 values
are fixed; the original typed general image is fixed to `9d5072a6...`, and
the RC image must be a distinct nonzero actual adopted image. No nonexistent
first-RC receipt or old aggregate-image assumption is introduced.

The retained encoder's one-arm layout independently gives these byte ranges:

| Bytes (zero-based, inclusive) | Meaning |
|---|---|
| 0–11 | scheme magic/version |
| 12–43 | aggregate image |
| 44–59 | four counts, each one |
| 60–244 | fixed-I tag and 184-byte parent journal |
| 245–440 | claim index, same journal, member index zero, empty sibling count |
| 441–624 | exact new 184-byte target |
| 625–628 | witness length |
| 629 onward | complete canonical witness |

The preparer verifies these lengths/counts and complete payload slices before
changing only the RC scheme prefix from DMKNAI02/version 2 to DMKNRC01/version 1.
It compares graph bytes 44–624 across both arms. The remaining differences
are the expected aggregate image, witness length and proof representation.
There is no mutable-global encoder patch or hidden trailing payload.

Both predicted output headers commit the same byte-sorted base/target members,
the same membership root, maximum rank one, seal height one, foundation and
policy. The exact header comparison permits only image bytes 12–43 to differ.
Both member openings are checked against both inert headers. Prediction and
membership hashing do not confer mathematical or receipt authority.

## Bounds and execution obligations

The raw fixture is bounded to 4 MiB before parsing. The RC value traversal
counts occurrences, including repeated structure, with the same native root
depth convention: at most 32,768 JSON nodes, depth 64, unsigned 64-bit integers
and 256 KiB canonical frame. The general witness has a 1-MiB canonical bound.
The preparer does not reproduce trusted inference or claim to be a hostile
source sandbox; its input is an exact already adopted finite fixture.

The enclosing adapter must still:

- bind both images to actual build/assembly results and use the matching host;
- give each arm the identical retained base receipt and predicted matching H;
- include preparation and execution costs without counting shared work as free;
- require each host's own native preflight, genuine receipt verification,
  actual guest claim/journal equality and clean bounded termination;
- preserve the predeclared 75% padded-row, 64-po18-segment and CPU-nonregression
  screen, without converting a single-pair timing into statistical evidence.

The unchanged host explicitly performs those mathematical/receipt checks;
this source review does not assert the future adapter invokes them correctly
or that either arm will succeed. No material defect was found in the pure
preparer. A source-review PASS does not select a launch or fund a proof.
