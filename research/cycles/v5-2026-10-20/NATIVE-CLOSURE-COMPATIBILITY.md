# Base witness image binding: diagnosis and minimal correction

2026-10-20, `core_growth`. Source/data inspection only. No native rerun, test,
proof/build, installation, RAM study or Git mutation. Original used files and
the failed actual01 operation remain unchanged.

## Cause

Root reports that actual01 failed safely with native reason
`member fixed relation profile`, exit 2, and no tokens. Rehashed base fixture
`experiments/v5-local-checks/module-base-snapshot-03/evidence/profile2-request.json`
still has SHA-256
`ce554d4877e0b865690f565384381a188ce13166e960a55d39106159f46c067c`.
Its schema is V2, but its `image` is the **unbound placeholder**
`[0,0,0,0,0,0,0,0]`.

The fixed aggregate member profile requires image bytes
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
`aggregate_claims/header.rs:member_journal` rejects a zero-image journal.
`bounded_parse/module_relation.rs:check_bound` puts `input.image` into its
returned J. Thus raw V2 syntax alone does not make this fixture ready for the
fixed aggregate relation. The retained deltas/parents already use the fixed
image, as separately inspected by root.

**Selection oversight:** my earlier comparator note correctly distinguished V2
from the older V1 file, but did not inspect/adapt the placeholder image before
recommending the raw bytes. That omission explains the failed input selection;
it does not invalidate the zero-premise induction or justify relaxing the
checker's fixed-image check. No native/owner change is indicated by this failure.

## Why narrowly binding this input is principled

Complete source inspection of `bounded_parse/module_relation.rs` finds only
two uses of `input.image`: exact image agreement with parent journals, and the
image field of the returned J. Mathematical foundation/descriptor/body/row/
kernel checks do not depend on it. For this **rank-0, no-parent** base, changing
only its placeholder image therefore leaves all mathematical obligations
unchanged and selects the required conclusion namespace.

This is also the existing preparation convention:
`modules/receipt/src/bin/module_host.rs:prepare` reads an untrusted raw input,
computes the selected guest image ID, replaces `value["image"]`, canonically
serializes the input, and explicitly does **not** relabel parent journal bytes.
The native adapter need not execute that prover host merely to perform this
same inert preparation step. It must still call the unchanged real native
checker before acquiring any authority.

## Minimal successor adapter contract

Root may select a **fresh adapter/input**, not edit actual01 or the raw fixture:

1. Pin the exact raw base, packet and final requested J as before.
2. Parse and require exact V2 fields, image eight integer zeros, rank integer
   zero and an empty parent list. Reject any other profile rather than silently
   adapting arbitrary input.
3. Create a separate input value whose only changed field is `image`, populated
   by the eight little-endian 32-bit words of `B.RELATION_IMAGE`. Require all
   other parsed fields equal to the original; record original/derived hashes.
4. Reconstruct the expected base J from the unchanged summary/rank and fixed
   image. Require equality to the exact base frontier J and every base-parent
   occurrence in the packet, not just equality of ModuleID. This reconstruction
   is an expected statement, not mathematical verification.
5. Preserve both descendant witnesses, every parent J/opening and the exact
   final target J. Check the complete three-node DAG once through the unchanged
   native owner, under a separately selected finite successor operation.

This changes untrusted preparation bytes, **not** an accepted receipt, a saved
success, a prior operation, or the requested theorem. No certificate authority
is inferred from the metadata replacement. It does not allow parent/target
relabeling or failure recovery by broad profile substitution.

The actual outcome of that successor remains to be established. The failed run
and its resource charges must remain in the full accounting.
