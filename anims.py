from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.solarized import * # TODO nenacita se solarized
from utils.util import *
from utils.util_graph import *



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
    # TODO pridat ikonu
    def construct(self):
        default()
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

class Chapter11(Scene):
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

        strategy = create_strategy(old = True, scale = 0.8).to_corner(DR, buff = 0).set_z_index(1000)
        self.play(
            FadeIn(strategy)
        )
        self.wait()

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

        # we need to do it in two parts
        air_potentials = G.gen_air_potentials(ROME)

        def f(u,v):
            ret = random.uniform(0.7, 1.0)
            # 0 16 17 5 1
            if (u,v) == (0,16) or (u,v) == (16, 17) or (u,v) == (17,5):
                ret = random.uniform(0.3, 0.5)
            return ret

        shorter_air = {}
        longer_air = {}
        zero = {}
        shorter_weird = {}
        longer_weird = {}

        for (u,v) in G.edges:
            zero[(u,v)] = G.edge_weights_vals[(u,v)].get_value()
            if air_potentials[u] < air_potentials[v]:
                longer_air[(u,v)] = G.edge_weights_vals[(u,v)].get_value() + air_potentials[v] - air_potentials[u]    
                longer_weird[(u,v)] = random.uniform(1.0, 1.4) * (G.edge_weights_vals[(u,v)].get_value() + air_potentials[v] - air_potentials[u] )
            else:
                shorter_air[(u,v)] = G.edge_weights_vals[(u,v)].get_value() + air_potentials[v] - air_potentials[u]
                shorter_weird[(u,v)] = f(u,v) * (G.edge_weights_vals[(u,v)].get_value() + air_potentials[v] - air_potentials[u] )

        changeWeights(self, G, shorter_air, color = GREEN)
        changeWeights(self, G, longer_air)


        # Then, I just run the good old Dijkstra’s algorithm on the new graph.  
        # Since the edges going in the right direction are shorter, the distance from Prague to Rome gets smaller, and the algorithm explores fewer nodes before it reaches Rome, exactly as we want.

        basicDijkstraRun(self, G)
        

        # But now the big question becomes: how should we change the edge lengths? There is an obvious problem with it: We need to guarantee that the shortest path we find in the changed graph is also the shortest path in the original graph. [*For simplicity let’s assume that the shortest path is unique] 
        # If we simply start making some edges shorter and some edges longer, the shortest path in the new graph could end up being different from the old one, which we actually wanted to find. 
        # [ změníme délky hran, pak vyznačíme jinou nejkratší cestu a k tomu popisek “new shortest path”]
        self.next_section(skip_animations=False)


        # first revert weights
        #changeWeights(self, G, zero, color = GRAY)

        # then do weird reweighting
        changeWeights(self, G, shorter_weird | longer_weird, color = GRAY)


        basicDijkstraRun(self, G)


class Chapter12(MovingCameraScene):
    def construct(self):
        default()
        self.next_section(skip_animations=True)
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
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

        self.play(
            FadeOut(strategy)
        )
        self.wait()

        # [přiblížit graf ať není vidět praha ani řím a evokuje to, že nevíme kudy vede nejkratší cesta
        # vyznačená cesta z prahy do říma, pak se změní na několik jiných cest at je jasné že nevíme která to je]

        # Since at this point in time we don’t know yet what the shortest path is, there is not that much that we can do. We can pick some edge and make it shorter or longer, but this way, I am also changing the length of all the paths that use that edge and this can totally mess up which path is the shortest. [Vyznačená hrana jde vahou nahoru a ukazují se různé cesty co přes ní vedou]

        self.play(self.camera.frame.animate.scale(0.3).move_to(G.vertices[7].get_center()))



        # So what can we do? Well, maybe we need to change more than one edge at a time. Look, let’s say I just take this edge and increase its length by one, but also, what if I offset this change by decreasing the length of all of these followup edges by one? Now, any path that uses the longer edge first gets longer by one, but immediately after that it gets shorter by one. So any one of these paths have the same length as before the change! [Ukáže se cesta červeně, změněná čísla možná tlustě]

        print(G.edges.keys())



        # first just 7 6
        simple_reweighting(self, G, [(7, 6)], [], -1)
        simple_reweighting(self, G, [(7, 6)], [], 2)
        simple_reweighting(self, G, [(7, 6)], [], -1)


        # then 7,6, 0,7


        edges_plus, edges_minus = [(7, 6)], [(0, 7)]
        simple_reweighting(self, G, edges_plus, edges_minus, -1)
        simple_reweighting(self, G, edges_plus, edges_minus, 2)
        simple_reweighting(self, G, edges_plus, edges_minus, -2)
        simple_reweighting(self, G, edges_plus, edges_minus, 1)

        self.play(G.vertices[7].animate.scale(2.0))
        self.play(G.vertices[7].animate.scale(1/2.0))
        self.wait()
        go_along_path(self, G, [(0, 7), (7, 6)])

        # then all four
	
        self.play(G.vertex_potentials[7].animate.increment_value(1))
        self.play(G.vertex_potentials[7].animate.increment_value(-2))
        self.play(G.vertex_potentials[7].animate.increment_value(2))
        go_along_path(self, G, [(0, 7), (7, 0)])
        
        # then another node
        self.play(self.camera.frame.animate.move_to(G.vertices[6].get_center()))
        self.play(G.vertices[7].animate.scale(2.0))
        self.play(G.vertices[7].animate.scale(1/2.0))
        self.wait()
        self.play(G.vertex_potentials[6].animate.increment_value(1))
        self.play(G.vertex_potentials[6].animate.increment_value(-2))
        self.play(G.vertex_potentials[6].animate.increment_value(2))
        self.play(G.vertex_potentials[6].animate.increment_value(-1))
        go_along_path(self, G, [(16, 5), (5, 6), (6, 22), (22, 25)])
        return


