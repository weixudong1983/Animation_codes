from manimlib import *
import numpy as np

GRAY = GREY
LIGHT_GREY = GREY_A
DARK_GREY = "#2E2E2E"
YELLOW  = "#00FF00"
GREEN  = "#00FF00"

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
