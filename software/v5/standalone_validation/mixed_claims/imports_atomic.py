"""Closed typed mixed imports, chosen whole-J derivations and semantic reuse.

No new checker. Direct A-member import requires no I/native owner. An immutable
relation basis is DATA, not a verifier or admission credential. Owner-controlled
installation/Python and bounded serialized-input processing remain trusted.
"""
from dataclasses import dataclass
from copy import deepcopy
from authoring.context import DEFAULT_LIMITS, SCHEMA as CONTEXT_SCHEMA, _foundation as _decode_foundation
import hashlib
from pathlib import Path
import sys
import time

from admission.verifier import ReceiptVerifier, VerifiedModule
from admission.bindings import journal
from admission import pin_phase as PP
from aggregate_claims.aggregate_admission import AggregateReceiptVerifier, VerifiedAggregateMember
from aggregate_claims import bindings as B
from modules import codec as C
from delta_claims.claims import expected_journal
from .receiver import MixedDeltaVerifier, VerifiedMixedDelta
from . import packet as P

need,MIB = P.need,P.MIB


def _sha(raw): return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class RelationBasis:
    """Fixed mathematical identifiers ONLY; no methods/handles/trust authority."""
    image: str = B.RELATION_IMAGE
    foundation: str = B.FOUNDATION
    policy: str = B.POLICY


def _encoded_fact(fact):
    result = dict(fact)
    for key in ("journal","aggregate_header","header"):
        if key in result: result[key] = list(result[key])
    if "siblings" in result: result["siblings"] = [list(part) for part in result["siblings"]]
    return result


def _receipt_key(tag,statement,receipt): return tag,statement,_sha(receipt),len(receipt)


class SealedSelection:
    """Opaque same-session token. Its public shape contains no transferable authority."""
    __slots__ = ()


