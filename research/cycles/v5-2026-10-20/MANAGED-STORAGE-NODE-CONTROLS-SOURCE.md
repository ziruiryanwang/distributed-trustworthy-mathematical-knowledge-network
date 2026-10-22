# Managed storage: minimal actual Node controls (source only)

Status: **AUTHORED, NOT EXECUTED**. Root selected this test-source work after
independent integrated storage review. No parser, import, Node launch, SQLite
open, test, build or Git mutation was performed while authoring it. Root reviews
and selects any actual finite run; a source note is not a passing result.

## Selected artifact and purpose

`software/v5/managed_storage/node_controls.mjs`

- Bytes: 16756.
- SHA-256: `8996b2e03a34e5085ea620a140a79e12847abcaa899083f94d02a883cf440491`.

The consequential question is whether the exact fresh-only intent-store
successor establishes the supported SQLite profile and retains the adopted
store's ordinary transactions/counters, while refusing old/foreign state before
writable database creation. This needs one small actual SQLite control, not a
network service or another mathematical proof campaign. The independent source
review already covers the broader integration; do not repeat it here.

## Exact source and runtime boundary

The one command shape is:

```text
<observed-01 installation>/base/runtime/node/node.exe
  <fresh output>/sources/software/v5/managed_storage/node_controls.mjs
  --output <fresh output>
```

Working directory must be the canonical project root. `<fresh output>` must be
an ordinary canonical directory strictly below `experiments/v5-local-checks`.
No Node flags, `NODE_OPTIONS` or `NODE_PATH` are accepted. The root-owned outer
runner is responsible for environment clearing, process containment and the
prospective allocation, including **10 CPU seconds, 45 wall seconds, 128 MiB,
one process**, bounded logs and at most 1 MiB of retained fixture file streams.
These are proposed/root-assigned limits, not observations or internally enforced
Job limits. No automatic retry or larger allocation follows failure.

The child reads the root's immutable `selection.json`, requiring schema
`DMKN_V5_LOCAL_CHECK_V1` and SHA-256 string entries in `sources`. It requires:

| Snapshot path below `sources/` | Exact pin |
|---|---|
| `software/v5/managed_storage/node_controls.mjs` | This control's selected SHA-256 |
| `software/v5/managed_storage/portable/location/intent.mjs` | `6c30e8793f737f0512e3e7e9d785d1311cafa35116784f4f8b3dda5c1a75fa29` |
| `software/v5/managed_storage/portable/location/maintained_roles.mjs` | `d69d0b123e52f5cfbf4c2eef2e2d2dfecf9b9b11c9ddfabc4c5e37499e1a12e0` |
| `software/v5/managed_storage/portable/location/protocol.mjs` | `88c2bc34e5ebefc412b564bef06e0d4210e0c44e3102be1d6adacfc6334af986` |

The last row is an **exact adjacent test-only fixture**, copied mechanically
from selected `software/v5/body_location/portable/location/protocol.mjs`
(13533 bytes). Root explicitly requested and authorized its creation as
`software/v5/managed_storage/portable/location/protocol.mjs`; `apply_patch`
created it and a byte-length/SHA-256 comparison confirmed the exact original
13533 bytes and pin above. It satisfies the real intent module's relative import
without rewriting that module or using a mock protocol. Root must select this
alias in the fresh test snapshot. It is **explicitly excluded from the SDK
overlay/product map**; the installed protocol continues to resolve to its
original selected source. No new protocol or preserved-source edit occurred.

The fixed installed runtime is:

`product-local/v5-distribution-managed-observed-01/Mathematical Commons v5/base`

Its exact release manifest is
`a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed`.
The Node executable is 92279112 bytes,
`b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3`.
The actual installed `overlay/quota_store.mjs` is 9487 bytes,
`7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4`.

The test imports the actual `intentStoreClass`, installed `QuotaDatastore` and
installed `interface-datastore` Key. It neither instantiates nor imports the
maintained service; that source is read solely for the static ordering check.
The protocol is real. The unused provider-key function throws if called.

Manifest-authenticated resolution and load hooks check each imported code
file's ordinary path, exact bytes and SHA-256, including the bytes returned by
Node's module loader. Present enclosing package metadata is authenticated as
well, because it controls package scope and exports. Data/network imports and
unselected paths/builtins refuse. Selected source bytes, manifest, Node binary,
imported code and present package metadata are rechecked afterward. This is
an **actual imported-source closure binding**, not a new full 5896-file runtime
tree census or an adversarial local filesystem sandbox. The adopted runtime
and trusted-owner/exclusive-writer premises remain; root may retain its ordinary
outer runtime authentication. Streaming executable hashing uses at most a
1 MiB buffer rather than loading the executable into memory.

