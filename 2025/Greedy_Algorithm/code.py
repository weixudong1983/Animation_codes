from manimlib import *

class Greedy(Scene):

    def construct(self):
        self.camera.frame.scale(0.78).shift(UP*0.65)
        # Define positions for each node in the tree
        positions = {
            "root": ORIGIN + UP * 3,                           # (Start)
            "L1": ORIGIN + UP * 1.5 + LEFT * 2,                # Left child of root
            "R1": ORIGIN + UP * 1.5 + RIGHT * 2,               # Right child of root
            "LL2": ORIGIN + LEFT * 3,                          # Left child of L1
            "LR2": ORIGIN + LEFT * 1,                          # Right child of L1
            "RL2": ORIGIN + RIGHT * 1,                         # Left child of R1
            "RR2": ORIGIN + RIGHT * 3,                         # Right child of R1
            "LLL3": ORIGIN + LEFT * 3.5 + DOWN * 1.5,          # Left child of LL2
            "LLR3": ORIGIN + LEFT * 2.5 + DOWN * 1.5,          # Right child of LL2
            "LRL3": ORIGIN + LEFT * 1.5 + DOWN * 1.5,          # Left child of LR2
            "LRR3": ORIGIN + LEFT * 0.5 + DOWN * 1.5,          # Right child of LR2
            "RLL3": ORIGIN + RIGHT * 0.5 + DOWN * 1.5,         # Left child of RL2
            "RLR3": ORIGIN + RIGHT * 1.5 + DOWN * 1.5,         # Right child of RL2
            "RRL3": ORIGIN + RIGHT * 2.5 + DOWN * 1.5,         # Left child of RR2
            "RRR3": ORIGIN + RIGHT * 3.5 + DOWN * 1.5,         # Right child of RR2
        }

        # Create nodes. The root gets labeled "Start" and is moved slightly up
        nodes = {}
        start = None
        for key, pos in positions.items():
            if key == "root":
                label = Text("", font_size=24).set_color(BLACK)
            else:
                label = Text("", font_size=24).set_color(BLACK)
            label.move_to(pos)
            node = VGroup(label)
            nodes[key] = node
            start = label

        # Add all the nodes to the scene
        for node in nodes.values():
            self.add(node)

        # Define edges between nodes as tuples: (start_node, end_node, weight)
        edges = [
            ("root", "L1", "4"),
            ("root", "R1", "2"),
            ("L1", "LL2", "1"),
            ("L1", "LR2", "3"),
            ("R1", "RL2", "5"),
            ("R1", "RR2", "6"),
            ("LL2", "LLL3", "7"),
            ("LL2", "LLR3", "9"),
            ("LR2", "LRL3", "8"),
            ("LR2", "LRR3", "2"),
            ("RL2", "RLL3", "3"),
            ("RL2", "RLR3", "4"),
            ("RR2", "RRL3", "1"),
            ("RR2", "RRR3", "5"),
        ]

        # Dictionary to store weight labels
        self.weight_labels = {}

        # Draw edges and label them with offset weights
        for start_key, end_key, weight in edges:
            start_pos = positions[start_key]
            end_pos = positions[end_key]
            
            # Draw the edge as a black line
            edge_line = Line(start_pos, end_pos, color=BLACK)
            self.play(ShowCreation(edge_line), run_time=0.15)
            
            # Calculate midpoint
            mid_point = (start_pos + end_pos) / 2
            
            # Determine if this is a left or right edge
            is_left_edge = end_pos[0] < start_pos[0]
            
            # Offset the weight label based on whether it's a left or right edge
            offset = LEFT * 0.3 if is_left_edge else RIGHT * 0.3
            weight_label = Text(weight, font_size=20).move_to(mid_point + offset).set_color(BLACK)
            self.play(Write(weight_label), run_time=0.15)
            
            # Store the weight label
            label_key = f"{start_key}_{end_key}"
            self.weight_labels[label_key] = weight_label

        self.wait(3)

        # Add a decorative floor line
        floor_y = min(pos[1] for pos in positions.values()) - 0.5
        floor_left_x = min(pos[0] for pos in positions.values()) - 1
        floor_right_x = max(pos[0] for pos in positions.values()) + 1
        
        # Create main floor line
        floor_line = Line(
            LEFT * abs(floor_left_x) + DOWN * abs(floor_y),
            RIGHT * abs(floor_right_x) + DOWN * abs(floor_y),
            color=GREY_E
        )

        temp =[]
        
        # Add some decorative parallel lines to create a "reflection" effect
        for i in range(1, 4):
            reflection_line = Line(
                LEFT * abs(floor_left_x) + DOWN * (abs(floor_y) + i * 0.1),
                RIGHT * abs(floor_right_x) + DOWN * (abs(floor_y) + i * 0.1),
                color=GREY_E,
                stroke_opacity=0.5 / i
            )
            temp.append(ShowCreation(reflection_line))
        
        temp.append(ShowCreation(floor_line))
        self.play(*temp, run_time=0.8)

        self.wait(2)

        start = Text("Bob", font_size=24).set_color(BLACK).to_edge(UP)
        self.play(Write(start), run_time=0.5)
        self.wait(2)

        # Highlight the left weight (root to L1)
        left_weight = self.weight_labels["root_L1"]
        right_weight = self.weight_labels["root_R1"]

        circle1 = Circle(stroke_color="#0000FF", stroke_width=7).move_to(left_weight).scale(0.3)
        circle2 = Circle(stroke_color="#0000FF", stroke_width=7).move_to(right_weight).scale(0.3)
        self.play(ShowCreation(circle1),ShowCreation(circle2),)
        self.wait(2)
        self.play(Uncreate(circle1),Uncreate(circle2),) 

        line_right = Line(start=positions["root"], end=positions["R1"], color="#FF0000", stroke_width=7)
        self.play(ShowCreation(line_right), start.animate.move_to(positions["R1"]+RIGHT*0.6+UP*0.15),
        self.camera.frame.animate.shift(DOWN*0.15))

        self.wait(1)

        line_right_left = Line(start=positions["R1"], end=positions["RL2"], color="#FF0000", stroke_width=7)
        self.play(ShowCreation(line_right_left),
        start.animate.move_to(positions["RL2"]+RIGHT*0.5))

        self.wait(2)

        line_right_left1 = Line(start=positions["RL2"], end=positions["RLL3"], color="#FF0000", stroke_width=7)
        self.play(ShowCreation(line_right_left1), start.animate.move_to(positions["RLL3"]+DOWN*0.23),)

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*0.6))
        self.wait(2)

        temp = self.weight_labels["root_R1"]
        temp1 = self.weight_labels["R1_RL2"]
        temp2 = self.weight_labels["RL2_RLL3"]


        text = Text("2 + 5 + 3", font_size=24).set_color(BLACK).to_edge(RIGHT).shift(LEFT*1.5+UP*2)
        self.play(FadeIn(Group(text[1], text[3])),
        TransformFromCopy(temp, text[0]),TransformFromCopy(temp1, text[2]),
        TransformFromCopy(temp2, text[4]),)

        self.wait(2)

        self.play(text.animate.become(Text("10", font_size=24).set_color(BLACK).move_to(text).scale(1.2)),)
        self.wait(2)
        self.play(FadeOut(text))
        self.wait(1)

        line = Line(start=positions["root"], end=positions["L1"], color="#00FF00", stroke_width=7)
        line1 = Line(start=positions["L1"], end=positions["LR2"], color="#00FF00", stroke_width=7)
        line2 = Line(start=positions["LR2"], end=positions["LRR3"], color="#00FF00", stroke_width=7)

        self.play(ShowCreation(line))
        self.play(ShowCreation(line1))
        self.play(ShowCreation(line2))

        temp = self.weight_labels["root_L1"]
        temp1 = self.weight_labels["L1_LR2"]
        temp2 = self.weight_labels["LR2_LRR3"]


        text = Text("4 + 3 + 2", font_size=24).set_color(BLACK).to_edge(RIGHT).shift(LEFT*1.5+UP*2)
        self.play(FadeIn(Group(text[1], text[3])),
        TransformFromCopy(temp, text[0]),TransformFromCopy(temp1, text[2]),
        TransformFromCopy(temp2, text[4]),)

        self.wait(2)

        self.play(text.animate.become(Text("9", font_size=24).set_color(BLACK).move_to(text).scale(1.2)),)
        self.wait(2)
        self.wait(1)



