from manimlib import *
import numpy as np

DARK_GREY = "#2E2E2E"
LIGHT_GREY = "#A9A9A9"

class Bulb(VMobject):
    """A class to represent a realistic-looking light bulb."""
    
    def __init__(self, radius=0.5, **kwargs):
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
            height=self.radius * 0.8,
            width=self.radius * 0.7,
        )
        self.base.set_fill(color=LIGHT_GREY, opacity=1)
        self.base.set_stroke(color=GREY, width=2)
        self.base.next_to(self.glass, DOWN, buff=0)
        
        # Create the screw part of the base
        self.screw = Rectangle(
            height=self.radius * 0.4,
            width=self.radius * 0.5,
        )
        self.screw.set_fill(color=GREY, opacity=1)
        self.screw.set_stroke(color=DARK_GREY, width=1)
        self.screw.next_to(self.base, DOWN, buff=0)
        
        # Create the filament - Fixed to use proper numpy arrays for points
        self.filament = VMobject()
        filament_points = [
            np.array([-self.radius * 0.25, 0, 0]),
            np.array([-self.radius * 0.1, self.radius * 0.3, 0]),
            np.array([self.radius * 0.1, -self.radius * 0.3, 0]),
            np.array([self.radius * 0.25, 0, 0])
        ]
        self.filament.set_points_as_corners([
            filament_points[0],
            filament_points[1],
            filament_points[2],
            filament_points[3]
        ])
        self.filament.set_stroke(color=LIGHT_GREY, width=2)
        self.filament.move_to(self.glass.get_center())
        
        # Create outer glow (initially invisible)
        self.outer_glow = Circle(radius=self.radius * 1.5)
        self.outer_glow.set_fill(color=YELLOW, opacity=0)
        self.outer_glow.set_stroke(color=YELLOW, width=10, opacity=0)
        self.outer_glow.move_to(self.glass.get_center())
        
        # Add all parts to the bulb
        self.add(self.glass, self.base, self.screw, self.filament, self.outer_glow)
        
    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            return AnimationGroup(
                self.glass.animate.set_fill(color=YELLOW, opacity=0.5),
                self.outer_glow.animate.set_fill(color=YELLOW, opacity=0.3).set_stroke(opacity=0.2),
                self.filament.animate.set_stroke(color=YELLOW, width=3),
                run_time=0.7
            )
        return Animation(Mobject())  # No-op animation if already on
        
    def turn_off(self):
        if self.is_on:
            self.is_on = False
            return AnimationGroup(
                self.glass.animate.set_fill(color=DARK_GREY, opacity=0.2),
                self.outer_glow.animate.set_fill(opacity=0).set_stroke(opacity=0),
                self.filament.animate.set_stroke(color=LIGHT_GREY, width=2),
                run_time=0.5
            )
        return Animation(Mobject())  # No-op animation if already off


class BulbSwitcherProblem(Scene):
    def construct(self):

        self.camera.frame.shift(UP*0.23).scale(0.9)
        # Create title
        title = Text("LeetCode Bulb Switcher Problem", font_size=40).set_color(GREEN)
        title.to_edge(UP).shift(DOWN*0.7)
        self.play(Write(title))
        
        # Create 5 bulbs in a row
        bulbs = VGroup()
        for i in range(6):
            bulb = Bulb()
            bulb.scale(0.8)
            bulbs.add(bulb)
        
        bulbs.arrange(RIGHT, buff=0.7)
        bulbs.shift(DOWN)
        
        # Add bulb numbers
        numbers = VGroup()
        for i, bulb in enumerate(bulbs):
            number = Text(str(i+1), font_size=24)
            number.next_to(bulb, DOWN, buff=0.5)
            numbers.add(number)
        
        self.play(
            FadeIn(bulbs),
            Write(numbers)
        )
        

        
        # First round - toggle every bulb (all on)
        round_text = Text("Round 1: Toggle every bulb", font_size=30)
        round_text.next_to(bulbs, UP, buff=1.0)
        self.play(Write(round_text))
        
        # Turn on all bulbs
        animations = []
        for bulb in bulbs:
            animations.append(bulb.turn_on())
        self.play(*animations)
        self.wait(1)
        
        # Second round - toggle every 2nd bulb
        self.play(
            FadeOut(round_text)
        )
        round_text = Text("Round 2: Toggle every 2nd bulb", font_size=30)
        round_text.next_to(bulbs, UP, buff=1.0)
        self.play(Write(round_text))
        
        # Toggle bulbs 2, 4
        animations = []
        for i, bulb in enumerate(bulbs):
            if (i + 1) % 2 == 0:  # Every 2nd bulb (index+1 is the bulb number)
                animations.append(bulb.turn_off())
        self.play(*animations)
        self.wait(1)
        
        # Third round - toggle every 3rd bulb
        self.play(
            FadeOut(round_text)
        )
        round_text = Text("Round 3: Toggle every 3rd bulb", font_size=30)
        round_text.next_to(bulbs, UP, buff=1.0)
        self.play(Write(round_text))
        
        # Toggle bulb 3
        animations = []
        for i, bulb in enumerate(bulbs):
            if (i + 1) % 3 == 0:  # Every 3rd bulb
                if bulb.is_on:
                    animations.append(bulb.turn_off())
                else:
                    animations.append(bulb.turn_on())
        self.play(*animations)
        self.wait(1)
        
        # Fourth round - toggle every 4th bulb
        self.play(
            FadeOut(round_text)
        )
        round_text = Text("Round 4: Toggle every 4th bulb", font_size=30)
        round_text.next_to(bulbs, UP, buff=1.0)
        self.play(Write(round_text))
        
        # Toggle bulb 4
        animations = []
        for i, bulb in enumerate(bulbs):
            if (i + 1) % 4 == 0:  # Every 4th bulb
                if bulb.is_on:
                    animations.append(bulb.turn_off())
                else:
                    animations.append(bulb.turn_on())
        self.play(*animations)
        self.wait(1)
        
        # Fifth round - toggle every 5th bulb
        self.play(
            FadeOut(round_text)
        )
        round_text = Text("Round 5: Toggle every 5th bulb", font_size=30)
        round_text.next_to(bulbs, UP, buff=1.0)
        self.play(Write(round_text))
        
        # Toggle bulb 5
        animations = []
        for i, bulb in enumerate(bulbs):
            if (i + 1) % 5 == 0:  # Every 5th bulb
                if bulb.is_on:
                    animations.append(bulb.turn_off())
                else:
                    animations.append(bulb.turn_on())
        self.play(*animations)
        self.wait(1)
        
        # Fifth round - toggle every 6th bulb
        self.play(
            FadeOut(round_text)
        )
        round_text = Text("Round 6: Toggle every 6th bulb", font_size=30)
        round_text.next_to(bulbs, UP, buff=1.0)
        self.play(Write(round_text))
        
        # Toggle bulb 6
        animations = []
        for i, bulb in enumerate(bulbs):
            if (i + 1) % 6 == 0:  # Every 6th bulb
                if bulb.is_on:
                    animations.append(bulb.turn_off())
                else:
                    animations.append(bulb.turn_on())
        self.play(*animations)
        self.wait(1)


        self.embed()

        # Final state explanation
        self.play(
            FadeOut(round_text),
           
        )
        
        final_text = Text(
            "Total bulbs Glowing: 2",
            font_size=28
        ).scale(1.28)
        final_text.move_to(round_text)
        self.play(Write(final_text))
        self.wait(2)




