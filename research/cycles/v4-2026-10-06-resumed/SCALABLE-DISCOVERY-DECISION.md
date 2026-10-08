# Next search seam: partitioned conclusion buckets and local candidate matching

2026-10-06. Source/theory decision only; no implementation/runtime selected.
This reuses the v3 crowding analysis and does not repeat its experiments.

## Current service and actual gap

The compact package's `codec/fragment_index.py:244-253` derives fragment,
interface, exact full-type and constant-name keys. Its bounded SQLite find reads
postings/offer metadata, not proof bodies; rows are ordered by insertion sequence.
`overlay02.mjs:323-337` automatically publishes only fragment/type/interface
keys; constant keys require explicit owner publication. Remote find currently
requests one local page, at most8rows, and exposes no cursor-continuation request.
Thus even the local index's existing continuation is not presently usable through
the maintained overlay. A query can efficiently miss a useful result forever.

Knowing a formal goal usually does not reveal a useful lemma's full type: the
lemma may quantify extra functions and require premises. Exact-type retrieval
therefore does not supply applicable-lemma search. Constant keys help only when
explicitly advertised and sufficiently selective. Eq/recursor keys can be huge.
DHT provider caps then hide whole local catalogs; local first-row caps hide
classes within a selected catalog. Better XOR routing fixes neither problem.

Reuse the exact v3 result:32 renamed reflexivity types followed by injectivity;
16 returned candidates all have one non-target type. Shape1 also collided because
it discarded variable co-reference/premises. The reviewed **materialized
type-diverse stream** is still the smallest duplicate repair. It does not solve
17 distinct competing types, bad first representatives or provider saturation.
See `../v3-2026-09-29/SEARCH-CAPABILITY-CROWDING-DECISION.md`, its independent
review, and `V3-FINAL-CORE-GAPS.md` for the already established counterexamples.

## Concrete proposed minimum

Use a fresh **optional candidate-search sidecar/version**, not a change to proof
identity, FoundationID, the guest, existing exact lookup or frozen owner state.
An admitted sidecar row means syntactically indexed unverified candidate data.
Let ns0 be the existing fragment namespace and ns1 a new search-version domain
bound to ns0. Keep existing ns0 type keys/offers unchanged; use ns1 for the new
signature and route hashes below. This avoids relabeling old mathematical data.

**Query key.** Strip at most64 outer forall binders and inspect a terminal
constant-headed application of at most8arguments. Define

`k = H("DMKN-CONCLUSION-BUCKET-1", policy_namespace, head_name_hash, arity)`.

The requester can derive k from its formal goal without a lemma ID, name, full
type or scorer answer (`policy_namespace` here is ns1). Do **not** require raw
argument constructor tags to agree:
a universally bound variable can instantiate to a concrete application. This
would reproduce a subtle false-negative version of the old shape mechanism.
First version emits exactly this one broad signature; unsupported head/telescope
shapes receive an explicit search-ineligible reason, never mathematical rejection.

**Local discrimination.** Materialize one immutable representative per
`(k, current_exact_type_key)` with an indexed representative sequence. Exact type
key retains namespace/foundation, ordered universe parameters, full structural
type and required definition identities. Preserve all raw offers and bounded
alternate-member enumeration. No query-time DISTINCT or duplicate walk.
Materialize a bounded canonical type descriptor during offer, charged to storage.
Within a selected representative-page budget, a simple one-way conclusion matcher
assigns telescope variables to requester syntax, requiring repeated occurrences
to agree. A constant matches only its exact adopted identity. Applied metavariable
heads, conversion, higher-order/universe solving and oversized descriptors can
return `UNRESOLVED`, not false `NO_MATCH`. Successful structural matching returns
the substitution and unfilled telescope/premise obligations, not a proof.

This distinguishes `Eq t t` from `Eq x y` for rigid unequal x,y in the old fixture;
it does not prove the latter's premises. The agent still chooses/fills obligations
and the unchanged final checker grants acceptance. Formal query goals are local
agent inputs, not mandatory system goals or human-intention criteria.

