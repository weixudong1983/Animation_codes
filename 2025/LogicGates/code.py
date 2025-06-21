from manimlib import *
import numpy as np

GRAY = GREY
LIGHT_GREY = GREY_A
DARK_GREY = "#2E2E2E"
YELLOW  = "#00FF00"
GREEN  = "#00FF00"

from manimlib import *
import numpy as np

GRAY = GREY
LIGHT_GREY = GREY_A
DARK_GREY = "#2E2E2E"
YELLOW = "#00FF00"
GREEN = "#00FF00"
RED = "#FF0000"

class Bulb(VMobject):
    def __init__(self, radius=0.3, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.is_on = False
        self.create_bulb()
        
    def create_bulb(self):
        self.glass = Circle(radius=self.radius).set_stroke(WHITE, 2).set_fill(DARK_GREY, opacity=0.2)
        self.base = Rectangle(height=self.radius * 0.6, width=self.radius * 0.5).set_fill(LIGHT_GREY).set_stroke(GREY, 1).next_to(self.glass, DOWN, buff=0)
        self.screw = Rectangle(height=self.radius * 0.3, width=self.radius * 0.4).set_fill(GREY).set_stroke(DARK_GREY, 1).next_to(self.base, DOWN, buff=0)

        self.filament = VMobject()
        filament_points = [
            np.array([-self.radius * 0.2, 0, 0]),
            np.array([-self.radius * 0.08, self.radius * 0.2, 0]),
            np.array([self.radius * 0.08, -self.radius * 0.2, 0]),
            np.array([self.radius * 0.2, 0, 0])
        ]
        self.filament.set_points_as_corners(filament_points).set_stroke(LIGHT_GREY, 1.5).move_to(self.glass.get_center())

        self.outer_glow = Circle(radius=self.radius * 1.3).set_fill(YELLOW, opacity=0).set_stroke(YELLOW, width=6, opacity=0).move_to(self.glass.get_center())
        self.add(self.outer_glow, self.glass, self.base, self.screw, self.filament)

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            return AnimationGroup(
                self.glass.animate.set_fill(YELLOW, opacity=0.6),
                self.outer_glow.animate.set_fill(YELLOW, opacity=0.2).set_stroke(opacity=0.15),
                self.filament.animate.set_stroke(YELLOW, width=2.5),
                run_time=0.5
            )
        return Animation(Mobject())

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            return AnimationGroup(
                self.glass.animate.set_fill(DARK_GREY, opacity=0.2),
                self.outer_glow.animate.set_fill(opacity=0).set_stroke(opacity=0),
                self.filament.animate.set_stroke(LIGHT_GREY, width=1.5),
                run_time=0.4
            )
        return Animation(Mobject())

class NANDGateWithComponents(Scene):
    def construct(self):

        self.camera.frame.scale(0.77).shift(DOWN*1.6)

        left_line = Line(UP * 0.6, DOWN * 0.6, stroke_width=3)
        top_line = Line(UP * 0.6, UP * 0.6 + RIGHT * 0.6, stroke_width=3)
        bottom_line = Line(DOWN * 0.6, DOWN * 0.6 + RIGHT * 0.6, stroke_width=3)
        arc = Arc(radius=0.6, start_angle=-PI / 2, angle=PI, arc_center=RIGHT * 0.6, stroke_width=3)
        and_gate_body = VGroup(left_line, top_line, bottom_line, arc).set_stroke(WHITE, width=3).move_to(LEFT * 2)

        triangle = Polygon(LEFT * 0.5 + UP * 0.4, LEFT * 0.5 + DOWN * 0.4, RIGHT * 0.4).set_stroke(WHITE, width=3).set_fill(opacity=0).move_to(RIGHT * 1.5)
        
        bubble_radius = 0.08
        bubble_center = RIGHT * (1.56 + 0.4 + bubble_radius)
        bubble = Circle(radius=bubble_radius).set_stroke(WHITE, width=3).set_fill(opacity=0).move_to(bubble_center)
        not_gate_body = VGroup(triangle, bubble)

        input_a_line = Line(LEFT * 3.5 + UP * 0.3, LEFT * 2.6 + UP * 0.3, stroke_width=3).set_stroke(WHITE, 3)
        input_b_line = Line(LEFT * 3.5 + DOWN * 0.3, LEFT * 2.6 + DOWN * 0.3, stroke_width=3).set_stroke(WHITE, 3)

        bulb_a = Bulb(radius=0.2)
        bulb_b = Bulb(radius=0.2)
        intermediate_bulb = Bulb(radius=0.15)
        output_bulb = Bulb(radius=0.2)

        bulb_a.rotate(PI / 2)
        bulb_b.rotate(PI / 2)
        intermediate_bulb.rotate(-PI / 2)
        output_bulb.rotate(-PI / 2)

        bulb_a.move_to(LEFT * 3.8 + UP * 0.3)
        bulb_b.move_to(LEFT * 3.8 + DOWN * 0.3)
        intermediate_bulb.move_to(LEFT * 0.15)
        output_bulb.move_to(RIGHT * 3.8)

        intermediate_line_left = Line(LEFT * 1.4, intermediate_bulb.get_left(), stroke_width=3).set_stroke(WHITE, 3)
        intermediate_line_right = Line(intermediate_bulb.get_right(), RIGHT * 1.06, stroke_width=3).set_stroke(WHITE, 3)
        intermediate_line = VGroup(intermediate_line_left, intermediate_line_right)

        output_line = Line(bubble.get_right(), RIGHT * 3.5, stroke_width=3).set_stroke(WHITE, 3)

        labels = VGroup(
            Text("A", font_size=20, color=WHITE).next_to(bulb_a, LEFT, buff=0.2),
            Text("B", font_size=20, color=WHITE).next_to(bulb_b, LEFT, buff=0.2),
            Text("AND", font_size=14, color=WHITE).next_to(intermediate_bulb, UP, buff=0.2),
            Text("Y", font_size=20, color=WHITE).next_to(output_bulb, RIGHT, buff=0.2),
            Text("AND", font_size=18, color=WHITE).next_to(and_gate_body, DOWN, buff=0.3),
            Text("NOT", font_size=18, color=WHITE).next_to(not_gate_body, DOWN, buff=0.3)
        )

        truth_table_title = Text("NAND Truth Table", font_size=20, color=WHITE)
        table_data = [["A", "B", "AND", "Y"], ["0", "0", "0", "1"], ["0", "1", "0", "1"], ["1", "0", "0", "1"], ["1", "1", "1", "0"]]
        table_group = VGroup()

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                t = Text(cell, font_size=16, color=WHITE)
                t.move_to(RIGHT * ((j - 1.5) * 0.8) + UP * (-2.5 - i * 0.4))
                row_group.add(t)
            table_group.add(row_group)

        truth_table_title.next_to(table_group, UP, buff=0.3)

        self.play(ShowCreation(and_gate_body), ShowCreation(not_gate_body), run_time=2)
        self.play(Write(labels[4]), Write(labels[5]), run_time=1)
        self.play(
            ShowCreation(input_a_line),
            ShowCreation(input_b_line),
            ShowCreation(intermediate_line_left),
            ShowCreation(intermediate_line_right),
            ShowCreation(output_line),
            run_time=1.5
        )
        self.play(FadeIn(bulb_a), FadeIn(bulb_b), FadeIn(intermediate_bulb), FadeIn(output_bulb), run_time=1)
        self.play(*[Write(label) for label in labels[:4]], run_time=1)
        self.play(Write(truth_table_title), Write(table_group), run_time=2)

        highlight_rect = Rectangle(width=2.6, height=0.32, fill_color=TEAL_B, fill_opacity=0.05, stroke_color=TEAL_B, stroke_width=3).move_to(table_group[1]).scale(1.1)
        self.play(FadeIn(highlight_rect), run_time=0.3)

        combinations = [(False, False, False, True), (False, True, False, True), (True, False, False, True), (True, True, True, False)]

        for i, (a_state, b_state, and_state, nand_state) in enumerate(combinations):
            if i > 0:
                self.play(highlight_rect.animate.move_to(table_group[i + 1]), run_time=0.7)

            animations = []

            if a_state and not bulb_a.is_on:
                animations += [bulb_a.turn_on(), Transform(input_a_line, input_a_line.copy().set_stroke(YELLOW, 5))]
            elif not a_state and bulb_a.is_on:
                animations += [bulb_a.turn_off(), Transform(input_a_line, input_a_line.copy().set_stroke(WHITE, 3))]

            if b_state and not bulb_b.is_on:
                animations += [bulb_b.turn_on(), Transform(input_b_line, input_b_line.copy().set_stroke(YELLOW, 5))]
            elif not b_state and bulb_b.is_on:
                animations += [bulb_b.turn_off(), Transform(input_b_line, input_b_line.copy().set_stroke(WHITE, 3))]

            if and_state and not intermediate_bulb.is_on:
                animations.append(intermediate_bulb.turn_on())
                animations.append(AnimationGroup(
                    Transform(intermediate_line_left, intermediate_line_left.copy().set_stroke(YELLOW, 5)),
                    Transform(intermediate_line_right, intermediate_line_right.copy().set_stroke(YELLOW, 5)),
                    lag_ratio=0
                ))
            elif not and_state and intermediate_bulb.is_on:
                animations.append(intermediate_bulb.turn_off())
                animations.append(AnimationGroup(
                    Transform(intermediate_line_left, intermediate_line_left.copy().set_stroke(WHITE, 3)),
                    Transform(intermediate_line_right, intermediate_line_right.copy().set_stroke(WHITE, 3)),
                    lag_ratio=0
                ))

            if nand_state and not output_bulb.is_on:
                animations.append(output_bulb.turn_on())
                animations.append(Transform(output_line, output_line.copy().set_stroke(GREEN, 5)))
            elif not nand_state and output_bulb.is_on:
                animations.append(output_bulb.turn_off())
                animations.append(Transform(output_line, output_line.copy().set_stroke(WHITE, 3)))

            if animations:
                self.play(*animations, run_time=0.8)
            self.wait(1.8)

        self.play(FadeOut(highlight_rect), run_time=0.5)
        self.wait(3)


class Bulb(VMobject):
    """A class to represent a realistic-looking light bulb."""
    
    def __init__(self, radius=0.3, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.is_on = False
        self.create_bulb()
        
    def create_bulb(self):
        # Create the glass bulb part (circle)
        self.glass = Circle(radius=self.radius)
        self.glass.set_stroke(color=WHITE, width=2)
        self.glass.set_fill(color=DARK_GREY, opacity=0.2)
        
        # Create the base of the bulb
        self.base = Rectangle(
            height=self.radius * 0.6,
            width=self.radius * 0.5,
        )
        self.base.set_fill(color=LIGHT_GREY, opacity=1)
        self.base.set_stroke(color=GREY, width=1)
        self.base.next_to(self.glass, DOWN, buff=0)
        
        # Create the screw part of the base
        self.screw = Rectangle(
            height=self.radius * 0.3,
            width=self.radius * 0.4,
        )
        self.screw.set_fill(color=GREY, opacity=1)
        self.screw.set_stroke(color=DARK_GREY, width=1)
        self.screw.next_to(self.base, DOWN, buff=0)
        
        # Create the filament
        self.filament = VMobject()
        filament_points = [
            np.array([-self.radius * 0.2, 0, 0]),
            np.array([-self.radius * 0.08, self.radius * 0.2, 0]),
            np.array([self.radius * 0.08, -self.radius * 0.2, 0]),
            np.array([self.radius * 0.2, 0, 0])
        ]
        self.filament.set_points_as_corners([
            filament_points[0],
            filament_points[1],
            filament_points[2],
            filament_points[3]
        ])
        self.filament.set_stroke(color=LIGHT_GREY, width=1.5)
        self.filament.move_to(self.glass.get_center())
        
        # Create outer glow (initially invisible)
        self.outer_glow = Circle(radius=self.radius * 1.3)
        self.outer_glow.set_fill(color=YELLOW, opacity=0)
        self.outer_glow.set_stroke(color=YELLOW, width=6, opacity=0)
        self.outer_glow.move_to(self.glass.get_center())
        
        # Add all parts to the bulb
        self.add(self.outer_glow, self.glass, self.base, self.screw, self.filament)
        
    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            return AnimationGroup(
                self.glass.animate.set_fill(color=YELLOW, opacity=0.6),
                self.outer_glow.animate.set_fill(color=YELLOW, opacity=0.2).set_stroke(opacity=0.15),
                self.filament.animate.set_stroke(color=YELLOW, width=2.5),
                run_time=0.5
            )
        return Animation(Mobject())
        
    def turn_off(self):
        if self.is_on:
            self.is_on = False
            return AnimationGroup(
                self.glass.animate.set_fill(color=DARK_GREY, opacity=0.2),
                self.outer_glow.animate.set_fill(opacity=0).set_stroke(opacity=0),
                self.filament.animate.set_stroke(color=LIGHT_GREY, width=1.5),
                run_time=0.4
            )
        return Animation(Mobject())


class ANDGateWithRealisticBulbs(Scene):
    def construct(self):

        self.camera.frame.shift(RIGHT*2.4 + UP).scale(0.956)

        # Create the AND gate symbol (exact IEEE standard symbol)
        left_line = Line(UP * 1.0, DOWN * 1.0, stroke_width=4)
        top_line = Line(UP * 1.0, UP * 1.0 + RIGHT * 1.0, stroke_width=4)
        bottom_line = Line(DOWN * 1.0, DOWN * 1.0 + RIGHT * 1.0, stroke_width=4)
        
        # Create the curved right side (perfect semicircle)
        arc = Arc(
            radius=1.0,
            start_angle=-PI/2,
            angle=PI,
            arc_center=RIGHT * 1.0,
            stroke_width=4
        )
        
        # Combine to form the perfect AND gate body
        and_gate_body = VGroup(left_line, top_line, bottom_line, arc)
        and_gate_body.set_stroke(WHITE, width=3)
        
        # Input lines - shortened and bulbs moved rightward
        input_a_line = Line(LEFT * 1.8 + UP*0.5, UP * 0.5, stroke_width=3)
        input_b_line = Line(LEFT * 1.8 + DOWN*0.5, DOWN * 0.5, stroke_width=3)
        input_a_line.set_stroke(WHITE, width=3)
        input_b_line.set_stroke(WHITE, width=3)
        
        # Output line - connecting to output bulb (extended to connect properly)
        output_line = Line(RIGHT * 2.0, RIGHT * 3.2, stroke_width=3)
        output_line.set_stroke(WHITE, width=3)
        
        # Create realistic input and output bulbs
        bulb_a = Bulb(radius=0.25)
        bulb_b = Bulb(radius=0.25)
        output_bulb = Bulb(radius=0.25)
        
        # Position and rotate bulbs - moved rightward by 1.0 unit
        # Input bulbs rotated 90 degrees to align horizontally with input lines
        bulb_a.rotate(PI/2)  # Rotate 90 degrees
        bulb_b.rotate(PI/2)  # Rotate 90 degrees
        bulb_a.move_to(LEFT * 2.2 + UP * 0.5)
        bulb_b.move_to(LEFT * 2.2 + DOWN * 0.5)
        
        # Output bulb rotated 90 degrees to align horizontally with output line
        output_bulb.rotate(-PI/2)  # Rotate -90 degrees (opposite direction)
        output_bulb.move_to(RIGHT * 3.6)
        
        # Input labels positioned better
        input_a_label = Text("A", font_size=24, color=WHITE).next_to(bulb_a, LEFT, buff=0.3)
        input_b_label = Text("B", font_size=24, color=WHITE).next_to(bulb_b, LEFT, buff=0.3)
        output_label = Text("Y", font_size=24, color=WHITE).next_to(output_bulb, RIGHT, buff=0.3)
        
        # Truth table positioned on the right - moved further right and scaled up
        truth_table_title = Text("Truth Table", font_size=24, color=WHITE)
        truth_table_title.to_corner(UR).shift(LEFT * 0.5 + DOWN * 0.5)  # Moved more to the right
        
        table_data = [
            ["A", "B", "Y"],
            ["0", "0", "0"],
            ["0", "1", "0"],
            ["1", "0", "0"],
            ["1", "1", "1"]
        ]
        
        # Create truth table with proper alignment - scaled up and moved more right
        table_group = VGroup()
        table_center_x = 6.6  # Moved further right
        row_height = 0.54  # Increased spacing for larger scale
        
        table_group.shift(DOWN*0.3)

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                cell_text = Text(cell, font_size=22, color=WHITE)  # Increased font size
                # Center each column properly
                cell_x = table_center_x + (j - 1) * 0.67  # Increased column spacing
                cell_y = 1.5 - i * row_height
                cell_text.move_to(RIGHT * cell_x + UP * cell_y)
                row_group.add(cell_text)
            table_group.add(row_group)
        
        # Scale up the entire table group
        table_group.scale(1.27)
        

        # Gate name
        gate_name = Text("AND gate", font_size=50, color=WHITE, weight=BOLD).move_to(UP * 1.8).shift(UP*1.3)
        
        # Initial setup animations
        self.play(ShowCreation(and_gate_body), run_time=2)
        self.play(
            ShowCreation(input_a_line),
            ShowCreation(input_b_line),
            ShowCreation(output_line),
            run_time=1.5
        )
        
        self.play(
            Write(input_a_label),
            Write(input_b_label),
            Write(output_label),
            Write(gate_name),
            run_time=1
        )
        
        self.play(
            FadeIn(bulb_a),
            FadeIn(bulb_b),
            FadeIn(output_bulb),
            run_time=1
        )


        truth_table_title.next_to(table_group, UP, buff=0.77).scale(1.3)

        # Show truth table
        self.play(Write(truth_table_title), run_time=1)
        self.play(Write(table_group), run_time=2)
        
        self.wait(1)
        
        # Create a single yellow highlight rectangle that will move between rows
        highlight_rect = Rectangle(
            width=1.8 * 1.35, height=0.45 * 1.35,  # Scaled to match table
            fill_color=TEAL_B, fill_opacity=0.05,
            stroke_color=TEAL_B, stroke_width=7
        )
        # Position it at the first data row initially
        highlight_rect.move_to(table_group[1])
        
        # Show the highlight rectangle
        self.play(FadeIn(highlight_rect), run_time=0.3)
        
        # Demonstrate all combinations with bulbs
        combinations = [
            (False, False, False),  # 0, 0 -> 0
            (False, True, False),   # 0, 1 -> 0
            (True, False, False),   # 1, 0 -> 0
            (True, True, True)      # 1, 1 -> 1
        ]

        j = 2
        
        for i, (a_state, b_state, output_state) in enumerate(combinations):
            # Move highlight rectangle to current row (skip if it's already at the first row)
            if i > 0:
                new_y = 1.5 - (i + 1) * row_height
                self.play(
                    highlight_rect.animate.move_to(table_group[j]),
                    run_time=0.9
                )

                j += 1
            
            # Prepare animations list
            animations = []
            
            # Update input A bulb and line
            if a_state and not bulb_a.is_on:
                animations.append(bulb_a.turn_on())
                new_input_a_line = input_a_line.copy().set_stroke(YELLOW, width=5)
                animations.append(Transform(input_a_line, new_input_a_line))
            elif not a_state and bulb_a.is_on:
                animations.append(bulb_a.turn_off())
                new_input_a_line = input_a_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(input_a_line, new_input_a_line))
            
            # Update input B bulb and line
            if b_state and not bulb_b.is_on:
                animations.append(bulb_b.turn_on())
                new_input_b_line = input_b_line.copy().set_stroke(YELLOW, width=5)
                animations.append(Transform(input_b_line, new_input_b_line))
            elif not b_state and bulb_b.is_on:
                animations.append(bulb_b.turn_off())
                new_input_b_line = input_b_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(input_b_line, new_input_b_line))
            
            # Update output bulb and line only (gate body stays WHITE)
            if output_state and not output_bulb.is_on:
                animations.append(output_bulb.turn_on())
                new_output_line = output_line.copy().set_stroke(GREEN, width=5)
                animations.append(Transform(output_line, new_output_line))
            elif not output_state and output_bulb.is_on:
                animations.append(output_bulb.turn_off())
                new_output_line = output_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(output_line, new_output_line))
            
            # Play all animations
            if animations:
                self.play(*animations, run_time=0.8)
            
            self.wait(1.5)
        
        # Final cleanup
        self.play(FadeOut(highlight_rect), run_time=0.5)

        self.wait(3)


