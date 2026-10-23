# Independent explicit-abstract-authoring source review

2026-10-23. Reviewer: `admission_event_audit`. Source-only review; no compiler,
test, owner consumer, receiver, catalog operation or Git command was run.

**No blocking source finding for the explicitly selected construction mode.**
This implements the previously reviewed conditional interface argument without
weakening receiver acceptance. Actual construction and independent successor
checking remain separate gates.

## Reviewed exact sources

| File | SHA-256 |
|---|---|
| `software/v5/ordinary_lean/OwnerRebind.lean` | `63ffaac12ae23d5e21ddbee7857e08f2a3f6d01a950b87a4128f27ae48594cc3` |
| `software/v5/ordinary_lean/OwnerUseCommand.lean` | `cfeaaf28f48234de86000694c52a0350bd62f1120ae4bbd18d76ee5f42776313` |
| `software/v5/ordinary_lean/run_owner_consumer.py` | `c305914f5d71405c2aa7508f7801fb0753e63f63bddb493aed657e0b6ea0e716` |
| `research/cycles/v5-2026-10-22-native-library/Select-OwnerConsumer.ps1` | `3aa44cad7c69ce3a35940d0f32e3283e604928e02993ae4aa9ed23fd2e9ec8a0` |
| `software/v5/ordinary_lean/OwnerAbstractChecks.lean` | `bcea5b8fb94bf603b02c2ac7f13d1140bebb4aace04dcee68e6f39fa1567c0c4` |

The five files and `ABSTRACT-AUTHORING-IMPLEMENTATION-PLAN.md` were read
completely. Implementation checkpoint cut
`33c8ef48972c34333285cd589281db151fb60421e388561111c2948210b4173b`
was also read, including its later synthetic-control addition. The earlier
principle review and existing command/successor-export review retain their
separate scopes; this note does not retroactively qualify old failures.

## Boundary checks

- **Opt-in is explicit and local.** `DefinitionView.exact` remains the default
  of both `rebindPrepared` and `OwnerUse.run`; `#ordinary_use` selects no weaker
  behavior. Only separately spelled `#ordinary_use_abstract` supplies
  `.existingAbstract`. Request JSON cannot select this policy.
- **The new case is a restricted match, not an insertion.** An ordinary accepted
  row must have non-theorem mode and kind 1 or 3; the actual existing owner record
  must be an axiom. `requireSafe` checks its name and unsafe/partial status. The
  ordinary branch compares exact ordered parameter encoding and type DAG; the
  fixed-basis branch compares its established normalized type/arity interface.
  Accepted exact identity still comes from authenticated controller bindings,
  never from matching a type or name alone.
- **Concrete disagreement still fails.** Concrete definitions/opaques bypass
  the new axiom branch and compare full existing inventories. A same-type,
  different-body concrete record has no abstract fallback. Generated records
  and quotient/foundation entries cannot enter the definition/opaque branch.
  Theorem matching and theorem-only payload classification remain distinct.
- **Classification survives use.** `MatchKind` is retained per name. Only
  theorem/abstract handles scan type alone; concrete bodies, recursor rules and
  group metadata retain their previous scans. The three counters partition all
  selected bindings. Final ordinary abstract targets must remain actual safe
  axiom-shaped frontend handles with the same interface. Fixed-basis target
  matching must return the original class. No abstract definition is reported
  as an exact semantics match or a theorem match.
- **Missing declarations still require construction checking.** The unchanged
  `CheckedExtension.checkBatch` path handles missing groups; no new axiom is
  manufactured or old record overwritten. Group shape, limits, dependency
  membership and prepared non-theorem body data remain. The only command-state
  installation is the final `modifyEnv`, after all fallible IO. Bound state
  remains local/nonpersistent plumbing and is not receiver authority.

The primitive qualification from `ABSTRACT-AUTHORING-REVIEW.md` is essential:
an axiom-shaped `Nat.xor` can still compute through the pinned kernel's native
name rule. Removing a delta body does not remove all computation. Sound
transport would require every available selected inference and primitive rule
to be preserved by the real receiver interpretation, not merely equality of
displayed types. The implementation claims no universal proved transport:
actual new declarations must still pass the unchanged independent receiver.

## Reuse driver and selector

The driver pins consumer02's successful preparation manifest
`09477faa163f9e2a6071d479552367650a41ac13218f70d66f8159740cb04d23`,
checks all 388 exact files and the 4,549,204-byte payload, copies the exact files
to a fresh request directory and rechecks both original and copy. It does not
rerun the basis projection or omit further required names. The generated source
uses the explicit abstract command and retains the original substantive consumer
body byte-for-byte after replacing its producer import. The source-map marker
records `existingAbstract` and no receiver policy change.

