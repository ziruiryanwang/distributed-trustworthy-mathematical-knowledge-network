"""Finite primitive tests; metadata authentication is not mathematical checking.

Root selects execution. No filesystem, native checker, prover or network work.
"""
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discovery import authenticated_index as A


def key(label):
    return hashlib.sha256(label.encode("ascii")).hexdigest()


class Memory:
    def __init__(self):
        self.nodes, self.reads, self.writes = {}, 0, 0

    def get_node(self, identifier):
        self.reads += 1
        return deepcopy(self.nodes[identifier])

    def put_node(self, node):
        self.writes += 1
        identifier = A.node_hash(node)
        if identifier in self.nodes and self.nodes[identifier] != node:
            raise ValueError("TEST_HASH_CONFLICT")
        self.nodes[identifier] = deepcopy(node)
        return identifier


class VectorContracts(unittest.TestCase):
    def test_widths_zero_through_five_and_preserved_roots(self):
        io, ctx = Memory(), A.context(key("namespace"), key("feature"), 7)
        roots = [A.vector_empty(ctx)]
        records = [key("record" + str(i)) for i in range(5)]
        with self.assertRaises(ValueError):
            A.vector_get(io, ctx, 0, roots[0], 0)
        with self.assertRaises(ValueError):
            A.verify_vector(ctx, 0, roots[0], 0, records[0], [])
        for count in range(5):
            before_reads, before_writes = io.reads, io.writes
            roots.append(A.append_vector(io, ctx, count, roots[-1], records[count]))
            height = A.vector_height(count + 1)
            self.assertLessEqual(io.reads - before_reads, height)
            self.assertLessEqual(io.writes - before_writes, height + 2)
        self.assertEqual([A.vector_height(i) for i in range(6)], [0, 0, 1, 2, 2, 3])
        for width in range(1, 6):
            for index in range(width):
                with self.subTest(width=width, index=index):
                    rid, proof = A.vector_get(io, ctx, width, roots[width], index)
                    self.assertEqual(rid, records[index])
                    self.assertEqual(len(proof), A.vector_height(width))
                    A.verify_vector(ctx, width, roots[width], index, rid, proof)
            with self.assertRaises(ValueError):
                A.vector_get(io, ctx, width, roots[width], width)
        # Length binds at the vector commitment, not an individual membership
        # path: widths 3 and 4 have equal proof depth but distinct commitments.
        self.assertNotEqual(A.vector_commit(ctx, 3, roots[3]),
                            A.vector_commit(ctx, 4, roots[3]))

    def test_membership_mutations_and_padding_are_rejected(self):
        io, ctx = Memory(), A.context(key("namespace"), key("feature"), 7)
        root = A.vector_empty(ctx)
        for i in range(5):
            root = A.append_vector(io, ctx, i, root, key("record" + str(i)))
        rid, proof = A.vector_get(io, ctx, 5, root, 3)
        cases = [
            (key("wrong-context"), 5, root, 3, rid, proof),
            (ctx, 5, key("wrong-root"), 3, rid, proof),
            (ctx, 5, root, 2, rid, proof),
            (ctx, 5, root, 3, key("wrong-record"), proof),
            (ctx, 5, root, 3, rid, proof[:-1]),
            (ctx, 5, root, 3, rid, [*proof, key("extra")]),
            (ctx, 5, root, 3, rid, [key("wrong-sibling"), *proof[1:]]),
            (ctx, 5, root, 5, rid, proof),
            (ctx, 5, root, True, rid, proof),
        ]
        for number, args in enumerate(cases):
            with self.subTest(mutation=number), self.assertRaises(ValueError):
                A.verify_vector(*args)
        with self.assertRaises(ValueError):
            A.append_vector(io, ctx, 0, root, rid)
        corrupted = Memory()
        corrupted.nodes = deepcopy(io.nodes)
        corrupted.nodes[root]["left"] = key("wrong-cas-child")
        with self.assertRaises(ValueError):
            A.vector_get(corrupted, ctx, 5, root, 3)


class MapContracts(unittest.TestCase):
    def test_partition_defaults_and_cross_partition_binding(self):
        io, ns, feature = Memory(), key("namespace"), key("feature")
        descriptors = [A.empty_descriptor(ns, feature, p) for p in range(256)]
        empty_root = A.partition_empty()[8]
        self.assertEqual(A.feature_root(ns, feature, descriptors), empty_root)
        bad = dict(descriptors[7], tree_root=key("wrong-empty-root"))
        with self.assertRaises(ValueError):
            A.descriptor_hash(ns, feature, bad)
        ctx = A.context(ns, feature, 7)
        tree = A.append_vector(io, ctx, 0, A.vector_empty(ctx), key("record"))
        descriptors[7] = dict(partition=7, count=1, tree_root=tree)
        root = A.partition_set(io, ns, feature, empty_root, descriptors[7])
        self.assertEqual(A.feature_root(ns, feature, descriptors), root)
        for p in range(256):
            actual, siblings = A.partition_get(io, ns, feature, root, p)
            self.assertEqual(actual, descriptors[p])
            self.assertEqual(len(siblings), 8)
        with self.assertRaises(ValueError):
            A.partition_get(io, key("another-namespace"), feature, root, 7)
        with self.assertRaises(ValueError):
            A.partition_get(io, ns, key("another-feature"), root, 7)

    def test_sparse_map_membership_absence_and_mutations(self):
        io, ns, feature = Memory(), key("namespace"), key("feature")
        empty = A.map_empty(ns)[0]
        selected_root = key("selected-feature-root")
        root = A.map_set(io, ns, empty, feature, selected_root)
        actual, proof = A.map_get(io, ns, root, feature)
        self.assertEqual(actual, selected_root)
        A.verify_map(ns, root, feature, actual, proof)
        absent = key("absent-feature")
        actual_absent, absent_proof = A.map_get(io, ns, root, absent)
        self.assertIsNone(actual_absent)
        A.verify_map(ns, root, absent, None, absent_proof)
        cases = [
            (ns, root, feature, None, proof),
            (ns, root, absent, selected_root, absent_proof),
            (ns, root, feature, key("wrong-selected-root"), proof),
            (ns, root, feature, selected_root, proof[:-1]),
            (ns, root, feature, selected_root, [key("wrong-sibling"), *proof[1:]]),
            (key("wrong-namespace"), root, absent, None, absent_proof),
        ]
        for number, args in enumerate(cases):
            with self.subTest(mutation=number), self.assertRaises(ValueError):
                A.verify_map(*args)
        # Insertion did not mutate the earlier absent snapshot.
        old, old_proof = A.map_get(io, ns, empty, feature)
        self.assertIsNone(old)
        A.verify_map(ns, empty, feature, None, old_proof)


if __name__ == "__main__":
    unittest.main(verbosity=2)
