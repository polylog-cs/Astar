#from os import startfile

from manim import *

from Bfs import *


example_vertices = list(range(1, 14))
example_edges = [
    (1, 2),
    (1, 11),
    (2, 3),
    (2, 4),
    (2, 5),
    (3, 4),
    (4, 5),
    (4, 10),
    (4, 11),
    (5, 6),
    (5, 7),
    (5, 8),
    (1, 9),
    (9, 10),
    (9, 11),
    (9, 12),
    (10, 11),
    (11, 12),
    (12, 13),
]


scene_width = 14.2
tree_scale = 3
node_radius = 0.2
arrow_width = 10


class WeightedAnim(Scene):
    def construct(self):
        g = BFSGraph(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": GRAY},  # for debugging
            labels=False,  # for debugging
            edge_config={"color": text_color},
        )
        self.play(
            DrawBorderThenFill(g)
        )

        changes = []
        i = 0.5

        for edge in example_edges:
            changes.append((edge, (i, 2 * UP)))
            i += 0.4

        print(changes)

        g.create_edge_lengths(changes)

        self.wait(5)

        self.play(
            g.show_edge_lengths(example_edges)
        )

        self.wait(5)

        self.play(
            g.hide_edge_lengths(example_edges)
        )
        self.wait(5)


class BFSAnim(Scene):
    def construct(self):
        g = BFSGraph(
            example_vertices,
            example_edges,
            layout="kamada_kawai",
            layout_scale=tree_scale,
            vertex_config={"radius": node_radius, "color": GRAY},  # for debugging
            labels=False,  # for debugging
            edge_config={"color": text_color},
        )
        self.play(
            DrawBorderThenFill(g)
        )

        g.run_bfs(1, self)

        self.wait(10)