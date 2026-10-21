# RC matched execution: prepared source boundaries

2026-10-21, core_release. Implements only the two files selected by
RESTRICTED-COMPOSITION-GUEST-PREPARATION after actual native-build02 audit.
No preparation call, compiler, host, guest, proof, installation or trust
adoption was executed. Root owns selection and subsequent invocation.

## Exact sources

| Source | SHA-256 |
|---|---|
| software/v5/restricted_composition/prepare_execution.py | `fd184d7be0ca6eaa139a4b79764ac435c9e2036fea9116d591701d85a192e71d` |
| software/v5/restricted_guest/build_snapshot_host.py | `719ed9058ca9a8d5dfa59a07a362f4438bd8e9b13753b7883bfb48333021c984` |

These sources remain unexecuted and await independent changed-boundary review.
Old build01/02, native core, controls, fixture generator, guest entry, host and
receipt source bytes were not modified. No public producer facade is added.

## Pure same-target preparation

The API is:

```text
prepare_pair(fixture_raw, *, fixture_sha256, parent_receipt,
             general_image, restricted_image)
  -> {general: {wire, header}, restricted: {wire, header},
      parent, target, derivation}
```

All values except `derivation` are byte strings or byte-valued dictionaries;
`derivation` is JSON-safe. The function does no filesystem or subprocess work.
Root's caller must bind the exact fixture SHA to the adopted native differential
outcome and both images to actual guest build/assembly records. A caller-supplied
hash by itself is not such adoption. No saved native result replaces the hosts'
mandatory preflight or receipt verification.

The function selects only the first context-transport target from the existing
four-field fixture (at most4MiB). It enforces the six-field RC schema, exact fixed
base-I journal/receipt hashes, one binary_congr opening and equality to the
selected fixture-generator's first theorem/proof. It preserves the original W
bytes' canonical value rather than re-emitting a more favorable comparator.
The exact adopted fixture binds the native-tested W/RC proof correspondence;
shared spec/parent/image/rank are also checked explicitly here. No second target
or historical FIRST is silently substituted.

RC preparation enforces256KiB frame bytes,32,768JSON-value occurrences and64
levels before encoding, with the same unsigned64-bit JSON-number boundary.
It does not duplicate trusted type inference. The general W is bounded to1MiB.
Both arms use the retained aggregate encoder with one fixed-I claim, one
frontier, one new target and one witness. For RC only, the validated exact
12-byte DMKNAI02/v2 prefix is replaced with DMKNRC01/v1; globals are not patched.
Exact fixed layout/count/EOF-derived payload checks retain all remaining bytes.

Both arms share identical ordered exact-J members, target, base receipt,
membership root/paths, maximum rank1, height1 and foundation/policy. Their
192-byte headers differ only at aggregate-image bytes12..43. The general image
is the selected typed implementation9d5072a6; RC must be a distinct nonzero
actual image. Neither predicted J nor H is mathematical authority.

Root can serialize each arm under a separate fresh output and launch the
unchanged host argument grammar. Include pure preparation CPU in the paired
comparison rather than hiding it outside the investment screen. Source import
closure adds this preparer, existing fixtures/native-row/witness codecs,
aggregate_claims input/bindings and their existing module/admission package
dependencies; no old FIRST-specific snapshot helper is imported.

## One RC snapshot-host link

Selection schema is `DMKN_V5_RC_SNAPSHOT_HOST_BUILD_V1`, exact name
`restricted-snapshot-host-build-01`, with fields schema/name/
authorizes_compile_only/sources/runtime_pins/limits. The three selected source
entries are the new builder, unchanged aggregate_small/aggregate_host.rs
(`6644d9a0`) and unchanged aggregate/receipt.rs (`41db7677`).

The builder pins the actual small-host01 result, command, environment, input
map, selection and finalization. It separately pins native-build02 result
`24e8ebf8`, source map, three-command recipe, selection and finalization; exact
RC core/aggregate artifact hashes and sizes must match that result. There is
no use of the failed01 library or controls executable as a relation artifact.

Take the exact retained small-host map of1071runtime files, remove its explicit
old aggregate library and add the two RC libraries. This gives1072pins and
2,322,344,899retained bytes. No retained tree is scanned to discover dependencies
and no backend view is recopied. The original module/checker, Rust, SDK, native
libraries and system-tool bindings remain unchanged. Pin checks occur before
work and at finalization; the pre-command refresh checks only small records/
sources, avoiding a third duplicate runtime hash pass.

One exact retained command changes only:

- Crate name, new source snapshot and output executable location.
- Explicit aggregate extern to native-build02's RC aggregate.
- A dependency search path and explicit extern for native-build02's RC core.
- A distinct `dmkn_rc_snapshot01` crate metadata suffix.

The host retains its native check_bytes preflight, fixed-I receipt verification,
actual ELF/image binding, po18/N256 execution, bounded capsule custody, exact H
comparison and no-dev-mode policy. No Rust host semantics are changed. The
builder does not call that executable, link a stage/proving host or produce a
receipt. Output is `restricted_snapshot_host.exe`, with result schema
`DMKN_V5_RC_SNAPSHOT_HOST_BUILD_RESULT_V1` and success status
`PASS_RC_SNAPSHOT_HOST_ONE_LINK_ONLY`.

The prior finite envelope is preserved:240inclusive worker CPU/300worker wall
seconds,3072MiB/six-process Job,40ordinary/60final controller CPU,420total wall,
512MiB/8192sampled output entries and1MiB command logs. These are upper bounds,
not projected cost or a hardware requirement. Output census is not a hard disk
quota and trusted-source building is not hostile-code sandboxing.

Every command/source/runtime/record map is recorded. Outputs are create-new;
failed attempts preserve diagnostics and block implicit name reuse. Final input,
source or owned-process closure failure overrides success; finalization has an
explicit overriding marker. Existing helper-specific VCTIP cleanup remains
limited to the exact pinned owned telemetry process. No unrelated application
is terminated.

## Remaining decisions

Independent source review precedes any new host-link selection. The native
controls gate and actual guest-build/assembly adoption remain prerequisites
for the paired execution. Its unchanged prospective thresholds are75% padded
rows, at most64po18 segments and no preparation-plus-execution CPU regression.
These files do not establish that the thresholds will pass and do not select
proof funding. Full v5 remains unfinished; the next useful outcome is the
same-target economic decision, not an additional release label or RAM survey.
