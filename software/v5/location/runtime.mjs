/** Owner-selected fixed import table. Launcher pins the full retained runtime. */
import { isAbsolute, join, resolve, dirname } from 'node:path'
import { lstat, realpath } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'
import { need } from './protocol.mjs'

const IMPORTS = Object.freeze({
  libp2p: 'node_modules/libp2p/dist/src/index.js',
  tcp: 'node_modules/@libp2p/tcp/dist/src/index.js',
  noise: 'node_modules/@chainsafe/libp2p-noise/dist/src/index.js',
  yamux: 'node_modules/@chainsafe/libp2p-yamux/dist/src/index.js',
  identify: 'node_modules/@libp2p/identify/dist/src/index.js',
  dht: 'node_modules/@libp2p/kad-dht/dist/src/index.js',
  dhtUtils: 'node_modules/@libp2p/kad-dht/dist/src/utils.js',
  dhtEvents: 'node_modules/@libp2p/kad-dht/dist/src/query/events.js',
  dhtNetwork: 'node_modules/@libp2p/kad-dht/dist/src/network.js',
  tcpSocket: 'node_modules/@libp2p/tcp/dist/src/socket-to-conn.js',
  keys: 'node_modules/@libp2p/crypto/dist/src/keys/index.js',
  peers: 'node_modules/@libp2p/peer-id/dist/src/index.js',
  addresses: 'node_modules/@multiformats/multiaddr/dist/src/index.js',
  cid: 'node_modules/multiformats/dist/src/cid.js',
  digest: 'node_modules/multiformats/dist/src/hashes/digest.js',
  datastore: 'node_modules/interface-datastore/dist/src/index.js',
  quota: 'quota_store.mjs'
})

export async function loadRuntime (root) {
  need(typeof root === 'string' && isAbsolute(root) && resolve(root) === root && dirname(root) !== root, 'LOCATION_RUNTIME_ROOT')
  need((await lstat(root)).isDirectory() && !(await lstat(root)).isSymbolicLink() && await realpath(root) === root, 'LOCATION_RUNTIME_CANONICAL')
  const entries = {}
  for (const [name, relative] of Object.entries(IMPORTS)) {
    const path = join(root, relative)
    let check = path
    while (check !== root) { const stat = await lstat(check); need(!stat.isSymbolicLink(), 'LOCATION_RUNTIME_NO_LINKS'); check = dirname(check) }
    need((await lstat(path)).isFile(), 'LOCATION_RUNTIME_FILE')
    entries[name] = await import(pathToFileURL(path).href)
  }
  return Object.freeze({ ...entries, selectedRoot: root })
}

// This loader checks path shape and fixes module names; it does NOT authenticate
// a dependency tree merely because a caller named a directory. The root-owned
// runtime selection must hash-pin Node, every transitive dependency and retained
// vendor patch before launch. A remote descriptor never reaches this interface.
