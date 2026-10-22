# Typed production: retained host and image adoption helpers

2026-10-22, storage_outcome_audit. Canonical root:
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Source implementation under TYPED-PRODUCTION-SELECTION only. No runtime, build,
proof, installation, trust adoption or Git mutation is selected by this note.
Root owns integration and subsequent decisions; independent review is pending.

## Result and contracts

Two fresh helpers are implemented. Existing source/evidence is unchanged.

| File under software/v5/typed_production | Bytes | SHA-256 |
|---|---:|---|
| host_adoption.py |16821|`0553220f16866f8f9d0cb586f73d182e15074cf66c030421a903f4dcde7e5f87`|
| image_adoption.py |15698|`e1bf74167d09d3dbaceb841366363dc698cf290a891d5ffce743f86dfce76f4a`|

APIs agreed with storage_integration_adapter:

```text
host_adoption.adopt_build(owner, pins, table) -> exact retained host file pin
image_adoption.adopt_image(owner) -> None; sets owner._image only after checks
```

Both use the existing pinned production utilities and owner `_records`, `_add`,
`_read`, `_check`, `_no_override` facilities. No prover_memory import is added.
The image helper also uses the unchanged `_local_outer`. Source closure must
include both new helpers. The producer retains checks over
`_refinement_empty_evidence`: ordinary absolute path and zero size, including
the newly appended selected empty logs. No empty executable pin is invented.

## Exact corrected-host derivative

The predecessor is `software/v5/prover_memory/adoption.py`, SHA-256
`b41fd140a13782be3258452ecee7c7389bf2b8621f24fdb4d21f64962b334176`.
The new file is its full narrow derivative. The complete substantive diff is:

1. Replace the impossible comparison between original descriptor aggregate
   image and selected runtime image with two explicit comparisons:
   descriptor aggregate equals original
   `99b9f1cf14f922f13790b4949999dd71f3da9143465a0033299cd3a3a960ec60`;
   runtime aggregate equals selected typed
   `9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865`.
   Individual image, foundation and policy comparisons remain unchanged.
2. After the unchanged exact-derived-source-map check, additionally require
   its two reviewed image-parametric source rows:
   `source/stage/software/v5/aggregate_small/stage_host.rs`,32291 bytes,
   `975e68dfbc8d091733cee72a18d81fb45617886585f1806fe9425cf4aa847955`;
   `source/stage/software/v5/aggregate/receipt.rs`,3631 bytes,
   `41db7677d40af4fd779159e8442724bff7842b7f4e5745411e5846d8e7678254`.
3. Add documentation and constants for those two changes.

All remaining code is unchanged: reviewed descriptor and patch, adapter/source
snapshots, SDK inventories, retained source-map derivation, five ordered compile
argv, actual linked dependency edges, all output pins, exact environments and
runtime manifests, closed phase jobs, aggregate accounting, limits, empty
nonexecutable evidence handling and final binding/override checks. There is no
owner proxy, forged profile, monkey-patch or rewritten historical report.

### Why changing the runtime image does not require rebuilding this host

The exact stage-host source computes the image ID of the actual supplied ELF
and compares it to the independent adopted image argument. It binds the decoded
header to that image, derives the same general-wire conditional header, and
verifies each exact pending I/A claim. Its session commitment includes ELF hash,
adopted image, relation image, foundation, policy, wire, header, execution limits
and ordered parent hashes. Capsule session and target claim must match.

The host checks ordered assumption receipts, stage graph and checkpoint/session
bindings. Finish verifies the complete composite integrity and target claim,
then the final succinct claim and exact aggregate application receipt. The
receipt helper accepts genuine succinct Poseidon2 receipts only, disables dev
mode, performs full application verification under the independently selected
image and compares the exact journal. Neither source hardcodes old99b9 as the
allowed runtime image. The original descriptor records build provenance, not
a restriction encoded in these reviewed generic runtime checks.

This argument establishes an image-parametric host interface, not that any
arbitrary new guest is trustworthy. Adoption permits only the exact typed A*
and its actual independently reviewed source/build/assembly records. General
DMKNAI02 compatibility and typed-checker correspondence remain prerequisites;
source adoption neither manufactures a receipt nor proves universal checker
correctness. A host/guest preflight disagreement remains a refusal, not a reason
to weaken the header or image checks.

## Typed image evidence chain

`image_adoption.IMAGE_ID` exposes exact A*. `RECORDS` maps the following ten
roles to `{relative_path, bytes, sha256}`. The full canonical-root-relative
paths and exact sizes are in the source constant, not inferred by a search.
Every caller-supplied pin must match this exact retained role before reading.

