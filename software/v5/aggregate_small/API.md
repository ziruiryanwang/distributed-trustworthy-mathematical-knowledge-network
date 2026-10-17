# Bounded small-segment aggregate producer

This package is the same-mathematics, po18/N256 successor to the retained
aggregate producer. It is an owner-controlled production service, not a peer
acceptance API. A saved report or checkpoint is never a mathematical warrant.
The receiver still verifies the actual resulting receipt under its own policy.

## Public operation

`AggregateProducer(profile)` adopts the pinned supervisor, real stage-host build,
actual aggregate image and this package's source bytes. `run(request)` performs
one finite ordered prefix of the missing proof graph. `close()` ends the owner.
`report()` supplies local operational observations, not complete external cost.
The owner must separately bound startup, construction, refusal and exit tails.

Profile schema is `DMKN_V5_SMALL_AGGREGATE_PRODUCER_PROFILE_V1`; request schema is
`DMKN_V5_SMALL_AGGREGATE_PRODUCER_REQUEST_V1`. Old profiles are not upgraded
implicitly. The profile includes an explicit stage-memory ceiling; it does not
reserve memory or prove that a stage will fit.

Requests bind a completed actual po18 execution capsule, A/I/F/P/H, ordered
parent receipts, actual snapshot evidence, every retained successful checkpoint,
fresh output location, exact finite budget and all prior attempts in the same
allowance. Checkpoints cannot be dropped to erase success or costs. A new
geometry needs a new capsule/session and allowance; old bytes are not relabelled.

## Dependency transport

Each call writes and syncs a new `dependencies.json` beneath its stage directory.
The `stage-manifest` command passes that file's exact path, byte count and SHA-256,
not a growing checkpoint argv vector. The file identifies session, capsule,
canonical stage key and ordered `{key,file:{path,bytes,sha256}}` rows. Both sides
derive the required dependency order. The native host checks actual bytes and
performs unchanged SDK verification; a file hash is not proof validity.

The manifest pin is in the reservation and result and is rebound alongside the
other inputs. The new command has `16 + parent_count` arguments including the
executable and checks the actual quoted Windows command-line bound. Legacy
trailing-checkpoint arguments are not accepted.

## Operational bounds

| Object | Bound |
|---|---:|
| Execution geometry | po18, at most 256 segments and 8 assumptions |
| Complete graph | at most 776 host calls / 775 checkpoints |
| Capsule / retained execution-segment sum | 96 MiB each |
| Parent receipt | 1 MiB each |
| Every retained/new checkpoint and final receipt | 512 KiB each |
| Internal complete composite | 160 MiB; never sent to clients |
| Host reads / initial request inventory | 512 MiB each |
| Fixed request remainder excluding capsule/checkpoints/prior reports | 20 MiB |
| Newly generated active administrative pins | separate 128 MiB |
| Snapshot output | 208 MiB / 288 entries |

Per-kind manifest bounds are 2/4/6/4/256 KiB for segment/lift/join/resolve/finish,
with at most 257 rows. Complete-composite integrity, exact claim equality and
final fully resolved A/H receipt verification remain mandatory. These are local
operational restrictions, not a claim that larger valid mathematics is false.

## Build and layout

`build_snapshot.py` and `build_stage.py` each require a separately selected exact
plan and link once against retained SDK/relation libraries. They do not rebuild
the guest or launch proofs. `capability_snapshot.py` requires a separately bounded
outer owner and a configuration containing the actual snapshot-host build's
five record pins (`result`, `attempt`, `selection`, `source_map`, `command`). It
executes one fresh complete layout of the retained mathematics at po18. The
result is an untrusted execution capsule, not a certificate.

No script here authorizes an automatic retry, cap escalation or full proof run.
Use actual layout and build records to compute complete-path cost and capacity
before choosing proof stages. The first informative segment does not establish
all later stages' peak memory or a positive full-cost sharing benefit.

## Evidence boundary

Focused Python controls exercise new graph/manifest/request/accounting seams
with explicit synthetic adoption and inert dispatch. They do not test native
JSON decoding, cryptographic soundness, real proof production or network growth.
Actual source, build, layout, production and public reuse outcomes are recorded
separately in the research checkpoint. This package is not by itself a v5 release.
