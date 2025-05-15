from manimlib import *

class TCP(Scene):
    def construct(self):
        self.camera.frame.shift(UP*0.5+LEFT*0.2)

        # Set up camera position
        self.camera.frame.shift(DOWN * 0.5)
        
        # Create the main elements
        computer = ImageMobject("computer.png").scale(0.6).shift(LEFT * 4.5)
        server = ImageMobject("server.png").scale(0.8).shift(RIGHT * 4.5)

        # Add labels
        computer_label = Text("Sender", font_size=40).next_to(computer, DOWN, buff=0.74)
        server_label = Text("Receiver", font_size=40).next_to(server, DOWN, buff=0.5)
        
        # Add elements to scene
        self.play(FadeIn(computer), FadeIn(server))
        self.play(Write(computer_label), Write(server_label))
        
        self.wait(3)


        # Create SYN packet
        syn_rect = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)
        syn_text = Text("SYN", font_size=26, color=BLACK).set_color(BLACK)
        syn_packet = VGroup(syn_rect, syn_text).next_to(computer, RIGHT, buff=0.4).scale(1.4)

        self.play(GrowFromCenter(syn_packet), run_time=1)
        self.wait(2)

        self.play(syn_packet.animate.move_to(server.get_center()).scale(0.8), run_time=1.5)
        self.play(FadeOut(syn_packet), run_time=1)
        self.wait(1)

        # Create SYN-ACK packet             
        syn_ack_rect = Rectangle(height=0.4, width=1.7, fill_color=ORANGE, fill_opacity=1, stroke_color=ORANGE)
        syn_ack_text = Text("SYN-ACK", font_size=26, color=BLACK).set_color(BLACK)
        syn_ack_packet = VGroup(syn_ack_rect, syn_ack_text).next_to(server, LEFT, buff=0.4).scale(1.4)
        self.play(GrowFromCenter(syn_ack_packet), run_time=1)
        self.wait(2)
        self.play(syn_ack_packet.animate.move_to(computer.get_center()).scale(0.8), run_time=1.5)
        self.play(FadeOut(syn_ack_packet), run_time=1)
        self.wait(1)

        # Create ACK packet
        syn_rect = Rectangle(height=0.4, width=0.8, fill_color=GREEN, fill_opacity=1, stroke_color=GREEN)
        syn_text = Text("ACK", font_size=26, color=BLACK).set_color(BLACK)
        syn_packet = VGroup(syn_rect, syn_text).next_to(computer, RIGHT, buff=0.4).scale(1.4)

        self.play(GrowFromCenter(syn_packet), run_time=1)
        self.wait(2)

        self.play(syn_packet.animate.move_to(server.get_center()).scale(0.8), run_time=1.5)
        self.play(FadeOut(syn_packet), run_time=1)
        self.wait(1)

        
        # Get positions for the connection line
        computer_pos = computer.get_center()
        server_pos = server.get_center()
        
        # Create connection line with proper z-index
        connection_line = Line(computer_pos, server_pos, stroke_width=5, stroke_opacity=0.9)
        connection_line.set_z_index(-3)  # Set z-index to -1 as requested
        connection_line.set_color("#00FF00")
        
        self.play(ShowCreation(connection_line))
        
        # Create animated tracers along the path with proper z-index
        def create_tracers(start, end, color=RED, num=8):
            dots = VGroup()
            line = Line(start, end)
            
            # Create the dots with always_redraw to ensure they're continuously updated
            for i in range(num):
                dot = always_redraw(
                    lambda i=i: Dot(
                        line.point_from_proportion(
                            (self.time * 0.5 + i/num) % 1
                        ),
                        radius=0.16
                    ).set_z_index(-2).set_color(color)  # Set z-index to -1 as requested
                )
                dots.add(dot)
            
            return dots
        
        # Create the tracers for the connection
        tracers = create_tracers(computer_pos, server_pos, "#FF0000").set_z_index(-2)
        
        # Add tracers to the scene
        self.add(tracers)

        self.wait(2)

        self.play(self.camera.frame.animate.shift(UP*0.5))
        
        # Let the animation run
        self.wait(1)




        rect_a = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)   
        rect_b = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)
        rect_c = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)
        rect_d = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)

        a = VGroup(rect_a, rect_b, rect_c, rect_d).arrange(RIGHT, buff=0)
        a.next_to(computer, UP, buff=0.8)
        self.play(GrowFromCenter(a), run_time=1)

        self.wait(2)

        # Animate the separation using .animate
        self.play(
            rect_b.animate.shift(RIGHT * 0.4),
            rect_c.animate.shift(RIGHT * 0.8),
            rect_d.animate.shift(RIGHT * 1.2),
            run_time=1.5
        )




        self.play(a.animate.shift(LEFT*0.5))
        self.wait(1)
        
        # Add red header rectangles to each segment
        headers = VGroup()  # Create a VGroup to store all headers
        for rect in a:
            header = Rectangle(height=0.4, width=0.2, fill_color="#FF0000", fill_opacity=1, stroke_color="#FF0000",)
            header.next_to(rect, RIGHT, buff=0)
            headers.add(header)  # Add each header to the group
            self.play(GrowFromCenter(header), run_time=0.5)
        
        self.wait(3)

        self.play(self.camera.frame.animate.shift(LEFT*15+DOWN*0.66))


        temp = VGroup(rect_a, headers[0]).copy()
        self.play(temp.animate.shift(LEFT*11.5+DOWN*0.5).scale(4))
        self.wait()

        brace = Brace(temp[0], DOWN).shift(DOWN*0.4)
        self.play(GrowFromCenter(brace))

        text = Text("Actual Data", font_size=26, color=BLACK).set_color(WHITE).next_to(brace, DOWN, buff=0.4).shift(DOWN*0.3).scale(1.66)
        self.play(Write(text))

        self.wait(2)

        brace_1 = Brace(temp[1], RIGHT).shift(RIGHT*0.4)
        self.play(GrowFromCenter(brace_1))
        text_1 = Text("Header", font_size=26, color=BLACK).set_color(WHITE).next_to(brace_1, RIGHT, buff=0.4).shift(RIGHT*0.7).scale(1.7)
        self.play(Write(text_1))
        self.wait(2)



                # TCP Header Content Bullets
        tcp_header_content = [
            "Source Port (16 bits)",
            "Destination Port (16 bits)",
            "Sequence Number (32 bits)",
            "Acknowledgment Number (32 bits)",
            "Checksum (16 bits)",
            "...................."
           
        ]
        
        # Create bullet points for TCP header contents
        tcp_bullets = VGroup()
        for i, item in enumerate(tcp_header_content):
            bullet = Text("• " + item, font_size=20)
            tcp_bullets.add(bullet)
        
        # Arrange bullets in a column
        tcp_bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Position the bullet points on the screen (adjust position as needed)
        tcp_bullets.to_edge(RIGHT, buff=1)
        tcp_bullets.shift(UP)

        tcp_bullets.next_to(text_1, DOWN, buff=0.5).shift(DOWN*1.32+RIGHT*1.1).scale(1.1*1.1)
                
        # Display title and bullet points
        self.play(Write(tcp_bullets), run_time=2)
        self.wait(3)



        self.play(self.camera.frame.animate.shift(RIGHT*15+UP*0.66))


        self.wait(2)




        smiley = ImageMobject("smily.png").scale(0.2).next_to(server, ORIGIN).shift(UP*0.85)
        
        temp_a = VGroup(rect_a, headers[0]).copy()

        self.play(temp_a.animate.next_to(server, UP , buff=0.4).shift(LEFT*2), run_time=2)
        self.wait()

        self.play(smiley.animate.move_to(computer.get_center()+UP*0.4).scale(0.8), run_time=2)
        self.play(FadeOut(smiley), run_time=1)

        self.wait()

        self.play(FadeOut(rect_a), FadeOut(headers[0]), run_time=1)
        self.wait()


        smiley = ImageMobject("smily.png").scale(0.2).next_to(server, ORIGIN).shift(UP*0.85)
        
        temp_b = VGroup(rect_b, headers[1]).copy()

        self.play(temp_b.animate.next_to(temp_a, RIGHT , buff=0.2), run_time=2)
        self.wait()

        self.play(smiley.animate.move_to(computer.get_center()+UP*0.4).scale(0.8), run_time=2)
        self.play(FadeOut(smiley), run_time=1)

        self.wait()

        self.play(FadeOut(rect_b), FadeOut(headers[1]), run_time=1)
        self.wait()

        temp_c = VGroup(rect_c, headers[2]).copy()

        self.play(temp_c.animate.next_to(temp_a, LEFT , buff=0.2).scale(0.000000000000000001),run_time=2)
        self.wait(3)

        smiley = ImageMobject("smily.png").scale(0.2).next_to(server, ORIGIN).shift(UP*0.85)
        
        temp_c = VGroup(rect_c, headers[2]).copy()

        self.play(temp_c.animate.next_to(temp_b, RIGHT , buff=0.2), run_time=2)
        self.wait()

        self.play(smiley.animate.move_to(computer.get_center()+UP*0.4).scale(0.8), run_time=2)
        self.play(FadeOut(smiley), run_time=1)

        self.wait()

        self.play(FadeOut(rect_c), FadeOut(headers[2]), run_time=1)
        self.wait(1)     

        smiley = ImageMobject("smily.png").scale(0.2).next_to(server, ORIGIN).shift(UP*0.85)
        
        temp_d = VGroup(rect_d, headers[3]).copy()

        self.play(temp_d.animate.next_to(temp_c, RIGHT , buff=0.2), run_time=2)

        self.play(smiley.animate.move_to(computer.get_center()+UP*0.4).scale(0.8), run_time=2)
        self.play(FadeOut(smiley), run_time=1)


        self.play(FadeOut(rect_d), FadeOut(headers[3]), run_time=1)
        self.wait(1)

        self.play(
            FadeOut(temp_c[1]),
            FadeOut(temp_d[1]),
            FadeOut(temp_a[1]),
            FadeOut(temp_b[1]),
        )

        self.play(
            temp_b[0].animate.shift(RIGHT*0.2),
            temp_a[0].animate.shift(RIGHT*0.57),
            temp_c[0].animate.shift(LEFT*0.2),
            temp_d[0].animate.shift(LEFT*0.57),
        )

        self.wait(2)

        self.play(FadeOut(VGroup(temp_a[0], temp_b[0], temp_c[0], temp_d[0])))

        self.play(self.camera.frame.animate.shift(DOWN*0.5))

        self.wait(2)


        # Create SYN packet
        syn_rect = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)
        syn_text = Text("FIN", font_size=26, color=BLACK).set_color(BLACK)
        syn_packet = VGroup(syn_rect, syn_text).next_to(computer, UP, buff=0.66).scale(1.4)

        self.play(GrowFromCenter(syn_packet), run_time=1)
        self.wait(2)

        self.play(syn_packet.animate.move_to(server.get_center()).scale(0.8), run_time=1.5)
        self.play(FadeOut(syn_packet), run_time=1)
        self.wait(1)

        # Create SYN-ACK packet             
        syn_ack_rect = Rectangle(height=0.4, width=1.7, fill_color=ORANGE, fill_opacity=1, stroke_color=ORANGE)
        syn_ack_text = Text("ACK-FIN", font_size=26, color=BLACK).set_color(BLACK)
        syn_ack_packet = VGroup(syn_ack_rect, syn_ack_text).next_to(server, UP, buff=0.56).scale(1.4)
        self.play(GrowFromCenter(syn_ack_packet), run_time=1)
        self.wait(2)
        self.play(syn_ack_packet.animate.move_to(computer.get_center()).scale(0.8), run_time=1.5)
        self.play(FadeOut(syn_ack_packet), run_time=1)
        self.wait(1)

        # Create ACK packet
        syn_rect = Rectangle(height=0.4, width=0.8, fill_color=GREEN, fill_opacity=1, stroke_color=GREEN)
        syn_text = Text("ACK", font_size=26, color=BLACK).set_color(BLACK)
        syn_packet = VGroup(syn_rect, syn_text).next_to(computer, UP, buff=0.66).scale(1.4)

        self.play(GrowFromCenter(syn_packet), run_time=1)
        self.wait(2)

        self.play(syn_packet.animate.move_to(server.get_center()).scale(0.8), run_time=1.5)
        self.play(FadeOut(syn_packet), run_time=1)
        self.wait(1)

        self.play(FadeOut(tracers), FadeOut(connection_line), run_time=1)

        tick = ImageMobject("tick.png").scale(0.6).shift(UP*0.2)

        self.play(GrowFromCenter(tick), run_time=1)


        self.wait(3)



