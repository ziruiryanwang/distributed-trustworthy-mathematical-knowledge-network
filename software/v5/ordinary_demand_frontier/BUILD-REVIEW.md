# Four-helper build source review

Disposition: PASS for a separately selected bounded build. This is source review,
not execution, helper qualification or package adoption. No blocking fix found.

Reviewed `build.py` SHA-256
`3efa71d4882d731cd4a67fd29ba3c4a8c02b3c6c75ececd79534f63ca0846cdb`
and `BUILD-PLAN.md`
`7d37f1fc26aed7c57a141462b7fe9a6d267d2f94d8928b7184b13b5ade056187`.
The actual supervisor is `tools/Run-V5-Check.py`, SHA-256
`44a7bf1bd26ac628c6020aa87116092eb9f03761b9ba67c7ad80e67290340651`.

The adapter requires isolated Python, canonical cwd, the selected executable,
snapshot location and one fresh sibling `native` output. It creates no owner
state and imports only the hash-pinned file utility module. Ordinary-path checks
reject redirected/hard-linked files. PROFILE and INSTALLATION hashes, their
binding, all 70 baseline helper artifacts, explicit runtime files, four source
files and final unchanged inputs are checked. The enclosing source selection
must pin the two changed sources; their expected hashes are deliberately not
hard-coded in this adapter. The unchanged two sources have explicit pins.

LEAN/PYTHON/ELAN environment variables and ambient PATH are removed. Fresh
compiled objects precede baseline helpers and runtime in LEAN_PATH. Compilation
is sequential in dependency order. The dependency chain imports each rebuilt
predecessor; unchanged baseline helpers do not import this changed chain. Exact
final census requires all five parts for all four modules, with bounded aggregate
output size and source readback. There is no fallback/retry or success report
after a failed compile. Thus old baseline files cannot satisfy the final fresh
output census. This assumes owner-controlled immutable local files, not a hostile
concurrent writer or hermetic toolchain.

Proposed outer limits are 120 wall seconds, 90 aggregate Job CPU seconds, 1536 MiB,
four active processes and 1 MiB per stream. The previously used supervisor assigns
the child to a finite Job and verifies closure; compiler children use only
CREATE_NO_WINDOW, with no breakaway. The adapter's wall check cannot interrupt a
blocked compiler itself; the outer Job provides that containment. Require the
actual selection and terminal Job report, including cleanup, before adoption.

For later packaging, the shortest suitable template is
`ordinary_intake_progress/assemble.py` (SHA-256
`b112e308982d79f4b7b087341962000389db48e3a85f4508a781eac6d8314a0f`).
It already copies a 154-file package without loading product code, preserves the
installation identity and commits PROFILE last. Extend its replacement map to
four Python files and twenty actual helper outputs. Preserve all eight documents,
117 auxiliary roles and every installation byte. Do not invoke its historical
entrypoint or the receiver installer. Actual helper hashes must come from the
adopted build receipt; equivalent rebuilt parts need not differ byte-for-byte.
