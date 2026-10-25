# Advisory authoring-offer codec

Source-only implementation, 2026-10-24. No execution, network, filesystem state,
Git operation or mathematical acceptance occurred. Root selects tests separately.
Logical package role: `support/transport/authoring_offers.py`.

## Interface

Constants: `ROUTE=/v5/ordinary/authoring-offers`, `MAP_MAX=2097152`,
`REPLY_MAX=32768`, `MAX_KEYS=2048`, `MAX_OFFERS=8`.

- `request_limit(request)` validates the request and returns its reply byte cap.
- `OfferMap.from_bytes(raw, check_budget=None)` parses one canonical finite map,
  validates every row once and indexes immutable encoded offer bytes by exact key.
- `map.reply(request, check_budget=None)` and `reply(map, request, ...)` return a
  canonical bounded reply. No file access or whole-map scan occurs per request.
- `read_reply(raw, request)` validates an exact-key reply and returns its inert
  JSON document. `offer_id(offer)` hashes canonical claim bytes for deduplication,
  never for source authenticity, compatibility or mathematical correctness.

Request schema `DMKN_AUTHORING_OFFERS_REQUEST_V1`: exact fields `schema`,
`semantic_id`, `export_id`, `max_offers` (1..8), `max_bytes` (1..32768).
The two identities use the existing 64-lowercase-hex format.

Map schema `DMKN_AUTHORING_OFFER_MAP_V1`: exact fields `schema`, `entries`.
Each entry has `semantic_id`, `export_id`, `offers` (1..8). At most2048 entries;
an empty map is permitted. Missing keys return an empty list, not global absence.
Duplicate keys and duplicate canonical offers within one key refuse. Offer order
is operator-selected, not interpreted as correctness or authenticated ranking.

Each offer has exactly these fields:

| Field | Meaning and bound |
|---|---|
| repository | ASCII HTTPS URI, at most2048 bytes; no userinfo/query/fragment, backslashes or encoded controls; no DNS or connection |
| object_format / commit | `sha1` with40 or `sha256` with64 lowercase hexadecimal digits; not a branch or tag |
| project_dir | Empty for repository root, otherwise normalized relative path, at most1024 UTF-8 bytes; no absolute/traversal/backslash/reserved components |
| module / export_name | Existing structured Lean names, at most64 components and1024 name bytes, at most2048 encoded bytes each |
| toolchain | Bounded256-byte asserted toolchain token, not a compatibility check or command |

Each encoded offer is at most8192 bytes. Git object IDs remain advisory revision
claims: neither commit syntax nor a returned hash establishes repository existence,
all transitive dependencies, compiled semantics, or safe executable content.

## Reply and limits

Reply schema `DMKN_AUTHORING_OFFERS_REPLY_V1` has exact fields `schema`,
`semantic_id`, `export_id`, `status`, `offers`, `truncated`,
`mathematical_acceptance`, `source_availability`, `correspondence`,
`execution_approved`, `global_complete`.

Status is always `UNVERIFIED_AUTHORING_ASSOCIATIONS`; mathematical acceptance,
execution approval and global completeness are false. Availability/correspondence
are `NOT_CHECKED`. A provider may lie about every association and omit valid ones.
The client establishes syntax and query binding, not truthful or complete source
discovery. `truncated` is an unverified provider statement about its chosen reply.

The provider returns a deterministic prefix satisfying both count and byte caps.
If the empty envelope fits but no offer fits, it returns empty/truncated=true.
If even that envelope cannot fit, it refuses `AUTHORING_REPLY_MINIMUM`. It does not
skip a large first offer to return later ones, retry, enlarge a grant or fetch data.
At most8 rows are examined per query. Startup work is bounded by the selected map;
query work does not depend on all worldwide mathematics or all provider keys.

Raw map/reply JSON reuses `formal_features.strict`: exact canonical UTF-8 bytes,
duplicate-field and depth checks. Existing `ordinary_evidence.name_key` checks
encoded names; this is syntax only, not proof checking. In-memory map integrity
is a local-process premise. Cooperative callbacks do not replace outer containment.

No URI, name, commit or directory is passed to shell or filesystem here. The
consumer must separately choose any source retrieval, approve executable context,
compare exported exact targets, and independently admit mathematical outputs.
