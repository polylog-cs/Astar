from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.util import *
from utils.util_graph import *

class Thanks(Scene):
    def construct(self):#TODO správný lidi
        s = [
            "Big thanks to",
            "-- 3blue1brown and Manim Community for Manim",
            "-- csha, Jindra Dušek, Martin Dvořák, Bernhard Haeupler, Florian Haeupler,",
            "Richard Hladík, Filip Hlásek, Aranka Hrušková, Yannic Maus, Jan Petr, ",
            "Hanka Rozhoňová, Jukka Suomela, Jan Volhejn, Vojtěch Volhejn, ",
            "Tung Anh Vu, Vilas Winstein",
            "See video description for links and some more related math. :)",
        ]
        t = [
            Tex(ss, color = text_color) for ss in s
        ]
        # for i in range(3, len(t)):
        #     t[i].scale(0.7)
        t[0].move_to(5*LEFT + 3*UP)
        t[1].next_to(t[0], DOWN).align_to(t[0], LEFT)
        t[2].next_to(t[1], DOWN).align_to(t[0], LEFT)
        t[3].scale(0.7).next_to(t[2], DOWN).align_to(t[0], LEFT)
        t[4].scale(0.7).next_to(t[3], DOWN).align_to(t[0], LEFT)
        t[5].scale(0.7).next_to(t[4], DOWN).align_to(t[0], LEFT)
        t[6].scale(0.7).next_to(t[5], DOWN).align_to(t[0], LEFT)
        t[7].move_to(t[5].get_center()[1]*UP + 2*DOWN)

        self.play(
            *[FadeIn(tt) for tt in t]
        )
        self.wait()
        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

class Intro(Scene):
    def construct(self):
        default()
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE)
        self.play(
            FadeIn(background), 
            FadeIn(europe_boundary), 
            FadeIn(G),
        )
        self.wait()
        
        # Dijkstra
        G.set_new_potentials(G.gen_zero_potentials())
        dijkstra_headline = tex_dijkstra_headline()
        self.play(FadeIn(dijkstra_headline))
        self.wait()
        tex_rome = rome_tex_name(G)
        tex_prague = prague_tex_name(G)
        self.play(
            FadeIn(tex_rome),
            FadeIn(tex_prague)
        )
        self.wait()

        for v in G.vertices.values():
            v.save_state()
        anims, lines, sp_nodes, sp_edges, _, red_nodes = G.run_dijkstra(0, 1, 1)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.play(
            anims
        )
        self.play(Flash(G.vertices[ROME], color = RED))
        self.wait()
        self.play(
            *[FadeOut(line) for (edge, line) in lines.items() if edge not in sp_edges],
            *[dot.animate.restore() for (v, dot) in G.vertices.items() if v not in sp_nodes]
        )
        self.wait()

        circle = Circle(
            radius = 1.1 * np.linalg.norm(G.vertices[PRAGUE].get_center() - G.vertices[ROME].get_center()),
            fill_opacity = 0.3,
            fill_color = RED,
            z_index = 10000,
            ).move_to(G.vertices[PRAGUE].get_center())

        self.play(
            *[FadeIn(line) for (edge, line) in lines.items() if edge not in sp_edges],
            *[G.vertices[dot].animate.set_color(RED) for dot in red_nodes],
            FadeIn(circle)
        )
        self.wait()

        
        self.play(
            FadeOut(circle),
            *[FadeOut(line) for line in lines.values()],
            *[dot.animate.restore() for dot in G.vertices.values()],
        )
        self.wait()

        a_headline = tex_astar_headline()
        self.play(
            Transform(dijkstra_headline[0], a_headline[0]),
            Transform(dijkstra_headline[1], a_headline[1])
            )

        #A*

        # show city positions
        self.play(
            G.show_names(range(N_CITIES)),
            *[FadeOut(edge) for edge in G.edges.values()],
        )
        self.wait()
        self.play(
            G.hide_names(range(N_CITIES)),
            *[FadeOut(edge) for edge in G.edges.values()],
        )
        self.wait()

        # run A*

        G.disable_heights()
        G.disable_colors()
        G.set_new_potentials(G.gen_air_potentials(ROME))
        anims, lines, sp_nodes, sp_edges, _, red_nodes = G.run_dijkstra(0, 1, 3)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.play(
            anims
        )
        self.play(Flash(G.vertices[ROME], color = RED))
        self.wait()
        
        ellipse = Ellipse(
            width = 1.2 * np.linalg.norm(G.vertices[PRAGUE].get_center() - G.vertices[ROME].get_center()),
            height = 0.6 * np.linalg.norm(G.vertices[PRAGUE].get_center() - G.vertices[ROME].get_center()),
            fill_opacity = 0.3,
            fill_color = RED,
            z_index = 10000,
            ).rotate((-10.0 - 90.0)/360*2*PI).move_to(0.6 * G.vertices[PRAGUE].get_center() + 0.4 * G.vertices[ROME].get_center())
        self.play(
            FadeIn(ellipse)
        )
        self.wait()

        self.play(
            *[FadeOut(line) for line in lines.values()],
            FadeOut(ellipse),
            FadeOut(dijkstra_headline),
            FadeOut(tex_rome),
            FadeOut(tex_prague)
        )
        self.wait()

