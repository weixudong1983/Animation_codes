from manimlib import *
import numpy as np


class QuickSortAnimation(Scene):
    def construct(self):

        self.camera.frame.shift(UP*0.66)
        # Simple title
        title = Text("QuickSort Algorithm", font_size=62, weight=BOLD)
        title.set_color("#00ff00")
        title.to_edge(UP, buff=0.6).shift(UP*0.2)
        
        self.play(ShowCreation(title), run_time=1.5)
        self.wait(0.5)
        
        # Array to sort - designed for balanced partitions
        self.array = [40, 20, 60, 10, 46, 50, 59, 5, 15, 25]
        self.n = len(self.array)
        
        # Visual parameters
        self.rect_width = 1.0
        self.rect_height = 1.0
        self.buff_between = 0.2
        
        # Create array visualization
        self.rectangles = []
        self.texts = []
        self.create_array()
        
        self.wait(1)
        
        # Start QuickSort
        self.quicksort(0, self.n - 1)
        
        # Final celebration - all green
        self.play(*[rect.animate.set_fill(GREEN, opacity=0.8) for rect in self.rectangles], run_time=1)
        self.wait(2)


        text = Text("Array Sorted", weight=BOLD).to_edge(DOWN).shift(UP).scale(1.23).set_color(YELLOW)
        self.play(ShowCreation(text))


        self.wait(2)
    
    def create_array(self):
        """Create the visual array"""
        total_width = len(self.array) * self.rect_width + (len(self.array) - 1) * self.buff_between
        start_x = -total_width / 2 + self.rect_width / 2
        
        for i, value in enumerate(self.array):
            rect = RoundedRectangle(
                width=self.rect_width,
                height=self.rect_height,
                corner_radius=0.15,
                stroke_color=WHITE,
                stroke_width=3,
                fill_color=BLUE,
                fill_opacity=0.7
            )
            x_pos = start_x + i * (self.rect_width + self.buff_between)
            rect.move_to([x_pos, 0, 0])
            
            text = Text(str(value), font_size=36, weight=BOLD, color=WHITE)
            text.move_to(rect.get_center())
            
            self.rectangles.append(rect)
            self.texts.append(text)
        
        # Show array creation
        for i in range(len(self.array)):
            self.play(
                ShowCreation(self.rectangles[i]),
                ShowCreation(self.texts[i]),
                run_time=0.3
            )
    
    def quicksort(self, low, high):
        """QuickSort showing the true divide-and-conquer nature"""
        if low < high:
            # Show current subarray being worked on
            if low > 0 or high < self.n - 1:
                for k in range(low, high + 1):
                    if self.rectangles[k].fill_color != GREEN:
                        self.play(self.rectangles[k].animate.set_stroke(YELLOW, width=5), run_time=0.1)
                self.wait(0.3)
            
            # Partition and get pivot position
            pivot_index = self.partition(low, high)
            
            # Reset stroke for processed elements
            for k in range(low, high + 1):
                self.play(self.rectangles[k].animate.set_stroke(WHITE, width=3), run_time=0.1)
            
            self.wait(0.4)
            
            # Recursively sort left half (elements < pivot)
            if low < pivot_index - 1:
                self.quicksort(low, pivot_index - 1)
            
            # Recursively sort right half (elements > pivot)  
            if pivot_index + 1 < high:
                self.quicksort(pivot_index + 1, high)
            
            # After both halves are sorted, make this entire subarray GREEN
            for k in range(low, high + 1):
                if self.rectangles[k].fill_color != GREEN:
                    self.play(self.rectangles[k].animate.set_fill(GREEN, opacity=0.8), run_time=0.2)
    
    def partition(self, low, high):
        """Partition with true QuickSort visualization - divide around pivot"""
        # Choose last element as pivot and highlight it
        pivot_value = self.array[high]
        
        # Highlight pivot in PURPLE
        self.play(self.rectangles[high].animate.set_fill(PURPLE, opacity=0.9), run_time=0.5)
        self.wait(0.5)
        
        # First pass: Color elements based on comparison with pivot
        for j in range(low, high):
            if self.array[j] < pivot_value:
                # Color smaller elements BLUE
                self.play(self.rectangles[j].animate.set_fill(BLUE, opacity=0.8), run_time=0.2)
            else:
                # Color larger elements RED
                self.play(self.rectangles[j].animate.set_fill(RED, opacity=0.8), run_time=0.2)
        
        self.wait(0.8)
        
        # Now physically rearrange: smaller elements to left, larger to right
        i = low - 1
        
        for j in range(low, high):
            if self.array[j] < pivot_value:
                i += 1
                if i != j:
                    self.swap_elements(i, j)
        
        # Place pivot in its final position (between smaller and larger)
        pivot_final_pos = i + 1
        if pivot_final_pos != high:
            self.swap_elements(pivot_final_pos, high)
        
        # Make pivot GREEN immediately when it reaches correct position
        self.play(self.rectangles[pivot_final_pos].animate.set_fill(GREEN, opacity=0.8), run_time=0.6)
        
        # Show the beautiful division: LEFT < PIVOT < RIGHT
        self.wait(0.5)
        
        return pivot_final_pos
    
    def swap_elements(self, i, j):
        """Swap two elements with animation"""
        if i == j:
            return
        
        # Get positions
        pos_i = self.rectangles[i].get_center()
        pos_j = self.rectangles[j].get_center()
        
        # Animate swap
        self.play(
            self.rectangles[i].animate.move_to(pos_j),
            self.texts[i].animate.move_to(pos_j),
            self.rectangles[j].animate.move_to(pos_i),
            self.texts[j].animate.move_to(pos_i),
            run_time=0.5
        )
        
        # Update arrays
        self.rectangles[i], self.rectangles[j] = self.rectangles[j], self.rectangles[i]
        self.texts[i], self.texts[j] = self.texts[j], self.texts[i]
        self.array[i], self.array[j] = self.array[j], self.array[i]
