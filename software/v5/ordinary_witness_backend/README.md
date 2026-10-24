# Offline evidence for an existing LP tactic

Source-only candidate, pinned to upstream Lean **4.33.1**. It has not been
compiled, installed or tested; compatibility with the project's installed
4.34.0 runtime is not claimed. Do not run it as a supported product command.

## Purpose

`FileBackend.lean` supplies a small optional file-backed callback for the existing
LP tactic. A locally approved caller explicitly registers exact request/response
file pairs. The callback matches the tactic's actual encoded problem, decodes the
retained inert response with the maintained decoder, and returns proposed evidence.
The existing tactic then constructs a proof from the actual local hypotheses and
target. Final kernel and axiom-policy checking, not the file or provider, warrants
that target.

No solver is called, no producer library is imported, and no request is sent over
the network. This module adds no axiom, unsafe cast, `native_decide` shortcut,
backend initializer or new rational/proof checker. Importing `LPTactic.Registry`
does initialize upstream's empty registry; it does not register this file backend.
`LPBackendSoplexJSON.Contract` contains the codec, not subprocess dispatch.

## Explicit integration shape

An approved caller imports `FileBackend` and `LPTactic` (not the solver-bearing
`LP` meta-package), calls `Commons.Witness.register` during its selected local
elaboration/IO workflow, retains the returned `Registration`, and explicitly sets
`lp.backend` to the same name. Registration takes:

```text
Config {
  name,
  pairs := #[FilePair {label, requestPath, responsePath}, ...],
  limits := Limits {...}
}
```

The source uses the actual upstream `LP.registerStaticBackend` API. Its callback
receives `Options` and the locally generated `Problem m n`. It handles the actual
decoder result (`Decoded.solution` or `Decoded.wireError`), not an invented direct
solution return. The opt-in backend's probe always fails; the pinned upstream
explicit-name dispatch bypasses the probe and does not try another backend.
Unpinned fallback may select an unrelated backend imported by other approved code:
therefore explicitly selecting this backend is a caller requirement.

This is an API shape, not a tested copy-paste invocation or package build recipe.
The inert `DEPENDENCIES.json` identifies exact upstream revisions and imports.
It is not an installer/Lake lock. No dependency download or build is selected.

## Exact binding and immutable snapshots

Each request file must contain **exactly** the String produced by the pinned
`LP.Backend.SoplexJSON.encodeRequest opts problem`: no extra newline, whitespace
reformatting or substitute field order. Keep files as UTF-8. The callback compares
that exact encoded request, including the encoded normalized problem, against
the actual local request before returning a response. Duplicate request contents
or duplicate local labels refuse registration. An unsupported/mismatched request
fails closed; no solver, follow-up query, alternative file or retry is selected.

This is encoded-request identity, not equality of every raw `Options` field:
upstream forces `presolve=false`, quantizes the time limit to milliseconds and
omits some options. All mathematical problem fields are encoded. Equivalent
mathematics with different normalized row/variable ordering may be refused.
No producer-echoed problem, theorem name or dimension match establishes binding.

Files are opened once per configured pair and read through finite capped reads;
strict UTF-8 conversion preserves the acquired contents. The callback captures
those Strings, so later file edits cannot alter this registration. The returned
`Registration.snapshots` exposes the exact acquired texts, configured labels,
paths and byte counts for local records. Labels and paths are not content hashes
or accepted mathematical identities. File races during initial acquisition are
not prevented; approval must protect the local files/process or provide stronger
isolation. A later byte change is simply not part of the captured snapshot.

## Deliberately small supported response subset

Before the maintained JSON/rational decoder runs, a lexical **resource preflight**
requires ASCII response bytes, no escaped strings, no JSON numeric tokens, nesting
depth at most eight, bounded string lengths, and bounded consecutive digit runs.
Rationals must be unescaped decimal strings such as `"-3/7"`, as in the upstream
wire contract. JSON formatting whitespace outside strings is allowed. Escaped
digits, non-ASCII error messages and numeric extension fields are refused even
when a general JSON parser could understand them. No numeric token can reach the
JSON parser's arbitrary-size/exponent handling through this subset.

The preflight is not a replacement parser or proof checker. Upstream `decodeResponse`
still decides JSON/rational syntax, status values and vector dimensions. Its
unknown/duplicate-field behavior remains upstream behavior; no stronger canonical
JSON claim is made. A malformed response or wire-error envelope yields a bounded
local failure diagnostic; untrusted error text is not forwarded as instructions.

## Finite work and explicit limitations

Defaults are eight pairs, 64 KiB per file, 256 KiB across all retained files,
dimension 128, 2,048 sparse entries, 128 digits per rational numerator/denominator
and iteration-limit integer, and 16 funded callbacks.
Configuration has fixed hard ceilings in `checkLimits`: 32 pairs, 1 MiB/file,
4 MiB total, dimension 512, 8,192 sparse entries, 256 digits and 256 callbacks.
Response strings are limited to `2 * maxDigits + 16` ASCII bytes. These constants
are conservative source choices, not measured safe operating envelopes.

The reader uses an over-limit sentinel: a rejected registration can read at most
one additional byte beyond the reached file/aggregate content allowance before
it stops. Successful registrations retain no more than the allowance. Partial
reads are handled under the same cap; no unbounded `readFile` is used. Only locally
approved ordinary files are accepted by the metadata check, which is not a
race-free filesystem guarantee or protection against a blocking filesystem.

Every callback atomically debits the one shared remaining allowance before
request checking, encoding or response decoding. Failures consume it too. Calls
after exhaustion only return failure; no expensive work or automatic renewal is
performed. An external caller can repeatedly invoke that constant-size failure
path, so overall process limits are still necessary. Equality/strict tactics may
make several calls; all consume the same allowance and need exact retained pairs.
Separate explicit registrations are separate locally authorized investments, not
a loophole providing an unbounded workflow budget.

Before request encoding, the callback bounds dimensions, sparse-array length and
each rational numerator/denominator (against `10^maxDigits`), including bounds and
objective offset. It also bounds the encoded iteration-limit integer. This avoids
unbounded decimal conversion of an already-local problem. The resulting encoded
request must fit the file-byte cap; string construction is additionally bounded
by the prior dimension/entry/digit ceilings, not claimed allocation-free.
`maxDigits` is not a cap on every encoded integer: dimensions and indices are
bounded by `maxDimension`; upstream's encoded time-limit milliseconds pass through
`UInt64` and have at most 20 decimal digits, even when `maxDigits` is smaller.

These bounds do **not** establish a hard wall deadline, OS sandbox, total memory
bound or total kernel-proof-construction cost. Registration file IO can block,
and upstream tactics can build costly terms. The supported invoking workflow must
apply its own finite process, elaboration and checking limits. No certificate
data authorizes execution of untrusted Lean source/plugins. Bounds are not proof
of mathematical relevance, useful growth or a globally deployable system.

## Source status and review checkpoint

Authored 2026-10-24 under the adjacent root-owned `CONTRACT.md` after in-memory
inspection of the pinned Registry, Dispatch, Contract, LPCore types, Lean file-IO
and rational APIs. No upstream source is vendored. No build, installation, test,
native invocation, solver or network service was run. Pinned source availability
is not a full audit of upstream dependencies or tested compatibility.

Independent source review must check Lean syntax/API use and the finite boundary
before root selects any later compatibility operation. If the source does not
compile on its declared pin, preserve that outcome and revise an unused successor;
do not claim that this draft supplies a tested backend. The next substantive
growth decision remains whether existing witness/parametric-region workflows
make this small adapter worth deploying, not automatic solver/RPC development.
