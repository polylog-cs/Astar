from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

import solarized
from util import *

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
