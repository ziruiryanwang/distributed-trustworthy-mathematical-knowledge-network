# Ordinary DAG type-pattern helper: source contract

2026-10-28. Source implementation only. Root has selected the port; no test,
package, index migration, native execution or product adoption follows here.
The prior module-codec TYPE-PATTERN-THEORY and its tests remain historical inputs,
not claimed execution evidence for this new DAG implementation.

## API and input boundary

`pattern.py` reuses the selected ordinary_evidence, ordinary_semantics,
formal_query and portable_preview modules. It accesses no files, owner state,
network, Lean worker or proof body. A caller supplies the exact inventory bytes.

- `prepare_inventory(inventory_raw)` checks the <=1 MiB bound and exact
  ordinary_semantics.INVENTORY hash before parsing the fixed 581-name inventory.
  It returns immutable same-process lookup tables. This is a cache for trusted
  Python callers, not a serialized token or a peer-selectable inventory.
- `preview_pattern(raw, inventory_or_prepared, limits=DEFAULT_LIMITS)` reparses
  a whole portable V2 preview, checks selected semantic ID, and derives a key.
- `native_pattern(raw, inventory_or_prepared, limits=DEFAULT_LIMITS)` reparses
  an ordinary native query AST. Local nonbasis names are temporary query
  identities; it invents no portable export ID and performs no owner lookup.

Both return `key`, the singleton-ready `spec`, `profile_id`, `semantic_id`,
`counters`, structural `work` and `mathematical_acceptance:false`. The spec tag
is `declared-type-pattern`. Failures raise and return no partial feature.
Caller-selected limits can only narrow the established preview/codec limits.

Raw input is reparsed even if it originated in an earlier successful report.
All existing syntax, scope, backward-edge, closed-root and reachable-node gates
remain. This Python gate does not additionally claim Lean's decode/reencode
canonicalization or kernel checking. The key deliberately ignores DAG numbering
and duplicate sharing when the validated represented syntax is the same.

## Exact relation and foundation boundary

Basis symbols are derived from the exact fixed inventory and selected semantic
and foundation IDs. A preview anchors a symbol only by that exact basis ID and
its exact inventory name; a known basis ID under another name refuses. A known
basis spelling with a different claimed symbol is nonbasis, not silently trusted.
Other preview references share slots iff their claimed portable IDs agree.

Native-query references are anchored by their exact basis names. Other distinct
names receive distinct local identities. This is an advisory convention: it
does not authenticate the frontend's meaning. A coherent preview and its native
query have equal keys when names correspond injectively to the same occurring
nonbasis symbols and basis names have the selected exact meaning. Malicious
alias claims cannot create acceptance; they can at most alter search or refuse.

The relation preserves all ordered expression structure, repeated symbol
identity, const/projection sharing, de Bruijn indices, binder annotations,
projection fields, let nondep flags, universe-parameter positions/arity,
universe expressions/instances and literal values. Binder/universe *labels*
are erased. Declaration name/kind are not part of the key; a kind filter is
separate. No reduction, unification, partial instantiation, binder permutation,
semantic equivalence or theorem transport is performed.

Modulo hash collisions, equality is equality of the retained complete type
structure under a bijection of occurring nonbasis identities, fixing selected
basis identities. This reuses the old first-occurrence variant theorem.
Changing the shape profile creates another profile ID; a future index namespace
must bind it. Old exact keys, namespaces or index snapshots cannot be relabeled.

## DAG work argument

First pass uses root-first ordered depth-first traversal with a visited set and
an explicit pending-node stack. A constant/projection identity is processed
before its children. Children are visited left-to-right by constructor field
order. Every newly encountered nonbasis identity receives the next slot.

Memoizing a shared subexpression preserves first-occurrence assignment: after
its first traversal all its symbols have already occurred, so a repeated visit
cannot introduce a new identity. The pass therefore agrees with traversal of the
unfolded tree without constructing it. The second pass computes level/expression
digests bottom-up with child digests, independent of node indices and sharing.
It never recursively serializes a normalized expression tree.

For B serialized bytes, V DAG nodes, E edges and S distinct type symbols, work is
expected O(B+V+E) with Python dictionaries/sets; memory is O(B+V+S). The parser,
input byte hashing and name/literal processing are included in that form. Hash
table worst-case behavior is not claimed constant. Fixed inventory preparation
adds its own bounded cost, amortizable by the immutable prepared table.

Counters expose visited expression nodes, expression/level/universe edges,
constant/projection occurrences, abstract/anchored identity counts, bottom-up
node hashes, largest pending-node stack, raw input bytes and inventory bytes
hashed in this invocation. `work` sums the structural node/edge/symbol counts;
it is not physical CPU, elapsed time or a complete parser/byte-work charge.

## Later adapter integration

Root owns the optional new adapter/profile and offline/public query integration.
The existing 128-feature cap remains. Feature exhaustion must explicitly refuse;
it must not silently discard an old feature or omit this profile's required key.
New indexing and its retention costs remain charged. No mathematical evidence
identity, acceptance rule, native build, policy, proof ancestry or owner schema
changes merely because the helper exists.

Needed changed-boundary controls include cross-vocabulary equality, changed
repetition/structure/levels/literals, exact basis preservation, native/preview
correspondence, reordered/sharing-varied DAG equivalence, exponentially expanding
shared DAGs with bounded visit counts, malformed/orphan/open/bounded input
refusal, forged inventory refusal, and no old-profile interpretation change.
They are test obligations, not assertions that tests have run.
