# Caller-directed semantic reader: independent source review

Reviewer: `core_release`, canonical project root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Selection: `SEMANTIC-READER-SELECTION.md`.

The preceding installed repair is complete in
`INSTALLED-REPAIR-REVIEW.md`; its used sources, installation and actual
results remain frozen. This review covers the new source and root's saved
controls02 output. The reviewer has not run a semantic-reader test, installed
call, proof or source-mapping change.

## Current disposition

The helper's proposed authority and lifetime boundaries are consistent with
the selected contract. Source review found an important **integration gap**
in the inherited staging API, described below. Root has now selected a
narrow staging-member successor in source, before any predictably ineligible
experiment. The unchanged original mixed packet, not manufactured standalone
evidence, must supply the eventual live warrants.

The final helper, staging-member successor, documentation and 16-group controls
passed independent source review. Root then selected controls02 once; its
actual saved outcome now passes this independent audit. All 16 groups passed
with exact original/snapshot pins and clean closure in 1.1875 known CPU seconds.
This is acceptance of the changed pure/inert boundary, not ordinary actual use,
product adoption or final v5 readiness. No repeat is required.

## Architecture and trust boundary

`SemanticReader` is an optional local strategy borrowing an exact live
validated client and its original grant. It creates neither a new grant nor
a new mathematical verifier. The caller chooses the initial candidate,
every offered packet variant, which returned demand to satisfy, and
per-packet admission limits. No global agenda, solver, provider search,
contact refresh, retry or trust downgrade is introduced.

The selected public sequence is:

1. Explicitly stage a selected offered packet and its selected group.
2. Preview the current structural closure.
3. Resolve caller-selected exact declaration demands; explicitly select a
   demanded internal member journal from a staged packet, stage another
   supported packet when needed, or fetch explicitly demanded committed
   computation bodies.
4. Repeat within the original grant and helper bounds.
5. After the latest preview is structurally ready, consume the selected
   one-shot admissions and call the unchanged live import.

Preview yields only status, demands, cost and an explicit nonacceptance
marker. It never yields an authoring context. Only `finish` can return the
opaque context from a successful actual `import_context`. A later failure
does not return success merely because earlier modules were admitted.

## Source-level checks completed so far

The reviewer read the new helper and the actual inherited implementations
of staged packet acquisition, staged description, preview, exact-name/body
acquisition, admission and live import.

- Constructor checks the exact validated-client type, retains the original
  grant object, verifies a finite caller-selected bound set, and restricts
  selected modules to original `max_members` and data to original `data_bytes`.
  Selected packet roots separately obey original `max_sources`.
- Each changing call is serialized, consumes a finite helper step and
  checks the original live client before and after. Any failure marks the
  helper failed; its `close` discards helper state without taking ownership
  of the caller's client.
- Candidate metadata is stored as immutable canonical bytes. Later use
  obtains the current same-client candidate description and compares its
  exact encoding. Candidate addresses use module identity and canonical
  relative-name identity.
- Stage uses the exact caller-specified offered packet. The returned token,
  candidate, provider, target summary, selected packet identity and
  journal are rebound. A second packet variant for a selected packet root is
  refused; an identical repeat yields explicit no progress. The complete
  member inventory is bounded, canonicalized and charged before retention.
  Each inventory row's exact journal binds its module and summary; the root
  must occur in the inventory.
- Explicit member choice is limited to a current demanded module in a held
  packet's inventory. Exactly one journal is chosen per module. An identical
  selection returns no progress, while a conflicting journal refuses. Packet
  roots and selected mathematical modules are separate maps.
- Exact groups are keyed by module/index and canonical bytes; conflicting
  groups are refused. Bodies are keyed by module/universe-arity/digest and
  checked against the exact returned commitment and expression hash.
- Only demands from the latest held preview may be fulfilled. Exact
  addresses are deduplicated. A repeated already-held result explicitly
  returns no progress and still consumes a bounded step.
