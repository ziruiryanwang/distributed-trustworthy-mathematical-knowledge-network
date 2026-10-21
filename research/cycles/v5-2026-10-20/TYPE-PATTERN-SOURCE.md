# Whole declared-type patterns: concrete source decision

Source-only; no implementation, launch or mathematical acceptance claim.
Authority: current109 `distribution-coherent-01-input.json` sdk_sources map.
Decision: implement one optional pattern feature, not another import API/test.

## Exact public interface and profile

New `discovery/type_pattern.py` exports
`pattern_spec(codec, owner_module_id, universes, type_expr)` returning exactly
`{"tag":"declared-type-pattern","value":<64-lowercase-hex-digest>}`.
Input is the existing closed, scoped canonical codec AST, not elaborated source.
The owner identifies the caller's local references; no target ModuleID is needed.
A local signature/template can use its own symbolic names and local owner.
The helper establishes only a structural query, never a valid theorem or transport.
Call existing `adapter.compile_query([pattern_spec(...), ...])`, then `find`.

Opt in with immutable `discovery_profile` exactly
`{"schema":"DMKN_MODULE_EXPORT_TYPE_PATTERN_PROFILE_V1"}`.
Use `DMKN_MODULE_EXPORT_TYPE_PATTERN_FEATURES_V1` and the new workspace schema
`DMKN_V5_CLIENT_EVIDENCE_TYPE_PATTERN_WORKSPACE_V1` (old fields plus profile).
This first profile adds patterns to ordinary atomic features, not pair features.
None and existing pair profiles must retain byte-identical namespaces/records.
Reject the new query tag outside pattern mode, including old pair profile atoms;
do not silently activate unsupported keys merely by extending `validate_spec`.

## Canonicalization contract

Validate owner and universe arity. In deterministic left-to-right preorder,
identify nonfoundation symbols by exact `(module, canonical relative name)`:
local n means `(owner,n)`; external(owner,n) denotes that same symbol.
One dictionary across const AND proj assigns first-use ordinals 0,1,... .
Replace these references by `["slot",ordinal]`; retain foundation names literally.
Preserve every AST tag/child order, bound-variable index, binder flag, projection
index, level AST/parameter index and declaration universe arity. No body access,
reduction, commutative sorting, universe permutation, aliasing or unification.
Hash a domain-separated canonical `{universes,type}` normalized value, with a
versioned domain such as `declared-type-pattern-v1`; return only its feature spec.
Same normalized value iff there is a bijection of the finite nonfoundation
supports carrying one syntax tree to the other while fixing foundation symbols.
Hash equality additionally assumes collision resistance. Neither implies semantic
equivalence: candidate acceptance and actual symbol transport remain separate.

## Bound before allocating

Public AST inputs may contain shared lists/cycles. Before serializing a whole
input, perform a small iterative preflight counting OCCURRENCES, not object IDs.
Bound generic nesting (256), visited JSON values (1,000,000), list length (256)
and encoded bytes (16 MiB minus a fixed 256-byte wrapper reserve).
Only list, str and nonnegative strict int are allowed. Reject bool/other types;
check integer <=2^32-1 and string character length <=1024 before converting it.
Each remaining bounded string can be encoded alone to count exact escaped UTF-8
bytes; count brackets, commas and integer digits too. This avoids serializing an
exponentially shared query before rejection. Use iterator frames, not bulk copying.
Then call unchanged `codec.validate_expr`, retaining its tighter semantic syntax,
node, depth, UTF-8-name and universe bounds. A cycle reaches the preflight bound.
Normalization uses one shared symbol map; no per-node subtree reserialization.
Count levels/names and repeated occurrences; retain existing whole-operation limits.
Work/storage is O(B+n) in bounded encoded syntax and occurrence count, not corpus
size; reject overflow explicitly. Do not silently omit a key from indexed records.

## Minimal selected source scope

Create fresh successors only; selected predecessors and installed bytes stay frozen.
1. New `discovery/type_pattern.py`: preflight, normalization and public helper.
2. Selected `conjunction_index/discovery/module_export_adapter.py`: profile/schema
   dispatch, tag validation, extraction and adapter query-mode guard. Describe
   adds exactly one pattern feature; resolve already re-extracts the same record.
3. Selected `conjunction_index/discovery/formal_features.py`: new schema constant.
4. Selected `conjunction_index/discovery/authenticated_index.py`: snapshot allowlist.
5. Selected `conjunction_index/discovery/discovery_store.py`: adapter allowlist.
6. Selected `conjunction_index/client/workspace_evidence.py`: validate/persist the
   new profile before any directory/lock mutation; pass it to the same adapter.
Root separately selects this helper/source map in a later installation; existing
runtime/remote-reader entry points already pass whole workspace configuration.
No transport, locator, receiver, checker, cryptographic image or planner changes.
Keep MAX_FEATURES=128; adding the one feature may refuse a full old profile.
Fresh namespace/index only; no automatic old-workspace or snapshot migration.

## Why this is the higher-payoff next seam

Current exact declared-type keys retain all symbol addresses; type-edge sets
discard positions/repetition relationships, and selected pairs cannot restore them.
No equivalent helper was found in the actual selected SDK sources. This feature
lets an independently constructed local signature find its renamed whole shape.
For a fixed searched corpus and exact shape bucket of size m inside an old broad
candidate class of size H, it can reduce candidate work from H to m, at one extra
posting per declaration and linear extraction. There is no universal bound m<<H.
Hot identical patterns, definitional variants and generalized theorem applicability
remain unresolved. This is a precise discovery improvement, not a growth theorem.
Required cheap controls: renaming/alias invariance; repeated-symbol distinction;
const/proj sharing; binder/level/foundation distinctions; malformed/cycle/shared-DAG
bounds; old-mode byte identity; profile guards; real store/query/resolve consistency.
Root owns implementation selection and any later finite tests; none ran here.
