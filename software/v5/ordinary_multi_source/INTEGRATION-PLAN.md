# Integrate multi-source receiving without invalidating checked mathematics

2026-10-26. Bounded source/identity analysis only. No new assembler, package,
archive, state migration, build, native check or execution is selected here.
The focused controls and their plan are unchanged. Root owns later selection.

## Decision

The smallest safe user-facing step is a **fresh file-only overlay of the current
exact-module package**, changing exactly three pure payloads. Keep its native
installation, owner, profile loader, module support and every other payload
byte-identical. Use the existing public launcher and an explicitly authored
receive config. Do not patch the bound old installation or rewrite old reports.

A new package PROFILE is necessary, but does **not by itself** require a fresh
owner, fresh inert custody, mathematical rechecking or new module realization.
For this exact three-file change, the source-derived checking, catalog, custody
and anchor-support bindings can all remain equal. That statement is conditional
on the exact map comparison and protected-state premises below; it is not an
executed package/state-reopen result.

There is one real operator-tool incompatibility: the current request preparer
pins the old interface and requires referenced parent/find reports to have its
current package PROFILE. Do not obtain a new-profile parent report by rerunning
initialization. The public raw-config route already avoids that unnecessary work.

## Current artifact actually inspected

Read-only SHA-256 checks match the adopted investigator distribution:

| Artifact | SHA-256 |
|---|---|
| `experiments/v5-local-checks/investigator-source-controls01/suite/packed/source.zip` (4,236,874 bytes) | `a757663ad564c382b55da98f5932efd26fe4c3d5e37e4561ef0127d31826fd28` |
| Relocated `INVESTIGATOR-SOURCE-MANIFEST.json` | `65edf28f928d4100346a4603fe508252ddc6393950c34a373fbb33da4c6491f5` |
| Packed external `RECEIPT.json` | `c81e36480f304a07683086627734a722fb0b991cc4362f6d1ce8d0ae54f2379a` |

Direct read-only ZIP inspection found 170 members, 4,207,452 uncompressed bytes,
the exact-module assembler and current manifest, and **zero multi-source files**.
The three selected ZIP entries were read and hashed directly, without extraction:

- Exact-module assembler: 12,326 bytes,
  `f7d5f3496d010c591a4de3872f47ff169c30413354c2576bf670b7b30c77a82b`.
- Investigator selector: 5,945 bytes,
  `72f27b6644f998a16b5fb3eb785d576a68d48338949b135cc4e96c18b8b89afc`.
- Investigator compatibility map: 10,728 bytes,
  `de4937bdcac4d9ed5550d4da9c59d4f4af4551275dcaaf9d36bc85affbddd1f0`.

This inspects the actual current archive, not a proposal or an arbitrary repository
tree. It does not repeat its full qualification campaign or promote the new
multi-source sources into the old manifest.

## The identities are different, intentionally

Let `P` be canonical package PROFILE bytes, `J` the native INSTALLATION bytes,
`Iraw = canonical(J.implementation)`, and `S` the portable semantic identity.

| Binding | Actual source rule | Consequence of the three-file overlay |
|---|---|---|
| Package selection | `ordinary_sparse_access/profile.py:156` verifies the approved SHA-256 of `P`, its complete payload pins and installation-manifest pin | `P` and its digest change. All subsequent commands must select the new actual profile. |
| Mathematical implementation | `ordinary_lean/ordinary_admission.py:85,158` validates support-group digests, role/search bindings and every installation/runtime pin; `ordinary_semantics.py:170` hashes `Iraw` under its implementation domain | `J`, its support groups, `Iraw` and implementation ID remain exact because none of the three files is in the native installation. |
| Local mathematical roots | `ordinary_semantics.py:210` hashes `[S, I, store_id, kind, parent, request_hash]` | No root acquires the outer package hash or path merely because the peer coordinator changed. Existing roots retain their identities. |
| Catalog adoption | `ordinary_lean/portable_catalog.py:143` constructs the marker from schema, store ID, implementation descriptor and persistent limits; `ordinary_admission.py:488` passes the unchanged implementation bytes | Reopen the same existing catalog with its original ID/limits. No migration or marker editing is needed. |
| Inert custody | `ordinary_authoring_offers/ordinary_acquisition.py:76` constructs stored config from schema, `S` and persistent limits | The successor leaves this store implementation/config unchanged. Reopen the same custody with the original limits; no new store or copied trust. |
| Local module anchors | `ordinary_exact_module/module_export.py:27` builds a narrow support descriptor; `anchor_store.py:763` hashes it and binds the existing catalog adoption/activation | Exact support equality is retained if the three-file footprint is respected. The full package PROFILE hash is deliberately not an input. |

