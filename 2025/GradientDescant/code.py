from manimlib import *

class GD1(Scene):
    
    def construct(self):

        self.camera.frame.scale(1.3).shift(DOWN)

        axes = Axes(
            (0, 9.2), (0, 8), height=6,
            axis_config={"include_ticks": False, "include_numbers": False, "stroke_width": 6},).set_color(GREY_E)
    
        x_label = Tex("x").scale(2).set_color(BLACK)
        y_label = Tex("y").scale(2).set_color(BLACK)

        # 2. Use .next_to() to place them precisely
        x_label.next_to(axes.x_axis.get_end(), DOWN)
        y_label.next_to(axes.y_axis.get_end(), LEFT)

        self.play(Write(axes, lag_ratio=0.01, run_time=1))
        self.play(ShowCreation(VGroup(x_label, y_label)))

        self.wait(2)

        # Axes.get_graph will return the graph of a function
        quad = axes.get_graph(
            lambda x: 0.1 * (1.87*(x - 4.6))**2 + 1.35,
            x_range=[0.56, 8.61], # Explicitly define the x_range for the plot
            stroke_width=8,
        ).set_color(BLUE_E).set_z_index(-3)

        self.play(ShowCreation(quad))

        self.wait(1)

        graph_func = lambda x: 0.1 * (1.87*(x - 4.6))**2 + 1.35

        # Create a yellow dot that will roll down the curve
        dot = Dot(radius=0.18).set_color(RED)
        # Start the dot at a peak (around x=4.7, which is near a local maximum)
        start_x = 8.23
        # Calculate the corresponding y-coordinate by calling the function
        start_y = graph_func(start_x)

        # Now, convert the (x, y) coordinates to a screen point
        start_point = axes.c2p(start_x, start_y)        
        
        dot.move_to(start_point)
        
        # Show the dot appearing
        self.play(FadeIn(dot))
        self.wait(2)

        # Create the Tex object
        update_rule = Tex(r"\boldsymbol{x_{n+1} = x_n - \alpha \frac{dy}{dx}}")
        
        # You can then set its color, size, and position
        update_rule.set_color(BLACK)
        update_rule.scale(1.2*1.2).next_to(axes, DOWN, buff=0.8).shift(DOWN*0.4)
        
        # And animate it
        self.play(Write(update_rule))

        self.wait(2)

        rect = SurroundingRectangle(update_rule[:4], color="#0000ff", stroke_width=6).scale(1.15)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(update_rule[5:7], color="#0000ff", stroke_width=6).scale(1.15)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(update_rule[8:], color="#0000ff", stroke_width=6).scale(1.07)))
        self.wait(2)

        self.play(update_rule[-6].animate.set_color(MAROON_D)) 
        self.wait(2)

        self.play(Transform(update_rule[-6], Tex(r"\boldsymbol{\eta}").scale(1.2*1.2).set_color(MAROON_D).move_to(update_rule[-6])))  
        self.wait(2)

        self.play(Transform(update_rule[-6], Tex(r"\boldsymbol{\alpha}").scale(1.2*1.2).set_color(BLACK).move_to(update_rule[-6])))  
        self.wait()
        self.play(update_rule[-5:].animate.set_color(MAROON_D))




        # 1. Define learning rate (alpha) and derivative function
        alpha = 0.4
        deriv_func = lambda x: 0.2 * (1.87**2) * (x - 4.6)
        
        # Keep track of the dot's current x-value
        current_x = start_x

        ORANGE = GREEN_E
        
        # 2. Create the initial tangent line to represent the slope
        slope_value = deriv_func(current_x)
        tangent_line = Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=6, color=ORANGE)
        tangent_line.rotate(np.arctan(slope_value))
        tangent_line.move_to(dot.get_center()).set_z_index(-2)
        
        self.play(ShowCreation(tangent_line))
        self.wait(1)
        self.play(Uncreate(rect), update_rule[-5:].animate.set_color(BLACK) )
        
        # 3. Loop to perform the update steps
        for _ in range(12):
            # Calculate the slope at the current position
            slope_value = deriv_func(current_x)
            
            # Update the x-position using the gradient descent rule
            new_x = current_x - alpha * slope_value
            
            # Find the new point on the curve
            new_point = axes.c2p(new_x, graph_func(new_x))
            
            # Create the new tangent line for the next position
            new_tangent_line = Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=6, color=ORANGE)
            new_tangent_line.rotate(np.arctan(deriv_func(new_x)))
            new_tangent_line.move_to(new_point).set_z_index(-2)

            # Animate the dot moving and the tangent line transforming
            self.play(
                dot.animate.move_to(new_point),
                Transform(tangent_line, new_tangent_line),
                update_rule[-5:].animate.scale(0.8),
                run_time=0.67
            )
            self.wait(0.5)
            
            
            # Update the current_x for the next iteration
            current_x = new_x

        self.wait(0.3)
        self.play(FadeOut(tangent_line))
        self.play(update_rule[-5:].animate.scale((1/0.8)*12))  

        self.wait(3)

        #second after

        start_x_right = 8.23
        # Create the path for the dot to return to its start position
        return_path = axes.get_graph(graph_func, x_range=[current_x, start_x_right])
        
        self.play(
            MoveAlongPath(dot, return_path), # Move dot back along the graph
            run_time=1.5
        )

        start_point_right = axes.c2p(start_x_right, graph_func(start_x_right))
        
        # Recreate the tangent at the start
        tangent_line.rotate(np.arctan(deriv_func(start_x_right)) - tangent_line.get_angle())
        tangent_line.move_to(start_point_right)
        self.play(ShowCreation(tangent_line))
        self.wait(1)

        # Highlight dy/dx term
        self.play(Transform(rect, SurroundingRectangle(update_rule[-5:], color="#0000ff", stroke_width=6)))
        positive = Text("Positive", weight=BOLD).set_color(PURPLE_C).next_to(update_rule, RIGHT, buff=1.8).scale(1.8)
        self.play(FadeIn(positive))
        self.wait(2)



        # Highlight the full update term
        self.play(Transform(rect, SurroundingRectangle(update_rule[8:], color="#0000ff", stroke_width=6).scale(1.05)))



        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(update_rule[:4], color="#0000ff", stroke_width=6).scale(1.1)))
        increasing = Text("Decrease" , weight=BOLD).set_color("#AF1717").next_to(update_rule, LEFT, buff=1.8).scale(1.77)
        self.play(FadeIn(increasing))
        self.wait(2)

        # Fade out everything to reset
        self.play(FadeOut(dot), FadeOut(tangent_line))
        self.wait(1)
        
        # 2. Setup for negative slope (left side)
        start_x_left = 1.4
        start_point_left = axes.c2p(start_x_left, graph_func(start_x_left))
        dot.move_to(start_point_left)

        self.play(
            FadeIn(dot),
        )
        self.wait(1)

        # Create tangent on the left side
        tangent_line.rotate(np.arctan(deriv_func(start_x_left)) - tangent_line.get_angle())
        tangent_line.move_to(start_point_left)
        self.play(ShowCreation(tangent_line))
        self.wait(1)
 
        self.play(Transform(rect, SurroundingRectangle(update_rule[-5:], color="#0000ff", stroke_width=6)))
        self.play(Transform(positive, Text("Negative", weight=BOLD).set_color(GREEN_E).move_to(positive).scale(1.8)))

        self.wait(2)
        # Highlight the full update term
        self.play(Transform(rect, SurroundingRectangle(update_rule[8:], color="#0000ff", stroke_width=6)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(update_rule[:4], color="#0000ff", stroke_width=6).scale(1.1)))

        self.play(Transform(increasing,Text("Increase" , weight=BOLD).set_color(PURPLE_D).move_to(increasing).scale(1.77) ))

        self.wait(2)

        self.play(FadeOut(rect), FadeOut(VGroup(increasing, positive)))
        
        # 3. Animate the gradient descent from the left side
        current_x = start_x_left
        for _ in range(12): 
            slope_value = deriv_func(current_x)
            new_x = current_x - alpha * slope_value
            new_point = axes.c2p(new_x, graph_func(new_x))
            
            new_tangent_line = Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=6, color=ORANGE)
            new_tangent_line.rotate(np.arctan(deriv_func(new_x)))
            new_tangent_line.move_to(new_point).set_z_index(-2)

            self.play(
                dot.animate.move_to(new_point),
                Transform(tangent_line, new_tangent_line),
                update_rule[-5:].animate.scale(0.8),
                run_time=0.67
            )
            self.wait(0.2)
            current_x = new_x

            

        self.wait(0.3)
        self.play(FadeOut(tangent_line))
        self.play(update_rule[-5:].animate.scale((1/0.8)*12))


        self.wait(3)

        rect = SurroundingRectangle(update_rule[8], stroke_width=5.5, color="#0000ff")
        self.play(ShowCreation(rect))
        self.wait(2)
        
        self.play(update_rule[8].animate.scale(0.5) )

        
        start_x_right = 7.23
        # Create the path for the dot to return to its start position
        return_path = axes.get_graph(graph_func, x_range=[current_x, start_x_right])
        
        self.play(
            MoveAlongPath(dot, return_path), # Move dot back along the graph
            run_time=1.5,
        )

        start_point_right = axes.c2p(start_x_right, graph_func(start_x_right))
        
        # Recreate the tangent at the start
        tangent_line.rotate(np.arctan(deriv_func(start_x_right)) - tangent_line.get_angle())
        tangent_line.move_to(start_point_right)
        self.play(ShowCreation(tangent_line))


        # Set a new, smaller learning rate
        alpha = 0.05  # The original alpha was 0.4

        # Reset the starting position to the right side
        current_x = start_x_right

        # The dot and tangent line are already in position, so we can start the loop.

        # Loop to perform gradient descent with the small learning rate
        for _ in range(39):  # Use the same number of iterations to contrast the distance covered
            # Calculate the slope at the current position
            slope_value = deriv_func(current_x)
            
            # Update the x-position using the gradient descent rule with the new small alpha
            new_x = current_x - alpha * slope_value
            
            # Find the new point on the curve
            new_point = axes.c2p(new_x, graph_func(new_x))
            
            # Create the new tangent line for the next position
            new_tangent_line = Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=6, color=ORANGE)
            new_tangent_line.rotate(np.arctan(deriv_func(new_x)))
            new_tangent_line.move_to(new_point).set_z_index(-2)

            # Animate the dot moving a small step and the tangent line transforming
            self.play(
                dot.animate.move_to(new_point),
                Transform(tangent_line, new_tangent_line),
                update_rule[-5:].animate.scale(0.97),
                run_time=0.7  # A bit faster per step, since the steps are small
            )
            # No wait time between steps to make the process feel continuous but slow
            
            # Update the current_x for the next iteration
            current_x = new_x

        self.play(FadeOut(tangent_line))
        
        



        self.play(update_rule[-5:].animate.scale(2.44).shift(RIGHT*0.2))
        self.wait(2)
        self.play(update_rule[8].animate.scale(3.45), rect.animate.scale(1.5), )
        


        start_x_right = 7.23
        # Create the path for the dot to return to its start position
        return_path = axes.get_graph(graph_func, x_range=[current_x, start_x_right])
        
        self.play(
            MoveAlongPath(dot, return_path), # Move dot back along the graph
            run_time=1.5,
        )
        self.wait(2)
        start_point_right = axes.c2p(start_x_right, graph_func(start_x_right))
        
        # Recreate the tangent at the start
        tangent_line.rotate(np.arctan(deriv_func(start_x_right)) - tangent_line.get_angle())
        tangent_line.move_to(start_point_right)
        self.play(ShowCreation(tangent_line))

        # Set a new, LARGER learning rate that will cause overshooting
        alpha = 3.9

        # Loop to perform gradient descent with the large learning rate
        for _ in range(3): # A few steps are enough to show divergence
            # Calculate the slope at the current position
            slope_value = deriv_func(current_x)
            
            # Update the x-position using the gradient descent rule
            new_x = current_x - alpha * slope_value
            
            # Get the coordinates for the dot's new position
            new_point = axes.c2p(new_x, graph_func(new_x))
            
            # Create the new tangent line for the next position
            new_tangent_line = Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=6, color=ORANGE)
            new_tangent_line.rotate(np.arctan(deriv_func(new_x)))
            new_tangent_line.move_to(new_point).set_z_index(-2)
            
            # Visualize the "jump" with a dashed line to emphasize the overshoot
            jump_line = DashedLine(dot.get_center(), new_point, color=PURPLE, stroke_width=7)

            # Animate the jump, the dot moving, and the tangent line transforming
            self.play(ShowCreation(jump_line), run_time=0.7)
            self.play(
                dot.animate.move_to(new_point),
                Transform(tangent_line, new_tangent_line),
                run_time=1.0
            )
            self.play(FadeOut(jump_line))
            self.wait(0.5)
            
            # Update the current_x for the next iteration
            current_x = new_x
            
            # Break if the dot goes too far off-screen
            if not (axes.x_range[0] < current_x < axes.x_range[1] + 1):
                break

        self.wait(3)


        self.play(FadeOut(VGroup(dot, tangent_line, rect, update_rule )), self.camera.frame.animate.scale(0.8).shift(UP))


        quad1 = axes.get_graph(
            lambda x: np.sin(3.4 * x) + np.sin(x) + 3,
            x_range=[0.56, 8.61], # Explicitly define the x_range for the plot
            stroke_width=8,
        ).set_color(PURPLE_D).set_z_index(-3)

        self.play(Transform(quad, quad1))

        self.wait(2)

        arrow = Arrow(ORIGIN, ORIGIN+DOWN*1.4, stroke_width=6).set_color(GREEN_E).shift(RIGHT*0.46+DOWN*0.5)
       
        a = arrow.copy().shift(LEFT*1.7 + UP*0.5)
        b = arrow.copy().shift(RIGHT*1.8+UP*0.9)
        c = arrow.copy().shift(LEFT*3.7+UP*1.19)
        

        self.play(GrowArrow(arrow), GrowArrow(a), GrowArrow(b), GrowArrow(c))

        
        self.wait(2)

        self.play(
            a.animate.shift(UP*0.8+RIGHT*0.7),
            b.animate.shift(UP*1.7+RIGHT),
            arrow.animate.shift(UP*1.7+RIGHT*1.1),
            c.animate.shift(UP*1.4+RIGHT*0.9)
        )


        self.wait(2)

        self.play(FadeOut(VGroup(a,b,c, arrow)))

        #NEW NON CONVEX VISUALS

        # Re-introduce the dot
        dot = Dot(radius=0.18).set_color(RED)

        non_convex_func = lambda x: np.sin(3.4 * x) + np.sin(x) + 3
        non_convex_deriv_func = lambda x: 3.4 * np.cos(3.4 * x) + np.cos(x)
 
        # Choose a starting point for GD that leads to a local minimum
        # Let's try to start near a local maximum or a point where it will fall into a local minimum.
        # Looking at the graph of sin(3.4x) + sin(x) + 3, a good starting point could be around x=2.5
        # This should converge to the local minimum around x=3.5-4
        start_x_non_convex = 2.5 
        start_point_non_convex = axes.c2p(start_x_non_convex, non_convex_func(start_x_non_convex))
        dot.move_to(start_point_non_convex)

        self.play(FadeIn(dot))
        self.wait(1)


        # Create the initial tangent line for the non-convex function
        slope_value_non_convex = non_convex_deriv_func(start_x_non_convex)
        tangent_line = Line(LEFT * 1.13, RIGHT * 1.13, stroke_width=6, color=ORANGE)
        tangent_line.rotate(np.arctan(slope_value_non_convex))
        tangent_line.move_to(dot.get_center()).set_z_index(-2)
        
        self.play(ShowCreation(tangent_line))
        self.wait(1)

        # Set a suitable learning rate for the non-convex function
        alpha_non_convex = 0.05 # Adjust as needed for good visualization

        current_x_non_convex = start_x_non_convex

        local_min_text = Tex("Local Minimum").scale(1.5).set_color(RED).to_edge(UP)
        
        for i in range(10): # More iterations to ensure it settles
            slope_value = non_convex_deriv_func(current_x_non_convex)
            new_x = current_x_non_convex - alpha_non_convex * slope_value
            new_point = axes.c2p(new_x, non_convex_func(new_x))
            
            new_tangent_line = Line(LEFT * 1.5, RIGHT * 1.5, stroke_width=6, color=ORANGE)
            new_tangent_line.rotate(np.arctan(non_convex_deriv_func(new_x)))
            new_tangent_line.move_to(new_point).set_z_index(-2)

            self.play(
                dot.animate.move_to(new_point),
                Transform(tangent_line, new_tangent_line),
                run_time=0.4 # Slightly faster to see convergence
            )
            current_x_non_convex = new_x
            
            # Optional: Add a small pause if you want to emphasize each step
            self.wait(0.1)

        

        self.play(FadeOut(tangent_line))
        self.play(Write(local_min_text))
        self.wait(2)



