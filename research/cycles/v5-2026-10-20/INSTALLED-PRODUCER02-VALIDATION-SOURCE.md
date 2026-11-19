# Installed producer02: narrow producer-purpose validation source

2026-10-22; author `storage_launch_review`, under root's explicit selection.
Canonical root only. No import, syntax check, test, build, owner, native call,
proof, installation change or Git mutation was performed.

New source:
`software/v5/installed_production02/body_location/distribution.py`

- 75,051 bytes.
- SHA-256 `9dd12c04577c5999f3f766a92f928c85127b6b284c271c9ac6007849f06931e8`.
- Created through `apply_patch` as an exact initial copy of frozen distribution
  `afbea96badbead846aecc2d3014c19d38375cd2605c225ab0799ebde0ce48774`.
  The initial successor hash matched that baseline before any edits.
- The predecessor source was rehashed after editing and remains `afbea96b...`.
  Used product installation, prior controls and actual evidence are unchanged.

Authority: root adopted the revised source argument
`INSTALLED-VALIDATION-AMORTIZATION.md` (`95bf993d...`) and independent design
review `INSTALLED-VALIDATION-AMORTIZATION-REVIEW.md` (`f2b820ae...`). The broader
63-file/no-census proposal is not implemented.

## Complete intended delta

1. New private `_verify_producer_release(root, manifest)` creates a fresh
   existing directory-validation scope and calls the common verifier with
   `full=False, producer_purpose=True`.
2. `_verify_release` adds the private `producer_purpose=False` selector. It
   rejects non-boolean purpose or simultaneous full/producer purpose. Complete
   manifest validation and physical census still run before any content loop.
   Only exact `assets/lean/` entries skip hashing in producer purpose; every
   previous non-Lean hash, base map, descriptor/template and held-helper check
   remains. There is no caller-provided exclusion list or persistent cache.
3. Only `installed_production_release` and `producer_profile`'s final rebind
   use this branch. Build and explicit full verification still use `full=True`.
   Ordinary consumer launch still uses the unchanged `verify_release(...,
   full=False)` path and therefore hashes its Lean dependency closure.
4. Profile output adds an `installation_validation` scope string specifying
   producer purpose, complete census, existing non-Lean hash selection, and
   **not** complete payload integrity. Schema/status and all existing profile
   bytes, metadata validation and pending-last-unlink semantics remain.
5. The generated README and function docstrings distinguish ordinary/full
   validation from producer-only hashing. They explicitly require trusted
   bootstrap/OS configuration not to load producer dependencies from
   `assets/lean`; this mode is unsupported when that premise fails.

The fresh entry-bound correction is owned separately at
`installed_production02/release_production/operator.py` (`1141f160...`). This
distribution edit does not alter or adopt that file by itself. Root may later
select both exact files in one distribution assembly.

## Invariants and scope

Missing/extra files, case/path aliases and reparse targets retain the complete
census/manifest refusal behavior. Only altered content in an existing unused
Lean payload is deliberately no longer a producer-purpose integrity failure;
ordinary/full verification still rejects it. Production source31, support49,
constructor60, child interpreter584, import policy, explicit input pins, host
calls, evidence rules and finite allowances are unchanged by this file.

The reduced work is the previously identified unused Lean hash loop, not all
installation validation. Full manifest parsing and complete physical census
remain. The source does not claim a measured latency improvement or a bound
independent of installation size. It creates no new trust/funding authority.
The preexisting trusted-local Windows loader/filesystem assumptions remain;
no claim of hermetic execution or hostile-local-mutation isolation is added.

Root retains source review and finite execution selection. New controls are
being authored independently; no passing predecessor suite is rerun or edited.
One subsequent fresh profile path can test actual integration after assembly,
without a new mathematical proof campaign.
