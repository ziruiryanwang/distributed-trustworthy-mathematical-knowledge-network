/** Continuation after frozen01 fixture failure: remaining six groups only. */
import assert from 'node:assert/strict'
import { mkdir, lstat } from 'node:fs/promises'
import { isAbsolute, resolve, join } from 'node:path'
import { createHash } from 'node:crypto'
import { EventEmitter } from 'node:events'
import net from 'node:net'
import * as P from './protocol.mjs'
import { prepare, Reader, sendBody } from './framing.mjs'
import { intentStoreClass, PROVIDER_PREFIX } from './intent.mjs'
import { MaintainedLocator } from './maintained.mjs'
import { loadRuntime } from './runtime.mjs'
import { TransportBudget, boundedTCP } from './transport.mjs'

const args = process.argv.slice(2)
assert.equal(args.length, 4); assert.equal(args[0], '--runtime-root'); assert.equal(args[2], '--state')
const root = args[1]; const state = args[3]
assert.ok(isAbsolute(state) && resolve(state) === state)
assert.ok(state.startsWith('E:\\Distributed Trustworthy Mathematical Knowledge Network\\experiments\\v5-local-checks\\'))
await assert.rejects(lstat(state), { code: 'ENOENT' }); await mkdir(state)
const r = await loadRuntime(root)
const NS = 'a'.repeat(64); const FEATURES = ['1'.repeat(64), '2'.repeat(64)]
const EP = { host: '127.0.0.1', port: 8765, tls: false, server_name: null }
const owner = r.peers.peerIdFromPrivateKey(await r.keys.generateKeyPair('Ed25519'))
const peer = owner.toString()
const policyConfig = { schema: 'DMKN_V5_OWNER_EGRESS_V1', mode: 'loopback-test', public_ports: [], test_endpoints: [{ host: EP.host, port: EP.port }] }
const policy = new P.OwnerEgressPolicy(policyConfig)
const request = P.descriptorRequest(NS, FEATURES, 0, 'b'.repeat(64), 4096)
const frame = raw => { const prefix = Buffer.alloc(4); prefix.writeUInt32BE(raw.length); return Buffer.concat([prefix, raw]) }
const goodBody = P.makeDescriptor(request, peer, [EP], policy)
const config = statePath => ({ schema: 'DMKN_V5_MAINTAINED_LOCATION_V1', state: statePath, namespace: NS,
  egress: policyConfig, listen: ['/ip4/127.0.0.1/tcp/8765'], announce: [], bootstrap: [], endpoints: [EP],
  limits: { service_ms: 10000, operation_ms: 1000, query_events: 8, provider_limit: 2, advertised_keys: 2,
    provider_ttl_ms: 3000, reprovide_interval_ms: 500, maintenance_ms: 1000, commands: 8,
    descriptor_requests: 4, descriptor_reply_bytes: 16384, metadata: {},
    transport: { outbound_attempts: 4, inbound_upgrades: 4, receive_bytes: 65536, send_bytes: 65536 } } })
const results = []; let ordinal = 0
async function test (name, run) {
  ordinal++
  if (ordinal <= 7) { console.log(JSON.stringify({ test: name, status: 'SKIPPED_ALREADY_PASSED_FROZEN_LOCATION_NODE_CONTROLS01' })); return }
  await run(); results.push(name); console.log(JSON.stringify({ test: name, status: 'PASS' }))
}
function memory (chunks) {
  return { output: [], aborted: null, closed: false,
    async *[Symbol.asyncIterator] () { for (const chunk of chunks) yield chunk },
    send (chunk) { this.output.push(Buffer.from(chunk)); return true },
    async onDrain () {}, async close () { this.closed = true }, abort (error) { this.aborted = error } }
}
function locator (cfg = config(join(state, 'unused'))) {
  const value = new MaintainedLocator(r, cfg); value.until = performance.now() + 10000
  value.node = { peerId: owner, getMultiaddrs: () => [] }; return value
}