class NOTGateWithRealisticBulbs(Scene):

    def construct(self):

        self.camera.frame.shift(RIGHT*1.8 + UP*0.845).scale(0.92)

        # Create the NOT gate symbol (triangle with circle)
        # Triangle body
        triangle_points = [
            LEFT * 1.0,
            RIGHT * 1.0 + UP * 0.0,
            LEFT * 1.0 + UP * 1.0,
            LEFT * 1.0 + DOWN * 1.0,
            LEFT * 1.0
        ]
        
        triangle = Polygon(
            LEFT * 1.0 + UP * 0.8,
            LEFT * 1.0 + DOWN * 0.8,
            RIGHT * 0.8,
            stroke_width=3
        )
        triangle.set_stroke(WHITE, width=3)
        triangle.set_fill(opacity=0)
        
        # Small circle (bubble) at the output
        bubble = Circle(radius=0.15)
        bubble.set_stroke(WHITE, width=3)
        bubble.set_fill(opacity=0)
        bubble.next_to(triangle, RIGHT, buff=0)
        
        # Combine triangle and bubble
        not_gate_body = VGroup(triangle, bubble)
        
        # Input line - single input for NOT gate
        input_line = Line(LEFT * 2.5, LEFT * 1.0, stroke_width=3)
        input_line.set_stroke(WHITE, width=3)
        
        # Output line - connecting from bubble to output bulb
        output_line = Line(RIGHT * 1.1, RIGHT * 2.8, stroke_width=3)
        output_line.set_stroke(WHITE, width=3)
        
        # Create realistic input and output bulbs
        input_bulb = Bulb(radius=0.25)
        output_bulb = Bulb(radius=0.25)
        
        # Position and rotate bulbs
        # Input bulb rotated 90 degrees to align horizontally with input line
        input_bulb.rotate(PI/2)
        input_bulb.move_to(LEFT * 2.9)
        
        # Output bulb rotated 90 degrees to align horizontally with output line
        output_bulb.rotate(-PI/2)
        output_bulb.move_to(RIGHT * 3.2)
        
        # Labels
        input_label = Text("A", font_size=24, color=WHITE).next_to(input_bulb, LEFT, buff=0.3)
        output_label = Text("Y", font_size=24, color=WHITE).next_to(output_bulb, RIGHT, buff=0.3)
        
        # Truth table positioned on the right - NOT gate truth table
        truth_table_title = Text("Truth Table", font_size=21, color=WHITE)
        
        # NOT gate truth table: output is opposite of input
        table_data = [
            ["A", "Y"],
            ["0", "1"],
            ["1", "0"]
        ]
        
        # Create truth table with proper alignment
        table_group = VGroup()
        table_center_x = 5.5
        row_height = 0.6
        
        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                cell_text = Text(cell, font_size=26, color=WHITE)
                # Center each column properly (only 2 columns for NOT gate)
                cell_x = table_center_x + (j - 0.5) * 0.8
                cell_y = 1.5 - i * row_height
                cell_text.move_to(RIGHT * cell_x + UP * cell_y)
                row_group.add(cell_text)
            table_group.add(row_group)
        
        # Scale up the entire table group
        table_group.scale(1.4).shift(RIGHT*0.75 + DOWN*0.5)
        
        # Position truth table title
        truth_table_title.next_to(table_group, UP, buff=0.8).scale(1.4)

        # Gate name
        gate_name = Text("NOT gate", font_size=50, color=WHITE, weight=BOLD).move_to(UP * 2.5)
        
        # Initial setup animations
        self.play(ShowCreation(not_gate_body), run_time=2)
        self.play(
            ShowCreation(input_line),
            ShowCreation(output_line),
            run_time=1.5
        )
        
        self.play(
            Write(input_label),
            Write(output_label),
            Write(gate_name),
            run_time=1
        )
        
        self.play(
            FadeIn(input_bulb),
            FadeIn(output_bulb),
            run_time=1
        )

        # Show truth table
        self.play(Write(truth_table_title), run_time=1)
        self.play(Write(table_group), run_time=2)
        
        self.wait(1)
        
        # Create a highlight rectangle for the truth table
        highlight_rect = Rectangle(
            width=1.6 * 1.4, height=0.5 * 1.4,
            fill_color=TEAL_B, fill_opacity=0.05,
            stroke_color=TEAL_B, stroke_width=7
        )
        # Position it at the first data row initially
        highlight_rect.move_to(table_group[1])
        
        # Show the highlight rectangle
        self.play(FadeIn(highlight_rect), run_time=0.3)
        
        # Demonstrate NOT gate logic: output is opposite of input
        combinations = [
            (False, True),   # 0 -> 1 (input off, output on)
            (True, False)    # 1 -> 0 (input on, output off)
        ]

        for i, (input_state, output_state) in enumerate(combinations):
            # Move highlight rectangle to current row (skip if it's already at the first row)
            if i > 0:
                self.play(
                    highlight_rect.animate.move_to(table_group[2]),
                    run_time=0.9
                )
            
            # Prepare animations list
            animations = []
            
            # Update input bulb and line
            if input_state and not input_bulb.is_on:
                animations.append(input_bulb.turn_on())
                new_input_line = input_line.copy().set_stroke(YELLOW, width=5)
                animations.append(Transform(input_line, new_input_line))
            elif not input_state and input_bulb.is_on:
                animations.append(input_bulb.turn_off())
                new_input_line = input_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(input_line, new_input_line))
            
            # Update output bulb and line (opposite of input)
            if output_state and not output_bulb.is_on:
                animations.append(output_bulb.turn_on())
                new_output_line = output_line.copy().set_stroke(GREEN, width=5)
                animations.append(Transform(output_line, new_output_line))
            elif not output_state and output_bulb.is_on:
                animations.append(output_bulb.turn_off())
                new_output_line = output_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(output_line, new_output_line))
            
            # Play all animations
            if animations:
                self.play(*animations, run_time=0.8)
            else:
                # For the first state (0->1), we need to show the initial state
                # Input is off, output should be on
                if not input_state and output_state:
                    animations.append(output_bulb.turn_on())
                    new_output_line = output_line.copy().set_stroke(GREEN, width=5)
                    animations.append(Transform(output_line, new_output_line))
                    self.play(*animations, run_time=0.8)
            
            self.wait(2)
        
        # Final cleanup
        self.play(FadeOut(highlight_rect), run_time=0.5)

        self.wait(3)

