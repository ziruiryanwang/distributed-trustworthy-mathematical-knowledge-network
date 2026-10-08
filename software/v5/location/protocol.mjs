/** Exact advisory v5 location wire. No mathematical or availability authority. */
import { createHash } from 'node:crypto'

export const ROLE = 'formal-index-v1'
export const REQUEST_SCHEMA = 'DMKN_V5_LOCATION_DESCRIPTOR_REQUEST_V1'
export const REPLY_SCHEMA = 'DMKN_V5_LOCATION_DESCRIPTOR_V1'
export const ASSURANCE = 'ADVISORY_SERVICE_HINT_ONLY'
export const MAX_DESCRIPTOR = 4096
export const need = (ok, code) => { if (!ok) throw new Error(code) }
export const uint = (value, low, high, code = 'INTEGER_BOUND') => {
  need(Number.isSafeInteger(value) && value >= low && value <= high, code); return value
}
export const hexid = value => { need(typeof value === 'string' && /^[0-9a-f]{64}$/.test(value), 'HASH_ENCODING'); return value }
export function fields (value, expected) {
  need(value != null && typeof value === 'object' && !Array.isArray(value) &&
    Object.keys(value).length === expected.length && expected.every(key => Object.hasOwn(value, key)), 'EXACT_FIELDS')
}
function ordered (value, depth = 0) {
  need(depth <= 32, 'LOCATION_JSON_DEPTH')
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value
  if (typeof value === 'number') { need(Number.isSafeInteger(value), 'LOCATION_JSON_INTEGER'); return value }
  if (Array.isArray(value)) return value.map(item => ordered(item, depth + 1))
  need(typeof value === 'object', 'LOCATION_JSON_VALUE')
  return Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key], depth + 1)]))
}
export const canonical = value => Buffer.from(JSON.stringify(ordered(value)), 'utf8')
export function parse (raw, maximum) {
  need(raw instanceof Uint8Array && raw.byteLength > 0 && raw.byteLength <= maximum, 'LOCATION_JSON_BYTES')
  const text = new TextDecoder('utf-8', { fatal: true }).decode(raw)
  let depth = 0; let quoted = false; let escaped = false
  for (const ch of text) {
    if (quoted) { if (escaped) escaped = false; else if (ch === '\\') escaped = true; else if (ch === '"') quoted = false } else if (ch === '"') quoted = true
    else if (ch === '[' || ch === '{') need(++depth <= 32, 'LOCATION_JSON_DEPTH')
    else if (ch === ']' || ch === '}') need(--depth >= 0, 'LOCATION_JSON_DEPTH')
  }
  const value = JSON.parse(text)
  need(canonical(value).equals(Buffer.from(raw)), 'LOCATION_CANONICAL_JSON')
  return value
}
const digest = (domain, value) => createHash('sha256').update(domain + '\0', 'ascii').update(canonical(value)).digest('hex')

export function features (value) {
  need(Array.isArray(value) && value.length >= 1 && value.length <= 8, 'LOCATION_FEATURE_COUNT')
  value.forEach(hexid)
  need(value.every((item, i) => i === 0 || item > value[i - 1]), 'LOCATION_FEATURE_ORDER')
  return value
}
export function routeSpec (namespace, selected, stripe = 0) {
  return { namespace: hexid(namespace), role: ROLE, predicate: { all: [...features(selected)] }, stripe: uint(stripe, 0, 255, 'LOCATION_STRIPE') }
}
export const routeKey = (namespace, selected, stripe = 0) => digest('DMKN-V5-INDEX-RENDEZVOUS-V1', routeSpec(namespace, selected, stripe))
export function descriptorRequest (namespace, selected, stripe, nonce, maximum) {
  return { schema: REQUEST_SCHEMA, ...routeSpec(namespace, selected, stripe), route_key: routeKey(namespace, selected, stripe),
    nonce: hexid(nonce), max_bytes: uint(maximum, 1024, MAX_DESCRIPTOR, 'LOCATION_DESCRIPTOR_BYTES') }
}
export function validateRequest (request) {
  fields(request, ['schema', 'namespace', 'role', 'predicate', 'stripe', 'route_key', 'nonce', 'max_bytes'])
  fields(request.predicate, ['all'])
  need(canonical(request).equals(canonical(descriptorRequest(request.namespace, request.predicate.all, request.stripe, request.nonce, request.max_bytes))), 'LOCATION_REQUEST_BINDING')
  return request
}

