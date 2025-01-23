from manimlib import *
PURE_RED = "#FF0000"
PURE_BLUE = "#00FF00"
PURE_GREEN = "#0000FF"

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



class GasExample(Scene):

    def construct(self):

        self.camera.frame.scale(0.93).shift(UP*0.83)

        
        # Example usage:
        array = Array(array_size=5).shift(UP)
        array1 = Array(array_size=5).next_to(array, DOWN, buff=1.2)

        array.append_element(self, "1")
        array.append_element(self, "2")
        array.append_element(self, "3")
        array.append_element(self, "4")
        array.append_element(self, "5")

        array1.append_element(self, "3")
        array1.append_element(self, "4")
        array1.append_element(self, "5")
        array1.append_element(self, "1")
        array1.append_element(self, "2")


        for i in range(5):
            array1.square_contents[i][0].set_fill(BLUE)



        self.wait(2)

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(5)],
                  ShowCreation(array1), *[ShowCreation(array1.square_contents[i]) for i in range(5)])
        
        self.wait(2)

        gas_sum = Text("1 + 2 + 3 + 4 + 5", font_size=44).next_to(array, UP, buff=1.2).set_color(BLACK)
        
        self.play(TransformFromCopy(array.square_contents[0][1], gas_sum[0]),
                  TransformFromCopy(array.square_contents[1][1], gas_sum[2]),
                  TransformFromCopy(array.square_contents[2][1], gas_sum[4]),
                  TransformFromCopy(array.square_contents[3][1], gas_sum[6]),
                  TransformFromCopy(array.square_contents[4][1], gas_sum[8]))
        
        self.play(FadeIn(gas_sum[1]), FadeIn(gas_sum[3]), FadeIn(gas_sum[5]), FadeIn(gas_sum[7]))
        self.wait(2)

        self.play(Transform(gas_sum, Text("15", font_size=44).move_to(gas_sum).set_color(BLACK).scale(1.2)))
        self.play(gas_sum.animate.shift(LEFT*4))

        self.wait(2)

        cost_sum = Text("3 + 4 + 5 + 1 + 2", font_size=44).next_to(array, UP, buff=1.2).set_color(BLACK).shift(RIGHT)
        
        self.play(TransformFromCopy(array1.square_contents[0][1], cost_sum[0]),
                  TransformFromCopy(array1.square_contents[1][1], cost_sum[2]),
                  TransformFromCopy(array1.square_contents[2][1], cost_sum[4]),
                  TransformFromCopy(array1.square_contents[3][1], cost_sum[6]),
                  TransformFromCopy(array1.square_contents[4][1], cost_sum[8]))
        
        self.play(FadeIn(cost_sum[1]), FadeIn(cost_sum[3]), FadeIn(cost_sum[5]), FadeIn(cost_sum[7]))
        self.wait(2)

        self.play(Transform(cost_sum, Text("15", font_size=44).move_to(cost_sum).set_color(BLACK).scale(1.2)))

        self.wait()

        self.play(gas_sum.animate.shift(RIGHT*2.7))

        self.wait(2)

        geq = Text(">=", font_size=44).next_to(gas_sum, RIGHT, buff=0.5).set_color(BLACK).scale(1.2)
        self.play(Write(geq))

        self.wait(2)

        self.play(FadeOut(gas_sum), FadeOut(cost_sum), FadeOut(geq))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*1.7))

        tank = Text("Tank = 0").set_color(BLACK).next_to(array, RIGHT, buff=0.2).shift(UP*0.58+RIGHT)
        index = Text("Index = 0").set_color(BLACK).next_to(tank, DOWN, buff=0.64)
        self.play(Write(tank))
        self.play(Write(index))

        self.wait(2)

        i = Text("i").set_color(BLACK).next_to(array.square_contents[0], DOWN, buff=0.34).set_color(BLACK)
        self.play(Write(i))

        self.wait(2)

        temp = Text("1 - 3", font_size=44).next_to(array, UP, buff=1.2).set_color(BLACK).scale(1.3)
        self.play(TransformFromCopy(array.square_contents[0][1], temp[0]),
                    TransformFromCopy(array1.square_contents[0][1], temp[2]), 
                    FadeIn(temp[1]))

        self.wait(2)

        self.play(Transform(temp, Text("-2", font_size=44).move_to(temp).set_color(BLACK).scale(1.3)))  

        self.wait(2)

        rect = Circle(stroke_width=10).set_color("#0000FF").scale(0.5).move_to(tank[-1])
        self.play(ShowCreation(rect))

        self.play(Transform(tank[-1], Text("-2",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(Transform(tank[-1], Text("0",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(rect.animate.move_to(index[-1]))
        self.wait(2)
        self.play(Transform(index[-1], Text("1",).move_to(index[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(FadeOut(rect), FadeOut(temp))
        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[1], DOWN, buff=0.34))

        self.wait(2)

        temp = Text("2 - 4", font_size=44).next_to(array, UP, buff=1.2).set_color(BLACK).scale(1.3)
        self.play(TransformFromCopy(array.square_contents[1][1], temp[0]),
                    TransformFromCopy(array1.square_contents[1][1], temp[2]), 
                    FadeIn(temp[1]))

        self.wait(2)

        self.play(Transform(temp, Text("-2", font_size=44).move_to(temp).set_color(BLACK).scale(1.3)))  

        self.wait(2)

        rect = Circle(stroke_width=10).set_color("#0000FF").scale(0.5).move_to(tank[-1])
        self.play(ShowCreation(rect))

        self.play(Transform(tank[-1], Text("-2",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(Transform(tank[-1], Text("0",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(rect.animate.move_to(index[-1]))
        self.wait(2)
        self.play(Transform(index[-1], Text("2",).move_to(index[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(FadeOut(rect), FadeOut(temp))
        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[2], DOWN, buff=0.34))
        self.wait()


        temp = Text("3 - 5", font_size=44).next_to(array, UP, buff=1.2).set_color(BLACK).scale(1.3)
        self.play(TransformFromCopy(array.square_contents[2][1], temp[0]),
                    TransformFromCopy(array1.square_contents[2][1], temp[2]), 
                    FadeIn(temp[1]))

        self.wait(2)

        self.play(Transform(temp, Text("-2", font_size=44).move_to(temp).set_color(BLACK).scale(1.3)))  

        self.wait(2)

        rect = Circle(stroke_width=10).set_color("#0000FF").scale(0.5).move_to(tank[-1])
        self.play(ShowCreation(rect))

        self.play(Transform(tank[-1], Text("-2",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(Transform(tank[-1], Text("0",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(rect.animate.move_to(index[-1]))
        self.wait(2)
        self.play(Transform(index[-1], Text("3",).move_to(index[-1]).set_color(BLACK)))
        self.wait(2)
        self.play(FadeOut(rect), FadeOut(temp))
        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[3], DOWN, buff=0.34))

        self.wait(2)

        temp = Text("4 - 1", font_size=44).next_to(array, UP, buff=1.2).set_color(BLACK).scale(1.3)
        self.play(TransformFromCopy(array.square_contents[3][1], temp[0]),
                    TransformFromCopy(array1.square_contents[3][1], temp[2]), 
                    FadeIn(temp[1]))

        self.wait(2)

        self.play(Transform(temp, Text("3", font_size=44).move_to(temp).set_color(BLACK).scale(1.3)))  

        self.wait(2)

        rect = Circle(stroke_width=10).set_color("#0000FF").scale(0.5).move_to(tank[-1])
        self.play(ShowCreation(rect))

        self.play(Transform(tank[-1], Text("3",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)

        self.play(FadeOut(rect), FadeOut(temp))
        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[4], DOWN, buff=0.34))

        self.wait()

        temp = Text("5 - 2", font_size=44).next_to(array, UP, buff=1.2).set_color(BLACK).scale(1.3)
        self.play(TransformFromCopy(array.square_contents[4][1], temp[0]),
                    TransformFromCopy(array1.square_contents[4][1], temp[2]), 
                    FadeIn(temp[1]))

        self.wait(2)

        self.play(Transform(temp, Text("3", font_size=44).move_to(temp).set_color(BLACK).scale(1.3)))  

        self.wait(2)

        rect = Circle(stroke_width=10).set_color("#0000FF").scale(0.5).move_to(tank[-1])
        self.play(ShowCreation(rect))

        self.play(Transform(tank[-1], Text("6",).move_to(tank[-1]).set_color(BLACK)))
        self.wait(2)

        self.play(FadeOut(rect), FadeOut(temp))
        self.wait(2)

        self.play(Uncreate(i), Uncreate(tank),
                  index.animate.next_to(array, UP, buff=1.2).scale(1.5),
                  self.camera.frame.animate.shift(LEFT*1.7))
        
        self.wait()
        self.play(array.square_contents[3][0].animate.set_fill(RED),
                  array1.square_contents[3][0].animate.set_fill(RED),)
        
        self.wait(2)

        self.embed()





class Gas(Scene):

    def construct(self):
        
        a = ImageMobject("gas.png").scale(0.6).shift(LEFT*5.51)
        b,c,d,e = a.copy(), a.copy(), a.copy(), a.copy()

        b.next_to(a, RIGHT, buff=0.5)
        c.next_to(b, RIGHT, buff=0.5)
        d.next_to(c, RIGHT, buff=0.5)   
        e.next_to(d, RIGHT, buff=0.5)   
 

        self.play(GrowFromCenter(a), GrowFromCenter(b), 
                  GrowFromCenter(c), GrowFromCenter(d),
                  GrowFromCenter(e))
        
        self.wait()
        GREY_E = GREY_D
        arrow = Arrow(a.get_right()+LEFT*0.6, b.get_left()+RIGHT*0.6, stroke_width=6).set_color(GREY_E).shift(DOWN*0.4+RIGHT*0.1)
        arrow1 = Arrow(b.get_right()+LEFT*0.6, c.get_left()+RIGHT*0.6, stroke_width=6).set_color(GREY_E).shift(DOWN*0.4+RIGHT*0.1)
        arrow2 = Arrow(c.get_right()+LEFT*0.6, d.get_left()+RIGHT*0.6, stroke_width=6).set_color(GREY_E).shift(DOWN*0.4+RIGHT*0.1)
        arrow3 = Arrow(d.get_right()+LEFT*0.6, e.get_left()+RIGHT*0.6, stroke_width=6).set_color(GREY_E).shift(DOWN*0.4+RIGHT*0.1)

        gas_a = Text("4", font_size=44).next_to(a, UP, buff=0).set_color(BLACK)
        gas_b = Text("1", font_size=44).next_to(b, UP, buff=0).set_color(BLACK)
        gas_c = Text("2", font_size=44).next_to(c, UP, buff=0).set_color(BLACK)
        gas_d = Text("3", font_size=44).next_to(d, UP, buff=0).set_color(BLACK)
        gas_e = Text("5", font_size=44).next_to(e, UP, buff=0).set_color(BLACK)




        line = Line(e.get_bottom(), e.get_bottom() + DOWN*1.9, stroke_width=9).set_color(GREY_E)
        line1 = Arrow(a.get_bottom() + DOWN*2.36 + LEFT*0.1, a.get_bottom() + LEFT*0.1, stroke_width=5).set_color(GREY_E).shift(UP*0.2)
        line2 = Line(line.get_bottom(), line1.get_bottom(), stroke_width=9).set_color(GREY_E)
        line.shift(LEFT*0.03)
        line1.shift(RIGHT*0.026)

        self.play(ShowCreation(arrow), ShowCreation(arrow1), ShowCreation(arrow2), ShowCreation(arrow3)) 
        self.play(ShowCreation(line))
        self.play(ShowCreation(line2))
        self.play(ShowCreation(line1)) 

        self.wait(2)

        GREEN_E = BLACK

        cost_a = Text("2", font_size=44).next_to(arrow, UP, buff=0.18).set_color(GREEN_E).scale(0.9)
        cost_b = Text("3", font_size=44).next_to(arrow1, UP, buff=0.18).set_color(GREEN_E).scale(0.9)
        cost_c = Text("5", font_size=44).next_to(arrow2, UP, buff=0.18).set_color(GREEN_E).scale(0.9)
        cost_d = Text("1", font_size=44).next_to(arrow3, UP, buff=0.18).set_color(GREEN_E).scale(0.9)
        cost_e = Text("2", font_size=44).next_to(line2, DOWN, buff=0.18).set_color(GREEN_E).scale(0.9)

        self.wait(2)
        self.play(Write(gas_a), Write(gas_b), Write(gas_c), Write(gas_d), Write(gas_e))

        self.wait(2)

        self.play(Write(cost_a), Write(cost_b), Write(cost_c), Write(cost_d), Write(cost_e))

        self.wait(2)

        self.play(Indicate(a, color="#FF0000"))
        self.play(Indicate(b, color="#FF0000"))
        self.play(Indicate(c, color="#FF0000"))
        self.play(Indicate(d, color="#FF0000"))
        self.play(Indicate(e, color="#FF0000"))

        self.wait(2)

        car = ImageMobject("car.png").scale(0.32).next_to(gas_a, UP, buff=0).shift(UP*0.09)

        gas_sum = Text("4 + 1 + 2 + 3 + 5", font_size=44).next_to(gas_c, UP, buff=1.2).set_color(BLACK)
        
        self.play(TransformFromCopy(gas_a, gas_sum[0]),
                  TransformFromCopy(gas_b, gas_sum[2]),
                  TransformFromCopy(gas_c, gas_sum[4]),
                  TransformFromCopy(gas_d, gas_sum[6]),
                  TransformFromCopy(gas_e, gas_sum[8]))
        
        self.play(FadeIn(gas_sum[1]), FadeIn(gas_sum[3]), FadeIn(gas_sum[5]), FadeIn(gas_sum[7]))
        self.wait(2)

        self.play(Transform(gas_sum, Text("15", font_size=44).move_to(gas_sum).set_color(BLACK).scale(1.2)))
        self.play(gas_sum.animate.shift(LEFT*4))

        self.wait(2)

        cost_sum = Text("2 + 3 + 5 + 1 + 2", font_size=44).next_to(gas_c, UP, buff=1.2).set_color(BLACK).shift(RIGHT)
        
        self.play(TransformFromCopy(cost_a, cost_sum[0]),
                  TransformFromCopy(cost_b, cost_sum[2]),
                  TransformFromCopy(cost_c, cost_sum[4]),
                  TransformFromCopy(cost_d, cost_sum[6]),
                  TransformFromCopy(cost_e, cost_sum[8]))
        
        self.play(FadeIn(cost_sum[1]), FadeIn(cost_sum[3]), FadeIn(cost_sum[5]), FadeIn(cost_sum[7]))
        self.wait(2)

        self.play(Transform(cost_sum, Text("13", font_size=44).move_to(cost_sum).set_color(BLACK).scale(1.2)))

        self.wait()

        self.play(gas_sum.animate.shift(RIGHT*2.7))

        self.wait(2)

        geq = Text(">=", font_size=44).next_to(gas_sum, RIGHT, buff=0.5).set_color(BLACK).scale(1.2)
        self.play(Write(geq))

        self.wait(2)

        self.play(FadeOut(gas_sum), FadeOut(cost_sum), FadeOut(geq))

        self.wait(2)

        self.play(FadeIn(car))
        self.wait(2)

        total = Text("4").set_color(BLACK).next_to(car, UP, buff=0.2)
        self.play(TransformFromCopy(gas_a, total))

        car = Group(car, total)


        self.wait()

        rect = Circle(stroke_width=6.7).set_color("#0000FF").scale(0.399).move_to(cost_a)
        self.play(ShowCreation(rect))

        self.wait()

        self.play(car.animate.next_to(gas_b, UP, buff=0).shift(UP*0.09),
                  )
        
        self.play(Transform(total, Text("2").move_to(total).set_color(BLACK)))

        self.wait()

        self.play(rect.animate.move_to(gas_b))
        self.wait(1)
        self.play(Transform(total, Text("3").move_to(total).set_color(BLACK)))
        self.wait(2)

        self.play(rect.animate.move_to(cost_b))
        self.wait(1)
        self.play(car.animate.next_to(gas_c, UP, buff=0).shift(UP*0.09),
                  )
        
        self.play(Transform(total, Text("0").move_to(total).set_color(BLACK)))

        self.wait()
    
        self.play(rect.animate.move_to(gas_c))
        self.wait(1)
        self.play(Transform(total, Text("2").move_to(total).set_color(BLACK)))
        self.wait(1)
        self.play(rect.animate.move_to(cost_c))
        self.wait(2)

        self.play(FadeOut(rect), FadeOut(total), FadeOut(car))


        car = ImageMobject("car.png").scale(0.32).next_to(gas_a, UP, buff=0).shift(UP*0.09)
        car.next_to(gas_b, UP, buff=0).shift(UP*0.09)
        self.play(FadeIn(car))
        self.wait(2)

        total = Text("1").set_color(BLACK).next_to(car, UP, buff=0.2)
        self.play(TransformFromCopy(gas_b, total))

        car = Group(car, total)

        rect.move_to(cost_b)
        self.play(ShowCreation(rect))
        self.wait(2)


        self.play(FadeOut(rect), FadeOut(total), FadeOut(car))
        self.wait(2)

        car = ImageMobject("car.png").scale(0.32).next_to(gas_a, UP, buff=0).shift(UP*0.09)
        car.next_to(gas_c, UP, buff=0).shift(UP*0.09)
        self.play(FadeIn(car))
        self.wait(2)

        total = Text("2").set_color(BLACK).next_to(car, UP, buff=0.2)
        self.play(TransformFromCopy(gas_c, total))

        rect.move_to(cost_c)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(FadeOut(rect), FadeOut(total), FadeOut(car))
        self.wait(2)

        car = ImageMobject("car.png").scale(0.32).next_to(gas_a, UP, buff=0).shift(UP*0.09)
        car.next_to(gas_d, UP, buff=0).shift(UP*0.09)
        self.play(FadeIn(car))
        self.wait(2)

        total = Text("3").set_color(BLACK).next_to(car, UP, buff=0.2)
        self.play(TransformFromCopy(gas_d, total))

        car = Group(car, total)

        rect.move_to(cost_d)
        self.play(ShowCreation(rect))
        self.wait(2)
        self.play(car.animate.next_to(gas_e, UP, buff=0).shift(UP*0.09),
                  )
        
        self.play(Transform(total, Text("2").move_to(total).set_color(BLACK)))
        self.wait(1)

        self.play(rect.animate.move_to(gas_e)) 
        self.wait(1)
        self.play(Transform(total, Text("7").move_to(total).set_color(BLACK)))
        self.wait(1)
        self.play(rect.animate.move_to(cost_e))
        self.wait(1)
        self.play(car.animate.next_to(gas_a, UP, buff=0).shift(UP*0.09),
                  )
        
        self.play(Transform(total, Text("5").move_to(total).set_color(BLACK)))
        self.wait(1)

        self.play(rect.animate.move_to(gas_a))
        self.wait()
        self.play(Transform(total, Text("9").move_to(total).set_color(BLACK)))
        self.wait(1)
        self.play(rect.animate.move_to(cost_a))

        self.play(car.animate.next_to(gas_b, UP, buff=0).shift(UP*0.09),
                  )
        
        self.play(Transform(total, Text("7").move_to(total).set_color(BLACK)))
        self.wait(1)
        self.play(rect.animate.move_to(gas_b))
        self.wait()
        self.play(Transform(total, Text("8").move_to(total).set_color(BLACK)))
        self.wait()
        self.play(rect.animate.move_to(cost_b))
        self.wait()

        self.play(car.animate.next_to(gas_c, UP, buff=0).shift(UP*0.09),
                  )
        
        self.play(Transform(total, Text("5").move_to(total).set_color(BLACK)))
        self.wait(1)

        self.play(rect.animate.move_to(gas_c))  
        self.wait()
        self.play(Transform(total, Text("7").move_to(total).set_color(BLACK)))
        self.wait()
        self.play(rect.animate.move_to(cost_c))
        self.wait()
        self.play(car.animate.next_to(gas_d, UP, buff=0).shift(UP*0.09),
                  )
        
        self.play(Transform(total, Text("2").move_to(total).set_color(BLACK)))
        self.wait(2)

        self.play(FadeOut(rect), FadeOut(total), car.animate.shift(UP*0.29))
        self.wait(2)

        self.play(Indicate(d, color=GREEN))

        self.wait(2)


        text = Text("O(n) * O(n)").set_color(BLACK).next_to(c, DOWN, buff=0.63)
        
        self.play(FadeIn(text[:4]))
        self.wait(2)
        self.play(FadeIn(text[4:]))
        self.wait(2)

        self.play(Transform(text, Tex("O(n^2)", stroke_width=2.5).set_color(BLACK).move_to(text).scale(1.6)))

        self.wait(2)










        self.embed()




class First(Scene):

    def construct(self):
        # Define the LaTeX text for summation comparison
        equation = Tex(
            r"\sum_{i=0}^{n-1}\text{gas}[i] ", r" \geq ", r" \sum_{i=0}^{n-1}\text{cost}[i]",
        )

        # Add colors to differentiate components
        equation.set_color_by_tex("gas[i]", BLUE)
        equation.set_color_by_tex("cost[i]", GREEN)

        # Position the equation in the center
        equation.scale(1.5).move_to(ORIGIN)
        self.play(Write(equation))
        self.wait(2)
