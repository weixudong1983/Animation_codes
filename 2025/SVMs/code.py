from manimlib import *
import numpy as np
from sklearn.svm import SVC

class SVM_Hard_Margin(Scene):
    def construct(self):
        # Create axes for first quadrant only
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            height=6,
            width=8,
            axis_config={
                "stroke_width": 4,
                "include_ticks": False,
                "include_numbers": False,
                "include_tip": True,
            }
        )
        
        self.add(axes)
        
        blue_points = np.array([
            [1.5, 4.2], [2.2, 4.9], [2.0, 3.4], [2.8, 4.0],
            [1.0, 3.8], [3.3, 4.6], [1.7, 3.1], [2.6, 4.5],
            [2.4, 4.1], [2.9, 3.3], [1.3, 4.5], [3.1, 3.7]
        ])
        
        green_points = np.array([
            [5.0, 1.8], [5.8, 2.3], [5.3, 1.2], [6.1, 2.0],
            [4.4, 1.4], [5.7, 2.6], [5.0, 0.9], [6.3, 1.5],
            [4.9, 2.0], [5.4, 2.5], [6.0, 1.1], [4.6, 2.8]
        ])
        
        # Combine data for SVM
        X = np.vstack([blue_points, green_points])
        y = np.array([0] * len(blue_points) + [1] * len(green_points))
        
        # Bigger dots
        blue_dots = VGroup()
        for coord in blue_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(BLUE)
            blue_dots.add(dot)
        
        green_dots = VGroup()
        for coord in green_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(GREEN)
            green_dots.add(dot)
        
        self.play(ShowCreation(blue_dots))
        self.play(ShowCreation(green_dots))
        self.wait(1)
        
        # Train SVM to find decision boundary
        svm = SVC(kernel='linear', C=1.0)
        svm.fit(X, y)
        
        # Decision boundary: w1*x + w2*y + b = 0 → y = (-w1*x - b)/w2
        w = svm.coef_[0]
        b = svm.intercept_[0]
        
        # ✂️ Reduced x range to make lines/rectangle much smaller
        x_start, x_end = 2.5, 4.9  # Changed from 2.0, 6.0 to make it smaller
        y_start = (-w[0] * x_start - b) / w[1] 
        y_end = (-w[0] * x_end - b) / w[1]
        
        decision_line = Line(
            axes.coords_to_point(x_start, y_start),
            axes.coords_to_point(x_end, y_end),
            color=RED,
            stroke_width=7
        )

        a = decision_line.copy().shift(DOWN*0.2+RIGHT*0.2).rotate(PI/20)
        self.play(GrowFromCenter(a))
        self.wait()

        self.play(a.animate.rotate(PI/20))
        self.play(a.animate.rotate(PI/20))
        self.play(a.animate.rotate(-PI/10))
        self.play(a.animate.rotate(-PI/5.4))
        self.wait(2)


        # Margin distance (1 / ||w||)
        margin_distance = 1.0 / np.linalg.norm(w)
        
        # Perpendicular vector for margins
        line_vector = np.array([x_end - x_start, y_end - y_start])
        line_length = np.linalg.norm(line_vector)
        perpendicular = np.array([-line_vector[1], line_vector[0]]) / line_length
        
        # Upper margin (towards blue)
        upper_start_x = x_start + perpendicular[0] * margin_distance
        upper_start_y = y_start + perpendicular[1] * margin_distance
        upper_end_x = x_end + perpendicular[0] * margin_distance
        upper_end_y = y_end + perpendicular[1] * margin_distance
        
        upper_margin_line = DashedLine(
            axes.coords_to_point(upper_start_x, upper_start_y),
            axes.coords_to_point(upper_end_x, upper_end_y),
            color=BLUE,
            stroke_width=5,
            stroke_opacity=0.8,
            dash_length=0.1
        )
        
        # Lower margin (towards green)
        lower_start_x = x_start - perpendicular[0] * margin_distance
        lower_start_y = y_start - perpendicular[1] * margin_distance
        lower_end_x = x_end - perpendicular[0] * margin_distance
        lower_end_y = y_end - perpendicular[1] * margin_distance
        
        lower_margin_line = DashedLine(
            axes.coords_to_point(lower_start_x, lower_start_y),
            axes.coords_to_point(lower_end_x, lower_end_y),
            color=GREEN,
            stroke_width=5,
            stroke_opacity=0.8,
            dash_length=0.1
        )
        
        # Fill area between margins
        margin_fill = Polygon(
            axes.coords_to_point(upper_start_x, upper_start_y),
            axes.coords_to_point(upper_end_x, upper_end_y),
            axes.coords_to_point(lower_end_x, lower_end_y),
            axes.coords_to_point(lower_start_x, lower_start_y),
            fill_opacity=0.2,
            fill_color=YELLOW,
            stroke_width=0
        )
        margin_fill.set_z_index(-1)
        
        # Support vectors
        support_vector_indices = svm.support_
        support_vectors_coords = X[support_vector_indices]
        
        support_vector_dots = VGroup()
        for i, coord in enumerate(support_vectors_coords):
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.15)
            if y[support_vector_indices[i]] == 0:
                dot.set_color(BLUE)
            else:
                dot.set_color(GREEN)
            dot.set_stroke(WHITE, width=4)
            support_vector_dots.add(dot)
        
        # Animate
        self.play(ReplacementTransform(a, decision_line))
        self.wait(1)
        self.play(ShowCreation(margin_fill))
        self.wait(0.5)
        self.play(ShowCreation(upper_margin_line), ShowCreation(lower_margin_line))
        self.wait(2)


        # Position margin indicator at the very end of decision boundary
        margin_x = x_end - 0.2  # Slightly before the absolute end for better visibility
        margin_y = (-w[0] * margin_x - b) / w[1]

        upper_margin_x = margin_x + perpendicular[0] * margin_distance
        upper_margin_y = margin_y + perpendicular[1] * margin_distance
        lower_margin_x = margin_x - perpendicular[0] * margin_distance  
        lower_margin_y = margin_y - perpendicular[1] * margin_distance

        # Create the margin measurement line at the end
        margin_line = Line(
            axes.coords_to_point(upper_margin_x, upper_margin_y),
            axes.coords_to_point(lower_margin_x, lower_margin_y),
            color=ORANGE,
            stroke_width=4
        )

        # Create simple triangular tips manually
        tip_size = 0.25
        line_direction = margin_line.get_unit_vector()
        perpendicular_to_line = np.array([-line_direction[1], line_direction[0], 0])

        # Tip at start (upper margin)
        tip1 = Polygon(
            margin_line.get_start(),
            margin_line.get_start() + tip_size * line_direction + tip_size * 0.5 * perpendicular_to_line,
            margin_line.get_start() + tip_size * line_direction - tip_size * 0.5 * perpendicular_to_line,
            color=ORANGE,
            fill_opacity=1
        )

        # Tip at end (lower margin)
        tip2 = Polygon(
            margin_line.get_end(),
            margin_line.get_end() - tip_size * line_direction + tip_size * 0.5 * perpendicular_to_line,
            margin_line.get_end() - tip_size * line_direction - tip_size * 0.5 * perpendicular_to_line,
            color=ORANGE,
            fill_opacity=1
        )

        margin_indicator = VGroup(margin_line, tip1, tip2).shift(RIGHT*0.35 + UP*0.65)

        margin_text = Text("Margin", font_size=60, color=ORANGE).set_color(ORANGE)
        margin_text.next_to(margin_line, RIGHT if perpendicular[0] > 0 else RIGHT, buff=0.5).shift(RIGHT*2)

        self.play(ShowCreation(margin_indicator))
        self.wait()
        self.play(Write(margin_text), self.camera.frame.animate.shift(RIGHT*1.3))
        self.wait(2)


        self.play(ShowCreation(support_vector_dots))
        text = Text("Support Vectors").next_to(margin_text, DOWN, buff=0.5)
        self.play(ShowCreation(text))
        self.wait(2)

        text1 = Text("Hard Margin", weight=BOLD).next_to(text, DOWN).scale(1.6).shift(DOWN*0.7)
        self.play(ShowCreation(text1))
        self.wait(2)

