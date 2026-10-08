/** Maintained advisory provider location only. Root owns process supervision. */
import { mkdir, lstat, readFile, writeFile } from 'node:fs/promises'
import { isAbsolute, resolve, dirname, join } from 'node:path'
import { createHash } from 'node:crypto'
import { canonical, parse, fields, hexid, need, uint, peerId, routeSpec, routeKey,
  validateRequest, makeDescriptor, OwnerEgressPolicy, ASSURANCE } from './protocol.mjs'
import { prepare, Reader, sendBody } from './framing.mjs'
import { intentStoreClass } from './intent.mjs'
import { TransportBudget, transportLimits, boundedTCP } from './transport.mjs'

export const DHT_PROTOCOL = '/dmkn/v5/location-kad/1.0.0'
export const DESCRIPTOR_PROTOCOL = '/dmkn/v5/index-descriptor/1.0.0'
const sha = raw => createHash('sha256').update(raw).digest('hex')
const errorText = error => `${error.name}: ${error.message}`.slice(0, 500)

async function ordinary (path, { fresh = false, directory = false } = {}) {
  need(typeof path === 'string' && isAbsolute(path) && resolve(path) === path && dirname(path) !== path, 'LOCATION_STATE_PATH')
  let check = fresh ? dirname(path) : path
  while (true) { need(!(await lstat(check)).isSymbolicLink(), 'LOCATION_STATE_NO_LINKS'); const parent = dirname(check); if (parent === check) break; check = parent }
  if (fresh) { try { await lstat(path); throw new Error('LOCATION_FRESH_STATE') } catch (error) { if (error.code !== 'ENOENT') throw error } }
  else need(directory ? (await lstat(path)).isDirectory() : (await lstat(path)).isFile(), 'LOCATION_STATE_KIND')
}
async function boundedRead (path, maximum) {
  await ordinary(path); need((await lstat(path)).size <= maximum, 'LOCATION_LOCAL_FILE_BOUND')
  const raw = await readFile(path); need(raw.length > 0 && raw.length <= maximum, 'LOCATION_LOCAL_FILE_BOUND'); return raw
}

export function validateConfig (input) {
  const cfg = structuredClone(input)
  fields(cfg, ['schema', 'role', 'state', 'namespace', 'egress', 'listen', 'announce', 'bootstrap', 'endpoints', 'limits'])
  need(cfg.schema === 'DMKN_V5_MAINTAINED_LOCATION_ROLES_V1' && ['reader', 'index-provider'].includes(cfg.role), 'LOCATION_CONFIG_SCHEMA_ROLE'); hexid(cfg.namespace)
  const policy = new OwnerEgressPolicy(cfg.egress)
  need(Array.isArray(cfg.listen) && cfg.listen.length === 1 && Array.isArray(cfg.announce) && cfg.announce.length <= 4 &&
    Array.isArray(cfg.bootstrap) && cfg.bootstrap.length <= 16 && Array.isArray(cfg.endpoints) && cfg.endpoints.length <= 4, 'LOCATION_CONFIG_ENTRIES')
  need(cfg.role === 'reader' ? cfg.endpoints.length === 0 : cfg.endpoints.length >= 1, 'LOCATION_ROLE_ENDPOINTS')
  cfg.listen.forEach(value => policy.listenAddress(value))
  cfg.announce.forEach(value => policy.peerAddress(value))
  cfg.bootstrap.forEach(value => { policy.peerAddress(value); need(value.includes('/p2p/'), 'LOCATION_BOOTSTRAP_PEER_ID') })
  cfg.endpoints.forEach(value => policy.endpoint(value))
  need(new Set(cfg.endpoints.map(value => canonical(value).toString('hex'))).size === cfg.endpoints.length, 'LOCATION_DUPLICATE_ENDPOINT')
  if (cfg.egress.mode === 'public-ipv4') need(cfg.announce.length > 0, 'LOCATION_PUBLIC_ANNOUNCE')
  const l = cfg.limits
  fields(l, ['service_ms', 'operation_ms', 'query_events', 'provider_limit', 'advertised_keys', 'provider_ttl_ms',
    'reprovide_interval_ms', 'maintenance_ms', 'commands', 'descriptor_requests', 'descriptor_reply_bytes', 'metadata', 'transport'])
  uint(l.service_ms, 1000, 3600000, 'LOCATION_SERVICE_TIME'); uint(l.operation_ms, 1, 60000, 'LOCATION_OPERATION_TIME')
  need(l.operation_ms <= l.service_ms, 'LOCATION_OPERATION_WITHIN_LIFETIME')
  uint(l.query_events, 1, 4096, 'LOCATION_QUERY_EVENTS'); uint(l.provider_limit, 1, 64, 'LOCATION_PROVIDER_LIMIT')
  uint(l.advertised_keys, 1, 4096, 'LOCATION_ADVERTISED_KEYS'); uint(l.provider_ttl_ms, 3000, 172800000, 'LOCATION_PROVIDER_TTL')
  uint(l.reprovide_interval_ms, 500, 3600000, 'LOCATION_REPROVIDE_INTERVAL')
  need(l.reprovide_interval_ms * 3 <= l.provider_ttl_ms, 'LOCATION_RENEWAL_MARGIN')
  uint(l.maintenance_ms, 1000, 3600000, 'LOCATION_MAINTENANCE_INTERVAL')
  uint(l.commands, 1, 8192, 'LOCATION_COMMANDS'); uint(l.descriptor_requests, 1, 8192, 'LOCATION_DESCRIPTOR_REQUESTS')
  uint(l.descriptor_reply_bytes, 4096, 1024 ** 3, 'LOCATION_SERVICE_REPLY_BYTES')
  transportLimits(l.transport)
  need(l.metadata != null && typeof l.metadata === 'object' && !Array.isArray(l.metadata), 'LOCATION_METADATA_LIMITS')
  return { cfg, policy, configHash: sha(canonical(cfg)) }
}