await test('exact route domain and strict canonical descriptor request', async () => {
  const model = { namespace: NS, predicate: { all: FEATURES }, role: 'formal-index-v1', stripe: 3 }
  const expected = createHash('sha256').update('DMKN-V5-INDEX-RENDEZVOUS-V1\0').update(JSON.stringify(model)).digest('hex')
  assert.equal(P.routeKey(NS, FEATURES, 3), expected)
  assert.equal(new Set([expected, P.routeKey(NS, FEATURES, 4), P.routeKey(NS, FEATURES.slice(0, 1), 3), P.routeKey('c'.repeat(64), FEATURES, 3)]).size, 4)
  assert.deepEqual(P.validateRequest(P.parse(P.canonical(request), 2048)), request)
  for (const changed of [{ ...request, nonce: 'bad' }, { ...request, role: 'custody' }, { ...request, max_bytes: true }, { ...request, extra: 1 }]) assert.throws(() => P.validateRequest(changed))
  assert.throws(() => P.routeKey(NS, [...FEATURES].reverse(), 0))
  assert.throws(() => P.parse(Buffer.from('{"a":1,"a":1}'), 1024))
  assert.throws(() => P.parse(Buffer.from('{"b":1,"a":1}'), 1024))
})
await test('selected Ed25519 identity and descriptor assurance fields', async () => {
  assert.equal(P.peerId(peer), peer)
  for (const bad of ['0'.repeat(52), '1'.repeat(52), peer + '1', peer.slice(1)]) assert.throws(() => P.peerId(bad))
  const reply = P.parse(goodBody, 4096)
  assert.equal(reply.peer_id, peer); assert.equal(reply.route_key, request.route_key); assert.equal(reply.nonce, request.nonce)
  assert.equal(reply.global_complete, false); assert.equal(reply.mathematical_acceptance, false)
  assert.throws(() => P.makeDescriptor(request, peer, [EP, EP], policy))
  assert.throws(() => P.makeDescriptor(request, peer, [{ ...EP, ca_file: '/tmp/root.pem' }], policy))
})
await test('every public IPv4 interval boundary and exception matches selected profile', async () => {
  const denied = ['0.0.0.0', '0.255.255.255', '10.0.0.0', '10.255.255.255', '100.64.0.0', '100.127.255.255',
    '127.0.0.0', '127.255.255.255', '169.254.0.0', '169.254.255.255', '172.16.0.0', '172.31.255.255',
    '192.0.0.0', '192.0.0.8', '192.0.0.11', '192.0.0.255', '192.0.2.0', '192.0.2.255',
    '192.168.0.0', '192.168.255.255', '198.18.0.0', '198.19.255.255', '198.51.100.0', '198.51.100.255',
    '203.0.113.0', '203.0.113.255', '224.0.0.0', '239.255.255.255', '240.0.0.0', '255.255.255.255']
  const allowed = ['1.0.0.0', '9.255.255.255', '11.0.0.0', '100.63.255.255', '100.128.0.0',
    '126.255.255.255', '128.0.0.0', '169.253.255.255', '169.255.0.0', '172.15.255.255', '172.32.0.0',
    '191.255.255.255', '192.0.0.9', '192.0.0.10', '192.0.1.0', '192.0.1.255', '192.0.3.0',
    '192.167.255.255', '192.169.0.0', '198.17.255.255', '198.20.0.0', '198.51.99.255', '198.51.101.0',
    '203.0.112.255', '203.0.114.0', '223.255.255.255']
  for (const value of denied) assert.equal(P.publicIPv4(value), false, value)
  for (const value of allowed) assert.equal(P.publicIPv4(value), true, value)
  for (const value of ['01.0.0.1', '127.1', '1.2.3.256', 'localhost', '::1']) assert.throws(() => P.publicIPv4(value))
})
await test('outbound destination policy differs from inbound ephemeral source policy', async () => {
  const publicPolicy = new P.OwnerEgressPolicy({ schema: 'DMKN_V5_OWNER_EGRESS_V1', mode: 'public-ipv4', public_ports: [443], test_endpoints: [] })
  assert.equal(publicPolicy.peerAddress('/ip4/8.8.8.8/tcp/443'), '/ip4/8.8.8.8/tcp/443')
  assert.throws(() => publicPolicy.peerAddress('/ip4/8.8.8.8/tcp/49152'))
  assert.equal(publicPolicy.inboundAddress('/ip4/8.8.8.8/tcp/49152'), '/ip4/8.8.8.8/tcp/49152')
  assert.equal(publicPolicy.listenAddress('/ip4/0.0.0.0/tcp/443'), '/ip4/0.0.0.0/tcp/443')
  assert.throws(() => publicPolicy.peerAddress('/ip4/0.0.0.0/tcp/443'))
  assert.throws(() => policy.peerAddress('/ip4/127.0.0.1/tcp/8766'))
  assert.equal(policy.inboundAddress('/ip4/127.0.0.1/tcp/49152'), '/ip4/127.0.0.1/tcp/49152')
  assert.throws(() => publicPolicy.endpoint({ host: '8.8.8.8', port: 443, tls: false, server_name: null }))
  assert.throws(() => publicPolicy.peerAddress('/dns4/example.org/tcp/443'))
  const other = r.peers.peerIdFromPrivateKey(await r.keys.generateKeyPair('Ed25519')).toString()
  assert.throws(() => policy.peerAddress(`/ip4/127.0.0.1/tcp/8765/p2p/${other}`, peer))
})
await test('descriptor framing exact body prefix EOF and cancellation', async () => {
  const signal = new AbortController().signal
  const bytes = frame(goodBody); const stream = memory([bytes.subarray(0, 2), bytes.subarray(2, 7), bytes.subarray(7)])
  const detach = prepare(stream, signal); const reader = new Reader(stream, signal, 4096)
  assert.deepEqual(await reader.body(), goodBody); await reader.eof(); detach()
  assert.equal(reader.received, goodBody.length + 4)
  const output = memory([]); assert.equal(await sendBody(output, goodBody, signal, 4096), goodBody.length + 4)
  assert.deepEqual(Buffer.concat(output.output), bytes)
  for (const bad of [bytes.subarray(0, bytes.length - 1), Buffer.concat([bytes, Buffer.from([1])]), Buffer.from([0, 0, 32, 0])]) {
    const value = new Reader(memory([bad]), signal, 4096)
    await assert.rejects(async () => { await value.body(); await value.eof() })
  }
  const controller = new AbortController(); const aborted = memory([]); const clean = prepare(aborted, controller.signal)
  controller.abort(new Error('control')); assert.equal(aborted.aborted.message, 'control'); clean()
})

