/** Only new role guards. No former controls, runtime packages or sockets. */
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { validateConfig, DESCRIPTOR_PROTOCOL } from './maintained_roles.mjs'
import { createLocator } from './role_composition.mjs'
assert.equal(process.argv.length, 4)
const raw = readFileSync(process.argv[2]); assert.ok(raw.length <= 16384)
assert.equal(createHash('sha256').update(raw).digest('hex'), process.argv[3])
const cfg = JSON.parse(raw)
assert.equal(cfg.role, 'reader'); assert.deepEqual(cfg.endpoints, [])
assert.equal(validateConfig(cfg).cfg.role, 'reader')
const endpoint = { host: '127.0.0.1', port: cfg.egress.test_endpoints[0].port, tls: false, server_name: null }
assert.throws(() => validateConfig({ ...cfg, endpoints: [endpoint] }), /ROLE_ENDPOINTS/)
assert.throws(() => validateConfig({ ...cfg, role: 'index-provider' }), /ROLE_ENDPOINTS/)
assert.throws(() => validateConfig({ ...cfg, role: 'unknown' }), /CONFIG_SCHEMA_ROLE/)
assert.equal(validateConfig({ ...cfg, role: 'index-provider', endpoints: [endpoint] }).cfg.role, 'index-provider')
const locator = createLocator({ tcp: { tcp: () => () => { throw new Error('No transport construction in role control') } } }, cfg)
await assert.rejects(locator.publish(['1'.repeat(64)]), /READER_CANNOT_PUBLISH/)
await assert.rejects(locator.withdraw(['1'.repeat(64)]), /READER_CANNOT_WITHDRAW/)
let refused = null
await locator._serve({ abort (error) { refused = error } }, null)
assert.match(refused.message, /READER_CANNOT_SERVE/)
assert.equal(locator.stats.commands, 0); assert.equal(locator.stats.descriptor_requests, 0)
assert.equal(locator.status().role, 'reader'); assert.deepEqual(locator.cfg.endpoints, [])
await locator.stop()
// Run the actual startup branch with explicit runtime/metadata mocks. This
// tests handler registration, not libp2p, Noise, key generation or SQLite.
const alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
let number = BigInt('0x2408011220' + '11'.repeat(32)); let encoded = ''
while (number > 0n) { encoded = alphabet[Number(number % 58n)] + encoded; number /= 58n }
const owner = { toString: () => '1' + encoded }
class MockStore {
  constructor () { this.db = { prepare: () => ({ iterate: () => [] }) } }
  async open () {} async close () {} report () { return { mocked: true } }
}
const registrations = []
const mock = {
  tcp: { tcp: () => () => { throw new Error('No mock transport construction') } },
  keys: { generateKeyPair: async () => ({}), privateKeyToProtobuf: () => Buffer.from('MOCK_NOT_A_KEY') },
  peers: { peerIdFromPrivateKey: () => owner }, quota: { QuotaDatastore: MockStore },
  datastore: { Key: class {} }, dhtUtils: { toProviderKey: () => { throw new Error('No mock publication') } },
  noise: { noise: () => ({}) }, yamux: { yamux: () => ({}) }, identify: { identify: () => ({}) },
  dht: { kadDHT: () => ({}) },
  libp2p: { createLibp2p: async () => ({ peerId: owner, getMultiaddrs: () => [],
    handle: async protocol => { registrations.push(protocol) }, start: async () => {}, stop: async () => {} }) }
}
for (const role of ['reader', 'index-provider']) {
  registrations.length = 0
  const roleCfg = { ...cfg, role, state: cfg.state + '-mock-' + role,
    endpoints: role === 'reader' ? [] : [endpoint] }
  const value = createLocator(mock, roleCfg)
  try {
    await value.start({ create: true })
    assert.deepEqual(registrations, role === 'reader' ? [] : [DESCRIPTOR_PROTOCOL])
  } finally { await value.stop() }
}
console.log(JSON.stringify({ status: 'PASS', role_groups: 4, reader_endpoints: 0,
  reader_publish_refused: true, reader_withdraw_refused: true, reader_serving_refused: true,
  actual_startup_mock_runtime_registration: 'READER_NONE_PROVIDER_DESCRIPTOR',
  refused_calls_changed_counters: false, real_network_calls: 0, mathematical_acceptance: false }))
