# Reconstructed Lean frontend gap: causal hypothesis, not a diagnosis closure

2026-09-23, America/Chicago. Read-only source inspection. No frozen U1 artifact,
product source, or runtime was changed; no additional Lean execution was made.

## Observation and causal chain

The [separate exact-context diagnostic](../../experiments/exact-context-source-syntax-01/RESULTS.md)
sent the trivial `Eq x x` theorem with multiline `by`, `let`, and `exact` through
the retained `AgentClient --check-source` path. It returned an unsolved goal at
the line-1 `by` and `unexpected token 'let'; expected command` at line 2.
The [standalone syntax probe](../../experiments/lean-agent-authoring-syntax/RESULTS.md)
accepted an analogous layout in Lean 4.34.0. This is evidence against a
general indentation rule or a defect in the original U1 mathematical proof;
it does not alone identify the cause.

The inspected path is:

1. [`receiveSeed`](../../software/native/BootstrapSupport.lean) at lines
   997–1018 creates `Lean.mkEmptyEnvironment 0` and inserts checked kernel
   `Declaration` values using `addDeclCore`. Its header, lines 8–12, explicitly
   describes this as an empty, declaration-only receiver.
2. [`receive`](../../software/native/AgentReplayCore.lean) at lines 400–417
   retains that environment and adds the requested batch as checked
   declarations, not by importing Lean source/modules into it.
3. [`checkSource`](../../software/native/AgentClient.lean) at lines 148–160
   passes precisely `state.env` to `Lean.Elab.process`.
4. Lean 4.34.0's [`Frontend.process`](../../software/runtime/lean-4.34.0-windows/src/lean/Lean/Elab/Frontend.lean)
   at lines 64–76 and 134–138 parses commands using parser state from the
   supplied environment. Ordinary tactic syntax is not solely a kernel
   declaration: [`Init/Tactics.lean`](../../software/runtime/lean-4.34.0-windows/src/lean/Init/Tactics.lean)
   declares `exact` syntax at line 237 and the `let` tactic macro at line 937;
   Lean's parser extension stores syntax entries in environment extension
   state ([`Parser/Extension.lean`](../../software/runtime/lean-4.34.0-windows/src/lean/Lean/Parser/Extension.lean),
   lines 77–92 and 341–345). `addDeclCore` does not replay those extension
   entries merely by inserting constants.

**Hypothesis H:** the reconstructed environment is sufficient for native
kernel checking but lacks imported frontend syntax/macro/tactic extension
state needed to elaborate ordinary Lean source. The observed sequence is
consistent with `by` being treated as an empty tactic block and `let` being
reinterpreted as an invalid next top-level command. H is strong but not yet
confirmed by direct parser-table inspection. Other environment extension or
option differences may also contribute. In particular, restoring parser
entries alone might expose a later macro or tactic-elaborator failure.

## Falsifiable, bounded diagnostic

In a fresh non-U1 diagnostic, compare the same trivial source under (a) the
reconstructed `state.env` and (b) a version-pinned ordinary imported Lean
environment. Before source processing, record whether each environment's
`tactic` parser category contains `let` and `exact`, along with the relevant
macro/tactic elaborator entry availability. Fix identical Lean executable,
source bytes, root, options, wall/output bounds, and capture complete logs and
hashes. H predicts the missing entries and the parse split in (a), with a
normal parse in (b). If the entries are present in (a), reject this simple H
and inspect parser scope/state/options and command snapshots instead. A
separate term-style proof can help distinguish tactic syntax from all source
processing, but cannot establish useful reuse.

This diagnostic is **not** a U1 retry, publication, or canonical acceptance.
Do not launch the planned multi-attempt authoring trial merely to spend its
finite submissions on an unresolved product frontend fault.

## Prospective repair constraints

Keep the data-only, checked reconstruction as the mathematical authority.
One candidate architecture uses a separate, explicitly pinned Lean frontend
environment for agent-authored source, after proving the imported foundation
constants agree with the reconstructed ones and installing checked peer
declarations without collisions. It then exports the resulting declarations
and accepts them **only after** their dependencies, axioms, and proof objects
pass the existing canonical capture/replay checks against the reconstructed
environment. Elaborator success must never count as peer admission. This is
a design candidate, not an implementation instruction or demonstrated fix;
blindly switching to an ambient imported environment would weaken the current
trust argument. A minimal regression must show the trivial `by let; exact`
front-end path succeeds, and a second regression must show a source-derived
proof depending on a checked peer result survives canonical replay and
publication while unbound ambient dependencies are rejected.