The selector requires the selected helper build's clean result bound to its
selection, carries its runtime pins, pins all actual helper build artifacts and
uses that newest build first in the helper path. It pins the adopted preparation
manifest, driver and unchanged consumer source. The existing 120 CPU / 150 wall /
1,536 MiB envelope remains. This is immutable protected local input selection,
not a defense against arbitrary concurrent local file mutation or a public
hostile-source sandbox.

## Focused synthetic checks

The 22 source controls exercise ordinary and distinct fixed-basis branches:
exact-default refusal, explicit definition/opaque handle success, wrong type or
universe refusal, different concrete body refusal, generated and unsafe stub
refusal, and separate theorem/exact classifications. Ordinary controls also
cover differing concrete opaque bodies and exact universe parameter names.
Each negative requires its intended marker, and each positive requires its
expected matching class. These are inert `ConstantInfo` fixtures, not inserted
axioms or real warrants. The final PASS text is conditional on actual successful
execution; source presence is not a passing outcome.

The controls do not by themselves establish native primitive correspondence,
real owner use, bound-context authentication or independent new proof acceptance.
Source arguments cover the unchanged authority seams; the next real consumer
and unchanged receiver should resolve the actual workflow question without
repeating successful old basis, projection or certificate work.

## Saved build/control evidence, read-only follow-up

Root subsequently supplied completed selected operations. This review read the
saved results, selections, compile reports and native logs, and rehashed every
selected snapshot source and runtime pin without mismatch. No rerun occurred.

| Operation | Selected cut | Actual outcome |
|---|---|---|
| `ordinary-abstract-helpers-01` | `32b37eeda8b11bff3a0b0c861fa47fe6557277a57187c4cf687cde72a84ddd1a` | Four selected modules compiled, all eight native logs empty, 20 artifacts retained. Zero exit, child reaped, Job closed, no termination/cleanup errors, zero active/terminated processes. Known Job plus wrapper CPU: 6.1875 seconds. |
| `ordinary-abstract-controls-01` | `e53c3a827439f04468bf8538f7e2fff20709ee187a6f8a215fb0ecf2e64e1f5b` | All 22 distinct expected PASS lines and final scoped summary present; native stderr empty, five artifacts retained. Same clean terminal predicates; known Job plus wrapper CPU: 1.5625 seconds. |

Helper RESULT is
`013dec47e9b9746899956225d58356cd1d8e2f24c6e5bc309c843be55489d4b5`;
its COMPILE-RESULT is
`049beedb4d063273915bc0ae1f30038dd840f18f711640672e66ecfeda6410ba`.
Control RESULT is
`79469525e6eaa0e86b28de83f843888c91c033e10410d77b784a38e63b3a213d`;
its COMPILE-RESULT is
`0a45fd84a6755ef1a9dfd187988957a308f10a6a4ca905e12d41e3d584d1335c`.

The actual selected control source is the reviewed `bcea5b8f...` cut. During
follow-up, the mutable source changed to `760435c0acef6641d569f9d08112bbbb285a5d623e7ba7724b71ea8200141f47`
with explicit local fixture bindings. The saved selected source and evidence
remain intact. This later unexecuted cut is not the source of the passing
outcome; root and author were notified. No repeated successful control run is
justified merely by that unused rewrite. Compilation and synthetic matching
still do not establish actual source-use or successor-admission success.

## Saved consumer03 refusal

The actual `ordinary-owner-consumer-03` operation selected
`6bce452229f01de0963c37bb24702cc8b7c6429473013ab6572543cc4642ad76`
finished with RESULT
`8be3230c880ac8fa24671bc162b9b078a0402c7f64399d3290ac8dd47b985ca0`.
Read-only saved inspection confirms the first failure:

```text
MISSING_FIXED_BASIS _private.Init.Prelude.0.isValidChar_UInt32
```

The explicit `existingAbstract` policy entered and matched the header's
316 basis rows / 387 groups / three targets, but failed in the basis loop before
group installation. This is not another type/abstract-match mismatch. Later
unknown `ReadsOnly` / `Avoids` / method errors and absence of bound context are
cascades, not independently selected failures. No owner `.olean`, successor
export or `CONSUMER-RESULT.json` exists.

All three selected snapshot sources, 69 runtime pins and 388 copied request
files match. The copied preparation manifest is exactly the adopted
`09477faa...` cut. The source map records explicit abstraction and no receiver
policy change. Child exit 1 was cleanly reaped and Job-closed, with no cleanup
errors/termination and zero active/terminated processes. Known Job plus wrapper
CPU is 5.359375 seconds; peak Job private commit is 902,135,808 bytes.

This preserved refusal identifies the next question: the request's prior exact
body closure may exceed what selected abstract authoring actually requires.
The existence of that possibility is not permission to omit this one private
name. A correct construction dependency rule must be specified and reviewed
across actual handle types, concrete computation, generated rules, literals
and newly checked units before any new request or runtime is selected. The
accepted receiver basis and final independent acceptance remain unchanged.
