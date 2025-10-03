from manimlib import *
import numpy as np

GRAY = GREY

class TanhScene(Scene):
    def construct(self):
        
        self.camera.frame.scale(0.65).shift(UP*0.34)
        # Set up axes for Tanh function (no ticks)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 0.5],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,  # Removed ticks
                "numbers_to_exclude": [0],
            },
        )

        # Create axis labels
        x_label = Tex("z", font_size=48, color=WHITE).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Tex("tanh(z)", font_size=48, color=WHITE).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # Tanh function
        x_vals = np.linspace(-3, 3, 1000)
        tanh_points = []
        for x in x_vals:
            tanh_val = np.tanh(x)  # Tanh function
            tanh_points.append(axes.c2p(x, tanh_val))

        tanh_graph = VMobject()
        tanh_graph.set_points_as_corners(tanh_points)
        tanh_graph.set_stroke(PURPLE, width=6)

        # Tanh derivative function
        tanh_derivative_points = []
        for x in x_vals:
            derivative_val = 1 - np.tanh(x)**2  # Tanh derivative: sech²(x) = 1 - tanh²(x)
            tanh_derivative_points.append(axes.c2p(x, derivative_val))

        tanh_derivative_graph = VMobject()
        tanh_derivative_graph.set_points_as_corners(tanh_derivative_points)
        tanh_derivative_graph.set_stroke(YELLOW, width=6)

        # Tanh title and formula positioned in top left
        tanh_title = Text("Tanh Function", font_size=40, color=PURPLE)
        tanh_title.to_corner(UL, buff=0.5)

        tanh_formula = Tex(r"\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}", font_size=32, color=PURPLE).set_color(PURPLE)
        tanh_formula.next_to(tanh_title, DOWN, buff=0.2)
        tanh_formula.shift(RIGHT*2.299+DOWN*1)

        # Derivative formula
        derivative_formula = Tex(r"\tanh'(z) = 1 - \tanh^2(z)", font_size=30, color=YELLOW).set_color(YELLOW)
        derivative_formula.next_to(tanh_formula, DOWN, buff=0.5)

        # Zero-centered note
        zero_centered = Tex(r"\text{Zero-centered}", font_size=24, color=GREEN)
        zero_centered.next_to(derivative_formula, DOWN, buff=0.4)

        # Horizontal asymptotes - visually shifted but labeled as 1 and -1
        upper_asymptote = DashedLine(
            start=axes.c2p(-3, 1.03), 
            end=axes.c2p(3, 1.03), 
            color=GRAY, 
            stroke_width=2
        )
        lower_asymptote = DashedLine(
            start=axes.c2p(-3, -1.03), 
            end=axes.c2p(3, -1.03), 
            color=GRAY, 
            stroke_width=2
        )

        # Asymptote labels - just the numbers
        upper_label = Tex("1", font_size=30, color=GRAY).next_to(upper_asymptote.get_end(), RIGHT, buff=0.1)
        lower_label = Tex("-1", font_size=30, color=GRAY).next_to(lower_asymptote.get_end(), RIGHT, buff=0.1)
        
        derivative_formula.next_to(upper_label, UP).shift(UP*0.34+LEFT*0.37)
        # Animation
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))

        # Show asymptotes first
        self.play(
            ShowCreation(upper_asymptote),
            ShowCreation(lower_asymptote),
            Write(upper_label),
            Write(lower_label)
        )
        self.wait(0.5)

        self.play(Write(tanh_formula))
        self.play(ShowCreation(tanh_graph), run_time=2.5)
        self.wait(1.5)

        self.play(Write(zero_centered))
        self.wait(2)

        self.play(Write(derivative_formula))
        self.play(ShowCreation(tanh_derivative_graph), run_time=2)
        self.wait(1.5)

        self.wait(3)

        # Highlight key properties with brief animations
        self.play(
            tanh_graph.animate.set_stroke(width=8),
            run_time=0.5
        )
        self.play(
            tanh_graph.animate.set_stroke(width=6),
            run_time=0.5
        )
        self.wait(2)





