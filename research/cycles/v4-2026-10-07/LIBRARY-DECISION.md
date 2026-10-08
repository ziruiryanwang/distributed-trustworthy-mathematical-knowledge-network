# October 7 decision: persistent typed recipes before new kernel modules

Source-backed recommendation, 2026-10-07 UTC. Parent selected implementation in
`experiments/named-library-01/CONTRACT.md`. No runtime has been performed by this
author. Existing sealer02 and every used source/evidence object remain unchanged.

## Decision

Implement immutable content-addressed **typed definition recipes** with acyclic
imports, bounded selected-closure acquisition, one shared-DAG lowering and the
existing exact F-closed native/guest checker. This delivers persistent modular
representation without making the kernel trust any new constants. A new guest
is required for a genuinely certified checked-environment import relation, but
is **not required for this storage/application layer**. Yesterday's new-guest
conclusion was about kernel environment extensions and must not be applied to
every form of named library storage.

Root owns store/CLI/provision/integration; growth owns pure codec/lowering/tests;
the scale lane owns bounded store/transport; independent assurance reviews the
changed boundary. No new cryptographic image or expensive proof campaign is
needed to establish this specific software consequence.

## Exact meaning and trust boundary

Each recipe binds the adopted foundation/profile, versioned lowering semantics,
one graph/header definition and up to four direct imports. An import maps a
**local graph name index** to another recipe's content ID. Name resolution is
`(source module, name hash)`, never a process-global display-name dictionary.
The recipe hashes its external IDs and local graph, not a hash occurring in its
own root name. Display names can therefore repeat across independent modules.

The selected pure lowerer emits only one final definition from the requested
module DAG. It does not compile every dependency into a separate flattened
capsule. Expression memoization keys include source, node and simultaneous
universe substitution; hash-consing shares equal emitted nodes across sources.
Separate aggregate bounds cover loaded modules, bytes, graph nodes, traversal,
specializations, depth and final output. Callback time/network behavior requires
the caller's separate bounded supervisor; pure code cannot constrain arbitrary
callback execution merely by counting its result bytes.

An imported definition `D:T:=v` becomes `(fun x:T => x) v`, with the same universe
substitution and source-aware lowering applied to T and v. This deliberately
preserves a demanded type annotation. Plain replacement by v would not validate
the imported advertised T, even if the final root happened to typecheck. The
wrapper is not beta-normalized by the lowerer. Both T and v are lexically closed
except for declared universes/imports, so the fresh identity binder cannot
capture caller variables. The output remains ordinary existing F-closed syntax.

Source justification in selected sealer02:

- `source/checker/src/tc.rs:82-91`: final definition value inferred in Check mode.
- `infer` at514 dispatches the raw application, with no preceding beta erasure;
  it reuses only Check-certified cached results for Check requests.
- `infer_app` at561 first checks the head, then every argument, comparing its
  inferred type against the Pi domain.
- `infer_lambda` at629 checks that the identity annotation T is a type.

Conditioned on the adopted checker's soundness, a successfully checked exact
output thus validates the demanded instantiated imported signatures as well as
the final definition. It does not validate every possible universe instantiation
of every library module or unrelated network mathematics. The lowerer's report
is always unverified; the native result is local/nontransferable; cryptographic
assurance still requires the existing actual certificate route. Typed wrappers
change exact capsule IDs from bare-body expansion; this is correct and is bound
by a new lowering tag, not concealed as byte compatibility.

## Why this is a consequential growth mechanism

For a chain where each recipe adds constant-size syntax and bounded import edges,
the persistent descriptor DAG stores O(n) logical structure. Storing every
successive independently flattened body can contain Theta(n^2) logical row
occurrences; the current compiler already avoids exponential duplication inside
each individual DAG. Only demanded lowering outputs need be cached. This is a
representation theorem, not a claim of O(n) proof-checking CPU, network latency,
or inevitable useful research growth. Universe specialization and deliberately
demanded computation remain charged, and ordinary bodies can still be large.

The reciprocal capability is new persistent library construction: an agent can
acquire compact earlier recipes, inspect their formal interfaces, build another
recipe referring to them, lower/check its requested result and return its compact
new contribution. Existing certificate-backed laws refer to exact lowered
definition IDs and can still be applied under that same checked meaning. No
global research agenda, human-intention acceptance or global ledger is needed.

## Deployment seam and changed-boundary evidence

Existing `definitions/definition_artifact.py` accepts exactly object.json plus
definition.json and its peer routes are definition-specific. Do not append a
recipe file or reuse the namespace as if already compatible. Add a distinct
inert recipe namespace/codec over the bounded transport machinery, immutable
local CAS, key-directed lookup and one composed acquisition budget. All stored
type features are unverified hints; unknown/missing/corrupted modules and partial
custody must fail closed when a requested closure is materialized.

Required discriminators are source-scoped alias collisions, shared diamond
imports fetched once, wrong module bytes/IDs/policy, cycle/missing import,
universe arity and capture controls, all aggregate bounds, deterministic output,
typed-wrapper presence, then **actual wrong imported-signature refusal** by the
unchanged native checker and a genuine acquire/extend/return use loop. Do not
repeat unrelated crypto campaigns. Compare retained compact recipe bytes with
the same family's flattened artifacts, and report all selected materialization
costs separately. The new guest environment route remains an optional later
optimization for authenticated semantic installation, not today's hidden gate.

Exact schema/API and finite constants are in
`experiments/named-library-01/API.md`; executable pure sources are
`library_codec.py` and `library_lower.py` there. Runtime qualification, packaging
and broad-v4 acceptance are separate from this decision.