const B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
export function peerId (value) {
  need(typeof value === 'string' && value.length === 52, 'LOCATION_PEER_ID')
  let number = 0n
  for (const char of value) { const i = B58.indexOf(char); need(i >= 0, 'LOCATION_PEER_ID'); number = number * 58n + BigInt(i) }
  let hexadecimal = number.toString(16); if (hexadecimal.length % 2) hexadecimal = '0' + hexadecimal
  const leading = value.length - value.replace(/^1+/, '').length
  const raw = Buffer.concat([Buffer.alloc(leading), number === 0n ? Buffer.alloc(0) : Buffer.from(hexadecimal, 'hex')])
  need(raw.length === 38 && raw.subarray(0, 6).equals(Buffer.from('002408011220', 'hex')), 'LOCATION_ED25519_PEER_ID')
  return value
}
function ipv4 (value) {
  need(typeof value === 'string' && value.length > 0 && value.length <= 15, 'LOCATION_NUMERIC_IPV4')
  const parts = value.split('.')
  need(parts.length === 4 && parts.every(part => /^(0|[1-9][0-9]{0,2})$/.test(part) && Number(part) <= 255), 'LOCATION_CANONICAL_IPV4')
  return parts.map(Number)
}
export function publicIPv4 (value) {
  const [a, b, c, d] = ipv4(value)
  // Exact selected Python3.14 ipaddress policy, plus multicast/reserved refusal.
  return !(a === 0 || a === 10 || a === 127 || a >= 224 || (a === 100 && b >= 64 && b <= 127) ||
    (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) ||
    (a === 192 && ((b === 0 && c === 0 && d !== 9 && d !== 10) || (b === 0 && c === 2) || b === 168)) ||
    (a === 198 && (b === 18 || b === 19 || (b === 51 && c === 100))) || (a === 203 && b === 0 && c === 113))
}
function serverName (value) {
  if (value === null) return null
  need(typeof value === 'string' && value.length >= 1 && value.length <= 253 && value === value.toLowerCase() &&
    value.split('.').every(label => /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(label)), 'LOCATION_TLS_NAME')
  return value
}

