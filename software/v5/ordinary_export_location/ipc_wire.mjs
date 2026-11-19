/** Private owner-created child pipe. Never a remote network protocol. */
import { once } from 'node:events'
import { canonical, parse, need, uint, fields } from './protocol.mjs'

export function commandEnvelope (message, previous, commandCap) {
  uint(commandCap, 1, 8192, 'LOCATION_IPC_COMMAND_CAP')
  fields(message, ['schema', 'sequence', 'command', 'payload', 'remaining_wall_ms'])
  need(message.schema === 'DMKN_V5_ORDINARY_LOCATION_IPC_COMMAND_V1' && message.sequence === previous + 1 &&
    previous < commandCap && ['locate', 'descriptor', 'publish', 'withdraw', 'status', 'stop'].includes(message.command),
  'LOCATION_IPC_COMMAND_BINDING')
  // Report and stop share the owner grant; ordinary work cannot consume them.
  const reserve = message.command === 'stop' ? 0 : message.command === 'status' ? 1 : 2
  need(message.sequence + reserve <= commandCap, 'LOCATION_IPC_FINALIZATION_RESERVE')
  uint(message.remaining_wall_ms, 1, 3600000, 'LOCATION_IPC_DURATION')
  return message
}
export class LocalFrames {
  constructor (readable, writable, limits) {
    this.readable = readable; this.writable = writable
    this.maxFrame = uint(limits.frame_bytes, 16384, 16384, 'LOCATION_IPC_FRAME_CAP')
    this.maxBytes = uint(limits.total_bytes, 3 * (16384 + 4), 129 * 1024 ** 2, 'LOCATION_IPC_BYTE_CAP')
    this.maxFrames = uint(limits.frames, 3, 8194, 'LOCATION_IPC_FRAME_COUNT')
    this.readBytes = 0; this.writeBytes = 0; this.readFrames = 0; this.writeFrames = 0
  }
  async *read () {
    let pending = Buffer.alloc(0)
    for await (const chunk of this.readable) {
      this.readBytes += chunk.length
      need(chunk.length <= 65536 && this.readBytes <= this.maxBytes, 'LOCATION_IPC_READ_BYTES')
      pending = Buffer.concat([pending, chunk])
      need(pending.length <= this.maxFrame + 4 + 65536, 'LOCATION_IPC_PENDING_BYTES')
      while (pending.length >= 4) {
        const size = pending.readUInt32BE(0)
        need(size > 0 && size <= this.maxFrame, 'LOCATION_IPC_BODY_BYTES')
        if (pending.length < size + 4) break
        need(++this.readFrames <= this.maxFrames, 'LOCATION_IPC_READ_FRAMES')
        const raw = pending.subarray(4, size + 4); pending = pending.subarray(size + 4)
        yield parse(raw, this.maxFrame)
      }
    }
    need(pending.length === 0, 'LOCATION_IPC_TRUNCATED_FRAME')
  }
  async write (value, signal) {
    signal.throwIfAborted()
    const raw = canonical(value)
    need(raw.length > 0 && raw.length <= this.maxFrame, 'LOCATION_IPC_BODY_BYTES')
    need(this.writeFrames < this.maxFrames && this.writeBytes + raw.length + 4 <= this.maxBytes, 'LOCATION_IPC_WRITE_CAP')
    this.writeFrames++; this.writeBytes += raw.length + 4
    const prefix = Buffer.alloc(4); prefix.writeUInt32BE(raw.length)
    if (!this.writable.write(Buffer.concat([prefix, raw]))) await once(this.writable, 'drain', { signal })
  }
  report () {
    return { read_bytes: this.readBytes, write_bytes: this.writeBytes,
      read_frames: this.readFrames, write_frames: this.writeFrames,
      authority: 'PRIVATE_LOCAL_CHILD_PIPE_NOT_REMOTE_CHANNEL_PROOF' }
  }
}

