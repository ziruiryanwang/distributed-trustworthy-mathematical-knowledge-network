"""Optional caller-directed acquisition of a bounded selected semantic closure.

No research policy, solver, new checker, implicit retry, grant or contact renewal.
Structural preview is data only. Only finish() calls actual admission/import.
The exact live validated client and its owner-controlled runtime remain trusted.
"""
from contextlib import contextmanager

from aggregate_claims import bindings as B
from discovery import formal_features as F
from modules import codec as C
from transport.semantic_staging import _bounded_json
from .workspace_validated import CommonsClient


MIB = 1024**2
LIMITS = {"modules": 128, "names": 4096, "groups": 4096, "bodies": 8192,
          "steps": 65536, "data_bytes": 16*MIB}
NEED, READY = "NEED_STRUCTURAL_CONTEXT_DATA", "STRUCTURAL_CLOSURE_STAGED"


class SemanticReader:
    """One serialized, finite helper borrowing, never owning, a live client.

    The caller chooses each offered packet and which preview demands to fulfill.
    Exact name/body requests default to the original selection policy. The
    caller may choose another already authorized supplier explicitly, within
    this same grant. No implicit fallback, retry or contact renewal is made.
    """
    def __init__(self, client, origin_candidate, *, limits, definition_mode="eager"):
        F.need(type(client) is CommonsClient, "SEMANTIC_READER_EXACT_VALIDATED_CLIENT")
        F.need(type(definition_mode) is str and definition_mode in ("eager", "interface-only"),
               "SEMANTIC_READER_DEFINITION_MODE")
        self._definition_mode = self._origin_definition_mode = definition_mode
        F.fields(limits, LIMITS)
        for key, cap in LIMITS.items():
            F.uint(limits[key], 1, cap, "SEMANTIC_READER_LIMIT:"+key)
        self._client, self._grant = client, client.grant
        self._limits = dict(limits)
        F.need(limits["modules"] <= self._grant._limits["imports"]["max_members"]
               and limits["data_bytes"] <= self._grant._limits["imports"]["data_bytes"],
               "SEMANTIC_READER_ORIGINAL_IMPORT_LIMITS")
        self._state, self._busy = "COLLECTING", False
        self._steps = self._bytes = self._revision = 0
        self._names, self._by_token, self._selected = {}, {}, {}
        self._supplier_names = {}
        self._members = {}
        self._groups, self._bodies, self._pending = {}, {}, {}
        self._ready_revision = None
        self._origin = origin_candidate
        self._active()
        origin = client.describe_candidate(origin_candidate)
        self._origin_provider = origin["provider"]
        self._remember(origin_candidate, origin)
        self._active()

    def _active(self):
        F.need(type(self._client) is CommonsClient and self._client.grant is self._grant,
               "SEMANTIC_READER_CLIENT_OR_GRANT_CHANGED")
        F.need(self._definition_mode == self._origin_definition_mode,
               "SEMANTIC_READER_DEFINITION_MODE_CHANGED")
        self._client._active()

    @contextmanager
    def _call(self):
        F.need(not self._busy, "SEMANTIC_READER_SERIALIZED_CALLS")
        F.need(self._state == "COLLECTING", "SEMANTIC_READER_TRANSITION_CONSUMED")
        self._busy = True
        try:
            self._active()
            F.need(self._steps < self._limits["steps"], "SEMANTIC_READER_STEP_LIMIT")
            self._steps += 1
            yield
            self._active()
        except BaseException:
            self._state = "FAILED"
            raise
        finally:
            self._busy = False

    def _encode(self, value):
        _bounded_json(value, self._limits["data_bytes"])
        raw = C.canonical(value)
        F.need(len(raw) <= self._limits["data_bytes"], "SEMANTIC_READER_VALUE_BYTES")
        return raw

    def _retain(self, raw):
        F.need(self._bytes+len(raw)+sum(len(item) for item in self._pending)
               <= self._limits["data_bytes"],
               "SEMANTIC_READER_RETAINED_BYTES")
        self._bytes += len(raw)

    @staticmethod
    def _address(description):
        locator = description["locator"]
        return C.digest_string(locator["module_id"]), C.name_key(locator["relative_name"])

    def _remember(self, candidate, description):
        key, raw = self._address(description), self._encode(description)
        supplier_key = description["provider"], *key
        F.need(supplier_key not in self._supplier_names and candidate not in self._by_token,
               "SEMANTIC_READER_CANDIDATE_CONFLICT")
        # The original name cap also bounds all retained supplier variants;
        # no unmetered Cartesian product of contacts and mathematical names.
        F.need(len(self._supplier_names) < self._limits["names"], "SEMANTIC_READER_NAME_LIMIT")
        if key in self._names:
            first = C.parse_json(self._names[key][1])
            F.need(all(first[field] == description[field]
                       for field in ("locator", "opening", "descriptor")),
                   "SEMANTIC_READER_SUPPLIER_CONTENT_CONFLICT")
        self._retain(raw)
        self._names.setdefault(key, (candidate, raw))
        self._supplier_names[supplier_key] = candidate, raw
        self._by_token[candidate] = supplier_key
        return key

    def _description(self, candidate):
        F.need(candidate in self._by_token, "SEMANTIC_READER_FOREIGN_CANDIDATE")
        key = self._by_token[candidate]
        actual = self._client.describe_candidate(candidate)
        F.need(self._encode(actual) == self._supplier_names[key][1],
               "SEMANTIC_READER_CANDIDATE_CHANGED")
        return actual

    def _explicit_supplier(self, supplier):
        if supplier is not None:
            status = self._client.check_supplier(supplier)
            F.need(status == {"status": "AUTHORIZED_LIVE_CONTACT", "supplier": supplier,
                              "mathematical_acceptance": False},
                   "SEMANTIC_READER_SUPPLIER_CHECK")

    def _group(self, description):
        module, unused = self._address(description)
        F.need(module in self._members, "SEMANTIC_READER_UNSELECTED_GROUP")
        opening = description["opening"]
        C.verify_group_opening(module, opening)
        choice = C.parse_json(self._members[module][1])
        F.need(opening["summary"] == choice["summary"], "SEMANTIC_READER_GROUP_SUMMARY")
        key, raw = (module, opening["index"]), self._encode(opening)
        if key in self._groups:
            F.need(self._groups[key] == raw, "SEMANTIC_READER_GROUP_CONFLICT")
            return False
        F.need(len(self._groups) < self._limits["groups"], "SEMANTIC_READER_GROUP_LIMIT")
        self._retain(raw); self._groups[key] = raw; self._revision += 1
        return True

    def _demand(self, demand):
        F.fields(demand, {"kind", "module", "name"} |
                 ({"universes", "body_hash"} if demand.get("kind") == "NeedBody" else set()))
        F.need(demand["kind"] in ("NeedModuleEvidence", "NeedDeclaration", "NeedBody"),
               "SEMANTIC_READER_DEMAND_KIND")
        raw = self._encode(demand)
        F.need(raw in self._pending, "SEMANTIC_READER_NOT_CURRENT_DEMAND")
        return C.parse_json(raw), (demand["module"], C.name_key(demand["name"]))

    def _arrays(self):
        openings = [{"module": module, "opening": C.parse_json(raw)}
                    for (module, unused), raw in sorted(self._groups.items())]
        bodies = [{"module": module, "universes": arity, "expression": C.parse_json(raw)}
                  for (module, arity, unused), raw in sorted(self._bodies.items())]
        return openings, bodies

    def _choose_member(self, root, member):
        module, raw = member["module"], self._encode(member)
        if module in self._members:
            F.need(self._members[module][1] == raw, "SEMANTIC_READER_MEMBER_VARIANT_CONFLICT")
            return False
        F.need(len(self._members) < self._limits["modules"], "SEMANTIC_READER_MODULE_LIMIT")
        self._retain(raw); self._members[module] = root, raw; self._revision += 1
        return True

    def select_member(self, packet_module, exact_journal):
        """Choose a demanded internal member; this does NOT admit an I/A claim."""
        with self._call():
            F.need(packet_module in self._selected and type(exact_journal) is bytes
                   and len(exact_journal) == 184, "SEMANTIC_READER_MEMBER_PACKET_OR_JOURNAL")
            inventory = C.parse_json(self._selected[packet_module][2])
            member = next((item for item in inventory if bytes(item["journal"]) == exact_journal), None)
            F.need(member is not None, "SEMANTIC_READER_MEMBER_NOT_IN_PACKET")
            module = member["module"]
            F.need(module in self._members or any(row["kind"] == "NeedModuleEvidence"
                   and row["module"] == module for row in self._pending.values()),
                   "SEMANTIC_READER_UNDEMANDED_MEMBER")
            added = self._choose_member(packet_module, member)
            return {"status": "SELECTED_MEMBER" if added else "NO_PROGRESS",
                    "module": module, "journal": list(exact_journal)}

    async def stage(self, candidate, entry):
        """Select this exact caller-chosen offered packet; never choose a variant."""
        with self._call():
            F.fields(entry, {"packet_sha256", "packet_bytes"})
            entry = C.parse_json(self._encode(entry))
            C.digest_string(entry["packet_sha256"])
            F.uint(entry["packet_bytes"], 1, 32*MIB, "SEMANTIC_READER_PACKET_BYTES")
            description = self._description(candidate)
            module, name = self._address(description)
            if module in self._selected:
                choice = C.parse_json(self._selected[module][1])
                F.need(all(choice[key] == entry[key] for key in entry),
                       "SEMANTIC_READER_VARIANT_CONFLICT")
                return {"status": "NO_PROGRESS", "module": module}
            F.need(candidate is self._origin and not self._selected or
                   any(row["kind"] == "NeedModuleEvidence" and row["module"] == module
                       and C.name_key(row["name"]) == name for row in self._pending.values()),
                   "SEMANTIC_READER_UNDEMANDED_MODULE")
            F.need(len(self._selected) < min(self._limits["modules"],
                   self._grant._limits["imports"]["max_sources"]), "SEMANTIC_READER_PACKET_LIMIT")
            token = await self._client.stage_packet(candidate, dict(entry))
            snapshot = self._client.describe_staged(token)
            choice = snapshot["selection"]
            F.need(snapshot["status"] == "STAGED_UNTRUSTED_EVIDENCE"
                   and snapshot["mathematical_acceptance"] is False
                   and snapshot["admission_consumed"] is False
                   and {"provider": snapshot["provider"], **snapshot["candidate"]} == description
                   and snapshot["provider"] == description["provider"]
                   and choice["module"] == module
                   and choice["summary"] == description["opening"]["summary"]
                   and all(choice[key] == entry[key] for key in entry),
                   "SEMANTIC_READER_STAGED_BINDING")
            exact = bytes(C.uint(part, 255) for part in choice["journal"])
            parsed = B.member_journal(exact)
            F.need(parsed["module"] == module and parsed["summary"] == choice["summary"],
                   "SEMANTIC_READER_STAGED_JOURNAL")
            inventory_raw = self._encode(snapshot["members"])
            inventory = C.parse_json(inventory_raw)
            F.need(type(inventory) is list and 0 < len(inventory)
                   <= self._grant._limits["imports"]["max_members"],
                   "SEMANTIC_READER_MEMBER_INVENTORY")
            seen, root_member = set(), None
            for member in inventory:
                F.fields(member, {"module", "journal", "summary"})
                value = bytes(C.uint(part, 255) for part in member["journal"])
                decoded = B.member_journal(value)
                F.need(value not in seen and decoded["module"] == member["module"]
                       and decoded["summary"] == member["summary"],
                       "SEMANTIC_READER_MEMBER_INVENTORY_BINDING")
                seen.add(value)
                if value == exact: root_member = member
            F.need(root_member is not None, "SEMANTIC_READER_ROOT_NOT_IN_INVENTORY")
            raw = self._encode(choice); self._retain(raw)
            self._retain(inventory_raw)
            self._selected[module] = token, raw, inventory_raw
            self._revision += 1; self._choose_member(module, root_member); self._group(description)
            return {"status": "STAGED", "module": module, "selection": C.parse_json(raw),
                    "members": inventory}

    async def resolve(self, demand, *, max_bytes, supplier=None):
        """Resolve a demand at the origin or an explicitly selected contact.

        A cached P candidate does not replace a requested Q candidate. The
        latter can use the existing packet_offers/stage APIs without changing
        the former's recorded supplier or fabricating an indexed Q hit.
        """
        with self._call():
            chosen, key = self._demand(demand)
            F.uint(max_bytes, 1, 16*MIB, "SEMANTIC_READER_RESPONSE_BYTES")
            self._explicit_supplier(supplier)
            provider = self._origin_provider if supplier is None else supplier
            supplier_key = provider, *key
            fresh = supplier_key not in self._supplier_names
            if fresh:
                F.need(len(self._supplier_names) < self._limits["names"], "SEMANTIC_READER_NAME_LIMIT")
                options = {} if supplier is None else {"supplier": supplier}
                candidate = await self._client.resolve_declaration(
                    self._origin, chosen["module"], chosen["name"], max_bytes=max_bytes, **options)
                data = self._client.describe_candidate(candidate)
                F.need(self._address(data) == key and data["provider"] == provider,
                       "SEMANTIC_READER_EXACT_NAME_BINDING")
                self._remember(candidate, data)
            candidate, unused = self._supplier_names[supplier_key]
            data = self._description(candidate)
            added = self._group(data) if key[0] in self._members else False
            return {"status": "RESOLVED" if fresh or added else "NO_PROGRESS",
                    "candidate": candidate, "description": data}

    async def try_resolve(self, demand, *, max_bytes, supplier=None, attempt_timeout_ms=5000):
        """Try one exact declaration, preserving all held work on settled absence.

        No retry is chosen here. A caller may explicitly choose another already
        authorized supplier in a later step of this same original operation.
        """
        with self._call():
            chosen, key = self._demand(demand)
            F.uint(max_bytes, 1, 16*MIB, "SEMANTIC_READER_RESPONSE_BYTES")
            F.uint(attempt_timeout_ms, 1, 60000, "SEMANTIC_READER_ATTEMPT_TIMEOUT")
            self._explicit_supplier(supplier)
            provider = self._origin_provider if supplier is None else supplier
            supplier_key = provider, *key
            fresh = supplier_key not in self._supplier_names
            if fresh:
                F.need(len(self._supplier_names) < self._limits["names"], "SEMANTIC_READER_NAME_LIMIT")
                options = {} if supplier is None else {"supplier": supplier}
                response = await self._client.try_resolve_declaration(
                    self._origin, chosen["module"], chosen["name"], max_bytes=max_bytes,
                    attempt_timeout_ms=attempt_timeout_ms, **options)
                if response["status"] == "UNAVAILABLE_AT_SELECTED_SUPPLIER":
                    F.fields(response, {"schema", "status", "supplier", "reason", "request",
                                        "settlement", "global_complete", "mathematical_acceptance"})
                    F.need(response["schema"] == "DMKN_SEMANTIC_DECLARATION_ATTEMPT_V1"
                           and response["supplier"] == provider
                           and response["request"] == {"module_id": chosen["module"],
                               "relative_name": chosen["name"], "group_index": None}
                           and response["settlement"] == "FULL_REPLY_RESERVATION_CHARGED"
                           and response["global_complete"] is False
                           and response["mathematical_acceptance"] is False,
                           "SEMANTIC_READER_DECLARATION_REFUSAL_BINDING")
                    # No candidate, group, retention, revision or pending update.
                    return response
                F.need(response["status"] == "DECLARATION_CUSTODIED"
                       and response["mathematical_acceptance"] is False,
                       "SEMANTIC_READER_DECLARATION_ATTEMPT_RESULT")
                candidate = response["candidate"]
                data = self._client.describe_candidate(candidate)
                F.need(self._address(data) == key and data["provider"] == provider,
                       "SEMANTIC_READER_EXACT_NAME_BINDING")
                self._remember(candidate, data)
            candidate, unused = self._supplier_names[supplier_key]
            data = self._description(candidate)
            added = self._group(data) if key[0] in self._members else False
            return {"status": "RESOLVED" if fresh or added else "NO_PROGRESS",
                    "candidate": candidate, "description": data}

    async def fetch_body(self, demand, *, max_bytes, supplier=None):
        """Fetch a committed body, optionally from another authorized supplier.

        A held first-name descriptor fixes its identity even if only Q has the
        body. Already held bytes remain local data; NO_PROGRESS does not claim
        they were fetched from a newly chosen supplier.
        """
        with self._call():
            chosen, address = self._demand(demand)
            F.need(chosen["kind"] == "NeedBody" and address in self._names
                   and chosen["module"] in self._members,
                   "SEMANTIC_READER_BODY_NEEDS_RESOLVED_SELECTED_MODULE")
            F.uint(max_bytes, 1, 16*MIB, "SEMANTIC_READER_RESPONSE_BYTES")
            self._explicit_supplier(supplier)
            candidate, unused = self._names[address]
            data = self._description(candidate); self._group(data)
            key = chosen["module"], chosen["universes"], chosen["body_hash"]
            if key in self._bodies:
                return {"status": "NO_PROGRESS", "module": key[0], "body_hash": key[2]}
            F.need(len(self._bodies) < self._limits["bodies"], "SEMANTIC_READER_BODY_LIMIT")
            options = {} if supplier is None else {"supplier": supplier}
            response = await self._client.acquire_body(candidate, key[2], max_bytes=max_bytes, **options)
            body = response["body"]
            F.need(body["module_id"] == key[0] and body["relative_name"] == chosen["name"]
                   and body["universes"] == key[1] and body["body_hash"] == key[2]
                   and C.body_id(body["expression"], key[1]) == key[2],
                   "SEMANTIC_READER_EXACT_BODY_BINDING")
            raw = self._encode(body["expression"]); self._retain(raw)
            self._bodies[key] = raw; self._revision += 1
            return {"status": "FETCHED", "module": key[0], "body_hash": key[2]}

    async def try_fetch_body(self, demand, *, max_bytes, supplier=None, attempt_timeout_ms=5000):
        """Attempt a committed body without discarding work on settled unavailability.

        A held first-name descriptor fixes its identity even if only Q has the
        body. Already held bytes remain local data; NO_PROGRESS does not claim
        they were fetched from a newly chosen supplier.
        """
        with self._call():
            chosen, address = self._demand(demand)
            F.need(chosen["kind"] == "NeedBody" and address in self._names
                   and chosen["module"] in self._members,
                   "SEMANTIC_READER_BODY_NEEDS_RESOLVED_SELECTED_MODULE")
            F.uint(max_bytes, 1, 16*MIB, "SEMANTIC_READER_RESPONSE_BYTES")
            F.uint(attempt_timeout_ms, 1, 60000, "SEMANTIC_READER_ATTEMPT_TIMEOUT")
            self._explicit_supplier(supplier)
            candidate, unused = self._names[address]
            data = self._description(candidate)
            key = chosen["module"], chosen["universes"], chosen["body_hash"]
            if key in self._bodies:
                return {"status": "NO_PROGRESS", "module": key[0], "body_hash": key[2]}
            F.need(len(self._bodies) < self._limits["bodies"], "SEMANTIC_READER_BODY_LIMIT")
            options = {} if supplier is None else {"supplier": supplier}
            response = await self._client.try_acquire_body(candidate, key[2], max_bytes=max_bytes,
                attempt_timeout_ms=attempt_timeout_ms, **options)
            if response["status"] == "UNAVAILABLE_AT_SELECTED_SUPPLIER":
                F.fields(response, {"schema", "status", "supplier", "reason", "request",
                                    "settlement", "global_complete", "mathematical_acceptance"})
                provider = data["provider"] if supplier is None else supplier
                F.need(response["schema"] == "DMKN_SEMANTIC_BODY_ATTEMPT_V1"
                       and response["supplier"] == provider
                       and response["request"] == {"module_id": key[0], "relative_name": chosen["name"],
                           "universes": key[1], "body_hash": key[2]}
                       and response["settlement"] == "FULL_REPLY_RESERVATION_CHARGED"
                       and response["global_complete"] is False
                       and response["mathematical_acceptance"] is False,
                       "SEMANTIC_READER_BODY_REFUSAL_BINDING")
                # No _group, _retain, revision, body or pending-demand update.
                # Only the ordinary helper/facade/transport costs have advanced.
                return response
            F.need(response["status"] == "BODY_CUSTODIED", "SEMANTIC_READER_BODY_ATTEMPT_RESULT")
            body = response["body"]
            F.need(body["module_id"] == key[0] and body["relative_name"] == chosen["name"]
                   and body["universes"] == key[1] and body["body_hash"] == key[2]
                   and C.body_id(body["expression"], key[1]) == key[2],
                   "SEMANTIC_READER_EXACT_BODY_BINDING")
            self._group(data)
            raw = self._encode(body["expression"]); self._retain(raw)
            self._bodies[key] = raw; self._revision += 1
            return {"status": "FETCHED", "module": key[0], "body_hash": key[2]}

    def preview(self):
        """Return only structural demands/readiness; never an authoring context."""
        with self._call():
            F.need(self._selected, "SEMANTIC_READER_SELECT_ORIGIN_FIRST")
            openings, bodies = self._arrays()
            result = self._client.preview_context(
                [self._selected[module][0] for module in sorted(self._selected)], openings, bodies,
                selected_members=[{"token": self._selected[root][0], "module": module,
                    "journal": bytes(C.parse_json(raw)["journal"])}
                    for module, (root, raw) in sorted(self._members.items())],
                definition_mode=self._definition_mode)
            F.need(result.get("definition_mode", "eager") == self._definition_mode,
                   "SEMANTIC_READER_PREVIEW_MODE")
            F.need(result["status"] in (NEED, READY) and result["mathematical_acceptance"] is False
                   and type(result["demands"]) is list
                   and (not result["demands"]) == (result["status"] == READY),
                   "SEMANTIC_READER_PREVIEW_STATUS")
            pending = {}
            for demand in result["demands"]:
                raw = self._encode(demand)
                F.need(raw not in pending, "SEMANTIC_READER_DUPLICATE_DEMAND")
                pending[raw] = C.parse_json(raw)
            pending_bytes = sum(len(raw) for raw in pending)
            F.need(self._bytes+pending_bytes <= self._limits["data_bytes"],
                   "SEMANTIC_READER_DEMAND_BYTES")
            self._pending = pending
            self._ready_revision = self._revision if result["status"] == READY else None
            # Whitelist data; even a future preview extension cannot leak an
            # apparent usable context through this helper.
            report = {"status": result["status"], "demands": [C.parse_json(raw) for raw in pending],
                    "cost": C.parse_json(self._encode(result["cost"])),
                    "mathematical_acceptance": False}
            if self._definition_mode != "eager": report["definition_mode"] = self._definition_mode
            return report

    def finish(self, admission, *, resolutions=None):
        """Admit each packet root once, then import explicitly chosen member journals."""
        with self._call():
            F.need(self._selected and self._ready_revision == self._revision,
                   "SEMANTIC_READER_STRUCTURAL_CLOSURE_REQUIRED")
            F.need(type(admission) is dict and set(admission) == set(self._selected),
                   "SEMANTIC_READER_EXACT_ADMISSION_CHOICES")
            selected_limits = {}
            for module, limits in admission.items():
                F.fields(limits, {"native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds", "memory_mib"})
                for key in ("native_cpu_seconds", "receipt_cpu_seconds", "wall_seconds"):
                    F.uint(limits[key], 1, 600, "SEMANTIC_READER_ADMISSION_LIMIT")
                F.uint(limits["memory_mib"], 64, 4096, "SEMANTIC_READER_ADMISSION_MEMORY")
                selected_limits[module] = dict(limits)
            choices = {} if resolutions is None else resolutions
            F.need(type(choices) is dict and set(choices) <= set(self._selected),
                   "SEMANTIC_READER_RESOLUTION_ROOTS")
            copied_choices = {}
            for module, rows in choices.items():
                F.need(type(rows) is dict and len(rows) <= self._grant._limits["imports"]["max_members"],
                       "SEMANTIC_READER_RESOLUTION_MAP")
                for exact, decision in rows.items():
                    F.need(type(exact) is bytes and len(exact) == 184
                           and type(decision) is str and decision in ("existing", "incoming"),
                           "SEMANTIC_READER_RESOLUTION_CHOICE")
                    B.member_journal(exact)
                copied_choices[module] = dict(rows)
            self._state = "ADMITTING"
            warrants = []
            for module in sorted(self._selected):
                token, raw, inventory_raw = self._selected[module]
                exact = bytes(C.parse_json(raw)["journal"])
                warrant = self._client.admit_staged(
                    token, expected_exact_journal=exact, **selected_limits[module])
                self._active()
                fact = self._client.describe(warrant)
                inventory = C.parse_json(inventory_raw)
                actual = [{"module": member["module"], "journal": list(member["journal"]),
                           "summary": member["summary"]} for member in fact["members"]]
                F.need(fact["live"]["journal"] == exact and fact["live"]["module"] == module
                       and sorted(actual, key=lambda item: item["journal"])
                       == sorted(inventory, key=lambda item: item["journal"]),
                       "SEMANTIC_READER_ACTUAL_MEMBER_INVENTORY")
                warrants.append({"warrant": warrant, "resolutions": copied_choices.get(module)})
            exacts = [bytes(C.parse_json(raw)["journal"]) for unused_root, raw
                      in (self._members[module] for module in sorted(self._members))]
            openings, bodies = self._arrays()
            result = self._client.import_context(warrants, exacts, openings, bodies,
                                                  definition_mode=self._definition_mode)
            complete = result["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY"
            F.need(complete or result["status"] == "NEED_AUTHORING_CONTEXT_DATA",
                   "SEMANTIC_READER_IMPORT_STATUS")
            self._state = "READY" if complete else "INCOMPLETE"
            return {"status": "READY" if complete else "NEED_SEMANTICS",
                    "context": result["context"] if complete else None,
                    "demands": result.get("demands", []), "cost": result["cost"],
                    "mathematical_acceptance": False}

    def report(self):
        """Inert accounting only; a report is not live mathematical authority."""
        return {"state": self._state, "steps": self._steps, "modules": len(self._members),
                "packets": len(self._selected),
                "names": len(self._names), "supplier_candidates": len(self._supplier_names),
                "groups": len(self._groups), "bodies": len(self._bodies),
                "data_bytes": self._bytes+sum(len(raw) for raw in self._pending),
                "revision": self._revision, "mathematical_acceptance": False}

    def close(self):
        """Discard this helper only; the caller still owns and must close the client."""
        F.need(not self._busy, "SEMANTIC_READER_SERIALIZED_CLOSE")
        self._state = "CLOSED"
        self._names.clear(); self._by_token.clear(); self._selected.clear()
        self._supplier_names.clear()
        self._members.clear()
        self._groups.clear(); self._bodies.clear(); self._pending.clear()
        self._bytes = 0
