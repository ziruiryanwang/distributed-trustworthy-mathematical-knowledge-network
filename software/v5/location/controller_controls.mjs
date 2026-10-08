/** Exact Python/Node vectors and changed IPC/composition controls, no sockets. */
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { Readable, PassThrough } from 'node:stream'
import * as P from './protocol.mjs'
import { LocalFrames, commandEnvelope } from './ipc_wire.mjs'
import { createLocator } from './composition.mjs'

assert.equal(process.argv.length, 4)
const raw = readFileSync(process.argv[2]); assert.ok(raw.length <= 65536)
assert.equal(createHash('sha256').update(raw).digest('hex'), process.argv[3])
const fixture = P.parse(raw, 65536)
const vectors = []
for (const row of fixture.routes) {
  const request = P.descriptorRequest(row.namespace, row.features, row.stripe, row.nonce, row.max_bytes)
  assert.equal(P.routeKey(row.namespace, row.features, row.stripe), row.key)
  assert.equal(P.canonical(request).toString('base64'), row.request_base64)
  vectors.push(row.key)
}
for (const row of fixture.addresses) assert.equal(P.publicIPv4(row.address), row.public)
const policy = new P.OwnerEgressPolicy(fixture.policy)
const request = P.parse(Buffer.from(fixture.routes[0].request_base64, 'base64'), 2048)
const descriptor = P.makeDescriptor(request, fixture.peer, [fixture.endpoint], policy)

const encode = value => {
  const body = P.canonical(value); const prefix = Buffer.alloc(4); prefix.writeUInt32BE(body.length)
  return Buffer.concat([prefix, body])
}
const message = { schema: 'DMKN_V5_LOCATION_IPC_COMMAND_V1', sequence: 1, command: 'status', payload: {}, remaining_wall_ms: 1000 }
assert.deepEqual(commandEnvelope(message, 0), message)
for (const bad of [{ ...message, sequence: 2 }, { ...message, command: 'eval' }, { ...message, remaining_wall_ms: 0 }, { ...message, extra: 0 }]) assert.throws(() => commandEnvelope(bad, 0))
const limits = { frame_bytes: 1024, total_bytes: 4096, frames: 2 }
const wire = encode(message); const stream = new LocalFrames(Readable.from([wire.subarray(0, 2), wire.subarray(2)]), new PassThrough(), limits)
const replies = []; for await (const value of stream.read()) replies.push(value)
assert.deepEqual(replies, [message]); assert.equal(stream.readBytes, wire.length)
for (const chunks of [[wire.subarray(0, wire.length - 1)], [Buffer.from([0, 1, 0, 0])], [wire, wire, wire]]) {
  const bad = new LocalFrames(Readable.from(chunks), new PassThrough(), limits)
  await assert.rejects(async () => { for await (const unused of bad.read()) {} })
}
const output = new PassThrough(); const written = []
output.on('data', data => written.push(data))
const sender = new LocalFrames(Readable.from([]), output, limits)
await sender.write(message, new AbortController().signal)
assert.deepEqual(Buffer.concat(written), wire); assert.equal(sender.writeBytes, wire.length)
const cancelled = new AbortController(); cancelled.abort(new Error('selected cancellation'))
await assert.rejects(sender.write(message, cancelled.signal), /selected cancellation/)
assert.equal(sender.writeFrames, 1)

let captured = null; let rejected = 0
const fakeRuntime = { tcp: { tcp: () => () => ({ dial (unused, options) {
  captured = options.signal
  return new Promise((resolve, reject) => options.signal.addEventListener('abort', () => { rejected++; reject(options.signal.reason) }, { once: true }))
} }) } }
const locator = createLocator(fakeRuntime, fixture.config)
const transport = locator.runtime.tcp.tcp()({})
const original = new AbortController()
const pending = transport.dial('/unused-no-socket', { signal: original.signal })
const expectation = assert.rejects(pending, /service capacity exhausted/)
locator.controller.abort(new Error('service capacity exhausted'))
await expectation
assert.equal(original.signal.aborted, false); assert.equal(captured.aborted, true); assert.equal(rejected, 1)
assert.throws(() => transport.dial('/unused-no-socket', { signal: original.signal }), /service capacity exhausted/)

console.log(JSON.stringify({ status: 'PASS', route_vectors: vectors, address_vectors: fixture.addresses.length,
  descriptor_base64: descriptor.toString('base64'), ipc_groups: 3, composition_groups: 1,
  actual_network_calls: 0, actual_runtime_dependency_imports: 0,
  mathematical_acceptance: false }))
