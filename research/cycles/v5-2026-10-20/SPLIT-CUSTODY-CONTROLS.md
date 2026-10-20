# Split-custody controls and one retained-data integration

2026-10-20, `core_growth`. Canonical guard passed. Source authoring only:
no imports, tests, native programs, proofs, installation or Git mutation by
this author. Root owns exact selection and all execution. Used predecessors
remain unchanged.

## Focused control candidate

`software/v5/client/supplier_selected/test_suppliers.py`, SHA-256
`d997519b37eadf3fa637b16ce982744e5ece267c87240c7946f7b2330e511606`.

Eight explicitly selected groups; inherited predecessor suites do not run:

1. Explicit Q name/body retrieval preserves P's original candidate, one grant,
   one deadline and one shared acquisition budget. The new `check_supplier`
   performs no I/O or acquisition reservation.
2. Omitting supplier retains candidate-origin P behavior.
3. Unknown/expired explicit supplier refuses without I/O. Expiry uses the
   actual contact guard with a clock just after a one-second contact lifetime
   but before the original operation deadline; no wait or synthetic new grant.
4. P and Q exhaust the same original request ceiling, not per-provider budgets.
5. Q cannot replace the descriptor-committed body with different bytes.
6. A cached P mathematical address does not hide a new explicit Q candidate;
   content/group deduplication and one final admission remain.
7. Q supplies a body using P's held descriptor without a redundant Q name
   request; retained identical bodies deduplicate by mathematical address.
8. Cached names/bodies cannot bypass explicit contact checking. Supplier
   variants consume the original name cap and conflicting Q metadata refuses.

The five facade controls use actual selected facade/decorators, contacts,
budget and SQLite custody with inert mathematical issuers and mocked HTTP
exchange. The three helper controls use an explicitly inert facade. Native
processes and real connections are forbidden by the runner. This is not live
mathematical admission or network evidence.

Imports reuse frozen fixture constructors from `test_direct_contacts.py` and
`test_semantic_reader.py`, not their test suites. Root's selected source closure
must include the former explicitly in addition to the prior helper-control
closure. The two new implementation files are loaded into their actual logical
client module names before fixture imports.

## Single actual split-custody candidate

`software/v5/client/supplier_selected/split_check.py`, SHA-256
`386d6db222d9ad9a2f4a3bd2d2d5612bc0f76d4d58e3597348659ed760100274`.
Schema: `DMKN_V5_SPLIT_CUSTODY_CHECK_V1`.

Reuse the exact retained `6998ba92...` packet, original runtime adoption,
formal query, target and worker budgets of the passed semantic integration.
The new source chooses only this already observed demand's supplier:

- Module `2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.
- Name `CommonsV5.fold`, universe arity 2.
- Body `0b5f265dfb01a1ed1232443bfdc79c5217be78664b15ee9d12e01fa77d2e6e55`.
- Explicit already-bound contact label `semantic-supplier`.

P's fresh semantic store is seeded with all 13 authentic groups and only
10 of 11 available bodies; the selected body is omitted **before insertion**.
P alone indexes the target and offers the unchanged packet. Q gets only the
selected authentic group and exact body, with no indexed exports or packet.
Before serving and after clean service closure, actual point lookup/readback
and store counts must establish this split. No original workspace is opened,
no database row is deleted, and no packet is rewritten.

The important scope is **P's public semantic store/body service lacks the
selected row**. The unchanged mixed packet can contain information from which
that body could be reconstructed. This experiment does not establish physical
erasure, information-theoretic absence or detached aggregate-A semantics.

Unknown-ID discovery still uses P. Actual returned preview demands drive the
walk; only the exact selected name/body requests choose Q. The helper does not
extract semantic witnesses from the packet. Prediction: 23 actual HTTP
requests total (Q gets one name/group request and one body request); original
acquisition accounting charges 25 requests including search prepayment.
Selected closure stays 2 modules / 9 groups / 12 declarations / 9 bodies.
One unchanged I/native packet admission checks all three inventory members;
there is no A attempt, new proof, authoring or publication.

## Exact selection and stopping rule

Root can reuse the passing semantic source map, replacing the two supplier
overlays, retaining frozen `semantic_check.py` under `v5/client/semantic_check.py`
for its pure utilities/discovery, and selecting the new adapter as
`owner/split_check.py`. Expected map size: 106 sources. Parameters stay the
same except the new schema and a provider cap of at least two.

Keep the original 90 controller CPU / 120 grant wall, 32 acquisition requests,
30 reserved worker CPU, 1 verification submission, 128 helper steps, 256 facade
calls, 32 MiB submitted/16 MiB reply limits. Keep outer 105 CPU seconds /
150 wall / 512 MiB. Both unchanged 75-second service lifetimes run concurrently,
not sequentially. Actual allowance remains root's decision after source review;
no automatic retry, larger grant or installation rebuild is authorized here.

Stop this increment after these changed-boundary controls and the one actual
split-service result, with independent outcome review. Failure should identify
the changed source boundary before any new selection. Do not repeat passed
predecessor campaigns, start proof/RAM work or claim net growth/final v5 from
this boundary alone.
