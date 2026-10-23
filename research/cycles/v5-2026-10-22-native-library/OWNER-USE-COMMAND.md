# Ordinary owner-use command: source checkpoint

## Modern command staging repair

Root selected command-build01; it failed before artifacts with Lean's explicit
`Invalid meta definition ... OwnerUse.run not marked meta`. Its saved output
remains unchanged. This is a module phase-distinction error, not a mathematical
checking failure or justification for importing full private libraries.

Root read the installed Lean Parser.Command meta documentation and LCNF
Visibility.checkMeta implementation. A command elaborator is compile-time code;
its same-module support must be in `public meta section`, with `public meta
import` for regular reusable helpers used during that phase. The source successor
changes only those three header modifiers. Reusable OwnerRebind and checking
helpers remain ordinary definitions; no kernel check or compiler stage check is
disabled. The exporter command receives the analogous change. New compilation
is necessary for the two command modules only.

2026-10-23. Author: `preview_boundary_review`. Source-only assignment;
compilation, execution, controller integration and adoption remain root-owned.

## Practical endpoint and scope

An ordinary Lean source imports `OwnerUseCommand` and calls:

```lean
#ordinary_use "<absolute prepared directory>" "<profile ID>" "<context ID>" "<basis ID>"
```

The current owner environment is retained. The existing `OwnerRebind` helper
matches selected already accepted interfaces and exact non-theorem semantics,
and checks only missing declarations. The command adds no second environment
import, private proof-library loading, certificate generation, network call or
new mathematical acceptance mechanism.

The saved actual owner request contains 387 semantic groups and three missing
units. This command has not yet consumed it; preparation evidence is not use
evidence. Its payoff is completing normal named Lean authoring over acquired
mathematics while keeping the separately warranted receiver as authority.

## Trust and transaction boundaries

The trusted outer controller must authenticate the exact prepared file census,
bytes, accepted context, runtime and helper and retain their immutability. The
three expected identity strings are pinned controller labels, not signatures
or independently established warrants. Canonical encoding and duplicate-key
rejection remain the controller's existing responsibilities.

The command uses its actual `getEnv`, refuses an async owner, and never unlocks
async checking. Parsing, correspondence, missing-declaration checks, local
context construction and diagnostic IO all precede the sole final `modifyEnv`.
A failure before that point does not install the candidate. No post-install IO
is requested. The last message says `READY_FOR_AUTHORING_INSTALL`, not accepted.

`BoundContext` stores `mainModule`, `profileId`, `contextId`, `basisId` and
`bindings : Array OwnerRebind.BoundName`. The public
`OrdinaryLean.OwnerUse.getBoundContext? : Environment → Option BoundContext`
returns state only for the originating main module. Its private **plain**
`EnvExtension` uses `.local`; it is not a `PersistentEnvExtension`, does not save
state into oleans, and does not convey correspondence through imports. A second
use in the same owner is initially refused rather than silently merging maps.
The successor exporter may use this map to stop traversal at exact accepted
identities; the receiver must still independently resolve those identities and
check every new declaration. Trusted owner code can fabricate construction data;
the command-local map is deliberately not an unforgeable acceptance warrant.

## Bounded input path

Only the absolute root-selected directory is supplied. Relative/dot-component
paths and paths exceeding 32,768 UTF-8 bytes refuse. Filenames are fixed locally:
`header.json` and `group-00000.json`, etc.; JSON never authorizes a path.

The header has exactly seven required fields and the expected schema. Identity
shape/equality, nonempty basis/target bounds and group-count bounds are checked
before rebinding. The header ceiling is 1 MiB. Each group is at most 8 MiB; a
single 64 MiB raw-byte allowance includes the header and every group, without
resetting per-file allowances. The callback enforces exactly increasing indices
and reads one group at a time. The existing helper additionally bounds aggregate
rows, semantic scans, encoded nodes, checked units and added names.

Metadata and actual bounded reads precede parsing. A raw lexical preflight
enforces depth at most 64, matching brackets, no string controls, unsigned
integer tokens of at most 20 digits/uint64, no leading zeros, and no boolean,
null, negative, fractional, exponent or nonfinite tokens. JSON parsing remains
responsible for complete JSON grammar and escape validity. UTF-8 must strictly
decode and re-encode to the same bytes. Aggregate resource refusal aborts the
whole operation; it does not authorize retries or new work allowances.

Symlink/alias exclusion, file authentication and races against local mutation
belong to the pinned immutable controller-selected input boundary, not a new
filesystem sandbox. This owner command is not a hostile-source sandbox.

## Review and next decision

Public `phase` and `absolutePath` helpers are available to the sibling successor
command; there is no output-writing or fresh-output helper here. Imports are
only public `OwnerRebind` and `Lean.Elab.Command`, not legacy exporter modules.
The new source awaits independent source review and a root-selected narrow
compilation. No test, replay, source use, export or receiver acceptance was run
by this assignment. Root should retain successful helper artifacts and compile
only newly changed boundaries, then exercise the substantive existing consumer
and independent successor check rather than treat this component as v5 release.