const Store = intentStoreClass(r.quota.QuotaDatastore, r.datastore.Key, r.dhtUtils.toProviderKey)
const store = new Store(join(state, 'intent.sqlite'), {}, owner)
await store.open()
const key = P.routeKey(NS, FEATURES, 0)
const cid = r.cid.CID.createV1(0x55, r.digest.create(0x12, Buffer.from(key, 'hex')))
const providerKey = r.dhtUtils.toProviderKey(PROVIDER_PREFIX, cid, owner)
try {
  await test('real SQLite current intent blocks prepublish and queued postwithdraw self hints', async () => {
    await assert.rejects(store.put(providerKey, Uint8Array.of(1)), /LOCAL_PROVIDER_INTENT_REVOKED/)
    await store.enableIntent(cid, key, P.routeSpec(NS, FEATURES), {})
    await store.put(providerKey, Uint8Array.of(1))
    assert.equal(await store.has(providerKey), true)
    await store.revokeIntent(cid, key, {})
    assert.equal(await store.has(providerKey), false)
    assert.equal(await store.has(new r.datastore.Key('/application/published/' + key)), false)
    await assert.rejects(store.put(providerKey, Uint8Array.of(2)), /LOCAL_PROVIDER_INTENT_REVOKED/)
    await assert.rejects(store.enableIntent(cid, 'c'.repeat(64), P.routeSpec(NS, FEATURES), {}))
    await store.enableIntent(cid, key, P.routeSpec(NS, FEATURES), {})
  })
  await test('actual descriptor handler checks intent and charges failed service allowance', async () => {
    const value = locator(); value.store = store
    const connection = { remoteAddr: { toString: () => '/ip4/127.0.0.1/tcp/49152' }, remotePeer: owner }
    const stream = memory([frame(P.canonical(request))]); await value._serve(stream, connection)
    assert.equal(stream.aborted, null); assert.equal(stream.closed, true)
    assert.deepEqual(Buffer.concat(stream.output), frame(goodBody))
    assert.equal(value.stats.reserved_descriptor_reply_bytes, 0); assert.equal(value.serving, 0)
    const before = value.stats.descriptor_reply_bytes
    await store.revokeIntent(cid, key, {})
    const withdrawn = memory([frame(P.canonical(request))]); await value._serve(withdrawn, connection)
    assert.ok(withdrawn.aborted); assert.equal(value.stats.descriptor_reply_bytes - before, 4096)
    assert.equal(value.stats.descriptor_failures, 1); assert.equal(value.stats.reserved_descriptor_reply_bytes, 0)
    const readBefore = value.stats.descriptor_request_bytes
    const truncated = memory([Buffer.from([0, 0])]); await value._serve(truncated, connection)
    assert.ok(truncated.aborted); assert.equal(value.stats.descriptor_request_bytes - readBefore, 2)
    assert.equal(value.stats.descriptor_failures, 2); assert.equal(value.stats.reserved_descriptor_reply_bytes, 0)
  })
  await test('mock routing event budget and returned-provider bound are distinct', async () => {
    const value = locator()
    value.node.services = { dht: { async *findProviders (unused, options) {
      r.dhtEvents.providerEvent({}, options); r.dhtEvents.providerEvent({}, options)
      yield { name: 'PROVIDER', providers: [{ id: owner, multiaddrs: [{ toString: () => '/ip4/127.0.0.1/tcp/8765' }] }] }
    } } }
    const ticket = { ticket: 1, operation: 'route', route_key: key, spec: P.routeSpec(NS, FEATURES), event_cap: 1, peer_cap: 1, remaining_wall_ms: 9000 }
    const result = await value.locate(ticket)
    assert.equal(result.peers.length, 0); assert.match(result.termination, /QUERY_EVENT_CAP/)
    assert.equal(value.stats.commands, 1); assert.equal(value.stats.query_events, 2)
    assert.equal(value.stats.admitted_query_events, 1); assert.equal(value.stats.refused_query_events, 1)
    assert.equal(value.known.size, 0); assert.equal(value.status().dht_wire_bytes, null)
  })
} finally { await store.close() }

