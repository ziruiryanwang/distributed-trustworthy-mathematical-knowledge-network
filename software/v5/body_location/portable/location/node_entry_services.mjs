/** Portable owner-selected V2 bootstrap for the fixed adopted Windows runtime.
 * An unavailable TCP dial remains data, not new authority. The trusted parent
 * pins the runtime before/after and supplies actual hard Job containment.
 */
import assert from 'node:assert/strict'
import { readFileSync, lstatSync, realpathSync } from 'node:fs'
import { dirname, join, resolve, relative, isAbsolute, sep } from 'node:path'
import { createHash } from 'node:crypto'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { registerHooks } from 'node:module'

const MANIFEST_SHA = 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
const expectedNames = ['composition.mjs', 'framing.mjs', 'intent.mjs', 'ipc_wire.mjs', 'maintained.mjs',
  'node_entry.mjs', 'protocol.mjs', 'runtime.mjs', 'transport.mjs', 'maintained_roles.mjs',
  'role_composition.mjs', 'node_entry_roles.mjs', 'services_composition.mjs', 'node_entry_services.mjs'].sort()
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

function directory (path) {
  assert.equal(typeof path, 'string'); assert.ok(isAbsolute(path)); assert.equal(resolve(path), path)
  for (let value = path; ; value = dirname(value)) {
    assert.equal(lstatSync(value).isSymbolicLink(), false)
    if (dirname(value) === value) break
  }
  assert.equal(realpathSync(path), path); assert.equal(lstatSync(path).isDirectory(), true)
  return path
}

function beneath (root, path) {
  const name = relative(root, path)
  return name !== '' && name !== '..' && !name.startsWith('..' + sep) && !isAbsolute(name)
}

function disjoint (left, right) {
  return left !== right && !beneath(left, right) && !beneath(right, left)
}

function freshWorkspacePath (workspace, path) {
  assert.equal(typeof path, 'string'); assert.ok(isAbsolute(path)); assert.equal(resolve(path), path)
  assert.ok(beneath(workspace, path), 'LOCATION_FRESH_WORKSPACE_PATH')
  directory(dirname(path))
  try {
    lstatSync(path)
  } catch (error) {
    if (error.code === 'ENOENT') return path
    throw error
  }
  throw new Error('LOCATION_FRESH_WORKSPACE_PATH')
}

function unavailableDial (error, depth = 0) {
  // Do not classify arbitrary messages, authentication/protocol errors, aborts
  // or budget exhaustion as ordinary absence. This is intentionally narrow.
  if (!(error instanceof Error) || depth > 4) return false
  if (error instanceof AggregateError) {
    return Array.isArray(error.errors) && error.errors.length > 0 && error.errors.length <= 16 &&
      error.errors.every(item => unavailableDial(item, depth + 1))
  }
  return error.syscall === 'connect' &&
    ['ECONNREFUSED', 'EHOSTUNREACH', 'ENETUNREACH', 'ETIMEDOUT'].includes(error.code)
}

assert.deepEqual(process.execArgv, [])
assert.equal(process.argv.length, 10)
assert.deepEqual([process.argv[2], process.argv[4], process.argv[6], process.argv[8]],
  ['--config', '--config-sha', '--source-map', '--source-map-sha'])
const configRaw = readBounded(process.argv[3], 16384); assert.equal(hash(configRaw), process.argv[5])
const mapRaw = readBounded(process.argv[7], 16384); assert.equal(hash(mapRaw), process.argv[9])
const mapping = JSON.parse(mapRaw)
assert.deepEqual(Object.keys(mapping).sort(),
  ['files', 'installation_root', 'manifest_sha256', 'root', 'schema', 'workspace_root'])
