# Tentative v3: scalable verification, experimental receiver

Checkpoint: **28 September 2026, 02:43 Chicago (07:43 UTC)**.
This delivers a runnable experimental certificate receiver and a more precise
scale-first architecture. It does **not** complete the decentralized certified
contribution loop or the broader mathematical-commons goal. Native v2 remains
unchanged. Licensing is undecided; nothing has been published or deployed
externally.

## What changed at the core

A receiver should not need the proof histories of the lemmas it uses. The new
boundary is an exact theorem interface plus a certificate of checking, under
an independently adopted mathematical foundation and verifier. A contributor
checks its new proof against certified immediate premises. Recursive proof
composition must discharge those premises before another receiver accepts the
new certificate. Neither popularity, author identity nor a peer's PASS record
substitutes for that check.

This is not just a paper design: one real base-lemma certificate was produced,
and the packaged receiver verified it after extraction. Four genuine seal or
claim-binding corruptions were rejected. The fresh receiver takes no ancestor
proof bodies, Lean runtime, guest-image file or global theorem ledger.

The first actual ordinary-source child uses the parent interface twice. Its
conditional Lean check and its guest execution have passed, but **its final
recursive certificate is still being produced at this checkpoint**. It has
31 proof segments and one actual premise assumption. Snapshot/checkpoint files
are not certificates; the running experiment cannot be counted as a pass.

## Try the receiver

- [Receiver ZIP](../../product-local/certified-verifier-package-01/mathematical-commons-v3-receiver.zip):
  56,577,912 bytes, including a copied Python runtime and verifier.
- [Real L sample bundle ZIP](lemma-L-bundle.zip): 223,898 bytes; exactly four
  bundle files at the archive root. This is a rank-zero example, not the child.
- [Windows instructions](RECEIVER-USAGE.md): checksum, extract and verify into
  a fresh output directory. No system Python or Lean installation is required
  for this receiver. This Windows-host result is not independent-host testing.

Receiver archive SHA-256:
`db862cc0c0b86a53d7f9e47c9c5c32ba4cc4406f805d1f08d6fb37b78b4f9ec4`.

Sample archive SHA-256:
`d6f2012e152b77e0e51ad189e156769c76ceddc9dd4604c4480fbbeac6f561f9`.

Adopt these values through a trusted handoff, not solely from the same
untrusted peer that supplies an archive. Keep installation and bundle files
unchanged. A successful local RESULT is evidence of that invocation, not a
portable replacement for the cryptographic receipt.

## Understand the design and its limits

Read [the layered architecture](SCALE-ARCHITECTURE.md) first, then
[measured results and remaining central work](RESULTS.md). The important
distinctions are validity, usable interfaces, availability and usefulness.
There is no mandatory global goal, unsolved-task list or human-intention rule
in mathematical acceptance. Search/ranking and agents' research strategy are
separate from verification.

The exact current profile is restricted to new proposition-valued theorems
over a fixed authenticated foundation. It is **not general Lean-library
support**. New definitions/inductive types, proof-sensitive reduction and
selective computational support remain central design/implementation work.
The experimental Nanoda checker is not proved equivalent to Lean's kernel;
production security for the exact recursive cryptographic profile remains
unestablished. The receiver deliberately reports `native_admission: false`.

The complete positive receiver command took about **2.15 seconds wall time**
and **1.375 CPU seconds** in the retained local sample. Its inner cryptographic
timer was 13 ms; that is not the whole receiver cost. Proof production was
expensive. No net certificate speedup, useful-growth advantage or exponential
growth is established.

## What happens next

The root-supervised child experiment has a fixed finite selection, retains
every completed stage, and does not retry or enlarge its budget automatically.
At the measured CPU proving rate it is expected to extend beyond the 03:00
tentative deadline. Its eventual outcome belongs in a new dated checkpoint,
not a rewrite of this checkpoint's pending status.

The next core gates are fully resolved child certification and fresh checking,
an installed ordinary-source contribution workflow, and affordable
whole-workflow costs under an explicit assurance profile. Political attribution
and additional coordination machinery are not substitutes for those gates.

Historical `DRAFT-*` files and the byte-preserved package `API.md`/`PLAN.md`
contain earlier pending/source-only wording. This dated handoff supersedes that
wording **only for the actual receiver capabilities listed above**. It does not
promote their unrun components. [The live research desk](../../research/NOW.md)
tracks later work; this milestone and its evidence stay preserved.
