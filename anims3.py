from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.solarized import * # TODO nenacita se solarized
from utils.util import *
from utils.util_graph import *
from utils.util_cube import *

random.seed(0)

class DvsA(Scene):
    def construct(self):
        default()
        sc = 0.7
        tex_name = Tex(r"{{Dijkstra}}{{A*}}").shift(1*UP)
        tex_opt = [
            Tex(r"{{pick $u$ with smallest: \\ }}{{distance(start, $u$)}}").scale(sc),
            Tex(r"{{pick $u$ with smallest: \\ }}{{distance(start, $u$) + potential($u$)}}").scale(sc)
        ]
        tex_opt1 = Tex(r"$\approx$ distance(start, $u$) + distance($u$, end)").scale(sc)
        tex_opt2 = Tex(r"$\approx$ distance from start to end via $u$").scale(sc)


        circle_pos = [
            np.array([-6.09142, -0.937142, 0]),
            np.array([12.3752, -15.2073, 0]),
            np.array([-15,.7391 -15.2073, 0]),
            np.array([-47,.6019 -6.77303, 0]),
            np.array([-43.3847, 19.9355, 0]),
            np.array([-26.0476, 33.9926, 0]),
            np.array([-6.36764, 20.4041, 0]),
            np.array([12.3752, 32.1183, 0]),
            np.array([29.2437, 20.4041, 0]),
            np.array([-23.8973, 14.5252, 0]),
            np.array([17.8055, 4.21666, 0]),
            np.array([-34.6745, -22.0233, 0]),
            np.array([-16.8688, -36.549, 0]),
            np.array([56.4209, -77.059, 0]),
            np.array([-1.21336, -23.1734, 0]),
            np.array([21.7466, -32.0762, 0]),
            np.array([35.3352, -7.71054, 0]),
            np.array([-13.3962, 47.1122, 0]),
            np.array([5.81521, 47.5808, 0]),
            np.array([-30.7338, -2.08736, 0]),
            np.array([1.59785, -41.9158, 0]),
            np.array([196.331, -2.34318, 0]),
            np.array([214.797, -16.6133, 0]),
            np.array([186.683, -16.6133, 0]),
            np.array([191.837, -54.099, 0]),
            np.array([209.174, -62.5333, 0]),
            np.array([221.826, -54.5676, 0]),
            np.array([196.054, 18.9981, 0]),
            np.array([243.38, -64.4076, 0]),
            np.array([218.546, -78.9332, 0]),
            np.array([178.525, 13.1192, 0]),
            np.array([220.228, 2.81062, 0]),
            np.array([185.553, -37.955, 0]),
            np.array([258.843, -78.465, 0]),
            np.array([201.209, -24.5794, 0]),
            np.array([224.169, -33.4822, 0]),
            np.array([237.757, -9.11658, 0]),
            np.array([240.569, -32.5452, 0]),
            np.array([248.534, -49.4137, 0]),
            np.array([171.688, -3.4934, 0]),
            np.array([204.02, -43.3218, 0]),
            np.array([235.415, -78.933, 0]),
        ]

        def is_left(i):
            return (0 <= i and i < len(circle_pos)//2)
        def is_source(i):
            return i == 0 or i == 21
        def is_target(i):
            return i == 13 or i == 33
        def is_closed(i):
            return i in [0, 1, 2, 14, 19, 9, 10, 21, 22, 34, 35, 40]
        def is_being_closed(i):
            return i in [6, 26]
        def is_being_opened(i):
            return i in [17, 18, 29, 41]


        circles = []
        for pos in circle_pos:
            circle = Circle(radius = 0.2, fill_opacity = 1, color = BLUE, fill_color = BLUE).move_to(
                pos/35.0
            )
            circles.append(circle)
        Group(*circles).move_to(1*UP)

        for i in range(len(circles)):
            if is_closed(i):
                circles[i].set(fill_color = GRAY)
                circles[i].set_color(GRAY)
            if is_source(i) or is_target(i):
                circles[i].set(fill_color = BLACK)
                circles[i].set_color(BLACK)
            if not is_left(i):
                circles[i].shift(0.5*LEFT + 0* UP)
            if is_left(i):
                circles[i].shift(0.5*DOWN)
            # self.add(Tex(i).scale(1.5).move_to(circles[i].get_center()))



        # nejdriv dijkstra pak A*
        start = [0, 21]
        end = [13, 33]
        open = [6, 26]
        tex_start = [Tex("start", color = BLACK).scale(0.7), Tex("start", color = BLACK).scale(0.7)]
        tex_end = [Tex("end", color = BLACK).scale(0.7), Tex("end", color = BLACK).scale(0.7)]
        
        for i in range(2):
            tex_start[i].next_to(circles[start[i]], UR, buff = 0.05).set(z_index = 100)
            tex_end[i].next_to(circles[end[i]], DOWN, buff = 0.2 ).set(z_index = 100)
            tex_name[i].move_to(circles[start[i]].get_center())
            tex_name[i].shift(2.0*UP)
            tex_opt[i][0].move_to(circles[start[i]].get_center())
            tex_opt[i][0].shift(3.0*DOWN)
            tex_opt[i][1].next_to(tex_opt[i][0], DOWN, buff = 0.2)

            self.play(
                FadeIn(tex_name[i]),
                FadeIn(tex_start[i]),
                FadeIn(tex_end[i]),
                FadeIn(circles[start[i]]),
                FadeIn(circles[end[i]]),
            )
            self.wait()
            self.play(
                *[FadeIn(circ) for j, circ in enumerate(circles) if (
                    (i==0 and is_left(j)) or (i==1 and not is_left(j))
                ) and not is_being_opened(j) and not is_source(j) and not is_target(j)],
            )

            self.play(
                circles[open[i]].animate.set_color(RED),
                FadeIn(tex_opt[i][1]),
            )
            self.wait()
            self.play(
                circles[open[i]].animate.set_color(GRAY),
                *[FadeIn(c) for j, c in enumerate(circles) if is_being_opened(j) and (
                    (i==0 and is_left(j)) or (i==1 and not is_left(j))
                )],
            )
            self.wait()


        tex_opt1.next_to(tex_opt[1], DOWN, buff = 0.2)
        self.play(FadeIn(tex_opt1))
        self.wait()

        tex_opt2.move_to(tex_opt1.get_center())
        self.play(Transform(tex_opt1, tex_opt2))
        self.wait()

class Consistency(Scene):
    def construct(self):
        default()

        pot_list = create_potential_list([1, 1, 1, 1])
        self.play(FadeIn(pot_list))
        self.wait()

        tex_ph = Tex("Potential = Heuristic").next_to(pot_list, DOWN, buff = 1)
        pot_list2 = create_potential_list([2, 2, 2, 2], heuristic=True)
        self.play(
            *[Transform(pot_list[i], pot_list2[i]) for i in list(range(1, 6))],
            FadeIn(tex_ph),
        )
        self.wait()

        tex_c = Tex("Consistency: ").next_to(pot_list[3], LEFT, buff = 0.3)
        tex_a = Tex("Admissibility: ").next_to(pot_list[4], LEFT, buff = 0.3)

        self.play(FadeIn(tex_c))
        self.wait()
        self.play(FadeIn(tex_a))
        self.wait()
        

class Practice(Scene):
    def construct(self):
        default()

        img = ImageMobject("img/practice.png").scale_to_fit_height(8)
        tex_d = Tex("Dijkstra: $\sim 200\,000$ nodes").move_to(4*LEFT + 3*UP)
        tex_a = Tex("A*: $\sim 47\,000$ nodes").move_to(0*RIGHT).shift(1*UP)
        rec_d = SurroundingRectangle(tex_d, fill_color = config.background_color, fill_opacity = 1, color = config.background_color)
        rec_a = SurroundingRectangle(tex_a, fill_color = config.background_color, fill_opacity = 1, color = config.background_color)
        tex_credit = Tex(r"""{100cm}https://public.opendatasoft.com/explore/dataset/europe-road/export/?refine.icc=BE""", 
        tex_environment='minipage').scale(0.5).to_corner(DL, buff = 0.1)
        tex_credit2 = Tex(r"https://geojson.io/").scale(0.5).to_corner(DR, buff = 0.1)
        #Group(tex_credit, tex_credit2).arrange_in_grid(cols = 1, cell_alignment=LEFT).to_corner(DL)

        self.add(img,  rec_d, rec_a, tex_d, tex_a,tex_credit, tex_credit2)

class Negative(Scene):
    def construct(self):
        default()
        tex1 = Tex("Shortest path in graphs with negative edges?*").shift(2*UP)
        texass = Tex("*Assuming there are no negative length cycles. ").scale(0.4).to_edge(DOWN)
        tex15 = Tex(r"{{Algorithm }}{{Time complexity").scale(0.7)
        
        tex2 = Tex(r"{{Bellman-Ford (1950's): }}{{$O(mn)$").scale(0.7)
        tex25 = Tex(r"{{Gabow-Tarjan (1989): }}{{$O(m\sqrt{n} \cdot \text{polylog}(n) )$").scale(0.7)
        tex3 = Tex(r"{{Bernstein, Nanongkai, Wulff-Nilsen (2022): }}{{$O((m+n) \cdot \text{polylog}(n))$").scale(0.7)
        tex4 = Tex(r"A simpler application in video description. ").scale(0.4).next_to(texass, DOWN, buff = 0.1)
        Group(tex15[0], tex15[1], tex2[0], tex2[1], tex25[0], tex25[1], tex3[0], tex3[1]).arrange_in_grid(cols = 2, cell_alignment=LEFT).next_to(tex1, DOWN, buff = 2)
        tex15.shift(0.5*UP)

        self.play(
            FadeIn(tex1),
            FadeIn(texass)
        )
        self.wait()
        
        self.play(
            FadeIn(tex15)
        )
        self.wait()

        self.play(
            FadeIn(tex2)
        )
        self.wait()

        self.play(
            FadeIn(tex25)
        )
        self.wait()
        
        self.play(
            FadeIn(tex3)
        )
        self.wait()

        self.play(
            FadeIn(tex4)
        )
        self.wait()
