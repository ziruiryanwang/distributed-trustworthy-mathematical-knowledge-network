/** Supply the retained DHT's required Ping capability, not a new protocol stack.
 * The parent verifies the full retained runtime before/after this import, and
 * the selected Node entry confines imports to that manifest and pinned source.
 */
import { lstat, realpath } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { loadRuntime as loadBaseRuntime } from './runtime.mjs'
import { createLocator as createRoleLocator } from './role_composition.mjs'
import { fields, need } from './protocol.mjs'

export async function loadRuntime (root) {
  const runtime = await loadBaseRuntime(root)
  const path = join(runtime.selectedRoot, 'node_modules', '@libp2p', 'ping', 'dist', 'src', 'index.js')
  for (let check = path; check !== runtime.selectedRoot; check = dirname(check)) {
    need(!(await lstat(check)).isSymbolicLink(), 'LOCATION_PING_NO_LINKS')
  }
  need((await lstat(path)).isFile() && await realpath(path) === path, 'LOCATION_PING_CANONICAL')
  const ping = await import(pathToFileURL(path).href)
  need(typeof ping.ping === 'function', 'LOCATION_REQUIRED_PING_FACTORY')
  return Object.freeze({ ...runtime, ping })
}

export function createLocator (runtime, config) {
  need(typeof runtime.ping?.ping === 'function', 'LOCATION_REQUIRED_PING_FACTORY')
  const adopted = { ...runtime, libp2p: { ...runtime.libp2p,
    createLibp2p: async input => {
      fields(input.services, ['identify', 'dht'])
      // Only supply the missing capability. It uses the SAME bounded transport,
      // owner egress, stream muxer, service lifetime and outer process Job.
      const services = { identify: input.services.identify,
        ping: runtime.ping.ping({ timeout: Math.min(5000, config.limits.operation_ms),
          maxInboundStreams: 4, maxOutboundStreams: 8 }), dht: input.services.dht }
      return await runtime.libp2p.createLibp2p({ ...input, services })
    }
  } }
  return createRoleLocator(adopted, config)
}
