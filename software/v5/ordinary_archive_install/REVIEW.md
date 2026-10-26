# Independent source and finite-selection review

2026-10-26. **SOURCE GO for the single selected archive-installation check.**
No blocker found in the complete driver and test plan, conditional on execution
through the selected enclosing Job. No driver, product import, compiler, test,
network request or protected-state operation was executed by this reviewer.
This is not a runtime pass or permission to repeat a failed stage.

## Exact reviewed selection

| New file | SHA-256 |
|---|---|
| `test_install.py` | `7b201b063012ffb93781dff0bfade528506429d40cc5a0d8e942db196c6b034c` |
| `TEST-PLAN.md` | `a2f14b80ffc0351546600ca97d7552daf9503e4fdb1599631a2ec2238b9d0e8e` |

Root's proposed `experiments/archive-install01-selection.json` has SHA-256
`ff55b721aab172dc3f3b3a61bd35fbc70eb6f1a7b149261f0671a4266c36ec74`.
Independent read-only hashing confirms all three source pins, all 27 external
input pins and this selection hash. The 27 are 23 named runtime attachments,
the existing ZIP/receipt and two retained inert query inputs. The selected
`experiments/v5-local-checks/archive-install01` output is absent at review time.
CLI flags match the driver, all external paths are absolute, and the selected
Python is invoked with `-I -S -B`. No existing generated package is passed in.

The selection's outer envelope is 600 wall seconds, 540 inclusive Job CPU seconds,
2304 MiB, eight active processes and 1 MiB per outer log. It fits the retained
runner's ceilings. The driver has one 550-wall/60-own-CPU-second cooperative
allowance; native build, overlays and query retain their existing finite limits.
The outer Job includes the extra driver process and native descendants. The
source uses sequential native lanes and overlays, not parallel build fan-out.
The exact original allowance can end unsuccessfully; no performance promise is
inferred from the earlier approximately 60-second build.

## Composition argument

The missing gate is genuine: prior source packing, native building and individual
overlays passed separately, but did not establish this entire archive-only chain.
The driver calls existing public commands and adds no product installer, API,
semantic policy or negative-test campaign. Reused public build, assembly and
launcher contracts were traced at their actual current sources. Read-only ZIP
hashing confirms the archived bounded/base builders, source map, bundle utility,
four assemblers, final launcher and query entry match those reviewed source bytes.

1. **Exact source acquisition.** The driver requires the already-adopted
   3,789,448-byte ZIP and exact external receipt. It binds the 21,331-byte
   manifest and checks precisely 144 sorted unique regular stored-file members,
   safe names, bounded sizes and each raw content hash before writing that file.
   Extraction is exclusive/fresh, with a complete files-and-directories census
   and hash check. Only the manifest and its 143 payloads enter `source/`.
   There is no arbitrary ZIP extraction, source supplementation or checkout copy.
2. **Actual relocated verification and build.** The public bundle verifier must
   return its exact verified status/manifest/count. The bounded builder receives
   only this extraction as source root and the named external runtimes. It stages
   84 source-map inputs plus builder/map; the driver verifies the actual 86-input
   SOURCES receipt against the archive. It requires build stdout/receipt equality,
   actual source identities and the exact 146-file package map. It checks all
   three direct native-build Job reports and the nested base compiler Job report
   for zero exit, reaping, closed Job, zero active/terminated processes, no cleanup
   error or termination request, and known finite CPU.
3. **Fresh receipt chain.** Fair uses `--base-build-receipt`; contact, sparse and
   transport use `--base-receipt` and their exact extracted overlay maps. Each
   stage's inputs are the immediately preceding fresh package, PROFILE digest
   and actual receipt digest. The driver compares stdout to saved receipt,
   validates predecessor bindings and selected assembler/changes, and applies
   only the declared changes to its prior exact file map. Censuses must be
   146 -> 148 -> 150 -> 152 -> 154 including PROFILE. Installation identity and
   native files are preserved across overlays; generated identities are not
   forced to match an older build. The final complete package map is checked
   independently with standard-library file hashing.
4. **Real packaged entry, inert operation.** Final `run.py` uses the new actual
   PROFILE and supported `query --` grammar, with no catalog/custody/context
   arguments. The retained query entry's manual branch neither opens owner state
   nor launches native checking or discovery. Both public RUN and raw supervisor
   closure must pass. The query result must bind both exact old inert inputs,
   report no mathematical acceptance/worker CPU, and yield expected QUERY hash
   `eb611ed660111779f3bf1a05c044c2a362735d08eb91f7a6151ea80d9108c16a`.
5. **Preservation and finalization.** Source and final-package complete maps and
   the original ZIP/receipt/query inputs are rechecked. Every public command has
   fresh argv/log/process evidence. Success is written only after all stages.
   Any failed check stops the chain and preserves partial outputs; no fallback,
   silent retry, repaired archive, historical receipt or allowance renewal exists.

This establishes an appropriate test oracle for the proposed positive chain;
it is not evidence that the chain has already run. The selected source archive
does not include the separately tested selected-export companion, and this
operation does not silently integrate it or enlarge the archive's release scope.

## Boundaries that the outcome audit must preserve

- `public()` times and reaps its direct process. On failure it terminates that
  process, but it deliberately does not claim independent descendant cleanup.
  The enclosing Job must settle the whole tree. A driver RESULT alone is
  insufficient: adoption requires the outer raw clean supervisor result too.
- Each stage needs its timeout plus five seconds remaining in the original
  driver wall allowance. The per-stage maxima do not all fit additively and are
  not new global grants. A slow successful build can leave insufficient time
  for the next stage; that must remain an incomplete run, never a resumed pass.
- Native/query Job CPU and driver CPU are nested inside outer Job CPU. Add only
  the separately reported outer-runner CPU to that inclusive charge. Peak Job
  private commitment is not total host memory. Log polling is not a disk quota.
- The retained runner uses its already pinned supervision infrastructure outside
  the archive; that is test infrastructure, not a borrowed product build input.
  Exact extracted/staged paths and compiler environment controls test the intended
  source-input contract on this PC. They do not enforce OS-level denial of every
  possible checkout read, sandbox hostile code or make the external toolchain
  hermetic. Stable owner-controlled files and approved runtimes remain premises.
- A native build plus inert manual query is not mathematical native intake or
  execution of every produced native binary. It does not demonstrate public
  networking, independently operated hosts, useful growth, worldwide deployment
  readiness or full v5 completion. Existing component tests are reused only within
  their stated scopes. No license or publication decision is made here.

Root owns the single finite launch, actual saved-output review and adoption.
No source change was requested or made by this review.
