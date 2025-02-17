from manimlib import *


class Compression(Scene):

    def construct(self):
        self.camera.frame.shift(UP*0.22)
        
        # Add a title
        title = Text("Data Compression").set_color(BLACK)
        title.scale(1.5)
        title.to_edge(UP).shift(DOWN*0.2)
        self.play(Write(title))
        self.wait(2)

        a1 = (
    RoundedRectangle(stroke_width=40, fill_opacity=1)
    .set_fill(BLUE, opacity=1)      # Fully opaque fill
    .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    .shift(LEFT * 3 + DOWN * 0.5)
)

        text=Text("Data", font=BOLD).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).shift(LEFT)
        self.play(GrowFromCenter(a))
        data_text = Text("100 MB").set_color(BLACK).next_to(a, DOWN, buff=1)
        self.play(Write(data_text))

        position = VGroup(a, data_text).get_center()


        hash_1 = Circle(radius=0.77, stroke_width=40).set_fill(RED, opacity=1).set_stroke(RED, opacity=0.6).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("C").set_color(BLACK).scale(1.4).move_to(hash_1)
        hash = VGroup(hash_1, hash_2).set_z_index(2)
        self.play(GrowFromCenter(hash))


        arrow4 = Arrow(a.get_right(), hash.get_left(), stroke_width=5).set_color(BLACK)

        self.play(GrowArrow(arrow4))

        self.wait()


        temp = a.copy().next_to(hash, RIGHT, buff=1.7).scale(0.5)     

        temp_a = VGroup(data_text, a).copy()

        self.play(FadeOut(a), FadeOut(arrow4) ,FadeOut(data_text) ,VGroup(a, data_text).animate.scale(0.00000000001).move_to(hash))

        arrow5 = Arrow(hash.get_right(), temp.get_left()+LEFT*0.05, stroke_width=5).set_color(BLACK)
        self.wait(1)

        self.play(GrowArrow(arrow5),GrowFromCenter(temp) )
        temp_text = Text("70 MB").set_color(BLACK).next_to(temp, DOWN, buff=0.7).scale(0.8)
        self.play(Write(temp_text))
        self.wait(2)

        self.play(hash[1].animate.become(Tex(r"C^{-1}", stroke_width=2).move_to(hash).set_color(BLACK).scale(1.4)),
                  )

        self.play(arrow5.animate.rotate(PI))
        self.wait()
        self.play(VGroup(temp, temp_text).animate.scale(0.000000001).move_to(hash),FadeOut(arrow5) )

        arrow4 = arrow4.rotate(PI)
        self.play(GrowArrow(arrow4),)
        self.play(Transform(a, temp_a))
        self.play(VGroup(a, hash, arrow4, data_text).animate.shift(RIGHT*1.87))

        self.wait(2)

        title1 = Text("Lossless Compression").set_color(BLACK)
        title1.scale(1.5).move_to(title)    
        self.play(TransformMatchingTex(title, title1), run_time=0.5)
        

        self.wait(2)


