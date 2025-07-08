from manimlib import *
import numpy as np

# Simple version with minimal configuration
class LinearRegressionIntro(Scene):
    def construct(self):
        self.camera.frame.scale(1.5)
        
        axes = Axes(
            x_range=[0, 15],
            y_range=[0, 8],
            axis_config={"color": WHITE, "include_ticks": False, "include_numbers": False, "stroke_width": 4.2},
        )
        
        x_label = Text("Size").next_to(axes.x_axis, DOWN).shift(RIGHT*7.6+DOWN*0.4)
        y_label = Text("Cost").next_to(axes.y_axis, UP).shift(UP*0.33)
        
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)
        
        # Create data points for linear regression
        # Generate 14 points that show a clear relationship but with realistic scatter
        np.random.seed(42)  # For reproducible results
        
        # Create x values spread across the range with some clustering
        x_values = np.array([2.1, 3.5, 4.2, 5.8, 6.1, 7.3, 8.0, 8.9, 9.4, 10.2, 11.0, 11.8, 12.3, 13.1])
        
        # Create y values with a clear trend but realistic variation
        slope = 0.45
        intercept = 1.2
        # Add controlled noise that maintains the relationship - reduce extreme high/low values
        noise = np.array([0.2, -0.2, 0.3, -0.1, 0.4, -0.2, 0.3, -0.3, 0.1, 0.2, -0.2, 0.3, -0.1, 0.2])
        y_values = slope * x_values + intercept + noise
        
        # Ensure y values are within our range
        y_values = np.clip(y_values, 1.0, 7.0)
        
        # Create the points
        points = []
        for i in range(len(x_values)):
            point_coords = axes.coords_to_point(x_values[i], y_values[i])
            dot = Dot(point_coords, radius=0.18).set_color(RED)
            points.append(dot)
        
        # Animate all points appearing simultaneously
        point_animations = [ShowCreation(point) for point in points]
        self.play(*point_animations, run_time=1.5)
        
        self.wait(2)
        
        # Compare three points one by one
        # Choose three points to highlight (indices 3, 7, 11 for good spread)
        highlight_indices = [3, 7, 11]
        
        current_highlighted_point = None
        current_x_line = None
        current_y_line = None
        
        for i, point_idx in enumerate(highlight_indices):
            # Reset previous point if it exists
            if current_highlighted_point is not None:
                self.play(
                    current_highlighted_point.animate.scale(1/1.8).set_color(RED),
                    FadeOut(current_x_line),
                    FadeOut(current_y_line),
                    run_time=0.5
                )
            
            # Highlight current point
            current_highlighted_point = points[point_idx]
            self.play(
                current_highlighted_point.animate.scale(1.8).set_color(YELLOW),
                run_time=0.5
            )
            
            # Get the coordinates of the highlighted point
            point_coords = current_highlighted_point.get_center()
            
            # Create perpendicular line to x-axis (vertical line down to x-axis)
            x_axis_point = axes.coords_to_point(x_values[point_idx], 0)
            current_x_line = DashedLine(
                point_coords, 
                x_axis_point, 
                color=BLUE, 
                stroke_width=3,
                dash_length=0.2
            ).set_z_index(-1)
            
            # Create perpendicular line to y-axis (horizontal line to y-axis)
            y_axis_point = axes.coords_to_point(0, y_values[point_idx])
            current_y_line = DashedLine(
                point_coords, 
                y_axis_point, 
                color=BLUE, 
                stroke_width=3,
                dash_length=0.2
            ).set_z_index(-1)
            
            # Animate the lines appearing
            self.play(
                ShowCreation(current_x_line),
                ShowCreation(current_y_line),
                run_time=0.8
            )
            
            self.wait(1.5)
        
        # Reset the last highlighted point
        if current_highlighted_point is not None:
            self.play(
                current_highlighted_point.animate.scale(1/1.8).set_color(RED),
                FadeOut(current_x_line),
                FadeOut(current_y_line),
                run_time=0.5
            )
        
        self.wait(2)

        # Calculate linear regression
        x_mean = np.mean(x_values)
        y_mean = np.mean(y_values)
        numerator = np.sum((x_values - x_mean) * (y_values - y_mean))
        denominator = np.sum((x_values - x_mean) ** 2)
        slope_fitted = numerator / denominator
        intercept_fitted = y_mean - slope_fitted * x_mean
        
        # Create initial horizontal line at y mean
        start_point = axes.coords_to_point(1, y_mean)
        end_point = axes.coords_to_point(14, y_mean)
        regression_line = Line(start_point, end_point, color=GREEN, stroke_width=8.5)
        
        self.play(ShowCreation(regression_line), run_time=1)
        self.wait(1)
        
        # Fit the line in 4 iterations
        iterations = 3
        for i in range(iterations):
            # Calculate intermediate slope and intercept for gradual fitting
            progress = (i + 1) / iterations
            current_slope = progress * slope_fitted
            current_intercept = y_mean + progress * (intercept_fitted - y_mean)
            
            # Calculate new line endpoints
            new_start_y = current_slope * 1 + current_intercept
            new_end_y = current_slope * 14 + current_intercept
            
            new_start_point = axes.coords_to_point(1, new_start_y)
            new_end_point = axes.coords_to_point(14, new_end_y)
            new_line = Line(new_start_point, new_end_point, color=GREEN, stroke_width=8)
            
            # Transform the line to fit better
            self.play(Transform(regression_line, new_line), run_time=1.2)
            self.wait(0.333)
        
        self.wait(2)


        # Fade out all the original dots
        dot_fadeout_animations = [FadeOut(dot) for dot in points]
        self.play(*dot_fadeout_animations, run_time=1)
        self.wait(1)
        
        # Step 1: Create a point on the X-axis representing the size we want to predict
        prediction_x = 9.5  # Choose a point on the x-axis
        x_axis_point_coords = axes.coords_to_point(prediction_x, 0)
        
        # Create the input dot on X-axis
        input_dot = Dot(x_axis_point_coords, radius=0.18, color=BLUE).set_color(BLUE)
        self.play(ShowCreation(input_dot.scale(1.5)), run_time=0.8)
        self.wait(1)
        
        # Step 2: Create vertical dotted line from X-axis to regression line
        prediction_y = slope_fitted * prediction_x + intercept_fitted
        intersection_point_coords = axes.coords_to_point(prediction_x, prediction_y)
        
        vertical_line = DashedLine(
            x_axis_point_coords,
            intersection_point_coords, 
            color=BLUE, 
            stroke_width=3,
            dash_length=0.2
        ).set_z_index(-1)
        
        self.play(ShowCreation(vertical_line), run_time=1)
        self.wait(0.5)
        
        # Step 3: Create the intersection point on the regression line
        intersection_dot = Dot(intersection_point_coords, radius=0.20, color=YELLOW).set_color(YELLOW)
        self.play(ShowCreation(intersection_dot.scale(1.6)), run_time=0.8)
        self.wait(0.5)
        
        # Step 4: Create horizontal dotted line from intersection point to Y-axis
        y_axis_point_coords = axes.coords_to_point(0, prediction_y)
        
        horizontal_line = DashedLine(
            intersection_point_coords,
            y_axis_point_coords, 
            color=BLUE, 
            stroke_width=3,
            dash_length=0.2
        ).set_z_index(-1)
        
        self.play(ShowCreation(horizontal_line), run_time=1)
        self.wait(0.5)
        
        # Step 5: Create the final prediction point on Y-axis
        output_dot = Dot(y_axis_point_coords, radius=0.18, color=RED).set_color(RED)
        self.play(ShowCreation(output_dot.scale(1.5)), run_time=0.8)
        
        self.wait(2)


