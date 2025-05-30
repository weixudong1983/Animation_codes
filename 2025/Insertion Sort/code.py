from manimlib import *
import numpy as np

class InsertionSortAnimation(Scene):
    def construct(self):
        # Title with stunning styling
        title = Text("Insertion Sort Algorithm", font_size=48, weight=BOLD)
        title.set_color("#00FF00")
        title.to_edge(UP, buff=0.6).shift(DOWN*0.24)
        
        self.play(ShowCreation(title), run_time=2, rate_func=smooth)
        self.wait(1)
        
        # Array to sort
        array = [64, 34, 25, 12, 22, 11, 9]
        n = len(array)
        
        # Create rectangles and text with proper spacing
        rectangles = []
        texts = []
        
        # Parameters for perfect spacing
        rect_width = 1.1
        rect_height = 1.1
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
        
        # First element is sorted - make it GREEN
        self.play(rectangles[0].animate.set_fill(GREEN, opacity=0.8), run_time=0.8)
        
        # Create brace for sorted portion
        brace = Brace(rectangles[0], DOWN, buff=0.2)
        brace_text = Text("Sorted", font_size=23, weight=BOLD, color=GREEN)
        brace_text.next_to(brace, DOWN, buff=0.2)
        
        self.play(ShowCreation(brace), ShowCreation(brace_text), run_time=1)
        
        # Status text position
        status_y = -2.8
        status_text = Text("Starting insertion sort...", font_size=34, color=WHITE, weight=BOLD)
        status_text.move_to([0, status_y, 0])
        self.play(ShowCreation(status_text), run_time=0.8)
        
        self.wait(1)
        
        # Insertion Sort Algorithm
        for i in range(1, n):
            current_value = array[i]
            
            # Show detailed text animations only for first 2 iterations (i=1 and i=2)
            show_detailed_text = (i <= 2)
            
            if show_detailed_text:
                # Update status text
                new_status = Text(f"Inserting element: {current_value}", 
                                font_size=34, color=YELLOW, weight=BOLD)
                new_status.move_to([0, status_y, 0])
                self.play(Transform(status_text, new_status), run_time=0.5)
            
            # Step 1: Lift the current element UP
            lift_height = 1.2
            lifted_rect = rectangles[i]
            lifted_text = texts[i]
            
            self.play(
                lifted_rect.animate.shift(UP * lift_height),
                lifted_text.animate.shift(UP * lift_height),
                run_time=1 if show_detailed_text else 0.5,
                rate_func=smooth
            )
            
            # Step 2: Find correct position
            j = i - 1
            insert_pos = i
            
            while j >= 0 and array[j] > current_value:
                insert_pos = j
                j -= 1
            
            # Step 3: Shift required elements to the right
            if insert_pos < i:
                if show_detailed_text:
                    shift_status = Text(f"Shifting elements to make space for {current_value}", 
                                      font_size=34, color=ORANGE, weight=BOLD)
                    shift_status.move_to([0, status_y, 0])
                    self.play(Transform(status_text, shift_status), run_time=0.8)
                
                # Shift all elements from insert_pos to i-1 one position right
                shift_animations = []
                shift_distance = rect_width + buff_between
                
                for k in range(insert_pos, i):
                    shift_animations.extend([
                        rectangles[k].animate.shift(RIGHT * shift_distance),
                        texts[k].animate.shift(RIGHT * shift_distance)
                    ])
                
                self.play(*shift_animations, run_time=1 if show_detailed_text else 0.5, rate_func=smooth)
                
                # Update array and rectangle positions
                temp_rect = lifted_rect
                temp_text = lifted_text
                temp_value = current_value
                
                # Shift elements in arrays
                for k in range(i, insert_pos, -1):
                    rectangles[k] = rectangles[k-1]
                    texts[k] = texts[k-1]
                    array[k] = array[k-1]
                
                rectangles[insert_pos] = temp_rect
                texts[insert_pos] = temp_text
                array[insert_pos] = temp_value
            
            # Step 4: Move lifted element to correct position
            target_x = start_x + insert_pos * (rect_width + buff_between)
            
            if show_detailed_text:
                place_status = Text(f"Placing {current_value} in correct position", 
                                  font_size=34, color=BLUE, weight=BOLD)
                place_status.move_to([0, status_y, 0])
                self.play(Transform(status_text, place_status), run_time=0.8)
            
            # Move to target position (horizontally first, then down)
            self.play(
                lifted_rect.animate.move_to([target_x, lift_height, 0]),
                lifted_text.animate.move_to([target_x, lift_height, 0]),
                run_time=1 if show_detailed_text else 0.5,
                rate_func=smooth
            )
            
            self.play(
                lifted_rect.animate.move_to([target_x, 0, 0]),
                lifted_text.animate.move_to([target_x, 0, 0]),
                run_time=1 if show_detailed_text else 0.5,
                rate_func=smooth
            )
            
            # Step 5: Change color to GREEN (sorted)
            self.play(lifted_rect.animate.set_fill(GREEN, opacity=0.8), run_time=0.8 if show_detailed_text else 0.4)
            
            # Step 6: Transform brace to show new sorted portion
            sorted_group = Group(*rectangles[:i+1])
            new_brace = Brace(sorted_group, DOWN, buff=0.2)
            new_brace_text = Text("Sorted", font_size=23, weight=BOLD, color=GREEN)
            new_brace_text.next_to(new_brace, DOWN, buff=0.2)
            
            self.play(
                Transform(brace, new_brace),
                Transform(brace_text, new_brace_text),
                run_time=0.8 if show_detailed_text else 0.8
            )
            
            if show_detailed_text:
                # Update status
                success_status = Text(f"Element {current_value} inserted successfully!", 
                                    font_size=34, color=GREEN, weight=BOLD)
                success_status.move_to([0, status_y, 0])
                self.play(Transform(status_text, success_status), run_time=0.5)
                
                self.wait(1)
            else:
                # For iterations after the first 2, just a brief pause
                if i == 3:
                    self.play(FadeOut(status_text))

                self.wait(0.3)
        
        # Final celebration
        final_status = Text("Array Successfully Sorted! 🎉", 
                          font_size=32, color=GOLD, weight=BOLD)
        final_status.move_to([0, status_y, 0])
        self.play(Write(final_status), run_time=1)
        
        # Final brace for complete array
        complete_brace = Brace(Group(*rectangles), DOWN, buff=0.2)
        complete_brace_text = Text("Completely Sorted", font_size=25, weight=BOLD, color=GOLD)
        complete_brace_text.next_to(complete_brace, DOWN, buff=0.2)
        
        self.play(
            Transform(brace, complete_brace),
            Transform(brace_text, complete_brace_text),
            run_time=1.2
        )
        
        self.wait(2)
