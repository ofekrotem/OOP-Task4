import subprocess
import sys
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
from pygame_widgets import *

# init pygame
from client_python.ImageControler import ImageControler

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
client = Client()
client.start_connection(HOST, PORT)
pygame.font.init()
pokemonsJson = client.get_pokemons()
pokemons_obj = json.loads(pokemonsJson, object_hook=lambda d: SimpleNamespace(**d))
INACTIVE_COLOR = (0, 255, 0)
ACTIVE_COLOR = (255, 0, 0)

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


def get_edge(pok_x: float, pok_y: float, t: int) -> (float, float):
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
        if e.src < e.dest:
            flag = True
        else:
            flag = False
        if math.fabs(n - res) < 0.0000001:
            if t > 0:
                if flag:
                    return e.src, e.dest
                else:
                    return e.dest, e.src
            else:
                if flag:
                    return e.dest, e.src
                else:
                    return e.src, e.dest


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def find_far_pok(pK: dict) -> int:
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    MaxSrc = -1
    MaxDist = -1
    for i, po in pK.items():
        ed = get_edge(pK.get(i)[0], pK.get(i)[1], pk.get(i)[2])
        tempDist = 0
        for k in range(0, len(agents)):
            if int(agents[k].dest) != -1:
                temp, tempList = algo.shortest_path(int(agents[k].dest), ed[0])
                tempDist += temp
            else:
                temp, tempList = algo.shortest_path(int(agents[k].src), ed[0])
                tempDist += temp
        if tempDist > MaxDist:
            MaxDist = tempDist
            MaxSrc = ed[0]
    return MaxSrc


def draw_button(button, screen):
    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback):
    """A button is a dictionary that contains the relevant data.

    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf = FONT.render(text, True, (255, 255, 255))
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        'callback': callback,
    }
    return button


def stop_Game():
    client.stop()
    pygame.quit()
    exit(0)


b = Rect(432, 7, 70, 40)
button = create_button(b.x+530, b.y, 100, 40, 'Quit Game!', stop_Game)

radius = 15
g = DiGraph()
algo = GraphAlgo()
algo.load_from_json(client.get_graph())
center = str(algo.centerPoint()[0])
info = json.loads(client.get_info())
numOfAgents = int(info.get("GameServer").get("agents"))
client.add_agent("{\"id\":" + center + "}")
pokemons = json.loads(client.get_pokemons(),
                      object_hook=lambda d: SimpleNamespace(**d)).Pokemons
pk = {}
i = 0
pokemons = [p.Pokemon for p in pokemons]
for p in pokemons:
    x, y, _ = p.pos.split(',')
    pk[i] = (x, y, int(p.type))
    i = i + 1

if numOfAgents > 1:
    for i in range(1, numOfAgents):
        if len(pk) > 0:
            if len(pk) == 1:
                client.add_agent("{\"id\":" + str(get_edge(pk[0][0], pk[0][1], p.type)[0]) + "}")
            else:
                client.add_agent("{\"id\":" + str(find_far_pok(pk)) + "}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
sc = 0
print((Decimal(client.time_to_end()) / 1000))
pics = ImageControler(WIDTH, HEIGHT)
bg = pics.background_images[0]
buttons_collor = (184, 15, 10)
while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pk = {}
    i = 0
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        pk[i] = (x, y, int(p.type))
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
        i = i + 1

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]

    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            stop_Game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                # `event.pos` is the mouse position.
                if button['rect'].collidepoint(event.pos):
                    # Increment the number by calling the callback
                    # function in the button list.
                    button['callback']()
        elif event.type == pygame.MOUSEMOTION:
            # When the mouse gets moved, change the color of the
            # buttons if they collide with the mouse.
            if button['rect'].collidepoint(event.pos):
                button['color'] = ACTIVE_COLOR
            else:
                button['color'] = INACTIVE_COLOR
    # refresh surface
    screen.fill(Color(0, 0, 0))
    screen.blit(bg, (0, 0))
    # time
    timeleft = Decimal(client.time_to_end()) / 1000
    timelabel = FONT.render(f"Time Left: {int(timeleft)}", True, buttons_collor)
    rect = timelabel.get_rect(center=(70, 10))
    screen.blit(timelabel, rect)

    # score
    info = json.loads(client.get_info())
    score = info.get("GameServer")["grade"]
    scorelabel = FONT.render(f"Score: {score}", True, buttons_collor)
    rect = scorelabel.get_rect(center=(200, 10))
    screen.blit(scorelabel, rect)

    # moves
    moves = info.get("GameServer")["moves"]
    moveslabel = FONT.render(f"Moves: {moves}", True, buttons_collor)
    rect = moveslabel.get_rect(center=(300, 10))
    screen.blit(moveslabel, rect)

    # # stop game button
    # if 432 <= mouse[0] <= 432 + 140 and 7 <= mouse[1] <= 30:
    #     pygame.draw.rect(screen, (255, 255, 255), [432, 7, 120, 30])
    #     screen.blit(stop, (400 + 50, 10))
    # else:
    #     # superimposing the text onto our button
    #     screen.blit(stop, (400 + 50, 10))
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

        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    i = 0
    for agent in agents:
        screen.blit(pics.agentsImages[i], (int(agent.pos.x), int(agent.pos.y)))
        i += 1

    i = 0
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        screen.blit(pics.pokImages[i % len(pokemons)], (int(p.pos.x), int(p.pos.y)))
        i += 1

    # update screen changes
    draw_button(button, screen)
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
                ed = get_edge(pk[i][0], pk[i][1], pk[i][2])
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
