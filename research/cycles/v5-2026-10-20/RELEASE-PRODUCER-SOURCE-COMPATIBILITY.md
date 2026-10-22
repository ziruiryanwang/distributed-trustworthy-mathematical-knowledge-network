# Release producer versus current distribution: source compatibility

2026-10-22; independent source-only audit by `storage_outcome_audit`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
No product import, constructor, test, host, proof or packaging operation was run.
No installation, used source or live proof evidence was changed or inspected.

## Decision-relevant result

Do not overlay the retained producer closure blindly on the current distribution.
Among its 29 command-source files, **16 shared files are byte-identical, 12 are
new logical names, and one shared name has materially different bytes**:
`v5/admission/verifier.py`. The retained producer set contains an older verifier;
the current distribution contains the successor with explicit trust withdrawal
and controlled nonacceptance. Replacing it would regress the receiver and break
its constructor contract.

The correct unique-name union is **130 + 12 = 142**, not 141. The helper
`v5/aggregate_small/operator.py` is required independently of the 27 core source
roles and the new entry. Current distribution source `body_location/distribution.py`
also rejects more than **141** SDK rows at both assembly and validation. Thus a
plain union has two concrete blockers before any expensive operation: the
verifier selection conflict and the source-count bound.

Retaining the current verifier appears compatible with the producer's operations
by source inspection: the producer never constructs or invokes `ReceiptVerifier`.
It imports that class indirectly through the two delta package initializers.
But its current verifier imports three additional modules. A unified producer
must pin and origin-check those before product imports; merely replacing the
verifier pin in a 27-role profile is insufficient to retain the stated complete
pre-import source-boundary guarantee.

## Exact compared inputs and method

| Input | SHA-256 |
|---|---|
| `experiments/v5-local-checks/distribution-candidate-preflight-01-input.json` | `25e7c849e41f394498e21a60cc7800ecffb67b0cee1b3911d7164977ce4f2364` |
| `experiments/v5-local-checks/typed-production-controls-01-profile.json` | `1242b0a8430e68032bbedbddcb3c6539fbdc95a2a5cf567936545c5f891246cc` |
| Current `software/v5/body_location/distribution.py` | `eb1348f6917e958e2ef233537e2e22986f18da545f56df1283fd7a74bc41c813` |

The current installation is
`product-local/v5-distribution-candidate-preflight-01/Mathematical Commons v5`.
Its authoritative source selection is the first input above, not a recursive
scan of `software/` or a predecessor distribution.

I compared the profile's 29 source rows minus its five `typed_production` rows
(lifecycle24), plus the three release core files, root's release entry, and the
required `aggregate_small/operator.py` helper. Logical map keys are normalized
to `v5/` plus the path after `software/v5/`. These map keys matter: an initial
unprefixed lookup reported everything as absent and was discarded, not adopted.

Read-only small-file size/SHA-256 checks matched all 24 retained source rows,
all 17 corresponding current source rows, the four new release sources and the
operator helper. The three additional current verifier imports were checked
against their exact current map rows too. A text `git diff --no-index` establishes
the sole shared-name semantic delta below. No Python code was imported or run.
This is not a new whole-installation integrity or runtime qualification claim.

## Complete name comparison

### Sole conflicting shared name

| Logical name | Current130 bytes / SHA-256 | Retained producer bytes / SHA-256 |
|---|---|---|
| `v5/admission/verifier.py` | 17,835 / `ec6474cdd0580df89f9c646a41c0d909ec20e83da0a42274e0510a6e01bbbaea` | 12,381 / `9f77bd17abbf87d8f777c52c047d41cfbfd1b29078f29a173006ccad99839571` |

The current physical source is
`software/v5/candidate_admission/admission/verifier.py`.
The retained source is under
`experiments/v5-local-checks/typed-production-controls-01/sources/software/v5/admission/verifier.py`.
These are intentionally different source versions, not a path-only mismatch.

### Twelve additions

All names below are prefixed `v5/` in the distribution map.

