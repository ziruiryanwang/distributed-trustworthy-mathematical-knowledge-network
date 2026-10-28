# Directory kit utility delta review

2026-10-28. query_scaling independent source/data inspection. **PASS for the
selected utility delta; no blocker found.** No product imports, execution,
packing, runtime, owner access or Git operations occurred. This does not replace
the forthcoming exact selection/pack outcome review.

Reviewed `kit.py` SHA-256:
`54296595561ec6b63510feaff466652c19874d155381e2ab0501d75e106f50e2`.
An exact text transformation of the adopted ordinary_usable_distribution
utility reproduces the new file using only seven changed lines: PROFILE,
source-map path/hash, builder path/hash, package count 158 -> 160, and mapped
source count 91 -> 93. No packing/extraction, content-relation, census, guard,
helper, byte limit, installation or runtime policy logic changed. The previously
reviewed archive/security implementation was not re-audited or re-executed.

The new constants match independently read local files:

- Actual package PROFILE:
  `7687d5276d8a7edc0beeb7066e4cbaae16529b0e88d8a0728b003dad04a4dd34`.
- Current ordinary_name_directory source map:
  `46709b30199384ad1e14f0d54529fe185d429d83c341dfebb117869bbe22ead3`.
- Its direct builder:
  `9bf43595182d969fe26b20012d9c569d6ffabde90543951cd0fd330e3025f8f3`.
- Unchanged actual installation manifest:
  `9112bc5dfeb688f5aaf266816781fa58a80c84f2916e820e030b9a2b86992f27`.

The actual name-directory-assembly01 receipt contains 160 files, totaling
39,603,928 bytes. Its PROFILE contains 122 auxiliary pins; all match the receipt.
All 27 local installation payload pins also match. Every one of the map's 78
direct-copy roles/pins matches the actual assembly receipt. The map has exactly
93 source inputs. Neither this mapped source closure nor the chosen package
contains pattern paths. No native payload was rebuilt or changed.

The source map and direct builder are additional kit source files, not members
of those 93 mapped inputs. With the existing nine top-level/operator/preview
companions, the minimal new kit therefore has 160 + 93 + 2 + 9 = **264 payloads**
excluding KIT-MANIFEST. The future exact selection must bind the newly assigned
docs/operator bytes and the unchanged preview/helper roles. The unchanged
utility will then validate the selected census/pins and the package/source
relations during the separately selected pack. This review does not claim those
not-yet-selected companion bytes or a packed archive have already passed.
