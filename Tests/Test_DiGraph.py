from unittest import TestCase

from client_python.DiGraph import DiGraph, Edge, Node

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


class TestGraph(TestCase):

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

    def test_v_size(self):
        self.assertEqual(4, g1.v_size())

    def test_e_size(self):
        self.assertEqual(8, g1.e_size())

    def test_get_all_v(self):
        nodes = g1.get_all_v()
        self.assertEqual(n1, nodes[1])
        self.assertEqual(n2, nodes[2])
        self.assertEqual(n3, nodes[3])
        self.assertEqual(n4, nodes[4])

    def test_all_in_edges_of_node(self):
        data = g1.all_in_edges_of_node(1)
        self.assertEqual(data[2], edges_in[1].get(2))
        self.assertEqual(data[3], edges_in[1].get(3))
        self.assertEqual(data[4], edges_in[1].get(4))

    def test_all_out_edges_of_node(self):
        data = g1.all_out_edges_of_node(3)
        self.assertEqual(data[1], edges_out[3].get(1))
        self.assertEqual(data[4], edges_out[3].get(4))

    def test_get_mc(self):
        self.assertEqual(0, g1.get_mc())

    def test_add_edge(self):
        self.assertEqual(False, g1.add_edge(1, 2, 1.12))
        self.assertEqual(True, g1.add_edge(1, 4, 1.14))

    def test_add_node(self):
        self.assertEqual(False, g1.add_node(1))
        self.assertEqual(True, g1.add_node(5, (12, 12, 12)))

    def test_remove_node(self):
        self.assertEqual(False, g1.remove_node(15))
        self.assertEqual(True, g1.remove_node(2))

    def test_remove_edge(self):
        self.assertEqual(True, g1.remove_edge(1, 2))
        self.assertEqual(False, g1.remove_edge(1, 4))
