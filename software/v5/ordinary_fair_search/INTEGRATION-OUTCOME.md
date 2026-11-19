# Fair-search integration: independent saved-outcome audit

Reviewer: `/root/onboarding_controls`. Review uses saved outputs, source/payload
hashes and read-only metadata comparisons only. No operation was rerun, no native
process or product module was executed by this reviewer, and no existing
mathematical state was opened. The preceding exact source review is
`INTEGRATION-REVIEW.md` (including the resolved auxiliary-versus-installation
approval clarification).

## File-only assembly01: PASS

Run: `experiments/v5-local-checks/fair-investigator-assembly01`.

| Artifact | SHA-256 |
|---|---|
| selection.json | `bb8e0e85c0e09da9082c7c74dba83fc2e69ff37bf373e0b75da6413f36fe118c` |
| outer RESULT.json | `363312b20886cf02feb1bbdd361d28f39d2d4a7a61dcde9a7448caf3ab11de01` |
| assembled/ASSEMBLY.json | `5074596bf2e70ff86edb3af215c9dc9e6ac5afac123e105ea6ff4027a91a3c0b` |
| assembled/package/PROFILE.json | `ea7a958db31ac070aa59be1c1e3c50d4b195cfd982c63658bd80de15ef3c6d01` |

The saved exact invocation uses the reviewed assembler/source snapshot, selected
baseline PROFILE and build-receipt hashes, one fresh output, and 60-wall/45-CPU
cooperative assembly limits inside a 90-wall/60-CPU/512-MiB/three-process outer
Job. Outer result is `COMMAND_EXITED_ZERO_AND_CLOSED`: exit zero, direct child
reaped, Job closed, zero final active processes, no termination request and no
cleanup errors. Stderr is empty. Observed cost is 5.716093899682164 wall seconds,
1.984375 inclusive Job CPU seconds, 0.09375 outer-wrapper CPU seconds, and
17,514,496 peak Job private-commit bytes. The nested supervision CPU figure is
part of wrapper accounting, not an additional independent child-work charge.

Independent full-map checks found:

- Exactly 148 package files and 115 PROFILE auxiliary entries; no reparse nodes.
- Every file's actual length/SHA-256 matches the reconstructed PROFILE,
  installation-manifest and documentation map. Total package bytes: 39,043,542;
  non-PROFILE copied bytes: 39,027,916, agreeing with the receipt.
- Exactly 142 non-PROFILE files are byte-identical to the selected baseline.
  Changes/additions are precisely profile.py, peer_api.py, README.md,
  support/discovery/fair_search.py and support/transport/fair_exchange.py.
- All seven selected source files match both current source and frozen snapshot
  pins. No native installation payload or helper changed.
- The unchanged installation-manifest SHA is
  `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`;
  receipt implementation identity remains
  `fafc83872c4b5bc0fce2a939fc26e38a24fa51944d5bfd7b91e03d51c8b817df`.
- Parsed stdout equals the external assembly receipt. There is no pending
  PROFILE or ASSEMBLY-FAILURE file. The final exact PROFILE is the one above.

This passes actual file-assembly integrity. It does not establish loader/CLI
execution, native checking, independent hosting or mathematical growth. Root may
select the separately reviewed public smoke and inert operator controls using
this exact successor; successful assembly is not full product adoption.

## Selected operator controls01: PASS

Run: `experiments/v5-local-checks/selected-operator-controls01`.

| Artifact | SHA-256 |
|---|---|
| selection.json | `428269fa80b0c4ba8cd6c4ee47f96aeb03eda918a411b965696fa465ee7b23b3` |
| outer RESULT.json | `5cb6fc04ed6245fd958c17cfea6802a2c4c69593e4ee9a1161bf9fb4b5672099` |
| suite/RESULT.json | `506107d65df212bbd96a9a18483cd2f3be83333fab01e5e0b5088956b44ab231` |

All twelve distinct selected cases completed, including the actual original
41-role and assembled fair 43-role auxiliary source checks, inert init outputs,
coherent/fresh-native layouts, five malformed-layout refusals, wrong PROFILE
refusal and same-length modified-source refusal. The source/snapshot hashes for
the wrapper, frozen helper, compatibility map, test and outer runner all match
the exact selection and independent source review. The three selected Python
runtime hashes were rechecked unchanged. Parsed stdout equals the suite result.

Both saved preparation receipts bind their correct distinct PROFILE, report
zero commands executed, no protected state opened and no mathematical acceptance.
All four generated payload files and both receipts' input bindings were
independently rehashed. Future catalog/custody and both refused output directories
are absent. The intentionally modified-code fixture remains as evidence; it is
not a second usable package or a product alteration. The tests invoke the wrapper
API with execution/network/state entrypoints trapped, not a product command.

Outer exit zero/closed, direct child reaped, zero final active processes, no
termination or cleanup errors, empty stderr. Measured cost:
1.072745000012219 wall seconds, 0.4375 inclusive Job CPU seconds, 0.125
outer-wrapper CPU seconds, and 25,395,200 peak Job private-commit bytes.
The one selected 90-wall/45-CPU/512-MiB/three-process allowance was not renewed.

