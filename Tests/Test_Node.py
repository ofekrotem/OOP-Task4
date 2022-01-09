import unittest

from client_python.DiGraph import Node

n = Node(0, 1.1, 2.2, 3.3)


class TestNode(unittest.TestCase):

    def test_get_id(self):
        id = n.get_id()
        self.assertEqual(id, 0)

    def test_get_x(self):
        x = n.get_x()
        self.assertEqual(x, 1.1)

    def test_get_y(self):
        y = n.get_y()
        self.assertEqual(y, 2.2)

    def test_get_z(self):
        z = n.get_z()
        self.assertEqual(z, 3.3)

    def test_get_tag(self):
        tag = n.get_tag()
        self.assertEqual(tag, 0)

    def test_set_tag(self):
        n.set_tag(3)
        tag = n.get_tag()
        self.assertEqual(tag, 3)


if __name__ == '__main__':
    unittest.main()
