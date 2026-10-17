# Structural semantic preview implementation

2026-10-17. Selected source-only implementation under
STRUCTURAL-STAGING-SELECTION, following CONTACT-LIFETIME-DECISION and its
independent review. Canonical root only. No imports, tests, native execution,
network activity, builds, proof work or Git mutations were performed here.

## Source and public contract

New file: `software/v5/transport/semantic_staging.py`.
Current source: **10,598 bytes**, SHA-256
`1b58f247a4f03c393fe6e52fb22037d56449b183bbb63b2767ab1b344c523be2`.
This is unexecuted source, sent to the independent reviewer and test author.

```python
preview(staged, openings, bodies, foundation_bytes, foundation_sha256,
        *, limits=None)
```

The `staged` records have exactly module, journal (184-byte list), summary,
packet_sha256 and packet_bytes. Each selected module is unique: two records with
the same ModuleID refuse even when their Js agree, avoiding implicit representation
selection. Openings are `{module, opening}`; bodies are
`{module, universes, expression}`. These data records are not verified receipts;
the caller must derive them from its actual same-client staged tokens.

Outputs contain exactly:

- `status`: NEED_STRUCTURAL_CONTEXT_DATA or STRUCTURAL_CLOSURE_STAGED.
- `demands`: NeedModuleEvidence, NeedDeclaration or NeedBody data only.
- `cost`: explicitly whitelisted structural/input-work census.
- `mathematical_acceptance`: false.

No frontend packet, selection binding, warrant census, owner, sealed selection,
author context or live mathematical handle is returned. A final actual verifier
and unchanged live import are required before authoring.

## Implementation invariants

The helper performs a finite data census before whole-input serialization and
before the semantic walker. It restricts ordinary JSON types, integers, strings,
depth, pending values and total canonical JSON size. Per-call bounds include
128 staged modules, 8,192 body records, 2,000,000 input JSON values and depth224;
the existing five context caps constrain groups, declarations, expression visits,
selected bytes and demands. The foundation plus serialized staging input must
fit the selected data cap. Cycles and oversized nested structures refuse before
the context walker. These counts are not claims of total CPU measurement.
The five-field optional limits record is separately bounded at2,048 JSON bytes
before passing it to the existing limits validator. This55-byte source addition
is the only change from the earlier d79c1698 review candidate.

Each complete J is parsed by `aggregate_claims.bindings.member_journal`, binding
the selected relation, foundation, policy, summary and ModuleID. Packet identities
are structurally valid and bounded by the existing32MiB custody ceiling. The
pure helper cannot itself establish that these packets were fetched: that is
the actual facade's opaque staged-token invariant.

Every supplied group requires such a staged module record, valid exact Merkle
opening and matching summary. Duplicate groups/declaration names refuse. Every
body requires staged module membership, a valid body digest and an actual
commitment in a supplied declaration at the same universe arity; duplicate body
identities refuse. The permitted commitment kinds match live materialization
(definition, opaque and recursor rules). The walker demands only definition and
recursor computation bodies, never theorem proof ancestry.

The helper deliberately creates a data item for **every staged module**, even
one with no supplied group. Therefore a referenced unstaged module produces
NeedModuleEvidence; a staged but unopened declaration produces NeedDeclaration.
A fetched group cannot suppress the former by inventing evidence membership.

The semantic algorithm is exclusively the retained pure
`mixed_claims.imports_atomic._build_context`, using the retained data-only
foundation decoder and adopted RelationBasis. It is not a second context
implementation or fake import session. Its provisional context packet and
authority-looking fields are discarded. Missing-module demand wording is
translated for the pre-admission boundary.

## Accounting and remaining work

Returned cost fields distinguish supplied objects, exact serialized input bytes,
JSON values, semantic expression visits, projected frontend size and fixed
foundation bodies. Each invocation reports one preview call. The caller must
charge all invocations/bytes/controller time under the original operation grant;
new per-call input limits are not new cumulative allowances. Repeated full scans
and final live materialization remain costs, not free work.

Root separately implements the staged-token facade. The test author is writing
source-only focused controls including actual preview-demand progression, bad
commitments/J, duplicate variants, missing evidence, finite caps and authority-free
output. Its actual foundation input must be the retained23,313-byte data with
SHA-256 `736792e52ff276f3ee7cdc2efd4fe464e984bc7441771b07cde2aa920ff6b01c`;
the older inert fake-foundation literal cannot satisfy the genuine pure decoder.
No old suite is rerun. Independent review, any root-selected bounded execution,
and the genuine A integration remain separate gates.

Root explicitly selects the facade's direct reuse of `_bounded_json` before its
own serialized-input charge; this prevents facade serialization from undoing the
helper's early bounds. The helper therefore belongs in the facade's actual
source-pin closure. The selected facade now uses its immutable same-client staged
metadata for preview instead of rereading full packet bytes. This pre-execution refinement,
adopted by root and independent review, supersedes the earlier packet-per-preview
proposal. Held groups/bodies are still rebound and repeated selected metadata,
semantic arrays and controller work are charged. Preview makes no present packet
availability or validity claim. Full exact packet readback remains at staging,
describe_staged and before/after actual admission; missing/corrupted packets
refuse before live authority. With one description per token, this gives four
client-charged packet reads per token, not a term proportional to preview rounds.
The original256MiB total-input limit still needs full actual-size preflight.
