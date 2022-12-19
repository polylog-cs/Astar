from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.solarized import * # TODO nenacita se solarized
from utils.util import *
from utils.util_graph import *



class Chapter21(ThreeDScene):
    def construct(self):
        Tex.set_default(font_size = 27)
        ThreeDPart = True
        default()
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


        self.move_camera(
            phi=40 * DEGREES,
            run_time=0.5,
            added_anims = [Group(background, europe_boundary, *G.vertices.values()).animate.shift(1*RIGHT + 0.5*UP)]
        )
    
        self.next_section(skip_animations=False)


        prop_list = create_potential_list([0, 0, 0, 0]).to_edge(LEFT)
        self.add_fixed_in_frame_mobjects(prop_list[0], prop_list[1])
        self.play(FadeIn(prop_list[0]), FadeIn(prop_list[1]))

        # The first property that we want is that the distance from Prague to Rome after we do potential reweighting is as small as possible. Let’s put it on the list. [1. Distance from Prague to Rome gets as small as possible] Fortunately, we understand very well how to achieve it. Remember, we have a formula for the new distance, it says that the new distance from Prague to Rome is equal to the old distance + the potential of Rome - the potential of Prague. 

        text_scale = 0.75
        formula = Tex( r"{{New distance(Prague, Rome)\\}}{{ as small as possible }}").scale(text_scale).next_to(prop_list, RIGHT)
        formulaRHS = Tex("{{= }}{{Old distance(Prague, Rome)}}{{ + }}{{potential(Rome)}}{{ - }}{{potential(Prague)}}").scale(text_scale).next_to(formula[0], RIGHT, buff = 0.1)
        background_formula = SurroundingRectangle(Group(formula, formulaRHS, formulaRHS.copy().shift(1*DOWN)), fill_color = config.background_color, fill_opacity = 1, color = RED)
        Group(formula, formulaRHS, background_formula).move_to(ORIGIN).to_edge(DOWN)

        self.add_fixed_in_frame_mobjects(background_formula, formula)
        self.play(FadeIn(formula))
        self.wait()

        
        self.add_fixed_in_frame_mobjects(formulaRHS)
        self.play(FadeIn(formulaRHS))
        self.wait()

        # self.play(Circumscribe(formulaRHS[1], color = RED))
        # self.wait()

        # self.play(Circumscribe(formulaRHS[3], color = RED))
        # self.wait()


        # So trying to make the left hand side as small as possible is really the same as saying that we want the potential of Prague as large as possible and the potential of Rome as small as possible [někde napsaná rovnice a posouváme rome dolu a prague nahoru]. 
        # Actually, to make it simple, let’s always fix the potential of Rome to be 0. We can do this without loss of generality, because moving all potentials by the same amount does not change the result of the potential reweighting trick. 
        # [někde je tam napsaný potential of Rome = …, celý graf jde nahoru a dolů, pak se zastaví na místě kde Rome = 0] 
        # Now our task is simply to make the potential of Prague as large as possible. [1. potential of Prague as large as possible]

        self.play(
            *[G.vertex_potentials[v].animate.increment_value(1) for v in G.vertices.keys()]
        )
        self.wait()
        self.play(
            *[G.vertex_potentials[v].animate.increment_value(-1) for v in G.vertices.keys()]
        )
        self.wait()
    
        # self.play(Circumscribe(formulaRHS[5], color = RED))
        # self.wait()

        self.add_fixed_in_frame_mobjects(prop_list[2])
        self.play(
            FadeIn(prop_list[2]),
            FadeOut(formula[1]),
        )
        self.wait()

        # self.play(
        #     Group(background_formula, formula[0], formulaRHS).animate.to_edge(DOWN)
        # )
        # self.wait()



        # If this was the only requirement for our potential, it would be a little bit too simple, so we are probably still missing some other items. Let’s see. Let’s leave the potential of all nodes as zero and simply increase the potential of Prague. The distance from Prague to Rome simply decreases, exactly as we want. [posouváme prahu nahoru a vedle je napsáno distance(Rome, Prague) = …]
        # Actually, when the potential of Prague exceeds the original distance from Prague to Rome, the length of the shortest path even becomes negative. 

        dist = 0
        for u,v in [(0, 7), (7, 6), (6, 5), (5, 1)]:
            dist += G.edge_weights_vals[(u,v)].get_value()
        
        n1 = DecimalNumber(dist, num_decimal_places=1, color = GRAY).next_to(formula[0], DOWN)
        n2 = DecimalNumber(dist, num_decimal_places=1, color = GRAY).next_to(formulaRHS[1], DOWN)
        n3 = DecimalNumber(0, num_decimal_places=1, color = GRAY).next_to(formulaRHS[3], DOWN)
        n4 = DecimalNumber(0, num_decimal_places=1, color = GRAY).next_to(formulaRHS[5], DOWN)
        o1 = Tex("=").move_to(n1.get_center()).align_to(formulaRHS[0], RIGHT)
        o2 = Tex("+").move_to(n1.get_center()).align_to(formulaRHS[2], RIGHT)
        o3 = Tex("-").move_to(n1.get_center()).align_to(formulaRHS[4], RIGHT)
        
        def up(mob, scene, G, m):
            mob.set_value(G.vertex_potentials[PRAGUE].get_value())

        n4.add_updater(lambda mob, scene=self,G=G,m=formulaRHS[5]: up(mob, scene, G, m))
        n1.add_updater(lambda mob: mob.set_value(dist - G.vertex_potentials[PRAGUE].get_value())) # .next_to(formula[0], DOWN)
        new_stuff = [n1, n2, n3, n4, o1, o2, o3]

        self.add_fixed_in_frame_mobjects(*new_stuff)
        self.play(
            *[FadeIn(o) for o in new_stuff],
        )
        self.wait()
        

        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(7)
        )
        self.wait()


        self.play(
            G.vertex_potentials[6].animate.increment_value(5),
            G.vertex_potentials[7].animate.increment_value(5),
            G.vertex_potentials[8].animate.increment_value(5)
        )
        self.wait()


        self.play(
            *[Flash(G.edge_weights_objs[e], GREEN) for e in G.edges.keys() if G.edge_weights_vals[e].get_value() < 0]
        )
        self.wait()


        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(3),
            G.vertex_potentials[6].animate.increment_value(0),
            G.vertex_potentials[7].animate.increment_value(0),
            G.vertex_potentials[8].animate.increment_value(0)
        )
        self.wait()


        self.play(
            *[Flash(G.edge_weights_objs[e], GREEN) for e in G.edges.keys() if G.edge_weights_vals[e].get_value() < 0]
        )
        self.wait()


        # # And that sounds veeery suspicious! In fact, you can see that the first edge on the shortest path from Prague soon has negative length! I did not mention it yet, but Dijkstra’s algorithm does not work if there are negative length edges in our graph. If you have the intuition that Dijkstra simply simulates the ants exploring in all directions, this should make a lot of sense, because what should the ants do when they encounter a negative edge? 
        # edges_from_prague = [(u,v) for (u,v) in G.edges.keys() if u == PRAGUE]
        # for e in edges_from_prague:
        #     G.edge_weights_objs[e].save_state()

        # self.play(
        #     *[G.edge_weights_objs[e].animate.scale(2.5) for e in edges_from_prague],
        #     #*[Flash(G.edge_weights_objs[e], color = GREEN) for e in edges_from_prague],
        # )
        # self.wait()
        # self.play(
        #     *[G.edge_weights_objs[e].animate.restore() for e in edges_from_prague],
            
        # )

        self.play(
            FadeOut(formula[0]),
            FadeOut(formulaRHS[0:6]),
            *[FadeOut(o) for o in [n1, n2, n3, n4, o1, o2, o3]],
            G.vertex_potentials[PRAGUE].animate.set_value(0),
            FadeOut(background_formula),
        )
        self.wait()

