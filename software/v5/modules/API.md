# Module codec and conditional demand model

New v5 source, 2026-10-07. **Authored, not run or qualified.** These Python files
perform structural/hash bookkeeping only. They do not verify a certificate,
type-check a term, create a certificate or admit mathematics. No mock receipt
or caller-controlled JSON status grants public authority.

## Data boundary

`codec.validate_spec`, `summarize` and `module_id` validate and identify a module.
The specification has `schema`, `foundation`, `policy` and ordered `groups`.
Each group is one ordinary declaration or one complete inductive block. Each
descriptor binds its exact kind, relative structured name, universe arity,
type expression, value commitment where appropriate, and kind-specific metadata.
Definition hints `abbrev`, `opaque` and `{regular: n}` remain **Definition** hints;
they do not turn the declaration into an Opaque value.

Lean names are arrays of string/numeric tagged components, not dot-split strings.
`[["s","Tree"],["s","rec"]]` differs from `[["s","Tree.rec"]]`.
Preserve this distinction throughout native translation and permissions.
Expressions use explicit bound variables, ordered positional universe binders,
sorts/constants/application/lambda/forall/let/projection. References are tagged
foundation/local/external; external references contain an exact ModuleSpecID.
The current codec is a bounded tree representation, not a claimed optimal
expression DAG compressor. Native adapters may intern it without changing identity.

`body_id(expr, universes)` identifies an exact closed value expression in its
owner's relative namespace. Definition and opaque bodies are committed by the
specification. Theorem proof witnesses are separate: a different proof and
proof-only imported module may preserve ModuleSpecID while changing witness,
certificate, imported premises and rank. Every new proof must actually check.

`group_opening(spec, index)` produces a bounded exact group inclusion witness.
`verify_group_opening(module_id, opening)` validates hash binding, not validity
of the named module. The certificate conclusion must authenticate the same
summary/module ID and group root. Canonical Merkle shape binds index and count;
odd padding and trailing siblings are checked.

`relocated_name` and `relocate_expr` preserve hierarchical local names under
`DMKN.Mod.<ModuleSpecID>`. They produce an intermediate explicit-name AST,
not native Lean input or a proof that relocation is correct. Group metadata
relocation and the native adapter are still required.

## Conditional environment

`model.ConditionalEnvironment(local_spec)` tracks local groups that **must** be
checked. `ImportClaim` explicitly represents an unverified certificate premise.
`add_claim` and `add_import_opening` only bind exact compatible alleged parents
and commitment openings. A later verifier/controller must discharge every
premise before assigning imported mathematical authority.

`lookup(address, local_cutoff, checking_inductive_group=None)` distinguishes
unknown imported records (`NeedDeclaration`) from invalid local names and
forbidden local self/forward references. Imported records are visible regardless
of temporary consumer insertion order; local groups retain strict cutoffs.
Only the currently checked inductive block may see its own atomic group.

`demand_definition_body` retains Definition kind and raises `NeedBody` if the
exact committed value is absent. It never replaces absence by an axiom,
opacity, false conversion or default expression. `supply_body` is hash-bound
storage, not checking. `supply_local_value` requires the committed definition/
opaque value, or a separate immutable local theorem witness.

`new_local_obligations` requires all new values/recursor rules to be present
and returns **unchecked** obligations. `conditional_premises` always reports
`CONDITIONAL_STRUCTURE_ONLY_NO_MATHEMATICAL_ADMISSION` and
`certificate_verification: NOT_PERFORMED`. Its suggested rank is not authority.

## Immediate next boundary: actual native checker

The model must not become a substitute for the checker. The next source slice
copies the exact needed Nanoda source and license into this evolving subtree,
records predecessor hashes, then implements original-kind missing-body demands,
strict local/new roles and complete new inductive checking. Root owns source
copy/build selection. The guest will rerun the completed witness independently;
native preflight cannot supply a success oracle to it.

Native direct environment lookups, `EnvLimit` distinction, name-cache behavior,
whole-group maps, declaration/body relocation and theorem-interface substitution
are required audit points. An imported type need not expose its original proof
history, but demanded type/conversion dependencies are still real resources.

See `research/cycles/v5-2026-10-07/MODULE-RELATION.md` for the conditional
soundness statement, supported-kind hazards and exact source seams.

## Producer source/native bridges (not acceptance)

`source_rows.decode_source(rows, local_names, foundation_names, foundation,
policy, external_names=None)` decodes ordinary Lean-export JSON rows into a
populated `ConditionalEnvironment`. Name lists contain structured names, not
rendered strings. Each external mapping has `source_name`, `module`, and
`relative_name`. The three inventories must be disjoint. Unknown references,
partial local inductive groups, unsafe declarations, local axioms and unsupported
expression literals refuse. Metadata wrappers and binder/universe spellings are
normalized without changing kernel expressions. Expression expansion has a
whole-operation node budget to block exponential DAG-to-tree growth.

`native_rows.emit_conditional(environment, exact_foundation_rows)` emits parser
rows for the revised native checker. It relocates bodies in their owner module,
preserves missing Definition kind/hint/body commitment and uses explicit theorem
stubs only for imports. All local values remain present. Complete recursor rule
values are currently required even for imported groups. Its output includes
unverified premise bindings and always reports no mathematical admission.

The foundation input is not authenticated by either helper; it must be bound to
the adopted foundation by the actual relation. Source decoding, row emission,
successful native preflight and structural correspondence are distinct from
cryptographic premise discharge. No helper output flag is an acceptance token.
