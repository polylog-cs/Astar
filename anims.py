from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

import solarized
from util import *
from util_graph import *

class Polylog(Scene):
    def construct(self):
        authors = Tex(
            r"\textbf{Tom Gavenčiak, Václav Rozhoň, Václav Volhejn}", 
            color=text_color,
            font_size = 40,
        ).shift(
            3*DOWN + 0*LEFT
        )

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)


        self.play(
           Write(authors),
           Write(channel_name)
        )

        self.wait()

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

class Explore(Scene):
    def construct(self):

        # self.move_camera(
        #     phi=75 * DEGREES,
        # )

        vertices = [1, 2, 3, 4]
        g = CustomGraph(vertices, [])
        
        self.play(Create(g))
        self.wait()

        self.play(g.add_directed_edge(1, 4, 0.05))
        self.play(g.add_directed_edge(4, 1, -0.05))
        self.play(g.add_directed_edge(1, 2, 0.0))
        self.play(g.add_directed_edge(1, 3, 0.0))
        self.play(g.add_directed_edge(4, 2, 0.0))

        self.play(g.vertices[1].animate.shift(2*RIGHT))
        self.play(g.vertices[4].animate.scale(5))
        self.wait()

        self.play(g.show_edge_lengths(g.edges))
        self.wait()

        g.setup_potentials()
        self.play(
            g.vertex_potentials[4].animate.set_value(-0.5)
        )
        self.wait()

        self.play(
            g.run_dijkstra(1, 2, 1)
        )
        self.wait(5)

        return
        for edge in edges:
            g.create_edge_length(edge, 1, 0)

        self.play(g.show_edge_lengths(g.edges))
        
class Chapter3(Scene):
    def construct(self):
        pass