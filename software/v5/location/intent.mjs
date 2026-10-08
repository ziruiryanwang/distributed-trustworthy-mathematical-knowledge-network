/** New v5 logical keys over the retained adopted quota-store primitive. */
import { canonical, fields, hexid, need, peerId, routeKey } from './protocol.mjs'

export const PROVIDER_PREFIX = '/dmknv5/provider'
export function bindCID (cid, key) {
  hexid(key)
  need(cid.version === 1 && cid.code === 0x55 && cid.multihash.code === 0x12 &&
    cid.multihash.size === 32 && Buffer.from(cid.multihash.digest).equals(Buffer.from(key, 'hex')), 'LOCATION_CID_BINDING')
}

// Arguments are adopted local runtime classes, never fields in peer messages.
export function intentStoreClass (QuotaDatastore, Key, toProviderKey) {
  return class V5IntentQuotaDatastore extends QuotaDatastore {
    constructor (path, limits, owner) {
      super(path, { ...limits, providerPrefix: PROVIDER_PREFIX })
      Object.defineProperty(this, 'ownerId', { value: peerId(owner.toString()) })
      Object.defineProperty(this, 'owner', { value: owner })
    }
    _intentKey (providerKey) {
      const parts = this._key(providerKey).split('/')
      need(parts.length === 5 && parts[1] === 'dmknv5' && parts[2] === 'provider' &&
        /^[A-Za-z0-9]{1,256}$/.test(parts[3]) && parts[4] === this.ownerId, 'LOCATION_INTENT_PROVIDER_KEY')
      return '/application/provider-intent/' + parts[3]
    }
    _put (key, value) {
      const text = this._key(key)
      if (text.startsWith(PROVIDER_PREFIX + '/') && text.endsWith('/' + this.ownerId)) {
        // Same synchronous SQLite transaction as insertion. No awaited has/put.
        need(this.db.prepare('SELECT 1 AS present FROM kv WHERE k=?').get(this._intentKey(text)) != null,
          'LOCATION_LOCAL_PROVIDER_INTENT_REVOKED')
      }
      super._put(key, value)
    }
    async open () {
      await super.open()
      try {
        for (const row of this.db.prepare("SELECT k FROM kv WHERE k LIKE '/dmknv5/provider/%'").iterate()) {
          if (row.k.endsWith('/' + this.ownerId)) need(this.db.prepare('SELECT 1 AS present FROM kv WHERE k=?').get(this._intentKey(row.k)) != null, 'LOCATION_ORPHAN_SELF_HINT')
        }
      } catch (error) { await this.close(); throw error }
    }
    async enableIntent (cid, key, spec, options) {
      bindCID(cid, key)
      fields(spec, ['namespace', 'role', 'predicate', 'stripe']); fields(spec.predicate, ['all'])
      need(spec.role === 'formal-index-v1' && routeKey(spec.namespace, spec.predicate.all, spec.stripe) === key, 'LOCATION_INTENT_KEY_BINDING')
      const intent = this._intentKey(toProviderKey(PROVIDER_PREFIX, cid, this.owner))
      const published = new Key('/application/published/' + key)
      const raw = canonical(spec)
      this._transaction(() => { this._put(intent, raw); this._put(published, raw) }, options)
    }
    async revokeIntent (cid, key, options) {
      bindCID(cid, key)
      const provider = toProviderKey(PROVIDER_PREFIX, cid, this.owner)
      const intent = this._intentKey(provider)
      const published = new Key('/application/published/' + key)
      this._transaction(() => { this._delete(intent); this._delete(provider); this._delete(published) }, options)
    }
  }
}
