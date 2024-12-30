from manimlib import *

PURE_RED = "#FF0000"
PURE_GREEN = "#00FF00"
PURE_BLUE = "#0000FF"



class Hash1(Scene):

    def construct(self):

        hash_table = Text("Hash Tables").to_edge(UP).shift(DOWN*0.32).set_color(BLACK).scale(1.2)

        self.play(FadeIn(hash_table, shift=DOWN))

        self.wait(2)
        a1 = (
    RoundedRectangle(stroke_width=30, fill_opacity=1)
    .set_fill(TEAL_B, opacity=1)      # Fully opaque fill
    .set_stroke(TEAL_B, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(LEFT * 3 + DOWN * 0.5)
)

        text=Text("KEY", font=BOLD).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).shift(LEFT*0.1)
        self.play(GrowFromCenter(a))


        b1 = (
    RoundedRectangle(stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(DOWN * 0.5 + RIGHT*3)
)

        text=Text("VALUE", font=BOLD).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.17)
        b=VGroup(b1, text).shift(LEFT*0.1)

        arrow = Arrow(a.get_right(), b.get_left(), stroke_width=5).set_color(BLACK)

        self.play(ShowCreation(arrow))
        self.play(GrowFromCenter(b))
        self.wait(2)

        self.play(Indicate(a, color=None))
        self.wait(1)
        self.play(Indicate(b, color=None))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*13))

        self.wait(2)


        #example key values

        c1 = (
    RoundedRectangle(height=1.33, stroke_width=30, fill_opacity=1)
    .set_fill(TEAL_B, opacity=1)      # Fully opaque fill
    .set_stroke(TEAL_B, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(UP * 2 + RIGHT*9)
)

        text=Text("Alice", font=BOLD).set_color(BLACK).move_to(c1).set_z_index(1)
        c=VGroup(c1, text).shift(LEFT*0.1)

        d1 = (
    RoundedRectangle(height=1.33, stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(UP * 2 + RIGHT*17)
)

        text=Text("8397", font=BOLD).set_color(BLACK).move_to(d1).set_z_index(1)
        d=VGroup(d1, text).shift(LEFT*0.1)

        #second goes here

        e1 = (
    RoundedRectangle(height=1.33, stroke_width=30, fill_opacity=1)
    .set_fill(TEAL_B, opacity=1)      # Fully opaque fill
    .set_stroke(TEAL_B, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(RIGHT*9)
)

        text=Text("Bob", font=BOLD).set_color(BLACK).move_to(e1).set_z_index(1)
        e=VGroup(e1, text).shift(LEFT*0.1)

        f1 = (
    RoundedRectangle(height=1.33, stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(RIGHT*17)
)

        text=Text("8371", font=BOLD).set_color(BLACK).move_to(f1).set_z_index(1)
        f=VGroup(f1, text).shift(LEFT*0.1)


        #third from here


        g1 = (
    RoundedRectangle(height=1.33, stroke_width=30, fill_opacity=1)
    .set_fill(TEAL_B, opacity=1)      # Fully opaque fill
    .set_stroke(TEAL_B, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(DOWN*2 + RIGHT*9)
)

        text=Text("Oscar", font=BOLD).set_color(BLACK).move_to(g1).set_z_index(1)
        g=VGroup(g1, text).shift(LEFT*0.1)

        h1 = (
    RoundedRectangle(height=1.33, stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(DOWN*2+RIGHT*17)
)

        text=Text("8420", font=BOLD).set_color(BLACK).move_to(h1).set_z_index(1)
        h=VGroup(h1, text).shift(LEFT*0.1)


        self.wait()


        arrow1 = Arrow(c.get_right(), d.get_left(), stroke_width=6).set_color(BLACK)
        arrow2 = Arrow(e.get_right(), f.get_left(), stroke_width=6).set_color(BLACK)
        arrow3 = Arrow(g.get_right(), h.get_left(), stroke_width=6).set_color(BLACK)


        self.play(GrowFromCenter(c), GrowFromCenter(d), 
                  GrowFromCenter(e), GrowFromCenter(f), 
                  GrowFromCenter(g), GrowFromCenter(h))
        
        self.play(ShowCreation(VGroup(arrow1, arrow2, arrow3)))

        self.wait(2)

        self.play(Indicate(e, color=None))
        self.wait()
        self.play(Indicate(f, color=None))

        self.wait(2)


        self.play(self.camera.frame.animate.shift(LEFT*13))


        self.play(FadeOut(arrow), a.animate.shift(LEFT*1.6), b.animate.shift(RIGHT*1.6))
        self.wait(1)

        hash_1 = Circle(radius=0.77, stroke_width=30).set_fill(RED_A, opacity=1).set_stroke(RED_A, opacity=0.6).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("H").set_color(BLACK).scale(1.4).move_to(hash_1)
        hash = VGroup(hash_1, hash_2).set_z_index(2)
        self.play(GrowFromCenter(hash))
        self.wait(2)


        arrow4 = Arrow(a.get_right(), hash.get_left(), stroke_width=5).set_color(BLACK)
        arrow5 = Arrow(hash.get_right(), b.get_left(), stroke_width=5).set_color(BLACK)

        self.play(ShowCreation(arrow4))
        self.wait(2)

        self.play(a[1].copy().animate.scale(0.2).move_to(hash))
        self.wait()
        self.play(ShowCreation(arrow5), FadeOut(VGroup(arrow1, arrow2, arrow3, c,d,e,f,g,h,)))
        self.wait(2)
        self.play(self.camera.frame.animate.shift(RIGHT*13), FadeOut(VGroup(a,b,arrow)))

        self.wait(2)

        rect1 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)
        rect2 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)
        rect3 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)
        rect4 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)
        rect5 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)
        rect6 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)
        rect7 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)
        rect8 = Rectangle(height=1, width=5).set_color(GREY_D).set_stroke(width=6.5)

        array = VGroup(rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8)
        array.arrange(DOWN, buff=0).shift(RIGHT * 17).scale(0.76)

        # Create indexes and align them
        indexes = VGroup()
        for i, rect in enumerate(array):
            index_text = Text(str(i)).scale(0.6).set_color(BLACK)  # Create index text
            index_text.next_to(rect, LEFT, buff=0.3)  # Position to the left of each rectangle
            indexes.add(index_text)

        # Align all indexes in a single straight vertical line
        indexes.align_to(array, LEFT).shift(LEFT * 0.5)  # Shift left to ensure alignment

        

        self.play(ShowCreation(array))
        self.play(GrowFromCenter(indexes))

        self.wait(2)

        hash_func = Text("key % size").set_color(BLACK).next_to(array, LEFT).scale(0.86).shift(UP*2.5+LEFT*1.88)

        self.play(ShowCreation(hash_func))
        self.wait(2)

        self.play(Transform(hash_func[4:], Text("8").set_color(BLACK).scale(0.86).move_to(hash_func[4])))
        self.wait(2)

        first_rect = (
    RoundedRectangle(height=1.23,width=8, stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(DOWN*2+RIGHT*17)
).next_to(hash_func, DOWN, buff=0.999)

        first_insert = Text("Insert(12, \"Alice\")").set_color(BLACK).scale(0.75).move_to(first_rect)
        first_group = VGroup(first_rect, first_insert)

        self.play(GrowFromCenter(first_group))

        self.wait(2)

        first_text = Text("12 % 8").set_color(BLACK).next_to(first_group, DOWN, buff=1).scale(0.88).shift(DOWN*0.62)
        self.play(TransformFromCopy(first_group[1][7:9], first_text[:2]))

        self.wait(1)

        self.play(FadeIn(first_text[2:]))
        self.wait(1)

        self.play(Transform(first_text, Text("4").set_color(BLACK).move_to(first_text).scale(0.88)))
        srect = SurroundingRectangle(indexes[4], color="#0000FF")
        self.play(ShowCreation(srect))

        self.wait()

        text_at_4 = Text("12, \"Alice\"").set_color(BLACK).scale(0.62).move_to(rect5)
        self.play(ReplacementTransform(first_group, text_at_4), run_time=1.5)
        self.play(FadeOut(srect), FadeOut(first_text))
        self.wait(2)

        #next is from here


        first_rect = (
    RoundedRectangle(height=1.23,width=8, stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(DOWN*2+RIGHT*17)
).next_to(hash_func, DOWN, buff=0.999)

        first_insert = Text("Insert(10, \"Bob\")").set_color(BLACK).scale(0.75).move_to(first_rect)
        first_group = VGroup(first_rect, first_insert)

        self.play(GrowFromCenter(first_group))

        self.wait(2)

        first_text = Text("10 % 8").set_color(BLACK).next_to(first_group, DOWN, buff=1).scale(0.88).shift(DOWN*0.62)
        self.play(TransformFromCopy(first_group[1][7:9], first_text[:2]))

        self.wait(1)

        self.play(FadeIn(first_text[2:]))
        self.wait(1)

        self.play(Transform(first_text, Text("2").set_color(BLACK).move_to(first_text).scale(0.88)))
        srect = SurroundingRectangle(indexes[2], color="#0000FF")
        self.play(ShowCreation(srect))

        self.wait()

        text_at_4 = Text("10, \"Bob\"").set_color(BLACK).scale(0.62).move_to(rect3)
        self.play(ReplacementTransform(first_group, text_at_4), run_time=1.5)
        self.play(FadeOut(srect), FadeOut(first_text))
        self.wait(2)

        #next is from here


        first_rect = (
    RoundedRectangle(height=1.23,width=8, stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(DOWN*2+RIGHT*17)
).next_to(hash_func, DOWN, buff=0.999)

        first_insert = Text("Insert(8, \"Oscar\")").set_color(BLACK).scale(0.75).move_to(first_rect)
        first_group = VGroup(first_rect, first_insert)

        self.play(GrowFromCenter(first_group))

        self.wait(2)

        first_text = Text("8 % 8").set_color(BLACK).next_to(first_group, DOWN, buff=1).scale(0.88).shift(DOWN*0.62)
        self.play(TransformFromCopy(first_group[1][7], first_text[:1]))

        self.wait(1)

        self.play(FadeIn(first_text[1:]))
        self.wait(1)

        self.play(Transform(first_text, Text("0").set_color(BLACK).move_to(first_text).scale(0.88)))
        srect = SurroundingRectangle(indexes[0], color="#0000FF")
        self.play(ShowCreation(srect))

        self.wait()

        text_at_4 = Text("8, \"Oscar\"").set_color(BLACK).scale(0.62).move_to(rect1)
        self.play(ReplacementTransform(first_group, text_at_4), run_time=1.5)
        self.play(FadeOut(srect), FadeOut(first_text))
        self.wait(2)


        first_rect = (
    RoundedRectangle(height=1.23,width=8, stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(DOWN*2+RIGHT*17)
).next_to(hash_func, DOWN, buff=0.999)

        first_insert = Text("Insert(2, \"Vivek\")").set_color(BLACK).scale(0.75).move_to(first_rect)
        first_group = VGroup(first_rect, first_insert)

        self.play(GrowFromCenter(first_group))

        self.wait(2)

        first_text = Text("2 % 8").set_color(BLACK).next_to(first_group, DOWN, buff=1).scale(0.88).shift(DOWN*0.62)
        self.play(TransformFromCopy(first_group[1][7], first_text[:1]))

        self.wait(1)

        self.play(FadeIn(first_text[1:]))
        self.wait(1)

        self.play(Transform(first_text, Text("2").set_color(BLACK).move_to(first_text).scale(0.88)))
        srect = SurroundingRectangle(indexes[2], color="#0000FF")
        self.play(ShowCreation(srect))

        self.wait(2)

        background = Rectangle(
            width=5,
            height=5,
            color=RED,
            fill_opacity=0.65  # Make it semi-transparent
        ).scale(10)
        background.set_z_index(2)  # Ensure it stays in the background

        background.move_to(array)

        self.play(FadeIn(background))

        self.wait(2)




class Double(Scene):
    def construct(self):



        rect1 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect2 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect3 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect4 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect5 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect6 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect7 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect8 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)

        array = VGroup(rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8)
        array.arrange(DOWN, buff=0).scale(0.76)
        array.shift(LEFT*2.8).scale(1.1)

        # Create indexes and align them
        indexes = VGroup()
        for i, rect in enumerate(array):
            index_text = Text(str(i)).scale(0.6).set_color(BLACK)  # Create index text
            index_text.next_to(rect, LEFT, buff=0.3)  # Position to the left of each rectangle
            indexes.add(index_text)

        # Align all indexes in a single straight vertical line
        indexes.align_to(array, LEFT).shift(LEFT * 0.5)  # Shift left to ensure alignment

        

        self.play(ShowCreation(array))
        self.play(GrowFromCenter(indexes))

        self.wait(2)

        formula = TexText(
            r"$\left( h_1(k) + i \cdot h_2(k) \right)  mod \ m$"
        ).set_color(BLACK)

        # Adjust scaling and positioning if necessary
        formula.scale(1.3).shift(RIGHT * 1.3).shift(UP*2.77+RIGHT*1.1)

        # Play the animation
        self.play(Write(formula))
        self.wait(2)
        self.play(Transform(formula[-1], TexText("$8$").scale(1.3).set_color(BLACK).move_to(formula[-1]).shift(UP*0.05+LEFT*0.06)))
        self.wait(2)

        formula1 = TexText(
    r"$P - (k \mod P)$"
).set_color(BLACK)

        
        formula1.scale(1.3).next_to(formula, DOWN).shift(DOWN*0.07)

        self.play(Write(formula1))

        self.wait(2)



        self.play(Transform(formula1[0], TexText("$5$").scale(1.3).set_color(BLACK).move_to(formula1[0]).shift(DOWN*0.02+RIGHT*0.06)),
                  Transform(formula1[-2], TexText("$5$").scale(1.3).set_color(BLACK).move_to(formula1[-2]).shift(LEFT*0.06))
                  )
        
        self.wait(2)





        a1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("2, \'A\'", font=BOLD).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.456).next_to(indexes[3], LEFT, buff=0.87)

        self.play(GrowFromCenter(a))
        self.wait(2)

        self.play(a.animate.move_to(rect3).scale(0.77))

        self.wait(2)


        #done here

        b1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("10, \'B\'", font=BOLD).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.37)
        b=VGroup(b1, text).scale(0.456).next_to(indexes[3], LEFT, buff=0.87)

        self.play(GrowFromCenter(b))
        self.wait(2)

        pointer = Arrow(a.get_right(), a.get_right()+RIGHT*1.1, stroke_width=3).set_color(PURE_RED)
        pointer.next_to(rect3, LEFT, buff=0.99)

        self.play(ShowCreation(pointer))
        self.wait(2)




        copy1 = formula1.copy()

        self.play(copy1.animate.shift(DOWN*2.3))
        self.wait(2)

        self.play(Transform(copy1[3], TexText("$10$").scale(1.3).set_color(BLACK).move_to(copy1[3]).shift(RIGHT*0.12)))
        self.wait(2)
        self.play(Transform(copy1, TexText("$5$").scale(1.3).set_color(BLACK).move_to(copy1[3])))
        self.wait(2)

        copy2 = TexText(
            r"$\left( 2 + 1 \cdot 5 \right)  mod \ 8$"
        ).set_color(BLACK)

        # Adjust scaling and positioning if necessary
        copy2.scale(1.3).next_to(copy1, DOWN).shift(DOWN*0.2)

        # Play the animation
        self.play(ShowCreation(copy2), FadeOut(copy1))
        self.wait(2)

        self.play(Transform(copy2, TexText("$7$").scale(1.3).set_color(BLACK).move_to(copy2)))

        self.wait(2)
        self.play(pointer.animate.next_to(rect8, LEFT, buff=0.99))
        self.wait(2)

        self.play(b.animate.move_to(rect8).scale(0.77), FadeOut(copy2), FadeOut(pointer))
        self.wait(2)








        c1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("18, \'C\'", font=BOLD).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.37)
        c=VGroup(c1, text).scale(0.456).next_to(indexes[3], LEFT, buff=1)

        self.play(GrowFromCenter(c))
        self.wait(2)

        pointer = Arrow(a.get_right(), a.get_right()+RIGHT*1.1, stroke_width=3).set_color(PURE_RED)
        pointer.next_to(rect3, LEFT, buff=0.99)

        self.play(ShowCreation(pointer))
        self.wait(2)



        copy1 = formula1.copy()

        self.play(copy1.animate.shift(DOWN*2.3))
        self.wait(2)

        self.play(Transform(copy1[3], TexText("$18$").scale(1.3).set_color(BLACK).move_to(copy1[3]).shift(RIGHT*0.12)))
        self.wait(2)
        self.play(Transform(copy1, TexText("$2$").scale(1.3).set_color(BLACK).move_to(copy1[3])))
        self.wait(2)

        copy2 = TexText(
            r"$\left( 2 + 1 \cdot 2 \right)  mod \ 8$"
        ).set_color(BLACK)

        # Adjust scaling and positioning if necessary
        copy2.scale(1.3).next_to(copy1, DOWN).shift(DOWN*0.2)

        # Play the animation
        self.play(ShowCreation(copy2), FadeOut(copy1))
        self.wait(2)

        self.play(Transform(copy2, TexText("$4$").scale(1.3).set_color(BLACK).move_to(copy2)))

        self.wait(2)
        self.play(pointer.animate.next_to(rect5, LEFT, buff=0.99))
        self.wait(2)

        self.play(c.animate.move_to(rect5).scale(0.77), FadeOut(copy2), FadeOut(pointer))
        self.wait(5)



















