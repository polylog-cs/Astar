from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.solarized import * # TODO nenacita se solarized
from utils.util import *
from utils.util_graph import *


scroll_properties_str = [
    [
        r"{{1. }}{{Potential(Prague) \\}}{{ as high as possible. }}",
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

# TODO svitek buď jen průhledný nebo jen pozadí

ThreeDPart = False
class Chapter21(ThreeDScene):
    def construct(self):
        Tex.set_default(color = GRAY)
        Tex.set_default(font_size = 28)
        self.next_section(skip_animations=True)

        background = Rectangle(fill_color = BLUE, fill_opacity = 1, height = 9, width =15, z_index = -100)
        europe_boundary, G = clipart_map_europe(SCALE_EUROPE, undirected = False)
        if ThreeDPart:
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

        if ThreeDPart:
            self.move_camera(
                phi=20 * DEGREES,
                #frame_center= G.vertices[6].get_center() + 2*UP,
                run_time=0.5,
                # added_anims=[
                #     self.camera.theta_tracker.animate(
                #         rate_func=rate_functions.ease_in_quad).increment_value((0.2 / 2) * 1.5)
                # ]
            )

        scroll = ImageMobject("img/scroll.png").rotate(90.0/360.0 * 2*PI).scale_to_fit_height(7).to_edge(LEFT, buff = 0)
        scroll_header_scale = 1.0
        scroll_properties_scale = 1
        scroll_header = Tex("Good potential satisfies: ", color = GRAY).scale(scroll_header_scale).move_to(
            scroll.get_center()
        ).align_to(scroll, UP).shift(1.3*DOWN)

        scroll_properties = []
        for i in range(3):
            scroll_properties.append(
                Tex(scroll_properties_str[i][0], color = GRAY).scale(scroll_properties_scale)
            )
        Group(*scroll_properties).arrange_in_grid(rows = 3, cols = 1, col_alignments="l").next_to(
            scroll_header, DOWN
        ).align_to(scroll_header, LEFT)

        scroll_stuff = Group(scroll, *scroll_properties, scroll_header)
        # Ok, let’s try to make a general list of what a good potential should satisfy. Then, we will use that list to find a potential that works well for real maps. [zobrazí se svitek “Good potential satisfies:”]

        self.add_fixed_in_frame_mobjects(scroll, scroll_header)
        self.play(
            FadeIn(scroll),
            FadeIn(scroll_header)
        )
        self.wait()


        # The first property that we want is that the distance from Prague to Rome after we do potential reweighting is as small as possible. Let’s put it on the list. [1. Distance from Prague to Rome gets as small as possible] Fortunately, we understand very well how to achieve it. Remember, we have a formula for the new distance, it says that the new distance from Prague to Rome is equal to the old distance + the potential of Rome - the potential of Prague. 

        text_scale = 0.75
        formula = Tex( r"{{New distance(Prague, Rome)\\}}{{ as small as possible }}").scale(text_scale).next_to(scroll, RIGHT)
        background_formula = Rectangle(fill_color = config.background_color, fill_opacity = 1, color = RED, height = 2, width =10).shift(2*RIGHT)

        self.add_fixed_in_frame_mobjects(background_formula, formula)
        self.play(FadeIn(formula))
        self.wait()

        formulaRHS = Tex("{{= }}{{Old distance(Prague, Rome)}}{{ + }}{{Potential(Rome)}}{{ - }}{{Potential(Prague)}}").scale(text_scale).next_to(formula[0], RIGHT, buff = 0.1)
        
        self.add_fixed_in_frame_mobjects(formulaRHS)
        self.play(FadeIn(formulaRHS))
        self.wait()

        self.play(Circumscribe(formulaRHS[1], color = RED))
        self.wait()

        self.play(Circumscribe(formulaRHS[3], color = RED))
        self.wait()


        # So trying to make the left hand side as small as possible is really the same as saying that we want the potential of Prague as large as possible and the potential of Rome as small as possible [někde napsaná rovnice a posouváme rome dolu a prague nahoru]. 
        # Actually, to make it simple, let’s always fix the potential of Rome to be 0. We can do this without loss of generality, because moving all potentials by the same amount does not change the result of the potential reweighting trick. 
        # [někde je tam napsaný potential of Rome = …, celý graf jde nahoru a dolů, pak se zastaví na místě kde Rome = 0] 
        # Now our task is simply to make the potential of Prague as large as possible. [1. Potential of Prague as large as possible]

        if ThreeDPart:
            self.play(
                *[G.vertex_potentials[v].animate.increment_value(1) for v in G.vertices.keys()]
            )
            self.wait()
            self.play(
                *[G.vertex_potentials[v].animate.increment_value(-1) for v in G.vertices.keys()]
            )
            self.wait()
        
        self.play(Circumscribe(formulaRHS[5], color = RED))
        self.wait()

        self.play(
            FadeIn(scroll_properties[0]),
            FadeOut(formula[1]),
        )
        self.wait()

        self.play(
            Group(background_formula, formula[0], formulaRHS).animate.to_edge(DOWN)
        )
        self.wait()



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
        
        n4.add_updater(lambda mob: mob.set_value(G.vertex_potentials[PRAGUE].get_value()))
        n1.add_updater(lambda mob: mob.set_value(dist - G.vertex_potentials[PRAGUE].get_value()))
        new_stuff = [n1, n2, n3, n4, o1, o2, o3]

        self.add_fixed_in_frame_mobjects(*new_stuff)
        self.play(
            *[FadeIn(o) for o in new_stuff],
        )
        self.wait()
        

        self.play(
            *[G.vertex_potentials[PRAGUE].animate.increment_value(dist) for v in G.vertices.keys()]
        )
        self.wait()


        # And that sounds veeery suspicious! In fact, you can see that the first edge on the shortest path from Prague soon has negative length! I did not mention it yet, but Dijkstra’s algorithm does not work if there are negative length edges in our graph. If you have the intuition that Dijkstra simply simulates the ants exploring in all directions, this should make a lot of sense, because what should the ants do when they encounter a negative edge? 
        if ThreeDPart:
            edges_from_prague = [(u,v) for (u,v) in G.edges.keys() if u == PRAGUE]
            self.play(
                *[Flash(G.vertices[v], color = RED) for (u,v) in edges_from_prague]
            )
            self.wait()

        self.play(
            FadeOut(formula[0]),
            FadeOut(formulaRHS[0:6]),
            *[FadeOut(o) for o in [n1, n2, n3, n4, o1, o2, o3]]
        )
        self.wait()

ThreeDPart = False
class Chapter22(ThreeDScene):
    def construct(self):
        Tex.set_default(color = GRAY)
        Tex.set_default(font_size = 28)

        background_formula = Rectangle(fill_color = config.background_color, fill_opacity = 1, color = RED, height = 2, width =10).shift(2*RIGHT + 3*DOWN)
        self.add_fixed_in_frame_mobjects(background_formula)
        scroll = ImageMobject("img/scroll.png").rotate(90.0/360.0 * 2*PI).scale_to_fit_height(7).to_edge(LEFT, buff = 0)
        scroll_header_scale = 1.0
        scroll_properties_scale = 1
        scroll_header = Tex("Good potential satisfies: ", color = GRAY).scale(scroll_header_scale).move_to(
            scroll.get_center()
        ).align_to(scroll, UP).shift(1.3*DOWN)

        scroll_properties = []
        for i in range(3):
            scroll_properties.append(
                Tex(scroll_properties_str[i][0], color = GRAY).scale(scroll_properties_scale)
            )
        Group(*scroll_properties).arrange_in_grid(rows = 3, cols = 1, col_alignments="l").next_to(
            scroll_header, DOWN
        ).align_to(scroll_header, LEFT)

        scroll_stuff = Group(scroll, *scroll_properties, scroll_header)
        self.add_fixed_in_frame_mobjects(scroll, scroll_header, scroll_properties[0])

        ############################
    
        # So this fact gives us another constraint on the potentials. Intuitively, what we want is that the potential of every node is at most the distance from that node to Rome. Otherwise, the shortest path from that node to Rome becomes negative which we do not want. 

        necessary = Tex("Every node: Potential(node) $\le$ Old distance(node, Rome)").move_to(background_formula.get_center()).align_to(background_formula, UP)
        self.play(FadeIn(necessary))
        self.wait()

        # In reality, this condition is not enough, in this example it is satisfied but we still got negative edge length here, so the condition that needs to be actually satisfied is more complicated: we want that if we write down the formula for the new edge length, this one, it is always nonnegative. 

        # Of course, having this property implies that the potential of every node is at most the distance from it to Rome, but it is saying a bit more. Basically, it is also saying that potential can never increase abruptly.  [Potenciál se postupně zvedne do trychtýře]. Any potential that satisfies it needs to look like a cone that is 0 at Rome and gets larger as you walk further away from Rome. 

        # Ok, so we want the potential of Prague to be as large as possible, but we also know that its size is at most the distance from Prague to Rome. Can we have equality here? 
        # In fact, what happens if we define a potential of every node to be exactly its distance to Rome? Does it satisfy the inequalities from the second item on our list? Lets see, if we take the inequality and plug in the definition of this potential [distance(u, Rome) <= length(u,v) + distance(v, Rome)], then it is just a triangle inequality that distances have to satisfy so, yes, such a potential satisfies the second point on our list. And also, remember that the first property says that we want the potential of Prague to be as large as possible. This is clearly the case here! [označí se potential(u) <= distance(u, Rome) které je tam pořád napsané]

        # So it looks like we are done! We found a formula for the best possible potential that satisfies both requirements on our list! Or are we still missing something? Well, let’s see what would happen if we apply the potential reweighting trick with this potential and then run Dijkstra’s algorithm on the new graph. You can see that the algorithm simply walks along the shortest path to Rome and it doesn’t even bother exploring anything else. Amazing!

        # It’s actually so amazing that it should also be pretty suspicious. Do you see the problem with this choice of potentials? Well, the problem is how to compute these potentials. Remember, we want to speed up Dijkstra’s algorithm. So computing these potentials should be something that we can do fast. But how do you compute, let’s say, the potential of Prague? It is defined as the length of the shortest path from Prague to Rome. But this shortest path is exactly what we are trying to compute! [animation with chicken and egg or uroboros]

        # So, we have to go back to our list of requirements for a good potential and add a third property - the potential should be something easy to compute. Now we finally have a complete list of requirements. 

        # Here is how you can think about it. Basically, the potential of every node should be something that approximates the distance from that node to Rome. Condition 2 says that it should be an optimistic guess of the actual distances. The actual condition is a bit more complicated than that, but let’s not be too meticulous. Given that the potential satisfies condition 2, we want it to be as close to actual distance as possible, this is what condition 1 says, but we also want it to be easily computable, which is condition 3. 

        # [zobrazí se tabulka]

        # So choosing the potential as the exact distances to Rome satisfies condition two and is amazing on 1, but it is horrible in 3. On the other hand, choosing all potentials to be zero, which leads to simply running the good old Dijkstra’s algorithm, satisfies condition 2 and is great on 3, but it is horrible in 1. 

        # [exact distance, all zero (=normal Dijsktra), air distance]

        # What would be a potential that has all three properties? 
        # Here is one proposal. Remember, we know the geographical position of every city. So, let me define the potential of every city to be not the distance from that city to Rome by road, but the geometrical, airdistance between that city and Rome. 

        # For example, Prague is …km away, so its potential would become … In general, these potentials are then forming a nice cone with Rome in the middle. This potential approximates the true distance from Prague to Rome quite decently. [point 1 je ticked] It is also definitely easy to compute if we know the geographical locations of the cities on the map. If the Earth was flat, we would compute the potential by literally plugging in the two positions to Pythagorean theorem [napsat vzoreček]. The Earth is not flat, but still the same story.  

        # And what about property two? That one is also true, because for any two nodes, we can first use triangle inequality for air distances, and then use the fact that actual distance is always longer than the air distance. 
        # [*Let’s postpone the discussion about Earth’s curvature and digging tunnels to the comment section…]

        # Let’s see what happens if we plug in this potential into our A* algorithm. We start with the original graph, then we elevate every node to appropriate height, and then we run Dijkstra. [strauss?]

        # Nice, you can see how Dijkstra prefers the paths that go in the direction of Rome, simply because they go downhill in our cone, whereas they are slower on the paths that go away, since these paths go uphill. 
        # This is exactly the animation we have seen at the beginning of the video. Pretty nice, right? 
        self.wait(5)




class Chapter3(Scene):
    def construct(self):
        pass
        

class ExploreStrategy(Scene):
    def construct(self):
        yes = clipart_yes_no_maybe("yes", 1).shift(1*LEFT)
        self.add(*yes)
        
        no = clipart_yes_no_maybe("no", 1)
        self.add(*no)
        
        maybe = clipart_yes_no_maybe("maybe", 1).shift(RIGHT)
        self.add(maybe)
        
