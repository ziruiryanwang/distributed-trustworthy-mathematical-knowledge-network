# Current ordinary distribution recipe

Updated 2026-10-24. This is a mutable entrypoint, not a frozen run receipt.

## Current candidate-preview development package

Use `experiments/v5-local-checks/ordinary-preview-assembly-01/package`, with
PROFILE `ab04e72440bcd09381a81d4b721d1103fa2e62bc260fa6c0434e6c568419016f`
and ASSEMBLY `6e09d2b255d8321bd522291276e03f10729cbc4f57536a57b29b63ab67a528bc`.
It changes only `peer.py` and `peer_api.py` from the approved-project package
below; the other 132 payloads, acceptance installation and owner semantics stay
unchanged. Existing adopted functionality is retained without native rebuilding.

The new [`peer.py preview`](../ordinary_preview_package/README.md) lets a local
agent inspect a candidate's type and symbol identities before paying to receive
its proof closure. No owner state opens. Exact preview/record binding is checked,
but no mathematical acceptance, applicability or index-membership claim is made.
`receive` still checks independently and fetches its own preview again.

[Independent review](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-DISCOVERY-NEXT-CHALLENGE.md)
passes 19 focused controls, exact two-file assembly and two actual packaged HTTP
calls (correct metadata and tampered-response refusal). Both calls charge their
single 1,351-byte response; no native work ran. The HTTP check used a bounded
static loopback responder, not an entire product-provider or TLS campaign.

The current source recipe is [`ordinary_preview_package/build.py`](../ordinary_preview_package/build.py)
with its `source-map.json`, using the same build arguments and a fresh output as
below. Only two direct-copy selections change; compiler lanes are unchanged and
were not rerun. This remains a development candidate, not final v5. Large-library
onboarding, useful-growth evidence and public deployment remain central open work.

## Preserved approved-project intake development package

The predecessor development package is
`experiments/v5-local-checks/ordinary-project-extraction-build-01/integration/package`,
with PROFILE
`aab7e2460c0879d0fbb2b570470984efe2a66c4a932f5725ce563a1df7c2530f`.
Its 134 payloads include three replacements from the incremental-module package
below: the owner entry, extraction controller and native missing-proof extractor.
The acceptance installation and the other 131 payloads are unchanged.

The [independent saved-outcome audit](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-MODULE-ANCHOR-SOURCE-REVIEW.md)
passes the new public workflow: a contribution correctly reports missing project
dependencies, `extract-project` retrieves their complete proof data from explicitly
approved local compiled modules, and `complete` independently checks all three
declarations above the original parent. The whole check took 21.45 wall seconds /
10.3125 known inclusive CPU seconds. No certificate, dependency rebuild, network
operation or old anchor migration was involved. This controlled project is not
an external-user or positive-growth benchmark.

Use [`ordinary_project_extraction_package/build.py`](../ordinary_project_extraction_package/build.py)
and its `source-map.json` for this predecessor source recipe, with the same build
arguments shown below and a fresh output. The changed native component was
compiled with exact retained shared objects; unchanged compiler lanes were not
rerun. Whole clean-source execution of this combined recipe is not newly claimed.
See [project-intake usage](../ordinary_project_extraction_package/README.md).

This package retains context-query and incremental-module functionality. Its
changed facade changes module-anchor support identity, so prior anchors are not
silently migrated. Their earlier evidence below remains about the earlier exact
package. The ordinary acceptance installation remains compatible with the
retained owner. This is a development candidate, not the final v5 release;
large cold imports, practical benefit and public deployment remain open.

## Preserved incremental-module development package

The predecessor development package is
`experiments/v5-local-checks/ordinary-module-anchor-assembly-04/package`, with
PROFILE `b0802fbe33b08bbf57e8050a18e96c2b1d277a75ba53192e51b487d34a3682a9`.
It contains 134 payloads plus PROFILE/ASSEMBLY. The native acceptance installation
is unchanged. Source builds use
[`ordinary_module_anchor_package/build02.py`](../ordinary_module_anchor_package/build02.py)
and its `source-map02.json`; the unchanged compiler lanes were not rebuilt.

The [independent audit](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-MODULE-ANCHOR-SOURCE-REVIEW.md)
passes all five actual module operations: new-support cold registration,
warm new-proof-only export, ordinary consumer, zero-native repeated reuse and
wrong-context refusal. See [module usage](../ordinary_module_anchor_package/README.md).
Whole-test cost was 50.89 wall / 44.359375 known inclusive CPU seconds. Different
calls perform different work; these numbers are not a matched speedup result.