class SigmoidScene(Scene):
    def construct(self):

        self.camera.frame.shift(UP*0.23+RIGHT*0.1).scale(0.83)
        
        # Set up axes for Sigmoid function (no ticks)
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-0.5, 4, 1],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,  # Removed ticks
                "numbers_to_exclude": [0],
            },
        )

        # Create axis labels using LaTeX sigma
        x_label = Tex("z", font_size=48, color=WHITE).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Tex("\\sigma(z)", font_size=48, color=WHITE).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # Sigmoid function - changed scaling to 3.5 so maximum (1) appears at y=3.5
        x_vals = np.linspace(-5, 5, 1000)
        sigmoid_points = []
        for x in x_vals:
            sigmoid_val = 1 / (1 + np.exp(-x))  # Sigmoid function
            sigmoid_points.append(axes.c2p(x, sigmoid_val * 3.5))  # Scale by 3.5

        sigmoid_graph = VMobject()
        sigmoid_graph.set_points_as_corners(sigmoid_points)
        sigmoid_graph.set_stroke(GREEN, width=6)

        # Sigmoid derivative function
        sigmoid_derivative_points = []
        for x in x_vals:
            sigmoid_val = 1 / (1 + np.exp(-x))
            derivative_val = sigmoid_val * (1 - sigmoid_val)  # Sigmoid derivative
            sigmoid_derivative_points.append(axes.c2p(x, derivative_val * 3.5))  # Scale by 3.5

        sigmoid_derivative_graph = VMobject()
        sigmoid_derivative_graph.set_points_as_corners(sigmoid_derivative_points)
        sigmoid_derivative_graph.set_stroke(ORANGE, width=6)

        # Custom tick marks and labels
        # Tick at y = 3.5 (sigmoid maximum, labeled "1")
        tick_1_pos = axes.c2p(0, 3.5)
        tick_1_mark = Line(
            axes.c2p(-0.1, 3.5), axes.c2p(0.1, 3.5),
            stroke_width=3, color=WHITE
        )
        tick_1_label = Tex("1", font_size=36, color=WHITE).next_to(tick_1_mark, LEFT, buff=0.1)
        
        # Tick at y = 1.75 (sigmoid at z=0, which is 0.5 * 3.5 = 1.75, labeled "0.5")
        tick_half_pos = axes.c2p(0, 1.75)
        tick_half_mark = Line(
            axes.c2p(-0.1, 1.75), axes.c2p(0.1, 1.75),
            stroke_width=3, color=WHITE
        )
        tick_half_label = Tex("0.5", font_size=36, color=WHITE).next_to(tick_half_mark, LEFT, buff=0.1)

        # Sigmoid formula positioned in top left (no title)
        sigmoid_formula = Tex(r"\sigma(z) = \frac{1}{1+e^{-z}}", font_size=46, color=GREEN).set_color(GREEN)
        sigmoid_formula.to_corner(UL, buff=0.5)
        sigmoid_formula.shift(RIGHT*2+DOWN*1.1)
      
        # Derivative formula
        derivative_formula = Tex(r"\sigma'(z) = \sigma(z)(1-\sigma(z))", 
                                 font_size=36, color=ORANGE).set_color(ORANGE)
        derivative_formula.next_to(sigmoid_formula, DOWN, buff=0.4)

        # Animation
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        
        # Add custom tick marks
        self.play(ShowCreation(tick_1_mark), Write(tick_1_label))
        self.play(ShowCreation(tick_half_mark), Write(tick_half_label))
        self.wait(1)

        self.play(Write(sigmoid_formula))
        self.play(ShowCreation(sigmoid_graph), run_time=1.8)
        self.wait(2)

        self.play(Write(derivative_formula))
        self.play(ShowCreation(sigmoid_derivative_graph), run_time=2)
        self.wait(5)  # Wait 5 seconds as requested

        self.embed()
        
