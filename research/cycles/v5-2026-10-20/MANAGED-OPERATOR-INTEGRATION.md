# Integrate managed generations through the existing installed `run` entry

2026-10-21, core_release. Source-only design selected by
`MANAGED-OPERATOR-INTEGRATION-SELECTION.md`. No implementation, build, import,
clock adoption, service launch, deletion or Git action. Root owns any later
selection. Current qualification outcomes remain recorded by root, not inferred
from this proposed integration.

## Decision

**Add one ordinary installed owner script, not a new builtin or launcher.**
Use the public `distribution.py launch RELEASE_SHA run REQUEST REQUEST_SHA`
command unchanged. Add the four existing lifecycle/composition modules and one
small `client/managed_owner.py` orchestration module to the next source map.
Its `main(context)` supports finite owner operations; service operations invoke
the selected `sessions.supervise` and unchanged `client.boot` for the worker.
No test-only module loader, private database patch or copied supervisor belongs
in the ordinary operator path.

The adopted installation has 121 SDK entries. The proposed map has **126**,
within the actual builder's 141-entry limit. This is a new reviewed distribution
selection, not an in-place edit or migration of consolidated121.

## Actual entry points resolved from the adopted input

Source of truth is `experiments/v5-local-checks/distribution-consolidated-01-input.json`,
SHA-256 `8ba3707236c1a6e01ab7f87886814f801034b2fe9144ad9603585adcc73feb33`.
Its distribution source is `software/v5/body_location/distribution.py`,
54824 bytes, SHA-256 `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813`.
It is not an older terminal/interface distribution module.

| Logical source | Exact selected SHA-256 | Relevant behavior |
|---|---|---|
| `v5/client/launch.py` | `523a3031da86457037af3c41f87425cd406e5fe3fcf6a2edb2d87eff9b59ef78` | Validates a finite plan, selects exact helpers, calls existing `A.supervise`, preserves original wrapper clocks. |
| `v5/client/boot.py` | `76cdcd42379d61c5fe37dc86a23363687c084c56887302dcdd922aa9b089ce2b` | Authenticates/snapshots exact source map, installs its pinned import guard, creates immutable `Context`, invokes `main(context)`. |
| `portable/location/controller.py` | `4dc0824d758e72fce591dbd9dddb9e487bcd0506cfaf4a71e894b0166b84e064` | Supplies adopted exact Node/source runtime and finite process/channel ownership. |
| `portable/location/controller_services.py` | `eeb82d5dd6fe34915d07b2927e7ddd44ee2b5b80278dbf4d2889b87222ad1501` | Supplies the selected `ServiceLocationProcess` and exact five role-source pins. |

The public request schema remains `DMKN_V5_INSTALLED_REQUEST_V1`, with the
existing fields `name`, `workspace_root`, `parameters`, `limits`, `output_limits`,
`owner` and `runtime_mode`. `owner={root,entry,sources}` selects explicitly
trusted local Python by exact byte count/hash. An operator can select the new
script directly from the new installation's `sdk/v5/client` directory:

```text
owner.root    = <adopted-install>/sdk/v5/client
owner.entry   = managed_owner.py
owner.sources = { managed_owner.py: <that exact release row> }
```

The file is then copied into the normal `owner/` source snapshot. No additional
wrapper file or modification to the closed builtin-command map is necessary.
The duplicate SDK/owner copy is the same small pinned file, not a second codebase.

For compatibility, existing `run` requires `runtime_mode="atomic"` or
`"aggregate"` even for a service-only owner. Select `"atomic"` and do not request
runtime placeholders or instantiate `RuntimeProfile`. The existing wrapper may
write its ordinary preparation description; this is **not** trust-domain
creation, mathematical issuer adoption or proof execution. Changing the public
schema merely to remove this unused description is not necessary for this cut.

## Smallest source delta

Add these exact existing files to the new SDK map:

- `v5/placement/lifecycle.py` from supervised_generations, `bec62143313e1abd400550bae45a6334be2ddffb94d77a14ba9b5853b565042f`.
- `v5/placement/sessions.py` from supervised_generations, `b4cfab61c990464756e87a7344e2a029a5374602283a4255d4d5aa854090b7f7`.
- `v5/placement/reclaim.py` from bounded_reclamation, `19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894`.
- `v5/client/serve_generations.py` from bounded_generations, `404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687`.

Author only the fifth source, `v5/client/managed_owner.py`, in a fresh selected
source directory. Its responsibilities are strict owner-parameter validation,
exact context/profile construction, dispatch and structured outcome reporting.
It must not duplicate lifecycle SQL, reclamation, `PlacementService`, Job cleanup
or boot/import-guard logic. Builder, distribution schemas, public launch/boot,
existing reader/serving entries and mathematical acceptance remain unchanged.