- Metadata, canonical values and pending demands have finite byte bounds.
  The underlying grant continues to charge network, repeated preview,
  import and validation work. The helper does not claim global-size-
  independent total computation or free repeated previews.
- `finish` requires a structurally ready preview at the current revision
  and exactly one caller-provided admission-limit choice per selected packet
  root. It changes state before admission and never retries consumed tokens.
  Each packet is admitted once in sorted root order. Its actual live root
  and complete member inventory must agree with the staged selection.
  Selected journals, not synthetic standalone warrants, reach unchanged live
  import. Explicit per-root representation maps are passed through; the
  unchanged importer rejects missing and unused resolutions.
- The result of live import must be genuinely ready before its context is
  returned. A missing-semantic result has no returned context. Unexpected
  status or any failure is terminal for this helper.
- Reports are explicitly inert; a report cannot restore live authority.

This analysis relies on the already trusted owner-controlled runtime and
exact validated client, not on Python objects being secure against a local
adversary. The helper is an orchestration layer, not a new acceptance rule.

## Important inherited staging precondition

`workspace_staged.preview_context` currently supplies one selected target
journal per staged token to `semantic_staging.preview`. It does not expose
all structurally described member journals inside a mixed packet.

In contrast, actual mixed admission may warrant multiple modules through
one packet: for example, a native extension plus its I-certified base.
A missing semantic dependency can therefore be warranted inside an already
selected packet without having a separate supported target packet offer.
The preview may still ask for `NeedModuleEvidence` for that dependency.

`stage_packet` supports terminal and mixed target packets only. It cannot
stage a naked I receipt as a target. The new helper correctly does not
invent such a transition, switch A to I or fabricate a staged token. It can
therefore complete only when each demanded module has an explicitly
available supported target packet, under this inherited preview contract.

This is relevant to the retained actual contributor: its output and input
mixed packets contain the base as an I frontier, while no standalone base
terminal/mixed offer has been established. An actual integration that merely
serves this output cannot be assumed eligible. Lack of an offer is an
honest bounded incomplete outcome, not global nonexistence or evidence that
the mathematics is false.

The author confirmed this limitation and is documenting it. Root was
notified before any new integration experiment.

### Selected principled extension, not yet runtime-qualified

The gap is structural, not a need for a new proof. Root selected
`software/v5/staging_members/workspace_staged.py`, installed under the existing
logical key `client/workspace_staged.py`, while preserving the predecessor.
It extracts all relevant member journals from each held mixed packet for
**untrusted preview only**, binds those records to the held packet and exact
same-client staging token, then admits the original packet once and uses the
unchanged live mixed warrant for actual import.

Initial successor-source findings:

- `_structural_members` uses the unchanged bounded mixed-packet parser. Its
  inventory is the exact frontier journals plus the existing expected-journal
  function applied to every parsed delta witness. This is the same set used by
  `MixedImportSession.use_delta_handle`, whose live path independently checks
  the complete inventory and each evidence representation.
- The parser already enforces packet/node/depth/claim/frontier/witness/graph
  bounds, exact frontier/delta uniqueness, known preceding parents, rank and
  target closure. The successor additionally bounds the member count by the
  original import grant and requires the selected target in the inventory.
- Terminal evidence exposes only its selected member. The implementation
  does not open or infer undisclosed aggregate membership.
- Staging caches the canonical inventory within the existing bounded
  snapshot. `_read_stage` recomputes and compares it from held packet bytes,
  alongside the existing exact hash, target, group and summary checks.
  `admit_staged` retains that readback both before and after unchanged real
  admission.
- `preview_context(selected_members=...)` accepts only an exact same-client
  staged token, module and journal already present in its bounded inventory.
  It rejects duplicate module selections, including competing journals for
  one module. The default target-only preview remains compatible.
