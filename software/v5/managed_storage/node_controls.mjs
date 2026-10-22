/** Selected local SQLite controls. No service, network or private-key generation.
 * The root-owned supervisor supplies the finite Job and immutable source snapshot.
 * All fixture files are retained, including every refused database/journal.
 */
import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { closeSync, lstatSync, mkdirSync, openSync, readFileSync, readSync,
  readdirSync, realpathSync, writeFileSync } from 'node:fs'
import { dirname, isAbsolute, join, relative, resolve, sep } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { registerHooks } from 'node:module'

const ROOT = 'E:\\Distributed Trustworthy Mathematical Knowledge Network'
const BASE = join(ROOT, 'product-local', 'v5-distribution-managed-observed-01', 'Mathematical Commons v5', 'base')
const MANIFEST_SHA = 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
const NODE_SHA = 'b3094d0b49f9ad602262a9921551737bb97637c05dd357a06ae98188d7290aa3'
const QUOTA_SHA = '7c6cbeea0c685ec81f8d263cf84c6b8b9dd2c1f09e9f2f0f063196abc929eca4'
const INTENT_SHA = '6c30e8793f737f0512e3e7e9d785d1311cafa35116784f4f8b3dda5c1a75fa29'
const ROLES_SHA = 'd69d0b123e52f5cfbf4c2eef2e2d2dfecf9b9b11c9ddfabc4c5e37499e1a12e0'
const PROTOCOL_SHA = '88c2bc34e5ebefc412b564bef06e0d4210e0c44e3102be1d6adacfc6334af986'
const SOURCE_PREFIX = 'software/v5/managed_storage/'
const started = performance.now(); const cpuStarted = process.cpuUsage()
const digest = raw => createHash('sha256').update(raw).digest('hex')
assert.equal(process.cwd(), ROOT)
assert.deepEqual(process.execArgv, [])
assert.equal(process.env.NODE_OPTIONS, undefined)
assert.equal(process.env.NODE_PATH, undefined)
assert.equal(process.execPath, join(BASE, 'runtime', 'node', 'node.exe'))
assert.equal(process.argv.length, 4)
assert.equal(process.argv[2], '--output')
const output = process.argv[3]
assert.ok(isAbsolute(output) && resolve(output) === output &&
  output.startsWith(join(ROOT, 'experiments', 'v5-local-checks') + sep))
const snapshot = join(output, 'sources')
const self = fileURLToPath(import.meta.url)
assert.equal(self, join(snapshot, ...SOURCE_PREFIX.split('/'), 'node_controls.mjs'))

function ordinary (path, directory = false) {
  assert.equal(resolve(path), path)
  for (let item = path; ; item = dirname(item)) {
    const stat = lstatSync(item)
    assert.equal(stat.isSymbolicLink(), false, item)
    if (item !== path) assert.equal(stat.isDirectory(), true, item)
    if (dirname(item) === item) break
  }
  const stat = lstatSync(path)
  assert.equal(directory ? stat.isDirectory() : stat.isFile(), true, path)
  assert.equal(realpathSync(path), path)
  if (!directory) assert.equal(stat.nlink, 1, path)
  return stat
}
function bounded (path, maximum) {
  const size = ordinary(path).size
  assert.ok(size > 0 && size <= maximum, path)
  const raw = readFileSync(path)
  assert.equal(raw.length, size)
  return raw
}
function hashFile (path, size) {
  assert.equal(ordinary(path).size, size)
  assert.ok(Number.isSafeInteger(size) && size >= 0 && size <= 128 * 1024 ** 2)
  const fd = openSync(path, 'r'); const buffer = Buffer.alloc(Math.min(Math.max(size, 1), 1024 ** 2))
  const hash = createHash('sha256'); let bytes = 0
  try {
    for (;;) {
      const count = readSync(fd, buffer, 0, buffer.length, null)
      if (count === 0) break
      bytes += count; assert.ok(bytes <= size); hash.update(buffer.subarray(0, count))
    }
  } finally { closeSync(fd) }
  assert.equal(bytes, size); assert.equal(ordinary(path).size, size)
  return hash.digest('hex')
}
ordinary(output, true); ordinary(snapshot, true)
const selectionPath = join(output, 'selection.json')
const selectionRaw = bounded(selectionPath, 1024 ** 2)
const selection = JSON.parse(selectionRaw)
assert.equal(selection.schema, 'DMKN_V5_LOCAL_CHECK_V1')
assert.ok(selection.sources != null && typeof selection.sources === 'object')
const sourcePins = new Map()
for (const [name, pin] of [
  ['node_controls.mjs', null], ['portable/location/intent.mjs', INTENT_SHA],
  ['portable/location/maintained_roles.mjs', ROLES_SHA], ['portable/location/protocol.mjs', PROTOCOL_SHA]
]) {
  const key = SOURCE_PREFIX + name; const selected = selection.sources[key]
  assert.match(selected, /^[0-9a-f]{64}$/)
  if (pin != null) assert.equal(selected, pin, key)
  const path = join(snapshot, ...key.split('/'))
  const raw = bounded(path, 128 * 1024)
  assert.equal(digest(raw), selected, key)
  sourcePins.set(path, { bytes: raw.length, sha256: selected })
}
const manifestPath = join(BASE, 'RELEASE-MANIFEST.json')
const manifestRaw = bounded(manifestPath, 2 * 1024 ** 2)
assert.equal(digest(manifestRaw), MANIFEST_SHA)
const manifest = JSON.parse(manifestRaw)
assert.equal(manifest.schema, 'DMKN_COMPACT_COMMONS_RELEASE_V1')
const nodeRow = manifest.files['runtime/node/node.exe']
assert.equal(nodeRow.bytes, 92279112); assert.equal(nodeRow.sha256, NODE_SHA)
assert.equal(hashFile(process.execPath, nodeRow.bytes), NODE_SHA)
assert.equal(manifest.files['overlay/quota_store.mjs'].sha256, QUOTA_SHA)
const imported = new Map()
const packageMetadata = new Map()
const builtins = new Set(['node:assert/strict', 'node:crypto', 'node:fs', 'node:path',
  'node:url', 'node:module', 'node:sqlite', 'node:buffer', 'node:util', 'node:events',
  'node:tty', 'node:os', 'node:process'])
