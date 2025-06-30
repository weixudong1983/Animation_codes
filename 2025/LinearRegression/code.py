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
