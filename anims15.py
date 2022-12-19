from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.solarized import * # TODO nenacita se solarized
from utils.util import *
from utils.util_graph import *
from utils.util_cube import *

random.seed(0)

class Puzzle(Scene):
    def construct(self):
        default()
        self.next_section(skip_animations=True)
        # As a small bonus, I want to give you at least one other application of the A* algorithm, so that you can appreciate that it is not just about finding paths in maps. You see, maps are perhaps not the most typical A* application, since the real algorithms in map applications are using many, many other tricks besides A*. A more authentic application is solving puzzles where your graph represents different states of a puzzle and transitions between them. 

        # This part is going to be a bit faster, so if you are not used to thinking about graphs representing state spaces,  I recommend you to watch this recent amazing video by Tom Sláma, who explains how they work in his video. 

        # The example I want to give you is the 15-puzzle – there you are given a 4x4 square and in it 15 small tiles numbered 1 to 15. The goal is to rearrange the tiles using these kind of moves, so that you get them nicely sorted, like this. 

        tiles = []
        tile_map = {}
        shift_map = {}
        L = 1
        for i in range(15):
            square = Square(side_length = L, fill_color = BLUE, fill_opacity = 1, color = GRAY)
            label = Tex(str(i+1)).move_to(square.get_center())
            tile = Group(square, label)
            tiles.append(tile)
            shift_map[tile] = np.array([0, 0])
            tile_map[(i // 4, i%4)] = tile

        tiles = Group(*tiles).arrange_in_grid(rows = 4, cols = 4, buff= MED_SMALL_BUFF)

        border = Square(side_length=tiles.width + 0.3, color = GRAY)
        title = Tex("15 puzzle").scale(1.4).to_edge(UP)

        Group(tiles, border).shift(1*DOWN)

        # a few random moves
        pos = (3, 3)
        starting_pos = (2,2)
        NUM_MOVES = 10
        anims = []
        forbidden_pos = (-1, -1)
        i = 0
        while(i < NUM_MOVES):
            neighbors = []
            if pos[0] > 0:
                neighbors.append((pos[0] - 1, pos[1]))
            if pos[0] < 3:
                neighbors.append((pos[0] + 1, pos[1]))
            if pos[1] > 0:
                neighbors.append((pos[0], pos[1] - 1))
            if pos[1] < 3:
                neighbors.append((pos[0], pos[1] + 1))

            if forbidden_pos in neighbors:
                neighbors.remove(forbidden_pos)

            neighbor = random.choice(neighbors)
            print(i, neighbor)
            tile_map[neighbor].shift(
                (pos[0] - neighbor[0])*(L + MED_SMALL_BUFF)*DOWN + (pos[1] - neighbor[1])*(L + MED_SMALL_BUFF)*RIGHT 
            )
            shift_map[tile_map[neighbor]][0] -= (pos[0] - neighbor[0])
            shift_map[tile_map[neighbor]][1] -= (pos[1] - neighbor[1])

            anims.append((
                tile_map[neighbor], 
                -(pos[0] - neighbor[0])*(L + MED_SMALL_BUFF)*DOWN + -(pos[1] - neighbor[1])*(L + MED_SMALL_BUFF)*RIGHT 
            ))

            tile_map[pos] = tile_map[neighbor]
            del tile_map[neighbor]

            forbidden_pos = pos
            pos = neighbor

            i += 1
            if i == NUM_MOVES and (pos != starting_pos):
                i -= 1

        print(shift_map)

        self.play(
            FadeIn(border),
            FadeIn(tiles),
            FadeIn(title)
        )
        self.wait()

        for tile in tiles:
            tile[0].save_state(), tile[1].save_state()

        for anim in reversed(anims):
            self.play(
                anim[0].animate.shift(anim[1])
            )
        self.wait()
        
        # If I give you a random solvable position of this puzzle, for example this one, how do you find the shortest possible solution? 

        self.play(
            *[tile[0].animate.restore() for tile in tiles],
            *[tile[1].animate.restore() for tile in tiles]
        )
        self.wait()
        # Well, you can imagine the graph where all possible states of this puzzle are nodes and edges correspond to the moves you can make. 

        picture = Group(tiles, border)

        scale = 0.5        
        self.play(
            picture.animate.scale(scale).shift(1*UP)
        )
        self.wait()

        neighboring_pictures = [picture.copy(), picture.copy(), picture.copy(), picture.copy()]

        for i, (shift, list_pos) in enumerate(zip([(-1, 0), (0, -1), (0, 1), (1, 0)], [11, 9, 8, 15])):
            neighbor_pos = (starting_pos[0] + shift[0], starting_pos[1] + shift[1])

            neighboring_pictures[i][0][list_pos-1].shift(
                -(shift[0])*scale*(L + MED_SMALL_BUFF)*DOWN + -(shift[1])*scale*(L + MED_SMALL_BUFF)*RIGHT 
            )        

        neighboring_pictures[0].shift(4*LEFT + 2 * UP)
        neighboring_pictures[1].shift(4*LEFT + 2 * DOWN)
        neighboring_pictures[2].shift(4*RIGHT + 2 * UP)
        neighboring_pictures[3].shift(4*RIGHT + 2 * DOWN)
        
        def make_edge(i, fr, dir):
            start = neighboring_pictures[i].get_corner(fr)
            end = start + dir * 5
            return Line(start, end, color = GRAY)

        edges = [
            Line(picture.get_corner(UL), neighboring_pictures[0].get_right(), color = GRAY),
            Line(picture.get_corner(DL), neighboring_pictures[1].get_right(), color = GRAY),
            Line(picture.get_corner(UR), neighboring_pictures[2].get_left(), color = GRAY),
            Line(picture.get_corner(DR), neighboring_pictures[3].get_left(), color = GRAY),
            #
            make_edge(0, UL, UL),
            make_edge(0, LEFT, LEFT),
            make_edge(0, UP, UP),
            #
            make_edge(1, DL, DL),
            make_edge(1, LEFT, LEFT),
            make_edge(1, DOWN, DOWN),
            #
            make_edge(2, RIGHT, RIGHT),
            make_edge(2, UP, UP),
            #
            make_edge(3, RIGHT, RIGHT),
            make_edge(3, DOWN, DOWN),            
        ]

        self.play(
            *[FadeIn(pic) for pic in neighboring_pictures],
            *[FadeIn(edge) for edge in edges],
        )
        self.wait()

        
        # In this graph, you can run breadth first search to find the shortest path, but I would not advise that. The graph has roughly 10^13 (= 16! = 2x10^13 ) possible states of the puzzle [*half of them in one connected component], so you would need to run the code for weeks at least and use terabytes of memory. So let’s improve on it by finding a good heuristic and then run A*. 

        bound = Tex(r"{{$16! \approx 2 \cdot 10^{13}$ nodes \\ }}{{in two connected components}}")
        bound[1].scale(0.7)
        bound.next_to(picture, DOWN, buff = 1)

        self.play(
            FadeIn(bound)
        )
        self.wait()

        self.play(
            FadeOut(bound),
            *[FadeOut(pic) for pic in neighboring_pictures],
            *[FadeOut(edge) for edge in edges],            
            picture.animate.shift(0*DOWN).scale(1/scale)
        )
        self.wait()

        # Remember, our heuristic should basically be an optimistic guess on the number of moves that we need to solve given configuration. 

        tex_heuristic = Tex(r"A* heuristic $\approx$ an optimistic guess on how many moves are needed. ").scale(0.7).next_to(picture, DOWN, buff = 0.5)
        self.play(
            FadeIn(tex_heuristic)
        )
        self.wait()


        # One simple heuristic is to look at each tile separately and compute how many moves we would need to put it in its place. Like, we need … moves to put the tile 1 to the final configuration, … moves to put the tile 2 and so on. If we sum up all these numbers, we get a lower bound on the number of moves we need to solve the whole puzzle. 

        self.play(
            picture.animate.shift(2*LEFT)
        )

        tex_our_heuristic = Tex(r"Our heuristic = ").scale(0.7).next_to(picture, RIGHT, buff = 1)
        num = Integer(0).next_to(tex_our_heuristic, RIGHT, 0.3)

        self.play(
            FadeIn(tex_our_heuristic),
            FadeIn(num),
        )
        self.wait()

        self.next_section(skip_animations=False)

        for i in range(15):

            new_tile = tiles[i].copy()
            self.add(new_tile)

            self.play(
                *[FadeOut(tile) for tile in tiles]
            )
            self.wait()

            for _ in range(abs(shift_map[tiles[i]][0])):
                self.play(
                    new_tile.animate.shift(np.sign(shift_map[tiles[i]][0]) * (L + MED_SMALL_BUFF) * DOWN),
                    num.animate.increment_value(1),
                    run_time = 0.5
                )
            for _ in range(abs(shift_map[tiles[i]][1])):
                self.play(
                    new_tile.animate.shift(np.sign(shift_map[tiles[i]][1]) * (L + MED_SMALL_BUFF) * RIGHT),
                    num.animate.increment_value(1),
                    run_time = 0.5
                )

            self.wait()
            self.play(FadeOut(new_tile))
            self.play(
                *[FadeIn(tile) for tile in tiles]
            )
            self.wait()


        tex_actual = Tex("Actual distance = ??").next_to(tex_our_heuristic, DOWN).align_to(tex_our_heuristic, LEFT)
        self.play(FadeIn(tex_actual))
        self.wait()
        self.play(
            FadeOut(tex_actual),
            FadeOut(num),
            FadeOut(tex_our_heuristic),
            FadeOut(tex_heuristic),
        )
        self.wait()

        list_stuff = create_potential_list([-1, -1, -1, -1]).next_to(picture, RIGHT, buff = 1)
        
        self.play(
            FadeIn(list_stuff),
        )
        self.wait()

        # Being a lower bound is not enough, we need to check that the heuristic is consistent but that is simple to do too. 
        
        height = 0.5
        yeses = [
            clipart_yes_no_maybe("yes", height = height).next_to(list_stuff[2 + 0], LEFT),
            clipart_yes_no_maybe("yes", height = height).next_to(list_stuff[2 + 1], LEFT),
            clipart_yes_no_maybe("yes", height = height).next_to(list_stuff[2 + 2], LEFT),
            clipart_yes_no_maybe("yes", height = height).next_to(list_stuff[2 + 3], LEFT),
        ]
        self.play(
            Succession(
                FadeIn(yeses[0]),
                FadeIn(yeses[3]),
                FadeIn(yeses[2]),
                FadeIn(yeses[1]),
            )
        )        
        self.wait()
        
        # Also, we can compute the heuristic very fast, so we can plug it into A* and see what happens. We of course tried it out, and this is the result. On average, we needed a explored roughly only 10 million nodes in roughly 10 seconds. [ZBYTECNE *You can deal with high memory by running IDA* which relates to iterative deepening DFS the same way A* relates to Dijkstra. ]

        tex_on_average = Tex("On average: $\sim$10\,000\,000 explored nodes and $\sim$ 10 seconds to find a solution. ").scale(0.6).to_edge(DOWN)
        self.play(FadeIn(tex_on_average))
        self.wait()

        # I really wanted to show you this example because it features a very different heuristic than the one we saw in the case of road network graphs. In general, the A* algorithm is so amazing because whenever you decide to use it, the only problem specific challenge you need to address is finding a good consistent heuristic and then the A* framework does the rest. [split screen, ukázat oba příklady]


        self.play(
            *[FadeOut(yes) for yes in yeses],
            FadeOut(list_stuff),
            FadeOut(title),
            FadeOut(tex_on_average),
            #picture.animate.move_to(0.5 * config.frame_width/2 * RIGHT + 0.5 * config.frame_height/2 * UP).scale(0.5)

        )
        self.wait()
        
        



 
class Puzzle2(RubikScene):
    def construct(self):
        default()
        picture = Circle(1)
        picture.generate_target()
        picture.target.scale(0.5)

        background, europe_boundary, G = clipart_map_europe(SCALE_EUROPE)
        graph = Group(background, europe_boundary, G).move_to(0.5 * config.frame_width/2 * LEFT + 0.5 * config.frame_height/2 * UP).scale(0.2)

        rubik_cube = RubiksCube(cubie_size=0.5)
        Tex.set_default(font_size = 30)
        
        table = Group(
            Dot(), Tex("Maps").scale(2), Tex("15 puzzle").scale(2), Tex("Rubik's cube").scale(2),
            Dot(), graph, picture.target, rubik_cube,
            Tex("Heuristic: "), Tex("Air distance"), Tex("sum of individual distances"), Tex(r"Heuristic(u) = min(dist(u, target), diameter/2)\\ a.k.a. meet in the middle if you know diameter").scale(0.7),
            Tex("Speedup: "), Tex(r"$4\times$"), Tex(r"$10^6\times$"), Tex(r"$10^{10}\times$")
        ).arrange_in_grid(rows = 4, cols = 4).move_to(ORIGIN)

        self.play(
            *[FadeIn(t) for t in table[1:3]],
            FadeIn(graph), MoveToTarget(picture),
            *[FadeIn(t) for t in table[8:11]],
            *[FadeIn(t) for t in table[12:15]],
        )
        self.wait()


        # By the way, if this puzzle reminds you of our earlier video about solving Rubik’s cube using meet in the middle trick, then you will be delighted to know that A* is an even more powerful approach for solving the cube. 
        # In fact, you can kind of interpret the meet in the middle trick as running A* with a certain heuristic [na scéně obrázek grafu s potenciály co vypadají jako obrácený klobouk - možná k tomu šipka a “heuristic = precomputing distances from target up to distance 4” nebo tak něco] which I think shows how general and powerful A* is. Actually this is also why it’s called A*, it’s simply the best algorithm there is. 

        self.play(
            FadeIn(table[3]),
            FadeIn(table[7]),
            FadeIn(table[11]),
            FadeIn(table[15]),
        )
        self.wait()

        # So, I hope you like it too and will see you next time. 