Static dependency inspection retained the strict `format === 'module'` load
rule. The actual datastore-core index reexports its wrappers; the logger branch
is `@libp2p/logger -> weald -> ms` and `supports-color`, not CJS `debug`.
Selected `ms` is 4.0.0-nightly.202508271359 with `type: module` and ESM
import/default export; selected `supports-color` is 10.2.2 with `type: module`
and Node `index.js`. Its `node:tty`, `node:os` and `node:process` imports are in
the finite builtin allowlist. The selected iterator branches (`it-drain`,
`it-filter`, `it-sort`, `it-take`, `it-map`, `it-merge`, `it-pipe`, `it-peekable`,
`it-all`, `it-queueless-pushable`, `it-pushable`, `p-defer`, `race-signal`),
`uint8arrays`, `multiformats` and `abort-error` also have module type. The
actual Node-conditioned uint8arrays helpers import `node:buffer`, already
admitted. This was bounded read-only package/source inspection, not a runtime
sweep or an executed import. An unexpected module format still fails closed;
no speculative CJS bypass was added.

## Seven fixed groups

1. **Static identity buffer order.** Read the exact maintained source and require
   both nonempty Uint8Array/1024-byte conditions before either identity/adoption
   `writeFile`. This is expressly static evidence, not private-key execution,
   serialization compatibility or a service-start control.
2. **Actual fresh profile and inherited operations.** Create one fresh fixture,
   open the actual intent subclass and read back 4096-byte pages, no auto-vacuum,
   DELETE journal, FULL synchronous, MEMORY temp store, 256-page cap and positive
   cache spill. Check empty counters; put/get/has; same-key replacement with exact
   byte accounting; rejection/rollback of a 1025-byte value under the 1024-byte
   limit; delete; zero counters; close; and unchanged identity/adoption fixtures.
3. **Existing same-profile database refuses.** Attempt a fresh store open against
   the just-closed actual database. Require refusal, null handle and exact
   before/after file-name/size/hash inventory. The original database stays put.
4. **Journal refuses before database creation.** Fresh fixture with a synthetic
   `metadata.sqlite-journal`; require unchanged files and no new main database.
5. **WAL refuses before database creation.** Same with `metadata.sqlite-wal`.
6. **SHM refuses before database creation.** Same with `metadata.sqlite-shm`.
7. **Unknown file refuses before database creation.** Same with `unexpected.bin`.

Each state has a short explicitly labeled **synthetic, invalid-as-private-key**
`identity.key` and synthetic adoption marker. The actual Store checks file
shape, not cryptographic identity: no private-key parser, identity generator,
credential file or existing owner state is touched. The owner argument is a
deterministically encoded public-shaped identifier made from constant bytes,
not a generated key pair. These fixtures are not service-adopted state.

For all five refusals, the current guard encounters the unexpected directory
entry before its later explicit suffix-absence loop, so the expected error is
`LOCATION_METADATA_STATE_ENTRIES`, not a fabricated hot-journal recovery error.
This demonstrates pre-open refusal and preservation; it does not test recovery
of an actual hot journal, continuing Python stores or crash consistency.

## Output, closure and limits

The script creates only a fresh `node-fixtures` subtree and the exclusive
`node-controls-result.json` under its selected output. It never unlinks,
renames, deletes, overwrites or reopens a fixture for writable recovery. The
normal result includes all seven groups, profile, bounded final inventory,
exact imported files, package metadata, CPU/wall observations and explicit
nonclaims. Final retained fixture inventory is limited to 64 entries, depth 2
and 1 MiB. The tiny fixed data makes the expected actual usage much lower; the
test does not fill a 256-page database or simulate the envelope worst case.

Every constructed store is tracked and closed in `finally`, including refusal
and assertion paths. Close/binding errors keep the result FAIL. Result output
is at most 65536 bytes and uses `wx`; console output mirrors it. Failures during
the preflight remain failures in the outer raw log even if no structured result
can yet be written. Outer timeout/Job enforcement and direct process reap remain
root-owned, not guarantees supplied by this script. All failure files remain.

Success would qualify only this exact Node storage sub-boundary. It would not
adopt a whole-root disk bound, production custody, managed lifecycle integration,
new mathematical acceptance, networking, hostile-source isolation or final v5.
