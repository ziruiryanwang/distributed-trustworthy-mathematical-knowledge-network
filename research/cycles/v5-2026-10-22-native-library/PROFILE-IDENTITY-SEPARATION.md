# Separate mathematical identity from local checking support

2026-10-22. `preview_boundary_review`. Source/theory only. No code, runtime,
tests, Git or migration selected. Existing V1 admission/recovery identities
remain unchanged. Root owns subsequent implementation selection.

## Decision

**The current experimental native profile is not a suitable portable semantic
identity.** Introduce a fresh versioned split before broad ordinary discovery:

1. A stable **semantic contract ID** identifies the interpretation, fixed
   foundation and mathematical admission policy of portable inert evidence.
2. An exact **local implementation ID** identifies the actual checker,
   controller, persistence support and platform under which a local acceptance
   observation was made.

Portable identities use the first. Protected acceptance records and native
snapshot restoration retain the second and their original support lineage.
Neither ID is a proof of validity. No global authority, new consensus protocol
or political identity scheme is required.

This is a prerequisite for useful interoperable software, not cosmetic naming.
Different supported machines should be able to independently check the **same
inert mathematical object**, while refusing to trust each other's native
snapshots or unsupported implementation claims.

## Exact existing coupling

Reviewed source:

- `local_catalog.py`, SHA-256
  `860a9d731290b2a7fbacd4852bb68185516329ee42845648f4ba3c3856d7c751`.
- `run_native_admission.py`, SHA-256
  `a9bdbfc826221d21cd6454b1f8171b77e657996d89bac0461bee2f6e74ee897a`.
- `ordinary_evidence.py`, SHA-256
  `fc52de53a260b37735da704f4a8a7a732168ca047410868e0f53765950749fa6`.
- `ordinary_preview.py`, SHA-256
  `0fd9bb516fbb53d9d4264271853904e35810286fc92d5670d15d7a9d3c26b0d6`.

The current chain is:

```text
selected DLL/executable hashes, source hashes, compiled helper hashes
    -> kernel_support / adapter_support / basis_receiver_support
    -> ordinary-native-profile-v1 ID
    -> ordinary-basis-root-v1 ID and basis-symbol IDs
    -> evidence bytes, UnitIDs, imported bindings and ExportIDs
    -> preview locator and the planned search namespace
```

`SelectedInputs.__init__` includes `run_native_admission.py` itself in
`source_rows`; `profile()` hashes that whole map. `LocalCatalog.open` hashes
this profile and uses it to identify both mathematics and local artifacts.
The profile also includes the native snapshot format.

Thus a controller cleanup, another valid compiled build, an operating-system
port or serializer revision changes every downstream mathematical identity even
when the interpretation and inert declarations are unchanged. This does not
make current checks unsound; it causes avoidable identity fragmentation and
makes the exact-symbol discovery plan machine/build-specific. Requiring all
users to run byte-identical Windows support is not an acceptable solution.

## Concrete V2 identity contract

Use fresh schemas and hash domains; do not change the meaning of V1's
`profile_id` in place. The exact spelling is a later implementation choice,
but the separation must satisfy the following contract.

### Portable semantic contract S

A canonical, versioned descriptor binds:

- The intended Lean calculus and builtin reduction/quotient rules.
- The ordinary expression/declaration interpretation, canonical byte encoding
  and `erase-mdata-only-v1` projection, including names, universe/binder
  metadata, generated groups, and definition hints that this format retains.
- The fixed basis's exact seed and expected normalized inventory bytes, its
  primitive initialization rules and its explicit permitted axioms.
- The mathematical extension policy: checked safe declarations, no new axioms,
  unsafe/partial declarations, sorry or native-evaluation escape, exact
  dependency meanings and generated inventory, and no overwriting.

Define `F = H(foundation-domain, foundationDescriptor)` and
`S = H(semantic-domain, {interpretation, foundation_id: F, policy})`.
Neither descriptor contains local paths, DLLs, `.olean` files, CPU limits,
controller source hashes or snapshot versions. F is not a local basis snapshot
root; S may reference F without a circular definition.

