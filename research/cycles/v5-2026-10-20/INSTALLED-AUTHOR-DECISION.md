# Installed author failure: missing Lean module closure

2026-10-20, core_growth. Read-only inspection; no compiler, prover, runtime,
retry, product patch or Git action was performed for this diagnosis.

## Exact cause, not a resource hypothesis

`installed-contribution-01` failed after its input reached `READY` with current
I/native admission and twelve groups/fifteen declarations. No successor output
or publication was produced. Its operation ID is
`ae3ffbfb6fb17cbbaf36a9b4a8287cf232936bce7bfb74848d55b3975ee959ef`.

The author-command stderr under that operation's `preparation/author-1/` says:

```text
OWNER_AUTHORING_FAILED failed to open file '...\assets\lean\lib\lean\Init.olean.server': 2
```

The 202-byte stderr SHA-256 is
`06aafe1c2b2ed9982c0c9812dda757bf2f245ac5f423d9e0550900b168fe259a`.
`worker-result.json`, SHA-256
`e50636fe7fd77291a22914bfca811c7f879ba4a129f51a41b778dfba4625d385`,
records native return code 1, no timeout, `WORKER_NATIVE_REFUSED`, no export,
and a reaped direct child. The author process report records 0.59375 Job CPU
seconds, 31,076,352 peak private-commit bytes, zero live processes and clean
closure. Its native-worker wall time was 0.8202449 seconds. Raising memory or
CPU limits cannot provide a missing file.

The relocated profile contains only five DLLs plus `Init.olean`. Those are
the historical minimum owner pins, not the complete importable Lean runtime.
Previous operations pointed at the full retained Lean distribution, so they
did not test this packaging omission.

## Loader-derived requirement

`software/v5/authoring/native02/AuthorLean.lean:840` calls
`Lean.importModules #[{ module := Init }] ... (loadExts := true)` using the
default private import level. In the retained Lean 4.34 source,
`Lean/Environment.lean:2078` reads `.olean`, `.olean.server` and
`.olean.private` for modules. Its private import traversal also requires IR;
where `.ir.sig` is present, the loader reads both `.ir.sig` and `.ir`.
The five-part set for every selected module therefore supplies these loader
branches without guessing which missing file will be requested next.

The retained `Environment.lean` source SHA-256 is
`ee364e4788ce0560c87f621eeb3c4c3dfec62e8db4e15e099fd80e6adc533b86`;
the root `Init.lean` source SHA-256 is
`28b57970b6f0adef586f14939a95362959b698a68463d4a803f81464ad8e0675`.
Lean's `Parser/Module.lean` confirms the header order
`[module] [prelude] ([public] [meta] import [all] identifier)*`.

## Source-closure audit and its assumptions

A second read-only audit superseded the initial line-regex census. It consumed
header tokens while skipping whitespace, `--` line comments and nested
`/- ... -/` comments. Tokens may cross lines. It recognized the exact modifier
order above and ordinary dotted ASCII module identifiers; an unsupported or
non-Init import is a refusal, not silently ignored syntax. The header ends at
the first non-import command, as in Lean's header parser. No file body is
executed. No regular expression is used to infer imports from comments,
strings or theorem bodies.

Actual retained source result:

| Quantity | Result |
|---|---:|
| `Init.lean` plus `Init/**/*.lean` | 649 modules |
| Modules with explicit `module` and `prelude` | 649 |
| Explicit import edges, preserving occurrences | 3,392 |
| Modules reachable from root `Init` | 649 |
| Imports outside `Init` family | 0 |
| Required five-part artifacts present | 3,245 |
| Required artifact bytes | 389,437,304 |

Every source has `prelude`, so no implicit default `Init` import is omitted.
All public, private, meta and `all` edges are conservatively included in
reachability. No flag-based pruning is used. All 648 source modules below
`Init/` are reachable, not merely copied because their filenames happen to
match the namespace.