export class OwnerEgressPolicy {
  #mode; #ports; #tests; #config
  constructor (config) {
    fields(config, ['schema', 'mode', 'public_ports', 'test_endpoints'])
    need(config.schema === 'DMKN_V5_OWNER_EGRESS_V1' && ['public-ipv4', 'loopback-test'].includes(config.mode), 'LOCATION_EGRESS_SCHEMA')
    const ports = config.public_ports; const tests = config.test_endpoints
    need(Array.isArray(ports) && ports.length <= 16 && Array.isArray(tests) && tests.length <= 16, 'LOCATION_EGRESS_ENTRIES')
    ports.forEach(port => uint(port, 1, 65535, 'LOCATION_PORT'))
    need(ports.every((port, i) => i === 0 || port > ports[i - 1]), 'LOCATION_CANONICAL_PORTS')
    const pairs = tests.map(item => {
      fields(item, ['host', 'port']); ipv4(item.host); need(item.host === '127.0.0.1', 'LOCATION_TEST_LOOPBACK_ONLY')
      return [item.host, uint(item.port, 1, 65535, 'LOCATION_PORT')]
    })
    need(pairs.every((pair, i) => i === 0 || pair[1] > pairs[i - 1][1]), 'LOCATION_CANONICAL_TEST_ENDPOINTS')
    need((config.mode === 'public-ipv4' && ports.length > 0 && pairs.length === 0) ||
      (config.mode === 'loopback-test' && pairs.length > 0 && ports.length === 0), 'LOCATION_EGRESS_MODE')
    this.#mode = config.mode; this.#ports = new Set(ports); this.#tests = new Set(pairs.map(pair => pair.join(':')))
    this.#config = structuredClone(config)
  }
  #destination (host, port) {
    ipv4(host); uint(port, 1, 65535, 'LOCATION_PORT')
    need(this.#mode === 'public-ipv4' ? publicIPv4(host) && this.#ports.has(port) : this.#tests.has(`${host}:${port}`), 'LOCATION_EGRESS')
  }
  endpoint (value) {
    fields(value, ['host', 'port', 'tls', 'server_name'])
    this.#destination(value.host, value.port)
    need(typeof value.tls === 'boolean' && (this.#mode !== 'public-ipv4' || value.tls), 'LOCATION_PUBLIC_TLS_PORT')
    serverName(value.server_name); need(value.tls || value.server_name === null, 'LOCATION_PLAINTEXT_HAS_NO_TLS_NAME')
    return structuredClone(value)
  }
  peerAddress (value, expectedPeer = null) {
    need(typeof value === 'string' && value.length <= 256, 'LOCATION_PEER_ADDRESS')
    const match = /^\/ip4\/([0-9.]+)\/tcp\/([1-9][0-9]{0,4})(?:\/p2p\/([^/]+))?$/.exec(value)
    need(match != null, 'LOCATION_DIRECT_TCP_ONLY')
    this.#destination(match[1], Number(match[2]))
    if (match[3] != null) peerId(match[3])
    if (expectedPeer != null) { peerId(expectedPeer); need(match[3] == null || match[3] === expectedPeer, 'LOCATION_ADDRESS_PEER_BINDING') }
    return value
  }
  listenAddress (value) {
    need(typeof value === 'string' && value.length <= 256, 'LOCATION_LISTEN_ADDRESS')
    const match = /^\/ip4\/([0-9.]+)\/tcp\/([1-9][0-9]{0,4})$/.exec(value)
    need(match != null, 'LOCATION_LISTEN_ADDRESS'); ipv4(match[1]); uint(Number(match[2]), 1, 65535, 'LOCATION_PORT')
    if (this.#mode === 'public-ipv4' && match[1] === '0.0.0.0') need(this.#ports.has(Number(match[2])), 'LOCATION_LISTEN_PORT')
    else this.#destination(match[1], Number(match[2]))
    return value
  }
  inboundAddress (value) {
    need(typeof value === 'string' && value.length <= 256, 'LOCATION_PEER_ADDRESS')
    const match = /^\/ip4\/([0-9.]+)\/tcp\/([1-9][0-9]{0,4})(?:\/p2p\/([^/]+))?$/.exec(value)
    need(match != null, 'LOCATION_DIRECT_TCP_ONLY'); ipv4(match[1]); uint(Number(match[2]), 1, 65535, 'LOCATION_PORT')
    if (match[3] != null) peerId(match[3])
    // Remote source ports are ephemeral; only outbound destinations use #ports.
    need(this.#mode === 'public-ipv4' ? publicIPv4(match[1]) : match[1] === '127.0.0.1', 'LOCATION_INBOUND_ADDRESS')
    return value
  }
  report () { return { config: structuredClone(this.#config), https_trust: 'OWNER_SYSTEM_CA_ONLY', ca_store_updates: 'TRUSTED_OWNER_ENVIRONMENT_NOT_PINNED_ROOT_SET' } }
}

export function makeDescriptor (request, authenticatedLocalPeer, endpoints, policy) {
  validateRequest(request); peerId(authenticatedLocalPeer)
  need(policy instanceof OwnerEgressPolicy && Array.isArray(endpoints) && endpoints.length >= 1 && endpoints.length <= 4, 'LOCATION_ENDPOINT_COUNT')
  const selected = endpoints.map(value => policy.endpoint(value))
  need(new Set(selected.map(value => canonical(value).toString('hex'))).size === selected.length, 'LOCATION_DUPLICATE_ENDPOINT')
  const reply = { schema: REPLY_SCHEMA, namespace: request.namespace, role: ROLE, route_key: request.route_key,
    nonce: request.nonce, peer_id: authenticatedLocalPeer, endpoints: selected, assurance: ASSURANCE,
    global_complete: false, mathematical_acceptance: false }
  const raw = canonical(reply); need(raw.length <= request.max_bytes, 'LOCATION_DESCRIPTOR_BYTES')
  return raw
}