class SVM_Soft_Margin(Scene):
    def construct(self):
        # Create axes for first quadrant only
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            height=6,
            width=8,
            axis_config={
                "stroke_width": 4,
                "include_ticks": False,
                "include_numbers": False,
                "include_tip": True,
            }
        )
        
        self.add(axes)
        
        # Modified data points to create overlapping regions for soft margin
        blue_points = np.array([
            [1.5, 4.2], [2.2, 4.9], [2.0, 3.4], [2.8, 4.0],
            [1.0, 3.8], [3.3, 4.6], [1.7, 3.1], [2.6, 4.5],
            [2.4, 4.1], [2.9, 3.3], [1.3, 4.5], [3.1, 3.7],
            [4.2, 3.8], [4.0, 2.5]  # Added points that create overlap
        ])
        
        green_points = np.array([
            [5.0, 1.8], [5.8, 2.3], [5.3, 1.2], [6.1, 2.0],
            [4.4, 1.4], [5.7, 2.6], [5.0, 0.9], [6.3, 1.5],
            [4.9, 2.0], [5.4, 2.5], [6.0, 1.1], [4.6, 2.8],
            [3.2, 2.8], [3.8, 3.5]  # Added points that create overlap
        ])
        
        # Combine data for SVM
        X = np.vstack([blue_points, green_points])
        y = np.array([0] * len(blue_points) + [1] * len(green_points))
        
        # Bigger dots
        blue_dots = VGroup()
        for coord in blue_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(BLUE)
            blue_dots.add(dot)
        
        green_dots = VGroup()
        for coord in green_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(GREEN)
            green_dots.add(dot)
        
        self.play(ShowCreation(blue_dots))
        self.play(ShowCreation(green_dots))
        self.wait(1)
        
        # Train SVM with soft margin (smaller C value allows more violations)
        svm = SVC(kernel='linear', C=0.3)  # Changed from C=1.0 to C=0.3 for softer margin
        svm.fit(X, y)
        
        # Decision boundary: w1*x + w2*y + b = 0 → y = (-w1*x - b)/w2
        w = svm.coef_[0]
        b = svm.intercept_[0]
        
        # Adjusted x range - a little higher x on left side
        x_start, x_end = 1.4, 5.8  # Changed from 1.2, 5.8 to move left side higher
        y_start = (-w[0] * x_start - b) / w[1] 
        y_end = (-w[0] * x_end - b) / w[1]
        
        decision_line = Line(
            axes.coords_to_point(x_start, y_start),
            axes.coords_to_point(x_end, y_end),
            color=RED,
            stroke_width=7
        )

        a = decision_line.copy().shift(DOWN*0.2+RIGHT*0.2).rotate(PI/20)
        self.play(GrowFromCenter(a))
        self.wait()

        self.play(a.animate.rotate(PI/20))
        self.play(a.animate.rotate(PI/20))
        self.play(a.animate.rotate(-PI/10))
        self.play(a.animate.rotate(-PI/5.4))
        self.wait(2)

        # Margin distance (1 / ||w||)
        margin_distance = 1.0 / np.linalg.norm(w)
        
        # Perpendicular vector for margins
        line_vector = np.array([x_end - x_start, y_end - y_start])
        line_length = np.linalg.norm(line_vector)
        perpendicular = np.array([-line_vector[1], line_vector[0]]) / line_length
        
        # Upper margin (towards blue)
        upper_start_x = x_start + perpendicular[0] * margin_distance
        upper_start_y = y_start + perpendicular[1] * margin_distance
        upper_end_x = x_end + perpendicular[0] * margin_distance
        upper_end_y = y_end + perpendicular[1] * margin_distance
        
        upper_margin_line = DashedLine(
            axes.coords_to_point(upper_start_x, upper_start_y),
            axes.coords_to_point(upper_end_x, upper_end_y),
            color=BLUE,
            stroke_width=5,
            stroke_opacity=0.6,  # Reduced opacity for soft margin
            dash_length=0.1
        )
        
        # Lower margin (towards green)
        lower_start_x = x_start - perpendicular[0] * margin_distance
        lower_start_y = y_start - perpendicular[1] * margin_distance
        lower_end_x = x_end - perpendicular[0] * margin_distance
        lower_end_y = y_end - perpendicular[1] * margin_distance
        
        lower_margin_line = DashedLine(
            axes.coords_to_point(lower_start_x, lower_start_y),
            axes.coords_to_point(lower_end_x, lower_end_y),
            color=GREEN,
            stroke_width=5,
            stroke_opacity=0.6,  # Reduced opacity for soft margin
            dash_length=0.1
        )
        
        # Fill area between margins with reduced opacity for soft margin
        margin_fill = Polygon(
            axes.coords_to_point(upper_start_x, upper_start_y),
            axes.coords_to_point(upper_end_x, upper_end_y),
            axes.coords_to_point(lower_end_x, lower_end_y),
            axes.coords_to_point(lower_start_x, lower_start_y),
            fill_opacity=0.15,  # Reduced opacity for soft margin
            fill_color=YELLOW,
            stroke_width=0
        )
        margin_fill.set_z_index(-1)
        
        # Support vectors
        support_vector_indices = svm.support_
        support_vectors_coords = X[support_vector_indices]
        
        support_vector_dots = VGroup()
        for i, coord in enumerate(support_vectors_coords):
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.15)
            if y[support_vector_indices[i]] == 0:
                dot.set_color(BLUE)
            else:
                dot.set_color(GREEN)
            dot.set_stroke(WHITE, width=4)
            support_vector_dots.add(dot)
        
        # Animate
        self.play(ReplacementTransform(a, decision_line))
        self.wait(1)
        self.play(ShowCreation(margin_fill))
        self.wait(0.5)
        self.play(ShowCreation(upper_margin_line), ShowCreation(lower_margin_line))
        self.wait(2)

        # Position margin indicator at the very end of decision boundary
        margin_x = x_end - 0.2  # Slightly before the absolute end for better visibility
        margin_y = (-w[0] * margin_x - b) / w[1]

        upper_margin_x = margin_x + perpendicular[0] * margin_distance
        upper_margin_y = margin_y + perpendicular[1] * margin_distance
        lower_margin_x = margin_x - perpendicular[0] * margin_distance  
        lower_margin_y = margin_y - perpendicular[1] * margin_distance

        # Create the margin measurement line at the end
        margin_line = Line(
            axes.coords_to_point(upper_margin_x, upper_margin_y),
            axes.coords_to_point(lower_margin_x, lower_margin_y),
            color=ORANGE,
            stroke_width=4
        )

        # Create simple triangular tips manually
        tip_size = 0.25
        line_direction = margin_line.get_unit_vector()
        perpendicular_to_line = np.array([-line_direction[1], line_direction[0], 0])

        # Tip at start (upper margin)
        tip1 = Polygon(
            margin_line.get_start(),
            margin_line.get_start() + tip_size * line_direction + tip_size * 0.5 * perpendicular_to_line,
            margin_line.get_start() + tip_size * line_direction - tip_size * 0.5 * perpendicular_to_line,
            color=ORANGE,
            fill_opacity=1
        )

        # Tip at end (lower margin)
        tip2 = Polygon(
            margin_line.get_end(),
            margin_line.get_end() - tip_size * line_direction + tip_size * 0.5 * perpendicular_to_line,
            margin_line.get_end() - tip_size * line_direction - tip_size * 0.5 * perpendicular_to_line,
            color=ORANGE,
            fill_opacity=1
        )

        margin_indicator = VGroup(margin_line, tip1, tip2).shift(RIGHT*0.35 + UP*0.4).scale(1.0)

        margin_text = Text("Margin", font_size=60, color=ORANGE).set_color(ORANGE)
        margin_text.next_to(margin_line, RIGHT if perpendicular[0] > 0 else RIGHT, buff=0.5).shift(RIGHT*1.2)

        self.play(ShowCreation(margin_indicator))
        self.wait()
        self.play(Write(margin_text), self.camera.frame.animate.shift(RIGHT*1.5).scale(1.05))
        self.wait(2)


        self.play(ShowCreation(support_vector_dots))
        text = Text("Support Vectors").next_to(margin_text, DOWN, buff=0.7)
        self.play(ShowCreation(text))
        self.wait(2)


        # Highlight margin violations (points that fall within the margin) - RED CIRCLES ADDED BACK
        violation_dots = VGroup()
        
        # First, find the green point furthest from decision boundary (but still violating) to exclude it
        green_violations = []
        for i, point in enumerate(X):
            if y[i] == 1:  # Green points only
                distance = abs(w[0] * point[0] + w[1] * point[1] + b) / np.linalg.norm(w)
                if distance < margin_distance:
                    green_violations.append((i, distance))
        
        # Find the green point furthest from decision boundary (largest distance among violations)
        furthest_green_violation = None
        if green_violations:
            furthest_green_violation = max(green_violations, key=lambda x: x[1])[0]
        
        for i, point in enumerate(X):
            # Calculate distance from point to decision boundary
            distance = abs(w[0] * point[0] + w[1] * point[1] + b) / np.linalg.norm(w)
            if distance < margin_distance:  # Point violates margin
                # Skip the green point furthest from decision boundary to make it look like hard support vector
                if i == furthest_green_violation:
                    continue
                    
                dot = Circle(radius=0.25, color=RED, stroke_width=3, fill_opacity=0)
                dot.move_to(axes.coords_to_point(point[0], point[1]))
                violation_dots.add(dot)
        
        if len(violation_dots) > 0:
            self.play(ShowCreation(violation_dots))
            violation_text = Text("Margin Violations", font_size=48, color=RED).set_color(RED)
            violation_text.next_to(text, DOWN, buff=0.3)
            self.play(Write(violation_text))
            self.wait(2)
        
        # Final text for Soft Margin
        text1 = Text("Soft Margin", weight=BOLD).next_to(text, DOWN).scale(1.6).shift(DOWN*0.7)
        if len(violation_dots) > 0:
            text1.next_to(violation_text, DOWN)
        self.play(ShowCreation(text1))
        self.wait(2)



