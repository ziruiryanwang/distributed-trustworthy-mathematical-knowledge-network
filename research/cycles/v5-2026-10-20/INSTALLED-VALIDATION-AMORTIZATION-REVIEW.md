# Producer validation locality: independent design review

2026-10-22, `storage_outcome_audit`. Canonical root only; source and saved-map
inspection, no product execution, tests, constructor, benchmark, proof or Git.

**PASS for the revised narrow design**, not an implementation/runtime pass:
producer-only entry may omit hashing unused `assets/lean/` content while keeping
the full physical census and every existing non-Lean check. The original
63-role/no-census proposal is **not approved** by this review. Root retains
implementation/launch authority.

Reviewed note: `INSTALLED-VALIDATION-AMORTIZATION.md`, SHA-256
`95bf993dc99326e06b9d9f3e36c112c7f7ad0a68c17be946e4b48ecdeadeaa71`.
This supersedes the initial draft's proposed omission of the physical census.

## Consequential finding and resolution

Hashing a selected closure and rejecting extra files answer different questions.
The current complete census also rejects unexpected filesystem candidates that
could participate in import or native DLL resolution. The child's guarded Python
importer does not establish closure for the parent's already executed imports
or Windows native-loader search. An exact63-file list cannot by itself justify
dropping that rejection behavior.

The author accepted this challenge and retained the complete census. Therefore
the first change deliberately broadens only the acceptance of **changed bytes in
existing, unused Lean files**; it does not broaden the accepted path namespace.
Missing/extra Lean files, missing/extra other files, junctions and selected-path
aliasing still refuse. This is a coherent producer-purpose contract rather than
a disguised complete-directory integrity claim.

## Dependency and path argument

The current distribution's `validate_manifest` validates the bounded whole map,
relative grammar, case aliases, file/parent conflicts, role bindings and exact
Lean closure as metadata. `production_metadata` binds descriptor/template and
executes held exact contract bytes; the contract fixes core31/runtime/native
roles. The proposal keeps all of these checks and `census` unchanged.

Producer roles do not select the Lean frontend. The lifecycle constructor binds
the selected stage host, snapshot host and guest image, and sets host cwd to the
release root. Stage/snapshot argv use explicit paths. The unchanged supervisor
`child_environment(cwd)` removes inherited PYTHON/LEAN/RUST/CARGO/RISC0/NODE
variables and inherited PATH, supplying paths constructed from the selected cwd
under `receiver/`; it does not add `assets/lean`. This supports the no-Lean-read
premise for the selected producer path. It does not establish that every generated
PATH directory exists, or that the Windows loader is hermetic.

Unchanged child bootstrap still hashes/censuses its584-file Python closure,
checks the interpreter/search paths, imports held exact product source through
its origin guard, and rechecks at finalization. The producer constructor/owner
retains its60 operative pins and all request/native evidence checks. Explicit
request inputs remain individually pinned even if a caller chooses a path inside
some otherwise unused tree. No pre-await or pre-subprocess observation becomes
post-await/subprocess authority.

Existing trust assumptions remain: an owner-adopted manifest, trusted bootstrap
interpreter/OS configuration and stable local filesystem during each validation
boundary. The proposal is not safe for a deployment intentionally loading
producer dependencies from `assets/lean` unless those reads are separately
covered. It must not be advertised as hostile-local-mutation isolation.

Formally, let L be the fixed `assets/lean/` subset and P the selected producer
operation. Under the premise that P's executable/semantic reads avoid L except
separately pinned explicit inputs, changes to bytes in L cannot change P's
mathematical computation. Thus omitting L's generic content-hash loop preserves
the producer's checked execution relation while deliberately weakening only the
unrelated-content integrity predicate. The complete physical namespace predicate
and all operative-content predicates remain. This conditional argument does not
require a new proof-production experiment.

## Work removed and work retained

I independently recomputed these counts from the installed pinned manifest:

| Set | Files | Bytes |
|---|---:|---:|
| Full payload map/census | 9894 | 919541411 |
| Existing `full=False` main hash loop | 3411 | 758886905 |
| Unused Lean content omitted only for producer purpose | 3250 | 601942392 |
| Retained main hash loop | 161 | 156944513 |

The public profile path currently performs that hash sweep twice. The revision
removes601942392 payload bytes from each such main sweep, not every repeated
metadata/helper read. Full-map parsing and the full physical traversal remain;
there is no measured CPU/latency percentage or corpus-independent complexity
claim. In particular, the earlier ordinary-client renewal overhead is not
explained or improved merely by this separate producer-only change.

## Implementation acceptance conditions

- Use a closed internal producer-purpose branch at
  `installed_production_release` and the profile final rebind only. No arbitrary
  caller-supplied exclusion list; no change to build, explicit full verify or
  ordinary consumer launch behavior.
- Retain full manifest grammar/role validation, physical census, base mapping,
  descriptor/template/held-source checks and every original non-Lean hash.
  Match the exact `assets/lean/` prefix, not a substring or broad assets filter.
- Retain fresh final validation and pending-marker-last-unlink completion.
  Label results as producer-purpose readiness, not complete payload integrity.
- Keep child Python closure, import guard, owner checks, finite allowances,
  trust withdrawal and actual native/evidence binding unchanged. No persistent
  cache, cross-await cache or broad owner-lifetime redesign is needed.

A small changed-boundary control can distinguish corrupted existing unused Lean
content from missing/extra files, selected corruption, role omission and late
mutation. Existing full verification must still reject Lean content corruption.
One selected public profile operation is sufficient to check integration of the
new branch; no duplicate mathematical campaign is justified by this change.

## Source anchors

Installed root:
`product-local/v5-distribution-installed-producer-01/Mathematical Commons v5`.
Manifest2375023 bytes, SHA-256
`8a32634040ac940bb93f6f20681cbbe943a9396c168c7ce9aec548c4153c2403`.

| Inspected source | SHA-256 |
|---|---|
| `distribution.py` | `afbea96badbead846aecc2d3014c19d38375cd2605c225ab0799ebde0ce48774` |
| `sdk/v5/release_production/launch.py` | `3310fbacc7c7724aea37bc2370a29d574fb49685389614e983e0dacf7329a337` |
| `sdk/v5/release_production/launch_contract.py` | `ad2e63a2236d52b2507834dce32f77c1dc3fc55f198dbf39382cb1374a95c802` |
| `sdk/v5/release_production/operator.py` | `f404f0ba4d5177654fd02e999b00c0d8d104f1a4b85295414dff2720ddf6021a` |
| `sdk/v5/release_production/producer.py` | `a466726b79c9a5851ea4e085307aa5ba593c83e2881dc4e168446cbc4f573b1a` |
| `base/operator/commons.py` | `6ea16154f4533e80d2e4e27e12fb6fa0ab7abfa0ff2c52cfb7479c1a35a8c1c9` |

This review approves the narrower principle, not uninspected successor bytes or
the deferred63-role architecture. Existing installation/evidence stay frozen.
