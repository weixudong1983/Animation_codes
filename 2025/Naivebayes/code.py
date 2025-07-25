from manimlib import *
import random


# Define a custom Star class since it's not a default Mobject
class Star(Polygon):
    def __init__(self, n=5, **kwargs):
        # Calculate vertices for a regular n-pointed star
        outer_radius = 1
        inner_radius = 0.5 # Adjust for pointiness
        
        outer_vertices = [
            np.array([
                outer_radius * np.cos(2 * PI * k / n),
                outer_radius * np.sin(2 * PI * k / n),
                0
            ]) for k in range(n)
        ]
        
        inner_vertices = [
            np.array([
                inner_radius * np.cos(2 * PI * (k + 0.5) / n),
                inner_radius * np.sin(2 * PI * (k + 0.5) / n),
                0
            ]) for k in range(n)
        ]

        # Interleave vertices to form the star shape
        vertices = []
        for i in range(n):
            vertices.append(outer_vertices[i])
            vertices.append(inner_vertices[i])
        
        # Set fill properties to match the stroke color by default
        if 'color' in kwargs and 'fill_color' not in kwargs:
            kwargs['fill_color'] = kwargs['color']
        if 'fill_opacity' not in kwargs:
            kwargs['fill_opacity'] = 1.0
            
        super().__init__(*vertices, **kwargs)
        self.scale(0.5) # Default scale to match Circle size better