await test('startup cancellation joins the same terminal cleanup without a network start', async () => {
  let enteredResolve; let releaseResolve; let starts = 0; let stops = 0
  const entered = new Promise(resolvePromise => { enteredResolve = resolvePromise })
  const release = new Promise(resolvePromise => { releaseResolve = resolvePromise })
  const fakeNode = { async start () { starts++ }, async stop () { stops++ } }
  const mocked = { ...r, libp2p: { async createLibp2p () { enteredResolve(); await release; return fakeNode } } }
  const value = new MaintainedLocator(mocked, config(join(state, 'cancelled-start')))
  const starting = value.start({ create: true }); const rejection = assert.rejects(starting, /LOCATION_STOPPED/)
  await entered
  const first = value.stop(); const second = value.stop(); releaseResolve()
  await Promise.all([first, second, rejection])
  assert.equal(starts, 0); assert.equal(stops, 1); assert.equal(value.store, null); assert.equal(value.stopped, true)
})

const log = Object.assign(() => {}, { trace () {}, error () {}, newScope () { return log } })
const logger = { forComponent () { return log } }
function fakeSocket () {
  const socket = new EventEmitter()
  Object.assign(socket, { remoteAddress: '127.0.0.1', remotePort: 49152, destroyed: false, writableEnded: false,
    sent: [], setTimeout () {}, write (data) { this.sent.push(Buffer.from(data)); return true },
    pause () {}, resume () {}, resetAndDestroy () { this.destroy() },
    destroy () { if (!this.destroyed) { this.destroyed = true; this.emit('close', false) } },
    destroySoon () { this.destroy() } })
  return socket
}
const smallLimits = { outbound_attempts: 2, inbound_upgrades: 2, receive_bytes: 1024, send_bytes: 1024 }
const rawConnection = () => {
  const socket = fakeSocket()
  const conn = r.tcpSocket.toMultiaddrConnection({ socket, direction: 'inbound', log })
  return { socket, conn }
}
await test('actual raw TCP receive callback rejects aggregate overflow before forwarding', async () => {
  let trips = 0
  const budget = new TransportBudget(smallLimits, new AbortController().signal, () => { trips++ })
  const first = rawConnection(); const second = rawConnection()
  budget.attach(first.conn); budget.attach(second.conn)
  let received = 0
  first.conn.addEventListener('message', event => { received += event.data.byteLength })
  second.conn.addEventListener('message', event => { received += event.data.byteLength })
  first.socket.emit('data', Buffer.alloc(700)); second.socket.emit('data', Buffer.alloc(324))
  assert.equal(received, 1024)
  second.socket.emit('data', Buffer.alloc(7))
  assert.equal(received, 1024); assert.equal(trips, 1)
  assert.equal(first.socket.destroyed, true); assert.equal(second.socket.destroyed, true)
  assert.equal(budget.report().receive_observed_bytes, 1031); assert.equal(budget.report().receive_admitted_bytes, 1024)
  assert.equal(budget.report().receive_refused_bytes, 7)
  assert.throws(() => first.conn.send(Buffer.from([1])), /TRANSPORT_RECEIVE_CAP/)
})
await test('actual raw TCP send allowance is charged before write-buffer admission', async () => {
  const budget = new TransportBudget(smallLimits, new AbortController().signal)
  const first = rawConnection(); const second = rawConnection()
  budget.attach(first.conn); budget.attach(second.conn)
  first.conn.send(Buffer.alloc(700)); second.conn.send(Buffer.alloc(324))
  assert.throws(() => second.conn.send(Buffer.alloc(5)), /TRANSPORT_SEND_CAP/)
  assert.equal(first.socket.sent.reduce((n, bytes) => n + bytes.length, 0), 700)
  assert.equal(second.socket.sent.reduce((n, bytes) => n + bytes.length, 0), 324)
  assert.equal(budget.report().send_admitted_bytes, 1024); assert.equal(budget.report().send_refused_bytes, 5)
})
await test('retained TCP failed connects and inbound upgrade refusals consume one service budget', async () => {
  const budget = new TransportBudget(smallLimits, new AbortController().signal)
  const transport = boundedTCP(r.tcp.tcp, budget)({ logger }); let connects = 0
  transport._connect = async () => { connects++; if (connects === 2) throw new Error('selected failed connect'); return fakeSocket() }
  const address = r.addresses.multiaddr('/ip4/127.0.0.1/tcp/8765')
  const options = { signal: new AbortController().signal, upgrader: { async upgradeOutbound (conn) { return conn } } }
  const admitted = await transport.dial(address, options)
  assert.equal(budget.report().attached_connections, 1)
  await assert.rejects(transport.dial(address, options), /selected failed connect/)
  await assert.rejects(transport.dial(address, options), /TRANSPORT_OUTBOUND_CAP/)
  assert.equal(connects, 2); assert.equal(admitted.socket.destroyed, true)
  assert.equal(budget.report().outbound_attempts, 2); assert.equal(budget.report().refused_outbound, 1)
  const incoming = new TransportBudget(smallLimits, new AbortController().signal)
  const inboundTransport = boundedTCP(r.tcp.tcp, incoming)({ logger })
  let upgrades = 0
  const listener = inboundTransport.createListener({ upgrader: { async upgradeInbound (conn) { upgrades++; return conn } } })
  const raw = [rawConnection(), rawConnection(), rawConnection()]
  for (const value of raw.slice(0, 2)) await listener.context.upgrader.upgradeInbound(value.conn, {})
  await assert.rejects(listener.context.upgrader.upgradeInbound(raw[2].conn, {}), /TRANSPORT_INBOUND_CAP/)
  assert.equal(upgrades, 2); assert.equal(incoming.report().inbound_upgrades, 2)
  assert.equal(raw.every(value => value.socket.destroyed), true)
  await listener.close()
})
await test('actual DHT Network hooks abort exhausted queries without throwing terminal callbacks', async () => {
  const value = locator(); let opened = 0; let writes = 0; let aborted = 0
  const network = new r.dhtNetwork.Network({ logger, connectionManager: { async openStream () {
    opened++; return { async close () {}, abort () { aborted++ } }
  } } }, { protocol: '/controlled-no-network', logPrefix: 'control', metricsPrefix: 'control' })
  network._writeReadMessage = async () => { writes++; return { type: 'FIND_NODE', closer: [], providers: [] } }
  await network.start()
  const options = value._events(new AbortController().signal, 1)
  const tcp = r.tcp.tcp()({ logger }); const actualConnect = net.connect; let rawDials = 0
  try {
    net.connect = () => { rawDials++; const socket = fakeSocket(); queueMicrotask(() => socket.emit('connect')); return socket }
    const raw = await tcp._connect(r.addresses.multiaddr('/ip4/127.0.0.1/tcp/8765'), options)
    assert.equal(rawDials, 1); assert.equal(value.stats.query_events, 0); raw.destroy()
  } finally { net.connect = actualConnect }
  for await (const unused of network.sendRequest(owner, { type: 'FIND_NODE' }, options)) {}
  assert.equal(options.signal.aborted, true); assert.equal(opened, 1); assert.equal(writes, 0); assert.equal(aborted, 1)
  assert.doesNotThrow(() => r.dhtEvents.pathEndedEvent({ path: 'control' }, options))
  assert.doesNotThrow(() => r.dhtEvents.queryErrorEvent({ error: new Error('terminal') }, options))
  try {
    net.connect = () => { rawDials++; throw new Error('unexpected real dial boundary') }
    await assert.rejects(tcp._connect(r.addresses.multiaddr('/ip4/127.0.0.1/tcp/8765'), options), /QUERY_EVENT_CAP/)
    assert.equal(rawDials, 1)
    assert.throws(() => options.onProgress({ type: 'tcp:open-connection' }), /QUERY_EVENT_CAP/)
  } finally { net.connect = actualConnect }
  for await (const unused of network.sendRequest(owner, { type: 'FIND_NODE' }, options)) {}
  assert.equal(opened, 1); assert.equal(writes, 0); assert.equal(value.stats.admitted_query_events, 1)
  assert.ok(value.stats.refused_query_events >= 3)
  await network.stop()
})

console.log(JSON.stringify({ status: 'PASS', groups: results.length, tests: results, real_sockets: 0,
  real_dht_queries: 0, real_sqlite_intent: true, actual_tcp_methods_with_fake_sockets: true,
  actual_dht_dispatch_with_mock_rpc: true, executed_cross_language_vectors: false, mathematical_acceptance: false }))
