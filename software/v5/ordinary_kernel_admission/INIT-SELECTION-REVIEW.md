# Independent exact fresh init01 selection review

Disposition: **GO FOR ONE FRESH PUBLIC INIT**; root owns launch and adoption.

Selection:
`experiments/v5-local-checks/std-kernel-init01.selection.json`, SHA-256
`a3a4ea1c0c310b51b6a315762fb3f69182d36806b595b7c4eb3b5638c11fb453`.
The reviewer inspected JSON/files only, with no product imports, native/owner/
status call, database or Git operation.

All four source pins and 207 external pins match actual bytes. The selected
package subset is exactly the 154 rows of the audited ASSEMBLY map. The remaining
entries are 23 named runtimes, fourteen retained historical evidence bindings and
sixteen immediate new evidence bindings. The map is within the existing runner
cap; it does not pin mutable owner state. Historical package descriptors occur
only as preserved evidence, not as the invoked package or runtime helper path.

The independently reviewed package outcome and root adoption bind:

| Binding | SHA-256 |
|---|---|
| PROFILE | `60b6e0d6c7d4e7d7761ed5f7ebb2d449afc55547f46f6924f0b93234a5a30f3b` |
| INSTALLATION | `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27` |
| Implementation | `86b6fcce8d8f13479e8131e1a386782b7bda5b6ee579df46e640ca8005affbea` |

The full argv differs from the old reviewed init template only at its run.py
path, PROFILE hash, catalog path, custody path and store ID. Its full outer limits
object is unchanged. Public limits remain 90 wall/60 CPU/1280 MiB/three processes,
under outer 120 wall/90 inclusive Job CPU/1536 MiB/four processes; diagnostics,
quotas and runtime arguments are unchanged. No status, intake or recovery is part
of this selection.

The run output `std-kernel-init01`, catalog `std-kernel-catalog01` and custody
`std-kernel-custody01` were all absent. Free disk was 48,404,779,008 bytes, exceeding
the 3 GiB premise. The store ID matches the reviewed deterministic fresh label:
`fb625cc1b7d03d081e45bbcf73f7d59765f04a64a402484f23d00ac3e60ce4e7`.
No old owner is reopened under the new implementation.

After this single operation, independently inspect the actual checked basis,
new implementation/store/path/limit bindings, child mathematical report and all
public/outer closure evidence. Only that successful result may supply a parent
for a separately reviewed intake selection. Refusal or uncertain completion
preserves state and does not authorize an automatic retry or private repair.