class LineEquation(Scene):
    def construct(self):

        self.camera.frame.scale(1.5)
        
        # Create axes
        axes = Axes(
            x_range=[0, 15],
            y_range=[0, 8],
            axis_config={"color": WHITE, "include_ticks": False, "include_numbers": False, "stroke_width": 4.2},
        )
        
        x_label = Text("x").next_to(axes.x_axis, DOWN).shift(RIGHT*7.6+DOWN*0.4).scale(1.6)
        y_label = Text("y").next_to(axes.y_axis, UP).shift(UP*0.33).scale(1.6)
        
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)
        
        # Create the line equation y = mx + c
        m_value = 0.5
        c_value = 1.5
        
        # Create the line function (1/5 smaller range)
        line = axes.get_graph(lambda x: m_value * x + c_value, color=YELLOW, stroke_width=6, x_range=[0, 15])
        
        # Create equation text (shifted more to the right)
        equation = Tex("y = mx + c").scale(2.2).to_corner(UL).shift(RIGHT*2)
        
        # Show the line and equation
        self.play(ShowCreation(line))
        self.play(Write(equation))
        self.wait(1)
        
        # Transform to beta version (using different variable names)
        beta_equation = Tex(r"y = \beta_0 + \beta_1 x").scale(2.2).to_corner(UL).shift(RIGHT*2)
        self.play(Transform(equation, beta_equation))
        self.wait(1)
        
        # Transform back to y = mx + c form
        original_equation = Tex("y = mx + c").scale(2.2).to_corner(UL).shift(RIGHT*2)
        self.play(Transform(equation, original_equation))
        self.wait(1)
        
        # Create a separate equation for highlighting to avoid indexing issues
        highlight_equation = equation
        
        # Highlight the 'm' term with green rectangle
        m_highlight = SurroundingRectangle(
            highlight_equation[3], 
            color="#00FF00",  # Pure green hex code
            stroke_width=5.6,
            buff=0.1
        )
        
        self.play(ShowCreation(m_highlight))
        self.wait(1)
        
        # Show how slope affects the line by changing angle
        # Store original line
        original_line = line.copy()
        
        # Create steeper line (1/5 smaller range)
        steep_line = axes.get_graph(lambda x: 1.2 * x + c_value, color=YELLOW, stroke_width=6, x_range=[0, 15])
        self.play(Transform(line, steep_line))
        self.wait(1)
        
        # Create flatter line (1/5 smaller range)
        flat_line = axes.get_graph(lambda x: 0.2 * x + c_value, color=YELLOW, stroke_width=6, x_range=[0, 15])
        self.play(Transform(line, flat_line))
        self.wait(1)
        
        # Back to original slope
        self.play(Transform(line, original_line))
        self.wait(1)
        m_highlight1 = SurroundingRectangle(
            highlight_equation[-1], 
            color="#00FF00",  # Pure green hex code
            stroke_width=5.6,
            buff=0.1
        )
        self.play(Transform(m_highlight, m_highlight1))
        
        # Show the c term (y-intercept) with brace
        # Find the y-intercept point
        y_intercept_point = axes.coords_to_point(0, c_value)
        origin_point = axes.coords_to_point(0, 0)
        
        # Create brace between origin and y-intercept
        brace = Brace(
            Line(origin_point, y_intercept_point),
            direction=LEFT,
            buff=0.2
        ).shift(LEFT*0.2)
        
        brace_text = brace.get_text("c").scale(1.45).shift(LEFT*0.29)
        
        self.play(ShowCreation(brace))
        self.play(Write(brace_text))
        self.wait(2)
        
        # Fade out all texts and braces except the graph
        fade_out_group = VGroup(equation, m_highlight, brace, brace_text,line )
        self.play(FadeOut(fade_out_group))
        self.wait(2)
        
        # Keep only the axes and line
        self.wait(1)


