from manimlib import *

PURE_RED = "#FF0000"
PURE_BLUE = "#0000FF"
PURE_GREEN = "#00FF00"


class Candy(Scene):

    def construct(self):
        
        boy = ImageMobject("bob.png").scale(0.64).shift(DOWN*1.95)
        a = boy.copy().next_to(boy, LEFT, buff=1)
        b = boy.copy().next_to(a, LEFT, buff=1)
        c = boy.copy().next_to(boy, RIGHT, buff=1)
        d = boy.copy().next_to(c, RIGHT, buff=1)
         
        self.play(GrowFromCenter(boy), GrowFromCenter(a), GrowFromCenter(b), GrowFromCenter(c), GrowFromCenter(d))
 
        self.wait(2)


        a1 = Text("1").set_color(BLACK).next_to(b, UP,buff=0.25)
        a2 = Text("2").set_color(BLACK).next_to(a, UP,buff=0.25)
        a3 = Text("4").set_color(BLACK).next_to(boy, UP,buff=0.25)
        a4 = Text("2").set_color(BLACK).next_to(c, UP,buff=0.25)
        a5 = Text("1").set_color(BLACK).next_to(d, UP,buff=0.25)

        self.play(FadeIn(VGroup(a1,a2,a3,a4,a5)))
        self.wait(2)

        candy = ImageMobject("candy.png").next_to(a3, UP).scale(0.42).shift(UP*0.6)
        self.play(GrowFromCenter(candy))
        self.wait(2)


        b1 = candy.copy().next_to(a1, UP).scale(0.8)
        b2 = candy.copy().next_to(a2, UP).scale(0.8)
        b3 = candy.copy().next_to(a3, UP).scale(0.8)
        b4 = candy.copy().next_to(a4, UP).scale(0.8)
        b5 = candy.copy().next_to(a5, UP).scale(0.8)


        self.play(TransformFromCopy(candy, b1),
                  TransformFromCopy(candy, b2),
                  TransformFromCopy(candy, b3),
                  TransformFromCopy(candy, b4),
                  TransformFromCopy(candy, b5),
                  self.camera.frame.animate.shift(UP*0.5))
        self.play(candy.animate.shift(UP*0.5))

        self.wait(2)

        circle = Circle(stroke_width=8).set_color("#0000FF").move_to(a1).scale(0.5)
        self.wait(2)

        circle.move_to(a2)
        self.play(ShowCreation(circle))
        self.wait(2)
        prev = circle.copy().set_color("#FF0000").move_to(a1)
        self.play(ShowCreation(prev))




        c2 = candy.copy().next_to(b2, UP, buff=0).scale(0.8).shift(DOWN*0.55)
        self.play(TransformFromCopy(candy, c2))
        self.wait(2)

        self.play(circle.animate.move_to(a3), prev.animate.move_to(a2))
        self.wait(2)
        self.play(candy.animate.shift(LEFT*6))
        c3 = candy.copy().next_to(b3, UP, buff=0).scale(0.8).shift(DOWN*0.55)
        c32 = candy.copy().next_to(c3, UP, buff=0).scale(0.8).shift(DOWN*0.55)
        self.play(TransformFromCopy(candy, c3))
        self.play(TransformFromCopy(candy, c32))
        self.wait()

        self.wait(2)

        self.play(circle.animate.move_to(a4), prev.animate.move_to(a3))

        self.wait(2)

        self.play(circle.animate.move_to(a5), prev.animate.move_to(a4))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*14))

        text = Text("Max(candies[i], candies[i + 1] + 1)").set_color(BLACK).shift(RIGHT*14+UP*0.6).scale(0.9)
        text[:3].set_color(PURE_RED)
        self.play(Write(text))
        self.wait(2)

        brace = Brace(text[4:14], DOWN, stroke_width=2).set_color(BLACK).shift(DOWN*0.1)
        self.play(GrowFromCenter(brace))
        self.wait(2)
        self.play(Transform(brace, Brace(text[15:27], DOWN, stroke_width=2).set_color(BLACK).shift(DOWN*0.1) ))
        self.wait(2)
        self.play(self.camera.frame.animate.shift(LEFT*14))


        self.play(circle.animate.move_to(a4), prev.animate.move_to(a5))
        self.wait(2)
        c4 = candy.copy().next_to(b4, UP, buff=0).scale(0.8).shift(DOWN*0.55)
        self.play(TransformFromCopy(candy, c4))
        self.wait(2)

        self.play(circle.animate.move_to(a3), prev.animate.move_to(a4))
        self.wait(2)



        self.play(circle.animate.move_to(a2), prev.animate.move_to(a3))
        self.wait(2)
        self.play(circle.animate.move_to(a1), prev.animate.move_to(a2))
        self.wait(2)
        self.play(Uncreate(circle), FadeOut(candy), FadeOut(prev))

        self.wait(2)



        nine = ImageMobject("nine.png").move_to(c3).scale(0.6)

        self.play(ReplacementTransform(b1, nine),
                  ReplacementTransform(b2, nine),
                  ReplacementTransform(b3, nine),
                  ReplacementTransform(b4, nine),
                  ReplacementTransform(b5, nine),
                  ReplacementTransform(c2, nine),
                  ReplacementTransform(c3, nine),
                  ReplacementTransform(c4, nine),
                  ReplacementTransform(c32, nine))
        
        self.wait(2)
                  


        self.embed()







