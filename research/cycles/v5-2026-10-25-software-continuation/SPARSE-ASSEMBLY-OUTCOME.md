# Sparse assembly01: independent saved-output audit

Disposition: **PASS, file-only assembly boundary**. The selected sparse successor
was assembled exactly from its selected contact predecessor and twelve-payload
overlay. This does not adopt its behavior, establish a search/growth speedup, or
complete v5. Reviewer: `concept_software_bridge`; root owns adoption and execution.

## Evidence identities

Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.
Operation: `experiments/v5-local-checks/sparse-access-assembly01`.

| Saved evidence, relative to operation | SHA-256 |
|---|---|
| `selection.json` | `4199da4d7e92100b7f4e2569908e523bdd6c01392bb4e33266bf35d2a7441f2c` |
| `RESULT.json` | `87a17188bce34e6e691374d1297ad18baa4fc2ae69bab42c4388305c59963519` |
| `assembled/ASSEMBLY.json` | `b138a6402a921ea1b7690a805cdab5d6bef2a3484659ff970eb4726dc90ba1a8` |
| `assembled/package/PROFILE.json` | `97f93cc66f77ebcecd7a3a341baaaf4725236a8dec5fb9cee3c3e67d478f2834` |
| `command/stdout.txt` | `7abb89fe7166f459ec5a4de532fe0bb6ad95f2bda88234e69b144a7bc151da99` |

Selected assembler is SHA
`3c2a197e0ca159a9472ad3535897d7bd2098399cd43efc104871d63abcb10b71`;
overlay is `e8c14ecee1ba1a95c5ff195e00346d4682e244820dc10300711fe3cc13c8987f`.
The baseline remains the contact assembly01 package with PROFILE
`3d127796190ca3d049bd956288025c10c4ac7e383a15685aca6ea8d2fbc61479`
and receipt `02739f6f44aeb0d56765dea12f82a5e195c1040379db9407221254d7f2dbe79d`.

## Independent checks

- The saved selection has the approved hash. All 17 preserved source snapshots
  and their current canonical source counterparts match its pins. All 154
  external runtime pins were independently rehashed, including every baseline
  file, predecessor receipt and the three selected Python runtime files.
- The actual baseline census is 150 files. Starting from those selected baseline
  identities, replacing the twelve overlay entries and regenerating PROFILE
  gives the exact actual 152-file output census: no missing/extra output file and
  no reparse point inside the package. Every output length/hash matches this
  independently reconstructed map; no product code was imported to check it.
- PROFILE contains the exact 117 expected auxiliary roles: the predecessor's
  roles with the nine non-document replacements and `pair_access.py` addition.
  All role lengths/hashes match. Schema, author-worker binding, helper paths and
  installation-manifest binding remain unchanged.
- The 28 installation payloads and all native/helper payloads are unchanged.
  The actual installation manifest is still
  `32236aa3d7bcbf4369a56a4988c75da80593bebd4b756694f079664036e42ae2`.
  The six documentation pins match their actual output bytes. README and
  SPARSE-SEARCH are selected new documentation; the other four are unchanged.
- Receipt accounting agrees: 151 non-PROFILE files, 117 auxiliary files and
  139 unchanged non-PROFILE payloads. `changed_or_added` records the approved
  twelve-file overlay. Saved stdout parses to exactly the same receipt object.
  The resulting PROFILE hash equals the receipt's reported hash.
- The outer saved result selects the approved isolated argv, reports exit zero,
  direct child reaped, Job closed, zero final active processes and no cleanup
  errors. Stderr is empty. These facts support a completed file-only operation,
  not compiler execution, native verification or mathematical acceptance.

## Costs and remaining boundary

The recorded total wrapper elapsed time is 4.7116544 seconds. Command elapsed
through cleanup is 4.615674 seconds; measured Job CPU is 1.296875 seconds;
outer wrapper CPU is separately 0.328125 seconds. The command report's
supervision CPU of 0.03125 seconds is not added again as an independent full-cost
measurement. Peak recorded Job private commit is 17,584,128 bytes. The operation
fits its selected 90-wall/60-CPU-second, 512-MiB, three-active-process envelope;
the selected limits are resource containment, not a hostile-code sandbox.

This audit used only saved JSON/text, file census and independent hashing. No
rerun, import, syntax check, socket, native work, Git mutation or used-input edit
was performed. Focused behavioral controls and any public forwarding smoke need
their separate root selections and actual outcome audits. The assembly is still
labelled `ASSEMBLED_NOT_ADOPTED`; this pass does not silently change that status.
