# Correct the installed check's public request, not the product

Root, 2026-10-20. Read/adopt failure audit `c05b690a`. Installed actual01
remains failed: 32 MiB violated the frozen launcher's 64 MiB minimum output
allowance before provider boot. Only the reader role ran; its close and the
outer Job were clean. Known CPU 11.15625 seconds, wall 19.257929 seconds.
All used adapter, request, selector, source snapshot and evidence bytes remain.

Source inspection of public launcher, boot, service and location constraints
supports one fresh narrow adapter `installed_service_check02.py`:

- Set the caller output-byte allowance to the documented minimum 64 MiB.
  This is a sampled output limit, not a RAM allocation. Do not change product
  validation, execution time, CPU, memory, process, network or proof budgets.
- Use a fresh inner operation name and fresh outer evidence destination.
- Distinguish expected roles from observed READY roles. Append a READY role
  only after its actual readiness checks; do not infer spawned process counts
  from an intended two-role fixture description.

`core_search` owns this new adapter and its exact-delta/source-contract note.
Root owns fresh `Select-InstalledService02.ps1`; it changes only adapter source
path and fresh outer name from the reviewed predecessor selector.
`core_release` reviews the changed boundary and audits saved output independently.
No product rebuild, integrity bypass, failed-run overwrite or warm-path
performance claim is permitted.

After exact source/selector clearance, root may prepare and select one operation
under the same original 120 CPU / 600 wall seconds / 512 MiB / six-process
envelope. The original adapter-entry deadline remains 570 seconds. No operation
is launched merely by this source selection. The selected connected installation
and release identity `69d9456e` remain unchanged.

Full v5 remains active and incomplete. Source work on typed-row refinement
continues in parallel, not another RAM/proof campaign.