class Polylog(Scene):
    def construct(self):
        default()
        authors = Tex(
            r"\textbf{Filip Hlásek, Václav Rozhoň, Václav Volhejn}", 
            color=text_color,
            font_size = 40,
        ).shift(
            3*DOWN + 0*LEFT
        )

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)

        logo_solarized = ImageMobject("img/logo-solarized.png").scale(0.032).move_to(2 * LEFT + 1 * UP + 0.55 * RIGHT)
        self.play(
           Write(authors),
           Write(channel_name), 
        )
        self.play(
            FadeIn(logo_solarized)
        )

        self.wait()

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()

        
class Chapter11(MovingCameraScene):
    def construct(self):
        self.next_section(skip_animations=False)
        default()
        # The problem we are trying to solve is how to speed up Dijkstra’s algorithm by somehow giving it whatever additional information we know about our graph. For example, in the specific case of our map, we have the additional information of knowing the geographical position of every city. The hard part is how to incorporate this information.
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE)
        self.play(
            FadeIn(background), 
            FadeIn(europe_boundary), 
            FadeIn(G),
        )
        self.wait()
        # self.play(
        #     G.show_names(range(N_CITIES))
        # )
        # self.wait()
        # self.play(
        #     G.hide_names(range(N_CITIES))
        # )
        # # for i in range(N_CITIES):
        # #     self.add(Tex(i).move_to(G.vertices[i].get_center()))
        # self.wait()

        # We could now look at the implementation of Dijkstra’s algorithm and start coming up with all kinds of heuristics, but that’s exactly what we are not going to do. 
        # In my head, the biggest idea of A* is that we want to keep Dijsktra’s algorithm exactly the same and, instead, we will simply try to Change the weights on which we run the algorithm. 
        # [Strategy: 1) Change the weights 2) run Dijkstra on the new graph]

        strategy = create_strategy(old = True, scale = 0.8).to_corner(DR, buff = 0).set_z_index(1000)
        self.play(
            FadeIn(strategy)
        )
        self.wait()

        # What do I mean by it? 
        _, _,  Gdirected = clipart_map_europe(SCALE_EUROPE, undirected = False)
        tex_prague = prague_tex_name(G)
        tex_rome = rome_tex_name(G)

        self.play(
            FadeOut(G),
            *[FadeIn(e) for e in Gdirected.edges.values()],
            *[FadeIn(v) for v in Gdirected.vertices.values()],
            FadeIn(tex_prague),
            FadeIn(tex_rome),
        )
        self.wait()

        G = Gdirected
        
        G.disable_heights()
        G.set_new_potentials(G.gen_zero_potentials())
        self.update_self(0) # TODO fix that we see old values

        self.play(
            G.show_edge_lengths(G.edges.keys())
        )
        self.wait()

        # for i in range(N_CITIES):
        #     self.add(Tex(i).move_to(G.vertices[i].get_center()))
        # return

        # Well, imagine that I somehow make the edges going in the direction of Rome shorter [stupně green, čísla jdou dolů], and the edges going away from Rome longer. 
        
        # we need to do it in two parts
        air_potentials = G.gen_air_potentials(ROME)
        G.disable_heights()
        self.play(
            *[G.vertex_potentials[v].animate.set_value(air_potentials[v]) for v in G.vertices],
        )
        self.wait()

        self.camera.frame.save_state()
        node1 = 31
        node2 = 17
        self.play(self.camera.frame.animate.scale(0.3).move_to((G.vertices[node1].get_center() + G.vertices[node2].get_center())/2))

        # G.vertices[ROME].save_state()
        # self.play(
        #     G.vertices[ROME].animate.scale(2.0).set_color(RED),
        #     FadeIn(tex_rome)
        # )
        # self.wait()
        # self.play(
        #     G.vertices[ROME].animate.restore(),
        #     FadeOut(tex_rome),
        # )
        # self.wait()


        self.play(
            Flash(G.edge_weights_objs[(node1, node2)], color = GREEN),
        )
        self.wait()

        self.play(
            Flash(G.edge_weights_objs[(node2, node1)], color = RED),
        )
        self.wait()
        

        self.play(self.camera.frame.animate.restore())        
        self.wait()

        # Then, I just run the good old Dijkstra’s algorithm on the new graph.  
        # Since the edges going in the right direction are shorter, the distance from Prague to Rome gets smaller, and the algorithm explores fewer nodes before it reaches Rome, exactly as we want.

        basicDijkstraRun(self, G)

        tex_how_can = Tex("How can we change lengths without changing which path is the shortest? ", z_index = 100).scale(0.8).to_edge(UP)
        rec = SurroundingRectangle(tex_how_can, color = RED, fill_opacity = 1.0, fill_color = config.background_color)

        self.play(
            FadeIn(rec),
            FadeIn(tex_how_can),
        )

        air_potentials = G.gen_air_potentials(13)
        self.play(
            *[G.vertex_potentials[v].animate.set_value(air_potentials[v]) for v in G.vertices],
        )
        self.wait()

        air_potentials = G.gen_air_potentials(0)
        self.play(
            *[G.vertex_potentials[v].animate.set_value(air_potentials[v]) for v in G.vertices],
        )
        self.wait()


        air_potentials = G.gen_air_potentials(22)
        self.play(
            *[G.vertex_potentials[v].animate.set_value(air_potentials[v]) for v in G.vertices],
        )
        self.wait()


        return 
        self.play(
            FadeOut(strategy),
            FadeOut(tex_how_can),
            FadeOut(rec)
        )
        self.wait()

