# Restricted guest image assembly01: independent actual outcome

2026-10-21, core_release. **PASS_ACTUAL_ASSEMBLY_BINDING_AND_CLEAN_CLOSURE**.
This is assembly evidence only: zero guest executions, proofs or mathematical
admissions. Source review2659bd39 is reused, not repeated.

All paths below are under the canonical project root
`E:\Distributed Trustworthy Mathematical Knowledge Network`.
Run: `experiments/v5-local-checks/restricted-guest-image-assembly-01`.

| Record | SHA-256 |
|---|---|
| sibling selection | ed4dfc5ee20432811e3330cdd56d93aed83096d5cac527a19bfddb1379ebba58 |
| outer RESULT.json | 0e9171754310e3e209b966194959c4d47cb9f9f82996f8fed4bd1cc2154ca510 |
| assembly/RESULT.json | 3d11596dfef8d4f81b684898468ca85f04853fb7cf42774ec89a79ece053135f |
| assembly/COMMAND.json | 0aba838ca0e869dffef56106dd9d9ba22000ff2877ef92c90ffd438e12046133 |
| guest03 build RESULT.json | 44f808cdd24c2707d114675bf77a4126a805865eaae825666db0c9403e354273 |

The saved selection is byte-identical to its sibling. The outer actual argv
equals the selection after exact snapshot/output substitution. All76 selected
runtime hashes, three original and three snapshot source hashes, and57 assembly
command input length/hash pins match actual files. Together with selected
records, image and logs this covers88 distinct files/92521633bytes. The236
compiler dependency files were not rehashed; their adopted build result is reused.

The actual driver command uses the pinned retained assembler, guest03's exact
623848-byte ELF SHA
`58250728be048d3badcb4db80cc162ea17b16044b927835e0d59ddf25a260840`,
the retained compatibility kernel and the selected fresh image output. The
guest result, ARTIFACT, build selection and input pins agree. No guest03
finalization override exists. Both actual driver log pins match; stderr is empty.

Actual driver stdout is exactly the reported combined-image line:

```text
COMBINED_IMAGE image_id=b6b09430b3a9c20a523c00d7cefe3e2312a2ad323ed089f70fe1d0188236a393 bytes=682616
```

The682616-byte retained `assembly/aggregate_image.bin` has SHA-256
`0e5053500df1b6c56d1fad204be0f96aa81cea4b2f2cefdac759b5ba264c3352`.
Image ID is the actual pinned assembler's output, not the file's SHA-256.
The outer stdout record structurally equals the saved inner result. Its SHA is
`664bf179b3126a7d59ef83dee72461bcbe4f3b4a5462ee64d9ed4e02342e04e9`;
outer command record SHA is
`187979d8da31a68e387e2c2612e0b43e6ad6f7fabf37cddb239340ec39f057ac`.

Outer process exited0 and was reaped, Job closed, cleanup errors empty, no
termination requested and zero active/limit-terminated processes. Observed
total process count4 is cumulative, not concurrent; the two-process limit is
unchanged. Peak Job private commit was25681920bytes. Both outer and inner stderr
are empty. The inner reports exactly one assembler call and no guest/proof call.

Known measured cost is0.640625inclusive worker Job CPU +0.390625disjoint outer
wrapper CPU = **1.03125CPU seconds**, with **1.2173325wall seconds**. Inner
subprocess work is already included in the worker Job and is not added again.
This excludes unmeasured audit work and the final report/exit tail under the
existing accounting convention; guest compilation remains a separate sunk cost.

Read-only audit shell summaries initially had a Hashtable aggregation error and
an unparenthesized key-set comparison. Corrected summary/comparison commands
confirmed the above; neither invoked product code or changed retained evidence.
No rebuild, assembler rerun, guest execution, proof or Git mutation occurred.

Disposition: the exact image may enter root's separately selected matched
execution screen after other reviews close. This outcome does not establish
semantic refinement, certification savings, useful growth or release readiness.
