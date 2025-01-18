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
        index_labels = VGroup(
            *[Text(str(i), font_size=30).next_to(square, DOWN, buff=0.23).set_color(BLACK) for i, square in enumerate(squares)]
        )
        return VGroup(squares, index_labels)

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



class Kadane(Scene):

    def construct(self):

        self.camera.frame.scale(0.93).shift(UP*0.83)

        
        # Example usage:
        array = Array(array_size=9)

        array.append_element(self, "-2")
        array.append_element(self, "1")
        array.append_element(self, "-3")
        array.append_element(self, "4")
        array.append_element(self, "-1")
        array.append_element(self, "2")
        array.append_element(self, "1")
        array.append_element(self, "-5")
        array.append_element(self, "4")



        self.wait(2)

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(9)])
        self.wait(2)



        global_max = Text("Global Max: -2").set_color(BLACK).to_edge(UP).shift(DOWN*0.39)
        current_max = Text("Current Max: -2").set_color(BLACK).next_to(global_max, DOWN, buff=0.55)

        self.play(ShowCreation(global_max[:10]), )
        self.wait()
        self.play(TransformFromCopy(array.square_contents[0][1], global_max[10:]))
        self.wait(2)
        self.play(ShowCreation(current_max[:11]), )
        self.wait()
        self.play(TransformFromCopy(array.square_contents[0][1], current_max[11:]))
        self.wait(2)

        i = Text("i").set_color(BLACK).next_to(array.square_contents[1], DOWN, buff=0.78).scale(0.78)
        self.play(ShowCreation(i),array.square_contents[1][0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(UP*0.7))
        
        text = Text("Current Max = max(1, 1 + (-2))").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait(2)

        self.play(TransformFromCopy(array.square_contents[1][1], text[15]))
        self.play(FadeIn(text[16]))
        self.wait(2)
        self.play(TransformFromCopy(array.square_contents[1][1], text[17]))
        self.play(FadeIn(text[18]))
        self.play(TransformFromCopy(current_max[-2:], text[-5:-1]))
        self.wait(2)
        text1 = Text("Current Max = max(1, -1)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait(1)
        text = Text("Current Max = 1").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait(2)

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))

        self.play(Transform(current_max[-2:], Text("1").set_color(BLACK).move_to(current_max[-2])))
        self.wait(2)
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(1, -2)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait(2)

        self.play(TransformFromCopy(current_max[-2], text1[14]))
        self.play(FadeIn(text1[15]))
        self.wait(1)
        self.play(TransformFromCopy(global_max[-2:], text1[-3:-1]))
        self.wait(2)

        text = Text("Global Max = 1").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait(2)

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))

        self.wait(1)

        self.play(Transform(global_max[-2:], Text("1").set_color(BLACK).move_to(global_max[-2])))
        self.play(Uncreate(rect), FadeOut(text))

        self.wait(2)


        #first iteration done

        self.play(i.animate.next_to(array.square_contents[2], DOWN, buff=0.78),
                  array.square_contents[2][0].animate.set_fill(TEAL_B),
                  array.square_contents[1][0].animate.set_fill(YELLOW))
        self.wait(2)


        text = Text("Current Max = max(-3, -3 + 1)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait(2)

        self.play(TransformFromCopy(array.square_contents[2][1], text[15:17]))
        self.play(FadeIn(text[17]))
        self.wait(2)
        self.play(TransformFromCopy(array.square_contents[2][1], text[18:20]))
        self.play(FadeIn(text[20]))
        self.play(TransformFromCopy(current_max[-2], text[-2]))
        self.wait(2)
        text1 = Text("Current Max = max(-3, -2)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait(1)
        text = Text("Current Max = -2").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait(2)

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))

        self.play(Transform(current_max[-2:], Text("-2").set_color(BLACK).move_to(current_max[-2])))
        self.wait(2)
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(-2, 1)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait(2)

        self.play(TransformFromCopy(current_max[-2:], text1[14:16]))
        self.play(FadeIn(text1[16]))
        self.wait(1)
        self.play(TransformFromCopy(global_max[-2:], text1[-2]))
        self.wait(2)

        text = Text("Global Max = 1").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait(2)

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))

        self.wait(2)

        self.play(Uncreate(rect), FadeOut(text))

        self.wait(2)

        #itertioan 3 begines i = 3


        self.play(i.animate.next_to(array.square_contents[3], DOWN, buff=0.78),
                  array.square_contents[3][0].animate.set_fill(TEAL_B),
                  array.square_contents[2][0].animate.set_fill(YELLOW))
        self.wait()


        text = Text("Current Max = max(4, 4 + (-2))").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait()



        self.play(TransformFromCopy(array.square_contents[3][1], text[15]))
        self.play(FadeIn(text[16]))
        self.wait()
        self.play(TransformFromCopy(array.square_contents[3][1], text[17]))
        self.play(FadeIn(text[18]))
        self.play(TransformFromCopy(current_max[-2:], text[-5:-1]))
        self.wait()
        text1 = Text("Current Max = max(4, 2)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait()
        text = Text("Current Max = 4").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))
        self.wait()

        self.play(Transform(current_max[-2:], Text("4").set_color(BLACK).move_to(current_max[-2])))
        self.wait()
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(4, 1)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait()

        self.play(TransformFromCopy(current_max[-2:], text1[14]))
        self.play(FadeIn(text1[15]))
        self.wait()
        self.play(TransformFromCopy(global_max[-2:], text1[-2]))
        self.wait()

        text = Text("Global Max = 4").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))

        self.wait()
        self.play(Transform(global_max[-2:], Text("4").set_color(BLACK).move_to(global_max[-2])))
        self.wait()

        self.play(Uncreate(rect), FadeOut(text))

        self.wait()


        #i = 4 from here beigns

        self.play(i.animate.next_to(array.square_contents[4], DOWN, buff=0.78),
                  array.square_contents[4][0].animate.set_fill(TEAL_B),
                  array.square_contents[3][0].animate.set_fill(YELLOW))
        self.wait()


        text = Text("Current Max = max(-1, -1 + 4)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait()



        self.play(TransformFromCopy(array.square_contents[4][1], text[15:17]))
        self.play(FadeIn(text[17]))
        self.wait()
        self.play(TransformFromCopy(array.square_contents[4][1], text[18:20]))
        self.play(FadeIn(text[20]))
        self.play(TransformFromCopy(current_max[-2:], text[-2]))
        self.wait()
        text1 = Text("Current Max = max(-1, 3)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait()
        text = Text("Current Max = 3").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))
        self.wait()

        self.play(Transform(current_max[-2:], Text("3").set_color(BLACK).move_to(current_max[-2])))
        self.wait()
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(3, 4)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait()

        self.play(TransformFromCopy(current_max[-2:], text1[14]))
        self.play(FadeIn(text1[15]))
        self.wait()
        self.play(TransformFromCopy(global_max[-2:], text1[-2]))
        self.wait()

        text = Text("Global Max = 4").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))
        self.wait()  
        self.play(Uncreate(rect), FadeOut(text))

        self.wait()


        self.play(i.animate.next_to(array.square_contents[5], DOWN, buff=0.78),
                  array.square_contents[5][0].animate.set_fill(TEAL_B),
                  array.square_contents[4][0].animate.set_fill(YELLOW))
        self.wait()


        text = Text("Current Max = max(2, 2 + 3)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait()



        self.play(TransformFromCopy(array.square_contents[5][1], text[15]))
        self.play(FadeIn(text[16]))
        self.wait()
        self.play(TransformFromCopy(array.square_contents[5][1], text[17]))
        self.play(FadeIn(text[18]))
        self.play(TransformFromCopy(current_max[-2:], text[-2]))
        self.wait()
        text1 = Text("Current Max = max(2, 5)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait()
        text = Text("Current Max = 5").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))
        self.wait()

        self.play(Transform(current_max[-2:], Text("5").set_color(BLACK).move_to(current_max[-2])))
        self.wait()
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(5, 4)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait()

        self.play(TransformFromCopy(current_max[-2:], text1[14]))
        self.play(FadeIn(text1[15]))
        self.wait()
        self.play(TransformFromCopy(global_max[-2:], text1[-2]))
        self.wait()

        text = Text("Global Max = 5").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))

        self.wait()
        self.play(Transform(global_max[-2:], Text("5").set_color(BLACK).move_to(global_max[-2])))
        self.wait()
        
        self.play(Uncreate(rect), FadeOut(text))

        self.wait()




        #itertation i = 5, ends and i = 6 begins from here....


        self.play(i.animate.next_to(array.square_contents[6], DOWN, buff=0.78),
                  array.square_contents[6][0].animate.set_fill(TEAL_B),
                  array.square_contents[5][0].animate.set_fill(YELLOW))
        self.wait()


        text = Text("Current Max = max(1, 1 + 5)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait()




        self.play(TransformFromCopy(array.square_contents[6][1], text[15]))
        self.play(FadeIn(text[16]))
        self.wait()
        self.play(TransformFromCopy(array.square_contents[6][1], text[17]))
        self.play(FadeIn(text[18]))
        self.play(TransformFromCopy(current_max[-2:], text[-2]))
        self.wait()
        text1 = Text("Current Max = max(1, 6)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait()
        text = Text("Current Max = 6").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))
        self.wait()

        self.play(Transform(current_max[-2:], Text("6").set_color(BLACK).move_to(current_max[-2])))
        self.wait()
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(6, 5)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait()

        self.play(TransformFromCopy(current_max[-2:], text1[14]))
        self.play(FadeIn(text1[15]))
        self.wait()
        self.play(TransformFromCopy(global_max[-2:], text1[-2]))
        self.wait()

        text = Text("Global Max = 6").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))

        self.wait()
        self.play(Transform(global_max[-2:], Text("6").set_color(BLACK).move_to(global_max[-2])))
        self.wait()
        
        self.play(Uncreate(rect), FadeOut(text))

        self.wait()

        #iteration i = 7 now begins

        self.play(i.animate.next_to(array.square_contents[7], DOWN, buff=0.78),
                  array.square_contents[7][0].animate.set_fill(TEAL_B),
                  array.square_contents[6][0].animate.set_fill(YELLOW))
        self.wait()


        text = Text("Current Max = max(-5, -5 + 6)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait()



        self.play(TransformFromCopy(array.square_contents[7][1], text[15:17]))
        self.play(FadeIn(text[17]))
        self.wait()
        self.play(TransformFromCopy(array.square_contents[3][1], text[18:20]))
        self.play(FadeIn(text[20]))
        self.play(TransformFromCopy(current_max[-2:], text[-2]))
        self.wait()
        text1 = Text("Current Max = max(-5, 1)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait()
        text = Text("Current Max = 1").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))
        self.wait()

        self.play(Transform(current_max[-2:], Text("1").set_color(BLACK).move_to(current_max[-2]).shift(UP*0.047)))
        self.wait()
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(1, 6)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait()

        self.play(TransformFromCopy(current_max[-2:], text1[14]))
        self.play(FadeIn(text1[15]))
        self.wait()
        self.play(TransformFromCopy(global_max[-2:], text1[-2]))
        self.wait()

        text = Text("Global Max = 6").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))        
        self.play(Uncreate(rect), FadeOut(text))

        self.wait()


        # i = 8, here

        self.play(i.animate.next_to(array.square_contents[8], DOWN, buff=0.78),
                  array.square_contents[8][0].animate.set_fill(TEAL_B),
                  array.square_contents[7][0].animate.set_fill(YELLOW))
        self.wait()


        text = Text("Current Max = max(4, 4 + 1)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        
        self.play(FadeIn(text[:15]), FadeIn(text[-1]))
        self.wait()



        self.play(TransformFromCopy(array.square_contents[-1][1], text[15]))
        self.play(FadeIn(text[16]))
        self.wait()
        self.play(TransformFromCopy(array.square_contents[-1][1], text[17]))
        self.play(FadeIn(text[18]))
        self.play(TransformFromCopy(current_max[-2:], text[-2]))
        self.wait()
        text1 = Text("Current Max = max(4, 5)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text, text1), run_time=0.56)
        self.wait()
        text = Text("Current Max = 5").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)
        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(current_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))
        self.wait()

        self.play(Transform(current_max[-2:], Text("5").set_color(BLACK).move_to(current_max[-2])))
        self.wait()
        self.play(FadeOut(rect))

        text1 = Text("Global Max = max(5, 6)").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)

        self.play(FadeOut(text),FadeIn(text1[:14]), FadeIn(text1[-1]) )
        self.wait()

        self.play(TransformFromCopy(current_max[-2:], text1[14]))
        self.play(FadeIn(text1[15]))
        self.wait()
        self.play(TransformFromCopy(global_max[-2:], text1[-2]))
        self.wait()

        text = Text("Global Max = 6").set_color(BLACK).scale(0.8).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED)
        self.play(TransformMatchingTex(text1, text), run_time=0.56)

        self.wait()

        rect = always_redraw(lambda: SurroundingRectangle(global_max[-2:], color="#0000FF", stroke_width=7.8).scale(1.2))
        self.play(GrowFromCenter(rect))        
        self.play(Uncreate(rect))

        self.play(FadeOut(i), FadeOut(VGroup(global_max, current_max)),
                  array.square_contents[-1][0].animate.set_fill(YELLOW))
        
        
        self.wait(2)
        brace = Brace(VGroup(array.square_contents[3], array.square_contents[4], 
                             array.square_contents[5], array.square_contents[6]), UP, buff=0.45).set_color(BLACK)
        

        self.play(text.animate.scale(1.77).shift(DOWN*0.8))

        self.play(array.square_contents[3][0].animate.set_fill(BLUE), array.square_contents[4][0].animate.set_fill(BLUE), 
                             array.square_contents[5][0].animate.set_fill(BLUE), array.square_contents[6][0].animate.set_fill(BLUE),
                             GrowFromCenter(brace))


        self.wait(2)