class First(Scene):
    def construct(self):
        # Create the main bulb
        bulb = Bulb(radius=0.7)
        bulb.scale(1.2)
        bulb.move_to(UP * 1.9)  # Move bulb up to avoid overlap

        self.add(bulb)


        Current = Text("Current:", font_size=64).next_to(bulb, DOWN, buff=1.2).shift(LEFT*1.3)


        off = Text("OFF", font_size=64).next_to(Current, RIGHT, buff=0.5)
        self.play(Write(off), Write(Current))
        self.wait(1)

        on = Text("ON", font_size=64).move_to(off)

        toggle = Text("TOGGLE = 1", font_size=54).next_to(Current, DOWN, buff=1).shift(RIGHT*1.1)
        
        
        self.play(
            bulb.turn_on(),
            ReplacementTransform(off, on), 
            Write(toggle)
            )
        
        self.wait(2)

        toggle1 = Text("TOGGLE = 2", font_size=54).next_to(Current, DOWN, buff=1).shift(RIGHT*1.1)
        
        off = Text("OFF", font_size=64).next_to(Current, RIGHT, buff=0.5)
        self.play(
            bulb.turn_off(),
            ReplacementTransform(on, off), 
            ReplacementTransform(toggle, toggle1 )
            )
        
        self.wait(2)

        toggle = Text("TOGGLE = 3", font_size=54).next_to(Current, DOWN, buff=1).shift(RIGHT*1.1)
        on = Text("ON", font_size=64).move_to(off)  
     
        
        self.play(
            bulb.turn_on(),
            ReplacementTransform(off, on), 
            ReplacementTransform(toggle1, toggle )
            )
        
        self.wait(2)


        toggle1 = Text("TOGGLE = 4", font_size=54).next_to(Current, DOWN, buff=1).shift(RIGHT*1.1)

        off = Text("OFF", font_size=64).next_to(Current, RIGHT, buff=0.5)

        
        self.play(
            bulb.turn_off(),
            ReplacementTransform(on, off), 
            ReplacementTransform(toggle, toggle1 )
            )
        
        self.wait(2)

        toggle = Text("TOGGLE = 5", font_size=54).next_to(Current, DOWN, buff=1).shift(RIGHT*1.1)
        on = Text("ON", font_size=64).move_to(off)  
     
        
        self.play(
            bulb.turn_on(),
            ReplacementTransform(off, on), 
            ReplacementTransform(toggle1, toggle )
            )
        
        self.wait(2)

        # Create conclusion text
        conclusion_text = VGroup(
            Text("Pattern:", font_size=36, weight=BOLD),
            Text("• Even number of toggles → Bulb is OFF", font_size=32),
            Text("• Odd number of toggles → Bulb is ON", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        # Position the conclusion at the center
        conclusion_text.move_to(ORIGIN)

        self.play(
       
            FadeOut(Current),
            FadeOut(toggle), 
            FadeOut(bulb), 
            FadeOut(off), 
            FadeOut(on), 
            FadeIn(conclusion_text)

        )

        rect = SurroundingRectangle(conclusion_text, color=GREEN, stroke_width=9).scale(1.29)
        self.play(ShowCreation(rect))
        self.wait(2)