class Candy_more_efficient(Scene):

    def construct(self):

        self.camera.frame.scale(0.93).shift(UP*1.65).scale(1.07)

        
        # Example usage:
        array = Array(array_size=7).scale(1.3)

        array.append_element(self, "1")
        array.append_element(self, "2")
        array.append_element(self, "3")
        array.append_element(self, "3")
        array.append_element(self, "1")
        array.append_element(self, "2")
        array.append_element(self, "1")

        for i in range(7):
            array.square_contents[i].scale(1.3)




        self.wait(2)

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(7)])
        self.wait(2)

        BLUE_E = MAROON

        last = 0.06

        # Create bars
        bar_a = Rectangle(
            height=1*0.7, width=0.6, fill_color=BLUE_E, fill_opacity=0.99
        ).next_to(array.array_group[0][0], UP, buff=last)
        
        bar_b = Rectangle(
            height=2*0.7, width=0.6, fill_color=BLUE_E, fill_opacity=0.99
        ).next_to(array.array_group[0][1], UP, buff=last)
        
        bar_c = Rectangle(
            height=3*0.7, width=0.6, fill_color=BLUE_E, fill_opacity=0.99
        ).next_to(array.array_group[0][2], UP, buff=last)
        
        bar_d = Rectangle(
            height=3*0.7, width=0.6, fill_color=BLUE_E, fill_opacity=0.99
        ).next_to(array.array_group[0][3], UP, buff=last)
        
        bar_e = Rectangle(
            height=1*0.7, width=0.6, fill_color=BLUE_E, fill_opacity=0.99
        ).next_to(array.array_group[0][4], UP, buff=last)
        

        bar_f = Rectangle(
            height=2*0.7, width=0.6, fill_color=BLUE_E, fill_opacity=0.99
        ).next_to(array.array_group[0][5], UP, buff=last)
        
        bar_g = Rectangle(
            height=1*0.7, width=0.6, fill_color=BLUE_E, fill_opacity=0.99
        ).next_to(array.array_group[0][6], UP, buff=last)
        
        # Animate bars growing from DOWN to UP
        self.play(
    GrowFromEdge(bar_a, DOWN),
    GrowFromEdge(bar_b, DOWN),
    GrowFromEdge(bar_c, DOWN),
    GrowFromEdge(bar_d, DOWN),
    GrowFromEdge(bar_e, DOWN),
    GrowFromEdge(bar_g, DOWN),
    GrowFromEdge(bar_f, DOWN),
    run_time=2
)
        self.wait(2)

        candy = Text("candy = 7").set_color(BLACK).to_edge(UP).shift(UP*1.65).shift(LEFT*0.2)
        peak = Text("peak = 0").set_color(BLACK).next_to(candy, LEFT, buff=1)
        valley = Text("valley = 0").set_color(BLACK).next_to(candy, RIGHT, buff=1)
        self.play(Write(candy))
        self.wait(2)

        i = Text("i").set_color(BLACK).next_to(array.square_contents[1], DOWN, buff=0.5).scale(1.5)
        self.play(GrowFromCenter(i))
        self.wait(2)

        self.play(array.square_contents[1][0].animate.set_fill(BLUE))
        self.play(array.square_contents[0][0].animate.set_fill(GREEN))

        self.wait(2)

        line = Line(start=bar_a.get_top(), end=bar_b.get_top(), stroke_width=10).set_color(GREY_D).shift(UP*0.3).scale(1.12)
        self.play(GrowFromCenter(line))

        self.play(FadeIn(peak))
        self.wait()
        rect = SurroundingRectangle(peak, color=PURE_BLUE, stroke_width=6).scale(1.12)
        self.play(ShowCreation(rect))
        self.play(Transform(peak, Text("peak = 1").set_color(BLACK).move_to(peak)))
        self.wait(1)
        self.play(Transform(rect, SurroundingRectangle(candy, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.wait(2)

        self.play(Transform(candy,Text("candy = 8").set_color(BLACK).move_to(candy) ))

        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[2], DOWN, buff=0.5))

        self.play(array.square_contents[2][0].animate.set_fill(BLUE)
        ,array.square_contents[1][0].animate.set_fill(GREEN)
        ,array.square_contents[0][0].animate.set_fill(YELLOW))

        self.wait()

        self.play(line.animate.shift(RIGHT*1.3+UP*0.7))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(peak, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.play(Transform(peak, Text("peak = 2").set_color(BLACK).move_to(peak)))
        self.wait(1.5)
        self.play(Transform(rect, SurroundingRectangle(candy, color=PURE_BLUE, stroke_width=6).scale(1.2)))
        self.wait()
        self.play(Transform(candy,Text("candy = 10").set_color(BLACK).move_to(candy) ))
        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[3], DOWN, buff=0.5))

        self.play(array.square_contents[3][0].animate.set_fill(BLUE)
        ,array.square_contents[2][0].animate.set_fill(GREEN)
        ,array.square_contents[1][0].animate.set_fill(YELLOW))

        self.wait()

        self.play(Transform(line, Line(start=bar_c.get_top(), end=bar_d.get_top(), stroke_width=10).set_color(GREY_D).shift(UP*0.3).scale(1.12)))

        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[4], DOWN, buff=0.5))

        self.play(array.square_contents[4][0].animate.set_fill(BLUE)
        ,array.square_contents[3][0].animate.set_fill(GREEN)
        ,array.square_contents[2][0].animate.set_fill(YELLOW))

        self.play(Transform(line, Line(start=bar_d.get_corner(UR), end=bar_e.get_top(), stroke_width=10).set_color(GREY_D).shift(UP*0.3).scale(1.12)))

        self.wait()

        self.play(FadeIn(valley))
        self.wait()

        self.play(Transform(rect, SurroundingRectangle(valley, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.wait(1)
        self.play(Transform(valley, Text("valley = 1").set_color(BLACK).move_to(valley)))
        self.wait()

        self.play(Transform(rect, SurroundingRectangle(candy, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.wait()
        self.play(Transform(candy,Text("candy = 11").set_color(BLACK).move_to(candy) ))
        self.wait()

        self.play(i.animate.next_to(array.square_contents[5], DOWN, buff=0.5))

        self.play(array.square_contents[5][0].animate.set_fill(BLUE)
        ,array.square_contents[4][0].animate.set_fill(GREEN)
        ,array.square_contents[3][0].animate.set_fill(YELLOW))

        self.play(Transform(line, Line(start=bar_e.get_top(), end=bar_f.get_top(), stroke_width=10).set_color(GREY_D).shift(UP*0.3).scale(1.12)))

        self.wait(2)

        self.play(Transform(candy,Text("candy = 10").set_color(BLACK).move_to(candy) ))

        self.wait(1)

        self.play(Transform(peak, Text("peak = 0").set_color(BLACK).move_to(peak)),
                 Transform(valley, Text("valley = 0").set_color(BLACK).move_to(valley)))
        
        self.wait(2)



        self.play(Transform(rect, SurroundingRectangle(peak, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.play(Transform(peak, Text("peak = 1").set_color(BLACK).move_to(peak)))
        self.wait(1)
        self.play(Transform(rect, SurroundingRectangle(candy, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.wait()

        self.play(Transform(candy,Text("candy = 11").set_color(BLACK).move_to(candy) ))

        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[6], DOWN, buff=0.5))

        self.play(array.square_contents[6][0].animate.set_fill(BLUE)
        ,array.square_contents[5][0].animate.set_fill(GREEN)
        ,array.square_contents[4][0].animate.set_fill(YELLOW))

        self.play(Transform(line, Line(start=bar_f.get_corner(UR), end=bar_g.get_top(), stroke_width=10).set_color(GREY_D).shift(UP*0.3).scale(1.12)))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(valley, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.wait(1)
        self.play(Transform(valley, Text("valley = 1").set_color(BLACK).move_to(valley)))
        self.wait()

        self.play(Transform(rect, SurroundingRectangle(candy, color=PURE_BLUE, stroke_width=6).scale(1.12)))
        self.wait()
        self.play(Transform(candy,Text("candy = 12").set_color(BLACK).move_to(candy) ))
        self.wait()

        self.wait(1)

        self.play(i.animate.shift(RIGHT*1.4))

        self.wait()

        self.play(FadeOut(VGroup(line, i, rect, peak, valley)))
        self.play(candy.animate.scale(2),
                  self.camera.frame.animate.shift(UP*0.8))
        
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
        square = Square(side_length=1.22, fill_opacity=1, fill_color=BLACK, color=BLACK).set_color(BLACK)
        text = Text(text, font_size=44, color=BLACK).scale(0.8).set_color(BLACK)
        return VGroup(square, text)

    def create_array(self):
        squares = VGroup(*[Square(side_length=1.22, color=PURE_RED, stroke_width=6).set_color(BLACK) for _ in range(self.array_size)])
        squares.arrange(RIGHT, buff=0)

        return VGroup(squares)

    def update_element(self, scene, index, new_value):
        if 0 <= index < self.array_size:
            new_square = Square(side_length=1.12, fill_opacity=1, fill_color=YELLOW_C, color=DARK_BLUE)
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

    def append_element(self, scene, value):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.22, fill_opacity=1, fill_color=YELLOW, color=BLACK,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1).set_color(BLACK)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def add_element(self, scene, value, color=YELLOW):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.22, fill_opacity=1, fill_color=color, color=BLACK,
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
