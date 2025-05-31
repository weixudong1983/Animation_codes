from manimlib import *
import numpy as np

class BubbleSortAnimation(Scene):
    def construct(self):
        # Title with stunning styling
        title = Text("Bubble Sort Algorithm", font_size=48, weight=BOLD)
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
        rect_width = 1.2
        rect_height = 1.2
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
            
            text = Text(str(value), font_size=37, weight=BOLD, color=BLACK)
            text.move_to(rect.get_center())
            
            rectangles.append(rect)
            texts.append(text)
        
        self.wait(1)
        
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
        
        # Create comparison brace (initially empty)
        comparison_brace = None
        comparison_brace_text = None
        
        # Status text position (moved up by UP*0.12)
        status_y = -2.8 + 0.12
        status_text = Text("Starting bubble sort...", font_size=39, color=WHITE, weight=BOLD)  # Increased font size by 5
        status_text.move_to([0, status_y, 0])
        self.play(ShowCreation(status_text), run_time=0.8)
        
        self.wait(1)
        
        # Bubble Sort Algorithm
        pass_number = 0
        
        for i in range(n - 1):
            pass_number += 1
            swapped = False
            
            # Show detailed text animations only for first pass
            show_detailed_text = (pass_number == 1)
            
            if show_detailed_text:
                # Update status text for new pass
                pass_status = Text(f"Bubbling largest element to the end", 
                                 font_size=39, color=YELLOW, weight=BOLD)  # Increased font size by 5
                pass_status.move_to([0, status_y, 0])
                self.play(Transform(status_text, pass_status), run_time=0.8)
                self.wait(0.5)
            
            # Compare adjacent elements
            for j in range(n - i - 1):
                # Create comparison brace for the two elements being compared
                comparing_group = Group(rectangles[j], rectangles[j + 1])
                new_comparison_brace = Brace(comparing_group, DOWN, buff=0.1)
                new_comparison_brace_text = Text("Comparing", font_size=26, weight=BOLD, color=BLUE)
                new_comparison_brace_text.next_to(new_comparison_brace, DOWN, buff=0.1)
                
                # Highlight the two elements being compared using fill color
                self.play(
                    rectangles[j].animate.set_fill(PURPLE, opacity=0.9),
                    rectangles[j + 1].animate.set_fill(PURPLE, opacity=0.9),
                    run_time=0.3 if show_detailed_text else 0.25
                )
                
                # Show or update comparison brace
                if comparison_brace is None:
                    comparison_brace = new_comparison_brace
                    comparison_brace_text = new_comparison_brace_text
                    self.play(
                        ShowCreation(comparison_brace),
                        ShowCreation(comparison_brace_text),
                        run_time=0.5 if show_detailed_text else 0.25
                    )
                else:
                    self.play(
                        Transform(comparison_brace, new_comparison_brace),
                        Transform(comparison_brace_text, new_comparison_brace_text),
                        run_time=0.3 if show_detailed_text else 0.15
                    )
                
                if show_detailed_text:
                    compare_status = Text(f"Comparing {array[j]} and {array[j + 1]}", 
                                        font_size=39, color=BLUE, weight=BOLD)  # Increased font size by 5
                    compare_status.move_to([0, status_y, 0])
                    self.play(Transform(status_text, compare_status), run_time=0.5)
                
                # Check if swap is needed
                if array[j] > array[j + 1]:
                    swapped = True
                    
                    if show_detailed_text:
                        swap_status = Text(f"{array[j]} > {array[j + 1]}, swapping!", 
                                         font_size=39, color=PURPLE, weight=BOLD)  # Increased font size by 5
                        swap_status.move_to([0, status_y, 0])
                        self.play(Transform(status_text, swap_status), run_time=0.5)
                    
                    # Lift both elements
                    lift_height = 1.2
                    self.play(
                        rectangles[j].animate.shift(UP * lift_height),
                        texts[j].animate.shift(UP * lift_height),
                        rectangles[j + 1].animate.shift(UP * lift_height),
                        texts[j + 1].animate.shift(UP * lift_height),
                        run_time=0.8 if show_detailed_text else 0.4,
                        rate_func=smooth
                    )
                    
                    # Calculate target positions for swap
                    target_j = start_x + (j + 1) * (rect_width + buff_between)
                    target_j_plus_1 = start_x + j * (rect_width + buff_between)
                    
                    # Swap positions horizontally
                    self.play(
                        rectangles[j].animate.move_to([target_j, lift_height, 0]),
                        texts[j].animate.move_to([target_j, lift_height, 0]),
                        rectangles[j + 1].animate.move_to([target_j_plus_1, lift_height, 0]),
                        texts[j + 1].animate.move_to([target_j_plus_1, lift_height, 0]),
                        run_time=1.2 if show_detailed_text else 0.6,
                        rate_func=smooth
                    )
                    
                    # Lower both elements
                    self.play(
                        rectangles[j].animate.move_to([target_j, 0, 0]),
                        texts[j].animate.move_to([target_j, 0, 0]),
                        rectangles[j + 1].animate.move_to([target_j_plus_1, 0, 0]),
                        texts[j + 1].animate.move_to([target_j_plus_1, 0, 0]),
                        run_time=0.8 if show_detailed_text else 0.4,
                        rate_func=smooth
                    )
                    
                    # Update arrays and references
                    array[j], array[j + 1] = array[j + 1], array[j]
                    rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
                    texts[j], texts[j + 1] = texts[j + 1], texts[j]
                    
                else:
                    if show_detailed_text:
                        no_swap_status = Text(f"{array[j]} ≤ {array[j + 1]}, no swap needed", 
                                            font_size=39, color=GREEN, weight=BOLD)  # Increased font size by 5
                        no_swap_status.move_to([0, status_y, 0])
                        self.play(Transform(status_text, no_swap_status), run_time=0.5)
                
                # Reset fill colors to original
                self.play(
                    rectangles[j].animate.set_fill(RED, opacity=0.8),
                    rectangles[j + 1].animate.set_fill(RED, opacity=0.8),
                    run_time=0.2 if show_detailed_text else 0.1
                )
                
                if show_detailed_text:
                    self.wait(0.3)
                else:
                    self.wait(0.1)
            
            # Mark the last element of this pass as sorted (it's now in correct position)
            sorted_pos = n - i - 1
            self.play(
                rectangles[sorted_pos].animate.set_fill(GREEN, opacity=0.8),
                run_time=0.8 if show_detailed_text else 0.4
            )
            
            # Update brace to show sorted portion
            if i == 0:
                # Create initial brace for the first sorted element
                brace = Brace(rectangles[sorted_pos], DOWN, buff=0.2)
                brace_text = Text("Sorted", font_size=28, weight=BOLD, color=GREEN)
                brace_text.next_to(brace, DOWN, buff=0.2)
                self.play(ShowCreation(brace), ShowCreation(brace_text), run_time=1 if show_detailed_text else 0.5)
            else:
                # Expand brace to include newly sorted elements
                sorted_group = Group(*rectangles[sorted_pos:])
                new_brace = Brace(sorted_group, DOWN, buff=0.2)
                new_brace_text = Text("Sorted", font_size=28, weight=BOLD, color=GREEN)
                new_brace_text.next_to(new_brace, DOWN, buff=0.2)
                
                self.play(
                    Transform(brace, new_brace),
                    Transform(brace_text, new_brace_text),
                    run_time=0.8 if show_detailed_text else 0.4
                )
            
            if show_detailed_text:
                # End of pass status
                if swapped:
                    pass_complete_status = Text(f"Pass {pass_number} complete! Largest element bubbled to position {sorted_pos}", 
                                              font_size=39, color=GREEN, weight=BOLD)  # Increased font size by 5
                else:
                    pass_complete_status = Text(f"Pass {pass_number} complete! No swaps made - array is sorted!", 
                                              font_size=39, color=GOLD, weight=BOLD)  # Increased font size by 5
                pass_complete_status.move_to([0, status_y, 0])
                self.play(Transform(status_text, pass_complete_status), run_time=0.8)
                self.wait(1)
                
                # Fade out the status text after first iteration
                self.play(FadeOut(status_text), run_time=0.8)
                status_text = None
            else:
                self.wait(0.3)
            
            # Early termination if no swaps were made
            if not swapped:
                break
        
        # Remove comparison brace after sorting is complete
        if comparison_brace is not None:
            self.play(FadeOut(comparison_brace), FadeOut(comparison_brace_text), run_time=0.5)
        
        # Mark any remaining elements as sorted
        for k in range(n - i - 1):
            if rectangles[k].fill_opacity < 0.5:  # Not already marked as sorted
                self.play(rectangles[k].animate.set_fill(GREEN, opacity=0.8), run_time=0.3)
        
        # Final celebration
        final_status = Text("Array Successfully Sorted! 🎉", 
                          font_size=37, color=GOLD, weight=BOLD)  # Increased font size by 5
        final_status.move_to([0, status_y, 0])
        if status_text is None:
            self.play(ShowCreation(final_status), run_time=1)
        else:
            self.play(Transform(status_text, final_status), run_time=1)
        
        # Final brace for complete array
        complete_brace = Brace(Group(*rectangles), DOWN, buff=0.2)
        complete_brace_text = Text("Completely Sorted", font_size=20, weight=BOLD, color=GOLD)
        complete_brace_text.next_to(complete_brace, DOWN, buff=0.2)
        
        self.play(
            Transform(brace, complete_brace),
            Transform(brace_text, complete_brace_text),
            run_time=1.2
        )
        
        self.wait(2)