class ORGateWithRealisticBulbs(Scene):

    def construct(self):

        self.camera.frame.shift(RIGHT*2.4 + UP).scale(0.956)

        # Create the OR gate symbol with correct structure:
        # Left side: Input arc where both inputs connect
        # Middle: Two curved sword-like shapes (top and bottom)
        # Right side: Pointed tip where output emerges
        
        # Input arc (leftmost, where inputs A and B connect) - much straighter
        input_arc = Arc(
            radius=1.6,  # Larger radius makes it straighter
            start_angle=-PI/4,  # Smaller angle range
            angle=PI/2,         # Smaller angle range
            arc_center=np.array([-1.6, 0, 0]),
            stroke_width=4
        )
        
        # Calculate the actual endpoints of the arc
        arc_top_point = np.array([-1.6, 0, 0]) + 1.6 * np.array([np.cos(PI/4), np.sin(PI/4), 0])
        arc_bottom_point = np.array([-1.6, 0, 0]) + 1.6 * np.array([np.cos(-PI/4), np.sin(-PI/4), 0])
        
        # Upper curved sword-like shape - curves outward then inward (mirrored)
        upper_sword = VMobject()
        upper_sword.set_points_smoothly([
            arc_top_point,              # Top endpoint of the arc
            np.array([0.6, 0.8, 0]),    # Control point - outward
            np.array([2.0, 0, 0])       # Output tip
        ])
        
        # Lower curved sword-like shape - curves outward then inward (mirrored)
        lower_sword = VMobject()
        lower_sword.set_points_smoothly([
            arc_bottom_point,           # Bottom endpoint of the arc
            np.array([0.6, -0.8, 0]),   # Control point - outward
            np.array([2.0, 0, 0])       # Output tip
        ])
        
        # Combine to form the OR gate body
        or_gate_body = VGroup(input_arc, upper_sword, lower_sword).shift(LEFT*0.34)
        or_gate_body.set_stroke(WHITE, width=3)
        
        # Input lines - connecting to the input arc
        input_a_line = Line(LEFT * 1.8 + UP*0.5, LEFT * 0.43 + UP*0.5, stroke_width=3)
        input_b_line = Line(LEFT * 1.8 + DOWN*0.5, LEFT * 0.43 + DOWN*0.5, stroke_width=3)
        input_a_line.set_stroke(WHITE, width=3)
        input_b_line.set_stroke(WHITE, width=3)
        
        # Output line - connecting from the pointed tip
        output_line = Line(RIGHT * 2.0, RIGHT * 3.2, stroke_width=3).shift(LEFT*0.34)
        output_line.set_stroke(WHITE, width=3)
        
        # Create realistic input and output bulbs
        bulb_a = Bulb(radius=0.25)
        bulb_b = Bulb(radius=0.25)
        output_bulb = Bulb(radius=0.25)
        
        # Position and rotate bulbs
        bulb_a.rotate(PI/2)  # Rotate 90 degrees
        bulb_b.rotate(PI/2)  # Rotate 90 degrees
        bulb_a.move_to(LEFT * 2.2 + UP * 0.5)
        bulb_b.move_to(LEFT * 2.2 + DOWN * 0.5)
        
        # Output bulb rotated 90 degrees to align horizontally with output line
        output_bulb.rotate(-PI/2)  # Rotate -90 degrees (opposite direction)
        output_bulb.move_to(RIGHT * 3.6).shift(LEFT*0.34)
        
        # Input labels positioned better
        input_a_label = Text("A", font_size=24, color=WHITE).next_to(bulb_a, LEFT, buff=0.3)
        input_b_label = Text("B", font_size=24, color=WHITE).next_to(bulb_b, LEFT, buff=0.3)
        output_label = Text("Y", font_size=24, color=WHITE).next_to(output_bulb, RIGHT, buff=0.3)
        
        # Truth table positioned on the right - OR gate truth table
        truth_table_title = Text("Truth Table", font_size=24, color=WHITE)
        truth_table_title.to_corner(UR).shift(LEFT * 0.5 + DOWN * 0.5)
        
        # OR gate truth table: output is 1 when at least one input is 1
        table_data = [
            ["A", "B", "Y"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "1"]
        ]
        
        # Create truth table with proper alignment
        table_group = VGroup()
        table_center_x = 6.6
        row_height = 0.54
        
        table_group.shift(DOWN*0.3)

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                cell_text = Text(cell, font_size=22, color=WHITE)
                cell_x = table_center_x + (j - 1) * 0.67
                cell_y = 1.5 - i * row_height
                cell_text.move_to(RIGHT * cell_x + UP * cell_y)
                row_group.add(cell_text)
            table_group.add(row_group)
        
        # Scale up the entire table group
        table_group.scale(1.27)
        
        # Gate name - corrected to OR gate
        gate_name = Text("OR Gate", font_size=50, color=WHITE, weight=BOLD).move_to(UP * 1.8).shift(UP*1.3)
        
        # Initial setup animations
        self.play(ShowCreation(or_gate_body), run_time=2)
        self.play(
            ShowCreation(input_a_line),
            ShowCreation(input_b_line),
            ShowCreation(output_line),
            run_time=1.5
        )
        
        self.play(
            Write(input_a_label),
            Write(input_b_label),
            Write(output_label),
            Write(gate_name),
            run_time=1
        )
        
        self.play(
            FadeIn(bulb_a),
            FadeIn(bulb_b),
            FadeIn(output_bulb),
            run_time=1
        )

        truth_table_title.next_to(table_group, UP, buff=0.77).scale(1.3)

        # Show truth table
        self.play(Write(truth_table_title), run_time=1)
        self.play(Write(table_group), run_time=2)
        
        self.wait(1)
        
        # Create a single highlight rectangle that will move between rows
        highlight_rect = Rectangle(
            width=1.8 * 1.35, height=0.45 * 1.35,
            fill_color=TEAL_B, fill_opacity=0.05,
            stroke_color=TEAL_B, stroke_width=7
        )
        # Position it at the first data row initially
        highlight_rect.move_to(table_group[1])
        
        # Show the highlight rectangle
        self.play(FadeIn(highlight_rect), run_time=0.3)
        
        # Demonstrate all combinations with bulbs - OR gate logic
        combinations = [
            (False, False, False),  # 0, 0 -> 0
            (False, True, True),    # 0, 1 -> 1
            (True, False, True),    # 1, 0 -> 1
            (True, True, True)      # 1, 1 -> 1
        ]

        j = 2
        
        for i, (a_state, b_state, output_state) in enumerate(combinations):
            # Move highlight rectangle to current row (skip if it's already at the first row)
            if i > 0:
                new_y = 1.5 - (i + 1) * row_height
                self.play(
                    highlight_rect.animate.move_to(table_group[j]),
                    run_time=0.9
                )

                j += 1
            
            # Prepare animations list
            animations = []
            
            # Update input A bulb and line
            if a_state and not bulb_a.is_on:
                animations.append(bulb_a.turn_on())
                new_input_a_line = input_a_line.copy().set_stroke(YELLOW, width=5)
                animations.append(Transform(input_a_line, new_input_a_line))
            elif not a_state and bulb_a.is_on:
                animations.append(bulb_a.turn_off())
                new_input_a_line = input_a_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(input_a_line, new_input_a_line))
            
            # Update input B bulb and line
            if b_state and not bulb_b.is_on:
                animations.append(bulb_b.turn_on())
                new_input_b_line = input_b_line.copy().set_stroke(YELLOW, width=5)
                animations.append(Transform(input_b_line, new_input_b_line))
            elif not b_state and bulb_b.is_on:
                animations.append(bulb_b.turn_off())
                new_input_b_line = input_b_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(input_b_line, new_input_b_line))
            
            # Update output bulb and line
            if output_state and not output_bulb.is_on:
                animations.append(output_bulb.turn_on())
                new_output_line = output_line.copy().set_stroke(GREEN, width=5)
                animations.append(Transform(output_line, new_output_line))
            elif not output_state and output_bulb.is_on:
                animations.append(output_bulb.turn_off())
                new_output_line = output_line.copy().set_stroke(WHITE, width=3)
                animations.append(Transform(output_line, new_output_line))
            
            # Play all animations
            if animations:
                self.play(*animations, run_time=0.8)
            
            self.wait(1.5)
        
        # Final cleanup
        self.play(FadeOut(highlight_rect), run_time=0.5)

        self.wait(3)