class Formula(Scene):
        
        def construct(self):

            text = Text("Current_Max = max(arr[i], arr[i] + Current_Max)").set_color(BLACK).scale(0.7).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED).shift(DOWN*3.5)
            text1 = Text("Global_Max = max(Current_Max, Global_Max)").set_color(BLACK).scale(0.7).to_edge(UP).shift(UP).set_color_by_text("max", PURE_RED).shift(DOWN*4.9)

            self.play(ShowCreation(text))
            self.wait(2)
            self.play(ShowCreation(text1))
            self.wait(2)

            rect = SurroundingRectangle(text, stroke_width=7.8, color="#0000FF").scale(1.03)

            self.play(ShowCreation(rect))

            self.wait(2)

            self.play(Transform(rect, SurroundingRectangle(text1, stroke_width=7.8, color="#0000FF").scale(1.03)))

            self.wait(2)

            self.play(Uncreate(rect))

            self.wait(2)

            




            self.embed()





class Kadane1(Scene):

    def construct(self):

        self.camera.frame.scale(0.93).shift(UP*1.06)

        
        # Example usage:
        array = Array(array_size=9)

        array.append_element(self, "-2")
        array.append_element(self, "1")
        array.append_element(self, "-3")
        array.append_element(self, "4")
        array.append_element(self, "-1")
        array.append_element(self, "2")
        array.append_element(self, "1")
        array.append_element(self, "-5")
        array.append_element(self, "4")



        self.wait(2)

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(9)])
        self.wait(2)


        brace = Brace(VGroup(array.square_contents[0]), UP, buff=0.4).set_color(BLACK)
        self.play(GrowFromCenter(brace), array.square_contents[0][0].animate.set_fill(BLUE))

        self.wait(1)

        result = Text("Sum = -2").next_to(array, UP, buff=2).scale(1.2).set_color(BLACK)
        self.play(ShowCreation(result))

        self.wait(2)

        self.play(Transform(brace, Brace(VGroup(array.square_contents[0], array.square_contents[1]), UP, buff=0.4).set_color(BLACK)),
                  array.square_contents[1][0].animate.set_fill(BLUE))
        

        result1 = Text("Sum = -1").next_to(array, UP, buff=2).scale(1.2).set_color(BLACK)

        self.play(TransformMatchingTex(result, result1), run_time=0.6)

        self.wait(2)
        
        self.play(Transform(brace, Brace(VGroup(array.square_contents[0], array.square_contents[1], array.square_contents[2]), UP, buff=0.4).set_color(BLACK)),
                  array.square_contents[1][0].animate.set_fill(BLUE), array.square_contents[2][0].animate.set_fill(BLUE))
        
        result = Text("Sum = -4").next_to(array, UP, buff=2).scale(1.2).set_color(BLACK)

        self.play(TransformMatchingTex(result1, result), run_time=0.6)

        self.wait(2)

        self.play(Transform(brace, Brace(VGroup(array.square_contents[2], array.square_contents[3], array.square_contents[4]), UP, buff=0.4).set_color(BLACK)),
                  array.square_contents[3][0].animate.set_fill(BLUE), array.square_contents[4][0].animate.set_fill(BLUE),
                  array.square_contents[0][0].animate.set_fill(YELLOW), array.square_contents[1][0].animate.set_fill(YELLOW))
        
        result1 = Text("Sum = 0").next_to(array, UP, buff=2).scale(1.2).set_color(BLACK)

        self.play(TransformMatchingTex(result, result1), run_time=0.6)


        self.wait()

        self.play(Transform(brace, Brace(VGroup(array.square_contents[2], array.square_contents[3], array.square_contents[4],
                                                array.square_contents[5], array.square_contents[6]), UP, buff=0.4).set_color(BLACK)),
                  array.square_contents[5][0].animate.set_fill(BLUE), array.square_contents[6][0].animate.set_fill(BLUE),
                  array.square_contents[0][0].animate.set_fill(YELLOW), array.square_contents[1][0].animate.set_fill(YELLOW))
        
        result = Text("Sum = 3").next_to(array, UP, buff=2).scale(1.2).set_color(BLACK)

        self.play(TransformMatchingTex(result1, result), run_time=0.6)

        self.wait()

        self.play(Transform(brace, Brace(VGroup(array.square_contents[0], array.square_contents[3], array.square_contents[4],
                                                array.square_contents[-1], array.square_contents[6]), UP, buff=0.4).set_color(BLACK)),
                  array.square_contents[0][0].animate.set_fill(BLUE), array.square_contents[-1][0].animate.set_fill(BLUE),
                  array.square_contents[1][0].animate.set_fill(BLUE), array.square_contents[-2][0].animate.set_fill(BLUE))
        
        result1 = Text("Sum = 1").next_to(array, UP, buff=2).scale(1.2).set_color(BLACK)

        self.play(TransformMatchingTex(result, result1), run_time=0.6)

        self.wait()

        self.play(Transform(brace, Brace(VGroup(array.square_contents[3],
                                                array.square_contents[6],), UP, buff=0.4).set_color(BLACK)),
                  array.square_contents[1][0].animate.set_fill(YELLOW), array.square_contents[-1][0].animate.set_fill(YELLOW),
                  array.square_contents[0][0].animate.set_fill(YELLOW), array.square_contents[2][0].animate.set_fill(YELLOW),
                  array.square_contents[-2][0].animate.set_fill(YELLOW))
        
        result = Text("Sum = 6").next_to(array, UP, buff=2).scale(1.2).set_color(BLACK)

        self.play(TransformMatchingTex(result1, result), run_time=0.6)
        
        self.wait(2)



        self.embed()
