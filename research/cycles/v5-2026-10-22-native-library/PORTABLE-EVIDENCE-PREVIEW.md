# Portable ordinary evidence and selected-type previews

2026-10-23. Pure source implementation selected by root. No runtime, network,
catalog mutation, migration, native checking, Git action or acceptance occurred.
V1 helpers and frozen evidence are unchanged.

## Problem and decision

An ordinary method must keep its mathematical identity when compatible receivers
use different installed binaries or paths. V1 binds a local implementation
profile into the evidence ID; using that ID as a worldwide search key would
unnecessarily fragment compatible mathematics. The existing `ordinary_semantics`
contract separates:

- **F, foundation:** exact selected basis and its initialization interpretation.
- **S, semantics:** expression/declaration/checking interpretation, including F.
- **I, implementation:** the local runtime/controller/support claimed to implement
  S. That claim requires separate local justification and actual warrant lineage.

The new pure modules implement the already proposed S-based evidence/preview
projection. They do not make I trustworthy, adopt S, migrate a catalog or rename
an accepted native snapshot. Root owns those separate implementation decisions.

## Exact wire and identities

`portable_evidence.py` recognizes canonical bytes of:

```text
{
  schema: "DMKN_LEAN_ORDINARY_EVIDENCE_V2",
  semantic_id: S,
  imports: [[originalName, portableSymbolID], ...],
  unit: unchanged ordinary V1 declaration unit
}
```

The ordered imports equal the complete direct external-reference census of the
unit, including its proof/body syntax. Duplicate, missing, extra or out-of-order
imports refuse. F is not repeated: S already commits to it. No implementation ID,
local context, store, provider address, filename or native artifact enters this
portable envelope.

UnitID is SHA-256 over the existing V2 domain, a NUL byte and the **exact canonical
envelope bytes**. ExportID and basis-symbol IDs delegate directly to
`ordinary_semantics.export_id` and `basis_symbol_id`. Thus changes to a unit, an
import ID or S change its UnitID, subject to the hash assumption; changing I alone
does not. The name and UnitID distinguish an export from its containing atomic
unit. This does not identify logically equivalent proofs or quotient mathematics
by equivalence. The selected full unit, including generated-group inventory,
remains the atomic evidence object.

`portable_preview.py` recognizes:

```text
{
  schema: "DMKN_ORDINARY_LEAN_TYPE_PREVIEW_V2",
  semantic_id: S,
  unit_id: UnitID,
  export_name: originalName,
  header: [kind, exactUniverseParameters, exactTypeDAG],
  type_bindings: [[referencedName, portableSymbolID], ...]
}
```

The corresponding locator has exactly `schema`, `semantic_id`, `unit_id` and
`export_name`, with schema `DMKN_ORDINARY_LEAN_EXPORT_LOCATOR_V2`. A provider's
location is not a mathematical locator field. Multiple advertised headers may
claim the same export; their exact preview byte hashes remain distinct, and only
the header regenerated from that exact evidence can pass `resolve`.

## Public API

| Module/API | Result and scope |
|---|---|
| `portable_evidence.read_evidence(raw, limits=DEFAULT_LIMITS)` | `Evidence(raw, document, unit_id, census)` after one strict parse and unit census. |
| `portable_evidence.portable_unit_id(raw, limits=DEFAULT_LIMITS)` | The same validated identity defined by `ordinary_semantics.portable_unit_id`. |
| `portable_evidence.export_id`, `basis_symbol_id` | Direct aliases of the existing semantic identity functions. |
| `portable_preview.read_preview(raw, limits=DEFAULT_LIMITS)` | Bounded advertisement, selected type-reference keys and node count. |
| `portable_preview.read_locator(value, limits=DEFAULT_LIMITS)` | Strict V2 locator shape and detached name value; not an existence claim. |
| `portable_preview.preview_from_evidence(evidence, export_name, limits=DEFAULT_LIMITS)` | Proof-free preview bytes projected from freshly parsed selected evidence. |
| `portable_preview.describe(raw, limits=DEFAULT_LIMITS)` | Exact preview hash/size, ExportID, locator and explicit nonacceptance result. |
| `portable_preview.resolve(raw, evidence, limits=DEFAULT_LIMITS)` | Exact UnitID/S match and byte equality with the regenerated preview, still nonacceptance. |

Evidence accepts raw bytes or its own inert wrapper at preview boundaries; the
wrapper's raw bytes are reparsed rather than trusting a mutable `document` or
caller-constructed identity field. Preview results likewise derive from raw bytes.
Both parsed structures expose `mathematical_acceptance = False`; describe/resolve
also return it explicitly. Successful parsing may assign an identity to an
**unsupported S**. Only the later controller may recognize and adopt a selected
interpretation; the parser's success is not such a decision.

## Reused mechanisms and costs

