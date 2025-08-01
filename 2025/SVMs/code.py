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
