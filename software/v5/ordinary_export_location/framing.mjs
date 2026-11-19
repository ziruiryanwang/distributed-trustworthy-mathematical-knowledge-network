/** One bounded body per half-closed descriptor stream. Not a DHT frame wrapper. */
import { need, uint } from './protocol.mjs'

export function prepare (stream, signal) {
  stream.maxReadBufferLength = 16384
  stream.maxWriteBufferLength = 16384
  stream.inactivityTimeout = 10000
  const abort = () => stream.abort(signal.reason instanceof Error ? signal.reason : new Error('LOCATION_ABORTED'))
  signal.throwIfAborted(); signal.addEventListener('abort', abort, { once: true })
  return () => signal.removeEventListener('abort', abort)
}

export class Reader {
  constructor (stream, signal, maximum) {
    uint(maximum, 1, 4096, 'LOCATION_BODY_CAP')
    this.iterator = stream[Symbol.asyncIterator](); this.signal = signal; this.maximum = maximum
    this.pending = Buffer.alloc(0); this.received = 0; this.consumed = 0; this.read = false; this.ended = false
  }
  async next () {
    this.signal.throwIfAborted()
    const item = await this.iterator.next()
    this.signal.throwIfAborted()
    if (item.done) return null
    const length = item.value.byteLength
    need(Number.isSafeInteger(length) && length > 0, 'LOCATION_EMPTY_CHUNK')
    this.received += length
    // Charge observed application bytes before refusing a transport overrun.
    need(length <= 8192 && this.received <= this.maximum + 4, 'LOCATION_STREAM_OVERRUN')
    return Buffer.from(item.value instanceof Uint8Array ? item.value : item.value.subarray())
  }
  async take (count) {
    uint(count, 0, this.maximum + 4, 'LOCATION_READ_BOUND')
    const result = Buffer.alloc(count); let used = 0
    while (used < count) {
      this.signal.throwIfAborted()
      if (this.pending.length === 0) { this.pending = await this.next(); need(this.pending != null, 'LOCATION_TRUNCATED_STREAM') }
      const length = Math.min(count - used, this.pending.length)
      this.pending.copy(result, used, 0, length); this.pending = this.pending.subarray(length); used += length; this.consumed += length
    }
    return result
  }
  async body () {
    need(!this.read && !this.ended, 'LOCATION_ONE_BODY'); this.read = true
    const length = (await this.take(4)).readUInt32BE()
    uint(length, 1, this.maximum, 'LOCATION_BODY_LENGTH')
    return await this.take(length)
  }
  async eof () {
    need(this.read && !this.ended && this.pending.length === 0, 'LOCATION_TRAILING_STREAM')
    need(await this.next() === null, 'LOCATION_TRAILING_STREAM'); this.ended = true
  }
}

export async function sendBody (stream, raw, signal, maximum) {
  need(raw instanceof Uint8Array, 'LOCATION_BODY_BYTES')
  uint(raw.byteLength, 1, maximum, 'LOCATION_BODY_LENGTH'); uint(maximum, 1, 4096, 'LOCATION_BODY_CAP')
  const prefix = Buffer.alloc(4); prefix.writeUInt32BE(raw.byteLength)
  for (const piece of [prefix, raw]) {
    signal.throwIfAborted()
    if (!stream.send(piece)) await stream.onDrain({ signal })
  }
  return raw.byteLength + 4 // queued framed application bytes, not TCP measurement
}
