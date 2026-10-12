"""Explicit exact warrants over shared semantic declarations; no new authority."""
import hashlib
import time

from admission.bindings import journal
from modules import codec as C
from delta.packet import SCHEMA, MIB, Envelope, need, parse_packet
from .receiver import DeltaVerifier, VerifiedDelta
from .claims import bind_members, expected_journal


def _sha(raw): return hashlib.sha256(raw).hexdigest()


def _inventory(items):
    return C.canonical([{**item,"journal":list(item["journal"])}
        for item in sorted(items,key=lambda item:item["journal"])])


class DeltaImportSession:
    """One owner; immutable explicit J selection per M for NEW direct imports.

    Each J has one chosen complete admitted derivation; conflicts require an
    explicit existing/incoming choice. Original witness parents never change.
    Semantic groups/bodies deduplicate by M, not rank. Saved copies give no authority.
    """
    def __init__(self, verifier, *, max_handles=8, max_members=256, max_calls=4096,
                 packet_bytes=128*MIB, data_bytes=16*MIB, wall_seconds=3600):
        need(type(verifier) is DeltaVerifier,"CLAIM_IMPORT_EXACT_VERIFIER")
        verifier._active()
        for value,cap in ((max_handles,8),(max_members,1024),(max_calls,65536),
                          (packet_bytes,256*MIB),(data_bytes,16*MIB),(wall_seconds,86400)):
            need(type(value) is int and 0 < value <= cap,"CLAIM_IMPORT_LIMIT")
        self._verifier = self._origin = verifier
        self._profile = verifier.report()["profile_id"]
        self._deadline = min(time.monotonic()+wall_seconds,verifier._deadline)
        self._caps = max_handles,max_members,max_calls,packet_bytes,data_bytes
        self._closed = False
        self._calls = self._packet_bytes = self._data_bytes = 0
        self._representation_revision = 0
        self._handles,self._nodes,self._summaries,self._selected = {},{},{},{}
        self._groups,self._bodies = {},{}
        self._active()

    def _active(self):
        need(not self._closed and self._verifier is self._origin
             and time.monotonic() < self._deadline,"CLAIM_IMPORT_CLOSED_OR_CHANGED_OR_EXPIRED")
        self._verifier._active()
        need(self._verifier.report()["profile_id"] == self._profile,"CLAIM_IMPORT_PROFILE_CHANGED")

    def _begin(self):
        self._active(); need(self._calls < self._caps[2],"CLAIM_IMPORT_CALL_LIMIT")
        self._calls += 1

    def _live(self):
        self._active()
        for digest,(handle,raw,inventory) in self._handles.items():
            live = self._verifier.describe(handle)
            need(live["profile_id"] == self._profile and live["packet_sha256"] == digest
                 and _sha(raw) == digest,"CLAIM_IMPORT_HANDLE_BINDING")
            need(_inventory(self._verifier.members(handle)) == inventory,"CLAIM_IMPORT_INVENTORY_CHANGED")
        self._active()

    def use_handle(self, handle, *, resolutions=None):
        """Register exact closure; resolve EVERY conflict to an established record.

        resolutions is {exact_J: "existing" | "incoming"}. No implicit choice,
        arbitrary payload, edge union or unused directive is accepted. All input
        bytes/calls charge before validation; state commits after final liveness.
        """
        self._begin(); need(type(handle) is VerifiedDelta,"CLAIM_IMPORT_EXACT_HANDLE")
        live = self._verifier.describe(handle); raw = self._verifier.export_packet(handle)
        digest = _sha(raw)
        self._packet_bytes += len(raw)
        need(self._packet_bytes <= self._caps[3],"CLAIM_IMPORT_SUBMITTED_PACKET_ALLOWANCE")
        need(live["profile_id"] == self._profile and live["packet_sha256"] == digest,
             "CLAIM_IMPORT_PACKET_BINDING")
        members = self._verifier.members(handle); inventory = _inventory(members)
        if digest in self._handles:
            previous = self._handles[digest]
            need(previous[1] == raw and previous[2] == inventory,"CLAIM_IMPORT_PACKET_CONFLICT")
        else:
            need(len(self._handles) < self._caps[0],"CLAIM_IMPORT_HANDLE_STORAGE")
        pending = bind_members(raw,members,envelope=self._verifier._envelope,
            image=self._verifier._image,profile=self._profile,packet_digest=digest)
        need(len(set(self._nodes)|set(pending)) <= self._caps[1],"CLAIM_IMPORT_WARRANT_STORAGE")
        summaries = dict(self._summaries); conflicts = set()
        for exact,node in pending.items():
            parsed = journal(exact); summary = C.canonical(parsed["summary"]); module = parsed["module"]
            need(module not in summaries or summaries[module] == summary,"CLAIM_IMPORT_SEMANTIC_CONFLICT")
            summaries[module] = summary
            if exact in self._nodes and self._nodes[exact][:4] != node[:4]: conflicts.add(exact)
        choices = {} if resolutions is None else resolutions
        need(type(choices) is dict and len(choices) <= self._caps[1],
             "EXACT_DERIVATION_RESOLUTION_MAP","REPRESENTATION_CONFLICT")
        choices = dict(choices)
        need(all(type(exact) is bytes and len(exact) == 184
                 and type(choice) is str and choice in ("existing","incoming")
                 for exact,choice in choices.items()),
             "EXACT_DERIVATION_RESOLUTION_DIRECTIVE","REPRESENTATION_CONFLICT")
        need(set(choices) == conflicts,"MISSING_OR_UNUSED_EXACT_DERIVATION_RESOLUTIONS",
             "REPRESENTATION_CONFLICT")
        next_nodes = dict(self._nodes); changed = False
        for exact,node in pending.items():
            if exact not in next_nodes:
                next_nodes[exact] = node
            elif exact in conflicts and choices[exact] == "incoming":
                next_nodes[exact] = node; changed = True
        available = set(next_nodes)
        need(all(set(node[3]) <= available for node in next_nodes.values()),
             "CHOSEN_DERIVATION_EXACT_ANCESTRY")
        next_handles = dict(self._handles)
        next_handles.setdefault(digest,(handle,raw,inventory))
        revision = self._representation_revision + int(changed)
        self._live()
        need(_inventory(self._verifier.members(handle)) == inventory,"CLAIM_IMPORT_FINAL_INVENTORY")
        self._active()
        # All fallible work is complete. In this single-owner controller, commit
        # selected whole records together; do not run a post-mutation live check.
        self._handles,self._nodes,self._summaries,self._representation_revision = (
            next_handles,next_nodes,summaries,revision)
        return live["journal"]

    def variants(self, module):
        """Enumerate established exact claims; does not choose one."""
        self._begin(); self._live(); C.digest_string(module)
        return [{"module":module,"journal":exact,"proof_form":node[1],
                 "evidence_sha256":_sha(node[2]),"packet_sha256":node[4]}
                for exact,node in sorted(self._nodes.items()) if journal(exact)["module"] == module]

    def select_warrant(self, exact_journal):
        self._begin(); self._live(); parsed = journal(exact_journal)
        need(exact_journal in self._nodes,"CLAIM_IMPORT_UNESTABLISHED_EXACT_J")
        module = parsed["module"]; previous = self._selected.get(module)
        need(previous is None or previous == exact_journal,
             "DIRECT_WARRANT_SELECTION_IMMUTABLE","SELECTION_CONFLICT")
        self._selected[module] = exact_journal
        self._active(); return module

    def open_group(self, module, opening):
        self._begin(); self._live(); C.digest_string(module)
        need(module in self._selected,"EXPLICIT_DIRECT_WARRANT_SELECTION_REQUIRED","NEEDS_SELECTION")
        exact = self._selected[module]; node = self._nodes[exact]
        handle = self._handles[node[4]][0]
        group = self._verifier.open_member_group(handle,exact,opening)
        raw = C.canonical(opening); key = module,opening["index"]
        old = self._groups.get(key)
        need(old is None or old == raw,"CLAIM_IMPORT_OPENING_CHANGED")
        if old is None:
            need(len(self._groups) < C.DEFAULT_LIMITS.max_groups
                 and self._data_bytes+len(raw) <= self._caps[4],"CLAIM_IMPORT_OPENING_STORAGE")
            self._active(); self._groups[key] = raw; self._data_bytes += len(raw)
        self._active(); return group

    def supply_body(self, module, universes, expression):
        self._begin(); self._live()
        need(module in self._selected,"EXPLICIT_DIRECT_WARRANT_SELECTION_REQUIRED","NEEDS_SELECTION")
        digest = C.body_id(expression,universes); allowed = False
        for (owner,unused),raw in self._groups.items():
            if owner != module: continue
            for descriptor in C.parse_json(raw)["group"]["declarations"]:
                if descriptor["universes"] != universes: continue
                if descriptor["kind"] in ("definition","opaque"):
                    allowed |= descriptor["value_hash"] == digest
                elif descriptor["kind"] == "recursor":
                    allowed |= any(rule["value_hash"] == digest for rule in descriptor["meta"]["rules"])
        need(allowed,"CLAIM_IMPORT_BODY_NOT_COMMITTED")
        raw = C.canonical(expression); key = module,universes,digest; old = self._bodies.get(key)
        need(old is None or old == raw,"CLAIM_IMPORT_BODY_CHANGED")
        if old is None:
            need(self._data_bytes+len(raw) <= self._caps[4],"CLAIM_IMPORT_BODY_STORAGE")
            self._active(); self._bodies[key] = raw; self._data_bytes += len(raw)
        self._active(); return digest

    def selected_data(self):
        """One semantic item per M; explicit exact J accompanies each direct parent."""
        self._begin(); self._live(); items = []
        for module in sorted({key[0] for key in self._groups}):
            need(module in self._selected,"CLAIM_IMPORT_MISSING_EXPLICIT_SELECTION")
            exact = self._selected[module]; node = self._nodes[exact]; summary = journal(exact)["summary"]
            openings = [C.parse_json(raw) for (owner,index),raw in sorted(self._groups.items()) if owner == module]
            for opening in openings:
                self._verifier.open_member_group(self._handles[node[4]][0],exact,opening)
                need(opening["summary"] == summary,"CLAIM_IMPORT_EXACT_SUMMARY")
            bodies = [{"universes":arity,"digest":body,"expression":C.parse_json(raw)}
                for (owner,arity,body),raw in sorted(self._bodies.items()) if owner == module]
            items.append({"module":module,"journal":exact,"summary":summary,"proof_form":node[1],
                "packet_sha256":node[4],"openings":openings,"bodies":bodies})
        self._active(); return items

    def selection(self):
        items = self.selected_data()
        public = {"profile":self._profile,"packets":sorted(self._handles),
            "representation_revision":self._representation_revision,
            "chosen_derivations":[{"journal":list(exact),"proof_form":node[1],
                "evidence_sha256":_sha(node[2]),"parents":[list(parent) for parent in node[3]],
                "packet_sha256":node[4]} for exact,node in sorted(self._nodes.items())],
            "warrant_selection":[[module,list(exact)] for module,exact in sorted(self._selected.items())],
            "selected":[{**item,"journal":list(item["journal"])} for item in items]}
        return items,C.hash_value("delta-exact-warrant-authoring-selection-v1",public)

    def require_selection(self, binding):
        C.digest_string(binding); unused,actual = self.selection()
        need(actual == binding,"CLAIM_IMPORT_SELECTION_CHANGED")

    def census(self):
        self._active()
        return {"retained_warrants":len(self._nodes),"unique_semantic_modules":len(self._summaries),
            "selected_direct_warrants":len(self._selected),"semantic_openings":len(self._groups),
            "retained_packets":len(self._handles),"representation_revision":self._representation_revision,
            "submitted_packet_bytes":self._packet_bytes,"calls":self._calls,
            "counts_are_not_useful_growth":True}

    def onward_packet(self, witness, binding, envelope):
        """Preserve the exact complete selected derivations; never substitute Js."""
        self.require_selection(binding); need(type(envelope) is Envelope,"CLAIM_AUTHORING_ENVELOPE")
        envelope.validate(); items,actual = self.selection(); need(actual == binding,"CLAIM_AUTHORING_SELECTION")
        selected_parents = [{"journal":list(item["journal"]),"openings":item["openings"]} for item in items]
        need(witness["parents"] == selected_parents,"NEW_WITNESS_EXACT_SELECTED_PARENTS")
        parent_journals = [item["journal"] for item in items]
        parent_modules = [journal(raw)["module"] for raw in parent_journals]
        child = C.module_id(witness["local_spec"])
        need(len(parent_modules) == len(set(parent_modules)) and child not in parent_modules,
             "UNCHANGED_SINGLE_WITNESS_DIRECT_MODULE_CONSTRAINT")
        rank = max((journal(raw)["rank"] for raw in parent_journals),default=-1)+1
        need(witness["rank"] == rank,"NEW_WITNESS_EXACT_SELECTED_RANK")
        target = expected_journal(C.summarize(witness["local_spec"]),rank,self._verifier._image)
        included,pending = set(),list(parent_journals)
        while pending:
            exact = pending.pop()
            if exact in included: continue
            need(exact in self._nodes,"CLAIM_AUTHORING_MISSING_EXACT_ANCESTOR")
            included.add(exact); pending.extend(self._nodes[exact][3])
        need(target not in included,"CLAIM_AUTHORING_DUPLICATE_TARGET_J")
        frontiers,deltas = [],[]
        for exact in sorted(included,key=lambda raw:(journal(raw)["rank"],raw)):
            node = self._nodes[exact]
            if node[1] == "receipt-frontier":
                frontiers.append({"receipt_hex":node[2].hex(),"summary":journal(exact)["summary"]})
            else:
                deltas.append(C.parse_json(node[2]))
        deltas.append(witness)
        raw = C.canonical({"schema":SCHEMA,"frontiers":frontiers,"deltas":deltas})
        unused_receipts,unused_witnesses,census = parse_packet(raw,envelope)
        self.require_selection(binding); return raw,census

    def close(self):
        self._closed = True
        for store in (self._handles,self._nodes,self._summaries,self._selected,self._groups,self._bodies): store.clear()