This qualifies inert compatibility selection/config generation for the two
actual reviewed packages and listed refusals. It does not approve variable native
or installation bytes, authenticate packages/reports, or accept mathematics.

## Real public-find01: PASS

Run: `experiments/v5-local-checks/fair-investigator-public01`.

| Artifact | SHA-256 |
|---|---|
| selection.json | `8b3f410da024458ba9be830309615803180505600bd5168acca5e3812de8772e` |
| outer RESULT.json | `a12056da3f54938c4922583540c90cf0e4f782a66c0b355b99d32bdb3e9eab57` |
| suite/RESULT.json | `874700e60c25915d06e4ed2be2a5536d89a080e386e15755a598bd3d8adef853` |
| suite/public-find/RESULT.json | `b4c9d962d8e2c46d15a1fa111f4fd821667e695052988039eebf9dcc6d24e611` |
| suite/launcher/RUN.json | `dc96623d01be2da93f9f27edf5d30a1b8233c8c58fdfc84e53ca0c135fc19b0b` |
| suite/launcher/SUPERVISION.json | `fb5458099b59b1d3766b19d004322a056b7a8210508b44cf8271bcfc7c38bb96` |

Actual saved PUBLIC-COMMAND records one invocation of the assembled public
`run.py peer find`; nested supervision records its real peer.py child. Both bind
the exact new PROFILE. Harness and current/snapshot runner/source hashes match
selection. The public report independently agrees with the harness's embedded
copy, and parsed outer stdout agrees with the full suite result.

The deliberately proof-free synthetic preview's saved bytes hash to
`9464d4f8b9c3186465dcd58c3ab38a58e255c3751793969f638f896bdda3484b`.
Exactly one record from B is returned, equal to the entire EXPECTED-RECORD, not
merely its label. Its object ID is
`3d7c5f41819b36cb38102c90fa2ac4d11a3a749a8db616148640790eccd9d92a`,
and its actual snapshot ID is
`a925ff1055f60cbbc87bb5386646ddda79431f803721f3829ec656198822044c`.
The saved config hash independently matches the public result:
`79ea5aedac61389fc8dae9b93cbb14544054703d8fea61c32a853b898894b061`.

Observed A receives the bound offer and client EOF, closes cleanly after its
approximately five-second stall, then B receives two actual requests. The sole
provider error is A/offer/SettledRefusal/ATTEMPT_TIMEOUT. All three connection
observers finish with wait_closed and without handler/close errors. B reports
two requests, 3,749 reply bytes, 877 received request-body bytes, zero failures,
zero active handlers and zero reserved reply bytes. The expected bound query
and unchanged real Provider handler—not fabricated replies—produced the match.

The one SearchSession reports three requests, one page, two providers, one
snapshot, one candidate, eight charged examined slots and 69,285 charged reply
bytes: the failed offer's full 65,536-byte reservation plus 3,749 actual B bytes.
All three reservations and pending-request count are zero. Outer network ledger
is closed with exactly one `peer-find` prepayment of eight requests/1,048,576
bytes, no pending/reserved requests, no new grant and no replacement session.
Status remains INCOMPLETE_SEARCH; global completeness, verified scan coverage
and mathematical acceptance remain false. Advisory termination is not promoted
to a completeness proof.

Both public and enclosing Jobs report exit zero/closed, direct child reaping,
zero final active processes and no termination/cleanup errors. The harness also
records closed listeners, completed handlers, reaped launcher and closed fresh
index. Harness/launcher/outer stderr are empty. There was one public operation;
no native mathematical subprocess or existing owner state was involved.

Whole-run cost under the original 90-wall/60-inclusive-CPU/1024-MiB/eight-process
outer envelope is 7.9873000998049974 wall seconds, 2.578125 inclusive Job CPU
seconds, 0.15625 outer-wrapper CPU seconds, and 74,543,104 peak Job private-commit
bytes. The public child subtree uses 1.1875 Job CPU seconds and its public wrapper
reports 0.203125 CPU seconds; harness CPU is 1.078125 seconds. These are nested
observations inside the enclosing Job total, not additional independent costs.

## Integrated disposition

All three selected operations have independently audited narrow PASS outcomes.
The successor is actually assembled, the inert helper selects its real profile,
and its real public launcher discovers B after A stalls while retaining the
original conservative charges and clean closure. This closes the selected
package/entrypoint integration gap without another native mathematics campaign.

It remains a same-host loopback test over synthetic metadata, not TLS or
independent-host qualification, semantic relevance/recall measurement, a native
mathematical acceptance test, autonomous concept discovery or demonstrated useful
growth. No full-v5 completion, universal fair latency or public deployment claim
follows. Used sources, packages, controls and evidence remain frozen; no rerun or
additional campaign is selected by this audit.