class Chapter12(MovingCameraScene):
    def construct(self):
        default()
        self.next_section(skip_animations=True)
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False, setup_potentials=False)
        
        self.add(background, europe_boundary, G)
        self.add(
            *[e for e in G.edges.values()],
            *[v for v in G.vertices.values()],
            *[G.edge_weights_objs[e] for e in G.edges.keys()],
        )
        self.wait()
        self.next_section(skip_animations=False)


        # So in this first chapter, we will try to understand in which ways we can change our graph without changing which path is the shortest. In the end we also want a change such that Rome gets closer to Prague, but let’s postpone this problem to the next chapter. 
        # [animace kde měním hrany potenciálově, takže cesta zůstává stejná]


        # [přiblížit graf ať není vidět praha ani řím a evokuje to, že nevíme kudy vede nejkratší cesta
        # vyznačená cesta z prahy do říma, pak se změní na několik jiných cest at je jasné že nevíme která to je]

        # Since at this point in time we don’t know yet what the shortest path is, there is not that much that we can do. We can pick some edge and make it shorter or longer, but this way, I am also changing the length of all the paths that use that edge and this can totally mess up which path is the shortest. [Vyznačená hrana jde vahou nahoru a ukazují se různé cesty co přes ní vedou]

        self.play(self.camera.frame.animate.scale(0.3).move_to(G.vertices[7].get_center()))



        # So what can we do? Well, maybe we need to change more than one edge at a time. Look, let’s say I just take this edge and increase its length by one, but also, what if I offset this change by decreasing the length of all of these followup edges by one? Now, any path that uses the longer edge first gets longer by one, but immediately after that it gets shorter by one. So any one of these paths have the same length as before the change! [Ukáže se cesta červeně, změněná čísla možná tlustě]

        G.edge_weights_objs[(7, 6)].save_state()
        self.play(
            Flash(G.edge_weights_objs[(7, 6)], color = RED),
            G.edge_weights_objs[(7, 6)].animate.scale(1.5),
        )
        self.wait()

        # first just 7 6
        simple_reweighting(self, G, [(7, 6)], [], -1, 2.0, -1)
        simple_reweighting(self, G, [(7, 6)], [], 2, 2.0, 1)
        simple_reweighting(self, G, [(7, 6)], [], -1, 2.0, 0)
        
        self.play(
            G.edge_weights_objs[(7, 6)].animate.restore(),
        )
        self.wait()

        # then 7,6, 0,7
        G.edge_weights_objs[(7, 6)].save_state()
        G.edge_weights_objs[(0, 7)].save_state()

        self.play(
            Flash(G.edge_weights_objs[(0, 7)], color = RED),
            Flash(G.edge_weights_objs[(7, 6)], color = RED),
            G.edge_weights_objs[(0, 7)].animate.scale(1.5),
            G.edge_weights_objs[(7, 6)].animate.scale(1.5),
        )
        self.wait()

        

        edges_plus, edges_minus = [(7, 6)], [(0, 7)]
        simple_reweighting(self, G, edges_plus, edges_minus, -1, 2.0, -1)
        # simple_reweighting(self, G, edges_plus, edges_minus, 2, 2.0, 1)
        # simple_reweighting(self, G, edges_plus, edges_minus, -2, 2.0, -1)

        go_along_path(self, G, [(0, 7), (7, 6)])
        simple_reweighting(self, G, edges_plus, edges_minus, 1, 2.0, 0)


        self.play(
            G.edge_weights_objs[(0, 7)].animate.restore(),
            G.edge_weights_objs[(7, 6)].animate.restore(),
        )
        self.wait()

        # set up potentials
        G.setup_potentials(rate = 0.5)
        G.disable_heights()

        # then around node 7
        # self.play(G.vertices[7].animate.scale(2.0))
        # self.play(G.vertices[7].animate.scale(1/2.0))
        # self.wait()

        # then all four
	
        self.play(G.vertex_potentials[7].animate.increment_value(1))
        self.play(G.vertex_potentials[7].animate.increment_value(-2))
        self.play(G.vertex_potentials[7].animate.increment_value(2))
        #go_along_path(self, G, [(0, 7), (7, 0)])
        
        # then another node
        self.play(self.camera.frame.animate.move_to(G.vertices[6].get_center()))

        self.play(G.vertices[6].animate.scale(2.0))
        self.play(G.vertices[6].animate.scale(1/2.0))
        self.wait()

        self.play(G.vertex_potentials[6].animate.increment_value(1))
        self.wait()
        self.play(
            Flash(G.edge_weights_objs[(5, 6)], color = RED),
            Flash(G.edge_weights_objs[(7, 6)], color = RED),
            Flash(G.edge_weights_objs[(8, 6)], color = RED),
            Flash(G.edge_weights_objs[(22, 6)], color = RED),
        )
        self.wait()
        self.play(
            Flash(G.edge_weights_objs[(6, 5)], color = GREEN),
            Flash(G.edge_weights_objs[(6, 7)], color = GREEN),
            Flash(G.edge_weights_objs[(6, 8)], color = GREEN),
            Flash(G.edge_weights_objs[(6, 22)], color = GREEN),
        )
        self.wait()

        # self.play(G.vertex_potentials[6].animate.increment_value(-2))
        # self.play(G.vertex_potentials[6].animate.increment_value(2))
        go_along_path(self, G, [(17, 16), (16, 5), (5, 6), (6, 22), (22, 25)])

        # self.play(
        #     Flash(G.edge_weights_objs[(5, 6)])
        # )
        # self.play(
        #     Flash(G.edge_weights_objs[(6, 22)])
        # )
        self.wait()
        return


