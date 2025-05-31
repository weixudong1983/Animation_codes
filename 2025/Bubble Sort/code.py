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
        array_y_pos = -0.3  # Consistent Y position for array
        
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
            rect.move_to([x_pos, array_y_pos, 0])
            
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
        
        # Create comparison group (initially empty)
        comparison_group = None
        
        self.wait(1)
        
        # Bubble Sort Algorithm
        pass_number = 0
        
        for i in range(n - 1):
            pass_number += 1
            swapped = False
            
            # Show detailed text animations only for first pass
            show_detailed_text = (pass_number == 1)
            
            # Compare adjacent elements
            for j in range(n - i - 1):
                # Create comparison brace for the two elements being compared
                comparing_elements = Group(rectangles[j], rectangles[j + 1])
                new_comparison_brace = Brace(comparing_elements, DOWN, buff=0.3)
                new_comparison_text = Text("Comparing", font_size=26, weight=BOLD, color=BLUE)
                new_comparison_text.next_to(new_comparison_brace, DOWN, buff=0.2)
                new_comparison_group = VGroup(new_comparison_brace, new_comparison_text).next_to(comparing_elements, DOWN, buff=0.3)
                
                # Highlight the two elements being compared using fill color
                self.play(
                    rectangles[j].animate.set_fill(PURPLE, opacity=0.9),
                    rectangles[j + 1].animate.set_fill(PURPLE, opacity=0.9),
                    run_time=0.4 if show_detailed_text else 0.4
                )
                
                # Show or update comparison group
                if comparison_group is None:
                    comparison_group = new_comparison_group
                    self.play(
                        ShowCreation(comparison_group),
                        run_time=0.5 if show_detailed_text else 0.5
                    )
                else:
                    # Move comparison group to new position

                    self.play(
                        comparison_group.animate.next_to(comparing_elements, DOWN, buff=0.3),
                        run_time=0.5 if show_detailed_text else 0.5
                    )
                
                if show_detailed_text:
                    self.wait(0.3)
                else:
                    self.wait(0.1)
                
                # Check if swap is needed
                if array[j] > array[j + 1]:
                    swapped = True
                    
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
                    
                    # Calculate target positions for swap (maintaining array_y_pos)
                    target_j = start_x + (j + 1) * (rect_width + buff_between)
                    target_j_plus_1 = start_x + j * (rect_width + buff_between)
                    
                    # Swap positions horizontally
                    self.play(
                        rectangles[j].animate.move_to([target_j, array_y_pos + lift_height, 0]),
                        texts[j].animate.move_to([target_j, array_y_pos + lift_height, 0]),
                        rectangles[j + 1].animate.move_to([target_j_plus_1, array_y_pos + lift_height, 0]),
                        texts[j + 1].animate.move_to([target_j_plus_1, array_y_pos + lift_height, 0]),
                        run_time=1.2 if show_detailed_text else 0.6,
                        rate_func=smooth
                    )
                    
                    # Lower both elements back to consistent array position
                    self.play(
                        rectangles[j].animate.move_to([target_j, array_y_pos, 0]),
                        texts[j].animate.move_to([target_j, array_y_pos, 0]),
                        rectangles[j + 1].animate.move_to([target_j_plus_1, array_y_pos, 0]),
                        texts[j + 1].animate.move_to([target_j_plus_1, array_y_pos, 0]),
                        run_time=0.8 if show_detailed_text else 0.4,
                        rate_func=smooth
                    )
                    
                    # Update arrays and references
                    array[j], array[j + 1] = array[j + 1], array[j]
                    rectangles[j], rectangles[j + 1] = rectangles[j + 1], rectangles[j]
                    texts[j], texts[j + 1] = texts[j + 1], texts[j]
                    
                else:
                    if show_detailed_text:
                        self.wait(0.3)
                    else:
                        self.wait(0.1)
                
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
                # Create initial brace for the first sorted element - positioned ABOVE elements
                brace = Brace(rectangles[sorted_pos], UP, buff=0.3)
                brace_text = Text("Sorted", font_size=28, weight=BOLD, color=GREEN)
                brace_text.next_to(brace, UP, buff=0.1)
                brace_group = VGroup(brace, brace_text)
                self.play(ShowCreation(brace_group), run_time=1 if show_detailed_text else 0.5)
            else:
                # Expand brace to include newly sorted elements using ReplacementTransform
                sorted_group = Group(*rectangles[sorted_pos:])
                new_brace = Brace(sorted_group, UP, buff=0.3)
                new_brace_text = Text("Sorted", font_size=28, weight=BOLD, color=GREEN)
                new_brace_text.next_to(new_brace, UP, buff=0.1)
                new_brace_group = VGroup(new_brace, new_brace_text)
                
                self.play(
                    ReplacementTransform(brace_group, new_brace_group),
                    run_time=0.8 if show_detailed_text else 0.4
                )
                brace_group = new_brace_group
                brace = new_brace
                brace_text = new_brace_text
            
            if show_detailed_text:
                self.wait(1)
            else:
                self.wait(0.3)
            
            # Early termination if no swaps were made
            if not swapped:
                break
        
        # Remove comparison group after sorting is complete
        if comparison_group is not None:
            self.play(FadeOut(comparison_group), run_time=0.5)
        
        # Mark any remaining elements as sorted
        for k in range(n - i - 1):
            if rectangles[k].fill_color != GREEN:  # Not already marked as sorted
                self.play(rectangles[k].animate.set_fill(GREEN, opacity=0.8), run_time=0.3)
        
        # Final celebration
        final_status = Text("Array Successfully Sorted! 🎉", 
                          font_size=37, color=GOLD, weight=BOLD).set_color(GOLD_C)
        final_status.move_to([0, -2, 0]).shift(DOWN*0.22)
        self.play(ShowCreation(final_status), run_time=1)
        
        # Final brace for complete array using ReplacementTransform
        final_brace = Brace(Group(*rectangles), UP, buff=0.3)
        final_brace_text = Text("Sorted", font_size=28, weight=BOLD, color=GREEN)
        final_brace_text.next_to(final_brace, UP, buff=0.1)
        final_brace_group = VGroup(final_brace, final_brace_text)
        
        self.play(
            ReplacementTransform(brace_group, final_brace_group),
            run_time=1.2
        )
        
        self.wait(2)
