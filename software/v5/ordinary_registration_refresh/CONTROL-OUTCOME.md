# Actual assembly and repaired refresh controls

2026-10-28. Saved-artifact audit by growth_design_audit. **PASS for assembly01
and controls02 within their stated boundaries. Controls01 remains non-clean.**
No operation, product import, test, socket, owner/database, Lean or Git action
was repeated during this audit. Root owns adoption. Public loopback composition
is still pending and is not claimed here.

## Exact package assembly

The recorded `registration-refresh-assembly01` invocation used selection
`e338801e2208a80414428140172c3c87c933fffc489d5c8f57bd51649f88e465`.
Its eight source snapshot pins match actual saved files. Saved stdout parses
identically to distribution/ASSEMBLY.json, SHA-256
`a604c0ecbf3991f20c84551c6ff606a73ecc534569944be5e0d38ae04a2481a2`.

The actual package is:

`experiments/v5-local-checks/registration-refresh-assembly01/distribution/package`

Independent byte checks confirm exactly 160 package files, each matching the
assembly receipt, with all 122 auxiliary PROFILE pins agreeing. Comparison with
the adopted directory kit's actual package finds **155 unchanged files** and
exactly these five changed paths:

- PROFILE.json;
- peer.py;
- peer_api.py;
- run.py;
- support/transport/http_provider.py.

There are no added files. The four changed source files are byte-identical to
their selected assembly snapshots. The source-map identity matches
`aeab07b21fb755614ea1432ca9b748d2f8abbfe8c6f43f262de9d2da66cbdb85`.
New package PROFILE is
`f75dda6e534450cdf5d4db2901c3e1964501514da817bc3eb8aadebc0c350f7b`.
The installation manifest remains
`9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`,
and mathematical implementation identity remains
`86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea`.
Every native payload is among the unchanged files. Assembly reports zero native
calls and no owner open; it is a file assembly, not mathematical acceptance.

## Preserve the first harness outcome

`registration-refresh-controls01` used original control_tests.py
`189489066a798bb46ef40817a1586e48ff974af46c9741a431f88d5b0421c2d0`.
Its twelve assertions returned PASS and the outer Job closed. Nevertheless,
stderr has 1,026 bytes and two Windows Proactor self-pipe TypeErrors caused by
the harness replacing the socket class with a function. The saved `passed:true`
field does not establish a clean run and remains unmodified.

CONTROL-HARNESS-REPAIR.md records the exact error and repair. Controls01 is
retained as **non-clean harness evidence**, with its full cost charged. It is
not counted as a second successful campaign or transformed into a product
failure. No source or result from it was overwritten.

## Repaired controls02: actual PASS

The fresh execution selected
`b1283044eb3ea0a96573157f2b1b10e644035632bdbb659747970a6123441cd7`
and control_tests02.py
`7e07e3cdb5e98e91ac84137846559792bb3548cd876ea9650c94cc49c5f89c34`.
Both copied source pins match. Actual argv and saved control output bind the
exact package path and new PROFILE above. The three retained external Python
runtime files were independently rehashed against the selected pins; no new
runtime provenance or hermeticity claim follows.

Its checks/RESULT.json, SHA-256
`31bc6f002cdb5e4bc49074e3c7168b5bf48e881053df07e22dfbcaf9ba987548`,
parses identically to stdout and reports:

- all twelve original groups PASS, with exactly the same group names as controls01;
- `passed:true`, `unhandled_loop_exceptions:0`, and an empty exception-context list;
- empty actual stderr;
- scope `SCRIPTED_CHANGED_SEAMS_NOT_NETWORK_OR_MATHEMATICS`.

These executed groups cover pre-I/O policy/slot allocations; shared-ledger
ownership, charges and nonrenewal; fresh replacement and no cached fallback;
empty/truncated/malformed/unavailable/HTTP distinctions; partial union and
source-local withdrawal; policy rejection; earlier-slot aging; direct cutoff and
caller checks; preheader/postdrain guards and charges; the lower-level writer's
chunk guard; None/noncontact compatibility; and late-start READY refusal under
the clipped service lease.

The selected product API, parser and budgets ran against scripted feed/service
and clock/writer doubles. The event-loop guard now preserves the socket class,
blocks application connection/listen methods, and explicitly checks callbacks.
This verifies those seams. It does not verify live refresh/listen/reader
composition, external TLS, independent providers, endpoint liveness, mathematical
discovery or knowledge growth. The large writer payload is a helper control,
not a claim that contact replies may exceed their existing 32-KiB limit.

## Closure and complete recorded cost

All three outer operations report child exit zero, direct child reaped, Job
closed, zero final active/terminated processes, no requested termination and no
cleanup errors. Their recorded limits equal their saved selections. Assembly
and controls02 have empty stderr; controls01's nonempty stderr is preserved as
the reason its clean-pass gate failed despite process closure.

| Operation | Job CPU | Outer wrapper CPU | Known CPU total | Outer wall seconds | Disposition |
| --- | ---: | ---: | ---: | ---: | --- |
| assembly01 | 1.953125 | 0.156250 | 2.109375 | 4.8042365 | File assembly PASS |
| controls01 | 0.937500 | 0.125000 | 1.062500 | 1.2004580 | Non-clean harness run retained |
| controls02 | 0.828125 | 0.109375 | 0.937500 | 1.0724572 | Repaired controls PASS |
| All recorded work | 3.718750 | 0.390625 | **4.109375** | **7.0771517** | Includes the failed harness cost |

Nested assembler/harness/supervisor counters overlap these scopes and are not
added again. These totals exclude this read-only audit and earlier development;
they are not end-to-end discovery, service or growth costs.

| Outer RESULT.json under experiments/v5-local-checks | SHA-256 |
| --- | --- |
| registration-refresh-assembly01 | 55fe3e4b10f8701c7a60367286b6e1eb72b89c3bd402aaac961af764cfe6458d |
| registration-refresh-controls01 | 8165cc4dda17682058371e868345d843383b6414d546ecd7722a682a6ba96ce1 |
| registration-refresh-controls02 | 11e48f86be030d4cda1fe83e3f4cb08b13110c35f930c74f71ba1affe23a67fb |

The next public workflow, packaging/adoption and full-v5 goal remain separate.
Nothing here publishes the software or changes the local-only, license-undecided
scope. Used sources, the package and all three evidence directories stay frozen.
