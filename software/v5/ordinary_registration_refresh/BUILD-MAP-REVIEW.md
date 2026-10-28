# Build-map review: exact four-role source successor

2026-10-28. operable_scale_decision. **SOURCE PASS** for the exact map/recipe
identified below. This is independent review of root's build-map selection, not
review of my peer API implementation; growth_design_audit owns that review.
Canonical guard passed. No product import, runtime, build, owner/native/network
operation or Git action occurred. Only this review checkpoint was written.

## Pinned inputs

| Input | SHA-256 |
| --- | --- |
| New source-map.json | `aeab07b21fb755614ea1432ca9b748d2f8abbfe8c6f43f262de9d2da66cbdb85` |
| New build.py | `08580aa9348cc1c84ceb2719fcd7748feba7c8ce51bd5d10eb82924918b1ccc3` |
| Adopted ordinary_name_directory/source-map.json | `46709b30199384ad1e14f0d54529fe185d429d83c341dfebb117869bbe22ead3` |
| Adopted ordinary_name_directory/build.py | `9bf43595182d969fe26b20012d9c569d6ffabde90543951cd0fd330e3025f8f3` |

## Exact selection delta

The new map has **93 source inputs and 78 direct copies**. Its logical copy-key
set is identical to the adopted map. Exactly these four copy values change:

| Logical role | Old source directory | New source directory |
| --- | --- | --- |
| peer.py | ordinary_sparse_access | ordinary_registration_refresh |
| peer_api.py | ordinary_multi_source | ordinary_registration_refresh |
| support/transport/http_provider.py | ordinary_reply_capacity | ordinary_registration_refresh |
| run.py | ordinary_name_directory | ordinary_registration_refresh |

Exactly four old source paths are removed and their four fresh paths added.
Every one of the **89 common source pins is unchanged**. All **93 selected file
lengths and SHA-256 values match the actual current source files**; no mismatch.
The four fresh selections are:

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| peer.py | 17,182 | `c70c8ad123b564ce2927eeb48d6e802695a8ab16c437dc74925362a94dd2fe6d` |
| run.py | 20,123 | `13394976a25f9dc492a6ecfb19cc96748e3cf43a8d11df54417a71edfc0a6dff` |
| peer_api.py | 83,002 | `12c29d1edb3f3bc0483d9fe01abb3a4c69dbc4cdc5225ead32c28842bb4699dc` |
| http_provider.py | 33,406 | `3ce581f4057b6694c6d99a697847984fe7431a695989018f3e179217712859a2` |

Structured comparisons find every other top-level map field unchanged: schema,
counts, authoring_suffixes, documentation, all receiver/authoring/extractor/query
lanes and their transforms/digests, native_outputs, native_runtime_pins, profile
descriptor and tools. All 19 installation direct-copy roles/pins are unchanged.
There is no hidden native, semantic, installation or owner-state migration in
this selection. Unchanged compiler inputs do not themselves establish identical
future binary output; no fresh build or reproducibility claim is made.

## Recipe and loader compatibility

The complete new build.py text equals the adopted recipe after exactly two
literal substitutions: PREFIX names `ordinary_registration_refresh/`, and
MAP_SHA pins the new map above. No other recipe line changed. Its counts and
exact-source-closure checks therefore retain the adopted direct build behavior;
it does not run historical overlay assemblies or introduce another build lane.

The map still selects `ordinary_name_directory/profile.py` unchanged. Its
required set already contains peer.py, peer_api.py and run.py, and its SUPPORT
set already contains transport/http_provider.py, contact_directory.py and
fair_exchange.py. It authenticates these existing roles before importing, then
executes the exact verified peer_api.py and exposes it as loaded.peer_api.
The fresh source imports require no additional product module or package role.
Consequently this four-role replacement needs no loader edit or payload census
increase: the selected package remains 159 payloads plus PROFILE.json.

This pass qualifies source selection and direct-recipe consistency only. Runtime
control outcomes, API/provider correctness, assembled package identities and
actual public behavior remain their separate selected reviews. Any later byte
change to the four sources requires a fresh map pin and corresponding review.
