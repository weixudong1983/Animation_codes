from manimlib import *

class LongestCommonSubsequence(Scene):
    def construct(self):
        # Problem statement
        title = Text("Longest Common Subsequence", font_size=48)
        title.to_edge(UP)
        self.wait(1)  # Wait longer for viewers to read
        
        # Input strings
        s2 = "abcdef"
        s1 = "aacf"
        
        problem_desc = Text(f"Finding LCS between \"{s1}\" and \"{s2}\"", font_size=32)
        problem_desc.next_to(title, DOWN, buff=0.5)
        self.wait(1.5)  # Give viewers time to read
        
        # DP table setup
        n, m = len(s1), len(s2)
        cell_size = 0.65
        table = VGroup()
        
        # Create cells for the table
        cells = {}
        for i in range(n + 1):
            for j in range(m + 1):
                cell = Square(side_length=cell_size)
                cell.set_stroke(WHITE, 2)
                cell.move_to(RIGHT * j * cell_size + DOWN * i * cell_size)
                table.add(cell)
                cells[(i, j)] = cell
        
        # Add row and column headers
        row_headers = VGroup()
        for i in range(n + 1):
            if i == 0:
                char = ""  # Empty set symbol for initial row
            else:
                char = s1[i-1]
            label = Text(char, font_size=24)
            label.next_to(cells[(i, 0)], LEFT, buff=0.2)
            row_headers.add(label)
        
        col_headers = VGroup()
        for j in range(m + 1):
            if j == 0:
                char = ""  # Empty set symbol for initial column
            else:
                char = s2[j-1]
            label = Text(char, font_size=24)
            label.next_to(cells[(0, j)], UP, buff=0.2)
            col_headers.add(label)
        
        # Center the table and add some space at the top
        table_group = VGroup(table, row_headers, col_headers)
        table_group.center()
        table_group.shift(UP * 1.1).scale(1.3)
        
        # Show the table
        self.play(
            FadeIn(table),
            Write(row_headers),
            Write(col_headers)
        )
        self.embed()
        self.wait(1.5)  # Pause to let viewers see the table structure

        # Initialize the dp table values
        dp_values = {}
        dp_texts = {}
        
        # Initialize with zeros
        for i in range(n + 1):
            for j in range(m + 1):
                dp_values[(i, j)] = 0
                text = Text("0", font_size=34)
                text.move_to(cells[(i, j)].get_center())
                dp_texts[(i, j)] = text
        
        # Show the initial zeros
        self.play(
            *[Write(dp_texts[(i, 0)]) for i in range(n + 1)],
            *[Write(dp_texts[(0, j)]) for j in range(1, m + 1)]
        )
        self.wait(1)  # Pause to let viewers see the initial values
        
        # Create black background for explanation text
        explanation_bg = Rectangle(
            width=11,
            height=1.37,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=2,
            stroke_color=YELLOW
        )
        explanation_bg.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(explanation_bg))
        
        # Explanation text area
        current_explanation = None
        
        # Function to update explanation
        def update_explanation(text):
            nonlocal current_explanation
            new_explanation = Text(text, font_size=34)
            new_explanation.move_to(explanation_bg.get_center())
            if current_explanation:
                self.play(ReplacementTransform(current_explanation, new_explanation))
            else:
                self.play(Write(new_explanation))
            current_explanation = new_explanation
            self.wait(1)  # Pause to let viewers read explanation
        
        update_explanation("Starting DP table filling process")
        self.wait(0.5)  # Pause before starting the algorithm
        
        # Create persistent rectangles for highlighting characters
        row_rect = SurroundingRectangle(row_headers[1],)
        col_rect = SurroundingRectangle(col_headers[1],)
        self.play(ShowCreation(row_rect), ShowCreation(col_rect))

        # Fill the dp table
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Highlight current cells being compared
                self.play(
                    cells[(i, j)].animate.set_fill(BLUE, opacity=0.3),
                    cells[(i-1, j)].animate.set_fill(YELLOW, opacity=0.3),
                    cells[(i, j-1)].animate.set_fill(YELLOW, opacity=0.3),
                    cells[(i-1, j-1)].animate.set_fill(YELLOW, opacity=0.3),
                    run_time=0.5
                )
                self.wait(0.5)  # Pause to let viewers see highlighted cells
                
                # Move the rectangles to highlight current characters
                self.play(
                    row_rect.animate.move_to(row_headers[i].get_center()),
                    col_rect.animate.move_to(col_headers[j].get_center()),
                    run_time=0.5
                )
                
                # Change rectangle colors based on character match
                if s1[i-1] == s2[j-1]:
                    self.play(
                        row_rect.animate.set_color(GREEN),
                        col_rect.animate.set_color(GREEN),
                        run_time=0.3
                    )
                    update_explanation(f"Characters match: {s1[i-1]} = {s2[j-1]}\nTake diagonal value + 1")
                    dp_values[(i, j)] = 1 + dp_values[(i-1, j-1)]
                    
                    # Highlight the diagonal cell with special color
                    self.play(
                        cells[(i-1, j-1)].animate.set_fill(GREEN, opacity=0.5),
                        run_time=0.5
                    )
                    self.wait(0.5)  # Pause to let viewers see the diagonal cell
                else:
                    self.play(
                        row_rect.animate.set_color(RED),
                        col_rect.animate.set_color(RED),
                        run_time=0.3
                    )
                    update_explanation(f"Characters don't match: {s1[i-1]} ≠ {s2[j-1]}\nTake max of left and top cells")
                    dp_values[(i, j)] = max(dp_values[(i-1, j)], dp_values[(i, j-1)])
                    
                    # Highlight both left and top cells, with brighter color for the max
                    self.play(
                        cells[(i-1, j)].animate.set_fill(YELLOW, opacity=0.3),
                        cells[(i, j-1)].animate.set_fill(YELLOW, opacity=0.3),
                        run_time=0.5
                    )
                    
                    # Highlight the max value with a brighter color
                    if dp_values[(i-1, j)] >= dp_values[(i, j-1)]:
                        self.play(
                            cells[(i-1, j)].animate.set_fill(GREEN, opacity=0.5),
                            run_time=0.5
                        )
                    else:
                        self.play(
                            cells[(i, j-1)].animate.set_fill(GREEN, opacity=0.5),
                            run_time=0.5
                        )
                    self.wait(0.5)  # Pause to let viewers see which cell is being used
                
                # Create and display new value
                new_text = Text(str(dp_values[(i, j)]), font_size=34)
                new_text.move_to(cells[(i, j)].get_center())
                
                self.play(
                    Write(new_text),
                    run_time=0.5
                )
                dp_texts[(i, j)] = new_text
                self.wait(0.5)  # Pause to let viewers see the new value
                
                # Reset cell colors
                self.play(
                    cells[(i, j)].animate.set_fill(opacity=0),
                    cells[(i-1, j)].animate.set_fill(opacity=0),
                    cells[(i, j-1)].animate.set_fill(opacity=0),
                    cells[(i-1, j-1)].animate.set_fill(opacity=0),
                    run_time=0.5
                )
                self.wait(0.3)  # Slight pause before next iteration
        
        # Fade out the character highlighting rectangles after filling the table
        self.play(FadeOut(row_rect), FadeOut(col_rect))
        
        # Highlight the final result
        final_cell = cells[(n, m)]
        final_value = dp_texts[(n, m)]
        
        self.play(
            final_cell.animate.set_fill(PURPLE, opacity=0.5),
            final_value.animate.scale(1.5),
            run_time=1
        )
        self.wait(1)  # Pause to let viewers see the final result
        
        final_text = f"LCS Length: {dp_values[(n, m)]}"
        update_explanation(final_text)
        self.wait(1)  # Pause to let viewers see the final result
        
        # Optional: Trace back to find the actual subsequence
        if dp_values[(n, m)] > 0:
            lcs = []
            i, j = n, m
            path_cells = []
            
            while i > 0 and j > 0:
                if s1[i-1] == s2[j-1]:
                    lcs.append(s1[i-1])
                    path_cells.append((i, j))
                    i -= 1
                    j -= 1
                elif dp_values[(i-1, j)] > dp_values[(i, j-1)]:
                    i -= 1
                else:
                    j -= 1
            
            lcs = lcs[::-1]  # Reverse to get the correct order
            
            # Show the path
            update_explanation(f"Tracing back to find LCS: {''.join(lcs)}")
            self.wait(1)  # Pause to let viewers understand we're tracing back
            
            for pos in path_cells:
                self.play(
                    cells[pos].animate.set_fill(RED, opacity=0.7),
                    run_time=0.7
                )
                self.wait(0.5)  # Pause between each step of the path
        
        self.wait(2)  # Final pause before the animation ends

# To run this animation, use:
# manimgl lcs_animation.py LongestCommonSubsequence
