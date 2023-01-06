from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.solarized import * # TODO nenacita se solarized
from utils.util import *
from utils.util_graph import *

hwidth = 14
hheight = 1.4

prop_buffer = 0.15

shft = 2.7*RIGHT + 0.5*UP
zoo = 0.9
class Chapter21(ThreeDScene):
    def construct(self):
        self.camera.background_color = BASE02
        Tex.set_default(font_size = 27)
        ThreeDPart = True
        default()
        self.next_section(skip_animations=True)

        _, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)

        self.add(europe_boundary, G)
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
            zoom = zoo,
            added_anims = [Group(europe_boundary, *G.vertices.values()).animate.shift(shft)]
        )
    
        self.next_section(skip_animations=False)


        prop_list = create_potential_list([0, 0, 0, 0]).to_corner(UL, buff = prop_buffer)
        self.add_fixed_in_frame_mobjects(prop_list[0], prop_list[1])
        self.play(FadeIn(prop_list[0]), FadeIn(prop_list[1]))

        self.play(
            *[G.vertex_potentials[v].animate.increment_value(1) for v in G.vertices.keys()]
        )
        self.wait()
        self.play(
            *[G.vertex_potentials[v].animate.increment_value(-1) for v in G.vertices.keys()]
        )
        self.wait()
    

        self.add_fixed_in_frame_mobjects(prop_list[2])
        self.play(
            FadeIn(prop_list[2]),
        )
        self.wait()


        # If this was the only requirement for our potential, it would be a little bit too simple, so we are probably still missing some other items. Let’s see. Let’s leave the potential of all nodes as zero and simply increase the potential of Prague. The distance from Prague to Rome simply decreases, exactly as we want. [posouváme prahu nahoru a vedle je napsáno distance(Rome, Prague) = …]
        # Actually, when the potential of Prague exceeds the original distance from Prague to Rome, the length of the shortest path even becomes negative. 

        dist = 0
        for u,v in [(0, 7), (7, 6), (6, 5), (5, 1)]:
            dist += G.edge_weights_vals[(u,v)].get_value()
        
        def up(mob, scene, G, m):
            mob.set_value(G.vertex_potentials[PRAGUE].get_value())

        
        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(7)
        )
        self.wait()


        # self.play(
        #     G.vertex_potentials[6].animate.increment_value(5),
        #     G.vertex_potentials[7].animate.increment_value(5),
        #     G.vertex_potentials[8].animate.increment_value(5)
        # )
        # self.wait()


        # for e in G.edges.keys():
        #     print(G.edge_weights_vals[e].get_value())

        # self.play(
        #     *[G.edge_weights_objs[e].animate.scale(2) for e in G.edges.keys() if G.edge_weights_objs[e].get_value() < 0]
        # )
        # self.wait()
        # self.play(
        #     *[G.edge_weights_objs[e].animate.scale(1.0/2) for e in G.edges.keys() if G.edge_weights_objs[e].get_value() < 0]
        # )
        # self.wait()


        self.play(
            G.vertex_potentials[PRAGUE].animate.set_value(3),
            G.vertex_potentials[6].animate.set_value(0),
            G.vertex_potentials[7].animate.set_value(0),
            G.vertex_potentials[8].animate.set_value(0)
        )
        self.wait()


        groups = []
        for e in G.edges.keys():
            if G.edge_weights_objs[e].get_value() < 0:
                groups.append(
                    Group(
                        SurroundingRectangle(G.edge_weights_objs[e], color = BACKGROUND_COLOR, buff = 0, fill_opacity = 1, fill_color = BACKGROUND_COLOR).set_z_index(99),
                        G.edge_weights_objs[e].set_z_index(100),                        
                    )
                )

        self.play(
            *[gr.animate.scale(2) for gr in groups]
        )
        for g in groups:
            self.remove(g[0])

        self.play(
            *[gr[1].animate.scale(1.0/2) for gr in groups]
        )
        self.wait()

        self.play(
            G.vertex_potentials[PRAGUE].animate.set_value(0),
        )
        self.wait()



        self.add_fixed_in_frame_mobjects(prop_list[3], prop_list[4] )
        self.play(
            FadeIn(prop_list[3]),
            FadeIn(prop_list[4]),
        )
        self.wait()