- Selection confers no trust. Actual import still checks that every selected
  journal exists in the live owner inventory; the original import handles
  exact-representation conflicts through explicit `existing`/`incoming`
  resolutions and rejects missing or unused resolutions.

The final helper keeps packet roots and selected modules separate, admits each
packet once, verifies its admitted live member inventory, and passes the caller's
selected journals to unchanged import. The full successor/predecessor source
diff contains only the new imports, inventory helpers, cached inventory,
readback comparison and optional preview subset; original admission logic is
unchanged except that its existing readback now performs the stronger check.
Direct pure boundary controls supplement helper-only mocks without replaying
the predecessor campaign.

### Why the extension does not add an acceptance axiom

Let `P` be exact held packet bytes, `U(P)` the bounded parsed member inventory,
and `V(P)` the member inventory of its eventual same-live admitted warrant.
Structural selection checks only `J in U(P)`. This statement is not mathematical
acceptance: the parser deliberately accepts some invalid mathematics.

The existing live import independently reconstructs the whole packet inventory
and requires exact agreement with the real owner's inventory and evidence
representations. Only that unchanged live path establishes `J in V(P)`.
Therefore an incorrect or stale preview can cause a failed, charged operation
but cannot replace a missing certificate or native check. Pre/post packet and
inventory rebinding prevents the helper from treating two held byte strings as
one selected packet. This argument is conditional on the existing checker,
cryptographic and trusted-runtime assumptions; it does not prove those layers.

The useful improvement is eliminating an unnecessary **separate target packet**
requirement for a module whose actual evidence is already inside `P`. It is not
a compression proof, aggregate-certification success or global-search claim.

## Inert-control selector review

Root's `Select-SemanticReaderChecks.ps1` at SHA-256
`40fa4b5599e624914cd249b97cfb7e8238c9944a7cad5072078a390517c59f58`
was read together with its retained runner. It verifies the exact existing
direct-contact source/runtime selection, omits the previous test invocation,
adds only two frozen fixture-constructor files and the exact new helper,
staging successor and controls. It refuses source-key collisions, malformed
or mismatching expected hashes, existing selection and existing run directory.
It creates one new plan with exclusive `CreateNew`; it does not execute it.

The prospective limits are 20 CPU seconds, 60 wall seconds, 128 MiB, two active
processes, and bounded stdout/stderr. The unchanged runner snapshots/pins the
selected sources, uses isolated/no-site/no-bytecode Python under the existing
Job supervisor, and verifies runtime/snapshot identity after closure. This is
local inert-test containment, not a hostile-source sandbox. At selector review
time root had not selected execution; the later controls02 outcome is below.
Final test source explicitly loads the new staging successor before importing
the helper; a copied predecessor in the retained closure is not evidence that
the successor ran.

## Remaining integration boundary

- Any later ordinary integration has its own changed-boundary selection and
  must run the new overlay under the logical selected source key. It must use
  actual live admission and import, not the inert fixtures.

Genuine aggregate-certificate economics, full-cost useful growth and final
public-deployment/security obligations remain open.

## Final source identities and control scope

| Source | SHA-256 |
|---|---|
| `software/v5/client/semantic_reader.py` | `175de65f72f056681237387c854d21671d7b3787b61f6685789a382b8a06ae18` |
| `software/v5/staging_members/workspace_staged.py` | `1a0922c395eb233f6fb4f1e8b10b5c538d69d445c732a9ae492539b568877f8d` |
| `software/v5/client/test_semantic_reader.py` | `f194dc9196b60aa91ff06d6a5009ae481f0b0cf982fa020737f8e21efca4190a` |
| `software/v5/client/SEMANTIC-READER.md` | `4e608a48265eb9770ba04fb9e88c84d99228d018bf146d393b5f44fb1612afe8` |