class Naive_Compression(Scene):

    def construct(self):
        
        text = Text("BANANA BANDANA").scale(1.9).set_color(BLACK).shift(UP*2)
        self.play(ShowCreation(text))

        self.wait(1)

        brace = Brace(text, DOWN, stroke_width=3).set_color(BLACK).shift(DOWN*0.1)
        self.play(GrowFromCenter(brace))
        temp = Text("14").set_color(BLACK).next_to(brace, DOWN, buff=0.8).scale(1.2)
        self.play(Write(temp))
        self.wait(2)

        temp1 = Text("14 * 8").set_color(BLACK).next_to(brace, DOWN, buff=0.8).scale(1.2)
        self.play(TransformMatchingTex(temp, temp1), run_time=0.5)

        self.wait()

        temp = Text("112 bits").set_color(BLACK).next_to(brace, DOWN, buff=0.8).scale(1.2)
        self.play(TransformMatchingTex(temp1, temp), run_time=0.5)

        self.wait(2)



        self.play(FadeOut(brace), FadeOut(temp), self.camera.frame.animate.shift(DOWN*0.7)) 

        a = Text("A : 000").set_color(BLACK).next_to(text[5], DOWN, buff=1)
        b = Text("B : 001").set_color(BLACK).next_to(a, DOWN, buff=0.5)
        n = Text("N : 010").set_color(BLACK).next_to(b, DOWN, buff=0.5)
        d = Text("D : 100").set_color(BLACK).next_to(n, DOWN, buff=0.5)
        space = Text("- : 101").set_color(BLACK).next_to(d, DOWN, buff=0.5)
        self.play(Write(VGroup(a[0],b[0],n[0],d[0],space[0])))
        self.wait(2)

        brace = Brace(VGroup(a[0],b[0],n[0],d[0],space[0]), RIGHT, buff=1, stroke_width=3).set_color(BLACK)
        self.play(GrowFromCenter(brace))
        temp = Text("5").set_color(BLACK).next_to(brace, RIGHT, buff=0.8).scale(1.7)
        self.play(Write(temp))

        self.wait(2)

        self.play(FadeOut(brace), FadeOut(temp), FadeOut(VGroup(a[0],b[0],n[0],d[0],space[0])))    

        self.wait(1)

        

        temp = Text("""
                    
        1 bit :  0, 1
                    
        2 bits : 00, 01, 10, 11
                    
        3 bits : 000, 001, 010, 011, 
                 100, 101, 110, 111""").set_color(BLACK).shift(RIGHT*0.3+DOWN*1.77)
        self.play(Write(temp[:8]))
        self.wait(2)
        self.play(Write(temp[8:25]))
        self.wait(2)
        self.play(Write(temp[25:]))

        self.wait(2)

        self.play(FadeOut(temp), FadeIn(VGroup(a[0],b[0],n[0],d[0],space[0])))
        self.wait(1)

        self.play(FadeIn(VGroup(a[1],b[1],n[1],d[1],space[1])))

        self.play(Write(a[2:]))
        self.wait(2)
        self.play(Write(b[2:]))
        self.wait(2)
        self.play(Write(n[2:]), Write(d[2:]), Write(space[2:]))
        self.play(VGroup(a,b,n,d,space).animate.shift(RIGHT))

        self.wait(2)

        temp_b = b[2:].copy()
        temp_a = a[2:].copy()
        temp_n = n[2:].copy()
        temp_a2 = a[2:].copy()
        temp_n2 = n[2:].copy()
        temp_a3 = a[2:].copy()
        temp_b2 = b[2:].copy()
        temp_a4 = a[2:].copy()
        temp_n3 = n[2:].copy()
        temp_d = d[2:].copy()
        temp_a5 = a[2:].copy()
        temp_n4 = n[2:].copy()
        temp_a6 = a[2:].copy()
        temp_space = space[2:].copy()

        self.play(temp_b.animate.next_to(text[0], DOWN).scale(0.5))
        self.wait(2)
        self.play(temp_a.animate.next_to(text[1], DOWN).scale(0.5))
        self.wait(1)
        self.play(
            temp_n.animate.next_to(text[2], DOWN).scale(0.5),
            temp_a2.animate.next_to(text[3], DOWN).scale(0.5),
            temp_n2.animate.next_to(text[4], DOWN).scale(0.5),
            temp_a3.animate.next_to(text[5], DOWN).scale(0.5),
            temp_b2.animate.next_to(text[6], DOWN).scale(0.5),
            temp_a4.animate.next_to(text[7], DOWN).scale(0.5),
            temp_a5.animate.next_to(text[10], DOWN).scale(0.5),
            temp_n3.animate.next_to(text[8], DOWN).scale(0.5),

            temp_d.animate.next_to(text[9], DOWN).scale(0.5),
            temp_n4.animate.next_to(text[11], DOWN).scale(0.5),
            temp_a6.animate.next_to(text[12], DOWN).scale(0.5),
            temp_space.animate.next_to(text[5], DOWN).scale(0.5).shift(RIGHT*0.8),
                
            VGroup(a,b,n,d,space).animate.shift(DOWN*0.36),

                  )
        
        self.wait(1)
        self.play(FadeOut(VGroup(a,b,n,d,space)), )

        brace = Brace(VGroup(temp_a,temp_b,temp_n,temp_d,temp_space, temp_a6), DOWN, buff=0.77, stroke_width=3).set_color(BLACK)
        self.play(GrowFromCenter(brace))

        temp = Text("14").set_color(BLACK).next_to(brace, DOWN, buff=0.8).scale(1.7)
        self.play(Write(temp))
        self.wait(2)
        temp1 = Text("14 * 3").set_color(BLACK).next_to(brace, DOWN, buff=0.8).scale(1.7)
        self.play(TransformMatchingTex(temp, temp1), run_time=0.5)
        self.wait()
        temp = Text("42 bits").set_color(BLACK).next_to(brace, DOWN, buff=0.8).scale(1.7)
        self.play(TransformMatchingTex(temp1, temp), run_time=0.5)

        self.wait(2)

        self.play(temp.animate.shift(LEFT*4).scale(0.64).shift(LEFT*0.5), Uncreate(brace))

        self.play(FadeIn(VGroup(a,b,n,d,space)))
        self.play(VGroup(a,b,n,d,space).animate.shift(RIGHT*4))

        self.wait()

        brace_left = Brace(VGroup(a,b,n,d,space), LEFT, buff=0.5, stroke_width=3).set_color(BLACK)
        self.play(GrowFromCenter(brace_left))  

        temp_ = Text("5").set_color(BLACK).next_to(brace_left, LEFT, buff=0.8).scale(1.1)
        self.play(Write(temp_)) 
        temp1 = Text("5 * (8 + 3)").set_color(BLACK).next_to(brace_left, LEFT, buff=0.8).scale(1.1)
        self.play(TransformMatchingTex(temp_, temp1), run_time=0.5)
        self.wait()
        temp_ = Text("55 bits").set_color(BLACK).next_to(brace_left, LEFT, buff=0.8).scale(1.1)
        self.play(TransformMatchingTex(temp1, temp_), run_time=0.5)
        self.play(temp_.animate.shift(LEFT*4), Uncreate(brace_left),
                  VGroup(a,b,n,d,space).animate.shift(LEFT*2))
        
        self.wait(2)

        temp2 = Text("97 bits").set_color(BLACK).next_to(temp, RIGHT, buff=0.5).scale(1.4).shift(LEFT*2+DOWN*0.5)
        self.play(ReplacementTransform(VGroup(temp, temp_), temp2))

        rect = SurroundingRectangle(temp2, color="#0000FF", stroke_width=10).scale(1.3)
        self.play(ShowCreation(rect)) 

        self.wait(2)


