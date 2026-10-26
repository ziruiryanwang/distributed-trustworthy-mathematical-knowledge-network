# Investigator file-only test source review

2026-10-26. Independent review by `received_vocabulary`. **SOURCE PASS after one
narrow pre-write output-path correction; no test or product execution occurred.**

## Reviewed selection

| File | Bytes | SHA-256 |
|---|---:|---|
| `test_selector.py` | 7029 | `e008d36f84b3b76b541974dad4798a7ea04c910590a069eb42564c88f7ea4324` |
| `test_bundle.py` | 7660 | `c09bc09e76cde3c28796e0797fc294f1fc736ccbf35c26e97015d1c1861ae372` |
| `TEST-PLAN.md` | 3278 | `e7ab37bade7ccb2e3c6dc805e8c9089f9ca046b0bf5794ce00bcac6a4abe9f6e` |

Both Python test files passed independent `ast.parse` and inert `compile` using
isolated Python with bytecode disabled. Neither compiled object was executed or
imported. The final corrected `test_bundle.py` was reread completely and both
tests were independently parsed/compiled again. Exact execution selection and
freeze remain root-owned.

## Resolved finding

The initial `test_bundle.py` (`6f9cce92...`) created its top-level output after
only lexical `is_relative_to`, existence and `parent.is_dir` checks, allowing a
directory write before stronger rejection of `..` or redirected ancestors. Root
corrected this before execution: the pinned file helper now validates the fresh
output and existing ordinary parent before the first `mkdir`, followed by the
selected subtree check. The helper rejects traversal, UNC/device paths, invalid
components, symlinks/reparse points and unexpected path kinds. The enclosing
launch must still select exact ordinary input/output paths and protect inputs
against concurrent modification. No unresolved test-source finding remains.

## Reviewed behavior and boundaries

- The six bundle groups match the plan: one pack, exact old/new payload comparison,
  one fresh relocated public verification, five pure manifest refusals, a separate
  extra-file refusal, four current-guide link closure and the nine selector cases.
  The successful extraction is finally recounted against exact archive bytes.
- The selector compares the exact three changed source roles against the old map,
  refuses each old/new mixture and the old map, and explicitly preserves the
  separate native-artifact approval boundary. Its actual preparation checks all
  45 source files; the counterfeit changes one actual source byte. Wrong profile
  and wrong actual source must refuse before their output leaves exist.
- The only proposed operational subprocess is the relocated file-only verifier.
  The pinned request preparer's `init` branch validates future catalog/custody
  metadata and writes inert arguments/limits/receipt; it neither creates those
  state directories nor imports or invokes product/native code. Real package
  data remains read-only. Synthetic writes stay under fresh test children; the
  top-level path correction closes the identified pre-write gap.
- The reused frozen test helper is
  `17cd0c44568ac347c4013b1e1564afb7bd92441ced4de5dae08fda3af6dcb66a`.
  Only its generic bounded read/archive/extract/census/CLI/refusal primitives are
  reused, not its main or predecessor cases. Its 110-wall/45-controller-CPU
  allowance starts on import and is not renewed. The proposed outer
  120-wall/60-inclusive-CPU/512-MiB/four-active-process envelope remains a separate
  exact launch selection; final clean closure and independent outcome review are
  prerequisites for adoption.
- Adjacent source tracing used current bundle
  `257fb1e1c1206cc5aff020ef0529d4d13436da913b9266209ee44cb48dafe481`,
  selector `72f27b6644f998a16b5fb3eb785d576a68d48338949b135cc4e96c18b8b89afc`
  and inert preparer
  `bca0979abaf9bb7e8a233b1432b9307bab53a3dd2532654536be5cb4fe5ef811`.
  This was a test/API/path review, not a duplicate complete bundle-author review.

The guide check is deliberately bounded inline Markdown file-link closure, not
CommonMark/anchor validation or command execution. Manifest shape/count constants
are taken from the separately reviewed, exact-pinned subject; byte comparisons,
retained prior manifest and public verifier provide the actual artifact checks.
Generic pure refusals establish rejection, not exact diagnostic codes. No broad
old suite, native build, mathematical operation, owner opening, network access,
deletion, retry or state mutation is authorized by this source review. Full v5
and actual investigator-workflow qualification remain separate.