| Role | Retained record | SHA-256 |
|---|---|---|
|result|typed-guest-image-assembly-01/assembly/RESULT.json|`4c26d075d850ff38a0922dbbdfad00303d16b49dee41f71a859f3777166e530c`|
|outer|typed-guest-image-assembly-01/RESULT.json|`174878e768ed578e0a4f239de8423591ebf4ea34f09213e52c84aff46362b33b`|
|selection|typed-guest-image-assembly-01/selection.json|`d911dbfd934b5e43c2743403076afd47794185a593f225582f1bfb73ab025362`|
|guest_build|typed-guest-build-01/RESULT.json|`b1b4f7a82aabddc5dd3349a4f82ba79e846517a6db94c3a3d911702c7d6576a4`|
|guest_selection|typed-guest-build-01/selection.json|`bab4fd3e335683be859a1f38843b415eff13a2dcb9c215c931ae1d6f463911e3`|
|guest_source_map|typed-guest-build-01/SOURCE-MAP.json|`a05c6e910664260b05c4c875ea0df6545a4dd969b608f22a3b9585e590885356`|
|artifact|typed-guest-build-01/ARTIFACT.json|`f1d732f34287a63096f816fcc62f0724a470f6dc3dc725ae6b816787e08800ff`|
|guest_attempt|typed-guest-build-01-attempt.json|`b807f0c299f40fa509a63099d2e75b4a92bf941062c60376bcf378a9657dc6e7`|
|guest_recipes|typed-guest-build-01/RECIPES.json|`fa11546f7fe58c752f58830429760c3958566ca36b6da7051fe2142306fa0ac5`|
|assembly_command|typed-guest-image-assembly-01/assembly/COMMAND.json|`9aa845df63ab85be75b4d54d2f3be94ee23d2dcd9580c825f662f9e3e60d2145`|

These paths have common prefix `experiments/v5-local-checks/`. The helper binds:

- Actual typed schemas, terminal attempt, four-compile/zero-execution scope,
  selected limits and closed build jobs. It preserves rather than relabels the
  actual typed records; the assembly result selects the guest-selection hash,
  whereas its outer operation selects the different assembly-selection hash.
- Exact37 selected/36 compiler-declared source rows (only bounded_parse census
  is support-only), two build adapters and actual retained source snapshots.
- Four recorded recipes, actual ordered argv/command records, normal closure,
  logs, seven declared outputs and exact artifact-to-ELF linkage. Recipes are
  explicitly reconstructed equivalent profiles, not captured Cargo argv.
- Exact assembly command/70 selected-input metadata, actual ELF and kernel
  arguments, output image, selected build/absent-failure marker and clean outer
  operation with exact build operands.
- Actual assembler stdout naming A* and1868700 image bytes, zero stderr,
  and the image file's separate SHA-256
  `0bb44c54238f78fe04a385b689ddcce9a1b8770eac5a2f0ae9e71de1b62b0d46`.
  Image ID and file hash are not substituted for one another.

### Rebinding scope and efficient reuse of adopted evidence

The active producer pin table retains the ten records, source snapshots/build
adapters/assembly snapshots, four actual command records, nonempty selected
logs, actual1809932-byte ELF,1927768-byte link map and1868700-byte image. Empty
logs are checked separately and rechecked by the integrating producer.

Six intermediate rlib/rmeta outputs, the old assembler and its kernel remain
exactly committed historical build metadata. They are not executed by proof
production and are not repeatedly rescanned. In particular, this bridge does
not rehash the2.3GB compiler runtime or the old66.7MB assembly driver on every
proof stage. The original adopted build/assembly is the provenance boundary;
the eventual host and receiver independently check the actual runtime image
and receipt. A future rebuild is different work requiring its own selection.

The bridge intentionally names actual retained local paths. It is not a public
relocatable release artifact or a generic newly built guest admission API.
Relocation of these evidence records cannot be faked by rewriting their content.

## Validation performed and next gate

Workspace guard passed after the documented process-local PowerShell-policy
invocation. Source/evidence reads and narrow metadata/hash inspection were used.
Both new files were reread; the derivative was generated by four exact textual
seams against the retained predecessor. No Python import, AST compile, test,
native executable, build, guest, proof or Git mutation was run by this author.

Independent author/reviewer owns focused binding controls and source review.
Root must read those before selecting execution. In particular genuine adoption
must be distinguished from explicit record doubles used to exercise rejection
branches. Neither a successful constructor nor passing structural controls
would establish cryptographic acceptance, capability completion or final v5.

The unchanged next central endpoint is resolved A*(U), ordinary proof-body-free
interface reuse, then resolved A*(V) whose actual frontier is A*(U) plus the U
member opening. This source checkpoint does not fund any part of that endpoint.
