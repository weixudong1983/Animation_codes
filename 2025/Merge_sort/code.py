from manimlib import *
import numpy as np

class MergeSortAnimation(Scene):
    def construct(self):
        
        self.camera.frame.scale(0.87)
        # Array to sort - 8 elements
        self.array = [38, 27, 43, 3, 9, 82, 10, 15]
        n = len(self.array)
        
        # Create rectangles as VGroup(rect, text) - complete cells
        self.rectangles = []
        
        # Parameters for perfect spacing
        self.rect_width = 0.8
        self.rect_height = 0.8
        self.buff_between = 0.15
        total_width = n * self.rect_width + (n - 1) * self.buff_between
        start_x = -total_width / 2 + self.rect_width / 2
        
        for i, value in enumerate(self.array):
            # Create rectangle
            rect = RoundedRectangle(
                width=self.rect_width,
                height=self.rect_height,
                corner_radius=0.12,
                stroke_color=WHITE,
                stroke_width=3,
                fill_color=BLUE,
                fill_opacity=0.7
            )
            
            # Create text
            text = Text(str(value), font_size=28, weight=BOLD, color=WHITE)
            
            # Position both at the same location
            x_pos = start_x + i * (self.rect_width + self.buff_between)
            rect.move_to([x_pos, 0, 0])
            text.move_to([x_pos, 0, 0])
            
            # Create VGroup containing both rectangle and text
            cell = VGroup(rect, text)
            self.rectangles.append(cell)
        
        # Create array
        for i in range(n):
            self.play(ShowCreation(self.rectangles[i]), run_time=0.4)
        
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*2))

        self.wait(2)

        a1 = self.rectangles[0].get_center().copy()
        a2 = self.rectangles[1].get_center().copy()
        a3 = self.rectangles[2].get_center().copy()
        a4 = self.rectangles[3].get_center().copy()
        a5 = self.rectangles[4].get_center().copy()
        a6 = self.rectangles[5].get_center().copy()
        a7 = self.rectangles[6].get_center().copy()
        a8 = self.rectangles[7].get_center().copy()

        self.play(
            VGroup(
                self.rectangles[1],
                self.rectangles[0],
                self.rectangles[2],
                self.rectangles[3],
            ).animate.shift(DOWN*1.3+LEFT*0.97),

            VGroup(
                self.rectangles[4],
                self.rectangles[5],
                self.rectangles[6],
                self.rectangles[7],
            ).animate.shift(DOWN*1.3+RIGHT*0.97), 
            )
        
        self.wait(1)

        b1 = self.rectangles[0].get_center().copy()
        b2 = self.rectangles[1].get_center().copy()
        b3 = self.rectangles[2].get_center().copy()
        b4 = self.rectangles[3].get_center().copy()
        b5 = self.rectangles[4].get_center().copy()
        b6 = self.rectangles[5].get_center().copy()
        b7 = self.rectangles[6].get_center().copy()
        b8 = self.rectangles[7].get_center().copy()

        self.play(

                VGroup(
                self.rectangles[1],
                self.rectangles[0],
            ).animate.shift(DOWN*1.3+LEFT*0.5),

                VGroup(
                self.rectangles[2],
                self.rectangles[3],
            ).animate.shift(DOWN*1.3+RIGHT*0.5),

                VGroup(
                self.rectangles[4],
                self.rectangles[5],
            ).animate.shift(DOWN*1.3+LEFT*0.5),

                VGroup(
                self.rectangles[6],
                self.rectangles[7],
            ).animate.shift(DOWN*1.3+RIGHT*0.5),

        )

        c1 = self.rectangles[0].get_center().copy()
        c2 = self.rectangles[1].get_center().copy()
        c3 = self.rectangles[2].get_center().copy()
        c4 = self.rectangles[3].get_center().copy()
        c5 = self.rectangles[4].get_center().copy()
        c6 = self.rectangles[5].get_center().copy()
        c7 = self.rectangles[6].get_center().copy()
        c8 = self.rectangles[7].get_center().copy()


        self.wait()


        self.play(
            self.rectangles[0].animate.shift(DOWN*1.28+LEFT*0.1),
            self.rectangles[1].animate.shift(DOWN*1.28+RIGHT*0.1),
            self.rectangles[2].animate.shift(DOWN*1.28+LEFT*0.1),
            self.rectangles[3].animate.shift(DOWN*1.28+RIGHT*0.1),
            self.rectangles[4].animate.shift(DOWN*1.28+LEFT*0.1),
            self.rectangles[5].animate.shift(DOWN*1.28+RIGHT*0.1),
            self.rectangles[6].animate.shift(DOWN*1.28+LEFT*0.1),
            self.rectangles[7].animate.shift(DOWN*1.28+RIGHT*0.1),

        )

        self.wait(2)

        self.play(
            self.rectangles[0][0].animate.set_fill(RED, 0.8),
            self.rectangles[1][0].animate.set_fill(RED, 0.8),
            self.rectangles[2][0].animate.set_fill(RED, 0.8),
            self.rectangles[3][0].animate.set_fill(RED, 0.8),
            run_time=0.4
        )

        self.wait(1.5)

        self.play(
            self.rectangles[0][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[1][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[2][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[3][0].animate.set_fill(BLUE, 0.8),

            run_time=0.4
        )

        self.wait(2)

        self.play(self.rectangles[1].animate.move_to(c1), run_time=0.4)
        self.play(self.rectangles[0].animate.move_to(c2), run_time=0.4)
        self.play(self.rectangles[3].animate.move_to(c3), run_time=0.4)
        self.play(self.rectangles[2].animate.move_to(c4), run_time=0.4)
        self.play(self.rectangles[4].animate.move_to(c5), run_time=0.4)
        self.play(self.rectangles[5].animate.move_to(c6), run_time=0.4)
        self.play(self.rectangles[6].animate.move_to(c7), run_time=0.4)
        self.play(self.rectangles[7].animate.move_to(c8), run_time=0.4)

       

        self.wait(2)


        self.play(

            self.rectangles[0][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[1][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[2][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[3][0].animate.set_fill(PURPLE, 0.8),


        )

        self.wait(2)



        self.play(

            self.rectangles[0][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[1][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[2][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[3][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[4][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[5][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[6][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[7][0].animate.set_fill(PURPLE, 0.8),


        )


        self.wait(2)

        self.play(
            self.rectangles[4][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[5][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[6][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[7][0].animate.set_fill(BLUE, 0.8),

        )


        self.wait(2)


        self.play(self.rectangles[3].animate.move_to(b1), run_time=0.4 )
        self.play(self.rectangles[1].animate.move_to(b2), run_time=0.4 )
        self.play(self.rectangles[0].animate.move_to(b3), run_time=0.4 )
        self.play(self.rectangles[2].animate.move_to(b4), run_time=0.4 )

        self.wait(2)

        self.play(self.rectangles[4].animate.move_to(b5), run_time=0.4 )
        self.play(self.rectangles[6].animate.move_to(b6), run_time=0.4 )
        self.play(self.rectangles[7].animate.move_to(b7), run_time=0.4 )
        self.play(self.rectangles[5].animate.move_to(b8), run_time=0.4 )

        self.wait(3)

        self.play(

            self.rectangles[0][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[1][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[2][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[3][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[4][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[5][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[6][0].animate.set_fill(PURPLE, 0.8),
            self.rectangles[7][0].animate.set_fill(PURPLE, 0.8),


        )


        self.wait(2)



        self.play(

            self.rectangles[0][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[1][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[2][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[3][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[4][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[5][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[6][0].animate.set_fill(BLUE, 0.8),
            self.rectangles[7][0].animate.set_fill(BLUE, 0.8),


        )




        self.play(self.rectangles[3].animate.move_to(a1), run_time=0.4 )
        self.play(self.rectangles[4].animate.move_to(a2), run_time=0.4 )
        self.play(self.rectangles[6].animate.move_to(a3), run_time=0.4 )
        self.play(self.rectangles[7].animate.move_to(a4), run_time=0.4 )
        self.play(self.rectangles[1].animate.move_to(a5), run_time=0.4 )
        self.play(self.rectangles[0].animate.move_to(a6), run_time=0.4 )
        self.play(self.rectangles[2].animate.move_to(a7), run_time=0.4 )
        self.play(self.rectangles[5].animate.move_to(a8), run_time=0.4 )


        self.wait(2)


        self.play(

            self.rectangles[0][0].animate.set_fill(GREEN, 0.8),
            self.rectangles[1][0].animate.set_fill(GREEN, 0.8),
            self.rectangles[2][0].animate.set_fill(GREEN, 0.8),
            self.rectangles[3][0].animate.set_fill(GREEN, 0.8),
            self.rectangles[4][0].animate.set_fill(GREEN, 0.8),
            self.rectangles[5][0].animate.set_fill(GREEN, 0.8),
            self.rectangles[6][0].animate.set_fill(GREEN, 0.8),
            self.rectangles[7][0].animate.set_fill(GREEN, 0.8),


        )

        self.play(self.camera.frame.animate.scale(0.8).shift(UP*2))

        self.wait(2)


