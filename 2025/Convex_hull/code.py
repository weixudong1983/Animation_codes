from manimlib import *
import numpy as np
from scipy.spatial import ConvexHull

 
class SimpleConvexHull(Scene):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hull_style = {
            "stroke_width": 3,
            "stroke_opacity": 1,
            "fill_opacity": 0.2
        }
        self.camera.background_color = "#1a1a1a"
    
    def construct(self):
        # First example
        self.show_geometric_example()
        self.wait(3)
        self.clear()
        self.wait(1)
        
        # Second example
        self.show_organic_example()
        self.wait(3)
        self.clear()
        self.wait(1)

        # Third new example
        self.show_random_example()
        self.wait(1)
    
    def show_geometric_example(self):
        points = [
            [0, 3.5, 0], [1.4, 1.4, 0], [3.5, 0, 0], [1.4, -1.4, 0],
            [0, -3.5, 0], [-1.4, -1.4, 0], [-3.5, 0, 0], [-1.4, 1.4, 0],
            [0, 2, 0], [1, 1, 0], [2, 0, 0], [1, -1, 0],
            [0, -2, 0], [-1, -1, 0], [-2, 0, 0], [-1, 1, 0],
            [0, 0, 0]
        ]
        self.create_hull_example(points, "#00ff88", "#ff0055")
    
    def show_organic_example(self):
        points = [
            [-4, 0.5, 0], [-2.8, 2.2, 0], [-1, 2.8, 0], [1.2, 2.5, 0],
            [3.2, 1.8, 0], [3.5, -0.5, 0], [2.2, -2, 0], [0, -2.8, 0],
            [-2.5, -1.8, 0], [-3.8, -0.2, 0],
            [-2, 1, 0], [-0.8, 1.5, 0], [0.8, 1.5, 0], [2, 0.5, 0],
            [1.8, -1, 0], [0, -1.5, 0], [-1.5, -0.8, 0], [0, 0, 0],
            [0.5, -0.5, 0], [-0.5, 0.5, 0]
        ]
        self.create_hull_example(points, "#00aaff", "#ffaa00")

    def show_random_example(self):
        # New example: random scattered points
        np.random.seed(42)
        points = np.random.uniform(-3.5, 3.5, size=(20, 2))
        points = np.hstack((points, np.zeros((20,1))))  # Make them 3D
        points = points.tolist()
        self.create_hull_example(points, "#ff66cc", "#66ffcc")
    
    def create_hull_example(self, points, point_color, hull_color):
        # Create dots
        dots = VGroup()
        for p in points:
            dot = Dot(point=p, radius=0.1, color=point_color)
            dots.add(dot)
        
        self.wait(1)
        
        # Show dots one-by-one
        for dot in dots:
            self.play(FadeIn(dot), run_time=0.1)
        self.wait(1)

        # Compute convex hull
        points_array = np.array(points)[:, :2]
        hull = ConvexHull(points_array)
        hull_indices = hull.vertices
        
        # Highlight hull points with pause
        for i in hull_indices:
            self.play(dot_highlight(dots[i], hull_color), run_time=0.2)
        self.wait(1)

        # Create and show hull edges one after another with pause
        edges = VGroup()
        for i in range(len(hull_indices)):
            start_idx = hull_indices[i]
            end_idx = hull_indices[(i+1) % len(hull_indices)]
            
            start_point = points[start_idx]
            end_point = points[end_idx]
            
            edge = Line(start_point, end_point, color=hull_color)
            edges.add(edge)
            
            self.play(ShowCreation(edge), run_time=0.3)
        
        self.wait(1)

        # Once all edges are drawn, create and show the filled polygon
        hull_points = [points[i] for i in hull_indices]
        hull_polygon = Polygon(*hull_points, color=hull_color, fill_opacity=0.2)
        
        self.play(FadeIn(hull_polygon), run_time=0.5)
        self.play(FadeOut(edges), run_time=0.3)

        self.wait(2)


# Helper animation function
def dot_highlight(dot, new_color):
    return AnimationGroup(
        dot.animate.set_color(new_color).scale(1.2),
        lag_ratio=0.5
    )