For reproducibility, the read-only audit computed a 156,426-byte graph
fingerprint input: UTF-8, modules sorted by ordinal name; one row per module:
`module<TAB>source_byte_count<TAB>source_sha256<TAB>imports<LF>`.
Imports preserve header order and duplicate occurrences, comma-separated as
`name:XYZ`, where X/Y/Z are 0 or 1 for public/meta/all respectively. Its SHA-256
is `ecbece96120350a2c14df2b519c6500b82c607a4c17d31c0157ac370dde4bbcd`.
The selector binds that fingerprint and records the complete source inventory
in its separately pinned source-closure checkpoint. The release commits the
chosen graph, exact artifacts and build-input identity; it does **not** embed
or authenticate the raw source inventory for a receiver. The sidecar points to
the selected input, not vice versa. This is selection/audit evidence under the
owner-adopted graph contract, not a receiver proof of source-to-binary identity.
The count 649 is a result, never the authority check.

This is a source-derived closure of the retained toolchain, not independent
decoding of binary `.olean` import metadata or a proof that source and compiler
artifacts correspond. That fixed-toolchain correspondence remains an explicit
local software-trust assumption. The unchanged mathematical output-admission
boundary still checks any produced contribution. A later bounded relocated
author invocation tests runtime operability; the static audit alone does not.

## Smallest principled repair

Root selected a fresh `distribution_complete` successor in
`INSTALLED-REPAIR-SELECTION.md`; old install02 and its failed contribution
remain untouched.

Supply a separate complete Lean support map with the source-derived module
graph and all five artifacts/module. The ordinary release manifest binds every
file and launch verifies all support bytes. Keep the existing small worker
pin list and its explicitly nonhermetic owner-trusted contract unchanged;
do not append thousands of paths to its 128-entry/128-KiB configuration or
increase the preparation owner's 512-MiB pin envelope.

The stable, owner-controlled installation is therefore part of the support
payload contract. This is not a sandbox against a local adversary mutating
files after release verification. No new mathematical acceptance shortcut,
frontend rebuild, checker image or proof campaign is needed.

Only `Init.olean` is already shipped; the additional support is 3,244 files
and 389,431,416 bytes. Without any base-role pruning, the old 6,771-payload
manifest would become 10,015 payloads/917,136,027 bytes, excluding generated
manifest changes. Root's newly selected narrower required-base role should
reduce unrelated payloads, not remove needed Lean support or weaken checks.

## Decision-changing controls only

The successor should refuse a missing sidecar, absent imported module,
unreachable extra graph node, unsupported external edge and inconsistent
overlap with an existing runtime pin. Tiny source-parser controls should cover
comments, multiline imports and public/meta/all modifiers; a changed source
digest or new unsupported header form must fail selection. The graph's
reachability and exact artifact-set equality are stronger than a hard-coded
module-count assertion. These controls do not repeat the prior six cache or
seven distribution tests.

## New source-only selection and controls

Root assigned `software/v5/distribution_complete/select_inputs.py` and
`test_complete.py`. The selector starts from exact frozen distribution02 input
`fcfbbc751148a1f8d730eb88ff0050473d738d4eaf1c2dbb1ef5faa033cb2f6c`,
uses an exact-hash imported pure builder helper and a fresh directory-validation
scope, and emits only fresh `distribution-03-input.json` plus
`distribution-03-source-closure.json`. It never builds, copies an installation,
imports the SDK or invokes mathematical workers.

The graph emitted to the product deduplicates direct module names; the stronger
source fingerprint retains all flagged occurrences. The unchanged six minimum
runtime pins remain separate and overlapping support pins must be identical.
Optional SDK overrides require exactly the three selected existing files and
the new `admission/pin_phase.py`, all at explicit reviewed successor paths.
Every other source row is preserved.

Seven small pure tests cover the header grammar/refusals, source-fingerprint
binding, graph/artifact closure, support-role overlap/scope, exact base-role
projection, every-launch support-pin dispatch, and exact SDK overrides.
Filesystem census/pin dispatch are explicitly mocked in the pure release
controls; no actual installation, native dependencies or complete support
runtime is asserted by those tests.

Current status: cause established; repair source and controls authored, not
executed. No repaired install or successful author result is yet claimed.

Before any control execution, root caught one test-fixture spelling error:
the sidecar key used dotted `Init.Small` rather than path `Init/Small`.
The unused test source was corrected and its complete fixture paths reread;
selector and product sources were unchanged.