class Chapter13(MovingCameraScene):
    def construct(self):
        self.next_section(skip_animations=True)
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
        self.add(background, europe_boundary, G)
        G.disable_heights()
        self.add(
            *[e for e in G.edges.values()],
            *[v for v in G.vertices.values()],
            *[G.edge_weights_objs[e] for e in G.edges.keys()],
            *[G.vertex_height_lines[v] for v in G.vertices.keys()]
        )
        self.wait()
        self.play(
            G.vertex_potentials[7].animate.increment_value(1),
            G.vertex_potentials[6].animate.increment_value(1)
        )
        self.play(self.camera.frame.animate.scale(0.3).move_to(G.vertices[6].get_center()))
        # G.vertex_potentials[7].increment_value(1)
        # G.vertex_potentials[6].increment_value(1)
        self.next_section(skip_animations=False)
        

        # There are two special cases – Prague and Rome themselves. If we try our operation for Prague, it is now a bit different, since any shortest path from Prague only goes out of Prague but it never goes in, so here all of these paths got shorter by the same amount. But fortunately, even this is OK, because our task is not to keep all the lengths of all the paths the same. We simply want that the shortest path in the new graph is the same as the shortest path in the old graph. And if we shift the length of all of those paths  by the same amount, it does not change which one of them is the shortest. We can also do analogous reasoning for Rome.  
        self.play(self.camera.frame.animate.move_to(G.vertices[PRAGUE].get_center()))
        tex_prague = prague_tex_name(G, scale = 0.5)

        self.play(G.vertices[PRAGUE].animate.scale(2.0), FadeIn(tex_prague))
        self.play(G.vertices[PRAGUE].animate.scale(1/2.0), FadeOut(tex_prague))
        self.wait()

        self.play(G.vertex_potentials[PRAGUE].animate.increment_value(2))
        # self.play(G.vertex_potentials[PRAGUE].animate.increment_value(-2))
        # self.play(G.vertex_potentials[PRAGUE].animate.increment_value(3))

        self.play(
            *[Flash(G.edge_weights_objs[(u, v)], color = RED) for (u,v) in G.edges if v == PRAGUE],
        )
        self.wait()
        self.play(
            *[Flash(G.edge_weights_objs[(u, v)], color = GREEN) for (u,v) in G.edges if u == PRAGUE],
        )
        self.wait()


        go_along_path(self, G, [(0, 15), (15, 16)])
        go_along_path(self, G, [(0, 12), (12, 13)])


        # So, we can repeatedly apply our trick to all the nodes, including Prague and Rome and we know that we are not changing what the shortest path is. I find this really magical, because after a few applications of this trick, the graph that we get looks very different from the graph we started with! Yet, finding the shortest path in the new graph gives the same result as in the old graph. 
        # And it is even more mind boggling that there is nothing special about Prague and Rome! Even if we wanted to find the shortest path from Paris to Lviv, it would still be the same path in the old and the new graph!

        # self.play(self.camera.frame.animate.move_to(G.vertices[8].get_center()))
        # self.play(G.vertex_potentials[PRAGUE].animate.increment_value(1))
 
        # self.play(self.camera.frame.animate.scale(1.0 / 0.3).move_to(ORIGIN))

        # self.play(*[G.vertices[v].animate.scale(2.0) for v in [PRAGUE, 7, 6]])
        # self.wait()
        # self.play(*[G.vertices[v].animate.scale(1/2.0) for v in [PRAGUE, 7, 6]])
        # self.wait()


        # PARIS = 10
        # KYIV = 14
        # G.vertices[PARIS].save_state()
        # G.vertices[KYIV].save_state()
    
        # self.play(
        #     G.vertices[PARIS].animate.scale(2.0).set_color(RED),
        #     G.vertices[KYIV].animate.scale(2.0).set_color(RED)
        # )        
        # self.wait()
        # self.play(
        #     G.vertices[PARIS].animate.restore(),
        #     G.vertices[KYIV].animate.restore(),
        # )        
        # self.wait()

        # reset weights

        self.play(
            *[G.vertex_potentials[v].animate.set_value(0) for v in range(N_CITIES)]
        ) 
        self.wait()

        # But now comes the best part. There is actually a very beautiful way of thinking about these operations. Do you still remember how we increased these lengths by one and decreased these lengths by the same amount? Here is how we can think of it. 

        self.play(self.camera.frame.animate.scale(0.3).move_to(G.vertices[6].get_center()))
        self.play(
            G.vertex_potentials[6].animate.increment_value(1),
        )
        self.play(
            G.vertex_potentials[6].animate.increment_value(-1),
        ) 

        self.play(self.camera.frame.animate.scale(1/0.3).move_to(ORIGIN))
        self.wait()


