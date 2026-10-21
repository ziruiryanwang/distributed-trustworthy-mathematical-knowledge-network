# Integration02: exact pinned-map preflight correction

2026-10-21, core_release. Source-only correction explicitly selected by root.
The used `integration.py` (`d6445354...`) and failed integration01 output remain
unchanged. No runtime, product import, test, proof, or Git mutation was performed.

Fresh file: `software/v5/incremental_native/integration02.py`, 16068 bytes,
SHA-256 `ea0269008128f774199d28c185cb4494564cac85cca88b2778307530ba9728ce`.

## Complete semantic diff

```diff
+MAP_BYTES = 2805479
 MAP_SHA = "d3519be18a8281355f7ec915ce3156735be649892c379f5008b5b1031026f9b0"
 ...
-    need(map_row["sha256"] == MAP_SHA, "CURRENT_MAP_IDENTITY")
-    raw = read(pin(map_row, 2*MIB), 2*MIB)
+    need(map_row["sha256"] == MAP_SHA and map_row["bytes"] == MAP_BYTES, "CURRENT_MAP_IDENTITY")
+    raw = read(pin(map_row, MAP_BYTES), MAP_BYTES)
```

A read-only whole-file diff confirms no other change. The selected map is
2805479 bytes, not the smaller SDK source total; it contains additional
distribution data. Integration01 stopped in this preflight before constructing
verifiers or executing checkers. This is an adapter-bound error, not an observed
mathematical/checker failure. The new route accepts only that exact already
pinned map size/hash, not an arbitrary larger source or input object.

## Remaining bounds checked against retained input metadata

Read-only scalar projection of the retained integration01 input and its pinned
map gives:

| Item | Actual bytes | Unchanged bound |
|---|---:|---:|
| Owner input JSON | 10264 | 1048576 |
| Largest mapped SDK source | 51539 | 2097152 |
| Supervisor manifest | 1070384 | 8388608 |
| Native executable | 1713152 | 134217728 |
| Receipt executable | 66652160 | 134217728 |
| Largest selected Python runtime file | 6778592 | 134217728 |
| Largest retained packet | 549456 | 1048576 |

The three successor source replacements are each below 51539 bytes. The largest
selected supervisor helper is 41984 bytes, below its unchanged 4194304-byte
bound. The new adapter itself is 16068 bytes, below its 2097152-byte read bound.
No other initial file read has the mistaken two-MiB map cap.

Counts and execution/output reservations remain exactly the already reviewed
ones: 114 selected files / 100 Python sources / 18 Python runtime files /
119 receipt pins / 101 native pins; two packets totaling 1048097 bytes; one
223594-byte receipt verification; three logical native reservations, two actual
native checks, one exact reuse; 50 reserved worker CPU. The expected per-result
records contain at most two fixed-size journals/observations, not packet/proof
bodies; the existing one-MiB result read is not a map-sized serialization.

No operation, CPU, wall, memory, source-object, packet, result or output limit
was widened. Root owns fresh selector02 and any eventual launch. Independent
review of this narrow diff remains required; original failed evidence is not
reclassified or overwritten.
