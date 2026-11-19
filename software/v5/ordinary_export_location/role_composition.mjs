/** Selected successor seam: cancel pending raw connects at service exhaustion.
 * The used MaintainedLocator/TransportBudget files remain unchanged.
 */
import { MaintainedLocator } from './maintained_roles.mjs'
import { need } from './protocol.mjs'

export function createLocator (runtime, config) {
  let locator = null
  const adopted = { ...runtime, tcp: { ...runtime.tcp, tcp: options => {
    const factory = runtime.tcp.tcp(options)
    return components => {
      const transport = factory(components); const dial = transport.dial.bind(transport)
      transport.dial = (address, dialOptions) => {
        need(locator != null && dialOptions.signal instanceof AbortSignal, 'LOCATION_CANCEL_COMPOSITION')
        const signal = AbortSignal.any([dialOptions.signal, locator.controller.signal])
        signal.throwIfAborted()
        return dial(address, { ...dialOptions, signal })
      }
      return transport
    }
  } } }
  locator = new MaintainedLocator(adopted, config)
  return locator
}
