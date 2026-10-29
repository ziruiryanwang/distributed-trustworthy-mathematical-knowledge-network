# Focused controls for the assembled owned-acquisition successor

2026-10-28, growth_design_audit. Source only until root selects the finite run.
No test, product import, network, database, owner or native call was executed to
author this plan. A static Python AST parse checked the runner's syntax only.

Target the actual file-only assembly at
`experiments/v5-local-checks/owned-acquisition-assembly01/distribution/package`.
Its PROFILE SHA-256 is
`85d45c928523c2b96f127ec8c15b2e2664f8428f0c1ef2415470a5b30737d3c8`.
Root supplies the exact runtime paths and fresh output under
`experiments/v5-local-checks/`; no passing or failed operation is reused/reset.

The runner is `control_tests.py`. It pins both successor helpers independently
of the supplied full PROFILE pin, loads the actual package through its selected
unchanged loader, checks shared module identities and reverifies its source
profile at completion. It uses the selected external Python/Lean installation
for profile validation only. No Lean process or owner is opened.

The runner accepts `--package`, `--profile-sha256`, `--python-runtime`,
`--lean-runtime`, `--output`, under `python -I -S -B` with assertions enabled.
Original cooperative harness limits are 120 wall / 60 process CPU seconds;
recommend root's outer 180 wall / 90 CPU seconds, 768 MiB, one simultaneous
process, 1 MiB per output stream. No socket or service lease is needed.

## Seven changed-boundary groups

| Group | Decisive assertion |
|---|---|
| Four typed positive reads | Real preview/locator/evidence/authoring parsers validate retained exact bytes through scripted owned responses; only preview/evidence invoke the inert retention spies. One original prepaid ledger charges validated response lengths. |
| Settled fallback | The unchanged actual `_ReceiveSources` scheduler tries B after A for precisely the five mapped transport reasons and framed HTTP 404/503. Before B's response, A's full reply cap and request are already charged to the same ledger. EOF maps to INCOMPLETE_READ. |
| Terminal transport cases | HTTP_PROTOCOL, unknown reason, unobserved cleanup, TLS error, cancellation, unknown local failure and ConnectionAbortedError propagate terminally; B is never invoked and the full cap is charged. |
| Default no retry | All four typed APIs, including authoring offers, treat a returned settled refusal as terminal in default mode. |
| Real invalid/mismatched payloads | Preview byte mismatch, valid-shaped wrong locator UnitID, a different valid evidence unit, and mismatched authoring ExportID fail their real validators, fully charged; the source scheduler never advances after invalid ordinary bytes. |
| Retention failure | After real evidence validation, the before-commit liveness callback runs; an injected retention failure remains terminal, is fully charged and does not try B. |
| Original horizon at setup and return | Real successor `_fetch` and `exchange` run through each added route. Controlled TLS setup advances only the helpers' clock beyond the original horizon; the guard refuses before allocation. A locator case uses a shorter attempt cap. A settled refusal returned after original-ledger expiry is charged but cannot escape as retryable. |

The raw-socket/stream lifecycle code did not change; reuse the adopted owned-
connect controls instead of replaying connection/handoff/close permutations.
The setup-expiry cases connect this new typed client to that existing boundary.
Scripted responses and substituted clocks do not claim real network behavior.
Root's separately selected retained public read is the integration evidence.

## Exact retained inputs and explicit doubles

Read only these two earlier completion-bundle unit files under
`experiments/v5-local-checks/contribution-bundle-controls01/checks/bundle-completion/units/`:

| Unit | Bytes | Raw SHA-256 |
|---|---:|---|
| `f1c20bb5d6ef8d37227b0db40e0479d22ef3849f34c71d7a41880497316b1aa0.json` | 4,997 | `53c957070a250ac49c9ec46d2fdb091d0967143852546238c4d21d08f7f1506e` |
| `25ae588e95228a64196a576aa9c9dd78249c23b0c26189c5671a434b93afa1b3.json` | 2,133 | `c7266a3047afcf59059b7884853b4d6b9be4244509f260e78dd072973f9704aa` |

Both raw pins are checked before and after. The first unit's target is the retained applyFour_eq ExportID
`d0c7be50520d2b91b72e43308b8f1ec75022b32c37fe9561381f4aef879fff1a`.
Preview and locator derive from that unit with the actual pure codecs. The
authoring success uses a genuine empty OfferMap reply, not a repository fetch.

Transport outcomes are explicit doubles except the post-setup route cases,
which enter the real owned helper and refuse before a socket. Retention uses
an uninitialized exact `OrdinaryStore` instance with method spies: this tests
the acquisition call/liveness boundary, not SQLite durability. The existing
real custody tests remain the evidence for unchanged store behavior.

The runner guards native/subprocess launch, SQLite connection, owner open and
application network entrypoints. The event loop's internal setup occurs before
guarding connection/bind methods; replacing the global socket class is avoided
to preserve Windows Proactor behavior. Unexpected loop errors, pending tasks or
attempted forbidden effects fail the run. No mathematical acceptance is asserted.

## Evidence and stop condition

Write one fresh `RESULT.json`, with completed case names, exact source/profile
pins, error details on failure, forbidden/loop-error observations and harness
wall/CPU. Outer supervision supplies process/Job closure and inclusive CPU;
harness CPU is nested and must not be added twice. Stop after seven groups or
the first failure. Do not retry, change a used source, open owner state or start
a native campaign to repair an unexpected outcome. Root owns any successor.
