# Portable ordinary authoring: source checkpoint

Date: 2026-10-23. Owner: `portable_integration_audit`.

Status: source implementation and author self-review only. These three new
files have not been executed, compiled, or independently reviewed by this author.
No store was opened, accepted state changed, old operation repeated, or native
runtime launched. Root owns independent review, integration and any finite test
selection. Existing used V1 sources remain unchanged.

## Purpose and decision

A local agent that acquired and accepted mathematics through the portable V2
path must be able to use it in an ordinary Lean authoring environment and export
its own complete successor. Reusing the V1 wrapper verbatim would mislabel the
portable semantic contract and foundation as machine-local implementation and
basis-root identities. This successor changes those wrappers explicitly while
preserving the already investigated construction and new-proof checking model.

The resulting path is:

1. A protected receiver context supplies exact accepted symbol bindings and
   retained inert evidence for the selected mathematical targets.
2. A bounded request prepares the relevant interfaces and construction units.
3. The Lean helper supplies missing scratch handles in the agent's environment.
4. The agent authors a complete new theorem and exports an inert candidate.
5. The protected receiver resolves that candidate's imports, checks complete new
   units against its actual accepted context, retains evidence and commits only
   through its separately controlled admission path.

Steps 2–4 confer no mathematical authority. Existing local Lean declarations
need not match the receiver's definitions; this may cause final checking to
refuse, but cannot justify bypassing that checking. Human intent, popularity,
root research goals and certificates do not enter this boundary.

## Exact identities and schemas

`S` is the selected semantic contract from `ordinary_semantics.semantic_id()`.
`F` is its selected foundation from `ordinary_semantics.foundation_id()`.
`K` is the exact active protected **local** context root. `K` is neither `F` nor
a portable identity shared by all machines. The semantic contract commits to F;
the request additionally carries F explicitly to prevent accidental relabeling.

`portable_owner_request.prepare` has the keyword-only interface:

```python
prepare(
    *, semantic_id, foundation_id, context_root, inventory_raw, targets,
    warranted_symbol, fetch_evidence, owner_absent, limits=Limits()
) -> PreparedRequest
```

It reuses `owner_request.Limits`, `PreparedRequest`, `RequestError` and
`_semantic_refs`. `PreparedRequest` contains immutable header/group bytes,
dependency-ordered selected evidence IDs and finite acquisition/payload counts.
The group format remains `DMKN_OWNER_GROUP_V1`; raw Lean unit grammar is unchanged.

The header has exactly these seven fields:

```text
schema = DMKN_OWNER_REQUEST_V2
semantic_id = S
foundation_id = F
context_root = K
basis_rows
targets
group_count
```

The exact fixed 581-row inventory is SHA-256 checked before parsing. Each basis
symbol must equal `basis_symbol_id(S, F, name)` and the protected lookup's answer.
Every acquired unit is parsed with `portable_evidence.read_evidence`, must name S,
and must actually export the requested name at `export_id(S, UnitID, name)`.
Every output and every import ID must match the selected protected context.
Merely hashing a claimed name or possessing an evidence envelope is insufficient.

## Selected closure and cost boundary

The Python traversal preserves V1's selected-group breadth-first acquisition,
complete direct-import census, atomic groups, cycle refusal and dependency order,
with the signature-only refinement described below.
No whole accepted-library enumeration or global-network traversal is added.
Theorem interface rows omit proof values even when the theorem is absent from
the scratch environment. Missing non-theorem groups retain full construction
units and their required import closure; generated groups retain complete units.
Partial group presence, overlapping outputs, mismatched IDs and
unclosed semantic dependencies refuse.

This is **not** a proof-free acquisition claim. The current request helper still
fetches and syntax-inspects complete retained evidence for each selected group;
its acquisition counts include those bytes and nodes. The native construction
helper does not replay accepted theorem proofs: missing theorem types become
well-formed scratch assumptions, while demanded definitions/generated groups
use the existing local checking path. A selected theorem can still have a large
raw evidence object. An accepted-interface store would be a separate later
optimization, justified only by an actual whole-workflow bottleneck.

