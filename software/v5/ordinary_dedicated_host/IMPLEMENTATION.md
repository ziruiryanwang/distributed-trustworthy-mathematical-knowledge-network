# Dedicated helper implementation

2026-10-28. `custodian.py` is source-only, awaiting independent review. No runtime,
test, owner data, native process or Git operation was used to author it.

The API follows CONTRACT.md: explicit host root and pinned profile; prepare takes
embedded targets and an inert file bundle, serve takes the exact HOST.json pin.
Both require the root controller's `finalize()` to recheck captured config/profile.
Failures after host creation carry `HostFailure.report`, including phase, cleanup
errors, closure states and descriptor publication state. Pre-creation validation
can raise the original refusal directly. Caller owns all external outputs.

Preparation reuses the selected baseline manifest/batch parser and global census
limits, OrdinaryStore puts/getters, portable preview generation/resolution and
existing `_index`/`Store.admit`. It reads back every inserted unit, selected preview,
target locator and admitted index record, then the final index snapshot. It closes
both stores before rechecking manifest/config/profile and publishing HOST.json.
The unit bytes captured from the manifest are read back from custody; no claim
that source files remain an available replica is introduced.

The permanent marker precedes store creation. One retained nonblocking Windows
byte-range lock covers preparation/sealing or the entire serve/cleanup lifecycle.
Fresh-root ancestor checks refuse recognized existing state roots. Serving reuses
the exact sealed store limits, verifies counts/latest snapshot under the same lock,
closes its preflight index and invokes the unchanged owner-free finite SDK serve.
The public serve helper is synchronous: its internal `asyncio.run` stays inside
the lock scope, so runner cancellation/drain of leftover provider tasks completes
before releasing exclusion, including SDK cleanup failures. The outer Job bounds
any hung shutdown. The SDK owns live provider/index cleanup; the helper attempts custody
closure and rechecks config/profile before releasing the lock. No refresh path,
mathematical owner, source/native loading or background service is introduced.

The package's current public guards must reject host descendants for ordinary
state/output and launcher diagnostics, as required by CONTRACT.md. A marker and
OS lock do not sandbox old binaries, arbitrary SDK callers or hostile same-user
code. Logical hosted content is fixed; existing SQLite opens/configuration and
journal recovery retain their original filesystem effects.
