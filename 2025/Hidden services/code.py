from manimlib import *

class TorNetworkAnimation(Scene):
    def construct(self):
        # Set up camera position
        self.camera.frame.shift(DOWN * 0.65 + LEFT*0.1)
        
        # Create the main elements
        laptop = ImageMobject("computer.png").scale(0.56).shift(LEFT * 5 + DOWN * 0.2)
        server = ImageMobject("server.png").scale(0.8).shift(RIGHT * 5 + DOWN * 0.2)

        a = Text("client", font_size=28).next_to(laptop, DOWN, buff=0.1).shift(DOWN).scale(1.4)
        b = Text("hidden\nserver", font_size=28).next_to(server, DOWN, buff=0.1).shift(DOWN*0.5).scale(1.4)

        
        # Create cloud for TOR network
        cloud = ImageMobject("cloud.png")
        cloud.set_z_index(-1)

        c = Text("TOR network", font_size=28).next_to(cloud, DOWN, buff=0.1).shift(DOWN*0.4).scale(1.4)

        
        # Add elements to scene
        self.add(laptop, server)
        self.play(FadeIn(cloud))

        self.play(Write(a), Write(b), Write(c))
        
        self.wait(2)
        
        # Get positions for the connection lines
        laptop_pos = laptop.get_right() + LEFT * 0.3
        cloud_left = cloud.get_left() + RIGHT * 0.5
        cloud_right = cloud.get_right() + LEFT * 0.5
        server_pos = server.get_left() + RIGHT * 0.3
        
        # Create connection lines
        line1 = Line(laptop_pos, cloud_left, stroke_width=5, stroke_opacity=0.7).set_z_index(-1).set_color("#00FF00")
        line2 = Line(cloud_right, server_pos, stroke_width=5, stroke_opacity=0.7).set_z_index(-1).set_color("#00FF00")
        
        self.play(ShowCreation(line1), ShowCreation(line2))
        
        # Create animated tracers along each path
        def create_tracers(start, end, color=GREEN, num=8):
            dots = VGroup().set_z_index(-1).set_color("#FF0000")
            line = Line(start, end).set_z_index(-1)
            
            # Create the dots with always_redraw to ensure they're continuously updated
            for i in range(num):
                dot = always_redraw(
                    lambda i=i: Dot(
                        line.point_from_proportion(
                            (self.time * 0.5 + i/num) % 1
                        ),
                        radius=0.077
                    ).set_z_index(-1).set_color(color)
                )
                dots.add(dot)
            
            return dots
        
        # Create the tracers for each connection
        tracers1 = create_tracers(laptop_pos, cloud_left, "#FF0000")
        tracers2 = create_tracers(cloud_right, server_pos, "#FF0000")
        
        # Add all tracers to the scene
        self.add(tracers1, tracers2)
        
        # Let the animation run
        self.wait(2)

        handshake = ImageMobject("handshake.png").move_to(cloud).scale(0.33).shift(DOWN*0.075)
        self.play(FadeIn(handshake))
        self.wait(4)
        self.play(FadeOut(handshake))

        self.wait(10)

        self.play(FadeOut(laptop),FadeOut(a), FadeOut(b), FadeOut(c), FadeOut(tracers1), FadeOut(line1), FadeOut(line2), FadeOut(tracers2),
                  self.camera.frame.animate.scale(0.7).shift(RIGHT*1.85+UP*0.6))
        self.play(cloud.animate.scale(1.2*1.2))
        self.wait(2)

        blue = ImageMobject("blue.png").scale(0.2)
        red = ImageMobject("red.png").scale(0.2).next_to(blue, RIGHT, buff=0.1)
        green = ImageMobject("green.png").scale(0.2).next_to(red, DOWN, buff=0.1)
        yellow = ImageMobject("yellow.png").scale(0.2).next_to(blue, DOWN, buff=0.1)
        black = ImageMobject("black.png").scale(0.2*0.82).next_to(yellow, LEFT, buff=0.1).shift(UP*0.08)
        self.add(blue, red, green, yellow, black)

        self.wait(2)

        line3 = CurvedDoubleArrow(server.get_center(), blue.get_center(), stroke_width=6).set_z_index(-1).set_color("#00FF00")
        line1 = CurvedDoubleArrow(server.get_center(), red.get_center()+UP*0.1, stroke_width=6).set_z_index(-1).set_color("#00FF00")
        line2 = CurvedDoubleArrow(server.get_center(), green.get_center()+UP*0.1, stroke_width=6).set_z_index(-1).set_color("#00FF00")

        self.play(ShowCreation(line3), ShowCreation(line1), ShowCreation(line2))
        
        # Create animated tracers along each curved path
        def create_curved_tracers(curved_path, color=YELLOW, num=8):
            dots = VGroup().set_z_index(-0.5)  # Set z-index as requested
            
            # Create the dots with always_redraw to ensure they're continuously updated
            for i in range(num):
                dot = always_redraw(
                    lambda i=i: Dot(
                        curved_path.point_from_proportion(
                            (self.time * 0.4 + i/num) % 1
                        ),
                        radius=0.077
                    ).set_z_index(-0.5).set_color(color)  # Set z-index as requested
                )
                dots.add(dot)
            
            return dots
        
        # Create the tracers for each curved connection
        curved_tracers1 = create_curved_tracers(line1, "#FF0000")
        curved_tracers2 = create_curved_tracers(line2, "#FF0000")
        curved_tracers3 = create_curved_tracers(line3, "#FF0000")
        
        # Add all curved tracers to the scene
        self.add(curved_tracers1, curved_tracers2, curved_tracers3)
        
        self.wait(2)


        self.play(self.camera.frame.animate.shift(DOWN*0.6))

        temp = Rectangle(color=YELLOW, fill_color=YELLOW, fill_opacity=0.7,height=0.8, width=2.9 ).set_z_index(-1).next_to(server, DOWN, buff=0.1)
        temp_text = Text("Descriptors", font_size=28).move_to(temp).set_color(BLACK)

        descriptor = VGroup(temp, temp_text)
        


        temp = Text("xyz.onion").next_to(descriptor, LEFT, buff=1).shift(DOWN*0.2)
        self.play(ShowCreation(temp))
        self.wait(3)

        self.play(GrowFromCenter(descriptor))

        self.wait(3)


        self.wait(4)
        self.play(Uncreate(temp))


        database = ImageMobject("database.png").scale(0.245).next_to(cloud, DOWN, buff=0.1).shift(UP*0.8+RIGHT*1.85)
        self.play(ShowCreation(database))

        self.play(descriptor.animate.move_to(database).scale(0.0000000000000001))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*2.5))

        laptop.scale(0.7).shift(RIGHT*0.8+DOWN*0.6)

        self.play(GrowFromCenter(laptop))



        line5 = CurvedArrow(laptop.get_center(), yellow.get_center()+UP*0.13, color="#00FF00", stroke_width=6, angle=PI/2).set_z_index(-0.7)
        self.play(ShowCreation(line5))



        def create_curved_tracers2(curved_path, color=YELLOW, num=13):
            dots = VGroup().set_z_index(-0.7)  # Set z-index as requested
            
            # Create the dots with always_redraw to ensure they're continuously updated
            for i in range(num):
                dot = always_redraw(
                    lambda i=i: Dot(
                        curved_path.point_from_proportion(
                            (self.time * 0.3 + i/num) % 1
                        ),
                        radius=0.077
                    ).set_z_index(-0.7).set_color(color)  # Set z-index as requested
                )
                dots.add(dot)
            
            return dots

        teacer2 = create_curved_tracers2(line5, "#FF0000")
        self.add(teacer2)

        self.wait(4)


        curved_arrow = CurvedArrow(laptop.get_center(), database.get_center(), color="#00FF00", stroke_width=6, angle=-PI/2).set_z_index(-2)
        self.play(ShowCreation(curved_arrow))

        # Create animated tracers along each curved path
        def create_curved_tracers1(curved_path, color=YELLOW, num=13):
            dots = VGroup().set_z_index(-1.5)  # Set z-index as requested
            
            # Create the dots with always_redraw to ensure they're continuously updated
            for i in range(num):
                dot = always_redraw(
                    lambda i=i: Dot(
                        curved_path.point_from_proportion(
                            (self.time * 0.3 + i/num) % 1
                        ),
                        radius=0.077
                    ).set_z_index(-2.5).set_color(color)  # Set z-index as requested
                )
                dots.add(dot)
            
            return dots


        tracer1 = create_curved_tracers1(curved_arrow, "#FF0000")
        self.add(tracer1)

        self.wait(4)
        
        self.remove(tracer1)
        self.play(FadeOut(curved_arrow))

        self.wait(2)

        line5 = CurvedArrow(laptop.get_center(), blue.get_center(), color="#00FF00", stroke_width=6, angle=-PI/2).set_z_index(-0.7)
        self.play(ShowCreation(line5), FadeOut(database), self.camera.frame.animate.shift(UP*0.43))

        tracer3 = create_curved_tracers2(line5, "#FF0000")
        self.add(tracer3)

        self.wait(2)

        data = ImageMobject("data.png").scale(0.15).next_to(laptop, UP, buff=0.1)
        self.play(ShowCreation(data))
        self.wait(1)

        self.play(data.animate.next_to(blue, UP,  buff=0.1),
                  self.camera.frame.animate.shift(RIGHT*2.2))
        self.play(data.animate.next_to(server, UP,  buff=0).shift(DOWN*0.3))

        self.wait(1)

        answer = ImageMobject("answer.png").scale(0.15).next_to(server, UP, buff=0.1).shift(DOWN*0.4)
        self.play(FadeIn(answer), FadeOut(data))
        self.wait()

        line6 = CurvedArrow(server.get_center(), yellow.get_center()+UP*0.1, color="#00FF00", stroke_width=6, angle=-PI/2).set_z_index(-0.7)
        self.play(ShowCreation(line6), FadeOut(answer))
        tracer4 = create_curved_tracers2(line6, "#FF0000")
        self.add(tracer4)
        self.play(FadeOut(tracer3), FadeOut(line5),
                  self.camera.frame.animate.scale(1.18).shift(LEFT+DOWN*0.4)
                  )
        self.wait(2)

        arrow = Arrow(yellow.get_center(), yellow.get_center()+DOWN*1.7, color=YELLOW, stroke_width=6, fill_color=YELLOW, fill_opacity=1).shift(DOWN*0.65).rotate(PI)
        self.play(ShowCreation(arrow))

        self.wait(10)


