from unittest import TestCase

from client_python.DiGraph import Edge, Node

n1 = Node(0, 1.1, 2.2, 3.3)
n2 = Node(1, 2.2, 4.4, 6.6)
e = Edge(n1, n2, 1.5)


class TestEdge(TestCase):
    def test_get_src(self):
        self.assertEqual(n1, e.get_src())

    def test_get_dest(self):
        self.assertEqual(n2, e.get_dest())

    def test_get_weight(self):
        self.assertEqual(1.5, e.get_weight())
