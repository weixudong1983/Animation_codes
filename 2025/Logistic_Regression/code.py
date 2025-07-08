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


class LossFunction(Scene):
    def construct(self):
        # Initial equations
        true_y = Tex("y")
        true_y.to_edge(UP).shift(DOWN*2).scale(2.2)
        
        # Predicted output
        pred_y = Tex("\\hat{y} = \\sigma(wx + b)").next_to(true_y, DOWN, buff=1.3).scale(2.2).shift(DOWN)
        
        self.play(Write(true_y))
        self.wait(2)
        self.play(Write(pred_y))
        self.wait(2)
        
        # Transform to MSE loss function
        mse_loss = Tex("L = \\frac{1}{2}(y - \\hat{y})^2")
        mse_loss.scale(2)
        mse_loss.move_to(ORIGIN)
        
        # Animate transformation to MSE
        self.play(
            ReplacementTransform(VGroup(true_y, pred_y), mse_loss),
        )
        self.wait(2)
        
        # Substitute the sigmoid term
        expanded_loss = Tex("L = \\frac{1}{2}(y - \\sigma(wx + b))^2")
        expanded_loss.scale(2)
        expanded_loss.move_to(ORIGIN)
        
        self.play(Transform(mse_loss, expanded_loss))
        self.wait(2)

        brace = Brace(mse_loss[8:-2], DOWN, buff=0.4)
        temp = brace.get_text("MSE Loss Term").shift(DOWN*0.32).set_color("#FF0000")
        
        self.play(
            GrowFromCenter(brace),
            Write(temp)
        )
        self.wait(2)

        # Create axes with proper range that matches the function
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 16, 2],  # Increased y-range for deeper valleys
            height=6,
            width=10,
            axis_config={"stroke_width": 4, "include_tip": True}
        ).shift(RIGHT*15)

        self.play(ShowCreation(axes), self.camera.frame.animate.shift(RIGHT*15))
        self.wait(1)
        
        # Create a curve
        demo = axes.get_graph(
            lambda x: func(x),
            x_range=[0, 10],  # Reduced x-range to match axes
            color=RED,
            stroke_width=8
        )
        
        # Show sigmoid curve
        self.play(ShowCreation(demo))
        self.wait(2)
        
        # Create a yellow dot that will roll down the curve
        dot = Dot(radius=0.2).set_color(YELLOW)
        # Start the dot at a peak (around x=4.7, which is near a local maximum)
        start_x = 7.23
        start_point = axes.c2p(start_x, func(start_x))
        dot.move_to(start_point)
        
        # Show the dot appearing
        self.play(FadeIn(dot))
        self.wait(1)
        
        # Create a value tracker to animate the dot's position
        x_tracker = ValueTracker(start_x)
        
        # Update function to keep the dot on the curve
        def update_dot(mob):
            x_val = x_tracker.get_value()
            y_val = func(x_val)
            new_point = axes.c2p(x_val, y_val)
            mob.move_to(new_point)
        
        dot.add_updater(update_dot)
        
        # Animate the dot rolling down to a local minimum
        # It will get stuck at the local minimum around x=6.3
        self.play(
            x_tracker.animate.set_value(4.5),
            rate_func=smooth,
            run_time=2
        )
        self.play(
            x_tracker.animate.set_value(5.4),
            rate_func=smooth,
            run_time=1.2
        )
        self.wait(1)
        
        # Add a text label showing it's stuck at local minimum
        stuck_text = Text("Stuck at Local Minimum!", font_size=36, color=YELLOW)
        stuck_text.next_to(dot, UP, buff=1.5).shift(UP*1.5)
        
        self.play(Write(stuck_text))
        self.wait(2)

        arrow = Arrow(dot.get_center(), dot.get_center()+DOWN*1.4,stroke_width=7, color=YELLOW).set_color(GREEN).shift(DOWN*0.2).rotate(PI)

        self.play(ShowCreation(arrow))

        self.wait(2)

        self.play(arrow.animate.shift(UP*0.99+LEFT*3.1).rotate(PI))

        self.wait(2)

        self.play(FadeOut(arrow), FadeOut(stuck_text), FadeOut(dot))

        demo1 = axes.get_graph(
            lambda x: (x-4)**2*0.6 + 1 ,
            x_range=[0.5, 10],  # Reduced x-range to match axes
            color=GREEN,
            stroke_width=8
        )

        self.play(Transform(demo, demo1))
        
        self.wait(2)

        # Create a new dot for the green function
        dot2 = Dot(radius=0.2).set_color(RED)
        # Start the dot at a higher point on the new function
        start_x2 = 7.5
        start_point2 = axes.c2p(start_x2, new_func(start_x2))
        dot2.move_to(start_point2)
        
        # Show the new dot appearing
        self.play(FadeIn(dot2))
        self.wait(1)
        
        # Create a new value tracker for the second dot
        x_tracker2 = ValueTracker(start_x2)
        
        # Update function to keep the dot on the new curve
        def update_dot2(mob):
            x_val = x_tracker2.get_value()
            y_val = new_func(x_val)
            new_point = axes.c2p(x_val, y_val)
            mob.move_to(new_point)
        
        dot2.add_updater(update_dot2)
        
        # Animate the dot rolling down to the global minimum at x=4
        self.play(
            x_tracker2.animate.set_value(4.0),
            rate_func=smooth,
            run_time=3
        )
        self.wait(1)
        
        # Add a text label showing it reached the global minimum
        success_text = Text("Reached Global Minimum!", font_size=36, color=GREEN)
        success_text.next_to(dot2, UP, buff=1.5).shift(UP*1.5)
        
        self.play(Write(success_text))
        self.wait(2)

        self.play(FadeOut(success_text), FadeOut(dot2), FadeOut(mse_loss),
                  self.camera.frame.animate.shift(LEFT*14.5+DOWN*0.15), FadeOut(temp), FadeOut(brace))
        
        # Create the TeX object
        formula = Tex(
            r"""
            \begin{aligned}
            y = 1 &\Longrightarrow L = -\log(\hat{y}) \\
            y = 0 &\Longrightarrow L = -\log(1 - \hat{y})
            \end{aligned}
            """
        ).shift(UP*2.3).scale(1.5)
        

        self.play(Write(formula))
        self.wait(2)

        arrow = Arrow(formula.get_right(), formula.get_right()+RIGHT*1.6, stroke_width=7, color=YELLOW).set_color(YELLOW).rotate(PI).shift(UP*0.57+LEFT*0.8)
        self.play(ShowCreation(arrow))

        self.wait(2)

        # Correct axes
        axes = Axes(
            x_range=[0, 1.2, 1],
            y_range=[0, 2,9],  
            height=6,
            width=10,
            axis_config={"stroke_width": 4, "include_ticks": True, "include_tip": True }
        ).next_to(formula, DOWN, buff=0.3).scale(0.6).shift(UP * 0.4 + RIGHT * 1)
        
        x_label = Tex(r"\hat{y}").next_to(axes.x_axis, DOWN).scale(1.2).shift(RIGHT * 3.5 + UP * 0.299)
        y_label = Tex("Loss").next_to(axes.y_axis, UP).shift(LEFT * 0.83 + DOWN * 0.66).scale(1.1)
        
        self.play(ShowCreation(axes))
        one = Tex("1").next_to(x_label, LEFT).shift(LEFT*1.1 + 0.082*DOWN)
        self.play(Write(x_label), Write(y_label), Write(one))
        self.wait(1)


        log_graph = axes.get_graph(
            lambda x: -np.log(x),
            x_range=[0.1, 0.99],
            color="#00DDFF",
            stroke_width=6
        )
        
        # Add the graph with animation
        self.play(ShowCreation(log_graph))
        self.wait(2)

        # Create a new dot for the green function
        dot2 = Dot(radius=0.2).set_color(YELLOW)
        # Start the dot at a higher point on the new function
        start_x2 = 0.5
        start_point2 = axes.c2p(start_x2, -np.log(start_x2))
        dot2.move_to(start_point2)
        
        # Show the new dot appearing
        self.play(FadeIn(dot2))
        self.wait(1)
        
        # Create a new value tracker for the second dot
        x_tracker2 = ValueTracker(start_x2)
        
        # Update function to keep the dot on the new curve
        def update_dot2(mob):
            x_val = x_tracker2.get_value()
            y_val = -np.log(x_val)
            new_point = axes.c2p(x_val, y_val)
            mob.move_to(new_point)
        
        dot2.add_updater(update_dot2)
        
        # Animate the dot rolling down to the global minimum at x=4
        self.play(
            x_tracker2.animate.set_value(0.98),
            rate_func=smooth,
            run_time=1.3
        )
        self.wait(2)  

        self.play(
            x_tracker2.animate.set_value(0.1),
            rate_func=smooth,
            run_time=1.3
        )
        self.wait(2)

        self.play(FadeOut(VGroup(dot2, log_graph)))
        self.play(arrow.animate.shift(RIGHT+DOWN*1.1))

        log_graph = axes.get_graph(
            lambda x: -np.log(1-x),
            x_range=[0, 0.92],
            color="#00DDFF",
            stroke_width=6
        )
        
        # Add the graph with animation
        self.play(ShowCreation(log_graph))
        self.wait(2)

        # Create a new dot for the green function
        dot2 = Dot(radius=0.2).set_color(YELLOW)
        # Start the dot at a higher point on the new function
        start_x2 = 0.5
        start_point2 = axes.c2p(start_x2, -np.log(1-start_x2))
        dot2.move_to(start_point2)
        
        # Show the new dot appearing
        self.play(FadeIn(dot2))
        self.wait(1)
        
        # Create a new value tracker for the second dot
        x_tracker2 = ValueTracker(start_x2)
        
        # Update function to keep the dot on the new curve
        def update_dot2(mob):
            x_val = x_tracker2.get_value()
            y_val = -np.log(1-x_val)
            new_point = axes.c2p(x_val, y_val)
            mob.move_to(new_point)
        
        dot2.add_updater(update_dot2)
        
        # Animate the dot rolling down to the global minimum at x=4
        self.play(
            x_tracker2.animate.set_value(0.9),
            rate_func=smooth,
            run_time=1.3
        )
        self.wait(2)  

        self.play(
            x_tracker2.animate.set_value(0),
            rate_func=smooth,
            run_time=1.3
        )
        self.wait(2)

        self.play(FadeOut(VGroup(log_graph, dot2, axes, y_label, x_label, one, arrow)))

        loss = Tex(
    r"L(y, \hat{y}) = - \bigl[ y \log(\hat{y}) + (1 - y) \log(1 - \hat{y}) \bigr]"
).scale(1.4).shift(DOWN*0.9+RIGHT*0.5)
        
        self.play(TransformFromCopy(formula, loss), self.camera.frame.animate.shift(UP*0.7))

        self.wait(2)

        cost = Tex(
    r"J(w, b) = \frac{1}{m}\sum_{i=1}^m L(\hat{y}^{(i)}, y^{(i)})"
).scale(1.6).move_to(loss)
        
        self.play(ReplacementTransform(loss, cost))

        self.wait(2)

        temp = Tex(
    r"J(w, b) = -\frac{1}{m}\sum_{i=1}^m \Bigl[ y^{(i)} \log(\hat{y}^{(i)}) "
    r"+ (1 - y^{(i)}) \log(1 - \hat{y}^{(i)}) \Bigr]"
).move_to(cost)
        
        self.play(Transform(cost, temp))

        rect = SurroundingRectangle(cost, color=YELLOW, stroke_width=5).scale(1.04)
        self.play(ShowCreation(rect))

        self.wait(2)


