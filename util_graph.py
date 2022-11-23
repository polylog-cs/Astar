import copy
import itertools
import random
import math
from manim import *
from util import *

class CustomGraph(Graph):

    edge_weights_vals = {} # edge -> float
    edge_weights_objs = {} # edge -> Decimal
    vertex_names = {} # vertex -> Tex
    vertex_potentials = {}

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

