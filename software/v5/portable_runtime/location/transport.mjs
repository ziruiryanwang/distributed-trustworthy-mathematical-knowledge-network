/** Aggregate raw-TCP admission limits for the exactly selected libp2p runtime.
 * These are stream-boundary counters, not packet/kernel bandwidth accounting.
 */
import { fields, need, uint } from './protocol.mjs'

export function transportLimits (input) {
  fields(input, ['outbound_attempts', 'inbound_upgrades', 'receive_bytes', 'send_bytes'])
  return Object.freeze({
    outbound_attempts: uint(input.outbound_attempts, 1, 8192, 'LOCATION_OUTBOUND_ATTEMPTS'),
    inbound_upgrades: uint(input.inbound_upgrades, 1, 8192, 'LOCATION_INBOUND_UPGRADES'),
    receive_bytes: uint(input.receive_bytes, 1024, 1024 ** 3, 'LOCATION_TRANSPORT_RECEIVE'),
    send_bytes: uint(input.send_bytes, 1024, 1024 ** 3, 'LOCATION_TRANSPORT_SEND')
  })
}

export class TransportBudget {
  constructor (limits, signal, onExhausted = () => {}) {
    this.limits = transportLimits(limits); this.signal = signal; this.onExhausted = onExhausted
    this.failure = null; this.connections = new Set(); this.attached = new WeakSet(); this.listeners = new Set()
    this.stats = { outbound_attempts: 0, inbound_upgrades: 0, refused_outbound: 0, refused_inbound: 0,
      receive_observed_bytes: 0, receive_admitted_bytes: 0, receive_refused_bytes: 0,
      send_admitted_bytes: 0, send_refused_bytes: 0, attached_connections: 0 }
  }
  _live () { if (this.failure != null) throw this.failure; this.signal.throwIfAborted() }
  _trip (message) {
    if (this.failure != null) return this.failure
    this.failure = new Error(message)
    // Abort raw connections synchronously; no further bytes are admitted to
    // Noise/identify/DHT and no later raw send reaches its write queue.
    for (const conn of this.connections) { try { conn.abort(this.failure) } catch {} }
    for (const listener of this.listeners) { try { Promise.resolve(listener.close()).catch(() => {}) } catch {} }
    this.onExhausted(this.failure)
    return this.failure
  }
  outbound () {
    this._live()
    if (this.stats.outbound_attempts >= this.limits.outbound_attempts) {
      this.stats.refused_outbound++; throw this._trip('LOCATION_TRANSPORT_OUTBOUND_CAP')
    }
    this.stats.outbound_attempts++
  }
  inbound () {
    this._live()
    if (this.stats.inbound_upgrades >= this.limits.inbound_upgrades) {
      this.stats.refused_inbound++; throw this._trip('LOCATION_TRANSPORT_INBOUND_CAP')
    }
    this.stats.inbound_upgrades++
  }
  attach (conn) {
    this._live(); need(!this.attached.has(conn), 'LOCATION_TRANSPORT_DOUBLE_ATTACH')
    need(typeof conn.onData === 'function' && typeof conn.send === 'function' && typeof conn.abort === 'function' &&
      typeof conn.addEventListener === 'function' && conn.readBufferLength === 0 && conn.writeBufferLength === 0,
    'LOCATION_TRANSPORT_UNEXPECTED_RAW_INTERFACE')
    // The selected TCP constructor calls this.onData from its socket callback.
    // Its upgrader is entered synchronously before that callback can run. These
    // two narrow instance methods are wrapped; dependency files stay unchanged.
    const read = conn.onData.bind(conn); const send = conn.send.bind(conn)
    conn.onData = data => {
      const count = uint(data.byteLength, 0, Number.MAX_SAFE_INTEGER, 'LOCATION_RAW_CHUNK')
      this.stats.receive_observed_bytes += count
      if (this.failure != null || this.signal.aborted || this.stats.receive_admitted_bytes + count > this.limits.receive_bytes) {
        this.stats.receive_refused_bytes += count
        conn.abort(this._trip('LOCATION_TRANSPORT_RECEIVE_CAP')); return
      }
      this.stats.receive_admitted_bytes += count
      read(data)
    }
    conn.send = data => {
      this._live()
      const count = uint(data.byteLength, 0, Number.MAX_SAFE_INTEGER, 'LOCATION_RAW_CHUNK')
      if (this.stats.send_admitted_bytes + count > this.limits.send_bytes) {
        this.stats.send_refused_bytes += count; throw this._trip('LOCATION_TRANSPORT_SEND_CAP')
      }
      // Conservative charge: a lower-layer failure or unsent queued bytes do
      // not refund this admission or authorize a replacement attempt.
      this.stats.send_admitted_bytes += count
      return send(data)
    }
    this.attached.add(conn); this.connections.add(conn); this.stats.attached_connections++
    conn.addEventListener('close', () => this.connections.delete(conn), { once: true })
    return conn
  }
  report () {
    return { limits: this.limits, ...this.stats, active_connections: this.connections.size,
      exhausted: this.failure?.message ?? null,
      scope: 'RAW_TCP_RECEIVE_FORWARDING_AND_PREBUFFER_SEND_ADMISSIONS_ALL_SERVICE_WORK',
      unbounded_by_this_counter: 'KERNEL_PACKETS_PRE_UPGRADE_ALLOCATION_AND_REFUSED_CHUNKS',
      external_process_memory_cpu_wall_containment_required: true }
  }
}

export function boundedTCP (tcpFactory, budget, options = {}) {
  return components => {
    const transport = tcpFactory(options)(components)
    const dial = transport.dial.bind(transport); const createListener = transport.createListener.bind(transport)
    const wrappedUpgrader = (upgrader, inbound) => {
      const method = inbound ? 'upgradeInbound' : 'upgradeOutbound'
      need(typeof upgrader?.[method] === 'function', 'LOCATION_TRANSPORT_UPGRADER')
      return new Proxy(upgrader, { get (target, property) {
        if (property !== method) return Reflect.get(target, property, target)
        return async (conn, upgradeOptions) => {
          try {
            if (inbound) budget.inbound()
            budget.attach(conn)
            return await target[method](conn, upgradeOptions)
          } catch (error) { conn.abort(error); throw error }
        }
      } })
    }
    transport.dial = async (address, dialOptions) => {
      budget.outbound()
      return await dial(address, { ...dialOptions, upgrader: wrappedUpgrader(dialOptions.upgrader, false) })
    }
    transport.createListener = listenerOptions => {
      budget._live()
      const listener = createListener({ ...listenerOptions, upgrader: wrappedUpgrader(listenerOptions.upgrader, true) })
      budget.listeners.add(listener)
      return listener
    }
    return transport
  }
}
