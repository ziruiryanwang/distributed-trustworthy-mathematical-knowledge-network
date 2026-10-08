/** Root-selected bounded Node controls: all verification is inside the same Job. */
import assert from 'node:assert/strict'
import { lstatSync, readFileSync, readdirSync, realpathSync, openSync, readSync, closeSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { resolve, join, dirname, relative, isAbsolute, sep } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { registerHooks } from 'node:module'

const ROOT = 'E:\\Distributed Trustworthy Mathematical Knowledge Network'
const BASE = join(ROOT, 'product-local', 'v4-library-commons-02', 'commons-v4')
const MANIFEST_SHA = 'a93714ecd267984d2bdc7830fc28027151d650d5b0aeea13fac850b52ba5beed'
const PATCH_SHA = 'e5546b65630d115c1081233d4e1591f624cedb9b3a242e8d247aac3558d7dcc8'
const digest = raw => createHash('sha256').update(raw).digest('hex')
const startCPU = process.cpuUsage(); const startWall = performance.now()
assert.equal(process.cwd(), ROOT); assert.deepEqual(process.execArgv, [])
assert.equal(process.argv.length, 4); assert.equal(process.argv[2], '--output')
const output = process.argv[3]
assert.ok(isAbsolute(output) && resolve(output) === output && output.startsWith(join(ROOT, 'experiments', 'v5-local-checks') + sep))
const snapshot = join(output, 'sources')
const current = fileURLToPath(import.meta.url)
assert.equal(current, join(snapshot, 'software', 'v5', 'location', 'run_node_controls.mjs'))
assert.equal(process.execPath, join(BASE, 'runtime', 'node', 'node.exe'))
assert.equal(process.env.NODE_OPTIONS, undefined); assert.equal(process.env.NODE_PATH, undefined)

function ordinary (path, directory = false) {
  assert.equal(resolve(path), path)
  for (let item = path; ; item = dirname(item)) {
    assert.equal(lstatSync(item).isSymbolicLink(), false, item)
    if (dirname(item) === item) break
  }
  assert.equal(directory ? lstatSync(path).isDirectory() : lstatSync(path).isFile(), true, path)
  assert.equal(realpathSync(path), path)
}
function hashFile (path, size) {
  ordinary(path); assert.equal(lstatSync(path).size, size)
  assert.ok(Number.isSafeInteger(size) && size >= 0 && size <= 128 * 1024 ** 2)
  const fd = openSync(path, 'r'); const buffer = Buffer.alloc(Math.min(Math.max(size, 1), 1024 ** 2)); const hash = createHash('sha256')
  let length = 0
  try {
    while (true) { const count = readSync(fd, buffer, 0, buffer.length, null); if (count === 0) break; length += count; assert.ok(length <= size); hash.update(buffer.subarray(0, count)) }
  } finally { closeSync(fd) }
  assert.equal(length, size); assert.equal(lstatSync(path).size, size)
  return hash.digest('hex')
}
const selectionPath = join(output, 'selection.json')
ordinary(selectionPath); assert.ok(lstatSync(selectionPath).size <= 1024 ** 2)
const selectionRaw = readFileSync(selectionPath); const selection = JSON.parse(selectionRaw)
assert.equal(selection.schema, 'DMKN_V5_LOCAL_CHECK_V1')
const allowed = new Set(); const imported = new Set()
function verifySources () {
  assert.deepEqual(readFileSync(selectionPath), selectionRaw)
  for (const [name, expected] of Object.entries(selection.sources)) {
    assert.ok(!name.includes('\\') && !name.split('/').some(part => ['', '.', '..'].includes(part)))
    const path = join(snapshot, ...name.split('/')); ordinary(path)
    assert.ok(lstatSync(path).size <= 2 * 1024 ** 2)
    assert.equal(hashFile(path, lstatSync(path).size), expected, name)
    allowed.add(path)
  }
}
function verifyRuntime () {
  const began = process.cpuUsage(); const wall = performance.now()
  const manifest = join(BASE, 'RELEASE-MANIFEST.json'); ordinary(manifest)
  assert.ok(lstatSync(manifest).size <= 8 * 1024 ** 2)
  const bytes = readFileSync(manifest); assert.equal(digest(bytes), MANIFEST_SHA)
  const value = JSON.parse(bytes)
  assert.equal(value.schema, 'DMKN_COMPACT_COMMONS_RELEASE_V1')
  const selected = Object.entries(value.files).filter(([name]) => name.startsWith('overlay/') || name.startsWith('runtime/node/'))
  assert.equal(selected.length, 5896)
  assert.equal(value.files['overlay/VENDOR-PATCHES.patch'].sha256, PATCH_SHA)
  const actual = new Set(); let directories = 0
  const walk = directory => {
    ordinary(directory, true); assert.ok(++directories <= 10000)
    for (const entry of readdirSync(directory, { withFileTypes: true })) {
      const path = join(directory, entry.name); const info = lstatSync(path)
      assert.equal(info.isSymbolicLink(), false, path)
      if (info.isDirectory()) walk(path)
      else { assert.ok(info.isFile()); actual.add(relative(BASE, path).split(sep).join('/')); assert.ok(actual.size <= 10000) }
    }
  }
  walk(join(BASE, 'overlay')); walk(join(BASE, 'runtime', 'node'))
  assert.deepEqual([...actual].sort(), selected.map(([name]) => name).sort())
  let total = 0
  for (const [name, row] of selected) {
    assert.ok(!name.includes('\\') && !name.split('/').some(part => ['', '.', '..'].includes(part)))
    const path = join(BASE, ...name.split('/')); total += row.bytes; assert.ok(total <= 192 * 1024 ** 2)
    assert.equal(hashFile(path, row.bytes), row.sha256, name); allowed.add(path)
  }
  return { files: selected.length, bytes: total, cpu_microseconds: process.cpuUsage(began), wall_ms: performance.now() - wall }
}

verifySources()
const pre = verifyRuntime()
// The retained known closure is small enough to hash in full (all overlay
// packages, including patched files, not unrelated Lean/prover/Python assets).
// Resolution is additionally confined so an undeclared parent node_modules,
// data URL, network URL or injected package cannot become an opaque import.
const hook = registerHooks({ resolve (specifier, context, nextResolve) {
  const result = nextResolve(specifier, context)
  if (result.url.startsWith('node:')) return result
  const url = new URL(result.url)
  assert.equal(url.protocol, 'file:'); assert.equal(url.search, ''); assert.equal(url.hash, '')
  const path = fileURLToPath(url); assert.ok(allowed.has(path), 'UNDECLARED_NODE_IMPORT:' + path)
  imported.add(path); return result
} })
let testError = null; let post = null
try {
  process.argv = [process.execPath, join(snapshot, 'software', 'v5', 'location', 'test_location_node.mjs'),
    '--runtime-root', join(BASE, 'overlay'), '--state', join(output, 'node-state')]
  await import(pathToFileURL(process.argv[1]).href)
} catch (error) { testError = error }
finally { hook.deregister(); post = verifyRuntime(); verifySources() }
console.log(JSON.stringify({ status: testError == null ? 'PASS_NODE_CONTROLS_AND_FULL_SELECTED_RUNTIME_BINDING' : 'NODE_CONTROLS_FAILED',
  manifest_sha256: MANIFEST_SHA, vendor_patch_sha256: PATCH_SHA, selected_runtime_pre: pre, selected_runtime_post: post,
  imported_files: imported.size, total_cpu_microseconds: process.cpuUsage(startCPU), total_wall_ms: performance.now() - startWall,
  accounting: 'ALL_HASHING_AND_CONTROLS_INSIDE_ONE_JOB_NOT_ADDITIONAL_CHARGES',
  qualification: 'SOURCE_BOUNDARY_CONTROLS_NOT_REAL_NETWORK_OR_MATHEMATICAL_ACCEPTANCE' }))
if (testError != null) throw testError
