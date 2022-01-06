import heapq
import json
import math
import os.path
import random
from types import SimpleNamespace
from typing import List

from DiGraph import Node, Edge, DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: GraphInterface = None):
        self.graph = graph;

    def get_graph(self) -> GraphInterface:
        return self.graph;

    def set_graph(self, g: GraphInterface):
        self.graph = g

    def load_from_json(self, file_name: str) -> bool:
        data = json.loads(
            file_name, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        Nodes = {}
        a = []
        for n in data.Nodes:
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))
            nodee = Node(n.id, n.pos.x, n.pos.y, 0)
            Nodes.update({n.id: nodee})
        allEdges = {}
        edgesIn = {}
        edgesOut = {}

        for e in data.Edges:
            ed = Edge(Nodes.get(e.src), Nodes.get(e.dest), e.w)
            s = str(e.src) + "," + str(e.dest)
            allEdges.update({s: ed})
            if e.src in edgesOut:
                edgesOut.get(e.src).update({e.dest: e.w})
            else:
                edgesOut.update({e.src: {e.dest: e.w}})
            if e.dest in edgesIn:
                edgesIn.get(e.dest).update({e.src: e.w})
            else:
                edgesIn.update({e.dest: {e.src: e.w}})
        if self.graph is None:
            g = DiGraph(Nodes, edgesIn, edgesOut, allEdges)
            self.set_graph(g)
        else:
            self.get_graph().set_nodes(Nodes)
            self.graph.set_allEdges(allEdges)
            self.graph.set_edgesIn(edgesIn)
            self.graph.set_edgesOut(edgesOut)

    def save_to_json(self, file_name: str) -> bool:
        nodes = []
        for k, n in self.graph.get_all_v().items():
            pos = str(n.get_x()) + "," + str(n.get_y()) + "," + str(n.get_z())
            Nid = n.get_id()
            nodes.append({"pos": pos, "id": Nid})
        edges = []
        for k, e in self.graph.get_allEdges().items():
            src = e.get_src().get_id()
            dst = e.get_dest().get_id()
            w = e.get_weight()
            edges.append({"src": src, "w": w, "dest": dst})

        data = {"Edges": edges, "Nodes": nodes}
        with open(file_name, "w") as outfile:
            json.dump(data, outfile)

    def Dijkstra(self, startID: int, allNodes: dict):
        start = self.graph.get_all_v().get(startID)
        tor = [start]
        daddymap = {startID: start}
        for k, n in self.graph.get_all_v().items():
            if n.get_id() != startID:
                daddymap[k] = n
        while len(tor) > 0:
            curr = tor[0]
            if self.graph.all_out_edges_of_node(curr.get_id()) is not None:
                for k, v in self.graph.all_out_edges_of_node(curr.get_id()).items():
                    if daddymap[k].get_tag() == 0:
                        total_length = curr.get_w() + v
                        curr_w = daddymap[k].get_w()
                        if curr_w > total_length:
                            daddymap[k].set_w(total_length)
                            daddymap[k].set_my_daddy(allNodes.get(curr.get_id()))
                            heapq.heappush(tor, daddymap[k])
            curr.set_tag(1)
            heapq.heappop(tor)
        return daddymap

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.graph is None:
            return math.inf, []
        allNodes = self.graph.get_all_v()
        if allNodes.get(id1) is None or allNodes.get(id2) is None:
            return math.inf, []
        if id1 == id2:
            return 0, [id2]
        self.graph.makeTagsZero()
        self.graph.DijkstraPrep(id1)
        check = self.Dijkstra(id1, allNodes)
        if check[id2].get_tag() == 0:
            return math.inf, []
        temp = []
        curr = check[id2]
        while curr.get_id() != id1:
            temp.append(allNodes.get(curr.get_id()))
            curr = check[curr.whos_my_daddy().get_id()]
        ans = []
        ans.append(id1)
        while len(temp) > 0:
            ans.append(temp.pop().get_id())

        return check[id2].get_w(), ans

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if len(node_lst) == 0:
            return None
        if len(node_lst) == 1:
            return node_lst
        full_path = []
        curr = []
        sum = 0
        curr_ind = node_lst.pop(0)
        flag = False
        last = node_lst[len(node_lst) - 1]
        while len(node_lst) > 0:
            next_ind = 0
            remove_ind = 0
            min_w = math.inf
            for i in range(len(node_lst)):
                (s_p_l, p_s_i) = self.shortest_path(curr_ind, node_lst[i])
                if min_w > s_p_l:
                    min_w = s_p_l
                    next_ind = i
                    remove_ind = i
                    flag = True
                    curr = p_s_i
                    if node_lst[i] == last:
                        sum = min_w
            if not flag:
                return None
            flag = False
            curr_ind = next_ind
            node_lst.pop(remove_ind)
            full_path = curr.copy()

        full_path = list(dict.fromkeys(full_path))
        return full_path, sum

    def centerPoint(self) -> (int, float):
        totalmaxDist = {}
        for src in self.graph.get_all_v().values():
            tempdist = -1
            for dest in self.graph.get_all_v().values():
                sp = self.shortest_path(src.get_id(), dest.get_id())[0]
                if sp > tempdist:
                    tempdist = sp
            totalmaxDist.update({src.get_id(): tempdist})
        maxdist = math.inf
        index = -1
        for k, v in totalmaxDist.items():
            if v < maxdist:
                maxdist = v
                index = k
        return index, maxdist

    def get_Node_courdinates(self, id: int) -> (float, float):
        for i, n in self.graph.get_all_v().items():
            if i == id:
                return n.get_x(), n.get_y()
        return None