class MixedImportSession:
    """One finite owner lifetime; explicit conflicts, atomic complete-record merge.

    Original configured owners remain live even if some chosen ancestry is cut.
    Fresh downstream use depends only on serialized chosen closure, not on these
    sender-local handles. Calls/bytes remain charged when a new import refuses.
    """
    def __init__(self,*,legacy_verifier=None,aggregate_verifier=None,delta_verifier=None,
                 max_sources=64,max_members=1024,max_receipts=128,max_calls=4096,
                 submitted_bytes=256*MIB,data_bytes=16*MIB,wall_seconds=3600):
        owners = legacy_verifier,aggregate_verifier,delta_verifier
        classes = ReceiptVerifier,AggregateReceiptVerifier,MixedDeltaVerifier
        need(any(owner is not None for owner in owners),"MIXED_IMPORT_OWNER_REQUIRED")
        need(all(owner is None or type(owner) is cls for owner,cls in zip(owners,classes)),
             "MIXED_IMPORT_EXACT_OWNERS")
        values = max_sources,max_members,max_receipts,max_calls,submitted_bytes,data_bytes
        ceilings = 128,1024,128,65536,256*MIB,16*MIB
        need(all(type(value) is int and 0 < value <= cap for value,cap in zip(values,ceilings))
             and type(wall_seconds) is int and 0 < wall_seconds <= 86400,"MIXED_IMPORT_LIMIT")
        self._owners = self._origins = owners
        self._basis = RelationBasis()
        self._profiles = tuple(None if owner is None else owner.report()["profile_id"] for owner in owners)
        self._aggregate_image = (aggregate_verifier._image if aggregate_verifier is not None else
            delta_verifier._aggregate_image if delta_verifier is not None else None)
        self._origin_aggregate_image = self._aggregate_image
        if aggregate_verifier is not None and delta_verifier is not None and delta_verifier._aggregate_image is not None:
            need(aggregate_verifier._image == delta_verifier._aggregate_image,"MIXED_IMPORT_A_PROFILE_CONFLICT")
        self._deadline = min(time.monotonic()+wall_seconds,*[owner._deadline for owner in owners if owner is not None])
        self._caps,self._closed = values,False
        self._calls = self._submitted_bytes = self._data_bytes = self._representation_revision = 0
        self._sources,self._receipts,self._nodes,self._summaries,self._selected = {},{},{},{},{}
        self._groups,self._bodies = {},{}
        self._sealed = self._batching = False
        self._view = self._view_payload = self._sealed_state = None
        self._definition_mode = "eager"
        self._origin_definition_mode = None
        root = Path(__file__).resolve().parents[1]
        # Pure A-only use still eagerly loads the mixed receiver's source graph.
        # These are source pins, not a demand for any I/native process to exist.
        names = ("mixed_claims","mixed_claims.packet","mixed_claims.receiver","mixed_claims.imports_atomic",
            "admission","admission.verifier","admission.bindings","admission.pin_phase","aggregate_claims",
            "aggregate_claims.aggregate_admission","aggregate_claims.admission_binding","aggregate_claims.bindings",
            "authoring","authoring.context","authoring.imports","modules","modules.codec",
            "modules.model","modules.source_rows","delta","delta.packet","delta.receiver",
            "delta_claims","delta_claims.receiver","delta_claims.claims","production","production.producer")
        self._required_origins = {name:root/(name.replace(".","/")+("/__init__.py" if "." not in name else ".py"))
                                  for name in names}
        available = {path for owner in owners if owner is not None for path in owner._pins}
        need(set(self._required_origins.values()) <= available,"MIXED_IMPORT_REQUIRED_SOURCE_PINS")
        self._profile = C.hash_value("mixed-import-session-v1",{"owners":list(self._profiles),
            "relation_image":self._basis.image,"foundation":self._basis.foundation,"policy":self._basis.policy,
            "aggregate_image":self._aggregate_image,"limits":list(values)})
        self._origin_profile = self._profile
        self._live()

    def _active(self):
        try:
            need((self._origin_definition_mode is None and self._definition_mode == "eager")
                 or (type(self._origin_definition_mode) is str
                     and self._origin_definition_mode in ("eager", "interface-only")
                     and self._definition_mode == self._origin_definition_mode),
                 "MIXED_IMPORT_DEFINITION_MODE_CHANGED")
            need(not self._closed and self._basis == RelationBasis() and self._profile == self._origin_profile
                 and self._aggregate_image == self._origin_aggregate_image
                 and all(a is b for a,b in zip(self._owners,self._origins)) and len(self._owners) == 3
                 and time.monotonic() < self._deadline,"MIXED_IMPORT_CLOSED_CHANGED_OR_EXPIRED")
            for index,(owner,cls) in enumerate(zip(self._owners,(ReceiptVerifier,AggregateReceiptVerifier,MixedDeltaVerifier))):
                if owner is None: continue
                need(type(owner) is cls,"MIXED_IMPORT_OWNER_TYPE_CHANGED"); owner._active()
                need(owner.report()["profile_id"] == self._profiles[index],"MIXED_IMPORT_OWNER_PROFILE_CHANGED")
                need((owner._foundation,owner._policy) == (self._basis.foundation,self._basis.policy)
                     and owner._image == (self._aggregate_image if index == 1 else self._basis.image),
                     "MIXED_IMPORT_RELATION_BASIS_CHANGED")
        except BaseException:
            self.close(); raise

    def _begin(self):
        self._active(); need(self._calls < self._caps[3],"MIXED_IMPORT_CALL_LIMIT")
        self._calls += 1

    def _charge(self,raw):
        need(type(raw) is bytes,"MIXED_IMPORT_IMMUTABLE_BYTES")
        self._submitted_bytes += len(raw)
        need(self._submitted_bytes <= self._caps[4],"MIXED_IMPORT_SUBMITTED_BYTE_LIMIT")

    def _snapshot(self,kind,handle,raw):
        owner = self._owners[kind]
        need(owner is not None,"MIXED_IMPORT_MISSING_OWNER","UNSUPPORTED_PROOF_FORM")
        need(type(handle) is (VerifiedModule,VerifiedAggregateMember,VerifiedMixedDelta)[kind],
             "MIXED_IMPORT_EXACT_HANDLE")
        if kind == 2:
            live = owner.describe(handle); members = owner.members(handle)
            need(owner.export_packet(handle) == raw and live["packet_sha256"] == _sha(raw),
                 "MIXED_IMPORT_PACKET_BINDING")
            encoded = {"kind":kind,"live":_encoded_fact(live),
                "members":[_encoded_fact(item) for item in sorted(members,key=lambda item:item["journal"])]}
        else:
            live = owner.describe(handle) if kind == 0 else owner.describe_member(handle)
            need(live["receipt_sha256"] == _sha(raw) and 0 < len(raw) <= 64*MIB,"MIXED_IMPORT_RECEIPT_BINDING")
            if kind == 1:
                need(live["receipt_bytes"] == len(raw) and live["aggregate_image"] == self._aggregate_image,
                     "MIXED_IMPORT_A_RECEIPT_BINDING")
            members = [live]; encoded = {"kind":kind,"live":_encoded_fact(live)}
        need(live["profile_id"] == self._profiles[kind],"MIXED_IMPORT_LIVE_SOURCE_PROFILE")
        for item in members:
            parsed = B.member_journal(item["journal"])
            need(parsed["module"] == item["module"] and parsed["summary"] == item["summary"]
                 and item["profile_id"] == self._profiles[kind],"MIXED_IMPORT_EXACT_SOURCE_MEMBER")
        return C.canonical(encoded),live,members

    def _live(self):
        original_mixed = None
        phase_body_complete = False
        try:
            # This call graph is synchronous owner validation only: no native
            # invocation, await, network operation, or external/user callback.
            # Only the original configured mixed owner may borrow this scope.
            # _active still refuses any changed current owner before body use.
            original_mixed = self._origins[2]
            borrowers = () if original_mixed is None else (original_mixed,)
            with PP.phase(self._active, borrowers=borrowers):
                self._live_phase()
                phase_body_complete = True
        except BaseException:
            # A borrowed _check may already have returned when this outer
            # pin/trust/origin finalization fails. Revoke the captured original,
            # never a substituted current owner or independently owned I/A.
            if phase_body_complete and type(original_mixed) is MixedDeltaVerifier:
                original_mixed._revoke()
            self.close(); raise

    def _live_phase(self):
        try:
            self._active()
            for name,path in self._required_origins.items():
                module = sys.modules.get(name)
                need(module is not None and type(getattr(module,"__file__",None)) is str
                     and Path(module.__file__).resolve() == path,"MIXED_IMPORT_LOADED_SOURCE_ORIGIN")
            need(MixedImportSession is sys.modules["mixed_claims.imports_atomic"].MixedImportSession
                 and PP is sys.modules["admission.pin_phase"]
                 and ReceiptVerifier is sys.modules["admission.verifier"].ReceiptVerifier
                 and AggregateReceiptVerifier is sys.modules["aggregate_claims.aggregate_admission"].AggregateReceiptVerifier
                 and MixedDeltaVerifier is sys.modules["mixed_claims.receiver"].MixedDeltaVerifier
                 and P is sys.modules["mixed_claims.packet"] and C is sys.modules["modules.codec"]
                 and B is sys.modules["aggregate_claims.bindings"]
                 and expected_journal is sys.modules["delta_claims.claims"].expected_journal,
                 "MIXED_IMPORT_SYMBOL_ORIGIN")
            for index,owner in enumerate(self._owners):
                if owner is not None:
                    if index == 0: owner._check_install()
                    elif index == 1: owner._check_live()
                    else: owner._check()
            for source in self._sources.values():
                kind,handle,raw,binding = source
                actual,unused,members = self._snapshot(kind,handle,raw)
                need(actual == binding,"MIXED_IMPORT_SOURCE_AUTHORITY_CHANGED")
            self._active()
        except BaseException:
            self.close(); raise

    def _merge(self,source_id,source,pending,receipts,resolutions):
        self._mutable()
        need(len(set(self._sources)|{source_id}) <= self._caps[0]
             and len(set(self._nodes)|set(pending)) <= self._caps[1]
             and len(set(self._receipts)|set(receipts)) <= self._caps[2],"MIXED_IMPORT_RETAINED_LIMIT")
        sources,stored,nodes,summaries = dict(self._sources),dict(self._receipts),dict(self._nodes),dict(self._summaries)
        if source_id in sources:
            need(sources[source_id][0] == source[0] and sources[source_id][2:] == source[2:],"MIXED_IMPORT_SOURCE_CONFLICT")
        else: sources[source_id] = source
        for key,receipt in receipts.items():
            need(key not in stored or stored[key] == receipt,"MIXED_IMPORT_EXACT_RECEIPT_DATA_CONFLICT")
            stored[key] = receipt
        conflicts = set()
        for exact,node in pending.items():
            parsed = B.member_journal(exact); summary = C.canonical(parsed["summary"]); module = parsed["module"]
            need(module not in summaries or summaries[module] == summary,"MIXED_IMPORT_SEMANTIC_CONFLICT")
            summaries[module] = summary
            if exact in nodes and nodes[exact][:4] != node[:4]: conflicts.add(exact)
        choices = {} if resolutions is None else resolutions
        need(type(choices) is dict and len(choices) <= self._caps[1]
             and all(type(exact) is bytes and len(exact) == 184 and type(choice) is str
                     and choice in ("existing","incoming") for exact,choice in choices.items()),
             "MIXED_IMPORT_RESOLUTION_MAP","REPRESENTATION_CONFLICT")
        choices = dict(choices)
        need(set(choices) == conflicts,"MIXED_IMPORT_MISSING_OR_UNUSED_RESOLUTIONS","REPRESENTATION_CONFLICT")
        changed = False
        for exact,node in pending.items():
            if exact not in nodes: nodes[exact] = node
            elif exact in conflicts and choices[exact] == "incoming": nodes[exact] = node; changed = True
        need(all(set(node[3]) <= set(nodes) for node in nodes.values()),"MIXED_IMPORT_CHOSEN_ANCESTRY")
        revision = self._representation_revision+int(changed)
        self._live()
        try:
            actual,live,members = self._snapshot(source[0],source[1],source[2])
            need(actual == source[3],"MIXED_IMPORT_FINAL_SOURCE_BINDING"); self._active()
        except BaseException:
            self.close(); raise
        self._mutable()
        # Every fallible check precedes this single-owner state publication.
        self._sources,self._receipts,self._nodes,self._summaries,self._representation_revision = (
            sources,stored,nodes,summaries,revision)
        return live["journal"]

    def _direct(self,kind,handle,receipt,resolutions):
        self._mutable()
        self._begin(); self._charge(receipt)
        binding,live,members = self._snapshot(kind,handle,receipt)
        source_id = C.hash_value("mixed-import-source-v1",C.parse_json(binding)); exact = live["journal"]
        if kind == 0:
            claim,frontier = (0,exact,receipt),(0,exact,0,())
        else:
            claim = 1,live["aggregate_header"],receipt
            frontier = 0,exact,live["member_index"],tuple(live["siblings"])
            B.bind_member(claim[1],exact,frontier[2],list(frontier[3]),adopted_image=self._aggregate_image)
        form = "i-receipt-frontier" if kind == 0 else "a-member-frontier"
        pending = {exact:(exact,form,P.frontier_evidence(claim,frontier),(),source_id)}
        return self._merge(source_id,(kind,handle,receipt,binding),pending,
                           {_receipt_key(*claim):receipt},resolutions)

    def use_legacy_handle(self,handle,receipt_bytes,*,resolutions=None):
        return self._direct(0,handle,receipt_bytes,resolutions)

    def use_aggregate_member(self,handle,receipt_bytes,*,resolutions=None):
        return self._direct(1,handle,receipt_bytes,resolutions)

    def use_delta_handle(self,handle,*,resolutions=None):
        self._mutable()
        self._begin(); owner = self._owners[2]
        need(owner is not None and type(handle) is VerifiedMixedDelta,"MIXED_IMPORT_EXACT_DELTA_HANDLE")
        raw = owner.export_packet(handle); self._charge(raw)
        binding,live,members = self._snapshot(2,handle,raw)
        source_id = C.hash_value("mixed-import-source-v1",C.parse_json(binding))
        claims,frontiers,witnesses,census = P.parse_packet(raw,owner._envelope,aggregate_image=self._aggregate_image)
        actual = {item["journal"]:item for item in members}
        need(len(actual) == len(members) == len(frontiers)+len(witnesses),"MIXED_IMPORT_ACTUAL_INVENTORY")
        pending,receipts = {},{_receipt_key(*claim):claim[2] for claim in claims}
        def add(exact,form,payload,parents):
            need(exact in actual and exact not in pending,"MIXED_IMPORT_ACTUAL_EXACT_MEMBER_REQUIRED")
            item = actual[exact]
            need(item["proof_form"] == form and item["evidence_sha256"] == _sha(payload)
                 and item["packet_sha256"] == _sha(raw),"MIXED_IMPORT_COMPLETE_REPRESENTATION_BINDING")
            pending[exact] = exact,form,payload,tuple(parents),source_id
        for frontier in frontiers:
            claim = claims[frontier[0]]
            add(frontier[1],"i-receipt-frontier" if claim[0] == 0 else "a-member-frontier",
                P.frontier_evidence(claim,frontier),())
        for witness,parents,summary,rank in witnesses:
            add(expected_journal(summary,rank,self._basis.image),"native-delta",witness,parents)
        need(set(pending) == set(actual),"MIXED_IMPORT_COMPLETE_INVENTORY")
        return self._merge(source_id,(2,handle,raw,binding),pending,receipts,resolutions)

    def variants(self,module):
        self._begin(); self._live(); C.digest_string(module)
        return [{"journal":exact,"module":module,"proof_form":node[1],"evidence_sha256":_sha(node[2]),
                 "source_id":node[4]} for exact,node in sorted(self._nodes.items()) if journal(exact)["module"] == module]

    def select_warrant(self,exact):
        self._mutable()
        self._begin(); self._live(); parsed = B.member_journal(exact)
        need(exact in self._nodes,"MIXED_IMPORT_UNESTABLISHED_EXACT_J")
        previous = self._selected.get(parsed["module"])
        need(previous is None or previous == exact,"MIXED_IMPORT_IMMUTABLE_DIRECT_SELECTION","SELECTION_CONFLICT")
        self._mutable(); self._selected[parsed["module"]] = exact; return parsed["module"]

    def _group(self,exact,opening):
        need(exact in self._nodes,"MIXED_IMPORT_GROUP_EXACT_WARRANT")
        kind,handle,unused,binding = self._sources[self._nodes[exact][4]]
        owner = self._owners[kind]
        if kind == 2: group = owner.open_member_group(handle,exact,opening)
        else: group = owner.open_group(handle,opening)
        need(opening["summary"] == journal(exact)["summary"],"MIXED_IMPORT_GROUP_SUMMARY")
        return C.parse_json(C.canonical(group))

    def open_group(self,module,opening):
        self._mutable()
        self._begin(); self._live()
        need(module in self._selected,"MIXED_IMPORT_EXPLICIT_SELECTION_REQUIRED","NEEDS_SELECTION")
        raw = C.canonical(opening); copied = C.parse_json(raw)
        group = self._group(self._selected[module],copied); key = module,copied["index"]
        old = self._groups.get(key); need(old is None or old == raw,"MIXED_IMPORT_GROUP_CHANGED")
        if old is None:
            need(len(self._groups) < C.DEFAULT_LIMITS.max_groups and self._data_bytes+len(raw) <= self._caps[5],
                 "MIXED_IMPORT_SEMANTIC_DATA_LIMIT")
            self._live(); self._mutable(); self._groups[key] = raw; self._data_bytes += len(raw)
        return group

    def supply_body(self,module,universes,expression):
        self._mutable()
        self._begin(); self._live()
        need(module in self._selected,"MIXED_IMPORT_EXPLICIT_SELECTION_REQUIRED","NEEDS_SELECTION")
        digest = C.body_id(expression,universes); allowed = False
        for (owner,index),raw in self._groups.items():
            if owner != module: continue
            for descriptor in C.parse_json(raw)["group"]["declarations"]:
                if descriptor["universes"] != universes: continue
                if descriptor["kind"] in ("definition","opaque"): allowed |= descriptor["value_hash"] == digest
                elif descriptor["kind"] == "recursor":
                    allowed |= any(rule["value_hash"] == digest for rule in descriptor["meta"]["rules"])
        need(allowed,"MIXED_IMPORT_BODY_NOT_COMMITTED")
        raw = C.canonical(expression); key = module,universes,digest; old = self._bodies.get(key)
        need(old is None or old == raw,"MIXED_IMPORT_BODY_CHANGED")
        if old is None:
            need(self._data_bytes+len(raw) <= self._caps[5],"MIXED_IMPORT_SEMANTIC_DATA_LIMIT")
            self._live(); self._mutable(); self._bodies[key] = raw; self._data_bytes += len(raw)
        return digest

    def selected_data(self):
        if self._sealed: return self.view_selection(self._view)[0]
        self._begin(); self._live(); items = []
        for module in sorted({key[0] for key in self._groups}):
            exact = self._selected[module]; node = self._nodes[exact]
            openings = [C.parse_json(raw) for (owner,index),raw in sorted(self._groups.items()) if owner == module]
            for opening in openings: self._group(exact,opening)
            bodies = [{"universes":arity,"digest":digest,"expression":C.parse_json(raw)}
                      for (owner,arity,digest),raw in sorted(self._bodies.items()) if owner == module]
            items.append({"module":module,"journal":exact,"summary":journal(exact)["summary"],
                "proof_form":node[1],"source_id":node[4],"openings":openings,"bodies":bodies})
        self._live(); return items

    def selection(self):
        if self._sealed: return self.view_selection(self._view)
        items = self.selected_data()
        return items,self._selection_binding(items,self._selected,definition_mode=self._definition_mode)

    def require_selection(self,binding):
        if self._sealed:
            C.digest_string(binding); self.require_view(self._view)
            need(binding == self._view_payload[2],"MIXED_IMPORT_SELECTION_CHANGED")
            return
        C.digest_string(binding); unused,actual = self.selection()
        need(actual == binding,"MIXED_IMPORT_SELECTION_CHANGED")

    def census(self):
        self._active()
        return {"retained_warrants":len(self._nodes),"unique_semantic_modules":len(self._summaries),
            "selected_direct_warrants":len(self._selected),"retained_sources":len(self._sources),
            "retained_receipts":len(self._receipts),"retained_receipt_bytes":sum(map(len,self._receipts.values())),
            "semantic_openings":len(self._groups),"representation_revision":self._representation_revision,
            "submitted_bytes":self._submitted_bytes,"calls":self._calls,"counts_are_not_useful_growth":True}

    def onward_packet(self,witness,binding,envelope):
        self.require_selection(binding); need(type(envelope) is P.Envelope,"MIXED_AUTHORING_ENVELOPE")
        envelope.validate(); items,actual = self.selection(); need(actual == binding,"MIXED_AUTHORING_SELECTION")
        parents = [{"journal":list(item["journal"]),"openings":item["openings"]} for item in items]
        need(witness["parents"] == parents,"MIXED_NEW_WITNESS_EXACT_PARENTS")
        parent_js = [item["journal"] for item in items]; parent_ms = [journal(exact)["module"] for exact in parent_js]
        child = C.module_id(witness["local_spec"])
        need(len(parent_ms) == len(set(parent_ms)) and child not in parent_ms,"MIXED_NEW_WITNESS_DIRECT_MODULES")
        rank = max((journal(exact)["rank"] for exact in parent_js),default=-1)+1
        need(witness["rank"] == rank,"MIXED_NEW_WITNESS_RANK")
        target = expected_journal(C.summarize(witness["local_spec"]),rank,self._basis.image)
        included,pending = set(),list(parent_js)
        while pending:
            exact = pending.pop()
            if exact in included: continue
            need(exact in self._nodes,"MIXED_MISSING_SELECTED_ANCESTOR")
            included.add(exact); pending.extend(self._nodes[exact][3])
        need(target not in included,"MIXED_NEW_TARGET_CANNOT_BE_INHERITED")
        claims,frontiers,deltas = {},[],[]
        for exact in sorted(included,key=lambda raw:(journal(raw)["rank"],raw)):
            node = self._nodes[exact]
            if node[1] == "native-delta": deltas.append(C.parse_json(node[2])); continue
            value = C.parse_json(node[2]); tag,statement = value["tag"],bytes(value["statement"])
            key = tag,statement,value["receipt_sha256"],value["receipt_bytes"]
            need(key in self._receipts,"MIXED_MISSING_TERMINAL_RECEIPT")
            receipt = self._receipts[key]; identity = tag,statement
            need(identity not in claims or claims[identity] == receipt,
                 "CLAIM_RECEIPT_REPRESENTATION_CONFLICT","REPRESENTATION_CONFLICT")
            claims[identity] = receipt
            frontiers.append((identity,{"journal":list(exact),"member_index":value["member_index"],"siblings":value["siblings"]}))
        ordered = sorted(claims); positions = {key:index for index,key in enumerate(ordered)}
        encoded_claims = [{"tag":key[0],"statement":list(key[1]),"receipt_hex":claims[key].hex()} for key in ordered]
        encoded_frontiers = [{"claim_index":positions[key],**value} for key,value in frontiers]
        deltas.append(witness)
        raw = C.canonical({"schema":P.SCHEMA,"claims":encoded_claims,"frontiers":encoded_frontiers,"deltas":deltas},
                          C.Limits(max_bytes=envelope.packet_bytes))
        unused_claims,unused_frontiers,checked,census = P.parse_packet(raw,envelope,aggregate_image=self._aggregate_image)
        self.require_selection(binding); return raw,census


    def _mutable(self):
        self._active()
        need(not self._sealed and not self._batching, "MIXED_IMPORT_SEALED_OR_BATCH_ACTIVE")

    def _state(self):
        """Exact immutable semantic-state snapshot; resource counters deliberately excluded."""
        return (self._representation_revision, self._data_bytes,
                self._definition_mode, self._origin_definition_mode,
                *(tuple(sorted(store.items())) for store in
                  (self._sources, self._receipts, self._nodes, self._summaries,
                   self._selected, self._groups, self._bodies)))

    def _selection_binding(self, items, selected, *, definition_mode="eager"):
        _definition_mode(definition_mode)
        public = {"profile":self._profile,"sources":sorted(self._sources),
            "representation_revision":self._representation_revision,
            "chosen":[{"journal":list(exact),"proof_form":node[1],"evidence_sha256":_sha(node[2]),
                "parents":[list(parent) for parent in node[3]],"source_id":node[4]} for exact,node in sorted(self._nodes.items())],
            "warrants":[[module,list(exact)] for module,exact in sorted(selected.items())],
            "selected":[_encoded_fact(item) for item in items]}
        # Preserve the default eager identity exactly. The opt-in view is a
        # different sealed selection, never an in-place reinterpretation.
        if definition_mode != "eager": public["definition_mode"] = definition_mode
        return C.hash_value("mixed-authoring-selection-v1",public)

    def _staged_items(self, selected, groups, bodies):
        items = []
        for module in sorted({key[0] for key in groups}):
            self._active()
            exact = selected[module]; node = self._nodes[exact]
            summary = journal(exact)["summary"]
            openings = [C.parse_json(raw) for (owner,index),raw in sorted(groups.items()) if owner == module]
            for opening in openings:
                self._active()
                C.verify_group_opening(module,opening)
                need(opening["summary"] == summary,"MIXED_IMPORT_GROUP_SUMMARY")
            values = [{"universes":arity,"digest":digest,"expression":C.parse_json(raw)}
                      for (owner,arity,digest),raw in sorted(bodies.items()) if owner == module]
            items.append({"module":module,"journal":exact,"summary":summary,
                "proof_form":node[1],"source_id":node[4],"openings":openings,"bodies":values})
        return items

    def materialize(self, batch_bytes, foundation_bytes, foundation_sha256, *, limits=None,
                    definition_mode="eager"):
        """Atomic synchronous pure-data batch; READY seals, NEED remains extendable.

        Full authority/file checks bracket the computation. This is intentionally
        not equivalent to every historical transient-file sampling instant.
        Input costs remain charged on refusal; only semantic maps are staged.
        """
        self._mutable()
        try:
            self._live(); entry = self._state(); self._batching = True
            _definition_mode(definition_mode)
            need(self._origin_definition_mode is None or definition_mode == self._origin_definition_mode,
                 "MIXED_IMPORT_DEFINITION_MODE_CHANGED")
            need(type(batch_bytes) is bytes and 0 < len(batch_bytes) <= self._caps[5],
                 "MIXED_IMPORT_BATCH_BYTES")
            self._charge(batch_bytes)
            batch = C.parse_json(batch_bytes,C.Limits(max_bytes=self._caps[5]))
            need(C.canonical(batch,C.Limits(max_bytes=self._caps[5])) == batch_bytes,
                 "MIXED_IMPORT_BATCH_CANONICAL")
            C.fields(batch,{"selected","openings","bodies"})
            need(all(type(batch[name]) is list for name in ("selected","openings","bodies")),
                 "MIXED_IMPORT_BATCH_LISTS")
            caps = _context_limits(limits)
            need(type(foundation_bytes) is bytes and len(foundation_bytes) <= caps["data_bytes"],
                 "MIXED_AUTHORING_FOUNDATION_INPUT")
            selected,groups,bodies = dict(self._selected),dict(self._groups),dict(self._bodies)
            data_bytes = self._data_bytes
            for value in batch["selected"]:
                self._begin()
                need(type(value) is list and len(value) == 184,"MIXED_IMPORT_BATCH_JOURNAL")
                exact = bytes(C.uint(part,255) for part in value)
                parsed = B.member_journal(exact)
                need(exact in self._nodes,"MIXED_IMPORT_UNESTABLISHED_EXACT_J")
                previous = selected.get(parsed["module"])
                need(previous is None or previous == exact,"MIXED_IMPORT_IMMUTABLE_DIRECT_SELECTION","SELECTION_CONFLICT")
                selected[parsed["module"]] = exact
            for row in batch["openings"]:
                self._begin(); C.fields(row,{"module","opening"})
                module,opening = row["module"],row["opening"]; C.digest_string(module)
                need(module in selected,"MIXED_IMPORT_EXPLICIT_SELECTION_REQUIRED","NEEDS_SELECTION")
                C.verify_group_opening(module,opening)
                need(opening["summary"] == journal(selected[module])["summary"],"MIXED_IMPORT_GROUP_SUMMARY")
                raw = C.canonical(opening); key = module,opening["index"]; old = groups.get(key)
                need(old is None or old == raw,"MIXED_IMPORT_GROUP_CHANGED")
                if old is None:
                    need(len(groups) < C.DEFAULT_LIMITS.max_groups and data_bytes+len(raw) <= self._caps[5],
                         "MIXED_IMPORT_SEMANTIC_DATA_LIMIT")
                    groups[key] = raw; data_bytes += len(raw)
            for row in batch["bodies"]:
                self._begin(); C.fields(row,{"module","universes","expression"})
                module,universes,expression = row["module"],row["universes"],row["expression"]
                C.digest_string(module)
                need(module in selected,"MIXED_IMPORT_EXPLICIT_SELECTION_REQUIRED","NEEDS_SELECTION")
                digest = C.body_id(expression,universes); allowed = False
                for (owner,index),raw in groups.items():
                    if owner != module: continue
                    for descriptor in C.parse_json(raw)["group"]["declarations"]:
                        if descriptor["universes"] != universes: continue
                        if descriptor["kind"] in ("definition","opaque"):
                            allowed |= descriptor["value_hash"] == digest
                        elif descriptor["kind"] == "recursor":
                            allowed |= any(rule["value_hash"] == digest for rule in descriptor["meta"]["rules"])
                need(allowed,"MIXED_IMPORT_BODY_NOT_COMMITTED")
                raw = C.canonical(expression); key = module,universes,digest; old = bodies.get(key)
                need(old is None or old == raw,"MIXED_IMPORT_BODY_CHANGED")
                if old is None:
                    need(data_bytes+len(raw) <= self._caps[5],"MIXED_IMPORT_SEMANTIC_DATA_LIMIT")
                    bodies[key] = raw; data_bytes += len(raw)
            self._begin()  # Same logical initial selection charge as ordinary context preparation.
            items = self._staged_items(selected,groups,bodies)
            binding = self._selection_binding(items,selected,definition_mode=definition_mode)
            foundation,work = _decode_context_foundation(foundation_bytes,foundation_sha256,self._basis)
            census = self.census()
            census.update(selected_direct_warrants=len(selected),semantic_openings=len(groups))
            ready = _build_context(items,binding,foundation_bytes,foundation_sha256,
                                   foundation,work,self._basis,census,caps,definition_mode=definition_mode)
            # Allocate/serialize everything before final validation and publication.
            payload = None; token = None
            if ready["status"] == "UNTRUSTED_AUTHORING_CONTEXT_READY":
                token = SealedSelection()
                payload = (C.canonical([_encoded_fact(item) for item in items]),
                           C.canonical(ready),binding,foundation_sha256,foundation_bytes)
            else:
                need(ready["status"] == "NEED_AUTHORING_CONTEXT_DATA","MIXED_IMPORT_CONTEXT_STATUS")
            self._begin()  # Retain the ordinary final require_selection charge.
            self._live()
            need(self._state() == entry and not self._sealed,"MIXED_IMPORT_BATCH_STATE_CHANGED")
            sealed_state = (self._representation_revision,data_bytes,definition_mode,definition_mode,
                *(tuple(sorted(store.items())) for store in
                  (self._sources,self._receipts,self._nodes,self._summaries,selected,groups,bodies)))
            self._active()
            self._selected,self._groups,self._bodies,self._data_bytes = selected,groups,bodies,data_bytes
            self._definition_mode = self._origin_definition_mode = definition_mode
            self._sealed,self._view,self._view_payload,self._sealed_state = (
                token is not None,token,payload,sealed_state if token is not None else None)
            return ready,token
        except BaseException:
            self.close(); raise
        finally:
            self._batching = False

    def _check_view(self, view):
        need(type(view) is SealedSelection and self._sealed and view is self._view
             and self._view_payload is not None,"MIXED_IMPORT_FOREIGN_OR_UNSEALED_VIEW")
        try:
            self._live()
            need(self._state() == self._sealed_state,"MIXED_IMPORT_SEALED_STATE_CHANGED")
        except BaseException:
            self.close(); raise

    def require_view(self, view):
        self._begin(); self._check_view(view)

    def view_context(self, view):
        self._begin(); self._check_view(view)
        result = C.parse_json(self._view_payload[1])
        self._check_view(view); return result

    def view_selection(self, view):
        self._begin(); self._check_view(view)
        items = C.parse_json(self._view_payload[0]); binding = self._view_payload[2]
        for item in items: item["journal"] = bytes(item["journal"])
        self._check_view(view); return items,binding

    def close(self):
        self._closed = True
        self._view = self._view_payload = self._sealed_state = None
        self._batching = False
        for store in (self._sources,self._receipts,self._nodes,self._summaries,self._selected,self._groups,self._bodies):
            store.clear()