For the first implementation, retain exactly the current seed/inventory and
ordinary codec rules. Pin the intended Lean 4.34.0 rules to the retained upstream
source revision `293d5d0c0c3f3dded4688b3ccd6a33939ac5102b` and an explicit
versioned interpretation contract; do not use merely the text "Lean4" as a
complete specification. This is a conservative source-defined semantics anchor,
not a claim that Lean has a complete proved metatheory or that any executable
claiming the version realizes it. The normalized fixed-basis correspondence
remains explicit; it does not become original-metadata equality by renaming IDs.

Changing an actual rule, foundation axiom, semantic projection or allowed
mathematical extension policy creates a new S. Parser/resource restrictions may
change which objects an implementation handles without changing their intended
meaning. A binary change alone does not force a new S. Two different S values
do not become compatible merely because their implementations are similar.

Portable evidence becomes:

```text
EvidenceV2      = {schema, semantic_id: S, imports, unit}
UnitIDv2        = H(evidence-v2-domain, canonical(EvidenceV2))
ExportIDv2      = H(export-v2-domain, [S, UnitIDv2, original_name])
BasisSymbolIDv2 = H(basis-symbol-v2-domain, [S, F, original_name])
```

Here `BasisSymbolIDv2` denotes a basis **symbol**, not a saved basis module. Exact
direct-reference imports and own-unit group members keep their existing
meaning. Evidence still identifies exact proof-bearing data; different proofs
or conservatively retained metadata may still produce different UnitIDs.
The split does not solve mathematical equivalence, nor does it guarantee that
different compilers export identical bytes from the same source program.

### Local implementation I and protected warrants

`I = H(implementation-domain, canonical(implementationManifest))` retains:

- The S this implementation is intended to realize.
- Exact selected kernel/runtime and adapter/basis-receiver source/binary pins.
- Exact controller, reader/writer and snapshot ABI/format support.
- Platform/materialization assumptions and the honest scope of the support map.

The existing finite pins are explicitly **not a hermetic toolchain**; the split
must not make their assurance sound stronger. A manifest's `semantic_id` is a
claim until the local owner adopts that implementation with its concrete
correspondence/support justification. Peer manifests cannot add implementations
to the owner's accepted set.

Each protected local accepted-root record binds S, the actual I, its accepted
parent root, exact input UnitIDs/request hash, generated name-to-ExportID map,
and exact native snapshot bytes/format. Parent records retain their own origins.
The native module name derives from a **local snapshot root**, not F or an
ExportID. Use a separate local-root hash domain, with I and parent/request in
that root's preimage, so different materializations cannot impersonate one
another while sharing portable mathematics.

The minimal implementation may keep one immutable I per catalog and the current
whole-store sticky withdrawal. It need not implement arbitrary mixed-checker
hot upgrades now. New implementations can use a new catalog; later explicit
migration may preserve old warrants and snapshot origins. No upgrade may claim
that an unchanged artifact was checked by the newly selected checker.

## Soundness and update rule

Let `Judgment(S,E)` mean validity in the selected interpretation and foundation.
Local admission is justified only under a locally adopted correspondence:

```text
Realizes(I,S) and active warranted parents under S
and actual clean checked extension by I with exact input/output binding
    => new protected warrant for Judgment(S,E + D).
```

`Realizes` names an assurance obligation, not a new Boolean network field.
Its evidence may combine source reasoning, independent review and targeted
controls; it is not established by hashing an implementation manifest.
Hash collision resistance supplies identity binding, not the implication above.

The resulting practical rules are:

| Change | Portable IDs | Local acceptance/snapshots |
|---|---|---|
| Same semantics, different supported OS/build | Unchanged for identical V2 inert data | New I; independently check or use explicitly justified local migration. Never import peer native artifacts on identity alone. |
| Controller/parser optimization preserving interpretation | Unchanged | New I records actual support. Reuse of old warrants must retain their old support, not relabel it. |
| Native serializer or ABI change | Unchanged | Old snapshots are not directly loadable without a selected compatibility/migration argument; their writer/reader lineage stays exact. |
| Checker bug discovered | Mathematical object IDs remain | Withdraw affected implementation support and disable affected warrants and descendants before reuse. Rechecking can establish new warrants under a supported I. |
| Foundation or interpretation changes | New S and portable IDs | No implicit cross-S import; a separately justified translation/bridge is required. |