class Chapter22(ThreeDScene):
    def construct(self):

        default()

        Tex.set_default(font_size = 27)
        self.next_section(skip_animations=True)

        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False, rate = 0.25)
        _, _, _, _, distances = G.run_dijkstra(ROME, PRAGUE, 1)

        self.add(background, europe_boundary, G)
        self.add(
            *[e for e in G.edges.values()],
            *[v for v in G.vertices.values()],
            *[G.vertex_height_lines[v] for v in G.vertices.keys()]
        )
        self.add_fixed_orientation_mobjects(
            *[G.edge_weights_objs[e] for e in G.edges.keys()],
        )


        self.move_camera(
            phi=40 * DEGREES,
            run_time=0.5,
            added_anims = [Group(background, europe_boundary, *G.vertices.values()).animate.shift(1*RIGHT + 0.5*UP)]
        )
        _, _, _, _, distances = G.run_dijkstra(ROME, PRAGUE, 1)

        self.next_section(skip_animations=False)



        prop_list = create_potential_list([0, 0, 0, 0]).to_corner(UL)
        self.add_fixed_in_frame_mobjects(prop_list[0], prop_list[1], prop_list[2])
        self.play(FadeIn(prop_list[0]), FadeIn(prop_list[1]), FadeIn(prop_list[2]))
        
        ############################
    
        # So this fact gives us another constraint on the potentials. Intuitively, what we want is that the potential of every node is at most the distance from that node to Rome. Otherwise, the shortest path from that node to Rome becomes negative which we do not want. 

        sufficient = Tex(r"{{Every edge $u,v$: }}{{New length(u,v) $\ge$ 0}}")
        sufficient2 = Tex(r"{{Every edge $u,v$: }}{{length(u,v) + potential(v) - potential(u) $\ge$ 0}}")
        sufficient3 = Tex(r"{{Every edge $u,v$: }}{{potential(u) - potential(v) $\le$ length(u,v) }}")
        back = SurroundingRectangle(Group(sufficient, sufficient2, sufficient3.copy().shift(1*DOWN + 1*RIGHT),sufficient3.copy().shift(1*DOWN + 1*LEFT),), color = RED, fill_color = config.background_color, fill_opacity = 1)
        Group(sufficient, sufficient2, back).to_edge(DOWN)
        

        self.add_fixed_in_frame_mobjects(back, sufficient)
        self.play(FadeIn(back), FadeIn(sufficient))
        self.wait()

        sufficient2.move_to(sufficient.get_center())
        self.add_fixed_in_frame_mobjects(sufficient2)
        self.play(FadeOut(sufficient), FadeIn(sufficient2))
        self.wait()

        sufficient3.move_to(sufficient.get_center())
        self.add_fixed_in_frame_mobjects(sufficient3)
        self.play(FadeOut(sufficient2), FadeIn(sufficient3))
        self.wait()


        self.add_fixed_in_frame_mobjects(prop_list[3])
        self.play(
            FadeIn(prop_list[3])
        )
        self.wait()


        # intuition

        self.play(FadeOut(sufficient3))

        necessary = Tex("More intuitive corollary: potential(node) $\le$ distance(node, Rome)").move_to(sufficient.get_center())
        self.add_fixed_in_frame_mobjects(necessary)
        self.play(
            FadeIn(necessary)
        )
        self.wait()


        self.play(
            G.vertex_potentials[PRAGUE].animate.set_value(distances[PRAGUE]),
        )
        self.wait()

        # TODO pridat animaci z predchozi chapter


        
        self.add_fixed_in_frame_mobjects(prop_list[4])
        self.play(
            FadeIn(prop_list[4]),
            FadeOut(necessary),
        )
        self.wait()

        # best potential

        tex_best_pot = Tex(r"{{Best potential is: }}{{potential(u) = distance(u, Rome)}}").move_to(back.get_center())


        self.add_fixed_in_frame_mobjects(tex_best_pot)

        self.play(
            *[G.vertex_potentials[v].animate.set_value(0.99*distances[v]) for v in G.vertices.keys()],
            FadeIn(tex_best_pot),
        )
        self.wait()

        

        # So it looks like we are done! We found a formula for the best possible potential that satisfies both requirements on our list! Or are we still missing something? Well, let’s see what would happen if we apply the potential reweighting trick with this potential and then run Dijkstra’s algorithm on the new graph. You can see that the algorithm simply walks along the shortest path to Rome and it doesn’t even bother exploring anything else. Amazing!

        anims, lines, sp_nodes, sp_edges, _ = G.run_dijkstra(PRAGUE, ROME, 100)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.play(anims)
        self.play(Flash(G.vertices[ROME], color = RED))
        self.wait()

        self.move_camera(
            zoom = 2,
            run_time=1,
        )
        self.wait()

        self.play(
            *[G.edge_weights_vals[e].animate.scale(2) for e in sp_edges[0:len(sp_edges)//2]]
        )
        self.wait()
        self.play(
            *[G.edge_weights_vals[e].animate.scale(1.0/2) for e in sp_edges[0:len(sp_edges)//2]]
        )
        self.wait()

        self.move_camera(
            zoom = 1.0,
            run_time=1,
        )
        self.play(
            *[FadeOut(l) for l in lines.values()],
            *[G.vertex_potentials[v].animate.set_value(0) for v in G.vertices.keys()],
            FadeOut(tex_best_pot),
        )
        self.wait()

        # It’s actually so amazing that it should also be pretty suspicious. Do you see the problem with this choice of potentials? Well, the problem is how to compute these potentials. Remember, we want to speed up Dijkstra’s algorithm. So computing these potentials should be something that we can do fast. But how do you compute, let’s say, the potential of Prague? It is defined as the length of the shortest path from Prague to Rome. But this shortest path is exactly what we are trying to compute! [animation with chicken and egg or uroboros]

        # So, we have to go back to our list of requirements for a good potential and add a third property - the potential should be something easy to compute. Now we finally have a complete list of requirements. 

        self.add_fixed_in_frame_mobjects(prop_list[5])
        self.play(
            FadeIn(prop_list[5])
        )
        self.wait()

        tex_good = Tex(r"A potential of $u$ = An optimistic guess of distance from $u$ to Rome. ").move_to(back.get_center()).shift(0.3*UP)
        self.add_fixed_in_frame_mobjects(tex_good)
        self.play(
            FadeIn(tex_good)
        )
        self.wait()
        self.play(
            FadeOut(tex_good)
        )
        self.wait()

        # Here is how you can think about it. Basically, the potential of every node should be something that approximates the distance from that node to Rome. Condition 2 says that it should be an optimistic guess of the actual distances. The actual condition is a bit more complicated than that, but let’s not be too meticulous. Given that the potential satisfies condition 2, we want it to be as close to actual distance as possible, this is what condition 1 says, but we also want it to be easily computable, which is condition 3. 

        # [zobrazí se tabulka]

        # What would be a potential that has all three properties? 
        # Here is one proposal. Remember, we know the geographical position of every city. So, let me define the potential of every city to be not the distance from that city to Rome by road, but the geometrical, air distance between that city and Rome. 



        self.play(
            G.show_names(range(N_CITIES))
        )
        self.wait()
        self.play(
            G.hide_names(range(N_CITIES))
        )
        self.wait()

        tex_decent = Tex(r"{{Very decent potential: }}{{potential(u) = air distance(u, ROME)}}").move_to(back.get_center()).shift(0.3*UP)
        air_distance = G.gen_air_potentials(ROME)
        
        self.add_fixed_in_frame_mobjects(tex_decent)
        self.play(
            FadeIn(tex_decent)
        )
        self.wait()

        r1 = Line(start = G.vertices[PRAGUE].get_center(), end = G.vertices[ROME].get_center(), color = BLACK)
        vec = G.vertices[PRAGUE].get_center() - G.vertices[ROME].get_center()
        vec[0], vec[1] = -vec[1], vec[0]
        eps = 0.1
        r2 = Line(start = G.vertices[PRAGUE].get_center() + eps * vec, end = G.vertices[PRAGUE].get_center() - eps * vec, color = BLACK)
        r3 = Line(start = G.vertices[ROME].get_center() + eps * vec, end = G.vertices[ROME].get_center() - eps * vec, color = BLACK)
        tex_ruler = DecimalNumber(np.linalg.norm(G.vertices[PRAGUE].get_center() - G.vertices[ROME].get_center()), num_decimal_places=1, color = BLACK).move_to(r1.get_center() - 0.15 * vec)

        ruler = Group(r1, r2, r3, tex_ruler)

        G.vertices[PRAGUE].save_state()
        G.vertices[ROME].save_state()

        self.play(
            G.vertices[PRAGUE].animate.set_color(RED),
            G.vertices[ROME].animate.set_color(RED),
        )

        self.play(
            FadeIn(ruler)
        )
        self.wait()
        self.play(
            FadeOut(ruler),
            G.vertices[PRAGUE].animate.restore(),
            G.vertices[ROME].animate.restore(),
        )
        self.wait()

        self.play(
            *[G.vertex_potentials[v].animate.set_value(air_distance[v]) for v in G.vertices.keys()],
        )
        self.wait()

        # For example, Prague is …km away, so its potential would become … In general, these potentials are then forming a nice cone with Rome in the middle. This potential approximates the true distance from Prague to Rome quite decently. [point 1 je ticked] It is also definitely easy to compute if we know the geographical locations of the cities on the map. If the Earth was flat, we would compute the potential by literally plugging in the two positions to Pythagorean theorem [napsat vzoreček]. The Earth is not flat, but still the same story.  

        ticks = [
            clipart_yes_no_maybe("yes", 0.5).next_to(prop_list[2], LEFT, buff = 0.2),
            clipart_yes_no_maybe("yes", 0.5).next_to(prop_list[3], LEFT, buff = 0.2),
            clipart_yes_no_maybe("yes", 0.5).next_to(prop_list[5], LEFT, buff = 0.2),
        ]

        self.add_fixed_in_frame_mobjects(ticks[0])
        self.play(
            FadeIn(ticks[0]),
        )
        self.wait()

        tex_formula = Tex(r"potential($u$) = $\sqrt{(u.x - \text{ROME}.x)^2 + (u.y - \text{ROME}.y)^2}$").next_to(tex_decent, DOWN).shift(0.1*DOWN)
        self.add_fixed_in_frame_mobjects(tex_formula)
        self.play(
            FadeIn(tex_formula)
        )
        self.wait()        

        self.add_fixed_in_frame_mobjects(ticks[2])
        self.play(
            FadeIn(ticks[2]),
        )
        self.wait()


        tex_inequality = Tex(r"air distance(u, Rome) $\le$ air distance(v, Rome) + air distance(u,v) \\ $\le^*$ air distance(v, Rome) + length(u,v) ").next_to(tex_decent, DOWN).shift(0.1*UP)
        tex_btw = Tex(r"Until you start digging tunnels. :)").next_to(tex_inequality, DOWN)


        
        self.add_fixed_in_frame_mobjects(tex_inequality)
        self.play(
            FadeIn(tex_inequality),
            FadeOut(tex_formula)
        )
        self.wait()
        self.add_fixed_in_frame_mobjects(tex_btw)
        self.play(
            FadeIn(tex_btw),
        )
        self.wait()

        self.add_fixed_in_frame_mobjects(ticks[1])
        self.play(
            FadeIn(ticks[1]),
        )
        self.wait()

        # And what about property two? That one is also true, because for any two nodes, we can first use triangle inequality for air distances, and then use the fact that actual distance is always longer than the air distance. 
        # [*Let’s postpone the discussion about Earth’s curvature and digging tunnels to the comment section…]



        # Let’s see what happens if we plug in this potential into our A* algorithm. We start with the original graph, then we elevate every node to appropriate height, and then we run Dijkstra. [strauss?]

        anims, lines, sp_nodes, sp_edges, _ = G.run_dijkstra(PRAGUE, ROME, 1)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.play(anims)
        self.play(Flash(G.vertices[ROME], color = RED))
        self.wait()

        # Nice, you can see how Dijkstra prefers the paths that go in the direction of Rome, simply because they go downhill in our cone, whereas they are slower on the paths that go away, since these paths go uphill. 
        # This is exactly the animation we have seen at the beginning of the video. Pretty nice, right? 
        self.wait(5)


class AstarBeautiful(ThreeDScene):
    def construct(self):
        default()
        self.next_section(skip_animations=False)

        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = True, rate = 0.3)
        self.add(background, europe_boundary, G, *[G.vertex_height_lines[v] for v in range(N_CITIES)])

        self.move_camera(
            phi= 80 * DEGREES,
            zoom = 1.5,
            run_time=1,
        )
        
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

        anims, lines, sp_nodes, sp_edges, _ = G.run_dijkstra(PRAGUE, ROME, 1)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.move_camera(
            theta= -60 * DEGREES,
            run_time=7,
            added_anims = [anims]
        )
        self.play(Flash(G.vertices[ROME], color = RED))

        self.wait()
        


