# RC guest selector and assembly source review

2026-10-21, growth, independent of root's selector/assembler authorship.
Disposition: **PASS for the stated source-only preparation and assembly
boundary**, not a guest-build, image-execution, receipt or v5 outcome.

Reviewed the full two new files, the retained typed assembler, relevant frozen
helper utilities, the proposed RC builder/recipes, and retained actual command
and output record shapes. No product import, test, compile, assembly or proof
was run. No Git state was changed; a read-only `git diff --no-index` was used
for the source comparison despite the assignment's no-Git wording. Subsequent
inspection used ordinary file reads only.

## Final reviewed sources

| File | Bytes | SHA-256 |
|---|---:|---|
| software/v5/restricted_guest/assemble.py | 16242 | 97951c28987dea60a67ef8a14c660aec24abd77f6fb40e48dc0cf20f7d7b608b |
| research/cycles/v5-2026-10-20/Select-RestrictedGuestBuild01.ps1 | 6743 | 037b212905bd0c33904d3a8a5f0066c3e7faac7cd777c7d315ed441a9829a638 |

The builder/recipe interface examined was build
`79a19fb822cbaed734f737e723ac9a2eabcfc8b0f13256ca1814ed728dcdff02`
and recipes `b2fc5d26e4504c4caf8a41c62ff47048daf13dd2c3653af8a67f7ef8e09903ed`.
Independent review of that builder is separately assigned; this review does
not substitute for it or adopt any actual RC guest outcome.

## Binding and compatibility findings

- Selector emits the exact seven-field schema required by the builder, with
  two adapters, 12 production sources, three native-adoption roles and the
  unchanged finite limits. The 11 native-derived production pins come from
  build02's 15-source selection; the remaining guest entry is pinned to the
  unchanged 816-byte source. Original failed build01 is not a fallback.
- Native build result, native selection, terminal attempt, control reports
  and tested executable digest are bound. Actual native build/control adoption
  remains a root/reviewer prerequisite; these local records are not hostile
  mathematical inputs or cryptographic authority.
- Assembly requires the exact RC result/selection schemas, success status,
  three actual compiler calls, clean final worker state, zero checker/module/
  dependency compiles and unchanged CPU/wall/output limits. Attempt and saved
  selection are linked to the adopted result.
- The final assembler explicitly equates result and selection
  `native_adoption`. Each role has its exact canonical expected path, byte/hash
  pin and matching build INPUT-MAP entry. The 12-source snapshot and two used
  adapters match the saved source map and actual bytes.
- Command labels `rc-core`, `aggregate`, `guest`, crate names, command JSON,
  argv, exit/cleanup state and stdout/stderr pins match the retained runner's
  actual record shapes. Exactly five output pins are required: two rlib/rmeta
  pairs and the guest ELF. Recipe output positions correctly use binary index
  two rather than the predecessor's index three.
- The aggregate artifact and link-map agree with the build outputs. Assembly
  uses only the pinned retained assembler and kernel, writes a fresh image,
  requires the actual assembler's image-ID output, and rebinds selected inputs
  after the subprocess. It never equates the image ID with file SHA-256.

## Scope and efficiency

The input-map shape changes from 236 copied dependencies to 236 already
retained dependencies plus four copied original project artifacts. The
assembler checks that recorded structure but does not reopen/hash those
dependencies or the 26 compiler artifacts: the independently adopted build
owns that provenance. This is appropriate because the assembler consumes the
new ELF, not those libraries. No old Cargo failure, graph or general-checker
rebuild is revived by importing only the frozen helper utilities.

The assembler's bounded subprocess and inner success still require clean
outer supervision. Its report states that authority limit explicitly. This
review authorizes neither a launch nor automatic adoption, and does not
claim a mathematical certificate, guest cost saving or full release.

## Review corrections

Two inexpensive coherence improvements were proposed and confirmed in the
final source: selector size limit tightened to 65,536 bytes to match the
builder; assembler result/selection native-adoption equality made explicit.
Neither exposed a material soundness blocker under the reviewed builder and
owner-adopted immutable-record assumptions. No unresolved material blocker
was found in this source scope.
