from manimlib import *
import numpy as np

class SelectionSortAnimation(Scene):
    def construct(self):
        # Title with stunning styling
        title = Text("Selection Sort Algorithm", font_size=48, weight=BOLD)
        title.set_color("#00FF00")
        title.to_edge(UP, buff=0.6).shift(DOWN*0.24)
        
        self.play(ShowCreation(title), run_time=2, rate_func=smooth)
        self.wait(1)
        
        # Array to sort
        array = [11, 34, 25, 12, 22, 64, 9]
        n = len(array)
        
        # Create rectangles and text with proper spacing
        rectangles = []
        texts = []
        
        # Parameters for perfect spacing
        rect_width = 1.16
        rect_height = 1.16
        buff_between = 0.2
        total_width = len(array) * rect_width + (len(array) - 1) * buff_between
        start_x = -total_width / 2 + rect_width / 2
        
        for i, value in enumerate(array):
            rect = RoundedRectangle(
                width=rect_width,
                height=rect_height,
                corner_radius=0.15,
                stroke_color=WHITE,
                stroke_width=3,
                fill_color=RED,
                fill_opacity=0.8
            )
            x_pos = start_x + i * (rect_width + buff_between)
            rect.move_to([x_pos, 0, 0])
            
            text = Text(str(value), font_size=32, weight=BOLD, color=BLACK)
            text.move_to(rect.get_center())
            
            rectangles.append(rect)
            texts.append(text)
        
        # Create array
        for i in range(len(array)):
            self.play(
                ShowCreation(rectangles[i]),
                ShowCreation(texts[i]),
                run_time=0.4,
                rate_func=smooth
            )
        
        self.wait(1)
        
        # Create brace for sorted portion (initially empty)
        brace = None
        brace_text = None
        
        # Create MIN text (initially hidden)
        min_text = Text(f"MIN = {array[0]}", font_size=48, color=WHITE, weight=BOLD)
        min_text.move_to([0, -2.8, 0]).shift(UP*0.1)
        
        # Create arrow pointer
        arrow = Arrow(
            start=ORIGIN, 
            end=DOWN*0.8, 
            stroke_width=9, 
            color=YELLOW,
            buff=0
        )
        arrow.move_to([start_x, 1.2, 0])  # Position above first element
        
        self.wait(1)
        
        # Selection Sort Algorithm
        for i in range(n - 1):
            # Show detailed text animations only for first 2 iterations (i=0 and i=1)
            show_detailed_text = (i < 2)
            
            # Step 1: Highlight current position (selection position) with PURPLE fill
            self.play(rectangles[i].animate.set_fill(PURPLE, opacity=0.8), 
                     run_time=0.7 if show_detailed_text else 0.5)
            
            # Step 2: Find minimum element
            min_idx = i
            min_value = array[i]
            
            # Show MIN text and arrow for first iteration
            if i == 0:
                self.play(
                    ShowCreation(min_text),
                    ShowCreation(arrow),
                    run_time=1
                )
            
            # Update MIN text and move arrow to current minimum
            new_min_text = Text(f"MIN = {min_value}", font_size=48, color=WHITE, weight=BOLD)
            new_min_text.move_to([0, -2.8, 0]).shift(UP*0.1)
            arrow_target_x = start_x + min_idx * (rect_width + buff_between)
            
            self.play(
                Transform(min_text, new_min_text),
                arrow.animate.move_to([arrow_target_x, 1.2, 0]),
                run_time=0.5 if show_detailed_text else 0.3
            )
            
            # Highlight current minimum with PURPLE fill
            self.play(rectangles[min_idx].animate.set_fill(PURPLE, opacity=0.8), 
                     run_time=0.7 if show_detailed_text else 0.5)
            
            # Search through remaining unsorted elements
            for j in range(i + 1, n):
                # Highlight element being compared with PURPLE fill
                self.play(rectangles[j].animate.set_fill(PURPLE, opacity=0.8), 
                         run_time=0.6 if show_detailed_text else 0.5)
                
                if array[j] < min_value:
                    # Reset previous minimum's fill
                    self.play(rectangles[min_idx].animate.set_fill(RED, opacity=0.8), 
                             run_time=0.6 if show_detailed_text else 0.5)
                    
                    # Update minimum
                    min_idx = j
                    min_value = array[j]
                    
                    # Update MIN text and move arrow to new minimum
                    new_min_text = Text(f"MIN = {min_value}", font_size=48, color=WHITE, weight=BOLD)
                    new_min_text.move_to([0, -2.8, 0]).shift(UP*0.1)
                    arrow_target_x = start_x + min_idx * (rect_width + buff_between)
                    
                    self.play(
                        Transform(min_text, new_min_text),
                        arrow.animate.move_to([arrow_target_x, 1.2, 0]),
                        run_time=0.7 if show_detailed_text else 0.5
                    )
                    
                    # Keep new minimum highlighted with PURPLE
                    # (j element already has PURPLE fill from comparison step)
                else:
                    # Reset comparison element's fill
                    self.play(rectangles[j].animate.set_fill(RED, opacity=0.8), 
                             run_time=0.6 if show_detailed_text else 0.5)
            
            # Step 3: Swap if needed
            if min_idx != i:
                # Use built-in Swap function
                self.play(
                    Swap(rectangles[i], rectangles[min_idx]),
                    Swap(texts[i], texts[min_idx]),
                    run_time=1.15
                )
                
                # Update arrays and references
                array[i], array[min_idx] = array[min_idx], array[i]
                rectangles[i], rectangles[min_idx] = rectangles[min_idx], rectangles[i]
                texts[i], texts[min_idx] = texts[min_idx], texts[i]
            
            # Step 4: Reset fills and mark current position as sorted
            self.play(
                rectangles[i].animate.set_fill(GREEN, opacity=0.8),
                run_time=0.8 if show_detailed_text else 0.4
            )
            
            # Reset any remaining highlighted fills
            for k in range(i + 1, n):
                if rectangles[k].fill_color == PURPLE:
                    self.play(rectangles[k].animate.set_fill(RED, opacity=0.8), 
                             run_time=0.5)
            
            # Step 5: Update brace to show sorted portion
            if i == 0:
                # Create initial brace
                brace = Brace(rectangles[0], DOWN, buff=0.2)
                brace_text = Text("Sorted", font_size=32, weight=BOLD, color=GREEN)
                brace_text.next_to(brace, DOWN, buff=0.2)
                self.play(ShowCreation(brace), ShowCreation(brace_text), run_time=1)
            else:
                # Expand brace to include newly sorted element
                sorted_group = Group(*rectangles[:i+1])
                new_brace = Brace(sorted_group, DOWN, buff=0.2)
                new_brace_text = Text("Sorted", font_size=32, weight=BOLD, color=GREEN)
                new_brace_text.next_to(new_brace, DOWN, buff=0.2)
                
                self.play(
                    Transform(brace, new_brace),
                    Transform(brace_text, new_brace_text),
                    run_time=0.8 if show_detailed_text else 0.4
                )
            
            if show_detailed_text:
                self.wait(1)
            else:
                # For iterations after the first 2, just a brief pause
                self.wait(0.3)
        
        # Mark last element as sorted (it's automatically in correct position)
        self.play(rectangles[n-1].animate.set_fill(GREEN, opacity=0.8), run_time=0.8)
        
        # Hide MIN text and arrow as sorting is complete
        self.play(
            FadeOut(min_text),
            FadeOut(arrow),
            run_time=1
        )
        
        # Final celebration text
        final_text = Text("Array Successfully Sorted! 🎉", 
                         font_size=42, color=GOLD, weight=BOLD).set_color(GOLD)
        final_text.move_to([0, -2.8, 0]).shift(UP*0.1)
        self.play(ShowCreation(final_text), run_time=1)
        
        # Final brace for complete array
        complete_brace = Brace(Group(*rectangles), DOWN, buff=0.2)
        complete_brace_text = Text("Completely Sorted", font_size=28, weight=BOLD, color=GOLD)
        complete_brace_text.next_to(complete_brace, DOWN, buff=0.2)
        
        self.play(
            Transform(brace, complete_brace),
            Transform(brace_text, complete_brace_text),
            run_time=1.2
        )
        

        self.wait(2)


# To run: python -m manimlib selection_sort.py SelectionSortAnimation