## Concrete operations and reusable calls

Use one bounded owner parameter schema, proposed `DMKN_V5_MANAGED_OWNER_V1`.
Every operation names an exact `manager_root`, complete manager config and
adopted release identity. The manager root is a persistent private sibling of
operation directories, disjoint from the installation/source roots. A new
request never silently recreates a missing root or resets its epoch/session cap.

| Operation | Calls and required owner choices |
|---|---|
| `initialize` | `ManagedGenerations.open(..., create=True, deadline=context.deadline, calls=..., cpu_seconds=...)`, `status()`, `close()`. Creates the new supervised schema only; takes explicit two-slot allocation, protected roots, clock-model ID and session cap. |
| `status` | Open the exact existing manager, `status()`, `close()`. It reports existing charges, phases and session state. A normal reopen conservatively changes saved RESERVED/LIVE/CLOSING to UNKNOWN; it is not a concurrent read-only inspector or recovery claim. A held owner lock yields refusal. |
| `serve` | Parent opens manager and calls `sessions.supervise`. Joined worker optionally `allocate(slot, generation_config)` or selects an exact current generation, creates `GenerationServices`, calls `start_slot`, serves for a finite interval and closes exact roles in `finally`. New-generation allocation is explicit, never inferred from failed lookup. |
| `seal` | Same joined worker/service path; call `manager.seal(generation)` while its exact service is live, then close. This consumes a new run if no service is already live. It is not a metadata-only phase update. Normal busy guards remain; no retry loop or guarantee of seal-before-first-listener is invented. A serve request can instead explicitly seal its already live service at its chosen finite point. |
| `retire` | Fresh owner asserts the current conservative-clock model, calls `adopt_clock`, `begin_retire`, `commit_retired`. Original horizon must have elapsed; only NONE/CLOSED/QUIESCED_UNCLEAN with no live handles can commit. Unknown closure is a refusal, not a request to repair private state. |
| `reclaim` | For RETIRED, explicitly select the original bounded private-layout profile and call `begin_reclamation`; for an existing RECLAIMING intent, reuse its stored profile without replacing it. Execute exactly one `reclaim_step(generation,max_entries=...,deadline<=context.deadline)`. Report partial progress/FREE or the original refusal. No recursive cleanup, resetting calls or implicit loop. |

`serve` may explicitly request fresh manager initialization on its first call,
using exactly the same create=True preconditions as `initialize`; the default is
open-existing. This ordinary first-start convenience avoids needing a separate
test-only initialization route. It must not fall back from failed open to create.

Current `GenerationServices` runtime data comes from the actual worker context:
`source_root=context.sources_portable/"location"`,
`installation_root=context.installation`, `source_pins` drawn from
`context.source_sha256["portable/location/"+name]` for `SOURCE_NAMES`, and
`role_pins` likewise for `ROLE_NAMES`. No development-machine absolute source
path is embedded. The controller retains its exact selected runtime validation.

Service shutdown uses the actual existing asynchronous close path; afterward
`manager.close()` succeeds only with no owned actor handles. All attempted
roles must be drained even if another raises. A child error is retained as an
error. Parent quiescence can justify unclean retirement capability but cannot
turn a failed service run into orderly operational success.

## Reuse the existing boot for the supervised worker

The parent `main(context)` is already inside the existing public launcher's
finite Job. It invokes the selected session supervisor for one nested child Job;
the direct worker and its Node descendents remain within both applicable Jobs.
Neither breakaway nor a new daemon is needed.

The new owner script prepares a normal `DMKN_V5_CLIENT_LAUNCH_V1` child plan:

1. Read/recheck the existing parent `context.run/"plan.json"` and its exact source
   rows against `context.source_sha256`. Require the owner entry to be this exact
   release-selected managed script. Copy **the map**, not an arbitrary module
   path, into the child plan; source roots are the current immutable parent
   snapshot (`context.sources_v5`, `sources_portable`, `sources_owner`).
2. Create a fresh child run directory and plan under this operation's work tree,
   disjoint from the persistent manager. Use the unchanged `client.launch`
   validators and exact plan encoding/hash. Validate owner-selected finite inner
   limits and output bounds; reserve the whole inner wall+cleanup interval inside
   `context.deadline`. Include worker mode and the internally derived profile ID
   in its parameters, not arbitrary Python code.