The initial control identity `1d5618b2...` was superseded before execution by
one additional exact I-frontier structural case in the existing inventory
test. Root caught the source drift after generating selection01 and before
any snapshot/runtime. Preserve that plan unexecuted; selection02 is a fresh
name/test-pin-only successor. The added case replaces synthetic claim tag,
statement and member opening fields consistently for the I parser branch
and expects the same inventory; it does not assert that the synthetic receipt
is a genuine I proof.

The controls explicitly install the fresh staging source as
`client.workspace_staged` before helper import and include the retained
portable-runtime import path. Three groups exercise the actual pure member
inventory, explicit subset and cached-inventory readback against inert held
stores. They check both I and A opened-frontier plus delta membership, exclusion of
unopened aggregate members, terminal-only membership, member bounds,
foreign/forged/duplicate selections, and changed cached inventory.

Thirteen helper groups cover arbitrary third modules; three selected modules
from one packet with no internal standalone offers and exactly one admission;
nonheld, undemanded, competing and over-cap member choices; actual-described
inventory mismatch before import; explicit packet variants; address
deduplication; unsolicited demands; caps/no progress; candidate conflicts;
original grant/deadline; nonauthoritative preview; one-shot partial failure;
and incomplete live-import behavior.

The helper facade, transport, semantic walk, admissions and final importer are
inert. The representation-map assertion tests exact pass-through only; its
synthetic unused map would be rejected by the actual importer. This deliberate
mock does not qualify real overlap-conflict acceptance. No fixture constructor
creates real authority, no previous suite is run, and no new source review is
a claim of cryptographic verification, measured growth or final v5 readiness.

## Actual controls02 outcome audit

Root selected and executed plan
`92f8d72766a25283be2e5dd8bc43b1aac509ddcf7bf51e08d9c3e5273b66e335`
once at `experiments/v5-local-checks/semantic-reader-controls-02`.
Independent read-only review found:

- The exact 01-to-02 map changes only `name` and the test source pin described
  above. Both maps have the same 88 source keys, no added or removed key,
  unchanged runtime pins, argv and limits. There is no controls01 run folder.
- All 88 original source files and all 88 snapshot files independently hash
  to the selected source map. All 19 runtime pins also match. The snapshot has
  exactly 88 files. Saved run selection and selected plan have the same
  SHA-256 above.
- The raw test transcript names all three structural and thirteen helper
  groups; every group is `ok`, with no failures, errors or skips. `controls.json`
  reports 16 tests, PASS, zero native/proof/network calls, and the exact five
  helper/overlay/fixture/test hashes. Eight inert admissions and three inert
  imports are explicitly synthetic, not mathematical verification.
- The actual command used selected isolated Python with `-I -S -B`, the
  snapshot test path and the fresh output under the canonical root. Child
  exit is zero; the direct child was reaped; final active-process count is
  zero; Job closed; no termination request or cleanup error.
- Job CPU was 0.84375 seconds plus 0.34375 wrapper CPU, totaling 1.1875 known
  CPU seconds. Whole wrapper wall was 2.419338599778712 seconds. Peak Job
  private commit was 32,071,680 bytes. Original limits were 20 CPU seconds,
  60 wall seconds and 128 MiB; no increased allowance or unchanged rerun was
  used.

| Saved evidence | SHA-256 |
|---|---|
| `RESULT.json` | `786eb6c5e72561188913d1777f8b284f519d913b8ee9c2cf8bbbce9462368a03` |
| `controls.json` | `276f8e56d5c95c5077b9ec0c1754d10ab30218632c391411e6596c7a0b250a7f` |
| `command/stderr.txt` | `0fb22c8ba91c064a1007ddd603c8918bbedab58ac4396975f1f468d9216d676a` |

Disposition: PASS for the selected staged-member structural boundary and
inert helper composition. Used sources and evidence are now frozen. This
does not exercise the real semantic walker, actual receipt/native admission,
actual overlap-conflict import or a new ordinary installed workflow. It
justifies proceeding to root's next source-backed integration decision,
not relabeling these mocks as the unchanged broader v5 goal.
