# Exact generated geometry17 layout selection review

2026-10-17. Independent reviewer: `memo_independent_review`.

**Disposition: PASS for the exact one-layout launch plan, conditional on root's
fresh launch headroom and no-overlap gate.** No launch, product import, test,
compiler, native call, guest execution or proof call was performed in this review.
The canonical workspace guard passed. This review does not qualify execution,
proof production, mathematical admission or v5 completion.

## Exact selected bytes

All paths below are under the canonical project root. These four files are in
`experiments/v5-local-checks/` and were independently rehashed from disk:

| File | Bytes | SHA-256 |
|---|---:|---|
| `geometry17-layout-01-selection.json` | 21,441 | `a717a88af4df86338888582ad48dbaad7dccdce7c307d471d51828c0bc071aa4` |
| `geometry17-layout-01-configuration.json` | 2,415 | `146b0ba5667eed4560c36d88699dd8becbf951c15506eeb1fa49628697774478` |
| `geometry17-layout-01-profile.json` | 14,046 | `0677abddd87f95edadcda9696b316248c44ad0d95fa321fa71182c0c10a5cc96` |
| `geometry17-layout-01-packet.json` | 561,844 | `359f2a601b6354c9e6a87d7887f56ff8996681e11046bed86618d10b8c0a0af6` |

All **28 source pins**, totaling **255,710 bytes**, match the actual originals.
Each also appears with the identical hash in the runtime map. All **88 runtime
pins**, totaling **67,816,579 bytes**, independently match actual files. All
59 profile pin occurrences (including deliberately repeated support pins) match
both their declared lengths/hashes and the runtime map. No mismatch was found.

The exact 11-argument entry command matches the installed isolated Python,
`-I -S -B`, copied `run_layout.py`, configuration path/hash and selection path.
Only that entry runs from the snapshot; the 26 canonical imported modules are
explicitly pinned originals, not an undeclared fallback. Future snapshot files
are not alleged to be preexisting runtime inputs.

The entry remains 11,804 bytes / SHA-256
`35e4111c76e0e3a3e4c210df0a9bea430ed84f670d2ffd17ee5cabd1e8f9a2ca`.
The selector remains 15,145 bytes /
`e276434c9b896909596f51482276b972f8e928cc1a411b99bd00cf8ea8bf9fc4`.
The existing source review is unchanged at 5,835 bytes /
`1b51e00cec4a1e4af8edd6ce854b87118767a50881246bc82afe0b0334b2f7ba`.
This review relies on that source review rather than duplicating it.

## Profile, genuine build and input binding

Hashing the literal domain `DMKN-GEOMETRY17-LAYOUT-PROFILE-V1` followed by NUL,
then the actual profile bytes including their final LF, independently produces
`a28d59596bd50ed7634bf4f060cdbbdc51ed403a2e1ecfc6b372c112e5cc7edd`.
This equals the configuration's profile ID; no JSON reserialization was used.

The profile selects actual Build02, not deferred Build01. Its support host is
identical by path, length and hash to the successful Build02 executable:
6,631,424 bytes / `4606258931a7c793c66e5002ee864bbfb8f7f9d81850b88bf1256126ac254869`.
The exact actual-build review remains 8,390 bytes /
`68af53904cbce8532e2ffe582c8eff08bd8a907ddd0516522ce0db6a8e31ebd3`.
The five selected Build02 records are its actual records. This review does not
repeat that review's compiler-recipe checks or the old full toolchain census.

The selected adopted ELF is 1,745,920 bytes /
`98686ced7979d55685c648f441f7ffbe40712e327a1311f9cb076a0c7250e773`;
its actual bytes and runtime-map membership match the image adoption record.
The reference wire (113,849 bytes), header (192 bytes) and I receipt (223,594
bytes) match their selected original hashes. The 184-byte configured J_FIRST
target independently hashes to
`07734789fd165d5c29667a2925c09b882d346db97a511c75644f2cb4b8ccd0da`.
The selected packet and profile bytes match their configuration pins.
No selected-input parent directory currently contains `FINALIZATION-FAILED.json`.

The command remains fixed po17, diagnostics `stats`, and 2^26 cycle ceiling.
The full mixed-envelope values match the reviewed plan (including UInt64 maximum
rank); no foundation, policy, relation image, selected H2 mathematics, receipt or
verifier-control change was introduced. Actual generic preparation, exact
regenerated packet/reference equality, canonical-profile serialization, native
parent verification and guest execution remain dispatch obligations, not facts
established by this data-only review.

## Finite reserves and launch conditions

The `_fixed_bound` calculation for these exact inputs is:

| Component | Bytes |
|---|---:|
| Configuration, profile, packet, selection and three original references | 937,381 |
| Adopted ELF | 1,745,920 |
| New wire/header/parent copies | 337,635 |
| Fixed report/diagnostic reserve (14 MiB) | 14,680,064 |
| **Total** | **17,701,000** |

This is below the 20 MiB limit (20,971,520 bytes). The generic native output
reserve is 214,247,139 bytes, below 218,103,808 (208 MiB), and 533 prospective
entries are below 544. Source snapshots fit their separate 2 MiB reserve. The
complete selected runtime set itself is below the owner's 512 MiB installation
ceiling; its 88 entries plus the 12-entry margin are below the 256-pin ceiling.
The reviewed owner/selection checks must still enforce actual membership at run.

Native limits are 60 worker CPU seconds, 30 controller CPU seconds, 120 wall
seconds, 512 MiB and two processes. The enclosing selection allows 120 inclusive
Job CPU seconds, 180 wall seconds, 1,024 MiB and three processes; logs are 1 MiB
each. Entry final checks are 60 process CPU / 170 wall seconds. The 224 MiB /
640-entry outer sampled census retains its 4 MiB / four-entry final reserve.
Nested native CPU is already contained in outer Job CPU and must not be added
again; outer-wrapper CPU is separate.

At the last read-only check, `geometry17-layout-01` did not exist. Root must
retain this freshness, bind the selection hash above and obtain a fresh
**at least 2 GiB physical AND true-commit headroom**, with no heavy overlapping
work, immediately before the one existing `Run-V5-Check` invocation. No memory
poll or new launcher framework was run/created by this reviewer. Failure is
terminal evidence for this attempt, not permission to retry or raise limits.

Acceptance of the observation requires clean outer closure, successful entry
finalization and the inner layout result together. An inner PASS alone is not
sufficient; early entry failure may have only outer failure evidence. The result
can justify a later proof-feasibility decision only; it is not a certificate.
