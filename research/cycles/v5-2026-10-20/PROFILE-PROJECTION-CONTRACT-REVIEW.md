# Independent contract review: bounded base projection

2026-10-20, adaptive_audit. Source/theory review only; no implementation,
test, network activity, build or Git mutation.

Reviewed full `PROFILE-PROJECTION-CONTRACT.md`, SHA-256
`25618050d4a7e70ced003856e390b87b9090b442ced6324dd544889e422b08a1`.
Canonical root: `E:\Distributed Trustworthy Mathematical Knowledge Network`.

## Disposition

**GO for root's proposed source implementation scope. No blocking contract change.**
This is a complete small operational seam: a separate finite materialization
operation and ordinary HTTP/advertised service selection of the retained result.
It is not an unserved metadata helper, silent cross-profile alias, multi-profile
router or new mathematical trust mechanism.

The four proposed files are sufficient in principle. Runtime selection and
implementation approval remain separate. The current installed candidate does
not gain the feature until actual integration/adoption.

## Principal review findings

### Installed reachability and unchanged old behavior

I inspected `distribution_coherent/distribution.py:502-517`:
`builtin_parameters` currently admits exactly the command's V1 schema and then
overwrites the field. Merely adding V2 to the services would leave the installed
entry unreachable. The contract correctly requires a matching explicit V2
allowlist, preserved selected schema, unchanged omitted-schema V1 default and
unchanged reserved `serve-advertised.location.installation_root` injection.

Likewise `serve_advertised._parameters` currently replaces the proxy schema with
`H.SCHEMA`. Its V2 branch must deliberately use HTTP V2 and retain `index_view`;
otherwise it either loses selection or refuses the extra field. Cross-command,
unknown-schema and V1-plus-selector refusals are meaningful control cases.
Preserving V1 response shapes avoids forcing unrelated consumers to migrate.

Materialization through the existing trusted owner `run` entry is operable.
It still has the installed runtime-mode/configuration requirements; documentation
must not advertise it as a new runtime-free built-in command. No mathematical
issuer or native/proof execution is required by the helper itself.

### Target ownership and lifetime

The fixed `<workspace>/base-projection-index` subtree avoids the unresolved
case where two different workspace locks could open one arbitrary external
projection database. One actual workspace owner plus a serialized borrow token
is sufficient for the stated trusted-owner, nonconcurrent calling model.

The contract refuses live clients/reserved grants and retains the original
workspace adapter/index. Its handle owns only the new target store; it borrows
the source workspace and original custody. Close the service first, the target
second and the workspace last. The old workspace closer cannot establish target
closure because it does not know this fourth store. A failed constructor/close
must preserve an accurate failed-cleanup outcome, even after best-effort release.

No claim is made against a hostile Python caller mutating those same objects.
The public helper must not imply that its borrow token changes the existing
workspace methods into a general concurrent ownership protocol.

### Exact served view and route identity

Existing HTTP offers select `index.snapshot()` (the latest snapshot). Requiring
the requested expected hash to equal the reopened target's actual latest and
verifying the snapshot is therefore necessary; selecting only a retained old cut
would misdescribe what the existing provider serves.

The contract derives both HTTP/location namespace from the actual selected target
and reports its real cut. It preserves the original module/packet objects and
foundation/policy checks. No materialization runs during this service invocation,
and the end-of-service latest check detects unexpected target changes under the
stated owner model. A deliberately selected partial cut is allowed without an
all-publications or synchronized-projection claim.

Existing location routes contain opaque feature hashes. Deriving route keys from
the target namespace does not prove the owner compiled each feature in that
namespace. The contract correctly leaves that compilation responsibility explicit
and does not invent validation from absent source specs.

### Failure, reconciliation and costs

The exact finite list, target quotas, maximum 64 exports, bounded report and
deadline prevent implicit corpus-scale work. I checked the selected codec:
`Limits.max_bytes` is 16 MiB and canonical export encoding enforces it. Reserving
one such maximum before each read and retaining it on unmeasured failure is
conservative under this codec/storage model. This is not a physical-I/O or peak-RAM
bound; the contract states that distinction and retains enclosing hard limits.

Stopping on the first failure makes the acknowledged prefix precise. An exception
after entering `admit` is conservatively unknown even if a typical SQLite error
rolls back. The last acknowledged snapshot must never be presented as the actual
latest after such a failure. A success requires final latest agreement and cleanup.

No additional per-item durable ledger is necessary for correctness. With hard
termination or missing final report, the batch is UNKNOWN; existing target
transactions survive and the pinned finite input identifies what was attempted.
A later explicit same-list idempotent projection reconciles under a new budget,
without deleting the earlier failure or refunding costs. An unusable partially
created target is a preserved refusal, not permission for automatic reconstruction.

Capturing `Store.work` before its next reset and recording unavailable constructor/
failure counters as unknown is necessary. Inclusive CPU/wall and enclosing Job
consumption are separate from those index-work counters; do not add overlapping
CPU figures or treat missing failed-item counters as zero.

## Focused implementation checks

- Avoid a top-level import cycle: the helper needs workspace-mode selection and
  the service needs the helper. A local import at the new selection seam suffices;
  do not refactor unrelated service behavior to solve this.
- Acquire/release only the matching borrow token, clean constructor failures and
  verify the real target database is closed. No normal service listener may start
  before expected-latest validation succeeds.
- Keep V1 field/report paths untouched; explicitly route V2 through dispatcher,
  advertised proxy, selected provider, READY/final result and cleanup.
- Record failing read/admission attempts before calls can raise, account for
  available failed-call counters and preserve unknown commit outcomes.
- Keep selectors and all data handles operational only. Base index candidates
  still require original mathematical admission before use.

The contract's focused structural controls cover these new boundaries. No new
theorem, expensive proof, broad repeated network campaign or global-scale test
is needed to decide this compatibility fact.
