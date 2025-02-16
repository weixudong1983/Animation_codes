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