class VisualRegression(Scene):
    def construct(self):
        self.camera.frame.scale(1.5)

        # Create axes
        axes = Axes(
            x_range=[0, 15],
            y_range=[0, 8],
            axis_config={"color": WHITE, "include_ticks": False, "include_numbers": False, "stroke_width": 4.2},
        )
        self.play(ShowCreation(axes))
        x_label = Text("x").next_to(axes.x_axis, DOWN).shift(RIGHT * 7.6 + DOWN * 0.4).scale(1.6)
        y_label = Text("y").next_to(axes.y_axis, UP).shift(UP * 0.33).scale(1.6)
        self.play(Write(x_label), Write(y_label))
        self.wait(1)

        # Generate points
        np.random.seed(42)
        num_points = 16
        x_coords = np.linspace(1, 14, num_points)
        true_slope = 0.4
        true_intercept = 1.5
        noise = np.random.normal(0, 0.8, num_points)
        y_coords = np.clip(true_slope * x_coords + true_intercept + noise, 0.5, 7.5)

        # Create and show all dots in red
        dots = VGroup(*[
            Dot(point=axes.coords_to_point(xi, yi), radius=0.22).set_color(RED)
            for xi, yi in zip(x_coords, y_coords)
        ])
        self.play(ShowCreation(dots), run_time=2)
        self.wait(1)

        # Split into training/testing and color
        num_train = int(0.7 * num_points)
        all_idx = np.arange(num_points)
        test_idx = np.random.choice(all_idx, num_points - num_train, replace=False)
        train_idx = np.setdiff1d(all_idx, test_idx)

        self.play(*[dots[i].animate.set_color("#00FF00") for i in train_idx], run_time=1.5)
        self.play(*[dots[i].animate.set_color("#3E4FFF") for i in test_idx], run_time=1.5)
        self.wait(1.5)

        # Create legend boxes with matching colors
        training_box = Rectangle(width=3, height=1.5, color="#00FF00", fill_opacity=0.8)
        training_text = Text("Training\n  70%", color=BLACK).scale(0.8)
        training_group = VGroup(training_box, training_text).to_edge(UL).shift(UP * 1.5)
        testing_box = Rectangle(width=3, height=1.5, color="#3E4FFF", fill_opacity=0.8)
        testing_text = Text("Testing\n  30%", color=BLACK).scale(0.8)
        testing_group = VGroup(testing_box, testing_text).next_to(training_group, DOWN, buff=0.5)
        self.play(ShowCreation(training_group))
        self.wait(0.5)
        self.play(ShowCreation(testing_group))
        self.wait(2)

        # Remove test points for now
        self.play(FadeOut(VGroup(*[dots[i] for i in test_idx])), FadeOut(VGroup(training_group, testing_group)), run_time=1.5)
        self.wait(2)

        # Keep only training
        train_x = x_coords[train_idx]
        train_y = y_coords[train_idx]

        # Compute optimal slope and intercept from training data
        x_mean = np.mean(train_x)
        y_mean = np.mean(train_y)
        numerator = np.sum((train_x - x_mean) * (train_y - y_mean))
        denominator = np.sum((train_x - x_mean) ** 2)
        optimal_slope = numerator / denominator
        optimal_intercept = y_mean - optimal_slope * x_mean

        # Trackers for line
        slope_tracker = ValueTracker(0.2)
        intercept_tracker = ValueTracker(2.0)

        # Regression line
        line = always_redraw(lambda: axes.get_graph(
            lambda x: slope_tracker.get_value() * x + intercept_tracker.get_value(),
            x_range=[0, 15], color=YELLOW, stroke_width=6
        ).set_z_index(-1))

        self.play(ShowCreation(line))
        self.wait(1)

        # Add MSE text
        mse_display = always_redraw(lambda: Text(
            f"MSE = {self.calculate_mse(train_x, train_y, slope_tracker.get_value(), intercept_tracker.get_value()):.3f}",
            color=WHITE
        ).scale(1.2).to_edge(UR).shift(UP + LEFT * 4.3))

        # Create error lines one by one
        error_lines = VGroup()
        for xi, yi in zip(train_x, train_y):
            y_pred = slope_tracker.get_value() * xi + intercept_tracker.get_value()
            p_pred = axes.coords_to_point(xi, y_pred)
            p_act = axes.coords_to_point(xi, yi)
            line_seg = Line(p_pred, p_act, color=WHITE, stroke_width=2)
            error_lines.add(line_seg)
            self.play(ShowCreation(line_seg), run_time=0.3)

        self.wait(1)

        # Dynamic squares group using always_redraw
        def squares_group():
            unit_y = axes.coords_to_point(0,1)[1] - axes.coords_to_point(0,0)[1]
            squares = VGroup()
            for xi, yi in zip(train_x, train_y):
                y_pred = slope_tracker.get_value() * xi + intercept_tracker.get_value()
                p_pred = axes.coords_to_point(xi, y_pred)
                p_act = axes.coords_to_point(xi, yi)
                err = abs(yi - y_pred)
                side = err * unit_y

                if yi > y_pred:
                    bl, br, tr, tl = p_pred, p_pred + RIGHT * side, p_act + RIGHT * side, p_act
                else:
                    bl, br, tr, tl = p_act, p_act + RIGHT * side, p_pred + RIGHT * side, p_pred

                square = Polygon(bl, br, tr, tl, color=PURPLE, fill_color=PURPLE, fill_opacity=0.7, stroke_width=2)
                squares.add(square)
            return squares

        self.wait(2)

        self.add(mse_display)

        error_squares = always_redraw(squares_group)

        # Fade out lines and fade in dynamic squares together
        self.play(FadeOut(error_lines), FadeIn(error_squares), run_time=2)
        self.wait(1)

        # Animate slope up
        self.play(slope_tracker.animate.set_value(slope_tracker.get_value() + 0.4), run_time=2)
        # Animate slope down
        self.play(slope_tracker.animate.set_value(slope_tracker.get_value() - 0.3), run_time=2)
        self.wait(1)
        # Animate intercept up
        self.play(intercept_tracker.animate.set_value(intercept_tracker.get_value() + 1.0), run_time=2)
        # Animate intercept down
        self.play(intercept_tracker.animate.set_value(intercept_tracker.get_value() - 1.5), run_time=2)
        self.wait(1)
        # Finally move to optimal slope/intercept
        self.play(
            slope_tracker.animate.set_value(optimal_slope),
            intercept_tracker.animate.set_value(optimal_intercept),
            run_time=3
        )
        self.wait(1)

        # Fade out all squares and MSE
        self.play(FadeOut(error_squares), FadeOut(mse_display), run_time=2)
        self.wait(1)

        # Fade out training points and fade in testing points
        self.play(
            FadeOut(VGroup(*[dots[i] for i in train_idx])),
            FadeIn(VGroup(*[dots[i] for i in test_idx])),
            run_time=2
        )
        self.wait(2)

    def calculate_mse(self, xs, ys, slope, intercept):
        preds = slope * xs + intercept
        return np.mean((ys - preds) ** 2)