class SVM_Hard_MarginMath(Scene):
    def construct(self):
        # Create axes for first quadrant only
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            height=6,
            width=8,
            axis_config={
                "stroke_width": 4,
                "include_ticks": False,
                "include_numbers": False,
                "include_tip": True,
            }
        )
        
        blue_points = np.array([
            [1.5, 4.2], [2.2, 4.9], [2.0, 3.4], [2.8, 4.0],
            [1.0, 3.8], [3.3, 4.6], [1.7, 3.1], [2.6, 4.5],
            [2.4, 4.1], [2.9, 3.3], [1.3, 4.5], [3.1, 3.7]
        ])
        
        green_points = np.array([
            [5.0, 1.8], [5.8, 2.3], [5.3, 1.2], [6.1, 2.0],
            [4.4, 1.4], [5.7, 2.6], [5.0, 0.9], [6.3, 1.5],
            [4.9, 2.0], [5.4, 2.5], [6.0, 1.1], [4.6, 2.8]
        ])
        
        # Combine data for SVM
        X = np.vstack([blue_points, green_points])
        y = np.array([0] * len(blue_points) + [1] * len(green_points))
        
        # Create dots
        blue_dots = VGroup()
        for coord in blue_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(BLUE)
            blue_dots.add(dot)
        
        green_dots = VGroup()
        for coord in green_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(GREEN)
            green_dots.add(dot)
        
        # Train SVM to find decision boundary
        svm = SVC(kernel='linear', C=1.0)
        svm.fit(X, y)
        
        # Decision boundary: w1*x + w2*y + b = 0 → y = (-w1*x - b)/w2
        w = svm.coef_[0]
        b = svm.intercept_[0]
        
        x_start, x_end = 2.5, 4.9
        y_start = (-w[0] * x_start - b) / w[1] 
        y_end = (-w[0] * x_end - b) / w[1]
        
        decision_line = Line(
            axes.coords_to_point(x_start, y_start),
            axes.coords_to_point(x_end, y_end),
            color=RED,
            stroke_width=7
        )
        
        # Margin distance (1 / ||w||)
        margin_distance = 1.0 / np.linalg.norm(w)
        
        # Perpendicular vector for margins
        line_vector = np.array([x_end - x_start, y_end - y_start])
        line_length = np.linalg.norm(line_vector)
        perpendicular = np.array([-line_vector[1], line_vector[0]]) / line_length
        
        # Upper margin (towards blue)
        upper_start_x = x_start + perpendicular[0] * margin_distance
        upper_start_y = y_start + perpendicular[1] * margin_distance
        upper_end_x = x_end + perpendicular[0] * margin_distance
        upper_end_y = y_end + perpendicular[1] * margin_distance
        
        upper_margin_line = DashedLine(
            axes.coords_to_point(upper_start_x, upper_start_y),
            axes.coords_to_point(upper_end_x, upper_end_y),
            color=BLUE,
            stroke_width=5,
            stroke_opacity=0.8,
            dash_length=0.1
        )
        
        # Lower margin (towards green)
        lower_start_x = x_start - perpendicular[0] * margin_distance
        lower_start_y = y_start - perpendicular[1] * margin_distance
        lower_end_x = x_end - perpendicular[0] * margin_distance
        lower_end_y = y_end - perpendicular[1] * margin_distance
        
        lower_margin_line = DashedLine(
            axes.coords_to_point(lower_start_x, lower_start_y),
            axes.coords_to_point(lower_end_x, lower_end_y),
            color=GREEN,
            stroke_width=5,
            stroke_opacity=0.8,
            dash_length=0.1
        )
        
        # Add everything at once - no animations
        self.add(axes, blue_dots, green_dots, decision_line, upper_margin_line, lower_margin_line)
        self.wait(2)
        
        # Create equations
        # Decision boundary equation
        decision_eq = Tex(r"\mathbf{w}^T\mathbf{x} + b = 0", font_size=58, color=RED).set_color(RED)
        decision_eq.to_edge(UP + RIGHT, buff=1)
        
        # Upper margin equation  
        upper_eq = Tex(r"\mathbf{w}^T\mathbf{x} + b = +1", font_size=58, color=BLUE).set_color(BLUE)
        upper_eq.next_to(decision_eq, DOWN, buff=0.5)
        
        # Lower margin equation
        lower_eq = Tex(r"\mathbf{w}^T\mathbf{x} + b = -1", font_size=58, color=GREEN).set_color(GREEN)
        lower_eq.next_to(upper_eq, DOWN, buff=0.5)
        
        # Animate equations
        self.play(Write(decision_eq), self.camera.frame.animate.shift(RIGHT))
        self.wait(1)
        self.play(Write(upper_eq))
        self.wait(1)
        self.play(Write(lower_eq))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*13))

        equation = Tex(r"\mathbf{w}^T\mathbf{x} + b = 0").scale(2).shift(RIGHT*14)
        self.play(ShowCreation(equation))
        self.wait(2)


        # Matrix representation - both as column vectors
        # W transpose matrix (column vector with T superscript)
        w_matrix = Tex(r"\begin{bmatrix} w_1 \\ w_2 \\ w_3 \\ : \\ w_n \end{bmatrix}^T").shift(RIGHT*14).shift(DOWN)
        
        # X matrix (column vector)
        x_matrix = Tex(r"\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ : \\ x_n \end{bmatrix}").shift(DOWN)
        x_matrix.next_to(w_matrix, RIGHT, buff=0.3)
        
        # Plus b = 0 (with space before b)
        plus_b = Tex(r"+ \ b = 0").shift(DOWN)
        plus_b.next_to(x_matrix, RIGHT, buff=0.3)

        temp = VGroup(w_matrix, x_matrix, plus_b).move_to(equation).scale(1.6).shift(RIGHT*0.3)
        
        self.play(Transform(equation, temp))

        self.wait(2)

        self.play(Transform(equation, Tex(r"w_1x_1 + w_2x_2 + w_3x_3 + \cdots + w_nx_n + b = 0").scale(1.3).move_to(equation).shift(LEFT*0.25)))

        self.wait(2)

        self.play(Transform(equation, Tex(r"wx + b = 0").scale(2).move_to(equation)))
        self.wait(2)

        # self.play(self.camera.frame.animate.shift(RIGHT*12.6))

        # Transform back to compact form
        compact_eq = Tex(r"sign(\mathbf{w}^\top \mathbf{x} + b)").scale(2)
        compact_eq.move_to(equation)

        self.play(Transform(equation, compact_eq))
        self.play(equation.animate.shift(UP*1.7))
        
        # Classification conditions
        condition1 = Tex(r"if: \ \mathbf{w}^T\mathbf{x} + b > 0, \ y_{i} \ = \ +1").shift(DOWN)
        condition1.next_to(equation, DOWN, buff=0.9)
        
        condition2 = Tex(r"if: \ \mathbf{w}^T\mathbf{x} + b < 0, \ y_{i} \ = \ -1").shift(DOWN)
        condition2.next_to(condition1, DOWN, buff=0.5)
        

        self.play(ShowCreation(condition1))
        self.wait(2)
        self.play(ShowCreation(condition2))
        self.wait(2)

        
        eq = Tex(r"y_i(w^\top x_i + b) > 0").scale(2).shift(RIGHT*13.9)

        self.play(ReplacementTransform(VGroup(condition1, condition2, equation), eq))

        self.wait(2)

        self.play(Transform(eq, Tex(r"y_i(w^\top x_i + b) \geq 1").scale(2).move_to(eq)))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*13))
        self.play(FadeOut(VGroup(decision_eq, upper_eq, lower_eq)))
        


        # Position margin indicator at the very end of decision boundary
        margin_x = x_end - 0.2  # Slightly before the absolute end for better visibility
        margin_y = (-w[0] * margin_x - b) / w[1]

        upper_margin_x = margin_x + perpendicular[0] * margin_distance
        upper_margin_y = margin_y + perpendicular[1] * margin_distance
        lower_margin_x = margin_x - perpendicular[0] * margin_distance  
        lower_margin_y = margin_y - perpendicular[1] * margin_distance

        # Create the margin measurement line at the end
        margin_line = Line(
            axes.coords_to_point(upper_margin_x, upper_margin_y),
            axes.coords_to_point(lower_margin_x, lower_margin_y),
            color=ORANGE,
            stroke_width=4
        )

        # Create simple triangular tips manually
        tip_size = 0.25
        line_direction = margin_line.get_unit_vector()
        perpendicular_to_line = np.array([-line_direction[1], line_direction[0], 0])

        # Tip at start (upper margin)
        tip1 = Polygon(
            margin_line.get_start(),
            margin_line.get_start() + tip_size * line_direction + tip_size * 0.5 * perpendicular_to_line,
            margin_line.get_start() + tip_size * line_direction - tip_size * 0.5 * perpendicular_to_line,
            color=ORANGE,
            fill_opacity=1
        )

        # Tip at end (lower margin)
        tip2 = Polygon(
            margin_line.get_end(),
            margin_line.get_end() - tip_size * line_direction + tip_size * 0.5 * perpendicular_to_line,
            margin_line.get_end() - tip_size * line_direction - tip_size * 0.5 * perpendicular_to_line,
            color=ORANGE,
            fill_opacity=1
        )

        margin_indicator = VGroup(margin_line, tip1, tip2).shift(RIGHT*0.35 + UP*0.65)


        self.play(ShowCreation(margin_indicator))
        self.wait()
        self.wait(2)

        margin = Tex(r"Margin = \frac{2}{||\mathbf{w}||}").next_to(margin_indicator, RIGHT).shift(DOWN+RIGHT).scale(1.37)
        self.play(ShowCreation(margin))
        self.wait(2)

        arrow = Arrow(margin.get_bottom(), margin.get_bottom()+DOWN, stroke_width=5).set_color(YELLOW).rotate(PI).shift(DOWN*0.14+RIGHT*1.64)
        self.play(ShowCreation(arrow))
        self.wait(2)


        self.play(self.camera.frame.animate.shift(RIGHT*13), eq.animate.shift(DOWN*1.25), )
        cost = Tex(r"\frac{1}{2}||\mathbf{w}||^2").next_to(eq, UP).scale(1.7).shift(UP*1.33)
        self.play(ShowCreation(cost))

        rect = SurroundingRectangle(cost, stroke_width=5).scale(1.14)
        self.play(ShowCreation(rect))

        self.wait(2)

        rect1= SurroundingRectangle(eq, stroke_width=5).scale(1.14).set_color("#00ff00")
        self.play(ShowCreation(rect1))
        self.wait(2)

        self.play(Uncreate(rect), Uncreate(rect1))
        self.wait(2)

        lagrangian = Tex(r"L(w,b,\alpha) = \frac{1}{2}|w|^2 - \sum_{i=1}^{m}\alpha_i[y_i(w^T x_i + b) - 1]").move_to(VGroup(eq, cost)).scale(1.3)

        self.play(ReplacementTransform(VGroup(eq, cost), lagrangian))
        self.wait()
        
        brace = Brace(lagrangian[:8], DOWN, buff=0.35).set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        text = Text("Lagrangian Function").next_to(brace, DOWN).scale(0.7).set_color("#00ff00")
        self.play(Write(text))
        self.wait(2)

        self.play(Transform(brace, Brace(lagrangian[9:16], DOWN, buff=0.35).set_color(YELLOW)), Uncreate(text))
        text = Text("Margin Term").next_to(brace, DOWN).set_color("#00ff00")
        self.play(Write(text))

        self.wait(2)

        self.play(Transform(brace, Brace(lagrangian[18:], DOWN, buff=0.35).set_color(YELLOW)), Uncreate(text))
        text = Text("Constraint penalty term").next_to(brace, DOWN).set_color("#ff0000")
        self.play(Write(text))
        self.wait(2)

        self.play(Uncreate(text), Uncreate(brace))
        self.play(lagrangian.animate.shift(UP*0.8))

        self.play(lagrangian[22:24].animate.set_color(RED))
        self.wait()
        text = Text("Lagrangian Multiplier").next_to(lagrangian, DOWN, buff=0.74).set_color("#00ff00")
        self.play(Write(text))
        self.wait()
        temp = Tex(r"\alpha_i \geq 0").next_to(text, DOWN, buff=0.8).scale(1.25)
        temp[:2].set_color(RED)
        self.play(ShowCreation(temp))
        self.wait(2)

        self.play(lagrangian.animate.shift(UP*1.4), FadeOut(VGroup(temp, text,)), )
        self.play(lagrangian[22:24].animate.set_color(WHITE))
        self.wait(2)

        partial_w_eq = Tex(r"\frac{\partial L}{\partial w} = w - \sum_{i=1}^{m}\alpha_i y_i x_i = 0").next_to(lagrangian, DOWN, buff=0.95).scale(1.3)
        self.play(ShowCreation(partial_w_eq[:5]))
        self.wait(2)
        self.play(ShowCreation(partial_w_eq[5:19]))
        self.wait(2)
        self.play(ShowCreation(partial_w_eq[19:]))
        self.wait(2)

        self.play(Transform(partial_w_eq, Tex(r"w = \sum_{i=1}^{m}\alpha_i y_i x_i").scale(1.3).move_to(partial_w_eq)))
        self.wait(2)
        partial_b_eq = Tex(r"\frac{\partial L}{\partial b} = -\sum_{i=1}^{m}\alpha_i y_i = 0").next_to(partial_w_eq, DOWN, buff=0.95).scale(1.3)
        self.play(ShowCreation(partial_b_eq))
        self.wait(2)
        self.play(Transform(partial_b_eq, Tex(r"\sum_{i=1}^{m}\alpha_i y_i = 0").scale(1.3).move_to(partial_b_eq)))
        self.wait(2)

        rect = SurroundingRectangle(partial_b_eq, color="#00ff00", stroke_width=5).scale(1.08)
        rect1 = SurroundingRectangle(partial_w_eq, color="#00ff00", stroke_width=5).scale(1.08)

        self.play(ShowCreation(rect), ShowCreation(rect1))
        self.wait(2)
        self.play(Uncreate(rect), Uncreate(rect1))
        dual_lagrangian = Tex(r"D(\alpha) = \sum_{i=1}^{m}\alpha_i - \frac{1}{2}\sum_{i=1}^{m}\sum_{j=1}^{m}\alpha_i\alpha_j y_i y_j (x_i \cdot x_j)").move_to(VGroup(partial_b_eq, partial_w_eq, lagrangian)).scale(1.3)

        self.play(ReplacementTransform(VGroup(partial_b_eq, partial_w_eq, lagrangian), dual_lagrangian))
        self.wait(2)

        text = Text("Dual Form").set_color(GREEN).next_to(dual_lagrangian, UP, buff=1).scale(2).shift(UP*0.8)
        self.play(ShowCreation(text))
        self.wait(2)

        brace = Brace(dual_lagrangian[-7:], DOWN, buff=0.7).set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        self.wait()

        text1 = Text("Dot Products").next_to(brace, DOWN, buff=0.5).set_color(BLUE)
        self.play(ShowCreation(text1))
        self.wait(2)

        rect = SurroundingRectangle(dual_lagrangian, stroke_width=6).scale(1.1)

        self.play(Uncreate(brace), Uncreate(text1), ShowCreation(rect))

        self.wait(2)

        self.play(Uncreate(rect), Uncreate(text), dual_lagrangian.animate.shift(UP*2))
        self.wait(2)

        w_optimal = Tex(r"w = \sum_{i=1}^{m}\alpha_i^* y_i x_i").next_to(dual_lagrangian, DOWN, buff=0.6).scale(1.3).shift(DOWN*0.3)
        self.play(ShowCreation(w_optimal))
        self.wait(2)

        b_optimal = Tex(r"b = y_i - w^T x_i").next_to(w_optimal, DOWN, buff=0.6).scale(1.3).shift(DOWN*0.1)
        self.play(ShowCreation(b_optimal))

        self.wait(2)