The default request limits retain 8,192 groups, 65,536 rows, 1,024 targets,
8 MiB/group, 64 MiB prepared payload, 128 MiB acquired evidence, 20 million
acquired syntax nodes and 262,144 selected dependency edges. The V2 helper also
refuses a header above 1 MiB before native work, matching the native reader.
These finite bounds are not a prediction of actual peak memory or latency.
Caller-customized Python limits do not enlarge the native helper's defaults.

## Lean construction and export

```lean
#ordinary_construct_portable directory semantic context foundation
#ordinary_export_constructed_portable target output
```

The first command checks the exact V2 header and the supplied S/K/F strings,
bounded sequential group reads and the final group census. It calls the unchanged
`OwnerConstruction.constructPrepared`. Its `OwnerRebind.Prepared` mapping is:

| Retained internal field | New value | Meaning |
|---|---|---|
| `profileId` | `semanticId` | S, not a V1 implementation profile |
| `contextId` | `contextRoot` | K, exact protected local context |
| `basisId` | `foundationId` | F, not a local basis root |

Source inspection of `OwnerConstruction.makeIndex` establishes that these three
fields are validated and counted as labels; no V1 identity or basis-root formula
is interpreted there. New explicit wrapper names and schemas prevent accidental
use as the retained V1 API.

Construction bookkeeping uses a separate nonpersistent, module-local environment
extension. It records S/K/F, interpretation labels and introduced names. The
exporter requires that exact same-module context, a new current-module theorem
record not already in the boundary, a fresh output file and nonempty new units.
It calls unchanged `SuccessorExport.selectedDeferred`, preserving complete new
unit serialization, claimed exact IDs and the finite unresolved-name frontier.

The exported candidate has exactly these ten fields:

```text
schema = DMKN_ORDINARY_CANDIDATE_BUNDLE_V2
assurance = INERT_OWNER_EXPORT_NOT_MATHEMATICAL_ACCEPTANCE
semantic_id
context_root
foundation_id
targets
boundary_imports
unresolved_imports
units
stats
```

Statistics retain the seven V1 names: `source_records_enumerated`,
`selected_units`, `dependency_edges`, `scan_nodes`, `unit_json_bytes`,
`boundary_imports`, `unresolved_imports`. Lean's bounded writer JSON is not itself
portable canonical evidence. Root's `portable_candidate.bind_candidate` must
validate the writer envelope and reconstruct canonical V2 evidence, or return
the full missing-name frontier before any admission.

The candidate binder must require the selected S/F/K, explicit expected targets,
and exact prepared labels. Claimed IDs must equal both prepared and protected
context bindings; unresolved names may be resolved only by protected point
lookups, never by replacing a previously claimed ID. The completed evidence is
still inert until independent final admission.

## Controller obligations and exclusions

- `warranted_symbol(name)` must be a stable point lookup in the selected eligible
  protected context. An arbitrary callback or peer dictionary is not a warrant.
- `fetch_evidence(name, ExportID)` must return exact retained portable bytes.
  Callback I/O, failed acquisition charges, absolute deadline and hard resource
  containment belong to the parent controller; the pure helper does not enforce
  those external operations. `owner_absent` is only a hint rechecked in Lean.
- The controller authenticates the canonical request and complete file map,
  rejects aliases/duplicates, and binds the actual invocation to those bytes and
  identities. The native wrapper's matching strings do not establish eligibility.
- Scratch signatures, authoring environments and candidate files must never be
  promoted as accepted snapshots. Complete new proofs cross the actual receiver
  checker and event-bound commit; raw evidence must be durably retained before
  accepted-catalog promotion if it is to be republished.
- This source seam adds no source sandbox, executable peer imports, certificate,
  remote checking trust, automatic unresolved-library acquisition, public CLI,
  deployment or native-artifact portability. Root must integrate the reviewed
  seam into a usable public workflow before claiming that capability.

## Source pins

