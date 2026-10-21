# Independent helper/preflight review

Decision: READY for the selected finite controls; no source blocker found.
This is read-only static review, not execution or final product acceptance.
Reviewed `software/v5/type_pattern/discovery/type_pattern.py`
SHA-256 `b75277b55cdb25a22fbdc517bdc0bdf1173ced7c22c895fdc313a86f23857582`,
and adapter `336ae03bccbb5c700c36ab45f91235a23e27d15543f3eeddbb24d28c47f0f6ce`.
Theory reference: TYPE-PATTERN-THEORY `3d1054d4`; ordinary codec default limits.
Workspace and test-suite review are outside this assignment.

## Allocation occurs after a bounded occurrence preflight

Owner is exact str, length64, then digest-validated; universe arity is a strict
bounded integer before any conversion. `_preflight` precedes codec.validate_expr,
whose canonical serialization would otherwise allocate an expanded whole tree.
Only exact list/str/int values pass: subclasses, bool and custom objects do not.
Integers are bounded before str conversion; an enormous integer is not printed.
String length is bounded before escaping/UTF-8 allocation. Each temporary scalar
encoding is at most 6146 bytes for 1024 characters; lone surrogates are refused.
The codec subsequently applies its stricter UTF-8 name-length and syntax rules.

Iterator frames avoid bulk child-stack copying. Every occurrence is visited and
charged, including each repeated DAG occurrence. Cycles hit depth256; expansion
hits depth, one-million-value, list256 or byte limits before whole serialization.
For this list-only AST grammar, counted brackets/commas/scalar encodings equal
compact JSON byte length. No dict keys or arbitrary encoding hooks are omitted.
This assumes ordinary non-concurrently-mutated inputs and the trusted pinned
codec; it is not protection against arbitrary code running inside the caller.

## Normalized output remains bounded before hashing

After preflight, unchanged codec validation limits syntax to250000 semantic
visits/depth192 and validates every reference, level, name and binder field.
The normalizer does not unfold semantics or recopy an expanded proof ancestry.
At most one slot is created per encountered nonfoundation reference, hence
fewer than1000000 slots. `['slot',index]` needs at most15 compact JSON bytes.
The shortest legal local reference needs19 bytes (a numeric name component);
an external reference is longer. Thus every replaced reference shrinks.
All remaining syntax is retained unchanged. The normalized dictionary wrapper
and universe arity need fewer than256 bytes, already reserved by MAX_BYTES.
Therefore hashing cannot first allocate an over-limit expanded normalized JSON
for a stable, successfully preflighted input. It still allocates bounded AST,
map and serialized output; this is not a zero-memory or streaming claim.

## Exact variant relation is preserved

One dictionary keys exact owner plus canonical name bytes, shared by const and
projection references. Local n and external(input_owner,n) coalesce. Foundation
names remain tagged/literal, and cannot coalesce with a nonfoundation slot.
First-use order follows ordered expression fields; repeated identity receives
one slot, while different identities cannot alias through a mere name hash.
The mapping preserves forall/lam binder flags and domain/body order, all let
fields, app positions, projection index and structure, bvar positions, complete
sort/constant universe expressions and declared universe arity. No fields from
the validated expression grammar are dropped. Binder names were already erased
by the codec; parameter indices are not permuted. This matches the stated iff
canonical-tree characterization, with the separate SHA-256 collision assumption.

The adapter uses the same helper for extraction, charges its occurrence count
to the existing work bound and adds the feature without silently truncating it.
Limits are explicit refusals. Ready to test these changed boundaries; no new
mathematical authority, generic matching or globally selective search follows.
