# Resolve the semantic refinement before implementing RC

2026-10-21, root. Fully read candidate decision
`324f42c1b3a5379ebaa5f1c337e90c4b02631678cb209cdf5d5a0834c02d4a13`.
The candidate is meaningfully different from the existing untrusted v4
assemblers: it checks a restriction of the current expression language instead
of invoking the full general checker. The typing/conversion and integration
obligations are explicit, but a design statement is not their discharge.

Select source/theory work only:

- Growth: RESTRICTED-COMPOSITION-REFINEMENT.md, constructive bridge from accepted
  RC terms/types/imports to the exact current conditional module relation and
  semantic member journal. Lean validity alone does not imply a particular
  checker accepts. Resolve imported transparent-type/signature closure and
  native-row witness construction; report a true obstruction if one exists.
- Release: RESTRICTED-COMPOSITION-REVIEW.md, independent challenge of soundness,
  actual work avoided and compatibility with ordinary module/aggregate clients.
  Coordinate directly with growth while retaining independent conclusions.
- Adaptive: finish the already selected sharing adapter review/actual audit.
- Root: choose the smallest implementation only after the above is resolved in
  principle; own the independent I+M sharing launch in parallel when reviewed.

The available base-I binary_congr is the first eligible premise. FIRST remains
uncertified, old A receipts are not silently accepted as A-RC parents, unsupported
conversion refuses. No checker implementation, compiler, profile sweep or proof
is authorized by this investigation. Do not restate the whole architecture;
answer the concrete refinement and interoperability questions.