The anchor descriptor's source roles are controller, collector, store, native,
worker, owner, profile, contribution, preview, owner_request, legacy_request,
candidate and ordinary_preview. It also binds native installation digest,
semantic/foundation/implementation identities, policy and 30 exact native-helper
parts. **None of `peer_api.py`, HTTP provider or ordinary acquisition is a role.**
Package absolute paths select the pinned files but are not serialized as source
identity; the serialized source rows are role-to-length/hash mappings. Native
helper names are normalized by helper-directory index. A fresh protected package
directory therefore need not change this descriptor when these bytes are exact.

This separation does not assert that transport is irrelevant to security. A
transport bug that permits arbitrary state writes could defeat protected-state
premises even when `I` is unchanged. This proposal is a reviewed behavior update,
not recovery from known owner compromise. Ordinary hashes do not prove those
premises or authenticate a package obtained from an untrusted supplier.

## Proposed exact overlay, not in-place replacement

The built-package map would change only:

| Package destination | Selected source |
|---|---|
| `support/transport/http_provider.py` | `ordinary_multi_source/http_provider.py` |
| `support/transport/ordinary_acquisition.py` | `ordinary_multi_source/ordinary_acquisition.py` |
| `peer_api.py` | `ordinary_multi_source/peer_api.py` |

All source paths above are below `software/v5/`. A new separately reviewed
assembler and three-row overlay map are needed: the existing exact-module
assembler has a fixed, different three-role allowlist and must not be weakened
or edited. Reuse its approved file-only helper primitives and lifecycle in a
fresh successor, not arbitrary overlay/path injection.

The base must be the operator's approved exact-module package, actual PROFILE,
terminal exact-module receipt and immutable byte map. Validate its 45 noncompiled
roles against the investigator compatibility map and its 72 named native roles;
native byte identities come from that operator's immediate receipt/profile, not
historical example hashes. Require the exact-module assembler identity and its
document/census layout. Preserve `installation/INSTALLATION.json` byte-for-byte.

Copy into a fresh disjoint leaf. Update only the three auxiliary file pins in
the copied PROFILE; retain the same 117 auxiliary roles. With no new document
inside the package, there remain 153 payloads excluding PROFILE: three changed,
150 byte-identical. Keep the eight old document payloads unchanged and place
the authoritative multi-source supplement outside the package. Recheck input
and output maps, commit PROFILE last, then produce a terminal receipt describing
exact differences with `ASSEMBLED_NOT_ADOPTED` and file-only/nonacceptance scope.
Failure outputs remain; do not renew the allocation or replace the base.

The unchanged native outputs can be copied from a genuine current approved base;
there is no reason to rerun its native build. The supported end-user build chain
would append this stage after exact-module, not replace an intermediate stage.

## Retained reports and the supported public path

Three different checks must not be confused:

1. `ordinary_investigator_bundle/prepare_selected.py:58` checks a fixed 45-source
   compatibility map. It correctly refuses the three changed source rows.
2. `ordinary_network_kit/prepare.py:209` (`Inputs.report`) and `:376` (`parent`)
   require a referenced report's `profile_sha256 == PROFILE`. A new selector/map
   alone would still refuse old-profile init/intake/receive/find reports.
3. `ordinary_sparse_access/peer.py:174` and `:214` accept an explicitly supplied
   hashed config, open state against the **implementation descriptor**, and call
   `api.receive`. They do not demand a new-profile historical parent report.

Therefore the first integration should document this existing public route:

- Independently approve/select the fresh package PROFILE and supported runtimes.
  Stop/close services and serialize access; retain old package/state/reports.
- Keep the existing catalog, custody, store ID and original persistent limits.
  Select an actual successful existing local parent root; preserve its original
  report and closure evidence as evidence of how that root was obtained.
- Author a **new** receive config with existing `contacts`, `selection`,
  `parent_root`, `limits`, `dependency_policy` and all three new source-policy
  fields. Copy the exact inert `{provider,snapshot_id,record}` selection from an
  independently selected successful find or explicit metadata handoff. Preserve
  its report; do not relabel it as new-profile output. Such metadata is not proof.
