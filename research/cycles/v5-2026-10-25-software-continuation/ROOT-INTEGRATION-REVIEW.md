# Independent sparse-access integration source review

2026-10-25, `concept_software_bridge`. **SOURCE GO for the six reviewed root
integration successors; no blocking defect found in this changed boundary.**
This is not an assembly, import, runtime, public workflow or full-v5 acceptance.
The reviewer authored the separate prospective test file and does not approve
that file here; its independent review belongs to `ordinary_routing_gap`.

Canonical guard passed. Compared each complete changed-file diff against the
actual contact-federation assembled package (PROFILE
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`), then read
the affected caller/callee paths, existing accounting/cleanup, provider route
definition and selected sparse contract. No product code, shared ledger, paper,
Git index or runtime state changed during this review.

## Exact reviewed source

All files below are under `software/v5/ordinary_sparse_access`.

| File | SHA-256 |
|---|---|
| search_session.py | a9f49c50d239656327a2a373df184922ed746f546e25761fcdcbacec33299ec8 |
| fair_search.py | 046f55c5498448c5f1d7696f3c81efd80663bbbacc8b363bfe75780d3e6d6d1b |
| fair_exchange.py | 89de88de6ddbc8a2d0aafb96aac150a8f5e7b550303fc9504f970e477ce16b71 |
| peer_api.py | 48ec02f0ecf76f44d7ab64e6e029bdfb4f7ccb3aba8513711dd6b07952c917e9 |
| peer.py | 968d13e4c926b1520cba00502f3e98a87ffda7bdfefa0ec3fcf362c2d3efb655 |
| profile.py | 1f40fb7a663c10d8f09132375ac8ab7899dea5830fff4979e0dda66b668003f8 |

## Resolved obligations

**Held-request protocol selection.** `SearchSession.begin_candidates` adds a
strict local string mode, defaulting to `atomic-v1`, constructs the corresponding
schema and invokes that validator. `accept` dispatches only from the retained
request schema, not the remote reply. Both use operation `candidates`; `_take`,
reservation and failure settlement remain unchanged. Thus the V2 change does
not evade conservative full-scan-allowance charges or enter contiguous Coverage.
Wrong-schema replies are rejected by the selected candidate verifier.

**One immutable mode and route.** FairSearch validates/binds candidate_mode in
its existing owner invariant, passes it into request creation and chooses one
route consistently. Offers stay unchanged. Success reports include the mode;
HTTP 400/404/503 and settled transport failures retain the existing abandonment
and incomplete-result behavior. There is no new V1 retry, capability negotiation
or grant renewal. `fair_exchange` adds only the new read-only route to its
allowlist; size, absolute deadline, TLS and settlement paths remain unchanged.

**Public configuration forwarding.** `find` accepts the one optional field,
validates it before network allocation and supplies it to FairSearch.
`directory_find` validates the optional nested search mode before its directory
work, deep-copies it, and forwards it through `search_config`'s `**search` to
exactly one existing find invocation. Hints do not supply that field. Original
combined prepayment, earliest-contact horizon and same ledger remain intact.

**Optional physical index selection.** `_index_fields` permits only the prior
three fields plus optional `access_pairs`; `_index` passes that exact value to
Store. Serving still requires an existing index and preserves overlap/owner
checks. The repeated CLI publish/serve index-field check is updated too, so it
does not reject the new field before the API sees it. None continues to select
the default physical profile; Store owns strict pair validation and exact reopen.

**Correct rollback scope.** The unchanged publish loop first saves each preview,
then admits its metadata, then records that successful publication. A pair quota
refusal propagates through the existing partial-publication error report; there
is no deletion of custody or reversal of earlier successful targets. This is
per-target metadata rollback, not whole-publication atomicity. Documentation
must retain that distinction; no native/custody experiment was run by this review.

**Pinned helper loading.** The new profile SUPPORT list includes pair_access.
Existing exact payload census, pin verification before import, source path
checks and selected installation verification therefore cover the helper in a
coherent new assembly. The loader intentionally does not open an old package
missing that newly required support file. This does not modify or migrate the
frozen old package or its state. No mathematical installation/semantic payload
was changed by these six files.

The peer_api diff also removes one trailing blank line. This is a harmless fresh
successor byte difference, not an unexplained behavioral change.

## Remaining gates and limits

Pair/Store and candidate/provider correctness have separate authors/reviewers;
this review checks their integration seams, not a substitute complete approval.
Root must bind the final versions in one exact package and read all independent
reviews before selecting a finite run. The prospective test suite targets Store,
query and session boundaries; its own source review is independent of this GO.

A later small public-forwarding smoke should check the new opt-in field/route
composition, including charged legacy-route refusal. Do not repeat the completed
contact directory or native mathematical campaigns solely for this addition.
No source argument here establishes measured demand, end-to-end speedup,
mathematical novelty, complete discovery or globally deployable v5.
