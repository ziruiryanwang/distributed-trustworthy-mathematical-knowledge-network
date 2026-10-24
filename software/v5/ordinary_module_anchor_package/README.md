# Incremental ordinary Lean modules

Development source, not an adopted release package. This change adds local module
anchors to the existing ordinary owner API. Core mathematical admission, search,
discovery and the optional-certificate route are unchanged.

## User workflow

1. Acquire and locally accept mathematics through the existing ordinary workflow.
2. Run `owner.py export-module` with exact targets and the selected owner context.
   With no anchor option, it checks the complete selected closure above Init.
   Successful generation automatically registers its protected five-part module.
3. Save the returned `anchor_id`. To export an extension, add
   `--module-anchor <that exact ID>` to the same command. The current context must
   still warrant every declaration in that anchor, not just the new targets.
4. Use the returned `module_name` and **all** `import_directories` in the ordinary
   Lean project's import configuration. The child is not a standalone artifact:
   its registered parent chain supplies definitions and their computation rules.
5. Requesting targets already in the selected anchor returns that module without
   a native checker call, new registration or new mathematical acceptance.

The existing profile/runtime/catalog/custody/store/limits/parent-root/output and
module-targets options still apply. `--module-anchor` is accepted only for
`export-module`. It does not infer an anchor, modify a project, import an external
manifest or automatically trust a module another participant compiled.

## Why this is sound and useful

Registration records a successful local generation event with private and public
delta checks, both fresh rereads, and exact controller validation. A warm operation
verifies the protected record, support compatibility, current warranted bindings
and artifact hashes. It then checks only unanchored complete proof units. Old
proof inventories are not fetched or decoded. This is local checked-result reuse,
not a succinct proof and not a new axiom-admission rule.

Correctness remains conditional on the pinned Lean kernel/importer/codec and the
existing trusted-owner storage/runtime assumptions. Hashes preserve a recorded
local event; they cannot establish one for a remote binary. An administrator able
to rewrite both trusted code and state is outside this boundary.

## Limits and operational behavior

- The existing 32-unit/4-MiB bound applies to each new delta, not its registered
  ancestors. The first profile still bounds chains to 32 modules, 1024 units,
  16384 names and 256 MiB of selected artifacts.
- Metadata validation, integrity hashing, ordinary imports and resident memory
  still cost resources proportional to the selected artifacts/context. There is
  no constant-time or arbitrary-size library claim.
- Existing trusted-project authoring accepts at most 16 project search paths;
  it has its own support envelope. Returning up to 32 import directories is not
  permission to silently enlarge that separate author's limits.
- The sidecar retains at most 256 operations/1 GiB, counting failures and orphans.
  Capacity exhaustion refuses. There is no automatic eviction, migration or GC.
- Cold consumers still need supported checking evidence. This feature does not
  solve cheap cold onboarding or establish a network-wide growth advantage.

The registry lives inside the catalog's `module-anchors-v1` directory and uses
the existing exclusive owner lock. Copied `MODULE.json` files do not register
anything. An incomplete/unclosed reservation or uncertain worker cleanup refuses
further anchor work. Clean failures retain ineligible output without invalidating
unrelated accepted mathematics. No automatic retry follows a failure.

The final record is published last. Reporting failure after that point does not
revoke it. `COMMIT_UNKNOWN` reports the exact attempted AnchorID for an explicit
later lookup; a saved PASS report cannot reconstruct missing registration.
Missing/corrupt/incompatible artifacts refuse warm use, without silently falling
back to a more expensive cold export. Retain all returned parent directories.

Source selection and the independent review are under
`research/cycles/v5-2026-10-22-native-library/ORDINARY-MODULE-ANCHOR-*`.
No public deployment, license choice or final-v5 completion is asserted here.