The same package supports [context-bound query preparation](../ordinary_query_context/README.md).
Its actual public command returned bindings/query/specs byte-identical to the
saved manual route, under the exact selected owner context. The enclosing test
harness remains FAILED on an unjustified Windows cumulative process-count
assertion; independent saved-output checks are recorded separately. No passing
query/native/search campaign was repeated to erase that failure.
The [separate postcheck](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-CONTEXT-QUERY-IMPLEMENTATION.md)
also records a later successful zero-write catalog-lock observation. It does not
identify the extra cumulatively counted process or relabel the original run.

For a fresh source build, use the unchanged build arguments illustrated below,
but select `software/v5/ordinary_module_anchor_package/build02.py` and a fresh
output. A build's actual generated hashes need not equal this assembly's hashes.
This is not final v5, a public release, proof-free cold onboarding, or a useful-
growth claim. Public deployment and licensing remain undecided.

## Preserved query-enabled predecessor

Use `build03.py` with `source-map03.json` for this predecessor source recipe. It adds
proof-free type queries and the exact installed-theorem export policy. The
unchanged base/extractor phases and separately validated query compilation were
reused in a file-only assembly; a complete build03 run was not repeated.

Its actual locally assembled package is
`experiments/v5-local-checks/ordinary-query-assembly-01/assembled/package`, with
PROFILE `2b8ac8cad152dde90a1b51d19dd1a821305bd7242b601c10eaa7a39f0db572f5`.
It contains 133 payloads plus PROFILE, with the previous native acceptance
installation unchanged. This identity describes this assembly, not all builds.

An [independently audited public workflow](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-QUERY-PUBLIC-OUTCOME.md)
now passes: a local proof-free type query drives actual loopback discovery, the
returned target drives a checked mixed-module export, and a normal Lean file
uses the new theorem. Whole-workflow cost was 45.15 wall / 23.390625 known CPU
seconds, including a deliberate 20-second service lease. This is controlled
compatibility evidence, not search speed, useful growth or a public release.
See [query package usage](../ordinary_query_package/README.md).

The build02 invocation below remains a preserved predecessor example. CLI flags
and supported runtimes remain unchanged. No license or external publication is selected.

## Preserved one-helper predecessor

Use `build02.py` with `source-map02.json` for a fresh source build. The earlier
`build.py`, `source-map.json` and README preserve the original build checkpoint;
their extraction helper is incompatible with a freshly rebuilt extractor whose
binary identity differs from the historical executable.

The successor binds extraction to the exact executable role in the operator's
approved package profile. It does not accept a peer-selected executable, change
the extractor protocol or grant mathematical authority to extracted material.
Explicit `complete` still independently checks the contributed full proofs.

The build CLI and supported Windows Python 3.14.6 / Lean 4.34.0 distributions
are unchanged. For example, with complete runtimes and a fresh output:

```powershell
& 'C:\tools\Python314\python.exe' -I -S -B `
  'C:\commons-source\software\v5\ordinary_distribution\build02.py' `
  --source-root 'C:\commons-source' `
  --python-runtime 'C:\tools\Python314' `
  --lean-runtime 'C:\tools\lean-4.34.0-windows' `
  --output 'C:\commons-builds\current-02' `
  --wall-seconds 600 --cpu-seconds 600 --memory-mib 2048
```

These allowances are explicit example choices, not guaranteed requirements.
The caller needs the selected source files, supported compiler tools and complete
runtime distributions. This is not a hermetic build. The generated package uses
only its own payloads and the separately selected runtimes; it does not need
historical experiment trees to operate. See the preserved README for the
unchanged build stages, resource accounting and output layout.

## Evidence and current boundary

The original complete source build is already independently audited. The
successor changes one Python helper; all compiler inputs and recipes are exactly
unchanged. We therefore reused its generated artifacts in a separate file-only
assembly instead of repeating compilation. That assembly has 126 payloads:
125 unchanged and one replacement, plus the newly derived `PROFILE.json`.

The resulting profile is
`192dfee12ac186fbdac0634212b28c1c6324222da2b035f8f295ec764303a68d`.
It identifies this particular locally assembled package, not all future builds.
The current source build recipe derives hashes from its actual generated bytes;
future builds need not produce this same binary identity.

Actual relocated use now passes its independent saved-outcome audit: a fresh
owner checked a definition and theorem, exported a proof-bearing module, and a
normal Lean consumer used both its theorem and definitional reduction. A separate
branch recovered a genuinely missing installed theorem using the newly built
extractor, then independently checked the two-theorem completion. The whole
workflow took 53.94 wall seconds / 48.703125 known inclusive CPU seconds on this
PC, without a source rebuild, old owner state, network or certificate. This is
controlled interoperability evidence, not a real-user usefulness comparison.

The
[live review](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-CURRENT-SMOKE-REVIEW.md)
records source, pure-control, assembly and later workflow evidence. This is a
development package, not final v5, independent-host evidence or a growth result.
No license or external publication has been selected.