| Name below `v5/` | Bytes | SHA-256 |
|---|---:|---|
| `aggregate_lifecycle/__init__.py` | 152 | `a159ba3ed681f7b8da374af2ce8698be68a67a5d7e4a92a3190c2a228a2f7833` |
| `aggregate_lifecycle/producer.py` | 8,724 | `a249bc3505a28aadff20d81e4ce30b43e03fbf5d9d6de45277c81a4c340833f4` |
| `aggregate_lifecycle/snapshot.py` | 22,628 | `8c65e623419f846c2b7607716ce7fdec8a611ae2bb340e9a9cab18af3c741546` |
| `aggregate_small/__init__.py` | 156 | `8226f83b753a224b57d5ef35338e437665fab72849c8f060dd61574a043ff36f` |
| `aggregate_small/producer.py` | 52,625 | `a2d23bcfe0b798f747d4a59330655a865a14a73cb4d635a50332fa65c75a6985` |
| `aggregate_small/operator.py` | 11,480 | `8a4876c28b1da2fbf80b3e425aa0f05486aa760a9b77cfe6d2d6c0a66dcffac6` |
| `aggregate_claims/input.py` | 5,679 | `d40b611e288fd73a060df021809e403f80b1e6c16ca8b81ff2fd528d1f2fe61f` |
| `aggregate_claims/prepare_mixed.py` | 7,502 | `2d03b635553eaffa406fba57011bf3bd346ec23fd59e0092b29d9442a95802ff` |
| `release_production/__init__.py` | 169 | `56653258ec5e2b9e8d6abffa55e4f889b979daae05c81282a36cf65453b60717` |
| `release_production/producer.py` | 7,617 | `4396de095caf214559674e0fdd5188fcc52d10c3e4c8fe32e1d5b63259f397ce` |
| `release_production/adoption.py` | 10,675 | `62255a98879ed7162eb1a3414c937a29a70258b7396ae070d32fac1253ec5710` |
| `release_production/operator.py` | 22,924 | `d1c5507f00f33df0eb0732e09113e389387e122c6786c460a42e7553695e2287` |

### Sixteen byte-identical shared names

These need no replacement. The retained profile and current130 map agree in
both byte length and SHA-256 for each name:

- `v5/production/__init__.py`
- `v5/production/producer.py`
- `v5/aggregate_claims/__init__.py`
- `v5/aggregate_claims/bindings.py`
- `v5/mixed_claims/__init__.py`
- `v5/mixed_claims/packet.py`
- `v5/delta/__init__.py`
- `v5/delta/packet.py`
- `v5/delta/receiver.py`
- `v5/delta_claims/__init__.py`
- `v5/delta_claims/claims.py`
- `v5/delta_claims/receiver.py`
- `v5/admission/__init__.py`
- `v5/admission/bindings.py`
- `v5/modules/__init__.py`
- `v5/modules/codec.py`

## Exact semantic risks of the verifier conflict

The current verifier changes the retained version in the following relevant ways:

1. `ReceiptVerifier.__init__` requires a `trust_binding`. It binds the original
   local trust domain and identity, verifies `admission.trust`'s loaded origin,
   and includes the trust identity in the operational profile identity. The
   old constructor does not accept that keyword. Current callers are therefore
   not backward compatible with the old class.
2. `_active` verifies the original binding/module/domain and current trust
   adoption on every authority-bearing use. Any failure revokes the owner and
   clears handles. `_revoke` works while receive is busy; `close` delegates to it.
   `describe` performs a final activity check before returning authority data.
   Replacing this code removes the current withdrawal/fail-stop contract.
3. The constructor requires exact pinned `pin_phase`, `trust` and `clean_refusal`
   sources. `_check_install` checks the phase/refusal origins and uses the bounded
   phase pin checker; `_fresh_install_check` creates a new post-subprocess phase.
4. `receive` preserves strict raising semantics and dispatches to `_receive`.
   The separate `try_receive` permits only the validated clean exit1 route to
   return `None`; other failures revoke the owner. That route checks command,
   cwd, limits, resource/closure report, bounded output census, unchanged receipt,
   fresh installation pins, activity and deadline before returning nonacceptance.
   Success on the optional route also has final census/fresh-pin guards. The old
   verifier has no `try_receive` method.

This is not a change to the receipt's mathematical journal format or adopted
native verifier binary. It is nevertheless a material authority/lifecycle and
API change, and cannot be erased because the older class is only incidental to
the producer's parsing path.

## Can the current verifier serve the producer?

**Source-level answer: probably yes for the selected producer actions, with an
explicit expanded source closure; not yet an executed integration result.**

`aggregate_lifecycle.producer` imports pure mixed-seal preparation. That imports
`delta.packet` and `delta_claims.claims`, whose package `__init__` files eagerly
import their receiver classes. Those receiver modules import `ReceiptVerifier`
for later exact-type checks. No selected producer method constructs a receipt
verifier, passes its constructor parameters or calls `receive`/`try_receive`.
`prepare_mixed_seal` explicitly returns unverified parent receipt candidates;
the actual native/guest relation checks them in the unchanged proof path.

