import math
import random

from client_python.GraphInterface import GraphInterface


class Node:
    def __init__(self, id: int, x: float = None, y: float = None, z: float = None):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.tag = 0
        self.w = 0
        self.daddy = None

    def whos_my_daddy(self):
        return self.daddy

    def set_my_daddy(self, papa):
        self.daddy = papa

    def get_w(self) -> float:
        return self.w

    def set_w(self, we: float):
        self.w = we

    def get_id(self) -> int:
        return self.id

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    def get_z(self) -> float:
        return self.z

    def get_tag(self) -> int:
        return self.tag

    def set_tag(self, n_tag: int):
        self.tag = n_tag

    def __eq__(self, other):
        if ((self.id == other.id) and (self.tag == other.tag) and (self.x == other.x) and (self.y == other.y) and (
                self.z == other.z)):
            return True
        return False

    def __lt__(self, other):
        return self.w < other.w


class Edge:
    def __init__(self, src: Node, dest: Node, w: float):
        self.src = src
        self.dest = dest
        self.weight = w

    def get_src(self) -> Node:
        return self.src

    def get_dest(self) -> Node:
        return self.dest

    def get_weight(self) -> float:
        return self.weight

    def __eq__(self, other) -> bool:
        return self.src == other.src and self.dest == other.dest and self.weight == other.weight


class DiGraph(GraphInterface):
    """ Nodes: { node_id : Node }
        edgesIn: { node1_id : { node2_id : weight } }
        edgesOut: { node1_id : { node2_id : weight } }
        allEdges: { "node1_id , node2_id": Edge() }
    """

    def __init__(self, nodes: dict = {}, edgesIn: dict = {}, edgesOut: dict = {}, allEdges: dict = {}):
        self.nodes = nodes
        self.edgesIn = edgesIn
        self.edgesOut = edgesOut
        self.mc = 0
        self.allEdges = allEdges
        self.maxX = 100
        self.maxY = 100
        self.minX = 0
        self.minY = 0
        self.minZ = 0
        self.maxZ = 100
        if len(self.nodes) > 0:
            self.init_min_max()  # Initialize range to random determine x,y,z values for empty Node()

    def makeTagsZero(self):
        for k, n in self.nodes.items():
            n.set_tag(0)

    def get_min_max(self) -> (float, float, float, float):
        return self.minX, self.maxX, self.minY, self.maxY

    def DijkstraPrep(self, src: int):
        for k, n in self.nodes.items():
            if k == src:
                self.nodes.get(k).set_w(0)
            else:
                self.nodes.get(k).set_w(math.inf)

    def get_allEdges(self) -> dict:
        return self.allEdges

    def set_nodes(self, nodes: dict):
        self.nodes = nodes
        self.init_min_max()

    def set_allEdges(self, all: dict):
        self.allEdges = all

    def set_edgesIn(self, i: dict):
        self.edgesIn = i

    def set_edgesOut(self, q: dict):
        self.edgesOut = q

    def init_min_max(self):
        if (len(self.nodes) == 2):
            self.maxX = self.nodes.get(0).get_x()
            self.maxY = self.nodes.get(0).get_y()
            self.minX = self.nodes.get(1).get_x()
            self.minY = self.nodes.get(1).get_y()
            self.minZ = self.nodes.get(1).get_z()
            self.maxZ = self.nodes.get(0).get_z()
        for k, v in self.nodes.items():
            if (v.get_x() > self.maxX): self.maxX = v.get_x()
            if (v.get_x() < self.minX): self.minX = v.get_x()
            if (v.get_y() > self.maxY): self.maxY = v.get_y()
            if (v.get_y() < self.minY): self.minY = v.get_y()
            if (v.get_z() < self.minZ): self.minZ = v.get_z()
            if (v.get_z() > self.maxZ): self.maxZ = v.get_z()

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        return len(self.allEdges)

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self.edgesIn.get(id1)

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edgesOut.get(id1)

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if (not id1 in self.nodes or not id2 in self.nodes): return False
        e = Edge(self.nodes.get(id1), self.nodes.get(id2), weight)
        s = str(id1) + "," + str(id2)
        if s in self.allEdges:
            if weight == self.allEdges.get(s):
                return False
            else:
                self.allEdges.update({s: weight})
                if self.edgesOut.get(id1) is not None:
                    self.edgesOut.get(id1).update({id2: weight})
                else:
                    self.edgesOut[id1] = {id2: weight}
                if self.edgesIn.get(id2) is not None:
                    self.edgesIn.get(id2).update({id1: weight})
                else:
                    self.edgesIn[id2] = {id1, weight}
        else:
            self.allEdges.update({s: weight})
            if id1 in self.edgesOut:
                self.edgesOut.get(id1).update({id2: weight})
            else:
                self.edgesOut.update({id1: {id2: weight}})
            if id2 in self.edgesIn:
                self.edgesIn.get(id2).update({id1: weight})
            else:
                self.edgesIn.update({id2: {id1: weight}})
        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if (node_id in self.nodes):
            return False
        else:
            if (not pos):
                x = random.uniform(self.minX, self.maxX)
                y = random.uniform(self.minY, self.maxY)
                z = random.uniform(self.minZ, self.maxZ)
                pos = (x, y, z)

            n1 = Node(node_id, pos[0], pos[1], pos[2])
            self.nodes.update({node_id: n1})
            self.mc += 1
            self.init_min_max()
            return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodes:
            return False
        else:
            self.nodes.pop(node_id)
            if node_id in self.edgesOut:
                self.edgesOut.pop(node_id)
            if node_id in self.edgesIn:
                self.edgesIn.pop(node_id)
        self.init_min_max()
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        s = str(node_id1) + "," + str(node_id2)
        if s not in self.allEdges:
            return False
        else:
            self.allEdges.pop(s)
            if self.edgesOut.get(node_id1) is not None:
                self.edgesOut.get(node_id1).pop(node_id2)
            if self.edgesIn.get(node_id2) is not None:
                self.edgesIn.get(node_id2).pop(node_id1)
            self.mc += 1
            return True