3. Invoke installed Python `-I -S -B` with the snapshot's unchanged
   `client/boot.py`, the child `plan.json`/hash, and fixed child started/deadline
   clocks satisfying its exact `deadline-started = limits.wall_seconds` check.
   Select those child clocks **before** calling `sessions.supervise`; they may
   therefore be earlier than the session's main deadline, never later. Keep
   service close margin within the earlier child deadline. The supervisor's
   prospective cleanup remains inside the original parent deadline.
4. The same managed owner script receives the ordinary child Context from boot.
   Worker mode first opens the exact manager and calls
   `join_current_worker(derived_profile_sha256)`; it cannot be entered merely by
   copying a request flag or nonce. Only then allocate/reserve managed resources.
5. The parent retains exact Job/direct handles through the session callback and
   emits both unchanged supervisor outcome and durable lifecycle outcome. For
   success require genuine worker success and the usual boot completion/post-
   binding conditions; saved report JSON never supplies recovery authority.

This adds a **plan adapter**, not a second source loader or process launcher.
The unchanged boot performs its import/runtime checks in the child, even though
that repeats some startup checks. Do not remove these checks or assume parent
module objects survive in the new interpreter. Parent/helper loading must use
fresh nonconflicting aliases for the exact manifest-pinned A/J modules; the
existing boot has already registered `_dmkn_client_supervisor`. The ordinary
`domains` compatibility module is loaded only from its exact selected helper;
an unexpected existing binding is refused, not overwritten.

## Profile, authority and refusal boundaries

Derive the profile internally from the exact adopted release/base manifests,
logical source hash map, managed-owner entry, selected fixed supervisor helpers,
worker role and ownership model. Verify the release map against the context and
current selected file bytes. The caller still explicitly adopts the trusted
release/owner code: a random supplied digest is not a safety proof. Use logical
source identities in this profile so the worker can recompute it after snapshot
relocation. The command's concrete paths/parameters remain separately bound by
the session's command digest; avoid a circular plan-hash/profile-hash definition.

This operational profile does not create or reopen mathematical trust domains.
Neither owner intent nor administrative state affects mathematical acceptance.
The current clock adoption is a separate fresh operator assertion, never a saved
timestamp silently reissued as authority. All nested calls receive remaining
original deadlines; CPU/call/session/run/reclamation caps stay charged on failure.

Use distinct machine-readable refusal codes/outcomes for old/mismatched manager
schema, unknown process closure, stale session/foreign worker, unclean restart,
retention still promised, exhausted session/run/cleanup cap, changed source map,
busy seal, unknown layout and commit uncertainty. The owner entry reports them;
it does not catch them to change schemas, bypass limits or repair state. Total
supervisor loss and the existing suspended-before-assignment gap remain outside
the supported recovery claim.

## The one necessary new integration boundary: ordinary multi-command lifecycle

After source review and a new reviewed distribution selection, use one bounded
sequence of fresh public installed `run` requests selecting the shipped owner
script and the same exact new manager:

1. Explicit first start: create the manager/new generation, run a short empty
   managed service, explicitly seal, then orderly close. The surviving supervisor
   must preserve genuine CLOSED, rather than relabel it QUIESCED_UNCLEAN.
2. A separate `status` request must recover the same exact durable state with no
   actor/session/run refund or private manipulation.
3. A separate `retire` request supplies a fresh conservative-clock assertion and
   retires only when the original horizon has elapsed.
4. A separate `reclaim` request admits and executes the fixed-layout bounded
   step on that exact retired disposable generation. Any deletion needs root's
   later explicit selection. Check FREE and preserved manager/session history
   bounds, with no operation-directory or unrelated data deletion.

Inspect exact worker profile/session/run joins, normal boot/import origins,
fixed nested deadlines and preserved original charges across these distinct
requests. Require no development paths, test-only loaders or unselected imports.
This single integration sequence tests the previously unexercised *public
launcher → owner → existing boot → prospectively bound worker → actual composer*,
followed by ordinary installed administration across process boundaries.

Do not repeat mathematical circulation, receipt production, large search or
the crash scenario simply to obtain a passing label. Root reports crash01 earned
live QUIESCED after actual exit23/descendant termination, but its fixture stopped
at an unsupported cumulative-process-count assertion before reopen/retirement.
That failure remains; no unclean-retirement runtime claim follows. The proposed
ordinary clean lifecycle tests a different path: installed dispatch, preserved
genuine CLOSED, and later public retirement/reclamation. An inner session failure
leaves the operation failed and retained; it is not grounds for automatic retry
or relaxed adoption.

This design does not itself select any of those effects. Root can now select the
single owner module and exact 126-entry map once the pending recovery evidence
is adopted, with current consolidated121 and all used sources kept intact.
