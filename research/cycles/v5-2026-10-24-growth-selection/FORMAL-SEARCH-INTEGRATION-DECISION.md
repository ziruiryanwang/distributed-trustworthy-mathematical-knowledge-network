# Formal search of independently developed theories: no new adapter selected

2026-10-24. `formal_search_integration`; source-only follow-up. No installation,
dependency fetch, remote query, native operation, experiment, protected-state
access or Git mutation. This note closes a possible duplicate investigation.

## Decision

**No new high-value source-level obstruction was found beyond an approved,
compatible corpus/provider. Preserve PREEXPORT-SELECTION's closed decision.**
Do not build another client, matcher or inert-to-Loogle importer, and do not run
a compatibility experiment merely to turn an optional route into another pass.

The existing pinned-upstream audit already establishes that Loogle is not limited
to Mathlib: a matching binary can search a built Lake project's selected root
module using `lake env <loogle binary> --module <root> <query>`. The HTTP wrapper
also has `--project-dir` and forwarded module selection. These are prior inspected
upstream capabilities, **not newly tested compatibility with Lean 4.34.0 or our
concept project**. No local Loogle artifact is selected in the current package map.

## The two distinct routes

| Route | What is justified | Remaining condition |
|---|---|---|
| Approved native project, local search | Existing upstream module selection can include non-Mathlib theories in principle | Matching Loogle/toolchain, built compatible project, selected public imports and explicit execution approval |
| Remote advisory provider | A consumer can receive candidates without locally importing provider code | A willing reachable provider actually covers the selected project; its answers remain unverified hints |
| Inert preview directly into Loogle | Not supplied by this product or the previously inspected upstream interface | Requires an environment/materialization integration; it is not a configuration-only use of the current exact index |

The provider's native-code approval is its own operational/security responsibility.
An advisory reply does not transfer mathematical authority or code-execution
approval to the consumer. Heterogeneous project/toolchain providers need not merge
their environments, but a consumer cannot infer compatibility or corpus coverage
from equal printed declaration names. The unmodified upstream JSON is not bound
to an exact corpus snapshot, as PREEXPORT-TOOLS already records.

## Current-source checks that prevent overclaiming

- `ordinary_research_distribution/source-map.json:27-353,443-457` selects our
  Python peer facade and `ordinary_formal_query` adapter, not a Loogle executable,
  provider or integration. No source-map role supplies native pattern search.
- `ordinary_authoring_offers/peer_api.py:162-198` compiles exact feature specs.
  `ordinary_formal_query/discovery/ordinary_export_adapter.py:64-100,137-205`
  accepts kind, exact type key, exact symbols and structural heads. It neither
  consumes a Loogle pattern nor constructs Lean's elaboration environment.
- `peer_api.py:665-756` returns one exact inert declaration unit while keeping
  dependency checking and native usability false. Inspection is not a hidden
  native-environment loader, and advisory authoring offers do not change that.
- `ordinary_native_package/owner.py:267-317` already accepts an explicitly
  approved compiled project and caller-selected target names for production;
  `ordinary_baseline/BaselineExporter.lean:223-249` imports selected modules and
  extracts their exact declarations. A chosen external search hit can therefore
  lead into the existing ordinary-project path without a new search protocol.
  Printed names are leads, not preexisting ExportIDs or mathematical acceptance.

Locally materializing an inert corpus solely to feed Loogle is not a cheaper
established alternative. `concept_episode/EXCHANGE-ROUTE.md` records A's actual
66-unit closure against the current generated-module limit of 32, plus existing
ambient-collision and frontend limitations. Reopening those boundaries just to
obtain pattern hints would substitute importer engineering for the still-missing
useful provider/content case. No general impossibility is claimed.

## Consequence for the next allocation

The source question is closed without product changes. Select an actual optional
provider integration only when a worthwhile independently supplied corpus and
consumer workflow identify its payoff; then test the genuinely uncertain
toolchain/import boundary once. Neither repeating the Repair/modulo example
already in Init nor wrapping the same upstream JSON would establish that payoff.
Continue higher-value growth or deployment work instead. This note establishes
no novel mathematics, actual external theory-search success or research speedup.

Sources reused: PREEXPORT-TOOLS, PREEXPORT-SELECTION, CREATIVE-GROWTH-MECHANISM,
and the exact local source files cited above. No new upstream verification is
claimed; current non-Mathlib toolchain compatibility remains untested.
