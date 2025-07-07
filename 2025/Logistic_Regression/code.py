from manimlib import *
import numpy as np


class LogisticRegressionIntro(Scene):
    def construct(self):
        # Initial True/False labels
        t = Text("True").scale(2).set_color("#00FF00").shift(LEFT*3.35 + UP*2.17)
        f = Text("False").scale(2).set_color("#FF0000").next_to(t, RIGHT, buff=2.37)
        
        self.play(ShowCreation(t), run_time=0.5)
        self.play(ShowCreation(f), run_time=0.5)
        
        # 1/0 labels
        one = Text("1").scale(2).set_color("#00FF00").next_to(t, DOWN, buff=1.2)
        zero = Text("0").scale(2).set_color("#FF0000").next_to(f, DOWN, buff=1.2)
        
        self.play(ShowCreation(one), run_time=0.5)
        self.play(ShowCreation(zero), run_time=0.5)
        
        # Yes/No labels
        yes = Text("Yes").scale(2).set_color("#00FF00").next_to(one, DOWN, buff=1.2)
        no = Text("No").scale(2).set_color("#FF0000").next_to(zero, DOWN, buff=1.2)
        
        self.play(ShowCreation(yes), run_time=0.5)
        self.play(ShowCreation(no), run_time=0.5)
        self.wait(3)
        

        # Create simple axis with thicker stroke
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.5, 1.5, 0.5],
            height=6,
            width=8,
            axis_config={"stroke_width": 6}
        ).shift(RIGHT*15)
        
        # Create some random data points for binary classification - more dispersed
        np.random.seed(42)
        x_data = np.random.uniform(-2.8, 2.8, 25)  # More spread and more points
        # Create more realistic binary data with some noise
        y_binary = (x_data > np.random.uniform(-0.5, 0.5, 25)).astype(int)
        y_data = y_binary + np.random.normal(0, 0.15, 25)  # More dispersion
        y_data = np.clip(y_data, 0, 1)
        
        # Create bigger dots with yellow color and full opacity
        dots = VGroup()
        for i in range(len(x_data)):
            dot = Dot(axes.c2p(x_data[i], y_data[i]), color=YELLOW_E, radius=0.15).set_color(YELLOW_E)
            dots.add(dot)
        
        # Show axes and dots
        self.play(ShowCreation(axes), self.camera.frame.animate.shift(RIGHT*15))
        self.play(ShowCreation(dots))
        self.wait(2)
        
        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )
        
        # Show sigmoid curve
        self.play(ShowCreation(sigmoid_curve))
        self.wait(2)
        
        # Add horizontal line at y = 0.5 (intersection point)
        horizontal_line = axes.get_graph(
            lambda x: 0.5,
            x_range=[-3, 3],
            color=WHITE,
            stroke_width=6
        )
        
        self.play(ShowCreation(horizontal_line))
        self.wait(1)
        
        # Create filled regions based on horizontal line at y = 0.5
        # Green region (above the horizontal line, y > 0.5)
        green_region = Polygon(
            axes.c2p(-3, 0.5), axes.c2p(3, 0.5), 
            axes.c2p(3, 1.5), axes.c2p(-3, 1.5),
            fill_color="#00FF00", fill_opacity=0.1, stroke_width=0
        )
        
        # Red region (below the horizontal line, y < 0.5)
        red_region = Polygon(
            axes.c2p(-3, -0.5), axes.c2p(3, -0.5), 
            axes.c2p(3, 0.5), axes.c2p(-3, 0.5),
            fill_color="#FF0000", fill_opacity=0.1, stroke_width=0
        )
        
        self.play(
            ShowCreation(green_region),
            ShowCreation(red_region)
        )
        self.wait(3)

        self.play(FadeOut(VGroup(green_region, red_region, horizontal_line, dots )))

        self.play(self.camera.frame.animate.shift(RIGHT*3).scale(1.1))


        sigmoid = Tex(r"\sigma(x) = \frac{1}{1 + e^{-x}}").next_to(axes, RIGHT, buff=1).scale(1.7).shift(RIGHT*0.4)

        self.play(Write(sigmoid))

        self.wait(2)

        x = sigmoid[-1]

        rect = always_redraw(lambda: SurroundingRectangle(x,color=PINK))

        self.play(x.animate.set_color(YELLOW_C), ShowCreation(rect))



        # First, transform to steeper curve (scale x by 2)
        sigmoid_steep = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-4*x)),  # Scale x by 2
            x_range=[-3, 3],
            color="#00ff00",  # Orange color
            stroke_width=8
        )
        

        self.play(
            Transform(sigmoid_curve, sigmoid_steep),
            x.animate.scale(2)
           
        )
        self.wait(2)
        
        # Transform to gentler curve (scale x by 0.2)
        sigmoid_gentle = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-x)),  # Scale x by 0.2
            x_range=[-3, 3],
            color="#00FF00",  # Blue color
            stroke_width=8
        )
        

        self.play(
            Transform(sigmoid_curve, sigmoid_gentle),
            x.animate.scale(0.25)
        )
        self.wait(2)
        
        # Transform back to original
        sigmoid_original = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )
        
        sigmoid_original_eq = Tex(r"\sigma(x) = \frac{1}{1 + e^{-x}}").next_to(axes, RIGHT, buff=1).scale(1.7).shift(RIGHT*0.4)
        
        self.play(
            Transform(sigmoid_curve, sigmoid_original),
            x.animate.scale(2)
        )
        self.wait(2)

        self.play(FadeOut(axes), FadeOut(sigmoid_curve), FadeOut(rect))

        self.play(
            self.camera.frame.animate.scale(0.7*0.9).shift(RIGHT*4+DOWN*1.5)
        )


        conditions = Tex(
    
    r"\begin{cases}"
    r"x \to +\infty & \Longrightarrow \sigma(x) \approx 1 \\"
    r"x = 0 & \Longrightarrow \sigma(x) = 0.5 \\"
    r"x \to -\infty & \Longrightarrow \sigma(x) \approx 0"
    r"\end{cases}"
).next_to(sigmoid, DOWN, buff=1)

        self.play(Write(conditions))
        self.wait(2)

        pointer = Arrow(
            conditions.get_top(),
            conditions.get_top()+RIGHT*1.12,
            buff=0.1,
            color=PINK,
            stroke_width=8,
            fill_color=PINK,
            fill_opacity=1
        ).set_color(ORANGE).shift(LEFT*4.3+DOWN*0.3)

        self.play(ShowCreation(pointer))

        self.wait(2)

        self.play(pointer.animate.shift(DOWN*0.7))
        self.wait(2)
        self.play(pointer.animate.shift(DOWN*0.7))
        self.wait(2)

        self.wait(2)