**Placement.** Use fixed supported partition levels `b in {0,8,16,24}` and
`s = prefix_b(H("DMKN-TYPE-SHARD-1", current_exact_type_key))`. A holder of a
candidate advertises itself under

`route_key = H("DMKN-CANDIDATE-ROUTE-1", ns1, k, b, s)`.

Publish at the four selected levels; deduplicate equal local route keys. The
type class, not exported name or proof bytes, chooses the shard, so renaming
one theorem cannot manufacture many search partitions. Each holder keeps local
representative indexes on `(k,b,s,sequence)`. Queries choose a level and bounded
shards, request provider hints, then use explicit fixed-cut local pagination
and candidate matching. Exact key derivation is rechecked on selected acquisition.
No global shard directory or mutable split consensus is required in this slice.

The four-level scheme is an explicit finite service envelope, not infinite
scalability. Rare classes can use coarse buckets; hot classes can use finer
ones. Observed overload/empty responses inform local query strategy. There is
no claim that the node can infer the optimal level or guarantee a rare answer.
Publication/renewal overhead is at most four unique route keys per represented
signature/class before local deduplication; the existing owner advertisement
quota and renewal economics must be charged, not silently increased.

## A real conditional service guarantee

Fix a query signature k, level b and stable query interval; let S=2^b.
Call a shard **good** only if (i) it contains a relevant retained candidate,
(ii) the maintained routing/replica/TTL contract reaches a holder within the
query's provider budget without cap loss, (iii) the holder's fixed-cut bounded
representative pages expose that candidate, and (iv) its finite structural match
and later independently checked use succeed. These are distinct obligations.

If h shards are good and the requester samples m distinct shards uniformly,
the probability of missing all good shards is

`choose(S-h,m) / choose(S,m) <= exp(-m*h/S)`.

This is sampling without replacement, not an assumption that provider choices
are uniform. The guarantee requires an owner-available randomness source and
explicit source/coverage/cap premises; it is not proved merely by hashing keys.
Under the maintained routing premises, charged requester work is bounded by
`m * (routing_work + provider_cap * local_page_match_budget)` plus actual selected
interface/proof intake. No all-peer or all-corpus scan is required. If a known
nonempty operating regime has `h/S >= rho`, m>=ln(1/delta)/rho suffices for
failure probability<=delta, within supported finite caps.

This says something nontrivial but deliberately not universal: aliases do not
consume distinct local classes/shards, and a healthy sufficiently dense relevant
bucket admits corpus-independent bounded sampling. If only one of a million
otherwise indistinguishable classes is useful, rho may be tiny. No bounded
feature scheme promises cheap guaranteed recovery without more information.
Neither extra provider capacity nor an LLM ranking score eliminates that limit.
Refinable signatures or richer matching should be justified by an observed
rho/selectivity failure, not presumed solved by this first scheme.

## Implementation consequence and next gate

The useful delta is one optional search version: signature/type-class descriptor
derivation; transactional representative/alternate indexes; the versioned route
key; bounded query descriptor and local matcher; remote fixed-cut page/cursor
plumbing; explicit auto-publication/renewal selection. It cannot be shipped as
only a new hash prefix: current strict key regex, offer/query validation, remote
request and selected-result binding paths must agree. A search reply should
retain the unchanged ns0 offer and exact ns0 type key, so final transfer can use
the existing exact-type acquisition API; rederive the extra search descriptor
against the acquired capsule separately, without promoting it to proof authority.
Keep existing mathematics and
exact acquisition unchanged; a discovery namespace changes only for changed
feature identity, not merely enumeration mode. Use fresh sidecar state and
charged selected re-offers, never an implicit global startup/backfill.

First reuse the old33-row case and17-distinct-class/poisoned-first controls to
qualify descriptor/matching/diversity/alternate semantics. Add one fixed
partitioned-provider-cap control and cross-page cursor/version/refusal checks.
No new cryptographic proof or100000-row timing campaign is needed. A subsequent
non-oracle query must return a genuinely retained compatible interface and feed
the unchanged application/check boundary before claiming a search-to-use win.

Recommendation: select this search seam before the optional interactive relay.
Do not label existing v4 exact-type public exchange general applicable-lemma
discovery, and do not label this source decision implemented or globally complete.
