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


from manimlib import *

class Final(Scene):

    def construct(self):
         
         self.camera.frame.scale(0.9)



         array = Array(array_size=6)

         array.append_element(self, "0")
         array.append_element(self, "0")
         array.append_element(self, "0")
         array.append_element(self, "0")
         array.append_element(self, "0")
         array.append_element(self, "0")


         self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(6)])
         self.wait(2)

         text = Text("f(n) = f(n-1) + f(n-2)\n\n  f(1) = 1, f(2) = 2 ").scale(0.88).next_to(array, DOWN, buff=0.8)
         self.play(Write(text), self.camera.frame.animate.shift(DOWN))    

         self.wait(2)
         
         self.play(array.square_contents[0][0].animate.set_fill(BLUE, 0.6).set_z_index(-1))
         self.play(array.square_contents[0][1].animate.become(Text("1").move_to(array.square_contents[0][1]).scale(1.4)))   
         self.wait()

         self.play(
             array.square_contents[0][0].animate.set_fill(BLUE, 0).set_z_index(-1),
             array.square_contents[1][0].animate.set_fill(BLUE, 0.6).set_z_index(-1),
             )
         self.play(array.square_contents[1][1].animate.become(Text("2").move_to(array.square_contents[1][1]).scale(1.4))) 

         self.wait()

         self.play(
             array.square_contents[1][0].animate.set_fill(BLUE, 0).set_z_index(-1),
             array.square_contents[2][0].animate.set_fill(BLUE, 0.6).set_z_index(-1),
             ) 
         
         self.play(FadeOut(text), self.camera.frame.animate.shift(UP*0.68))

         brace = Brace(VGroup(array.square_contents[0], array.square_contents[1]), DOWN, buff=0.7)
         self.play(GrowFromCenter(brace))
         self.wait()
         self.play(array.square_contents[2][1].animate.become(Text("3").move_to(array.square_contents[2][1]).scale(1.4))) 

         self.wait()

         self.play(Transform(brace, Brace(VGroup(array.square_contents[1], array.square_contents[2]), DOWN, buff=0.7)),
                   array.square_contents[2][0].animate.set_fill(BLUE, 0).set_z_index(-1),
             array.square_contents[3][0].animate.set_fill(BLUE, 0.6).set_z_index(-1),
             )
         self.wait()
         self.play(array.square_contents[3][1].animate.become(Text("5").move_to(array.square_contents[3][1]).scale(1.4))) 
         self.wait(0.2)
 
         self.play(Transform(brace, Brace(VGroup(array.square_contents[2], array.square_contents[3]), DOWN, buff=0.7)),
                   array.square_contents[3][0].animate.set_fill(BLUE, 0).set_z_index(-1),
             array.square_contents[4][0].animate.set_fill(BLUE, 0.6).set_z_index(-1),
             )
         self.wait()
         self.play(array.square_contents[4][1].animate.become(Text("8").move_to(array.square_contents[4][1]).scale(1.4))) 
         self.wait(0.2)

         self.play(Transform(brace, Brace(VGroup(array.square_contents[3], array.square_contents[4]), DOWN, buff=0.7)),
                   array.square_contents[4][0].animate.set_fill(BLUE, 0).set_z_index(-1),
             array.square_contents[5][0].animate.set_fill(BLUE, 0.6).set_z_index(-1),
             )
         self.wait()
         self.play(array.square_contents[5][1].animate.become(Text("13").move_to(array.square_contents[5][1]).scale(1.4))) 
         self.wait(2)

         self.play(FadeOut(VGroup(brace)),
                   array.square_contents[5][0].animate.set_fill(RED, 0.6).set_z_index(-1),
                   self.camera.frame.animate.shift(DOWN*0.8)
                   )
         
         text = Text("Total Ways to reach the 6th stair = 13").next_to(array, DOWN, buff=1.3).scale(0.9*0.8)
         self.play(Write(text))

         self.wait(3)


         self.embed()






class Array(VGroup):
    def __init__(self, array_size=5, **kwargs):
        super().__init__(**kwargs)
        self.array_size = array_size
        self.square_contents = [None] * array_size
        self.array_group = self.create_array()
        self.add(self.array_group)

    def create_element(self, text):
        square = Square(side_length=1.42, fill_opacity=0, fill_color=BLACK, color=WHITE).set_color(GREEN)
        text = Text(text, font_size=44, color=BLACK).scale(0.8)
        return VGroup(square, text)

    def create_array(self):
        squares = VGroup(*[Square(side_length=1.42, color=WHITE, stroke_width=6) for _ in range(self.array_size)])
        squares.arrange(RIGHT, buff=0)

        return VGroup(squares)



    def append_element(self, scene, value):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.42, fill_opacity=0, fill_color=YELLOW, color=GREEN,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1).scale(1.3*1.1)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def add_element(self, scene, value, color=YELLOW):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.42, fill_opacity=1, fill_color=color, color=BLACK,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK, font_size=50).set_z_index(1).set_color(BLACK)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                scene.play(FadeIn(new_square1))
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def pop_element(self, scene):
        for i in range(self.array_size - 1, -1, -1):
            if self.square_contents[i] is not None:
                scene.play(FadeOut(self.square_contents[i]))
                self.square_contents[i] = None
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def delete_from_front(self, scene):
        if self.square_contents[0] is not None:
            scene.play(FadeOut(self.square_contents[0]))
            self.square_contents[0] = None
            animations = []
            for i in range(1, self.array_size):
                if self.square_contents[i] is not None:
                    animations.append(
                        self.square_contents[i].animate.move_to(self.array_group[0][i - 1].get_center())
                    )
                    self.square_contents[i - 1] = self.square_contents[i]
                    self.square_contents[i] = None
            if animations:
                scene.play(*animations)
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def create_new_array(self, scene, new_size):
        new_array = Array(array_size=new_size)
        new_array.next_to(self, DOWN, buff=0.7)
        scene.play(ShowCreation(new_array))
        return new_array

    def transfer_elements_to_new_array(self, scene, new_array):
        for i, content in enumerate(self.square_contents):
            if content is not None:
                scene.play(Transform(content, new_array.array_group[0][i]))
                new_array.square_contents[i] = content
                self.square_contents[i] = None





        self.embed()