class LogsiticRegression(Scene):
    def construct(self):

        z = Text("z = wx + b").scale(1.9).shift(UP)

        self.play(ShowCreation(z))

        self.wait(2)

        self.play(z[3].animate.set_color(YELLOW))

        self.wait(2)

        self.play(z[2].animate.set_color(YELLOW), z[3].animate.set_color(WHITE))

        w = Text("weight").scale(1.5).next_to(z, DOWN, buff=1.5)
        b = Text("bias").scale(1.5).next_to(z, DOWN, buff=1.5)

        self.play(ShowCreation(w))

        self.wait(2)

        self.play(z[2].animate.scale(1.5))
        self.wait(2)
        self.play(z[2].animate.scale(1/1.5))
        self.play(z[2].animate.scale(0.5))
        
        self.wait(2)


        self.play(z[2].animate.scale((2)), )

        self.play(z[2].animate.set_color(WHITE), Uncreate(w), z[-1].animate.set_color(YELLOW))
        self.play(ShowCreation(b))

        

        self.wait(2)

        self.play(Uncreate(b), z[-1].animate.set_color(WHITE),)

        axes = Axes(
            x_range=[0, 15],
            y_range=[0, 8],
            axis_config={"color": WHITE, "include_ticks": False, "include_numbers": False, "stroke_width": 4.2},
        ).scale(0.75)
        
        x_label = Text("x").next_to(axes.x_axis, DOWN).shift(RIGHT*5.5+DOWN*0.1)
        y_label = Text("z").next_to(axes.y_axis, UP)
        
        self.play(ReplacementTransform(z, axes), self.camera.frame.animate.shift(LEFT*0.14))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)


        # Create the line equation y = mx + c
        m_value = 0.5
        c_value = 1.5
        
        # Create the line function (1/5 smaller range)
        line = axes.get_graph(lambda x: m_value * x + c_value, color=YELLOW, stroke_width=6, x_range=[0, 13])
        

        # Show the line and equation
        self.play(ShowCreation(line))
        self.wait(1)
        

        original_line = line.copy()
        
        # Create steeper line (1/5 smaller range)
        steep_line = axes.get_graph(lambda x: 1.2 * x + c_value, color=YELLOW, stroke_width=6, x_range=[0, 13])
        self.play(Transform(line, steep_line))
        self.wait(1)
        
        # Create flatter line (1/5 smaller range)
        flat_line = axes.get_graph(lambda x: 0.2 * x + c_value, color=YELLOW, stroke_width=6, x_range=[0, 13])
        self.play(Transform(line, flat_line))
        self.wait(1)
        
        # Back to original slope
        self.play(Transform(line, original_line))
        self.wait(1)

        origin_point = axes.coords_to_point(0, 0)
        
        # Create brace between origin and y-intercept
        brace =always_redraw(lambda: Brace(
            Line(origin_point, line.get_start()),
            direction=LEFT,
            buff=0.2
        ).shift(LEFT*0.06))
        
        brace_text = always_redraw(lambda: brace.get_text("b").scale(1).shift(LEFT*0.09))

        self.play(ShowCreation(brace), Write(brace_text))

        self.wait(2)

        self.play(line.animate.shift(UP*2))
        self.play(line.animate.shift(DOWN*2))

        self.wait(2)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.5, 1.5, 0.5],
            height=6,
            width=8,
            axis_config={"stroke_width": 6}
        ).shift(RIGHT*15)

        self.play(ShowCreation(axes), self.camera.frame.animate.shift(RIGHT*15+UP*0.4).scale(0.98))

        x_label = Tex("z").next_to(axes.x_axis, DOWN).shift(RIGHT*4.5+DOWN*0.1).scale(1.6)
        y_label = Tex(r"\sigma(z)").next_to(axes.y_axis, UP).scale(1.4).shift(UP*0.1)
        
        self.play(Write(x_label), Write(y_label))
        self.wait(1)

        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )
        
        # Show sigmoid curve
        self.play(ShowCreation(sigmoid_curve))
        self.wait(2)


        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve1 = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-3*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve2 = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-1*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )


        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve3 = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2.5*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        self.play(Transform(sigmoid_curve, sigmoid_curve1))
        self.play(Transform(sigmoid_curve, sigmoid_curve2))
        self.play(Transform(sigmoid_curve, sigmoid_curve3))

        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve1 = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-6*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve2 = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-0.6*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )


        # Create sigmoid curve (decision boundary) with thick stroke
        sigmoid_curve3 = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-1.5*x)),
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        self.play(Transform(sigmoid_curve, sigmoid_curve1))
        self.play(Transform(sigmoid_curve, sigmoid_curve2))
        self.play(Transform(sigmoid_curve, sigmoid_curve3))

        self.wait(2)


        # Create new axes for the final plot
        final_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.5, 1.5, 0.5],
            height=6,
            width=8,
            axis_config={"stroke_width": 6}
        ).shift(RIGHT*15)  # Same position as sigmoid_axes
        
        # New labels
        x_final_label = Tex("x").next_to(final_axes.x_axis, DOWN).shift(RIGHT*4.5+DOWN*0.1).scale(1.6)
        sigma_x_label = Tex(r"\sigma(wx+b)").next_to(final_axes.y_axis, UP).scale(1.4).shift(UP*0.1)
        
        # Create the final sigmoid curve as a function of x
        final_sigmoid_curve = final_axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*(0.5*x + 1.5))),  # Using w=0.5, b=1.5 from earlier
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )
        
        # Transform the labels and curve
        self.play(
            Transform(x_label, x_final_label),
            Transform(y_label, sigma_x_label),
            Transform(sigmoid_curve, final_sigmoid_curve)
        )
        self.wait(3)
        
        final_sigmoid_curve1 = final_axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*(1.5*x + 2.5))),  # Using w=0.5, b=1.5 from earlier
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        final_sigmoid_curve2 = final_axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*(2.5*x - 0.5))),  # Using w=0.5, b=1.5 from earlier
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        final_sigmoid_curve3 = final_axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*(0.99*x - 3.5))),  # Using w=0.5, b=1.5 from earlier
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        final_sigmoid_curve4 = final_axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*(0*x + 4.5))),  # Using w=0.5, b=1.5 from earlier
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )

        final_sigmoid_curve5 = final_axes.get_graph(
            lambda x: 1 / (1 + np.exp(-2*(-2*x + 0.5))),  # Using w=0.5, b=1.5 from earlier
            x_range=[-3, 3],
            color="#00FF00",
            stroke_width=8
        )


        self.play(Transform(sigmoid_curve, final_sigmoid_curve1))
        self.play(Transform(sigmoid_curve, final_sigmoid_curve2))
        self.play(Transform(sigmoid_curve, final_sigmoid_curve3))
        self.play(Transform(sigmoid_curve, final_sigmoid_curve4))
        self.play(Transform(sigmoid_curve, final_sigmoid_curve5))

        self.wait(2)

        