class Chapter13(MovingCameraScene): # TODO are the scenes joined properly?
    def construct(self):
        self.next_section(skip_animations=True)
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
        self.add(background, europe_boundary, G)
        self.add(
            *[e for e in G.edges.values()],
            *[v for v in G.vertices.values()],
            *[G.edge_weights_objs[e] for e in G.edges.keys()],
            *[G.vertex_height_lines[v] for v in G.vertices.keys()]
        )
        self.wait()
        G.vertex_potentials[7].increment_value(1)
        G.vertex_potentials[6].increment_value(1)
        self.next_section(skip_animations=False)

        # There are two special cases – Prague and Rome themselves. If we try our operation for Prague, it is now a bit different, since any shortest path from Prague only goes out of Prague but it never goes in, so here all of these paths got shorter by the same amount. But fortunately, even this is OK, because our task is not to keep all the lengths of all the paths the same. We simply want that the shortest path in the new graph is the same as the shortest path in the old graph. And if we shift the length of all of those paths  by the same amount, it does not change which one of them is the shortest. We can also do analogous reasoning for Rome.  
        self.play(self.camera.frame.animate.scale(0.3).move_to(G.vertices[PRAGUE].get_center()))
        self.play(G.vertices[PRAGUE].animate.scale(2.0))
        self.play(G.vertices[PRAGUE].animate.scale(1/2.0))
        self.wait()

        self.play(G.vertex_potentials[PRAGUE].animate.increment_value(1))
        self.play(G.vertex_potentials[PRAGUE].animate.increment_value(-2))
        self.play(G.vertex_potentials[PRAGUE].animate.increment_value(3))
 
        go_along_path(self, G, [(0, 15), (15, 16)])
        go_along_path(self, G, [(0, 11), (11, 31), (31, 9), (9, 8), (8, 6)])


        # So, we can repeatedly apply our trick to all the nodes, including Prague and Rome and we know that we are not changing what the shortest path is. I find this really magical, because after a few applications of this trick, the graph that we get looks very different from the graph we started with! Yet, finding the shortest path in the new graph gives the same result as in the old graph. 
        # And it is even more mind boggling that there is nothing special about Prague and Rome! Even if we wanted to find the shortest path from Paris to Lviv, it would still be the same path in the old and the new graph!

        self.play(self.camera.frame.animate.move_to(G.vertices[8].get_center()))
        self.play(G.vertex_potentials[PRAGUE].animate.increment_value(1))
 
        self.play(self.camera.frame.animate.scale(1.0 / 0.3).move_to(ORIGIN))
        PARIS = 10
        KYIV = 14
        self.play(
            G.vertices[PARIS].animate.scale(2.0),
            G.vertices[KYIV].animate.scale(2.0)
        )        
        self.wait()
        self.play(
            G.vertices[PARIS].animate.scale(1/2.0),
            G.vertices[KYIV].animate.scale(1/2.0)
        )        
        self.wait()

        # reset weights

        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(-2),
            G.vertex_potentials[8].animate.increment_value(-1),
            G.vertex_potentials[7].animate.increment_value(-1),
            G.vertex_potentials[6].animate.increment_value(-1),
        ) 

        # But now comes the best part. There is actually a very beautiful way of thinking about these operations. Do you still remember how we increased these lengths by one and decreased these lengths by the same amount? Here is how we can think of it. 

        self.play(self.camera.frame.animate.scale(0.3).move_to(G.vertices[6].get_center()))
        self.play(
            G.vertex_potentials[6].animate.increment_value(1),
        )
        self.play(
            G.vertex_potentials[6].animate.increment_value(-1),
        ) 