class Knapsack(Scene):

    def construct(self):
        
        bag = ImageMobject("sack.png").scale(0.8).shift(DOWN*1.92).shift(LEFT*0.49)
        self.play(GrowFromCenter(bag))
        weight = Text("6 - 3").set_color(BLACK).scale(1.5).next_to(bag, RIGHT).shift(RIGHT*0.2)
        self.play(Write(weight[0]))
        self.wait(2)

        orange = ImageMobject("banana.png").scale(0.6).to_edge(UP)
        fish1 = ImageMobject("fish.png").scale(0.6).next_to(orange, RIGHT)
        grapes = ImageMobject("grapes.png").scale(0.7).next_to(orange, LEFT)
        grapes.shift(LEFT*1.1)
        orange.shift(LEFT*0.46)

        self.play(GrowFromCenter(orange), GrowFromCenter(fish1), GrowFromCenter(grapes))
        self.wait(1)

        grape_text = Text("{3,9}").set_color(BLACK).next_to(grapes, DOWN)
        orange_text = Text("{2,5}").set_color(BLACK).next_to(orange, UP).shift(DOWN+RIGHT*0.45)
        fish_text = Text("{2,4}").set_color(BLACK).next_to(fish1, DOWN)

        self.play(Write(grape_text), Write(orange_text), Write(fish_text))

        self.wait(2)

        arrow = Arrow(grape_text[1].get_bottom()+DOWN*2, grape_text[1].get_bottom()+DOWN*0.1, stroke_width=5).set_color("#FF0000")
        self.play(GrowArrow(arrow))
        self.wait(2)

        self.play(arrow.animate.become(Arrow(grape_text[3].get_bottom()+DOWN*2, grape_text[3].get_bottom()+DOWN*0.1, stroke_width=5).set_color("#FF0000")))

        self.wait(2)

        self.play(grapes.animate.next_to(bag, UP).shift(DOWN*2.2).scale(0.0001), run_time=1.77)

        self.wait(1)

        self.play(TransformFromCopy(grape_text[1], weight[1:]))

        self.wait()
        self.play(weight.animate.become(Text("3").set_color(BLACK).scale(1.5).next_to(bag, RIGHT).shift(RIGHT*0.2)))

        profit_text = Text("9").set_color(BLACK).next_to(bag, LEFT).scale(1.5).shift(LEFT*0.6)
        self.play(TransformFromCopy(grape_text[-2],profit_text))

        self.play(FadeOut(grape_text),)
        self.play(arrow.animate.become(Arrow(orange_text[1].get_bottom()+DOWN*2, orange_text[1].get_bottom()+DOWN*0.1, stroke_width=5).set_color("#FF0000")))
        self.play(arrow.animate.become(Arrow(orange_text[1].get_bottom()+DOWN*2, orange_text[3].get_bottom()+DOWN*0.1, stroke_width=5).set_color("#FF0000")))
        self.wait(1)

        self.play(arrow.animate.become(Arrow(fish_text[1].get_bottom()+DOWN*2, fish_text[1].get_bottom()+DOWN*0.1, stroke_width=5).set_color("#FF0000")))
        self.play(arrow.animate.become(Arrow(fish_text[1].get_bottom()+DOWN*2, fish_text[3].get_bottom()+DOWN*0.1, stroke_width=5).set_color("#FF0000")))

        self.wait(2)

        self.play(FadeOut(arrow),
        orange.animate.next_to(bag, UP).shift(DOWN*2.2).scale(0.0001),)

        self.wait(1)

        weight2 = Text("-2").set_color(BLACK).scale(1.5).next_to(weight, RIGHT)
        self.play(TransformFromCopy(orange_text[1], weight2))

        self.wait(1)

        weight3 = Text("1").set_color(BLACK).scale(1.5).move_to(Group(weight, weight2), RIGHT).shift(LEFT*0.6)

        self.play(ReplacementTransform(VGroup(weight, weight2), weight3))
        self.wait(1)



        self.play(profit_text.animate.shift(LEFT*2.2))
        temp = Text("+ 5").next_to(profit_text, RIGHT).set_color(BLACK).scale(1.5).shift(RIGHT*0.6)
        self.play(TransformFromCopy(orange_text[-2], temp))

        self.wait(1)

        profit = Text("14").set_color(BLACK).move_to(Group(profit_text, temp)).scale(1.5).shift(RIGHT*0.2)

        self.play(ReplacementTransform(VGroup(profit_text, temp), profit))
        self.play(FadeOut(orange_text))

        self.wait(1)

        fish_1 = ImageMobject("fish_1.png").scale(0.6).to_edge(UP)
        fish_2 = ImageMobject("fish_2.png").scale(0.6).next_to(fish_1, RIGHT)

        Group(fish_2, fish_1).move_to(fish1, RIGHT)

        arrow = Arrow(fish_text[1].get_bottom()+DOWN*2, fish_text[1].get_bottom()+DOWN*0.1, stroke_width=5).set_color("#FF0000")
        self.play(GrowArrow(arrow))
        self.wait(2)

        self.play(FadeOut(fish1), FadeIn(fish_1), FadeIn(fish_2))
        self.wait(1)

        self.play(fish_1.animate.next_to(bag, UP).shift(DOWN*2.2).scale(0.0001),)
        self.wait(1)

        self.play(arrow.animate.rotate(PI/2, ).shift(DOWN*1.2))

        self.wait()
        self.play(FadeOut(weight3))
        self.wait()

        self.play(arrow.animate.rotate(PI/2).shift(LEFT*7.8+UP*1.43))
        self.wait()
        self.play(profit.animate.shift(LEFT*1.7))
        temp = Text("+ 2").next_to(profit, RIGHT).set_color(BLACK).scale(1.5).shift(RIGHT*0.5)
        self.play(TransformFromCopy(fish_text[-2], temp))

        self.wait(1)

        profit_last = Text("16").set_color(BLACK).move_to(Group(profit, temp)).scale(1.5).shift(RIGHT)

        self.play(ReplacementTransform(VGroup(profit, temp), profit_last))
        self.play(FadeOut(fish_text), FadeOut(arrow),FadeOut(fish_2))
        self.play(self.camera.frame.animate.shift(DOWN*1.8+LEFT).scale(0.8))

        self.wait(2)

