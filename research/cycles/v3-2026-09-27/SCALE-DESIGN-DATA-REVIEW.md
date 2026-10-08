# Scale design: bounded adversarial dataflow review

2026-09-27. Reviewer: v3_growth, author of SCALE-DATAFLOW.md. Read-only review
of root's SCALE-DESIGN.md and SCALE-REQUIREMENTS.md, plus the native-only
discriminator in SCALE-LEAN-INTERFACES.md. No code, runtime, experiment or
product change. This is not an independent review of the reviewer's own note.

## Disposition

**No blocking dataflow defect found in the proposed direction.** The root
design explicitly seals remote theorem premises, excludes implicit ancestor
replay, distinguishes local native evidence from transferable cryptographic
evidence, and makes real cold receiving plus subsequent proving a separate
release gate. It does not require one global ledger, complete index, mandatory
global environment, or permanently current global view. Availability and
mathematical validity are correctly separated.

Two narrow wording/gate repairs are recommended before treating this as the
test contract; neither warrants another architecture or broad campaign.

## Actionable clarifications

### Include unrelated-corpus growth in the explicit release gate

SCALE-REQUIREMENTS.md's required discriminator varies both ancestral witness
size H and unrelated corpus/history N. SCALE-DESIGN.md release gate 4 mentions
only H. This omission could allow a future implementation to pass by skipping
proof bodies while scanning every unrelated record/update on cold intake.

**Change:** gate 4 should explicitly require absence of mandatory global
scan/history replay as unrelated N grows, with selected immutable interfaces,
task and views held fixed. Report selected-index lookup costs separately;
bounded logarithmic lookup overhead is not the forbidden linear global scan.
This can be one additional dimension of the same experiment, not a new system.

### Make need-for-body a profile boundary, not an implicit fallback

SCALE-DESIGN.md's sealed default is clear. SCALE-REQUIREMENTS.md still says
`controlled need-for-body/refusal`, which is ambiguous if read in isolation.

**Change:** say that forbidden proof-body computation gives a sealed-profile
refusal/unsupported outcome. A certified propositional equation or an explicitly
selected, separately charged transparent/native route may be attempted; there
is no automatic ancestral witness fetch in the scale lane. Selected definition
data cannot be a label under which the whole witness closure is hydrated.

## The finite local discriminator is useful, with a strict claim boundary

The proposed L -> M -> N native chain isolates a consequential seam: stock Lean
can check a new proof against body-free typed theorem premises, and its next
generation can use the newly produced interface without loading the preceding
proof implementation. That addresses the actual import/conditional-check/export
obstacle which a tiny standalone certificate verifier would not address.

It is **not** a cold remote trust result. A fresh process receiving an audited
local evidence record is still inside that local trust domain. Its authority
comes from A's genuine local check and B's correctly grounded conditional check,
not a hash/signature or a transferred claim that somebody checked it. Do not
call this recursive certificate verification, remote validation or gate 4.

The prelaunch contract should make these observations mandatory:

- B imports L as an actual safe body-free premise; its environment inspection
  confirms no L theorem value. Its checked M proof contains the prescribed
  substantive L applications, not a separately reconstructed congruence proof.
- C receives only M's needed interface/local evidence and adopted base/support.
  It does not receive L or M proof bodies or recursively walk L's evidence to
  rebuild a proof environment. Its checked N proof actually references M.
- A/B evidence registration is controlled by the audited local harness after
  the relevant successful kernel/interface/dependency checks. An input packet
  cannot insert an arbitrary record into the registry. The missing/altered
  evidence and unproved False controls must hit the real gate before import.
- Attribute fresh-record authority honestly: M is checked relative to L, then
  locally grounded by A's established evidence and exact compatible bindings.
  Merely seeing successful `addDeclCore` under L's axiom-shaped entry is not
  sufficient to issue a foundation-grounded M record.
- Record actual B/C packet/file maps and environment contents. If a shared
  harness executable contains issuer fixture construction code, claim absence
  from the selected input and checking environment, not hostile filesystem
  isolation or that no executable could possibly reconstruct the old proof.
  Static role-path review plus exact observed interfaces is appropriate for
  this local seam; it is not an OS confinement claim.
- A conversion negative must use a prospectively fixed actual native term and
  an appropriate positive control. CP-001H's Acc example is source-backed paper
  analysis, not a previously executed reproducer. An ordinary missing-definition
  refusal alone does not qualify proof-sensitive theorem-body behavior.

These observations are consistent with the native draft. They are integration
acceptance details, not a request to replace the finite L/M/N workload with an
LLM discovery campaign or to rerun earlier product tests.

## Release/availability claims that must stay unchanged

Gate 2 may pass while gates 3--6 remain unpassed. A source16 engineering release
can retain its honest native-full behavior and measured reader saving, but
neither that release nor the local-registry experiment satisfies the new
large-network requirement. A mock or trusted-issuer certificate must never be
advertised as a temporary implementation of cryptographic verification.

The root design correctly permits certified sealed reliance when old archives
are unavailable, provided exact required interfaces/definition support remain
available. It correctly makes revalidation/migration after a backend flaw
conditional on retained appropriate evidence. No further replication/ledger
mechanism is needed to resolve this review; actual retention/service policies
can remain separate from the central acceptance/import discriminator.

## Reviewed sources

- [Root scale design](SCALE-DESIGN.md).
- [Scale requirements](SCALE-REQUIREMENTS.md).
- [Lean interface/native discriminator](SCALE-LEAN-INTERFACES.md).
- [Selective dataflow proposal](SCALE-DATAFLOW.md), reviewer-authored comparison
  reference rather than independent evidence.