def _definition_mode(value):
    need(type(value) is str and value in ("eager", "interface-only"),
         "MIXED_AUTHORING_DEFINITION_MODE")
    return value


def _context_limits(limits):
    need(limits is None or (type(limits) is dict
         and all(type(key) is str and type(value) is int for key,value in limits.items())),
         "MIXED_AUTHORING_EXACT_CONTEXT_LIMITS")
    caps = dict(DEFAULT_LIMITS if limits is None else limits)
    C.fields(caps, set(DEFAULT_LIMITS))
    for key, maximum in DEFAULT_LIMITS.items():
        need(0 < C.uint(caps[key], maximum), "MIXED_AUTHORING_CONTEXT_LIMIT:"+key)
    return caps


@dataclass(frozen=True)
class _FoundationIdentifiers:
    _foundation: str
    _policy: str


@dataclass(frozen=True)
class _FoundationView:
    _verifier: _FoundationIdentifiers


def _decode_context_foundation(raw, pin, basis):
    """Pure data-only bridge; no live-owner callbacks or filesystem."""
    view = _FoundationView(_FoundationIdentifiers(basis.foundation, basis.policy))
    return _decode_foundation(raw, pin, view)


def _build_context(items, binding, foundation_bytes, foundation_sha256,
                   foundation, work, basis, census, caps, *, definition_mode="eager"):
    """Build original authenticated context; no frontend descriptor projection."""
    _definition_mode(definition_mode)
    need(work <= caps["expression_visits"], "MIXED_AUTHORING_FOUNDATION_WORK")
    foundation_names = {C.name_key(name) for name in foundation["names"]}
    groups, addresses, bodies, modules = {}, {}, {}, set()
    demands = {}; stored_bytes = len(foundation_bytes); declarations = 0
    deferred_definitions = 0
    for item in items:
        owner = item["module"]; modules.add(owner)
        for opening in item["openings"]:
            group = C.verify_group_opening(owner, opening); key = owner, opening["index"]
            need(key not in groups, "MIXED_AUTHORING_DUPLICATE_GROUP")
            stored_bytes += len(C.canonical(opening)); declarations += len(group["declarations"])
            need(len(groups)+1 <= caps["groups"] and declarations <= caps["declarations"]
                 and stored_bytes <= caps["data_bytes"], "MIXED_AUTHORING_CONTEXT_CENSUS")
            groups[key] = deepcopy(group)
            for d in group["declarations"]:
                address = owner, C.name_key(d["name"])
                need(address not in addresses, "MIXED_AUTHORING_DUPLICATE_DECLARATION")
                addresses[address] = key
        for body in item["bodies"]:
            key = owner, body["universes"], body["digest"]
            need(key not in bodies and C.body_id(body["expression"], body["universes"]) == body["digest"],
                 "MIXED_AUTHORING_BODY_BINDING")
            stored_bytes += len(C.canonical(body))
            need(stored_bytes <= caps["data_bytes"], "MIXED_AUTHORING_CONTEXT_CENSUS")
            bodies[key] = deepcopy(body["expression"])
    edges = {key: set() for key in groups}; selected_bodies = {key: {} for key in groups}

    def demand(value):
        key = C.canonical(value)
        need(key in demands or len(demands) < caps["demands"], "MIXED_AUTHORING_DEMAND_LIMIT")
        demands[key] = value

    def reference(key, ref):
        if ref[0] == "foundation":
            need(C.name_key(ref[1]) in foundation_names, "MIXED_AUTHORING_UNKNOWN_FOUNDATION")
            return
        owner, name = (key[0], ref[1]) if ref[0] == "local" else (ref[1], ref[2])
        address = owner, C.name_key(name)
        if owner not in modules:
            demand({"kind": "NeedVerifiedMixedMember", "module": owner, "name": deepcopy(name)})
        elif address not in addresses:
            demand({"kind": "NeedDeclaration", "module": owner, "name": deepcopy(name)})
        else:
            target = addresses[address]
            need(target != key or groups[key]["kind"] == "inductive", "MIXED_AUTHORING_SELF_REFERENCE")
            if target != key: edges[key].add(target)

    def expression(key, value):
        nonlocal work
        pending = [value]
        while pending:
            expr = pending.pop(); work += 1
            need(work <= caps["expression_visits"], "MIXED_AUTHORING_EXPRESSION_WORK")
            tag = expr[0]
            if tag in ("const", "proj"): reference(key, expr[1])
            children = {"sort": (), "bvar": (), "const": (), "app": (1, 2),
                        "lam": (2, 3), "forall": (2, 3), "let": (1, 2, 3), "proj": (3,)}[tag]
            pending.extend(expr[i] for i in children)

    for key, group in groups.items():
        for d in group["declarations"]:
            expression(key, d["type"])
            hashes = ([d["value_hash"]] if d["kind"] == "definition" else
                      [r["value_hash"] for r in d["meta"]["rules"]] if d["kind"] == "recursor" else [])
            for digest in hashes:
                address = key[0], d["universes"], digest
                if (address not in bodies and definition_mode == "interface-only"
                        and group["kind"] == "ordinary" and d["kind"] == "definition"):
                    # Retain the real descriptor/hash/hints. Only avoid following
                    # a missing ordinary body. Final native checking may demand it.
                    deferred_definitions += 1
                elif address not in bodies:
                    demand({"kind": "NeedBody", "module": key[0], "name": deepcopy(d["name"]),
                            "universes": d["universes"], "body_hash": digest})
                elif address not in selected_bodies[key]:
                    selected_bodies[key][address] = bodies[address]
                    expression(key, bodies[address])
    report = {"groups": len(groups), "declarations": declarations,
              "counted_expression_visits": work, "selected_input_bytes": stored_bytes,
              "all_session_openings_included": True, "frontend_theorem_ancestor_proof_bytes": 0,
              "onward_selected_uncertified_proof_ancestry_retained": True,
              "fixed_foundation_proof_bodies_included": True,
              "expression_counter_is_not_total_cpu_work": True, "whole_operation_supervision_required": True,
              "warrant_census": census}
    if definition_mode != "eager":
        report.update(definition_mode=definition_mode,
                      deferred_definition_bodies=deferred_definitions)
    if demands:
        return {"status": "NEED_AUTHORING_CONTEXT_DATA", "demands": [demands[k] for k in sorted(demands)],
                "selection_binding": binding, "cost": report, "mathematical_acceptance": False}
    remaining, ordered, done = set(groups), [], set()
    while remaining:
        ready = [key for key in sorted(remaining) if edges[key] <= done]
        need(ready, "MIXED_AUTHORING_INTERGROUP_CYCLE")
        for key in ready:
            ordered.append({"owner": key[0], "index": key[1], "group": groups[key],
                "bodies": [{"universes": address[1], "digest": address[2], "expression": body}
                           for address, body in sorted(selected_bodies[key].items())]})
        remaining.difference_update(ready); done.update(ready)
    packet = {"schema": CONTEXT_SCHEMA, "foundation": basis.foundation,
              "policy": basis.policy, "foundation_sha256": foundation_sha256,
              "foundation_view": foundation, "imports": ordered,
              "selection_binding": binding, "mathematical_acceptance": False}
    if definition_mode != "eager": packet["definition_mode"] = definition_mode
    raw = C.canonical(packet)
    need(len(raw) <= caps["data_bytes"], "MIXED_AUTHORING_CONTEXT_OUTPUT")
    report["frontend_packet_bytes"] = len(raw)
    return {"status": "UNTRUSTED_AUTHORING_CONTEXT_READY", "packet": C.parse_json(raw),
            "selection_binding": binding, "cost": report, "mathematical_acceptance": False}

