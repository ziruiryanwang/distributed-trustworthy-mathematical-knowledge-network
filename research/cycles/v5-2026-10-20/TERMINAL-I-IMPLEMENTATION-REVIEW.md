# Direct-I ordinary circulation: independent implementation review

2026-10-21, core_release. **Source GO; no blocking implementation defect found
in the five reviewed successors.** Focused controls are still being authored;
this note is not execution, installation or release clearance. No product code
was imported or executed. Root retains launches, integration and Git.

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Reviewed root selection `TERMINAL-I-IMPLEMENTATION.md`, full contract
`38a5f73ccabe70e1bdcffba55623d6f9ce008b46188f46d4348a86668a8c80a8`,
independent design challenge `c82d15c6...`, and author checkpoint
`TERMINAL-I-SOURCE.md`, SHA-256
`6555ef209db291cb0c06b37befafd8dff640d3b89f61f58ccb716b72ea04877a`.

## Exact reviewed sources

All paths below are beneath `software/v5/terminal_i/` in the canonical root.
The predecessor map is the exact 114-entry `distribution-validation-01-input`
(`d11abac9...`); origin input `2ea83228...` changes two disjoint admission files,
not these five predecessors. Reviewed all five diffs and the complete new
packet/custody/transport/staged files, plus affected facade and inherited
admission, live-warrant, import, action-failure and transport paths.

| Path | SHA-256 |
|---|---|
| `evidence_network/packet.py` | `cf8aaa6190d46c4b41792cb54da7da5983d19450cafb65920af2a188afbbcefd` |
| `evidence_network/custody.py` | `c039af086cf73d57191187e9d5b02292c5c9b8a3fb455d67dc719ad8f7d183a0` |
| `evidence_network/transport.py` | `7ac7204b6e97b48eb1764c92b98437ad87e45f0fc62aa78973f5985816d63827` |
| `client/workspace_evidence.py` | `8531ee14e24d60617491b9f00e14ea1f7c410a279d116322489fe763a421ea68` |
| `client/workspace_staged.py` | `ae3dc1a743a0cf4bd2da7f388ed46d6f75f73330802b9263a03a54a230fafd2b` |

## Binding and compatibility checks

The new I packet is an explicit tag with exactly journal and receipt fields.
Canonical JSON, exact byte-array element types, 184-byte journal, adopted
relation/foundation/policy/nonempty-group profile, rank and receipt/packet caps
remain mandatory. The parser returns inert facts, not authority. Existing
`terminal` continues to mean A membership; mixed grammar is not relaxed.

Default `public_profile(image)` still constructs the exact V1 fields and
proof-form value. Explicit `terminal_i=True` chooses a closed V2 with its own
profile ID and I-schema commitment. Unknown/crossed versions or extra fields
fail exact profile comparison. V1 inspection and packing reject terminal-I;
installing a parser alone does not widen a V1 store. Fresh-store immutable
configuration prevents silent V1-to-V2 migration.

The required `verify_offer(..., profile=...)` keyword is the root-approved API
change; it verifies both selected request profile ID and its corresponding
proof form. Source search across the exact selected SDK establishes that the
two evidence-function callers are `PacketStore.offer` and
`EvidenceAcquisition.offers`; both are updated. Other same-named functions are
separate delta/frontier/mixed/receipt module APIs, not missed callers. Old
two-argument external helper callers require adaptation; V1 wire bytes and
default meaning remain compatible, not that Python helper signature.

Facade construction snapshots the validated profile ID, and `_active` ties
configuration, original ID, exact store and acquisition profile together.
`resolve` passes that chosen profile instead of reconstructing V1. Existing
loaded-source origins and required source pins still cover the modified
modules; new parser/packer imported symbols join the identity guards.

## Mathematical authority and lifecycle

The I branch invokes the existing inherited `admit_receipt` implementation.
That path checks the presence of the original I owner, retains existing byte
and worker reservations, uses actual receipt verification on a miss and
revalidates the same-client live handle on a receipt-cache hit. It does not
invoke A verification/membership or native-delta checking for terminal-I.
The facade still requires its real configured A owner for broader operations;
no independently deployable I-only runtime is claimed.

After either admission route, `_admit_evidence` obtains a fresh live fact and
requires kind I, exact receipt bytes/digest, original I profile, exact journal
and selected summary. In particular the common live-J comparison is
**unconditional**, preceding return and packet-cache insertion. Thus a genuine
receipt for `J_r` paired with the same-summary `J_(r+1)` fails even without an
optional caller expectation and even after a same-live receipt-cache hit.
The outer public `_action`/`_async_action` catches that failure and clears
warrants/caches and closes original owners. Its internally minted token cannot
escape via a successful public return. No new bypassing catch was introduced.

Conditionally on the unchanged real verifier and checking interpretation:
`Verify_I(receipt) => Valid(J_live)` and the new boundary establishes
`J_live = J_packet`. Existing authenticated group/body and sealed-import checks
then bind actually used mathematics to this exact journal. A certificate does
not attest provenance of separately supplied source or proof bytes.

Direct acquisition and staged admission dispatch I group openings to the real
I owner. Staging has a singleton inert journal inventory, keeps its one-use
transition, and performs final packet/group/member readback. Existing generic
reader and import selection dispatch I through `use_legacy_handle`; neither
is replaced. Missing transparent-definition/recursor semantics remain explicit
demands. No ancestor proof witness is added to the import requirement.

Export checks the original live warrant before packing and again before return.
Publication reuses durable terminal group/body/packet readback and existing
quota/partial-outcome handling, with `mathematical_acceptance=False`. Releasing
public bytes is not releasing a transferable live authority token. Existing
withdrawal, source checks, finite accounting and cleanup remain necessary.

## Next decision

The source implements the selected narrow connection from existing direct-I
certificates to ordinary discovery, custody, staging, admission and reuse.
It does not produce cheaper certificates, prove net useful growth, establish
successful installed circulation, or close final-v5 obligations.

Review the single focused control set when stable: strict forms/profiles,
fresh/cache rank substitution, actual facade/staged dispatch with explicitly
inert issuer fixtures, readback and failure revocation. Reuse unchanged lower
layers rather than repeating their campaigns. The live origin distribution
outcome remains the immediate operational audit priority. Root selects any
later finite controls or real same-facade workload separately.
