# Real aggregate adoption/request preflight: minimal source contract

Initial status: **DESIGN ONLY; NO RUNTIME SELECTED BY THIS NOTE**.
Owner: `memo_tests_review`; root selects implementation and any finite launch.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
This investigation inspected source and saved data only; it imported or executed
no product code. The product candidate remains `aggregate_resources/producer.py`
SHA256 `1d191bdc2079760ce89a57a08924254f01487d24726e10b386c7eca1ef9eec09`.

## Purpose and shortest credible operation

One private, native-free integration preflight should instantiate the **real**
`AggregateProducer(profile)`, then call its real `_request(request)` exactly
once and finally `close()`. It must not subclass, bypass constructor checks,
mock adoption, fabricate a capsule, patch the support supervisor, call `run`,
invoke any host, reserve proof stages or create a production output directory.

This validates an important seam the seven focused policy controls deliberately
mock: real stage-build adoption, real guest/image adoption, actual supervisor
loading, exact source pins and complete retained snapshot/request correspondence.
It is a private test of an existing method, **not** a new public API or authority
to produce a receipt. Successful parsing is not fresh cryptographic verification
of the retained I premise or validity of the untrusted execution capsule.

The code path supports this distinction: constructor loads pinned Python
helpers and checks records/files; `_request` checks pins/header/capsule prefix,
saved snapshot evidence, graph/history/limits and returns a plan/envelope.
`run` alone creates the production directory and invokes the supervisor for
proof stages. Calling neither `run` nor any native helper is sufficient here.

## Genuine profile inputs

Abbreviate `HERE = <canonical root>/experiments/v5-local-checks`.
All pins must be selected explicitly before launch, never adopted solely
because a live file can be hashed. Reuse the prior independent adoption records.

| Profile role | Exact retained source |
|---|---|
| Base support-profile template | `HERE/module-base-production-01/profile.json`, SHA256 `71af83f7c4822d8d2a322e93dda5f08a59311614d434ab887cc5c33c318d84d0` |
| Supervisor manifest | `product-local/v4-library-commons-02/commons-v4/RELEASE-MANIFEST.json`, SHA256 `a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed` |
| Running Python/DLL and16 runtime pins | Same installed paths/pins as that retained support profile; runtime pins total10,270,560bytes. This is not a hermetic OS closure. |
| Support host | `HERE/aggregate-stage-host-build-01/aggregate_stage_host.exe`,67,992,064bytes, SHA256 `1266b6c990fc21f04f80f88c714a22d7841e4819c64bee0746992a47858a32ac` |
| Support image ID A | `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60` |
| Relation image I | `9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e` |
| Foundation and policy | Exact retained support-profile F/P, also present in the actual192-byte header |
| New profile schema | `DMKN_V5_AGGREGATE_PRODUCER_PROFILE_V2`; mandatory explicit stage-memory ceiling, proposed8192MiB for this **non-executing quote** |

Keep the old support-profile schema and its unchanged loader helpers, but replace
the template's old module host/image with the actual aggregate host/A. The new
outer profile has its own two source pins and the exact relation image I.

**Snapshot path trap:** if the outer runner imports the selected source snapshot,
both source-pin pairs must name those actual imported paths. The support pair
is the selected snapshot's `production/producer.py` and `production/__init__.py`;
the outer pair is the snapshot's `aggregate_resources/producer.py` and marker.
Do not copy the original absolute source paths from the retained support profile
while importing different snapshot paths. The constructor intentionally rejects
that mismatch. Preserve the exact old support-source hashes, not its old path
roles. Check imported origins and selected bytes before constructing the owner.

### Stage-build adoption map

Use `host_build` keys exactly `result`, `attempt`, `selection`, `source_map`,
`command`:

- `aggregate-stage-host-build-01/RESULT.json`;
- adjacent `aggregate-stage-host-build-01-attempt.json`;
- adjacent `aggregate-stage-host-build-01-selection.json`;
- build-root `source-map.json` and `compile-command.json`.