class Chapter21flat(Scene):
    def construct(self):
        Tex.set_default(font_size = 27)
        default()

        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
    
        self.next_section(skip_animations=False)


        # The first property that we want is that the distance from Prague to Rome after we do potential reweighting is as small as possible. Let’s put it on the list. [1. Distance from Prague to Rome gets as small as possible] Fortunately, we understand very well how to achieve it. Remember, we have a formula for the new distance, it says that the new distance from Prague to Rome is equal to the old distance + the potential of Rome - the potential of Prague. 

        text_scale = 1
        background_formula = Rectangle(height = hheight, width = hwidth, 
        fill_color = config.background_color, fill_opacity = 1, color = RED)
        formula = Tex( r"New distance(Prague, Rome)").scale(text_scale)
        formulaRHS = Tex(r"{{= }}{{Old distance(Prague, Rome)}}{{ $+$ }}{{potential(Rome)}}{{ $-$ }}{{potential(Prague)}}").scale(text_scale).next_to(formula[0], RIGHT, buff = 0.1)
        Group(formula, formulaRHS).move_to(background_formula.get_center()+0.3*UP)
        Group(formula, formulaRHS, background_formula).to_edge(DOWN, buff = prop_buffer)

        self.play(FadeIn(background_formula), FadeIn(formula))
        self.wait()

        self.play(FadeIn(formulaRHS[0]), FadeIn(formulaRHS[1]), )
        self.wait()
        self.play(FadeIn(formulaRHS[2]), FadeIn(formulaRHS[3]), )
        self.wait()
        self.play(FadeIn(formulaRHS[4]), FadeIn(formulaRHS[5]), )
        self.wait()


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

        self.play(
            *[FadeIn(o) for o in new_stuff],
        )
        self.wait()
        

        self.play(
            G.vertex_potentials[PRAGUE].animate.increment_value(7)
        )
        self.wait()


        # self.play(
        #     G.vertex_potentials[6].animate.increment_value(5),
        #     G.vertex_potentials[7].animate.increment_value(5),
        #     G.vertex_potentials[8].animate.increment_value(5)
        # )
        # self.wait()

        self.play(
            FadeOut(formula[0]),
            FadeOut(formulaRHS[0:6]),
            *[FadeOut(o) for o in [n1, n2, n3, n4, o1, o2, o3]],
        )
        self.wait()



        necessary = Tex(r"{{\textit{Necessary} for every node: }}{{potential(node) $\le$ distance(node, Rome)}}")
        sufficient = Tex(r"{{\textit{Sufficient} for every edge $u,v$: }}{{New length($u$,$v$) $\ge$ 0}}")
        gr = Group(necessary[0], necessary[1], sufficient[0], Group(*sufficient[1:])).arrange_in_grid(cols = 2, col_widths=[5, 5]).move_to(background_formula.get_center())


        sufficient2 = Tex(r"{{\textit{Sufficient} for every edge $u,v$: }}{{length($u$,$v$) $+$ potential($v$) - potential($u$) $\ge$ $0$}}").move_to(sufficient.get_center())
        sufficient23 = Tex(r"{{\textit{Sufficient} for every edge $u,v$: }}{{length($u$,$v$) }}{{$+$ }}{{potential($v$) }}{{$-$ }}{{potential($u$) }}{{$\ge$ }}{{0}}").move_to(sufficient.get_center())
        sufficient3 = Tex(r"{{\textit{Sufficient} for every edge $u,v$: }}{{potential($u$)}}{{ $-$ }}{{potential($v$) }}{{$\le$ }}{{length($u$,$v$) }}").move_to(sufficient.get_center())

        for s in [sufficient2, sufficient23, sufficient3]:
            s[0].move_to(sufficient[0].get_center())
            Group(*s[1:]).move_to(Group(*sufficient[1:]).get_center())

        self.play(FadeIn(necessary))
        self.wait()


        self.play(FadeIn(sufficient))
        self.wait()
        self.play(
            Transform(sufficient, sufficient2)
        )
        self.wait()
        self.remove(sufficient)
        self.add(sufficient23)

        self.play(
            Transform(sufficient23[0], sufficient3[0]),
            Transform(sufficient23[1], sufficient3[5]),
            FadeOut(sufficient23[2]),
            FadeOut(sufficient23[7]),
            Transform(sufficient23[3], sufficient3[3]),
            Transform(sufficient23[4], sufficient3[2]),
            Transform(sufficient23[5], sufficient3[1]),
            Transform(sufficient23[6], sufficient3[4]),
        )
        self.wait()

        # Our potential has to satisfy this second condition which also implies this first one, but let me add both of them to our list, simply because the first condition is much easier to understand. So if this inequality is hard to understand, just think of it as a bit more complicated version of this one. 

        rec = SurroundingRectangle(sufficient23, color = RED)
        rec.generate_target()
        rec.target = SurroundingRectangle(necessary, color = RED)

        self.play(FadeIn(rec))
        self.wait()
        self.play(MoveToTarget(rec))
        self.wait()
        self.play(FadeOut(rec))
        self.wait()


        self.play(
            *[FadeOut(sufficient23[i]) for i in [0, 1, 3, 4, 5, 6]],
            FadeOut(necessary)
        )
        self.wait()


        optimistic = Tex(r"potential($u$) is optimistic estimate of distance($u$, Rome)", font_size = 50).move_to(background_formula.get_center())
        self.play(FadeIn(optimistic))
        self.wait()
        self.play(FadeOut(optimistic))
        self.wait()
        


