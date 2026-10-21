# Incremental native integration02: actual outcome audit

2026-10-21, adaptive_audit. **PASS for the selected real-constructor,
same-owner M then M+V warm-prefix integration.** This is an audit of retained
actual output, not another execution. No product import, test, proof, native
command, network operation or Git mutation was performed for this review.
Used01 remains a separately retained failed attempt (`18f258cc`); its cost and
failure are not overwritten by this fresh02 success.

## Exact execution and source closure

Output: `experiments/v5-local-checks/incremental-native-integration-02`.
Root reported terminal session6330, exit0. The retained outer report agrees:
`COMMAND_EXITED_ZERO_AND_CLOSED`, direct child reaped, Job closed, zero active
or terminated processes, eight total processes, no cleanup errors, no requested
termination, stdout51 bytes and stderr0. Limits were90CPU/180wall/512MiB/four
active processes. The source/launch review is `0e6336d6`; adapter02 `ea026900`
only fixes the exact current source-map size ceiling from failed01.

Read-only SHA-256 checks independently matched all119 selected physical source
files at BOTH original and frozen snapshot paths (238 comparisons), all28
runtime pins, and all24 exact input file rows. All114 staged logical copies
match their recorded source bytes and sizes. Comparison with terminal-I114
map `d3519be1` finds precisely the three selected replacements:

| Logical role | SHA-256 |
|---|---|
| `v5/admission/pin_phase.py` | `ac7ed2285f2c15630a482817828cf4784ca807c6ec700b4a17bfe3e561eee881` |
| `v5/mixed_claims/imports_atomic.py` | `8a8313376d736f25a45b6089f491373bc7e0206aa77b539dbff077fc4eb92595` |
| `v5/mixed_claims/receiver.py` | `5436569971c272b129fbaec480d51d57a1ec521d43fd4d4ad14133b786691d5b` |

The unchanged input is10264 bytes, SHA-256
`3611e1267d6f5d4906c6a2db79facda3f6c34e39a133d7524c8412a97240917f`.
No source substitution, mocked worker or constructor bypass occurs in the
reviewed adapter; it creates an actual TrustDomain, ReceiptVerifier and
MixedDeltaVerifier under the exact staged114 map.

## Actual mathematical checks and reuse

The actual receipt worker is the selected installed `module_host.exe receive`
with relation image
`9dfd589213a3245cf88e0d28096356aae4d2666bf0e85a7c3302b92e21d2c69e`.
Its stdout reports `REAL_MODULE_RECEIPT_VERIFIED`, fully resolved succinct
Poseidon2 receipt, and exact retained I frontier
`2b54d3be0ee27667c864ede130980f3fdeef963141296989b60113ba90e5be9e`.
The actual receipt file is223594 bytes, SHA-256
`850c33b2a26649bd5d68762b75b4b4618eb5cd837d50507490d02a28db6e5d47`.

The two actual `native_delta.exe check` processes report conditional relation
checks, explicitly NOT stand-alone mathematical admission. Their exact input
files are M50017 bytes/`8b84084486b0aadceb9ee353a28654b2777e297a726693135c575d5c50e85f5a`
and V50814 bytes/`bca4534a839390c72732f40d9a3665bdb8f12c7039cbc1656920b789ff308b48`.
Independent array comparison confirms M's parent journal equals actual I's
journal, and V's two parent journals equal actual I and M respectively. The
live-owner described target journals exactly match the two worker outputs.

First accepted target M is
`bbf0845d2622374699a93a9d8ccc6e565dd1c985e72441ec0eeae41bb03fc0c5`,
group_count1/root`f0505daeabecea8f16b53feb8674db02233578dc02e8e775a70f3c2de1ffcc16`.
Second target V is
`540f82c8f0b75c4703074c92f5de514f33d2fb84ec45317b672fadb4fe946c17`,
group_count2/root`d25b0ad3365251ea432d7696152612e6b721282740456af8d7c61140308ce341`.
Saved packets match the retained originals exactly:498641 bytes/`efc96de9`
and549456 bytes/`30566df7`.

