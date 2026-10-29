# Coherent investigator kit delta

2026-10-28, root. Source preparation only; packaging not yet selected.
Actual assembly PROFILE is
`85d45c928523c2b96f127ec8c15b2e2664f8428f0c1ef2415470a5b30737d3c8`.
All 157 other package payloads remain exact. The deterministic module-anchor
descriptor has unchanged inputs by the reviewed support closure; this does not
require reopening an owner or rerunning native checks.

SELECTED-FILES.json
`8850811b7e1d4108252f79bf36b5d8092433c2b698985c4fbf194cefeffc1746`
retains 268 payloads: actual package160, mapped sources93, map/build2,
companions13. No tests, state, credentials or runtime are added to the kit.

The direct builder changes only PREFIX and the new map pin; its compile lanes
are identical. The file-only kit utility changes only PROFILE/map/build constants.
The offline preparer's compatibility map changes only the two transport source
pins, and its wrapper changes only the map digest. Existing preparer behavior,
request templates, contribution projector and preview utilities are unchanged.
Refresh companions change only their selected PROFILE. The guide updates PROFILE
and source-build path and explains the changed ordinary failure behavior.

The new kit utility is
`62c15511e6f2330142da9fb4872c12cc289356efa2b8d9229ce6b759f3bcc28f`;
compatibility map is
`493e8b76697b23454874887b4449cde8138687b81bf5ba9e2a9b3a5a317ae942`.
No repeat native build or preparer campaign is needed. Validate the exact fresh
archive/extraction once after independent source review, alongside disjoint
transport controls and the retained-data typed-API fallback check. Adoption
requires their actual results; final-v5 completion is a different gate.
