# Existing-context contribution: independent source review

Disposition: **PASS for the selected source boundary and one bounded execution
of the eight new controls.** This is not an actual test outcome, Lean admission,
succinct certificate, growth advantage or v5 release acceptance. Root owns launch
and adoption.

## Exact reviewed sources

| File | SHA-256 |
|---|---|
| `software/v5/examples/contribution.py` | `ce82e170e1fad04beeb0be8722c89d748e381762b4957dfaf7b5850e2a57495c` |
| `software/v5/examples/test_contribution.py` | `18425a7e1142d8ae63f3defb11db863d0ee699f9492d45643941a325eb18bc27` |
| `software/v5/examples/CONTEXT-CONTRIBUTION.md` | `55b8d9794b0b795aa36c9692846288ac036bfdc2ac37d5396c93839a12b0a1d8` |
| `research/cycles/v5-2026-10-20/Select-ContextContribution.ps1` | `123701cf964c781e5de319cc5da7566bc0540a28bd44ed6410a405cc843455a7` |

I read the complete helper, tests, usage note and selector, and traced their
calls into the existing `workspace_atomic`, `workspace_evidence`, semantic
reader, mixed authoring/receiver and installed bootstrap sources. No author
source or predecessor was modified by this review.

## Authority and workflow checks

- The helper borrows `client.workspace` and `client.grant`, never accepts a
  second grant, and neither opens nor closes a client. It does not acquire,
  import or re-admit the input context. Caller serialization/cleanup remains
  explicit.
- It calls the original `author(context, ...)`. That method's `_live_context`
  checks exact `AuthorContext` type, same-client object identity, current
  selection/view and liveness. A saved READY preview cannot authorize authoring.
  The original action wrapper retains fail-stop behavior and charges work.
- Limits are validated within existing ranges and passed through unchanged;
  owner/client calls retain their original cumulative grants and deadline
  clipping. The helper creates no worker or new allowance. The lower-level
  packet put remains quota-bounded custody, not a separately charged client
  action; this scope is documented rather than falsely counted twice.
- A need-for-data result returns demands before custody, admission or
  publication. An untrusted prepared packet must have the exact packet digest,
  source digest and selected roots. Only this new raw packet is stored and
  passed to `admit_local(module, digest, length)`.
- Existing admission reloads and inspects that exact stored packet and invokes
  the actual mathematical owner. Subsequent live description binds module,
  packet digest and summary. The prepared result has no independent exact-J
  field: the helper correctly records actual checked J rather than inventing
  a prepared journal or treating a status string as a warrant.
- Publication receives those same raw bytes and exports. CONTRIBUTED requires
  LOCALLY_PUBLISHED plus exact module/digest/length/export binding. Partial
  publication exceptions propagate unchanged; there is no automatic retry or
  fresh operation. Operational reports carry no live authority.

## Controls and selector

The eight named controls cover successful new-only ordering/original grant,
explicit need-for-data, the real inherited context-identity guard within an
inert shell, parameter refusal, malformed/unbound preparation, stage exception
propagation, mismatched live output and incomplete/mismatched publication.
The positive authoring, storage, admission and publication implementations are
explicitly inert. These controls do not claim to execute Lean or prove that
cryptography is sound. The actual unchanged public author guard is used for
foreign, superseded, preview, absent and missing-owner refusals before any
native preparation object can be constructed.

Only these eight tests are constructed in the suite; predecessor suites are
not discovered or executed. Native subprocess entry points are patched to
refuse; successful status additionally requires zero attempted native launches.
The report distinguishes observed test outcome from mathematical acceptance.

The selector binds unchanged basis
`5eff81de1ed686cf3db2d6d901073f7f7070c3497762d22aef998736c4ddc4e4`:
96 inherited source pins plus exactly the two new helper/test paths = 98;
19 unchanged runtime pins. It verifies each digest, rejects source collisions,
pins the existing runner, uses only the new test script with `-I -S -B`, and
creates a fresh selection exclusively. Envelope: 20 CPU seconds, 60 wall
seconds, 128 MiB, two processes, 1 MiB stdout and stderr each. Its act is plan
generation, not test execution. Both fresh selection/output paths were absent
at review; root must revalidate at creation/use.

After root prepared the plan, I read the actual generated selection SHA-256
`f48135a3f5e6e1862f354acb90a79afd1b4203c0e822425df17d9dab745dfbef`.
Its 98 sources/19 runtime pins, exact helper/test hashes, schema/name, argv and
envelope match this reviewed derivation. All 96 inherited source-map values and
19 runtime-map values equal the pinned basis. The retained interpreter was not
redundantly hashed here; the actual runner rechecks its runtime closure at use.

## One issue found and resolved before use

The first usage snippet permanently inserted the owner snapshot into `sys.path`.
The unchanged installed bootstrap checks the exact original import path at
completion, so that snippet would fail `CLIENT_IMPORT_SELECTION_CHANGED`.
The author corrected it to restore the original list in `finally` immediately
after the selected helper import. I reread the corrected bytes above. The
bootstrap's selected-source loader still binds the imported helper; neither
the helper nor import path is described as a security sandbox.

No remaining blocker in this selected scope. This review ran no imports,
tests, compiler, prover, network operation or RAM inquiry and did not mutate Git.

## Saved execution outcome (root-authorized append)

**PASS: the exact eight selected controls completed once with clean closure.**
I audited only retained `context-contribution-controls-01` evidence; no rerun.

- Copied selection retains `f48135a3...`; all 98 snapshotted source digests match
  it, including exact reviewed helper/test/real context-guard sources. Command
  argv, canonical cwd and 20 CPU / 60 wall / 128 MiB / two-process limits match.
- Retained stderr lists all eight required tests individually as `ok`, then
  `Ran 8 tests` and `OK`; stdout is empty. The structured control report agrees:
  eight tests, zero failures/errors/skips, 40 inert client instances, five real
  inherited context-guard calls, one inert successful composition and zero
  native-launch attempts. Assertions have the source-reviewed scope above.
- Supervisor returned child exit 0, direct child reaped, Job closed, zero active
  or terminated processes, no requested termination and no cleanup errors.
  Recorded logs stay within caps. Final Job CPU 0.640625 seconds plus wrapper
  CPU 0.390625 = **1.03125 known CPU seconds**; total wall **3.5701969997 seconds**.
  These are scoped control costs, not mathematical production costs.
- Exact outer result SHA-256:
  `0b82f7c2ca060abe7eaefd2ee232556d63c3e9acd32394cf793959ae31ff4ee2`.
  Exact control result:
  `6d3936cc13ac840053e14240ba68b95611f30b28a1be0c31fa64083348ed7bfe`.
  Exact stderr:
  `9e46f2d2827c36ffda806f429eaf44d51e7480d75b888dd7d70ba0a318b3238e`.

This qualifies changed-boundary composition controls only. No actual Lean
authoring/admission/publication, new certificate, useful-growth advantage or
final v5 release is established. Preserve these used sources and evidence;
do not repeat the passing controls. No implementation or Git change was made.
