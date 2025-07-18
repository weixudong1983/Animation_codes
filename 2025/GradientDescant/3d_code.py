from manim import *
import numpy as np

class GradientDescentOnMSE(ThreeDScene):
    def construct(self):
        # Set background color to white
        self.camera.background_color = LOGO_WHITE
        
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 8, 1],
            x_length=7,
            y_length=7,
            z_length=6,
            axis_config={"color": BLACK},  # Changed to black for white background
        )

        # Axis labels - made black for white background
        w_label = axes.get_x_axis_label(Tex("w", font_size=48, color=BLACK))
        b_label = axes.get_y_axis_label(Tex("b", font_size=48, color=BLACK))
        j_label = axes.get_z_axis_label(Tex("J(w,b)", font_size=48, color=BLACK))

        # Cost function
        def mse_cost_function(u, v):
            return np.array([u, v, 0.5 * (u ** 2 + v ** 2)])

        # Surface
        surface = Surface(
            lambda u, v: axes.c2p(*mse_cost_function(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(40, 40),
            fill_opacity=8,
        )
        surface.set_color(RED)

        # Group the scene
        graph_3d = VGroup(axes, w_label, b_label, j_label, surface)
        graph_3d.shift(DOWN * 2 + IN * 2)

        # Gradient descent rule display - made black text
        w_rule = MathTex(r"w \leftarrow w - \alpha \frac{\partial J}{\partial w}", font_size=32, color=BLACK)
        b_rule = MathTex(r"b \leftarrow b - \alpha \frac{\partial J}{\partial b}", font_size=32, color=BLACK)
        update_rules = VGroup(w_rule, b_rule).arrange(DOWN, buff=0.2).to_corner(UR).scale(1.3).shift(DOWN*4.67+LEFT*1.23)

        # Camera setup
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        self.add(axes, w_label, b_label, j_label)
        self.add_fixed_in_frame_mobjects(update_rules)
        self.play(Create(surface), run_time=3)
        self.play(Write(update_rules))
        self.wait(1)
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=3)
        self.wait(1.5)

        # --- Gradient Descent Dot Animation ---
        alpha = 0.2
        w, b = 2.5, 2.0
        dot = Dot3D(point=axes.c2p(w, b, 0.5 * (w**2 + b**2)), color=YELLOW).scale(2)
        
        # Modified tangent line - extends beyond the dot
        def create_tangent_line():
            current_pos = axes.c2p(w, b, 0.5 * (w**2 + b**2))
            # Calculate gradient direction
            grad_w = w  # derivative of 0.5*(w^2 + b^2) w.r.t. w
            grad_b = b  # derivative of 0.5*(w^2 + b^2) w.r.t. b
            
            # Normalize gradient for consistent line length
            grad_magnitude = np.sqrt(grad_w**2 + grad_b**2)
            if grad_magnitude > 0:
                grad_w_norm = grad_w / grad_magnitude
                grad_b_norm = grad_b / grad_magnitude
            else:
                grad_w_norm = grad_b_norm = 0
            
            # Create line that extends in both directions from the dot
            line_length = 1.5  # Adjust this to make line longer/shorter
            start_point = current_pos - line_length * np.array([grad_w_norm, grad_b_norm, 0])
            end_point = current_pos + line_length * np.array([grad_w_norm, grad_b_norm, 0])
            
            return Line3D(
                start=start_point,
                end=end_point,
                color=GREEN,
                stroke_width=4
            )
        
        self.add(dot)

        # Animate descent
        for _ in range(20):
            # Gradient updates
            w *= (1 - alpha)
            b *= (1 - alpha)
            new_pos = axes.c2p(w, b, 0.5 * (w**2 + b**2))
            self.play(dot.animate.move_to(new_pos), run_time=0.7)

        self.wait(2)

