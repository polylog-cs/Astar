import common.solarized as solarized

from common.directed_graph import *
from common.weighted_graph import *


class BFSGraph(WeightedGraph, DirectedGraph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.potentials = []
        for vertex in self.vertices:
            self.potentials.append(DecimalNumber(self[vertex].get_center()[2]))

    def animate_edge(self, vertices: [int], colour):
        print(vertices)
        edge_colours = {}
        vertex_colours = {}
        adj = self.get_adjacency_list()
        new_in_skeleton = set()
        for v1 in vertices:
            for v2 in adj[v1]:
                if v2 not in vertices and v2 not in new_in_skeleton and self[
                    v2].get_color().__str__() != colour.__str__():
                    new_in_skeleton.add(v2)
                    edge_colours[(v1, v2)] = colour
                    vertex_colours[v2] = colour
        self.set_colors(vertex_colors=vertex_colours, edge_colors=edge_colours)

    def create_arrow(self, start: int, end: int, is_half: bool):
        if is_half:
            return Arrow(
                start=self[start].get_center(),
                end=self[end].get_center() - ((self[end].get_center() - self[start].get_center()) / 2.0),
                color=RED,
                stroke_width=10
            ).scale(2)
        else:
            return Arrow(
                start=self[start].get_center(),
                end=self[end].get_center(),
                color=RED,
                stroke_width=10
            ).scale(1.3)

    def run_bfs(self, vertex: int, scene):
        self.set_colors(vertex_colors={vertex: solarized.RED})
        for anims in self.bfs_animation(vertex, visit_all_not_closed=True,
                                        anim_vertex_visit_fce=lambda start, end, is_half: self.create_arrow(start, end,
                                                                                                            is_half)):
            print(type(anims[0]))
            if len(anims) > 0 and isinstance(anims[0], int):
                self.animate_edge(anims, solarized.RED)
            else:
                scene.play(*anims)