No second Lean parser is introduced. All strict JSON/name/unit/DAG grammar is
from `ordinary_evidence`; preview limits, DAG closure and orphan checks are from
`ordinary_preview._type_census`. The V2 wrapper changes the semantic envelope and
identity projection only. Its evidence reader performs one parse/census rather
than calling an identity helper that would force the same full parse twice.

Reading/describing an advertised preview costs work proportional to its bounded
type DAG, encoded names and bindings; it reads no proof/body or ancestor. Creating
or resolving a preview additionally reads and validates the **selected complete
unit once**, including its proof/body syntax, without following imported units.
This one-time producer/selected-acquisition cost must not be described as
proof-free indexing preparation. Generated groups may make a selected unit larger
than one declaration. Existing trusted byte/node/feature profiles can refuse such
inputs; refusal is not a claim that the mathematics is invalid.

For an internal type reference in a generated unit, the preview derives that
member's ExportID from the same S/UnitID/name. External references use the exact
evidence import IDs. The binding census is complete for the root-reachable type,
with no expansion of shared DAG terms. This provides indexable exact identities,
not a decision procedure for mathematical relevance or equivalence.

## Acceptance remains separate

`resolve` establishes only that advertised metadata equals a projection of exact
inert evidence. It does not establish that a proof is valid, that an import is
warranted, that a provider indexed all mathematics, or that I implements S.
The protected controller must still resolve the exact permitted S/F, authenticate
its local implementation and context, resolve every exact import to eligible
accepted mathematics, check all new units and commit actual checked outputs.
No preview, peer-selected ID, `.olean` or metadata success flag can replace that
event. V2 migration remains separately source-designed and unexecuted.

## Decision-changing checks, not yet run

The first focused test set should check:

1. V2 reader UnitID equals the existing semantic helper on the same real unit;
   unchanged bytes/IDs under different local I, but changed IDs for S/import/unit
   mutations. V1 envelopes refuse V2 readers and old V1 sources remain unchanged.
2. Exact import census rejects missing, extra, duplicate, reordered and forged
   shape inputs; noncanonical bytes and trusted resource bounds refuse.
3. A real theorem preview omits its proof and proof-only dependencies; generated
   internal type references get the correct same-unit portable member IDs.
4. Exact evidence resolves its preview; altered header/type binding/name/S/unit
   fails. Unknown S may parse but still yields no supported-profile or acceptance
   claim. Mutated public wrapper fields cannot bypass raw-byte revalidation.
5. Locator fields are exact and detached. Preview orphan/type/node/byte bounds
   retain the existing shared grammar behavior.

These checks should share the next portable/index integration campaign rather
than repeat old kernel, basis, matcher, certificate or whole-library campaigns.
The next product step is the adapter plus coherent protected V2 catalog and
legacy-lineage integration, followed by actual query-to-use-to-contribution.
This pure source seam is not a completed v5 release or growth result.

## Focused checks authored, not executed

Root subsequently selected new `portable_identity_checks.py` source only. Invoke
as `python -B software/v5/ordinary_lean/portable_identity_checks.py` with canonical
root as workdir. It imports the existing small `semantic_identity_checks`
fixtures without invoking their old suite, and uses only bounded synthetic
inert data and hashing. It performs no file/network/native/catalog operations;
bytecode writing is disabled before project imports.

The15 prospective discriminator groups are identity-definition agreement;
implementation/store/location separation; exact unit discrimination; exact import
discrimination; unsupported semantics without adoption; complete ordered import
census; type-only preview and exact binding; different-evidence refusal; forged
export/extra fields; strict detached locator; forged kind/type; forged/missing
type bindings; type-node/orphan bounds; V1/V2 parser separation plus the unchanged
literal V1 hash domain; and forged public-wrapper field resistance. This is not
a repeat of the existing full grammar/descriptor suites.

Each completed group emits `PORTABLE_IDENTITY_CHECK <label> PASS`; successful
completion would emit
`PORTABLE_IDENTITY_ALL_PASS checks=15 mathematical_acceptance=false`.
The expected markers are prospective, not observed evidence. Root owns the
finite run, saved snapshots/output and subsequent qualification decision.

### Controls01 fixture repair; controls02 not run here

Root reports the once-executed `controls01` selection `c331aebd` ended cleanly
after12passing markers. Its appended-orphan fixture kept the old root index,
violating the shared syntax rule that the root must be the last serialized node.
It therefore refused at `EXPR_ROOT` before the intended orphan-reachability gate.
The failure and executed source snapshot remain preserved.

The sole test delta replaces that malformed packet with three nodes: an unused
Nat literal at0, `True` at1 and the `True -> True` root at2, whose two references
both point backward to1. Root-last and backward indices are valid; node0 is still
genuinely unreachable. Expected `PREVIEW_ORPHAN_TYPE_NODE` is unchanged. No
product helper or validation rule changed. Root owns the fresh controls02 launch;
the author ran nothing and makes no claim that the remaining markers passed.