assert.equal(mapping.schema, 'DMKN_V5_LOCAL_NODE_SOURCE_MAP_V2'); assert.equal(mapping.manifest_sha256, MANIFEST_SHA)
const source = directory(mapping.root)
const installation = directory(mapping.installation_root)
const workspace = directory(mapping.workspace_root)
assert.ok(disjoint(workspace, source) && disjoint(workspace, installation), 'LOCATION_WORKSPACE_IMMUTABLE_ROOT_OVERLAP')
assert.equal(process.cwd(), workspace)
assert.equal(process.execPath, join(installation, 'runtime', 'node', 'node.exe'))
assert.equal(mapping.root, dirname(fileURLToPath(import.meta.url)))
const evidence = directory(dirname(process.argv[3]))
assert.equal(dirname(process.argv[7]), evidence)
assert.equal(process.argv[3], join(evidence, 'config.json'))
assert.equal(process.argv[7], join(evidence, 'source-map.json'))
assert.ok(beneath(workspace, evidence), 'LOCATION_EVIDENCE_SCOPE')
const configuration = JSON.parse(configRaw)
const state = freshWorkspacePath(workspace, configuration.state)
assert.ok(disjoint(state, evidence), 'LOCATION_STATE_EVIDENCE_OVERLAP')
assert.deepEqual(Object.keys(mapping.files).sort(), expectedNames)
const allowed = new Set()
for (const [name, digest] of Object.entries(mapping.files)) {
  const path = join(mapping.root, name); assert.equal(hash(readBounded(path, 2 * 1024 ** 2)), digest); allowed.add(path)
}
const manifestRaw = readBounded(join(installation, 'RELEASE-MANIFEST.json'), 8 * 1024 ** 2)
assert.equal(hash(manifestRaw), MANIFEST_SHA)
const manifest = JSON.parse(manifestRaw)
for (const name of Object.keys(manifest.files)) if (name.startsWith('overlay/')) allowed.add(join(installation, ...name.split('/')))
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
const { loadRuntime, createLocator } = await import(pathToFileURL(join(mapping.root, 'services_composition.mjs')).href)
const config = P.parse(configRaw, 16384)
const locator = createLocator(await loadRuntime(join(installation, 'overlay')), config)
const channel = new LocalFrames(process.stdin, process.stdout, { frame_bytes: 16384, total_bytes: 1024 ** 2, frames: 64 })
let sequence = 0; let terminal = false; let unavailable = 0
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
        case 'locate-body':
          result = await locator.locateBody({ ...payload, remaining_wall_ms: Math.min(duration, payload.remaining_wall_ms) }); break
        case 'descriptor':
          P.need(!Object.hasOwn(payload, 'until'), 'LOCATION_NO_FOREIGN_ABSOLUTE_CLOCK')
          result = await locator.descriptor({ ...payload, until: 0, remaining_wall_ms: Math.min(duration, payload.remaining_wall_ms) }); break
        case 'descriptor-body':
          P.need(!Object.hasOwn(payload, 'until'), 'LOCATION_NO_FOREIGN_ABSOLUTE_CLOCK')
          result = await locator.descriptorBody({ ...payload, until: 0, remaining_wall_ms: Math.min(duration, payload.remaining_wall_ms) }); break
        case 'publish':
          P.fields(payload, ['features', 'stripe']); result = await locator.publish(payload.features, payload.stripe); break
        case 'withdraw':
          P.fields(payload, ['features', 'stripe']); result = await locator.withdraw(payload.features, payload.stripe); break
        case 'publish-body':
          P.fields(payload, ['body']); result = await locator.publishBody(payload.body); break
        case 'withdraw-body':
          P.fields(payload, ['body']); result = await locator.withdrawBody(payload.body); break
        case 'status':
          P.fields(payload, []); result = locator.status(); break
        case 'stop':
          P.fields(payload, []); await locator.stop(); result = locator.status(); terminal = true; break
        default: throw new Error('LOCATION_IPC_COMMAND_NOT_ALLOWED')
      }
      signal.throwIfAborted()
      await reply('OK', result, signal)
    } catch (error) {
      if (['descriptor', 'descriptor-body'].includes(message.command) && !signal.aborted && !life.signal.aborted &&
          !locator.controller.signal.aborted && !locator.stopped &&
          locator.until != null && performance.now() < locator.until && unavailableDial(error)) {
        // Same command, channel, service, transport counters and owner deadline.
        // There is no remote authentication or claimed nonexistence here.
        unavailable++
        await reply('OK', { status: 'DESCRIPTOR_UNAVAILABLE', ticket: payload.ticket,
          peer: payload.peer, reason: 'TCP_CONNECT_UNAVAILABLE', mathematical_acceptance: false }, signal)
      } else {
        await reply('ERROR', { error: `${error.name}: ${error.message}`.slice(0, 500) }, life.signal)
        terminal = true
      }
    } finally { signal.removeEventListener('abort', cancelOperation) }
    if (terminal) break
  }
} finally {
  clearTimeout(timer); await locator.stop(); hook.deregister()
  process.stderr.write(JSON.stringify({ status: 'LOCATION_IPC_CLOSED', sequence,
    descriptor_unavailable: unavailable, pipe: channel.report(), transport: locator.status().transport,
    mathematical_acceptance: false }) + '\n')
}

