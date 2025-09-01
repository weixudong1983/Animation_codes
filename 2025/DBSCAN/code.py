from manimlib import *
import numpy as np
from scipy.spatial import ConvexHull

class SimpleAxes(VGroup):
    """
    Minimal first-quadrant axes with a c2p mapper.
    Draws only positive x/y arrows starting at origin.
    """
    def __init__(
        self,
        x_max=10, y_max=7,           
        x_length=8.8, y_length=5.2,  
        origin=ORIGIN + 2.5*DOWN + 4.4*LEFT,
        stroke_width=2,
        tip=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.x_max = float(x_max)
        self.y_max = float(y_max)
        self.x_length = float(x_length)
        self.y_length = float(y_length)
        self.origin = origin
        self.x_unit = self.x_length / self.x_max
        self.y_unit = self.y_length / self.y_max

        # Positive axes only
        x_end = self.origin + np.array([self.x_length, 0, 0])
        y_end = self.origin + np.array([0, self.y_length, 0])
        if tip:
            self.x_axis = Arrow(start=self.origin, end=x_end, buff=0, stroke_width=stroke_width)
            self.y_axis = Arrow(start=self.origin, end=y_end, buff=0, stroke_width=stroke_width)
        else:
            self.x_axis = Line(self.origin, x_end, stroke_width=stroke_width)
            self.y_axis = Line(self.origin, y_end, stroke_width=stroke_width)

        self.add(self.x_axis, self.y_axis)

    def c2p(self, x, y, z=0.0):
        return self.origin + np.array([x * self.x_unit, y * self.y_unit, 0.0])

    def get_x_end(self):
        return self.x_axis.get_end()

    def get_y_end(self):
        return self.y_axis.get_end()

class KMeans(Scene):
    def construct(self):
        self.camera.frame.scale(1.08)
        self.camera.frame.scale(1.05)
        
        # Tunables
        DOT_RADIUS = 0.044
        CENTROID_RADIUS = 0.28
        CENTROID_STROKE = 4
        MAX_ITERS = 10
        TOL = 1e-6

        # Colors - 3 PURE COLORS
        DOT_RED = RED
        DOT_GREEN = GREEN
        DOT_BLUE = BLUE
        PURE_RED = "#FF0000"
        PURE_GREEN = "#00FF00"
        PURE_BLUE = "#0000FF"

        # Z-index layering
        Z_DOTS = 0
        Z_CENTROIDS = 3
        Z_CENTROID_LABELS = 4

        # Helper functions
        def color_for(assign):
            if assign == "red":
                return DOT_RED
            elif assign == "green":
                return DOT_GREEN
            else:
                return DOT_BLUE

        def dist(p, q):
            return np.linalg.norm(p - q)

        def make_X():
            try:
                t = Text("X", weight=BOLD)
            except Exception:
                t = Tex("\\mathbf{X}")
            t.set_stroke(width=1)
            return t

        # Create axes
        axes = SimpleAxes(
            x_max=10, y_max=7,
            x_length=8.8, y_length=5.2,
            origin=ORIGIN + 2.5*DOWN + 4.4*LEFT,
            stroke_width=2, tip=True
        ).set_color(WHITE)
        x_label = Tex("x_{1}")
        y_label = Tex("x_{2}")
        x_label.next_to(axes.get_x_end(), DOWN, buff=0.28)
        y_label.next_to(axes.get_y_end(), LEFT, buff=0.28)

        a = VGroup(axes, x_label, y_label).scale(1.17)
        a.scale(1.2)
        self.play(ShowCreation(a))

        # Create multi-concentric dataset with MANY MORE OUTLIERS
        np.random.seed(42)
        points_coords = []
        
        center_x, center_y = 5.0, 3.5
        
        # Generous boundary conditions
        def in_bounds(x, y):
            return 0.8 <= x <= 9.5 and -0.3 <= y <= 7.3

        # 1. Central cluster (increased noise)
        central_cluster = []
        for i in range(30):
            angle = np.random.uniform(0, 2*np.pi)
            radius = np.random.uniform(0, 0.6)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.075)  # increased from 0.05
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.075)  # increased from 0.05
            if in_bounds(x, y):
                central_cluster.append((x, y))

        # 2. First ring (middle ring) - increased noise
        first_ring = []
        ring1_radius = 2.2
        ring1_thickness = 0.25
        
        # All 5 methods for dense coverage with increased noise
        for i in range(60):
            angle = (2 * np.pi * i) / 60
            radius = ring1_radius + np.random.uniform(-ring1_thickness, ring1_thickness)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)  # increased from 0.02
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)  # increased from 0.02
            if in_bounds(x, y):
                first_ring.append((x, y))
        
        for layer in [-0.15, 0, 0.15]:
            for i in range(40):
                angle = (2 * np.pi * i) / 40 + np.random.uniform(-0.03, 0.03)
                radius = ring1_radius + layer + np.random.uniform(-0.06, 0.06)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                if in_bounds(x, y):
                    first_ring.append((x, y))
        
        for i in range(40):
            angle = (2 * np.pi * i) / 40 + np.pi/40
            radius = ring1_radius + np.random.uniform(-ring1_thickness*0.8, ring1_thickness*0.8)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.038)  # increased from 0.025
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.038)  # increased from 0.025
            if in_bounds(x, y):
                first_ring.append((x, y))
        
        for quadrant in range(4):
            for i in range(15):
                base_angle = quadrant * np.pi/2
                angle = base_angle + (np.pi/2 * i / 15) + np.random.uniform(-0.02, 0.02)
                radius = ring1_radius + np.random.uniform(-ring1_thickness*0.7, ring1_thickness*0.7)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                if in_bounds(x, y):
                    first_ring.append((x, y))
        
        for i in range(50):
            angle = np.random.uniform(0, 2*np.pi)
            radius = ring1_radius + np.random.uniform(-ring1_thickness, ring1_thickness)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.045)  # increased from 0.03
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.045)  # increased from 0.03
            if in_bounds(x, y):
                first_ring.append((x, y))

        # 3. Second ring (outer ring) - increased noise
        second_ring = []
        ring2_radius = 3.6
        ring2_thickness = 0.3
        
        # All 5 methods for dense coverage with increased noise
        for i in range(60):
            angle = (2 * np.pi * i) / 60
            radius = ring2_radius + np.random.uniform(-ring2_thickness/2, ring2_thickness/2)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)  # increased from 0.02
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)  # increased from 0.02
            if in_bounds(x, y):
                second_ring.append((x, y))
        
        for layer_offset in [-0.15, 0, 0.15]:
            for i in range(40):
                angle = (2 * np.pi * i) / 40 + np.random.uniform(-0.03, 0.03)
                radius = ring2_radius + layer_offset + np.random.uniform(-0.06, 0.06)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                if in_bounds(x, y):
                    second_ring.append((x, y))
        
        for i in range(40):
            angle = (2 * np.pi * i) / 40 + np.pi/40
            radius = ring2_radius + np.random.uniform(-ring2_thickness*0.8, ring2_thickness*0.8)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.038)  # increased from 0.025
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.038)  # increased from 0.025
            if in_bounds(x, y):
                second_ring.append((x, y))
        
        for quadrant in range(4):
            for i in range(15):
                base_angle = quadrant * np.pi/2
                angle = base_angle + (np.pi/2 * i / 15) + np.random.uniform(-0.02, 0.02)
                radius = ring2_radius + np.random.uniform(-ring2_thickness*0.7, ring2_thickness*0.7)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)  # increased from 0.02
                if in_bounds(x, y):
                    second_ring.append((x, y))
        
        for i in range(50):
            angle = np.random.uniform(0, 2*np.pi)
            radius = ring2_radius + np.random.uniform(-ring2_thickness, ring2_thickness)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.045)  # increased from 0.03
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.045)  # increased from 0.03
            if in_bounds(x, y):
                second_ring.append((x, y))

        # 4. EXPANDED outlier collection with increased noise
        outliers = []
        
        # Original distant outliers (20 points)
        outlier_regions = [
            (0.8, 1.8, 0.0, 1.0),    # Bottom left corner
            (8.2, 9.5, 0.0, 1.0),    # Bottom right corner  
            (0.8, 1.8, 6.0, 7.3),    # Top left corner
            (8.2, 9.5, 6.0, 7.3),    # Top right corner
            (0.8, 2.0, 2.0, 5.0),    # Left edge
            (8.0, 9.5, 2.0, 5.0),    # Right edge
            (3.0, 7.0, 6.5, 7.3),    # Top edge
            (3.0, 7.0, -0.3, 0.5),   # Bottom edge
        ]
        
        for i in range(20):
            region = outlier_regions[i % len(outlier_regions)]
            x_min, x_max, y_min, y_max = region
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            dist_to_center = np.sqrt((x-center_x)**2 + (y-center_y)**2)
            if dist_to_center > 4.5:
                if in_bounds(x, y):
                    outliers.append((x, y))
        
        # NEW: Outliers INSIDE the rings but away from dense clusters with increased noise
        for i in range(7):
            angle = np.random.uniform(0, 2*np.pi)
            radius_choice = np.random.choice([
                np.random.uniform(0.8, 1.3),   # Between center and inner ring
                np.random.uniform(3.0, 3.3)    # Between inner and outer ring
            ])
            x = center_x + radius_choice * np.cos(angle) + np.random.normal(0, 0.12)  # increased from 0.08
            y = center_y + radius_choice * np.sin(angle) + np.random.normal(0, 0.12)  # increased from 0.08
            if in_bounds(x, y):
                outliers.append((x, y))
        
        # NEW: Additional far-away outliers (6 points)
        extreme_regions = [
            (0.0, 1.0, 0.0, 0.6),     # Very far bottom left
            (9.0, 10.0, 0.0, 7.3),    # Very far right
            (0.0, 10.0, 7.3, 8.0),    # Very far top
            (9.0, 10.0, -1.0, 0.0),   # Very far bottom right
            (0.0, 0.8, -0.3, 7.3),    # Extreme left edge
            (9.5, 10.0, -0.3, 7.3),   # Extreme right edge
        ]
        
        for i in range(6):
            region = extreme_regions[i % len(extreme_regions)]
            x_min, x_max, y_min, y_max = region
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            # Even further requirement
            dist_to_center = np.sqrt((x-center_x)**2 + (y-center_y)**2)
            if dist_to_center > 5.0:  # Even more distant
                outliers.append((x, y))

        # Combine all points
        points_coords = central_cluster + first_ring + second_ring + outliers
        
        points = VGroup(*[
            Dot(axes.c2p(x, y), radius=DOT_RADIUS, color=GREY).set_z_index(Z_DOTS)
            for x, y in points_coords
        ])

        self.play(FadeIn(points, lag_ratio=0.02, run_time=1.0))

        # Initialize 3 CENTROIDS with PURE COLORS and crosses
        red_centroid = Circle(
            radius=CENTROID_RADIUS,
            stroke_color=PURE_RED, fill_color=PURE_RED,
            stroke_width=CENTROID_STROKE, fill_opacity=1.0
        ).move_to(axes.c2p(2.5, 5.2)).set_z_index(Z_CENTROIDS)
        red_X = make_X().move_to(red_centroid.get_center()).set_z_index(Z_CENTROID_LABELS)
        red_centroid = VGroup(red_centroid, red_X).scale(0.75)

        green_centroid = Circle(
            radius=CENTROID_RADIUS,
            stroke_color=PURE_GREEN, fill_color=PURE_GREEN,
            stroke_width=CENTROID_STROKE, fill_opacity=1.0
        ).move_to(axes.c2p(7.5, 1.8)).set_z_index(Z_CENTROIDS)
        green_X = make_X().move_to(green_centroid.get_center()).set_z_index(Z_CENTROID_LABELS)
        green_centroid = VGroup(green_centroid, green_X).scale(0.75)

        blue_centroid = Circle(
            radius=CENTROID_RADIUS,
            stroke_color=PURE_BLUE, fill_color=PURE_BLUE,
            stroke_width=CENTROID_STROKE, fill_opacity=1.0
        ).move_to(axes.c2p(5.0, 3.5)).set_z_index(Z_CENTROIDS)
        blue_X = make_X().move_to(blue_centroid.get_center()).set_z_index(Z_CENTROID_LABELS)
        blue_centroid = VGroup(blue_centroid, blue_X).scale(0.75)

        self.play(
            ShowCreation(red_centroid),
            ShowCreation(green_centroid),
            ShowCreation(blue_centroid)
        )
        self.wait(1)

        # K-means iterations with 3 CLUSTERS
        for iteration in range(MAX_ITERS):
            assignments = []
            for i, (x, y) in enumerate(points_coords):
                p = axes.c2p(x, y)
                r_dist = dist(p, red_centroid.get_center())
                g_dist = dist(p, green_centroid.get_center())
                b_dist = dist(p, blue_centroid.get_center())
                
                min_dist = min(r_dist, g_dist, b_dist)
                if min_dist == r_dist:
                    assignments.append("red")
                elif min_dist == g_dist:
                    assignments.append("green")
                else:
                    assignments.append("blue")

            color_animations = []
            for i, assignment in enumerate(assignments):
                color_animations.append(points[i].animate.set_color(color_for(assignment)))
            
            self.play(*color_animations, run_time=0.66)
            self.wait(0.1)

            # Calculate new centroids
            red_pts = [axes.c2p(*points_coords[i]) for i, a in enumerate(assignments) if a == "red"]
            green_pts = [axes.c2p(*points_coords[i]) for i, a in enumerate(assignments) if a == "green"]
            blue_pts = [axes.c2p(*points_coords[i]) for i, a in enumerate(assignments) if a == "blue"]

            if len(red_pts) > 0:
                red_mean = np.mean(np.vstack(red_pts), axis=0); red_mean[2] = 0
            else:
                red_mean = red_centroid.get_center()
            if len(green_pts) > 0:
                green_mean = np.mean(np.vstack(green_pts), axis=0); green_mean[2] = 0
            else:
                green_mean = green_centroid.get_center()
            if len(blue_pts) > 0:
                blue_mean = np.mean(np.vstack(blue_pts), axis=0); blue_mean[2] = 0
            else:
                blue_mean = blue_centroid.get_center()

            r_old = red_centroid.get_center()
            g_old = green_centroid.get_center()
            b_old = blue_centroid.get_center()
            
            converged = (dist(r_old, red_mean) < TOL and 
                        dist(g_old, green_mean) < TOL and 
                        dist(b_old, blue_mean) < TOL)

            if converged:
                break

            self.play(
                red_centroid.animate.move_to(red_mean),
                red_X.animate.move_to(red_mean),
                green_centroid.animate.move_to(green_mean),
                green_X.animate.move_to(green_mean),
                blue_centroid.animate.move_to(blue_mean),
                blue_X.animate.move_to(blue_mean),
                *[pt.animate.set_color(GREY) for pt in points],
                run_time=0.67
            )
            self.wait(0.1)

        # Final coloring
        final_assignments = []
        for i, (x, y) in enumerate(points_coords):
            p = axes.c2p(x, y)
            r_dist = dist(p, red_centroid.get_center())
            g_dist = dist(p, green_centroid.get_center())
            b_dist = dist(p, blue_centroid.get_center())
            
            min_dist = min(r_dist, g_dist, b_dist)
            if min_dist == r_dist:
                final_assignments.append("red")
            elif min_dist == g_dist:
                final_assignments.append("green")
            else:
                final_assignments.append("blue")

        final_colors = []
        for i, assignment in enumerate(final_assignments):
            final_colors.append(points[i].animate.set_color(color_for(assignment)))

        self.play(*final_colors, run_time=1.0)

        # Remove centroids
        self.play(
            FadeOut(red_centroid), FadeOut(red_X),
            FadeOut(green_centroid), FadeOut(green_X),
            FadeOut(blue_centroid), FadeOut(blue_X),
            run_time=0.8
        )
        self.wait(3)

        arrow = Arrow(start=red_centroid.get_center(), end=green_centroid.get_center()+LEFT*1.8, color=YELLOW, stroke_width=7).set_color(YELLOW)
        arrow.shift(LEFT*3.7+DOWN*0.87)
        self.play(GrowArrow(arrow))
        self.play(arrow.animate.shift(UP*4.7+RIGHT*0.45))
        self.play(arrow.animate.shift(RIGHT*9).flip())
        self.play(arrow.animate.shift(DOWN*4.7+RIGHT*0.45))

        self.wait(2)

        self.play(FadeOut(arrow))

        self.play(*[pt.animate.set_color(GREY_A) for pt in points])

        self.wait(2)



