# Supported fresh-build transport integration

This file-only integration applies the existing bounded-transport repair to an
explicitly owner-approved **actual supported sparse build**, not only the one
historical local build. It changes no mathematics, discovery protocol, custody
rule, native executable or provider implementation. Source availability alone is
not a runtime test pass, supported fresh-build compilation or complete v5 release.

## Build and select actual inputs

Follow the source bundle's build recipe through these stages, retaining each
fresh result and its immediate receipt:

```text
bounded source build -> fair-search overlay -> contact overlay -> sparse overlay
                    -> this transport overlay
```

The final stage uses the sparse overlay's actual `package/PROFILE.json` and its
adjacent `ASSEMBLY.json`. Independently review and approve those exact bytes and
hashes. Do not copy PROFILE, INSTALLATION or receipt hashes from the historical
bounded-transport experiment: legitimate new generated outputs and receipts can
differ. A filename, a downloaded receipt or a past passing report is not approval
of a new executable build. No old installation bound to owner state is modified.

Use approved supported Windows Python with `-I -S -B`:

```powershell
& $approvedPython -I -S -B "$sourceRoot/software/v5/ordinary_transport_release/assemble.py" `
  --source-root $sourceRoot `
  --base-package $approvedSparsePackage `
  --base-profile-sha256 $approvedSparseProfileSha256 `
  --base-receipt $approvedSparseAssemblyReceipt `
  --base-receipt-sha256 $approvedSparseReceiptSha256 `
  --overlay "$sourceRoot/software/v5/ordinary_transport_release/OVERLAY.json" `
  --overlay-sha256 $approvedTransportOverlaySha256 `
  --output $freshTransportOutput --wall-seconds 120 --cpu-seconds 60
```

Variables above are explicit local selections, not defaults or shell environment
changes. Use absolute local paths. The output leaf must not exist; its parent
must exist. The allowances are finite cooperative checks, not hard OS limits;
an outer owner Job remains appropriate for hard containment. Retain partial
outputs and failures. Do not automatically retry or enlarge an allowance.

## What stays fixed and what may change

The source checkout must preserve its supplied paths and exact bytes, including
the fair assembler, network-kit compatibility map, bounded source map and frozen
bounded-transport files. The selected OVERLAY has the existing schema
`DMKN_ORDINARY_BOUNDED_TRANSPORT_OVERLAY_V1` and exactly these three payloads:

| Destination in fresh package | Source relative to `software/v5/` |
|---|---|
| `support/transport/http_provider.py` | `ordinary_bounded_transport/http_provider.py` |
| `BOUNDED-TRANSPORT.md` | `ordinary_transport_release/README.md` |
| `EXECUTION-TRUST.md` | `ordinary_bounded_transport/EXECUTION-TRUST.md` |

The assembler checks the 45 exact noncompiled auxiliary sources, the 72 native
auxiliary role names, all 19 copied installation source/foundation files, the
eight receiver object names and the nine fixed supported named-runtime pins.
Actual generated identities may differ only in those named native outputs.
Installation roles, helper layout and all support commitments must remain
coherent with the selected actual file pins. Runtime pins describe external
attachments; the overlay does not open or certify those runtimes.

The actual input package must have exactly 152 files and match every expected
byte. The new package has 154 files including PROFILE and the same 117 auxiliary
roles. It preserves all native files and all other predecessor payloads, replaces
one provider and adds these two documentation sidecars. Its installation manifest
and implementation identity remain unchanged from the caller's selected build.
Its older README remains as historical sparse documentation; **this sidecar
supersedes any instruction to use sparse as the final transport-ready profile.**

Source hashes identify a supported interface, not correct compilation. Native
code approval remains the owner's responsibility. The resulting `ASSEMBLY.json`
binds copied bytes and the new PROFILE, with status `ASSEMBLED_NOT_ADOPTED`; it
does not grant mathematical acceptance, execution permission or state adoption.
The installation is named supported software, not a hermetic toolchain. Inputs
must be immutable owner-controlled storage; hash checks do not provide a lock
against hostile concurrent writers.

## Prepare and run with the final profile

Use the unchanged
`software/v5/ordinary_bounded_transport/prepare_selected.py`, **not** the older
`ordinary_network_kit/prepare_selected.py`. Supply `--package`, the new actual
`--profile-sha256`, `--request` and a fresh `--output`. Keep both those sibling
directories in the checkout. The final wrapper recognizes the selected repaired
provider among the same 45 noncompiled/72 native roles and loads only the pinned
offline preparer. It does not execute product code or approve a native build.

Use the existing network kit request forms and public launcher after separately
reviewing the generated files. Select the **new final PROFILE** and the original
finite runtime envelope. There is no new configuration schema, contact trust
rule or checking policy. Read `EXECUTION-TRUST.md` in the resulting package before
approving local projects: Lean source execution permission, mathematical validity
and resource containment are distinct. The supervisor is not a hostile-code
security sandbox.

## Existing bounded provider behavior

The unchanged repaired provider reserves a processing slot before TLS handshake.
`max_connections` bounds application-owned slots across handshake, HTTP work and
cleanup. The OS listen queue is separate. It uses nonblocking socket acceptance
and a 10 ms idle poll on supported Windows; scheduler delay is additional.

`max_requests` bounds accepted connection attempts as well as HTTP handler starts.
`accepted_attempts` records acceptance; `requests` records handlers begun, not
parsed/successful requests. Failed or incomplete TLS consumes an attempt. A peer
can exhaust a finite allowance; this bounds work, not denial of service or fair
access. Shutdown closes admission and owned connections before waiting for
cleanup; it does not renew the original service/cleanup deadlines.

This repair establishes neither global availability nor mathematical discovery
speedup. Independent hosting, public security assurance and the complete v5
release decision remain separate from file-only integration. No publication,
license choice, native rebuild or network service is selected by this document.