class Chapter14(ThreeDScene): 
    def construct(self):
        Tex.set_default(color = GRAY)
        self.next_section(skip_animations=True)
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
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


        # [v animaci se nejdřív zkosí graf tak, aby se tam přidala třetí dimenze, pak se jeden node zvedne, délky hran se zvětšují a zmenšují, zvětšující jsou červeně, zmenšující zeleně]

        # Nice, right? What I did is that I added a third dimension to the picture and raised this node to the elevation of one. Every edge then simply gets longer by the amount you need to climb, or shorter by the amount you descend. 

        # TODO lepsi pohled plus tocit kamerou
        self.move_camera(
            phi=75 * DEGREES,
            #frame_center= G.vertices[6].get_center() + 2*UP,
            run_time=1.5,
            # added_anims=[
            #     self.camera.theta_tracker.animate(
            #         rate_func=rate_functions.ease_in_quad).increment_value((0.2 / 2) * 1.5)
            # ]
        )
            

        self.play(
            G.vertex_potentials[6].animate.increment_value(1),
        )

        # In general, the three operations that we did to our graph are equivalent to raising these two nodes to elevation one and Prague to elevation two. And then we just redefine the lengths of all edges by the following formula. The new length of every edge is equal to its old length + the elevation of the node it goes to - the elevation of the node where it starts. 
        # [někde vedle se ukáže jen jedna hrana a jak je to pro ni] This is really just a different way of looking at the same trick. 
        self.play(
            G.vertex_potentials[7].animate.increment_value(1),
        )
        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(2),
        )

        # But now we can understand very visually what’s happening. For example, the new length of this path after we do the reweighting is always equal to the old length of that path plus the potential of Rome minus the potential of Prague. You can certainly prove that this is the case by writing down the definitions of new edge weights and observing that it is a telescoping sum, but I hope that this feels very intuitive even without any calculation. 

        formula = Tex("{{New length($u,v$)}}{{ = }}{{Old length($u,v$)}}{{ + }}{{height($v$)}}{{ - }}{{height($u$)}}").scale(0.7).shift(2.5*UP +0 *LEFT)
        defined = Tex("Definition of new edge lengths. ").scale(0.6).to_corner(UL)
        ar2 = clipart_arrow().scale(0.5).rotate(-20.0/360 * 2*PI).next_to(defined, DOWN).shift(0.2*UP + 0.3*RIGHT)
        self.add_fixed_in_frame_mobjects(defined, ar2) # TODO jak to udelat aby se formula nezobrazila dvakrat?

        self.play(FadeIn(defined), FadeIn(ar2))
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
        

        a = G.edges[(0, 7)].copy()
        a.put_start_and_end_on(G.edges[(0, 7)].get_start(), G.edges[(0, 7)].get_end())
        a.set_color(RED).set_z_index(100000)
        self.add_fixed_in_frame_mobjects(a)
        self.play(Create(a))
        self.play(Uncreate(a))
        self.wait()
        
        a = G.edges[(7, 0)].copy()
        a.put_start_and_end_on(G.edges[(7, 0)].get_start(), G.edges[(7, 0)].get_end())
        a.set_color(RED).set_z_index(100000)
        self.add_fixed_in_frame_mobjects(a)
        self.play(Create(a))
        self.play(Uncreate(a))
        self.wait()
        

        # This formula is super important because although we defined it to be true just for edges, it actually holds for any path. [holds for any path between u and v] Example: take this path from Prague to Rome. Originally, its length was bla, but the new length is smaller by 2, because that is how much higher Prague is than Rome. And if you walk along the path in the opposite direction, it gets longer by 2. 


        holds = Tex("Holds for any path from $u$ to $v$!").scale(0.6).to_corner(UR)
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

        self.play(
            *[v.animate.set_color(RED) for v in path_vertices],
            *[FadeIn(e) for e in path_edges]
        )
        self.wait()

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

        # This physical intuition of climbing is exactly why these elevations are usually called potentials. In fact, if you are a physicist, the observations we made are just variations on the equations you know and love. So I will use the name potential from now on and I will also use the name potential reweighting for this trick that we can do with them.  

        shft1 = 4*RIGHT
        shft2 = 7*LEFT
        eq1 = Tex(r"$\nabla \times (\nabla \varphi) = 0$", color = PINK).to_edge(LEFT).shift(1*DOWN - shft1)
        eq2 = Tex(r"$\oint_{u \rightarrow v} (\nabla \varphi) \cdot d\ell = \varphi(v) - \varphi(u)$", color = PINK).to_edge(RIGHT).shift(1*DOWN - shft2)
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



class Chapter15(ThreeDScene): 
    def construct(self):
        Tex.set_default(color = GRAY)
        self.next_section(skip_animations=True)
        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
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

        self.move_camera(
            phi=20 * DEGREES,
            #frame_center= G.vertices[6].get_center() + 2*UP,
            run_time=0.5,
            # added_anims=[
            #     self.camera.theta_tracker.animate(
            #         rate_func=rate_functions.ease_in_quad).increment_value((0.2 / 2) * 1.5)
            # ]
        )
            

        self.play(
            G.vertex_potentials[7].animate.increment_value(1),
        )
        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(2),
        )

        self.wait(5)

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
            Tex("Change the graph!").scale(scale),
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
            Tex("Change the graph!", color = GREEN).scale(scale),
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
            Tex("Change the graph!", color = GREEN).scale(scale),
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
            Tex("Change the graph!", color = GREEN).scale(scale),
            Tex("What is a good potential?", color = GREEN).scale(scale),
            Tex("Implementation", color = GREEN).scale(scale),
        ])
        for i in range(3):
            chapter_texts[i].next_to(chapter_borders[i], DOWN)

        self.play(FadeIn(chapter_borders), FadeIn(chapter_texts))
        self.wait()
