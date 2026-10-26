# Independent source review: ordinary contact federation

2026-10-25. Reviewer: `concept_software_bridge`, independent of the protocol,
provider, API, fair transport/search and launcher/loader authors. This reviewer
authored `test_directory.py`; that test is not independently reviewed merely by
this document. `ordinary_routing_gap` has the separate test-source review.

## Disposition

**SOURCE GO for the selected bounded composition and one finite native-free
verification, subject to root adopting the exact package map and test source.**
No runtime was launched by this reviewer. This is not an executed test result,
public-network or TLS qualification, security-sandbox assurance, growth result
or completed-v5 finding. File assembly and final public command smoke have their
own exact inputs and reviews.

The complete CONTRACT, including its absolute-deadline correction, was read.
The new helper and API definitions were read; selected predecessor/current
source differences were inspected for the HTTP provider, fair exchange/search,
peer dispatch, loader and launcher. All original API functions from `find`
through EOF are identical after normalizing line endings/final whitespace and
replacing the one explicit three-line SearchSession deadline change below.
There is no hidden mathematical-checking, custody, admission or indexing change.

## Resolved blocker: relative entry drift

Initial source checked a contact horizon before calling transport, but transport
then created `now + relative_timeout`. A local delay before entering that
coroutine could therefore extend the attempt beyond the contact's original
deadline. A successful ordinary-search test would not establish the stronger
predial property.

Root accepted this as a blocker and selected the minimal propagation repair:

- `directory_find` passes the minimum original attempt/contact deadline to
  `fair_exchange.exchange(..., absolute_deadline=...)`.
- Ordinary `find` first creates SearchSession, then narrows its deadline to
  the original shared ledger, then constructs FairSearch. Its immutable binding
  consequently records the narrowed value, not a subsequently mutated session.
- FairSearch forwards its bound absolute session deadline on every exchange.
- Transport sets `until = min(start + relative_timeout, absolute_deadline)`,
  refuses an already expired entry, and checks remaining time after local
  request/TLS setup before calling `open_connection`.

Thus neither delayed entry nor TLS setup gets a fresh horizon. The proposed
deterministic control advances only the transport's local clock during injected
TLS setup and requires zero connection callbacks. This is a cooperative
checked-before-connect property, not a hard real-time guarantee about when the
OS emits packets. Existing external process containment remains necessary.

## Acceptance and resource argument

The new role returns only inert advisory endpoint tuples. ContactMap commits to
canonical bounded input bytes, uses exact namespace/feature tuples, retains
immutable encoded rows and returns detached parsed output. The 2-MiB map,
2048-key, 16-endpoint-per-key, 32768-byte reply and 64-returned-contact limits
are enforced at the appropriate boundaries. Replies bind the nonce and exact
request namespace/features; extra fields, duplicate endpoint tuples, false
assurance flags and noncanonical JSON are rejected. A different namespace may
return request-bound empty advice; this is correctly not global absence.

Each selected directory/route pair is attempted at most once, with at most 32
planned pairs. The pure owner egress policy is applied before a hint is retained.
Public mode requires canonical literal public IPv4, an owner-selected port,
HTTPS and the owner's system roots. Private/special/mapped addresses, DNS dial
names, peer-selected CA files and peer-selected policy changes cannot turn into
learned contacts. Explicit test mode allows only its listed loopback endpoints.
Bootstrap contacts remain separately owner-selected with the existing CA-pin
mechanism. The new route never follows a second referral tier or executes source.

Before I/O, `directory_find` checks capacity for both directory and search slices,
the zero fetch sequence/pending phase, and availability of both prepayment
labels. It prepays the directory slice without `begin`, preserving the same
OrdinaryBudget for at most one real `find` call. `find` prepays its existing slice;
there is no per-contact grant, refund or new outer wall allowance. Directory
counters charge every started attempt's full reply cap, including failed,
malformed, rejected and truncated results. Request/header overhead is separately
bounded and reported, not silently included in reply-byte accounting.

Contact horizons start before lookup, are capped by the original ledger and
owner max age, and can only narrow. Duplicate hints take the minimum horizon.
Expired hints are dropped before search; the earliest remaining horizon bounds
the combined search. This is conservative and can reduce useful coverage;
it is explicitly not a freshness claim. An uncertain transport cleanup failure
remains terminal. Only settled transport refusals and bounded remote-metadata
parse refusals can advance to another planned lookup.

The finite state-free service compiles ordinary route features, creates one
in-memory immutable map, reserves a fixed lease/cleanup window and uses the
existing provider's connection/request/reply bounds. It does not open a
mathematical catalog, custody store or discovery database. The new HTTP route
uses the exact request-dependent reply reservation and returns bytes once,
without double JSON encoding. Missing other roles retain their existing behavior,
including a `NO_OFFER` reply rather than an index claim.

## Product composition

`peer.py` adds both operations to parsing and state-free dispatch, preserves
output/support path separation, and writes finite service readiness through
the existing bounded report encoder. `run.py` only expands the peer-operation
allowlist. `profile.py` adds the new transport helper to its exact support
closure. The fresh source map must bind the successor fair_search/fair_exchange
and API/provider together; a mixture with the old two-route transport is not
compatible. No predecessor file was changed.

The actual finite API suite uses a newly assembled coherent package and its
pinned loader. It does not manually replace imported product classes. Its
single ordinary V3 record is explicitly synthetic metadata, with no proof or
evidence admission. Actual directory serving, lookup, offer/page transport and
ordinary Store/FairSearch/OrdinaryBudget run on loopback. Separate deterministic
faults inject only clock/TLS setup or an unsettled-transport outcome. Root must
retain those distinctions when interpreting a passing result.

## Exact reviewed product bytes

SHA-256:

| File | Hash |
|---|---|
| contact_directory.py | `a77486e716eb774337f2aedc04771c34395b24a910848600a2eae702f8ae3eb4` |
| http_provider.py | `250543498b83deb4a0893bd159ef6b890fcdd3744be4ca562079368a7f110954` |
| fair_exchange.py | `27e2dffe65aeef12ba22fc18078ed8718ac0548dd39984936b19c27f2f12b321` |
| fair_search.py | `8bf1f0fb5f16d4e460318cb7fa75d2f11322d36d968b6e6524510d177e17ccf7` |
| peer_api.py | `6674a047987cd89d92ede025d2fbd9973f6192a27ae761abc2b24eda9be03c4a` |
| peer.py | `bc8a1c3e3bac2d66e647b3e7154640045cb73ca865bdc412a6c0dc82e39b9712` |
| profile.py | `123f958cb6cdb9260bc0af37b670eb84cb823ca08aba6d84335c4e6b5f16ac41` |
| run.py | `47a2b63c73f1bd8346c5881c6d6a76abac86d33aa8e55bfc19bf3359ea924a39` |

Selected predecessor PROFILE:
`ea7a958db31ac070aa59be1c1e3c50d4b195cfd982c63658bd80de15ef3c6d01`.
Root owns the exact package overlay/assembly selection and execution allowance.

## Boundaries deliberately not converted into claims

One-hop contact lookup removes endpoint preconfiguration for an admitted route;
it does not establish route coverage, relevance, semantic equivalence, scalable
within-provider selectivity, durable availability, independent hosting or useful
growth. There is no universal directory, authenticated global registration list
or automatic endpoint-possession check. The system-CA store and local immutable
owner environment remain trust premises. Testing loopback HTTP cannot establish
public TLS operation. These are explicit remaining obligations, not reasons to
replace this small missing operation with an unbounded networking campaign.
