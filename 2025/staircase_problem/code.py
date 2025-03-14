from manimlib import *
PURE_RED = "#FF0000"


class SimpleStaircaseAnimation(Scene):
    def construct(self):

        
        self.camera.frame.shift(LEFT*1.14+UP*0.29)
        # Create a staircase with 6 steps
        staircase = VGroup()
        stair_width = 1.2
        
        # Create 6 stairs with increasing heights
        for i in range(6):
            # Each stair increases in height
            stair_height = 1 + (i)
            stair = Rectangle(
                width=stair_width,
                height=stair_height,
                color=WHITE,
                fill_opacity=0.2
            )
            
            # Position stairs to form a staircase (from left to right)
            # Each stair's bottom is aligned
            if i == 0:
                stair.align_to(ORIGIN, DOWN+LEFT)
            else:
                stair.next_to(staircase[i-1], RIGHT, buff=0)
                stair.align_to(staircase[0], DOWN)
            
            staircase.add(stair)
        
        # Center the staircase
        staircase.center()
        
        # Show the complete staircase
        self.play(ShowCreation(staircase))

        self.wait(1)

        bob = ImageMobject("bob.png").next_to(staircase, LEFT).scale(0.58*0.72).shift(DOWN*2.5)
        self.play(GrowFromCenter(bob))

        self.wait(2)
        self.play(staircase[0].animate.set_fill(GREEN, 0.8))


        arrow = CurvedArrow(bob.get_top(), staircase[0].get_top(), stroke_width=8, angle=-PI/1.5, color=YELLOW)
        self.play(ShowCreation(arrow))

        self.wait(2)
        self.play(Uncreate(arrow))
        
        arrow = CurvedArrow(bob.get_top(), staircase[0].get_top(), stroke_width=8, angle=-PI/1.5, color=YELLOW)
        arrow1 = CurvedArrow(staircase[0].get_top(), staircase[1].get_top(), stroke_width=8, angle=-PI/1.12, color=YELLOW)
        arrow11 = CurvedArrow(staircase[1].get_top(), staircase[2].get_top(), stroke_width=8, angle=-PI/1.12, color=YELLOW)
        self.play(staircase[1].animate.set_fill(GREEN, 0.8),
                  staircase[0].animate.set_fill(WHITE, 0.2))

        self.play(ShowCreation(arrow))
        self.play(ShowCreation(arrow1))
        self.wait(2)

        arrow2 = CurvedArrow(bob.get_top(), staircase[1].get_top(), stroke_width=8, angle=-PI/1.5, color=YELLOW)

        self.play(Uncreate(arrow, ), Uncreate(arrow1))
        self.play(ShowCreation(arrow2))

        self.wait(2)

        
        arrow = CurvedArrow(bob.get_top(), staircase[0].get_top(), stroke_width=8, angle=-PI/1.5, color=YELLOW)
        arrow1 = CurvedArrow(staircase[0].get_top(), staircase[1].get_top(), stroke_width=8, angle=-PI/1.12, color=YELLOW)
        arrow11 = CurvedArrow(staircase[1].get_top(), staircase[2].get_top(), stroke_width=8, angle=-PI/1.12, color=YELLOW)


        self.play(Uncreate(arrow2))
        self.play(staircase[2].animate.set_fill(GREEN, 0.8),
                  staircase[1].animate.set_fill(WHITE, 0.2))

        self.play(ShowCreation(arrow), run_time=0.6)
        self.play(ShowCreation(arrow1), run_time=0.6)
        self.play(ShowCreation(arrow11), run_time=0.6)

        self.wait(2)
        self.play(Uncreate(arrow), Uncreate(arrow1), Uncreate(arrow11))


        arrow2 = CurvedArrow(bob.get_top(), staircase[1].get_top(), stroke_width=8, angle=-PI/1.5, color=YELLOW)
        self.play(ShowCreation(arrow2), run_time=0.6)

        arrow11 = CurvedArrow(staircase[1].get_top(), staircase[2].get_top(), stroke_width=8, angle=-PI/1.12, color=YELLOW)
        self.play(ShowCreation(arrow11), run_time=0.6)

        self.wait(2)
        self.play(Uncreate(arrow2), Uncreate(arrow11))

        arrow2 = CurvedArrow(bob.get_top(), staircase[0].get_top(), stroke_width=8, angle=-PI/1.5, color=YELLOW)
        self.play(ShowCreation(arrow2), run_time=0.6)

        arrow11 = CurvedArrow(staircase[0].get_top(), staircase[2].get_top(), stroke_width=8, angle=-PI/1.12, color=YELLOW)
        self.play(ShowCreation(arrow11), run_time=0.6)

        self.wait(2)

        self.play(staircase[2].animate.set_fill(WHITE, 0.2),
                  Uncreate(arrow11), Uncreate(arrow2))


        self.wait(2)


        self.play(staircase[-1].animate.set_fill(GREEN, 0.8))
        self.wait(2)

        arrow1 = CurvedArrow(staircase[-2].get_top(), staircase[-1].get_top(), stroke_width=8, angle=-PI/0.92, color=YELLOW)
        self.play(staircase[-2].animate.set_fill(ORANGE, 0.8), ShowCreation(arrow1))
        self.wait(2)
        self.play(Uncreate(arrow1), run_time=0.4)

        arrow1 = CurvedArrow(staircase[-3].get_top(), staircase[-1].get_top(), stroke_width=8, angle=-PI/1.22, color=YELLOW)
        self.play(staircase[-3].animate.set_fill(ORANGE, 0.8), ShowCreation(arrow1))
        self.wait(2)
        self.play(Uncreate(arrow1), run_time=0.34)
        


        
        text = Text("f(n) = f(n-1) + f(n-2)\n\nf(1) = 1, f(2) = 2 ").to_edge(UP).shift(LEFT*3.6).scale(0.88)
        self.play(Write(text[:18]))
        self.wait(2)
        self.play(Write(text[18:]))
        self.wait(2)


        code = Text("""
def climbStairs(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climbStairs(n-1) + climbStairs(n-2)
""").set_color_by_text_to_color_map({
            "def": ORANGE,
            "float": ORANGE,
            "if": ORANGE,
            "return": ORANGE,
            "range":PURE_RED,
            "for":ORANGE,
            "in":ORANGE,
            "inf":YELLOW,
            "else":ORANGE,
            "min":PURE_RED,
            "coin":WHITE,
            "climbStairs": PURE_RED,
            "1":GREEN,
            "2":GREEN

           }).shift(LEFT*16.23).scale(0.73)
        

        self.play(ShowCreation(code), self.camera.frame.animate.shift(LEFT*15))
        

        self.wait(2)






        self.embed()