class Quad(Scene):
    def construct(self):



        rect1 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect2 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect3 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect4 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect5 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect6 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect7 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect8 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)

        array = VGroup(rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8)
        array.arrange(DOWN, buff=0).scale(0.76)
        array.shift(LEFT*2.8).scale(1.1)

        # Create indexes and align them
        indexes = VGroup()
        for i, rect in enumerate(array):
            index_text = Text(str(i)).scale(0.6).set_color(BLACK)  # Create index text
            index_text.next_to(rect, LEFT, buff=0.3)  # Position to the left of each rectangle
            indexes.add(index_text)

        # Align all indexes in a single straight vertical line
        indexes.align_to(array, LEFT).shift(LEFT * 0.5)  # Shift left to ensure alignment

        

        self.play(ShowCreation(array))
        self.play(GrowFromCenter(indexes))

        self.wait(2)


        formula = Tex(r"(h(k) + i^2)\ \text{mod}").set_color(BLACK)        
        formula1 = Tex(r"mod").set_color(BLACK).next_to(formula, RIGHT)
        formula2 = Tex(r"size").set_color(BLACK).next_to(formula1, RIGHT)
        f = VGroup(formula, formula1, formula2).shift(RIGHT*1.3).scale(1.5)
        self.play(ShowCreation(f))
        self.wait(2)

        self.play(f.animate.scale(0.82).shift(UP*2.53))
        self.wait(2)





        a1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("1, \'A\'", font=BOLD).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.456).next_to(indexes[3], RIGHT, buff=4)

        self.play(GrowFromCenter(a))
        self.wait(2)

        self.play(a.animate.move_to(rect2).scale(0.77))

        self.wait(2)


        #done here

        b1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("2, \'B\'", font=BOLD).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.37)
        b=VGroup(b1, text).scale(0.456).next_to(indexes[3], RIGHT, buff=4)

        self.play(GrowFromCenter(b))
        self.wait(2)





        self.play(b.animate.move_to(rect3).scale(0.77),)
        self.wait(2)

        c1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("9, \'C\'", font=BOLD).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.37)
        c=VGroup(c1, text).scale(0.456).next_to(indexes[3], RIGHT, buff=4)

        self.play(GrowFromCenter(c))
        self.wait(2)

        pointer = Arrow(a.get_right(), a.get_right()+RIGHT*1.1, stroke_width=3).set_color(PURE_RED)
        pointer.next_to(rect2, LEFT, buff=0.99)

        self.play(ShowCreation(pointer))
        self.wait(2)


        formula11 = Tex(r"(1 + 1^2)\ \text{mod}").set_color(BLACK)        
        formula111 = Tex(r"mod").set_color(BLACK).next_to(formula11, RIGHT)
        formula21 = Tex(r"8").set_color(BLACK).next_to(formula111, RIGHT)
        ff = VGroup(formula11, formula111, formula21).next_to(c, DOWN).scale(1.2).shift(DOWN+RIGHT*1.5)
        self.play(ShowCreation(ff))
        self.wait(2)
        fff = Tex(r"2").set_color(BLACK).move_to(ff).scale(1.4)
        self.play(Transform(ff, fff))

        self.wait(2)

        self.play(pointer.animate.next_to(rect3, LEFT, buff=0.99))

        self.wait(2)

        self.play(FadeOut(ff))

        self.wait(2)

        formula11 = Tex(r"(1 + 2^2)\ \text{mod}").set_color(BLACK)        
        formula111 = Tex(r"mod").set_color(BLACK).next_to(formula11, RIGHT)
        formula21 = Tex(r"8").set_color(BLACK).next_to(formula111, RIGHT)
        ff1 = VGroup(formula11, formula111, formula21).next_to(c, DOWN).scale(1.2).shift(DOWN+RIGHT*1.5)
        self.play(ShowCreation(ff1))
        self.wait(2)
        fff = Tex(r"5").set_color(BLACK).move_to(ff).scale(1.4)
        self.play(Transform(ff1, fff))


        self.wait(2)

        self.play(pointer.animate.next_to(rect6, LEFT, buff=0.99))
        self.wait(2)

        self.play(c.animate.move_to(rect6).scale(0.77),FadeOut(ff1), FadeOut(pointer))

        self.wait(2)

        self.play(VGroup(array, indexes, a,b,c).animate.shift(LEFT))
        self.wait()

        arrow_1 = CurvedArrow(rect2.get_right(), rect3.get_right(), stroke_width=5).set_color(BLACK).flip().shift(RIGHT*0.4)
        self.play(ShowCreation(arrow_1))

        self.wait(1)

        arrow_2 = CurvedArrow(rect3.get_right(), rect6.get_right(), stroke_width=5).set_color(BLACK).flip().shift(RIGHT*0.63)
        self.play(ShowCreation(arrow_2))

        self.wait(2)

        formula11 = Tex(r"(1 + 3^2)\ \text{mod}").set_color(BLACK)        
        formula111 = Tex(r"mod").set_color(BLACK).next_to(formula11, RIGHT)
        formula21 = Tex(r"8").set_color(BLACK).next_to(formula111, RIGHT)
        ff1 = VGroup(formula11, formula111, formula21).next_to(ff, ORIGIN).scale(1.2)
        self.play(ShowCreation(ff1))
        self.wait(2)
        fff = Tex(r"2").set_color(BLACK).move_to(ff).scale(1.4)
        self.play(Transform(ff1, fff))

        self.wait(2)

        arrow_3 = CurvedArrow(indexes[5].get_left(), indexes[2].get_left(), stroke_width=5).set_color(BLACK).flip().shift(RIGHT*0.63+LEFT*1.4)
        self.play(ShowCreation(arrow_3), FadeOut(ff1))
        self.wait(2)








        self.embed()




        


















