/** Focused source-selected exact-custody controls. No live node or networking.
 * Uses actual protocol, intent, routing wrapper and stream-framing code with
 * finite inert runtime/store/streams. The parent owns execution and containment.
 */
import assert from 'node:assert/strict'
import { readFileSync, writeFileSync, statSync } from 'node:fs'
import { isAbsolute, join, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import { createHash } from 'node:crypto'

const args = process.argv.slice(2)
assert.equal(args.length, 6)
const options = {}
for (let i = 0; i < args.length; i += 2) {
  assert.ok(['--code', '--vectors', '--output'].includes(args[i]) && !(args[i] in options))
  assert.ok(isAbsolute(args[i + 1])); options[args[i]] = resolve(args[i + 1])
}
assert.equal(Object.keys(options).length, 3)
const source = join(options['--code'], 'portable', 'location')
const bounded = (path, maximum) => {
  assert.ok(statSync(path).isFile() && statSync(path).size <= maximum)
  const raw = readFileSync(path); assert.ok(raw.length > 0 && raw.length <= maximum); return raw
}
const vector = JSON.parse(bounded(options['--vectors'], 65536).toString('utf8'))
const load = name => import(pathToFileURL(join(source, name)).href)
const P = await load('protocol.mjs')
const { MaintainedLocator, validateConfig, DESCRIPTOR_PROTOCOL, BODY_DESCRIPTOR_PROTOCOL } = await load('maintained_roles.mjs')
const { intentStoreClass } = await load('intent.mjs')
const { commandEnvelope, LocalFrames } = await load('ipc_wire.mjs')
const output = { schema: 'DMKN_V5_EXACT_CUSTODY_NODE_CONTROLS_V1', status: 'PASS', groups: {},
  scope: 'ACTUAL_PURE_AND_WRAPPER_CODE_WITH_INERT_RUNTIME_NO_NODE_START_OR_NETWORK',
  mathematical_acceptance: false }

function peer (seed) {
  const alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
  let number = BigInt('0x' + Buffer.concat([Buffer.from('002408011220', 'hex'), Buffer.alloc(32, seed)]).toString('hex'))
  let encoded = ''
  while (number > 0n) { encoded = alphabet[Number(number % 58n)] + encoded; number /= 58n }
  return P.peerId('1' + encoded)
}
const owner = vector.reply.peer_id
const other = peer(3)
const endpoint = vector.reply.endpoints[0]
const config = (overrides = {}) => ({
  schema: 'DMKN_V5_MAINTAINED_LOCATION_ROLES_V2', role: 'index-provider',
  state: join(options['--code'], 'inert-state-never-created'),
  namespace: vector.index_spec.namespace, body_domain: structuredClone(vector.domain),
  egress: structuredClone(vector.policy),
  listen: [`/ip4/${endpoint.host}/tcp/${endpoint.port}`], announce: [], bootstrap: [],
  endpoints: [structuredClone(endpoint)],
  limits: { service_ms: 60000, operation_ms: 60000, query_events: 8, provider_limit: 4,
    advertised_keys: 2, provider_ttl_ms: 9000, reprovide_interval_ms: 1000, maintenance_ms: 1000,
    commands: 16, descriptor_requests: 8, descriptor_reply_bytes: 32768, metadata: {},
    transport: { outbound_attempts: 16, inbound_upgrades: 16, receive_bytes: 65536, send_bytes: 65536 } },
  ...overrides
})
class Key {
  constructor (value) { this.value = value }
  toString () { return this.value }
}
const cid = key => ({ version: 1, code: 0x55,
  multihash: { code: 0x12, size: 32, digest: Buffer.from(key, 'hex') } })
const providerKey = (prefix, selected, identity) => new Key(`${prefix}/k${Buffer.from(selected.multihash.digest).toString('hex')}/${identity}`)
class InertQuotaStore {
  constructor () {
    this.rows = new Map(); this.transactions = 0; this.closed = false; this.rejectKey = null
    this.db = { prepare: () => ({ get: key => this.rows.has(key) ? { present: 1 } : undefined,
      iterate: () => [...this.rows.keys()].map(k => ({ k })) }) }
  }
  _key (value) { return typeof value === 'string' ? value : value.toString() }
  _put (key, raw) {
    const name = this._key(key)
    assert.notEqual(name, this.rejectKey, 'INERT_INJECTED_TRANSACTION_FAILURE')
    this.rows.set(name, Buffer.from(raw))
  }
  _delete (key) { this.rows.delete(this._key(key)) }
  _transaction (callback) {
    const before = new Map(this.rows); this.transactions++
    try { callback() } catch (error) { this.rows = before; throw error }
  }
  async has (key) { return this.rows.has(this._key(key)) }
  async *queryKeys ({ prefix }) { for (const key of this.rows.keys()) if (key.startsWith(prefix)) yield new Key(key) }
  async close () { this.closed = true }
  report () { return { scope: 'INERT_TRANSACTION_PRIMITIVE', entries: this.rows.size } }
}
const Store = intentStoreClass(InertQuotaStore, Key, providerKey)
function framed (raw) {
  const size = Buffer.alloc(4); size.writeUInt32BE(raw.length); return Buffer.concat([size, raw])
}
function gate () {
  let release
  const promise = new Promise(resolvePromise => { release = resolvePromise })
  return { promise, release }
}
class InertStream {
  constructor (raw, held = null) {
    this.incoming = framed(raw); this.held = held; this.sent = []; this.closed = 0; this.aborted = null
  }
  async *[Symbol.asyncIterator] () {
    if (this.held != null) await this.held.promise
    yield this.incoming
  }
  send (piece) { this.sent.push(Buffer.from(piece)); return true }
  async onDrain () { throw new Error('UNEXPECTED_INERT_BACKPRESSURE') }
  async close () { this.closed++ }
  abort (error) { this.aborted = error }
  reply () {
    const raw = Buffer.concat(this.sent)
    assert.ok(raw.length >= 4); assert.equal(raw.readUInt32BE(), raw.length - 4)
    return P.parse(raw.subarray(4), 4096)
  }
}
function locator (cfg = config()) {
  const stats = { provides: [], finds: [], dials: [], merges: 0, stops: 0 }
  const runtime = {
    datastore: { Key },
    cid: { CID: { createV1: (code, multihash) => ({ version: 1, code, multihash }) } },
    digest: { create: (code, digest) => ({ code, size: digest.length, digest }) },
    peers: { peerIdFromString: value => ({ toString: () => P.peerId(value) }) },
    addresses: { multiaddr: value => ({ toString: () => value }) },
    libp2p: { createLibp2p: () => { throw new Error('REAL_NODE_START_FORBIDDEN') } }
  }
  const result = new MaintainedLocator(runtime, cfg)
  result.until = performance.now() + 60000
  result.store = new Store('unused', {}, owner)
  result.node = {
    peerId: { toString: () => owner }, getMultiaddrs: () => [],
    services: { dht: { routingTable: { size: 1 },
      async *provide (selected, opts) {
        opts.signal.throwIfAborted(); stats.provides.push(selected)
        opts.onProgress({ type: 'kad-dht:query:send-query' })
        yield { name: 'PEER_RESPONSE', messageName: 'ADD_PROVIDER' }
      },
      async *findProviders (selected, opts) {
        opts.signal.throwIfAborted(); stats.finds.push(selected)
        opts.onProgress({ type: 'kad-dht:query:send-query' })
        yield { name: 'PROVIDER', providers: [{ id: { toString: () => other },
          multiaddrs: [{ toString: () => `/ip4/${endpoint.host}/tcp/${endpoint.port}/p2p/${other}` }] }] }
      } } },
    peerStore: { merge: async () => { stats.merges++ } },
    dialProtocol: async (id, protocol) => {
      stats.dials.push(protocol)
      assert.equal(id.toString(), other)
      const request = protocol === BODY_DESCRIPTOR_PROTOCOL ? vector.request : indexRequest()
      const raw = protocol === BODY_DESCRIPTOR_PROTOCOL
        ? P.makeBodyDescriptor(request, other, [endpoint], result.policy)
        : P.makeDescriptor(request, other, [endpoint], result.policy)
      return new InertStream(raw)
    },
    stop: async () => { stats.stops++ }
  }
  return { value: result, stats }
}
const indexRequest = () => P.descriptorRequest(vector.index_spec.namespace,
  vector.index_spec.predicate.all, vector.index_spec.stripe, vector.request.nonce, 4096)
const routeTicket = (body, n = 1) => ({ ticket: n, operation: body ? 'body-route' : 'route',
  route_key: body ? vector.key : vector.index_key,
  spec: structuredClone(body ? vector.spec : vector.index_spec), event_cap: 4, peer_cap: 1, remaining_wall_ms: 60000 })
const descriptorTicket = (body, n = 1) => ({ ticket: n, operation: body ? 'body-descriptor' : 'descriptor',
  peer: other, request: body ? structuredClone(vector.request) : indexRequest(),
  max_reply_bytes: 4096, until: 0, remaining_wall_ms: 60000 })
const connection = { remoteAddr: { toString: () => '/ip4/127.0.0.1/tcp/43000' },
  remotePeer: { toString: () => other } }
async function group (name, work) {
  try { output.groups[name] = { status: 'PASS', ...await work() } }
  catch (error) { output.status = 'FAIL'; output.groups[name] = { status: 'FAIL',
    error: `${error.name}: ${error.message}`.slice(0, 2000), stack: String(error.stack).slice(0, 4000) } }
}

await group('protocol_cross_language_and_role_isolation', async () => {
  assert.equal(P.bodyNamespace(vector.domain), vector.namespace)
  assert.deepEqual(P.bodyRef(vector.body), vector.body)
  assert.deepEqual(P.bodyRouteSpec(vector.namespace, vector.body), vector.spec)
  assert.equal(P.bodyRouteKey(vector.namespace, vector.body), vector.key)
  assert.deepEqual(P.bodyDescriptorRequest(vector.namespace, vector.body, vector.request.nonce), vector.request)
  assert.deepEqual(P.validateBodyRequest(vector.request), vector.request)
  const policy = new P.OwnerEgressPolicy(vector.policy)
  assert.deepEqual(P.parse(P.makeBodyDescriptor(vector.request, owner, [endpoint], policy), 4096), vector.reply)
  assert.deepEqual(P.routeSpec(vector.index_spec.namespace, vector.index_spec.predicate.all, vector.index_spec.stripe), vector.index_spec)
  assert.equal(P.routeKey(vector.index_spec.namespace, vector.index_spec.predicate.all, vector.index_spec.stripe), vector.index_key)
  const independent = (tag, value) => createHash('sha256').update(tag + '\0', 'ascii').update(P.canonical(value)).digest('hex')
  assert.equal(independent('DMKN-V5-BODY-RENDEZVOUS-V1', vector.spec), vector.key)
  assert.equal(independent('DMKN-V5-INDEX-RENDEZVOUS-V1', vector.index_spec), vector.index_key)
  for (const field of Object.keys(vector.body)) {
    const changed = { ...vector.body, [field]: field === 'universes' ? 4 : 'aa'.repeat(32) }
    assert.notEqual(P.bodyRouteKey(vector.namespace, changed), vector.key)
  }
  for (const field of ['foundation', 'policy']) assert.notEqual(P.bodyNamespace({ ...vector.domain, [field]: 'bb'.repeat(32) }), vector.namespace)
  assert.throws(() => P.bodyNamespace({ ...vector.domain, index_profile: 'aa'.repeat(32) }))
  for (const bad of [{ ...vector.body, universes: true }, { ...vector.body, extra: 0 }, { ...vector.body, export_id: 'x' }]) assert.throws(() => P.bodyRef(bad))
  for (const bad of [{ ...vector.request, schema: P.REQUEST_SCHEMA }, { ...vector.request, role: P.ROLE },
    { ...vector.request, route_key: vector.index_key }, { ...vector.request, max_bytes: 2048 },
    { ...vector.request, extra: 0 }]) assert.throws(() => P.validateBodyRequest(bad))
  assert.throws(() => P.validateRequest(vector.request))
  assert.throws(() => P.validateBodyRequest(indexRequest()))
  assert.throws(() => P.makeBodyDescriptor(vector.request, owner, [endpoint, endpoint], policy))
  assert.throws(() => P.makeBodyDescriptor(vector.request, owner, [{ ...endpoint, port: 1 }], policy))
  P.validateIntentSpec(vector.spec, vector.key); P.validateIntentSpec(vector.index_spec, vector.index_key)
  assert.throws(() => P.validateIntentSpec({ ...vector.spec, role: 'unknown' }, vector.key))
  return { body_key: vector.key, index_key: vector.index_key, request_bytes: P.canonical(vector.request).length,
    body_reply_bytes: P.makeBodyDescriptor(vector.request, owner, [endpoint], policy).length,
    cross_language_equal: true, role_substitution_refused: true }
})

await group('same_locator_wrappers_and_shared_publication_caps', async () => {
  const old = config({ schema: 'DMKN_V5_MAINTAINED_LOCATION_ROLES_V1' }); delete old.body_domain
  validateConfig(old)
  assert.throws(() => validateConfig({ ...old, body_domain: vector.domain }))
  const legacy = locator(old)
  try {
    await assert.rejects(legacy.value.publishBody(vector.body), /BODY_LOCATION_STARTUP_DOMAIN_REQUIRED/)
    await assert.rejects(legacy.value.locateBody(routeTicket(true)), /BODY_LOCATION_STARTUP_DOMAIN_REQUIRED/)
    await assert.rejects(legacy.value.descriptorBody(descriptorTicket(true)), /BODY_LOCATION_STARTUP_DOMAIN_REQUIRED/)
    assert.equal(legacy.value.stats.commands, 0)
  } finally { await legacy.value.stop() }
  const capConfig = config(); capConfig.limits.commands = 3
  const shared = locator(capConfig)
  try {
    const first = await shared.value.publish(vector.index_spec.predicate.all, vector.index_spec.stripe)
    const second = await shared.value.publishBody(vector.body)
    for (const row of [first, second]) {
      assert.equal(row.status, 'HINT_DISPATCHED_UNACKNOWLEDGED'); assert.equal(row.remote_placement_confirmed, false)
      assert.equal(row.census.add_provider_write, 1)
    }
    assert.equal(shared.stats.provides.length, 2)
    await assert.rejects(shared.value.publishBody({ ...vector.body, universes: 4 }), /LOCATION_ADVERTISEMENT_CAP/)
    assert.equal(shared.value.stats.commands, 3)
    assert.equal(shared.stats.provides.length, 2)
    await assert.rejects(shared.value.withdrawBody(vector.body), /LOCATION_COMMAND_CAP_OR_BUSY/)
    assert.equal(shared.value.stats.commands, 3)
  } finally { await shared.value.stop() }
  const reader = locator(config({ role: 'reader', endpoints: [] }))
  try {
    const oldRoute = await reader.value.locate(routeTicket(false))
    const bodyRoute = await reader.value.locateBody(routeTicket(true, 2))
    assert.deepEqual(oldRoute.peers, [other]); assert.deepEqual(bodyRoute.peers, [other])
    assert.equal(reader.value.known.size, 1); assert.equal(reader.stats.finds.length, 2)
    const a = await reader.value.descriptor(descriptorTicket(false, 3))
    const b = await reader.value.descriptorBody(descriptorTicket(true, 4))
    assert.deepEqual(reader.stats.dials, [DESCRIPTOR_PROTOCOL, BODY_DESCRIPTOR_PROTOCOL])
    assert.equal(P.parse(Buffer.from(a.raw_base64, 'base64'), 4096).schema, P.REPLY_SCHEMA)
    assert.equal(P.parse(Buffer.from(b.raw_base64, 'base64'), 4096).schema, P.BODY_REPLY_SCHEMA)
    assert.equal(a.authenticated_peer, other); assert.equal(b.authenticated_peer, other)
    await assert.rejects(reader.value.publishBody(vector.body), /LOCATION_READER_CANNOT_PUBLISH/)
    await assert.rejects(reader.value.withdrawBody(vector.body), /LOCATION_READER_CANNOT_WITHDRAW/)
    await assert.rejects(reader.value.locateBody({ ...routeTicket(true), spec: vector.index_spec }))
    await assert.rejects(reader.value.locateBody({ ...routeTicket(true), route_key: vector.index_key }))
    await assert.rejects(reader.value.descriptorBody({ ...descriptorTicket(true), request: indexRequest() }))
    assert.equal(reader.value.stats.commands, 4)
    assert.equal(reader.value.transportBudget.report().send_admitted_bytes, 0)
  } finally { await reader.value.stop() }
  return { actual_node_start_calls: 0, shared_publications: 2, common_key_and_command_caps: true,
    same_reader_known_peer_map: true, exact_descriptor_protocols: [DESCRIPTOR_PROTOCOL, BODY_DESCRIPTOR_PROTOCOL] }
})

await group('intent_atomic_role_validation_and_withdrawal', async () => {
  const store = new Store('unused', {}, owner)
  try {
    await store.enableIntent(cid(vector.index_key), vector.index_key, vector.index_spec, {})
    await store.enableIntent(cid(vector.key), vector.key, vector.spec, {})
    assert.equal(store.transactions, 2); assert.equal(store.rows.size, 4)
    assert.ok(store.rows.has('/application/published/' + vector.index_key))
    assert.ok(store.rows.has('/application/published/' + vector.key))
    const saved = new Map(store.rows)
    await assert.rejects(store.enableIntent(cid(vector.key), vector.key, vector.index_spec, {}))
    await assert.rejects(store.enableIntent(cid(vector.key), vector.key, { ...vector.spec, role: 'anything' }, {}))
    assert.deepEqual(store.rows, saved); assert.equal(store.transactions, 2)
    const ownRecord = providerKey('/dmknv5/provider', cid(vector.key), owner)
    store._put(ownRecord, Buffer.from('hint'))
    assert.ok(await store.has(ownRecord))
    await store.revokeIntent(cid(vector.key), vector.key, {})
    assert.equal(await store.has(ownRecord), false)
    assert.equal(await store.has(new Key('/application/published/' + vector.key)), false)
    assert.throws(() => store._put(ownRecord, Buffer.from('late-renewal')), /LOCATION_LOCAL_PROVIDER_INTENT_REVOKED/)
    const nextBody = { ...vector.body, universes: 4 }
    const nextSpec = P.bodyRouteSpec(vector.namespace, nextBody), nextKey = P.bodyRouteKey(vector.namespace, nextBody)
    store.rejectKey = '/application/published/' + nextKey
    const before = new Map(store.rows)
    await assert.rejects(store.enableIntent(cid(nextKey), nextKey, nextSpec, {}), /INERT_INJECTED_TRANSACTION_FAILURE/)
    assert.deepEqual(store.rows, before)
    return { exact_role_validation: true, one_transaction_per_intent_pair: true,
      provider_renewal_after_revoke_refused: true,
      atomic_primitive_scope: 'INERT_TRANSACTION_ROLLBACK_NOT_NEW_SQLITE_QUALIFICATION' }
  } finally { await store.close() }
})

await group('shared_descriptor_stream_caps_and_ipc', async () => {
  const cappedConfig = config(); cappedConfig.limits.descriptor_requests = 2
  const serving = locator(cappedConfig)
  try {
    await serving.value.publish(vector.index_spec.predicate.all, vector.index_spec.stripe)
    await serving.value.publishBody(vector.body)
    const oldStream = new InertStream(P.canonical(indexRequest()))
    const bodyStream = new InertStream(P.canonical(vector.request))
    await serving.value._serve(oldStream, connection)
    await serving.value._serveBody(bodyStream, connection)
    assert.equal(oldStream.aborted, null); assert.equal(bodyStream.aborted, null)
    assert.equal(oldStream.closed, 1); assert.equal(bodyStream.closed, 1)
    assert.equal(oldStream.reply().schema, P.REPLY_SCHEMA); assert.deepEqual(bodyStream.reply(), vector.reply)
    assert.equal(serving.value.stats.descriptor_requests, 2)
    const refused = new InertStream(P.canonical(vector.request))
    await serving.value._serveBody(refused, connection)
    assert.match(refused.aborted.message, /LOCATION_DESCRIPTOR_SERVICE_CAP/)
    assert.equal(refused.sent.length, 0); assert.equal(serving.value.stats.descriptor_requests, 2)
    assert.equal(serving.value.serving, 0); assert.equal(serving.value.stats.reserved_descriptor_reply_bytes, 0)
  } finally { await serving.value.stop() }
  const simultaneous = locator()
  const hold = gate()
  try {
    await simultaneous.value.publish(vector.index_spec.predicate.all, vector.index_spec.stripe)
    await simultaneous.value.publishBody(vector.body)
    const first = new InertStream(P.canonical(indexRequest()), hold)
    const second = new InertStream(P.canonical(vector.request), hold)
    const a = simultaneous.value._serve(first, connection), b = simultaneous.value._serveBody(second, connection)
    assert.equal(simultaneous.value.serving, 2)
    assert.equal(simultaneous.value.stats.reserved_descriptor_reply_bytes, 8192)
    const third = new InertStream(P.canonical(vector.request))
    await simultaneous.value._serveBody(third, connection)
    assert.match(third.aborted.message, /LOCATION_DESCRIPTOR_SERVICE_CAP/)
    hold.release(); await Promise.all([a, b])
    assert.equal(first.aborted, null); assert.equal(second.aborted, null)
    assert.equal(simultaneous.value.stats.reserved_descriptor_reply_bytes, 0)
    assert.equal(simultaneous.value.serving, 0)
  } finally { hold.release(); await simultaneous.value.stop() }
  const byteConfig = config(); byteConfig.limits.descriptor_reply_bytes = 4096
  const byteCapped = locator(byteConfig)
  try {
    await byteCapped.value.publish(vector.index_spec.predicate.all, vector.index_spec.stripe)
    await byteCapped.value.publishBody(vector.body)
    await byteCapped.value._serve(new InertStream(P.canonical(indexRequest())), connection)
    assert.ok(byteCapped.value.stats.descriptor_reply_bytes > 0)
    const body = new InertStream(P.canonical(vector.request))
    await byteCapped.value._serveBody(body, connection)
    assert.match(body.aborted.message, /LOCATION_DESCRIPTOR_SERVICE_CAP/)
    assert.equal(byteCapped.value.stats.descriptor_requests, 1)
  } finally { await byteCapped.value.stop() }
  const invalid = locator()
  try {
    const stream = new InertStream(P.canonical(vector.request))
    await invalid.value._serveBody(stream, connection)
    assert.match(stream.aborted.message, /LOCATION_ROUTE_NOT_ADVERTISED/)
    assert.equal(stream.sent.length, 0); assert.equal(invalid.value.stats.descriptor_failures, 1)
    assert.equal(invalid.value.stats.reserved_descriptor_reply_bytes, 0)
  } finally { await invalid.value.stop() }
  const commands = ['locate', 'descriptor', 'publish', 'withdraw', 'status', 'stop',
    'locate-body', 'descriptor-body', 'publish-body', 'withdraw-body']
  const envelope = command => ({ schema: 'DMKN_V5_LOCATION_IPC_COMMAND_V1', sequence: 1,
    command, payload: {}, remaining_wall_ms: 1000 })
  for (const name of commands) commandEnvelope(envelope(name), 0)
  assert.throws(() => commandEnvelope(envelope('arbitrary'), 0))
  assert.throws(() => commandEnvelope(envelope('locate-body'), 1))
  assert.throws(() => commandEnvelope({ ...envelope('locate-body'), extra: 1 }, 0))
  assert.throws(() => commandEnvelope({ ...envelope('locate-body'), sequence: 63 }, 62))
  const chunks = []
  const writable = { write: raw => { chunks.push(raw); return true } }
  const empty = { async *[Symbol.asyncIterator] () {} }
  const frames = new LocalFrames(empty, writable, { frame_bytes: 16384, total_bytes: 1024 ** 2, frames: 1 })
  const signal = new AbortController().signal
  await frames.write(envelope('locate-body'), signal)
  await assert.rejects(frames.write(envelope('descriptor-body'), signal), /LOCATION_IPC_WRITE_CAP/)
  assert.equal(frames.report().write_frames, 1)
  const entry = bounded(join(source, 'node_entry_services.mjs'), 2 * 1024 ** 2).toString('utf8')
  for (const name of commands.slice(6)) assert.ok(entry.includes(`case '${name}':`))
  assert.match(entry, /case 'descriptor-body':\s+P\.need\(!Object\.hasOwn\(payload, 'until'\), 'LOCATION_NO_FOREIGN_ABSOLUTE_CLOCK'\)/)
  assert.ok(entry.includes("['descriptor', 'descriptor-body'].includes(message.command)"))
  return { actual_framing: true, common_active_handler_cap: 2, common_request_and_reply_caps: true,
    ipc_exact_command_and_frame_caps: true, executable_entry_review: 'SOURCE_BRANCH_ASSERTIONS_ONLY_NOT_IMPORTED' }
})

const raw = Buffer.from(JSON.stringify(output, null, 2) + '\n')
assert.ok(raw.length <= 65536)
writeFileSync(options['--output'], raw, { flag: 'wx' })
process.stdout.write(JSON.stringify({ status: output.status, groups: Object.keys(output.groups).length,
  mathematical_acceptance: false }) + '\n')
if (output.status !== 'PASS') process.exitCode = 1
