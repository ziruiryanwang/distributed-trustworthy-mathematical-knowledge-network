"""Pure changed-format controls using synthetic ranks; NO receipt authority."""
import hashlib

from aggregate_claims import bindings as B, input as W, admission_binding as A
from modules import codec as C


def run(base_journal, adopted_image):
    checks = []

    def reject(name, function):
        try: function()
        except (ValueError, TypeError): checks.append(name); return
        raise ValueError("EXPECTED_REFUSAL:"+name)

    # All alternate ranks here are synthetic structural fixtures, not checked
    # mathematical claims. The same semantic interface is deliberately reused.
    members = sorted(base_journal[:176]+rank.to_bytes(8,"little") for rank in (0,1,256))
    C.require([B.member_journal(j)["rank"] for j in members] == [0,256,1],
              "EXACT_BYTES_NOT_NUMERIC_RANK_ORDER")
    C.require(len({B.member_journal(j)["module"] for j in members}) == 1,
              "ONE_SEMANTIC_MODULE_THREE_SYNTHETIC_WARRANTS")
    header = (B.MAGIC+B.VERSION.to_bytes(4,"little")+bytes.fromhex(adopted_image)
              +bytes.fromhex(B.RELATION_IMAGE)+bytes.fromhex(B.FOUNDATION)+bytes.fromhex(B.POLICY)
              +B.commitment(members)+(3).to_bytes(4,"little")
              +(256).to_bytes(8,"little")+(1).to_bytes(8,"little"))
    for index,j in enumerate(members):
        B.bind_member(header,j,index,B.opening(members,index),adopted_image=adopted_image)
    checks.append("distinct_exact_warrants_same_semantics_lexicographic_all_openings")
    reject("duplicate_exact_warrant", lambda:B.commitment([members[0],members[0]]))
    reject("numeric_rank_order_not_canonical", lambda:B.commitment([members[0],members[2],members[1]]))
    reject("same_semantic_variant_not_substitutable", lambda:B.bind_member(
        header,members[2],0,B.opening(members,0),adopted_image=adopted_image))
    reject("v1_header_not_v2", lambda:B.decode_header(
        b"DMKNA001"+(1).to_bytes(4,"little")+header[12:],adopted_image=adopted_image))
    target = base_journal[:176]+(257).to_bytes(8,"little")
    common = dict(adopted_image=adopted_image,claims=[(0,j) for j in members],
                  frontiers=[(i,j,0,[]) for i,j in enumerate(members)],
                  witnesses=[b"{}"],targets=[target])
    wire = W.encode(**common)
    # This deliberately malformed witness is encoded, not falsely certified.
    offset = 60+len(members)*(185+196)
    C.require(wire[:12] == b"DMKNAI02\x02\0\0\0"
              and wire[offset:offset+184] == target and wire[offset+184:] == b"\x02\0\0\0{}",
              "EXACT_V2_WIRE_FULL_J_TARGET")
    checks.append("wire_variants_and_full_exact_target_inert")
    reject("ambiguous_ModuleID_target", lambda:W.encode(**dict(common,targets=[target[108:140]])))
    reject("frontier_not_new_target", lambda:W.encode(**dict(common,targets=[members[0]])))
    reject("duplicate_frontier_not_deduplicated", lambda:W.encode(**dict(common,
        frontiers=common["frontiers"]+[(0,members[0],0,[])])))
    reject("duplicate_target_not_deduplicated", lambda:W.encode(**dict(common,
        targets=[target,target],witnesses=[b"{}",b"{}"])) )
    reject("duplicate_claim_not_deduplicated", lambda:W.encode(**dict(common,
        claims=common["claims"]+[(0,members[0])])) )
    # Old-v1 membership roots cannot become v2 roots by changing header magic.
    old_leaf = hashlib.sha256(b"DMKN-V5-AGGREGATE\0LEAF\0"+(1).to_bytes(4,"little")
                             +(0).to_bytes(4,"little")+members[0]).digest()
    old_root = hashlib.sha256(b"DMKN-V5-AGGREGATE\0ROOT\0"+(1).to_bytes(4,"little")+old_leaf).digest()
    old_commitment = header[:140]+old_root+(1).to_bytes(4,"little")+header[176:]
    reject("v1_membership_domain_not_relabelable", lambda:B.bind_member(
        old_commitment,members[0],0,[],adopted_image=adopted_image))
    receipt = b"fabricated_receipt_to_demonstrate_inert_binding"
    report = dict(schema=A.SCHEMA,status=A.STATUS,aggregate_image=adopted_image,
                  header=list(header),receipt_sha256=hashlib.sha256(receipt).hexdigest(),
                  receipt_bytes=len(receipt))
    bound = A.bind_output(C.canonical(report),receipt,header,adopted_image=adopted_image)
    C.require(bound["header"] == header,"SIX_FIELD_INERT_BINDING")
    checks.append("saved_output_binding_explicitly_not_receipt_verification")
    reject("reported_header_mismatch", lambda:A.bind_output(C.canonical(dict(report,
        header=list(header[:-1]+b"\x01"))),receipt,header,adopted_image=adopted_image))
    reject("reported_receipt_mismatch", lambda:A.bind_output(C.canonical(report),
        receipt+b"x",header,adopted_image=adopted_image))
    return checks