class Linear(Scene):
    def construct(self):



        rect1 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect2 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect3 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect4 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect5 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect6 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect7 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect8 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)

        array = VGroup(rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8)
        array.arrange(DOWN, buff=0).scale(0.76)
        array.shift(LEFT*2.8).scale(1.1)

        # Create indexes and align them
        indexes = VGroup()
        for i, rect in enumerate(array):
            index_text = Text(str(i)).scale(0.6).set_color(BLACK)  # Create index text
            index_text.next_to(rect, LEFT, buff=0.3)  # Position to the left of each rectangle
            indexes.add(index_text)

        # Align all indexes in a single straight vertical line
        indexes.align_to(array, LEFT).shift(LEFT * 0.5)  # Shift left to ensure alignment

        

        self.play(ShowCreation(array))
        self.play(GrowFromCenter(indexes))

        self.wait(2)

        a1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("4, \'A\'", font=BOLD).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.456).next_to(indexes[3], RIGHT, buff=4)

        self.play(GrowFromCenter(a))
        self.wait(2)

        self.play(a.animate.move_to(rect5).scale(0.77))

        self.wait(2)

        b1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("12, \'B\'", font=BOLD).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.37)
        b=VGroup(b1, text).scale(0.456).next_to(indexes[3], RIGHT, buff=4)

        self.play(GrowFromCenter(b))
        self.wait(2)

        pointer = Arrow(a.get_right(), a.get_right()+RIGHT*1.1, stroke_width=3).set_color(PURE_RED)
        pointer.next_to(rect5, LEFT, buff=0.99)

        self.play(ShowCreation(pointer))
        self.wait(2)

        self.play(pointer.animate.next_to(rect6, LEFT, buff=0.99))
        self.wait(2)

        self.play(b.animate.move_to(rect6).scale(0.77), FadeOut(pointer))
        self.wait(2)

        c1 = (
    RoundedRectangle(stroke_width=20, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.7)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("20, \'C\'", font=BOLD).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.37)
        c=VGroup(c1, text).scale(0.456).next_to(indexes[3], RIGHT, buff=4)

        self.play(GrowFromCenter(c))
        self.wait(2)

        pointer = Arrow(a.get_right(), a.get_right()+RIGHT*1.1, stroke_width=3).set_color(PURE_RED)
        pointer.next_to(rect5, LEFT, buff=0.99)

        self.play(ShowCreation(pointer))
        self.wait(2)

        self.play(pointer.animate.next_to(rect6, LEFT, buff=0.99))
        self.wait(1)
        self.play(pointer.animate.next_to(rect7, LEFT, buff=0.99))
        self.wait(2)

        self.play(c.animate.move_to(rect7).scale(0.77), FadeOut(pointer))
        self.wait(2)

        formula = Tex(r"(h(k) + i)\ \text{mod}").set_color(BLACK)        
        formula1 = Tex(r"mod").set_color(BLACK).next_to(formula, RIGHT)
        formula2 = Tex(r"size").set_color(BLACK).next_to(formula1, RIGHT)
        f = VGroup(formula1, formula, formula2).shift(RIGHT*1.3)
        self.play(ShowCreation(formula))
        self.wait(3)
        self.play(ShowCreation(formula1), ShowCreation(formula2))
        self.wait(2)

        brace = Brace(VGroup(rect5, rect6, rect7), RIGHT).set_color(BLACK)
        self.play(GrowFromCenter(brace))

        self.wait(2)


        








        self.embed()























