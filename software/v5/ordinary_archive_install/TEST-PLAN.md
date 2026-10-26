# One archive-only installation gate

2026-10-26. Source preparation only; no execution has occurred. Root selection:
`research/cycles/v5-2026-10-26-local-discovery/ARCHIVE-INSTALL-SELECTION.md`.
Root owns the exact launch selection and adoption; independent source review
must precede any launch. Existing product, archive, inputs and evidence stay frozen.

## Decision-changing question

Can the exact already-adopted 143-payload source ZIP supply one native build,
all four public overlays with fresh actual generated receipts, and a final
public inert query without borrowing a product source or binary from the full
checkout? This is source-distribution integration, not repeated native correctness,
independent-host deployment, mathematical growth or complete v5 qualification.

The sole driver is `test_install.py`. It imports only Python standard-library
modules. It does not implement an installer, product API, overlay, new archive,
repair/retry mechanism or mathematical test. It invokes existing public commands.

## Exact inputs and invocation

The driver requires absolute paths for these arguments:

```text
--archive PATH --archive-receipt PATH
--native-type PATH --bindings PATH
--python-runtime DIRECTORY --lean-runtime DIRECTORY --output FRESH_DIRECTORY
```

Run with the approved Python `-I -S -B` inside the existing `Run-V5-Check.py`
outer Job, with the canonical root as explicit cwd. The output must be a fresh
leaf below the canonical root, separate from all selected inputs and runtimes.
Do not launch this driver without the enclosing Job.

| Input | Retained path / exact SHA-256 |
|---|---|
| ZIP | `experiments/v5-local-checks/transport-release-handoff01/suite/packed/source.zip`; `897a6eb57056b911b200551413c65ce7788ba3d448ff8b6b8c143d883180ebd0` |
| External ZIP receipt | Adjacent `RECEIPT.json`; `053bdcf14f7c67a4685081c0f6044a9b76defec89907040b28a5954e05ba075b` |
| Manifest within ZIP | `SOURCE-MANIFEST.json`; `f1beab01d43e4b5fc6d7b9999ff2795598e3f2ee77c0dc85f1d99e82a15b31f1` |
| Native-type data | `experiments/v5-local-checks/ordinary-query-public-01/public/query-local/native-type.json`; `226bb411b2a7255eabc522f482afd2c199877ad624737fddf7b27ec0f8658480` |
| Known-binding data | `experiments/v5-local-checks/ordinary-query-public-01/public/fixtures/known-bindings.json`; `0ebd5b6de9942a1f9359e23c4d7a36219d30bd71af69c73813de8cfd03d95f2f` |
| Expected inert QUERY | `eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a`, unchanged from `experiments/bounded-public-query01-selection.json` |

Root's outer selection pins the existing 23 named runtime attachments (three
Python and twenty Lean compiler/library files), plus ZIP/receipt/two inert input
files: 27 external inputs. No existing generated product/package is an input.
The supported external runtimes remain Python 3.14.6 and Lean 4.34.0 on Windows
x86-64. This does not make them hermetic, independently authenticated or sandboxed.

## Sequential path and pass conditions

1. Check exact ZIP/receipt pins. Validate the fixed manifest and all 144 sorted,
   unique stored regular-file members, bounded sizes and safe relative paths.
   Extract to fresh `source/` and check the complete byte map/census. No source
   supplement, `extractall`, mutable source overlay or inherited Python import.
2. Run relocated public `ordinary_release_bundle/bundle.py verify` against the
   exact manifest digest; require its terminal verified result.
3. Run relocated `ordinary_bounded_operations/build.py` with source root equal
   to that extraction. Require actual `BUILT_NOT_ADOPTED`, stdout/receipt equality,
   the manifest-pinned builder/source map, the actual 86-input staged map, all
   three direct build Job closures and the nested base compiler Job closure.
   Check actual 146-file package and receipt/PROFILE/installation coherence.
4. Run fair, contact, sparse and transport-release assemblers, each against the
   immediately preceding **new** package/PROFILE/receipt. Fair uses its distinct
   `--base-build-receipt` flags. Others use `--base-receipt` and the extracted
   exact overlay map. Require stdout/receipt equality, expected source identities,
   exact declared changes and censuses 148, 150, 152, 154. Native installation
   bytes must remain unchanged across overlays. No stage uses a historical hash
   for generated native output or a historical package as its base.
5. Run final packaged `run.py` with the actual final PROFILE and `query --`, the
   two retained inert inputs, no catalog/custody/contact/native-check operation.
   Require actual RUN plus clean raw SUPERVISION, the exact expected QUERY hash,
   `mathematical_acceptance=false` and zero reported native-worker CPU.
6. Recheck complete source/final package maps and original ZIP/receipt/query
   inputs. Write terminal `RESULT.json`; any failed condition stops and retains
   `FAILURE.json` where possible, plus partial child diagnostics. No automatic
   retry, permission expansion, archive correction or new test campaign.

The driver preserves every public argv, stdout, stderr, direct exit/reaping and
process interval under its output. The final report records each observed fresh
receipt/profile and final package. Root separately audits the outer Job result;
driver success alone cannot assert its own enclosing Job closure.

## Original resource envelope

Driver cooperative lifetime: **550 wall seconds / 60 driver CPU seconds**, with
one nonrenewable start time. Child CPU belongs to the enclosing Job, not this
process counter. Each public stage must fit wholly inside the remaining original
driver wall budget, with five seconds reserved after its timeout; otherwise it
refuses before starting. No deadline is reset after a failed/slow stage.

| Stage | Public allowance | Direct-process timeout |
|---|---|---:|
| Relocated verification | Existing verifier's cooperative 60 wall / 30 CPU | 20 seconds |
| Native build | 480 wall / 360 CPU / 2048 MiB | 490 seconds |
| Each of four overlays | 30 wall / 20 process CPU | 40 seconds |
| Public inert query | 60 wall / 30 CPU / 512 MiB / four active processes / 1 MiB per log | 75 seconds |

The stage maxima are not additive new grants. If the build uses nearly its entire
allowance, the driver may legitimately stop before a later stage because the
original 550-second budget has insufficient room. Retained native cost was about
60 wall / 53 known CPU seconds and 883 MiB peak commitment, not a success promise.

Proposed enclosing selection: **600 wall / 540 aggregate Job CPU seconds /
2304 MiB / eight active processes / 1 MiB per outer log**. Root chooses and pins
the exact envelope. The extra driver process shares that outer cap; no concurrent
build or unrelated worker is launched. The built-in native stages remain serial.
Per-stage driver stdout/stderr checks are sampled at 50 ms with 1 MiB bounds;
they are not hard disk quotas.

On timeout/error, the driver terminates/reaps its direct child if present and
fails. This does **not** establish descendant cleanup: the enclosing existing
Job supervisor owns full-tree settlement. Nested successful build/query Job
closures are checked separately. CPU in those nested reports is already included
in the enclosing Job CPU and must not be added again. The driver reports its CPU
separately only as a nested diagnostic, not another full-cost charge.

## Honest boundary

The extracted sources and explicit runtime paths exercise a source-only input
contract on this one PC. They do not impose OS-level denial of arbitrary checkout
reads or prove hostile-source isolation. No external network, owner mathematical
state, proof/certificate campaign, publication, license decision, source approval
or independently operated host is introduced. Passing closes this specific local
release-installation gap; full deployable v5 remains open.
