from manimlib import *
import numpy as np

from manimlib import *


class BackPropGeneral(Scene):
    def construct(self):
        self.camera.frame.scale(1.2).shift(RIGHT)

        # Create 5 input layer nodes (GREEN, radius=0.36)
        input_layer = []
        input_labels = []
        for i in range(5):
            node = Circle(radius=0.36, color=GREEN, fill_opacity=1, stroke_width=6, stroke_color=GREEN_B)
            node.move_to(LEFT * 6 + UP * (2.5 - i * 1.2))
            input_layer.append(node)

            # Add input labels with black color
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK)
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
            label = Tex(f"a^{{(1)}}_{{{i+1}}}").set_color(BLACK).scale(0.9)
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
            label = Tex(f"a^{{(2)}}_{{{i+1}}}").set_color(BLACK).scale(0.9)
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
            label = Tex(f"a^{{(3)}}_{{{i+1}}}").set_color(BLACK).scale(0.9)
            label.move_to(node.get_center())
            hidden_labels3.append(label)

        # Create output layer
        output_node = Circle(radius=0.72, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 6)

        # Add output label scaled by 1.8
        output_label = Tex("a_{1}^{(4)}").set_color(BLACK).scale(1.4)
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

        # Function to create glow effect around a dot
        def create_glow(center_point, radius=0.15, color=YELLOW, intensity=0.3):
            glow_group = VGroup()
            for i in range(20):
                glow_radius = radius * (1 + i * 0.1)
                opacity = intensity * (1 - i/20)
                glow_circle = Circle(
                    radius=glow_radius, 
                    stroke_opacity=0, 
                    fill_color=color,
                    fill_opacity=opacity
                ).move_to(center_point)
                glow_group.add(glow_circle)
            return glow_group

        # Enhanced pulse creation function
        def create_pulse(start_point, color="#ff0000"):
            # Create the main pulse dot
            pulse = Dot(radius=0.12, color=color, fill_opacity=1)
            pulse.move_to(start_point)

            # Create the enhanced glow effect
            glow = create_glow(start_point, radius=0.1, color=color, intensity=0.4)

            # Combine pulse and glow into a group
            pulse_group = VGroup(glow, pulse)
            return pulse_group

        # SINGLE ITERATION WITH ONE PULSE PER WEIGHT CONNECTION

        # Stage 1: Input to Hidden Layer 1 (5×4 = 20 pulses)
        input_pulses = []


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
                pulse_group = create_pulse(input_node.get_center(), "#ff0000")
                input_pulses.append(pulse_group)
                self.add(pulse_group)

        self.wait(0.3)

        # Move each pulse along its specific weight connection AND color the connections
        h1_animations = []
        for i, pulse_group in enumerate(input_pulses):
            input_idx = i // len(hidden_layer1)
            h1_idx = i % len(hidden_layer1)
            target_pos = hidden_layer1[h1_idx].get_center()

            h1_animations.append(pulse_group.animate.move_to(target_pos))


        # Add connection coloring animations
        for line in input_to_h1_connections:
            h1_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*h1_animations, run_time=1.5)

        # Fade out and write h1 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in input_pulses])
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
                pulse_group = create_pulse(h1_node.get_center(), "#ff0000")
                h1_pulses.append(pulse_group)
                self.add(pulse_group)

        self.wait(0.3)

        # Move each pulse along its weight connection AND color the connections
        h2_animations = []
        for i, pulse_group in enumerate(h1_pulses):
            h1_idx = i // len(hidden_layer2)
            h2_idx = i % len(hidden_layer2)
            target_pos = hidden_layer2[h2_idx].get_center()

            h2_animations.append(pulse_group.animate.move_to(target_pos))


        # Add connection coloring animations
        for line in h1_to_h2_connections:
            h2_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*h2_animations, run_time=1.5)

        # Fade out and write h2 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in h1_pulses])
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
                pulse_group = create_pulse(h2_node.get_center(), "#ff0000")
                h2_pulses.append(pulse_group)
                self.add(pulse_group)

        self.wait(0.3)

        # Move each pulse along its weight connection AND color the connections
        h3_animations = []
        for i, pulse_group in enumerate(h2_pulses):
            h2_idx = i // len(hidden_layer3)
            h3_idx = i % len(hidden_layer3)
            target_pos = hidden_layer3[h3_idx].get_center()

            h3_animations.append(pulse_group.animate.move_to(target_pos))


        # Add connection coloring animations
        for line in h2_to_h3_connections:
            h3_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*h3_animations, run_time=1.5)

        # Fade out and write h3 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in h2_pulses])
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
            pulse_group = create_pulse(h3_node.get_center(), "#ff0000")
            h3_pulses.append(pulse_group)
            self.add(pulse_group)

        self.wait(0.3)

        # Move to output AND color the connections
        output_animations = []
        for pulse_group in h3_pulses:
            output_animations.append(pulse_group.animate.move_to(output_node.get_center()))


        # Add connection coloring animations
        for line in h3_to_output_connections:
            output_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

        self.play(*output_animations, run_time=1.5)

        # Fade out and write output label AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse_group) for pulse_group in h3_pulses])
        reset_animations.append(Write(output_label))


        # Reset connection colors and widths
        for line in h3_to_output_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )


        self.play(*reset_animations, run_time=1.0)


        output_arrow = Arrow(output_node.get_right(), output_node.get_right()+RIGHT*1.5, stroke_width=4).set_color(WHITE)
        y_hat = Tex(r'\hat{y}').scale(2).next_to(output_arrow, RIGHT, buff=0.33)
        self.play(ShowCreation(output_arrow))
        self.play(ShowCreation(y_hat))

        self.wait(2)


        self.camera.frame.save_state()
        self.camera.frame.restore()


        self.play(self.camera.frame.animate.shift(RIGHT*5))


        temp = Tex(f"a^{{(l)}}_{{m}} \ = f(z^{{(l)}}_{{m}})").next_to(y_hat, RIGHT).shift(RIGHT*0.5)
        temp.scale(1.5).shift(RIGHT*0.89)
        self.play(ShowCreation(temp)) 
        rect  = SurroundingRectangle(temp, color=RED_D).scale(1.04)
        self.play(ShowCreation(rect))
        self.wait(2)
        self.play(FadeOut(temp), Uncreate(rect))


        loss_equation = Tex(r"L = \frac{1}{2}(\hat{y} - y)^2").next_to(y_hat, RIGHT).shift(RIGHT*1.12).scale(1.57)
        self.play(ShowCreation(loss_equation))
        rect  = SurroundingRectangle(loss_equation, color=RED_D).scale(1.04)
        self.play(ShowCreation(rect))
        self.wait(2)




        self.play(Indicate(output_node, color="#ff0000"))



        # Highlight with color and thickness change
        self.play(*[line.animate.set_stroke(width=8, color="#ff0000") for line in h3_to_output_connections])
        self.wait(1)
        # Reset back to original
        for line in h3_to_output_connections:
            line_idx = connections.index(line)
            self.play(line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                            color=original_colors[line_idx]), run_time=0.3)

        self.wait(2)



        weight_update = Tex(r"w_{1j}^{(4)} \leftarrow w_{1j}^{(4)} - \alpha \frac{\partial L}{\partial w_{1j}^{(4)}}").next_to(y_hat, RIGHT, buff=1.5).shift(UP*1.2).scale(1.65).shift(RIGHT*1.4)
        bias_update = Tex( r"b^{(4)} \leftarrow b^{(4)} - \alpha \frac{\partial L}{\partial b^{(4)}}").scale(1.65).next_to(weight_update, DOWN, buff=0.68)


        self.play(ShowCreation(weight_update), ShowCreation(bias_update), Uncreate(rect), FadeOut(loss_equation), self.camera.frame.animate.shift(RIGHT*6))


        self.wait(2)


        rect = SurroundingRectangle(weight_update).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(bias_update).scale(1.1)))
        self.wait(2)




        a = weight_update[-10:]  # Adjusted index for braces
        b = bias_update[-8:]     # Adjusted index for braces


        self.play(Uncreate(rect), FadeOut(weight_update[:-10]), FadeOut(bias_update[:-8]))        
        self.play(self.camera.frame.animate.shift(RIGHT*5.7))


        self.wait(2)



        weight_chain = Tex(
            r"\frac{\partial L}{\partial w_{1j}^{(4)}} = "
            r"\frac{\partial L}{\partial a_1^{(4)}} \cdot "
            r"\frac{\partial a_1^{(4)}}{\partial z_1^{(4)}} \cdot "
            r"\frac{\partial z_1^{(4)}}{\partial w_{1j}^{(4)}}"
        ).move_to(a).shift(RIGHT*1.04).scale(1.6)

        bias_chain = Tex(
            r"\frac{\partial L}{\partial b_1^{(4)}} = "
            r"\frac{\partial L}{\partial a_1^{(4)}} \cdot "
            r"\frac{\partial a_1^{(4)}}{\partial z_1^{(4)}} \cdot "
            r"\frac{\partial z_1^{(4)}}{\partial b_1^{(4)}}"
        ).next_to(weight_chain, DOWN, buff=0.88).scale(1.6)


        self.play(
            Transform(a, weight_chain),
            Transform(b, bias_chain)
        )


        self.wait(2)




        # 2️⃣ Solved Derivatives (in terms of f(z))
        weight_solved = Tex(
            r"\frac{\partial L}{\partial w_{1j}^{(4)}} = "
            r"(a_1^{(4)} - y) \cdot f'(z_1^{(4)}) \cdot a_j^{(3)}"
        ).move_to(a).scale(1.8)

        bias_solved = Tex(
             r"\frac{\partial L}{\partial b_1^{(4)}} = "
             r"(a_1^{(4)} - y) \cdot f'(z_1^{(4)})"
        ).next_to(weight_solved, DOWN, buff=0.88).scale(1.8)

        self.play(
            Transform(a, weight_solved),
            Transform(b, bias_solved)
        )
        self.wait(2)


        weight_chain = Tex(
            r"\frac{\partial L}{\partial w_{1j}^{(4)}} = "
            r"\frac{\partial L}{\partial a_1^{(4)}} \cdot "
            r"\frac{\partial a_1^{(4)}}{\partial z_1^{(4)}} \cdot "
            r"\frac{\partial z_1^{(4)}}{\partial w_{1j}^{(4)}}"
        ).move_to(a).scale(1.6)

        bias_chain = Tex(
            r"\frac{\partial L}{\partial b_1^{(4)}} = "
            r"\frac{\partial L}{\partial a_1^{(4)}} \cdot "
            r"\frac{\partial a_1^{(4)}}{\partial z_1^{(4)}} \cdot "
            r"\frac{\partial z_1^{(4)}}{\partial b_1^{(4)}}"
        ).next_to(weight_chain, DOWN, buff=0.88).scale(1.6)


        self.play(
            Transform(a, weight_chain),
            Transform(b, bias_chain)
        )


        self.wait(2)


        self.play(
            a[11:34].animate.set_color(RED),  # Adjusted index for braces
            b[10:33].animate.set_color(RED),  # Adjusted index for braces
        )


        self.wait(2)



        weight_chain = Tex(
            r"\frac{\partial L}{\partial w_{1j}^{(4)}} = "
            r"\frac{\partial L}{\partial z_{1}^{(4)}} \cdot "
            r"\frac{\partial z^{(4)}_{1}}{\partial w_{1j}^{(4)}}"
        ).move_to(a).scale(1.6)

        bias_chain = Tex(
            r"\frac{\partial L}{\partial b^{(4)}} = "
            r"\frac{\partial L}{\partial z_{1}^{(4)}} \cdot "
            r"\frac{\partial z^{(4)}_{1}}{\partial b^{(4)}}"
        ).next_to(weight_chain, DOWN, buff=0.88).scale(1.6)


        weight_chain.shift(UP*0.3)
        bias_chain.shift(DOWN*0.3)


        self.play(
            Transform(a, weight_chain),
            Transform(b, bias_chain)
        )


        self.wait(2)



        self.play(
            a[15:28].animate.set_color(RED),  # Adjusted index for braces  
            b[14:27].animate.set_color(RED),  # Adjusted index for braces
        )


        self.wait(2)



        self.play(Group(a,b).animate.shift(LEFT*3.5))


        z = Tex(r"z_{1}^{(4)} = \sum_{i=1}^{3} w_i^{(4)} \, f(z_i^{(3)}) + b^{(4)}").scale(1.14).next_to(Group(a,b), RIGHT, buff=0.85)


        self.play(ShowCreation(z))

        self.wait(2)

        self.play(Group(a,b).animate.shift(RIGHT*3.5), FadeOut(z))


        self.wait(1)



        weight_chain = Tex(
            r"\frac{\partial L}{\partial w_{1j}^{(4)}} = \delta_1^{(4)} \cdot a_j^{(3)}"        ).move_to(a).scale(1.6).shift(DOWN*0.4)

        bias_chain = Tex(
             r"\frac{\partial L}{\partial b_1^{(4)}} = \delta_1^{(4)}"
        ).next_to(weight_chain, DOWN, buff=1.28).scale(1.6)




        self.play(
            Transform(a, weight_chain),
            Transform(b, bias_chain)
        )


        self.play(
            a[24:36].animate.set_color(RED),  # Adjusted index for braces
            b[-15:].animate.set_color(RED)    # Adjusted index for braces
        )


        self.wait(2)


        self.play(FadeOut(Group(a,b)), self.camera.frame.animate.restore())
        self.wait()




        # BACKPROPAGATION ANIMATION WITH BRIGHT PURPLE PULSES

        # Create bright purple pulse starting at y_hat position
        backprop_pulse = create_pulse(y_hat.get_center(), "#9932CC")  # Bright purple
        self.add(backprop_pulse)
        self.wait(0.3)

        # Move pulse to output node while coloring arrow and y_hat the same purple color
        self.play(
            backprop_pulse.animate.move_to(output_node.get_center()),
            output_arrow.animate.set_color("#9932CC"),  # Color arrow purple
            y_hat.animate.set_color("#9932CC"),  # Color y_hat purple
            run_time=1.5
        )
        self.wait(0.3)

        # Create 2 additional copies at output node (original pulse + 2 copies = 3 total)
        additional_pulses = []
        for i in range(2):  # Create 2 additional copies
            pulse_copy = create_pulse(output_node.get_center(), "#9932CC")
            additional_pulses.append(pulse_copy)
            self.add(pulse_copy)

        # Combine original pulse with the 2 copies to get all 3 pulses
        all_3_pulses = [backprop_pulse] + additional_pulses

        # Move all 3 pulses to the 3 hidden layer 3 nodes AND permanently color the connections
        move_animations = []
        for i, pulse in enumerate(all_3_pulses):
            target_pos = hidden_layer3[i].get_center()
            move_animations.append(pulse.animate.move_to(target_pos))

        # Permanently color the connections from hidden layer 3 to output
        for line in h3_to_output_connections:
            move_animations.append(line.animate.set_stroke(width=5, color="#9932CC"))

        self.play(*move_animations, run_time=1.5)

        # Fade out all 3 pulses at hidden layer 3 nodes
        self.play(*[FadeOut(pulse) for pulse in all_3_pulses], run_time=1.0)

        self.wait(2)
        # Indicate all three nodes in the last hidden layer (hidden_layer3)
        for i in range(3):
            self.play(Indicate(hidden_layer3[i], color="#ff0000"), run_time=0.49)

        # Highlight hidden layer 2 to hidden layer 3 connections (5-3)
        self.play(*[line.animate.set_stroke(width=8, color="#ff0000") for line in h2_to_h3_connections])
        self.wait(1)
        # Reset back to original
        for line in h2_to_h3_connections:
            line_idx = connections.index(line)
            self.play(line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                            color=original_colors[line_idx]), run_time=0.1)

        self.wait(2)



        weight_update = Tex(r"w_{ij}^{(3)} \leftarrow w_{ij}^{(3)} - \alpha \frac{\partial L}{\partial w_{ij}^{(3)}}").next_to(y_hat, RIGHT, buff=1.5).shift(UP*1.2).scale(1.65).shift(RIGHT*1.4)
        bias_update = Tex(r"b_i^{(3)} \leftarrow b_i^{(3)} - \alpha \frac{\partial L}{\partial b_i^{(3)}}").scale(1.65).next_to(weight_update, DOWN, buff=0.68)


        self.play(ShowCreation(weight_update), ShowCreation(bias_update), self.camera.frame.animate.shift(RIGHT*10))       


        rect = SurroundingRectangle(weight_update).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(bias_update).scale(1.1)))
        self.wait(2)


        a = weight_update[-10:]  # Adjusted index for braces
        b = bias_update[-9:]     # Adjusted index for braces


        self.play(Uncreate(rect), FadeOut(weight_update[:-10]), FadeOut(bias_update[:-9]))        
        self.play(self.camera.frame.animate.shift(RIGHT*6.3))



        self.wait(2)



        weight_chain = Tex(
                r"\frac{\partial L}{\partial w_{ij}^{(3)}} = "
                r"\frac{\partial L}{\partial z_1^{(4)}} \cdot "
                r"\frac{\partial z_1^{(4)}}{\partial a_i^{(3)}} \cdot "
                r"\frac{\partial a_i^{(3)}}{\partial z_i^{(3)}} \cdot "
                r"\frac{\partial z_i^{(3)}}{\partial w_{ij}^{(3)}}"
        ).move_to(a).shift(RIGHT*0.74).scale(1.6)

        bias_chain = Tex(
                r"\frac{\partial L}{\partial b_i^{(3)}} = "
                r"\frac{\partial L}{\partial z_1^{(4)}} \cdot "
                r"\frac{\partial z_1^{(4)}}{\partial a_i^{(3)}} \cdot "
                r"\frac{\partial a_i^{(3)}}{\partial z_i^{(3)}} \cdot "
                r"\frac{\partial z_i^{(3)}}{\partial b_i^{(3)}}"
        ).next_to(weight_chain, DOWN, buff=0.88).scale(1.6)


        weight_chain.shift(UP*0.3)
        bias_chain.shift(DOWN*0.3)



        self.play(
            Transform(a, weight_chain),
            Transform(b, bias_chain)
        )


        self.wait(2)

        self.play(
            a[11:34].animate.set_color(RED),
            b[10:33].animate.set_color(RED),
        )

        self.wait(2)



        # 2️⃣ Expand derivatives into solved form (no direct delta_3 yet)
        weight_solved_L3 = Tex(
            r"\frac{\partial L}{\partial w_{ij}^{(3)}} = "
            r"(a_1^{(4)} - y) \cdot f'(z_1^{(4)}) \cdot "
            r"w_{1i}^{(4)} \cdot f'(z_i^{(3)}) \cdot a_j^{(2)}"
        ).move_to(a).scale(1.46).shift(DOWN*0.3)
        
        bias_solved_L3 = Tex(
            r"\frac{\partial L}{\partial b_i^{(3)}} = "
            r"(a_1^{(4)} - y) \cdot f'(z_1^{(4)}) \cdot "
            r"w_{1i}^{(4)} \cdot f'(z_i^{(3)})"
        ).next_to(weight_solved_L3, DOWN, buff=0.88).scale(1.46)
        
        # Slight positioning tweaks to align nicely
        bias_solved_L3.shift(DOWN*0.6)
        
        # Transform from chain rule form to expanded solved form
        self.play(
            Transform(a, weight_solved_L3),
            Transform(b, bias_solved_L3)
        )
        self.wait(2)
        


        # 3️⃣ Transformation introducing delta_4, delta_3, and final derivatives
        delta_4_def = Tex(
            r"\delta_1^{(4)} = (a_1^{(4)} - y) \cdot f'(z_1^{(4)})"
        ).scale(1.6).move_to(a).shift(UP*0.6)
        
        delta_3_def = Tex(
            r"\delta_i^{(3)} = f'(z_i^{(3)}) \cdot w_{1i}^{(4)} \cdot \delta_1^{(4)}"
        ).next_to(delta_4_def, DOWN, buff=1.1).scale(1.6)
        
        final_derivatives = Tex(
            r"\frac{\partial L}{\partial w_{ij}^{(3)}} = \delta_i^{(3)} \cdot a_j^{(2)}, \quad"
            r"\frac{\partial L}{\partial b_i^{(3)}} = \delta_i^{(3)}"
        ).next_to(delta_3_def, DOWN, buff=1.1).scale(1.6)
        
        # Animate stacking transformation
        self.play(
            ReplacementTransform(Group(a,b), Group(delta_3_def, delta_4_def, final_derivatives)),
        )

        rect = SurroundingRectangle(delta_4_def).scale(1.08)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(delta_3_def).scale(1.08)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(final_derivatives).scale(1.08)))
        self.wait(2)

        self.play(
            FadeOut(VGroup(rect, delta_3_def, delta_4_def, final_derivatives)),
            self.camera.frame.animate.restore())
        
        # BACKPROPAGATION FROM HIDDEN LAYER 3 TO HIDDEN LAYER 2
        # Create purple pulses on all 3 nodes of hidden_layer3, with 5 pulses per node (3×5 = 15 total)
        h3_backprop_pulses = []
        
        for h3_node in hidden_layer3:  # 3 nodes
            for h2_node in hidden_layer2:  # 5 nodes - create one pulse for each h2 node
                pulse_group = create_pulse(h3_node.get_center(), "#9932CC")  # Bright purple
                h3_backprop_pulses.append(pulse_group)
                self.add(pulse_group)
        
        self.wait(0.3)
        
        # Move all 15 pulses to their corresponding hidden_layer2 nodes AND color the connections
        backprop_animations = []
        
        # Group pulses by their destination (5 groups of 3 pulses each)
        for i, pulse_group in enumerate(h3_backprop_pulses):
            h3_idx = i // len(hidden_layer2)  # Which h3 node (0, 1, or 2)
            h2_idx = i % len(hidden_layer2)   # Which h2 node (0, 1, 2, 3, or 4)
            target_pos = hidden_layer2[h2_idx].get_center()
            backprop_animations.append(pulse_group.animate.move_to(target_pos))
        
        # Color all connections from hidden_layer2 to hidden_layer3 purple
        for line in h2_to_h3_connections:
            backprop_animations.append(line.animate.set_stroke(width=5, color="#9932CC"))
        
        self.play(*backprop_animations, run_time=1.5)
        
        # Fade out all pulses at hidden_layer2 nodes
        self.play(*[FadeOut(pulse) for pulse in h3_backprop_pulses], run_time=1.0)
        
        self.wait(2)
        
        # Indicate all five nodes in hidden_layer2
        for i in range(5):
            self.play(Indicate(hidden_layer2[i], color="#ff0000"), run_time=0.5)
        
        # Highlight hidden layer 1 to hidden layer 2 connections
        self.play(*[line.animate.set_stroke(width=8, color="#ff0000") for line in h1_to_h2_connections])
        self.wait(1)
        
        # Reset connections back to original
        for line in h1_to_h2_connections:
            line_idx = connections.index(line)
            self.play(line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                            color=original_colors[line_idx]), run_time=0.1)
        
        self.wait(2)
       

        




        # Path 1: RED path - Step by step creation
        # Step 1: Create red circle around first selected node in hidden layer 2 (index 0)
        h2_red_circle = Circle(
            radius=0.5,  # Same radius as hidden nodes
            color="#ff0000",
            fill_opacity=0,  # No fill
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h2_red_circle.move_to(hidden_layer2[0].get_center())
        self.play(ShowCreation(h2_red_circle))
        
        # Step 2: Create line from red h2 node to TOP node in hidden layer 3 (index 0)
        h2_to_h3_red_line1 = Line(
            hidden_layer2[0].get_center(),
            hidden_layer3[0].get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        self.play(ShowCreation(h2_to_h3_red_line1))
        
        # Step 3: Create red circle over the hidden layer 3 node (top)
        h3_red_circle1 = Circle(
            radius=0.5,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h3_red_circle1.move_to(hidden_layer3[0].get_center())
        self.play(ShowCreation(h3_red_circle1))
        
        # Step 4: Create line from h3 node to output
        h3_to_output_red_line1 = Line(
            hidden_layer3[0].get_center(),
            output_node.get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        self.play(ShowCreation(h3_to_output_red_line1))
        
        # Step 5: Create red circle over the final output
        output_red_circle = Circle(
            radius=0.72,  # Same radius as output node
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        output_red_circle.move_to(output_node.get_center())
        self.play(ShowCreation(output_red_circle))

        self.wait(2)
        
        # Continue with RED paths to the remaining 2 nodes in hidden layer 3
        # Create red line from same h2 node to MIDDLE node in hidden layer 3 (index 1)
        h2_to_h3_red_line2 = Line(
            hidden_layer2[0].get_center(),
            hidden_layer3[1].get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        self.play(ShowCreation(h2_to_h3_red_line2))
        
        # Create red line from same h2 node to BOTTOM node in hidden layer 3 (index 2)
        h2_to_h3_red_line3 = Line(
            hidden_layer2[0].get_center(),
            hidden_layer3[2].get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        self.play(ShowCreation(h2_to_h3_red_line3))
        
        # Create red circles over the remaining 2 nodes in hidden layer 3
        h3_red_circle2 = Circle(
            radius=0.5,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h3_red_circle2.move_to(hidden_layer3[1].get_center())
        
        h3_red_circle3 = Circle(
            radius=0.5,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h3_red_circle3.move_to(hidden_layer3[2].get_center())
        
        self.play(ShowCreation(h3_red_circle2), ShowCreation(h3_red_circle3))
        
        # Create red lines from the remaining 2 h3 nodes to output
        h3_to_output_red_line2 = Line(
            hidden_layer3[1].get_center(),
            output_node.get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        h3_to_output_red_line3 = Line(
            hidden_layer3[2].get_center(),
            output_node.get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        self.play(ShowCreation(h3_to_output_red_line2), ShowCreation(h3_to_output_red_line3))
        self.wait(2)
        
        # Fade out all the red path elements
        red_elements = [
            h2_red_circle,
            h2_to_h3_red_line1, h2_to_h3_red_line2, h2_to_h3_red_line3,
            h3_red_circle1, h3_red_circle2, h3_red_circle3,
            h3_to_output_red_line1, h3_to_output_red_line2, h3_to_output_red_line3,
            output_red_circle
        ]
        
        self.play(*[FadeOut(element) for element in red_elements], run_time=1.5)
        self.wait(2)


        # Step 1: Create red circle around third node in hidden layer 2 (index 2)
        h2_red_circle_3rd = Circle(
            radius=0.5,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h2_red_circle_3rd.move_to(hidden_layer2[2].get_center())
        self.play(ShowCreation(h2_red_circle_3rd))
        
        # Step 2: Create all three lines simultaneously from h2 node to all h3 nodes
        h2_to_h3_red_line1_3rd = Line(
            hidden_layer2[2].get_center(),
            hidden_layer3[0].get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        h2_to_h3_red_line2_3rd = Line(
            hidden_layer2[2].get_center(),
            hidden_layer3[1].get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        h2_to_h3_red_line3_3rd = Line(
            hidden_layer2[2].get_center(),
            hidden_layer3[2].get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        self.play(
            ShowCreation(h2_to_h3_red_line1_3rd),
            ShowCreation(h2_to_h3_red_line2_3rd),
            ShowCreation(h2_to_h3_red_line3_3rd)
        )
        
        # Step 3: Create all three circles simultaneously on all h3 nodes
        h3_red_circle1_3rd = Circle(
            radius=0.5,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h3_red_circle1_3rd.move_to(hidden_layer3[0].get_center())
        
        h3_red_circle2_3rd = Circle(
            radius=0.5,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h3_red_circle2_3rd.move_to(hidden_layer3[1].get_center())
        
        h3_red_circle3_3rd = Circle(
            radius=0.5,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        h3_red_circle3_3rd.move_to(hidden_layer3[2].get_center())
        
        self.play(
            ShowCreation(h3_red_circle1_3rd),
            ShowCreation(h3_red_circle2_3rd),
            ShowCreation(h3_red_circle3_3rd)
        )
        
        # Step 4: Create all three lines simultaneously from h3 nodes to output
        h3_to_output_red_line1_3rd = Line(
            hidden_layer3[0].get_center(),
            output_node.get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        h3_to_output_red_line2_3rd = Line(
            hidden_layer3[1].get_center(),
            output_node.get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        h3_to_output_red_line3_3rd = Line(
            hidden_layer3[2].get_center(),
            output_node.get_center(),
            stroke_width=6,
            color="#ff0000",
            z_index=-0.5
        )
        
        self.play(
            ShowCreation(h3_to_output_red_line1_3rd),
            ShowCreation(h3_to_output_red_line2_3rd),
            ShowCreation(h3_to_output_red_line3_3rd)
        )
        
        # Step 5: Create red circle over the final output
        output_red_circle_3rd = Circle(
            radius=0.72,
            color="#ff0000",
            fill_opacity=0,
            stroke_width=9,
            stroke_color="#ff0000",
            z_index=1
        )
        output_red_circle_3rd.move_to(output_node.get_center())
        self.play(ShowCreation(output_red_circle_3rd))
        
        self.wait(2)
        
        # Fade out all the red path elements for third node
        red_elements_3rd = [
            h2_red_circle_3rd,
            h2_to_h3_red_line1_3rd, h2_to_h3_red_line2_3rd, h2_to_h3_red_line3_3rd,
            h3_red_circle1_3rd, h3_red_circle2_3rd, h3_red_circle3_3rd,
            h3_to_output_red_line1_3rd, h3_to_output_red_line2_3rd, h3_to_output_red_line3_3rd,
            output_red_circle_3rd
        ]
        
        self.play(*[FadeOut(element) for element in red_elements_3rd], run_time=1.5)

        self.wait(2)


        a = Tex(
            r"\frac{\partial L}{\partial w_{ij}^{(2)}} = "
            r"\frac{\partial L}{\partial z_i^{(2)}} \cdot "
            r"\frac{\partial z_i^{(2)}}{\partial w_{ij}^{(2)}}"
        ).scale(1.6).next_to(y_hat, RIGHT).shift(RIGHT*5)

        self.play(self.camera.frame.animate.shift(RIGHT*17), ShowCreation(a))
        self.wait(2)

        self.play(a[11:20].animate.set_color(RED))
        self.wait(2)

        self.play(a.animate.shift(UP*2))

        b = Tex(
               r"\delta_i^{(2)} = \frac{\partial L}{\partial z_i^{(2)}} = "
               r"\left(\sum_{k=1}^{3} \frac{\partial L}{\partial z_k^{(3)}} "
               r"\frac{\partial z_k^{(3)}}{\partial a_i^{(2)}} \right) "
               r"\cdot \frac{\partial z_i^{(2)}}{\partial a_i^{(2)}}"
                    ).scale(1.4).next_to(a, DOWN, buff=0.9)
        
        self.play(TransformFromCopy(a[11:20], b[:15]))
        self.wait(2)

        self.play(TransformFromCopy(a[11:20], b[15:]))
        self.wait(2)

        brace = Brace(b[16:-14], DOWN, buff=0.5).set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        self.play(b[22:31].animate.set_color(RED))
        self.wait(2)


        self.play(Transform(b, Tex(r"\delta_i^{(2)} = \left(\sum_{k=1}^{3} \delta_k^{(3)} \, w_{ki}^{(3)} \right) "r"\cdot f'(z_i^{(2)})").scale(1.6).next_to(a, DOWN).shift(DOWN*0.65)), FadeOut(brace))
        self.wait(2)

        self.play(ReplacementTransform(b, a[11:20]))

        self.play(Transform(a, Tex(r"\frac{\partial L}{\partial w_{ij}^{(2)}} = \delta_i^{(2)} \cdot a_j^{(1)}").move_to(a).shift(DOWN*0.75).scale(1.7)))
        self.wait(2)

        b = Tex(r"\frac{\partial L}{\partial b_i^{(2)}} = \delta_i^{(2)}").next_to(a, DOWN, buff=0.86).scale(1.7)

        self.play(ShowCreation(b))

        self.wait(2)

        # 1️⃣ Delta for layer l
        delta_eq = Tex(
            r"\delta_i^{(l)} = \left( \sum_k \delta_k^{(l+1)} \, w_{ki}^{(l+1)} \right) \cdot f'(z_i^{(l)})"
        ).scale(1.4).next_to(a, UP).shift(LEFT*0.3+DOWN)
        
        # 2️⃣ Weight gradient for layer l
        weight_eq = Tex(
            r"\frac{\partial L}{\partial w_{ij}^{(l)}} = \delta_i^{(l)} \cdot a_j^{(l-1)}"
        ).scale(1.4)
        
        # 3️⃣ Bias gradient for layer l
        bias_eq = Tex(
            r"\frac{\partial L}{\partial b_i^{(l)}} = \delta_i^{(l)}"
        ).scale(1.4)
        
        # Position them stacked
        weight_eq.next_to(delta_eq, DOWN, buff=0.8)
        bias_eq.next_to(weight_eq, DOWN, buff=0.8)
                
        self.play(FadeOut(VGroup(a,b)), FadeIn(VGroup(delta_eq, weight_eq,bias_eq )))
                  
        rect = SurroundingRectangle(delta_eq).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(weight_eq).scale(1.1)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(bias_eq).scale(1.1)))
        self.wait(2)

        self.play(FadeOut(VGroup(delta_eq, weight_eq,bias_eq )), self.camera.frame.animate.restore())





        # BACKPROPAGATION FROM HIDDEN LAYER 2 TO HIDDEN LAYER 1
        # Create purple pulses on all 5 nodes of hidden_layer2, with 4 pulses per node (5×4 = 20 total)
        h2_backprop_pulses = []
        
        for h2_node in hidden_layer2:  # 5 nodes
            for h1_node in hidden_layer1:  # 4 nodes - create one pulse for each h1 node
                pulse_group = create_pulse(h2_node.get_center(), "#9932CC")  # Bright purple
                h2_backprop_pulses.append(pulse_group)
                self.add(pulse_group)
        
        self.wait(0.3)
        
        # Move all 20 pulses to their corresponding hidden_layer1 nodes AND color the connections
        backprop_h1_animations = []
        
        # Group pulses by their destination (4 groups of 5 pulses each)
        for i, pulse_group in enumerate(h2_backprop_pulses):
            h2_idx = i // len(hidden_layer1)  # Which h2 node (0, 1, 2, 3, or 4)
            h1_idx = i % len(hidden_layer1)   # Which h1 node (0, 1, 2, or 3)
            target_pos = hidden_layer1[h1_idx].get_center()
            backprop_h1_animations.append(pulse_group.animate.move_to(target_pos))
        
        # Color all connections from hidden_layer1 to hidden_layer2 purple
        for line in h1_to_h2_connections:
            backprop_h1_animations.append(line.animate.set_stroke(width=5, color="#9932CC"))
        
        self.play(*backprop_h1_animations, run_time=1.5)
        
        # Fade out all pulses at hidden_layer1 nodes
        self.play(*[FadeOut(pulse) for pulse in h2_backprop_pulses], run_time=1.0)
        
        
        # BACKPROPAGATION FROM HIDDEN LAYER 1 TO INPUT LAYER
        # Create purple pulses on all 4 nodes of hidden_layer1, with 5 pulses per node (4×5 = 20 total)
        h1_backprop_pulses = []
        
        for h1_node in hidden_layer1:  # 4 nodes
            for input_node in input_layer:  # 5 nodes - create one pulse for each input node
                pulse_group = create_pulse(h1_node.get_center(), "#9932CC")  # Bright purple
                h1_backprop_pulses.append(pulse_group)
                self.add(pulse_group)
        
        
        # Move all 20 pulses to their corresponding input_layer nodes AND color the connections
        backprop_input_animations = []
        
        # Group pulses by their destination (5 groups of 4 pulses each)
        for i, pulse_group in enumerate(h1_backprop_pulses):
            h1_idx = i // len(input_layer)  # Which h1 node (0, 1, 2, or 3)
            input_idx = i % len(input_layer)   # Which input node (0, 1, 2, 3, or 4)
            target_pos = input_layer[input_idx].get_center()
            backprop_input_animations.append(pulse_group.animate.move_to(target_pos))
        
        # Color all connections from input_layer to hidden_layer1 purple
        for line in input_to_h1_connections:
            backprop_input_animations.append(line.animate.set_stroke(width=5, color="#9932CC"))
        
        self.play(*backprop_input_animations, run_time=1.5)
        
        # Fade out all pulses at input_layer nodes
        self.play(*[FadeOut(pulse) for pulse in h1_backprop_pulses], run_time=1.0)
        

        loss1 = Text("Loss").next_to(y_hat, UP).shift(UP*2+LEFT*1.8).scale(2.58)
        rect = SurroundingRectangle(loss1, fill_color=RED, fill_opacity=0.25, color=RED).scale(1.1).set_z_index(-1)
        loss1.set_z_index(1)
        loss = VGroup(loss1, rect).next_to(output_node, DOWN).shift(DOWN*1.3+RIGHT*0.4)
        

        epoch = Text("Epoch = 1").scale(1.7).next_to(output_node, UP, ).shift(UP*1.45+RIGHT*0.3)
        self.play(ShowCreation(epoch))
        self.wait(2)

        self.play(Write(loss))
        self.wait(2)



        


        


                
        # CONTINUOUS FORWARD AND BACKWARD PROPAGATION LOOP
        for epoch_num in range(1, 5):  # Start from epoch 1, go to epoch 4 (4 iterations)
            # FORWARD PROPAGATION (RED FLASH ONLY - KEEP CURRENT COLORS)

            # Stage 1: Input to Hidden Layer 1
            input_pulses = []
            for input_node in input_layer:
                for h1_node in hidden_layer1:
                    pulse_group = create_pulse(input_node.get_center(), "#ff0000")
                    input_pulses.append(pulse_group)
                    self.add(pulse_group)


            h1_animations = []
            for i, pulse_group in enumerate(input_pulses):
                input_idx = i // len(hidden_layer1)
                h1_idx = i % len(hidden_layer1)
                target_pos = hidden_layer1[h1_idx].get_center()
                h1_animations.append(pulse_group.animate.move_to(target_pos))

            # Store CURRENT colors before flashing red
            current_colors_h1 = []
            current_widths_h1 = []
            for line in input_to_h1_connections:
                current_colors_h1.append(line.get_stroke_color())
                current_widths_h1.append(line.get_stroke_width())
                h1_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

            self.play(*h1_animations, run_time=1.0)

            # Fade pulses and reset to CURRENT colors
            reset_animations = []
            for pulse_group in input_pulses:
                reset_animations.append(FadeOut(pulse_group))
            for i, line in enumerate(input_to_h1_connections):
                reset_animations.append(
                    line.animate.set_stroke(width=current_widths_h1[i], color=current_colors_h1[i])
                )
            self.play(*reset_animations, run_time=0.5)

            # Stage 2: Hidden Layer 1 to Hidden Layer 2
            h1_pulses = []
            for h1_node in hidden_layer1:
                for h2_node in hidden_layer2:
                    pulse_group = create_pulse(h1_node.get_center(), "#ff0000")
                    h1_pulses.append(pulse_group)
                    self.add(pulse_group)


            h2_animations = []
            for i, pulse_group in enumerate(h1_pulses):
                h1_idx = i // len(hidden_layer2)
                h2_idx = i % len(hidden_layer2)
                target_pos = hidden_layer2[h2_idx].get_center()
                h2_animations.append(pulse_group.animate.move_to(target_pos))

            # Store CURRENT colors before flashing red
            current_colors_h2 = []
            current_widths_h2 = []
            for line in h1_to_h2_connections:
                current_colors_h2.append(line.get_stroke_color())
                current_widths_h2.append(line.get_stroke_width())
                h2_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

            self.play(*h2_animations, run_time=1.0)

            # Fade pulses and reset to CURRENT colors
            reset_animations = []
            for pulse_group in h1_pulses:
                reset_animations.append(FadeOut(pulse_group))
            for i, line in enumerate(h1_to_h2_connections):
                reset_animations.append(
                    line.animate.set_stroke(width=current_widths_h2[i], color=current_colors_h2[i])
                )
            self.play(*reset_animations, run_time=0.5)

            # Stage 3: Hidden Layer 2 to Hidden Layer 3
            h2_pulses = []
            for h2_node in hidden_layer2:
                for h3_node in hidden_layer3:
                    pulse_group = create_pulse(h2_node.get_center(), "#ff0000")
                    h2_pulses.append(pulse_group)
                    self.add(pulse_group)


            h3_animations = []
            for i, pulse_group in enumerate(h2_pulses):
                h2_idx = i // len(hidden_layer3)
                h3_idx = i % len(hidden_layer3)
                target_pos = hidden_layer3[h3_idx].get_center()
                h3_animations.append(pulse_group.animate.move_to(target_pos))

            # Store CURRENT colors before flashing red
            current_colors_h3 = []
            current_widths_h3 = []
            for line in h2_to_h3_connections:
                current_colors_h3.append(line.get_stroke_color())
                current_widths_h3.append(line.get_stroke_width())
                h3_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

            self.play(*h3_animations, run_time=1.0)

            # Fade pulses and reset to CURRENT colors
            reset_animations = []
            for pulse_group in h2_pulses:
                reset_animations.append(FadeOut(pulse_group))
            for i, line in enumerate(h2_to_h3_connections):
                reset_animations.append(
                    line.animate.set_stroke(width=current_widths_h3[i], color=current_colors_h3[i])
                )
            self.play(*reset_animations, run_time=0.5)

            # Stage 4: Hidden Layer 3 to Output
            h3_pulses = []
            for h3_node in hidden_layer3:
                pulse_group = create_pulse(h3_node.get_center(), "#ff0000")
                h3_pulses.append(pulse_group)
                self.add(pulse_group)


            output_animations = []
            for pulse_group in h3_pulses:
                output_animations.append(pulse_group.animate.move_to(output_node.get_center()))

            # Store CURRENT colors before flashing red
            current_colors_output = []
            current_widths_output = []
            for line in h3_to_output_connections:
                current_colors_output.append(line.get_stroke_color())
                current_widths_output.append(line.get_stroke_width())
                output_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))

            self.play(*output_animations, run_time=1.0)

            # Fade pulses and reset to CURRENT colors
            reset_animations = []
            for pulse_group in h3_pulses:
                reset_animations.append(FadeOut(pulse_group))
            for i, line in enumerate(h3_to_output_connections):
                reset_animations.append(
                    line.animate.set_stroke(width=current_widths_output[i], color=current_colors_output[i])
                )
            self.play(*reset_animations, run_time=0.5)

            # Stage 5: Output to Y_HAT (FORWARD PROPAGATION FINAL STAGE)
            # Create pulse from output node to y_hat
            output_to_yhat_pulse = create_pulse(output_node.get_center(), "#ff0000")
            self.add(output_to_yhat_pulse)


            # Store current arrow and y_hat colors
            current_arrow_color = output_arrow.get_stroke_color()
            current_yhat_color = y_hat.get_color()

            # Move pulse to y_hat and color arrow + y_hat RED
            forward_final_animations = []
            forward_final_animations.append(output_to_yhat_pulse.animate.move_to(y_hat.get_center()))
            forward_final_animations.append(output_arrow.animate.set_color("#ff0000"))
            forward_final_animations.append(y_hat.animate.set_color("#ff0000"))

            self.play(*forward_final_animations, run_time=1.0)

            # Fade pulse and reset arrow + y_hat to current colors
            forward_reset_animations = []
            forward_reset_animations.append(FadeOut(output_to_yhat_pulse))
            forward_reset_animations.append(output_arrow.animate.set_stroke(color=current_arrow_color))
            forward_reset_animations.append(y_hat.animate.set_color(current_yhat_color))

            self.play(*forward_reset_animations, run_time=0.5)

            # BACKWARD PROPAGATION WITH DIFFERENT COLORS - WEIGHTS STAY COLORED
            backprop_colors = ["#FFFF00", "#00FF00", "#8B4513", "#FF69B4"]  # Bright Yellow, Pure Green, Maroon, Pink
            backprop_color = backprop_colors[epoch_num - 1]  # Use different color for each epoch

            # Stage 1: Y_HAT to Output (BACKWARD PROPAGATION STARTING STAGE)
            # Create pulse from y_hat to output node
            yhat_to_output_pulse = create_pulse(y_hat.get_center(), backprop_color)
            self.add(yhat_to_output_pulse)

            self.wait(0.2)

            # Move pulse from y_hat to output node and color arrow + y_hat with backprop color
            backprop_start_animations = []
            backprop_start_animations.append(yhat_to_output_pulse.animate.move_to(output_node.get_center()))
            backprop_start_animations.append(output_arrow.animate.set_color(backprop_color))
            backprop_start_animations.append(y_hat.animate.set_color(backprop_color))

            self.play(*backprop_start_animations, run_time=1.0)

            # Fade pulse but KEEP arrow and y_hat colored
            self.play(FadeOut(yhat_to_output_pulse), run_time=0.5)

            # Stage 2: Output to Hidden Layer 3
            output_backprop_pulses = []
            for h3_node in hidden_layer3:
                pulse_group = create_pulse(output_node.get_center(), backprop_color)
                output_backprop_pulses.append(pulse_group)
                self.add(pulse_group)

            self.wait(0.2)

            # Move pulses and COLOR WEIGHTS (don't reset them back)
            h3_backprop_animations = []
            for i, pulse_group in enumerate(output_backprop_pulses):
                target_pos = hidden_layer3[i].get_center()
                h3_backprop_animations.append(pulse_group.animate.move_to(target_pos))

            for line in h3_to_output_connections:
                h3_backprop_animations.append(line.animate.set_stroke(width=5, color=backprop_color))

            self.play(*h3_backprop_animations, run_time=1.0)

            # Only fade pulses, KEEP weight colors
            fade_animations = [FadeOut(pulse) for pulse in output_backprop_pulses]
            self.play(*fade_animations, run_time=0.5)

            # Stage 3: Hidden Layer 3 to Hidden Layer 2
            h3_backprop_pulses = []
            for h3_node in hidden_layer3:
                for h2_node in hidden_layer2:
                    pulse_group = create_pulse(h3_node.get_center(), backprop_color)
                    h3_backprop_pulses.append(pulse_group)
                    self.add(pulse_group)

            self.wait(0.2)

            # Move pulses and COLOR WEIGHTS
            h2_backprop_animations = []
            for i, pulse_group in enumerate(h3_backprop_pulses):
                h3_idx = i // len(hidden_layer2)
                h2_idx = i % len(hidden_layer2)
                target_pos = hidden_layer2[h2_idx].get_center()
                h2_backprop_animations.append(pulse_group.animate.move_to(target_pos))

            for line in h2_to_h3_connections:
                h2_backprop_animations.append(line.animate.set_stroke(width=5, color=backprop_color))

            self.play(*h2_backprop_animations, run_time=1.0)

            # Only fade pulses, KEEP weight colors
            fade_animations = [FadeOut(pulse) for pulse in h3_backprop_pulses]
            self.play(*fade_animations, run_time=0.5)

            # Stage 4: Hidden Layer 2 to Hidden Layer 1
            h2_backprop_pulses = []
            for h2_node in hidden_layer2:
                for h1_node in hidden_layer1:
                    pulse_group = create_pulse(h2_node.get_center(), backprop_color)
                    h2_backprop_pulses.append(pulse_group)
                    self.add(pulse_group)

            self.wait(0.2)

            # Move pulses and COLOR WEIGHTS
            h1_backprop_animations = []
            for i, pulse_group in enumerate(h2_backprop_pulses):
                h2_idx = i // len(hidden_layer1)
                h1_idx = i % len(hidden_layer1)
                target_pos = hidden_layer1[h1_idx].get_center()
                h1_backprop_animations.append(pulse_group.animate.move_to(target_pos))

            for line in h1_to_h2_connections:
                h1_backprop_animations.append(line.animate.set_stroke(width=5, color=backprop_color))

            self.play(*h1_backprop_animations, run_time=1.0)

            # Only fade pulses, KEEP weight colors
            fade_animations = [FadeOut(pulse) for pulse in h2_backprop_pulses]
            self.play(*fade_animations, run_time=0.5)

            # Stage 5: Hidden Layer 1 to Input Layer
            h1_backprop_pulses = []
            for h1_node in hidden_layer1:
                for input_node in input_layer:
                    pulse_group = create_pulse(h1_node.get_center(), backprop_color)
                    h1_backprop_pulses.append(pulse_group)
                    self.add(pulse_group)

            self.wait(0.2)

            # Move pulses and COLOR WEIGHTS
            input_backprop_animations = []
            for i, pulse_group in enumerate(h1_backprop_pulses):
                h1_idx = i // len(input_layer)
                input_idx = i % len(input_layer)
                target_pos = input_layer[input_idx].get_center()
                input_backprop_animations.append(pulse_group.animate.move_to(target_pos))

            for line in input_to_h1_connections:
                input_backprop_animations.append(line.animate.set_stroke(width=5, color=backprop_color))

            self.play(*input_backprop_animations, run_time=1.0)

            # Only fade pulses, KEEP weight colors
            fade_animations = [FadeOut(pulse) for pulse in h1_backprop_pulses]
            self.play(*fade_animations, run_time=0.5)

            # UPDATE EPOCH TEXT AND SCALE LOSS
            epoch_update_animations = []

            # Update epoch text: 1→2, 2→3, 3→4, 4→5
            new_epoch_text = Text(f"Epoch = {epoch_num + 1}").scale(1.7).move_to(epoch.get_center())
            epoch_update_animations.append(Transform(epoch, new_epoch_text))

            # Scale loss by 0.66
            epoch_update_animations.append(loss.animate.scale(0.66))

            self.play(*epoch_update_animations, run_time=1.0)

            self.wait(0.5)  # Brief pause between epochs







        temp = Text(" Model\nTrained").set_color(YELLOW_B).move_to(epoch).scale(1.9)
        temp1 = Text(" Model\nTrained").set_color(YELLOW_B).move_to(loss).scale(1.9)

        self.play(Transform(loss, temp), Transform(epoch, temp1))
        self.wait(2)






class BackPropSimple(Scene):
    def construct(self):

        PURPLE = "#7000D9"

        self.camera.frame.scale(0.87).shift(RIGHT).shift(UP*0.3)
        
        # Input node - green circle with x embedding
        input_node = Circle(radius=0.4, color=GREEN, fill_opacity=1, stroke_width=6, stroke_color=GREEN_B)
        input_node.move_to(LEFT * 4)
        
        # Input label x
        x_label = Tex("x", font_size=48).scale(1.8).set_color(BLACK).move_to(input_node)
        input_node = VGroup(input_node, x_label)

        # Hidden layer neuron - blue circle WITHOUT f(z₁) initially
        hidden_circle = Circle(radius=0.6, color=BLUE, fill_opacity=1, stroke_width=7, stroke_color=BLUE_B)
        hidden_circle.move_to(ORIGIN).shift(LEFT*0.5)
        hidden_neuron = VGroup(hidden_circle)
        
        # Output neuron - blue circle WITHOUT f(z₂) initially
        output_circle = Circle(radius=0.6, color=BLUE, fill_opacity=1, stroke_width=7, stroke_color=BLUE_B)
        output_circle.move_to(RIGHT * 3.5)
        output_neuron = VGroup(output_circle)
        
        # Connection lines
        line_input_hidden = Line(input_node.get_center(), hidden_neuron.get_center(), stroke_width=5, z_index=-1, color=WHITE)
        line_hidden_output = Line(hidden_neuron.get_center(), output_neuron.get_center(), stroke_width=5, z_index=-1, color=WHITE)
        
        # Weight labels
        w1_label = Tex("w_1", font_size=42, color=RED).scale(1.3)
        w1_label.move_to(line_input_hidden.get_center() + UP * 0.4)
        
        w2_label = Tex("w_2", font_size=42, color=RED).scale(1.3)
        w2_label.move_to(line_hidden_output.get_center() + UP * 0.4)
        
        # Bias arrows and labels
        bias_arrow_hidden = Arrow(UP * 2+LEFT*0.5, hidden_neuron.get_top() + UP * 0.1, stroke_width=3).set_color(WHITE)
        b1_label = Tex("b_1", font_size=42, ).scale(1.3).next_to(bias_arrow_hidden.get_start(), UP, buff=0.2)
        
        bias_arrow_output = Arrow(UP * 2+LEFT*0.5 + RIGHT * 4, output_neuron.get_top() + UP * 0.1, stroke_width=3).set_color(WHITE)
        b2_label = Tex("b_2", font_size=42,).scale(1.3).next_to(bias_arrow_output.get_start(), UP, buff=0.2)
        
        # Function to create glow effect around a dot
        def create_glow(center_point, radius=0.15, color=YELLOW, intensity=0.3):
            glow_group = VGroup()
            for i in range(20):
                glow_radius = radius * (1 + i * 0.1)
                opacity = intensity * (1 - i/20)
                glow_circle = Circle(
                    radius=glow_radius, 
                    stroke_opacity=0, 
                    fill_color=color,
                    fill_opacity=opacity
                ).move_to(center_point)
                glow_group.add(glow_circle)
            return glow_group
        
        # STEP 1: Create all elements except output arrow, output label, and f(z) labels
        self.play(
            GrowFromCenter(hidden_neuron), 
            GrowFromCenter(input_node), 
            GrowFromCenter(output_neuron)
        )
        self.wait(0.5)
        
        self.play(
            ShowCreation(line_input_hidden),
            Write(w1_label),
            ShowCreation(bias_arrow_hidden),
            Write(b1_label),
            ShowCreation(line_hidden_output),
            Write(w2_label),
            ShowCreation(bias_arrow_output),
            Write(b2_label),
        )
        self.wait(0.5)

        z1 = Tex(r"z_1 = w_1 x + b_1").next_to(hidden_neuron, DOWN).shift(DOWN*0.86+LEFT*2.5)
        z2 = Tex(r"z_2 = w_2 f(z_1) + b_2").next_to(z1, RIGHT, buff=0.9)
        y = Tex(r"\hat{y} = f(z_2)").next_to(z2, RIGHT, buff=0.9)

        # STEP 2: Create pulses from input node and b1 bias traveling to hidden neuron
        
        # Create pulse dots with glow
        pulse1_dot = Dot(radius=0.1, color=YELLOW).move_to(input_node.get_center())
        pulse1_glow = create_glow(input_node.get_center(), radius=0.12, color="#ff0000")
        pulse1 = VGroup(pulse1_glow, pulse1_dot)
        
        pulse2_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_hidden.get_start())
        pulse2_glow = create_glow(bias_arrow_hidden.get_start(), radius=0.12, color="#ff0000")
        pulse2 = VGroup(pulse2_glow, pulse2_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse1),
            GrowFromCenter(pulse2),
            run_time=0.4
        )



        
        # Move pulses to hidden neuron
        self.play(
            pulse1.animate.move_to(hidden_neuron.get_center()),
            pulse2.animate.move_to(hidden_neuron.get_center()),
            run_time=0.8
        )
        
        # Fade out pulses and write f(z1)
        fz1_label = Tex(r"f(z_1)", font_size=36, stroke_width=1.12).scale(1.2).set_color(BLACK).move_to(hidden_circle)

        self.play(
            FadeOut(pulse1),
            FadeOut(pulse2),
            Write(fz1_label),
            run_time=0.5
        )
        self.play(ShowCreation(z1), self.camera.frame.animate.shift(DOWN*0.33))
        self.wait(2)  
        # Update hidden neuron to include the label
        hidden_neuron.add(fz1_label)
        
        self.wait(0.5)
        
        # STEP 3: Create pulses from hidden neuron and b2 bias traveling to output neuron
        
        # Create new pulse dots with glow
        pulse3_dot = Dot(radius=0.1, color=YELLOW).move_to(hidden_neuron.get_center())
        pulse3_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color="#ff0000")
        pulse3 = VGroup(pulse3_glow, pulse3_dot)
        
        pulse4_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_output.get_start())
        pulse4_glow = create_glow(bias_arrow_output.get_start(), radius=0.12, color="#ff0000")
        pulse4 = VGroup(pulse4_glow, pulse4_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse3),
            GrowFromCenter(pulse4),
            run_time=0.4
        )
        
        # Move pulses to output neuron
        self.play(
            pulse3.animate.move_to(output_neuron.get_center()),
            pulse4.animate.move_to(output_neuron.get_center()),
            run_time=0.8
        )
        
        # Fade out pulses and write f(z2)
        fz2_label = Tex(r"f(z_2)", font_size=36, stroke_width=1.12).scale(1.2).set_color(BLACK).move_to(output_circle)
        
        self.play(
            FadeOut(pulse3),
            FadeOut(pulse4),
            Write(fz2_label),
            run_time=0.5
        )
        
        # Update output neuron to include the label
        output_neuron.add(fz2_label)
        
        self.play(ShowCreation(z2))
        self.wait(2) 
        
        # STEP 4: Create output arrow and label
        output_arrow = Arrow(output_neuron.get_right(), RIGHT * 6, stroke_width=4).set_color(WHITE)
        y_hat_label = Tex(r"\hat{y}", font_size=48, color=BLUE).scale(1.5).next_to(output_arrow.get_end(), RIGHT, buff=0.2)
        self.wait(0.19)
        self.play(GrowArrow(output_arrow))
        self.play(Write(y_hat_label))
        
        self.play(ShowCreation(y))
        self.wait(2)


        

        self.play(self.camera.frame.animate.shift(RIGHT*5))

        loss = Tex(r"L \ = \ \frac{1}{2}(\hat{y} - y)^2").next_to(y_hat_label, RIGHT, buff=0.66).shift(RIGHT)
        self.play(ShowCreation(loss))

        rect = SurroundingRectangle(loss, color=RED_C, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Uncreate(rect), loss.animate.shift(UP*2))
        self.play(self.camera.frame.animate.shift(LEFT*5))

        rect_1 = SurroundingRectangle(b1_label, stroke_width=5).scale(1.1)
        rect_2 = SurroundingRectangle(b2_label, stroke_width=5).scale(1.1)
        rect_3 = SurroundingRectangle(w1_label, stroke_width=5).scale(1.1)
        rect_4 = SurroundingRectangle(w2_label, stroke_width=5).scale(1.1)

        
        self.play(ShowCreation(VGroup(rect_1, rect_2, rect_3, rect_4)), run_time=2)
        self.wait(2)

        self.play(Uncreate(VGroup( rect_1, rect_3)))
        self.wait()
        self.play(self.camera.frame.animate.shift(RIGHT*5), )

        w2 = Tex(r"w_2 \rightarrow w_2 - \alpha \frac{\partial L}{\partial w_2}").next_to(loss, DOWN).shift(DOWN*0.78)
        b2 = Tex(r"b_2 \rightarrow b_2 - \alpha \frac{\partial L}{\partial b_2}").next_to(w2, DOWN).shift(DOWN*0.35)

        self.play(ShowCreation(w2), ShowCreation(b2))

        rect = SurroundingRectangle(w2, color=GREEN_C, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(b2, color=GREEN_C, stroke_width=6).scale(1.1)))
        self.wait(2)

        self.play(Uncreate(rect))

        self.play(
            b2[-6:].animate.set_color(RED_C),
            w2[-6:].animate.set_color(RED_C),
            )
        
        self.wait(2)
        self.camera.frame.save_state()

        self.camera.frame.restore()


        self.play(self.camera.frame.animate.shift(RIGHT*7))

        a = w2[-6:].copy().set_color(WHITE)

        self.play(a.animate.shift(RIGHT*7), self.camera.frame.animate.shift(RIGHT*5))
        self.wait(2)


        self.play(Transform(a, Tex(r"\frac{\partial}{\partial w_2} \left[ \frac{1}{2}(\hat{y} - y)^2 \right]").move_to(a)))
        self.wait(2)

        self.play(a[3:5].animate.set_color(RED_C))
        self.wait()
        self.play(a[10:12].animate.set_color(GREEN_C))
        self.wait(2)
        

        self.play(Transform(a, Tex(r" \frac{\partial}{\partial \hat{y}} \left[ \frac{1}{2}(\hat{y} - y)^2 \right] \cdot \frac{\partial \hat{y}}{\partial w_2}").move_to(a)))
        self.wait()

        brace = Brace(a[:17], DOWN, buff=0.5)
        self.play(GrowFromCenter(brace))

        self.play(
        a[3:5].animate.set_color(GREEN_C),
        a[10:12].animate.set_color(GREEN_C)
        )

        self.wait(2)

        self.play(Transform(brace, Brace(a[18:], DOWN, buff=0.5)))
        self.play(
        a[19:21].animate.set_color(GREEN_C),
        a[-2:].animate.set_color(RED_C)
        )

        self.wait(2)

        temp = Tex(r"\frac{\partial}{\partial \hat{y}} \left[ \frac{1}{2}(\hat{y} - y)^2 \right] \cdot \frac{\partial f(z_2)}{\partial w_2}").move_to(a)
        
        temp[3:5].set_color(GREEN_C)
        temp[10:12].set_color(GREEN_C)
        temp[19:24].set_color(BLUE_C)
        temp[-2:].set_color(RED_C)

        self.play(Transform(a, temp), FadeOut(brace))

        self.wait(2)


        temp = Tex(r"\frac{\partial}{\partial \hat{y}} \left[ \frac{1}{2}(\hat{y} - y)^2 \right] \cdot \frac{\partial f(z_2)}{\partial z_2} \cdot \frac{\partial z_2}{\partial w_2}").move_to(a)

        temp[3:5].set_color(GREEN_C)
        temp[10:12].set_color(GREEN_C)
        temp[19:24].set_color(BLUE_C)
        temp[26:28].set_color(BLUE_C)
        temp[-6:-4].set_color(BLUE_C)
        temp[-2:].set_color(RED_C)

        self.play(Transform(a, temp))
        self.wait(2)

        temp = Tex(r"\frac{\partial}{\partial \hat{y}} \left[ \frac{1}{2}(\hat{y} - y)^2 \right] \cdot \frac{\partial f(z_2)}{\partial z_2} \cdot \frac{\partial}{\partial w_2}[w_2 f(z_1) + b_2]").move_to(a)

        temp[3:5].set_color(GREEN_C)
        temp[10:12].set_color(GREEN_C)
        temp[19:24].set_color(BLUE_C)
        temp[26:28].set_color(BLUE_C)
        temp[-14:-12].set_color(RED_C)
        temp[-11:-9].set_color(RED_C)

        self.play(Transform(a, temp))
        self.wait(2)

        self.play(a.animate.shift(UP))

        temp_a = Tex(r"\hat{y} = f(z_2)").next_to(a, DOWN, buff=1.5).scale(1.2)
        temp_a[:2].set_color(GREEN_C)
        temp_a[3:].set_color(BLUE_C)
        temp_a.shift(LEFT*2.3)

        temp_b = Tex(r"z_2 = w_2f(z_1) + b_2").next_to(temp_a, RIGHT, buff=1.5).scale(1.2)
        temp_b[:2].set_color(BLUE_C)
        temp_b[3:5].set_color(RED_C)
        

        self.play(ShowCreation(temp_b), ShowCreation(temp_a))
        self.wait(2)

        self.play(FadeOut(VGroup(temp_a, temp_b)),)
        
        self.wait(2)

        # Create the chain elements
        w2_tex = Tex(r"w_2").scale(1.0).set_color(RED_C)
        arrow1 = Tex(r"\leftarrow").scale(1.0) 
        z2_tex = Tex(r"z_2").scale(1.0).set_color(BLUE_C)
        arrow2 = Tex(r"\leftarrow").scale(1.0)
        yhat_tex = Tex(r"\hat{y}").scale(1.0).set_color(GREEN_C)
        arrow3 = Tex(r"\leftarrow").scale(1.0)
        loss_tex = Tex(r"L").scale(1.0).set_color(YELLOW)
        
        # Arrange horizontally
        chain = VGroup(loss_tex, arrow1, yhat_tex, arrow2, z2_tex, arrow3, w2_tex).arrange(RIGHT, buff=0.5).next_to(a, DOWN, buff=1.66).scale(1.4)
        
        # Add the chain to scene
        self.play(GrowFromCenter(w2_tex))
        self.play(GrowFromCenter(arrow3))
        self.play(GrowFromCenter(z2_tex))
        self.play(GrowFromCenter(arrow2))
        self.play(GrowFromCenter(yhat_tex))
        self.play(GrowFromCenter(arrow1))
        self.play(GrowFromCenter(loss_tex))

        self.wait(2)
        
        rect = SurroundingRectangle(w2_tex, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait()

        self.play(loss_tex.animate.scale(0.33))
        self.wait(2)

        self.play(FadeOut(chain), Uncreate(rect))
        self.wait()

        derivative = Tex(r"\frac{\partial L}{\partial w_2} = (\hat{y} - y) \cdot f'(z_2) \cdot f(z_1)").next_to(a, DOWN, buff=1.4)
        self.play(ShowCreation(derivative[:7]))
        self.wait(2)

        brace = Brace(a[:17], UP, buff=0.57)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        self.play(TransformFromCopy(a[:17], derivative[7:13]))
        self.wait()

        self.play(Transform(brace, Brace(a[18:28], UP, buff=0.57)))
        self.wait()
        self.play(TransformFromCopy(a[18:28], derivative[14:20]), FadeIn(derivative[13]))
        self.wait()

        self.play(Transform(brace, Brace(a[29:], UP, buff=0.57)))
        self.wait()
        self.play(TransformFromCopy(a[29:], derivative[21:]), FadeIn(derivative[20]))
        self.wait()

        self.play(FadeOut(brace), derivative.animate.next_to(a, UP).shift(DOWN*0.2), FadeOut(a))
        self.wait()

        b = Tex(r"\frac{\partial L}{\partial b_2} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z_2} \cdot \frac{\partial z_2}{\partial b_2}")

        b.next_to(a, DOWN, buff=0.4)
        b[4:6].set_color(RED_C)
        b[11:13].set_color(GREEN_C)
        b[15:17].set_color(GREEN_C)
        b[19:21].set_color(BLUE_C)
        b[23:25].set_color(BLUE_C)
        b[27:].set_color(RED_C)

        self.play(ShowCreation(b))

        self.wait(2)

        temp = Tex(r"\frac{\partial L}{\partial b_2} = \frac{\partial}{\partial \hat{y}} \left[ \frac{1}{2}(y - \hat{y})^2 \right] \cdot \frac{\partial f(z_2)}{\partial z_2} \cdot \frac{\partial}{\partial b_2}[w_2 f(z_1) + b_2]").move_to(b)
        
        temp[4:6].set_color(RED_C)
        temp[10:12].set_color(GREEN_C)
        temp[19:21].set_color(GREEN_C)
        temp[26:31].set_color(BLUE_C)
        temp[33:35].set_color(BLUE_C)
        temp[39:41].set_color(RED_C)
        temp[50:52].set_color(RED_C)

        self.play(Transform(b, temp))

        self.wait(2)


        self.play(Transform(b, Tex(r"\frac{\partial L}{\partial b_2} = (\hat{y} - y) \cdot f'(z_2)").move_to(b)))

        self.play(derivative.animate.shift(DOWN*1.4), b.animate.shift(DOWN*0.4))
        self.wait(2)


        self.play(self.camera.frame.animate.shift(LEFT*12))
 
        
        w_rect = SurroundingRectangle(w2, stroke_width=6, color=GREEN_C).scale(1.1)
        b_rect = SurroundingRectangle(b2, stroke_width=6, color=GREEN_C).scale(1.1)

        self.play(ShowCreation(w_rect), ShowCreation(b_rect))
        self.wait(2)

        self.play(Uncreate(w_rect), Uncreate(b_rect), self.camera.frame.animate.shift(LEFT*5+UP*0.23), Uncreate(VGroup(z1, y, z2)))
        self.wait()

        # PURPLE PULSE ANIMATION - Backpropagation visualization  
        self.wait(1)
        
        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(y_hat_label.get_center())
        purple_pulse_glow = create_glow(y_hat_label.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        
        # Move pulse toward output neuron
        self.play(
            purple_pulse.animate.move_to(output_neuron.get_center()),
            output_arrow.animate.set_color(PURPLE),
            y_hat_label.animate.set_color(PURPLE),
            run_time=0.8
        )
        self.wait(0.3)
        

        self.wait(0.2)
        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b2_label.get_center()),
            purple_pulse_weight.animate.move_to(hidden_neuron.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_hidden_output.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_output.animate.set_color(PURPLE),

            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),
            b2_label.animate.set_color(PURPLE),
            w2_label.animate.set_color(PURPLE),
            run_time=0.8
        )
        
        self.wait(2)

        self.play(
            rect_2.animate.move_to(b1_label),
            rect_4.animate.move_to(w1_label)
        )
        self.wait(1)

        self.play(self.camera.frame.animate.shift(RIGHT*5))

        w_rect = SurroundingRectangle(w2, stroke_width=6, color=GREEN_C).scale(1.1)
        b_rect = SurroundingRectangle(b2, stroke_width=6, color=GREEN_C).scale(1.1)

        self.play(ShowCreation(w_rect), ShowCreation(b_rect))
        self.wait(2)

        w1 = Tex(r"w_1 \rightarrow w_1 - \alpha \frac{\partial L}{\partial w_1}").move_to(w2)
        b1 = Tex(r"b_1 \rightarrow b_1 - \alpha \frac{\partial L}{\partial b_1}").move_to(b2)
        

        w1[-6:].set_color(RED_C)
        b1[-6:].set_color(RED_C)

        self.play(
            ReplacementTransform(b2, b1),
            ReplacementTransform(w2, w1)
            )
        
        self.wait(2)

        self.remove(b,a, derivative)

        self.camera.frame.save_state()

        self.camera.frame.restore()

        a = w1[-6:].copy().set_color(WHITE)
        b = b1[-6:].copy().set_color(WHITE)

        self.play(
            a.animate.shift(RIGHT*7+UP*1.14),
            b.animate.shift(RIGHT*7+UP*0.9),
            self.camera.frame.animate.shift(RIGHT*12)
              )
        
        self.wait(2)

        w1_expanded = Tex(r"\frac{\partial L}{\partial w_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z_2} \cdot \frac{\partial z_2}{\partial f(z_1)} \cdot \frac{\partial f(z_1)}{\partial z_1} \cdot \frac{\partial z_1}{\partial w_1}")
        
        # Color the terms
        w1_expanded[4:6].set_color(RED_C)        # w_1 in denominator
        w1_expanded[11:13].set_color(GREEN_C)    # \hat{y} in numerator  
        w1_expanded[15:17].set_color(GREEN_C)    # \hat{y} in denominator
        w1_expanded[19:21].set_color(BLUE_C)     # z_2 in numerator
        w1_expanded[23:25].set_color(BLUE_C)     # z_2 in denominator  
        w1_expanded[27:32].set_color(PURPLE_C)   # f(z_1) in numerator
        w1_expanded[34:39].set_color(PURPLE_C)   # f(z_1) in denominator
        w1_expanded[41:43].set_color(MAROON_C)   # z_1 in numerator
        w1_expanded[45:47].set_color(MAROON_C)   # z_1 in denominator
        w1_expanded[-2:].set_color(RED_C)      # w_1 in final denominator
        
        
        b1_expanded = Tex(r"\frac{\partial L}{\partial b_1} = \frac{\partial L}{\partial \hat{y}} \cdot \frac{\partial \hat{y}}{\partial z_2} \cdot \frac{\partial z_2}{\partial f(z_1)} \cdot \frac{\partial f(z_1)}{\partial z_1} \cdot \frac{\partial z_1}{\partial b_1}")
        
        # Color the terms
        b1_expanded[4:6].set_color(RED_C)        # b_1 in denominator
        b1_expanded[11:13].set_color(GREEN_C)    # \hat{y} in numerator
        b1_expanded[15:17].set_color(GREEN_C)    # \hat{y} in denominator  
        b1_expanded[19:21].set_color(BLUE_C)     # z_2 in numerator
        b1_expanded[23:25].set_color(BLUE_C)     # z_2 in denominator
        b1_expanded[27:32].set_color(PURPLE_C)   # f(z_1) in numerator
        b1_expanded[34:39].set_color(PURPLE_C)   # f(z_1) in denominator
        b1_expanded[41:43].set_color(MAROON_C)   # z_1 in numerator
        b1_expanded[45:47].set_color(MAROON_C)   # z_1 in denominator
        b1_expanded[-2:].set_color(RED_C)      # b_1 in final denominator
        
        
        self.play(
            Transform(b, b1_expanded.move_to(b)),
            Transform(a, w1_expanded.move_to(a)) )


        self.wait(2)

        self.play(VGroup(a,b).animate.shift(UP*1))

        # Create the chain elements
        w2_tex = Tex(r"w_1 / b_1").scale(1.0).set_color(RED_C)
        arrow1 = Tex(r"\leftarrow").scale(1.0) 
        z1_tex = Tex(r"z_1").scale(1.0).set_color(MAROON_C)
        arrow2 = Tex(r"\leftarrow").scale(1.0)
        fz1_tex = Tex(r"f(z_1)").scale(1.0).set_color(PURPLE_C)
        arrow25 = Tex(r"\leftarrow").scale(1.0)
        z2_tex = Tex(r"z_2").scale(1.0).set_color(BLUE_C)
        arrow26 = Tex(r"\leftarrow").scale(1.0)
        yhat_tex = Tex(r"\hat{y}").scale(1.0).set_color(GREEN_C)
        arrow3 = Tex(r"\leftarrow").scale(1.0)
        loss_tex = Tex(r"L").scale(1.0).set_color(YELLOW)
        
        # Arrange horizontally
        chain = VGroup(loss_tex, arrow3, yhat_tex, arrow26, z2_tex, arrow25,fz1_tex, arrow2, z1_tex, arrow1, w2_tex).arrange(RIGHT, buff=0.4).next_to(b, DOWN, buff=1.26).scale(0.7*1.52)
        
        # Add the chain to scene
        self.play(GrowFromCenter(chain))

        self.wait(2)

        self.play(FadeOut(chain))

        self.play(VGroup(a,b).animate.shift(DOWN*1))

        self.wait(1)


        self.play(
            Transform(b, Tex(r"\frac{\partial L}{\partial b_1} = (\hat{y} - y) \cdot f'(z_2) \cdot w_2 \cdot f'(z_1)").move_to(b)),
            Transform(a, Tex(r"\frac{\partial L}{\partial w_1} = (\hat{y} - y) \cdot f'(z_2) \cdot w_2 \cdot f'(z_1) \cdot x").move_to(a)),
        )

        self.wait(1)

        self.play(self.camera.frame.animate.shift(LEFT*12))
        self.wait(2)

        self.play(Uncreate(b_rect), Uncreate(w_rect), self.camera.frame.animate.shift(LEFT*5+UP*0.29))
        self.wait(1)


        # PURPLE PULSE ANIMATION - Backpropagation visualization  
        self.wait(1)
        
        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(hidden_neuron.get_center())
        purple_pulse_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        

        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b1_label.get_center()),
            purple_pulse_weight.animate.move_to(input_node.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_input_hidden.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_hidden.animate.set_color(PURPLE),
            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),
            b1_label.animate.set_color(PURPLE),
            w1_label.animate.set_color(PURPLE),
            Uncreate(rect_4),
            Uncreate(rect_2),
            run_time=0.8
        )
        
        self.wait()

        loss = Text("Loss").next_to(line_hidden_output, DOWN, buff=0.9).shift(DOWN).scale(2)

        self.play(Write(loss), self.camera.frame.animate.shift(DOWN*0.7))

        self.wait(2)

        self.camera.frame.save_state()

        #forward prop
        # Create pulse dots with glow
        pulse1_dot = Dot(radius=0.1, color=YELLOW).move_to(input_node.get_center())
        pulse1_glow = create_glow(input_node.get_center(), radius=0.12, color="#ff0000")
        pulse1 = VGroup(pulse1_glow, pulse1_dot)
        
        pulse2_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_hidden.get_start())
        pulse2_glow = create_glow(bias_arrow_hidden.get_start(), radius=0.12, color="#ff0000")
        pulse2 = VGroup(pulse2_glow, pulse2_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse1),
            GrowFromCenter(pulse2),
            run_time=0.4
        )

        
        # Move pulses to hidden neuron
        self.play(
            pulse1.animate.move_to(hidden_neuron.get_center()),
            pulse2.animate.move_to(hidden_neuron.get_center()),
            run_time=0.8
        )
        
        self.play(
            FadeOut(pulse1),
            FadeOut(pulse2),
            run_time=0.5
        )

            
        # STEP 3: Create pulses from hidden neuron and b2 bias traveling to output neuron
        
        # Create new pulse dots with glow
        pulse3_dot = Dot(radius=0.1, color=YELLOW).move_to(hidden_neuron.get_center())
        pulse3_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color="#ff0000")
        pulse3 = VGroup(pulse3_glow, pulse3_dot)
        
        pulse4_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_output.get_start())
        pulse4_glow = create_glow(bias_arrow_output.get_start(), radius=0.12, color="#ff0000")
        pulse4 = VGroup(pulse4_glow, pulse4_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse3),
            GrowFromCenter(pulse4),
            run_time=0.4
        )
        
        # Move pulses to output neuron
        self.play(
            pulse3.animate.move_to(output_neuron.get_center()),
            pulse4.animate.move_to(output_neuron.get_center()),
            run_time=0.8
        )

        self.play(
            pulse3.animate.move_to(y_hat_label.get_center()),
            pulse4.animate.move_to(y_hat_label.get_center()),
            run_time=0.8
        )        
        
        

        self.play(
            FadeOut(pulse3),
            FadeOut(pulse4),
            run_time=0.5
        )
        
        PURPLE = YELLOW_C


        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(y_hat_label.get_center())
        purple_pulse_glow = create_glow(y_hat_label.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        
        # Move pulse toward output neuron
        self.play(
            purple_pulse.animate.move_to(output_neuron.get_center()),
            output_arrow.animate.set_color(PURPLE),
            y_hat_label.animate.set_color(PURPLE),
            run_time=0.8
        )
        

        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b2_label.get_center()),
            purple_pulse_weight.animate.move_to(hidden_neuron.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_hidden_output.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_output.animate.set_color(PURPLE),
            b2_label.animate.set_color(PURPLE),
            w2_label.animate.set_color(PURPLE),

            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),

            run_time=0.8
        )
    

        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(hidden_neuron.get_center())
        purple_pulse_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        

        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b1_label.get_center()),
            purple_pulse_weight.animate.move_to(input_node.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_input_hidden.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_hidden.animate.set_color(PURPLE),
            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),
            b1_label.animate.set_color(PURPLE),
            w1_label.animate.set_color(PURPLE),
            Uncreate(rect_4),
            Uncreate(rect_2),
            run_time=0.8
        )

        self.play(loss.animate.scale(0.8))



        #Next Iteration


        #forward prop
        # Create pulse dots with glow
        pulse1_dot = Dot(radius=0.1, color=YELLOW).move_to(input_node.get_center())
        pulse1_glow = create_glow(input_node.get_center(), radius=0.12, color="#ff0000")
        pulse1 = VGroup(pulse1_glow, pulse1_dot)
        
        pulse2_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_hidden.get_start())
        pulse2_glow = create_glow(bias_arrow_hidden.get_start(), radius=0.12, color="#ff0000")
        pulse2 = VGroup(pulse2_glow, pulse2_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse1),
            GrowFromCenter(pulse2),
            run_time=0.4
        )

        
        # Move pulses to hidden neuron
        self.play(
            pulse1.animate.move_to(hidden_neuron.get_center()),
            pulse2.animate.move_to(hidden_neuron.get_center()),
            run_time=0.8
        )
        
        self.play(
            FadeOut(pulse1),
            FadeOut(pulse2),
            run_time=0.5
        )

            
        # STEP 3: Create pulses from hidden neuron and b2 bias traveling to output neuron
        
        # Create new pulse dots with glow
        pulse3_dot = Dot(radius=0.1, color=YELLOW).move_to(hidden_neuron.get_center())
        pulse3_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color="#ff0000")
        pulse3 = VGroup(pulse3_glow, pulse3_dot)
        
        pulse4_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_output.get_start())
        pulse4_glow = create_glow(bias_arrow_output.get_start(), radius=0.12, color="#ff0000")
        pulse4 = VGroup(pulse4_glow, pulse4_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse3),
            GrowFromCenter(pulse4),
            run_time=0.4
        )
        
        # Move pulses to output neuron
        self.play(
            pulse3.animate.move_to(output_neuron.get_center()),
            pulse4.animate.move_to(output_neuron.get_center()),
            run_time=0.8
        )

        self.play(
            pulse3.animate.move_to(y_hat_label.get_center()),
            pulse4.animate.move_to(y_hat_label.get_center()),
            run_time=0.8
        )        
        

        self.play(
            FadeOut(pulse3),
            FadeOut(pulse4),
            run_time=0.5
        )
        
        PURPLE = "#00ff00"


        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(y_hat_label.get_center())
        purple_pulse_glow = create_glow(y_hat_label.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        
        # Move pulse toward output neuron
        self.play(
            purple_pulse.animate.move_to(output_neuron.get_center()),
            output_arrow.animate.set_color(PURPLE),
            y_hat_label.animate.set_color(PURPLE),
            run_time=0.8
        )
        

        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b2_label.get_center()),
            purple_pulse_weight.animate.move_to(hidden_neuron.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_hidden_output.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_output.animate.set_color(PURPLE),
            b2_label.animate.set_color(PURPLE),
            w2_label.animate.set_color(PURPLE),

            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),

            run_time=0.8
        )
    

        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(hidden_neuron.get_center())
        purple_pulse_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        

        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b1_label.get_center()),
            purple_pulse_weight.animate.move_to(input_node.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_input_hidden.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_hidden.animate.set_color(PURPLE),
            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),
            b1_label.animate.set_color(PURPLE),
            w1_label.animate.set_color(PURPLE),
            Uncreate(rect_4),
            Uncreate(rect_2),
            run_time=0.8
        )

        self.play(loss.animate.scale(0.6))
     
        


        #Next Iteration


        #Next Iteration


        #forward prop
        # Create pulse dots with glow
        pulse1_dot = Dot(radius=0.1, color=YELLOW).move_to(input_node.get_center())
        pulse1_glow = create_glow(input_node.get_center(), radius=0.12, color="#ff0000")
        pulse1 = VGroup(pulse1_glow, pulse1_dot)
        
        pulse2_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_hidden.get_start())
        pulse2_glow = create_glow(bias_arrow_hidden.get_start(), radius=0.12, color="#ff0000")
        pulse2 = VGroup(pulse2_glow, pulse2_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse1),
            GrowFromCenter(pulse2),
            run_time=0.4
        )

        
        # Move pulses to hidden neuron
        self.play(
            pulse1.animate.move_to(hidden_neuron.get_center()),
            pulse2.animate.move_to(hidden_neuron.get_center()),
            run_time=0.8
        )
        
        self.play(
            FadeOut(pulse1),
            FadeOut(pulse2),
            run_time=0.5
        )

            
        # STEP 3: Create pulses from hidden neuron and b2 bias traveling to output neuron
        
        # Create new pulse dots with glow
        pulse3_dot = Dot(radius=0.1, color=YELLOW).move_to(hidden_neuron.get_center())
        pulse3_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color="#ff0000")
        pulse3 = VGroup(pulse3_glow, pulse3_dot)
        
        pulse4_dot = Dot(radius=0.1, color=YELLOW).move_to(bias_arrow_output.get_start())
        pulse4_glow = create_glow(bias_arrow_output.get_start(), radius=0.12, color="#ff0000")
        pulse4 = VGroup(pulse4_glow, pulse4_dot)
        
        # Animate pulses growing from center
        self.play(
            GrowFromCenter(pulse3),
            GrowFromCenter(pulse4),
            run_time=0.4
        )
        
        # Move pulses to output neuron
        self.play(
            pulse3.animate.move_to(output_neuron.get_center()),
            pulse4.animate.move_to(output_neuron.get_center()),
            run_time=0.8
        )

        self.play(
            pulse3.animate.move_to(y_hat_label.get_center()),
            pulse4.animate.move_to(y_hat_label.get_center()),
            run_time=0.8
        )        
        

        self.play(
            FadeOut(pulse3),
            FadeOut(pulse4),
            run_time=0.5
        )
        
        PURPLE = "#ff00aa"


        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(y_hat_label.get_center())
        purple_pulse_glow = create_glow(y_hat_label.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        
        # Move pulse toward output neuron
        self.play(
            purple_pulse.animate.move_to(output_neuron.get_center()),
            output_arrow.animate.set_color(PURPLE),
            y_hat_label.animate.set_color(PURPLE),
            run_time=0.8
        )
        

        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b2_label.get_center()),
            purple_pulse_weight.animate.move_to(hidden_neuron.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_hidden_output.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_output.animate.set_color(PURPLE),
            b2_label.animate.set_color(PURPLE),
            w2_label.animate.set_color(PURPLE),

            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),

            run_time=0.8
        )
    

        # Create purple pulse starting from y_hat
        purple_pulse_dot = Dot(radius=0.1, color=PURPLE).move_to(hidden_neuron.get_center())
        purple_pulse_glow = create_glow(hidden_neuron.get_center(), radius=0.12, color=PURPLE)
        purple_pulse = VGroup(purple_pulse_glow, purple_pulse_dot)
        
        # Animate pulse growing from y_hat
        self.play(GrowFromCenter(purple_pulse), run_time=0.4)
        self.wait(0.2)
        

        
        # Create two split pulses - one for bias, one for weight
        purple_pulse_bias = purple_pulse.copy()
        purple_pulse_weight = purple_pulse.copy()
        
        # Split the pulse and move to targets (no new lines created)
        self.play(
            purple_pulse_bias.animate.move_to(b1_label.get_center()),
            purple_pulse_weight.animate.move_to(input_node.get_center()),
            FadeOut(purple_pulse),  # Original pulse disappears
            line_input_hidden.animate.set_color(PURPLE).set_stroke(width=6),
            bias_arrow_hidden.animate.set_color(PURPLE),
            run_time=1.0
        )
        
        # Fade out pulses while coloring the labels PURPLE
        self.play(
            FadeOut(purple_pulse_bias),
            FadeOut(purple_pulse_weight),
            b1_label.animate.set_color(PURPLE),
            w1_label.animate.set_color(PURPLE),
            Uncreate(rect_4),
            Uncreate(rect_2),
            run_time=0.8
        )

        self.play(loss.animate.scale(0.6))

        self.play(FadeOut(loss), self.camera.frame.animate.shift(DOWN*0.01))

        text = Text("Network Trained", weight=BOLD).next_to(w2_label, DOWN).shift(DOWN*1.68).set_color(GREEN_C).scale(1.5)
        self.play(GrowFromCenter(text))

        self.wait(2)
     
        