class NORGateWithComponents(Scene):
    def construct(self):

        self.camera.frame.scale(0.77).shift(DOWN*1.6)

        # Create the OR gate symbol with correct structure
        # Input arc (leftmost, where inputs A and B connect) - much straighter
        input_arc = Arc(
            radius=1.6,  # Larger radius makes it straighter
            start_angle=-PI/4,  # Smaller angle range
            angle=PI/2,         # Smaller angle range
            arc_center=np.array([-1.6, 0, 0]),
            stroke_width=3
        )
        
        # Calculate the actual endpoints of the arc
        arc_top_point = np.array([-1.6, 0, 0]) + 1.6 * np.array([np.cos(PI/4), np.sin(PI/4), 0])
        arc_bottom_point = np.array([-1.6, 0, 0]) + 1.6 * np.array([np.cos(-PI/4), np.sin(-PI/4), 0])
        
        # Upper curved sword-like shape - curves outward then inward
        upper_sword = VMobject()
        upper_sword.set_points_smoothly([
            arc_top_point,              # Top endpoint of the arc
            np.array([0.6, 0.8, 0]),    # Control point - outward
            np.array([2.0, 0, 0])       # Output tip
        ])
        
        # Lower curved sword-like shape - curves outward then inward
        lower_sword = VMobject()
        lower_sword.set_points_smoothly([
            arc_bottom_point,           # Bottom endpoint of the arc
            np.array([0.6, -0.8, 0]),   # Control point - outward
            np.array([2.0, 0, 0])       # Output tip
        ])
        
        # Combine to form the OR gate body
        or_gate_body = VGroup(input_arc, upper_sword, lower_sword).set_stroke(WHITE, width=3).move_to(LEFT * 2).scale(0.5)

        # NOT gate (triangle + bubble)
        triangle = Polygon(LEFT * 0.5 + UP * 0.4, LEFT * 0.5 + DOWN * 0.4, RIGHT * 0.4).set_stroke(WHITE, width=3).set_fill(opacity=0).move_to(RIGHT * 1.5)
        
        bubble_radius = 0.08
        bubble_center = RIGHT * (1.56 + 0.4 + bubble_radius)
        bubble = Circle(radius=bubble_radius).set_stroke(WHITE, width=3).set_fill(opacity=0).move_to(bubble_center)
        not_gate_body = VGroup(triangle, bubble)

        # Input lines
        input_a_line = Line(LEFT * 3.5 + UP * 0.3, LEFT * 2.45 + UP * 0.3, stroke_width=3).set_stroke(WHITE, 3)
        input_b_line = Line(LEFT * 3.5 + DOWN * 0.3, LEFT * 2.45 + DOWN * 0.3, stroke_width=3).set_stroke(WHITE, 3)

        # Create bulbs
        bulb_a = Bulb(radius=0.2)
        bulb_b = Bulb(radius=0.2)
        intermediate_bulb = Bulb(radius=0.15)
        output_bulb = Bulb(radius=0.2)

        # Position and rotate bulbs
        bulb_a.rotate(PI / 2)
        bulb_b.rotate(PI / 2)
        intermediate_bulb.rotate(-PI / 2)
        output_bulb.rotate(-PI / 2)

        bulb_a.move_to(LEFT * 3.8 + UP * 0.3)
        bulb_b.move_to(LEFT * 3.8 + DOWN * 0.3)
        intermediate_bulb.move_to(LEFT * 0.15)
        output_bulb.move_to(RIGHT * 3.8)

        # Intermediate and output lines
        intermediate_line_left = Line(LEFT * 1.4, intermediate_bulb.get_left(), stroke_width=3).set_stroke(WHITE, 3)
        intermediate_line_right = Line(intermediate_bulb.get_right(), RIGHT * 1.06, stroke_width=3).set_stroke(WHITE, 3)
        intermediate_line = VGroup(intermediate_line_left, intermediate_line_right)

        output_line = Line(bubble.get_right(), RIGHT * 3.5, stroke_width=3).set_stroke(WHITE, 3)

        # Labels
        labels = VGroup(
            Text("A", font_size=20, color=WHITE).next_to(bulb_a, LEFT, buff=0.2),
            Text("B", font_size=20, color=WHITE).next_to(bulb_b, LEFT, buff=0.2),
            Text("OR", font_size=14, color=WHITE).next_to(intermediate_bulb, UP, buff=0.2),
            Text("Y", font_size=20, color=WHITE).next_to(output_bulb, RIGHT, buff=0.2),
            Text("OR", font_size=18, color=WHITE).next_to(or_gate_body, DOWN, buff=0.3),
            Text("NOT", font_size=18, color=WHITE).next_to(not_gate_body, DOWN, buff=0.3)
        )

        # NOR Truth Table
        truth_table_title = Text("NOR Truth Table", font_size=20, color=WHITE)
        table_data = [["A", "B", "OR", "Y"], ["0", "0", "0", "1"], ["0", "1", "1", "0"], ["1", "0", "1", "0"], ["1", "1", "1", "0"]]
        table_group = VGroup()

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                t = Text(cell, font_size=16, color=WHITE)
                t.move_to(RIGHT * ((j - 1.5) * 0.8) + UP * (-2.5 - i * 0.4))
                row_group.add(t)
            table_group.add(row_group)

        truth_table_title.next_to(table_group, UP, buff=0.3)

        # Animation sequence
        self.play(ShowCreation(or_gate_body), ShowCreation(not_gate_body), run_time=2)

        self.play(Write(labels[4]), Write(labels[5]), run_time=1)
        self.play(
            ShowCreation(input_a_line),
            ShowCreation(input_b_line),
            ShowCreation(intermediate_line_left),
            ShowCreation(intermediate_line_right),
            ShowCreation(output_line),
            run_time=1.5
        )
        self.play(FadeIn(bulb_a), FadeIn(bulb_b), FadeIn(intermediate_bulb), FadeIn(output_bulb), run_time=1)
        self.play(*[Write(label) for label in labels[:4]], run_time=1)
        self.play(Write(truth_table_title), Write(table_group), run_time=2)

        highlight_rect = Rectangle(width=2.6, height=0.32, fill_color=TEAL_B, fill_opacity=0.05, stroke_color=TEAL_B, stroke_width=3).move_to(table_group[1]).scale(1.1)
        self.play(FadeIn(highlight_rect), run_time=0.3)

        # NOR gate combinations: OR output is inverted by NOT gate
        combinations = [(False, False, False, True), (False, True, True, False), (True, False, True, False), (True, True, True, False)]

        for i, (a_state, b_state, or_state, nor_state) in enumerate(combinations):
            if i > 0:
                self.play(highlight_rect.animate.move_to(table_group[i + 1]), run_time=0.7)

            animations = []

            # Update input A
            if a_state and not bulb_a.is_on:
                animations += [bulb_a.turn_on(), Transform(input_a_line, input_a_line.copy().set_stroke(YELLOW, 5))]
            elif not a_state and bulb_a.is_on:
                animations += [bulb_a.turn_off(), Transform(input_a_line, input_a_line.copy().set_stroke(WHITE, 3))]

            # Update input B
            if b_state and not bulb_b.is_on:
                animations += [bulb_b.turn_on(), Transform(input_b_line, input_b_line.copy().set_stroke(YELLOW, 5))]
            elif not b_state and bulb_b.is_on:
                animations += [bulb_b.turn_off(), Transform(input_b_line, input_b_line.copy().set_stroke(WHITE, 3))]

            # Update OR intermediate output
            if or_state and not intermediate_bulb.is_on:
                animations.append(intermediate_bulb.turn_on())
                animations.append(AnimationGroup(
                    Transform(intermediate_line_left, intermediate_line_left.copy().set_stroke(YELLOW, 5)),
                    Transform(intermediate_line_right, intermediate_line_right.copy().set_stroke(YELLOW, 5)),
                    lag_ratio=0
                ))
            elif not or_state and intermediate_bulb.is_on:
                animations.append(intermediate_bulb.turn_off())
                animations.append(AnimationGroup(
                    Transform(intermediate_line_left, intermediate_line_left.copy().set_stroke(WHITE, 3)),
                    Transform(intermediate_line_right, intermediate_line_right.copy().set_stroke(WHITE, 3)),
                    lag_ratio=0
                ))

            # Update NOR final output
            if nor_state and not output_bulb.is_on:
                animations.append(output_bulb.turn_on())
                animations.append(Transform(output_line, output_line.copy().set_stroke(GREEN, 5)))
            elif not nor_state and output_bulb.is_on:
                animations.append(output_bulb.turn_off())
                animations.append(Transform(output_line, output_line.copy().set_stroke(WHITE, 3)))

            if animations:
                self.play(*animations, run_time=0.8)
            self.wait(1.8)

        self.play(FadeOut(highlight_rect), run_time=0.5)
        self.wait(2)



        # Create clean NOR gate symbol (OR gate with NOT bubble at output)
        # OR gate part
        clean_input_arc = Arc(
            radius=1.6,
            start_angle=-PI/4,
            angle=PI/2,
            arc_center=np.array([-1.6, 0, 0]),
            stroke_width=4
        )
        
        clean_arc_top = np.array([-1.6, 0, 0]) + 1.6 * np.array([np.cos(PI/4), np.sin(PI/4), 0])
        clean_arc_bottom = np.array([-1.6, 0, 0]) + 1.6 * np.array([np.cos(-PI/4), np.sin(-PI/4), 0])
        
        clean_upper_sword = VMobject()
        clean_upper_sword.set_points_smoothly([
            clean_arc_top,
            np.array([0.6, 0.8, 0]),
            np.array([2.0, 0, 0])
        ])
        
        clean_lower_sword = VMobject()
        clean_lower_sword.set_points_smoothly([
            clean_arc_bottom,
            np.array([0.6, -0.8, 0]),
            np.array([2.0, 0, 0])
        ])
        
        # NOT bubble at the tip
        bubble_radius_clean = 0.12
        bubble_center_clean = np.array([2.0 + bubble_radius_clean, 0, 0])
        clean_bubble = Circle(radius=bubble_radius_clean).set_stroke(WHITE, width=4).set_fill(opacity=0).move_to(bubble_center_clean)
        
        # Complete NOR gate symbol
        nor_gate_symbol = VGroup(clean_input_arc, clean_upper_sword, clean_lower_sword, clean_bubble).set_stroke(WHITE, width=4).move_to(ORIGIN).scale(0.8).shift(DOWN*1.5)

        # Input and output lines for the symbol
        symbol_input_a = Line(LEFT * 2.5 + UP * 0.5, LEFT * 0.8 + UP * 0.5, stroke_width=4).set_stroke(WHITE, 4).shift(DOWN*1.5)
        symbol_input_b = Line(LEFT * 2.5 + DOWN * 0.5, LEFT * 0.8 + DOWN * 0.5, stroke_width=4).set_stroke(WHITE, 4).shift(DOWN*1.5)
        symbol_output = Line(RIGHT * 1.1, RIGHT * 2.5, stroke_width=4).set_stroke(WHITE, 4).shift(DOWN*1.5)

        # Labels for the symbol
        symbol_labels = VGroup(
            Text("A", font_size=24, color=WHITE).next_to(symbol_input_a, LEFT, buff=0.3),
            Text("B", font_size=24, color=WHITE).next_to(symbol_input_b, LEFT, buff=0.3),
            Text("Y", font_size=24, color=WHITE).next_to(symbol_output, RIGHT, buff=0.3),
            Text("NOR", font_size=44, color=WHITE).next_to(nor_gate_symbol, DOWN, buff=0.7)
        )

        # Fade out truth table and all components
        self.play(
            FadeOut(truth_table_title),
            FadeOut(table_group),
            FadeOut(or_gate_body),
            FadeOut(not_gate_body),
            FadeOut(input_a_line),
            FadeOut(input_b_line),
            FadeOut(intermediate_line_left),
            FadeOut(intermediate_line_right),
            FadeOut(output_line),
            FadeOut(bulb_a),
            FadeOut(bulb_b),
            FadeOut(intermediate_bulb),
            FadeOut(output_bulb),
            FadeOut(labels),

            run_time=0.77
        )

        self.play(
            ShowCreation(nor_gate_symbol),
            ShowCreation(symbol_input_a),
            ShowCreation(symbol_input_b),
            ShowCreation(symbol_output),
        )



        self.play(Write(symbol_labels), run_time=1.5)
        self.wait(3)
