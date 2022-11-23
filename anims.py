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
        edges = [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4)]
        g = CustomGraph(vertices, edges)
        
        self.play(Create(g))
        self.wait()
        for edge in edges:
            g.create_edge_length(edge, 1, 0)

        self.play(g.show_edge_lengths(g.edges))
        g.setup_potentials()
        self.play(
            g.vertex_potentials[1].animate.set_value(1)
        )
        self.wait()