class CollisionHandling(Scene):
    def construct(self):



        rect1 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect2 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect3 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect4 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect5 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect6 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect7 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)
        rect8 = Rectangle(height=1, width=2).set_color(GREY_D).set_stroke(width=6.5)

        array = VGroup(rect1, rect2, rect3, rect4, rect5, rect6, rect7, rect8)
        array.arrange(DOWN, buff=0).scale(0.76)
        array.shift(LEFT*2.8).scale(1.1)

        # Create indexes and align them
        indexes = VGroup()
        for i, rect in enumerate(array):
            index_text = Text(str(i)).scale(0.6).set_color(BLACK)  # Create index text
            index_text.next_to(rect, LEFT, buff=0.3)  # Position to the left of each rectangle
            indexes.add(index_text)

        # Align all indexes in a single straight vertical line
        indexes.align_to(array, LEFT).shift(LEFT * 0.5)  # Shift left to ensure alignment

        

        self.play(ShowCreation(array))
        self.play(GrowFromCenter(indexes))

        self.wait(2)

        a1 = (
    RoundedRectangle(stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("4, \'A\'", font=BOLD).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.456).next_to(indexes[3], LEFT, buff=0.7)

        self.play(GrowFromCenter(a))
        self.wait(2)

        arrow_1 = Arrow(rect5.get_center(), rect5.get_right()+RIGHT, stroke_width=5).set_color(GREY_D)

        self.play(ShowCreation(arrow_1), a.animate.move_to(rect5.get_right()+RIGHT*1.7))
        self.wait(2)



        b1 = (
    RoundedRectangle(stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77).shift(RIGHT)
    
)

        text=Text("12, \'C\'", font=BOLD).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.1)
        b=VGroup(b1, text).scale(0.456).next_to(indexes[3], LEFT, buff=0.7)

        self.play(GrowFromCenter(b))
        self.wait(2)

        self.play(b.animate.move_to(a.get_right()+RIGHT*2.3))

        arrow_2 = Arrow(a.get_right(), b.get_left(), stroke_width=5).set_color(GREY_D)

        self.play(ShowCreation(arrow_2), )
        self.wait(2)

        c1 = (
    RoundedRectangle(stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77).shift(RIGHT)
    
)

        text=Text("20, \'F\'", font=BOLD).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.1)
        c=VGroup(c1, text).scale(0.456).next_to(indexes[3], LEFT, buff=0.7)

        self.play(GrowFromCenter(c))
        self.wait(2)

        self.play(c.animate.move_to(b.get_right()+RIGHT*2.3))

        arrow_3 = Arrow(b.get_right(), c.get_left(), stroke_width=5).set_color(GREY_D)

        self.play(ShowCreation(arrow_3), )
        self.wait(2)



        #next position insertion

        d1 = (
    RoundedRectangle(stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("8, \'O\'", font=BOLD).set_color(BLACK).move_to(d1).set_z_index(1).scale(1.37)
        d=VGroup(d1, text).scale(0.456).next_to(indexes[3], LEFT, buff=0.7)

        self.play(GrowFromCenter(d))
        self.wait(2)

        arrow_4 = Arrow(rect1.get_center(), rect1.get_right()+RIGHT, stroke_width=5).set_color(GREY_D)

        self.play(ShowCreation(arrow_4), d.animate.move_to(rect1.get_right()+RIGHT*1.7))
        self.wait(2)


        e1 = (
    RoundedRectangle(stroke_width=30, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77).shift(RIGHT)
    
)

        text=Text("16, \'F\'", font=BOLD).set_color(BLACK).move_to(e1).set_z_index(1).scale(1.1)
        e=VGroup(e1, text).scale(0.456).next_to(indexes[3], LEFT, buff=0.7)

        self.play(GrowFromCenter(e))
        self.wait(2)

        self.play(e.animate.move_to(d.get_right()+RIGHT*2.3))

        arrow_5 = Arrow(d.get_right(), e.get_left(), stroke_width=5).set_color(GREY_D)

        self.play(ShowCreation(arrow_5), )
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT))

        #deletion animation

        self.wait(2)

        self.play(Indicate(b, color = "#FF0000"))

        self.wait(1)

        pointer = Arrow(c.get_right(), c.get_right()+RIGHT*1.1, stroke_width=3).set_color(PURE_RED)
        pointer.next_to(rect5, LEFT, buff=0.99)

        self.play(ShowCreation(pointer))
        self.wait(2)

        self.play(pointer.animate.next_to(a, UP, buff=0.5999).rotate(-PI/2))

        self.wait(2)

        self.play(pointer.animate.next_to(b, UP, buff=0.5999))

        self.wait(2)

        self.play(FadeOut(b), FadeOut(arrow_3),)

        arrow = always_redraw(lambda: Arrow(a.get_right(), c.get_left(), stroke_width=5).set_color(GREY_D))

        self.play(ReplacementTransform(arrow_2, arrow))
        self.wait(2)

        self.play(c.animate.move_to(b), FadeOut(pointer))

        self.wait(2)





        self.embed()

        self.wait(2)