PURE_RED = "#FF0000"

class Example(Scene):

    def construct(self):

        self.camera.frame.shift(RIGHT*1.8)

        array = Array(array_size=5).shift(UP*2.4)
        array.append_element(self, "10")
        array.append_element(self, "25")
        array.append_element(self, "40")
        array.append_element(self, "50")
        array.append_element(self, "30")

        for i in range(5):
            array.square_contents[i]

        array1 = Array(array_size=5).next_to(array, DOWN, buff=0)
        BLUE = TEAL_B
        array1.append_element1(self, "60", color=BLUE)
        array1.append_element1(self, "100", color=BLUE)
        array1.append_element1(self, "120", color=BLUE)
        array1.append_element1(self, "140", color=BLUE)
        array1.append_element1(self, "150", color=BLUE)

        for i in range(5):
            array1.square_contents[i]

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(5)])
        self.wait(2)
        self.play(ShowCreation(array1), *[ShowCreation(array1.square_contents[i]) for i in range(5)])
        self.wait(2)
        n = Text("N = 5").set_color(BLACK).next_to(array, RIGHT).shift(RIGHT*1.75)
        w = Text("W = 70").set_color(BLACK).next_to(n,DOWN).shift(DOWN*0.64)

        self.play(Write(n))
        self.wait(2)
        self.play(Write(w))
        self.wait(2)

        a = Tex(r"\frac{60}{10}").set_color(BLACK).next_to(array1.square_contents[0], DOWN).scale(1.34).shift(DOWN*0.3)
        b = Tex(r"\frac{100}{25}").set_color(BLACK).next_to(array1.square_contents[1], DOWN).scale(1.34).shift(DOWN*0.3)
        c = Tex(r"\frac{120}{40}").set_color(BLACK).next_to(array1.square_contents[2], DOWN).scale(1.34).shift(DOWN*0.3)
        d = Tex(r"\frac{140}{70}").set_color(BLACK).next_to(array1.square_contents[3], DOWN).scale(1.34).shift(DOWN*0.3)
        e = Tex(r"\frac{150}{30}").set_color(BLACK).next_to(array1.square_contents[4], DOWN).scale(1.34).shift(DOWN*0.3)

        self.play(TransformFromCopy(array1.square_contents[0][1], a[:2]),
                  TransformFromCopy(array1.square_contents[1][1], b[:3]),
                  TransformFromCopy(array1.square_contents[2][1], c[:3]),
                  TransformFromCopy(array1.square_contents[3][1], d[:3]),
                  TransformFromCopy(array1.square_contents[4][1], e[:3]),
                  )
        
        self.play(FadeIn(Group(a[2], b[3], c[3], d[3], e[3])))

        self.play(TransformFromCopy(array.square_contents[0][1], a[3:]),
                  TransformFromCopy(array.square_contents[1][1], b[4:]),
                  TransformFromCopy(array.square_contents[2][1], c[4:]),
                  TransformFromCopy(array.square_contents[3][1], d[4:]),
                  TransformFromCopy(array.square_contents[4][1], e[4:]),
                  )
        
        self.wait(2)

        self.play(a.animate.become(Text("6").set_color(BLACK).move_to(a).scale(0.8).shift(UP*0.3)),
                  b.animate.become(Text("4").set_color(BLACK).move_to(b).scale(0.8).shift(UP*0.3)),
                  c.animate.become(Text("3").set_color(BLACK).move_to(c).scale(0.8).shift(UP*0.3)),
                  d.animate.become(Text("2.8").set_color(BLACK).move_to(d).scale(0.8).shift(UP*0.3)),
                  e.animate.become(Text("5").set_color(BLACK).move_to(e).scale(0.8).shift(UP*0.3)))
        
        self.wait(2)
        
        a1, b1, c1, d1, e1 = a.copy().shift(DOWN), b.copy().shift(DOWN), c.copy().shift(DOWN), d.copy().shift(DOWN), e.copy().shift(DOWN)

        self.play(TransformFromCopy(a, a1),
                  TransformFromCopy(b, b1),
                  TransformFromCopy(c, c1),
                  TransformFromCopy(d, d1),
                  TransformFromCopy(e, e1),
                  )
        
        temp_b = b1.get_center()
        temp_c = c1.get_center()
        temp_d = d1.get_center()
        temp_e = e1.get_center()

        self.play(
            e1.animate.move_to(temp_b),
            b1.animate.move_to(temp_c),
            c1.animate.move_to(temp_d),
            d1.animate.move_to(temp_e),  
                  )
        
        self.wait(2)

        profit = Text("profit = 0").set_color(BLACK).to_edge(DOWN).shift(UP*0.2+RIGHT*1.6)
        self.play(Write(profit))
        self.wait(2)

        circle = Circle(radius=0.4, stroke_color="#0000FF", stroke_width=6).move_to(a1)
        self.play(ShowCreation(circle))
        self.wait(1)
        self.play(circle.animate.move_to(a))

        self.wait(1)


        rect = SurroundingRectangle(profit, color="#0000FF", stroke_width=6).scale(1.3)
        self.play(ReplacementTransform(circle, rect))
        self.wait(1)    

        self.play(profit.animate.become(Text("profit = 60").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(w, color="#0000FF", stroke_width=6).scale(1.2)))
        self.wait()
        self.play(w.animate.become(Text("W = 60").set_color(BLACK).move_to(w)), run_time=0.5)
        self.wait()

        circle = Circle(radius=0.4, stroke_color="#0000FF", stroke_width=6).move_to(e1)
        self.play(Transform(rect, circle))
        self.wait()
        self.play(rect.animate.move_to(e))
        self.wait(2)

        rect1 = SurroundingRectangle(profit, color="#0000FF", stroke_width=6).scale(1.23)
        self.play(ReplacementTransform(rect, rect1))
        self.wait(1)
        self.play(profit.animate.become(Text("profit = 210").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait(2)

        self.play(Transform(rect1, SurroundingRectangle(w, color="#0000FF", stroke_width=6).scale(1.23)))
        self.wait()
        self.play(w.animate.become(Text("W = 30").set_color(BLACK).move_to(w)), run_time=0.5)
        self.wait()

        circle = Circle(radius=0.4, stroke_color="#0000FF", stroke_width=6).move_to(b1)
        self.play(Transform(rect1, circle))
        self.wait()
        self.play(Transform(rect1, Circle(radius=0.4, stroke_color="#0000FF", stroke_width=6).move_to(b)))
        self.wait(2)


        rect = SurroundingRectangle(profit, color="#0000FF", stroke_width=6).scale(1.23)
        self.play(ReplacementTransform(rect1, rect))
        self.wait(1)
        self.play(profit.animate.become(Text("profit = 310").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(w, color="#0000FF", stroke_width=6).scale(1.23)))
        self.wait()
        self.play(w.animate.become(Text("W = 5").set_color(BLACK).move_to(w)), run_time=0.5)
        self.wait(1)

        circle = Circle(radius=0.4, stroke_color="#0000FF", stroke_width=6).move_to(c1)
        self.play(Transform(rect, circle))
        self.wait()
        self.play(Transform(rect, Circle(radius=0.4, stroke_color="#0000FF", stroke_width=6).move_to(c)))
        self.wait(2)

        temp = Text("3 * 5").set_color(BLACK).next_to(w, DOWN, buff=1.5)
        self.play(TransformFromCopy(c, temp[0]))
        self.play(FadeIn(temp[1]), TransformFromCopy(w[-1], temp[-1]))
        self.wait(1)
        self.play(temp.animate.become(Text("15").set_color(BLACK).move_to(temp)), run_time=0.5)
        self.wait(1)

        rect1 = SurroundingRectangle(profit, color="#0000FF", stroke_width=6).scale(1.23)
        self.play(ReplacementTransform(rect, rect1))
        self.wait(1)
        self.play(profit.animate.become(Text("profit = 325").set_color(BLACK).move_to(profit)), FadeOut(temp),run_time=0.5)
        self.wait(2)

        self.play(Transform(rect1, SurroundingRectangle(w, color="#0000FF", stroke_width=6).scale(1.23)))
        self.wait()
        self.play(w.animate.become(Text("W = 0").set_color(BLACK).move_to(w)), run_time=0.5)
        self.wait(3)

        rect = SurroundingRectangle(profit, color="#00FF00", stroke_width=9).scale(1.23)
        self.play(ReplacementTransform(rect1, rect))


        self.wait(2)





        



        self.embed()






class Array(VGroup):
    def __init__(self, array_size=5, **kwargs):
        super().__init__(**kwargs)
        self.array_size = array_size
        self.square_contents = [None] * array_size
        self.array_group = self.create_array()
        self.add(self.array_group)

    def create_element(self, text):
        square = Square(side_length=1.3, fill_opacity=1, fill_color=BLACK, color=BLACK).set_color(BLACK)
        text = Text(text, font_size=44, color=BLACK).set_color(BLACK)
        return VGroup(square, text)

    def create_array(self):
        squares = VGroup(*[Square(side_length=1.3, color=PURE_RED, stroke_width=6).set_color(BLACK) for _ in range(self.array_size)])
        squares.arrange(RIGHT, buff=0)

        return VGroup(squares)

    def update_element(self, scene, index, new_value):
        if 0 <= index < self.array_size:
            new_square = Square(side_length=1.3, fill_opacity=1, fill_color=YELLOW_C, color=DARK_BLUE)
            new_number = Text(str(new_value), color=BLACK)
            new_square.add(new_number)
            new_square.move_to(self.array_group[0][index].get_center())
            if self.square_contents[index] is None:
                scene.play(FadeIn(new_square))
            else:
                scene.play(Transform(self.square_contents[index], new_square))
            self.square_contents[index] = new_square
        else:
            scene.play(Indicate(self.array_group, color=RED))
            print(f"Index {index} is out of bounds")

    def append_element(self, scene, value, color=YELLOW):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.3, fill_opacity=1, fill_color=color, color=BLACK,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1).set_color(BLACK)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def append_element1(self, scene, value, color=YELLOW):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.3, fill_opacity=1, fill_color=color, color=BLACK,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1).set_color(BLACK).scale(0.85)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))


    def add_element(self, scene, value, color=YELLOW):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.3, fill_opacity=1, fill_color=color, color=BLACK,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK, font_size=50).set_z_index(1).set_color(BLACK)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                scene.play(FadeIn(new_square1))
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def pop_element(self, scene):
        for i in range(self.array_size - 1, -1, -1):
            if self.square_contents[i] is not None:
                scene.play(FadeOut(self.square_contents[i]))
                self.square_contents[i] = None
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def delete_from_front(self, scene):
        if self.square_contents[0] is not None:
            scene.play(FadeOut(self.square_contents[0]))
            self.square_contents[0] = None
            animations = []
            for i in range(1, self.array_size):
                if self.square_contents[i] is not None:
                    animations.append(
                        self.square_contents[i].animate.move_to(self.array_group[0][i - 1].get_center())
                    )
                    self.square_contents[i - 1] = self.square_contents[i]
                    self.square_contents[i] = None
            if animations:
                scene.play(*animations)
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def create_new_array(self, scene, new_size):
        new_array = Array(array_size=new_size)
        new_array.next_to(self, DOWN, buff=0.7)
        scene.play(ShowCreation(new_array))
        return new_array

    def transfer_elements_to_new_array(self, scene, new_array):
        for i, content in enumerate(self.square_contents):
            if content is not None:
                scene.play(Transform(content, new_array.array_group[0][i]))
                new_array.square_contents[i] = content
                self.square_contents[i] = None       
