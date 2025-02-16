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


