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