class MathRegressionSimple(Scene):
    def construct(self):
        self.camera.frame.scale(1.5)

        # Create axes
        axes = Axes(
            x_range=[0, 15],
            y_range=[0, 8],
            axis_config={"color": WHITE, "include_ticks": False, "include_numbers": False, "stroke_width": 4.2},
        )
        self.play(ShowCreation(axes))
        x_label = Text("x").next_to(axes.x_axis, DOWN).shift(RIGHT * 7.6 + DOWN * 0.4).scale(1.6)
        y_label = Text("y").next_to(axes.y_axis, UP).shift(UP * 0.33).scale(1.6)
        self.play(Write(x_label), Write(y_label))
        self.wait(1)

        # Generate few points
        np.random.seed(42)
        num_points = 5
        x_coords = np.linspace(2, 13, num_points)
        true_slope = 0.4
        true_intercept = 1.5
        noise = np.random.normal(0, 0.6, num_points)
        y_coords = np.clip(true_slope * x_coords + true_intercept + noise, 0.5, 7.5)

        # Create and show all dots in green
        dots = VGroup(*[
            Dot(point=axes.coords_to_point(xi, yi), radius=0.24).set_color("#00FF00")
            for xi, yi in zip(x_coords, y_coords)
        ])
        self.play(ShowCreation(dots), run_time=2)
        self.wait(1)

        # Line
        slope_tracker = ValueTracker(0.1)
        intercept_tracker = ValueTracker(3.6)
        line = axes.get_graph(
            lambda x: slope_tracker.get_value() * x + intercept_tracker.get_value(),
            x_range=[0, 15], color=YELLOW, stroke_width=6
        )
        self.play(ShowCreation(line))
        self.wait(1)

        # Create error lines
        error_lines = VGroup()
        for xi, yi in zip(x_coords, y_coords):
            y_pred = slope_tracker.get_value() * xi + intercept_tracker.get_value()
            p_pred = axes.coords_to_point(xi, y_pred)
            p_actual = axes.coords_to_point(xi, yi)
            line_seg = Line(p_actual, p_pred, color=WHITE, stroke_width=4).set_color(RED)
            error_lines.add(line_seg)

        self.play(LaggedStartMap(ShowCreation, error_lines, lag_ratio=0.1))
        self.wait(1)

        # Create big residual texts with indices
        residual_texts = VGroup()
        for idx, (xi, yi) in enumerate(zip(x_coords, y_coords), start=1):
            y_pred = slope_tracker.get_value() * xi + intercept_tracker.get_value()
            tex = Tex(r"y_{%d} - \hat{y}_{%d}" % (idx, idx)).scale(1.5)
            tex.move_to(axes.coords_to_point(xi, (yi + y_pred)/2)).shift(UP*2)
            residual_texts.add(tex)

        self.play(LaggedStartMap(Write, residual_texts, lag_ratio=0.1))
        self.wait(2)

        # Create one big MSE formula
        mse_tex = Tex(
            r"\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2"
        ).scale(3.0).to_edge(UP).shift(DOWN*2.2)

        title = Text("Loss Function", weight=BOLD).scale(2).to_edge(UP).shift(UP)

        # Transform all residual texts into this final MSE formula
        self.play(
            *[ReplacementTransform(res_tex, mse_tex) for res_tex in residual_texts],
            FadeOut(line),
            FadeOut(error_lines),
            FadeOut(axes),
            FadeOut(dots),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeIn(title),
            run_time=2
        )
        self.wait(3)

        mse = Tex(
            "L(m, c) = \\frac{1}{n} \\sum_{i=1}^{n} (y_i - (mx_i + c))^2"
        )        .scale(2.6).move_to(mse_tex)

        self.play(ReplacementTransform(mse_tex, mse))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*3.88))

        # Create Tex for each variable definition
        x_def = Tex(r"x_{i}: Input\ variable\ (feature)")
        y_def = Tex(r"y_{i}: True\ output\ (target)")
        m_def = Tex(r"m: Slope\ (weight)")
        c_def = Tex(r"c: Intercept\ (bias)")
        n_def = Tex(r"n: Number\ of\ data\ points")

        # Arrange vertically
        defs = VGroup(x_def, y_def, m_def, c_def, n_def)
        defs.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        defs.scale(0.9*1.677).next_to(mse, DOWN, buff=2.1).shift(UP*0.75)

        # Display
        self.play(Write(defs))
        self.wait(3)

        self.play(self.camera.frame.animate.shift(RIGHT*21))

        title = Text("Gradient Descent", weight=BOLD).scale(2).to_edge(UP).shift(RIGHT*21+DOWN*2.3)

        m_eq = Tex(r"m_{i} = m_{i-1} - \alpha \frac{\partial L}{\partial m}").next_to(title, DOWN, buff=0.7).scale(2.6).shift(DOWN*2)
        c_eq = Tex(r"c_{i} = c_{i-1} - \alpha \frac{\partial L}{\partial c}").next_to(m_eq, DOWN, buff=0.7).scale(2.6).shift(DOWN*1.27)

        self.play(ShowCreation(title))

        self.wait(2)

        self.play(
            Write(m_eq),
            Write(c_eq),
            run_time=1
        )

        self.wait(2)

        self.play(
            m_eq[0:2].animate.set_color(YELLOW),
            c_eq[0:2].animate.set_color(YELLOW),
        )

        self.wait(2)

        self.play(
            m_eq[0:2].animate.set_color(WHITE),
            c_eq[0:2].animate.set_color(WHITE),
            m_eq[3:7].animate.set_color(YELLOW),
            c_eq[3:7].animate.set_color(YELLOW),
        )

        self.wait(2)

        self.play(
            m_eq[3:7].animate.set_color(WHITE),
            c_eq[3:7].animate.set_color(WHITE),
            m_eq[8].animate.set_color(YELLOW),
            c_eq[8].animate.set_color(YELLOW),
        )

        self.wait(2)

        self.play(
            m_eq[8].animate.set_color(WHITE),
            c_eq[8].animate.set_color(WHITE),
            m_eq[9:].animate.set_color(YELLOW),
            c_eq[9:].animate.set_color(YELLOW),
        )

        self.wait(2)

        self.play(
            m_eq[8].animate.set_color(WHITE),
            c_eq[8].animate.set_color(WHITE),
            m_eq[9:].animate.set_color(WHITE),
            c_eq[9:].animate.set_color(WHITE),
        )

        self.wait(2)