class BayesRule(Scene):
    
    def construct(self):
        self.camera.frame.scale(1.4).shift(DOWN*2.1)
        # Create all shapes
        all_shapes = []
        
        # Create 3 stars: 2 green, 1 red
        for i in range(2):
            star = Star(color=GREEN, fill_opacity=1)
            all_shapes.append(star)
        
        star = Star(color=RED, fill_opacity=1)
        all_shapes.append(star)
        
        # Create 7 circles: 2 green, 5 red
        for i in range(2):
            circle = Circle(color=GREEN, fill_opacity=1, stroke_color=GREEN)
            circle.scale(0.5)
            all_shapes.append(circle)
        
        for i in range(5):
            circle = Circle(color=RED, fill_opacity=1, stroke_color=RED)
            circle.scale(0.5)
            all_shapes.append(circle)
        
        # Shuffle shapes randomly
        random.shuffle(all_shapes)
        
        # Define 2x5 grid parameters
        rows = 2
        cols = 5
        x_spacing = 2.5
        y_spacing = 1.6
        
        # Calculate grid positions
        x_positions = np.linspace(-x_spacing * (cols-1)/2, x_spacing * (cols-1)/2, cols)
        y_positions = [y_spacing / 2, -y_spacing / 2]  # Top row, bottom row
        
        # Create grid coordinates
        grid_positions = []
        for y in y_positions:
            for x in x_positions:
                grid_positions.append([x, y, 0])
        
        # Create the enclosing box
        box_width = x_spacing * (cols - 1) + 2.0  # Grid width + padding
        box_height = y_spacing + 2.0  # Grid height + padding
        
        enclosing_box = Rectangle(
            width=box_width,
            height=box_height,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0  # Transparent fill so shapes are visible
        )
        enclosing_box.move_to(ORIGIN).set_color(GREY)
        
        # Display the box first
        self.play(ShowCreation(enclosing_box), run_time=1)
        self.wait(0.5)
        
        # Assign shapes to grid positions
        for i, shape in enumerate(all_shapes):
            shape.move_to(grid_positions[i])
        
        # Display all shapes using GrowFromCenter
        for shape in all_shapes:
            self.play(GrowFromCenter(shape), run_time=0.3)
        
        self.wait(2)


        probability_text = Tex(r"P(star) = \frac{3}{10}",color=BLACK).set_color(WHITE)
        probability_text.next_to(enclosing_box, DOWN, buff=1.5).shift(DOWN).scale(3)

        self.play(Write(probability_text[:7]))
        self.wait(2)

        rect = SurroundingRectangle(all_shapes[2], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect2 = SurroundingRectangle(all_shapes[6], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect3 = SurroundingRectangle(all_shapes[7], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        self.play(ShowCreation(rect), ShowCreation(rect2), ShowCreation(rect3), run_time=1.5)
        self.wait(2)

        self.play(FadeIn(probability_text[7:]), run_time=1.8)
        self.wait(2)

        self.play(FadeOut(probability_text), 
                  FadeOut(rect), FadeOut(rect2), FadeOut(rect3), run_time=1.5)


        probability_text = Tex(r"P(Green) = \frac{4}{10}",color=BLACK).set_color(WHITE)
        probability_text.next_to(enclosing_box, DOWN, buff=1.5).shift(DOWN).scale(3)

        self.play(Write(probability_text[:8]))
        self.wait(2)

        rect = SurroundingRectangle(all_shapes[2], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect2 = SurroundingRectangle(all_shapes[4], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect3 = SurroundingRectangle(all_shapes[5], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect4 = SurroundingRectangle(all_shapes[7], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        self.play(ShowCreation(rect), ShowCreation(rect2), ShowCreation(rect3), ShowCreation(rect4), run_time=1.5)
        self.wait(2)


        self.play(FadeIn(probability_text[8:]), run_time=1.8)
        self.wait(2)

        self.play(FadeOut(probability_text), 
                  FadeOut(rect), FadeOut(rect2), FadeOut(rect3), FadeOut(rect4), run_time=1.5)
        
        self.play(self.camera.frame.animate.shift(RIGHT*2))

        question = ImageMobject("question.png").next_to(enclosing_box, RIGHT, buff=0).scale(0.8)

        self.play(FadeIn(question))

        self.wait(2)

        text = Text("P(star|Green) = ").next_to(enclosing_box, DOWN, buff=1.8).shift(DOWN+LEFT*3.06).scale(2)

        self.play(Write(text))
        self.wait(2)

        temp = Text("Total Green Stars").next_to(text, RIGHT, buff=1).scale(2).shift(UP*0.5+RIGHT*2.2)
        line = Line(LEFT*3, RIGHT*3, stroke_width=6).next_to(temp, DOWN, buff=0.4).scale(1.6)
        temp_1 = Text("Total Green").next_to(line, DOWN, buff=0.1).scale(2).shift(DOWN*0.3)

        self.play(Write(temp), Write(line), )
        self.play(Write(temp_1))

        self.wait(2)

        rect = SurroundingRectangle(all_shapes[2], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect2 = SurroundingRectangle(all_shapes[7], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)

        self.play(ShowCreation(rect), ShowCreation(rect2), run_time=1.5)
        self.wait(2)

        a = rect.copy()
        b = rect2.copy()

        self.play(a.animate.move_to(all_shapes[4]), b.animate.move_to(all_shapes[5]), run_time=1.5)

        self.wait(2)

        self.play(Transform(temp, Text("2").scale(2).move_to(temp.get_center())),
                  Transform(temp_1, Text("4").scale(2).move_to(temp_1.get_center())),
                  Transform(line, Line(LEFT*0.4, RIGHT*0.4, stroke_width=6).move_to(line).scale(1.6)),
                  text.animate.shift(RIGHT*4),
                  run_time=1.5)
        
        self.wait(2)



class BayesTheoremDerivation(Scene):
    def construct(self):
        self.camera.frame.scale(0.8).shift(UP*1.73)
        # STEP 1: Complete equation in one line
        eq1 = Tex(r"P(Star \mid Green) = \frac{P(Star \cap Green)}{P(Green)}").scale(1.2).to_edge(UP)
        self.play(Write(eq1))
        self.wait(1)

        # STEP 2: Second complete equation in one line
        eq2 = Tex(r"P(Green \mid Star) = \frac{P(Green \cap Star)}{P(Star)}").scale(1.1).next_to(eq1, DOWN, buff=1.2)
        self.play(Write(eq2))
        self.wait(1.2)


        # STEP 3: Isolate intersection - complete equation
        isolate = Tex(r"P(Green \cap Star) = P(Green \mid Star) \cdot P(Star)")
        isolate.move_to(eq1)
        self.play(Transform(eq1, isolate))
        self.wait(1.5)

        # STEP 4: Final Bayes theorem - complete equation
        final_eq = Tex(r"P(Star \cap Green) = P(Star \mid Green) \cdot P(Green)").move_to(eq2)
        self.play(Transform(eq2, final_eq))
        self.wait(2)

        rect1 = SurroundingRectangle(eq1[:14], color=YELLOW, stroke_width=6)
        rect2 = SurroundingRectangle(eq2[:13], color=YELLOW, stroke_width=6)

        self.play(
            ShowCreation(rect1),
            ShowCreation(rect2),
            run_time=1
        )

        self.wait(2)

        self.play(
            Transform(rect1, SurroundingRectangle(eq1[15:], color=YELLOW)),
            Transform(rect2, SurroundingRectangle(eq2[14:], color=YELLOW)), run_time=1)

        # Box it

        self.wait(2)

        final_eq = Tex(r"P(Star \mid Green) = \frac{P(Green \mid Star) \cdot P(Star)}{P(Green)}").move_to(VGroup(eq1, eq2).get_center()).scale(1)
        self.play(ReplacementTransform(VGroup(eq2, eq1), final_eq),Uncreate(rect1), Uncreate(rect2))
        self.wait(1.5)

        box = SurroundingRectangle(final_eq, color="#00FF00", stroke_width=6).scale(1.06)
        self.play(ShowCreation(box))
        self.wait(2)
        self.play(Uncreate(box))


        # STEP 5: Explain the Denominator
        denom_explain = Tex(r"P(Green) = P(Green \mid Star) \cdot P(Star) + P(Green \mid \neg Star) \cdot P(\neg Star)").scale(0.95*0.7)
        denom_explain.next_to(final_eq, DOWN, buff=1.5)
        self.play(Write(denom_explain), self.camera.frame.animate.shift(DOWN))
        self.wait(3)

        brace = Brace(denom_explain[:8], DOWN, buff=0.2).set_color(YELLOW)
        self.play(GrowFromCenter(brace))

        self.wait(1.5)

        self.play(Transform(brace, Brace(denom_explain[9:30], DOWN, buff=0.2).set_color(YELLOW)))
        
        self.wait(1.5)

        self.play(Transform(brace, Brace(denom_explain[31:], DOWN, buff=0.2).set_color(YELLOW)))

        self.wait(1.5)


        # STEP 6: Final transformed full Bayes Equation with expanded denominator
        expanded_bayes = Tex(
            r"P(Star \mid Green) = \frac{P(Green \mid Star) \cdot P(Star)}{P(Green \mid Star) \cdot P(Star) + P(Green \mid \neg Star) \cdot P(\neg Star)}"
        ).scale(0.9)
        expanded_bayes.move_to(final_eq.get_center()).scale(0.9*0.9*0.87)

        self.play(
            ReplacementTransform(VGroup(final_eq, denom_explain), expanded_bayes),
            self.camera.frame.animate.shift(UP),
            FadeOut(brace)
        )
        self.wait(2)



        equation_A_B = Tex(r"P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B \mid A) \cdot P(A) + P(B \mid \neg A) \cdot P(\neg A)}").scale(1.3*0.9*0.9*0.9).move_to(expanded_bayes)
        self.play(Transform(expanded_bayes, equation_A_B))
        self.wait(2)

        self.play(expanded_bayes[-16].animate.set_color(RED), 
                  expanded_bayes[-5].animate.set_color(RED),)
        
        self.wait(2)


        temp  =  Tex(r"P(A \mid x_1, x_2, \ldots, x_n) = \frac{P(x_1, x_2, \ldots, x_n \mid A) \cdot P(A)}{P(x_1, x_2, \ldots, x_n)}").scale(0.9).move_to(expanded_bayes)
        self.play(Transform(expanded_bayes, temp))
        self.wait(2)



 
