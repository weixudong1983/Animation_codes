from manimlib import *

class MatrixChainMultiplication(Scene):

    def construct(self):

        a = Text("A").scale(2.7).shift(LEFT*3.5+UP*2.3)
        b = Text("B").scale(2.7).next_to(a, RIGHT, buff=2.5)
        c = Text("C").scale(2.7).next_to(b, RIGHT, buff=2.5)

        self.play(ShowCreation(a), ShowCreation(b), ShowCreation(c))

        text1 = Text("10 x 30").next_to(a, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)
        text2 = Text("30 x 5").next_to(b, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)
        text3 = Text("5 x 60").next_to(c, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)

        self.play(ShowCreation(text1), ShowCreation(text2), ShowCreation(text3))

        self.wait(2)

        star1 = Text("*").scale(2).next_to(a, RIGHT, buff=0.7).shift(RIGHT*0.2)
        star2 = Text("*").scale(2).next_to(b, RIGHT, buff=0.7).shift(RIGHT*0.2)

        self.play(GrowFromCenter(star1), GrowFromCenter(star2))

        self.wait(2)



        brace1 = Brace(VGroup(text1, text2), DOWN, buff=0.66)
        brace2 = Brace(VGroup(text3), DOWN, buff=0.66)

        self.play(GrowFromCenter(brace1))
        self.wait()
        self.play(GrowFromCenter(brace2))

        self.wait(2)

        self.play(
            Transform(brace1, Brace(VGroup(text1), DOWN, buff=0.66)),
            Transform(brace2, Brace(VGroup(text2, text3), DOWN, buff=0.66)),
            )
        
        self.wait(2)
        self.play(FadeOut(VGroup(brace1, brace2)))
        self.wait(1)





        first = Text("A(BC) = 9000 + 18000").scale(1.2).shift(DOWN*2.6)
        self.play(ShowCreation(first[:6]))
        self.wait()

        self.play(GrowFromCenter(brace2))
        self.wait()
        temp = Text("30 x 5 x 60").next_to(brace2, DOWN, buff=0.6)
        
        self.play(
            TransformFromCopy(text2[0:2], temp[0:2]),
            FadeIn(temp[2]),
            TransformFromCopy(text2[-1] ,temp[3]), TransformFromCopy(text3[0], temp[3]),
            FadeIn(temp[4]),
            TransformFromCopy(text3[-2:], temp[5:])
            )
        
        self.wait(2)

        self.play(ReplacementTransform(temp, first[6:10]))
        self.wait(2)

        text4 = Text("30 x 60").scale(0.7).move_to(VGroup(text2, text3)).set_color(YELLOW)
        self.play(ReplacementTransform(VGroup(text2, text3), text4))
        self.wait(1)

        self.play(Transform(brace2, Brace(VGroup(text1, text3), DOWN, buff=0.7).shift(RIGHT*0.25)))
        self.wait(2)

        temp = Text("10 x 30 x 60").next_to(brace2, DOWN, buff=0.6)
        
        self.play(
            TransformFromCopy(text1[0:2], temp[0:2]),
            FadeIn(temp[2]),
            TransformFromCopy(text1[-2:] ,temp[3:5]), TransformFromCopy(text4[0:2], temp[3:5]),
            FadeIn(temp[5]),
            TransformFromCopy(text4[-2:], temp[6:])
            )
        
        self.wait(1)
        self.play(ReplacementTransform(temp, first[11:]), FadeIn(first[10]))

        text2 = Text("30 x 5").next_to(b, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)
        text3 = Text("5 x 60").next_to(c, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)

        self.play(FadeOut(brace2), FadeOut(text4),ShowCreation(text2), ShowCreation(text3))

        self.wait()

        second = Text("A(BC) = 27000").scale(1.4).move_to(first)
        self.play(TransformMatchingTex(first, second), run_time=0.5)

        self.play(second.animate.shift(UP*1.4))

        self.wait(2)

        first = Text("(AB)C = 4500").scale(1.4).next_to(second, DOWN, buff=0.7)
        self.play(Write(first))

        self.wait(2)

        rect = SurroundingRectangle(first, color=GREEN, stroke_width=9).scale(1.25)
        self.play(ShowCreation(rect))


        self.play(self.camera.frame.animate.shift(RIGHT*16))

        a = Text("A B C D").shift(RIGHT*16).scale(2.6)
        self.play(ShowCreation(a))
        self.wait(2)

        b = Text("((AB)C)D").scale(2.6).move_to(a)
        c = Text("(AB)(CD)").scale(2.6).move_to(b)
        d = Text("(A(BC))D").scale(2.6).move_to(c)
        e = Text("((AB)C)D").scale(2.6).move_to(d)
        f = Text("A((BC)D)").scale(2.6).move_to(e)
        g = Text("A(B(CD))").scale(2.6).move_to(f)


        self.play(TransformMatchingTex(a,b), run_time=0.5)
        self.wait()
        self.play(TransformMatchingTex(b,c), run_time=0.5)
        self.wait()

        self.play(TransformMatchingTex(c,d), run_time=0.5)
        self.wait()

        self.play(TransformMatchingTex(d,e), run_time=0.5)
        self.wait()

        self.play(TransformMatchingTex(e,f), run_time=0.5)

        self.wait()

        self.play(TransformMatchingTex(f,g), run_time=0.5)

        self.wait(3)


