# Source-map and builder review

2026-10-28, query_scaling. **PASS for the selected two-role map/builder change.**
This independently reviews root's map and builder, not the two helper bodies
authored by this reviewer. `growth_design_audit` owns their independent source
review. This is file/data inspection only: no product import, builder execution,
owner/database open, native operation, network operation or Git change.

## Exact reviewed inputs

| File below `software/v5/` | SHA-256 |
|---|---|
| `ordinary_incremental_host/source-map.json` | `f5ea607c6774872113f404e2afcaf188b12a43e8839ac4ff5017b4edb02d8ab6` |
| `ordinary_incremental_host/build.py` | `d64ef13504564c86a527563aa66034ab19634311ea7f36e50ce45e175afd8426` |
| `ordinary_owned_acquisition/source-map.json` | `797ea254070ea489643fefcba2c4f092bdd4442d0f2eb670694fadb8e5dffa10` |
| `ordinary_owned_acquisition/build.py` | `6b7df0ef3fd60ffe47b4aadddbfc208dffd7f796b2d3013214f779cf0958a18e` |

## Map result

Parsed both maps as data and compared all their logical fields. Both retain
93 source inputs and 78 direct-copy roles. Exactly two role values change:

| Copy role | Prior source | Selected source |
|---|---|---|
| `support/transport/ordinary_acquisition.py` | `ordinary_multi_source/ordinary_acquisition.py` | `ordinary_owned_acquisition/ordinary_acquisition.py` |
| `support/transport/fair_exchange.py` | `ordinary_connect_ownership/fair_exchange.py` | `ordinary_owned_acquisition/fair_exchange.py` |

The source table removes those two predecessor paths and adds those two successor
paths. Every one of the 91 shared source records is unchanged. All 76 other
copy-role values are unchanged. All other map fields are unchanged: schema,
profile selection, counts, receiver/authoring/extractor/query lanes and their
transforms, tools, authoring suffixes, runtime pins, native output roles and
documentation. The successor JSON is reformatted/reordered; this conclusion is
logical-map equality outside the two substitutions, not unchanged JSON bytes.

Independently read the length and SHA-256 of all 93 selected source files:
zero mismatches against the new map; total selected source bytes 3,062,834.
The new acquisition record pins 30,636 bytes with hash
`677b6a6acd17de5ad60dbdd5700aac3014fc7a571876757b39382f8642f6d37e`.
The new exchange record pins 8,397 bytes with hash
`a04c4577a4fd6b3f68a48a869397d5ee35ec5075f7e5c1c496f5bb31fb06fc9a`.

The unchanged census remains 19 installed direct roles, 50 auxiliary direct
roles, 9 documents, 8 generated receiver roles, 65 authoring roles, 5 query
roles, 2 extractor outputs, 1 installation manifest, 159 payloads excluding
PROFILE and 122 auxiliary payloads. The two substitutions are outside the
installed mathematical support and native lanes. Owner/profile/module-anchor
source selections are unchanged.

## Builder result and boundary

The builder diff changes exactly two assignments: `PREFIX` points to this fresh
folder and `MAP_SHA` pins the actual new source-map hash. Applying those two
literal replacements to the predecessor text and encoding UTF-8 produces exactly
38,900 bytes and the successor builder SHA-256 above. Thus no hidden builder
logic, runtime pin, source count, compiler lane, allowance, child supervision,
copying, validation or failure-cleanup change accompanies this cut.

Its existing complete-source build capability is not a new execution selection.
Root's separate assembly must still establish the actual unchanged installation
and anchor-support closure and produce a fresh profile. This review does not
claim that an output package exists, adopt the two helper implementations, modify
the frozen standalone host or authorize any native rebuild/public workflow.
No map/builder finding blocks the next separately selected assembly step.