class DBSCAN(Scene):
    def construct(self):
        self.camera.frame.scale(1.08)
        self.camera.frame.scale(1.05)
        
        # Tunables
        DOT_RADIUS = 0.044
        EPSILON = 0.75  # DBSCAN epsilon parameter
        MIN_POINTS = 4  # DBSCAN min_points parameter
        
        # Colors
        CORE_COLOR = BLUE
        BORDER_COLOR = GREEN
        NOISE_COLOR = RED
        CLUSTER_FILL = BLUE
        EPSILON_COLOR = YELLOW
        
        # Z-index layering
        Z_DOTS = 0
        Z_EPSILON_CIRCLE = 1
        Z_CLUSTER_OUTLINE = 2
        
        def dist(p, q):
            return np.linalg.norm(p - q)
        
        def get_neighbors(point_idx, points_coords, epsilon):
            neighbors = []
            point = points_coords[point_idx]
            for i, other_point in enumerate(points_coords):
                if i != point_idx and dist(np.array(point), np.array(other_point)) <= epsilon:
                    neighbors.append(i)
            return neighbors
        
        # Create axes
        axes = SimpleAxes(
            x_max=10, y_max=7,
            x_length=8.8, y_length=5.2,
            origin=ORIGIN + 2.5*DOWN + 4.4*LEFT,
            stroke_width=2, tip=True
        ).set_color(WHITE)
        x_label = Tex("x_{1}")
        y_label = Tex("x_{2}")
        x_label.next_to(axes.get_x_end(), DOWN, buff=0.28)
        y_label.next_to(axes.get_y_end(), LEFT, buff=0.28)

        a = VGroup(axes, x_label, y_label).scale(1.17)
        a.scale(1.2)
        self.play(ShowCreation(a))

        # Create the same multi-concentric dataset
        np.random.seed(42)
        points_coords = []
        
        center_x, center_y = 5.0, 3.5
        
        def in_bounds(x, y):
            return 0.8 <= x <= 9.5 and -0.3 <= y <= 7.3

        # 1. Central cluster (increased noise)
        central_cluster = []
        for i in range(30):
            angle = np.random.uniform(0, 2*np.pi)
            radius = np.random.uniform(0, 0.6)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.075)
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.075)
            if in_bounds(x, y):
                central_cluster.append((x, y))

        # 2. First ring (middle ring) - increased noise
        first_ring = []
        ring1_radius = 2.2
        ring1_thickness = 0.25
        
        for i in range(60):
            angle = (2 * np.pi * i) / 60
            radius = ring1_radius + np.random.uniform(-ring1_thickness, ring1_thickness)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)
            if in_bounds(x, y):
                first_ring.append((x, y))
        
        for layer in [-0.15, 0, 0.15]:
            for i in range(40):
                angle = (2 * np.pi * i) / 40 + np.random.uniform(-0.03, 0.03)
                radius = ring1_radius + layer + np.random.uniform(-0.06, 0.06)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)
                if in_bounds(x, y):
                    first_ring.append((x, y))
        
        for i in range(40):
            angle = (2 * np.pi * i) / 40 + np.pi/40
            radius = ring1_radius + np.random.uniform(-ring1_thickness*0.8, ring1_thickness*0.8)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.038)
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.038)
            if in_bounds(x, y):
                first_ring.append((x, y))
        
        for quadrant in range(4):
            for i in range(15):
                base_angle = quadrant * np.pi/2
                angle = base_angle + (np.pi/2 * i / 15) + np.random.uniform(-0.02, 0.02)
                radius = ring1_radius + np.random.uniform(-ring1_thickness*0.7, ring1_thickness*0.7)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)
                if in_bounds(x, y):
                    first_ring.append((x, y))
        
        for i in range(50):
            angle = np.random.uniform(0, 2*np.pi)
            radius = ring1_radius + np.random.uniform(-ring1_thickness, ring1_thickness)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.045)
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.045)
            if in_bounds(x, y):
                first_ring.append((x, y))

        # 3. Second ring (outer ring) - increased noise
        second_ring = []
        ring2_radius = 3.6
        ring2_thickness = 0.3
        
        for i in range(60):
            angle = (2 * np.pi * i) / 60
            radius = ring2_radius + np.random.uniform(-ring2_thickness/2, ring2_thickness/2)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)
            if in_bounds(x, y):
                second_ring.append((x, y))
        
        for layer_offset in [-0.15, 0, 0.15]:
            for i in range(40):
                angle = (2 * np.pi * i) / 40 + np.random.uniform(-0.03, 0.03)
                radius = ring2_radius + layer_offset + np.random.uniform(-0.06, 0.06)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)
                if in_bounds(x, y):
                    second_ring.append((x, y))
        
        for i in range(40):
            angle = (2 * np.pi * i) / 40 + np.pi/40
            radius = ring2_radius + np.random.uniform(-ring2_thickness*0.8, ring2_thickness*0.8)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.038)
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.038)
            if in_bounds(x, y):
                second_ring.append((x, y))
        
        for quadrant in range(4):
            for i in range(15):
                base_angle = quadrant * np.pi/2
                angle = base_angle + (np.pi/2 * i / 15) + np.random.uniform(-0.02, 0.02)
                radius = ring2_radius + np.random.uniform(-ring2_thickness*0.7, ring2_thickness*0.7)
                x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.03)
                y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.03)
                if in_bounds(x, y):
                    second_ring.append((x, y))
        
        for i in range(50):
            angle = np.random.uniform(0, 2*np.pi)
            radius = ring2_radius + np.random.uniform(-ring2_thickness, ring2_thickness)
            x = center_x + radius * np.cos(angle) + np.random.normal(0, 0.045)
            y = center_y + radius * np.sin(angle) + np.random.normal(0, 0.045)
            if in_bounds(x, y):
                second_ring.append((x, y))

        # 4. EXPANDED outlier collection with increased noise
        outliers = []
        
        outlier_regions = [
            (0.8, 1.8, 0.0, 1.0),    # Bottom left corner
            (8.2, 9.5, 0.0, 1.0),    # Bottom right corner  
            (0.8, 1.8, 6.0, 7.3),    # Top left corner
            (8.2, 9.5, 6.0, 7.3),    # Top right corner
            (0.8, 2.0, 2.0, 5.0),    # Left edge
            (8.0, 9.5, 2.0, 5.0),    # Right edge
            (3.0, 7.0, 6.5, 7.3),    # Top edge
            (3.0, 7.0, -0.3, 0.5),   # Bottom edge
        ]
        
        for i in range(20):
            region = outlier_regions[i % len(outlier_regions)]
            x_min, x_max, y_min, y_max = region
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            dist_to_center = np.sqrt((x-center_x)**2 + (y-center_y)**2)
            if dist_to_center > 4.5:
                if in_bounds(x, y):
                    outliers.append((x, y))
        
        for i in range(7):
            angle = np.random.uniform(0, 2*np.pi)
            radius_choice = np.random.choice([
                np.random.uniform(0.8, 1.3),
                np.random.uniform(3.0, 3.3)
            ])
            x = center_x + radius_choice * np.cos(angle) + np.random.normal(0, 0.12)
            y = center_y + radius_choice * np.sin(angle) + np.random.normal(0, 0.12)
            if in_bounds(x, y):
                outliers.append((x, y))
        
        extreme_regions = [
            (0.0, 1.0, 0.0, 0.6),
            (9.0, 10.0, 0.0, 7.3),
            (0.0, 10.0, 7.3, 8.0),
            (9.0, 10.0, -1.0, 0.0),
            (0.0, 0.8, -0.3, 7.3),
            (9.5, 10.0, -0.3, 7.3),
        ]
        
        for i in range(6):
            region = extreme_regions[i % len(extreme_regions)]
            x_min, x_max, y_min, y_max = region
            x = np.random.uniform(x_min, x_max)
            y = np.random.uniform(y_min, y_max)
            dist_to_center = np.sqrt((x-center_x)**2 + (y-center_y)**2)
            if dist_to_center > 5.0:
                outliers.append((x, y))

        # Combine all points
        points_coords = central_cluster + first_ring + second_ring + outliers
        
        points = VGroup(*[
            Dot(axes.c2p(x, y), radius=DOT_RADIUS, color=GREY).set_z_index(Z_DOTS)
            for x, y in points_coords
        ])

        self.play(FadeIn(points, lag_ratio=0.02, run_time=1.0))

        # ITERATIVE CLUSTERING - MIXED APPROACH
        # Identify cluster indices based on distance from center
        central_indices = []
        ring1_indices = []
        ring2_indices = []
        outlier_indices = []
        
        for i, (x, y) in enumerate(points_coords):
            ring_dist = dist(np.array([x, y]), np.array([center_x, center_y]))
            if ring_dist <= 1.0:
                central_indices.append(i)
            elif 1.5 <= ring_dist <= 2.8:
                ring1_indices.append(i)
            elif 3.0 <= ring_dist <= 4.2:
                ring2_indices.append(i)
            else:
                outlier_indices.append(i)

        # Function to animate each point individually (for central cluster)
        def animate_point_individually(point_index, color):
            circle = Circle(
                radius=EPSILON/3.3, 
                color=BLUE, 
                stroke_width=5
            ).move_to(points[point_index].get_center()).set_z_index(Z_EPSILON_CIRCLE).set_color(BLUE)
            
            self.play(GrowFromCenter(circle), run_time=0.15)
            self.play(points[point_index].animate.set_color(color), run_time=0.05)
            self.play(ShrinkToCenter(circle), run_time=0.15)

        def animate_point_individually1(point_index, color):
            circle = Circle(
                radius=EPSILON/2, 
                color=EPSILON_COLOR, 
                stroke_width=3
            ).move_to(points[point_index].get_center()).set_z_index(Z_EPSILON_CIRCLE).set_color(EPSILON_COLOR)
            
            self.play(GrowFromCenter(circle), run_time=0.15)
            self.play(points[point_index].animate.set_color(color), run_time=0.05)
            self.play(ShrinkToCenter(circle), run_time=0.15)

        # Function to animate ring with moving circle (FAKE IT!)
        def animate_ring_with_moving_circle(indices, color, ring_radius, cluster_name):
            if not indices:
                return
            print(f"Animating {cluster_name} with moving circle...")
            
            # Create a single circle that will move around the ring
            moving_circle = Circle(
                radius=EPSILON/2,
                color=EPSILON_COLOR,
                stroke_width=2
            ).set_z_index(Z_EPSILON_CIRCLE).set_color(EPSILON_COLOR)
            
            # Start position - place circle at ring radius
            start_pos = axes.c2p(center_x + ring_radius, center_y)
            moving_circle.move_to(start_pos)
            
            # Create invisible circular path for the circle to follow
            circular_path = Circle(
                radius=ring_radius * axes.x_unit,  # Convert to screen coordinates
                color=EPSILON_COLOR,
                stroke_width=0  # Invisible
            ).move_to(axes.c2p(center_x, center_y)).set_color(EPSILON_COLOR)
            
            # Show the circle
            self.play(GrowFromCenter(moving_circle), run_time=0.1)
            
            # Move circle around the ring AND color all points simultaneously
            self.play(
                # Move circle in circular path
                MoveAlongPath(moving_circle, circular_path),
                # Color all ring points at the same time
                *[points[i].animate.set_color(color) for i in indices],
                run_time=2,
                rate_func=linear
            )
            
            # Remove the circle
            self.play(ShrinkToCenter(moving_circle), run_time=0.25)


        

        self.play(self.camera.frame.animate.scale(0.7*0.7*0.7*0.7))

        # 1. Animate central cluster point by point (REAL iterative)
        print("Animating Central Cluster point by point...")
        for point_idx in central_indices:
            animate_point_individually(point_idx, BLUE)
        self.wait(2)


        self.play(self.camera.frame.animate.scale((1/0.7)*3))

        # 2. Animate ring1 with moving circle (FAKE)
        animate_ring_with_moving_circle(ring1_indices, GREEN, ring1_radius, "Ring 1")
        self.wait(0.3)
        
        # 3. Animate ring2 with moving circle (FAKE)  
        animate_ring_with_moving_circle(ring2_indices, PURPLE, ring2_radius, "Ring 2")
        self.wait(3)
        
        # 4. Animate noise points individually
        print("Animating Noise points...")
        for point_idx in outlier_indices:
            animate_point_individually1(point_idx, RED)
        
        self.wait(2)