class ReLUScene(Scene):
    def construct(self):
        
        self.camera.frame.scale(0.8).shift(UP*0.34)
        # Set up axes for ReLU function (no ticks)
        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-0.5, 4, 1],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,  # Removed ticks
                "numbers_to_exclude": [0],
            },
        )

        # Create axis labels
        x_label = Tex("z", font_size=48, color=WHITE).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Tex("ReLU(z)", font_size=48, color=WHITE).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # ReLU function
        x_vals = np.linspace(-3, 5, 1000)
        relu_points = []
        for x in x_vals:
            relu_val = max(0, x)  # ReLU function
            relu_points.append(axes.c2p(x, relu_val))

        relu_graph = VMobject()
        relu_graph.set_points_as_corners(relu_points)
        relu_graph.set_stroke(GREEN, width=6)

        # ReLU derivative function (step function)
        relu_derivative_points = []
        for x in x_vals:
            derivative_val = 1 if x > 0 else 0  # ReLU derivative
            relu_derivative_points.append(axes.c2p(x, derivative_val * 0.8))  # Scale for visibility

        relu_derivative_graph = VMobject()
        relu_derivative_graph.set_points_as_corners(relu_derivative_points)
        relu_derivative_graph.set_stroke(ORANGE, width=6)

        # ReLU title and formula positioned in top left
        relu_title = Text("ReLU Function", font_size=40, color=GREEN)
        relu_title.to_corner(UL, buff=0.5)

        relu_formula = Tex(r"ReLU(z) = \max(0, z)", font_size=32, color=GREEN).set_color(GREEN)
        relu_formula.next_to(relu_title, DOWN, buff=0.2)
        relu_formula.shift(RIGHT*1.8+DOWN*1.5)
      
        # Initial derivative formula
        derivative_formula_1 = Tex(r"ReLU'(z) = \begin{cases} 1 & \ if \ z > 0 \\ 0 & \ if \ z \leq 0 \end{cases}", 
                                 font_size=26, color=ORANGE).set_color(ORANGE)
        derivative_formula_1.next_to(relu_formula, DOWN, buff=0.4)

        # Leaky ReLU components (initially hidden)
        alpha = 0.1  # Leaky ReLU parameter
        
        # Leaky ReLU function
        leaky_relu_points = []
        for x in x_vals:
            leaky_relu_val = max(alpha * x, x)  # Leaky ReLU function
            leaky_relu_points.append(axes.c2p(x, leaky_relu_val))

        leaky_relu_graph = VMobject()
        leaky_relu_graph.set_points_as_corners(leaky_relu_points)
        leaky_relu_graph.set_stroke(BLUE, width=6)

        # Leaky ReLU derivative function
        leaky_relu_derivative_points = []
        for x in x_vals:
            derivative_val = 1 if x > 0 else alpha  # Leaky ReLU derivative
            leaky_relu_derivative_points.append(axes.c2p(x, derivative_val * 0.8))  # Scale for visibility

        leaky_relu_derivative_graph = VMobject()
        leaky_relu_derivative_graph.set_points_as_corners(leaky_relu_derivative_points)
        leaky_relu_derivative_graph.set_stroke(RED, width=6).shift(DOWN*0.066)

        # Leaky ReLU title and formulas
        leaky_relu_title = Text("Leaky ReLU Function", font_size=40, color=BLUE)
        leaky_relu_title.to_corner(UL, buff=0.5)

        leaky_relu_formula = Tex(r"LReLU(z) = \max(\alpha z, z)", font_size=32, color=BLUE).set_color(BLUE)
        leaky_relu_formula.move_to(relu_formula)

        alpha_parameter = Tex(r"\alpha = 0.1", font_size=28, color=BLUE).set_color(BLUE)
        alpha_parameter.next_to(leaky_relu_formula, ORIGIN).shift(DOWN*0.4)

        leaky_derivative_formula = Tex(r"LReLU'(z) = \begin{cases} 1 & \ if \ z > 0 \\ \alpha & \ if \ z \leq 0 \end{cases}", 
                                     font_size=26, color=RED).set_color(RED)
        leaky_derivative_formula.move_to(derivative_formula_1)

        # New y-axis label for Leaky ReLU
        y_label_leaky = Tex("LReLU(z)", font_size=48, color=WHITE).move_to(y_label)

        # Animation
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)

        self.play(Write(relu_formula))
        self.play(ShowCreation(relu_graph), run_time=2)
        self.wait(2)

        self.play(Write(derivative_formula_1))
        self.play(ShowCreation(relu_derivative_graph) , run_time=2)
        self.wait(2.8)  # Wait as requested

        # Transform to Leaky ReLU
        self.play(
            Transform(relu_formula, leaky_relu_formula),
            Transform(y_label, y_label_leaky),
            Transform(relu_graph, leaky_relu_graph),
            Write(alpha_parameter),
            Transform(derivative_formula_1, leaky_derivative_formula),
            Transform(relu_derivative_graph, leaky_relu_derivative_graph),

            run_time=1.2
        )
        
        self.wait(3)



