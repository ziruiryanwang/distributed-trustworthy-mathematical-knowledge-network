# Discovery 02: actual search-to-interface bridge

2026-10-28. Read-only audit of the saved `finite-map-discovery-serve02`, `find02`
and `preview02-01` through `preview02-06` operations under
`experiments/v5-local-checks`. No product imports, native checks, owner mutations
or services ran during this audit.

**Outcome:** actual formal-feature search returned six theorem records. All six
public previews completed and bound their returned type documents to those
records. Reading the returned types selected two interfaces for the substantive
refinement contribution. This closes the bounded local discovery-to-interface
bridge. It does not establish mathematical acceptance, independent recipient
operation, novelty, search completeness or useful-growth acceleration.

## Actual query and coverage

Find02 used the fresh service's READY endpoint, `127.0.0.1:62853`, TLS disabled.
Its query contained only `ordinary-lean-export-v2`, theorem declaration kind and
the known portable `Std.HashMap` symbol
`baa1877cd14b1dc673e5273d7289fac7217bd71ac12087079c32df5503f8d452`.
No finite-map theorem name or identifier appears in the query.

One offer and six candidate pages used seven actual requests. They returned six
unique records from snapshot
`4c641b21a09a37b31a96fce6c31761c4e312619f26c36fba3407d076f6714c78`.
The selected nonempty partitions were 12, 53, 61, 63, 245 and 247. Search charged
48 scan allowances, six candidates, six pages, one provider and one snapshot.
There were no failed requests, provider errors or duplicate verified hits.

The returned status is **`INCOMPLETE_SEARCH`**, with termination
`SELECTED_CONTACTS_FINISHED_NO_COMPLETENESS_CLAIM`. Candidate membership does not
establish scan coverage. Actual `verified_scan_coverage`, global completeness,
complete committed anchor domain and conditional completeness are all false;
build assurance is `NOT_PROVIDED`. The six nonempty partitions have no verified
scan intervals. Provider `anchor_boundary` advisories do not change those flags.

The selected search caps were nine requests, eight pages, 64 examined allowances,
16 candidates, 1 MiB, one provider, one snapshot, one inflight request and 20 s.
Each preview had a one-request / 65,536-byte cap. Find's enclosing network ledger
conservatively prepaid nine requests and 1 MiB, while its HTTP accounting records
seven requests and 24,420 response bytes. Do not replace the prepaid accounting
with the smaller actual use.

## Returned interfaces and selection

The six returned names, in actual result/preview order, were:

1. `FiniteMapEffects.optional_then_writing_choice`
2. `FiniteMapEffects.forces_nonempty`
3. `FiniteMapEffects.zero_effect_witness`
4. `FiniteMapEffects.nonempty_iff`
5. `FiniteMapEffects.preserves_nonempty`
6. `FiniteMapEffects.optional_write_empty_outcome`

I decoded the inert returned type DAGs with a standard-library-only reader. The
consequential selection is based on the following types, with ordinary implicit
parameters and typeclass arguments displayed compactly:

```lean
-- K : Type u, V : Type v; [BEq K] [Hashable K]
-- The equivalence additionally assumes [EquivBEq K] [LawfulHashable K].
nonempty_iff (p : Plan K V) (m : Std.HashMap K V) :
  (forall n, Exec p m n -> n.isEmpty = false) <->
    (m.isEmpty = false Or mustWrite p = true)

zero_effect_witness (p : Plan K V) (m : Std.HashMap K V) :
  mustWrite p = false -> Exec p m m
```

The first characterizes all nonempty-result guarantees using the write summary
and input map; the second supplies an execution that preserves the input when
the summary is false. These are the required semantic ingredients for reasoning
about refinement and contexts. The displayed text is an explanatory rendering;
the bound returned type DAGs remain the exact data.

`discovered-acquired-targets.json` was written from preview02-04 followed by
preview02-03: `name` from `preview.export_name`, `unit_id` from `preview.unit_id`,
and `export_id` from that preview's actual matched `record.object_id`. Each
preview selection equals a member of the actual find result. Only **after**
writing the derived file did I read and compare the prospective
`acquired-targets.json`: the structures agree exactly.

| Selected interface | Export ID | Unit ID |
|---|---|---|
| `nonempty_iff` | `3fe2401bbd04ea80d7d7ab4851005865e43b9669099f78f5e0892dfeeaad4175` | `63603a0a47d769693bdfd62227e546b67069dd6a041a3e1632e325c341cc4562` |
| `zero_effect_witness` | `3d68aec796ef21713c99e7c839663a4c49f3aa06a45ab3f17982dc812113877c` | `0783babf0985c4777d9712c2c3be813056f65dcca0d5e39ee8e49856be3b8757` |

Derived file: 1,776 bytes, SHA-256
`a62aba4352f6310741738618c7a2fc56b7cfe92571239bf28423825a4315e690`.
This is an engineered workload with a preplanned mathematical extension, not a
blinded novel-concept discovery study.

## Binding and closure checks

