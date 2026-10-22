"""Fixed V source and pure renewal shape checks; never receipt verification.

The ordinary owner loads this as its separately pinned renewal_source.py.
prepare_renewal accepts an already selected producer; it never constructs one,
executes a snapshot, spends a proof allowance or creates mathematical authority.
"""
from dataclasses import replace
import hashlib

from aggregate_claims import bindings as B
from delta_claims.claims import expected_journal
from mixed_claims import packet as P
from modules import codec as C
from modules.model import Address
from modules.source_rows import decode_source

A_IMAGE = "9d5072a67f5ab2c4f9468df03c2424d71c457021c4b442d7739c5a3d51ba2865"
U_MODULE = "ad0cc7c499ec6ca71cd211733c3f566f417b4d86a6064292510b927c4eb122c3"
U_J_SHA = "0ba261cd27c816223aa56bc6cbe217e67f48264b8d1c707326095492620a1657"
V_MODULE = "38fbe7771b5ec333bde219631bfb9d6c0a75193f51695723abd41f8b5cfe6dc8"
U_NAME = [["s", "RC0"], ["s", "context_transport"]]
V_NAME = [["s", "RC0"], ["s", "context_transport_then"]]
MATERIAL_SCHEMA = "DMKN_TYPED_RENEWAL_MATERIAL_V1"


def v_source():
    name = C.relocated_name(U_MODULE, U_NAME)
    external = ".".join("\u00ab" + part[1] + "\u00bb" for part in name)
    return """universe u v w z
theorem RC0.context_transport_then
    {A : Sort u} {B : Sort v} {C : Sort w} {D : Sort z}
    (f : B -> C -> D) (g : A -> A -> B) (h : A -> A -> C)
    {a aa b bb c cc : A} (ha : a = aa) (hb : b = bb) (hc : c = cc)
    (d : D) (hd : f (g aa bb) (h bb cc) = d) :
    f (g a b) (h b c) = d :=
  @Eq.trans.{z} D (f (g a b) (h b c)) (f (g aa bb) (h bb cc)) d
    (@""" + external + ".{u, v, w, z} A B C D f g h a aa b bb c cc ha hb hc) hd\n"


def validate_material(material):
    """Only bind candidate bytes/semantics; a real issuer must verify receipt."""
    C.fields(material, {"schema", "receipt", "header", "journal", "member_index", "siblings", "opening"})
    C.require(material["schema"] == MATERIAL_SCHEMA, "RENEWAL_MATERIAL_SCHEMA")
    C.require(type(material["receipt"]) is bytes and 0 < len(material["receipt"]) <= 64*1024**2,
              "RENEWAL_ACTUAL_RECEIPT_REQUIRED")
    exact = material["journal"]
    C.require(type(exact) is bytes and hashlib.sha256(exact).hexdigest() == U_J_SHA,
              "RENEWAL_EXACT_U_JOURNAL")
    parsed = B.member_journal(exact)
    C.require(parsed["module"] == U_MODULE and parsed["rank"] == 1, "RENEWAL_U_TARGET")
    header = B.decode_header(material["header"], adopted_image=A_IMAGE)
    C.require(header["member_count"] == 2 and header["maximum_member_rank"] == 1
              and header["seal_height"] == 1, "RENEWAL_U_AGGREGATE_SHAPE")
    B.bind_member(material["header"], exact, material["member_index"], material["siblings"],
                  adopted_image=A_IMAGE)
    opening = material["opening"]
    group = C.verify_group_opening(U_MODULE, opening)
    C.require(opening["summary"] == parsed["summary"] and opening["index"] == 0
              and group["kind"] == "ordinary" and len(group["declarations"]) == 1,
              "RENEWAL_U_ONLY_GROUP")
    declaration = group["declarations"][0]
    C.require(declaration["name"] == U_NAME and declaration["kind"] == "theorem"
              and declaration["universes"] == 4, "RENEWAL_U_INTERFACE")
    return parsed


def validate_renewal_packet(raw, exact_journal, material, *, envelope):
    """Enforce the sole A frontier and source target; not native/crypto checking."""
    validate_material(material)
    claims, frontiers, witnesses, census = P.parse_packet(raw, envelope, aggregate_image=A_IMAGE)
    C.require(claims == ((1, material["header"], material["receipt"]),), "RENEWAL_SOLE_A_CLAIM")
    C.require(frontiers == ((0, material["journal"], material["member_index"],
                             tuple(material["siblings"])),), "RENEWAL_SOLE_U_FRONTIER")
    C.require(len(witnesses) == 1, "RENEWAL_ONLY_V_DELTA")
    encoded, parents, summary, rank = witnesses[0]
    witness = C.parse_json(encoded)
    C.require(parents == (material["journal"],) and rank == 2
              and witness["parents"] == [{"journal": list(material["journal"]),
                                          "openings": [material["opening"]]}]
              and witness["bodies"] == [], "RENEWAL_NO_U_ANCESTRY")
    C.require(C.module_id(witness["local_spec"]) == V_MODULE
              and C.summary_id(summary) == V_MODULE, "RENEWAL_EXACT_V_SPEC")
    predicted = expected_journal(summary, rank, B.RELATION_IMAGE)
    C.require(type(exact_journal) is bytes and exact_journal == predicted, "RENEWAL_EXACT_V_JOURNAL")
    return {"journal": predicted, "summary": summary, "witness": witness, "census": census}