function admittedFile (url) {
  const parsed = new URL(url)
  assert.equal(parsed.protocol, 'file:'); assert.equal(parsed.search, ''); assert.equal(parsed.hash, '')
  const path = fileURLToPath(parsed)
  let row = sourcePins.get(path)
  if (row == null) {
    const name = relative(BASE, path).split(sep).join('/')
    assert.ok(name.startsWith('overlay/') && !name.split('/').includes('..'), 'UNSELECTED_MODULE:' + name)
    row = manifest.files[name]
    assert.ok(row != null && Number.isSafeInteger(row.bytes) && row.bytes <= 2 * 1024 ** 2)
    // Package scope/exports metadata also influences Node's resolver. Bind every
    // present enclosing package.json, without enumerating the unrelated runtime.
    for (let scope = dirname(path); scope.startsWith(join(BASE, 'overlay')); scope = dirname(scope)) {
      const metadata = join(scope, 'package.json')
      if (packageMetadata.has(metadata)) continue
      const key = relative(BASE, metadata).split(sep).join('/')
      const selected = manifest.files[key]
      if (selected != null) {
        assert.equal(hashFile(metadata, selected.bytes), selected.sha256, key)
        packageMetadata.set(metadata, selected)
      } else {
        assert.throws(() => lstatSync(metadata), { code: 'ENOENT' })
      }
    }
  }
  assert.equal(hashFile(path, row.bytes), row.sha256, path)
  imported.set(path, row)
  return { path, row }
}
const hooks = registerHooks({
  resolve (specifier, context, nextResolve) {
    const result = nextResolve(specifier, context)
    if (result.url.startsWith('node:')) assert.ok(builtins.has(result.url), 'UNSELECTED_BUILTIN:' + result.url)
    else admittedFile(result.url)
    return result
  },
  load (url, context, nextLoad) {
    if (url.startsWith('node:')) { assert.ok(builtins.has(url)); return nextLoad(url, context) }
    const { path, row } = admittedFile(url)
    const result = nextLoad(url, context)
    assert.ok(result.source != null && result.format === 'module', 'UNEXPECTED_MODULE_FORMAT:' + path)
    const raw = typeof result.source === 'string' ? Buffer.from(result.source) :
      (result.source instanceof ArrayBuffer ? Buffer.from(result.source) :
        Buffer.from(result.source.buffer, result.source.byteOffset, result.source.byteLength))
    assert.equal(raw.length, row.bytes); assert.equal(digest(raw), row.sha256, path)
    return result
  }
})
const report = { schema: 'DMKN_V5_MANAGED_STORAGE_NODE_CONTROLS_V1', status: 'FAIL', groups: [],
  scope: 'ACTUAL_INTENT_SQLITE_AND_STATIC_IDENTITY_ORDER_ONLY', mathematical_acceptance: false,
  service_or_network_started: false, private_key_generation: false, whole_root_envelope_adopted: false }
