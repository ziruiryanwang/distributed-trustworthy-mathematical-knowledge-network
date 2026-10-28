# Directory kit: actual archive and relocated preparation

2026-10-28. **PASS for the completed local pack and changed operator handoff.**
growth_design_audit inspected saved JSON, source snapshots and file bytes only.
No product module was imported or executed; no packing, preparation, lookup,
search, proof, Lean, owner/database or network operation was repeated. No Git
operation or existing evidence change occurred. Root owns adoption.

## Exact coherent distribution

The sole recorded pack execution used selection
`45975f22215feefe6cc412e04e5b0223aab15b47c1b6a78c8f97eae3d2343b18`.
Its copied selection is byte-identical to
`experiments/v5-directory-kit-pack01-selection02.json`. All four saved source
snapshot pins match, including the exact payload selection
`579864e032412aa1d4290ffafeb85b9dc6ff4099e804d5bddf711fee6e6cf2e6`.

The earlier `experiments/v5-directory-kit-pack01.json` has an empty source map,
SHA-256 `ba757b6765ed8d453428d568a4c0429bdcb7e1795f80f9083662c6136f6e1a09`.
It is preserved preparation, not the selection of the recorded run. EXECUTION
records that the PowerShell precedence error was corrected before execution;
this audit does not convert that preparation defect into a failed or successful
runtime attempt.

The new handoff is under
`experiments/v5-local-checks/directory-kit-pack01/packed`:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| commons-local.zip | 42,991,391 | ed50cc5e956c5a25df1ea02d22ce3c608e3f9d73ba50b4d7c35598e60023ed99 |
| commons/KIT-MANIFEST.json | 38,231 | efb1282f9997ccc6d1a0c127bf971726538a0be41ab15a3e06734012717a21cf |

Independent byte inspection confirms:

- Exactly 264 payloads in the manifest and extraction, plus KIT-MANIFEST itself;
  no extra extraction files. Every payload's size and SHA-256 match both the
  manifest and exact selected origin.
- All 160 package files are byte-identical to the adopted
  name-directory-assembly01 package. Its census also matches exactly.
- The 93 mapped source inputs match the selected source map and source origins.
  Builder/map contribute two additional files, and the nine kit/operator/preview
  companions complete `160 + 93 + 2 + 9 = 264`.
- The ZIP has exactly 265 unique members. Every member's actual uncompressed
  size/hash matches the payload manifest or manifest pin; the archive's own
  size/hash match the external receipt. This is actual artifact inspection, not
  repetition of hostile-archive control cases.
- Package PROFILE is unchanged:
  `7687d5276d8a7edc0beeb7066e4cbaae16529b0e88d8a0728b003dad04a4dd34`.
  Installation manifest is unchanged:
  `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.
  No pattern-profile path occurs in the selected kit.

Pack stdout parses identically to packed RECEIPT.json and reports
`PACKED_AND_RELOCATED_LOCAL_KIT` with `VERIFIED_LOCAL_KIT_BYTES`. The three
selected external Python runtime files were also rehashed against their retained
pins. This establishes selected byte identity, not runtime hermeticity or new
native correctness. No native build was performed by either recorded operation.

## One relocated directory-to-find handoff

The saved `directory-kit-relocation01` execution used selection
`69105fb1521dee84708e16a4c47a391388055812d63cedfa7d99d171b691dfa1`.
Both copied source pins match. The controller's saved result agrees with its
stdout and reports `PASS_RELOCATED_DIRECTORY_FIND_PREPARATION`.

Its single inert CLI child used the operator files from the extracted kit. The
saved wrapper result identifies the current historical-directory interface and
50 known noncompiled roles. Its nested preparation result equals the retained
RECEIPT.json, with `commands_executed:0`, `protected_state_opened:false` and
`mathematical_acceptance:false`. This is an interface handoff, not a public find.

The exact input was the previously completed historical directory lookup result
`f6ce728d0d5396ddc99fb9eb71a158a98daa6de0b4a897e6ddabd860cad43822`.
Its specs equal the prepared request's specs and the prior authentic find
configuration. Independent inspection establishes the stronger actual fact that
the prepared config is **byte-for-byte identical** to that retained config:
654 bytes, SHA-256
`463c3aee55ded3338098dca9f092b6532cd05c501f412deda3db601c6cb758f9`.
The runtime control itself asserted parsed JSON equality; that assertion is not
retroactively changed.

All preparation receipt input/output size/hash pins match actual files. Prepared
arguments select the current PROFILE, `peer` entry and `find` command with the
exact config hash. The designated `unexecuted-find` output does not exist.
Child stdout/stderr hashes match the saved control result, and stderr is empty.
The inspected trusted runner invokes only the inert preparer, not the prepared
product command. Owner opens, network calls and native calls remain zero for
this control; no mathematical acceptance is claimed.

## Closure and cost

Both outer operations ended `COMMAND_EXITED_ZERO_AND_CLOSED`, child exit zero,
direct child reaped, Job closed, final active processes zero, no requested
termination, no terminated processes and no cleanup errors. Their actual limits
match the saved selections, and both outer stderr files are empty.

| Operation | Job CPU seconds | Outer wrapper CPU seconds | Known total CPU seconds | Outer wall seconds |
| --- | ---: | ---: | ---: | ---: |
| Pack | 1.906250 | 0.109375 | 2.015625 | 7.0954452 |
| Relocated preparation | 0.218750 | 0.062500 | 0.281250 | 0.4284239 |
| Total | 2.125000 | 0.171875 | **2.296875** | **7.5238691** |

Nested controller/preparer counters and the supervisor subcounter are not added
again. These are the two recorded operation costs, not this read-only audit's
cost, initial mathematical development cost or a whole-network growth measure.
Peak Job private commitment was 147,365,888 bytes for pack and 32,485,376 for the
relocated preparation. The recorded finite grants do not create hard disk quotas
or a hostile-source sandbox.

## Evidence and claim boundary

Paths below are relative to `experiments/v5-local-checks`:

| Saved file | SHA-256 |
| --- | --- |
| directory-kit-pack01/RESULT.json | f3773bdbc2c79196d384aa602871adb3303f41acde8b6accc93665c22e6901bf |
| directory-kit-pack01/packed/RECEIPT.json | bee23b466ba9d19a3ab69e1b7f621aa99cd776ea708810930d6050d44faab5e0 |
| directory-kit-relocation01/RESULT.json | c519902760c18d63496d19c8133936592cb46e54decc972c3bc74312c032f35d |
| directory-kit-relocation01/checks/RESULT.json | 82fcd9280124f72745a4bc4e05594abb82094af52101b5136c600f4b9ee35cbd |
| directory-kit-relocation01/checks/prepared/RECEIPT.json | ac18ee64ef665e0cc9a6a5723d82f45fb01ac6ff60fd36bce8d1a675ab3dfec3 |

This closes the coherent packaging and changed relocated preparation boundary.
Existing name-directory algorithm/export/lookup controls, preview rendering and
mathematical reuse outcomes remain their separate adopted evidence; none was
rerun or enlarged by this kit. The guide's actual shared-carrier discovery example
is historical capability evidence, not the result of this preparation control.
Source compilation, independent hosting, broad relevance, useful-growth speedup
and full-v5 deployability are not established here. The kit stays local and
unpublished, with its license undecided and the full project goal open.
