# Independent actual fresh init01 audit

Disposition: **PASS_FRESH_PUBLIC_INITIALIZATION**.

Saved run: `experiments/v5-local-checks/std-kernel-init01`. The reviewer read
saved JSON/logs/artifact bytes and hashes only. No owner/status/recovery call,
database API, native execution, artifact import or Git operation was performed.
All four current/source-snapshot pairs and 207 external pins still match the
selected bytes. The saved selection is
`a3a4ea1c0c310b51b6a315762fb3f69182d36806b595b7c4eb3b5638c11fb453`.

The child reports `ok=true`, `INITIALIZED_LOCAL_OWNER` and a genuine `CHECKED`
basis with 456 units and no retained extension units. Its actual new bindings are:

| Binding | Value |
|---|---|
| Local basis root | `4d7cc70e515293b3037a8fa34f60fa97fe082196e005aa7cd894204464ca5f2b` |
| Store ID | `fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7` |
| Implementation | `86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea` |
| PROFILE | `60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b` |
| INSTALLATION | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |

Catalog/custody are the selected fresh `std-kernel-catalog01` and
`std-kernel-custody01`. Reported catalog defaults and custody quota match the
selection. The catalog's ADOPTION document exactly matches the installation's
implementation, store and reported limits. No old owner identity is reused.

The one native call is
`std-kernel-catalog01/admission-calls/f272777043d1091818da7cfc8f5dab678321f1177f6799da513638e72769464e`.
Its command and retained installation bind the selected fixed seed/inventory,
new root and exact artifact/report paths. The native report is `kind=basis`,
456 units, anonymous parent, `DMKNLocal.r<new-root>` module and 581 names.
Every reported name matches the corresponding fixed inventory row. Its trace
contains 456 check-begin records and an exact received inventory, followed by
the 456-unit/581-export completion. The trace is supplementary evidence; the
reviewed controller grants CHECKED only after clean native event, report/artifact
binding and catalog commit.

The actual artifact is
`operations/7816507ebfdacca0e8de26d1100226c7d9a6c37fad07229373a491e39bef7bc8/chunk.olean`
under that catalog: 669,968 bytes, SHA-256
`627f13203ff33d4134daad615a81c53238a037a6ec74e8155816788fb3132bc5`.
Its size agrees with the native report. This is a fresh artifact, not promotion
of the former owner's basis or failed extension. No WITHDRAWN marker is present;
absence is not independently used as an acceptance warrant.

Native, public and outer supervision all show zero exit, reaped children, closed
Jobs, no active/terminated processes, no termination request and no cleanup error.
All three stderr files are empty. Public LAUNCH/RUN/owner paths and identity
bindings agree, and outer stdout equals the saved public RUN document. No hidden
owner refusal or close error appears.

Outer wall time is 10.856913 seconds. Inclusive Job CPU 9.5625 plus wrapper
1.078125 is **10.640625 known CPU seconds**; nested native CPU 8.078125 is already
included. Peak aggregate private commit is 708,530,176 bytes. No limit event
appears. Key evidence hashes:

| File | SHA-256 |
|---|---|
| RESULT.json | `f7cc1749568202e61eb369161869bdc7fa4527004c58fa744b67e9facf1a1de8` |
| public-launch/child/stdout.txt | `a3211d8cce75e030112d25772ea4ac905b1d3de70b09e677729e380262e49d4e` |
| native worker-report.json | `5cc2d47a6098c32f0e6c5775cdb091c74a483010caf4aabffcfaf3736cb09162` |

This establishes the new checked basis through the public owner path. It does
not qualify the Std intake, growth workflow or final v5. Root may adopt this
actual basis and separately select intake; no old-state recovery, automatic
retry or allowance renewal follows.