class Chapter14(ThreeDScene):  # TODO check návaznost
    def construct(self):
        default()
        self.next_section(skip_animations=True)
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
        graph = Group(background, europe_boundary, G)
        self.add(background, europe_boundary, G)
        self.add(
            *[e for e in G.edges.values()],
            *[v for v in G.vertices.values()],
            *[G.vertex_height_lines[v] for v in G.vertices.keys()]
        )
        self.add_fixed_orientation_mobjects(
            *[G.edge_weights_objs[e] for e in G.edges.keys()],
        )
        self.next_section(skip_animations=False)
        # for i in range(N_CITIES):
        #     self.add(Tex(i).move_to(G.vertices[i].get_center()))

        # [v animaci se nejdřív zkosí graf tak, aby se tam přidala třetí dimenze, pak se jeden node zvedne, délky hran se zvětšují a zmenšují, zvětšující jsou červeně, zmenšující zeleně]

        # Nice, right? What I did is that I added a third dimension to the picture and raised this node to the elevation of one. Every edge then simply gets longer by the amount you need to climb, or shorter by the amount you descend. 

        # TODO lepsi pohled plus tocit kamerou
        self.move_camera(
            phi= 40 * DEGREES,
            run_time=1,
        )
        self.move_camera(
            zoom = 2.5,
            run_time=1,
            added_anims= [Group(background, europe_boundary, *G.vertices.values()).animate.shift(1*RIGHT + 0.5*UP)]
        )
        self.play(
            G.vertex_potentials[6].animate.increment_value(1),
        )
        self.wait()


        # In general, the three operations that we did to our graph are equivalent to raising these two nodes to elevation one and Prague to elevation two. And then we just redefine the lengths of all edges by the following formula. The new length of every edge is equal to its old length + the elevation of the node it goes to - the elevation of the node where it starts. 
        # [někde vedle se ukáže jen jedna hrana a jak je to pro ni] This is really just a different way of looking at the same trick. 
        self.move_camera(
            zoom = 1.5,
            run_time=1,
            added_anims= [Group(background, europe_boundary, *G.vertices.values()).animate.shift(1*LEFT + -2.3*UP)]
        )
            

        self.play(
            G.vertex_potentials[7].animate.increment_value(1),
        )
        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(2),
        )
        self.wait()
        
        # But now we can understand very visually what’s happening. For example, the new length of this path after we do the reweighting is always equal to the old length of that path plus the potential of Rome minus the potential of Prague. You can certainly prove that this is the case by writing down the definitions of new edge weights and observing that it is a telescoping sum, but I hope that this feels very intuitive even without any calculation. 

        formula = Tex("{{New length($u,v$)}}{{ = }}{{Old length($u,v$)}}{{ + }}{{height($v$)}}{{ - }}{{height($u$)}}").scale(0.7).shift(2.5*UP +0 *LEFT)
        defined = Tex("Definition of new edge lengths. ").scale(0.6).to_corner(UL)
        holds = Tex("Holds for any path from $u$ to $v$!").scale(0.6).to_corner(UR)

        rect = SurroundingRectangle(Group(formula, defined, holds, formula.copy().shift(1*DOWN)), color = RED, fill_opacity = 1.0, fill_color = config.background_color, buff = 0.3)

        ar2 = clipart_arrow().scale(0.5).rotate(-20.0/360 * 2*PI).next_to(defined, DOWN).shift(0.2*UP + 0.3*RIGHT)
        self.add_fixed_in_frame_mobjects(rect, defined, ar2) # TODO jak to udelat aby se formula nezobrazila dvakrat?

        self.play(FadeIn(rect), FadeIn(defined), FadeIn(ar2))
        self.wait()

        self.add_fixed_in_frame_mobjects(formula[0])
        self.play(FadeIn(formula[0]))
        self.wait()

        self.add_fixed_in_frame_mobjects(*formula[1:3])
        self.play(*[FadeIn(f) for f in formula[1:3]])
        self.wait()

        self.add_fixed_in_frame_mobjects(*formula[3:5])
        self.play(*[FadeIn(f) for f in formula[3:5]])
        self.wait()

        self.add_fixed_in_frame_mobjects(*formula[5:])
        self.play(*[FadeIn(f) for f in formula[5:]])
        self.wait()
        

        # a = G.edges[(0, 7)].copy()
        # a.put_start_and_end_on(G.edges[(0, 7)].get_start(), G.edges[(0, 7)].get_end())
        # a.set_color(RED).set_z_index(100000)
        # self.add_fixed_in_frame_mobjects(a)
        # self.play(Create(a))
        # self.play(Uncreate(a))
        # self.wait()
        
        # a = G.edges[(7, 0)].copy()
        # a.put_start_and_end_on(G.edges[(7, 0)].get_start(), G.edges[(7, 0)].get_end())
        # a.set_color(RED).set_z_index(100000)
        # self.add_fixed_in_frame_mobjects(a)
        # self.play(Create(a))
        # self.play(Uncreate(a))
        # self.wait()
        
        path_edges = []
        path_vertices = [G.vertices[u] for u in [0, 7]]
        og_length = 0
        for u,v in [(0, 7)]:
            path_edges.append(Line(G.vertices[u].get_center(), G.vertices[v].get_center(), color = RED))
            og_length += G.edge_weights_vals[(u,v)].get_value()

        for v in path_vertices:
            v.save_state()

        self.play(
            *[v.animate.set_color(RED) for v in path_vertices],
            *[FadeIn(e) for e in path_edges],
            *[Flash(v.get_center(), color = RED) for v in path_vertices],
        )
        self.wait()

        self.play(
            *[v.animate.restore() for v in path_vertices],
            *[FadeOut(e) for e in path_edges]
        )
        self.wait()


        # This formula is super important because although we defined it to be true just for edges, it actually holds for any path. [holds for any path between u and v] Example: take this path from Prague to Rome. Originally, its length was bla, but the new length is smaller by 2, because that is how much higher Prague is than Rome. And if you walk along the path in the opposite direction, it gets longer by 2. 

        # now for paths

        ar = clipart_arrow().scale(0.5).rotate(200.0/360 * 2*PI).next_to(holds, DOWN).shift(0.2*UP + 0.3*LEFT)

        self.add_fixed_in_frame_mobjects(holds, ar)
        self.play(FadeIn(holds), FadeIn(ar))
        self.wait()


        path_edges = []
        path_vertices = [G.vertices[u] for u in [0, 7, 6, 5]]
        og_length = 0
        for u,v in [(0, 7), (7, 6), (6, 5), (5, 1)]:
            path_edges.append(Line(G.vertices[u].get_center(), G.vertices[v].get_center(), color = RED))
            og_length += G.edge_weights_vals[(u,v)].get_value()

        # formula_pr = Tex("{{New length(Prague, Rome)}}{{ = }}{{Old length(Prague, Rome)}}{{ + }}{{height(Rome)}}{{ - }}{{height(Prague)}}").scale(0.5).move_to(formula.get_center())
        # self.add_fixed_in_frame_mobjects(formula_pr)

        
        self.play(
            *[v.animate.set_color(RED) for v in path_vertices],
            *[FadeIn(e) for e in path_edges],
            # FadeOut(formula),
            # FadeIn(formula_pr),
        )
        self.wait()

        # self.play(
        #     *[v.animate.set_color(GRAY) for v in path_vertices],
        #     *[FadeOut(e) for e in path_edges]
        # )
        # self.wait()


        new_formula = Tex(
            r"{{ "+
            str(round(og_length + G.vertex_potentials[ROME].get_value() - G.vertex_potentials[PRAGUE].get_value(),1)) +
            r"}}{{ = }}{{ "+
            str(round(og_length, 1))+
            r"}}{{ + }}{{"+
            str(G.vertex_potentials[ROME].get_value())+
            r"}}{{ - }}{{"+
            str(G.vertex_potentials[PRAGUE].get_value())+
            r"}}"
        )
        for i in range(len(new_formula)):
            new_formula[i].next_to(formula[i], DOWN)
        new_formula[5].move_to(formula[5].get_center()[0] * RIGHT + new_formula[0].get_center()[1] * UP)
        new_formula[1].move_to(formula[1].get_center()[0] * RIGHT + new_formula[0].get_center()[1] * UP)
        new_formula[3].move_to(formula[3].get_center()[0] * RIGHT + new_formula[0].get_center()[1] * UP)

        self.add_fixed_in_frame_mobjects(new_formula[2])
        self.play(FadeIn(new_formula[2]))
        self.wait()

        self.add_fixed_in_frame_mobjects(*new_formula[3:])
        self.play(*[FadeIn(f) for f in new_formula[3:]])
        self.wait()

        self.add_fixed_in_frame_mobjects(*new_formula[0:2])
        self.play(FadeIn(new_formula[0]), FadeIn(new_formula[1]))


        # air_pots = G.gen_air_potentials(ROME)  
        # self.play(
        #     *[G.vertex_potentials[v].animate.set_value(air_pots[v]) for v in range(N_CITIES)]
        # )
        # self.wait()
        # air_pots = G.gen_air_potentials(PRAGUE)
        # self.play(
        #     *[G.vertex_potentials[v].animate.set_value(air_pots[v]) for v in range(N_CITIES)]
        # )
        # self.wait()
        # air_pots = G.gen_air_potentials(31)
        # self.play(
        #     *[G.vertex_potentials[v].animate.set_value(air_pots[v]) for v in range(N_CITIES)]
        # )
        # self.wait()
        # air_pots = G.gen_air_potentials(24)
        # self.play(
        #     *[G.vertex_potentials[v].animate.set_value(air_pots[v]) for v in range(N_CITIES)]
        # )
        # self.wait()


        # This physical intuition of climbing is exactly why these elevations are usually called potentials. In fact, if you are a physicist, the observations we made are just variations on the equations you know and love. So I will use the name potential from now on and I will also use the name potential reweighting for this trick that we can do with them.  

        shft1 = 4*RIGHT
        shft2 = 7*LEFT
        eq1 = Tex(r"$\nabla \times (\nabla \varphi) = 0$", color = RED).to_edge(DOWN).to_edge(LEFT).shift(- shft1)
        eq2 = Tex(r"$\oint_{u \rightarrow v} (\nabla \varphi) \cdot d\ell = \varphi(v) - \varphi(u)$", color = RED).to_edge(DOWN).to_edge(RIGHT).shift(- shft2)
        eq1 = Group(SurroundingRectangle(eq1, color = RED, fill_opacity = 1, fill_color = BACKGROUND_COLOR_LIGHT))
        eq2 = Group(SurroundingRectangle(eq1, color = RED, fill_opacity = 1, fill_color = BACKGROUND_COLOR_LIGHT))
        self.add_fixed_in_frame_mobjects(eq1, eq2)

        self.play(
            eq1.animate.shift(shft1),
            eq2.animate.shift(shft2)
        )
        self.wait()
        self.play(
            eq1.animate.shift(- shft1),
            eq2.animate.shift(- shft2)
        )
        self.wait()

        self.wait(5)





