# Proposed refresh kit: static integration review

2026-10-28, query_scaling. **PASS for the exact static delta below; NOT ADOPTED.**
Canonical guard passed. No product imports, runtime, sockets, tests, owner/database
access or Git. SELECTED-FILES and a packed/relocated result were not yet selected
for this review. Root reports public01 failed and is closed; transport diagnosis
is a separate assignment. This review does not convert that failure into a pass
or authorize packing/adopting PROFILE
`f75dda6e534450cdf5d4db2901c3e1964501514da817bc3eb8aadebc0c350f7b`.
A subsequent transport/profile change requires a fresh exact kit selection.

## Reviewed pins

Paths are relative to `software/v5/ordinary_registration_refresh`.

| File | SHA256 |
| --- | --- |
| kit/kit.py | `a8f321ecb7b798138af1cac91449bce3d9a284b96dd9fb08436afe6e8d8ea7ad` |
| kit/file_helpers.py | `b5d211a83644b61c6a6fe673785ccd1e1960816a2d58f20787b9d4dfdb3c9da9` |
| kit/operator/prepare_selected.py | `229ad3f9608e85e234aed1b07056020984f8a97870c135dc0b0d1d4c4ae2b5ee` |
| kit/operator/compatibility.json | `f86ce690ec7429f6d2508af2fb736132a623c5a955907eaed5fed37b974e37a7` |
| kit/GUIDE.md | `8b081947d09e102c2641d0a3767d6baaa7eee5e1077f298b0e60998004c85ac6` |
| kit/REQUESTS.json | `7a0e248e908b3b6275dfb0a768d830a5bdabed7ea98143337bea75348f02c64a` |
| REFRESH-USAGE.md | `8d48234e964ec14673ed5fb27e7d14f8eb70745d509e3adcd9b46713ab139fde` |
| REFRESH-REQUESTS.json | `db4aaf7d8322cc07bca8696b195b564bf24cbf188b1bfe60a55f743cb2ae04fc` |
| source-map.json | `aeab07b21fb755614ea1432ca9b748d2f8abbfe8c6f43f262de9d2da66cbdb85` |
| build.py | `08580aa9348cc1c84ceb2719fcd7748feba7c8ce51bd5d10eb82924918b1ccc3` |

## Exact implementation boundary

Comparison with adopted `ordinary_directory_kit` confirms that compatibility
changes exactly four direct-source pins: peer.py, peer_api.py, run.py and
support/transport/http_provider.py. Each matches the assembled PROFILE. The
50 direct roles, 72 generated roles and compatibility schema are unchanged.
The selected-preparer wrapper changes only its compatibility hash and identity
label. Its actual preparer remains the existing
`ordinary_reply_capacity/operator/prepare.py`, pin
`203f6249e0659d13b58c79232b8e7a9533d0fc44d843c55a9eba03f244bb0892`;
there is no new refresh-preparer action. file_helpers.py and REQUESTS.json are
byte-identical to the adopted kit.

The kit utility changes only PROFILE, source-map/builder identities and the two
required refresh companion names. Its checking/packing logic and installation
identity remain unchanged. The source map stays at 93 sources / 78 direct copy
roles, substituting exactly the four refresh sources. All shared source pins,
schema, counts, native outputs/runtime selections and other map fields are
unchanged. The direct builder changes only PREFIX and MAP_SHA. No native rebuild
or mathematical schema change is introduced by this kit delta.

## CLI and documentation usability

The templates' provider-feed, registrar and reader field sets agree with the
static directory, final refresh API and directory-find contracts. Their example
values satisfy declared limits once required placeholders are filled. The
documented `run.py ... peer -- OPERATION` form matches the exact public launcher;
state arguments are correctly omitted. Source-build, profile and package paths
in the main guide select the proposed refresh version.

The procedure distinguishes feed origin, registrar and learned mathematical
service, requires the same compiled route and independent scope/egress policy,
and leaves mathematical service startup to the existing workflow. It explains
fresh configs/outputs, service overlap, live READY observation, empty no-listen
outcomes, partial refresh, retained client horizons and final cleanup. The
Std.HashMap name array is an exact structured name rather than an invented symbol
hash. Historical lookup still requires successful output and a selected directory.

Two review findings were corrected by root before this pin: the companion now
uses a relocated `C:\commons` package choice with matching operator files, and
its dangling link to an unbundled REFRESH-CONTRACT was removed. Remaining runtime,
directory, certificate and contact placeholders are explicit choices rather
than presumed local resources. No stale experiment path is required by its CLI.

The static bundle is coherent at these exact identities. The pending source-file
selection, actual pack/extraction and unresolved public-workflow outcome remain
separate gates; no release or independent-host evidence follows from this review.