The exact pins and audited source/closure chain are in
`AGGREGATE-BUILD-OUTCOME.md`. Its three actual snapshotted Rust/builder source
paths are added by the real constructor. The runtime preflight does not rehash
the2.32GB compiler/link tree; the build record binds that separately reviewed
inventory.

### Image-adoption map

Use `image_adoption` keys exactly:

| Key | Path under HERE |
|---|---|
| `result` | `proof-memo-image-assembly-01/assembly/RESULT.json` |
| `outer` | `proof-memo-image-assembly-01/RESULT.json` |
| `selection` | `proof-memo-image-assembly-01/selection.json` |
| `guest_build` | `proof-memo-guest-build-01/RESULT.json` |
| `guest_selection` | `proof-memo-guest-build-01/selection.json` |
| `guest_source_map` | `proof-memo-guest-build-01/SOURCE-MAP.json` |
| `artifact` | `proof-memo-guest-build-01/ARTIFACT.json` |

Inner assembly result SHA256
`8a2174ad097333a54f3a314d63f0e646607a639aa5755efdd31c2ee1d08d43ea`;
outer result `50de313fbc8f20b3f48d971f3183bf66f1079cafe18af460538b414d715a2f4e`;
guest selection `16730dce90438a8ee83215af842babfc0def7ef1ef89a6a8bf901c8e05b855b9`;
guest source map `3ba8ee6781f249d9a49e9d1befb4d1becb8f899fd6f1a70270a8fa36eed76829`.
Inner/outer records are not interchangeable. The actual image is
`proof-memo-image-assembly-01/assembly/aggregate_image.bin`,1,745,920bytes,
SHA256 `98686ced7979d55685c648f441f7ffbe40712e327a1311f9cb076a0c7250e773`.
File hash and cryptographic image ID remain different fields.

## Genuine request and snapshot map

Reuse the complete `frontier-capability-execution-01/evidence` capsule, not a
new guest execution. Its exact session has s=113,m=1,cycles=67,108,864,po2=19:

- Capsule37,187,089bytes, SHA256
  `7996306944a51e0eec597266819871115f4bdea1f799c944442e472869465ffd`.
- Session binding `bdd42310ed62504e78e4da164b633da7751597eda74eb00b873a06c552268649`;
  capsule binding `28908f4aaf31d289c374047129dbf5c1e65c36def34ea877a59366b3185732f9`.
- `wire.bin`:215,540bytes, SHA256
  `2aea63ff488a4c012233742306c71526aea37c67d9f8d214e94c0d95d1200cb4`.
- `header.bin`:192bytes, SHA256
  `2bec7b73408dda33c1490360ea34330a846861283a5a5ee6ec6b7632bc5211e4`.
