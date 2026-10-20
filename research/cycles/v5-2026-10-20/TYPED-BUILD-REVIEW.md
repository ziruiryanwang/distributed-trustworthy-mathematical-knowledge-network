# Typed-row compile adapter: independent source review

Reviewer: `core_search`, 2026-10-20. Canonical root only. This review is distinct
from the decoder/correspondence semantic review and the control authoring owned
by `core_release`. No compiler, test, native checker, guest or prover was run.

## Disposition

The prospective `software/v5/typed_rows/build.py` has no identified blocker in
its four compile paths or their exact source/type/link interfaces. The final
control-root closure and manifest selector were subsequently reviewed below.
**CLEAR at this source-review boundary.** This is not an execution selection
or successful compile; root owns exact-source selection and all execution.

Reviewed build adapter: SHA-256
`93e9946222ee1d46db665e1a00b0b1f31a9474a16b5e805f47a11da07ed7c739`.

## Concrete checks

1. The adapter derives its commands from the retained four-command
   `proof-validation-integration-build-01/compile-commands.json`, whose labels
   and exact bytes are required. Each source/output substitution requires one
   occurrence. Checker, module and aggregate outputs are fresh rlibs; no
   retained project rlib is copied or linked as the new implementation.
2. The checker command retains its original third-party dependency paths.
   The module and aggregate commands replace the prior project dependency
   directory and all explicit project externs with the fresh build directory.
   The post-transform assertion disallows any surviving prior-project path.
   Checker compilation precedes module compilation, which precedes aggregate
   compilation. No Cargo, dependency build, guest target or proof command is
   added.
3. `checker_lib.rs` binds the frozen memo correspondence as
   `module_correspondence_legacy`, the fresh correspondence under its ordinary
   module name, and `rows.rs` as `typed_rows`. Fresh correspondence reexports
   the actual legacy `BodyOpening`, `GroupBinding`, `MatchedGroup` and
   `StructuralCorrespondence` types, so retained input/module call sites and
   new typed callers share those identities. The unchanged parser entry points
   coexist with the explicit typed constructor in the same parser module.
4. `module_lib.rs` includes the frozen bounded parser/relation as distinct
   modules. `Prepared` carries either its original `BoundedValue` or the new
   private-construction `HybridFrame`. Their public method visibility matches
   the module relation and cross-crate census callers; `into_parts` is called
   inside the module crate. The old and new paths return the same reexported
   `RelationConclusion`, preventing aggregate type substitution.
5. `foundation_static.rs` retains `matches_rows(&[Value])` for the literal
   legacy relation and adds a borrowed mixed-row method for the new relation.
   Its actual `include!` resolves to the selected unchanged foundation data.
   No suffix Value reconstruction is required by that interface.
6. The listed non-test Rust `#[path]`, `mod` and `include!` closure is present
   in `FRESH | REUSED`. Checker legacy tests and aggregate graph controls are
   behind `cfg(test)` in library crates that are not compiled as test crates.
   They are correctly not silently pulled into those three compile targets.
7. The fourth command is formed from the aggregate command but changes the
   crate name to `dmkn_typed_rows_controls`, uses `--test`, changes its source
   to `controls_root.rs`, and writes `typed_rows_tests.exe`. The unique crate
   name avoids an external aggregate/self-crate identity collision. Explicit
   externs include the fresh aggregate/module/checker rlibs and the same
   pinned serde/serde_json/RISC0 libraries. Compilation does not execute it.
8. Selection must name the exact source set; all source byte lengths/hashes
   are checked before snapshotting, after copying and at finalization. Source
   snapshots have exclusive-create writes into a fresh run directory. Runtime
   and helper pins are retained and rechecked. Existing evidence is not edited.
9. One shared phase/Job contains all four compiler invocations, not a fresh
   allowance per command: 180 worker CPU seconds, 1536 MiB, six processes and
   240 phase wall seconds. Controller checks retain 30 CPU/360 wall seconds,
   and output census retains 1 GiB/4096 entries. These are limits, not a
   prediction that compilation will fit. The phase's error path closes its
   owned children; the original exact owned-MSVC-telemetry exception remains.
10. Only four completed commands and pinned outputs can produce
    `PASS_TYPED_ROWS_FOUR_COMPILES_ONLY`. Cleanup, changed-input, output-census
    or finalization failure prevents usable success. The result explicitly
    asserts no test/native/guest/proof/network execution and no admission.

## Boundaries

This is source review, not Rust type checking, compiler success, performance
measurement, proof issuance or product adoption. It does not claim the new
representation is semantically equivalent merely because its modules link.
The separate implementation review and prospective focused controls own that
obligation. The full v5 goal remains open.

## Final control-root and selector closure

The final files were read, not executed. Exact identities:

| File | Bytes | SHA-256 |
|---|---:|---|
| `software/v5/typed_rows/build.py` | 14,536 | `93e9946222ee1d46db665e1a00b0b1f31a9474a16b5e805f47a11da07ed7c739` |
| `software/v5/typed_rows/controls_root.rs` | 224 | `5c0232d74e052e55d159803d57c1246fab5c10c3141abddc24d649e8d297bb68` |
| `software/v5/typed_rows/controls.rs` | 14,225 | `4de1694aa8a90b83ffae9afa8f57fd7016e9a87509a6b4b6f9163d23301d2e02` |
| `research/cycles/v5-2026-10-20/Select-TypedRowsBuild.ps1` | 3,032 | `06305d440041c42ab7b147286437f525bebc88eb1ee9f54ee21554c69695c9f2` |

The actual control root uses the already linked production aggregate `relation`
and compiles just the new `census.rs`, the retained bounded-parse census and
`controls.rs` locally. These are all in the selected closure. Both census
modules resolve `crate::relation::MAX_EDGES` to the actual aggregate relation;
their private `charge` methods remain callable by sibling controls within the
test crate. No graph-control or checker-test source is pulled in implicitly.
The three retained fixture files are runtime reads, not `include!`,
`include_bytes!`, `include_str!` or compile-time `env!` inputs. Their existence
and identity therefore belong to the separately selected controls run, not
this compile's source closure. No additional direct external crate is needed.

The selector enumerates exactly the builder's 39-source set (14 fresh, 25
retained). The selector itself is reviewed separately and is not included in
that source snapshot. It requires canonical cwd and the caller's exact reviewed
builder hash, snapshots each selected source's size/digest, rejects preexisting
selection/run/attempt paths and uses exclusive-create durable writing for one
UTF-8 JSON selection. Its schema, fixed fresh name and keys match the builder's
parser. It cannot launch compilation. No wildcard snapshot, overwritten
evidence, old output reuse, process launch or external write is introduced.

No additional blocker identified. Root may prepare a fresh exact source
selection if the separate implementation/control review also clears; source
review alone does not claim any runtime outcome. No broad repeat is needed.