class DBSCANVisualization(Scene):
    def construct(self):

        self.camera.frame.scale(0.644)

        # Data points
        cluster_1_points = [
            [-1.5, 0.5, 0], [-0.5, 0.8, 0], [-1.4, -0.2, 0], [-0.6, -0.1, 0], 
            [-1.0, 0.9, 0], [-1.2, 0.1, 0], [-0.9, 0.2, 0], [-1.3, 0.3, 0],
            [-1.1, 0.0, 0], [-0.7, 0.7, 0], [-1.05, -0.3, 0], [-0.95, -0.5, 0],
            [-1.25, 0.7, 0], [-0.75, -0.6, 0], [-1.4, 0.4, 0]
        ]
        
        cluster_2_points = [
            [0.5, 0.5, 0], [1.5, 0.8, 0], [0.4, -0.2, 0], [1.6, -0.1, 0],
            [1.0, 0.9, 0], [1.2, 0.1, 0], [0.9, 0.2, 0], [1.3, 0.3, 0],
            [1.1, 0.0, 0], [0.7, 0.7, 0], [1.05, -0.3, 0], [0.95, -0.5, 0],
            [1.25, 0.7, 0], [0.75, -0.6, 0], [1.4, 0.4, 0]
        ]
        
        outlier_points = [
            [2.5, 2, 0], [-2.5, -2, 0], [3, 0, 0], [-3, 0, 0], [-2, 1, 0]
        ]
        
        all_points = cluster_1_points + cluster_2_points + outlier_points
        
        # Create dots (initially all WHITE)
        dots = VGroup(*[
            Dot(point=point, color=WHITE, radius=0.08)
            for point in all_points
        ])
        
        self.add(dots)
        self.wait(1)
        
        # DBSCAN parameters
        epsilon = 0.66
        min_pts = 4
        
        # Create epsilon circle
        epsilon_circle = Circle(
            radius=epsilon, 
            color=YELLOW, 
            stroke_width=4,
            fill_color=YELLOW,
            fill_opacity=0.1
        ).move_to(all_points[0])
        self.play(ShowCreation(epsilon_circle))

        
        # Add epsilon text below the clusters
        epsilon_text = Tex(f"epsilon = {epsilon}").set_color(ORANGE)
        epsilon_text.move_to([0, -2, 0]).shift(RIGHT*0.67)  # Position below the clusters
        self.play(Write(epsilon_text), run_time=1)
        self.wait(2)
        

        
        # Fade out epsilon text and fade in midpoint text
        midpoint_text = Tex(r"Min \  point \geq 4").set_color(ORANGE)
        midpoint_text.move_to([0, -2, 0]).shift(RIGHT*0.67)  # Same position as epsilon text

        self.play(
            ReplacementTransform(epsilon_text, midpoint_text),
            run_time=1
        )
        self.wait(2)
        
        # Fade out midpoint text
        self.play(FadeOut(midpoint_text), run_time=1)
        
        # Algorithm state
        visited = [False] * len(all_points)
        cluster_assignments = [-1] * len(all_points)  # -1 = unclassified, -2 = noise
        current_cluster_id = 0
        cluster_colors = [BLUE, GREEN, PURPLE, PINK]
        
        def get_neighbors(point_idx):
            """Find neighbors within ε → call this set N(P)"""
            neighbors = []
            current_point = all_points[point_idx]
            for i, other_point in enumerate(all_points):
                if i != point_idx:
                    distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(current_point, other_point)))
                    if distance <= epsilon:
                        neighbors.append(i)
            return neighbors
        
        def get_current_color(point_idx):
            """Get the current color a point should have based on its cluster assignment"""
            if cluster_assignments[point_idx] == -2:  # Noise
                return RED
            elif cluster_assignments[point_idx] >= 0:  # In cluster
                return cluster_colors[cluster_assignments[point_idx] % len(cluster_colors)]
            else:  # Unclassified
                return WHITE
        
        def reset_colors(point_indices):
            """Reset colors to their current classification state"""
            if len(point_indices) > 0:
                color_updates = []
                for idx in point_indices:
                    current_color = get_current_color(idx)
                    color_updates.append(dots[idx].animate.set_color(current_color))
                
                if color_updates:
                    self.play(*color_updates, run_time=0.3)
        
        def expand_cluster(core_point_idx, cluster_id):
            """Expand cluster from a core point using the specified algorithm"""
            cluster_color = cluster_colors[cluster_id % len(cluster_colors)]
            
            # Step 1: Find neighbors of the core point
            neighbors = get_neighbors(core_point_idx)
            
            # Step 2: Add core point to cluster
            cluster_assignments[core_point_idx] = cluster_id
            self.play(dots[core_point_idx].animate.set_color(cluster_color), run_time=0.5)
            
            # Step 3: Add ALL neighbors to the cluster (including those marked as noise)
            neighbor_updates = []
            unclassified_neighbors = []
            
            for neighbor_idx in neighbors:
                if cluster_assignments[neighbor_idx] <= -1:  # Unclassified or noise
                    cluster_assignments[neighbor_idx] = cluster_id
                    neighbor_updates.append(dots[neighbor_idx].animate.set_color(cluster_color))
                    if cluster_assignments[neighbor_idx] != -2:  # Only add to queue if wasn't noise
                        unclassified_neighbors.append(neighbor_idx)
                    else:
                        unclassified_neighbors.append(neighbor_idx)  # Add noise points too for expansion check
            
            if neighbor_updates:
                self.play(*neighbor_updates, run_time=0.8)
                self.wait(0.5)
            
            # Step 4: For each neighbor, check if it's also a core point
            expansion_queue = unclassified_neighbors.copy()
            
            for neighbor_idx in expansion_queue:
                if not visited[neighbor_idx]:
                    visited[neighbor_idx] = True
                    
                    # Store original color
                    original_color = get_current_color(neighbor_idx)
                    
                    # Make it orange to show it's being processed
                    self.play(
                        epsilon_circle.animate.move_to(all_points[neighbor_idx]),
                        dots[neighbor_idx].animate.set_color(ORANGE),
                        run_time=0.4
                    )
                    
                    # Find neighbors of this neighbor
                    neighbor_neighbors = get_neighbors(neighbor_idx)
                    
                    # Highlight ALL neighbors as YELLOW (regardless of current assignment)
                    if neighbor_neighbors:
                        yellow_dots = VGroup(*[dots[j] for j in neighbor_neighbors])
                        self.play(yellow_dots.animate.set_color(YELLOW), run_time=0.4)
                        self.wait(0.6)
                    
                    # Check if this neighbor is also a core point
                    if len(neighbor_neighbors) >= min_pts:
                        # It's a core point! Recursively expand
                        # Add its neighbors to the cluster
                        new_additions = []
                        for nn in neighbor_neighbors:
                            if cluster_assignments[nn] <= -1:  # Unclassified or noise
                                cluster_assignments[nn] = cluster_id
                                new_additions.append(dots[nn].animate.set_color(cluster_color))
                                expansion_queue.append(nn)  # Add to queue for potential expansion
                        
                        if new_additions:
                            self.play(*new_additions, run_time=0.5)
                    
                    # Restore the point to its cluster color
                    self.play(dots[neighbor_idx].animate.set_color(original_color), run_time=0.3)
                    
                    # Reset ALL neighbor highlights to their proper colors
                    if neighbor_neighbors:
                        reset_colors(neighbor_neighbors)
                    
                    self.wait(0.3)
        
        # Main algorithm loop
        for point_idx in range(len(all_points)):
            if visited[point_idx]:
                continue
            
            # Store original color (if already classified)
            original_color = get_current_color(point_idx)
            
            # Step 1: Color current point ORANGE and move circle
            self.play(
                epsilon_circle.animate.move_to(all_points[point_idx]),
                dots[point_idx].animate.set_color(ORANGE),
                run_time=0.6
            )
            
            visited[point_idx] = True
            
            # Step 2: Find neighbors within ε → call this set N(P)
            neighbors = get_neighbors(point_idx)
            
            # Highlight ALL neighbors in YELLOW (regardless of current assignment)
            if len(neighbors) > 0:
                neighbor_dots = VGroup(*[dots[j] for j in neighbors])
                self.play(neighbor_dots.animate.set_color(YELLOW), run_time=0.6)
                self.wait(1)
            
            # Step 3: Check if P is a core point (|N(P)| ≥ minPts)
            if len(neighbors) >= min_pts:
                # P is a core point: Start/expand a cluster (only if not already classified)
                if cluster_assignments[point_idx] <= -1:  # Unclassified or noise
                    expand_cluster(point_idx, current_cluster_id)
                    current_cluster_id += 1
                else:
                    # Already classified, just restore its color
                    self.play(dots[point_idx].animate.set_color(original_color), run_time=0.3)
            else:
                # Not a core point - mark as temporary noise (RED) if unclassified
                if cluster_assignments[point_idx] == -1:  # Only if unclassified
                    self.play(dots[point_idx].animate.set_color(RED), run_time=0.6)
                    cluster_assignments[point_idx] = -2  # Mark as noise
                else:
                    # Already classified, restore its color
                    self.play(dots[point_idx].animate.set_color(original_color), run_time=0.3)
            
            # Reset ALL neighbor highlights to their proper colors
            if len(neighbors) > 0:
                reset_colors(neighbors)
            
            self.wait(0.8)
        
        # Remove circle
        self.play(FadeOut(epsilon_circle))
        self.wait(1)
        
        # Create convex hulls for final clusters
        cluster_hulls = []
        
        for cluster_id in range(current_cluster_id):
            # Get all points in this cluster
            cluster_points = []
            for i, assignment in enumerate(cluster_assignments):
                if assignment == cluster_id:
                    cluster_points.append([all_points[i][0], all_points[i][1]])
            
            if len(cluster_points) >= 3:
                cluster_points = np.array(cluster_points)
                
                # Calculate convex hull
                hull = ConvexHull(cluster_points)
                hull_vertices = cluster_points[hull.vertices]
                
                # Scale hull by 1.3 around centroid
                centroid = np.mean(hull_vertices, axis=0)
                scaled_hull_vertices = centroid + 1.3 * (hull_vertices - centroid)
                
                # Convert to 3D points
                hull_points_3d = [[p[0], p[1], 0] for p in scaled_hull_vertices]
                
                # Create polygon with fill only
                hull_polygon = Polygon(
                    *hull_points_3d,
                    fill_color=cluster_colors[cluster_id],
                    fill_opacity=0.3,
                    stroke_width=0
                )
                
                cluster_hulls.append(hull_polygon)
        
        # Fade in convex hulls
        if cluster_hulls:
            self.play(*[FadeIn(hull) for hull in cluster_hulls], run_time=1.5)
            self.wait(2)
        
        self.wait(2)

