from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.util import *
from utils.util_graph import *

class Tom(ThreeDScene):
    def construct(self):
        default()
        self.camera.background_color = BASE02
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False, rate = 0.3, weird_bug=False) # weird_bug = True
        self.add(europe_boundary, G, *[G.vertex_height_lines[v] for v in range(N_CITIES)]) #*[G.edges[e] for e in G.edges.keys()])

        self.move_camera(
            phi= 80 * DEGREES,
            zoom = 1.5,
            run_time=1,
        )
        
        G.disable_colors()
        air_potentials = G.gen_air_potentials(ROME)
        self.move_camera(
            theta= -140 * DEGREES,
            run_time=1,
            added_anims = [G.vertex_potentials[v].animate.set_value(air_potentials[v]) for v in G.vertices]
        )
        self.wait()

        self.play(
            *[FadeOut(G.vertex_height_lines[v]) for v in range(N_CITIES)]
        )
        self.wait()

        anims, lines, sp_nodes, sp_edges, _, _ = G.run_dijkstra(PRAGUE, ROME, 1)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.move_camera(
            theta= -60 * DEGREES,
            run_time=7,
            added_anims = [anims]
        )
        self.play(Flash(G.vertices[ROME], color = RED))

        self.wait()
        

