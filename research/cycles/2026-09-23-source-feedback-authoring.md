# Iterative Lean feedback as a knowledge-production interface

2026-09-23, America/Chicago. Prospective design/test note. This changes no
frozen U1 packet, arm, source, product, ledger, or outcome. It supplies no proof
plan to either consumer.

## Observation and claim boundary

Arm B independently acquired and freshly admitted a useful-looking peer
theorem. Its two permitted theorem submissions nevertheless ended in
`REFUSED/SOURCE_REJECTED`. Both reached Lean; the first produced an unsolved
goal at line 17 and an unexpected `let` at line 18, and the agent's second
version produced the same classes of error at those lines. The second
[mathematical audit](../../experiments/useful-reuse-u1/U1-ARM-B-SUBMIT-02-MATH-INDEPENDENT-AUDIT.md)
finds no accepted target or checked reachable proof use. This is an observed
authoring/feedback failure under an unusually tight experimental contract,
not evidence that the theorem is unprovable, the imported theorem is false, or
the product lacks all diagnostic output. The current `submit` already returns
Lean diagnostics; U1 forbade the agent from running Lean or the product itself
and charged at most two submissions. Arm A's expired-service acquisition is a
separate availability failure.

The system need not prescribe when an agent searches or how it proves a goal.
Those remain agent strategy. But it must expose a usable, bounded feedback
loop for exact formal source in the agent's *actual admitted context*; otherwise
recoverable syntax and elaboration errors can consume the only chance to add
knowledge. This is a product/interface and resource-design question, not a
mathematical acceptance rule. Documentation and prompting help an agent choose
actions but cannot alone guarantee that a source term elaborates.

## Minimal contract

For node context `C`, source bytes `s` and selected root `r`, let
`Probe(C,s,r)` be an optional local diagnostic operation. Its required safety
properties are:

1. **No authority from diagnostics.** A `Probe` response, including a success
   response, creates no accepted artifact, changes no checked context/head or
   publication snapshot, and is never a peer-admission certificate. Only the
   ordinary `submit` followed by `publish` produces a public contribution.
2. **Context and byte binding.** Every response binds the exact source digest,
   root, context/foundation and checker/runtime cut. A successful probe against
   `C` cannot be reused as evidence after `C`, dependencies or policy change.
   Final `submit` rechecks all normal obligations and may still fail in export,
   replay, resource, capacity or publication stages.
3. **Useful front-end agreement.** For the same fixed inputs and compiler cut,
   parse/elaboration errors exposed by a probe should agree with the shared
   front-end of `submit`, modulo explicitly reported timeout/resource failure.
   It must not claim completeness for later canonicalization or inverse replay.
4. **Bounded isolation and accounting.** Probe uses the same selected source
   restrictions and sandbox/process limits as native checking; each attempt,
   including failure, charges wall time, Job CPU, peak memory, package reads,
   output bytes and retained evidence. Diagnostics must be bounded and must not
   leak another client's private context or make unchecked peer metadata
   authoritative. Unknown process outcomes do not become free retries.

These are local-node obligations. They require neither a global task queue nor
a shared research objective. The formal correctness boundary stays unchanged.

## Smallest mechanism decision

The first experiment should **not** assume a new `Probe` opcode is necessary.
Allowing more fully charged `submit` attempts under an honest finite budget is
the least invasive route: it uses the existing exact-context checker and native
diagnostics, but repeats costly package/context preparation and consumes stage
and request capacity. B's second rejected attempt took another native stage;
its event reported seven canonical package reads and 12.10 seconds spent on
those reads, so failed authoring is not free. A better general Lean syntax
reference or machine-readable error span/source excerpt may improve correction
without changing the kernel boundary, but the U1 result does not prove that
such presentation alone would suffice.

If repeated `submit` is too expensive or operationally awkward, a separate
`Probe` can stop after exact-context front-end checking and return structured
diagnostics without building/storing a publishable package. It must use the
same selected Lean environment as real submission; a standalone host `lean`
invocation with missing admitted declarations is not a valid substitute.
An incremental Lean session may later amortize startup, but session invalidation,
cross-client isolation, timeout/abort recovery and state leakage make it a
larger second-stage design, not a prerequisite to the next test. No observed
micro-cost is yet evidence of whole-agent speedup.

## Falsifiable next test

1. **Freeze a fresh authoring-only allocation**, not a U1 replay: fixed Lean
   foundation, independently admitted prior theorem, exact target type, finite
   source/document access, agent information boundary, request/stage/CPU/wall/
   storage budgets and stop rules. Preflight that at least six post-onboarding
   native stages and their reserved bytes are actually authorized; the U1 B
   node's configured eight-stage total, of which four were spent before its
   two theorem submissions, would not by itself support this new allowance.
   Obtain any prospective owner capacity grant before dispatch or lower the
   declared attempt cap; never renew reactively after observing an agent's
   failures. Do not expose either U1 attempted source or
   its proof strategy. Start after acquisition/admission so this test isolates
   source iteration; delayed peer availability has its separate test.
2. Give one no-history agent ordinary returned diagnostics and up to six
   *charged* `submit` attempts, with a fixed aggregate budget. It alone authors
   every revision. The operator executes exact requests once, relays complete
   bounded replies, and does not edit source. Require exact frozen canonical
   target type, a reachable proof-producing dependency on the prior theorem,
   and ordinary publication for a positive endpoint. Retain every failed
   attempt and its costs. If the agent still cannot produce a checked result,
   classify its actual failure rather than adding a hint mid-run. One success
   would show feasibility with existing API, not that six is an optimal cap or
   that prompting solves general formal authoring.
3. Only if authoring cost/failure remains consequential, implement a separately
   versioned diagnostic probe and first test its purity, context binding,
   negative syntax/unknown-name/forbidden-source cases, bounded resource
   behavior and differential front-end agreement with `submit`. Then compare
   fresh agents on matched fixed task families under equal aggregate CPU/wall/
   storage ceilings: submit-only with up to six attempts versus at most four
   probes plus two final submits (both at most six Lean checks). Measure actual
   checked/published endpoints, whole-workflow wall and enclosing Job CPU,
   package reads, native stages, retained bytes, diagnostic output and agent
   time/compute where observable. A single pair cannot support a population
   speedup claim. A probe that saves per-attempt cost but worsens completed
   publication rate or weakens isolation is not selected.

The immediate central question is whether the existing API with realistic
iteration suffices. If not, measure a source-feedback route before selecting
an incremental checker, speculative search changes or peripheral identity/
ledger work. Neither outcome alters the frozen failed U1 result.