Across the two live calls, attempts advance1→2, native attempts1→2, reuse
observations0→1, retained memo records1→2, memo witness bytes50017→100831,
reserved workerCPU20→50, submitted bytes498641→1048097 and live handles1→2.
The receipt owner stays at one attempt,223594 submitted bytes,10 reservedCPU
and one live handle. Both descriptions use the same mixed profile.

The second call labels M
`SAME_OWNER_REUSED_CONDITIONAL_CHECK_NO_EXECUTION` and V
`NATIVE_EXECUTED_CONDITIONAL_CHECK`. Its M journal equals the first actual M
journal. Independently confirmed absent under `mixed/2`: `delta-0.json`,
`native-0`, `process-0.json`, `claim-0`. Thus the actual evidence supports
skipping this already checked native prefix, not fabricating another worker
record or replaying I. Current-premise and memo-refusal behavior is supported
by the separately adopted nine-control result `513b91d8`, not retested here.

## Authority closure and costs

Every selected source role matches the saved support. The adoption's support
equals that saved manifest; independent domain-framed SHA-256 reconstruction
gives support_id
`8dffbe4a6521e4c9a1b5b93d9c41c3d235085dfa488fa0af0a03c94d8d07e4a9`.
The persisted WITHDRAWN marker binds that support, the exact domain and the
actual adoption-file hash. Final reports show both owners closed, zero live
handles and zero retained native records/witness bytes. Final errors are empty.
Saved result files grant no continuing or transferable mathematical authority.

Whole-run elapsed time is20.663805299904197 seconds; supervised elapsed time
through cleanup is20.518296899739653. Outer JobCPU15.609375 plus separately
reported wrapperCPU0.59375 gives **16.203125 known measured CPU seconds**.
Wrapper-supervisionCPU0.078125 is already included in wrapperCPU.

The actual I/M/V workerCPU values are0.046875/0.03125/0.03125, summing to
0.109375 and matching the final observed-worker counter. Their elapsed times
are0.5630087000317872/0.1208806000649929/0.0668210000731051 seconds.
All three exited0 with clean closed Jobs and zero final active processes.
These nested workerCPU values are already inside the outer Job total: do NOT
add them again. Reservations are authorization ceilings, not measured CPU.

## Artifact anchors and scope

| Artifact under the output directory | SHA-256 |
|---|---|
| `selection.json` | `a88998e58082bfadc92378367fef52c644dadf1681e707219f771e9ce16e1c6f` |
| `RESULT.json` | `b99c13f516962a71d148ea94745294194b95dfcaaf41bdf417e2a117c133c19a` |
| `integration-result.json` | `66630226598fd309c33b0977304d7fef7e70e0d0024441e2eb21092bbbf6d0e8` |
| `integration-sources.json` | `5272485f9586a0c87f8b01eb0ce6ab6542b151abf17330f0887992e596f9ca09` |
| `integration-support.json` | `7740206886f9910a814c537621d642978845f62644f47b4d781aba7b9680c6d6` |
| `trust/ADOPTION.json` | `98ed0c72a45254475fcb22d1c6fb1f9868d197e5377dbe4b86872ce0eb6eb728` |
| `trust/WITHDRAWN` | `4d0ea9254b650fcda8ea1e30cdd5d588114cea90d4aa77e172b307c4c98fae97` |

This closes the selected real-constructor warm-prefix seam, not a new receipt
production, installation, import/authoring campaign, network/discovery test,
cold-cache ancestry-elimination theorem, matched performance comparison or
full-cost growth result. M and V were retained earlier mathematics. One avoided
worker invocation establishes the intended mechanism, not a measured end-to-end
speedup percentage. Full v5 remains open; root owns adoption and any next
source/runtime selection. No rerun is indicated by this passing outcome.
