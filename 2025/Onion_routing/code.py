from manimlib import *


class TOR1(Scene):

    def construct(self):
        self.camera.frame.shift(DOWN*0.15)

        server = ImageMobject("server.png").shift(RIGHT*5+DOWN*1.66)
        dns = ImageMobject("dns.png").scale(0.7).shift(UP*2+RIGHT*0.34)
        laptop = ImageMobject("computer.png").scale(0.62).shift(LEFT*4.4 + DOWN*1.9)
        self.add(laptop)

        self.add(dns)

        self.add(server)

        dns_text = Text("DNS Server").next_to(dns, DOWN).scale(0.72)
        yt_server = Text("YT Server").next_to(server, UP, buff=0.4).scale(0.72).shift(DOWN*0.3)
        ip_ty = Text("198.162.1.1").scale(0.48).next_to(yt_server, DOWN, buff=0.28)
        self.play(Write(dns_text))
        self.play(Write(yt_server), Write(ip_ty))
        self.wait(2)

        temp = Text("youtube.com").scale(0.75).next_to(laptop, UP)
        self.play(Write(temp))

        self.wait(1)

        arrow = CurvedArrow(temp.get_center(), dns.get_center(), angle=-PI/2, color=WHITE, stroke_width=8).set_color(ORANGE).set_z_index(-1)


        self.play(
            MoveAlongPath(temp, arrow), 
            )
        self.play(temp.animate.scale(0.0000001))
        self.wait()

        temp2 = Text("198.162.1.1").scale(0.001).move_to(temp)
        self.play(temp2.animate.scale(620).next_to(laptop, UP, buff=0.35), run_time=2)

        self.wait(1)

        rect = SurroundingRectangle(temp2, color=YELLOW,stroke_width=7).set_stroke(width=6).scale(1.2)
        self.play(ShowCreation(rect))
        self.wait()

        arrow = Arrow(laptop.get_right()+LEFT, server.get_left()+DOWN*0.184+RIGHT*0.61, color=GREEN, stroke_width=7, fill_color=GREEN).set_z_index(-1)
        self.play(GrowArrow(arrow))

        self.wait(2)
        self.play(self.camera.frame.animate.shift(DOWN*8).scale(0.9))

        text = Text("ISP knows All these things").shift(DOWN*7.5)
        self.play(Write(text))
        self.wait(2)
        text1 = Text("Server Knows Your IP").next_to(text, DOWN, buff=1)
        self.play(Write(text1))

        self.wait(2)