class Test3(ThreeDScene):
    def construct(self):

        self.move_camera(
            phi= 70 * DEGREES,
            run_time=1,
        )

        t1 = Tex("{{a}}{{a}}", color = RED)
        self.add_fixed_in_frame_mobjects(t1)
        self.play(FadeIn(t1))
        self.wait()

        self.play(Circumscribe(t1, color = RED))
        self.wait()

class Intermezzo1(Scene):
    def construct(self):
        Tex.set_default(color = GRAY)

        width = 3
        chapter_borders = Group(
            Square(side_length = width, color = GRAY), 
            Square(side_length = width, color = GRAY), 
            Square(side_length = width, color = GRAY)
        ).arrange(RIGHT, buff = 1)

        scale = 0.7
        chapter_texts = Group(*[
            Tex("Change the weights!").scale(scale),
            Tex("What is a good potential?").scale(scale),
            Tex("Implementation").scale(scale),
        ])
        for i in range(3):
            chapter_texts[i].next_to(chapter_borders[i], DOWN)

        self.play(FadeIn(chapter_borders), FadeIn(chapter_texts))
        self.wait()


class Intermezzo2(Scene):
    def construct(self):
        Tex.set_default(color = GRAY)

        width = 3
        chapter_borders = Group(
            Square(side_length = width, color = GREEN), 
            Square(side_length = width, color = GRAY), 
            Square(side_length = width, color = GRAY)
        ).arrange(RIGHT, buff = 1)

        scale = 0.7
        chapter_texts = Group(*[
            Tex("Change the weights!", color = GREEN).scale(scale),
            Tex("What is a good potential?").scale(scale),
            Tex("Implementation").scale(scale),
        ])
        for i in range(3):
            chapter_texts[i].next_to(chapter_borders[i], DOWN)

        Group(chapter_borders, chapter_texts).shift(2*UP)
        self.play(FadeIn(chapter_borders), FadeIn(chapter_texts))
        self.wait()




        # old strategy 
        buff = 0.3
        strategy_old_group = create_strategy(old=True).to_edge(DOWN, buff = buff)
        strategy_old = strategy_old_group[1]
        self.play(
            FadeIn(strategy_old_group),
        )
        self.wait()

        a = strategy_old[1].copy()
        self.add(a)

        # new strategy
        strategy_new_group = create_strategy(old = False).to_edge(DOWN, buff = buff)
        strategy_new = strategy_new_group[1]

        self.play(
            Transform(strategy_old[0], strategy_new[0]),
            Transform(strategy_old[1], strategy_new[1]),
            Transform(a, strategy_new[2]),
            Transform(strategy_old[2], strategy_new[3]),
            #Transform(strategy_old_group[1], strategy_new_group[1]),
        )
        self.wait()

        ar = clipart_arrow().scale(0.5)
        ar.next_to(strategy_new[1], LEFT)
        self.play(FadeIn(ar))
        self.wait()
        self.play(ar.animate.next_to(strategy_new[2], LEFT))
        self.wait()
        self.play(ar.animate.next_to(strategy_new[3], LEFT))
        self.wait()

        self.play(
            Transform(strategy_old[0], strategy_new[0]),
            FadeOut(ar),
        )
        self.wait()

        self.play(
            Circumscribe(Group(chapter_borders[1], chapter_texts[1]), color = RED)
        )
        self.wait()

        self.play(
            Circumscribe(Group(chapter_borders[2], chapter_texts[2]), color = RED)
        )
        self.wait()


class Intermezzo3(Scene):
    def construct(self):
        Tex.set_default(color = GRAY)

        width = 3
        chapter_borders = Group(
            Square(side_length = width, color = GREEN), 
            Square(side_length = width, color = GREEN), 
            Square(side_length = width, color = GRAY)
        ).arrange(RIGHT, buff = 1)

        scale = 0.7
        chapter_texts = Group(*[
            Tex("Change the weights!", color = GREEN).scale(scale),
            Tex("What is a good potential?", color = GREEN).scale(scale),
            Tex("Implementation").scale(scale),
        ])
        for i in range(3):
            chapter_texts[i].next_to(chapter_borders[i], DOWN)

        self.play(FadeIn(chapter_borders), FadeIn(chapter_texts))
        self.wait()


class Intermezzo4(Scene):
    def construct(self):
        Tex.set_default(color = GRAY)

        width = 3
        chapter_borders = Group(
            Square(side_length = width, color = GREEN), 
            Square(side_length = width, color = GREEN), 
            Square(side_length = width, color = GREEN)
        ).arrange(RIGHT, buff = 1)

        scale = 0.7
        chapter_texts = Group(*[
            Tex("Change the weights!", color = GREEN).scale(scale),
            Tex("What is a good potential?", color = GREEN).scale(scale),
            Tex("Implementation", color = GREEN).scale(scale),
        ])
        for i in range(3):
            chapter_texts[i].next_to(chapter_borders[i], DOWN)

        self.play(FadeIn(chapter_borders), FadeIn(chapter_texts))
        self.wait()