class SVM_Soft_MarginMath(Scene):
    def construct(self):
        # Create axes for first quadrant only
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            height=6,
            width=8,
            axis_config={
                "stroke_width": 4,
                "include_ticks": False,
                "include_numbers": False,
                "include_tip": True,
            }
        )
        
        blue_points = np.array([
            [1.5, 4.2], [2.2, 4.9], [2.0, 3.4], [2.8, 4.0],
            [1.0, 3.8], [3.3, 4.6], [1.7, 3.1], [2.6, 4.5],
            [2.4, 4.1], [2.9, 3.3], [1.3, 4.5], [3.1, 3.7]
        ])
        
        green_points = np.array([
            [5.0, 1.8], [5.8, 2.3], [5.3, 1.2], [6.1, 2.0],
            [4.4, 1.4], [5.7, 2.6], [5.0, 0.9], [6.3, 1.5],
            [4.9, 2.0], [5.4, 2.5], [6.0, 1.1], [4.6, 2.8]
        ])
        
        # Combine data for SVM
        X = np.vstack([blue_points, green_points])
        y = np.array([0] * len(blue_points) + [1] * len(green_points))
        
        # Create dots
        blue_dots = VGroup()
        for coord in blue_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(BLUE)
            blue_dots.add(dot)
        
        green_dots = VGroup()
        for coord in green_points:
            dot = Dot(axes.coords_to_point(coord[0], coord[1]), radius=0.14)
            dot.set_color(GREEN)
            green_dots.add(dot)
        
        # Train SVM to find decision boundary
        svm = SVC(kernel='linear', C=1.0)
        svm.fit(X, y)
        
        # Decision boundary: w1*x + w2*y + b = 0 → y = (-w1*x - b)/w2
        w = svm.coef_[0]
        b = svm.intercept_[0]
        
        x_start, x_end = 2.5, 4.9
        y_start = (-w[0] * x_start - b) / w[1] 
        y_end = (-w[0] * x_end - b) / w[1]
        
        decision_line = Line(
            axes.coords_to_point(x_start, y_start),
            axes.coords_to_point(x_end, y_end),
            color=RED,
            stroke_width=7
        )
        
        # Margin distance (1 / ||w||)
        margin_distance = 1.0 / np.linalg.norm(w)
        
        # Perpendicular vector for margins
        line_vector = np.array([x_end - x_start, y_end - y_start])
        line_length = np.linalg.norm(line_vector)
        perpendicular = np.array([-line_vector[1], line_vector[0]]) / line_length
        
        # Upper margin (towards blue)
        upper_start_x = x_start + perpendicular[0] * margin_distance
        upper_start_y = y_start + perpendicular[1] * margin_distance
        upper_end_x = x_end + perpendicular[0] * margin_distance
        upper_end_y = y_end + perpendicular[1] * margin_distance
        
        upper_margin_line = DashedLine(
            axes.coords_to_point(upper_start_x, upper_start_y),
            axes.coords_to_point(upper_end_x, upper_end_y),
            color=BLUE,
            stroke_width=5,
            stroke_opacity=0.8,
            dash_length=0.1
        )
        
        # Lower margin (towards green)
        lower_start_x = x_start - perpendicular[0] * margin_distance
        lower_start_y = y_start - perpendicular[1] * margin_distance
        lower_end_x = x_end - perpendicular[0] * margin_distance
        lower_end_y = y_end - perpendicular[1] * margin_distance
        
        lower_margin_line = DashedLine(
            axes.coords_to_point(lower_start_x, lower_start_y),
            axes.coords_to_point(lower_end_x, lower_end_y),
            color=GREEN,
            stroke_width=5,
            stroke_opacity=0.8,
            dash_length=0.1
        )
        
        # Add everything at once - no animations
        self.add(axes, blue_dots, green_dots, decision_line, upper_margin_line, lower_margin_line)
        self.wait(2)
        
        # Create equations
        # Decision boundary equation
        decision_eq = Tex(r"\mathbf{w}^T\mathbf{x} + b = 0", font_size=58, color=RED).set_color(RED)
        decision_eq.to_edge(UP + RIGHT, buff=1)
        
        # Upper margin equation  
        upper_eq = Tex(r"\mathbf{w}^T\mathbf{x} + b = +1", font_size=58, color=BLUE).set_color(BLUE)
        upper_eq.next_to(decision_eq, DOWN, buff=0.5)
        
        # Lower margin equation
        lower_eq = Tex(r"\mathbf{w}^T\mathbf{x} + b = -1", font_size=58, color=GREEN).set_color(GREEN)
        lower_eq.next_to(upper_eq, DOWN, buff=0.5)
        
        # Animate equations
        self.play(Write(decision_eq), self.camera.frame.animate.shift(RIGHT))
        self.wait(1)
        self.play(Write(upper_eq))
        self.wait(1)
        self.play(Write(lower_eq))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*13))

        equation = Tex(r"\mathbf{w}^T\mathbf{x} + b = 0").scale(2).shift(RIGHT*14)
        self.play(ShowCreation(equation))
        self.wait(2)


        # Matrix representation - both as column vectors
        # W transpose matrix (column vector with T superscript)
        w_matrix = Tex(r"\begin{bmatrix} w_1 \\ w_2 \\ w_3 \\ : \\ w_n \end{bmatrix}^T").shift(RIGHT*14).shift(DOWN)
        
        # X matrix (column vector)
        x_matrix = Tex(r"\begin{bmatrix} x_1 \\ x_2 \\ x_3 \\ : \\ x_n \end{bmatrix}").shift(DOWN)
        x_matrix.next_to(w_matrix, RIGHT, buff=0.3)
        
        # Plus b = 0 (with space before b)
        plus_b = Tex(r"+ \ b = 0").shift(DOWN)
        plus_b.next_to(x_matrix, RIGHT, buff=0.3)

        temp = VGroup(w_matrix, x_matrix, plus_b).move_to(equation).scale(1.6).shift(RIGHT*0.3)
        
        self.play(Transform(equation, temp))

        self.wait(2)

        self.play(Transform(equation, Tex(r"w_1x_1 + w_2x_2 + w_3x_3 + \cdots + w_nx_n + b = 0").scale(1.3).move_to(equation).shift(LEFT*0.25)))

        self.wait(2)

        self.play(Transform(equation, Tex(r"wx + b = 0").scale(2).move_to(equation)))
        self.wait(2)

        # self.play(self.camera.frame.animate.shift(RIGHT*12.6))

        # Transform back to compact form
        compact_eq = Tex(r"sign(\mathbf{w}^\top \mathbf{x} + b)").scale(2)
        compact_eq.move_to(equation)

        self.play(Transform(equation, compact_eq))
        self.play(equation.animate.shift(UP*1.7))
        
        # Classification conditions
        condition1 = Tex(r"if: \ \mathbf{w}^T\mathbf{x} + b > 0, \ y_{i} \ = \ +1").shift(DOWN)
        condition1.next_to(equation, DOWN, buff=0.9)
        
        condition2 = Tex(r"if: \ \mathbf{w}^T\mathbf{x} + b < 0, \ y_{i} \ = \ -1").shift(DOWN)
        condition2.next_to(condition1, DOWN, buff=0.5)
        

        self.play(ShowCreation(condition1))
        self.wait(2)
        self.play(ShowCreation(condition2))
        self.wait(2)

        
        eq = Tex(r"y_i(w^\top x_i + b) > 0").scale(2).shift(RIGHT*13.9)

        self.play(ReplacementTransform(VGroup(condition1, condition2, equation), eq))

        self.wait(2)

        self.play(Transform(eq, Tex(r"y_i(w^\top x_i + b) \geq 1").scale(2).move_to(eq)))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*13))
        self.play(FadeOut(VGroup(decision_eq, upper_eq, lower_eq)))
        



        self.play(self.camera.frame.animate.shift(RIGHT*13), eq.animate.shift(DOWN*1.25), )
        cost = Tex(r"\frac{1}{2}||\mathbf{w}||^2").next_to(eq, UP).scale(1.7).shift(UP*1.33)
        self.play(ShowCreation(cost))

        self.wait(2)

        self.play(Transform(cost, Tex(r"\frac{1}{2}||\mathbf{w}||^2 + C\sum_{i=1}^{m}\xi_i").scale(1.7).move_to(cost)))

        self.play(Transform(eq, Tex(r"y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0").scale(1.6).move_to(eq).shift(DOWN*0.15)))

        self.wait(2)

        rect = SurroundingRectangle(eq, stroke_width=5,).scale(1.06)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*3.88))
        self.wait(2)

        conditions = VGroup(Tex(r"\xi_i = 0 \Rightarrow y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 1 \text{ (outside margin)}"),Tex(r"0 < \xi_i < 1 \Rightarrow y_i(\mathbf{w}^T\mathbf{x}_i + b) \geq 0 \text{ (inside margin)}"),Tex(r"\xi_i \geq 1 \Rightarrow y_i(\mathbf{w}^T\mathbf{x}_i + b) < 0 \text{ (misclassified)}")).arrange(DOWN, buff=0.5).next_to(eq, DOWN, buff=0.6)
        conditions.scale(1.4).shift(DOWN*1.1)
        self.play(ShowCreation(conditions))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(conditions[0], stroke_width=5,color="#00ff00").scale(1.06) ))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(conditions[1], stroke_width=5,color="#00ff00").scale(1.06) ))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(conditions[2], stroke_width=5,color="#ff0000").scale(1.06) ))
        self.wait(2)

        self.play(FadeOut(VGroup(conditions, rect)), self.camera.frame.animate.shift(UP*7))
        
        rect = SurroundingRectangle(cost[10:], stroke_width=5,).scale(1.06)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Uncreate(rect), cost[10].animate.set_color(RED))

        case1 = Text("C is large:  strict on misclassification (narrow margin)", font="Arial")
        case2 = Text("C is moderate:  balances margin and classification error", font="Arial")
        case3 = Text("C is small:  allows more violations (wider margin)", font="Arial")

        # Arrange vertically
        conditions = VGroup(case1, case2, case3).arrange(DOWN, buff=0.5).next_to(cost, UP, buff=0.8).shift(UP*0.2)

        self.play(ShowCreation(conditions))

        self.wait(2)

        rect = SurroundingRectangle(conditions[0], stroke_width=5,).scale(1.06) 
        self.play(ShowCreation(rect, ))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(conditions[1], stroke_width=5).scale(1.06) ))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(conditions[2], stroke_width=5,).scale(1.06) ))
        self.wait(2)

        self.play(Uncreate(rect), self.camera.frame.animate.shift(DOWN*3), Uncreate(conditions))
        self.wait(2)

        lagrangian = Tex(r"L(w,b,\xi,\alpha,\mu) = \frac{1}{2}||\mathbf{w}||^2 + C\sum_{i=1}^{m}\xi_i - \sum_{i=1}^{m}\alpha_i[y_i(\mathbf{w}^T\mathbf{x}_i + b) - 1 + \xi_i] - \sum_{i=1}^{m}\mu_i\xi_i").move_to(VGroup(eq,cost)).scale(0.8)
        self.play(ReplacementTransform(VGroup(eq, cost), lagrangian))
        self.wait(2)

        brace = Brace(lagrangian[:12], DOWN, buff=0.66).set_color(YELLOW)
        self.play(ShowCreation(brace))
        
        self.play(self.camera.frame.animate.scale(0.8).shift(LEFT*1.5))
        self.wait(2)
        
        self.play(self.camera.frame.animate.shift(RIGHT*0.5), Transform(brace, Brace(lagrangian[13:30], DOWN, buff=0.66).set_color(YELLOW)))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*1), Transform(brace, Brace(lagrangian[32:56], DOWN, buff=0.66).set_color(YELLOW)))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*2.5).scale(0.8), Transform(brace, Brace(lagrangian[57:], DOWN, buff=0.46).set_color(YELLOW)))
        self.wait()
        temp = Tex(r"\xi_i \geq 0").next_to(brace, DOWN)
        self.play(ShowCreation(temp))

        self.wait(2)

        self.play(FadeOut(VGroup(temp, brace)), self.camera.frame.animate.scale(1.5).shift(LEFT*2.58))
        self.play(lagrangian.animate.shift(UP*2))
        self.wait(2)

        partial_w = Tex(r"\frac{\partial L}{\partial \mathbf{w}} = \mathbf{w} - \sum_{i=1}^{m}\alpha_i y_i \mathbf{x}_i = 0")
        partial_w.next_to(lagrangian, DOWN, buff=0.6)
        self.play(Write(partial_w))

        
        partial_derivatives = VGroup(Tex(r"\frac{\partial L}{\partial \mathbf{w}} = \mathbf{w} - \sum_{i=1}^{m}\alpha_i y_i \mathbf{x}_i = 0"),Tex(r"\frac{\partial L}{\partial b} = -\sum_{i=1}^{m}\alpha_i y_i = 0"),Tex(r"\frac{\partial L}{\partial \xi_i} = C - \alpha_i - \mu_i = 0")).arrange(DOWN, buff=0.5).next_to(lagrangian, DOWN, buff=0.6)
        partial_derivatives.scale(0.9)
        self.play(ShowCreation(partial_derivatives))
        self.wait(2)

        self.play(Transform(partial_derivatives, VGroup(Tex(r"\mathbf{w} = \sum_{i=1}^{m}\alpha_i y_i \mathbf{x}_i"),Tex(r"\sum_{i=1}^{m}\alpha_i y_i = 0"),Tex(r"\mu_i = C - \alpha_i")).arrange(DOWN, buff=0.5).scale(0.9).move_to(partial_derivatives)))
        self.wait(2)

        rect = SurroundingRectangle(partial_derivatives, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        dual_formulation = VGroup(Tex(r"D(\alpha) = \sum_{i=1}^{m}\alpha_i - \frac{1}{2}\sum_{i=1}^{m}\sum_{j=1}^{m}\alpha_i\alpha_j y_i y_j (\mathbf{x}_i \cdot \mathbf{x}_j)"),Tex(r"\text{subject to:}"),Tex(r"0 \leq \alpha_i \leq C, \quad \forall i"),Tex(r"\sum_{i=1}^{m}\alpha_i y_i = 0")).arrange(DOWN, buff=0.5)
        dual_formulation.move_to(VGroup(rect, lagrangian)).scale(1.1*1.1)

        self.play(Uncreate(rect), ReplacementTransform(VGroup(partial_derivatives, lagrangian), dual_formulation))
        self.wait(2)

        arrow = Arrow(dual_formulation.get_center(), dual_formulation.get_center()+RIGHT*1.8, stroke_width=7).set_color(YELLOW)
        arrow.shift(LEFT*4.2+DOWN*0.3)
        self.play(ShowCreation(arrow))

        self.wait(2)

        solution_formulas = VGroup(Tex(r"w^* = \sum_{i=1}^{m}\alpha_i^* y_i \mathbf{x}_i"),Tex(r"b^* = y_j - (w^*)^T \mathbf{x}_j \quad \text{(any support vector)}")).arrange(DOWN, buff=0.5)

        solution_formulas.scale(2).move_to(dual_formulation)

        self.play(Transform(dual_formulation, solution_formulas))

        self.wait(2)

class OneDToTwoDSeparableBetterScaling(Scene):
    def construct(self):
        # Set up camera
        self.camera.frame.scale(0.9).shift(DOWN*0.3)
        
        # Create horizontal x axis
        axis_x = NumberLine(
            x_range=[-6, 6, 1],
            include_numbers=False,
            stroke_width=4
        ).shift(DOWN*2)
        
        self.add(axis_x)
        
        # GREEN class: BIGGER x values so they move more in transform
        green_points_1d = np.array([-1, -0.5, 0.0, 0.5, 1])
        
        # BLUE class: SMALLER x values so they don't go too high
        blue_points_1d = np.array([-3.5, -2.8, -2.2, 1.8, 2.5, 3.2])
        
        # Create dots
        green_dots = VGroup()
        for point in green_points_1d:
            dot = Dot(axis_x.number_to_point(point), radius=0.15)
            dot.set_color(GREEN)
            green_dots.add(dot)
        
        blue_dots = VGroup()
        for point in blue_points_1d:
            dot = Dot(axis_x.number_to_point(point), radius=0.15)
            dot.set_color(BLUE)
            blue_dots.add(dot)
        
        # Show 1D data
        self.play(ShowCreation(green_dots))
        self.play(ShowCreation(blue_dots))
        self.wait(2)
        
        # RED decision boundary
        decision_x = -1.0
        decision_line_1d = Line(
            start=axis_x.number_to_point(decision_x) + UP*0.8,
            end=axis_x.number_to_point(decision_x) + DOWN*0.8,
            color=RED,
            stroke_width=8
        )
        
        self.play(ShowCreation(decision_line_1d))
        self.wait(1)
        
        # MOVE DECISION LINE LEFT AND RIGHT
        self.play(decision_line_1d.animate.shift(RIGHT*1.5), run_time=2)
        self.wait(0.5)
        self.play(decision_line_1d.animate.shift(LEFT*3), run_time=2) 
        self.wait(0.5)
        self.play(decision_line_1d.animate.shift(RIGHT*4.5), run_time=2)
        self.wait(1)
        
        # Remove failed decision boundary
        self.play(FadeOut(decision_line_1d))
        self.wait(1)

        
        # Create TALLER y-axis at middle of green dots
        green_middle = np.mean(green_points_1d)
        axis_y = NumberLine(
            x_range=[0, 6, 1],  # TALLER RANGE
            include_numbers=False,
            stroke_width=4
        ).rotate(PI/2)
        
        # Position y-axis HIGHER and make it TALLER
        axis_y.move_to(axis_x.number_to_point(green_middle) + UP*3)
        axis_y.set_z_index(-1)
        
        self.play(ShowCreation(axis_y), self.camera.frame.animate.scale(1.2).shift(UP*1.43))
        self.wait(1)
        

        # BIG TEXT for labels
        label_x = Text("x", font_size=60)
        label_x.set_color(WHITE).next_to(axis_x, RIGHT, buff=0.5)
        
        label_phi = Text("φ(x)", font_size=60)
        label_phi.set_color(WHITE).next_to(axis_y, UP, buff=0.5)
        
        self.play(Write(label_x))
        self.play(Write(label_phi))
        self.wait(1)
        
        # BIG formula text
        formula = Text("φ(x) = x²", font_size=50)
        formula.set_color(YELLOW)
        formula.to_edge(UP + RIGHT).shift(LEFT*1)
        
        self.play(Write(formula))
        self.wait(2)

        
        # Transform to 2D with BALANCED scaling
        def transform_to_2d(x_val):
            y_val = x_val**2 * 0.41  # Better scaling factor
            x_pos = axis_x.number_to_point(x_val)
            y_offset = axis_y.number_to_point(y_val) - axis_y.number_to_point(0)
            return x_pos + y_offset
        
        # Animate transformation
        animations = []
        
        for i, dot in enumerate(green_dots):
            new_pos = transform_to_2d(green_points_1d[i])
            animations.append(dot.animate.move_to(new_pos))
        
        for i, dot in enumerate(blue_dots):
            new_pos = transform_to_2d(blue_points_1d[i])
            animations.append(dot.animate.move_to(new_pos))
        
        self.play(*animations, run_time=3)
        self.wait(2)
        
        # Create 2D decision boundary that PROPERLY SEPARATES
        decision_y = 1.0  # Good separation level
        decision_line_2d = Line(
            start=axis_x.number_to_point(-5.5) + (axis_y.number_to_point(decision_y) - axis_y.number_to_point(0)),
            end=axis_x.number_to_point(5.5) + (axis_y.number_to_point(decision_y) - axis_y.number_to_point(0)),
            color=RED,
            stroke_width=8
        )
        
        self.play(ShowCreation(decision_line_2d))
        self.wait(3)


from manimlib import *
import numpy as np
from sklearn.svm import SVC
from sklearn.datasets import make_circles
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class PolyAndRBFKernelDemo(Scene):
    def construct(self):
        self.camera.frame.scale(1.1)
        self.camera.frame.scale(0.9)
        self.camera.frame.shift(UP*0.1+RIGHT*0.33)

        # Coordinate plane
        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            height=6, width=6,
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            }
        ).shift(LEFT * 2.5)

        def train_real_svm(X, y, kernel='poly', **params):
            """Train actual SVM and return model + decision boundary"""
            svm = SVC(kernel=kernel, **params)
            svm.fit(X, y)
            
            h = 0.05
            x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
            y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
            xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                               np.arange(y_min, y_max, h))
            
            Z = svm.decision_function(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)
            return svm, xx, yy, Z

        def create_boundary_from_real_svm(xx, yy, Z, plane, color, level=0):
            """Extract real SVM decision boundary"""
            try:
                fig, ax = plt.subplots(figsize=(6, 6))
                cs = ax.contour(xx, yy, Z, levels=[level])
                
                boundary_curves = []
                # Handle both old and new matplotlib versions
                if hasattr(cs, 'collections'):
                    for collection in cs.collections:
                        for path in collection.get_paths():
                            vertices = path.vertices
                            if len(vertices) > 10:
                                manim_points = []
                                for vertex in vertices:
                                    x, y = vertex[0], vertex[1]
                                    if -3 <= x <= 3 and -3 <= y <= 3:
                                        manim_points.append(plane.coords_to_point(x, y))
                                if len(manim_points) > 5:
                                    curve = VMobject().set_points_smoothly(manim_points)
                                    curve.set_stroke(color, width=8)
                                    boundary_curves.append(curve)
                else:
                    # Newer matplotlib versions
                    for line_collection in cs.allsegs:
                        for line in line_collection:
                            if len(line) > 10:
                                manim_points = []
                                for point in line:
                                    x, y = point[0], point[1]
                                    if -3 <= x <= 3 and -3 <= y <= 3:
                                        manim_points.append(plane.coords_to_point(x, y))
                                if len(manim_points) > 5:
                                    curve = VMobject().set_points_smoothly(manim_points)
                                    curve.set_stroke(color, width=8)
                                    boundary_curves.append(curve)
                
                plt.close(fig)
                return boundary_curves
            except:
                return []

        def create_dots_from_data(X, y, plane):
            """Convert data points to manim dots"""
            blue_dots, red_dots = [], []
            for point, label in zip(X, y):
                x, y_coord = point[0], point[1]
                if -3 <= x <= 3 and -3 <= y_coord <= 3:
                    dot = Dot(plane.coords_to_point(x, y_coord), radius=0.09)
                    if label == 1:
                        dot.set_color(BLUE)
                        blue_dots.append(dot)
                    else:
                        dot.set_color(RED)
                        red_dots.append(dot)
            return VGroup(*blue_dots), VGroup(*red_dots)



        self.play(ShowCreation(plane))


        # ==================== POLYNOMIAL KERNEL ====================
        print("Training Polynomial SVM...")
        
        # Generate XOR-like data for polynomial kernel
        np.random.seed(123)
        n_samples = 50
        X_poly = np.random.randn(n_samples, 2)
        y_poly = np.logical_xor(X_poly[:, 0] > 0, X_poly[:, 1] > 0).astype(int)
        y_poly = 2 * y_poly - 1  # Convert to -1,1

        # Initial polynomial SVM training
        svm_poly, xx_poly, yy_poly, Z_poly = train_real_svm(
            X_poly, y_poly, kernel='poly', degree=2, C=1.0, coef0=1
        )

        # Display polynomial formula and info
        poly_formula = Tex(r"K_{poly}(x,y) = (x \cdot y + c)^d", font_size=52).set_color(GREEN)
        poly_formula.to_edge(RIGHT, buff=0.5).shift(UP)

        poly_label = Text("Polynomial Kernel", font_size=42).set_color(GREEN)
        poly_label.next_to(poly_formula, DOWN, buff=0.5)

        poly_params = Tex(r"c = 1, \quad d = 2", font_size=48).set_color(YELLOW)
        poly_params.next_to(poly_label, DOWN, buff=0.5)

        poly_info = Tex(f"\\text{{Support Vectors: }}{len(svm_poly.support_)}", font_size=24).set_color(WHITE)
        poly_info.next_to(poly_params, DOWN, buff=0.3)

        self.play(Write(poly_formula), Write(poly_label), Write(poly_params), )

        # Show polynomial data
        blue_dots, red_dots = create_dots_from_data(X_poly, y_poly, plane)
        self.play(*[GrowFromCenter(dot) for dot in blue_dots], lag_ratio=0.08)
        self.play(*[GrowFromCenter(dot) for dot in red_dots], lag_ratio=0.08)
        self.wait(1)


        # Show initial polynomial boundary
        poly_boundary_curves = create_boundary_from_real_svm(xx_poly, yy_poly, Z_poly, plane, "#00ff00")
        poly_boundary = VGroup(*poly_boundary_curves) if poly_boundary_curves else VGroup()
        if len(poly_boundary) > 0:
            self.play(ShowCreation(poly_boundary), run_time=2)


        self.wait(1.5)



        # Animate parameter changes for polynomial (degree)
        for degree in [3, 4, 5]:
            print(f"Updating Polynomial SVM to degree {degree}...")
            
            new_svm, xx_new, yy_new, Z_new = train_real_svm(
                X_poly, y_poly, kernel='poly', degree=degree, C=1.0, coef0=1
            )
            
            # Create new boundary
            new_curves = create_boundary_from_real_svm(xx_new, yy_new, Z_new, plane, "#00ff00")
            new_boundary = VGroup(*new_curves) if new_curves else VGroup()
            
            # Create new parameter text
            new_params = Tex(f"c = 1, \\quad d = {degree}", font_size=48).set_color(YELLOW)
            new_params.next_to(poly_label, DOWN, buff=0.5)
            

            
            # Use .become() for smooth transitions
            self.play(
                Transform(poly_boundary, new_boundary),
                Transform(poly_params, new_params),
                run_time=0.7
            )
            self.wait(1.2)

        # Clear polynomial scene
        self.play(FadeOut(VGroup(blue_dots, red_dots, poly_boundary,
                                poly_formula, poly_label, poly_params, )))

        # ==================== RBF KERNEL ====================
        print("Training RBF SVM...")
        

        # Generate circular data for RBF kernel
        np.random.seed(456)
        X_rbf, y_rbf = make_circles(n_samples=80, noise=0.12, factor=0.4, random_state=42)
        X_rbf = X_rbf * 2.2  # Scale for visibility
        y_rbf = 2 * y_rbf - 1  # Convert to -1,1

        # Initial RBF SVM training
        svm_rbf, xx_rbf, yy_rbf, Z_rbf = train_real_svm(
            X_rbf, y_rbf, kernel='rbf', gamma=1.0, C=1.0
        )

        # Display RBF formula and info
        rbf_formula = Tex(r"K_{RBF}(x,y) = \exp\left(-\frac{||x - y||^2}{2\sigma^2}\right)", 
                         font_size=40).set_color(GREEN)
        rbf_formula.to_edge(RIGHT, buff=0.5).shift(UP * 1.23)

        rbf_label = Text("RBF (Gaussian) Kernel", font_size=42).set_color(GREEN)
        rbf_label.next_to(rbf_formula, DOWN, buff=0.5)

        rbf_params = Tex(r"\sigma = 1.0", font_size=48).set_color(YELLOW)
        rbf_params.next_to(rbf_label, DOWN, buff=0.5)



        self.play(Write(rbf_formula), Write(rbf_label), Write(rbf_params),)

        # Show RBF data
        blue_dots_rbf, red_dots_rbf = create_dots_from_data(X_rbf, y_rbf, plane)
        self.play(*[GrowFromCenter(dot) for dot in blue_dots_rbf])
        self.play(*[GrowFromCenter(dot) for dot in red_dots_rbf])
        self.wait(1)



        # Show initial RBF boundary
        rbf_boundary_curves = create_boundary_from_real_svm(xx_rbf, yy_rbf, Z_rbf, plane, "#00ff00")
        rbf_boundary = VGroup(*rbf_boundary_curves) if rbf_boundary_curves else VGroup()
        if len(rbf_boundary) > 0:
            self.play(ShowCreation(rbf_boundary), run_time=2)


        self.wait(1.5)

        # Animate sigma parameter changes for RBF
        sigma_values = [0.7, 1.5, 0.5, 2.0]
        
        for sigma in sigma_values:
            print(f"Updating RBF SVM to sigma {sigma}...")
            
            # Convert sigma to gamma (gamma = 1/(2*sigma^2))
            gamma_val = 1.0 / (2 * sigma ** 2)
            
            new_svm, xx_new, yy_new, Z_new = train_real_svm(
                X_rbf, y_rbf, kernel='rbf', gamma=gamma_val, C=1.0
            )
            
            # Create new boundary
            new_curves = create_boundary_from_real_svm(xx_new, yy_new, Z_new, plane, "#00ff00")
            new_boundary = VGroup(*new_curves) if new_curves else VGroup()
            
            # Create new parameter text
            new_params = Tex(f"\\sigma = {sigma:.1f}", font_size=48).set_color(YELLOW)
            new_params.next_to(rbf_label, DOWN, buff=0.5)
            
            # Use .become() for smooth transitions
            self.play(
                rbf_boundary.animate.become(new_boundary),
                rbf_params.animate.become(new_params),
                run_time=0.3
            )
            self.wait(1.2)



        self.wait(2)

        print("Real SVM Training Complete!")
