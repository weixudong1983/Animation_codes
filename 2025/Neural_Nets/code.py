from manimlib import *
import numpy as np



class NeuronsIntro(Scene):
    def construct(self):

        self.camera.frame.scale(0.9).shift(RIGHT*0.9+UP*0.1)
        # Create the main neuron (circular node) - full opacity
        neuron = Circle(radius=0.8, color=BLUE, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        neuron.move_to(ORIGIN)
        
        # Input nodes - full opacity, closer to make more space on right
        input1 = Circle(radius=0.3, color=GREEN, fill_opacity=1, stroke_width=7
                        , stroke_color=GREEN_B)
        input2 = Circle(radius=0.3, color=GREEN, fill_opacity=1, stroke_width=7, stroke_color=GREEN_B)
        input1.move_to(LEFT * 3.2 + UP * 1.5)
        input2.move_to(LEFT * 3.2 + DOWN * 1.5)
        
        # Larger input labels - scaled 1.8
        x1_label = Tex("x_1", font_size=40).scale(1.8).next_to(input1, LEFT, buff=0.2)
        x2_label = Tex("x_2", font_size=40).scale(1.8).next_to(input2, LEFT, buff=0.2)
        
        # Larger weight labels - scaled 1.8
        w1_label = Tex("w_1", font_size=36, color=RED).scale(1.8)
        w2_label = Tex("w_2", font_size=36, color=RED).scale(1.8)
        
        # Bias arrow and larger label - positioned slightly UP
        bias_arrow = Arrow(UP * 2.5, neuron.get_top() + UP * 0.1, stroke_width=3)
        bias_arrow.set_color(PURPLE)
        bias_label = Tex("b", font_size=40, color=PURPLE).scale(1.8).next_to(bias_arrow.get_start(), UP, buff=0.28)
        
        # Thicker connection lines from center to center with z_index = -1
        line1 = Line(input1.get_center(), neuron.get_center(), stroke_width=6, z_index=-1)
        line2 = Line(input2.get_center(), neuron.get_center(), stroke_width=6, z_index=-1)
        line1.set_color(WHITE)
        line2.set_color(WHITE)
        
        # Position weight labels
        w1_label.move_to(line1.get_center() + UP * 0.5)
        w2_label.move_to(line2.get_center() + DOWN * 0.5)
        
        # Output arrow
        output_arrow = Arrow(neuron.get_right(), RIGHT * 2.5, stroke_width=3)
        output_arrow.set_color(BLUE)
        output_label = Tex("y", font_size=40, color=BLUE).scale(1.8).next_to(output_arrow.get_end(), RIGHT)
        
        # Build structure
        self.play(
            ShowCreation(input1), ShowCreation(input2),
            Write(x1_label), Write(x2_label)
        )

        self.play(ShowCreation(neuron))
        self.wait(1)
        self.play(
            ShowCreation(line1), ShowCreation(line2),
            Write(w1_label), Write(w2_label)
        )

        self.wait(2)


        
        # First formula without bias - larger size
        linear_no_bias = Tex("z = w_1 x_1 + w_2 x_2", font_size=58)
        linear_no_bias.to_edge(RIGHT, buff=1)
        self.play(
            FadeIn(linear_no_bias[:2]),
            FadeIn(linear_no_bias[6]),

            TransformFromCopy(x1_label, linear_no_bias[4:6]),
            TransformFromCopy(w1_label, linear_no_bias[2:4]),
            TransformFromCopy(x2_label, linear_no_bias[-4:-2]),
            TransformFromCopy(w2_label, linear_no_bias[-2:]),
        )
        self.wait(2)

        self.play(linear_no_bias[2:4].animate.set_color(YELLOW).scale(1.32))
        self.wait(2)
        self.play(linear_no_bias[2:4].animate.set_color(YELLOW).scale(1/1.32*0.66))
        self.wait(2)
        self.play(linear_no_bias[2:4].animate.set_color(WHITE).scale(1.4))
        self.wait(2)

        

        brace = Brace(linear_no_bias[2:], DOWN)
        brace_text = Text("0", font_size=46, color=YELLOW)
        brace_text.next_to(brace, DOWN, buff=0.3)
        
        self.play(GrowFromCenter(brace), Write(brace_text))
        self.wait(2)


        self.play(FadeOut(brace), FadeOut(brace_text))
        self.wait(1)


        # Add bias term and arrow
        self.play(ShowCreation(bias_arrow), Write(bias_label))
        
        # Update formula with bias - same size
        linear_with_bias = Tex("z = w_1 x_1 + w_2 x_2 + b", font_size=48)
        linear_with_bias.move_to(linear_no_bias.get_center())
        self.play(Transform(linear_no_bias, linear_with_bias))
        self.wait(2)
        
        # Transform that formula into general form AT THE SAME PLACE
        general_formula = Tex(r"z = \sum_{i=1}^{n} w_i x_i + b", font_size=62)
        general_formula.move_to(linear_no_bias.get_center())
        self.play(Transform(linear_no_bias, general_formula))
        self.wait(2)

        self.play(linear_no_bias.animate.shift(UP))

        # BELOW it, show y = phi() first (fade in phi() without z)
        activation_phi = Tex(r"y = \phi(z)", font_size=68)
        activation_phi.next_to(linear_no_bias, DOWN, buff=1)
        self.play(FadeIn(activation_phi[:4]), FadeIn(activation_phi[-1]))
        self.wait(1.5)
        

        
        self.play(
            TransformFromCopy(linear_no_bias, activation_phi[4]),
        )
        self.wait(2)



        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2.9, 2.9, 1],
            axis_config={
                "stroke_width": 7,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            },



        ).shift(RIGHT*12.6+DOWN*0.2)

        # Create axis labels (at the end of axes)
        x_label = Tex("z", font_size=63).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Tex("y", font_size=63).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # First, add little white bars at y = -2 and y = 2 on y-axis (but label them as -1 and 1)
        y_tick_neg2 = Line(
            axes.c2p(-0.2, -1.7), axes.c2p(0.2, -1.7),
            stroke_width=6, color=WHITE
        )
        y_tick_pos2 = Line(
            axes.c2p(-0.2, 1.7), axes.c2p(0.2, 1.7),
            stroke_width=6, color=WHITE
        )
        
        # Add labels showing -1 and 1 (for visual clarity) even though ticks are at -2 and 2
        y_label_neg1 = Tex("-1", font_size=40, color=WHITE).next_to(y_tick_neg2, LEFT, buff=0.3)
        y_label_pos1 = Tex("1", font_size=40, color=WHITE).next_to(y_tick_pos2, LEFT, buff=0.3)
        

        self.play(ShowCreation(axes), self.camera.frame.animate.shift(RIGHT*12), ShowCreation(y_tick_neg2), ShowCreation(y_tick_pos2),
           )

        self.play(ShowCreation(x_label), ShowCreation(y_label))

        self.wait(2)

        # Step Function (scaled to -2, 2 range)
        step_points = []
        x_vals = np.linspace(-5, 5, 1000)
        for x in x_vals:
            y = 1.7 if x >= 0 else -1.7  # Using 2 and -2 instead of 1 and 0
            step_points.append(axes.c2p(x, y))
        
        step_graph = VMobject()
        step_graph.set_points_as_corners(step_points)
        step_graph.set_stroke(RED, width=8)
        
        # Step function title and formula in second quadrant
        step_title = Text("Step Function", font_size=44, color=RED)
        step_title.move_to(axes.c2p(-3, 3.3))
        step_title.z_index = 10
        
        step_formula = Tex(r"\phi(z) = \begin{cases} 1 & \text{if } z \geq 0 \\ -1 & \text{if } z < 0 \end{cases}", 
                           font_size=40, color=RED)
        step_formula.next_to(step_title, DOWN, buff=0.46)
        step_formula.z_index = 10
        
        self.play(ShowCreation(step_graph), Write(step_title), Write(step_formula))
        self.wait(2)

        
        # Transform Step to ReLU (scaled to fit -2, 2 range)
        relu_points = []
        for x in x_vals:
            y = max(0, x)  # Scaled ReLU to fit in -2 to 2 range
            relu_points.append(axes.c2p(x, y))
        
        relu_graph = VMobject()
        relu_graph.set_points_as_corners(relu_points)
        relu_graph.set_stroke(GREEN, width=8)
        
        # ReLU title and formula in second quadrant
        relu_title = Text("ReLU Function", font_size=44, color=GREEN)
        relu_title.move_to(step_title)
        relu_title.z_index = 10
        
        relu_formula = Tex(r"ReLU(z) = \max(0, z)", font_size=46, color=GREEN)
        relu_formula.next_to(relu_title, DOWN, buff=0.44)
        relu_formula.z_index = 10
        
        self.play(
            Transform(step_graph, relu_graph),
            Transform(step_title, relu_title),
            Transform(step_formula, relu_formula)
        )
        self.wait(2)
        
        # Transform ReLU to Sigmoid (scaled to -2, 2 range)
        sigmoid_points = []
        for x in x_vals:
            sigmoid_val = 1 / (1 + np.exp(-x))  # Standard sigmoid (0 to 1)
            y = (sigmoid_val * 2 - 1) * 1.7  # Scale to -1.7 to +1.7 range
            sigmoid_points.append(axes.c2p(x, y))
        
        sigmoid_graph = VMobject()
        sigmoid_graph.set_points_smoothly(sigmoid_points)
        sigmoid_graph.set_stroke(PURPLE, width=8)
        
        # Sigmoid title and formula in second quadrant
        sigmoid_title = Text("Sigmoid Function", font_size=44, color=PURPLE)
        sigmoid_title.move_to(relu_title)
        sigmoid_title.z_index = 10
        
        sigmoid_formula = Tex(r"\sigma(z) = \frac{1}{1 + e^{-z}}", font_size=46, color=PURPLE)
        sigmoid_formula.next_to(relu_title, DOWN, buff=0.45)
        sigmoid_formula.z_index = 10
        
        self.play(
            Transform(step_graph, sigmoid_graph),
            Transform(step_title, sigmoid_title),
            Transform(step_formula, sigmoid_formula)
        )
        self.wait(3)


        
        self.wait(1)
        
        # Move camera back to the left
        self.play(
            self.camera.frame.animate.shift(LEFT*12+UP*0.24),
            run_time=2
        )
        self.wait(1)

        self.play(FadeOut(linear_no_bias), FadeOut(activation_phi), self.camera.frame.animate.shift(LEFT*1.55))
        

        # Add output arrow and label
        self.play(ShowCreation(output_arrow))
        
        # Information flow animation
        def create_pulse(start_point, end_point, color=YELLOW, duration=1.5):
            pulse = Dot(radius=0.2, color=color, fill_opacity=0.9)
            pulse.move_to(start_point)
            glow = Circle(radius=0.4, color=color, fill_opacity=0.4, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        pulse1, glow1 = create_pulse(input1.get_center(), neuron.get_center(), color=YELLOW)
        pulse2, glow2 = create_pulse(input2.get_center(), neuron.get_center(), color=ORANGE)
        pulse_bias, glow_bias = create_pulse(bias_arrow.get_start(), neuron.get_center(), color=PURPLE)
        
        self.add(pulse1, glow1, pulse2, glow2, pulse_bias, glow_bias)
        
        self.play(
            pulse1.animate.move_to(neuron.get_center()),
            glow1.animate.move_to(neuron.get_center()),
            pulse2.animate.move_to(neuron.get_center()),
            glow2.animate.move_to(neuron.get_center()),
            pulse_bias.animate.move_to(neuron.get_center()),
            glow_bias.animate.move_to(neuron.get_center()),
            run_time=2
        )
        
        self.play(
            neuron.animate.set_fill(YELLOW, opacity=1),
            FadeOut(pulse1), FadeOut(glow1),
            FadeOut(pulse2), FadeOut(glow2),
            FadeOut(pulse_bias), FadeOut(glow_bias),
            run_time=0.8
        )
        
        # Show phi in neuron - scale 1.7 and set_color BLACK
        phi_in_neuron = Tex(r"\phi(z)", font_size=32).scale(1.7)
        phi_in_neuron.set_color(BLACK)
        phi_in_neuron.move_to(neuron.get_center())
        
        self.play(Write(phi_in_neuron))
        self.wait(1)
        
        # Output pulse
        output_pulse, output_glow = create_pulse(neuron.get_center(), output_arrow.get_end(), color=BLUE)
        self.add(output_pulse, output_glow)
        
        self.play(
            output_pulse.animate.move_to(output_label),
            output_glow.animate.move_to(output_label),
            neuron.animate.set_fill(BLUE, opacity=1),
            run_time=1.5
        )
        
        self.play(FadeOut(output_pulse), FadeIn(output_label) ,FadeOut(output_glow),FadeOut(VGroup(axes, step_formula, sigmoid_graph, step_title, x_label, y_label, y_label_neg1, y_label_pos1, step_graph, y_tick_neg2, y_tick_pos2)))
        self.wait(2)

        self.camera.frame.save_state()

        self.camera.frame.restore()
       

        # OR gate truth table: output is 1 when at least one input is 1
        table_data = [
            ["x_1", "x_2", "y"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "1"]
        ]
        
        # Create truth table with proper alignment
        table_group = VGroup()
        table_center_x = 6.6
        row_height = 0.54
        
        table_group.shift(DOWN*0.3)

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                cell_text = Tex(cell, font_size=22, color=WHITE)
                cell_x = table_center_x + (j - 1) * 0.67
                cell_y = 1.5 - i * row_height
                cell_text.move_to(RIGHT * cell_x + UP * cell_y)
                row_group.add(cell_text)
            table_group.add(row_group)
        
        # Scale up the entire table group
        table_group.scale(1.87).shift(RIGHT*2.69+DOWN*0.64)

        title = Text("OR Gate", weight=BOLD).next_to(table_group, UP, buff=0.69).set_color(GREEN_B).scale(1.3)
        self.play(ShowCreation(title))


        self.play(ShowCreation(table_group), self.camera.frame.animate.shift(RIGHT*9.9))
        
        self.wait(2)

        self.play(FadeOut(table_group),  FadeOut(title), self.camera.frame.animate.shift(LEFT*9.9))
        self.wait(2)

        weight_1 = Text("1").move_to(w1_label).scale(1.2)
        weight_2 = Text("1").move_to(w2_label).scale(1.2)
        bias = Text("0").move_to(bias_label).scale(1.2)

        self.play(
            ReplacementTransform(w1_label, weight_1),
            ReplacementTransform(w2_label, weight_2),
            ReplacementTransform(bias_label, bias),
        )

        self.wait(2)

        x1 = Text("1").move_to(x1_label).scale(1.2)
        x2 = Text("1").move_to(x2_label).scale(1.2)
        y = Text("1").move_to(output_label).scale(1.2)


        self.play(
            ReplacementTransform(x1_label, x1),
            ReplacementTransform(x2_label, x2),
        )




        # Information flow animation
        def create_pulse(start_point, end_point, color=YELLOW, duration=1.5):
            pulse = Dot(radius=0.2, color=color, fill_opacity=0.9)
            pulse.move_to(start_point)
            glow = Circle(radius=0.4, color=color, fill_opacity=0.4, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        pulse1, glow1 = create_pulse(input1.get_center(), neuron.get_center(), color=YELLOW)
        pulse2, glow2 = create_pulse(input2.get_center(), neuron.get_center(), color=ORANGE)
        pulse_bias, glow_bias = create_pulse(bias_arrow.get_start(), neuron.get_center(), color=PURPLE)
        
        self.add(pulse1, glow1, pulse2, glow2, pulse_bias, glow_bias)
        
        self.play(
            pulse1.animate.move_to(neuron.get_center()),
            glow1.animate.move_to(neuron.get_center()),
            pulse2.animate.move_to(neuron.get_center()),
            glow2.animate.move_to(neuron.get_center()),
            pulse_bias.animate.move_to(neuron.get_center()),
            glow_bias.animate.move_to(neuron.get_center()),
            run_time=2
        )
        
        self.play(
            neuron.animate.set_fill(YELLOW, opacity=1),
            FadeOut(pulse1), FadeOut(glow1),
            FadeOut(pulse2), FadeOut(glow2),
            FadeOut(pulse_bias), FadeOut(glow_bias),
            run_time=0.8
        )
        

        # Output pulse
        output_pulse, output_glow = create_pulse(neuron.get_center(), output_arrow.get_end(), color=BLUE)
        self.add(output_pulse, output_glow)
        
        self.play(
            output_pulse.animate.move_to(output_label),
            output_glow.animate.move_to(output_label),
            neuron.animate.set_fill(BLUE, opacity=1),
            run_time=1.5
        )
        
        self.play(FadeOut(output_pulse), FadeOut(output_glow),FadeOut(VGroup(axes, step_formula, sigmoid_graph, step_title, x_label, y_label, y_label_neg1, y_label_pos1, step_graph, y_tick_neg2, y_tick_pos2)))
        self.play(ReplacementTransform(output_label, y),)


        self.wait(2)



        self.play(
            Transform(x1, Text("0").scale(1.2).move_to(x1))
        )

        self.wait()

        self.play(
            Transform(x1, Text("1").scale(1.2).move_to(x1)),
            Transform(x2, Text("0").scale(1.2).move_to(x2)),
        )

        self.wait()

        self.play(
            Transform(x1, Text("0").scale(1.2).move_to(x1)),
            Transform(x2, Text("0").scale(1.2).move_to(x2)),
            Transform(y, Text("0").scale(1.2).move_to(y)),
        )


        self.wait(2)


        self.play(
            Transform(x1, Tex("x_1").scale(1.2).move_to(x1)),
            Transform(x2, Tex("x_2").scale(1.2).move_to(x2)),
            Transform(y, Tex("y").scale(1.2).move_to(y)),
            Transform(weight_1, Tex("w_1").scale(1.2).move_to(weight_1)),
            Transform(weight_2, Tex("w_2").scale(1.2).move_to(weight_2)),
            Transform(bias, Text("b").scale(1.2).move_to(bias)),
        )

        self.wait()


        self.camera.frame.save_state()
        self.camera.frame.restore()



        axes = Axes(
            x_range=[-0.4, 8, 0.1],
            y_range=[-0.4, 5.5, 0.1],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            },
        ).shift(LEFT * 12.7)

        # Add ticks at scaled positions (7 represents 1 on x, 4.5 represents 1 on y)
        x_tick = Line(axes.c2p(7, -0.2), axes.c2p(7, 0.2), stroke_width=4, color=WHITE)
        y_tick = Line(axes.c2p(-0.2, 4.5), axes.c2p(0.2, 4.5), stroke_width=4, color=WHITE)

        # Tick labels showing "1" 
        x_tick_label = Tex("1", font_size=36, color=WHITE).next_to(x_tick, DOWN, buff=0.2)
        y_tick_label = Tex("1", font_size=36, color=WHITE).next_to(y_tick, LEFT, buff=0.2)

        # Axis labels
        x1_label = Tex(r"x_1", font_size=48).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        x2_label = Tex(r"x_2", font_size=48).next_to(axes.y_axis.get_end(), UP, buff=0.2)
 
        # OR gate data points with proper scaling
        point_00 = Dot(axes.c2p(0, 0), radius=0.2, color=RED).set_color(RED)        # (0,0) → (0, 0)
        point_01 = Dot(axes.c2p(0, 4.5), radius=0.2, color=GREEN).set_color(GREEN)    # (0,1) → (0, 4.5)
        point_10 = Dot(axes.c2p(7, 0), radius=0.2, color=GREEN).set_color(GREEN)      # (1,0) → (7, 0)
        point_11 = Dot(axes.c2p(7, 4.5), radius=0.2, color=GREEN).set_color(GREEN)    # (1,1) → (7, 4.5)
        
        # Point labels
        label_00 = Tex("(0,0)", font_size=36, color=RED).next_to(point_00, DOWN+LEFT, buff=0.3)
        label_01 = Tex("(0,1)", font_size=36, color=GREEN).next_to(point_01, UP+LEFT, buff=0.3)
        label_10 = Tex("(1,0)", font_size=36, color=GREEN).next_to(point_10, DOWN+RIGHT, buff=0.3)
        label_11 = Tex("(1,1)", font_size=36, color=GREEN).next_to(point_11, UP+RIGHT, buff=0.3)
        
        # Linear separating line (separates (0,0) from others)
        line = Line(axes.c2p(-0.2, 3.25), axes.c2p(5.5, -0.2), stroke_width=6, color=YELLOW)
         
    

        
        # Animate creation
        self.play(ShowCreation(axes), self.camera.frame.animate.scale(1.15).shift(LEFT*12.1+DOWN*0.23))
        self.play(ShowCreation(x_tick), ShowCreation(y_tick))
        self.play(Write(x_tick_label), Write(y_tick_label))
        self.play(Write(x1_label), Write(x2_label))
        self.wait(1)
        
        # Add data points
        self.play(
            ShowCreation(point_00), Write(label_00),
            ShowCreation(point_01), Write(label_01),
            ShowCreation(point_10), Write(label_10),
            ShowCreation(point_11), Write(label_11)
        )
        self.wait(2)
        
        # Show separating line
        self.play(ShowCreation(line))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1/1.15).shift(RIGHT*12.1+UP*0.23))
        self.wait(2)



        # OR gate truth table: output is 1 when at least one input is 1
        table_data = [
            ["x_1", "x_2", "y"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "0"]
        ]
        
        # Create truth table with proper alignment
        table_group = VGroup()
        table_center_x = 6.6
        row_height = 0.54
        
        table_group.shift(DOWN*0.3)

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                cell_text = Tex(cell, font_size=22, color=WHITE)
                cell_x = table_center_x + (j - 1) * 0.67
                cell_y = 1.5 - i * row_height
                cell_text.move_to(RIGHT * cell_x + UP * cell_y)
                row_group.add(cell_text)
            table_group.add(row_group)
        
        # Scale up the entire table group
        table_group.scale(1.87).shift(RIGHT*2.69+DOWN*0.64)

        title = Text("X-OR Gate", weight=BOLD).next_to(table_group, UP, buff=0.69).set_color(PURPLE_B).scale(1.3)
        self.play(ShowCreation(title))


        self.play(ShowCreation(table_group), self.camera.frame.animate.shift(RIGHT*9.9))
        
        self.wait(2)

        self.play(FadeOut(table_group), FadeOut(title), self.camera.frame.animate.shift(LEFT*9.9))

        # Animate creation
        self.play(FadeOut(axes),run_time=0.02 )
        self.play(FadeOut(x_tick), FadeOut(y_tick),run_time=0.02 )
        self.play(FadeOut(x_tick_label), FadeOut(y_tick_label),run_time=0.02 )
        self.play(FadeOut(x1_label), FadeOut(x2_label),run_time=0.02 )        
        # Add data points
        self.play(
            FadeOut(point_00), FadeOut(label_00),
            FadeOut(point_01), FadeOut(label_01),
            FadeOut(point_10), FadeOut(label_10),
            FadeOut(point_11), FadeOut(label_11),run_time=0.02 
        ) 
        # Show separating line
        self.play(FadeOut(line))  

        
        self.wait()
        self.camera.frame.save_state()



        axes = Axes(
            x_range=[-0.4, 8, 0.1],
            y_range=[-0.4, 5.5, 0.1],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            },
        ).shift(LEFT * 12.7)

        # Add ticks at scaled positions (7 represents 1 on x, 4.5 represents 1 on y)
        x_tick = Line(axes.c2p(7, -0.2), axes.c2p(7, 0.2), stroke_width=4, color=WHITE)
        y_tick = Line(axes.c2p(-0.2, 4.5), axes.c2p(0.2, 4.5), stroke_width=4, color=WHITE)

        # Tick labels showing "1" 
        x_tick_label = Tex("1", font_size=36, color=WHITE).next_to(x_tick, DOWN, buff=0.2)
        y_tick_label = Tex("1", font_size=36, color=WHITE).next_to(y_tick, LEFT, buff=0.2)

        # Axis labels
        x1_label = Tex(r"x_1", font_size=48).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        x2_label = Tex(r"x_2", font_size=48).next_to(axes.y_axis.get_end(), UP, buff=0.2)
 
        # OR gate data points with proper scaling
        point_00 = Dot(axes.c2p(0, 0), radius=0.2, color=RED).set_color(RED)        # (0,0) → (0, 0)
        point_01 = Dot(axes.c2p(0, 4.5), radius=0.2, color=GREEN).set_color(GREEN)    # (0,1) → (0, 4.5)
        point_10 = Dot(axes.c2p(7, 0), radius=0.2, color=GREEN).set_color(GREEN)      # (1,0) → (7, 0)
        point_11 = Dot(axes.c2p(7, 4.5), radius=0.2, color=GREEN).set_color(RED)    # (1,1) → (7, 4.5)
        
        # Point labels
        label_00 = Tex("(0,0)", font_size=36, color=RED).next_to(point_00, DOWN+LEFT, buff=0.3)
        label_01 = Tex("(0,1)", font_size=36, color=GREEN).next_to(point_01, UP+LEFT, buff=0.3)
        label_10 = Tex("(1,0)", font_size=36, color=GREEN).next_to(point_10, DOWN+RIGHT, buff=0.3)
        label_11 = Tex("(1,1)", font_size=36, color=GREEN).next_to(point_11, UP+RIGHT, buff=0.3)
        
        # Linear separating line (separates (0,0) from others)
        line = Line(axes.c2p(-0.2, 3.25), axes.c2p(5.5, -0.2), stroke_width=6, color=YELLOW)
         
    
        # Animate creation
        self.play(ShowCreation(axes), self.camera.frame.animate.scale(1.15).shift(LEFT*12.1+DOWN*0.23))
        self.play(ShowCreation(x_tick), ShowCreation(y_tick))
        self.play(Write(x_tick_label), Write(y_tick_label))
        self.play(Write(x1_label), Write(x2_label))
        self.wait(1)
        
        # Add data points
        self.play(
            ShowCreation(point_00), Write(label_00),
            ShowCreation(point_01), Write(label_01),
            ShowCreation(point_10), Write(label_10),
            ShowCreation(point_11), Write(label_11)
        )
        self.wait(2)
        
        # Show separating line
        self.play(ShowCreation(line))
        self.wait(2)


        self.play(Transform(line, Line(axes.c2p(-0.4, 5.25), axes.c2p(3.5, -0.2), stroke_width=6, color=YELLOW) ))
        self.play(Transform(line, Line(axes.c2p(-0.4, 2.25), axes.c2p(7.5, 2.25), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(3.5, -0.4), axes.c2p(3.5, 5.2), stroke_width=6, color=YELLOW)))        
        self.play(Transform(line, Line(axes.c2p(1, -0.4), axes.c2p(6, 5.2), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(6, -0.4), axes.c2p(1, 5.2), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(-0.4, 3.5), axes.c2p(7.5, 3.5), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(-0.4, 1), axes.c2p(7.5, 1), stroke_width=6, color=YELLOW)))

        # Final frustrated attempt - make line blink/flash
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        


        # Two diagonal lines with extended ranges
        diag_line1 = Line(axes.c2p(-1, 5.5), axes.c2p(9, -0.8), stroke_width=6, color=YELLOW).shift(UP*0.34)
        diag_line2 = Line(axes.c2p(-0.8, 3.5), axes.c2p(7.5, -1.4), stroke_width=6, color=YELLOW)
        
        # Transform existing line into first diagonal line
        self.play(Transform(line, diag_line1), ShowCreation(diag_line2), run_time=1.5)
        self.wait(2)

        self.play(self.camera.frame.animate.restore())

        # Animate creation
        self.play(FadeOut(axes),run_time=0.02 )
        self.play(FadeOut(x_tick), FadeOut(y_tick),run_time=0.02 )
        self.play(FadeOut(x_tick_label), FadeOut(y_tick_label),run_time=0.02 )
        self.play(FadeOut(x1_label), FadeOut(x2_label),run_time=0.02 )        
        # Add data points
        self.play(
            FadeOut(point_00), FadeOut(label_00),
            FadeOut(point_01), FadeOut(label_01),
            FadeOut(point_10), FadeOut(label_10),
            FadeOut(point_11), FadeOut(label_11),run_time=0.02 
        ) 
        # Show separating line
        self.play(FadeOut(line))      
        self.wait(2)




        # Group all current neuron-related elements for shifting
        current_neuron_group = VGroup(
            neuron, phi_in_neuron, 
            output_arrow, y, 
            bias_arrow, bias
        )
        
        # Shift the entire group to the right
        self.play(
            Uncreate(line1), Uncreate(line2),
            Uncreate(weight_1), Uncreate(weight_2),
            run_time=1
        )

        self.play(current_neuron_group.animate.shift(RIGHT * 3), self.camera.frame.animate.shift(RIGHT))

        self.wait(1)
        
        # Create two hidden layer neurons with ReLU text
        hidden1 = Circle(radius=0.6, color=BLUE, fill_opacity=1, stroke_width=6, stroke_color=BLUE_B)
        hidden2 = Circle(radius=0.6, color=BLUE, fill_opacity=1, stroke_width=6, stroke_color=BLUE_B)
        hidden1.move_to(LEFT * 0.5 + UP * 1.2)
        hidden2.move_to(LEFT * 0.5 + DOWN * 1.2)
        
        # ReLU text inside hidden neurons (black color)
        relu1_text = Tex("ReLU", font_size=34, color=BLACK).move_to(hidden1.get_center()).set_color(BLACK)
        relu2_text = Tex("ReLU", font_size=34, color=BLACK).move_to(hidden2.get_center()).set_color(BLACK)
        
        # Change output neuron text to ReLU
        relu_output_text = Tex("ReLU", font_size=42, color=BLACK).move_to(neuron.get_center()).set_color(BLACK)
        
        self.play(
            GrowFromCenter(hidden1), GrowFromCenter(hidden2),
        )
        self.play(GrowFromCenter(relu1_text), GrowFromCenter(relu2_text), Transform(phi_in_neuron, relu_output_text))

        
        # Create connections from inputs to hidden layer
        line_x1_h1 = Line(input1.get_center(), hidden1.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_x1_h2 = Line(input1.get_center(), hidden2.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_x2_h1 = Line(input2.get_center(), hidden1.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_x2_h2 = Line(input2.get_center(), hidden2.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        
        # Create connections from hidden layer to output
        line_h1_out = Line(hidden1.get_center(), neuron.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_h2_out = Line(hidden2.get_center(), neuron.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        
        self.play(
            ShowCreation(line_x1_h1), ShowCreation(line_x1_h2),
            ShowCreation(line_x2_h1), ShowCreation(line_x2_h2),
            ShowCreation(line_h1_out), ShowCreation(line_h2_out)
        )
        
        # Add bias arrows for hidden layer
        bias_arrow_h1 = Arrow(UP * 3 + LEFT * 0.5, hidden1.get_top() + UP * 0.1, stroke_width=3, color=PURPLE).set_color(PURPLE)
        bias_arrow_h2 = Arrow(DOWN * 3 + LEFT * 0.5, hidden2.get_bottom() + DOWN * 0.1, stroke_width=3, color=PURPLE).set_color(PURPLE)
        
        self.play(ShowCreation(bias_arrow_h1), ShowCreation(bias_arrow_h2), self.camera.frame.animate.shift(DOWN*0.25).scale(1.02))
        
        # XOR solution weights and biases
        # Hidden layer 1: w1=1, w2=1, b=-0.5 (OR gate)
        # Hidden layer 2: w1=1, w2=1, b=-1.5 (AND gate with high threshold)
        # Output layer: w1=1, w2=-2, b=0 (h1 - 2*h2)
        
        # Weight labels for input to hidden layer 1
        w11_label = Text("1", font_size=32, color=RED).move_to(line_x1_h1.get_center() + UP * 0.3 + LEFT * 0.2)
        w21_label = Text("1", font_size=32, color=RED).move_to(line_x2_h1.get_center() + DOWN * 0.3 + LEFT * 0.2).shift(DOWN*0.13+RIGHT*0.1)
        
        # Weight labels for input to hidden layer 2  
        w12_label = Text("1", font_size=32, color=RED).move_to(line_x1_h2.get_center() + DOWN * 0.3 + LEFT * 0.2).shift(LEFT*0.13+UP*0.26)
        w22_label = Text("1", font_size=32, color=RED).move_to(line_x2_h2.get_center() + UP * 0.3 + LEFT * 0.2)
        
        # Weight labels for hidden to output
        w_h1_out = Text("1", font_size=32, color=RED).move_to(line_h1_out.get_center() + UP * 0.3)
        w_h2_out = Text("-2", font_size=32, color=RED).move_to(line_h2_out.get_center() + DOWN * 0.3)
        
        # Bias labels
        b1_label = Text("0", font_size=52, color=PURPLE).next_to(bias_arrow_h1.get_start(), UP, buff=0.2)
        b2_label = Text("-1", font_size=52, color=PURPLE).next_to(bias_arrow_h2.get_start(), DOWN, buff=0.2)
        
        # Transform output bias to number
        output_bias_label = Text("0", font_size=52, color=PURPLE).move_to(bias.get_center())
        
        self.play(
            Write(w11_label), Write(w21_label),
            Write(w12_label), Write(w22_label),
            Write(w_h1_out), Write(w_h2_out),
            Write(b1_label), Write(b2_label),
            Transform(bias, output_bias_label)
        )

        self.wait(2)

        self.camera.frame.save_state()
        
        self.play(
            Transform(x1, Text("1", font_size=60).move_to(x1)),
            Transform(x2, Text("1", font_size=60).move_to(x2)),
            )
        
        self.wait(2)

        # Data flow animation for multi-layer perceptron
        def create_pulse(start_point, end_point, color=YELLOW, duration=1.5):
            pulse = Dot(radius=0.15, color=color, fill_opacity=0.9)
            pulse.move_to(start_point)
            glow = Circle(radius=0.3, color=color, fill_opacity=0.3, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        # Create pulses from inputs to hidden layer
        pulse_x1_h1, glow_x1_h1 = create_pulse(input1.get_center(), hidden1.get_center(), color=YELLOW)
        pulse_x1_h2, glow_x1_h2 = create_pulse(input1.get_center(), hidden2.get_center(), color=YELLOW)
        pulse_x2_h1, glow_x2_h1 = create_pulse(input2.get_center(), hidden1.get_center(), color=ORANGE)
        pulse_x2_h2, glow_x2_h2 = create_pulse(input2.get_center(), hidden2.get_center(), color=ORANGE)
        
        # Create bias pulses for hidden layer
        pulse_bias_h1, glow_bias_h1 = create_pulse(bias_arrow_h1.get_start(), hidden1.get_center(), color=PURPLE)
        pulse_bias_h2, glow_bias_h2 = create_pulse(bias_arrow_h2.get_start(), hidden2.get_center(), color=PURPLE)
        
        # Add all input pulses
        self.add(pulse_x1_h1, glow_x1_h1, pulse_x1_h2, glow_x1_h2,
                 pulse_x2_h1, glow_x2_h1, pulse_x2_h2, glow_x2_h2,
                 pulse_bias_h1, glow_bias_h1, pulse_bias_h2, glow_bias_h2)
        
        # Animate pulses moving to hidden layer
        self.play(
            pulse_x1_h1.animate.move_to(hidden1.get_center()),
            glow_x1_h1.animate.move_to(hidden1.get_center()),
            pulse_x2_h1.animate.move_to(hidden1.get_center()),
            glow_x2_h1.animate.move_to(hidden1.get_center()),
            pulse_bias_h1.animate.move_to(hidden1.get_center()),
            glow_bias_h1.animate.move_to(hidden1.get_center()),
            
            pulse_x1_h2.animate.move_to(hidden2.get_center()),
            glow_x1_h2.animate.move_to(hidden2.get_center()),
            pulse_x2_h2.animate.move_to(hidden2.get_center()),
            glow_x2_h2.animate.move_to(hidden2.get_center()),
            pulse_bias_h2.animate.move_to(hidden2.get_center()),
            glow_bias_h2.animate.move_to(hidden2.get_center()),
            run_time=1.2
        )
        
        # Hidden layer neurons activate
        self.play(
            hidden1.animate.set_fill(YELLOW, opacity=1),
            hidden2.animate.set_fill(YELLOW, opacity=1),
            FadeOut(pulse_x1_h1), FadeOut(glow_x1_h1),
            FadeOut(pulse_x2_h1), FadeOut(glow_x2_h1),
            FadeOut(pulse_bias_h1), FadeOut(glow_bias_h1),
            FadeOut(pulse_x1_h2), FadeOut(glow_x1_h2),
            FadeOut(pulse_x2_h2), FadeOut(glow_x2_h2),
            FadeOut(pulse_bias_h2), FadeOut(glow_bias_h2),
            run_time=0.8
        )
        
        self.wait(1)
        
        # Create pulses from hidden layer to output
        pulse_h1_out, glow_h1_out = create_pulse(hidden1.get_center(), neuron.get_center(), color=GREEN)
        pulse_h2_out, glow_h2_out = create_pulse(hidden2.get_center(), neuron.get_center(), color=GREEN)
        
        # Create output bias pulse
        pulse_bias_out, glow_bias_out = create_pulse(bias_arrow.get_start(), neuron.get_center(), color=PURPLE)
        
        # Add output pulses
        self.add(pulse_h1_out, glow_h1_out, pulse_h2_out, glow_h2_out,
                 pulse_bias_out, glow_bias_out)
        
        # Animate pulses moving to output
        self.play(
            pulse_h1_out.animate.move_to(neuron.get_center()),
            glow_h1_out.animate.move_to(neuron.get_center()),
            pulse_h2_out.animate.move_to(neuron.get_center()),
            glow_h2_out.animate.move_to(neuron.get_center()),
            pulse_bias_out.animate.move_to(neuron.get_center()),
            glow_bias_out.animate.move_to(neuron.get_center()),
            run_time=1.2
        )
        
        # Output neuron activates and hidden layers return to blue
        self.play(
            neuron.animate.set_fill(YELLOW, opacity=1),
            hidden1.animate.set_fill(BLUE, opacity=1),
            hidden2.animate.set_fill(BLUE, opacity=1),
            FadeOut(pulse_h1_out), FadeOut(glow_h1_out),
            FadeOut(pulse_h2_out), FadeOut(glow_h2_out),
            FadeOut(pulse_bias_out), FadeOut(glow_bias_out),
            run_time=0.8
        )
        
        # Show final output value
        self.play(Transform(y, Text("0", font_size=60, color=GREEN).move_to(y)))
        
        # Reset neuron back to blue
        self.play(neuron.animate.set_fill(BLUE, opacity=1))
        

        h1_eq = Tex(r"h_1 \ = \ ReLU(1 \cdot x_1 + 1 \cdot x_2 + 0)", font_size=54).shift(RIGHT*12.33+UP*0.8)
        
        # Hidden layer 2 equation  
        h2_eq = Tex(r"h_2 \  =  ReLU(1 \cdot x_1 + 1 \cdot x_2 + (-1))", font_size=54)
        h2_eq.next_to(h1_eq, DOWN, buff=0.8)

        self.play(
          Write(h1_eq),
          Write(h2_eq), 
          self.camera.frame.animate.shift(RIGHT*12)
                      )
        
        self.wait(2)

        self.play(
            Transform(h1_eq,  Tex(r"h_1 \ = \ ReLU(1 \cdot 1 + 1 \cdot 1 + 0)", font_size=54).move_to(h1_eq)),
            Transform(h2_eq, Tex(r"h_2 \  =  ReLU(1 \cdot 1 + 1 \cdot 1 + (-1))", font_size=54).move_to(h2_eq)),
        )

        self.wait(2)

        self.play(
            Transform(h1_eq,  Tex(r"h_1 \ = \ 2", font_size=74).move_to(h1_eq)),
            Transform(h2_eq, Tex(r"h_2 \  = \ 1", font_size=74).move_to(h2_eq)),
        )

        self.play()

        hhh = Tex(r"y \ = \ ReLU(1 \cdot h_1 + (-2) \cdot h_2 + 0)", font_size=54).move_to(Group(h1_eq, h2_eq))

        self.play(ReplacementTransform(VGroup(h1_eq, h2_eq), hhh))

        self.wait(2)

        self.play(Transform(hhh, Tex(r"y \ = \ ReLU(1 \cdot 2 + (-2) \cdot 1 + 0)", font_size=74).move_to(hhh)))

        self.wait(2)

        self.play(Transform(hhh, Tex(r"y \ = \ 0", font_size=94).move_to(hhh)))
        self.wait(2)
        

        self.play(FadeOut(hhh), self.camera.frame.animate.restore())

        self.wait(2)

        self.play(
            Transform(x1, Text("1", font_size=60).move_to(x1)),
            Transform(x2, Text("0", font_size=60).move_to(x2)),
            Transform(y, Text("1", font_size=60).move_to(y)),
            
            )
        self.wait()
    
        self.play(
            Transform(x1, Text("0", font_size=60).move_to(x1)),
            Transform(x2, Text("0", font_size=60).move_to(x2)),
            Transform(y, Text("0", font_size=60).move_to(y)),
            
            )
        

        self.wait(2)



class NeuralNetworkFlow(Scene):
    def construct(self):
        self.camera.frame.scale(1.18)
        
        # Create 5 input layer nodes (GREEN, radius=0.36)
        input_layer = []
        input_labels = []
        for i in range(5):
            node = Circle(radius=0.36, color=GREEN, fill_opacity=1, stroke_width=6, stroke_color=GREEN_B)
            node.move_to(LEFT * 6 + UP * (2.5 - i * 1.2))
            input_layer.append(node)
            
            # Add input labels with black color
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK).scale(0.7)
            label.move_to(node.get_center())
            input_labels.append(label)
        
        # Create hidden layer 1 with 4 neurons
        hidden_layer1 = []
        hidden_labels1 = []
        for i in range(4):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(LEFT * 3 + UP * (2.4 - i * 1.6))
            hidden_layer1.append(node)
            
            # Standard notation: A(Z^[1]_i)
            label = Tex(f"A(Z^{{[1]}}_{{{i+1}}})").set_color(BLACK).scale(0.45)
            label.move_to(node.get_center())
            hidden_labels1.append(label)
        
        # Create hidden layer 2 with 5 neurons (reduced from 6)
        hidden_layer2 = []
        hidden_labels2 = []
        for i in range(5):  # Changed from 6 to 5
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(ORIGIN + UP * (3.2 - i * 1.6))  # Adjusted positioning for 5 neurons
            hidden_layer2.append(node)
            
            # Standard notation: A(Z^[2]_i)
            label = Tex(f"A(Z^{{[2]}}_{{{i+1}}})").set_color(BLACK).scale(0.45)
            label.move_to(node.get_center())
            hidden_labels2.append(label)
        
        # Create hidden layer 3 with 3 neurons
        hidden_layer3 = []
        hidden_labels3 = []
        for i in range(3):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(RIGHT * 3 + UP * (1.6 - i * 1.6))
            hidden_layer3.append(node)
            
            # Standard notation: A(Z^[3]_i)
            label = Tex(f"A(Z^{{[3]}}_{{{i+1}}})").set_color(BLACK).scale(0.45)
            label.move_to(node.get_center())
            hidden_labels3.append(label)
        
        # Create output layer
        output_node = Circle(radius=0.72, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 6)
        
        # Add output label scaled by 1.8
        output_label = Tex("\\hat{y}").set_color(BLACK).scale(1.8)
        output_label.move_to(output_node.get_center())
        
        # Create all connections
        connections = []
        
        # Input to Hidden Layer 1
        for input_node in input_layer:
            for hidden_node in hidden_layer1:
                line = Line(input_node.get_center(), hidden_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)
        
        # Hidden Layer 1 to Hidden Layer 2
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                line = Line(h1_node.get_center(), h2_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)
        
        # Hidden Layer 2 to Hidden Layer 3
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                line = Line(h2_node.get_center(), h3_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)
        
        # Hidden Layer 3 to Output
        for h3_node in hidden_layer3:
            line = Line(h3_node.get_center(), output_node.get_center(), 
                      stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
            connections.append(line)
        
        # Store original line properties (ADD THIS RIGHT AFTER CREATING CONNECTIONS)
        original_stroke_widths = [line.stroke_width for line in connections]
        original_colors = [line.get_color() for line in connections]
        
        # Show the network structure
        all_nodes = input_layer + hidden_layer1 + hidden_layer2 + hidden_layer3 + [output_node]
        
        self.play(*[ShowCreation(node) for node in all_nodes])
        self.play(*[ShowCreation(line) for line in connections])
        self.wait(1.5)

        # Write input labels first
        self.play(*[Write(label) for label in input_labels])
        self.wait(1)
        
        # Enhanced pulse creation function
        def create_pulse(start_point, color):
            pulse = Dot(radius=0.12, color=color, fill_opacity=1)
            pulse.move_to(start_point)
            glow = Circle(radius=0.25, color=color, fill_opacity=0.3, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        # SINGLE ITERATION WITH ONE PULSE PER WEIGHT CONNECTION
        
        # Stage 1: Input to Hidden Layer 1 (5×4 = 20 pulses)
        input_pulses = []
        input_glows = []

        # Get the specific connections for this stage
        input_to_h1_connections = []
        for input_node in input_layer:
            for h1_node in hidden_layer1:
                for line in connections:
                    start_pos = line.get_start()
                    input_pos = input_node.get_center()
                    h1_pos = h1_node.get_center()
                    if (abs(start_pos[0] - input_pos[0]) < 0.1 and abs(start_pos[1] - input_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h1_pos[0]) < 0.1 and abs(end_pos[1] - h1_pos[1]) < 0.1):
                            input_to_h1_connections.append(line)

        for input_node in input_layer:
            for h1_node in hidden_layer1:
                pulse, glow = create_pulse(input_node.get_center(), "#ff0000")
                input_pulses.append(pulse)
                input_glows.append(glow)
                self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move each pulse along its specific weight connection AND color the connections
        h1_animations = []
        for i, (pulse, glow) in enumerate(zip(input_pulses, input_glows)):
            input_idx = i // len(hidden_layer1)
            h1_idx = i % len(hidden_layer1)
            target_pos = hidden_layer1[h1_idx].get_center()
            
            h1_animations.extend([
                pulse.animate.move_to(target_pos),
                glow.animate.move_to(target_pos)
            ])

        # Add connection coloring animations
        for line in input_to_h1_connections:
            h1_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*h1_animations, run_time=1.5)
        
        # Fade out and write h1 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in input_pulses])
        reset_animations.extend([FadeOut(glow) for glow in input_glows])
        reset_animations.extend([Write(label) for label in hidden_labels1])

        # Reset connection colors and widths
        for line in input_to_h1_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        # Stage 2: Hidden Layer 1 to Hidden Layer 2 (4×5 = 20 pulses)
        h1_pulses = []
        h1_glows = []

        # Get the specific connections for this stage
        h1_to_h2_connections = []
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                for line in connections:
                    start_pos = line.get_start()
                    h1_pos = h1_node.get_center()
                    h2_pos = h2_node.get_center()
                    if (abs(start_pos[0] - h1_pos[0]) < 0.1 and abs(start_pos[1] - h1_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h2_pos[0]) < 0.1 and abs(end_pos[1] - h2_pos[1]) < 0.1):
                            h1_to_h2_connections.append(line)
        
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                pulse, glow = create_pulse(h1_node.get_center(), "#ff0000")
                h1_pulses.append(pulse)
                h1_glows.append(glow)
                self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move each pulse along its weight connection AND color the connections
        h2_animations = []
        for i, (pulse, glow) in enumerate(zip(h1_pulses, h1_glows)):
            h1_idx = i // len(hidden_layer2)
            h2_idx = i % len(hidden_layer2)
            target_pos = hidden_layer2[h2_idx].get_center()
            
            h2_animations.extend([
                pulse.animate.move_to(target_pos),
                glow.animate.move_to(target_pos)
            ])

        # Add connection coloring animations
        for line in h1_to_h2_connections:
            h2_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*h2_animations, run_time=1.5)
        
        # Fade out and write h2 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in h1_pulses])
        reset_animations.extend([FadeOut(glow) for glow in h1_glows])
        reset_animations.extend([Write(label) for label in hidden_labels2])

        # Reset connection colors and widths
        for line in h1_to_h2_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        # Stage 3: Hidden Layer 2 to Hidden Layer 3 (5×3 = 15 pulses)
        h2_pulses = []
        h2_glows = []

        # Get the specific connections for this stage
        h2_to_h3_connections = []
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                for line in connections:
                    start_pos = line.get_start()
                    h2_pos = h2_node.get_center()
                    h3_pos = h3_node.get_center()
                    if (abs(start_pos[0] - h2_pos[0]) < 0.1 and abs(start_pos[1] - h2_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h3_pos[0]) < 0.1 and abs(end_pos[1] - h3_pos[1]) < 0.1):
                            h2_to_h3_connections.append(line)
        
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                pulse, glow = create_pulse(h2_node.get_center(), "#ff0000")
                h2_pulses.append(pulse)
                h2_glows.append(glow)
                self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move each pulse along its weight connection AND color the connections
        h3_animations = []
        for i, (pulse, glow) in enumerate(zip(h2_pulses, h2_glows)):
            h2_idx = i // len(hidden_layer3)
            h3_idx = i % len(hidden_layer3)
            target_pos = hidden_layer3[h3_idx].get_center()
            
            h3_animations.extend([
                pulse.animate.move_to(target_pos),
                glow.animate.move_to(target_pos)
            ])

        # Add connection coloring animations
        for line in h2_to_h3_connections:
            h3_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*h3_animations, run_time=1.5)
        
        # Fade out and write h3 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in h2_pulses])
        reset_animations.extend([FadeOut(glow) for glow in h2_glows])
        reset_animations.extend([Write(label) for label in hidden_labels3])

        # Reset connection colors and widths
        for line in h2_to_h3_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        # Stage 4: Hidden Layer 3 to Output (3×1 = 3 pulses)
        h3_pulses = []
        h3_glows = []

        # Get the specific connections for this stage
        h3_to_output_connections = []
        for h3_node in hidden_layer3:
            for line in connections:
                start_pos = line.get_start()
                h3_pos = h3_node.get_center()
                output_pos = output_node.get_center()
                if (abs(start_pos[0] - h3_pos[0]) < 0.1 and abs(start_pos[1] - h3_pos[1]) < 0.1):
                    end_pos = line.get_end()
                    if (abs(end_pos[0] - output_pos[0]) < 0.1 and abs(end_pos[1] - output_pos[1]) < 0.1):
                        h3_to_output_connections.append(line)
        
        for h3_node in hidden_layer3:
            pulse, glow = create_pulse(h3_node.get_center(), "#ff0000")
            h3_pulses.append(pulse)
            h3_glows.append(glow)
            self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move to output AND color the connections
        output_animations = []
        for pulse, glow in zip(h3_pulses, h3_glows):
            output_animations.extend([
                pulse.animate.move_to(output_node.get_center()),
                glow.animate.move_to(output_node.get_center())
            ])

        # Add connection coloring animations
        for line in h3_to_output_connections:
            output_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*output_animations, run_time=1.5)
        
        # Fade out and write output label AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in h3_pulses])
        reset_animations.extend([FadeOut(glow) for glow in h3_glows])
        reset_animations.append(Write(output_label))

        # Reset connection colors and widths
        for line in h3_to_output_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        self.wait(3)

        self.camera.frame.save_state()
        self.camera.frame.restore()

        self.play(self.camera.frame.animate.scale(0.5).shift(LEFT*4))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT+UP*1.33).scale(0.8))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*3), run_time=3.6)

        self.wait()

        self.play(self.camera.frame.animate.shift(RIGHT*3+UP*3.8), run_time=2)
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*4.44), run_time=5)
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*3.7+UP*2.77))
        self.wait()
        self.play(self.camera.frame.animate.shift(DOWN), run_time=2)
        self.wait()

        self.play(self.camera.frame.animate.shift(RIGHT+UP*0.55))
        self.wait(2)

        self.play(self.camera.frame.animate.restore().scale(1.14).shift(DOWN*0.8))
        
        a = Text("Input layer", weight=BOLD).next_to(input_layer[4], DOWN).scale(1.2).shift(DOWN*0.45)
        b = Text("Hidden layers", weight=BOLD).next_to(hidden_layer2[4], DOWN).scale(1.3).shift(DOWN*0.55)
        c = Text("Output layer", weight=BOLD).next_to(output_node, DOWN).scale(1.15).shift(DOWN*0.44)

        self.play(ShowCreation(a), Write(b), Write(c))

        self.wait(2)

        self.play(self.camera.frame.animate.restore() , FadeOut(a), FadeOut(b), FadeOut(c))
        self.wait(2)

        import random

        # After self.play(*[ShowCreation(line) for line in connections])
        # Add random flickering effect
        flicker_colors = [YELLOW, GREEN, PURPLE, ORANGE, PINK, BLUE, RED, TEAL, DARK_BROWN, GREY_B]
        
        # Start random flickering
        for line in connections:
            line.add_updater(lambda mob: mob.set_color(random.choice(flicker_colors)))
        
        self.wait(10)  # Flicker for 10 seconds
        
        # Stop flickering and restore original colors
        for line, original in zip(connections, original_colors):
            line.clear_updaters()
            line.set_color(original)

        self.wait(2)

        # Add this code directly inside your construct() method after the forward propagation animation
        PURPLE_HEX = "#ff0000"
        PURE_GREEN_HEX = "#8A2BE2"
        
        # Organize connections by layer pairs for sequential animation
        layer_connections = []
        
        # Input to Hidden Layer 1 connections
        input_to_h1 = []
        for input_node in input_layer:
            for h1_node in hidden_layer1:
                for line in connections:
                    start_pos = line.get_start()
                    input_pos = input_node.get_center()
                    h1_pos = h1_node.get_center()
                    if (abs(start_pos[0] - input_pos[0]) < 0.1 and abs(start_pos[1] - input_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h1_pos[0]) < 0.1 and abs(end_pos[1] - h1_pos[1]) < 0.1):
                            input_to_h1.append(line)
        
        # Hidden Layer 1 to Hidden Layer 2 connections
        h1_to_h2 = []
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                for line in connections:
                    start_pos = line.get_start()
                    h1_pos = h1_node.get_center()
                    h2_pos = h2_node.get_center()
                    if (abs(start_pos[0] - h1_pos[0]) < 0.1 and abs(start_pos[1] - h1_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h2_pos[0]) < 0.1 and abs(end_pos[1] - h2_pos[1]) < 0.1):
                            h1_to_h2.append(line)
        
        # Hidden Layer 2 to Hidden Layer 3 connections
        h2_to_h3 = []
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                for line in connections:
                    start_pos = line.get_start()
                    h2_pos = h2_node.get_center()
                    h3_pos = h3_node.get_center()
                    if (abs(start_pos[0] - h2_pos[0]) < 0.1 and abs(start_pos[1] - h2_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h3_pos[0]) < 0.1 and abs(end_pos[1] - h3_pos[1]) < 0.1):
                            h2_to_h3.append(line)
        
        # Hidden Layer 3 to Output connections
        h3_to_output = []
        for h3_node in hidden_layer3:
            for line in connections:
                start_pos = line.get_start()
                h3_pos = h3_node.get_center()
                output_pos = output_node.get_center()
                if (abs(start_pos[0] - h3_pos[0]) < 0.1 and abs(start_pos[1] - h3_pos[1]) < 0.1):
                    end_pos = line.get_end()
                    if (abs(end_pos[0] - output_pos[0]) < 0.1 and abs(end_pos[1] - output_pos[1]) < 0.1):
                        h3_to_output.append(line)
        
        # Repeat forward-backward cycle 3 times
        for cycle in range(3):
            
            # FORWARD PROPAGATION - Layer by layer
            layer_groups = [input_to_h1, h1_to_h2, h2_to_h3, h3_to_output]
            
            for layer_lines in layer_groups:
                # Create pulses for this layer's connections
                layer_pulses = []
                layer_glows = []
                
                for line in layer_lines:
                    pulse, glow = create_pulse(line.get_start(), PURPLE_HEX)
                    layer_pulses.append(pulse)
                    layer_glows.append(glow)
                    self.add(pulse, glow)
                
                # Move pulses and change line properties simultaneously
                forward_animations = []
                for i, (pulse, glow, line) in enumerate(zip(layer_pulses, layer_glows, layer_lines)):
                    forward_animations.extend([
                        pulse.animate.move_to(line.get_end()),
                        glow.animate.move_to(line.get_end()),
                        line.animate.set_stroke(width=5, color=PURPLE_HEX)
                    ])
                
                self.play(*forward_animations, run_time=1.0)
                
                # Fade out pulses and reset line properties
                fadeout_animations = []
                for pulse, glow in zip(layer_pulses, layer_glows):
                    fadeout_animations.extend([FadeOut(pulse), FadeOut(glow)])
                
                for line in layer_lines:
                    line_idx = connections.index(line)
                    fadeout_animations.append(
                        line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                              color=original_colors[line_idx])
                    )
                
                self.play(*fadeout_animations, run_time=0.3)
            
            self.wait(0.5)
            
            # BACKPROPAGATION - Layer by layer (reverse order)
            reverse_layer_groups = [h3_to_output, h2_to_h3, h1_to_h2, input_to_h1]
            
            for layer_lines in reverse_layer_groups:
                # Create pulses for this layer's connections (starting from end)
                layer_pulses = []
                layer_glows = []
                
                for line in layer_lines:
                    pulse, glow = create_pulse(line.get_end(), PURE_GREEN_HEX)
                    layer_pulses.append(pulse)
                    layer_glows.append(glow)
                    self.add(pulse, glow)
                
                # Move pulses backward and change line properties
                backward_animations = []
                for pulse, glow, line in zip(layer_pulses, layer_glows, layer_lines):
                    backward_animations.extend([
                        pulse.animate.move_to(line.get_start()),
                        glow.animate.move_to(line.get_start()),
                        line.animate.set_stroke(width=6, color=PURE_GREEN_HEX)
                    ])
                
                self.play(*backward_animations, run_time=1.0)
                
                # Fade out pulses and reset line properties
                fadeout_animations = []
                for pulse, glow in zip(layer_pulses, layer_glows):
                    fadeout_animations.extend([FadeOut(pulse), FadeOut(glow)])
                
                for line in layer_lines:
                    line_idx = connections.index(line)
                    fadeout_animations.append(
                        line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                              color=original_colors[line_idx])
                    )
                
                self.play(*fadeout_animations, run_time=0.3)
            
            self.wait(0.5)
        
        self.wait(3)
