# Complete formal view of the retained contextual-refinement preview

2026-10-28. Hand-derived specimen for design review, not renderer output or a
fresh mathematical check. Decoded from the saved preview's 75 expression nodes
and six level nodes; compared with source03's statement, including its implicit
parameters. No product module was imported and no Lean/network/owner operation
ran. The proposed display preserves explicit applications and does not reconstruct
source notation or omit the atomic law and two observation witnesses.

## Exact input and assurance

| Item | Value |
|---|---|
| Saved report | `experiments/v5-local-checks/dedicated-host-preview01/RESULT.json` |
| Report SHA-256, read from actual file | `77065fe33292368d3d4a177c4b836cf0bcf98128b0984a6178168734226c5113` |
| Recorded preview bytes / SHA-256 | `4798` / `f3fd920019c877c33483c8b82bfa1692e300aad7307008cb70edd97d7c32a435` |
| Semantic ID | `9108f44dba66e2a26a06f65566e143e3185e3f8237e156a4e5c826222a308ad7` |
| Unit ID | `c59ee7bd4eed61193dc06729ca76e28887ad83171f11173353e93bb46305c2c4` |
| Export ID | `b093eb970b89de31662abccdb05552270225e26b93e4f0dc47a6463b1590f8be` |
| Declaration name | `str("ResetEffects") / str("contextual_iff")` |
| Kind / root expression | `2 = theorem` / `e74` |
| Original report status | `PREVIEW_BOUND_NOT_ACCEPTED` |

The preview's byte count/hash above are the saved report's selected values and
previously adopted audit, not a new product-validation result from this specimen.
The report's `mathematical_acceptance`, `evidence_bound` and
`snapshot_membership_reverified` remain false. This view explains a claimed type;
it does not establish truth, applicability, dependency availability or relevance.

## Complete type

`#bN` identifies one scoped binder occurrence; `#cN` identifies a row in the
exact binding table below. `u#u0` and `v#u1` retain the original universe order.
Braces denote implicit binders, parentheses default binders. All applications
include their actual implicit arguments. No universe suffix means an empty list.
This is formal display syntax, not a file to compile.

```text
theorem ResetEffects.contextual_iff
universe parameters [u#u0, v#u1]

forall {A#b0 : Sort(succ(u#u0))},
forall {S#b1 : Sort(succ(v#u1))},
forall (observe#b2 : forall (arg#b3 : S#b1), Bool#c2),
forall (step#b4 :
  forall (arg#b5 : A#b0), forall (arg#b6 : S#b1), S#b1),
forall (effect#b7 : forall (arg#b8 : A#b0), ResetEffects.Mode#c9),
forall (atomic_law#b9 :
  forall (a#b10 : A#b0), forall (s#b11 : S#b1),
    (Eq#c3.{succ(zero)} Bool#c2
      (observe#b2 (step#b4 a#b10 s#b11))
      (ResetEffects.Mode.eval#c7
        (effect#b7 a#b10) (observe#b2 s#b11)))),
forall (s0#b12 : S#b1),
forall (s1#b13 : S#b1),
forall (h0#b14 :
  (Eq#c3.{succ(zero)} Bool#c2 (observe#b2 s0#b12) Bool.false#c0)),
forall (h1#b15 :
  (Eq#c3.{succ(zero)} Bool#c2 (observe#b2 s1#b13) Bool.true#c1)),
forall (p#b16 : (ResetEffects.Plan#c10.{u#u0} A#b0)),
forall (q#b17 : (ResetEffects.Plan#c10.{u#u0} A#b0)),
  (Iff#c4
    (ResetEffects.ContextuallyRefines#c6.{u#u0,v#u1}
      A#b0 S#b1 observe#b2 step#b4 p#b16 q#b17)
    (ResetEffects.Mode.Refines#c8
      (ResetEffects.summary#c5.{u#u0} A#b0 effect#b7 p#b16)
      (ResetEffects.summary#c5.{u#u0} A#b0 effect#b7 q#b17)))
```

The outer binders are nodes e74,e73,e72,e71,e70,e69,e68,e67,e66,e65,e64,e63
in that order; the final result is e62. The atomic-law type is e26, observation
witness types are e31 and e36, and final Iff arguments are e51 and e61. These
locations refer to original data, not globally valid abbreviations of open terms.

## Exact binding-index table

Indices are unchanged from `type_bindings`, so row N is the existing operator's
`binding_index: N`. Names here list exact string components; no numeric component,
name normalization, or name-equivalence inference is involved. SymbolIDs bind
identities; they do not prove the advertised declarations. Basis symbols need
not be ordinary exports, so a table row does not promise an inspectable unit.