The current verifier's import adds the following source dependencies, all
already present in current130:

| Logical name | Bytes | SHA-256 |
|---|---:|---|
| `v5/admission/pin_phase.py` | 8,677 | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` |
| `v5/admission/trust.py` | 13,774 | `c997d2a83ae5246dec9ff30eeca72e405ec0f66c0a307e53e0521eef66fae6d0` |
| `v5/admission/clean_refusal.py` | 6,462 | `7c1386cce693185ac7d6e1dda149993c892ac5b2d417242fb7e02b873648e5a7` |

`pin_phase` additionally imports `trust`; `trust` uses the already-selected
`modules.codec`; `clean_refusal` has only standard-library imports. There are
no further project-module imports in these three sources. Their top-level code
does not construct a trust domain or receipt verifier.

The existing release entry prechecks only its 27 declared core files, the helper
and its installed self, then imports product modules. Its runtime map may contain
more files, but that does not prevalidate their bytes or check their module origins
before execution. Keeping `PRODUCER_MODULES` at27 with the current verifier would
therefore leave the three new imports outside this explicit boundary.

## Minimum alternatives before integration

### Unified SDK, preserve all current receiver sources

This is the smaller source-reuse change if one shared SDK remains desired:

- Keep all 130 current map rows, especially verifier `ec6474cd`; add the twelve
  new logical names. Do not replace the sixteen identical rows or downgrade any
  current receiver/trust helper.
- Select fresh successors of release adoption and entry if the current files
  have already been used. Extend their matching declared core closure from27
  to30 with the three exact current verifier dependencies. All three must be
  checked before imports, included in descriptor/profile/runtime pins, and have
  loaded origins checked afterward.
- The release producer obtains its `SOURCE_MODULES` dynamically from adoption;
  the generic lifecycle's inherited source-origin check still checks its original
  24 subset. No generic lifecycle/scheduler or mathematical relation edit is
  apparent from this source analysis. Predicted repeated-rebind union is56+3=59,
  still within the new64 bound; this count is not an execution claim.
- A fresh distribution successor must explicitly accommodate142 SDK rows in
  both `build` and `validate` bounds. Current source rejects them at lines698
  and818. Do not silently remove a required module merely to fit141.
- Assembly must separately add exact runtime-artifact/descriptor/profile roles
  and a genuine public launch-evidence adapter. The 142 source-name calculation
  is not a complete distribution design or an assertion that existing launch
  behavior already supports production.

The complete current receiver set then remains byte-identical. Relative to the
retained producer proposal, the verifier pin is updated and three helpers enter
its closure. Fresh focused pre-import/origin and constructor controls can test
that changed integration boundary without another proof or repeated host build.
Any such runtime remains root-selected, not authorized by this audit.

### Role-scoped isolated producer process

This can preserve the already reviewed 27-role producer closure while preventing
its historical verifier from entering the reader process. It needs a deliberate
packaging contract, not merely a new `sys.path` entry:

- `release_production.producer` requires its source root to equal
  `adopted.root / "sdk/v5"`; adoption maps source roles to that same relative path.
  A role prefix under the main SDK does not satisfy this unmodified contract.
- A separately adopted component root could contain its own `sdk/v5` and V3
  file-map container, or a selected constructor/adoption successor could expose
  a pinned role root. The former's subset V3 container is **not** automatically
  a valid full distribution under the normal validator.
- Namespace/process isolation must be explicit: never import both verifier
  classes into the same `admission` module namespace, silently reuse preloaded
  modules or supply producer proof candidates as receiver authority.
- Whole-release immutability/output exclusion must remain protected. If the
  producer's `_install` becomes a nested role root, inherited exclusion protects
  only that component; the outer launcher must additionally reject output under
  any sibling immutable payload of the full public installation.
- Both component identity and outer release mapping must be validated by the
  real public launcher. The installed launch evidence grammar remains distinct
  from historical local-check records; do not forge old PASS records.

The independent public-launch designer is evaluating this alternative. The
source audit does not select a winner or edit either role. Both options preserve
the ongoing proof and its old profile; neither permits migrating that allowance.

## Scope and stop condition

The exact divergent name, its semantic consequences, complete additions and
required import closure are identified. Root and the public-launch designer
were informed before integration. No broad test campaign is needed to discover
these deterministic blockers. Root should first select one explicit packaging
and launch contract, then only the smallest changed-boundary checks needed to
validate it. This note does not establish full-v5 completion, mathematical
acceptance, release security or compatibility of an unbuilt successor.