class TCPvsUDPComparison(Scene):
    def construct(self):

        self.camera.frame.shift(DOWN*0.88)


        # Title
        # Create table headers
        tcp_header = Text("TCP", font_size=40, color=BLUE)
        tcp_header.move_to(LEFT * 3 + UP * 2)
        
        udp_header = Text("UDP", font_size=40, color=GREEN)
        udp_header.move_to(RIGHT * 3 + UP * 2)
        
        divider_line = Line(
            start=UP * 2,
            end=DOWN * 4.45,
            stroke_width=2
        )
        
        # Create comparison points
        comparisons = [
            ["Connection-oriented", "Connectionless"],
            ["Reliable data transfer", "Unreliable data transfer"],
            ["Flow control", "No flow control"],
            ["Congestion control", "No congestion control"],
            ["Ordered packets", "Unordered packets"],
            ["Error checking & correction", "Basic error checking only"],
            ["Acknowledgment", "No acknowledgment"],
            ["Retransmission of lost data", "No retransmission"],
            ["Higher overhead", "Lower overhead"],
            ["Slower speed", "Faster speed"]
        ]
        
        # Create table rows
        table_rows = VGroup()
        tcp_items = VGroup()
        udp_items = VGroup()
        
        for i, (tcp_feature, udp_feature) in enumerate(comparisons):
            # TCP feature
            tcp_text = Text(tcp_feature, font_size=24)
            tcp_text.move_to(LEFT * 3 + DOWN * (i * 0.5 - 0.5))
            tcp_items.add(tcp_text)
            
            # UDP feature
            udp_text = Text(udp_feature, font_size=24)
            udp_text.move_to(RIGHT * 3 + DOWN * (i * 0.5 - 0.5))
            udp_items.add(udp_text)
            
            # Add to table rows
            table_rows.add(VGroup(tcp_text, udp_text))
        
        # Animation sequence
        self.play(ShowCreation(tcp_header), ShowCreation(udp_header))
        self.play(ShowCreation(divider_line))
        self.wait(0.5)


        
        # Animate the rows appearing
        for i, row in enumerate(table_rows):
            self.play(ShowCreation(row[0]), ShowCreation(row[1]), run_time=0.5)
            self.wait(0.1)
        
        self.wait(1)
        
        # Highlight corresponding pairs to emphasize comparisons
        for i in range(len(comparisons)):
            self.play(
                tcp_items[i].animate.set_color(YELLOW),
                udp_items[i].animate.set_color(YELLOW),
                run_time=0.7
            )
            self.wait(2)
            self.play(
                tcp_items[i].animate.set_color(WHITE),
                udp_items[i].animate.set_color(WHITE),
                run_time=0.5
            )
        
        # Use cases
        use_case_title = Text("Common Use Cases", font_size=36, color=YELLOW)
        use_case_title.next_to(table_rows, DOWN, buff=0.8)
        
        tcp_uses = Text("Web, Email, File Transfer", font_size=28, color=BLUE)
        tcp_uses.next_to(use_case_title, DOWN, buff=0.5).shift(LEFT * 3)
        
        udp_uses = Text("Streaming, Gaming, VoIP", font_size=28, color=GREEN)
        udp_uses.next_to(use_case_title, DOWN, buff=0.5).shift(RIGHT * 3)
        
        self.play(ShowCreation(use_case_title))
        self.play(ShowCreation(tcp_uses), ShowCreation(udp_uses))
        
        self.wait(2)
        

        self.wait(1)
