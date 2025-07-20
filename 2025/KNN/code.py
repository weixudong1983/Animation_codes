from manimlib import *
import numpy as np

class KNNVisualizationImproved(Scene):
    def construct(self):
        self.camera.frame.shift(UP*0.23)
        # Define cluster centers with better spacing
        cluster_centers = [
            np.array([-4, 2, 0]),    # Green cluster center
            np.array([3.5, 2, 0]),   # Yellow cluster center
            np.array([0, -2, 0])     # Red cluster center
        ]
        
        cluster_colors = [GREEN, YELLOW, RED]
        all_points = []
        point_colors = []
        
        # Create filled circles with specified color and opacity 1
        def create_filled_dot(position, color):
            dot = Circle(radius=0.2)
            dot.set_fill(color, opacity=1.0)
            dot.set_stroke(color, width=1)
            dot.move_to(position)
            return dot
        
        # Green cluster - 7 dots with more organic, scattered positioning
        green_positions = [
            cluster_centers[0] + np.array([-1.2, 0.5, 0]),
            cluster_centers[0] + np.array([-0.8, 1.0, 0]),
            cluster_centers[0] + np.array([-0.4, -0.4, 0]),
            cluster_centers[0] + np.array([-0.9, -1.0, 0]),
            cluster_centers[0] + np.array([1.0, 0.3, 0]),   # One closer for potential voting
            cluster_centers[0] + np.array([1.3, -0.7, 0]),
            cluster_centers[0] + np.array([-0.5, 1.4, 0])
        ]
        
        # Yellow cluster - 7 dots with asymmetric, natural spread
        yellow_positions = [
            cluster_centers[1] + np.array([1.0, 0.9, 0]),
            cluster_centers[1] + np.array([1.2, -0.5, 0]),
            cluster_centers[1] + np.array([0.0, 0.7, 0]),
            cluster_centers[1] + np.array([-0.6, 0.0, 0]),
            cluster_centers[1] + np.array([-1.2, -0.8, 0]),  # One closer for voting
            cluster_centers[1] + np.array([-1.5, -1.5, 0]),
            cluster_centers[1] + np.array([0.5, -1.3, 0])
        ]
        
        # Red cluster - 7 dots with strategic positioning near test point
        red_positions = [
            cluster_centers[2] + np.array([1.0, 0.8, 0]),   # Close to test point
            cluster_centers[2] + np.array([0.6, 1.3, 0]),   # Close to test point
            cluster_centers[2] + np.array([0.3, 0.5, 0]),   # Close to test point
            cluster_centers[2] + np.array([-1.0, 0.3, 0]),
            cluster_centers[2] + np.array([-1.3, -0.5, 0]),
            cluster_centers[2] + np.array([-0.7, -1.0, 0]),
            cluster_centers[2] + np.array([0.4, -0.9, 0])
        ]
        
        # Create all points with filled circles
        for pos in green_positions:
            dot = create_filled_dot(pos, GREEN)
            all_points.append(dot)
            point_colors.append(GREEN)
        
        for pos in yellow_positions:
            dot = create_filled_dot(pos, YELLOW)
            all_points.append(dot)
            point_colors.append(YELLOW)
        
        for pos in red_positions:
            dot = create_filled_dot(pos, RED)
            all_points.append(dot)
            point_colors.append(RED)
        
        # Create test point with grey fill and full opacity
        test_point = Circle(radius=0.2)
        test_point.set_fill(GREY_C, opacity=1.0)
        test_point.set_stroke(GREY_C, width=1)
        test_point.move_to([-0.87, 1.2, 0])  # Strategic position for desired voting outcome
        
        # Create k=5 label
        k_label = Text("k = 6")
        k_label.to_edge(DOWN,).shift(LEFT*4+UP*1.2).scale(1.6)
        
        # Animate creation of all elements with staggered timing for visual appeal
        self.play(*[ShowCreation(dot) for dot in all_points[:7]], run_time=1.5)  # Green dots
        self.play(*[ShowCreation(dot) for dot in all_points[7:14]], run_time=1.5)  # Yellow dots
        self.play(*[ShowCreation(dot) for dot in all_points[14:21]], run_time=1.5)  # Red dots
        
        self.wait(2)


        self.play(ShowCreation(test_point), Write(k_label), run_time=1)
        self.wait(1)
        
        # Calculate distances and find 5 nearest neighbors
        test_pos = test_point.get_center()
        distances = []
        
        for i, point in enumerate(all_points):
            point_pos = point.get_center()
            distance = np.linalg.norm(test_pos - point_pos)
            distances.append((distance, i, point, point_colors[i]))
        
        # Sort by distance and get 5 nearest neighbors
        distances.sort(key=lambda x: x[0])
        nearest_neighbors = distances[:6]
        
        # Create and animate connection lines to nearest neighbors
        lines = []
        for distance, idx, neighbor, color in nearest_neighbors:
            line = DashedLine(test_pos, neighbor.get_center())
            line.set_color(WHITE)
            line.set_z_index(-1)
            lines.append(line)
            
            # Animate line creation with shorter timing for better flow
            self.play(ShowCreation(line), run_time=0.4)
            self.wait(0.1)
        
        self.wait(2)
        
        # Count votes from the 5 nearest neighbors
        color_votes = {GREEN: 0, YELLOW: 0, RED: 0}
        for distance, idx, neighbor, color in nearest_neighbors:
            color_votes[color] += 1
        
        # Change test point color to RED (maintaining the voting outcome)
        self.play(
            test_point.animate.set_fill(RED, opacity=1.0).set_stroke(RED, width=1), 
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # Remove the connection lines
        self.play(*[FadeOut(line) for line in lines], run_time=1)
        
        # Final pause to show result
        self.wait(2)

from manimlib import *
import numpy as np


class KNNRegression(Scene):
    def construct(self):
        self.camera.frame.scale(0.9)
        # Create axes with x longer than y as requested
        axes = Axes(
            x_range=[-1, 8, 1], 
            y_range=[-1, 5, 1], 
            # Add number labels to axes
            axis_config={
                "numbers_to_exclude": [-1], # Exclude -1 from both axes for cleaner look
            },
        )
        # Add axis labels
        x_label = axes.get_x_axis_label("x").shift(DOWN*0.5).scale(1.6)
        y_label = axes.get_y_axis_label("y").shift(LEFT*1.43).scale(1.6)
        
        axes.add_coordinate_labels(
            font_size=20,
            num_decimal_places=0,
        )

        # Create fewer data points with moderate dispersion
        # Still scattered but not completely random
        data_points_coords = [
            (0.8, 1.4), (1.3, 2.1), (1.7, 1.8), (2.1, 2.6), (2.5, 3.1),
            (3.1, 2.9), (3.6, 3.5), (4.2, 3.2), (4.7, 2.8), (5.1, 3.4),
            (5.6, 2.5), (6.2, 2.1), (1.5, 1.2), (3.4, 4.1), (4.9, 4.0),
            (6.5, 3.0)
        ]
        
        # Create uncolored (gray) dots for all data points
        data_dots = []
        for x_val, y_val in data_points_coords:
            dot = Circle(radius=0.1)
            dot.set_fill(GREY, opacity=1.0)
            dot.set_stroke(GREY, width=1)
            dot.move_to(axes.c2p(x_val, y_val))  # Convert to coordinate system
            data_dots.append(dot)
        
        # Create test point (the point we want to predict for)
        test_x = 4
        test_point = Circle(radius=0.12)
        test_point.set_fill(BLUE, opacity=1.0)
        test_point.set_stroke(BLUE, width=2)
        test_point.move_to(axes.c2p(test_x, 0))  # Place on x-axis initially
        
        # Create k=6 label
        k_label = Text("k = 6")
        k_label.next_to(test_point, UP, buff=0.4)
        
        # Animate creation of axes and points
        self.play(ShowCreation(axes), Write(x_label), Write(y_label), run_time=2)
        self.wait(0.5)
        
        # Animate creation of data points
        self.play(*[ShowCreation(dot) for dot in data_dots], run_time=2)
        self.wait(0.5)
        
        # Add test point and label
        self.play(ShowCreation(test_point),  run_time=1)
        self.wait(1)
        
        # Calculate distances from test point to all data points
        test_pos_2d = (test_x, 0)  # 2D coordinates for distance calculation
        distances = []
        
        for i, (x_val, y_val) in enumerate(data_points_coords):
            distance = np.sqrt((test_x - x_val)**2 + (0 - y_val)**2)
            distances.append((distance, i, x_val, y_val, data_dots[i]))
        
        # Sort by distance and get 6 nearest neighbors
        distances.sort(key=lambda x: x[0])
        nearest_neighbors = distances[:6]
        
        # Create and animate connection lines to nearest neighbors
        lines = []
        neighbor_y_values = []
        
        for distance, idx, x_val, y_val, dot in nearest_neighbors:
            # Create line from test point to neighbor
            line = DashedLine(
                axes.c2p(test_x, 0), 
                axes.c2p(x_val, y_val)
            )
            line.set_color(WHITE)
            line.set_z_index(-1)
            lines.append(line)
            neighbor_y_values.append(y_val)
            
            # Highlight the neighbor dot
            self.play(
                ShowCreation(line),
                dot.animate.set_fill(YELLOW, opacity=1.0).set_stroke(YELLOW, width=2),
                run_time=0.4
            )
            self.wait(0.1)
        
        self.wait(1)
        
        # Calculate the average y-value of the 6 nearest neighbors (regression prediction)
        predicted_y = sum(neighbor_y_values) / len(neighbor_y_values)
        
        # Create prediction point
        prediction_point = Circle(radius=0.12)
        prediction_point.set_fill(RED, opacity=1.0)
        prediction_point.set_stroke(RED, width=2)
        prediction_point.move_to(axes.c2p(test_x, predicted_y))
        
        # Create vertical line from test point to prediction
        prediction_line = Line(
            axes.c2p(test_x, 0),
            axes.c2p(test_x, predicted_y)
        ).set_z_index(-1)

        prediction_line.set_color(RED)
        prediction_line.set_stroke(width=3)
        
        # Show the regression prediction
        prediction_text = Text(f"Predicted y = {predicted_y:.2f}")
        prediction_text.scale(0.9)
        prediction_text.next_to(prediction_point, RIGHT, buff=0.3).shift(DOWN*1.2+RIGHT*0.2)
        
        # Animate the prediction
        self.play(
            ShowCreation(prediction_line),
            ShowCreation(prediction_point),
            run_time=1.5
        )
        

        
        # Remove the connection lines for cleaner final view
        self.play(*[FadeOut(line) for line in lines], run_time=1)
        self.play(Write(prediction_text), run_time=1)
        self.wait(1)

        # Final pause to show the regression result
        self.wait(2)

from manimlib import *
import numpy as np

class KNNRegressionNoAxes(Scene):
    def construct(self):
        self.camera.frame.shift(UP*1.65+RIGHT*2.4)
        
        # First pair of dots and line - Euclidean
        dot1 = Dot(np.array([1, 1, 0]), color=BLUE, radius=0.3).set_color(RED)
        dot2 = Dot(np.array([4, 3, 0]), color=BLUE, radius=0.3).set_color(RED)
        line1 = Line(dot1.get_center(), dot2.get_center(), color=BLUE, stroke_width=8.5).set_color(YELLOW)
        line1.set_z_index(-1)
        
        # Distance type title (BOLD) on top
        euclidean_title = Text(r"Euclidean Distance", weight=BOLD, color=BLUE).to_edge(UP).scale(1.4).shift(UP*1.3+RIGHT*2.3)
        
        # Formula below the dots and lines
        euclidean_formula = Tex(
            r"d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}", 
            color=BLUE
        ).next_to(dot1, DOWN, buff=1.5).shift(RIGHT*1.5).scale(1.2*1.1*1.1)
        
        # Show Euclidean
        self.play(FadeIn(dot1), FadeIn(dot2))
        self.play(ShowCreation(line1))
        self.play(Write(euclidean_title), Write(euclidean_formula))
        self.wait(2)
        
        # Uncreate the Euclidean line
        self.play(Uncreate(line1))
        
        # Create Manhattan distance lines (horizontal then vertical)
        # Horizontal line from dot1 to directly below dot2
        horizontal_line = Line(
            dot1.get_center(), 
            np.array([dot2.get_center()[0], dot1.get_center()[1], 0]), 
            color=YELLOW, 
            stroke_width=8.5
        ).set_z_index(-1)
        
        # Vertical line from end of horizontal line to dot2
        vertical_line = Line(
            np.array([dot2.get_center()[0], dot1.get_center()[1], 0]), 
            dot2.get_center(), 
            color=YELLOW, 
            stroke_width=8.5
        ).set_z_index(-1)
        
        # Manhattan distance title and formula
        manhattan_title = Text(r"Manhattan Distance", weight=BOLD, color=BLUE).to_edge(UP).scale(1.4).shift(UP*1.3+RIGHT*2.3)
        manhattan_formula = Tex(
            r"d = |x_2 - x_1| + |y_2 - y_1|", 
            color=BLUE
        ).next_to(dot1, DOWN, buff=1.5).shift(RIGHT*1.5).scale(1.2*1.1*1.1)
        
        # Transform title and formula to Manhattan
        self.play(
            Transform(euclidean_title, manhattan_title),
            Transform(euclidean_formula, manhattan_formula)
        )
        
        # Show Manhattan distance lines
        self.play(ShowCreation(horizontal_line))
        self.play(ShowCreation(vertical_line))
        self.wait(2)
        
        self.embed()


