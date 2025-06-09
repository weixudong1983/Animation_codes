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




class Merge(Scene):
    def construct(self):
        
        self.camera.frame.scale(0.75*0.799)
        
        self.array = [3, 27, 43, 50, 55]
        self.array1 = [8, 29, 52]
        
        n = len(self.array)
        n1 = len(self.array1)
        
        # Create rectangles as VGroup(rect, text) - complete cells
        self.rectangles = []
        self.rectangles1 = []
        self.empty_rectangles = []
        
        # Parameters for perfect spacing
        self.rect_width = 0.8
        self.rect_height = 0.8
        self.buff_between = 0.15
        self.vertical_spacing = 1.4  # Space between arrays
        
        # Calculate positioning for first array
        total_width = n * self.rect_width + (n - 1) * self.buff_between
        start_x = -total_width / 2 + self.rect_width / 2
        
        # Create first array (self.array) at top
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
            rect.move_to([x_pos, self.vertical_spacing, 0])
            text.move_to([x_pos, self.vertical_spacing, 0])
            
            # Create VGroup containing both rectangle and text
            cell = VGroup(rect, text)
            self.rectangles.append(cell)
        
        # Calculate positioning for second array (self.array1)
        total_width1 = n1 * self.rect_width + (n1 - 1) * self.buff_between
        start_x1 = -total_width1 / 2 + self.rect_width / 2
        
        # Create second array (self.array1) in middle
        for i, value in enumerate(self.array1):
            # Create rectangle
            rect = RoundedRectangle(
                width=self.rect_width,
                height=self.rect_height,
                corner_radius=0.12,
                stroke_color=WHITE,
                stroke_width=3,
                fill_color=GREEN,  # Different color for distinction
                fill_opacity=0.7
            )
            
            # Create text
            text = Text(str(value), font_size=28, weight=BOLD, color=WHITE)
            
            # Position both at the same location
            x_pos = start_x1 + i * (self.rect_width + self.buff_between)
            rect.move_to([x_pos, 0, 0])
            text.move_to([x_pos, 0, 0])
            
            # Create VGroup containing both rectangle and text
            cell = VGroup(rect, text)
            self.rectangles1.append(cell)
        
        # Create empty rectangles array (8 elements) at bottom
        empty_array_size = 8
        total_width_empty = empty_array_size * self.rect_width + (empty_array_size - 1) * self.buff_between
        start_x_empty = -total_width_empty / 2 + self.rect_width / 2
        
        for i in range(empty_array_size):
            # Create empty rectangle
            rect = RoundedRectangle(
                width=self.rect_width,
                height=self.rect_height,
                corner_radius=0.12,
                stroke_color=GREY_C,
                stroke_width=2,
                fill_color=GREY_E,
                fill_opacity=0.3
            )
            
            # Position rectangle
            x_pos = start_x_empty + i * (self.rect_width + self.buff_between)
            rect.move_to([x_pos, -self.vertical_spacing, 0])
            
            self.empty_rectangles.append(rect)
        
        # Animate creation of first array
        for i in range(n):
            self.play(ShowCreation(self.rectangles[i]), run_time=0.4)
        
        self.wait(1)
        
        # Animate creation of second array
        for i in range(n1):
            self.play(ShowCreation(self.rectangles1[i]), run_time=0.4)
        
        self.wait(1)
        
        # Animate creation of empty rectangles
        for i in range(empty_array_size):
            self.play(ShowCreation(self.empty_rectangles[i]), run_time=0.3)
        
        self.wait(2)

        # MERGE ALGORITHM STARTS HERE
        # Merge Algorithm Implementation
        i = 0  # Pointer for first array
        j = 0  # Pointer for second array
        k = 0  # Pointer for result array
        
        # Create result array to store merged values
        result_values = []
        
        # Merge the two arrays
        while i < len(self.array) and j < len(self.array1):
            # Highlight current elements being compared
            self.play(
                self.rectangles[i][0].animate.set_fill(PURPLE, opacity=0.9),
                self.rectangles1[j][0].animate.set_fill(PURPLE, opacity=0.9),
                run_time=0.8
            )
            
            self.wait(1)
            
            # Compare elements
            if self.array[i] <= self.array1[j]:
                # Copy from first array
                smaller_value = self.array[i]
                result_values.append(smaller_value)
                
                # Create copy of the element
                copy_rect = RoundedRectangle(
                    width=self.rect_width,
                    height=self.rect_height,
                    corner_radius=0.12,
                    stroke_color=WHITE,
                    stroke_width=3,
                    fill_color=ORANGE,
                    fill_opacity=0.7
                )
                copy_text = Text(str(smaller_value), font_size=28, weight=BOLD, color=WHITE)
                
                # Position at original location first
                original_pos = self.rectangles[i].get_center()
                copy_rect.move_to(original_pos)
                copy_text.move_to(original_pos)
                copy_cell = VGroup(copy_rect, copy_text)
                
                # Add to scene
                self.add(copy_cell)
                
                # Move to result array position
                result_x = start_x_empty + k * (self.rect_width + self.buff_between)
                result_pos = [result_x, -self.vertical_spacing, 0]
                
                self.play(
                    copy_cell.animate.move_to(result_pos),
                    self.rectangles[i][0].animate.set_fill(RED, opacity=0.5),  # Mark as used
                    run_time=1.2
                )
                
                i += 1
            else:
                # Copy from second array
                smaller_value = self.array1[j]
                result_values.append(smaller_value)
                
                # Create copy of the element
                copy_rect = RoundedRectangle(
                    width=self.rect_width,
                    height=self.rect_height,
                    corner_radius=0.12,
                    stroke_color=WHITE,
                    stroke_width=3,
                    fill_color=ORANGE,
                    fill_opacity=0.7
                )
                copy_text = Text(str(smaller_value), font_size=28, weight=BOLD, color=WHITE)
                
                # Position at original location first
                original_pos = self.rectangles1[j].get_center()
                copy_rect.move_to(original_pos)
                copy_text.move_to(original_pos)
                copy_cell = VGroup(copy_rect, copy_text)
                
                # Add to scene
                self.add(copy_cell)
                
                # Move to result array position
                result_x = start_x_empty + k * (self.rect_width + self.buff_between)
                result_pos = [result_x, -self.vertical_spacing, 0]
                
                self.play(
                    copy_cell.animate.move_to(result_pos),
                    self.rectangles1[j][0].animate.set_fill(RED, opacity=0.5),  # Mark as used
                    run_time=1.2
                )
                
                j += 1
            
            k += 1
            self.wait(0.5)
        
        # Copy remaining elements from first array
        while i < len(self.array):
            self.play(self.rectangles[i][0].animate.set_fill(PURPLE, opacity=0.9), run_time=0.5)
            
            remaining_value = self.array[i]
            result_values.append(remaining_value)
            
            # Create copy
            copy_rect = RoundedRectangle(
                width=self.rect_width,
                height=self.rect_height,
                corner_radius=0.12,
                stroke_color=WHITE,
                stroke_width=3,
                fill_color=ORANGE,
                fill_opacity=0.7
            )
            copy_text = Text(str(remaining_value), font_size=28, weight=BOLD, color=WHITE)
            
            original_pos = self.rectangles[i].get_center()
            copy_rect.move_to(original_pos)
            copy_text.move_to(original_pos)
            copy_cell = VGroup(copy_rect, copy_text)
            
            self.add(copy_cell)
            
            result_x = start_x_empty + k * (self.rect_width + self.buff_between)
            result_pos = [result_x, -self.vertical_spacing, 0]
            
            self.play(
                copy_cell.animate.move_to(result_pos),
                self.rectangles[i][0].animate.set_fill(RED, opacity=0.5),
                run_time=1.0
            )
            
            i += 1
            k += 1
            self.wait(0.5)
        
        # Copy remaining elements from second array
        while j < len(self.array1):
            self.play(self.rectangles1[j][0].animate.set_fill(PURPLE, opacity=0.9), run_time=0.5)
            
            remaining_value = self.array1[j]
            result_values.append(remaining_value)
            
            # Create copy
            copy_rect = RoundedRectangle(
                width=self.rect_width,
                height=self.rect_height,
                corner_radius=0.12,
                stroke_color=WHITE,
                stroke_width=3,
                fill_color=ORANGE,
                fill_opacity=0.7
            )
            copy_text = Text(str(remaining_value), font_size=28, weight=BOLD, color=WHITE)
            
            original_pos = self.rectangles1[j].get_center()
            copy_rect.move_to(original_pos)
            copy_text.move_to(original_pos)
            copy_cell = VGroup(copy_rect, copy_text)
            
            self.add(copy_cell)
            
            result_x = start_x_empty + k * (self.rect_width + self.buff_between)
            result_pos = [result_x, -self.vertical_spacing, 0]
            
            self.play(
                copy_cell.animate.move_to(result_pos),
                self.rectangles1[j][0].animate.set_fill(RED, opacity=0.5),
                run_time=1.0
            )
            
            j += 1
            k += 1
            self.wait(0.5)
        
        self.wait(3)
