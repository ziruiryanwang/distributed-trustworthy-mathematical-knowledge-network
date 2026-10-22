/** New v5 logical keys over the retained adopted quota-store primitive. */
import { canonical, hexid, need, peerId, validateIntentSpec } from './protocol.mjs'

import { DatabaseSync } from 'node:sqlite'
import { lstatSync, realpathSync, opendirSync } from 'node:fs'
import { isAbsolute, resolve, dirname, basename, join } from 'node:path'

const fail = code => { throw new Error(code) }

// The selected public entry allocates a fresh state directory for every run.
// Existing metadata, including a same-profile hot journal, is never reopened.
function freshMetadata (path) {
  need(typeof path === 'string' && isAbsolute(path) && resolve(path) === path &&
    basename(path) === 'metadata.sqlite', 'LOCATION_METADATA_PATH')
  const state = dirname(path)
  for (let check = state; ; check = dirname(check)) {
    const stat = lstatSync(check)
    need(stat.isDirectory() && !stat.isSymbolicLink() && realpathSync(check) === check,
      'LOCATION_METADATA_ORDINARY_ANCESTOR')
    if (dirname(check) === check) break
  }
  const expected = new Set(['identity.key', 'adopted.json'])
  const seen = new Set()
  const directory = opendirSync(state)
  try {
    for (let entry = directory.readSync(); entry != null; entry = directory.readSync()) {
      need(seen.size < 2 && expected.has(entry.name) && !seen.has(entry.name),
        'LOCATION_METADATA_STATE_ENTRIES')
      const file = join(state, entry.name); const stat = lstatSync(file)
      need(stat.isFile() && !stat.isSymbolicLink() && stat.nlink === 1 &&
        realpathSync(file) === file && stat.size > 0 && stat.size <= 1024,
      'LOCATION_METADATA_STATE_FILE')
      seen.add(entry.name)
    }
  } finally { directory.closeSync() }
  need(seen.size === 2, 'LOCATION_METADATA_STATE_INCOMPLETE')
  for (const suffix of ['', '-journal', '-wal', '-shm']) {
    try { lstatSync(path + suffix); fail('LOCATION_METADATA_FRESH_REQUIRED') } catch (error) {
      if (error.code !== 'ENOENT') throw error
    }
  }
}

function configureFreshDatabase (db, pages) {
  // Runtime/default-VFS/source correspondence is an explicit owner premise.
  // These readbacks do not adopt a whole manager/generation storage envelope.
  need(Number.isSafeInteger(pages) && pages >= 256 && pages <= 65536, 'STORE_PAGE_LIMIT')
  need(db.prepare('PRAGMA page_count').get().page_count === 0, 'STORE_FRESH_DATABASE')
  need(db.prepare('PRAGMA compile_options').all().some(row => row.compile_options === 'TEMP_STORE=1'),
    'STORE_TEMP_BUILD')
  db.exec('PRAGMA page_size=4096; PRAGMA auto_vacuum=NONE; PRAGMA journal_mode=DELETE; PRAGMA synchronous=FULL; PRAGMA temp_store=MEMORY; PRAGMA cache_spill=ON;')
  need(db.prepare(`PRAGMA max_page_count=${pages}`).get().max_page_count === pages, 'STORE_DISK_CAP')
  for (const [name, expected] of [['page_size', 4096], ['auto_vacuum', 0], ['journal_mode', 'delete'],
    ['synchronous', 2], ['temp_store', 2], ['max_page_count', pages]]) {
    need(db.prepare('PRAGMA ' + name).get()[name] === expected, 'STORE_MANAGED_PROFILE:' + name)
  }
  need(db.prepare('PRAGMA cache_spill').get().cache_spill > 0, 'STORE_CACHE_SPILL')
}

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
    async _openFreshProfile () {
      if (this.db != null) fail('STORE_ALREADY_OPEN')
      freshMetadata(this.path)
      const db = new DatabaseSync(this.path)
      try {
        configureFreshDatabase(db, this.limits.pages)
        db.exec('PRAGMA page_size=4096; PRAGMA journal_mode=DELETE; PRAGMA synchronous=FULL; PRAGMA busy_timeout=250; PRAGMA locking_mode=EXCLUSIVE;')
        if (db.prepare('PRAGMA page_size').get().page_size !== 4096) fail('STORE_PAGE_SIZE')
        const cap = db.prepare(`PRAGMA max_page_count=${this.limits.pages}`).get().max_page_count
        if (cap !== this.limits.pages) fail('STORE_DISK_CAP')
        db.exec('BEGIN EXCLUSIVE')
        db.exec('CREATE TABLE IF NOT EXISTS config (id INTEGER PRIMARY KEY CHECK(id=1), schema TEXT NOT NULL, limits TEXT NOT NULL); CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v BLOB NOT NULL, sz INTEGER NOT NULL, provider_group TEXT NOT NULL); CREATE INDEX IF NOT EXISTS provider_groups ON kv(provider_group); CREATE TABLE IF NOT EXISTS totals (id INTEGER PRIMARY KEY CHECK(id=1), entries INTEGER NOT NULL, bytes INTEGER NOT NULL);')
        const config = db.prepare('SELECT schema,limits FROM config WHERE id=1').get()
        const adopted = JSON.stringify(this.limits)
        if (config == null) {
          if (db.prepare('SELECT COUNT(*) AS n FROM kv').get().n !== 0) fail('STORE_UNADOPTED_ROWS')
          db.prepare('INSERT INTO config VALUES(1,?,?)').run('DMKN_QUOTA_STORE_V1', adopted)
          db.prepare('INSERT INTO totals VALUES(1,0,0)').run()
        } else if (config.schema !== 'DMKN_QUOTA_STORE_V1' || config.limits !== adopted) fail('STORE_POLICY_CHANGED')
        const totals = db.prepare('SELECT entries,bytes FROM totals WHERE id=1').get()
        const actual = db.prepare('SELECT COUNT(*) AS entries, COALESCE(SUM(sz),0) AS bytes FROM kv').get()
        if (totals == null || totals.entries !== actual.entries || totals.bytes !== actual.bytes || actual.entries > this.limits.entries || actual.bytes > this.limits.bytes) fail('STORE_COUNTERS_OR_CAP')
        let visited = 0
        for (const row of db.prepare('SELECT k,v,sz,provider_group FROM kv').iterate()) {
          if (++visited > this.limits.entries) fail('STORE_CENSUS_BOUND')
          const selected = this._value(row.k, row.v)
          if (row.sz !== selected.weight || row.provider_group !== selected.group) fail('STORE_ROW_BINDING')
        }
        const groups = db.prepare("SELECT provider_group,COUNT(*) AS n FROM kv WHERE provider_group <> '' GROUP BY provider_group").all()
        if (groups.some(group => group.n > this.limits.providersPerKey)) fail('STORE_PROVIDER_CAP')
        db.exec('COMMIT')
        this.db = db
      } catch (error) {
        try { db.exec('ROLLBACK') } catch {}
        db.close()
        throw error
      }
    }
    async open () {
      await this._openFreshProfile()
      try {
        for (const row of this.db.prepare("SELECT k FROM kv WHERE k LIKE '/dmknv5/provider/%'").iterate()) {
          if (row.k.endsWith('/' + this.ownerId)) need(this.db.prepare('SELECT 1 AS present FROM kv WHERE k=?').get(this._intentKey(row.k)) != null, 'LOCATION_ORPHAN_SELF_HINT')
        }
      } catch (error) { await this.close(); throw error }
    }
    async enableIntent (cid, key, spec, options) {
      bindCID(cid, key)
      validateIntentSpec(spec, key)
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