class Chapter22(ThreeDScene):
    def construct(self):

        default()
        self.camera.background_color = BASE02
        
        Tex.set_default(font_size = 27)
        self.next_section(skip_animations=True)

        _, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False, rate = 0.25)
        _, _, _, _, distances, _ = G.run_dijkstra(ROME, PRAGUE, 1)


        self.add(europe_boundary, G)
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
            zoom = zoo,
            added_anims = [Group(europe_boundary, *G.vertices.values()).animate.shift(shft)]
        )

        self.next_section(skip_animations=False)




        prop_list = create_potential_list([0, 0, 0, 0]).to_corner(UL, buff = prop_buffer)
        self.add_fixed_in_frame_mobjects(prop_list[0], prop_list[1], prop_list[2], prop_list[3], prop_list[4])
        self.play(
            FadeIn(prop_list[0]), FadeIn(prop_list[1]), 
            FadeIn(prop_list[2]), FadeIn(prop_list[3]), FadeIn(prop_list[4])
        )
        
        ############################
    
        # So this fact gives us another constraint on the potentials. Intuitively, what we want is that the potential of every node is at most the distance from that node to Rome. Otherwise, the shortest path from that node to Rome becomes negative which we do not want. 

        back = Rectangle(height = hheight, width = hwidth, color = RED, fill_color = config.background_color, 
        fill_opacity = 1).to_edge(DOWN, buff = 0.3)     

        tex_best_pot = Tex(r"{{for every node $u$ }}{{potential($u$) $=$ distance($u$, Rome)}}", z_index = 100).move_to(back.get_center())
        tex_best_pot.shift(2*LEFT)

        self.add_fixed_in_frame_mobjects(back, tex_best_pot)

        self.play(
            *[G.vertex_potentials[v].animate.set_value(0.999*distances[v]) for v in G.vertices.keys()],
            FadeIn(tex_best_pot),
        )
        self.wait()

        
        rec = SurroundingRectangle(prop_list[4][1], color = RED).set_z_index(1000)
        self.add_fixed_in_frame_mobjects(rec)
        self.remove(rec)
        self.play(FadeIn(rec))
        self.wait()

        recp = SurroundingRectangle(prop_list[3][1], color = RED).set_z_index(1000)
        self.add_fixed_in_frame_mobjects(recp)
        self.remove(recp)
        self.play(Transform(rec, recp))
        self.wait()

        recp = SurroundingRectangle(prop_list[4][1], color = RED).set_z_index(1000)
        self.add_fixed_in_frame_mobjects(recp)
        self.remove(recp)
        self.play(Transform(rec, recp))
        self.wait()

        recp = SurroundingRectangle(prop_list[2], color = RED).set_z_index(1000)
        self.add_fixed_in_frame_mobjects(recp)
        self.remove(recp)
        self.play(Transform(rec, recp))
        self.wait()

        self.play(FadeOut(rec))
        self.wait()


        # So it looks like we are done! We found a formula for the best possible potential that satisfies both requirements on our list! Or are we still missing something? Well, let’s see what would happen if we apply the potential reweighting trick with this potential and then run Dijkstra’s algorithm on the new graph. You can see that the algorithm simply walks along the shortest path to Rome and it doesn’t even bother exploring anything else. Amazing!

        for v in G.vertices.values():
            v.save_state()
        anims, lines, sp_nodes, sp_edges, _, red_nodes = G.run_dijkstra(PRAGUE, ROME, 100)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.play(anims)
        self.play(Flash(G.vertices[ROME], color = RED))
        self.wait()

        # self.move_camera(
        #     zoom = 2,
        #     run_time=1,
        # )
        # self.wait()

        # self.play(
        #     *[G.edge_weights_vals[e].animate.scale(2) for e in sp_edges[0:len(sp_edges)//2]]
        # )
        # self.wait()
        # self.play(
        #     *[G.edge_weights_vals[e].animate.scale(1.0/2) for e in sp_edges[0:len(sp_edges)//2]]
        # )
        # self.wait()

        # self.move_camera(
        #     zoom = 1.0,
        #     run_time=1,
        # )
        self.play(
            *[FadeOut(l) for l in lines.values()],
            *[G.vertices[node].animate.restore() for node in red_nodes],
            *[G.vertex_potentials[v].animate.set_value(0) for v in G.vertices.keys()],
            FadeOut(tex_best_pot),
        )
        self.wait()

        self.add_fixed_in_frame_mobjects(prop_list[5])
        self.play(FadeIn(prop_list[5]))
        self.wait()


        tex_decent = Tex(r"{{for every node $u$ }}{{potential($u$) $=$ air distance($u$, Rome)}}", z_index = 100).move_to(back.get_center()).shift(0.3*UP)
        tex_decent.shift(2*LEFT)
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
        ruler_background = SurroundingRectangle(tex_ruler, fill_opacity = 1, fill_color = config.background_color, color = config.background_color)
        ruler = Group(r1, r2, r3, ruler_background, tex_ruler)

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
            clipart_yes_no_maybe("yes", 0.5).next_to(prop_list[2], RIGHT, buff = 0.2).set_z_index(1000).shift(0.5*RIGHT),
            clipart_yes_no_maybe("yes", 0.5).next_to(prop_list[3], RIGHT, buff = 0.2).set_z_index(1000).shift(0.5*RIGHT),
            clipart_yes_no_maybe("yes", 0.5).next_to(prop_list[4], RIGHT, buff = 0.2).set_z_index(1000).shift(0.5*RIGHT),
            clipart_yes_no_maybe("yes", 0.5).next_to(prop_list[5], RIGHT, buff = 0.2).set_z_index(1000).shift(0.5*RIGHT),
        ]

        for i in [1, 2, 3]:
            ticks[i].align_to(ticks[0].get_left(), LEFT)

        self.add_fixed_in_frame_mobjects(ticks[0])
        self.play(
            FadeIn(ticks[0]),
            #Flash(ticks[0].get_center(), color = GREEN),
        )
        self.wait()

        tex_btw = Tex(r"Until you start digging tunnels. :)", z_index = 100).scale(0.5).next_to(tex_decent, DOWN)
        self.add_fixed_in_frame_mobjects(ticks[2], tex_btw)
        self.play(
            FadeIn(ticks[2]),
            FadeIn(tex_btw),
            #Flash(ticks[2].get_center(), color = GREEN),
        )
        self.wait()

        tex_inequality = Tex(r"air distance(u, Rome) $\le$ air distance(v, Rome) $+$ air distance(u,v) \\ $\le$ air distance(v, Rome) $+$ length(u,v) ", 
        z_index = 100).scale(0.5).move_to(back.get_center()).next_to(tex_decent, DOWN)
        self.add_fixed_in_frame_mobjects(ticks[1], tex_inequality)
        self.play(
            FadeIn(ticks[1]),
            #Flash(ticks[1].get_center(), color = GREEN),
            FadeOut(tex_btw),
            FadeIn(tex_inequality)
        )
        self.wait()

        self.play(
            *[G.vertex_potentials[v].animate.set_value(0) for v in G.vertices.keys()],
        )
        self.wait()
        

        self.play(
            FadeOut(tex_inequality),
            G.show_names(range(20)),
            G.show_names(range(22, N_CITIES)),
            *[FadeOut(edge) for edge in G.edges.values()],
            *[FadeOut(G.edge_weights_objs[e]) for e in G.edges.keys()],
        )
        self.wait()
        
        self.play(
            G.hide_names(range(20)),
            G.hide_names(range(22, N_CITIES)),
            *[FadeIn(edge) for edge in G.edges.values()],
            *[FadeIn(G.edge_weights_objs[e]) for e in G.edges.keys()],
        )
        self.wait()


        tex_formula = Tex(r"$\text{potential}(u) = \sqrt{(u.x - \text{Rome}.x)^2 + (u.y - \text{Rome}.y)^2}$", 
        z_index = 100).next_to(tex_decent, DOWN).shift(0.1*DOWN)
        self.add_fixed_in_frame_mobjects(ticks[3], tex_formula)
        self.play(
            FadeIn(ticks[3]),
            #Flash(ticks[3].get_center(), color = GREEN),
            FadeIn(tex_formula),
        )
        self.wait()
        
        self.play(
            FadeOut(tex_formula),
        )
        self.wait()

        # And what about property two? That one is also true, because for any two nodes, we can first use triangle inequality for air distances, and then use the fact that actual distance is always longer than the air distance. 
        # [*Let’s postpone the discussion about Earth’s curvature and digging tunnels to the comment section…]

        self.play(
            *[G.vertex_potentials[v].animate.set_value(air_distance[v]) for v in G.vertices.keys()],
        )
        self.wait()


        # Let’s see what happens if we plug in this potential into our A* algorithm. We start with the original graph, then we elevate every node to appropriate height, and then we run Dijkstra. [strauss?]

        anims, lines, sp_nodes, sp_edges, _, _ = G.run_dijkstra(PRAGUE, ROME, 1)
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
        self.camera.background_color = BASE02
        _, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = True, rate = 0.3)
        self.add(europe_boundary, G, *[G.vertex_height_lines[v] for v in range(N_CITIES)])

        self.move_camera(
            phi= 80 * DEGREES,
            zoom = 1.5,
            run_time=3,
        )
        
        G.disable_colors()
        air_potentials = G.gen_air_potentials(ROME)
        self.move_camera(
            theta= -140 * DEGREES,
            run_time=3,
            added_anims = [G.vertex_potentials[v].animate.set_value(air_potentials[v]) for v in G.vertices]
        )
        self.wait()

        self.play(
            *[FadeOut(G.vertex_height_lines[v]) for v in range(N_CITIES)]
        )
        self.wait()

        anims, lines, sp_nodes, sp_edges, _, _ = G.run_dijkstra(PRAGUE, ROME, 3)
        self.play(Flash(G.vertices[PRAGUE], color = RED))
        self.move_camera(
            theta= -60 * DEGREES,
            run_time=7,
            added_anims = [anims]
        )
        self.play(Flash(G.vertices[ROME], color = RED))

        self.wait()
        





class AstarMoreBeautiful(ThreeDScene):
    def construct(self):
        default()
        self.camera.background_color = BASE02
        _, europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = True, rate = 0.3)
        Group(europe_boundary, G).shift(0.5*RIGHT + 4*DOWN)
        #.shift(0.5*RIGHT + 2*DOWN) 70
        self.add(europe_boundary, G)

        self.move_camera(
            phi= 80 * DEGREES,
            theta= -90 * DEGREES,
            zoom = 0.9,
            run_time=3,
        )
        
        air_potentials = G.gen_air_potentials(ROME)
        self.play(
            *[G.vertex_potentials[v].animate.set_value(air_potentials[v]) for v in G.vertices]
        )

        G.disable_colors()

        anims, lines, sp_nodes, sp_edges, _, _ = G.run_dijkstra(PRAGUE, ROME, 3, thumbnail = True)
        self.play(anims)

        self.wait()
        
class Test(Scene):
    def construct(self):
        dot = Dot(color = RED)
        dot2 = Dot(color = RED).move_to(RIGHT)
        dot2.add_updater(lambda mob,dt: mob.next_to(dot, DOWN))

        self.add(dot, dot2)
        self.wait()

