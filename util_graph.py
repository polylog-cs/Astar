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

    def get_adjacency_list(self):
        adj = dict([(v, []) for v in self.vertices])
        for v1, v2 in self.edges:
            adj[v1].append(v2)
            if not self.directed:
                adj[v2].append(v1)

        return adj

    def neighbors(self, vertex):
        return self.get_adjacency_list()[vertex]


    def create_name(self, vertex, name, offset):
        self.vertex_names[vertex] = Tex(name, color=GRAY).move_to(vertex.get_center()).shift(offset)
        self.vertex_names[vertex].add_updater(
            lambda mob: mob.move_to(vertex.get_center()).shift(offset)
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


    def create_edge_length(self, edge, weight, offset):
        number = DecimalNumber(weight, color = GRAY)
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

    def setup_potentials(self):
        # updater: edge_length = original_edge_length + potential(v) - potential(u)
        # ideally (but maybe hard), add also updater on the color, so that when it decreases/increases it gets a shade of green/red based on how fast it increases/decreases
        for v in self.vertices:
            self.vertex_potentials[v] = ValueTracker(0)
            self.vertices[v].add_updater(
                lambda mob, v=v: mob.move_to(
                    [
                        mob.get_center()[0],
                        mob.get_center()[1],
                        self.vertex_potentials[v].get_value()
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

    def add_directed_edge(self, u, v, offset = 0, weight = 1, offset_weight = 0):
        def compute_positions(u, v, offset):
            vec = self.vertices[v].get_center() - self.vertices[u].get_center()
            vec = vec / np.linalg.norm(vec)

            start_angle = np.arcsin(offset / (self.vertices[u].get_right() - self.vertices[u].get_center())[0])
            start_vec = np.array([
                vec[0] * np.cos(start_angle) + vec[1] * np.sin(start_angle),
                vec[1] * np.cos(start_angle) - vec[0] * np.sin(start_angle),
                0
            ])
            start_pos = self.vertices[u].get_center() + start_vec * (self.vertices[u].get_right() - self.vertices[u].get_center())[0]


            end_angle = -np.arcsin(offset / (self.vertices[v].get_right() - self.vertices[v].get_center())[0])
            end_vec = np.array([
                -vec[0] * np.cos(end_angle) - vec[1] * np.sin(end_angle),
                -vec[1] * np.cos(end_angle) + vec[0] * np.sin(end_angle),
                0
            ])
            end_pos = self.vertices[v].get_center() + end_vec * (self.vertices[v].get_right() - self.vertices[v].get_center())[0]
            return (start_pos, end_pos)

        (start_pos, end_pos) = compute_positions(u, v, offset)
        
        edge = Arrow(
            start = start_pos,
            end = end_pos,
            buff = 0,
            color = GRAY
        )

        self.edges[(u,v)] = edge
        def edge_updater(mob):
            start_pos, end_pos = compute_positions(u, v, offset)
            mob.put_start_and_end_on(start_pos, end_pos)

        edge.add_updater(edge_updater)
        edge.put_start_and_end_on(start_pos, end_pos)

        self.create_edge_length((u,v), weight, offset_weight)

        return AnimationGroup(Create(edge))

    def run_dijkstra(self, start, end, speed):
        # initialize potentials and weights to default values to be sure
        for edge in self.edges:
            if not edge in self.edge_weights_vals:
                self.edge_weights_vals[edge] = 1

        for vert in self.vertices:
            if not vert in self.vertex_potentials:
                self.vertex_potentials[vert] = 0

        # run A*
        all_anims = []

        G = self.get_adjacency_list()
        q = PriorityQueue()
        q.put((0, start, -1))
        
        visited = set()

        while not q.empty():
            (dist, node, predecessor) = q.get()
            if not node in visited:
                visited.add(node)

                if predecessor != -1:
                    all_anims.append(
                        Succession(
                            Wait(dist * speed),
                            self.edges[(predecessor, node)].animate.set_color(RED)
                        )
                    )

                for neighbor in G[node]:
                    if not neighbor in visited:
                        edge = (node, neighbor)
                        if self.directed == False:
                            edge = (min(node, neighbor), max(node, neighbor))

                        new_dist = dist + self.edge_weights_vals[edge] + self.vertex_potentials[neighbor].get_value() - self.vertex_potentials[node].get_value()
                        q.put((new_dist, neighbor, node))

                        mover = Circle(radius = 0.1, color = RED).move_to(self.vertices[node].get_center())
                        all_anims.append(
                            Succession(
                                Wait(dist * speed),
                                AnimationGroup(
                                    mover.animate.move_to(self.vertices[neighbor].get_center()),
                                    run_time = ( dist + self.edge_weights_vals[edge] + self.vertex_potentials[neighbor].get_value() - self.vertex_potentials[node].get_value() ) * speed,
                                )
                            ) # TODO fix
                        )

        return AnimationGroup(*all_anims)
        