class GradientDescentND(Scene):
    def construct(self):

        # Title
        title = Text("Gradient Descent: General Case", weight=BOLD).set_color(GREEN).shift(DOWN*0.3).scale(1.3)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Cost function
        cost_func = Tex(r"\mathbf{J(w_1, w_2, \dots, w_n, b)}").set_color(BLACK).scale(1.3)
        cost_func.scale(1.3)
        cost_func.next_to(title, DOWN, buff=1)
        self.play(Write(cost_func))
        self.wait(1)


        # Update rules
        # Update rules (split into a 2x2 matrix)
        eq1 = Tex(r"w_1 := w_1 - \alpha \frac{\partial J}{\partial w_1}").set_color(BLACK).scale(1.3)
        eq2 = Tex(r"w_2 := w_2 - \alpha \frac{\partial J}{\partial w_2}").set_color(BLACK).scale(1.3)
        eq3 = Tex(r"w_n := w_n - \alpha \frac{\partial J}{\partial w_n}").set_color(BLACK).scale(1.3)
        eq4 = Tex(r"b := b - \alpha \frac{\partial J}{\partial b}").set_color(BLACK).scale(1.3)
        
        # Arrange in 2 rows, 2 columns
        left_col = VGroup(eq1, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        right_col = VGroup(eq2, eq4).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        
        eqs_group = VGroup(left_col, right_col).arrange(RIGHT, buff=1.5)
        eqs_group.next_to(cost_func, DOWN, buff=1)
        
        # Animate equations
        for eq in [eq1, eq2, eq3, eq4]:
            self.play(Write(eq))
            self.wait(0.3)

        self.wait(2)