export class MaintainedLocator {
  constructor (adoptedRuntime, ownerConfig) {
    this.runtime = adoptedRuntime
    const { cfg, policy, configHash } = validateConfig(ownerConfig)
    this.cfg = cfg; this.policy = policy; this.configHash = configHash
    this.node = null; this.store = null; this.controller = new AbortController(); this.timer = null
    this.started = false; this.stopped = false; this.busy = false; this.serving = 0
    this.startPromise = null; this.stopPromise = null
    this.transportBudget = new TransportBudget(cfg.limits.transport, this.controller.signal, error => {
      this.stats.last_error = errorText(error); this.controller.abort(error)
      queueMicrotask(() => this.stop().catch(failure => { this.stats.last_error = errorText(failure) }))
    })
    this.until = null; this.known = new Map(); this.stats = { commands: 0, query_events: 0, admitted_query_events: 0,
      refused_query_events: 0, returned_provider_slots: 0,
      descriptor_requests: 0, descriptor_reply_bytes: 0, reserved_descriptor_reply_bytes: 0,
      descriptor_request_bytes: 0, descriptor_failures: 0, last_error: null }
  }
  _signal (duration = this.cfg.limits.operation_ms) {
    uint(duration, 1, 60000, 'LOCATION_TICKET_DURATION')
    need(!this.stopped && this.until != null && performance.now() < this.until, 'LOCATION_SERVICE_EXPIRED')
    return AbortSignal.any([this.controller.signal, AbortSignal.timeout(Math.max(1,
      Math.min(duration, this.cfg.limits.operation_ms, Math.floor(this.until - performance.now()))))])
  }
  _cid (key) { hexid(key); return this.runtime.cid.CID.createV1(0x55, this.runtime.digest.create(0x12, Buffer.from(key, 'hex'))) }
  _events (signal, cap) {
    let used = 0; const controller = new AbortController()
    const combined = AbortSignal.any([signal, controller.signal])
    return { signal: combined, onProgress: event => {
      // The allowance counts adopted DHT query events, not opaque nested
      // transport progress. TCP emits open-connection between its signal check
      // and net.connect; an already-aborted operation must not pass that seam.
      if (event?.type === 'tcp:open-connection') { combined.throwIfAborted(); return }
      if (!event?.type?.startsWith('kad-dht:query:')) return
      this.stats.query_events++
      if (!combined.aborted && used < cap) { used++; this.stats.admitted_query_events++; return }
      this.stats.refused_query_events++
      if (!combined.aborted) controller.abort(new Error('LOCATION_QUERY_EVENT_CAP'))
      // The selected library emits these two hooks immediately before dispatch.
      // Throw there to prevent dispatch even if a lower layer delays reading its
      // signal. Terminal/error hooks must not throw inside Queue event listeners.
      if (event?.type === 'kad-dht:query:dial-peer' || event?.type === 'kad-dht:query:send-query') combined.throwIfAborted()
    } }
  }
  async start ({ create = false } = {}) {
    need(!this.started && !this.stopped, 'LOCATION_ALREADY_STARTED'); this.started = true
    this.until = performance.now() + this.cfg.limits.service_ms
    this.timer = setTimeout(() => { this.stop().catch(error => { this.stats.last_error = errorText(error) }) }, this.cfg.limits.service_ms)
    this.timer.unref()
    this.startPromise = this._startCore(create)
    try { return await this.startPromise } catch (error) { await this.stop(); throw error }
  }
  async _startCore (create) {
      const r = this.runtime; const cfg = this.cfg
      await ordinary(cfg.state, { fresh: create, directory: true })
      if (create) await mkdir(cfg.state)
      const keyPath = join(cfg.state, 'identity.key'); const adoptionPath = join(cfg.state, 'adopted.json')
      let privateKey
      if (create) {
        privateKey = await r.keys.generateKeyPair('Ed25519')
        await writeFile(keyPath, r.keys.privateKeyToProtobuf(privateKey), { flag: 'wx', mode: 0o600 })
        await writeFile(adoptionPath, canonical({ schema: 'DMKN_V5_LOCATION_STATE_V1', config_sha256: this.configHash }), { flag: 'wx' })
      } else {
        const adopted = parse(await boundedRead(adoptionPath, 1024), 1024)
        fields(adopted, ['schema', 'config_sha256'])
        need(adopted.schema === 'DMKN_V5_LOCATION_STATE_V1' && adopted.config_sha256 === this.configHash, 'LOCATION_STATE_CONFIG_CHANGED')
        privateKey = r.keys.privateKeyFromProtobuf(await boundedRead(keyPath, 1024))
      }
      const owner = r.peers.peerIdFromPrivateKey(privateKey); peerId(owner.toString())
      this.controller.signal.throwIfAborted()
      const Store = intentStoreClass(r.quota.QuotaDatastore, r.datastore.Key, r.dhtUtils.toProviderKey)
      this.store = new Store(join(cfg.state, 'metadata.sqlite'), cfg.limits.metadata, owner); await this.store.open()
      const allows = (address, inbound = false, target = null) => {
        try { inbound ? this.policy.inboundAddress(address.toString()) : this.policy.peerAddress(address.toString(), target); return true } catch { return false }
      }
      const mapPeer = peer => ({ ...peer, multiaddrs: peer.multiaddrs.filter(value => allows(value, false, peer.id.toString())).slice(0, 4) })
      this.node = await r.libp2p.createLibp2p({ start: false, privateKey, datastore: this.store,
        addresses: { listen: cfg.listen, announce: cfg.announce },
        transports: [boundedTCP(r.tcp.tcp, this.transportBudget, { maxConnections: 64,
          inboundSocketInactivityTimeout: 5000, outboundSocketInactivityTimeout: 5000 })],
        connectionEncrypters: [r.noise.noise()], streamMuxers: [r.yamux.yamux({ maxInboundStreams: 16,
          maxOutboundStreams: 16, maxEarlyStreams: 4, maxMessageSize: 65536,
          streamOptions: { maxReadBufferLength: 262144, maxWriteBufferLength: 262144, inactivityTimeout: 15000,
            initialStreamWindowSize: 262144, maxStreamWindowSize: 262144 } })],
        connectionGater: { denyDialMultiaddr: value => !allows(value), denyInboundConnection: conn => !allows(conn.remoteAddr, true) },
        connectionManager: { maxConnections: 64, maxParallelDials: 8, maxDialQueueLength: 64, maxPeerAddrsToDial: 4,
          dialTimeout: 5000, addressDialTimeout: 3000, maxIncomingPendingConnections: 16, inboundUpgradeTimeout: 5000,
          outboundStreamProtocolNegotiationTimeout: 5000, inboundStreamProtocolNegotiationTimeout: 5000, connectionCloseTimeout: 2000 },
        services: { identify: r.identify.identify(), dht: r.dht.kadDHT({ protocol: DHT_PROTOCOL,
          datastorePrefix: '/dmknv5', clientMode: false, peerInfoMapper: mapPeer,
          prefixLength: 256, kBucketSize: 20, alpha: 3, disjointPaths: 3, allowQueryWithZeroPeers: true,
          maxInboundStreams: 4, maxOutboundStreams: 8, routingTableUpdateQueueConcurrency: 4, routingTableUpdateMaxQueueSize: 64,
          pingNewContactConcurrency: 4, pingNewContactMaxQueueSize: 32, pingOldContactConcurrency: 4, pingOldContactMaxQueueSize: 32,
          onPeerConnectTimeout: 5000, incomingMessageTimeout: 5000, querySelfInterval: cfg.limits.maintenance_ms,
          initialQuerySelfInterval: 1000, providers: { provideValidity: cfg.limits.provider_ttl_ms / 1000 },
          reprovide: { concurrency: 2, maxQueueSize: 32, validity: cfg.limits.provider_ttl_ms,
            threshold: Math.floor(cfg.limits.provider_ttl_ms / 2), interval: cfg.limits.reprovide_interval_ms,
            timeout: { minTimeout: Math.min(5000, cfg.limits.operation_ms), maxTimeout: cfg.limits.operation_ms } }
        }) }
      })
      this.controller.signal.throwIfAborted()
      if (cfg.role === 'index-provider') {
        await this.node.handle(DESCRIPTOR_PROTOCOL, (stream, connection) => this._serve(stream, connection), { maxInboundStreams: 2, maxOutboundStreams: 2 })
      }
      this.controller.signal.throwIfAborted()
      await this.node.start()
      this.controller.signal.throwIfAborted()
      const joins = []
      for (const address of cfg.bootstrap) {
        try { this.policy.peerAddress(address); await this.node.dial(r.addresses.multiaddr(address), { signal: this._signal() }); joins.push({ address, status: 'CONNECTED' }) }
        catch (error) { joins.push({ address, status: 'UNAVAILABLE', error: errorText(error) }) }
      }
      this.controller.signal.throwIfAborted()
      return { ...this.status(), joins }
  }
  async _command (callback, duration = this.cfg.limits.operation_ms) {
    need(this.node != null && !this.busy && !this.stopped && this.stats.commands < this.cfg.limits.commands, 'LOCATION_COMMAND_CAP_OR_BUSY')
    this.stats.commands++; this.busy = true
    try { return await callback(this._signal(duration)) } finally { this.busy = false }
  }
  async publish (selected, stripe = 0) {
    need(this.cfg.role === 'index-provider', 'LOCATION_READER_CANNOT_PUBLISH')
    return await this._command(async signal => {
      const key = routeKey(this.cfg.namespace, selected, stripe); const cid = this._cid(key)
      let count = 0
      for await (const unused of this.store.queryKeys({ prefix: '/application/published/' }, { signal })) count++
      const published = new this.runtime.datastore.Key('/application/published/' + key)
      need(await this.store.has(published, { signal }) || count < this.cfg.limits.advertised_keys, 'LOCATION_ADVERTISEMENT_CAP')
      await this.store.enableIntent(cid, key, routeSpec(this.cfg.namespace, selected, stripe), { signal })
      let status = 'ADVERTISED_HINT'; let error = null
      const options = this._events(signal, this.cfg.limits.query_events)
      try { for await (const unused of this.node.services.dht.provide(cid, options)) options.signal.throwIfAborted(); options.signal.throwIfAborted() }
      catch (failure) { status = 'INCOMPLETE'; error = errorText(failure) }
      return { route_key: key, status, error, assurance: ASSURANCE, global_complete: false, mathematical_acceptance: false }
    })
  }
  async withdraw (selected, stripe = 0) {
    need(this.cfg.role === 'index-provider', 'LOCATION_READER_CANNOT_WITHDRAW')
    return await this._command(async signal => {
      const key = routeKey(this.cfg.namespace, selected, stripe)
      await this.store.revokeIntent(this._cid(key), key, { signal })
      return { route_key: key, status: 'LOCAL_RENEWAL_STOPPED_REMOTE_HINTS_EXPIRE', assurance: ASSURANCE, global_complete: false, mathematical_acceptance: false }
    })
  }
  async locate (ticket) {
    fields(ticket, ['ticket', 'operation', 'route_key', 'spec', 'event_cap', 'peer_cap', 'remaining_wall_ms'])
    uint(ticket.ticket, 1, Number.MAX_SAFE_INTEGER, 'LOCATION_TICKET'); need(ticket.operation === 'route', 'LOCATION_OPERATION')
    fields(ticket.spec, ['namespace', 'role', 'predicate', 'stripe']); fields(ticket.spec.predicate, ['all'])
    need(canonical(ticket.spec).equals(canonical(routeSpec(this.cfg.namespace, ticket.spec.predicate.all, ticket.spec.stripe))) &&
      routeKey(this.cfg.namespace, ticket.spec.predicate.all, ticket.spec.stripe) === ticket.route_key, 'LOCATION_ROUTE_BINDING')
    uint(ticket.event_cap, 1, this.cfg.limits.query_events, 'LOCATION_TICKET_EVENT_CAP')
    uint(ticket.peer_cap, 1, this.cfg.limits.provider_limit, 'LOCATION_TICKET_PROVIDER_CAP')
    return await this._command(async signal => {
      const found = new Map(); let termination = 'ROUTING_EXHAUSTED_NOT_GLOBAL_COMPLETE'
      const options = this._events(signal, ticket.event_cap)
      try {
        outer: for await (const event of this.node.services.dht.findProviders(this._cid(ticket.route_key), options)) {
          options.signal.throwIfAborted()
          if (event.name !== 'PROVIDER') continue
          for (const info of event.providers) {
            const id = peerId(info.id.toString()); if (id === this.node.peerId.toString()) continue
            const addresses = info.multiaddrs.map(value => value.toString()).filter(value => { try { this.policy.peerAddress(value, id); return true } catch { return false } }).slice(0, 4)
            if (addresses.length === 0) continue
            found.set(id, addresses)
            if (found.size >= ticket.peer_cap) { termination = 'PROVIDER_BUDGET'; break outer }
          }
        }
        options.signal.throwIfAborted()
      } catch (error) { termination = errorText(error) }
      // Finite process-local result cache, not an unbounded global contact map.
      need(new Set([...this.known.keys(), ...found.keys()]).size <= 256, 'LOCATION_KNOWN_PEER_CAP')
      for (const [id, addresses] of found) this.known.set(id, addresses)
      this.stats.returned_provider_slots += found.size
      return { ticket: ticket.ticket, route_key: ticket.route_key, peers: [...found.keys()], termination,
        assurance: ASSURANCE, global_complete: false, mathematical_acceptance: false }
    }, Math.min(uint(ticket.remaining_wall_ms, 1, 3600000, 'LOCATION_TICKET_DURATION'), this.cfg.limits.operation_ms))
  }
  async descriptor (ticket) {
    fields(ticket, ['ticket', 'operation', 'peer', 'request', 'max_reply_bytes', 'until', 'remaining_wall_ms'])
    uint(ticket.ticket, 1, Number.MAX_SAFE_INTEGER, 'LOCATION_TICKET'); need(ticket.operation === 'descriptor', 'LOCATION_OPERATION')
    peerId(ticket.peer); validateRequest(ticket.request)
    need(ticket.request.namespace === this.cfg.namespace && ticket.request.max_bytes === ticket.max_reply_bytes && this.known.has(ticket.peer), 'LOCATION_DESCRIPTOR_TICKET')
    return await this._command(async signal => {
      const r = this.runtime; const id = r.peers.peerIdFromString(ticket.peer)
      const addresses = this.known.get(ticket.peer).map(value => r.addresses.multiaddr(this.policy.peerAddress(value, ticket.peer)))
      await this.node.peerStore.merge(id, { multiaddrs: addresses })
      let stream; let detach = () => {}
      try {
        // dialProtocol's target identity is Noise-authenticated by libp2p. The
        // returned channel identity is this exact dial target, never reply JSON.
        stream = await this.node.dialProtocol(id, DESCRIPTOR_PROTOCOL, { signal, maxReadBufferLength: 16384, maxWriteBufferLength: 16384 })
        detach = prepare(stream, signal)
        const raw = canonical(ticket.request); need(raw.length <= 2048, 'LOCATION_REQUEST_BYTES')
        await sendBody(stream, raw, signal, 2048); await stream.close({ signal })
        const reader = new Reader(stream, signal, ticket.max_reply_bytes)
        const body = await reader.body(); await reader.eof()
        return { ticket: ticket.ticket, authenticated_peer: ticket.peer, raw_base64: body.toString('base64'),
          request_body_bytes: raw.length, reply_body_bytes: body.length, framed_reply_bytes: reader.received,
          assurance: ASSURANCE, mathematical_acceptance: false }
      } catch (error) { stream?.abort(error); throw error } finally { detach() }
    }, Math.min(uint(ticket.remaining_wall_ms, 1, 3600000, 'LOCATION_TICKET_DURATION'), this.cfg.limits.operation_ms))
  }
  async _serve (stream, connection) {
    if (this.cfg.role !== 'index-provider') { stream.abort(new Error('LOCATION_READER_CANNOT_SERVE')); return }
    const l = this.cfg.limits
    if (this.stopped || this.serving >= 2 || this.stats.descriptor_requests >= l.descriptor_requests ||
      this.stats.descriptor_reply_bytes + this.stats.reserved_descriptor_reply_bytes + 4096 > l.descriptor_reply_bytes) {
      stream.abort(new Error('LOCATION_DESCRIPTOR_SERVICE_CAP')); return
    }
    this.serving++; this.stats.descriptor_requests++; this.stats.reserved_descriptor_reply_bytes += 4096
    let detach = () => {}; let charged = 4096; let reader = null
    try {
      this.policy.inboundAddress(connection.remoteAddr.toString()); peerId(connection.remotePeer.toString())
      const signal = this._signal(); detach = prepare(stream, signal)
      reader = new Reader(stream, signal, 2048)
      const raw = await reader.body(); await reader.eof()
      const request = validateRequest(parse(raw, 2048))
      need(request.namespace === this.cfg.namespace, 'LOCATION_NAMESPACE_NOT_SERVED')
      // A live local intent is necessary, but only an advisory serving claim.
      need(await this.store.has(new this.runtime.datastore.Key('/application/published/' + request.route_key), { signal }), 'LOCATION_ROUTE_NOT_ADVERTISED')
      const reply = makeDescriptor(request, this.node.peerId.toString(), this.cfg.endpoints, this.policy)
      charged = reply.length
      await sendBody(stream, reply, signal, request.max_bytes); await stream.close({ signal })
    } catch (error) { this.stats.descriptor_failures++; this.stats.last_error = errorText(error); stream.abort(error) }
    finally {
      detach(); this.stats.descriptor_request_bytes += reader?.received ?? 0
      this.stats.reserved_descriptor_reply_bytes -= 4096; this.stats.descriptor_reply_bytes += charged; this.serving--
    }
  }
  status () {
    return { status: this.stopped ? 'STOPPED' : this.node == null ? 'NOT_STARTED' : 'RUNNING', namespace: this.cfg.namespace, role: this.cfg.role,
      peer_id: this.node?.peerId.toString() ?? null, addresses: this.node?.getMultiaddrs().map(value => value.toString()) ?? [],
      metadata: this.store?.report() ?? null, known_peers: this.known.size, serving: this.serving, stats: { ...this.stats },
      transport: this.transportBudget.report(), dht_wire_bytes: null,
      dht_byte_assurance: 'SUBSET_OF_AGGREGATE_RAW_STREAM_ADMISSIONS_NOT_SEPARATELY_MEASURED',
      descriptor_request_byte_scope: 'OBSERVED_FRAME_BYTES_READ_BY_HANDLER_PRE_READER_TRAFFIC_UNMEASURED',
      background_work_assurance: 'FINITE_SERVICE_LIFETIME_NOT_PER_QUERY_MEASUREMENT',
      assurance: ASSURANCE, global_complete: false, mathematical_acceptance: false }
  }
  async stop () {
    if (this.stopPromise != null) return await this.stopPromise
    this.stopped = true; clearTimeout(this.timer); this.controller.abort(new Error('LOCATION_STOPPED'))
    this.stopPromise = (async () => {
      // Wait for cancellation-aware startup before closing dynamically created
      // node/store resources. Every caller awaits this same cleanup operation.
      if (this.startPromise != null) await this.startPromise.catch(() => {})
      if (this.node != null) await this.node.stop()
      const until = performance.now() + 5000
      while (this.serving > 0 || this.busy) { need(performance.now() < until, 'LOCATION_STOP_DRAIN_TIMEOUT'); await new Promise(resolvePromise => setTimeout(resolvePromise, 10)) }
      if (this.store != null) { await this.store.close(); this.store = null }
    })()
    return await this.stopPromise
  }
}