| Index | Readable label | Exact name components | SymbolID |
|---:|---|---|---|
| 0 | Bool.false | `str("Bool") / str("false")` | `c58ea752ff22e192f539e316af9ea1b66ef3aa3becb6676f02fd402470d4486d` |
| 1 | Bool.true | `str("Bool") / str("true")` | `f342ce840a1ddda25188888c3214540586a2299a1ae29ac443a9c2402651c280` |
| 2 | Bool | `str("Bool")` | `3b2bb906ca16844b42996316249bf8323f6392f933c6d39b467c8683c6326d72` |
| 3 | Eq | `str("Eq")` | `80b9689fa00451ea0cb456c6e822415c8ca66d4d0cd6a47c890c84371a59d6d5` |
| 4 | Iff | `str("Iff")` | `1fd6c3cc343ada103e3db76001c3e452d4ad483958b315eff3d02cfbb0cdd062` |
| 5 | ResetEffects.summary | `str("ResetEffects") / str("summary")` | `3c25594dc843ab715599d46ebecbb58e20a95b2e69902b815c5a8cb5d2d9a1ce` |
| 6 | ResetEffects.ContextuallyRefines | `str("ResetEffects") / str("ContextuallyRefines")` | `6e1e698f6f493b68cf80e26bd41e3b47e71c46cac781e1797407843d5e8f9b41` |
| 7 | ResetEffects.Mode.eval | `str("ResetEffects") / str("Mode") / str("eval")` | `23549823acaad891421644b327aaddf2e38cbef8887880b18d85533e7b748383` |
| 8 | ResetEffects.Mode.Refines | `str("ResetEffects") / str("Mode") / str("Refines")` | `0c2a10deb348975617a4ce78efd97d94f593af28f3370fb482db94b4cb404708` |
| 9 | ResetEffects.Mode | `str("ResetEffects") / str("Mode")` | `a52e5b6e3e32dd271ea43d4dc70b5f018b2e99c1de6a214596c95bbd09c627fb` |
| 10 | ResetEffects.Plan | `str("ResetEffects") / str("Plan")` | `dd71ac44349aa741c617ddd920ebe9f899bf36c8b929cfa4f621fdfde2ee02ca` |

## Binder and universe legends

`H` below is the exact original hygienic label
`str("a") / str("_@") / str("_internal") / str("_hyg") / num(0)`.
Four different binder occurrences retain that label and receive distinct display
tokens. The labels `arg` are readability hints only. All other labels in the
table are the single exact string component shown.

| Display token | Source node | Original label | Binder code |
|---|---:|---|---|
| A#b0 | e74 | `str("A")` | 1 implicit |
| S#b1 | e73 | `str("S")` | 1 implicit |
| observe#b2 | e72 | `str("observe")` | 0 default |
| arg#b3 | e4 | H | 0 default |
| step#b4 | e71 | `str("step")` | 0 default |
| arg#b5 | e8 | H | 0 default |
| arg#b6 | e7 | H | 0 default |
| effect#b7 | e70 | `str("effect")` | 0 default |
| arg#b8 | e10 | H | 0 default |
| atomic_law#b9 | e69 | `str("atomic_law")` | 0 default |
| a#b10 | e26 | `str("a")` | 0 default |
| s#b11 | e25 | `str("s")` | 0 default |
| s0#b12 | e68 | `str("s0")` | 0 default |
| s1#b13 | e67 | `str("s1")` | 0 default |
| h0#b14 | e66 | `str("h0")` | 0 default |
| h1#b15 | e65 | `str("h1")` | 0 default |
| p#b16 | e64 | `str("p")` | 0 default |
| q#b17 | e63 | `str("q")` | 0 default |

| Parameter position | Exact name | Display token |
|---:|---|---|
| 0 | `str("u")` | u#u0 |
| 1 | `str("v")` | v#u1 |

The original level DAG is l0=`param(0)`, l1=`succ(l0)`, l2=`param(1)`,
l3=`succ(l2)`, l4=`zero`, l5=`succ(l4)`. Thus the two type binders use
`Sort(succ(u))` and `Sort(succ(v))`, and Eq's universe is exactly `succ(zero)`.
No let, lambda, projection, native literal, max or imax occurs in this specimen;
those constructors still require the contract's explicit treatment.

## Payoff assessment and boundary

The source comparison is `research/cycles/v5-2026-10-28-growth/Proposed03.lean`,
SHA-256 `4743094ebb82157bff58c0131c52592911672909c522e58b0efae3c747d2754a`,
variables at line116 and statement at line245. Its old UNCHECKED comment is not
a current acceptance claim; this specimen does not repeat or supersede the saved
checking evidence. Ordinary approved source remains the more compact reading
route when available.

Unlike the raw JSON, this specimen makes the atomic-law premise, the false/true
observation witnesses and the exact contextual-refinement criterion visible in
one place. The table directly identifies `ResetEffects.Plan` as binding10 and
the unfamiliar refinement relation as binding6 for existing inspection. That
is a concrete interpretation/selection improvement over decimal names and DAG
indices. It is not a measured time saving, evidence of independent usefulness,
or justification for a ranker, richer body browser or another theory episode.
