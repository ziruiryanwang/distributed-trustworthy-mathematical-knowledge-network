# Reuse installed Lean library proofs in an ordinary contribution

This is development integration toward v5, not a completed public release.
The practical workflow is: author once, retain a candidate with missing library
dependencies, extract their complete proofs, then check the combined result.
No certificate generation is required.

## What the commands do

1. `owner.py contribute` elaborates owner-approved source. If its candidate
   references library names absent from the selected parent, retain its output
   directory. A missing-dependency result is not mathematical acceptance.
2. `owner.py extract-std` reconstructs the original preparation, checks its
   bindings against that same protected parent, and asks the installed exporter
   for complete declarations for genuinely missing names. It returns inert,
   pinned completion inputs. It does not admit mathematics.
3. `owner.py complete` checks the missing declarations and original contribution
   together through the existing receiver. Only this successful admission adds
   warranted mathematics. Existing publication commands can then expose it.

Use the ordinary owner's profile, runtime, catalog, custody, store identity and
resource arguments for each command. `extract-std` additionally requires:

```text
--parent-root <original-selected-parent>
--retained-contribution <original-contribution-output-directory>
--retained-request-sha256 <REQUEST.json-hash>
--retained-candidate-sha256 <candidate.json-hash>
--library-modules <structured-Std-module-names.json>
--output <fresh-extraction-directory>
```

The module file is a JSON array of structured Lean names, using the existing
formal-name encoding. Module components must be bounded ASCII identifiers;
the first must be `Std`. This is not a filesystem path or source-code argument.
Use the smallest installed module that contains the needed declarations.

On extraction success, `EXTRACTION-RESULT.json` identifies the exact candidate,
supplement, original target names and recovered prepared-bindings files. Pass
those files and reported hashes to [complete](../ordinary_library_package/README.md),
with the same parent and a fresh completion output directory. Do not silently
substitute the latest parent, edit a retained file, or treat a failed command
as permission to erase its cost or state. A post-admission reporting failure
may retain committed mathematics; inspect the returned acceptance information.

## Trust and cost

The exporter is an existing pinned local executable, not a downloaded peer
binary. Installed Std and its transitive compiled/private artifacts are
owner-trusted support. Named executable/runtime pins do not authenticate that
entire transitive installation. Peers exchange inert proof evidence, not these
trusted binaries. Hashes identify bytes; the receiver checks mathematics.

The public completion limits are 32 new units, 4 MiB combined candidate and
supplement, 131,072 expression nodes and 4,096 selected bindings. Extraction
can refuse a closure too large for this envelope. Native module loading and
parent-context materialization still cost real resources; this implementation
does not promise work proportional only to the missing proof closure. Every
explicit command has its own caller-selected allowance. Extraction, checking,
failed attempts and storage all count toward whole-workflow cost.

Windows Job containment bounds the selected child and tracks cleanup/accounting;
it is not a hostile-code filesystem sandbox. Unknown child CPU is retained as
unknown and charged conservatively, never recorded as measured zero.

## Current evidence and correction

File-only assembly01 passed: 122 payloads, profile
`1801fee2c3e9e39cef35182478acc693c923fef32ebb47ae2d7099d9a7776d3e`.
Its first preparation test found a real compatibility bug: the fixed basis
inventory includes four quotient entries of kind 7, while the new decoder used
the ordinary exported-unit bound 6. **Do not use this failed decoder as the
current working extraction path.** The fresh one-helper correction is under
[ordinary_library_support02](../ordinary_library_support02/); failed evidence
and all used bytes remain preserved. Native extraction qualification is separate
from mocked controls and file-only assembly.

This path does not yet supply arbitrary Mathlib/project imports or turn checked
snapshots into ordinary project libraries. Those are explicit interoperability
gaps, not reasons to distribute scratch modules containing assumed theorems.
See the [independent review](../../../research/cycles/v5-2026-10-22-native-library/ORDINARY-EXTRACTION-SUPPORT-REVIEW.md).