class UDP(Scene):

    def construct(self):

        self.camera.frame.shift(UP*0.5+LEFT*0.2)

        # Set up camera position
        self.camera.frame.shift(DOWN * 0.5)
        
        # Create the main elements
        computer = ImageMobject("computer.png").scale(0.6).shift(LEFT * 4.5)
        server = ImageMobject("server.png").scale(0.8).shift(RIGHT * 4.5)

        # Add labels
        computer_label = Text("Sender", font_size=40).next_to(computer, DOWN, buff=0.74)
        server_label = Text("Receiver", font_size=40).next_to(server, DOWN, buff=0.5)
        
        # Add elements to scene
        self.play(FadeIn(computer), FadeIn(server))
        self.play(Write(computer_label), Write(server_label))
        
        self.wait(3)

        # Create UDP packet


        rect_a = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)   
        rect_b = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)
        rect_c = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)
        rect_d = Rectangle(height=0.4, width=0.8, fill_color=YELLOW, fill_opacity=1, stroke_color=YELLOW)

        a = VGroup(rect_a, rect_b, rect_c, rect_d).arrange(RIGHT, buff=0)
        a.next_to(computer, UP, buff=0.8)
        self.play(GrowFromCenter(a), run_time=1)


        # Animate the separation using .animate
        self.play(
            rect_b.animate.shift(RIGHT * 0.4),
            rect_c.animate.shift(RIGHT * 0.8),
            rect_d.animate.shift(RIGHT * 1.2),
            run_time=1.5
        )

        self.play(a.animate.shift(LEFT*0.5))
        
        # Add red header rectangles to each segment
        headers = VGroup()  # Create a VGroup to store all headers
        for rect in a:
            header = Rectangle(height=0.4, width=0.2, fill_color="#FF0000", fill_opacity=1, stroke_color="#FF0000",)
            header.next_to(rect, RIGHT, buff=0)
            headers.add(header)  # Add each header to the group
            self.play(GrowFromCenter(header), run_time=0.5)
        
        self.wait(3)


        self.play(VGroup(rect_a, headers[0]).animate.move_to(server).scale(0.8), run_time=1.5)
        self.play(FadeOut(VGroup(rect_a, headers[0])), run_time=1)
        self.play(VGroup(rect_b, headers[1]).animate.move_to(server).scale(0.8), run_time=1.5)
        self.play(FadeOut(VGroup(rect_b, headers[1])), run_time=1)
        self.play(VGroup(rect_c, headers[2]).animate.move_to(server).scale(0.8), run_time=1.5)
        self.play(FadeOut(VGroup(rect_c, headers[2])), run_time=1)
        self.play(VGroup(rect_d, headers[3]).animate.move_to(server).scale(0.8), run_time=1.5)
        self.play(FadeOut(VGroup(rect_d, headers[3])), run_time=1)
        self.wait(3)