- Explicitly select 1..8 approved contact labels, the timeout and reserve. The
  discovery provider remains in `selection`; it need not be an acquisition source.
  Never automatically add the discovery provider or follow unapproved referrals.
- Hash the **new config bytes**, then call the unchanged final
  `run.py ... peer -- receive --config ... --config-sha256 ... --catalog ...
  --custody ... --store-id ... --custody-limits ... --output ...` with finite
  launcher limits, fresh diagnostics/output and the new actual PROFILE.
- Require outer clean closure plus actual receive status, local-acceptance facet,
  resulting parent/root bindings, network ledger and bounded source report.
  Partial acquisition does not imply admission; a reported committed admission
  followed by later failure must not be blindly replayed.

No report authority is broadened, no old report is rewritten, and no fresh
native initialization is needed just to satisfy an offline preparer. A wrong
parent still refuses in `owner.catalog.context(parent)` before network I/O;
selected evidence still passes ordinary preflight and actual local admission.
This is the supported CLI config surface, not a private in-memory module patch.

For subsequent authoring/module calls, existing direct owner CLI forms accept
the actual resulting local root. A future preparer successor can support the
new interface and optional source fields. Cross-profile report acceptance would
need its own precise compatibility evidence and explicit source selection; it
is not necessary for this transport feature and should not be smuggled in now.

## Minimal guide/distribution work

For the immediate local integration, add one authoritative `MULTI-SOURCE.md`
supplement next to its source-only overlay instructions. It needs the direct
config/launcher recipe above, exact scope/default behavior, error/charge semantics,
the retained-report caveat, existing-state reuse conditions and explicit no-native-
recheck/no-new-init guidance. Do not tell readers to use the old selector against
the changed package, edit the old map, or modify a hash-bound package manually.

The current investigator archive remains frozen and does not contain this feature.
Before making a later single self-contained distribution, select a fresh source
bundle with updated root README and build/continue navigation, the new overlay
source/map/guide and a new exact full-root manifest/receipt. Preserve the old
archive and predecessor association. Do not repeatedly repack it during source
development or claim the existing archive already includes multi-source receive.

## Bounded validation after focused controls pass

Theory leads: exact unchanged bytes plus the identity equations above establish
why transport selection does not inherently require reproving the library. Test
the changed file-selection boundary, not the unchanged Lean checker again.

1. Independently review the new file-only assembler/map/guide and its full diff.
   Include rejection of wrong base interface, wrong immediate receipt/overlay
   pin and output reuse; no database or native imports are needed.
2. Select one fresh bounded file-only assembly from the actual approved current
   base. Compare the entire output map, exact three differences, unchanged native
   installation, owner/profile/module support and complete role census. Verify
   that no old state/report/archive was touched and no extra output is claimed.
3. Check the resulting PROFILE and loader-required role paths, and bind the
   already-reviewed/tested H/O/peer bytes to their final destinations. Source/
   import-identity controls can reuse the focused suite's conclusions when the
   selected bytes are exact; do not repeat its full suite merely after copying.
4. Check the new guide's CLI/config fields against unchanged peer entry and new
   receive fields; explicitly test new-config generation/hash binding if a helper
   is later added. Historical report-profile refusal remains a documented fact,
   not a reason to repeat native init or change old evidence.

An actual old-owner reopen is **not claimed** by these file-only steps. If a
deployment review needs such evidence, select one separately bounded,
non-mutating compatible-state operation through a supported API; do not infer
permission to inspect/mutate a live catalog or rerun its mathematical campaign.
No native positive/negative/build campaign is warranted solely by the exact
three-file transport update. Any additional changed trust-boundary source would
invalidate this minimality argument and require a fresh decision.

## If the footprint later grows

- Changed checking implementation: preserve old state; fresh supported owner
  and independently check selected inert mathematics using the existing update/
  recovery procedure. Never edit ADOPTION to force compatibility.
- Changed only module-support identity: mathematical catalog acceptance may
  remain; old warm anchors refuse. Recreate the needed realization under the new
  support without pretending old anchors migrated.
- Changed semantics/foundation/runtime profile: no silent identifier substitution
  or generic migration is supplied by this plan.
- Compromised owner environment: identical hashes alone do not restore trust.

The existing `software/v5/UPDATE-AND-RECOVERY.md` already states these distinctions.
The catalog's private legacy-import activation is not a general transport-update
migration API and is neither needed nor selected here.