An implementation bug does not prove every previously checked theorem false,
but it removes the affected acceptance justification. Rechecking one object's
body against still-unwarranted parents is insufficient: all needed parent
warrants must also be eligible. Independent valid warrant lineages may survive;
the initial homogeneous catalog can conservatively quarantine the entire store.
Checks of withdrawal/eligibility must apply on open, parent restoration and
before promotion, not only when an implementation is first adopted.

## V1 preservation and explicit migration

**Do not apply this split to the selected recovery.** The controller author
confirmed recovery retains V1 profile `fd23ae28...` by recomputing it from the
original immutable controller plus existing compiled/runtime maps. The new
recovery controller is independently selected, not inserted into historical
hashes. The copied catalog retains exact store/basis/prefix identities and the
failed reservation. No V2 warrant follows from that recovery.

For a later migration, V1 and V2 are distinct identity domains. Changing the
envelope field or swapping the catalog profile is not sufficient: the whole
dependency-ID DAG changes, including basis symbols.

The preferred bounded migration, if its obligations can be established, is an
explicit owner-local identity translation rather than replaying all proofs:

1. Identify one exact V1 profile/support manifest and an exact S. Establish
   that its checked relation, foundation and retained unit interpretation are
   the same intended judgment. Do not accept a generic `compatible=true`.
2. Start only from a protected eligible V1 root and its exact inert evidence.
   In dependency order, keep every `unit` byte projection unchanged and rewrite
   only schema/profile references and each import to the corresponding mapped
   V2 symbol. Record the total old-to-new mapping and its exact inputs.
3. For every translated unit, verify all external imports map to already
   translated warranted meanings and its exact output-name census is unchanged.
   The preservation argument is induction on this dependency order, rooted in
   the explicitly matched fixed foundation.
4. Issue owner-local V2 warrant records whose support includes the original
   checker lineage **and** the selected migration adapter. These are not new
   native-check observations. Preserve old records and failed operations.
5. Retain each snapshot's original writer/reader compatibility and bytes. Any
   new materialization is separately authorized; changing semantic identity
   does not itself authorize binary deserialization under a different runtime.

If exact relation correspondence or protected lineage is unavailable, the
safe fallback is checking the retained inert evidence under the new profile.
This is an explicit exceptional migration cost, not an automatic repeat of the
current successful basis/prefix campaign. Network users never inherit local
warrants merely from an old-to-new map received from another machine.

## Smallest next software selection

After the current recovery is settled, select a fresh coherent successor:

1. Add a small semantic/implementation descriptor module and exact S/F fixture.
2. Add V2 evidence, export/basis domains and previews/locators using `semantic_id`.
   Preserve V1 validators and bytes; use explicit schema dispatch, no fallback
   that silently interprets a V1 profile as S.
3. Split the local catalog's basis **meaning** from its basis **snapshot root**;
   bind local roots to I while matching evidence dependencies by S. Preserve
   grants, actual worker-event checks, no-overwrite rules and withdrawal.
4. Change admission preparation to supply S and I separately. The Lean unit
   expression/declaration format and kernel checker need no change solely for
   this identity split. Native build work is not a prerequisite to demonstrate
   the pure identity invariant.
5. Use S, not I or a local root, in the forthcoming ordinary index namespace.

The high-value discriminator is small and mostly pure: the same exact inert
unit/import closure under two different implementation manifests yields the
same portable IDs and different local support/root IDs; a changed foundation
or interpretation changes portable IDs; incompatible/withdrawn support still
cannot restore or promote a local snapshot. Only a separately selected V1
migration requires the induction checks above. No large certificate or
multi-machine experiment is needed to resolve this design defect in principle.