def inspect_source_export(request, exported, witness, material):
    """Bind actual frontend output and inspect the U-to-Eq.trans proof edge."""
    validate_material(material)
    source_sha = hashlib.sha256(v_source().encode("utf-8")).hexdigest()
    C.require(request["source"] == v_source() and request["source_sha256"] == source_sha
              and request["roots"] == exported["roots"] == [V_NAME]
              and exported["source_sha256"] == source_sha, "RENEWAL_FIXED_SOURCE_EXPORT")
    context = request["context"]
    imports = context["imports"]
    C.require(context["definition_mode"] == "interface-only" and len(imports) == 1
              and imports[0]["owner"] == U_MODULE and imports[0]["index"] == 0
              and imports[0]["group"] == material["opening"]["group"]
              and imports[0]["bodies"] == [], "RENEWAL_FRONTEND_ONLY_U_INTERFACE")
    external = [{"source_name": C.relocated_name(U_MODULE, U_NAME),
                 "module": U_MODULE, "relative_name": U_NAME}]
    limits = replace(C.DEFAULT_LIMITS, max_name_parts=C.DEFAULT_LIMITS.max_name_parts+3)
    env = decode_source(exported["rows"], exported["local_names"], context["foundation_view"]["names"],
                        B.FOUNDATION, B.POLICY, external, limits)
    C.require(env.module == V_MODULE and env.spec == witness["local_spec"], "RENEWAL_EXACT_EXPORTED_SPEC")
    proof_hash = env.local_proofs[Address.of(env.module, V_NAME)]
    proof = C.parse_json(env.bodies[4, proof_hash])
    typ = env.spec["groups"][0]["declarations"][0]["type"]
    body = proof
    for unused in range(18):
        C.require(body[0] == "lam" and typ[0] == "forall" and body[1:3] == typ[1:3],
                  "RENEWAL_EXACT_PROOF_TELESCOPE")
        body, typ = body[3], typ[3]
    def app(head, *arguments):
        for argument in arguments: head = ["app", head, argument]
        return head
    def var(index): return ["bvar", index]
    left = app(var(13), app(var(12), var(10), var(8)), app(var(11), var(8), var(6)))
    middle = app(var(13), app(var(12), var(9), var(7)), app(var(11), var(7), var(5)))
    used = app(["const", ["external", U_MODULE, U_NAME], [["param", i] for i in range(4)]],
               *(var(i) for i in range(17, 1, -1)))
    expected = app(["const", ["foundation", [["s", "Eq"], ["s", "trans"]]], [["param", 3]]],
                   var(14), left, middle, var(1), used, var(0))
    C.require(body == expected, "RENEWAL_EXACT_U_FEEDS_TRANS")
    return {"source_sha256": source_sha, "proof_sha256": hashlib.sha256(C.canonical(proof)).hexdigest(),
            "outer_binders": 18, "U_uses": 1, "Eq_trans_uses": 1, "exact_U_feeds_trans": True,
            "authority": "SOURCE_SHAPE_INSPECTION_NOT_MATHEMATICAL_ACCEPTANCE"}


def prepare_renewal(producer, raw, exact_journal, material, *, envelope):
    """Separate preparation-only call; no snapshot, proving or implicit funding."""
    validate_renewal_packet(raw, exact_journal, material, envelope=envelope)
    prepared = producer.prepare(raw, exact_journal, envelope=envelope)
    C.require(prepared.adopted_image == A_IMAGE and prepared.target_journal == exact_journal
              and prepared.input_sha256 == hashlib.sha256(raw).hexdigest() and prepared.input_bytes == len(raw)
              and prepared.status == "UNTRUSTED_MIXED_SEAL_PREPARATION"
              and prepared.mathematical_admission is False
              and len(prepared.parents) == 1 and prepared.parents[0].tag == 1
              and prepared.parents[0].statement == material["header"]
              and prepared.parents[0].receipt == material["receipt"], "RENEWAL_PREPARED_A_PARENT")
    C.require(prepared.selected_claim_indices == prepared.selected_frontier_indices
              == prepared.selected_delta_indices == (0,)
              and prepared.members == tuple(sorted((material["journal"], exact_journal))),
              "RENEWAL_PREPARED_EXACT_SELECTION")
    census = prepared.census
    C.require((census.claims, census.frontiers, census.deltas, census.members, census.edges) == (1, 1, 1, 2, 1),
              "RENEWAL_PREPARED_CENSUS")
    header = B.decode_header(prepared.expected_header, adopted_image=A_IMAGE)
    C.require(header["maximum_member_rank"] == header["seal_height"] == 2,
              "RENEWAL_PREPARED_RANK_HEIGHT")
    return prepared