All paths below are relative to the canonical project root. SHA-256 values pin
this source checkpoint, not compilation or mathematical acceptance.

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/portable_owner_request.py` | `cf4a899642128f99839010248b5817a0e00e79411cfae36c4be654f85a6fc242` |
| `software/v5/ordinary_lean/PortableOwnerConstructCommand.lean` | `250a8dd1292c1dd5d228d69eaeb7abdbb5f0e9ad96c48a8b32d80203c27619b2` |
| `software/v5/ordinary_lean/PortableConstructExportCommand.lean` | `8251bc13836fde6620203752b9378bfafccefeef16587788221dec7ad7e95a8b` |
| `software/v5/ordinary_lean/owner_request.py` | `b6f39083728304c49f99cd8c223b5e44b3fa89a4c6a1092ec7eefdeddabfcd17` |
| `software/v5/ordinary_lean/OwnerConstructCommand.lean` | `bded743c7ce6a76ebbfcc375dac78c4b240555acf246622ed483fe69d4abdffc` |
| `software/v5/ordinary_lean/ConstructExportCommand.lean` | `b7f9cd638a2178068b485adb6695bb476517eda1a10b3b6b584d74707d257a94` |
| `software/v5/ordinary_lean/OwnerConstruction.lean` | `04f605717af3b907195756455c2ec645e37e20ce9897c0510f47d7da24895ed3` |
| `software/v5/ordinary_lean/OwnerRebind.lean` | `63ffaac12ae23d5e21ddbee7857e08f2a3f6d01a950b87a4128f27ae48594cc3` |
| `software/v5/ordinary_lean/OwnerUseCommand.lean` | `cfeaaf28f48234de86000694c52a0350bd62f1120ae4bbd18d76ee5f42776313` |
| `software/v5/ordinary_lean/SuccessorExport.lean` | `c68286f46711d0f2c2e13db972ffbc207feb6a4bfea157a53a251bfb5cb1d8c8` |
| `software/v5/ordinary_lean/SuccessorExportCommand.lean` | `1b5a381476d84b832d5200456aa6087c3c9e5e25d322c61076e86d9bf538a741` |
| `software/v5/ordinary_lean/ordinary_evidence.py` | `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6` |
| `software/v5/ordinary_lean/ordinary_semantics.py` | `ee601536f53640a2695e51d37d3e87e6746604ed6433cb3ace9349ae1aedf915` |
| `software/v5/ordinary_lean/portable_evidence.py` | `f8ea819bdd9344d696cef2725888828125b2ef5d1b60d2c31a0412657a62cbd8` |

Author self-review compared all three new sources to their V1 counterparts,
the complete `OwnerConstruction` implementation, the retained candidate writer,
the portable identity/evidence definitions and the root-owned candidate binder's
current schema. No source-level incompatibility was identified. This is not an
independent review or an executed outcome; root selects the smallest changed-
boundary checks and native build/use only after the independent review.

## Independent binding/controller-source review

Root separately assigned this author to review root-written
`portable_candidate.py` and `portable_candidate_checks.py`. This subsection is
independent of those two sources' authorship, but not an independent review of
the three authoring wrappers above. Review was source-only; no controls ran here.

Disposition: **no source-level blocker identified for the scoped candidate
binding path or its proposed finite controls**. This does not establish native
acceptance, public integration or a deployed workflow.

The complete binder and all eleven test methods were read, along with the
retained synthetic fixture, portable identity/evidence definitions and the exact
candidate-writing wrapper. The seven-field request and ten-field writer formats,
the seven statistic names and default aggregate boundary/bundle limits align.
Writer JSON may have Lean's key order; it is bounded and checked before canonical
portable evidence is emitted. No binding step opens a store, loads a native
artifact or grants an accepted root.

The consequential bindings are explicit and correctly ordered in source:

- Exact selected S/F/K and expected target list are checked before interpretation.
- Each claimed import requires equal exporter, authenticated prepared and
  protected-context IDs. Duplicate claims refuse; no ID is substituted.
- An explicitly unresolved name cannot already occur in prepared labels or
  claimed imports. Only the protected point-lookup callback may assign it a
  local interpretation. That interpretation remains subject to final proof checking.
- New outputs are syntax-censused, disjoint from imports/other outputs, and must
  be absent in the actual selected context. Complete new raw units are retained.
- Every unit's external names must be available from the finite boundary or
  earlier new units. Forward references refuse. Missing names return together
  with no evidence; a READY result constructs each new ExportID from its exact
  canonical V2 unit and uses it in later units.
- Limits bound input, units, bindings, returned evidence and aggregate nodes;
  the callback is checked at bounded workflow boundaries. Hard containment and
  the callback's stable protected lookup remain controller premises, not claims
  of instantaneous interruption during a single parser/census operation.

The tests exercise a two-unit dependency chain, deduplicated point lookups,
multiple missing names, explicit unclaimed interpretation, both claimed-ID
disagreements, prepared-to-unclaimed relabel refusal, duplicate/existing outputs,
forward references, exact context/schema/targets, byte counts, node/deadline
limits and noncanonical writer order/duplicate-key refusal. Their small
declarations are synthetic well-shaped syntax, deliberately not proved Lean
mathematics. The fixture's expected callback count is consistent with the three
sequential refusal attempts; the first two each reach Nat once and the expired
third call reaches no lookup.

One nonblocking pre-freeze recommendation was sent to root: add wrong
`semantic_id` and `foundation_id` envelope values to the existing context/schema
test's table. These new identities are the adaptation's principal boundary and
can be covered without another test campaign. The code already checks both;
the reviewed test cut below does not yet contain those two table rows.

| Independently reviewed source | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/portable_candidate.py` | `29ae111a362472b09b2b1ff16b567b352be793d76c2cd1b5421e0aee29219331` |
| `software/v5/ordinary_lean/portable_candidate_checks.py` | `23859730dd8732a10d373b808231693bb8c17c4c02beca445e787d1638b14aee` |
| Retained fixture `software/v5/ordinary_lean/semantic_identity_checks.py` | `9614df54f8bc66ab4d5086aa94eef46cd738466d38bdecdfff474e6d2ba972b4` |

