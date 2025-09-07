from manimlib import *
import numpy as np

class FeatureSelection(Scene):
    def construct(self): 

        self.camera.frame.scale(0.73).shift(UP*0.17)
        # Create custom axes without ticks, in first quadrant
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 4, 1],
            axis_config={
                "stroke_width": 7,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            }
        ).set_color(GREY_E)
        
        # Create axis labels (at the end of axes)
        x_label = Tex("x_1").next_to(axes.x_axis.get_end(), RIGHT, buff=0.2).set_color(BLACK)
        y_label = Tex("x_2").next_to(axes.y_axis.get_end(), UP, buff=0.2).set_color(BLACK)
        
        # Create 8 data points with high variance in x1 and low variance in x2 (in first quadrant)
        data_points = [
            [0.8, 1.8],
            [1.68, 2.0],
            [2.6, 1.9],
            [3.46, 2.2],
            [4.25, 2.1],
            [5.0, 1.8],
            [5.8, 2.0],
            [6.4, 1.9]
        ]
        
        # Create blue dots for data points (bigger and using set_color)
        dots = VGroup()
        for x, y in data_points:
            dot = Dot(axes.c2p(x, y), radius=0.123)
            dot.set_color(BLUE_D)
            dots.add(dot).set_z_index(1)
        
        # Create green dotted lines to x-axis and projection dots
        x_projection_lines = VGroup()
        x_projection_dots = VGroup()
        for x, y in data_points:
            line = DashedLine(
                axes.c2p(x, y),
                axes.c2p(x, 0),
                dash_length=0.1,
                stroke_width=4
            )
            line.set_color(GREEN)  
            line.set_z_index(-1)
            x_projection_lines.add(line).set_z_index(-1)
            
            # Small green dot at projection point
            proj_dot = Dot(axes.c2p(x, 0), radius=0.12)
            proj_dot.set_color(GREEN)  # Pure green
            x_projection_dots.add(proj_dot)
        
        # Create red dotted lines to y-axis and projection dots
        y_projection_lines = VGroup()
        y_projection_dots = VGroup()
        for x, y in data_points:
            line = DashedLine(
                axes.c2p(x, y),
                axes.c2p(0, y),
                dash_length=0.1,
                stroke_width=4
            )
            line.set_color(RED) 
            y_projection_lines.add(line).set_z_index(-1)
            
            # Small red dot at projection point
            proj_dot = Dot(axes.c2p(0, y), radius=0.12)
            proj_dot.set_color(RED)  # Pure red
            y_projection_dots.add(proj_dot)
        
        # Animation sequence
        self.play(
            ShowCreation(axes.x_axis),
            ShowCreation(axes.y_axis),
            run_time=1.5
        )
        
        self.play(
            Write(x_label),
            Write(y_label),
            run_time=1
        )

        
        self.wait(1.5)
        
        # Show data points
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.2),
            run_time=2
        )
        
        self.wait(1)
        
        # Show projections to x-axis with small green dots
        self.play(
            LaggedStart(*[ShowCreation(line) for line in x_projection_lines], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(dot) for dot in x_projection_dots], lag_ratio=0.2),
            run_time=2
        )
        
        self.wait(1)
        
        # Show projections to y-axis with small red dots
        self.play(
            LaggedStart(*[ShowCreation(line) for line in y_projection_lines], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(dot) for dot in y_projection_dots], lag_ratio=0.2),
            run_time=2
        )

        
        self.wait(2)
        
        # ------------------ NEW ADDITIONS ------------------

        # Uncreate the projection lines, keep only the dots
        self.play(
            Uncreate(x_projection_lines),
            Uncreate(y_projection_lines),
            run_time=2
        )

        self.wait(1)

        # Create horizontal brace for x-axis projections (High Variance)
        x_proj_points = [axes.c2p(x, 0) for x, _ in data_points]
        leftmost_x = min(x_proj_points, key=lambda p: p[0])
        rightmost_x = max(x_proj_points, key=lambda p: p[0])

        x_brace = Brace(
            Line(leftmost_x, rightmost_x),
            direction=DOWN,
            color=GREEN
        ).set_color(GREEN)
        x_brace_label = Text("High Variance").next_to(x_brace, DOWN).set_color(GREEN)

        # Create vertical brace for y-axis projections (Low Variance)
        y_proj_points = [axes.c2p(0, y) for _, y in data_points]
        bottom_y = min(y_proj_points, key=lambda p: p[1])
        top_y = max(y_proj_points, key=lambda p: p[1])

        y_brace = Brace(
            Line(bottom_y, top_y),
            direction=LEFT,
            color=RED
        ).set_color(RED)
        y_brace_label = Text("Low Variance", color=RED).rotate(PI/2).next_to(y_brace, LEFT).set_color(RED)
        
        self.play(self.camera.frame.animate.scale(1.1).shift(DOWN*0.29))

        # Animate braces and labels
        self.play(
            GrowFromCenter(x_brace),
            Write(x_brace_label),
            GrowFromCenter(y_brace),
            Write(y_brace_label),
            run_time=1.5
        )

        self.wait(2)

        self.play(FadeOut(VGroup(x_brace, x_brace_label, y_brace, y_brace_label,y_projection_dots, dots,  )))
        self.play(FadeOut(VGroup(axes.get_y_axis(), y_label)))

        self.play(self.camera.frame.animate.scale(0.82).shift(DOWN*1.6+RIGHT*0.3))
        self.wait(2)

