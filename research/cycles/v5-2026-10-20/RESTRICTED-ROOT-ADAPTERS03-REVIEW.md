# Restricted guest03 and matched-pair root adapters: independent source review

2026-10-21, core_release. Status: **PASS_SOURCE_CHANGED_BOUNDARY_ONLY**.

This review covers root-owned selection/assembly adapters, not the reviewer's
own matched-pair implementation. It is source/data review, with read-only
PowerShell hashing and JSON inspection. No reviewed selector, Python module,
preparer, compiler, assembler, host, guest, proof or network operation ran.
Root owns source adoption, exact future inputs and any runtime selection.

## Exact reviewed files

Paths are relative to the sole canonical project root,
`E:\Distributed Trustworthy Mathematical Knowledge Network`.

| File | SHA-256 |
|---|---|
| research/cycles/v5-2026-10-20/Select-RestrictedPair01.ps1 | e06a2da5e3025a686cd1522d066ea8114d8b1e0aa4ae7604dfe72c37d80f08ee |
| research/cycles/v5-2026-10-20/Select-RestrictedGuestBuild03.ps1 | e4f17794310792989df3f73706f78c67abec3c3ea1f83192161e65b1db958e8c |
| software/v5/restricted_guest/assemble.py | 0ebc655842b1092f4314e27fa4f6e57e452303eae06b2e60b1b5a19bac46a957 |
| research/cycles/v5-2026-10-20/Select-RestrictedGuestAssembly01.ps1 | e1e745b6375ef7c3456fa30e9756aea6777ca813234f89e43b21b4671074c6ad |

The pair contract used for this comparison is source
`6deb0711c94fb6baba44e17a216befcd2ff8e945ede64148f7f7d54e0e241af6`
and checkpoint `RESTRICTED-PAIR-EXECUTION-SOURCE.md`.
Growth's consulted build03/recipes03 interface has source hashes
`847589a36df894a022fe3dc8bf8251d32d49cfc605c2357a3311dd30ac1e8fbb`
and `e51b7b02d24c430599a021acaf92262fd7c49f6a3ebc2aa34287d6d5e29ccdef`.
This is not a replacement for that build source's independent review.

## Matched-pair selector

The selector constructs exactly the sixteen source paths recorded in the pair
checkpoint. I independently reconstructed that map from actual adopted controls
and general-execution selections and matched all sixteen current file hashes.
The five additional admission/aggregate files, pure preparer and pair adapter
are included; old controls sources are reused without rewriting them.

Thirteen fixed retained record/input digests named by the selectors were
independently checked against actual files. They include controls selection,
fixture and both outcomes; original general execution selection; base receipt;
both host results; general guest build and image/outer results; original module
source map; and retained assembly selection. Both host result-to-selection,
attempt-to-result, three-source-map and command-argv bindings agree. Actual
executables also match their recorded pins:

| Host | Bytes | SHA-256 |
|---|---:|---|
| general | 6630400 | a9438205bbb091623f12bd10a7e9a0a2b437c873003fec3cb000c7d8dbbd7a05 |
| restricted | 5426176 | e3f35fb15ac19ce9862796e50f01807145583307b9b607c8219411c8206271b9 |

Both retained host jobs report zero active and limit-terminated processes, and
neither host directory has a finalization override. The general assembled image
is1868700bytes with SHA
`0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46`.
These observations verify selector compatibility, not a repeated host-build
source or full outcome audit.

The config has the required schema, exact23 named leaf records, general/RC
roots, fixture and genuine base receipt. The future RC guest/assembly/outer
digests are mandatory hash parameters, not placeholders. The selector also
pins both dynamically named host/image artifacts. At review time RC guest03
and RC image-assembly results did not exist; the selector therefore cannot yet
produce a usable selection and the review does not assume those operations pass.

The retained Python basis contains exactly18 files; all were hashed. The frozen
manifest and three supervisor/helper files also match. Expected eventual runtime
pin count is51: the adapter's32 data/runtime pins,18 Python files, and the general
execution selection used to derive source hashes. No compiler/SDK dependency
tree or build-library copy is introduced for execution.

The outer selection is420inclusive CPU seconds,600wall seconds,4096MiB,
three processes,1MiB per captured stream. Three processes suffice for the pair
Python process plus the inner host Job's at-most-two processes; host arms are
serial. The inner180CPU/120wall host ceilings,240wall arm ceilings and530wall/
60controller-CPU pair ceiling remain separate nested bounds. Reaching any bound
may fail the run; the outer cap is not a promise that all inner maxima plus
overhead can simultaneously be consumed. The outer inclusive CPU total must
not be added again to inner Job totals in final accounting. No proof or retry
is authorized by this selector.

## Guest03 selector and four-crate consumer boundary

All four consumers agree on:

- Run `restricted-guest-build-03`.
- Selection schema `DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_V1`.
- Result schema `DMKN_V5_RC_GUEST_FOUR_CRATE_BUILD_RESULT_V1`.
- Required status `PASS_RC_GUEST_FOUR_CRATE_COMPILES_ONLY`.
- Recipes schema `DMKN_V5_RC_GUEST_FOUR_CRATE_RECIPES_V1`.
- Four commands in order: module, rc-core, aggregate, guest.
- Twenty-one production sources, seven outputs, one module compile and zero
  checker compiles.

The21-source set is nine reviewed RC Rust files, two aggregate commitment
helpers, unchanged aggregate/main.rs and nine original module-relation files.
I checked their actual length/hash pins against native-build02 or the explicitly
pinned original module source map; all agree. Neither the bounded-parser module
successor nor a silently adopted failed module artifact enters this map.

The build selector retains the240worker-CPU/300worker-wall/4096MiB/six-process
envelope,40ordinary/60final controller CPU,420total wall and256MiB/2048-entry
sampled fresh-output bounds. It only writes a new selection with create-new
semantics. It binds independently adopted native build and exact controls;
the build source separately checks the full controls contract before compilation.

Assembly now checks the exact03 four-crate selection,21-source snapshot and
input-map shape,236 retained dependency entries and two copied Nanoda artifacts.
It requires four clean matching commands and their retained logs, exact seven
output names and pins, exact recipe outputs, unchanged ELF/artifact/link-map
bindings and no finalization override before/after. The seven outputs are the
module,RC,aggregate rlib/rmeta pairs and one guest ELF. Its interface agrees with
the unchanged actual-image receipt required by the pair adapter.

The assembly selector covers those21 snapshot files, two used build adapters,
four command records/eight logs, seven outputs, link map, six build records,
attempt, three native adoption records and retained runtime. The retained runtime
filter yields exactly21 Python/driver/kernel files, whose hashes were checked.
The root's exact build-result hash transitively binds the maps, commands and
artifact pins; assembly independently validates their contents before use.
The selector retains120CPU/120wall/1024MiB/two-process outer ownership, invokes
only the assembly adapter, and permits no guest execution or proof.

The unchanged assembler subprocess mechanism was not broadly re-audited; this
assignment specifically covered the four-crate changed boundary and selector
closure. Its frozen helper pin and3-source selection agree with retained files.

## Disposition and remaining gates

No blocking source/selector mismatch was found in this scope. Source acceptance
does not supply missing guest/image outcomes, certify mathematics or establish
economic benefit. Before the pair, root must separately adopt actual guest03
and assembly outcomes, pin their exact bytes and adopt the independent review of
the pair adapter itself. Preserve failed01/02 guest attempts and all old evidence.
The two-host/public-release and full useful-growth obligations remain unchanged.