### Root-reported candidate control outcome

Root subsequently added the two recommended envelope S/F mismatch rows and
reported `ordinary-portable-candidate-controls-01` PASS: all eleven test methods,
0.34375 known CPU seconds, 0.512086 wall seconds and clean closure. The selection
prefix is `e44e62bf`. Root reported that stderr contained the normal unittest
summary, not a failure. This is a **root-reported executed result**, not a second
execution or an independently audited outcome by this author. The updated used
test file hashes to `2a346e1cca24276d2fa2a0b7b40fa4c5e68f156f2883b232f4bccdeeb5892ace`;
the two added rows were source-read here. Candidate and used test bytes now stay
unchanged.

## Signature-only missing-theorem refinement

Root identified a central avoidable cost in the unexecuted V2 request successor:
the copied V1 `if missing` branch fetched proof-only ancestors and included a
complete optional unit even for a singleton theorem. Yet the unchanged native
`OwnerConstruction.demand` mode-0 branch ignores that optional unit. It decodes
only the theorem's type, demands the type's dependencies, and installs a checked
scratch signature. The theorem's accepted receiver identity—not replay of its
proof in scratch authoring—determines how the final complete proof is interpreted.

The V2 helper now classifies `signature_only` exactly when the acquired unit has
one output whose inventory kind is theorem (`2`). The optional full unit is
included only for a generated group or a missing non-signature group. The full
external-reference census is added to acquisition traversal only for a missing
non-signature group. The same semantic-reference extraction still follows every
theorem type reference; definitions and generated groups keep their complete
construction dependencies.

This omission is justified by the native helper's actual demand relation, not
by assuming the theorem has no proof dependencies. Every original import ID,
including proof-only imports, is still compared to the protected context.
The selected theorem's complete raw evidence is still read and syntax-censused
to establish its exact UnitID and output census. Only unnecessary **recursive
acquisition** and unused optional proof payload are removed. No accepted-proof
replay, receiver rule, evidence identity or old V1 source changes.

The source-only focused control is
`software/v5/ordinary_lean/portable_owner_request_checks.py`, SHA-256
`735d4ef564b22dc110b09ec791c4bc08f3d6cfebcaffb669733ec3d72a77650b`.
It reads the exact fixed inventory with SHA-256 `c81800ab...f7cdba1b0` and uses
synthetic portable units/callback bindings, not mathematical warrants. Its single
test has two subcases: a missing theorem must still check its proof-only import
ID but fetch only its own evidence and emit no optional unit; a missing definition
with a body dependency must fetch both complete units and order the dependency
first. Payload, selected IDs and acquisition-byte counts are checked. No execution
was performed by this author; independent review and root selection remain gates.

The former unexecuted V2 request pin `d3e804f6...b8db9f6` is superseded by
`cf4a8996...a6fc242`; used V1 and prior native/evidence bytes remain unchanged.
