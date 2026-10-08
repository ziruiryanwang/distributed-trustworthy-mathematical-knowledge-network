/** Fixed private-pipe entry; invoked only by the adopted local controller. */
import assert from 'node:assert/strict'
import { readFileSync, lstatSync, realpathSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { createHash } from 'node:crypto'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { registerHooks } from 'node:module'

const ROOT = 'E:\\Distributed Trustworthy Mathematical Knowledge Network'
const BASE = join(ROOT, 'product-local', 'v4-library-commons-02', 'commons-v4')
const MANIFEST_SHA = 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
const expectedNames = ['composition.mjs', 'framing.mjs', 'intent.mjs', 'ipc_wire.mjs', 'maintained.mjs',
  'node_entry.mjs', 'protocol.mjs', 'runtime.mjs', 'transport.mjs']
const hash = raw => createHash('sha256').update(raw).digest('hex')
function readBounded (path, maximum) {
  assert.equal(resolve(path), path)
  for (let value = path; ; value = dirname(value)) {
    assert.equal(lstatSync(value).isSymbolicLink(), false)
    if (dirname(value) === value) break
  }
  assert.equal(realpathSync(path), path); assert.equal(lstatSync(path).isFile(), true)
  assert.ok(lstatSync(path).size <= maximum)
  const raw = readFileSync(path); assert.ok(raw.length > 0 && raw.length <= maximum); return raw
}
assert.equal(process.cwd(), ROOT); assert.deepEqual(process.execArgv, [])
assert.equal(process.execPath, join(BASE, 'runtime', 'node', 'node.exe'))
assert.equal(process.argv.length, 10)
assert.deepEqual([process.argv[2], process.argv[4], process.argv[6], process.argv[8]],
  ['--config', '--config-sha', '--source-map', '--source-map-sha'])
const configRaw = readBounded(process.argv[3], 16384); assert.equal(hash(configRaw), process.argv[5])
const mapRaw = readBounded(process.argv[7], 16384); assert.equal(hash(mapRaw), process.argv[9])
const mapping = JSON.parse(mapRaw)
assert.equal(mapping.schema, 'DMKN_V5_LOCAL_NODE_SOURCE_MAP_V1'); assert.equal(mapping.manifest_sha256, MANIFEST_SHA)
assert.equal(mapping.root, dirname(fileURLToPath(import.meta.url)))
assert.deepEqual(Object.keys(mapping.files).sort(), expectedNames)
const allowed = new Set()
for (const [name, digest] of Object.entries(mapping.files)) {
  const path = join(mapping.root, name); assert.equal(hash(readBounded(path, 2 * 1024 ** 2)), digest); allowed.add(path)
}
const manifestRaw = readBounded(join(BASE, 'RELEASE-MANIFEST.json'), 8 * 1024 ** 2)
assert.equal(hash(manifestRaw), MANIFEST_SHA)
const manifest = JSON.parse(manifestRaw)
// Parent has just hash-verified this complete subtree and will do so again
// after exit. This child additionally refuses imports outside that declaration.
for (const name of Object.keys(manifest.files)) if (name.startsWith('overlay/')) allowed.add(join(BASE, ...name.split('/')))
const hook = registerHooks({ resolve (specifier, context, nextResolve) {
  const result = nextResolve(specifier, context)
  if (result.url.startsWith('node:')) return result
  const url = new URL(result.url)
  assert.equal(url.protocol, 'file:'); assert.equal(url.search, ''); assert.equal(url.hash, '')
  assert.ok(allowed.has(fileURLToPath(url)), 'LOCATION_UNDECLARED_IMPORT')
  return result
} })
const P = await import(pathToFileURL(join(mapping.root, 'protocol.mjs')).href)
const { LocalFrames, commandEnvelope } = await import(pathToFileURL(join(mapping.root, 'ipc_wire.mjs')).href)
const { loadRuntime } = await import(pathToFileURL(join(mapping.root, 'runtime.mjs')).href)
const { createLocator } = await import(pathToFileURL(join(mapping.root, 'composition.mjs')).href)
const config = P.parse(configRaw, 16384)
const locator = createLocator(await loadRuntime(join(BASE, 'overlay')), config)
const channel = new LocalFrames(process.stdin, process.stdout, { frame_bytes: 16384, total_bytes: 1024 ** 2, frames: 64 })
let sequence = 0; let terminal = false
const life = new AbortController()
const timer = setTimeout(() => {
  life.abort(new Error('LOCATION_IPC_SERVICE_EXPIRED'))
  process.stdin.destroy(new Error('LOCATION_IPC_SERVICE_EXPIRED'))
  locator.stop().catch(() => {})
}, config.limits.service_ms)
timer.unref()
const reply = (status, result, signal) => channel.write({ schema: 'DMKN_V5_LOCATION_IPC_REPLY_V1', sequence, status, result }, signal)
try {
  const started = await locator.start({ create: true })
  await reply('READY', started, life.signal)
  for await (const message of channel.read()) {
    commandEnvelope(message, sequence)
    sequence++
    const duration = P.uint(message.remaining_wall_ms, 1, 3600000, 'LOCATION_IPC_DURATION')
    const signal = AbortSignal.any([life.signal, AbortSignal.timeout(duration)])
    const cancelOperation = () => {
      locator.controller.abort(signal.reason)
      locator.stop().catch(() => {})
    }
    signal.addEventListener('abort', cancelOperation, { once: true })
    const payload = message.payload; let result
    try {
      switch (message.command) {
        case 'locate':
          result = await locator.locate({ ...payload, remaining_wall_ms: Math.min(duration, payload.remaining_wall_ms) }); break
        case 'descriptor':
          P.need(!Object.hasOwn(payload, 'until'), 'LOCATION_NO_FOREIGN_ABSOLUTE_CLOCK')
          result = await locator.descriptor({ ...payload, until: 0, remaining_wall_ms: Math.min(duration, payload.remaining_wall_ms) }); break
        case 'publish':
          P.fields(payload, ['features', 'stripe']); result = await locator.publish(payload.features, payload.stripe); break
        case 'withdraw':
          P.fields(payload, ['features', 'stripe']); result = await locator.withdraw(payload.features, payload.stripe); break
        case 'status':
          P.fields(payload, []); result = locator.status(); break
        case 'stop':
          P.fields(payload, []); await locator.stop(); result = locator.status(); terminal = true; break
        default: throw new Error('LOCATION_IPC_COMMAND_NOT_ALLOWED')
      }
      signal.throwIfAborted()
      await reply('OK', result, signal)
    } catch (error) {
      // A failed command is terminal. There is no fresh process/allowance on
      // timeout or ambiguity; the parent conservatively settles its ticket.
      await reply('ERROR', { error: `${error.name}: ${error.message}`.slice(0, 500) }, life.signal)
      terminal = true
    } finally { signal.removeEventListener('abort', cancelOperation) }
    if (terminal) break
  }
} finally {
  clearTimeout(timer); await locator.stop(); hook.deregister()
  process.stderr.write(JSON.stringify({ status: 'LOCATION_IPC_CLOSED', sequence, pipe: channel.report(),
    transport: locator.status().transport, mathematical_acceptance: false }) + '\n')
}