BLUE, YELLOW = YELLOW, BLUE


class MatrixMultiplication(Scene):

    def construct(self):

        self.camera.frame.shift(RIGHT*1.05+DOWN*0.5)
        
        matrix1 = Matrix([["a", "b", "c"], ["d", "e", "f"]]).shift(LEFT).scale(1.3)
        matrix2 = Matrix([["g", "h", ], ["i", "j", ], ["k", "l",]]).next_to(matrix1, RIGHT).shift(RIGHT).scale(1.3)

        self.play(Write(matrix1), Write(matrix2))
        self.wait(1)

        text_1 = Text("2 x 3").next_to(matrix1, DOWN).shift(DOWN*0.3).scale(0.77).set_color(BLUE)
        text_2 = Text("3 x 2").next_to(matrix2, DOWN).shift(DOWN*0.3).scale(0.77).set_color(BLUE)

        self.play(Write(text_1))
        self.wait(2)
        self.play(Write(text_2))
        self.wait(2)

        a = Circle(radius=0.37, stroke_width=7, color=RED).move_to(text_1[-1])
        b = Circle(radius=0.37, stroke_width=7, color=RED).move_to(text_2[0])
        self.play(ShowCreation(a))
        self.play(ShowCreation(b))
        self.wait(2)

        self.play(Uncreate(a), Uncreate(b), self.camera.frame.animate.shift(DOWN*1.36))

        self.wait()

        matrix3 = Matrix([["ag+bi+ck", "ah+bj+cl"], ["dg+ei+fk", "dh+ej+fl"]]).scale(1.3).shift(DOWN*4+RIGHT*1.17)
        self.play(Write(matrix3.get_brackets()))
        self.wait()

        text_3 = Text("2 x 2").next_to(matrix3, DOWN).shift(DOWN*0.1).scale(0.77).set_color(BLUE)
        self.play(TransformFromCopy(text_1[0], text_3[0]), TransformFromCopy(text_2[-1], text_3[2]), FadeIn(text_3[1]),
                  self.camera.frame.animate.scale(1.1).shift(DOWN*0.16))
        
        self.wait(2)

        final_rect = SurroundingRectangle(matrix3.get_entries()[0],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)
        self.play(ShowCreation(final_rect))

        self.wait(2)

        row_rect = SurroundingRectangle(matrix1.get_rows()[0], 
                                                 color=YELLOW, 
                                                 buff=0.1).scale(1.07)
        
        col_rect = SurroundingRectangle(matrix2.get_columns()[0],
                                                 color=GREEN, 
                                                 buff=0.1).scale(1.07)
        
        self.play(ShowCreation(row_rect), ShowCreation(col_rect))

        self.wait(1)


        self.play(
            TransformFromCopy(matrix1.get_entries()[0], matrix3.get_entries()[0][0]),
            TransformFromCopy(matrix2.get_entries()[0], matrix3.get_entries()[0][1]),
            
            TransformFromCopy(matrix1.get_entries()[1], matrix3.get_entries()[0][3]),
            TransformFromCopy(matrix2.get_entries()[2], matrix3.get_entries()[0][4]),
            
            TransformFromCopy(matrix1.get_entries()[2], matrix3.get_entries()[0][6]),
            TransformFromCopy(matrix2.get_entries()[4], matrix3.get_entries()[0][7]),

            FadeIn(matrix3.get_entries()[0][2]),

            FadeIn(matrix3.get_entries()[0][5])

            
            )
        
        self.wait(2)

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[1],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.wait()

        self.play(Transform(col_rect, SurroundingRectangle(matrix2.get_columns()[1], color=GREEN).scale(1.07)))
        self.wait(1)


        self.play(
            TransformFromCopy(matrix1.get_entries()[0], matrix3.get_entries()[1][0]),
            TransformFromCopy(matrix2.get_entries()[1], matrix3.get_entries()[1][1]),
            
            TransformFromCopy(matrix1.get_entries()[1], matrix3.get_entries()[1][3]),
            TransformFromCopy(matrix2.get_entries()[3], matrix3.get_entries()[1][4]),
            
            TransformFromCopy(matrix1.get_entries()[2], matrix3.get_entries()[1][6]),
            TransformFromCopy(matrix2.get_entries()[5], matrix3.get_entries()[1][7]),

            FadeIn(matrix3.get_entries()[1][2]),

            FadeIn(matrix3.get_entries()[1][5])

            
            )
        
        self.wait(2)

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[2],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.wait()

        self.play(
            Transform(col_rect, SurroundingRectangle(matrix2.get_columns()[0], color=GREEN).scale(1.07)),
            Transform(row_rect, SurroundingRectangle(matrix1.get_rows()[1], color=YELLOW).scale(1.07))
            
            )
        self.wait(1)


        self.play(
            TransformFromCopy(matrix1.get_entries()[3], matrix3.get_entries()[2][0]),
            TransformFromCopy(matrix2.get_entries()[0], matrix3.get_entries()[2][1]),
            
            TransformFromCopy(matrix1.get_entries()[4], matrix3.get_entries()[2][3]),
            TransformFromCopy(matrix2.get_entries()[2], matrix3.get_entries()[2][4]),
            
            TransformFromCopy(matrix1.get_entries()[5], matrix3.get_entries()[2][6]),
            TransformFromCopy(matrix2.get_entries()[4], matrix3.get_entries()[2][7]),

            FadeIn(matrix3.get_entries()[2][2]),

            FadeIn(matrix3.get_entries()[2][5])

            
            )
        

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[3],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        

        self.play(
            Transform(col_rect, SurroundingRectangle(matrix2.get_columns()[1], color=GREEN).scale(1.07)),
            Transform(row_rect, SurroundingRectangle(matrix1.get_rows()[1], color=YELLOW).scale(1.07))
            
            )
        self.wait()


        self.play(
            TransformFromCopy(matrix1.get_entries()[3], matrix3.get_entries()[3][0]),
            TransformFromCopy(matrix2.get_entries()[1], matrix3.get_entries()[3][1]),
            
            TransformFromCopy(matrix1.get_entries()[4], matrix3.get_entries()[3][3]),
            TransformFromCopy(matrix2.get_entries()[3], matrix3.get_entries()[3][4]),
            
            TransformFromCopy(matrix1.get_entries()[5], matrix3.get_entries()[3][6]),
            TransformFromCopy(matrix2.get_entries()[5], matrix3.get_entries()[3][7]),

            FadeIn(matrix3.get_entries()[3][2]),

            FadeIn(matrix3.get_entries()[3][5])

            
            )
        
        self.wait()

        self.play(
            Uncreate(row_rect), Uncreate(col_rect),
                  self.camera.frame.animate.shift(RIGHT*1.7)
                  )
        
        self.wait()

        self.play(Indicate(final_rect))

        text = Text("3").next_to(matrix2, RIGHT, buff=0.8).scale(1.7).shift(RIGHT*2.88+DOWN)
        self.play(Write(text))

        self.wait(1)

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[2],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        
        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[1],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[0],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.wait()

        
        text1 = Text("3 * 4").scale(1.7).move_to(text)

        self.play(TransformMatchingTex(text, text1), run_time=0.5)

        self.wait()

        text = Text("12").scale(1.7).move_to(text)
        self.play(TransformMatchingTex(text1, text), Uncreate(final_rect),run_time=0.5)

        self.wait(1)

        rect_1 = SurroundingRectangle(text_1, color=RED).scale(1.1)
        rect_2 = SurroundingRectangle(text_2, color=RED).scale(1.1)
       
        self.play(ShowCreation(rect_1), ShowCreation(rect_2))

        self.wait()

        text11 = Text("2 * 3 * 2").scale(1.2).next_to(text, DOWN, buff=0.9).shift(RIGHT*0.2)

        self.play(TransformFromCopy(text_1[0], text11[0]), FadeIn(text11[1]))
        self.wait(1)
        self.play(TransformFromCopy(text_1[2], text11[2]), FadeIn(text11[3]))
        self.wait(1)
        self.play(TransformFromCopy(text_2[-1], text11[-1]))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*16.8))

        a = Text("A").scale(4).shift(RIGHT*16)
        b = Text("B").scale(4).next_to(a, RIGHT, buff=0.8).shift(RIGHT*3.8)

        self.play(ShowCreation(a), ShowCreation(b))

        text1 = Text("p x q").next_to(a, DOWN+RIGHT).set_color(BLUE)
        text2 = Text("q x r").next_to(b, DOWN+RIGHT).set_color(BLUE)

        self.play(ShowCreation(text1), ShowCreation(text2))
        self.wait(2)

        star = Text("*").scale(3).next_to(a, RIGHT).shift(RIGHT*1.5)
        self.play(ShowCreation(star))

        self.wait(2)


        dimention = Text("p x r").next_to(text1, DOWN, buff=0.7).scale(1.4).shift(DOWN*0.7+LEFT*1.8)

        self.play(TransformFromCopy(text1[0], dimention[0]))
        self.play(FadeIn(dimention[1]))
        self.play(TransformFromCopy(text2[-1], dimention[-1]))
        self.wait(2)

        rect = SurroundingRectangle(dimention, color=PINK, stroke_width=8).scale(1.3)
        self.play(ShowCreation(rect))
        rect_text = Text("Dimention").next_to(rect, RIGHT, buff=1.4)
        self.play(Write(rect_text))
        self.wait(2)



        final = Text("p x q x r").next_to(text1, DOWN).shift(DOWN*2+RIGHT*2).scale(1.2).shift(LEFT*3.9+DOWN)


        self.play(TransformFromCopy(text1[0], final[0]))
        self.play(FadeIn(final[1]))

        self.play(TransformFromCopy(text1[2], final[2]), TransformFromCopy(text2[0], final[2]))
        self.play(FadeIn(final[3]))

        self.play(TransformFromCopy(text2[-1], final[-1]))

        rect = SurroundingRectangle(final, color=PINK, stroke_width=7).scale(1.35)
        self.play(ShowCreation(rect))
        self.wait()

        rect_text = Text("Number of Operations").scale(0.9).next_to(rect, RIGHT, buff=0.5)
        self.play(Write(rect_text))


        self.wait(2)