class Simulation(Scene):
    def construct(self):
        self.camera.frame.shift(DOWN * 0.2 + LEFT*0.5)

        # Axes
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 1.1, 0.5],
            height=6,
            width=10,
            axis_config={"stroke_width": 6, "include_tip": True},
        )

        x_label = Text("Amount Of Cholesterol", font_size=32).next_to(axes.x_axis, DOWN).shift(DOWN * 0.1).set_color(RED)
        y_label = Text("Disease Probability", font_size=32).next_to(axes.y_axis, LEFT).rotate(PI / 2).shift(RIGHT * 1.77).set_color(GREEN)

        self.play(ShowCreation(axes), Write(x_label), Write(y_label))
        self.wait(1)

        # Generate training data
        np.random.seed(42)
        n_points = 30

        chol_low = np.random.uniform(10, 40, n_points // 2)
        chol_high = np.random.uniform(60, 90, n_points // 2)

        y_low = np.zeros(n_points // 2)  # Class 0
        y_high = np.ones(n_points // 2)  # Class 1

        cholesterol_values = np.concatenate([chol_low, chol_high])
        labels = np.concatenate([y_low, y_high])

        # Shuffle
        indices = np.arange(n_points)
        np.random.shuffle(indices)
        cholesterol_values = cholesterol_values[indices]
        labels = labels[indices]

        data_points = []
        for i in range(n_points):
            x_coord = cholesterol_values[i]
            y_coord = labels[i]

            point_pos = axes.c2p(x_coord, y_coord)
            dot = Dot(point_pos, radius=0.12, color=YELLOW).set_color(YELLOW)
            data_points.append(dot)

        self.play(
            LaggedStart(
                *[FadeIn(dot) for dot in data_points],
                lag_ratio=0.05,
                run_time=3
            )
        )

        self.wait(1)

        # Start with random sigmoid
        sigmoid_curve = axes.get_graph(
            lambda x: 1 / (1 + np.exp(-(0.1 * (x-15) - 3))),
            x_range=[0, 100],
            color="#00FF00",
            stroke_width=8
        )
        self.play(ShowCreation(sigmoid_curve))
        self.wait(0.5)

        # Iterate step by step sigmoid improvements
        sig_params = [
            (0.12, 5),
            (0.18, 7),
            (0.23, 9),
            (0.26, 11),
            (0.38, 13),
            

        ]

        for a, c in sig_params:
            new_curve = axes.get_graph(
                lambda x, a=a, c=c: 1 / (1 + np.exp(-a * ((x-15) - 50 + c))),
                x_range=[0, 100],
                color="#00FF00",
                stroke_width=8
            )
            self.play(Transform(sigmoid_curve, new_curve), run_time=0.8)

        self.wait(1.5)




        # Fade out training dots
        self.play(*[FadeOut(dot) for dot in data_points])
        self.wait(1)



        # Create regions divided by threshold 0.5
        threshold_line = DashedLine(
            start=axes.c2p(0, 0.5),
            end=axes.c2p(100, 0.5),
            color=WHITE,
            stroke_width=2
        )
        

        self.play(
            ShowCreation(threshold_line),
        )
        self.wait(1)
        
        dot = Dot(radius=0.2).set_color(YELLOW).move_to(axes.c2p(50, 0))
        self.play(ShowCreation(dot))
        
        # Vertical dashed line from dot to curve
        predicted_y = 1 / (1 + np.exp(-0.38 * ((50-15) - 50 + 13)))
        curve_point = axes.c2p(50, predicted_y)
        
        vertical_line = DashedLine(
            start=axes.c2p(50, 0),
            end=curve_point,
            color=BLUE,
            stroke_width=3
        ).set_z_index(-1)
        
        # Horizontal dashed line from curve to y-axis
        horizontal_line = DashedLine(
            start=curve_point,
            end=axes.c2p(0, predicted_y),
            color=BLUE,
            stroke_width=5
        ).set_z_index(-1)
        
        self.play(ShowCreation(vertical_line))

        a = dot.copy().scale(0.7).set_color(RED).move_to(axes.c2p(50, predicted_y))
        self.play(GrowFromCenter(a))

        self.play(ShowCreation(horizontal_line))
        
        a = dot.copy().set_color("#eeff00").move_to(axes.c2p(0, predicted_y))

        self.play(GrowFromCenter(a))

        self.wait(2)
