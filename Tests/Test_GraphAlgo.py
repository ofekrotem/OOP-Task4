from unittest import TestCase

from client_python.DiGraph import DiGraph, Edge, Node
from client_python.GraphAlgo import GraphAlgo

n1 = Node(1, 1.1, 2.1, 3.1)
n2 = Node(2, 1.2, 2.2, 3.2)
n3 = Node(3, 1.3, 2.3, 3.3)
n4 = Node(4, 1.4, 2.4, 3.4)

e12 = Edge(n1, n2, 1.12)
e13 = Edge(n1, n3, 1.13)
e21 = Edge(n2, n1, 1.21)
e24 = Edge(n2, n4, 1.24)
e31 = Edge(n3, n1, 1.31)
e34 = Edge(n3, n4, 1.34)
e41 = Edge(n4, n1, 1.41)
e43 = Edge(n4, n3, 1.43)

Nodes = {}
Nodes[1] = n1
Nodes[2] = n2
Nodes[3] = n3
Nodes[4] = n4

all_edges = {}
s12 = "1,2"
s13 = "1,3"
s21 = "2,1"
s24 = "2,4"
s31 = "3,1"
s34 = "3,4"
s41 = "4,1"
s43 = "4,3"
all_edges[s12] = e12
all_edges[s13] = e13
all_edges[s21] = e21
all_edges[s24] = e24
all_edges[s31] = e31
all_edges[s34] = e34
all_edges[s41] = e41
all_edges[s43] = e43

edges_out = {}
edges_out[1] = {2: e21.weight}
edges_out[1].update({3: e13.weight})
edges_out[2] = {1: e21.weight}
edges_out[2].update({4: e24.weight})
edges_out[3] = {1: e31.weight}
edges_out[3].update({4: e34.weight})
edges_out[4] = {1: e41.weight}
edges_out[4].update({3: e43.weight})

edges_in = {}
edges_in[1] = {2: e21.weight}
edges_in[1].update({3: e31.weight})
edges_in[1].update({4: e41.weight})
edges_in[3] = {1: e13.weight}
edges_in.get(3).update({4: e43.weight})
edges_in[4] = {2: e24.weight}
edges_in.get(4).update({3: e34.weight})

g1 = DiGraph(Nodes, edges_in, edges_out, all_edges)
g1_algo = GraphAlgo(g1)


class TestGraphAlgo(TestCase):
    def setUp(self) -> None:
        n1 = Node(1, 1.1, 2.1, 3.1)
        n2 = Node(2, 1.2, 2.2, 3.2)
        n3 = Node(3, 1.3, 2.3, 3.3)
        n4 = Node(4, 1.4, 2.4, 3.4)

        e12 = Edge(n1, n2, 1.12)
        e13 = Edge(n1, n3, 1.13)
        e21 = Edge(n2, n1, 1.21)
        e24 = Edge(n2, n4, 1.24)
        e31 = Edge(n3, n1, 1.31)
        e34 = Edge(n3, n4, 1.34)
        e41 = Edge(n4, n1, 1.41)
        e43 = Edge(n4, n3, 1.43)

        Nodes = {}
        Nodes[1] = n1
        Nodes[2] = n2
        Nodes[3] = n3
        Nodes[4] = n4

        all_edges = {}
        s12 = "1,2"
        s13 = "1,3"
        s21 = "2,1"
        s24 = "2,4"
        s31 = "3,1"
        s34 = "3,4"
        s41 = "4,1"
        s43 = "4,3"
        all_edges[s12] = e12
        all_edges[s13] = e13
        all_edges[s21] = e21
        all_edges[s24] = e24
        all_edges[s31] = e31
        all_edges[s34] = e34
        all_edges[s41] = e41
        all_edges[s43] = e43

        edges_out = {}
        edges_out[1] = {2: e21.weight}
        edges_out[1].update({3: e13.weight})
        edges_out[2] = {1: e21.weight}
        edges_out[2].update({4: e24.weight})
        edges_out[3] = {1: e31.weight}
        edges_out[3].update({4: e34.weight})
        edges_out[4] = {1: e41.weight}
        edges_out[4].update({3: e43.weight})

        edges_in = {}
        edges_in[1] = {2: e21.weight}
        edges_in[1].update({3: e31.weight})
        edges_in[1].update({4: e41.weight})
        edges_in[3] = {1: e13.weight}
        edges_in.get(3).update({4: e43.weight})
        edges_in[4] = {2: e24.weight}
        edges_in.get(4).update({3: e34.weight})

        g1 = DiGraph(Nodes, edges_in, edges_out, all_edges)
        g1_algo = GraphAlgo(g1)

    def test_get_graph(self):
        self.assertEqual(g1, g1_algo.get_graph())

    def test_shortest_path(self):
        p12 = (1.21, [1, 2])
        p13 = (1.13, [1, 3])
        p14 = (2.45, [1, 2, 4])
        p21 = (1.21, [2, 1])
        p23 = (2.34, [2, 1, 3])
        p24 = (1.24, [2, 4])
        p31 = (1.31, [3, 1])
        p32 = (2.52, [3, 1, 2])
        p34 = (1.34, [3, 4])
        p41 = (1.41, [4, 1])
        p42 = (2.62, [4, 1, 2])
        p43 = (1.43, [4, 3])
        self.assertEqual(p12, g1_algo.shortest_path(1, 2))
        self.assertEqual(p13, g1_algo.shortest_path(1, 3))
        self.assertEqual(p14, g1_algo.shortest_path(1, 4))
        self.assertEqual(p21, g1_algo.shortest_path(2, 1))
        self.assertEqual(p23, g1_algo.shortest_path(2, 3))
        self.assertEqual(p24, g1_algo.shortest_path(2, 4))
        self.assertEqual(p31, g1_algo.shortest_path(3, 1))
        self.assertEqual(p32, g1_algo.shortest_path(3, 2))
        self.assertEqual(p34, g1_algo.shortest_path(3, 4))
        self.assertEqual(p41, g1_algo.shortest_path(4, 1))
        self.assertEqual(p42, g1_algo.shortest_path(4, 2))
        self.assertEqual(p43, g1_algo.shortest_path(4, 3))

    def test_TSP(self):
        lst1 = [1, 2, 3]
        lst2 = [2, 4]
        lst3 = [1, 4, 2]
        t1 = ([1, 2], 1.13)
        t2 = ([2, 4], 1.24)
        t3 = ([1, 2, 4], 1.21)
        self.assertEqual(t1, g1_algo.TSP(lst1))
        self.assertEqual(t2, g1_algo.TSP(lst2))
        self.assertEqual(t3, g1_algo.TSP(lst3))

    def test_centerPoint(self):
        self.assertEqual((2, 2.34), g1_algo.centerPoint())

    def test_get_Node_courdinates(self):
        self.assertEqual((1.1, 2.1), g1_algo.get_Node_courdinates(1))
