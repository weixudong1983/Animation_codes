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

class GiftWrappingAlgorithm(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = "#1a1a1a"
    
    def construct(self):
        # Use the organic example points
        points = [
            [-4, 0.5, 0], [-2.8, 2.2, 0], [-1, 2.8, 0], [1.2, 2.5, 0],
            [3.2, 1.8, 0], [3.5, -0.5, 0], [2.2, -2, 0], [0, -2.8, 0],
            [-2.5, -1.8, 0], [-3.8, -0.2, 0],
            [-2, 1, 0], [-0.8, 1.5, 0], [0.8, 1.5, 0], [2, 0.5, 0],
            [1.8, -1, 0], [0, -1.5, 0], [-1.5, -0.8, 0], [0, 0, 0],
            [0.5, -0.5, 0], [-0.5, 0.5, 0]
        ]
        self.demonstrate_gift_wrapping(points)
    
    def demonstrate_gift_wrapping(self, points):
        # Create dots for all points
        dots = VGroup()
        for p in points:
            dot = Dot(point=p, radius=0.1, color="#00aaff")
            dots.add(dot)
        
        # Show all dots at once
        self.play(FadeIn(dots), run_time=1)
        self.wait(1)
        
        # Find the leftmost point (minimum x-coordinate)
        points_array = np.array(points)
        leftmost_idx = np.argmin(points_array[:, 0])
        current_point = points[leftmost_idx]
        
        # Highlight the starting point
        self.play(
            dots[leftmost_idx].animate.set_color("#ffaa00").scale(1.5),
            run_time=0.5
        )
        self.wait(0.5)
        
        # Initialize the hull
        hull_points = [leftmost_idx]
        current_idx = leftmost_idx
        
        # Gift wrapping algorithm visualization
        edges = VGroup()
        scanning_line = None
        
        # We'll continue until we reach the starting point again
        next_idx = None
        
        while next_idx != hull_points[0]:
            # Start from a point that is not the current point
            next_idx = (current_idx + 1) % len(points)
            
            # Create a scanning line (initially pointing to the candidate next point)
            if scanning_line is not None:
                self.play(FadeOut(scanning_line), run_time=0.2)
            
            scanning_line = Line(
                start=current_point,
                end=points[next_idx],
                color="#ffaa00",
                stroke_width=2
            )
            self.play(ShowCreation(scanning_line), run_time=0.3)
            
            # Scan all points to find the most counterclockwise point
            for i in range(len(points)):
                if i == current_idx:
                    continue
                
                # Check if point i is more counterclockwise than the current next_idx
                orientation = self.orientation(
                    current_point,
                    points[next_idx],
                    points[i]
                )
                
                if orientation < 0:  # More counterclockwise
                    # Create new scanning line to this point
                    new_scanning_line = Line(
                        start=current_point,
                        end=points[i],
                        color="#ffaa00",
                        stroke_width=2
                    )
                    # Replace old scanning line with new one
                    self.play(
                        ReplacementTransform(scanning_line, new_scanning_line),
                        run_time=0.2
                    )
                    scanning_line = new_scanning_line
                    next_idx = i
            
            # Highlight the chosen next point
            self.play(
                dots[next_idx].animate.set_color("#ffaa00").scale(1.5),
                run_time=0.5
            )
            
            # Add an edge from current to next
            edge = Line(
                start=current_point,
                end=points[next_idx],
                color="#ffaa00",
                stroke_width=3
            )
            edges.add(edge)
            self.play(
                ReplacementTransform(scanning_line, edge),
                run_time=0.3
            )
            scanning_line = None
            
            # Update current point
            current_idx = next_idx
            current_point = points[current_idx]
            hull_points.append(next_idx)
            
            # If we've come back to the start, break
            if next_idx == hull_points[0]:
                break
            
            self.wait(0.3)
        
        self.wait(1)
        
        # Create and show the filled polygon
        hull_point_coords = [points[i] for i in hull_points[:-1]]  # Exclude the duplicated start point
        hull_polygon = Polygon(*hull_point_coords, color="#ffaa00", fill_opacity=0.2)
        
        self.play(FadeIn(hull_polygon), run_time=0.5)
        self.wait(1)
        
        # Show completed hull
        self.wait(2)
    
    def orientation(self, p, q, r):
        """
        Returns the orientation of triplet (p, q, r).
        0 --> Collinear 
        1 --> Clockwise
        -1 --> Counterclockwise
        """
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return -1 if val > 0 else 1





