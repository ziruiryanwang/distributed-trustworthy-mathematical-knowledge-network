# Assemble one actual restricted guest image

2026-10-21, root. Source/consumer reviews85cbf4ab,614a1071 and2659bd39
are read/adopted, with the final four-crate consumer changes covered by2659bd39.
This selects one restricted-guest-image-assembly-01 operation only after the
independent actual guest03 audit confirms result
44f808cdd24c2707d114675bf77a4126a805865eaae825666db0c9403e354273.

- Assembler0ebc655842b1092f4314e27fa4f6e57e452303eae06b2e60b1b5a19bac46a957.
- Selector e1e745b6375ef7c3456fa30e9756aea6777ca813234f89e43b21b4671074c6ad.

Use the exact reviewed selector, then the retained Run-V5-Check with the new
selection digest, pinned receiver Python and no interpreter changes. One
retained assembler invocation combines the source-bound ELF with its pinned
kernel. No compiler, guest execution, proof or installed trust change.
Unchanged120CPU/120wall/1024MiB/two-process outer envelope and inner60wall.
No retry or limit renewal. Release independently reviews actual image binding,
command, output digest and clean outer closure; root then decides the pair.
The actual assembler's image ID, not the file digest, is used as the guest ID.
