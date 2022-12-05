import copy
import itertools
import random
import math
from manim import *
from util import *
from queue import PriorityQueue

class CustomGraph(Graph):

    edge_weights_vals = {} # edge -> float
    edge_weights_objs = {} # edge -> Decimal
    vertex_names = {} # vertex -> Tex
    vertex_potentials = {}
    directed = True

    def make_directed(self, directed):
        self.directed = directed

    def get_adjacency_list(self):
        adj = dict([(v, []) for v in self.vertices])
        for v1, v2 in self.edges:
            adj[v1].append(v2)
            if not self.directed:
                adj[v2].append(v1)

        return adj

    def neighbors(self, vertex):
        return self.get_adjacency_list()[vertex]


    def create_name(self, vertex, name, offset, scale = 0.5):
        self.vertex_names[vertex] = Tex(name, color=GRAY).scale(scale).move_to(self.vertices[vertex].get_center()).shift(offset)
        self.vertex_names[vertex].add_updater(
            lambda mob: mob.move_to(self.vertices[vertex].get_center()).shift(offset)
        )

    def show_names(self, vertices):
        # shows selected vertex names
        anims = []
        for v in vertices:
            anims.append(FadeIn(self.vertex_names[v]))
        return AnimationGroup(*anims)

    def hide_names(self, vertices):
        # hides selected vertex names
        anims = []
        for v in vertices:
            anims.append(FadeOut(self.vertex_names[v]))
        return AnimationGroup(*anims)


    def create_edge_length(self, edge, weight, offset = 0*RIGHT):
        number = DecimalNumber(
            weight, 
            num_decimal_places=1,
            color = GRAY
        ).scale(0.5)
        self.edge_weights_objs[edge] = number
        self.edge_weights_vals[edge] = weight
        number.move_to(self.edges[edge].get_center()).shift(offset)
        number.add_updater(
            lambda mob: mob.move_to(self.edges[edge].get_center()).shift(offset)
        )

    def show_edge_lengths(self, edges):
        anims = []
        for e in edges:
            anims.append(
                FadeIn(self.edge_weights_objs[e])
            )
        return AnimationGroup(*anims)

    def hide_edge_lengths(self, edges):
        anims = []
        for e in edges:
            anims.append(FadeOut(self.edge_weights_objs[e]))
        return AnimationGroup(*anims)

    def change_edge_length(self, edge, change, new_color):
        return AnimationGroup(
            self.edges[edge].animate().set_color(new_color),
            self.edge_weights_objs[edge].animate().increment_value(change),
        )

    def setup_potentials(self, potentials = {}, rate = 1):
        # updater: edge_length = original_edge_length + potential(v) - potential(u)
        # ideally (but maybe hard), add also updater on the color, so that when it decreases/increases it gets a shade of green/red based on how fast it increases/decreases
        for v in self.vertices:
            self.vertex_potentials[v] = ValueTracker(0)
            if v in potentials:
                self.vertex_potentials[v] = ValueTracker(potentials[v])

            self.vertices[v].add_updater(
                lambda mob, v=v: mob.move_to(
                    [
                        mob.get_center()[0],
                        mob.get_center()[1],
                        self.vertex_potentials[v].get_value() * rate
                    ]
                )
            )

        for edge in self.edges:
            self.edge_weights_objs[edge].add_updater(
                lambda mob, edge = edge: mob.set_value(
                    self.edge_weights_vals[edge] 
                    + self.vertex_potentials[edge[1]].get_value()
                    - self.vertex_potentials[edge[0]].get_value()
                )
            )

    def gen_zero_potentials(self):
        pots = {}
        for v in self.vertices:
            pots[v] = 0
        return pots

    def gen_air_potentials(self, source):
        pots = {}
        for v in self.vertices:
            pots[v] = np.linalg.norm(self.vertices[v].get_center() - self.vertices[source].get_center())
        return pots


    def set_new_potentials(self, potentials):
        for v, pot in potentials.items():
            self.vertex_potentials[v].set_value(pot)

    def anim_new_potentials(self, new_potentials):
        anims = []
        for v, pot in new_potentials.items():
            anims.append(self.vertex_potentials[v].animate.set_value(pot))
        return AnimationGroup(*anims)

    def add_directed_edge(self, u, v, offset = 0, weight = 1, offset_weight = 0):
        def compute_positions(u, v, offset):
            #TODO vyhezkat
            return (self.vertices[u].get_center() + offset, self.vertices[v].get_center() + offset)
            
        start_pos, end_pos = compute_positions(u, v, offset)

        edge = Arrow(
            start = start_pos,
            end = end_pos,
            buff = 0,
            stroke_width=1,
            tip_length = 0.13,
            color = GRAY,
        )

        self.edges[(u,v)] = edge
        def edge_updater(mob):
            start_pos, end_pos = compute_positions(u, v, offset)
            mob.put_start_and_end_on(start_pos, end_pos)

        edge.add_updater(edge_updater)
        edge.put_start_and_end_on(start_pos, end_pos)

        self.create_edge_length((u,v), weight, offset_weight)

        return AnimationGroup(Create(edge))

    def run_dijkstra(self, start_node, end_node, speed):
        # initialize potentials and weights to default values to be sure
        for edge in self.edges:
            if not edge in self.edge_weights_vals:
                self.edge_weights_vals[edge] = 1
            # u, v = edge
            # if (not self.directed) and not (v, u) in self.edge_weights_vals:
            #     self.edge_weights_vals[(v,u)] = 1

        for vert in self.vertices:
            if not vert in self.vertex_potentials:
                self.vertex_potentials[vert] = ValueTracker(0)

        # run A*
        all_anims = []

        G = self.get_adjacency_list()
        q = PriorityQueue()
        q.put((0, start_node, -1))
        
        distances = {}
        predecessors = {}

        mover_anims = []
        while not q.empty():
            (dist, node, predecessor) = q.get()
            if not node in distances:
                distances[node] = dist
                predecessors[node] = predecessor

                if predecessor != -1:
                    pass
                    # all_anims.append(
                    #     Succession(
                    #         Wait(dist * speed),
                    #         self.edges[(predecessor, node)].animate.set_color(RED)
                    #     )
                    # )

                for neighbor in G[node]:
                    if not neighbor in distances:
                        edge = (node, neighbor)
                        
                        new_dist = dist + self.edge_weights_vals[edge] + self.vertex_potentials[neighbor].get_value() - self.vertex_potentials[node].get_value()
                        q.put((new_dist, neighbor, node))

                        mover = Circle(radius = 0.1, color = RED).move_to(self.vertices[node].get_center())
                        mover_anims.append(
                            (
                                self.vertices[node].get_center(), 
                                self.vertices[neighbor].get_center(), 
                                dist, 
                                dist + self.edge_weights_vals[edge] + self.vertex_potentials[neighbor].get_value() - self.vertex_potentials[node].get_value(),
                                node,
                                neighbor
                            )
                        )

        shortest_path_nodes = [end_node]
        shortest_path_edges = []

        node = end_node
        while node != start_node:
            pred = predecessors[node]
            shortest_path_nodes.append(pred)
            shortest_path_edges.append((pred, node))
            shortest_path_edges.append((node, pred))
            node = pred

        all_lines = []
        for anim in mover_anims:
            (start_pos, end_pos, start_time, end_time, node, neighbor) = anim
            #finish_time = min(finish_time, distances[end_node])
            if start_time >= distances[end_node]:
                continue
            if end_time >= distances[end_node]:
                ratio = (distances[end_node] - start_time) *1.0 / (end_time - start_time)
                end_time = start_time + ratio * (end_time - start_time)
                end_pos = ratio * end_pos + (1-ratio) * start_pos

            line = Line(
                    start = start_pos,
                    end = end_pos,
                    buff = 0,
                    color = RED,
                    z_index = 1000
                )
            all_anims.append(
                Succession(
                    Wait(start_time * speed),
                    AnimationGroup(
                        Create(line, rate_functions = "linear"), # TODO na zacatku je wait
                        run_time = ( end_time - start_time ) * speed,
                    )
                )
            )
            print(node, neighbor, start_time, end_time)
            all_lines.append(line)

        return (
            AnimationGroup(*all_anims),
            all_lines,
            shortest_path_nodes,
            shortest_path_edges
        )
        

