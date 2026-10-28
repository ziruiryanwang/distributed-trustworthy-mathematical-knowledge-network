# Installed offline name-directory controls

2026-10-28. Source-only plan. Root separately selects runtime after exporter,
assembly and source review. Do not run this plan automatically.

`lookup_checks.py` takes exact package/PROFILE, an approved completed real
directory/DIRECTORY.json hash, a retained exact structured-name file/hash, the
successful earlier symbol-neighborhood query's RESULT.json/hash, its own source
hash, and a fresh output directory. The prior query is read as a comparison;
it is not rerun or treated as current owner authority.

The four independent installed `lookup_directory.py` children run concurrently:

1. Resolve the real names and require byte-parsed specs equal to the retained
   query's specs. Check historical metadata, current package identity, no owner
   open, no mathematical acceptance and saved/stdout result agreement.
2. Resolve the first real name plus one fresh test-only absent name. Require
   the exact missing name, the one diagnostic existing binding, and no specs
   or SPECS.json. If the chosen new name unexpectedly already exists, this
   control fails; do not silently change or relabel that outcome.
3. Change one character of the selected directory-manifest pin. Require the
   exact manifest-pin refusal, nonzero exit and no created result directory.
4. Change one character of PROFILE pin. Require the exact profile-pin refusal,
   nonzero exit and no created result directory.

No directory files are copied or mutated. Only DIRECTORY.json and fixed file
sizes are inspected directly by the driver; ENTRIES.bin/TREE.bin are neither
scanned nor hashed. Each installed child uses its normal authenticated point
reads. Existing core controls already cover altered rows/proof paths, ordering
premises and fixed/logarithmic read counts; do not duplicate them here.

The driver pins and rechecks its own source, the six executed package sources,
PROFILE, its selected INSTALLATION.json, directory manifest, real names and prior
result. Four auxiliary source pins come from PROFILE.files; the two core codec
pins come from the pinned installation's exact evidence/semantics roles and
files. It reads no native artifacts. Child imports perform the actual CLI's pin
checks. Synthetic mixed-name input is separately saved and rechecked.
The original historical source PROFILE is preserved even if different from the
selected package PROFILE. The output explains both without rewriting history.

Root should select one enclosing Windows Job with at most six active processes
(driver, its supervisor allowance and four direct children), bounded memory and
aggregate CPU. Suggested envelope: 90 wall seconds, 90 CPU seconds, 768 MiB,
six processes, bounded standard output/error. These are ceilings, not expected
costs. Each child retains its 30-wall/20-CPU cooperative allowance; the driver
checks a 55-second wall allowance, polls child logs at 50 ms with 2 MiB/128 KiB
caps per child, and terminates/reaps direct children on failure. The outer Job
is the hard aggregate containment/closure mechanism and remains required.

Expected success is four scoped passing controls and clean Job closure. It is
not a new theorem, owner validation, current-root absence or performance claim.
No native build, service, network call, repeat of the original symbol query or
mathematical campaign is included.
