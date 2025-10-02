from manimlib import *
import numpy as np

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

        relu_formula = Tex(r"ReLU(z) = \max(0, z)", font_size=32, color=GREEN)
        relu_formula.next_to(relu_title, DOWN, buff=0.2)
        relu_formula.shift(RIGHT*1.8+DOWN*1.5)
      
        # Initial derivative formula
        derivative_formula_1 = Tex(r"ReLU'(z) = \begin{cases} 1 & if  \ z > 0 \\ 0 & if  \ z \leq 0 \end{cases}", 
                                 font_size=26, color=ORANGE)
        derivative_formula_1.next_to(relu_formula, DOWN, buff=0.4)


        # Animation
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)

        self.play(Write(relu_formula))
        self.play(ShowCreation(relu_graph))
        self.wait(2)

        self.play(Write(derivative_formula_1))
        self.play(ShowCreation(relu_derivative_graph))
        self.wait(5)  # Wait 5 seconds as requested