All eight outer operations ended `COMMAND_EXITED_ZERO_AND_CLOSED`: child exit
zero, reaped, Job closed, final active processes zero, no termination requested,
empty cleanup errors and empty stderr. The service ended `LEASE_FINISHED`,
quiescent, no pending cleanup or reserved replies, and stopped accepting.

For all 25 source snapshots, saved bytes match the corresponding selections.
All eight selection hashes match their outer result. Every saved stdout parses
identically to its public RESULT. Service READY equals its saved public result
and find's contact. Selected runtime pins number 164 for serve, 165 for find and
166 per preview; these runtime files were not independently rehashed here.

For all six previews, canonical JSON re-encoding of the returned document has
exactly the returned/record byte count and SHA-256. Export name, unit ID and
semantic ID equal the selected locator; selection equals an actual find match
and the exact selected preview config. Each preview finished with
`PREVIEW_BOUND_NOT_ACCEPTED`, closed its one-request ledger, and has zero pending
requests/reservations. `evidence_bound`, `snapshot_membership_reverified` and
`mathematical_acceptance` are all false. No theorem proof was acquired by these
preview calls. Mathematical use still requires the unchanged admission boundary.

The service's final totals exactly agree with client HTTP totals:

| Quantity | Find | Six previews | Total |
|---|---:|---:|---:|
| Actual requests | 7 | 6 | 13 |
| Response-body bytes | 24,420 | 32,038 | 56,458 |
| Request-body bytes | 4,333 | 888 | 5,221 |
| Reported header bytes | 1,598 | 1,350 | 2,948 |

Provider failures/refusals are zero. Thirteen actual requests fit the 16-request
provider cap; 56,458 response bytes fit its 4 MiB cap. Client conservative charges
are 15 request slots and 1,080,614 response bytes including find prepayment.

## Cost retained

The table sums disjoint Job CPU and its outer wrapper CPU. Nested controller and
inner-supervision counters overlap those scopes and are not added again.

| Operation | Wall seconds | Job CPU seconds | Outer-wrapper CPU seconds |
|---|---:|---:|---:|
| serve02 | 301.486091 | 5.078125 | 2.593750 |
| find02 | 1.742965 | 0.812500 | 0.500000 |
| preview02-01 | 1.444633 | 0.765625 | 0.515625 |
| preview02-02 | 1.445194 | 0.812500 | 0.531250 |
| preview02-03 | 1.402680 | 0.828125 | 0.468750 |
| preview02-04 | 1.391554 | 0.765625 | 0.515625 |
| preview02-05 | 1.488156 | 0.859375 | 0.500000 |
| preview02-06 | 1.532824 | 0.906250 | 0.500000 |

Known measured CPU is **16.953125 seconds** for this bridge: 7.671875 service
and 9.28125 client CPU seconds. The seven client operation durations sum to
10.4480048 s, which is not end-to-end elapsed time because operations overlap
the service and some previews overlap. Peak per-operation Job private commitment
was at most 31,502,336 bytes; this is not an aggregate-memory peak.

The prior idle serve01's 9.203125 known CPU seconds and 301.609174 s elapsed
remain charged separately in DISCOVERY01-OUTCOME. Including that idle attempt,
known CPU across the two service attempts and actual clients is **26.15625 s**.
These numbers exclude earlier creation, publication, indexing and human/agent
research costs; they are not a full-cost growth comparison or speedup result.

## Evidence pins and next action

| Operation | Public `peer/RESULT.json` SHA-256 |
|---|---|
| serve02 | `088641178230502e62be97f139dc00817e62b2c16b0fc5a813835f01258340df` |
| find02 | `69ed25ff27c46d6d56a70a821d5b1589151b318da8eb11374b4973a0600b2830` |
| preview02-01 | `0e51b73aa4953a74bff6f68b787985d21bca4883f73f80fb65b90eb8e243ae20` |
| preview02-02 | `805973d2cdb4b0849dc4d096a5f48691b83b6845b0598a55f656760b34cee1a3` |
| preview02-03 | `35e1eb3f34ff431e2f38a0ea06ed7cc94fd9d47c6f987b609da3c2bee24ec08b` |
| preview02-04 | `a7033a64689209cf80b4916f355c9869070b9167c998f23bccd878d245c1b49d` |
| preview02-05 | `4a55f4153482cfb430774e1be7718e37d6b4b16e3cf6ca9cbcacab91258c326d` |
| preview02-06 | `8773e3079e94c227146e34a1c0ed95fa57c14e1e9fcf9583bb188c5f00003e17` |

Serve02 outer RESULT SHA-256:
`360b37b9c386c9d419342d508ac7972214897b61a11003b3ff2a0698e00c8714`;
find02 outer RESULT:
`866d8999824c3f29f58ee30ec637631ffe928d05b0a8e3e37dea058fd73305a6`.

The next decision-changing operation is the already prepared BodyMath contextual
refinement contribution with these discovered targets and the protected Std
ancestor. The discovery service is terminal and no longer holds the owner.
There is no reason to repeat search, previews, index construction or idle hosting.
Root owns selection and launch after the remaining frontier gate.
