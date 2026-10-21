# Natural-literal importer: independently inspected actual outcomes

2026-10-20, core_release. Root owns execution and adoption. Reviewer authored
controls; root and core_search independently reviewed them. This audit reads
saved evidence only and does not rerun tests or native work.

## Source clearance retained

See NAT-LITERAL-SOURCE-REVIEW.md `896ccdd4` for the full source argument and fixed
external-relative-name allocation gap. Selected importer `b9525df0` and controls
`2c3191fd` passed source review; no native checker, policy, foundation, frontend
or receipt-image change. Native adapter `61594c33`, Lean source `a87d47ab` and
native selector `8b73b9d5` also passed source review, conditional on the contracts.
No observed source-side reason requires a larger campaign or a new representation.

## Focused contracts: PASS

Actual directory: `experiments/v5-local-checks/nat-literal-controls-01`.
Selection SHA-256:
`a2deb4e5dd3a46c58ca5a80aec3b8b5188c740bffee627dc3f65abb48a736489`.
All seven source originals AND saved snapshots independently match that selection.
The outer result binds the exact selection and records exit0, reaped direct child,
closed Job, zero remaining active processes, no cleanup errors or termination.

Nine selected groups PASS with zero failures, errors or skips. They observe exact
0/1/2 constructor decoding; unchanged nonliteral/OfNat syntax; census-only behavior;
huge/malformed literal refusals; 24 exact group/recursor shape refusals; lowering
through type/body/rule paths; repeated occurrence charging; work/depth limits;
and output-byte refusal including long external aliases.
For the single numeral100 case, raw1418 bytes and expanded5849 bytes exceed its
selected1482-byte cap. The mapped external-reference output is33427 bytes against
a20000-byte cap. These are structural prospective-refusal controls, not evidence
that the conservative preflight accepts every otherwise encodable input.

Known cost is0.8125 CPU seconds =0.546875 Job +0.265625 wrapper, with
2.8027175 seconds outer wall time. No native, proof or network calls occurred.
The synthetic group deliberately lacks mathematical recursor correctness;
passing these tests cannot be described as mathematical acceptance.

Evidence SHA-256:

- controls-result.json: `53532049ddcd1a0422a3fc50159e181fee7fe0475bd809bc83728bc580342458`
- RESULT.json: `0393aa4e4c6d284be71ae24e4a170a4e0708d98dadb5556496bb0aad635c23f9`

## Real native follow-through

At the contract-audit checkpoint the actual frontend/fresh-checker call is
separately root-owned and not yet adopted here. Its outcome must be appended
from saved evidence. Source review alone does not establish native success,
public-client adoption, cryptographic certification, profitable growth or v5.

### Subsequent actual native outcome: PASS

Read `experiments/v5-local-checks/nat-literal-native-01` after terminal completion.
Its selection is `ac4110992554a14bfbb7bf33ab25fc0fdf84fd4312801d49915ab835b05803e8`.
All 13 selected source originals and saved snapshots independently match their
pins. No large retained-runtime hash replay or mathematical rerun was performed.

The saved Arithmetic.lean has selected hash `a87d47ab...`; raw original EXPORT
has hash `28e9da70...` and binds that same source hash. Its actual expression
row 254 is `natVal: "2"`, with 18 local declarations. The raw source is the
ordinary addTwo definition and addTwo_spec with explicit double-successor RHS.
Independently inspected normalized descriptors and body retain exact Nat.add,
OfNat.ofNat universe0 and instOfNatNat applications. Both literal occurrences
inside that selected numeral instance/application become two successor cells.
The theorem uses Eq at universe1 and the explicit two-successor RHS, not another
overloaded numeral. Its complete local closure occupies 13 groups.

The exact saved native input is 62,839 bytes with SHA-256
`28405b3609d66295a86475cedfab982faa7bffd6e40b20f997e0f17a523bc081`.
It has zero parents, rank0 and no residual Nat/String literal rows. The actual
unchanged native checker returned exit0 with matching input hash/length and
`CHECKED_CONDITIONAL_RELATION_NOT_ADMISSION`. Its 184-byte DMKNM002/version2
journal independently decodes to 13 groups, rank0 and module
`349e201e3ff12b35c6699fb2513f5d1723a7535920931d5f916df24bede7f132`.
Journal SHA-256 is
`253aea50b8e4d68c96d4b7eafc6db03d76654d5529e9bf434fbadeea638ba186`.

Frontend worker and checker both report reaped direct children and successful
actual return codes. The outer Job closed cleanly after four total processes,
with zero active processes, no cleanup error and no requested termination.
Known CPU is 4.484375 seconds = 3.65625 Job + 0.828125 wrapper; outer wall is
35.9836096 seconds. Its wrapper-supervision subcounter is not added twice.
This establishes actual bounded ordinary-numeral export and fresh checking of
the complete relocated extension. No certificate, verifier receipt, public-client
integration, later built-in-Nat bridge or profitable-growth result was produced.
Root may adopt this exact interoperability result without claiming completed v5.
