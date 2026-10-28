# Remaining native frontier cases

SOURCE ONLY. Root selects execution separately after review. The complete v5
goal is unchanged; this is the last two cases of one bounded frontier check.

Native02 closed after successful setup and positive native admission. Its harness
then rejected the diagnostic proof head: source `:= rfl` exported `rfl`, whereas
the strict helper expected `Eq.refl`. Preserve every original source/result byte
and the failed outer status. Do not rerun setup, the positive case, or compilation.

## Exact continuation

`native_remaining.py` reopens only native02's closed fixture through the existing
public `OrdinaryStore(..., create=False)` and `OrdinaryAdmission.open(...,
create=False)` APIs. The original store identity and unchanged capacity limits
are recovered from pinned saved inputs. Public opening may perform the ordinary
catalog recovery behavior; this is not a read-only state operation. No private
database edits, identity changes, allowance reset, migration or repair are used.

Authenticate the four original roots/calls and exact F/P contexts before work:

- F `90825f1b8218c08af43335b1692e8b3a7918c84732bf1a450ef359484c20fefd`.
- P `d0b4bcfa16e72ec840e52aa0b31ecd94b3457e7bd717c1d34b1f2bff0b57453c`.
- Exact accepted `Base.c = 0`, `Above.d = Nat.succ Base.c` evidence and bindings.
- The authenticated F module plan is a prefix of P's plan.

Fresh output must be a new run's `workflow` directory under
`experiments/v5-local-checks`; the old owner/custody remain at native02/workflow.
The old workflow02 helper is loaded from its immutable source snapshot without
executing its guarded main. Its unchanged Allowance, closure, name and exact
expression/proof diagnostics are reused. Both five-file compiled frontend sets
are pinned before/after; only the alternate frontend is used by these two cases.

1. **False parent:** import existing AlternateBase (`Base.c = 1`); author
   `Above.d = Nat.succ (Nat.succ Nat.zero) := Eq.refl Above.d`. Demand the real
   Above.d group above F. Scratch construction must succeed with exactly one
   reconstructed unit. The unchanged final checker over actual P must fail in
   admission, with no accepted root and one new admission call. Preserve exact
   false theorem syntax and `KERNEL_REJECTED_OR_RESOURCE_LIMIT`; that combined
   marker does not establish a particular kernel error versus resource cause.
2. **Missing:** import only Init; demand the same Above.d over F. Missing Base.c
   must stop construction with the precise kernel/frontend frontier marker,
   no candidate, no admission call and no new accepted root.

Each request must be V3 with original P/F, the exact acquired Above.d triple,
one fetched group and exact Base.c frontier label. A pass-through evidence-read
guard forbids fetching Base.c and requires the one Above.d read. F/P contexts,
the four accepted roots, all pinned old report/evidence/frontend bytes, package profile
and receiver files must remain unchanged. Expected calls grow from four to five
only through the public failed admission; no successful native event is added.

## Finite proposed allowance and claim

Fresh continuation only: 180 s whole wall / 100 s whole CPU; false-parent at most
90/45 s, missing at most 60/25 s, all clipped to the whole allowance. Each native
operation keeps the existing 1536 MiB / four-process / 32 MiB output ceiling.
Proposed outer Job: 210 s wall / 120 s CPU / 2048 MiB / eight processes, 4 MiB per
output stream. These are not additions to an old operation or catalog quota.
No network, basis initialization, new compilation, positive repetition or retry.

Record new outcomes, evidence reads, public inventories/context summaries,
old immutable-input pins, costs and owner/custody closure in fresh output. Any
unexpected result fails closed, with original and fresh evidence retained. The
claim is only the two actual negative outcomes of this finite optional scratch
boundary; final v5 deployment, general isolation and useful growth remain open.
