# Genuine service-to-reclamation adapter: source challenge

2026-10-21, core_release. Adapter-only source review requested by root. No
adapter/product edits, imports, runtime, tests, deletion or Git mutation.
The full fresh-product review is separately owned by support_guest.

**No remaining adapter/API blocker found in the revised source.** This is a
source assessment, not execution qualification or authority to launch.

## Exact scope

- Root selection: `BOUNDED-RECLAMATION-SERVICE-SELECTION.md` in this cycle.
- Reviewed adapter: `software/v5/bounded_reclamation/service_smoke.py`, 17929
  bytes, SHA-256 `1284985fedd78f7fb64e29721ab080bff83bec23c4605ddabf3b985f914889e8`.
- Actual target lifecycle/reclaimer: `d59615b664ca8dc934d07778046164313d226965cc3b2486e1e98d15bd57d9ef`
  and `19713fc4baec821a5c77a0071182c63401b292cbe79a7ed7c04b7deba50e1894`.
- Unchanged composer: `404365849dd0e41860ba8ccda01a5b064d028241a2d8b0063d76936fcd306687`.
- Installed SDK: exact consolidated 121-source release `1fd0ae63...`; the
  source map, relevant actual source and workspace basis `6e14ba3b...` were
  inspected read-only, not rebuilt or requalified.

## Concrete blocker identified and fixed by root

The initial adapter rejected every product module with `__file__ is None`
during final origin checks. The installed `discovery` package has no
`__init__.py` in the exact source map and is a namespace package, so an
otherwise successful scenario would have failed its final origin check.
This was sent to root before execution. The revised adapter permits only
installed-SDK namespace paths while checking imported executable modules
against the exact selected file set. It loads the three new modules by exact
specification in dependency order: reclaim, lifecycle, composer. Installed
package paths are no longer mutated. The actual placement/client packages
have installed `__init__.py`; the earlier path insertion was not itself a
namespace-list failure.

Root also changed final cleanup to preserve a prior operation exception and
attach cleanup/deadline notes. The revised adapter initializes that primary
exception state and still refuses PASS for incomplete cleanup.

## Positive-path source correspondence

1. Only an ordinary fresh `managed` child of the exact new output is enrolled.
   The snapshot, source, research and installation roots are protected and
   disjoint. Schema is the new reclaim-enrolled manager schema, not an old-root
   migration. The derived first-generation path is checked before deletion.
2. Two slots have six distinct loopback ports. Owner allocation is exactly
   36 MiB = two 16 MiB slots + 2 MiB registry + 2 MiB cleanup. These remain
   logical allocations, not a physical quota assertion.
3. The fingerprint Workspace configuration uses the actual accepted schema
   and `[[]]` profile; its namespace and wire profile feed the placement and
   locator configuration. Existing store/table names and `status()["objects"]`
   match the selected sources.
4. The empty original horizon lies before the explicitly assumed UTC lower
   bound. The actual controller/ledger `start_service`/`start_run` path does not
   require an unexpired admission horizon; token/request paths do. No token,
   request or cell is created, and the adapter checks those tables are empty.
   This avoids a TTL wait without claiming clock synchronization or expiry of
   a previously funded data promise.
5. Service/locator limits satisfy the checked relationships: health reservation
   is 4 + 2*1 + 1 = 7 commands, within 16; TTL 120000 >= 3*30000; locator
   lifetime 150 seconds covers its selected stop interval. The original
   170-second outer bound and locator 140-second deadline retain cleanup
   margins. Runtime costs remain actual-run observations, not a guaranteed
   timing prediction from this review.
6. `GenerationServices.retire_slot` uses actual current objects, revokes/wakes,
   awaits the genuine service close, then applies exact CLOSED/task/store
   checks before retirement. The service monitor returns on wake before a
   health operation; normal close is not suppressed. Adapter assertions add
   successful Node exit and completed close tasks, rather than inventing
   positive closure or relying on a saved report alone.
7. The real one-run directory grammar fits the fixed 29-role inventory.
   Normal absent journals simply have absent presence bits. The actual
   workspace/locator creation sites match the reclaimer's six workspace DBs,
   empty operations directory, per-run key/adoption/metadata and two channel
   metadata files. No arbitrary saved logs are expected or authorized.
8. Reclamation uses the real begin/step API after genuine retirement. Both
   Python deletion primitives are wrapped to require an ordinary exact target
   at/below this newly enrolled generation, never manager/output roots; recursive
   deletion is forbidden. The original two-call, 64-role window cap suffices
   for the intended one-window 29-role path without renewal.
9. FREE and exact absence precede sequence-3 allocation. The other slot's full
   record/marker must remain equal, and old-ID reservation must explicitly
   refuse. Final exact source rechecks cover installed/additional bytes;
   cleanup requires zero pending tasks after one loop settlement.

## Remaining review boundary

The root's eventual selector/input/outer containment still need their own
exact review before a fixture-only launch. Actual failure/output, Node close,
fixed-layout census and observed deletion events require an outcome audit.
This adapter tests empty genuine actor closure and capacity reuse, not retained
mathematics, useful growth, public networking, independent hosts, physical
envelope adoption or full v5. It must not replace the separate already adopted
retained-content smoke evidence or restart it.