class Hufflman_Compression(Scene):

    def construct(self):
        self.camera.frame.shift(DOWN*0.8)
        
        text = Text("BANANA BANDANA").scale(1.9).set_color(BLACK).shift(UP*2)
        self.play(ShowCreation(text))

        self.wait(1)

        a = Text("A : 6").set_color(BLACK).next_to(text[5], DOWN, buff=1)
        b = Text("B : 2").set_color(BLACK).next_to(a, DOWN, buff=0.5)
        n = Text("N : 4").set_color(BLACK).next_to(b, DOWN, buff=0.5)
        d = Text("D : 1").set_color(BLACK).next_to(n, DOWN, buff=0.5)
        space = Text("- : 1").set_color(BLACK).next_to(d, DOWN, buff=0.5)
        self.play(Write(VGroup(a[0],b[0],n[0],d[0],space[0])))
        self.wait(2)

        self.play(FadeIn(VGroup(a[1],b[1],n[1],d[1],space[1])))
        self.play(Write(VGroup(a[2], b[2], n[2], d[2], space[2])))
        self.wait(2)

        a1 = Text("0").set_color(BLACK).next_to(a, RIGHT, buff=1.2)
        b1 = Text("01").set_color(BLACK).next_to(b, RIGHT, buff=1.2)
        n1 = Text("11").set_color(BLACK).next_to(n, RIGHT, buff=1.2)
        d1 = Text("100").set_color(BLACK).next_to(d, RIGHT, buff=1.2)
        e1 = Text("101").set_color(BLACK).next_to(space, RIGHT, buff=1.2)
        
        self.play(ShowCreation(a1))
        self.wait(2)
        self.play(ShowCreation(b1))
        self.wait(2)

        self.play(ShowCreation(n1))
        self.play(ShowCreation(d1))
        self.play(ShowCreation(e1))

        self.wait(2)

        self.play(VGroup(a,b,n,d,space, a1,b1,n1, d1, e1).animate.shift(RIGHT*3))

        self.wait(1)

        brace = Brace(text[:3], DOWN, buff=0.44, stroke_width=3.4).set_color(BLACK)
        self.play(GrowFromCenter(brace))

        ban = Text("01011").set_color(BLACK).next_to(brace, DOWN, buff=0.4)
        
        self.wait()
        self.play(TransformFromCopy(b1, ban[:2]))
        self.wait(2)
        self.play(TransformFromCopy(a1, ban[2]))
        self.wait(1)
        self.play(TransformFromCopy(n1, ban[3:]))
        self.wait(2)

        self.play(ban[:2].animate.set_color("#FF0000"))
        rect = SurroundingRectangle(b1, color="#0000FF", stroke_width=7).scale(1.3)
        self.play(ShowCreation(rect))
        self.wait(2)
        self.play(ban[1].animate.set_color(BLACK))
        self.play(Transform(rect, SurroundingRectangle(a1, color="#0000FF", stroke_width=7).scale(1.3)))
        self.wait(2)
        self.play(ban[0].animate.set_color(BLACK),
                  ban[1:4].animate.set_color("#FF0000")
                  )
        self.play(Transform(rect, SurroundingRectangle(e1, color="#0000FF", stroke_width=7).scale(1.3)))

        self.wait(2)

        self.play(FadeOut(Group(rect, brace, ban, a1,b1,n1,d1,e1)),
                          VGroup(a,b,n,d,space).animate.shift(RIGHT*2.2)
                          )
        
        self.wait(2)

        RED = BLUE
        RED_E = BLUE_E

        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=6).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("-").set_color(BLACK).scale(1.4).move_to(hash_1)
        circle = VGroup(hash_1, hash_2).shift(LEFT*12+DOWN*3).scale(0.7).shift(LEFT*1.7+DOWN*0.45)

        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=6).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("D").set_color(BLACK).scale(1.55).move_to(hash_1)
        circle1 = VGroup(hash_1, hash_2).scale(0.7).next_to(circle, RIGHT, buff=0.7)

        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=6).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("B").set_color(BLACK).scale(1.55).move_to(hash_1)
        circle2 = VGroup(hash_1, hash_2).scale(0.7).next_to(circle1, RIGHT, buff=0.7)

        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=1).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("N").set_color(BLACK).scale(1.55).move_to(hash_1)
        circle3 = VGroup(hash_1, hash_2).scale(0.7).next_to(circle2, RIGHT, buff=0.7)

        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=1).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("A").set_color(BLACK).scale(1.55).move_to(hash_1)
        circle4 = VGroup(hash_1, hash_2).scale(0.7).next_to(circle3, RIGHT, buff=0.7)

        self.play(GrowFromCenter(circle4[0]), GrowFromCenter(circle3[0]), GrowFromCenter(circle2[0]), GrowFromCenter(circle[0]), GrowFromCenter(circle1[0]))
        self.play(
            TransformFromCopy(space[0], circle[1]),
            TransformFromCopy(d[0], circle1[1]),
            TransformFromCopy(b[0], circle2[1]),
            TransformFromCopy(n[0], circle3[1]),
            TransformFromCopy(a[0], circle4[1]),
        )

        temp1 = a[2].copy().next_to(circle4, DOWN).shift(DOWN*0.08)
        temp2 = b[2].copy().next_to(circle2, DOWN).shift(DOWN*0.08)
        temp3 = n[2].copy().next_to(circle3, DOWN).shift(DOWN*0.08)
        temp4 = d[2].copy().next_to(circle1, DOWN).shift(DOWN*0.08)
        temp5 = space[2].copy().next_to(circle, DOWN).shift(DOWN*0.08)

        self.play(
              TransformFromCopy(space[2], temp5),
              TransformFromCopy(d[2], temp4),
              TransformFromCopy(b[2], temp2),
              TransformFromCopy(n[2], temp3),
              TransformFromCopy(a[2], temp1),

        )

        self.wait()

        self.play(FadeOut(text))

        self.wait()


        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=1).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("2").set_color(BLACK).scale(1.55).move_to(hash_1)
        circle5 = VGroup(hash_1, hash_2).scale(0.7).next_to(VGroup(circle, circle1), UP, buff=0.7)

        self.play(GrowFromCenter(circle5[0]))
        edge_1 = always_redraw(lambda: Line(circle.get_center(), circle5.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        edge_2 = always_redraw(lambda: Line(circle1.get_center(), circle5.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        self.play(GrowArrow(edge_1), GrowArrow(edge_2))
        self.play(TransformFromCopy(VGroup(temp5, temp4), circle5[1]))

        self.wait(2)

        arrow = Arrow(circle5.get_right(), circle5.get_right()+RIGHT*1.8, stroke_width=7).set_color("#FF0000").rotate(PI)
        self.play(GrowArrow(arrow))
        self.wait(2)

        self.play(arrow.animate.rotate(PI/2).next_to(circle2, UP))
        self.play(arrow.animate.next_to(circle3, UP))
        self.play(arrow.animate.next_to(circle4, UP))
        self.wait()

        self.play(Uncreate(arrow))


        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=1).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("4").set_color(BLACK).scale(1.55).move_to(hash_1)
        circle6 = VGroup(hash_1, hash_2).scale(0.7).next_to(VGroup(circle1, circle2), UP, buff=1.4).shift(UP+LEFT*0.8)

        self.play(GrowFromCenter(circle6[0]))
        edge_3 = always_redraw(lambda: Line(circle5.get_center(), circle6.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        edge_4 = always_redraw(lambda: Line(circle2.get_center(), circle6.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        self.play(GrowArrow(edge_3), GrowArrow(edge_4))
        self.play(TransformFromCopy(VGroup(temp2, circle5[1]), circle6[1]))

        self.wait(1)

        arrow = Arrow(circle6.get_right(), circle6.get_right()+RIGHT*1.6, stroke_width=7).set_color("#FF0000").rotate(PI)
        self.play(GrowArrow(arrow))
        self.wait()

        self.play(arrow.animate.rotate(PI/2).next_to(circle3, UP))
        self.play(arrow.animate.next_to(circle4, UP))
        self.wait()
        self.play(Uncreate(arrow))


        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=1).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("8").set_color(BLACK).scale(1.55).move_to(hash_1)
        circle7 = VGroup(hash_1, hash_2).scale(0.7).next_to(circle6, UP, buff=0.7).shift(RIGHT)

        self.play(GrowFromCenter(circle7[0]))
        edge_5 = always_redraw(lambda: Line(circle6.get_center(), circle7.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        edge_6 = always_redraw(lambda: Line(circle3.get_center(), circle7.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        self.play(GrowArrow(edge_5), GrowArrow(edge_6))
        self.play(TransformFromCopy(VGroup(temp3, circle6[1]), circle7[1]))

        self.wait(1)

        self.play(self.camera.frame.animate.scale(1.2).shift(UP*0.6),
                  VGroup(a,b,n,d,space).animate.shift(RIGHT+UP*0.1).scale(1.2))
        

        self.wait(1)

        hash_1 = Circle(radius=0.77, stroke_width=10).set_fill(RED, opacity=1).set_stroke(RED_E, opacity=1).move_to(a.get_right() + RIGHT*3.02)
        hash_2 = Text("14").set_color(BLACK).scale(1.39).move_to(hash_1)
        circle8 = VGroup(hash_1, hash_2).scale(0.7).next_to(circle7, UP, buff=0.7).shift(RIGHT)

        self.play(GrowFromCenter(circle8[0]))
        edge_7 = always_redraw(lambda: Line(circle7.get_center(), circle8.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        edge_8 = always_redraw(lambda: Line(circle4.get_center(), circle8.get_center(), stroke_width=7, color=GREY_E).set_z_index(-1))
        self.play(GrowArrow(edge_7), GrowArrow(edge_8))
        self.play(TransformFromCopy(VGroup(temp1, circle7[1]), circle8[1]))

        self.play(FadeOut(VGroup(temp1, temp2, temp3, temp4, temp5)))

        self.play(self.camera.frame.animate.shift(UP*0.6),
                  VGroup(a,b,n,space,d).animate.shift(UP+LEFT))
        

        self.play(
            circle2.animate.next_to(circle5, RIGHT, buff=0.86),
            circle3.animate.next_to(circle6, RIGHT, buff=0.86),
            circle4.animate.next_to(circle7, RIGHT, buff=0.86),
            )
        
        self.wait(2)

        temp_1_1 = Text("1").set_color(BLACK).move_to(edge_1.get_center()).shift(LEFT*0.5+UP*0.2)
        temp_1_2 = Text("1").set_color(BLACK).move_to(edge_3.get_center()).shift(LEFT*0.5+UP*0.2)
        temp_1_3 = Text("1").set_color(BLACK).move_to(edge_5.get_center()).shift(LEFT*0.5+UP*0.2)
        temp_1_4 = Text("1").set_color(BLACK).move_to(edge_7.get_center()).shift(LEFT*0.5+UP*0.2)

        self.play(FadeIn(VGroup(temp_1_1, temp_1_2, temp_1_3, temp_1_4)))

        self.wait(2)
        
        temp_0_1 = Text("0").set_color(BLACK).move_to(edge_2.get_center()).shift(RIGHT*0.4+UP*0.2)
        temp_0_2 = Text("0").set_color(BLACK).move_to(edge_4.get_center()).shift(RIGHT*0.4+UP*0.2)
        temp_0_3 = Text("0").set_color(BLACK).move_to(edge_6.get_center()).shift(RIGHT*0.4+UP*0.2)
        temp_0_4 = Text("0").set_color(BLACK).move_to(edge_8.get_center()).shift(RIGHT*0.4+UP*0.2)

        self.play(FadeIn(VGroup(temp_0_1, temp_0_2, temp_0_3, temp_0_4)))


        self.wait(2)

        temp_circle = Circle(color="#FF0000", stroke_width=11).scale(0.55).move_to(circle8).set_color("#FF0000")
        self.play(ShowCreation(temp_circle))

        temp_line = Line(circle8.get_center(), circle4.get_center(), stroke_width=10).set_color("#FF0000").set_z_index(-1)
        self.play(ShowCreation(temp_line))

        temp_circle1 = Circle(color="#FF0000", stroke_width=11).scale(0.55).move_to(circle4).set_color("#FF0000")
        self.play(ShowCreation(temp_circle1))

        self.wait()

        a1 = Text("0").set_color(BLACK).next_to(a, RIGHT, buff=1.2).scale(1.2)
        b1 = Text("110").set_color(BLACK).next_to(b, RIGHT, buff=1.2).scale(1.2)
        n1 = Text("10").set_color(BLACK).next_to(n, RIGHT, buff=1.2).scale(1.2)
        d1 = Text("1110").set_color(BLACK).next_to(d, RIGHT, buff=1.2).scale(1.2)
        e1 = Text("1111").set_color(BLACK).next_to(space, RIGHT, buff=1.2).scale(1.2)

        self.play(TransformFromCopy(temp_0_4, a1))

        self.play(Uncreate(temp_line), Uncreate(temp_circle), Uncreate(temp_circle1))

        self.wait(1)

        temp_circle = Circle(color="#FF0000", stroke_width=11).scale(0.55).move_to(circle8).set_color("#FF0000")
        self.play(ShowCreation(temp_circle))

        temp_line = Line(circle8.get_center(), circle7.get_center(), stroke_width=10).set_color("#FF0000").set_z_index(-1)
        self.play(ShowCreation(temp_line))

        temp_circle1 = Circle(color="#FF0000", stroke_width=11).scale(0.55).move_to(circle7).set_color("#FF0000")
        self.play(ShowCreation(temp_circle1))
        
        temp_line1 = Line(circle7.get_center(), circle6.get_center(), stroke_width=10).set_color("#FF0000").set_z_index(-1)
        self.play(ShowCreation(temp_line1))

        temp_circle2 = Circle(color="#FF0000", stroke_width=11).scale(0.55).move_to(circle6).set_color("#FF0000")
        self.play(ShowCreation(temp_circle2))
        
        temp_line2 = Line(circle6.get_center(), circle2.get_center(), stroke_width=10).set_color("#FF0000").set_z_index(-1)
        self.play(ShowCreation(temp_line2))

        temp_circle3 = Circle(color="#FF0000", stroke_width=11).scale(0.55).move_to(circle2).set_color("#FF0000")
        self.play(ShowCreation(temp_circle3))

        self.wait()

        self.play(
           
           TransformFromCopy(temp_1_4, b1[0]),
           TransformFromCopy(temp_1_3, b1[1]),
           TransformFromCopy(temp_0_2, b1[2]),

        )

        self.play(FadeOut(VGroup(temp_circle, temp_circle1, temp_circle2, temp_circle3,)),
                  Uncreate(temp_line), Uncreate(temp_line1), Uncreate(temp_line2))
        
        self.play(FadeIn(VGroup(n1, d1, e1)))

        self.wait(2)

        self.remove(circle, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8,
                    edge_1, edge_2, edge_3, edge_4, edge_5, edge_6, edge_7, edge_8,
                    temp_0_1, temp_0_2, temp_0_3, temp_0_4, temp_1_1, temp_1_2, temp_1_3, temp_1_4)
        
        text.shift(UP*2).scale(1.3)
        self.play(FadeIn(text), VGroup(a,b,n,d,space, a1,b1,n1,d1,e1).animate.shift(LEFT*0.5+DOWN*0.5))
        

        temp_b = b1.copy()
        temp_a = a1.copy()
        temp_n = n1.copy()
        temp_a2 = a1.copy()
        temp_n2 = n1.copy()
        temp_a3 = a1.copy()
        temp_b2 = b1.copy()
        temp_a4 = a1.copy()
        temp_n3 = n1.copy()
        temp_d = d1.copy()
        temp_a5 = a1.copy()
        temp_n4 = n1.copy()
        temp_a6 = a1.copy()
        temp_space = e1.copy()

        self.play(temp_b.animate.next_to(text[0], DOWN).scale(0.5))
        self.wait()
        self.play(temp_a.animate.next_to(text[1], DOWN).scale(0.5))
        self.wait()
        self.play(
            temp_n.animate.next_to(text[2], DOWN).scale(0.5),
            temp_a2.animate.next_to(text[3], DOWN).scale(0.5),
            temp_n2.animate.next_to(text[4], DOWN).scale(0.5),
            temp_a3.animate.next_to(text[5], DOWN).scale(0.5),
            temp_b2.animate.next_to(text[6], DOWN).scale(0.5),
            temp_a4.animate.next_to(text[7], DOWN).scale(0.5),
            temp_a5.animate.next_to(text[10], DOWN).scale(0.5),
            temp_n3.animate.next_to(text[8], DOWN).scale(0.5),

            temp_d.animate.next_to(text[9], DOWN).scale(0.5),
            temp_n4.animate.next_to(text[11], DOWN).scale(0.5),
            temp_a6.animate.next_to(text[12], DOWN).scale(0.5),
            temp_space.animate.next_to(text[5], DOWN).scale(0.5).shift(RIGHT),
                
        
                  )
        




        self.wait(3)

        brace = Brace(VGroup(temp_b, temp_a6), stroke_width=3.5, buff=0.4).set_color(RED_E)
        self.play(GrowFromCenter(brace))
        temp = Text("28 Bits").set_color(BLACK).next_to(brace, DOWN).shift(DOWN*0.25)
        self.play(Write(temp))
        self.wait(1)

        self.play(temp.animate.shift(LEFT*6), FadeOut(brace))

        self.wait(2)

        self.play(FadeOut(VGroup(a[2], b[2], n[2], d[2], space[2])),
                  VGroup(a1, b1, n1, d1, e1).animate.shift(LEFT*1.4)
                  )
        
        self.wait(2)

        brace = Brace(VGroup(a,space), LEFT, buff=0.4, stroke_width=3.4).set_color(RED_E)
        self.play(GrowFromCenter(brace))
        temp_1 = Text("54 Bits").set_color(BLACK).next_to(brace, LEFT).shift(LEFT*0.25)
        self.play(Write(temp_1))

        self.wait(2)

        final = Text("82 Bits").set_color(BLACK).shift(LEFT*3+DOWN).scale(1.8)
        
        self.play(ReplacementTransform(VGroup(temp, temp_1), final), FadeOut(brace))

        rect = SurroundingRectangle(final, color="#0000FF", stroke_width=9).scale(1.3)
        self.play(ShowCreation(rect))

        self.wait(2)
