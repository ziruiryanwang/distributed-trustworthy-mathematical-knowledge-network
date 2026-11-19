# Actual typed renewal01: preserved failure, exact cause

Independent saved-evidence audit, 2026-10-22. Reviewer: `storage_outcome_audit`.

## Decision

**FAIL: the U-to-V renewal did not complete.** The actual aggregate receipt
verification, interface-only U import and ordinary Lean source/export completed;
the owner adapter then rejected the operational worker report because it used
the integer-only mathematical JSON parser on fractional timing fields. There was
no independent V admission, no V handoff, no new certificate, and no publication.

The evidence is consistent with clean closure and exact temporary-trust
withdrawal. This is a failure audit, not a passing renewal qualification or a
full-v5 result. Preserve the used sources, input, output, charges and failure.
This review performed only bounded reads, hashes and source inspection: no
product imports, constructors, helper execution, tests, verification replay,
proof production, repair or retry.

## Exact run and source identity

All paths below are relative to the canonical project root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

- Base `B`: `product-local/v5-distribution-candidate-preflight-01`.
- Run `R`: `B/typed-renewal01-operations/installed-typed-renewal-01`.
- Consumer operation `O`:
  `B/typed-renewal01-consumer/operations/fd74c7ab7575ed461e2d6b5f6488bdce62de7f5a31c269b84586842df07bc200`.
- Author `A`: `O/preparation/author-1`.
- Trust directory: `B/typed-renewal01-trust`.

Root reports session37038 terminal exit1. Saved outer and nested reports agree
with that terminal outcome; this audit does not infer completion from a still
running process. The installed candidate release remains
`bd9f161c43551a578605d5e0c7da34c332cb838c1c70ddb859d2ebd0062b8f03`.

