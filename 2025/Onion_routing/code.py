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





from manimlib import *

class TOR2(Scene):
    def construct(self):

        self.camera.frame.shift(DOWN*0.3+LEFT*0.3)
        laptop = ImageMobject("computer.png").scale(0.56).shift(LEFT*4.6+DOWN*0.22)
        server = ImageMobject("server.png").shift(RIGHT*5+DOWN*1.66)
        dns = ImageMobject("dns.png").scale(0.7).shift(UP*2+RIGHT*0.34)
        
        self.add(laptop)

        self.wait(2)
        
        blue = ImageMobject("blue.png").scale(0.36).shift(UP*2.2)
        red = ImageMobject("red.png").scale(0.36).shift(RIGHT).next_to(blue, DOWN).shift(DOWN*3.6+RIGHT*0.2)
        green = ImageMobject("green.png").scale(0.36).next_to(red, RIGHT).shift(UP*2.3+RIGHT*1.6)
        
        
        self.play(FadeIn(blue))
        self.play(FadeIn(red),)
        self.play(FadeIn(green))
        self.wait(1)

        green_key = ImageMobject("green_key.png").scale(0.2).next_to(green, RIGHT, buff=0.15)
        red_key = ImageMobject("red_key.png").scale(0.2).next_to(red, RIGHT, buff=0.15)
        blue_key = ImageMobject("blue_key.png").scale(0.2).next_to(blue, RIGHT, buff=0.15)


        self.play(FadeIn(green_key), FadeIn(red_key), FadeIn(blue_key))

        
        self.wait(1)
        
        # Get positions
        laptop_pos = laptop.get_center()
        blue_pos = blue.get_center()
        red_pos = red.get_center()
        green_pos = green.get_center()
        
        # Create connection lines
        line1 = Line(laptop_pos, blue_pos, stroke_width=1, stroke_opacity=0.3).set_z_index(-1)
        line2 = Line(blue_pos, red_pos, stroke_width=1, stroke_opacity=0.3).set_z_index(-1)
        line3 = Line(red_pos, green_pos, stroke_width=1, stroke_opacity=0.3).set_z_index(-1)
        
        self.add(line1, line2, line3)
        
        # Create animated tracers along each path
        def create_tracers(start, end, color=YELLOW, num=10):
            dots = VGroup().set_z_index(-1)
            line = Line(start, end).set_z_index(-1)
            
            # Create the dots with always_redraw to ensure they're continuously updated
            for i in range(num):
                dot = always_redraw(
                    lambda i=i: Dot(
                        line.point_from_proportion(
                            (self.time * 0.7 + i/num) % 1
                        ),
                        color=color,
                        radius=0.05
                    ).set_z_index(-1)
                )
                dots.add(dot)
            
            return dots
        
        # Create the tracers for each connection
        tracers1 = create_tracers(laptop_pos, blue_pos, YELLOW)
        tracers2 = create_tracers(blue_pos, red_pos, YELLOW)
        tracers3 = create_tracers(red_pos, green_pos, YELLOW)
        
        # Add all tracers to the scene
        self.add(tracers1, tracers2, tracers3)
        
        # Let the animation run
        self.wait(2)




        green_key_1 = green_key.copy().next_to(laptop, UP, buff=0.15).shift(LEFT*0.5)
        red_key_1 = red_key.copy().next_to(green_key_1, RIGHT, buff=0.15)
        blue_key_1 = blue_key.copy().next_to(red_key_1, RIGHT, buff=0.15)

        self.play(TransformFromCopy(green_key, green_key_1), TransformFromCopy(red_key, red_key_1), TransformFromCopy(blue_key, blue_key_1))
        self.wait(2)

        query = ImageMobject("query.png").scale(0.34).next_to(laptop, DOWN, buff=0.77)
        self.play(FadeIn(query))
        self.wait(2)

        temp = green_key_1.copy()
        green_lock = ImageMobject("green_lock.png").scale(0.35).move_to(query)
        red_lock = ImageMobject("red_lock.png").scale(0.35).move_to(query)
        blue_lock = ImageMobject("blue_lock.png").scale(0.35).move_to(query)
        self.play(temp.animate.move_to(query))
        self.play(FadeIn(green_lock), FadeOut(temp), FadeOut(query))
        self.wait(2)

        temp = red_key_1.copy()
        self.play(temp.animate.move_to(query))
        self.play(FadeIn(red_lock), FadeOut(temp), FadeOut(green_lock))
        self.wait(2)

        temp = blue_key_1.copy()
        self.play(temp.animate.move_to(query))
        self.play(FadeIn(blue_lock), FadeOut(temp), FadeOut(red_lock))
        self.wait(2)

        self.play(blue_lock.animate.next_to(blue_key, RIGHT, buff=0.8).shift(LEFT*0.5))
        temp = blue_key.copy()
        self.play(temp.animate.move_to(blue_lock))
        red_lock = ImageMobject("red_lock.png").scale(0.35).move_to(blue_lock)
        self.play(FadeOut(blue_lock), FadeOut(temp), FadeIn(red_lock))
        self.wait(2)

        self.play(red_lock.animate.next_to(red_key, RIGHT, buff=0.8).shift(LEFT*0.5))
        temp = red_key.copy()
        self.play(temp.animate.move_to(red_lock))
        green_lock = ImageMobject("green_lock.png").scale(0.35).move_to(red_lock)
        self.play(FadeOut(red_lock), FadeOut(temp), FadeIn(green_lock))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*4))
        self.play(green_lock.animate.next_to(green_key, RIGHT, buff=0.8).shift(LEFT*0.5))
        temp = green_key.copy()
        self.play(temp.animate.move_to(green_lock))
        query = ImageMobject("query.png").scale(0.35).move_to(green_lock)
        self.play(FadeOut(green_lock), FadeOut(temp), FadeIn(query))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*6))

        dns = ImageMobject("dns.png").scale(0.6).next_to(query, RIGHT, buff=2.7).shift(UP*2.5)
        self.play(FadeIn(dns))
        self.wait()

        arrow1 = CurvedArrow(start_point=query.get_top(), end_point=dns.get_left(), angle=-PI/2, color=YELLOW, stroke_width=7).set_z_index(-1)
        self.play(ShowCreation(arrow1))

        self.wait()

        temp = Dot(color=YELLOW, radius=0.2).move_to(query).set_color(GREEN)
        self.play(MoveAlongPath(temp, arrow1), run_time=2)
        self.play(FadeOut(temp))

        arrow2 = CurvedArrow(start_point=dns.get_bottom(), end_point=query.get_right(), angle=-PI/2, color=YELLOW, stroke_width=7).set_z_index(-1)
        self.play(ShowCreation(arrow2))
        temp = Dot(color=YELLOW, radius=0.2).move_to(query).set_color(BLUE)
        self.play(MoveAlongPath(temp, arrow2), run_time=2)
        self.play(FadeOut(temp))

        self.wait()

        self.play(FadeOut(arrow1), FadeOut(arrow2), FadeOut(dns))

        self.wait(2)

        server = ImageMobject("server.png").next_to(query, RIGHT, buff=4.5).scale(1).shift(UP)
        text = Text("Server", font_size=50).next_to(server, DOWN, buff=0.2)
        self.play(FadeIn(server), FadeIn(text)) 
        self.wait(1)


        self.play(query.animate.move_to(server).scale(0.000001), run_time=2)

        self.wait()

        answer = ImageMobject("answer.png").scale(0.35*0.001).move_to(server).shift(UP*0.5)
        self.play(answer.animate.scale(1000).next_to(green_key, RIGHT, buff=0.65))
        self.wait()

        self.embed()


        temp = green_key.copy()
        self.play(temp.animate.move_to(answer))
        green_lock = ImageMobject("green_lock.png").scale(0.35).move_to(answer)
        self.play(FadeIn(green_lock), FadeOut(temp), FadeOut(answer))
        self.play(self.camera.frame.animate.shift(LEFT*7))
        self.wait()

        self.play(green_lock.animate.next_to(red_key, RIGHT, buff=0.8).shift(LEFT*0.5))
        temp = red_key.copy()
        self.play(temp.animate.move_to(green_lock))
        red_lock = ImageMobject("red_lock.png").scale(0.35).move_to(green_lock)
        self.play(FadeOut(green_lock), FadeOut(temp), FadeIn(red_lock))
        self.wait(1)

        self.play(red_lock.animate.next_to(blue_key, RIGHT, buff=0.8).shift(LEFT*0.5))
        temp = blue_key.copy()
        self.play(temp.animate.move_to(blue_lock))
        blue_lock = ImageMobject("blue_lock.png").scale(0.35).move_to(red_lock)
        self.play(FadeOut(red_lock), FadeOut(temp), FadeIn(blue_lock))
        self.play(self.camera.frame.animate.shift(LEFT*3.16))
        self.wait(1)

        self.play(blue_lock.animate.next_to(laptop, DOWN, buff=0.8))

        self.wait(2)

        temp = blue_key_1.copy()
        self.play(temp.animate.move_to(blue_lock))
        red_lock = ImageMobject("red_lock.png").scale(0.35).move_to(blue_lock)
        self.play(FadeOut(blue_lock), FadeOut(temp), FadeIn(red_lock))
        self.wait(1)

        temp = red_key_1.copy()
        self.play(temp.animate.move_to(red_lock))
        green_lock = ImageMobject("green_lock.png").scale(0.35).move_to(blue_lock)
        self.play(FadeOut(red_lock), FadeOut(temp), FadeIn(green_lock))
        self.wait(1)


        temp = green_key_1.copy()
        self.play(temp.animate.move_to(green_lock))
        answer = ImageMobject("answer.png").scale(0.35).move_to(green_lock)
        self.play(FadeOut(green_lock), FadeOut(temp), FadeIn(answer))
        self.wait(3)
        









