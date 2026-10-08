"""Exact owner-workload module split and native inputs, never admission.

Read one pinned export, retain complete groups, compact the explicit foundation
dependency DAG, then produce conditional module fixtures. No prover/network or
source execution occurs here. All purported import receipts remain synthetic.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modules import codec as C, model as M, native_rows as N, source_rows as S

FOUNDATION = ("Eq", "Eq.refl", "Eq.rec", "PUnit", "PUnit.unit", "PUnit.rec",
              "PProd", "PProd.mk", "PProd.rec", "Eq.trans", "Eq.casesOn", "HEq",
              "HEq.refl", "HEq.rec", "Eq.ndrec", "rfl", "Eq.symm", "Prod",
              "Prod.mk", "Prod.rec", "Prod.fst", "Prod.snd")
BASE = ("CommonsV5.Tree", "CommonsV5.Tree.leaf", "CommonsV5.Tree.node",
        "CommonsV5.Tree.rec", "CommonsV5.Tree.below", "CommonsV5.Tree.brecOn.go",
        "CommonsV5.Tree.brecOn", "CommonsV5.Tree.casesOn", "CommonsV5.fold.match_1",
        "CommonsV5.fold._f", "CommonsV5.fold", "CommonsV5.map._f", "CommonsV5.map",
        "CommonsV5.binary_congr")
LAYERS = [("base", BASE, []),
          ("fusion", ("CommonsV5.fusion",), ["base"]),
          ("fold_map", ("CommonsV5.fold_map",), ["base"]),
          ("fusion_map", ("CommonsV5.fusion_map",), ["base", "fusion", "fold_map"]),
          ("project_summary", ("CommonsV5.project_summary",), ["base", "fusion"])]


def names(label):
    return [["s", part] for part in label.split(".")]


def records(row):
    tag, value = next(iter(row.items()))
    if tag == "inductive":
        return [item for field in ("types", "ctors", "recs") for item in value[field]]
    return [value]


def declaration(row):
    return not ({"meta", "in", "il", "ie"} & set(row))


class Compact:
    """Reindex only reachable raw DAG nodes, without altering mathematical fields."""
    def __init__(self, rows):
        self.old = {domain: {row[domain]: row for row in rows if domain in row}
                    for domain in ("in", "il", "ie")}
        self.memo = {"in": {0: 0}, "il": {0: 0}, "ie": {}}
        self.next = {"in": 1, "il": 1, "ie": 0}
        self.rows = [copy.deepcopy(rows[0])]

    def node(self, domain, index):
        if index in self.memo[domain]:
            return self.memo[domain][index]
        old = self.old[domain][index]
        tag, v = next((k, copy.deepcopy(v)) for k, v in old.items() if k != domain)
        n = lambda i: self.node("in", i)
        l = lambda i: self.node("il", i)
        e = lambda i: self.node("ie", i)
        if domain == "in":
            C.require(tag in ("str", "num"), "WORKLOAD_NAME_TAG")
            v["pre"] = n(v["pre"])
        elif domain == "il":
            if tag == "param": v = n(v)
            elif tag == "succ": v = l(v)
            elif tag in ("max", "imax"): v = [l(i) for i in v]
            else: raise ValueError("WORKLOAD_LEVEL_TAG")
        elif tag == "sort": v = l(v)
        elif tag == "bvar": pass
        elif tag == "const": v = {"name": n(v["name"]), "us": [l(i) for i in v["us"]]}
        elif tag == "app": v = {"fn": e(v["fn"]), "arg": e(v["arg"])}
        elif tag in ("lam", "forallE", "letE"):
            v["name"] = n(v["name"])
            for field in ("type", "body", "value"):
                if field in v: v[field] = e(v[field])
        elif tag == "proj":
            v["typeName"], v["struct"] = n(v["typeName"]), e(v["struct"])
        elif tag == "mdata": v["expr"] = e(v["expr"])
        else: raise ValueError("WORKLOAD_EXPRESSION_TAG:" + tag)
        new = self.next[domain]
        self.next[domain] += 1
        self.memo[domain][index] = new
        self.rows.append({domain: new, tag: v})
        return new

    def record(self, item):
        out = copy.deepcopy(item)
        for field in ("name", "induct"):
            if field in out: out[field] = self.node("in", out[field])
        for field in ("levelParams", "all", "ctors"):
            if field in out: out[field] = [self.node("in", i) for i in out[field]]
        for field in ("type", "value"):
            if field in out: out[field] = self.node("ie", out[field])
        if "rules" in out:
            out["rules"] = [{**r, "ctor": self.node("in", r["ctor"]),
                             "rhs": self.node("ie", r["rhs"])} for r in out["rules"]]
        return out

    def add(self, row):
        tag, value = next(iter(row.items()))
        mapped = ({key: [self.record(item) for item in value[key]]
                   for key in ("types", "ctors", "recs")} if tag == "inductive"
                  else self.record(value))
        self.rows.append({tag: mapped})


def body_refs(spec):
    result = set()
    for group in spec["groups"]:
        for d in group["declarations"]:
            if d["value_hash"] is not None: result.add((d["universes"], d["value_hash"]))
            if d["kind"] == "recursor":
                result.update((d["universes"], r["value_hash"]) for r in d["meta"]["rules"])
    return result


def prepare(rows, out, semantic_policy=None, observe=None):
    # This inventory is a selected fixture census, not a general namespace trust rule.
    inventory = S.SourceRows(rows, [names(x) for _, group, _ in LAYERS for x in group],
                             [names(x) for x in FOUNDATION])
    actual = {C.name_key(inventory.name(r["name"]))
              for row in rows if declaration(row) for r in records(row)}
    expected = {C.name_key(names(x)) for x in FOUNDATION}
    expected.update(C.name_key(names(x)) for _, group, _ in LAYERS for x in group)
    C.require(actual == expected, "EXACT_WORKLOAD_DECLARATION_CENSUS")
    foundation_keys = {C.name_key(names(x)) for x in FOUNDATION}
    compact = Compact(rows)
    for row in rows:
        if not declaration(row): continue
        chosen = [C.name_key(inventory.name(r["name"])) in foundation_keys for r in records(row)]
        C.require(all(chosen) or not any(chosen), "ATOMIC_FOUNDATION_GROUP")
        if all(chosen): compact.add(row)
    seed = compact.rows
    # Exact seed is a candidate to be independently checked, not an adopted foundation.
    foundation = C.hash_value("owner-workload-foundation-candidate", seed)
    policy = C.hash_value("owner-workload-conditional-policy", {"permitted_axioms": [],
                           "nat_extension": False, "string_extension": False,
                           "certificate_verification": "NOT_PERFORMED"})
    if semantic_policy is not None:
        C.require(semantic_policy.get("schema") == "DMKN_MODULE_SEMANTIC_POLICY_V1"
                  and semantic_policy.get("foundation") == foundation, "EXPLICIT_SEMANTIC_POLICY")
        policy = C.hash_value("semantic-policy", semantic_policy)
    write(out / "foundation.json", seed)
    write(out / "all-new.json", {"schema": "DMKN_V5_NATIVE_PREFLIGHT_V1", "mode": "all_new",
                                "rows": rows, "permitted_axioms": []})
    write(out / "foundation-check.json", {"schema": "DMKN_V5_NATIVE_PREFLIGHT_V1", "mode": "all_new",
                                         "rows": seed, "permitted_axioms": []})
    libraries, summaries = {}, []
    for label, group, dependencies in LAYERS:
        keys = {C.name_key(names(x)) for x in group}
        selected = [row for row in rows if not declaration(row) or
                    all(C.name_key(inventory.name(r["name"])) in keys | foundation_keys for r in records(row))]
        externals = [{"source_name": d["name"], "module": libraries[dep].module,
                      "relative_name": d["name"]} for dep in dependencies
                     for g in libraries[dep].spec["groups"] for d in g["declarations"]]
        env = S.decode_source(selected, [names(x) for x in group], [names(x) for x in FOUNDATION],
                              foundation, policy, externals)
        for dep in dependencies:
            parent = libraries[dep]
            summary = C.summarize(parent.spec)
            env.add_claim(M.ImportClaim(parent.module, foundation, policy, summary["group_root"],
                summary["group_count"], 0, "33"*32, "44"*32))
            for i in range(len(parent.spec["groups"])):
                env.add_import_opening(parent.module, C.group_opening(parent.spec, i))
            # Copy only committed computation bodies; NEVER imported theorem proofs.
            for arity, digest in body_refs(parent.spec):
                env.supply_body(C.parse_json(parent.bodies[arity, digest]), arity)
        libraries[label] = env
        emitted = N.emit_conditional(env, seed)
        foundation_indices = [r["name"] for row in seed if declaration(row) for r in records(row)]
        premises = [{"authority": {"kind": "foundation", "foundation": foundation},
                     "names": foundation_indices}]
        premises.extend({"authority": {"kind": "module", "module": p["module"],
            "group": p["descriptor_hash"], "journal": p["journal_hash"], "receipt": p["receipt_hash"]},
            "names": p["native_name_indices"]} for p in emitted["unverified_module_premises"])
        request = {"schema": "DMKN_V5_NATIVE_PREFLIGHT_V1", "mode": "corresponding_module",
                   "rows": emitted["rows"], "module": env.module, "foundation": foundation,
                   "premises": premises, "permitted_axioms": []}
        bindings = [{"owner": owner, "imported": owner != env.module,
                     "descriptor": C.parse_json(encoded)} for (owner, _), encoded in
                    sorted(env.groups.items()) if owner != env.module]
        bindings.extend({"owner": env.module, "imported": False, "descriptor": g} for g in env.spec["groups"])
        correspondence = {"foundation_rows": len(seed), "groups": bindings,
                          "bodies": [{"universes": u, "digest": h, "expression": C.parse_json(b)}
                                     for (u, h), b in sorted(env.bodies.items())]}
        request["correspondence"] = correspondence
        base = out / label
        base.mkdir()
        write(base / "spec.json", env.spec)
        write(base / "native.json", request)
        write(base / "correspondence.json", correspondence)
        bundle = {"schema": "DMKN_V5_OWNER_WORKLOAD_BUNDLE_V1", "module": env.module,
                  "spec": env.spec, "openings": [C.group_opening(env.spec, i)
                  for i in range(len(env.spec["groups"]))], "bodies": [
                  {"universes": u, "digest": h, "expression": C.parse_json(env.bodies[u, h])}
                  for u, h in sorted(body_refs(env.spec))], "mathematical_admission": False,
                  "certificate_verification": "NOT_PERFORMED"}
        write(base / "bundle.json", bundle)
        if observe is not None:
            observe(label, env, seed, dependencies, base)
        summaries.append({"label": label, "module": env.module, "groups": len(env.spec["groups"]),
                          "dependencies": dependencies, "native_rows": len(emitted["rows"]),
                          "imported_theorem_proof_bodies_supplied": 0})
    return {"schema": "DMKN_V5_OWNER_WORKLOAD_SPLIT_V1", "foundation": foundation, "policy": policy,
            "foundation_rows": len(seed), "modules": summaries, "mathematical_admission": False}


def write(path, value):
    raw = C.canonical(value)
    with path.open("xb") as stream: stream.write(raw)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--export", required=True); p.add_argument("--sha256", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    source, out = Path(args.export), Path(args.output)
    C.require(source.is_absolute() and out.is_absolute() and not out.exists(), "EXPLICIT_FRESH_PATHS")
    C.require(source.stat().st_size <= 2**20, "WORKLOAD_SOURCE_BYTES")
    raw = source.read_bytes()
    C.require(hashlib.sha256(raw).hexdigest() == args.sha256, "WORKLOAD_EXPORT_PIN")
    rows = [C.parse_json(line) for line in raw.splitlines()]
    out.mkdir()
    report = prepare(rows, out)
    report["source_sha256"] = args.sha256
    write(out / "RESULT.json", report)
    print(json.dumps(report))


if __name__ == "__main__": main()
