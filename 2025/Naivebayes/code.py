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





 