class LinearRegressionMatrixClean(Scene):
    def construct(self):

        self.camera.frame.scale(0.9)

        # Long explicit equation
        eq1 = Tex(r"y = m_1x_1 + m_2x_2 + \dots + m_nx_n + c").scale(1.2*1.1*1.1)
        self.play(Write(eq1))
        self.wait(1.5)
        self.play(eq1.animate.shift(UP * 2.33))
        self.wait(2)

        # Matrix form
        # Matrix equation

        matrix_eq = Tex(
    r"y = \begin{bmatrix} m_1 \\ m_2 \\ \cdot \\  \cdot \\ m_n \end{bmatrix}^T"
    r"\begin{bmatrix} x_1 \\ x_2 \\ \cdot \\  \cdot \\ x_n \end{bmatrix} + c"
).scale(1.1*1.1).next_to(eq1, DOWN, buff=1)


        self.play(TransformFromCopy(eq1, matrix_eq))
        self.wait(2)


        # Compact matrix equation
        compact_eq = Tex(
            r"y = \mathbf{w}^T \mathbf{x} + c"
        ).scale(1.7).next_to(matrix_eq, DOWN, buff=1)

        self.play(TransformFromCopy(matrix_eq, compact_eq), self.camera.frame.animate.shift(DOWN * 2))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*4.2))

        self.wait(2)

        # Start from single point equation (reusing compact_eq)
        single_pred_eq = Tex(
            r"\hat{y} = \mathbf{w}^T \mathbf{x} + c"
        ).scale(1.5).next_to(compact_eq, DOWN, buff=1)

        self.play(Write(single_pred_eq))
        self.wait(2)


        # Show stacked predictions
        stacked_eq = Tex(
    r"\begin{aligned}"
    r"\hat{y}^{(1)} &= \mathbf{w}^T \mathbf{x}^{(1)} + c \\"
    r"\hat{y}^{(2)} &= \mathbf{w}^T \mathbf{x}^{(2)} + c \\"
    r"&\cdots \\"
    r"\hat{y}^{(n)} &= \mathbf{w}^T \mathbf{x}^{(n)} + c"
    r"\end{aligned}"
).scale(1.1).move_to(single_pred_eq).shift(DOWN*1)
        

        self.play(ReplacementTransform(single_pred_eq, stacked_eq))
        self.wait(3)

        # Show vector form of predictions
        vector_yhat = Tex(
    r"\hat{\mathbf{y}} = X\mathbf{w} + c"
).scale(1.7).move_to(stacked_eq)
        
        self.play(ReplacementTransform(stacked_eq, vector_yhat),self.camera.frame.animate.shift(DOWN*2.77))


        m1 = Tex(
    r"\hat{\mathbf{y}} = \begin{bmatrix} \hat{y}^{(1)} \\ \hat{y}^{(2)} \\ \cdots \\ \hat{y}^{(d)} \end{bmatrix}"
).scale(1.3).next_to(vector_yhat, DOWN, buff=1).shift(LEFT*2.4+DOWN*0.5)

        m2 = Tex(
    r"X = \begin{bmatrix} (\mathbf{x}^{(1)})^T \\ (\mathbf{x}^{(2)})^T \\ \cdots \\ (\mathbf{x}^{(d)})^T \end{bmatrix}"
).scale(1.1).next_to(m1, RIGHT, buff=1)
        
        self.play(FadeIn(m1), FadeIn(m2))


        self.wait(2)

        loss_eq = Tex(
    r"L = \frac{1}{n}\sum_{i=1}^{n}(y^{(i)} - \hat{y}^{(i)})^2"
).scale(1.8).move_to(VGroup(vector_yhat, m1, m2))
        
        self.play(ReplacementTransform(VGroup(vector_yhat,m1,m2), loss_eq),)

        self.wait(2)

        # Vector form loss equation
        loss_vector_eq = Tex(
    r"L = \frac{1}{n}\left\lVert \mathbf{y} - (X\mathbf{w} + c) \right\rVert^2"
).scale(1.6).move_to(loss_eq)

        self.play(ReplacementTransform(loss_eq, loss_vector_eq))
        self.wait(3)



        self.play(self.camera.frame.animate.shift(RIGHT*21))

        title = Text("Gradient Descent", weight=BOLD).scale(1.2).to_edge(UP).shift(RIGHT*21+DOWN*9.5)

        m_eq = Tex(r"w_{new} = w_{old} - \alpha \frac{\partial L}{\partial w}").next_to(title, DOWN, buff=0.7).scale(1.6).shift(DOWN*0.9)
        c_eq = Tex(r"c_{new} = c_{old} - \alpha \frac{\partial L}{\partial c}").next_to(m_eq, DOWN, buff=0.7).scale(1.6).shift(DOWN*0.27)

        self.play(ShowCreation(title))

        self.wait(2)

        self.play(
            Write(m_eq),
            Write(c_eq),
            run_time=1
        )

        self.wait(2)


        rect = SurroundingRectangle(m_eq[:4], color=YELLOW, stroke_width=5).scale(1.2)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(c_eq[:4], color=YELLOW, stroke_width=5).scale(1.2)))

        self.wait(2)

        self.play(Uncreate(rect))

        self.wait(2)