The authoritative130-entry map is
`experiments/v5-local-checks/distribution-candidate-preflight-01-input.json`,
SHA-256 `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364`.
All130 logical SDK entries equal the plan's entries. All132 planned original
files and all132 operation-local copied files independently match their exact
planned lengths and SHA-256 values. The two additional files are the owner and
helper, not a producer/runtime expansion:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/typed_renewal/owner.py` | 15146 | `2bae25aecfd5935674a540d79580531334179ecce7a1e00ca6171d858fde87ac` |
| `software/v5/typed_renewal/source.py` copied as `owner/renewal_source.py` | 8984 | `fc5902f778fa37b484a4ab50d0594a1d5a0afe8b91896928bf321cce64dac019` |

The five consumer material files in PREPARED independently match their pins:

| File under `B/typed-renewal01-inputs` | Bytes | SHA-256 |
|---|---:|---|
| `U.receipt` | 223610 | `6fb85d28ac62afbc74e5e6c41f466ae45a3b6281a5c480a7e4c54822dc0f2774` |
| `U.header` | 192 | `2df5af1a7ded10f5693fb9bff07a7849a67e2a22eaaca39475bf85f96546cd15` |
| `U.journal` | 184 | `0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657` |
| `U.membership.json` | 92 | `d370d99549af613a6c5a8a8f13c145a4e5e84b0437cec9974b5babc41ad4cc91` |
| `U.opening.json` | 1919 | `392dabae0175f3759ae6862824733f831d28c5548afb44c220b9ffd423d2be43` |

The input directory contains exactly these five files, owner/helper, request and
PREPARED. PREPARED retains producer provenance; it is not an owner parameter.
The actual plan parameters contain the selected foundation, the five consumer
materials, explicit runtime adoption, paths/configuration and finite limits;
they do not pass the full historical production fixture as consumer mathematics.
This does not claim isolation from every file on the host: the operation remains
the explicit trusted-caller lane, not a hostile-source sandbox.

## Actual sequence and boundary reached

1. The owner explicitly created its temporary A-only trust domain and opened the
   ordinary installed client/workspace operation.
2. `O/aggregate-1/command/command.json` invokes the selected aggregate host with
   `verify`, exact A* image
   `9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`,
   and local receipt/header paths. The command exited0, with no termination,
   zero active processes and clean/reaped/closed Job accounting. Its stdout is
   `VERIFIED_RESOLVED_AGGREGATE_RECEIPT`, naming the exact223610-byte receipt
   above. Both local receipt and header match the consumer input bytes.
   `binding.json` records `SAME_CALL_AGGREGATE_BOUND_BEFORE_HANDLE` under profile
   `8ab1d2fb88ffc9fd462ca29d8e2ca410e60e4886fd06c504b24904eca5a71b17`.
3. The owner records the actual U member
   `ad0cc7c499ec6ca71cd211733c3f566f417b4d86a6064292510b927c4eb122c3`.
   The import returns `UNTRUSTED_AUTHORING_CONTEXT_READY`, no demands, one
   group/one declaration, `definition_mode=interface-only` and
   `frontend_theorem_ancestor_proof_bytes=0`. Its selected input is25231 bytes,
   frontend packet26677 bytes, with1047 counted expression visits. The fixed
   foundation includes proof bodies; zero U ancestry bytes is not zero semantic,
   foundation, certificate or controller work.
4. Exactly one source-author call reaches `PASS_NATIVE_EXPORT_ONLY`.
   `A/author-process.json` records exit0, clean/reaped/closed containment,
   no timeout, no termination and empty stdout/stderr. Worker status binds the
   exact request and actual6866-byte export. `A/RESULT.json` reports
   `UNTRUSTED_MIXED_DELTA_PACKET_PREPARED`, explicitly not mathematical
   acceptance. The485109-byte mixed packet is retained.
5. The owner fails before its `source_inspection` assignment and before setting
   stage `independent-native-V-admission`. The report is `FAILED`, stage
   `source-author-once`, error `StructureError: JSON_DECODE`.
6. Closure succeeds. The owner returns nonzero; boot records
   `CLIENT_OWNER_NONZERO_OR_INVALID_RESULT` and outer status `COMMAND_FAILED`.
   The boot traceback is the consequence of owner failure, not its root cause.

## Causal source diagnosis

The used owner contains:

```python
worker = C.parse_json(_raw(directory/"worker-result.json", MIB))
```

Here `C` is `modules.codec`. Its `parse_json` deliberately supplies
`parse_float=bad_number` and `parse_constant=bad_number` to `json.loads`.
`bad_number` raises `StructureError("NONINTEGER_JSON_NUMBER")`.
`StructureError` subclasses `ValueError`, so the surrounding ValueError handler
wraps it as `StructureError("JSON_DECODE")`.

The actual837-byte worker report contains ordinary operational floating-point
fields:

```json
{"deadline_monotonic":2367717.6326964,"wall_seconds":1.9894659002311528}
```

It therefore cannot pass this particular parser. The observed exception follows
directly from those saved bytes and the used source; no rerun is needed to
explain it. The worker's actual successful result also has all the binding fields
which the next owner check requires:

- `status=PASS_NATIVE_EXPORT_ONLY`;
- request hash `8ffddd75b51219ff4757201f71d9fde82c20a3bf8e7a5c09dc33402063c461ab`;
- export hash `e810f5e2fcf2ffc5d67c849af58a6f413bd3ad1d27ba2237e65aba44855c8e78`;
- `export_bytes=6866`, `native_return_code=0`;
- `native_timed_out=false`, `direct_child_reaped=true`.

This is an owner-adapter representation defect, **not** a Lean theorem rejection,
invalid aggregate certificate or evidence that the canonical mathematical JSON
format must permit floats. The minimal future correction is to parse this
bounded operational report with the already selected operational-report parser,
while retaining exact worker/request/export bindings. Leave mathematical packet,
request, export, membership and opening parsing unchanged. Root owns any fresh
source/selector, launch and adoption; this audit changes none of them.

## Source-only lookahead requested by root

The saved request is the helper's intended18-binder theorem: four sort variables,
three functions, six arguments, three equalities, `d`, and `hd`. It imports only
U's group0 interface with an empty `bodies` list. Its source digest is
`b142d1f689171bba47a27df66c7a9a2f121b15937be27ed5337f5d1fee22136a`.

The actual export's theorem root is `RC0.context_transport_then`; its type root
is expression69 and proof root120. Rows103–120 contain18 lambdas matching the
types/binder modes in the18 forall rows52–69. The final proof body is row102:

- row81 names relocated U with universe parameters1,2,3,4;
- rows83–100 apply U to bound variables17 through2, in that order;
- row70 names `Eq.trans` with universe4;
- rows71–80 apply transitivity to D, the left term, the middle term and d;
- row101 supplies the U application; row102 supplies bound variable0 (`hd`).

After the source decoder's zero-based universe mapping, this matches the
helper's expected `Eq.trans.{param3}`/U application structure. In particular,
U is genuinely the first equality argument of transitivity, not a dead mention.
The source successfully compiled under the interface-only context. This narrow
inspection finds no next obvious source-shape blocker. It does **not** execute
`inspect_source_export`, predict independent admission success or retroactively
populate the absent source-inspection result. The packet-shape checks precede
the failing parser in owner control flow, but that fact is not a V warrant.

## Non-admission and cleanup

The client report has one admission submission (the A member), one author call,
one import session; mixed attempts and native-check attempts are both0.
`O/delta` contains only its owner metadata. `R/work` contains only
`typed-renewal-result.json`; `V.packet.json`, `V.journal` and `V.lean` are absent.
No V handoff can be adopted from the retained untrusted author packet.

The final report records `client_closed=true`, `workspace_closed=true`,
`domain_withdrawn=true`, `cleanup_errors=[]`. Client status is `CLOSED`, with
`cleanup_uncertain=false`, no client failures, closed aggregate/mixed/preparation
owners and no receipt issuer. Snapshot, proof-production, network and publication
counts are0. No cleanup failure overrides the already failed result; outer
`final_error=null` means finalization itself succeeded, not that renewal passed.

The saved WITHDRAWN record exactly repeats the owner's trust identity:

```json
{
  "adoption_sha256": "d1ed2443416227a142707b79c07bdaf53c364c0177a63134f75c958609cc3908",
  "domain_id": "5499e433a8a542c59409c652abbae49fe87ab5d46ee749d383f8a65bb204e527",
  "support_id": "2e975813fa6ce63768ad7fa5caecf9909232f0adbf0926f54a8bbfb3db75dd51"
}
```

## Costs, without double counting

The outer operation has44.640625 inclusive Job CPU seconds and9.875 separate
wrapper CPU seconds: **54.515625 known CPU seconds**, with120.756381 wall seconds.
Peak recorded Job private commit is533450752 bytes. Limits remain360 CPU seconds,
480 wall seconds,1024MiB,4 active processes; no cap was raised. The terminal Job
reports7 total processes,0 active,0 terminated; direct child reaped and Job closed.

Within that total, aggregate verification records0.03125 Job CPU seconds and
0.46483559999614954 wall seconds. The author records1.59375 Job CPU seconds and
2.3614539997652173 wall seconds. These are nested observations, **not additive
to the outer total**. Reserved allowances are not measured CPU. Interpreter
startup before the outer clock remains unmeasured, not zero. Outer output
observation is1786859 bytes/163 entries before final-report write; it is not an
exact final disk census. Outer stderr is962 bytes, the saved boot traceback.

## Retained evidence pins

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| `B/typed-renewal01-inputs/installed-typed-renewal-01-request.json` | 7011 | `ed9c39fee4e4e1b93cc7e2e4387f9e4b6c49a8335b7c67b2f16b51c1330be1a6` |
| `B/typed-renewal01-inputs/PREPARED.json` | 7005 | `99dcbf552ab788982f65e71479b3be3f082611a8576d7c5fdedee9ef7978a503` |
| `R/plan.json` | 23465 | `3fa17aff6019481341d6a572c34c29fd35ceb8ee637454bdf977b5ef6c3ee55c` |
| `R/RESULT.json` | 2458 | `2f95fdaf85634d6f6ab38ac0f64e30be47250ed2c4b231dbdb1eb641d44d0c9a` |
| `R/BOOT-FAILED.json` | 102 | `00698c5e9f27b0c3c240a3b1c42af6b079975ee9f789fea5066adbe0e2023ddd` |
| `R/work/typed-renewal-result.json` | 8351 | `d2619445511ef87ad374a71af3e6c24f661d9239a89178f27d9945af97fac84a` |
| `R/command/stderr.txt` | 962 | `95a8b290e0a42c916c41c7c369324cdf521ab349f85f7cdf87189886a34b76d2` |
| `O/aggregate-1/command/command.json` | 1008 | `4476d9bf36a6d50ad82fe94185860bed0ac64f2d8e492809d2480de3a2be9290` |
| `O/aggregate-1/command/stdout.txt` | 938 | `98ef5a08804c0fad8ccc8da00e3d4e5f91e64e89df087307884746b5b31ba95d` |
| `O/aggregate-1/process.json` | 2026 | `2edad207ba51862352f584d784575873cd2885bfd27933c54efb1d3d39640271` |
| `O/aggregate-1/binding.json` | 923 | `5e86d575c1b351760bfabdaf8fde75e0fd33f3636bb4f66bc84a7df2c8a2092b` |
| `A/source-request.json` | 27478 | `8ffddd75b51219ff4757201f71d9fde82c20a3bf8e7a5c09dc33402063c461ab` |
| `A/frontend/EXPORT.json` | 6866 | `e810f5e2fcf2ffc5d67c849af58a6f413bd3ad1d27ba2237e65aba44855c8e78` |
| `A/worker-result.json` | 837 | `70b7f54fd0bc6b082f44a41e6a3e3457b26a624e3db9812b7feb2de7fadb39c7` |
| `A/author-process.json` | 2075 | `dd0bf2787878d6ce4a2a1bf612be3514789e14abd66f6d21ebe97e1009abc5a5` |
| `A/mixed-packet.json` | 485109 | `20edd3884f6af9af365226519375236f6634af008c19090249d0343d4bc81bb1` |
| `A/RESULT.json` | 626 | `91ca975587ff9cacc59a48f4f647773d51c4f1eb7c0ba3d4e5543b6364f4ec51` |
| `B/typed-renewal01-trust/WITHDRAWN` | 370 | `e49da1e2b8db321c7f8e817cafb7b65c83516103bcd4699f48b5db302ce6691c` |

The retained successful stages are valuable evidence for genuine A receipt
consumption and proof-ancestry-free authoring under the selected trust policy.
They do not erase the failure, justify useful-growth claims, or complete final v5.
