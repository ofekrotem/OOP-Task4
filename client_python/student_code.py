"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import math
from decimal import Decimal
import time

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15
g = DiGraph()
algo = GraphAlgo()
algo.load_from_json(client.get_graph())
pk = {}
center = str(algo.centerPoint()[0])
info = json.loads(client.get_info())
numOfAgents = int(info.get("GameServer").get("agents"))
client.add_agent("{\"id\":" + center + "}")
cur_grade = 0
old_grade = 0
cur_agents = 1
# this commnad starts the server - the game is running now
print(client.start())
print(client.start())
print(client.start())
print(client.start())
print(client.start())
print(client.start())
print(client.start())
print(client.start())
print(client.start())
print(client.start())
client.start()
client.start()
client.start()
print(client.is_running())
"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


def get_edge(pok_x: float, pok_y: float) -> (float, float):
    for e in graph.Edges:
        src = algo.get_Node_courdinates(e.src)
        dest = algo.get_Node_courdinates(e.dest)
        src_x = Decimal(str(src[0]))
        src_y = Decimal(str(src[1]))
        dst_x = Decimal(str(dest[0]))
        dst_y = Decimal(str(dest[1]))
        mone = src_y - dst_y
        mehane = src_x - dst_x
        m = mone / mehane
        n = dst_y - (m * dst_x)
        res = Decimal(str(pok_y)) - m * Decimal(str(pok_x))
        if math.fabs(n - res) < 0.0000001:
            return e.src, e.dest


def find_far_pok(pokemons: dict) -> int:
    ag = json.loads(client.get_agents()).get("Agents")
    MaxSrc = -1
    MaxDist = -1
    for i, po in pokemons.items():
        ed = get_edge(pokemons.get(i)[0], pokemons.get(i)[1])
        tempDist = 0
        for a in ag:
            if int(a.get("dest")) != -1:
                temp, tempList = algo.shortest_path(int(a.get("dest")), ed[0])
                tempDist += temp
            else:
                temp, tempList = algo.shortest_path(int(a.get("src")), ed[0])
                tempDist += temp
        if tempDist > MaxDist:
            MaxDist = tempDist
            MaxSrc = ed[0]
    return MaxSrc

while client.is_running() == 'true':
    cur_grade = int(info.get("GameServer").get("grade"))
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pk = {}
    i = 0
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        pk[i] = (x, y)
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
        i = i + 1
    if (cur_grade > old_grade and cur_agents < numOfAgents):
        old_grade = cur_grade
        cur_agents += 1
        if len(pk) > 0:
            if len(pk) == 1:
                client.add_agent("{\"id\":" + str(get_edge(pk[0][0], pk[0][1])[0]) + "}")
            else:
                client.add_agent("{\"id\":" + str(find_far_pok(pk)) + "}")
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]

    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            closestDist = math.inf
            next_node = agent.src
            i = 0
            for poke in pokemons:
                ed = get_edge(pk[i][0], pk[i][1])
                tempDist, tempList = algo.shortest_path(agent.src, int(ed[0]))
                if tempDist == 0:
                    next_node = int(ed[1])
                    break
                if tempDist < closestDist:
                    closestDist = tempDist
                    next_node = tempList[1]
                i = i + 1
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
    time.sleep(0.1)
# game over:
