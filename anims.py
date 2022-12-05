from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from solarized import * # TODO nenacita se solarized
from util import *
from util_graph import *


scroll_properties_str = [
    [
        r"1. Distance from Prague to Rome\\ gets as small as possible. ",
        "1. Potential of Prague as high as possible. ",
        "1. Potential of Prague as close to dist(Prague, Rome) as possible. ",
        "1. Potential of source as close to dist(source, target) as possible. ",
    ],
    [
        "2. All edge retain nonnegative lengths. ",
        "2. For every edge $(u,v):$ potential$(u)$ $\le $ potential$(v)$ + length$(u,v)$ "
    ],
    [
        "3. Potential is easy to compute. "
    ],
]

class Intro(Scene):
    def construct(self):
        background = Rectangle(fill_color = BLUE, fill_opacity = 1, height = 9, width =15)
        europe_boundary, G = clipart_map_europe(SCALE_EUROPE)
        self.play(
            FadeIn(background), 
            FadeIn(europe_boundary), 
            FadeIn(G),
        )
        self.wait()
        
        # Dijkstra
        G.set_new_potentials(G.gen_zero_potentials())
        dijkstra_headline = Tex("{{Dijkstra's}}{{ algorithm}}", color = GRAY).scale(1.5).to_corner(LEFT + UP)
        self.play(FadeIn(dijkstra_headline))

        anims, lines, sp_nodes, sp_edges = G.run_dijkstra(0, 1, 1)
        self.play(
            anims
        )
        self.wait()
        self.play(
            *[FadeOut(line) for line in lines],
        )
        self.wait()
        self.play(
            *[G.edges[e].animate.set_color(RED) for e in sp_edges],
            *[G.vertices[v].animate.set_color(RED) for v in sp_nodes],
        )
        self.wait()

        circle = Circle(
            radius = 1.1 * np.linalg.norm(G.vertices[PRAGUE].get_center() - G.vertices[ROME].get_center()),
            fill_opacity = 0.3,
            fill_color = RED,
            z_index = 10000,
            ).move_to(G.vertices[PRAGUE].get_center())

        self.play(
            *[FadeIn(line) for line in lines],
            *[G.edges[e].animate.set_color(GRAY) for e in sp_edges],
            *[G.vertices[v].animate.set_color(GRAY) for v in sp_nodes],
            FadeIn(circle)
        )
        self.wait()

        
        self.play(
            FadeOut(circle),
            *[FadeOut(line) for line in lines]
        )
        self.wait()
        

        a_headline = Tex("{{A*}}{{ algorithm}}", color = GRAY).scale(1.5).to_corner(LEFT + UP)
        self.play(Transform(dijkstra_headline, a_headline))

        #A*

        # show city positions
        self.play(
            G.show_names(range(N_CITIES))
        )
        self.wait()
        self.play(
            G.hide_names(range(N_CITIES))
        )
        self.wait()

        # run A*
        G.set_new_potentials(G.gen_air_potentials(ROME))
        anims, lines, sp_nodes, sp_edges = G.run_dijkstra(0, 1, 3)
        self.play(
            anims
        )
        self.wait()
        
        ellipse = Ellipse(
            width = 1.0 * np.linalg.norm(G.vertices[PRAGUE].get_center() - G.vertices[ROME].get_center()),
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
            *[FadeOut(line) for line in lines],
            FadeOut(ellipse),
            FadeOut(dijkstra_headline),
        )
        self.wait()

class Polylog(Scene):
    def construct(self):
        authors = Tex(
            r"\textbf{Filip Hlásek, Václav Rozhoň}", 
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

class Chapter1(Scene):
    def construct(self):

        # The problem we are trying to solve is how to speed up Dijkstra’s algorithm by somehow giving it whatever additional information we know about our graph. For example, in the specific case of our map, we have the additional information of knowing the geographical position of every city. The hard part is how to incorporate this information.
        background = Rectangle(fill_color = BLUE, fill_opacity = 1, height = 9, width =15, z_index = -100)
        
        europe_boundary, G = clipart_map_europe(SCALE_EUROPE)
        self.play(
            FadeIn(background), 
            FadeIn(europe_boundary), 
            FadeIn(G),
        )
        self.wait()
        self.play(
            G.show_names(range(N_CITIES))
        )
        self.wait()
        self.play(
            G.hide_names(range(N_CITIES))
        )
        self.wait()

        # We could now look at the implementation of Dijkstra’s algorithm and start coming up with all kinds of heuristics, but that’s exactly what we are not going to do. 
        # In my head, the biggest idea of A* is that we want to keep Dijsktra’s algorithm exactly the same and, instead, we will simply try to change the graph on which we run the algorithm. 
        # [Strategy: 1) change the graph 2) run Dijkstra on the new graph]

        # What do I mean by it? 
        _, Gdirected = clipart_map_europe(SCALE_EUROPE, undirected = False)
        self.play(
            FadeOut(G),
            *[FadeIn(e) for e in Gdirected.edges.values()],
            *[FadeIn(v) for v in Gdirected.vertices.values()],
        )
        self.wait()

        G = Gdirected
        G.set_new_potentials(G.gen_zero_potentials())
        self.update_self(0) # TODO fix that we see old values

        self.play(
            G.show_edge_lengths(G.edges.keys())
        )
        self.wait()

        # Well, imagine that I somehow make the edges going in the direction of Rome shorter [stupně green, čísla jdou dolů], and the edges going away from Rome longer. 
        print(G.gen_air_potentials(ROME))
        return
        self.play(
            G.anim_new_potentials(G.gen_air_potentials(ROME))
        )
        self.wait()
        return

        # Then, I just run the good old Dijkstra’s algorithm on the new graph.  
        # Since the edges going in the right direction are shorter, the distance from Prague to Rome gets smaller, and the algorithm explores fewer nodes before it reaches Rome, exactly as we want.
        anims, lines, _, _ = G.run_dijkstra(PRAGUE, ROME, 3)
        self.play(
            anims
        )
        

        # But now the big question becomes: how should we change the edge lengths? There is an obvious problem with it: We need to guarantee that the shortest path we find in the changed graph is also the shortest path in the original graph. [*For simplicity let’s assume that the shortest path is unique] 
        # If we simply start making some edges shorter and some edges longer, the shortest path in the new graph could end up being different from the old one, which we actually wanted to find. 
        # [ změníme délky hran, pak vyznačíme jinou nejkratší cestu a k tomu popisek “new shortest path”]

        # So in this first chapter, we will try to understand in which ways we can change our graph without changing which path is the shortest. In the end we also want a change such that Rome gets closer to Prague, but let’s postpone this problem to the next chapter. 
        # [animace kde měním hrany potenciálově, takže cesta zůstává stejná]


        # [přiblížit graf ať není vidět praha ani řím a evokuje to, že nevíme kudy vede nejkratší cesta
        # vyznačená cesta z prahy do říma, pak se změní na několik jiných cest at je jasné že nevíme která to je]

        # Since at this point in time we don’t know yet what the shortest path is, there is not that much that we can do. We can pick some edge and make it shorter or longer, but this way, I am also changing the length of all the paths that use that edge and this can totally mess up which path is the shortest. [Vyznačená hrana jde vahou nahoru a ukazují se různé cesty co přes ní vedou]

        # So what can we do? Well, maybe we need to change more than one edge at a time. Look, let’s say I just take this edge and increase its length by one, but also, what if I offset this change by decreasing the length of all of these followup edges by one? Now, any path that uses the longer edge first gets longer by one, but immediately after that it gets shorter by one. So any one of these paths have the same length as before the change! [Ukáže se cesta červeně, změněná čísla možná tlustě]

        # This still does not quite work though since there are still paths like this one that get shorter. So what we actually have to do is pick a node, and make all of the ingoing edges longer, and all of the outgoing edges shorter by the same amount. Then, any path going through that node gets first a bit longer and then shorter by the same amount, so it has in the end the same length. That’s nice! We managed to change our graph without messing up what is the shortest path from Prague to Rome! 

        # There are two special cases – Prague and Rome themselves. If we try our operation for Prague, it is now a bit different, since any shortest path from Prague only goes out of Prague but it never goes in, so here all of these paths got shorter by the same amount. But fortunately, even this is OK, because our task is not to keep all the lengths of all the paths the same. We simply want that the shortest path in the new graph is the same as the shortest path in the old graph. And if we shift the length of all of those paths  by the same amount, it does not change which one of them is the shortest. We can also do analogous reasoning for Rome.  

        # So, we can repeatedly apply our trick to all the nodes, including Prague and Rome and we know that we are not changing what the shortest path is. I find this really magical, because after a few applications of this trick, the graph that we get looks very different from the graph we started with! Yet, finding the shortest path in the new graph gives the same result as in the old graph. 
        # And it is even more mind boggling that there is nothing special about Prague and Rome! Even if we wanted to find the shortest path from Paris to Lviv, it would still be the same path in the old and the new graph!

        # But now comes the best part. There is actually a very beautiful way of thinking about these operations. Do you still remember how we increased these lengths by one and decreased these lengths by the same amount? Here is how I think of it. 

        # [v animaci se nejdřív zkosí graf tak, aby se tam přidala třetí dimenze, pak se jeden node zvedne, délky hran se zvětšují a zmenšují, zvětšující jsou červeně, zmenšující zeleně]

        # Nice, right? What I did is that I added a third dimension to the picture and raised the node to the elevation of one. I now define the new graph by saying that every edge gets longer by the amount you need to climb, or it gets shorter by the amount you descend. 

        # Now we can easily visualize all the operations that we can do to the graph. All we do is that we give every node some elevation and then we redefine the lengths of all edges by the following formula. The new length of the edge is equal to the old length + the elevation of the node we go to - the elevation of the node where we start. 
        # [někde vedle se ukáže jen jedna hrana a jak je to pro ni]

        # Now we can understand very visually what’s happening. For example, the general formula for the new distance from Prague to Rome is that it’s equal to the old distance plus the elevation of Rome minus the elevation of Prague. It does not depend on other elevations at all. That is because what we have already seen, if we change the elevation of some node except for Prague and Rome, the path first gets longer and then shorter by the same amount. Another way to see it is that this is a telescoping sum.

        # But I like to look at it more from a physics perspective. These elevations are really behaving like potential energy. If you bike from Prague to Rome, it does not matter which path you take, the total amount of altitude that you gain or lose on that trip is always the same, and it is simply the difference between these two elevations. And this difference is exactly the amount by which the path gets shorter or longer. 

        # The connection with potentials in physics is also why these elevations are often also called potentials. I will now use this name and I will also use the name potential reweighting for this trick that we can do with them. If you know the physics potentials, you might enjoy thinking about how the analogy works. 

        # [
        # tohle možná dropnout, je to moc advanced
        # Levo Physics pravo CS
        # potentials \phi: V->R, potential \phi R^3->R
        # define length(e) =  phi(v) - phi(u), Esipka = grad phi
        # then, any cycle has length 0, For above E, Rot E = 0 / circ int E . dl = 0
        #  For any path P from u to v: length(P)= phi(v) - phi(u) vs krivkovy integral E od u do v = phi(v) - phi(u)
        # ]


        self.wait(5)

    

class Chapter2(Scene):
    def construct(self):
        pass

class Chapter3(Scene):
    def construct(self):
        pass
        
class ExploreScroll(Scene):
    def construct(self):

        scroll = ImageMobject("img/scroll.png").scale_to_fit_height(4).to_corner(LEFT + UP)
        print(scroll.get_center())
        scroll_header_scale = 0.8
        scroll_properties_scale = 0.6
        scroll_header = Tex("Good potential satisfies: ", color = GRAY).scale(scroll_header_scale).move_to(
            scroll.get_center()
        ).align_to(scroll, UP).shift(0.3*DOWN)

        scroll_properties = []
        for i in range(3):
            scroll_properties.append(
                Tex(scroll_properties_str[i][0], color = GRAY).scale(scroll_properties_scale)
            )
        Group(*scroll_properties).arrange_in_grid(rows = 3, cols = 1, col_alignments="l").next_to(
            scroll_header, DOWN
        ).align_to(scroll_header, LEFT)

        scroll_stuff = Group(scroll, *scroll_properties, scroll_header)

        self.add(*scroll_stuff)

        ##### TABLE

        self.play(scroll_stuff.animate.shift(1*DOWN))

        potential_exact = [
            "f"
        ]


class ExploreStrategy(Scene):
    def construct(self):
        yes = clipart_yes_no_maybe("yes", 1).shift(1*LEFT)
        self.add(*yes)
        
        no = clipart_yes_no_maybe("no", 1)
        self.add(*no)
        
        maybe = clipart_yes_no_maybe("maybe", 1).shift(RIGHT)
        self.add(maybe)
        



class ExplorePotentials(ThreeDScene):
    def construct(self):
        _, G = clipart_map_europe(1.2)
        self.add(G)

        self.move_camera(
            phi=75 * DEGREES,
            frame_center=(0, 0, 2),
            run_time=1.5,
            added_anims=[
                self.camera.theta_tracker.animate(
                    rate_func=rate_functions.ease_in_quad).increment_value((0.2 / 2) * 1.5)
            ])
        self.begin_ambient_camera_rotation(rate=0.2)

        #A*
        anims, lines, sp_nodes, sp_edges = G.run_dijkstra(0, 1, 10)
        self.play(
            anims
        )
        self.wait(5)
        