const fixtures = join(output, 'node-fixtures')
const closedStores = new Set()
const limits = { entries: 32, bytes: 65536, valueBytes: 1024, providersPerKey: 2, pages: 256 }
const identityFixture = Buffer.from('SYNTHETIC TEST FIXTURE; NOT A PRIVATE KEY\n', 'ascii')
const adoptionFixture = Buffer.from('{"config_sha256":"' + '0'.repeat(64) + '","schema":"DMKN_V5_LOCATION_STATE_V1"}', 'ascii')
function inventory (directory) {
  ordinary(directory, true)
  const rows = []; let total = 0
  const visit = (parent, depth) => {
    assert.ok(depth <= 2)
    for (const entry of readdirSync(parent, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const path = join(parent, entry.name); const stat = lstatSync(path)
      assert.equal(stat.isSymbolicLink(), false)
      const name = relative(directory, path).split(sep).join('/')
      if (stat.isDirectory()) { rows.push({ name, directory: true }); visit(path, depth + 1) }
      else {
        assert.ok(stat.isFile() && stat.size <= 1024 ** 2)
        total += stat.size; assert.ok(total <= 1024 ** 2)
        rows.push({ name, bytes: stat.size, sha256: hashFile(path, stat.size) })
      }
      assert.ok(rows.length <= 64)
    }
  }
  visit(directory, 0); return { bytes: total, rows }
}
function fixture (name) {
  const state = join(fixtures, name); mkdirSync(state)
  writeFileSync(join(state, 'identity.key'), identityFixture, { flag: 'wx' })
  writeFileSync(join(state, 'adopted.json'), adoptionFixture, { flag: 'wx' })
  return state
}
async function closeStore (store) {
  await store.close(); assert.equal(store.db, null); closedStores.delete(store)
}
let failure = null
try {
  const rolesPath = join(snapshot, ...SOURCE_PREFIX.split('/'), 'portable', 'location', 'maintained_roles.mjs')
  const roles = bounded(rolesPath, 128 * 1024).toString('utf8')
  const start = roles.indexOf('      if (create) {', roles.indexOf('  async _startCore (create) {'))
  const firstWrite = roles.indexOf('        await writeFile(keyPath, identityRaw,', start)
  const secondWrite = roles.indexOf('        await writeFile(adoptionPath, adoptionRaw,', firstWrite)
  assert.ok(start >= 0 && firstWrite > start && secondWrite > firstWrite)
  const before = roles.slice(start, firstWrite)
  assert.equal((before.match(/writeFile\(/g) ?? []).length, 0)
  assert.ok(before.includes('identityRaw instanceof Uint8Array && identityRaw.byteLength > 0 && identityRaw.byteLength <= 1024 &&'))
  assert.ok(before.includes('adoptionRaw instanceof Uint8Array && adoptionRaw.byteLength > 0 && adoptionRaw.byteLength <= 1024,'))
  assert.ok(before.includes("'LOCATION_IDENTITY_SERIALIZATION_BOUND')"))
  report.groups.push({ name: 'identity-buffers-before-writes', status: 'PASS', evidence: 'STATIC_SOURCE_ONLY_NO_KEY_EXECUTION' })

  const { intentStoreClass } = await import(pathToFileURL(join(snapshot, ...SOURCE_PREFIX.split('/'), 'portable', 'location', 'intent.mjs')).href)
  const { QuotaDatastore } = await import(pathToFileURL(join(BASE, 'overlay', 'quota_store.mjs')).href)
  const { Key } = await import(pathToFileURL(join(BASE, 'overlay', 'node_modules', 'interface-datastore', 'dist', 'src', 'index.js')).href)
  // A deterministic, syntactically valid public-shaped ID; no private key exists.
  const alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
  let number = BigInt('0x002408011220' + '03'.repeat(32)); let encoded = ''
  while (number > 0n) { encoded = alphabet[Number(number % 58n)] + encoded; number /= 58n }
  const owner = { toString: () => '1' + encoded }
  const Store = intentStoreClass(QuotaDatastore, Key, () => { throw new Error('PROVIDER_INTENT_NOT_IN_THIS_CONTROL') })
  const newStore = state => { const store = new Store(join(state, 'metadata.sqlite'), limits, owner); closedStores.add(store); return store }
  mkdirSync(fixtures)
  const fresh = fixture('fresh-profile'); const store = newStore(fresh)
  await store.open()
  const profile = {}
  for (const [name, expected] of [['page_size', 4096], ['auto_vacuum', 0], ['journal_mode', 'delete'],
    ['synchronous', 2], ['temp_store', 2], ['max_page_count', 256]]) {
    profile[name] = store.db.prepare('PRAGMA ' + name).get()[name]; assert.equal(profile[name], expected)
  }
  assert.ok(store.db.prepare('PRAGMA cache_spill').get().cache_spill > 0)
  assert.equal(store.report().entries, 0); assert.equal(store.report().bytes, 0)
  const key = new Key('/application/control'); const first = Uint8Array.of(1, 2, 3); const replacement = Uint8Array.of(9, 8)
  assert.equal(await store.put(key, first), key)
  assert.deepEqual(await store.get(key), first); assert.equal(await store.has(key), true)
  assert.equal(store.report().entries, 1); assert.equal(store.report().bytes, Buffer.byteLength(key.toString()) + first.length)
  await store.put(key, replacement)
  assert.deepEqual(await store.get(key), replacement)
  assert.equal(store.report().entries, 1); assert.equal(store.report().bytes, Buffer.byteLength(key.toString()) + replacement.length)
  const beforeBadValue = store.report()
  await assert.rejects(store.put(key, new Uint8Array(1025)), { message: 'STORE_VALUE_BOUND' })
  assert.deepEqual(store.report(), beforeBadValue); assert.deepEqual(await store.get(key), replacement)
  await store.delete(key); assert.equal(await store.has(key), false)
  assert.equal(store.report().entries, 0); assert.equal(store.report().bytes, 0)
  await closeStore(store)
  assert.deepEqual(readFileSync(join(fresh, 'identity.key')), identityFixture)
  assert.deepEqual(readFileSync(join(fresh, 'adopted.json')), adoptionFixture)
  report.groups.push({ name: 'fresh-profile-inherited-operations-and-close', status: 'PASS', profile })

  async function refuseUnchanged (state, name) {
    const before = inventory(state); const refused = newStore(state)
    await assert.rejects(refused.open(), { message: 'LOCATION_METADATA_STATE_ENTRIES' })
    assert.equal(refused.db, null)
    await closeStore(refused)
    assert.deepEqual(inventory(state), before)
    report.groups.push({ name, status: 'PASS', error: 'LOCATION_METADATA_STATE_ENTRIES', retained_files_unchanged: true })
  }
  await refuseUnchanged(fresh, 'same-profile-database-reopen-refused')
  for (const [name, forbidden] of [['journal', 'metadata.sqlite-journal'], ['wal', 'metadata.sqlite-wal'],
    ['shm', 'metadata.sqlite-shm'], ['extra', 'unexpected.bin']]) {
    const state = fixture('refuse-' + name)
    writeFileSync(join(state, forbidden), Buffer.from('SYNTHETIC RETAINED REFUSAL FIXTURE\n'), { flag: 'wx' })
    await refuseUnchanged(state, name + '-refused-before-database-creation')
    assert.equal(readdirSync(state).includes('metadata.sqlite'), false)
  }
  assert.equal(report.groups.length, 7)
  report.fixtures = inventory(fixtures)
  report.status = 'PASS'
} catch (error) {
  failure = error
  report.error = { name: String(error?.name ?? 'Error').slice(0, 80), message: String(error?.message ?? error).slice(0, 1000) }
} finally {
  report.close_errors = []
  for (const store of [...closedStores]) {
    try { await closeStore(store) } catch (error) { report.close_errors.push(String(error?.message ?? error).slice(0, 300)); failure ??= error }
  }
  hooks.deregister()
  try {
    assert.deepEqual(bounded(selectionPath, 1024 ** 2), selectionRaw)
    assert.deepEqual(bounded(manifestPath, 2 * 1024 ** 2), manifestRaw)
    for (const [path, row] of sourcePins) assert.equal(hashFile(path, row.bytes), row.sha256)
    for (const [path, row] of imported) assert.equal(hashFile(path, row.bytes), row.sha256)
    for (const [path, row] of packageMetadata) assert.equal(hashFile(path, row.bytes), row.sha256)
    assert.equal(hashFile(process.execPath, nodeRow.bytes), NODE_SHA)
    report.binding = { manifest_sha256: MANIFEST_SHA, node_sha256: NODE_SHA, quota_sha256: QUOTA_SHA,
      imported_files: [...imported.keys()].map(path => path.startsWith(BASE + sep) ? relative(BASE, path).split(sep).join('/') : relative(snapshot, path).split(sep).join('/')),
      package_metadata_files: [...packageMetadata.keys()].map(path => relative(BASE, path).split(sep).join('/')),
      scope: 'EXACT_IMPORTED_CLOSURE_PRE_LOAD_AND_POST_NOT_FULL_RUNTIME_TREE_CENSUS' }
  } catch (error) {
    failure ??= error; report.binding_error = String(error?.message ?? error).slice(0, 1000)
  }
  if (failure != null) report.status = 'FAIL'
  report.cpu_microseconds = process.cpuUsage(cpuStarted)
  report.wall_ms = performance.now() - started
  const result = Buffer.from(JSON.stringify(report) + '\n')
  assert.ok(result.length <= 65536)
  writeFileSync(join(output, 'node-controls-result.json'), result, { flag: 'wx' })
  console.log(result.toString('utf8').trimEnd())
}
if (failure != null) throw failure
