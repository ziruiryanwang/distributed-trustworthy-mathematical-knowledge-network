# Focused remaining-capacity controls

Root-authored source, 2026-10-28. No execution yet. The independently reviewed
candidate has only eight new lines in the provider's per-request admission path.
Use the already adopted dedicated-host package, PROFILE
`21bcb169cced5d85c3d2272265ef1f24f6848fbe2da0d2ab3f3acfe27697bba7`, as the exact
unchanged support source. The test loads its pinned Python modules without native
support loading, creates one disposable SQLite custody store, and uses the
candidate provider with the real parser and ordinary dispatch.

The fixture is the already retained observation-growth-produce01 unit
`c59ee7bd4eed61193dc06729ca76e28887ad83171f11173353e93bb46305c2c4.json`,
26,650 bytes, SHA-256
`bf13287aed53c34ccf58798d3e77ab0df1b60f74ed780641de88a9dc7fd813bd`.
This is an inert byte fixture; no theorem is checked again. Required input modules
are pinned by the package PROFILE and installation manifest. All loaded sources
and fixture bytes are checked again after controls; no existing state is opened.

Seven groups cover the changed boundary:

1. A real locator plus complete evidence under a 30,000-byte provider grant,
   even though client maxima are 1 MiB and 8 MiB. Exact returned bytes and
   input-request preservation are asserted.
2. A grant one byte below the real unit size refuses before the BLOB SELECT;
   a SQLite trace distinguishes length lookup from materializing the object.
3. Absent evidence and a Boolean original cap refuse without successful output.
4. Exact-budget evidence succeeds; any following locator receives no output.
5. A writer held at its first drain keeps the charge and reservation; competing
   admission refuses, then the remainder becomes usable after release.
6. Cancellation during the held write retains the body charge and releases
   its reservation.
7. Preview's exact advertised size and a discovery offer keep their previous
   whole-cap refusal behavior.

StreamReader inputs and bounded controlled writers isolate the changed path.
No actual network or native process is needed; TLS and socket admission are
unchanged and their previous tests are not repeated. External execution will use
the existing bounded local-check runner: at most 60 wall / 20 CPU seconds,
512 MiB, one process and 1 MiB per log. Root will capture exact reviewed source
pins and a fresh output before selecting the one run. A failure remains saved;
there is no automatic retry or grant renewal.
