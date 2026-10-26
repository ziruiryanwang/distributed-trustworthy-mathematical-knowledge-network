# Producer-local validation reuse: independent source review

2026-10-26. Reviewer: `current_acceptance_challenge`.

**Disposition: SOURCE-CLEAR for the selected construction-local successor and
focused test design.** No unresolved equivalence defect found in this exact
delta under the stated unchanged-helper/nonmutation assumptions. This is not
runtime clearance, installed adoption, a measured speedup or successful Std
production/intake. Root owns those separate selections. The prior std-export01
failure, installed package and all used evidence remain unchanged.

This reviewer read the complete predecessor, exact successor delta/current
binding loop, full PROOF, portable reader, semantic identity definitions,
writer lexer/parser and unit/JSON validators. Work was source/file inspection
and hashing only: no product import, binder, build, test, native operation,
owner-state access or Git mutation. Only this REVIEW file was authored.

## Exact reviewed inputs

| Input | SHA-256 |
|---|---|
| This directory's `CONTRACT.md` | `3a2cb91a153d4bb92c6bab407497ffbde1ff1c3550d72e7b72ee4d4858554c7e` |
| Successor `baseline_bundle.py` | `e4b52c2f2e823cc98aa37c8cc7adb0cf79952def9c19b54d7072116a39fa19b6` |
| `PROOF.md` | `71881604daa93fec41a76f2f8107a25dbff817cf2e5472845b849de958bb71ce` |
| Frozen `ordinary_baseline/baseline_bundle.py` | `d5a9c13392e2de8b170cbaf4a9a27e4d1e5d99eb2714165848a640069fe42fce` |
| `ordinary_lean/portable_evidence.py` | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |
| `ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `ordinary_lean/ordinary_semantics.py` | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| `ordinary_lean/portable_candidate.py` | `29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331` |

Predecessor and helper paths above are relative to `software/v5/`. The five
predecessor/helper files were also independently hash-matched to their selected
installed copies in
`experiments/v5-local-checks/multi-source-package01/suite/assembled/package`.
Thus this argument does not silently substitute older source for current support.

## Exact delta and equivalence argument

Only `bind_writer` changes. The first `inspect_unit(unit)` remains. Its first
canonical unit encoding is retained as `unit_raw`, rather than discarded after
measuring its length. The subsequent full portable-reader call is expanded inline
with every check except the second inspection of the same unit. Measurement is
expanded inline with the same formulas, using the first census and unit bytes.
Later target/export calculations use the identically calculated local unit ID.
There is no new helper, public parameter or externally supplied cached object.

The central lemma in PROOF is valid for this boundary. The unchanged writer
parser returns only ordinary JSON lists, dictionaries with string keys, strings
and bounded unsigned integers. Its lexer and duplicate-key parser exclude the
numeric/token/object cases that could invalidate ordinary canonical round-trip
reasoning. After successful `inspect_unit(U)`, canonical encoding embeds that
exact U in the fresh envelope R. Successful strict decoding of R returns a unit
structurally equal to U. Under unchanged helper defaults, deterministic repeated
inspection would therefore yield the same census, and repeated unit encoding
would yield exactly `unit_raw`. No attacker-supplied census is inferred valid.

Induct over writer order. Both versions start with the same pinned 581-name
basis map. Given the same prior available map and measured sequence, unchanged
reference/collision checks produce the same ordered imports and raw envelope R.
The retained reader obligations and lemma give the same unit ID, binding-byte
count and complete measurement. Export and target IDs consequently agree, so the
next maps agree. The unchanged splitter, aggregate check and manifest constructor
then produce identical boundaries, raw evidence, manifest bytes/hash, targets
and final census for successful non-resource-refused execution.

## Skipped-reader and limit checklist

| Obligation | Independent disposition |
|---|---|
| Default reader limit type | Explicit `type(syntax_limits) is E.Limits` retained |
| Strict bytes, depth, numeric/string/UTF-8/canonical syntax | Full `E.strict_json(raw, PE.DEFAULT_LIMITS)` retained |
| Exact envelope keys/schema and semantic hex | Same checks retained after strict decoding |
| Complete unit/DAG/name/declaration/group validation | First `inspect_unit` retained; round-trip lemma justifies omitting only its duplicate |
| Import-array ceiling | Explicit default `max_imports = 65536` retained; not inferred from node or byte size |
| Import row arity, name validity and ID hex | Same `_array`, `name_key`, `_hex` loop retained |
| Exact import census and order | Same tuple equality against sorted duplicate-free external names retained |
| Portable ID | Exact SHA-256 of PE domain ASCII, NUL and the unchanged full raw envelope |
| Selected semantic and per-unit evidence bytes | Same measurement checks retained |
| Binding bytes and budget cadence | Same output-row calculation/checkpoint and ceiling |
| Nodes/names/edges/native-array bytes | Identical first census, decoded row/import counts and `len(unit_raw)+2` |
| Per-unit, batch and total limits | Same `_fits_batch`, `_total_bound`, splitter and manifest checks |
| Exact evidence locator | Same unit ID, raw SHA-256, raw length and `Entry` validation |

Writer/statistics bounds, full atomic groups, pinned inventory correspondence,
expected targets, forward/unbound-reference refusal and output collisions are
outside the changed block and remain. In particular, malformed unit structure
cannot acquire acceptance by skipping its second inspection: the retained first
inspection uses the same selected limits on an equal JSON value.

`_measure_parsed`, `_measure`, `validate_batch`, `split_units`, `make_manifest`
and every other function are unchanged. Their generic raw inputs still go through
`PE.read_evidence`; this is **not a peer-cache shortcut** or a change in mathematical
authority. Portable Evidence objects remain inert claims. Native checking and
receiver admission remain separate, unchanged obligations.

## Caveats and focused follow-up

The source argument assumes no hostile in-process/helper-global mutation and a
nonmutating budget callback. Existing API support for a callable callback is not
a sandbox for arbitrary hostile code. No cross-process cache is introduced.

All logical budget checkpoints remain, but elapsed/resource outcomes need not:
less work can finish where the predecessor timed out. Conversely, retaining the
unit encoding across envelope parsing changes live-object overlap. Neither lower
peak RAM nor a whole-workflow speedup is established. The exact source saving is
one duplicate unit inspection and one explicit duplicate unit serialization per
unit; writer/envelope scans and canonical checks, imports, hashes, output writes,
native extraction and recipient checks remain. Asymptotic class is unchanged.

Inlining reader obligations creates a maintenance coupling: future changes to
PE/evidence defaults, syntax, census or identity definitions require fresh review
and focused equivalence controls here. The exact helper pins bound this finding.

Before integration, root's focused tests should compare exact old/new output on
small ordered-dependency and full-group fixtures; preserve malformed, reduced
bound and budget-refusal behavior; and verify generic raw routes still invoke the
complete reader. A later saved-writer-only discriminator can be separately chosen
to address actual remaining cost. Neither a full old-binder repetition nor another
native export follows from this review. Do not count a future local construction
pass as independent mathematical grounding, useful growth or final v5 delivery.