- Ordered sole parent `module-base-production-01/finish-0/receipt.bin`,223,594bytes,
  SHA256 `850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.

Use `snapshot_evidence` keys:

| Key | Path under HERE |
|---|---|
| `result` | `frontier-capability-execution-01/evidence/RESULT.json` |
| `outer` | `frontier-capability-execution-01/RESULT.json` |
| `selection` | `frontier-capability-execution-01/selection.json` |
| `configuration` | `frontier-capability-execution-01/evidence/configuration.json` |
| `command` | `frontier-capability-execution-01/evidence/COMMAND.json` |

The copied configuration bytes match external selected configuration SHA256
`d4d9751b155bc4b04e9d110ca23bfe31a8adc34e267d86fd00003da6c64004bd`.
The real parser reconstructs the outer argv's `{snapshot}`/`{output}` expansions
and checks the selected external config path/hash. Its native COMMAND names the
retained **snapshot** host `aggregate-host-build-01/aggregate_host.exe`, not the
new **stage** host. Both host pins are therefore needed, in their distinct roles.

Prospective request: exact existing REQUEST_V1 schema, no checkpoints, no prior
attempts, stage_limit340, and a fresh designated production-output path whose
parent already exists, e.g. `HERE/aggregate-production-planned-01`. Verify it
stays absent before/after preflight. Use a unique owner-selected quote identity
and record `NOT_A_PROOF_ALLOWANCE`; the request is never passed to `run` or
reused later as proof funding merely because its shape validates. Carried costs
must come from the explicitly selected retained cost records with scope and
omissions stated; do not call earlier creation/proof work free.

## Full-path quote and separate feasibility facts

Proposed **planning caps**, not proof execution authority:

- CPU caps segment1700,lift250,join250,resolve600,finish300 seconds.
- Whole worker250000,controller3600,wall86400 seconds; output2048MiB/8192entries.
- Every artifact512KiB; each stdout/stderr64KiB; existing two-process ceiling.
- Profile ceiling8192MiB; per-kind memory must be explicitly selected at or below
  it (e.g. segment8192, other kinds4096). The preflight itself does not need8GiB.
- Per-stage wall ceilings remain within the existing600seconds; no limit is
  automatically enlarged after preflight or a later failure.

With no prior stages, the genuine `_request` result should expose340missing host
calls/339proof stages,113segment/113lift/112join/1resolve/1finish, selectedCPU
249250, conservative new output940,048,384bytes (896.5MiB),2724entries, and
maximum host-read99,141,167bytes. Fixed host inputs total39,372,335bytes; finish
adds114checkpoint bounds of524,288bytes. Actual request input totals and the
constructor installation-pin totals must be reported from the real returned
maps and separately satisfy512MiB; neither equals the host-read expression.

Also report these **extra facts**, because `_envelope` does not check them:

1. Compute every prospective argv using the real `stage_argv` and graph-derived
   dependency paths, without creating them. Count `subprocess.list2cmdline`
   output in UTF-16 code units plus the terminating NUL; require<=32767 and
   report the maximum and its stage. No shell invocation or fake file pins are
   needed for this pure path calculation. Root must freeze the prospective
   output path so the result is reproducible.
2. Check the internal complete-composite serialization bound, not only final
   succinct receipt size. With fixed-int bincode, two Vec headers and the
   parameter digest add48bytes. Segment payloads are no larger than their
   checkpoint artifact caps. The one erased parent assumption is no larger
   than its existing223,594-byte Receipt: it preserves succinct fields,
   replaces the claim by a36-byte pruned claim, and removes at least the
   journal Vec header8 plus metadata digest32; both enum tags are4bytes.
   Therefore a conservative bound is
   `113*524288 + 223594 + 48 = 59,468,186 < 67,108,864` bytes. This is a
   source-derived upper bound **conditional on stage artifact caps**, not a
   new bincode execution or assurance that actual proofs meet those caps.
   See pinned SDK `receipt.rs:116,314,778`, `receipt/succinct.rs:258` and
   `receipt/composite.rs:45`, plus stage-host finish at`:316`.
3. Report both unknowns explicitly: actual po19 proving memory and actual stage
   CPU/artifact sizes. A configured8GiB limit is not provisioned capacity;
   these planning caps do not prove feasibility or authorize a pilot.

The distinct full-path reviewer owns independent challenge of those arithmetic/
serializer/argv claims. This adapter need not parse or fabricate Rust receipts.

## Minimal adapter outputs and launch boundary

If selected, one new private adapter with a pinned configuration can save a
fresh profile, prospective request, genuine preflight report and exact input/
import-origin map in its own small evidence directory. Constructor/request
failure is retained with exact exception and reached-phase information; there
is no repair/retry loop. `close()` runs on a successfully constructed owner,
and final pin/path/output checks must be preserved. Unexpected final-binding
failure overrides a previously prepared PASS report.

Suggested finite **preflight-only** outer envelope:30CPU/90wall seconds,
512MiB, one process,1MiB stdout/stderr,12MiB/64 evidence entries. Root must
review/select the actual adapter and exact sources/data before any import.
This is deliberately unrelated to the8192MiB prospective proof ceiling.
Potential output status: `PASS_REAL_ADOPTION_AND_REQUEST_PREFLIGHT_ONLY`;
include host_calls=guest_calls=proof_calls=0, mathematical_admission=false,
proof_funding=false, private_api_test=true, and actual controller/outer costs.

A pass would remove evidence-schema/preparation uncertainty cheaply. It would
not validate a host execution, certificate, future machine capacity, actual
full proof cost, network growth or final v5 release.

## Subsequently selected source implementation

Root selected only fresh `software/v5/aggregate_resources/preflight_actual.py`.
The source is21,982bytes, SHA256
`07b8fc63269f8033885747554c99a60e0682cacd54c040f1d7f3c26605eb6a15`,
pending independent source review and a separate exact root runtime selection.
No extra product API, asset helper, constructor mock or test-suite import was
introduced. CLI is `--output {output}/evidence`, where the outer runner has
already created its source snapshot and `selection.json`. No separate config
is needed.

Source closure is five files: the private adapter, new resource package pair,
and unchanged legacy production pair. Existing runtime/data closure is51files:
19 exact retained records, seven exact assets,19 retained template inputs
(supervisor manifest, Python/DLL and16runtime pins), three manifest-selected
supervisor helpers and three actual stage-build source snapshots. The root
selector must pin every one; the adapter checks each existing read against the
enclosing selection's `runtime_pins`, not just against a hash discovered at run
time. The returned real owner's installation/input maps are compared against
that selection plus the five actual source files. The enclosing selection
itself is a runner-created control document, not a recursively self-pinned input.

The original adapter draft caught two concrete preparation mistakes before
execution: Run-V5-Check's `sources` values are SHA strings, not byte/hash records;
the retained snapshot executable is6,626,304bytes, not the larger stage executable.
Both are corrected in the hash above. The snapshot executable remains exact
SHA256 `b1605995c957e06b7c4529d28dfc2a49e496cefae7629b3fdddfc4a1bfb6f6d1`.

The code binds real snapshot-local package origins, records the actual
constructor/_request phase, never calls `run`, and uses `list2cmdline` only as
a pure quoting function. It saves profile/request/argv-envelope/input-map and
RESULT; prospective proof output remains absent. Existing input/source and
generated control bytes are rebound both before and after RESULT; a post-result
failure emits a create-new overriding `FINALIZATION-FAILED.json`. Evidence is
bounded at12MiB/64entries, with report/sentinel reserves. Inner CPU is part of the
enclosing Job and must not be added to it again.

The carried subtotal is computed from pinned base-I production (including its
recorded prefix), this stage-host build and retained capsule acquisition. Its
scope explicitly excludes other preserved costs, not calling them zero. The
prospective request is marked by a quote-only identity; no actual allowance is
reserved. All code creation used `apply_patch`. The author performed no import,
test, native call, proof or Git operation.

## Source-only wall-cap correction before selection02

The preceding implementation pin is historical. Root selected four localized
hunks in the still-unused adapter; the product producer, prepared selector01
and plan01 remain unchanged. The corrected adapter is22,623bytes, SHA256
`4720822d4174c2808db57972046cd23b16189fd6769981d36811540e9f918f27`.

The old uniform600-second stage wall caps summed to204,000seconds across340
host calls, exceeding the prospective86,400-second whole-operation wall cap.
The genuine `_envelope` checks other dimensions but does not check this sum.
That omission did not justify claiming the complete serial cap envelope fits.
The correction adds per-kind wall caps, uses them in the hypothetical budget,
requires their exact graph-weighted sum and slack, and reports both explicitly:

| Stage kind | Count | Wall cap per call (seconds) | Weighted cap (seconds) |
|---|---:|---:|---:|
| segment | 113 | 420 | 47,460 |
| lift | 113 | 150 | 16,950 |
| join | 112 | 150 | 16,800 |
| resolve | 1 | 600 | 600 |
| finish | 1 | 120 | 120 |
| Total | 340 | | 81,930 |

Thus86,400-81,930=4,470seconds is unallocated total wall slack for controller
transitions and finalization. It is not a completion guarantee or evidence that
actual proof stages satisfy their caps. CPU, memory, artifact, read, output and
entry caps are unchanged. No new proof funding or runtime selection follows.

Data-only reverse substitution of exactly these four hunks reconstructed the
21,982-byte predecessor with its exact07b8fc63 SHA256 above. Independent
PowerShell integer arithmetic confirmed81,930 and4,470; no Python import,
test, native call or proof was executed. Root's fresh selector02/plan02 must
bind the corrected4720822d adapter; previously prepared controls are preserved.
