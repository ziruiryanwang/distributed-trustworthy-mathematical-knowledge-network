# Ordinary natural-number source interoperability: decision before implementation

Root, 2026-10-20. Source/theory only; no runtime, build, checker/image change,
new producer, Mathlib port or proof campaign is authorized here.

## Why this is central

A useful shared mathematical library must accept ordinary supported Lean source,
not only specially rewritten examples. The current selected `modules/source_rows.py`
(`60c7255d...`) rejects literal expression tags; canonical expressions have no
literal constructor and the checker policy disables the Nat extension. Ordinary
numeral notation also elaborates through OfNat and its selected instance.
This is a concrete interoperability obstacle, not evidence of a growth advantage.
The speculative SAT benefit construction is separately rejected before coding.

Current source map: distribution-coherent-01-input.json `1903bb44...`; installed
candidate `0fbbbc59...`. Follow this map and the selected AuthorLean build records,
not similarly named older native/AgentClient files. Predecessors stay immutable.

## Exact decision

Use `fun n : Nat => Nat.add n 2` as a source-level discriminator. Compare:

1. bounded exact lowering of native Nat literals into the already specified
   zero/successor representation, then ordinary unchanged fresh checking;
2. explicit canonical literal/policy extension, which would need new assurance
   and receipt relation/image selection rather than a silent format change.

Before choosing (1), establish native literal typing and definitional equality,
exact adopted/relocated Nat/zero/succ/add/OfNat identities and closure, source
correspondence through native export/reconstruction, and explicit expansion
accounting including depth/nodes. Handle only actual native Nat literals, never
reinterpret arbitrary overloaded OfNat instances. Large values must refuse
before expansion beyond existing bounds; do not waive safety or raise limits.
If source support is already present in a selected path, reuse it rather than
implement it again. If native defeq is not preserved under relocation, reject
the proposed shortcut and state the exact missing semantic obligation.

## Disjoint deliverables and stop

- core_growth: NAT-LITERAL-SEMANTICS.md, at most 90 lines, exact foundation and
  typing/computation/correspondence argument or counterexample.
- core_search: NAT-LITERAL-SOURCE-SEAM.md, at most 90 lines, actual selected
  frontend/export/source conversion map, smallest affected boundaries and bounds.
- core_release: independently challenge the combined decision after both notes;
  no repeated audit of the completed installed integration.
- root: reconcile and select a narrowly justified implementation only afterward.

This decision ends at one implementable semantics-preserving seam or one precise
obstruction. Do not turn it into another broad survey or a new proof framework.
Neither literal compatibility nor a passing arithmetic example closes full v5
or the remaining useful-growth obligation.
