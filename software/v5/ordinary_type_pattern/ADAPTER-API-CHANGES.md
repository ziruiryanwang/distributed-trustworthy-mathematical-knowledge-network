# Optional pattern adapter and peer API source checkpoint

2026-10-28. Source implementation only under INTEGRATION-SELECTION. Only the
fresh `ordinary_export_adapter.py`, `peer_api.py`, and this checkpoint were
authored by query_scaling. The used pure pattern helper and all baseline/package
sources remain unchanged. No Python import, compilation, execution, test, owner
access, native operation or Git command was performed for this assignment.

## Exact API agreed with root and host owner

The packaged helper import is `ordinary_type_pattern`. The fresh adapter exports:

```python
namespace_for(semantic_id, *, discovery_profile="exact-v2")
validate_spec(spec, *, discovery_profile="exact-v2")
feature_id(namespace, spec, *, discovery_profile="exact-v2")
compile_query(namespace, specs, *, discovery_profile="exact-v2")

OrdinaryExportAdapter(semantic_id, *, limits=None,
                     discovery_profile="exact-v2", inventory=None)
adapter.compile_query(specs)
```

The only modes are `exact-v2` and `type-pattern-v1`. Instance properties include
`semantic_id`, `namespace`, `limits`, and `discovery_profile`. Pattern instances
require raw fixed inventory bytes, prepared once by `prepare_inventory` in the
constructor. Exact instances reject a non-None inventory rather than ignore it.
The public namespace/spec helpers require no inventory or adapter construction.
Pattern feature/query helpers require the approved pattern namespace; exact
default helpers retain their old behavior and refuse the pattern spec tag.

Peer integration exports the agreed signatures:

```python
_adapter(loaded, config)
_index(loaded, owner, custody, index_config, check, adapter=None)
```

`_adapter` validates the explicit optional top-level `discovery_profile`; missing
means exact. Only pattern mode reads `loaded.installation.path("inventory")`,
through the ordinary-path checker and a 1 MiB bounded read. The adapter then
checks `ordinary_semantics.INVENTORY` before parsing. No config supplies an
inventory path, hash or prepared table. `_index` retains exact behavior when no
adapter is supplied; a supplied value must have the exact OrdinaryExportAdapter
class and selected installation semantic ID. Every pattern-aware caller supplies
its already selected adapter. The unchanged Store binds its namespace in config.

## Adapter behavior

The exact descriptor retains every old namespace field/value. Default extraction
has the old spec set, record schema, feature hashes, record fields, work count
and describe/resolve result shape. Pattern mode changes the feature revision,
binds the pure helper's PROFILE_ID and the unchanged 128-feature ceiling, and
adds exactly one required `declared-type-pattern` spec. Existing kind, symbol,
head and exact-type specs remain, rehashed under the pattern namespace.

The existing exact adapter class and V3 record schema are retained, preserving
the acquisition exact-class gate. Generic V3 locator validation first accepts the
old exact namespace through its old path; otherwise it recognizes only the
selected pattern namespace. It never accepts an arbitrary namespace or derives
semantic validity from generic feature hashes. Selected adapter resolution and
preview/receive validation still demand their exact selected namespace and full
preview-record rederivation.

When all old features already occupy 128 slots, pattern extraction refuses with
`ORDINARY_PATTERN_FEATURE_PROFILE_EXHAUSTED` before computing/adding the extra
feature. It drops nothing and does not fall back. An unexpected feature-hash
collision also refuses. At 127 old features the added feature can fit, subject
to all existing syntax/preview/byte checks and pattern validation. Generic caps
and Store transactions are unchanged. Pattern describe results additionally
report `pattern_profile`, `pattern_work`, and `pattern_counters`; `work` adds
the pure helper's structural work. These are not whole-process CPU measurements.

## Propagation inspected in source

| Operation | Selection and propagation |
| --- | --- |
| `find` | Optional mode validated before dialing; instance compiles all conjuncts; session namespace is selected namespace |
| `directory_find` | Instance compiles query and route subsets; request namespace matches; generated nested find config explicitly carries the same mode |
| `directory_serve` | All registration specs compile under one selected instance; ContactMap and service namespace match |
| `preview` | Selected namespace checked on record before budget/acquisition; unchanged typed acquisition receives same selected class instance |
| `receive` | Selected namespace checked before operation/network acquisition; unchanged evidence/preflight/admission path uses the same instance |
| `publish` | Factory runs before selected-context reading; `_index(..., adapter=adapter)` selects required extraction; existing per-target commits and partial-failure reporting remain |
| `serve` | Factory runs before Store/provider creation; `_index(..., adapter=adapter)` refuses incompatible stored namespace/config |
| Dedicated host | next_value's fresh custodian explicitly calls the factory and passes the adapter to prepare/serve indexes; selected semantic/namespace must match the existing pinned seal; service config forwards the mode |

The seven peer configuration gates above accept only their existing fields plus
this optional selector; nested index/search schemas do not accept an independent
conflicting selector. Reports add the selected `discovery_profile`; existing
namespace-bearing reports retain their namespace, and receive/publish/serve now
record it explicitly too. A peer record or store never chooses the mode.

`inspect` and `authoring_offers` retain their exact source bodies and constructor
calls: they operate on exact portable identities, not discovery feature records.
Other peer helpers, network allowance/cleanup, custody and acceptance code were
not changed. Source-text function comparison found exactly two added helpers and
the eight changed functions listed above (including `_index`). There was no
runtime verification in this assignment; independent seam controls remain a
separate owner/selection.

## Source pins for review

- `ordinary_export_adapter.py`:
  `2dc27c4f1e6ce37f3bb51467dd9ba8b8e7b23abd16bdabfd0bf9d50f9cdfcb3c`
- `peer_api.py`:
  `d04a5ee9659a026adf18802df634f94c88d4b745f2a5108ed823198804a5e606`

Baselines are exactly the current mapped
`ordinary_formal_query/discovery/ordinary_export_adapter.py` and
`ordinary_multi_source/peer_api.py`. Root owns package/loader/query/operator
selection and final pins. No Store, generic formal_features, transport, native,
owner, query-directory or used-source file was edited here.
