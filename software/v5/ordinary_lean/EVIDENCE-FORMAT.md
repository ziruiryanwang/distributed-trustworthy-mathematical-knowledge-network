# Ordinary evidence identity and byte-reader API

`ordinary_evidence.py` is inert content processing, not a mathematical checker.
It never loads Lean modules, executes source, accepts a proof, accesses a network,
or grants a cache warrant. Source-only until root selects review and execution.

```text
read_evidence(raw: bytes, limits=Limits()) -> Evidence
strict_json(raw: bytes, limits=Limits()) -> parsed inert JSON
inspect_unit(unit, limits=Limits()) -> UnitCensus
name_key(originalName, limits=Limits(), semantic=True) -> canonical name bytes
export_id(profileID, unitID, originalName) -> 64 lowercase hexadecimal digits
basis_symbol_id(profileID, basisID, originalName) -> 64 lowercase hex digits
canonical_json(value) -> UTF-8 bytes
```

`read_evidence` is the external-byte entry point. Other parsed-object APIs are
for bounded locally held data, not substitutes for that reader. `Evidence.raw`
is the identity-bound immutable input. Its `document` is ordinary mutable Python
data, deliberately not an acceptance capability: a controller must not mutate
it and then attribute the mutation to the old ID. Re-read `raw` at a changed trust
boundary, or compare exact bytes. Successful parsing means neither proof validity
nor that any referenced object exists.

## Envelope and identity

```text
{
  "schema": "DMKN_LEAN_ORDINARY_EVIDENCE_V1",
  "profile_id": profileID,
  "imports": [[originalName, externalSymbolID], ...],
  "unit": ["DMKN_LEAN_ORDINARY_UNIT_V1", descriptor, expectedInventory]
}
```

Exact keys only. Names, descriptors and inventory use `EXPRESSION-FORMAT.md`
and `DECLARATION-FORMAT.md` without renaming. Imports sort by lexicographic
**canonical UTF-8 name bytes**, not dotted spelling or Lean name ordering. Each
distinct external referenced name occurs exactly once, without unused entries.

Let `C` be Python's existing discovery-compatible JSON encoding: recursively
sorted object keys, `ensure_ascii=False`, separators `,` and `:`, no whitespace,
no trailing newline, UTF-8, and no nonfinite values. For the format's legal
values this is exact, not merely a promise to normalize unknown input. Let
`H_d(x) = SHA256(ASCII(d) || 0x00 || C(x))`.

```text
UnitID = H_DMKN-ORDINARY-EVIDENCE-V1(envelope)
ExportID = H_DMKN-ORDINARY-EXPORT-V1([profileID, UnitID, originalName])
BasisSymbolID = H_DMKN-ORDINARY-BASIS-SYMBOL-V1([profileID, basisID, originalName])
```

All IDs are lowercase 64-hex strings; domains distinguish their construction.
A supplied hex value is not proof of its construction, let alone of mathematics.
The controller must compare every original name and symbol ID to an actually
warranted binding under its selected exact profile and basis. The profile itself
is selected outside this envelope and fixes policy and interpretation. No local
accepted-root or provider ID enters these identities: unrelated local extensions
do not rename existing evidence or exports. Metadata/proof variations may change
IDs conservatively; no theorem-equivalence deduplication is claimed.

## Census and deliberate limits of this layer

The census visits descriptor types/bodies and every claimed inventory type/body
and generated recursor RHS. It includes constants and projection structure names
in all serialized expression nodes, subtracting the distinct expected generated
names of this unit. Thus mutually generated members need no cyclic self-hashes.
Expected names remain claims: forged extra group names confer no accepted premise;
the actual kernel-generated name census and every output row must subsequently
match exactly. Single ordinary declarations have exactly their own expected name.

Binder names, universe parameter names and nonlogical `all` metadata are not
constant references. Structural inventory fields are shape-checked, not turned
into theorem premises. Native literals do not invent explicit constant nodes;
their standard builtin semantics must come from the warranted selected profile.

The scanner validates exact syntactic tags/arity, name and byte shapes, UTF-8,
parameter indices, backward edges, finite node/depth bounds and closed expression
roots, without constructing Lean expressions. It does not typecheck or implement
the Lean kernel. All serialized nodes are counted, including any orphan nodes;
the subsequent Lean decode/re-encode gate rejects orphan/duplicate/noncanonical
DAGs. Kernel generation then enforces declaration semantics. Inventory expressions
are still advertised claims until equality with actual checked output.

## Before the general JSON parser

The default raw limit is 8 MiB, JSON nesting 64, and integer tokens 20 digits
(also bounded by UInt64). The lexical pass rejects negative numbers, fractions,
exponents, nonfinite tokens, boolean/null syntax, mismatched brackets and excessive
nesting **before** `json.loads`. Arbitrary naturals instead use bounded magnitude
bytes in the ordinary expression format. Duplicate object keys are refused during
parsing; exact canonical-byte equality is mandatory afterward. Strings are opaque
to numeric scanning, and UTF-8/JSON escape correctness is checked by the parser.

Trusted callers can provide finite `Limits`, not peer-specified resource grants.
JSON depth is capped at 128 and numeric token length at 20 even in such a profile.
Transport must enforce incoming byte limits while receiving. These syntax limits
do not replace the outer aggregate network, CPU, memory, storage and wall budget.

Discovery may expose a committed advertised type preview. That commitment is
**not mathematical acceptance**. The later controller must bind the preview to
this exact unit/header, match warranted imported meanings, perform local checked
admission and compare actual outputs. No certificate requirement is invented by
this ordinary lane, and no identity function bypasses the acceptance gate.
