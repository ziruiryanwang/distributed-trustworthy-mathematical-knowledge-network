# Retain the actual proof, repair only witness row emission

The independently audited author01 result remains FAIL. Its ordinary Lean
export succeeded and contains exactly two uses of the accepted first theorem,
but cold checking rejected `CORRESPONDENCE_DESCRIPTOR_RECORD_MISSING`.
Actual imported position1 was base.binary_congr while the relation required
base.Tree.below. The source frontend needs topological declaration order; the
unchanged relation builds bindings in BTreeMap(owner,index) order. Reusing the
former ordering for native relation rows was a producer bug, not evidence that
the theorem is false or reason to weaken the verifier.

Root selects a fresh producer-only successor: authoring02.py9438a5cb uses shared
emit_relation_rows in reprepare.pyaf225a6d; imported groups sort by canonical
owner/index, followed by unchanged local-spec order. All other authoring behavior
and frontend context order remain unchanged. Independent minimal-diff/helper
review passes. Used predecessors and failed evidence remain untouched.

## One new decisive operation, pending exact review

Independent final source and140 actual/future-snapshot bindings pass. Root
adopts the review and launches this exact selection once; pending above is
superseded, not an actual outcome claim.

- Selection:d20434664f4e94ff20186c659e71851c76c0ce2e394c08aa68551901e2a425d9.
- Config:640c3fb38142b6cc1da0686137544a23c62eb3f20c37f458b61c1b42a16ecb77.
- Harness:fcb9af85e264047caf31b4936c8fb93e8ae6da71d4d6db1802e30ba1621b68bc.
- Retained source request:17cc96571235788c335e7426e9060f43c5ec42bc0a299d83756b6b37092daf38.
- Actual export:268681e0e4193badaa073be369ac062b678ef65123d152780182c448c2f902b7.
- Failed packet:40aac3921a49b144c19cb7310679741abbd82bb7d796f05a5a0beb71ee60649d.

Reconstruct the local descriptor/proof from retained export, bind its context
to exact parent openings and committed bodies, and require that ONLY final
witness rows change. Save a fresh untrusted packet, then receive it through
one cold real receipt verifier and two unchanged native relation calls.
Require exact target52c564f8,rank2, all three members, target opening and full
export bytes. All owners close; final durable reporting rechecks original time.
No authoring, snapshot, guest, proof generation, rebuild or network execution.
Outer300CPU/300wall/2048MiB/cap4,workflow240wall, each worker30CPU/90wall/1024MiB.

Prior author01 cost stays charged:46.796875inclusive workerCPU+1.171875wrapper,
56.0269228wall, including the successful3.625CPU author worker. Correcting the
packet does not erase failure or authorize rerunning that successful prefix.

## Actual outcome adopted

Independent184-binding audit PASS. Actual corrected packet is662480bytes,
SHA54c7dac7f83a9a06c2b23b17a77be20364c1b90e4cd3b1db58b69c62fda2dcf1.
Decoded comparison independently confirms only final witness rows differ.
Fresh receipt and both native checks exit0; computed exact parent journals
match the actual base/first conclusions. Target52c564f8rank2 is admitted and
opened; complete export and all three member identities match. All owners have
zero handles after closure; every worker/outer Job is closed/reaped with no
active or terminated process. Outer6.625CPU+.5625wrapperCPU,8.638137wall.
No predecessor authoring/proof work repeated. The corrected common emitter is
tested; the full ordinary authoring02 live wrapper is still source-reviewed
only. Retain this packet for actual network integration instead of regenerating.
