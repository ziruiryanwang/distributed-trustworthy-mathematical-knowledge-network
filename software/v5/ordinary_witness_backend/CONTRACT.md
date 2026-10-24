# Optional offline witness backend: source contract

2026-10-24. Root selects source implementation only. This is not installed,
compiled, compatible with the retained runtime, or a new mathematical authority.
Rationale: research/cycles/v5-2026-10-24-growth-selection/GROWTH-DESIGN-REVISION.md.

## Exact useful operation

An approved local Lean project uses an existing LP tactic to reconstruct an
ordinary proof from a previously acquired inert certificate file. The operation
must not invoke a solver, import the producer's environment, contact a service,
or accept a native success report in place of the theorem. Preserve the existing
tactic's actual local hypothesis/target binding and final kernel checking.

Use the public `LP.registerStaticBackend` interface as it actually
exists in lp-tactic 86634295a1fa2b45110a680215e208b16f40cd33; verify its exact
namespace/signature before authoring. Use the response decoder and request encoder
from the Contract-only module in lp-backend-soplex-json
ce953f3b926815ebda5d65f88f1a06e9578abdc8. These pin lp-core
8b6d241bc84e54357aa6628f1b18ff795d53de7e. No subprocess Backend import or solver
meta-package. Upstream is pinned to Lean 4.33.1, versus installed 4.34.0; do not
claim binary/source compatibility, switch toolchains or migrate any state.

## Input, scope and cost contract

- One approved local configuration names the backend and a small finite list of
  exact request/response file pairs. Paths come only from that configuration,
  never from a response or a remote discovery result. No automatic registration
  or file reading at module import; expose an explicit registration operation.
- Read each selected file once under a finite aggregate byte allowance, with an
  over-limit sentinel and strict UTF-8. Keep the exact acquired contents in the
  callback closure so later file changes cannot change an active registration.
  Retain per-pair identity in the local report/config, not mathematical authority.
- Match the actual locally generated request against its explicitly retained
  request before returning evidence. Use the maintained request encoding; do not
  trust a producer's echoed problem or equate matching dimensions with matching
  mathematics. Exact representation matching may refuse equivalent requests;
  that is acceptable for this first boundary and must be documented.
- Finite configured caps cover record count, total bytes, dimensions, integer
  numeral length and callback invocations, including failed requests. Reject
  malformed or unsupported data. Do not invent a new rational parser or proof
  checker where the upstream decoder supplies the semantics; preflight resource
  bounds must occur before expensive decoding where required.
- Explicitly select this backend in the caller's tactic options. An unsupported
  request or exhausted allowance returns failure; no alternative backend, solver,
  subprocess, HTTP request, suggested follow-up or automatic budget renewal.
  Equality/strict-goal tactics may make multiple requests; the finite artifact
  set and counter must account for them, not assume one callback per theorem.
- Decoder output is only proposed evidence. Existing tactic proof construction
  and actual final kernel/axiom-policy checking establish the local theorem.
  This module must add no axiom, unsafe cast or native-decide acceptance shortcut.
- File byte/count caps are not an OS sandbox or a total kernel-work guarantee.
  Document that the invoking supported workflow needs its own finite process,
  proof-construction and kernel limits. No execution of untrusted Lean code is
  authorized merely because a certificate is data.

## Allowed source changes and responsibilities

Author owns only `FileBackend.lean`, `README.md` and a minimal local dependency
manifest under this new directory. Use maintained APIs, keep the module small,
and stop/report if the requested bounds require a new parser or substantial
tactic fork. No upstream source vendoring, runtime/dependency download, build,
test, native invocation or package integration is selected yet. Root owns this
contract, subsequent review/launch decisions, navigation and Git.

The author must state which guarantees follow from the source and which remain
untested, and identify any API or resource mismatch rather than omit a check.
Source review comes before one targeted future compatibility/integration check.
No broad benchmark, new solver, generic RPC, region catalog or growth-performance
claim follows from writing the adapter. The separate parametric-region argument
justifies what useful reusable mathematics can eventually be carried; this module
does not discover or generalize regions automatically.

## Selected source outcome

Root read all three authored files and the independent final source verdict in
research/cycles/v5-2026-10-24-growth-selection/GROWTH-CLAIMS-CHALLENGE.md.
The reviewed source satisfies the narrow contract by inspection; exact file
hashes are retained in that verdict. It has not been compiled or run. The
upstream 4.33.1 versus installed 4.34.0 compatibility boundary remains unresolved.

Source work is closed. No dependency installation, port, runtime or packaging
is selected. A concrete method/application/return use must justify reopening
this optional component. Its existence is not a growth result or a release gate
that forces further investment. Existing ordinary library sharing stays primary.
