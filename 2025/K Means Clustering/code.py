from manimlib import *
import numpy as np


class SimpleAxes(VGroup):
    """
    Minimal first-quadrant axes with a c2p mapper.
    Draws only positive x/y arrows starting at origin.
    """
    def __init__(
        self,
        x_max=10, y_max=7,           # expanded extents for more spread
        x_length=8.8, y_length=5.2,  # on-screen lengths
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


class KMeansIntroduction(Scene):
    def construct(self):

        self.camera.frame.scale(1.08)
        # ------------------- Tunables (sizes kept) -------------------
        DOT_RADIUS = 0.14
        CENTROID_RADIUS = 0.28
        CENTROID_STROKE = 4
        LINE_STROKE = 5           # thicker dashed lines
        DASH_LEN = 0.14
        MAX_ITERS = 10
        DEMO_ITERS = 2            # Only show dotted lines for first 2 iterations
        TOL = 1e-6                # tighter so convergence needs multiple moves


        # Colors
        DOT_RED = RED             # dots use Manim RED/BLUE
        DOT_BLUE = BLUE
        PURE_RED = "#FF0000"      # centroids are pure hex
        PURE_BLUE = "#0000FF"


        # Z-index layering: dots < dashed lines < centroids < centroid labels
        Z_DOTS = 0
        Z_LINES = 1
        Z_CENTROIDS = 3
        Z_CENTROID_LABELS = 4


        # ------------------- Helpers -------------------
        def color_for(assign):
            return DOT_RED if assign == "red" else DOT_BLUE


        def dist(p, q):
            return np.linalg.norm(p - q)


        def make_X():
            try:
                t = Text("X", weight=BOLD)
            except Exception:
                t = Tex("\\mathbf{X}")
            t.set_stroke(width=1)
            return t


        # ------------------- Axes -------------------
        axes = SimpleAxes(
            x_max=10, y_max=7,
            x_length=8.8, y_length=5.2,
            origin=ORIGIN + 2.5*DOWN + 4.4*LEFT,
            stroke_width=2, tip=True
        )
        x_label = Tex("x_{1}")
        y_label = Tex("x_{2}")
        x_label.next_to(axes.get_x_end(), DOWN, buff=0.28)
        y_label.next_to(axes.get_y_end(), LEFT, buff=0.28)



        # ------------------- Points: Two VERY dispersed clusters -------------------
        # Cluster A (left region): WIDELY scattered across left half
        cluster_A = [
            (0.8, 1.2), (1.5, 4.8), (0.6, 6.1), (2.2, 0.9), (1.9, 5.7),
            (0.9, 3.4), (2.8, 2.1), (1.1, 6.3), (2.6, 4.2), (0.7, 2.8),
            (1.7, 1.5), (3.1, 5.9), (0.5, 4.1), (2.4, 3.7), (1.3, 0.7),
            (2.9, 6.2), (1.8, 2.3), (0.4, 5.4), (2.7, 1.8), (1.2, 3.9),
            (3.2, 0.8), (0.8, 5.1), (2.1, 4.6), (1.6, 1.1), (2.5, 6.0)
        ]
        
        # Cluster B (right region): WIDELY scattered across right half  
        cluster_B = [
            (6.2, 5.8), (7.8, 1.4), (8.9, 4.2), (6.7, 2.8), (9.1, 5.9),
            (7.4, 0.8), (8.1, 6.1), (6.9, 3.7), (9.3, 2.1), (7.2, 4.9),
            (8.7, 1.7), (6.4, 5.2), (9.0, 3.4), (7.6, 6.4), (8.3, 0.9),
            (6.8, 4.1), (9.2, 2.6), (7.1, 5.7), (8.5, 3.8), (6.5, 1.3),
            (9.4, 4.8), (7.9, 2.4), (8.0, 5.4), (6.6, 3.1), (8.8, 6.2)
        ]


        points_coords = cluster_A + cluster_B
        nA = len(cluster_A)
        A_indices = list(range(0, nA))
        B_indices = list(range(nA, len(points_coords)))


        points = VGroup(*[
            Dot(axes.c2p(x, y), radius=DOT_RADIUS, color=GREY).set_z_index(Z_DOTS)
            for x, y in points_coords
        ])



        a = VGroup(axes, x_label, y_label).scale(1.17)
        self.play(ShowCreation(a))


        self.play(FadeIn(points, lag_ratio=0.02, run_time=1.0))


        # ------------------- Centroids: Start FAR from actual clusters -------------------
        # Red centroid starts at top-middle (far from both clusters)
        red_centroid = Circle(
            radius=CENTROID_RADIUS,
            stroke_color=PURE_RED, fill_color=PURE_RED,
            stroke_width=CENTROID_STROKE, fill_opacity=1.0
        ).move_to(axes.c2p(5.0, 6.5)).set_z_index(Z_CENTROIDS)  # Top-middle
        red_X = make_X().move_to(red_centroid.get_center()).set_z_index(Z_CENTROID_LABELS)


        # Blue centroid starts at bottom-middle (far from both clusters)
        blue_centroid = Circle(
            radius=CENTROID_RADIUS,
            stroke_color=PURE_BLUE, fill_color=PURE_BLUE,
            stroke_width=CENTROID_STROKE, fill_opacity=1.0
        ).move_to(axes.c2p(5.0, 0.5)).set_z_index(Z_CENTROIDS)  # Bottom-middle
        blue_X = make_X().move_to(blue_centroid.get_center()).set_z_index(Z_CENTROID_LABELS)


        self.play(
            ShowCreation(red_centroid), Write(red_X),
            ShowCreation(blue_centroid), Write(blue_X)
        )


        # Pointers to rotate demo choices each iteration
        a_ptr, b_ptr = 0, 0
        alternate_order = True  # alternate demo order each iteration to vary RED/BLUE first


        # ------------------- K-means iterations -------------------
        for iteration in range(MAX_ITERS):
            # Full assignments container
            full_assignments = [None] * len(points_coords)
            
            # Only show dotted line demo for first DEMO_ITERS iterations
            if iteration < DEMO_ITERS:
                # Choose 2 demo points: one from each cluster, rotating
                demo = []
                if alternate_order:
                    # Show B first, then A
                    if B_indices:
                        demo.append(B_indices[b_ptr])
                    if A_indices:
                        demo.append(A_indices[a_ptr])
                else:
                    # Show A first, then B
                    if A_indices:
                        demo.append(A_indices[a_ptr])
                    if B_indices:
                        demo.append(B_indices[b_ptr])

                # Advance pointers for next iteration (round-robin)
                if A_indices:
                    a_ptr = (a_ptr + 1) % len(A_indices)
                if B_indices:
                    b_ptr = (b_ptr + 1) % len(B_indices)
                alternate_order = not alternate_order

                # Demo: for each selected point, draw to red (pause), draw to blue (pause), remove, then color
                for idx in demo:
                    x, y = points_coords[idx]
                    p = axes.c2p(x, y)
                    r = red_centroid.get_center()
                    b = blue_centroid.get_center()

                    line_r = DashedLine(p, r, dash_length=DASH_LEN, color=PURE_RED, stroke_width=LINE_STROKE).set_z_index(Z_LINES)
                    self.play(ShowCreation(line_r), run_time=0.25)
                    self.wait(1.0)

                    line_b = DashedLine(p, b, dash_length=DASH_LEN, color=PURE_BLUE, stroke_width=LINE_STROKE).set_z_index(Z_LINES)
                    self.play(ShowCreation(line_b), run_time=0.25)
                    self.wait(1.0)

                    assign = "red" if dist(p, r) < dist(p, b) else "blue"
                    full_assignments[idx] = assign

                    self.play(Uncreate(line_r), Uncreate(line_b), run_time=0.25)
                    self.play(points[idx].animate.set_color(color_for(assign)), run_time=0.25)
                    self.wait(1.0)  # 1-second pause after each individual dot coloring

                # Assign remaining points (non-demo) and color them together
                for i in range(len(points_coords)):
                    if full_assignments[i] is not None:
                        continue
                    x, y = points_coords[i]
                    p = axes.c2p(x, y)
                    r = red_centroid.get_center()
                    b = blue_centroid.get_center()
                    full_assignments[i] = "red" if dist(p, r) < dist(p, b) else "blue"

                self.play(*[
                    points[i].animate.set_color(color_for(full_assignments[i]))
                    for i in range(len(points_coords)) if i not in demo
                ], run_time=0.9)
                self.wait(1.0)  # 1-second pause after batch coloring
                
            else:
                # After DEMO_ITERS: just assign colors without dotted line demonstrations
                for i in range(len(points_coords)):
                    x, y = points_coords[i]
                    p = axes.c2p(x, y)
                    r = red_centroid.get_center()
                    b = blue_centroid.get_center()
                    full_assignments[i] = "red" if dist(p, r) < dist(p, b) else "blue"

                # Color all points at once
                self.play(*[
                    points[i].animate.set_color(color_for(full_assignments[i]))
                    for i in range(len(points_coords))
                ], run_time=0.6)


            # Compute new centroids (scene coords) and check convergence
            red_pts = [axes.c2p(*points_coords[i]) for i, a in enumerate(full_assignments) if a == "red"]
            blue_pts = [axes.c2p(*points_coords[i]) for i, a in enumerate(full_assignments) if a == "blue"]


            if len(red_pts) > 0:
                red_mean = np.mean(np.vstack(red_pts), axis=0); red_mean[2] = 0
            else:
                red_mean = red_centroid.get_center()
            if len(blue_pts) > 0:
                blue_mean = np.mean(np.vstack(blue_pts), axis=0); blue_mean[2] = 0
            else:
                blue_mean = blue_centroid.get_center()


            r_old = red_centroid.get_center()
            b_old = blue_centroid.get_center()
            converged = (dist(r_old, red_mean) < TOL) and (dist(b_old, blue_mean) < TOL)


            if converged:
                break


            # Move centroids AND reset ALL dots to GREY for the next iteration
            self.play(
                red_centroid.animate.move_to(red_mean),
                red_X.animate.move_to(red_mean),
                blue_centroid.animate.move_to(blue_mean),
                blue_X.animate.move_to(blue_mean),
                *[pt.animate.set_color(GREY) for pt in points],
                run_time=1.1
            )
            self.wait(0.2)


        # ------------------- Final coloring -------------------
        final_assignments = []
        for i, (x, y) in enumerate(points_coords):
            p = axes.c2p(x, y)
            r = red_centroid.get_center()
            b = blue_centroid.get_center()
            final_assignments.append("red" if dist(p, r) < dist(p, b) else "blue")


        self.play(*[
            points[i].animate.set_color(color_for(final_assignments[i]))
            for i in range(len(points))
        ], run_time=0.8)


        # Fade out centroids; keep colored dots only
        self.play(
            FadeOut(red_centroid), FadeOut(red_X),
            FadeOut(blue_centroid), FadeOut(blue_X),
            run_time=0.7
        )
        self.wait(2)

        from scipy.spatial import ConvexHull
        
        # Separate points by final assignment
        red_cluster_points = []
        blue_cluster_points = []
        
        for i, assignment in enumerate(final_assignments):
            x, y = points_coords[i]
            screen_point = axes.c2p(x, y)
            if assignment == "red":
                red_cluster_points.append(screen_point[:2])  # Only x,y coordinates
            else:
                blue_cluster_points.append(screen_point[:2])
        
        # Create convex hull shapes
        shapes_to_add = []
        
        if len(red_cluster_points) >= 3:  # Need at least 3 points for ConvexHull
            red_points_array = np.array(red_cluster_points)
            red_hull = ConvexHull(red_points_array)
            red_vertices = red_points_array[red_hull.vertices]
            # Convert back to 3D points for Manim
            red_vertices_3d = [np.array([x, y, 0]) for x, y in red_vertices]
            red_shape = Polygon(*red_vertices_3d, 
                               fill_color=RED, fill_opacity=0.2, 
                               stroke_width=0).set_z_index(Z_DOTS - 1).scale(1.)  # Behind dots
            shapes_to_add.append(red_shape)
        
        if len(blue_cluster_points) >= 3:  # Need at least 3 points for ConvexHull
            blue_points_array = np.array(blue_cluster_points)
            blue_hull = ConvexHull(blue_points_array)
            blue_vertices = blue_points_array[blue_hull.vertices]
            # Convert back to 3D points for Manim
            blue_vertices_3d = [np.array([x, y, 0]) for x, y in blue_vertices]
            blue_shape = Polygon(*blue_vertices_3d, 
                                fill_color=BLUE, fill_opacity=0.2, 
                                stroke_width=0).set_z_index(Z_DOTS - 1).scale(1.3)  # Behind dots
            shapes_to_add.append(blue_shape)
        
        # Animate the shapes appearing
        if shapes_to_add:
            self.play(*[FadeIn(shape) for shape in shapes_to_add], run_time=1.0)
        
        self.wait(2)




