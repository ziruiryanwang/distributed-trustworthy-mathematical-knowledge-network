# Skip unavailable executable compilation while retaining checked mathematics

2026-10-28. Source/data decision only. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
No product import, compiler/test execution, owner/database operation, old-source
edit or Git mutation occurred. The failed native01 remains preserved.

## Decision for the tiny fixture

Use a fresh successor of native_workflow.py changing only setup-P's source string
from `def Above.d : Nat := Nat.succ Base.c` to
`noncomputable def Above.d : Nat := Nat.succ Base.c`. Keep its body, type, acquired
Base.c identity, final parent checking, all three intended outcomes and budgets.
This selects an ordinary mathematical definition without requesting executable
code. It is the smallest principled correction; no checker/helper rebuild or
compiler metadata reconstruction is justified.

Actual native01 evidence shows that V2 construction of Base.c already succeeded
with one checked unit. Lean then reported an IR check failure for
`Above.d._closed_0` and `unknown join point 'block_0'`. Basis/F were accepted;
P and all V3 cases were not. A candidate file exists despite diagnostics, but
the product correctly refused authoring before P admission. This locates the
failure in executable compilation; it does not isolate every internal cause of
the compiler panic or qualify any frontier outcome. See NATIVE-OUTCOME.md.

Pinned Lean `Elab/PreDefinition/Basic.lean:134-135` makes `shouldGenCodeFor` false
for an explicitly noncomputable definition. Lines186-223 construct the same
ordinary `Declaration.defnDecl`, add it through normal checking, then optionally
compile. Safety depends on the unsafe modifier, not noncomputability. The type
and value remain present and reducible to the kernel; no axiom, opaque constant,
unchecked declaration or weakened receiver is introduced. The plain setup-P body
has no pattern matcher or recursion requiring a second source correction.

The prior source-profile argument in
`software/drafts/CONTEXT-NONCOMPUTABLE-REVIEW.md` supports the same distinction.
It concerns an older failure and is not execution evidence for this fixture.
The fresh run must still establish all three actual outcomes and exact source/
candidate/parent correspondence. The original kernel diagnostic still conflates
type and internal resource refusal; preserve that limitation.

## Alternative and tradeoff

Setup-P could instead import F's actual approved OrdinaryProducer module, leave
the acquired list empty and compile using its existing executable support.
Final parent checking would still be mandatory. This requires rearranging the
fixture's frontend preparation and changes its setup route; it does not repair
ordinary mathematical authoring over inert received definitions. Prefer the
one-keyword correction for this test. Approved source/module reuse remains the
appropriate route when users actually need executable functions or `#eval`.

`noncomputable` is a source authoring choice, not a claim that the mathematical
function is inherently uncomputable. This fixture needs kernel reduction in
proof checking, not executable code for Above.d. Do not advertise executable
compilation of arbitrary restored libraries as a capability of this route.

## Consequence for the forthcoming contextual-refinement source

Do **not** replace this with a blanket `noncomputable section`. In the pinned
version, `Command/Scope.lean:66-72` describes the section as allowing declarations
that fail compilation to become noncomputable. `PreDefinition/Basic.lean:137-142`
still invokes compilation and changes error logging. It is not a guarantee that
the problematic compiler path is skipped.

The reviewed Body.lean contains recursive `fill` plus four Prop-valued definitions.
For a selected mathematics-only successor, explicitly mark these five definitions
`noncomputable`, preserving their types, bodies and exposure attributes. Structural
recursion adds its checked nonrecursive representation first; its optional runtime
counterpart is gated by `preDefs.all shouldGenCodeFor` (Basic:280-296 and
Structural/Main:185-210). The theorem declarations already omit executable code.

There is a separate generated-matcher path: `Meta/Match/Match.lean:1089,1120-1124`
compiles matchers when `bootstrap.genMatcherCode` is true (its default), independently
of the enclosing definition's noncomputable modifier. Therefore scope
`set_option bootstrap.genMatcherCode false in` to the `fill` declaration in that
fresh source. The matcher is still added and kernel checked; only its optional
inline/code-generation actions are omitted. No global option or meta-command
change is needed. This is a source-supported avoidance of an additional executable
path, not a proof that every new inductive helper will elaborate successfully.

Preserve original Body.lean (`3c965c81...`) and its mathematical review. A new
source successor and a small exact-delta review are required before use; generated
artifact identities must come from its actual checked output. The root's subsequent
source-only selection is recorded below. No runtime is selected by this note.

## Source identities

Runtime paths below begin `software/runtime/lean-4.34.0-windows/src/lean/`.

| Source | SHA-256 |
|---|---|
| Lean/Elab/PreDefinition/Basic.lean | `46a2876ccbe1efc4cc491dc24658fea5e972544a64da888334fe2ffcc9c1a5c7` |
| Lean/Elab/Command/Scope.lean | `1e3801241c52ab88e29492c639e04ce4e178b5d3131b89b230021dd51191cf61` |
| Lean/Meta/Match/Match.lean | `6d447f20c2a7bb9d9bbc26c8cac24f95baed700e13e2fc763a869765dcc44e8e` |
| Lean/Elab/PreDefinition/Structural/Main.lean | `8a86ae2d1bae7f1b6c3e52a86f20e3460eecf0dbb7f7a891a16f89971d36be29` |
| Used native_workflow.py | `2cd81f0dd601368a897b12353a5ea97ccd84fee9b3ffdecb41de43a1fb505c73` |
| Original refinement Body.lean | `3c965c818395db4d2f20b1abcfbdf6dbe972a492b63f325b00789ccf33572f7c` |

## Root-selected fresh source successors

After this source argument, root explicitly selected only these two fresh files:

| File | Bytes | SHA-256 |
|---|---:|---|
| native_workflow02.py | 24,213 | `e5ac5c841b48431ce3d627a2b42ad751254350cea478c616dbae436edca5ed05` |
| ../ordinary_finite_map_refinement/BodyMath.lean | 6,927 | `276e64eada849a8ed46a23b6ceee122124ef99c0b91a57fdd97b619de3708b89` |

The workflow is an exact copy except one 14-byte insertion, `noncomputable `,
in setup-P's source string. No assertions, budgets, paths, package choices,
stage order or mathematical expressions changed. Root chose one cheap fresh
tiny fixture rather than building new recovery machinery; no old state reuse
or enlarged allowance is selected.

BodyMath adds exactly five `noncomputable ` modifiers and one source-local
matcher option before fill's doccomment: 115 additional bytes, retaining its existing LF
line endings. All names, types, bodies, proof terms and other source bytes remain
unchanged. Both original source files were re-read and remain byte-identical.
Only standard-library file/hash manipulation created the successors; no source
import, syntax check, compiler, native operation or Git mutation ran. Independent
delta review and a separately selected runtime remain required.

Independent pre-launch review caught the first unused BodyMath variant's option
line between fill's doccomment and declaration. The scoped `set_option` now
precedes that unchanged doccomment, preserving the parser's doccomment/declaration
association. The first unexecuted hash `759c5fd8...` is superseded. Removing the
single option line and five modifiers from the corrected bytes reproduces the
original Body exactly. The workflow02 source remains unchanged; no runtime ran.
The initial note incorrectly called the original line endings CRLF; a byte census
confirms LF with zero CRLF in both original and successor. No line-ending
normalization occurred. One correction script's CRLF-pattern assertion failed
before writing BodyMath; the subsequent LF-exact replacement passed its inverse
byte-equality check. This was file manipulation only, not a product/test run.