class SwishScene(Scene):
    def construct(self):
        
        self.camera.frame.scale(0.65)
        # Set up axes for Swish function (no ticks)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 2.3, 1],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,  # Removed ticks
                "numbers_to_exclude": [0],
            },
        )

        # Create axis labels
        x_label = Tex("z", font_size=48, color=WHITE).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Tex("Swish(z)", font_size=38, color=WHITE).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # Swish function
        x_vals = np.linspace(-3, 3, 1000)
        swish_points = []
        for x in x_vals:
            sigmoid_val = 1 / (1 + np.exp(-x))
            swish_val = x * sigmoid_val  # Swish function: x * sigmoid(x)
            swish_points.append(axes.c2p(x, swish_val))

        swish_graph = VMobject()
        swish_graph.set_points_as_corners(swish_points)
        swish_graph.set_stroke(MAROON_B, width=6)

        # Swish derivative function
        swish_derivative_points = []
        for x in x_vals:
            sigmoid_val = 1 / (1 + np.exp(-x))
            derivative_val = sigmoid_val * (1 + x * (1 - sigmoid_val))  # Swish derivative
            swish_derivative_points.append(axes.c2p(x, derivative_val))

        swish_derivative_graph = VMobject()
        swish_derivative_graph.set_points_as_corners(swish_derivative_points)
        swish_derivative_graph.set_stroke(YELLOW_B, width=6)

        # Swish title and formula positioned in top left
        swish_title = Text("Swish Function", font_size=40, color=MAROON_B)
        swish_title.to_corner(UL, buff=0.5)

        swish_formula = Tex(r"Swish(z) = z \cdot \sigma(z)", font_size=30, color=MAROON_B).set_color(MAROON_B)
        swish_formula.next_to(swish_title, DOWN, buff=0.2)
        swish_formula.shift(RIGHT*2.299+DOWN*1)

        # Alternative formula showing sigmoid explicitly
        swish_formula_expanded = Tex(r"Swish(z) = \frac{z}{1 + e^{-z}}", font_size=30, color=MAROON_B).set_color(MAROON_B)
        swish_formula_expanded.next_to(swish_formula, DOWN, buff=0.3)

        # Derivative formula
        derivative_formula = Tex(r"Swish'(z) = \sigma(z)(1 + z(1-\sigma(z)))", font_size=36, color=YELLOW_B).set_color(YELLOW_B)
        derivative_formula.next_to(swish_formula_expanded, DOWN, buff=0.5)


        # Zero line for reference
        zero_line = DashedLine(
            start=axes.c2p(-3, 0), 
            end=axes.c2p(3, 0), 
            color=GREY, 
            stroke_width=1,
            opacity=0.5
        )

        derivative_formula.next_to(axes.c2p(1.5, 3.5), ORIGIN)
        
        # Animation
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))

        # Show zero reference line
        self.play(ShowCreation(zero_line))
        self.wait(0.5)

        swish_formula.shift(DOWN*0.75+RIGHT*0.29)
        swish_formula_expanded.shift(DOWN*0.75+RIGHT*0.29)
        self.play(Write(swish_formula))
        self.play(Write(swish_formula_expanded))
        self.wait(1.5)

        self.play(ShowCreation(swish_graph), run_time=2.5)

        self.wait(1)

        self.embed()

        derivative_formula.next_to(axes, DOWN)


        self.play(Write(derivative_formula))
        self.wait()
        self.play(ShowCreation(swish_derivative_graph), run_time=2)
        self.wait(1.5)

        self.wait(3)
