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

