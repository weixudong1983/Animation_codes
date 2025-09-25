from manimlib import *
import numpy as np



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
     
        
