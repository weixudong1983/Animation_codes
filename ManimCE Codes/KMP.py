from manim import *


class KMP(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(0.97)
        # Define the text and pattern
        text = "BABABABABCABABCABAB"  # String text
        pattern = "ABABCABAB"  # Pattern text

        # Create rectangles for text and pattern with larger cells
        text_rects = VGroup(
            *[Square(side_length=0.66, fill_color=TEAL_B, fill_opacity=1, stroke_color=DARK_BLUE) for _ in text])
        pattern_rects = VGroup(
            *[Square(side_length=0.66, fill_color=YELLOW, fill_opacity=1, stroke_color=DARK_BLUE) for _ in pattern])

        # Align rectangles in a row
        text_rects.arrange(RIGHT, buff=0)
        pattern_rects.arrange(RIGHT, buff=0)

        # Position the pattern above the text and move them further down
        pattern_rects.next_to(text_rects, UP, buff=1.125)
        pattern_rects.shift(DOWN * 1.1)
        text_rects.shift(DOWN * 1.4)

        # Add text to rectangles
        text_mobjects = VGroup(
            *[Text(char, font_size=30, color=BLACK).move_to(rect) for char, rect in zip(text, text_rects)])

        # Add indexes below each rectangle
        index_mobjects = VGroup(
            *[Text(str(i), font_size=24, color=WHITE).next_to(rect, DOWN, buff=0.14) for i, rect in
              enumerate(text_rects)])  # Add indexes below each rectangle

        index_mobjects2 = VGroup(
            *[Text(str(i), font_size=24, color=WHITE).next_to(rect, DOWN, buff=0.14) for i, rect in
              enumerate(pattern_rects)])

        # Correctly position pattern text in the center of the pattern squares
        pattern_mobjects = VGroup(
            *[Text(char, font_size=30, color=BLACK).move_to(rect) for char, rect in zip(pattern, pattern_rects)])

        # Group the pattern rectangles and texts together
        pattern_group = VGroup(pattern_rects, pattern_mobjects)

        # Create a title
        title = Text("Knuth-Morris-Pratt Algorithm", font_size=48).to_edge(UP, )
        code = Text("""
                if Matched:
                       i += 1
                       j += 1
                    """, font_size=25)
        code.shift(UP * 3)
        code2 = Text("""
                if Found:
                    j = LPS[j-1]

                    """, font_size=25).next_to(code, ORIGIN, )

        code3 = Text("""

                if NoMatch:
                    if j != 0:
                        j = LPS[j-1]
                    else:
                        i += 1
                    """, font_size=25).next_to(code2, ORIGIN, )

        # Set the permanent color of conditions to blue
        code[2:9].set_color(BLUE)
        code2[2:7].set_color(BLUE)
        code3[2:9].set_color(BLUE)
        code3[12:16].set_color(BLUE)

        code[10:].set_color(ORANGE)
        code2[8:].set_color(ORANGE)
        code3[17:27].set_color(ORANGE)
        code3[31:36].set_color(WHITE)

        # Updated "Found at" text with font size 26, color PURE_GREEN, and shifted to the left
        found_at_text = Text("Found at:", font_size=26, color=PURE_GREEN).next_to(index_mobjects, DOWN, buff=0.77)
        found_at_text.shift(LEFT * 2)  # Shift the text slightly to the left

        found_indices = VGroup()  # Group to hold the indices where the pattern is found

        # Add to the scene
        self.play(Create(text_rects), Create(pattern_group), Create(text_mobjects), Create(index_mobjects),
                  Write(title), Write(found_at_text), Create(index_mobjects2))

        self.wait(2)

        self.play(FadeOut(text_rects, text_mobjects, index_mobjects, found_at_text, title))

        self.wait(3)

        # Group the pattern and its indices
        pattern_with_indices = VGroup(pattern_group, index_mobjects2)

        # Animate the grouped pattern and indices growing bigger
        # self.play(pattern_with_indices.animate.scale(1.2))

        self.wait()

        self.play(self.camera.frame.animate.scale(0.7).shift(UP))

        self.wait()

        # Create empty rectangles with the same size as pattern_rects, but uncolored and empty
        empty_rects = VGroup(
            *[Square(side_length=0.66, stroke_color=DARK_BLUE) for _ in pattern]
        )
        empty_rects.arrange(RIGHT, buff=0)
        empty_rects.next_to(pattern_with_indices, UP, buff=0.15)
        text3 = Text("LPS =", font_size=27).next_to(empty_rects, LEFT, buff=0.73)
        text3.shift(RIGHT * 0.4)

        # Create a new.py group including the empty rectangles and add it to the scene
        self.play(Create(empty_rects))

        self.wait(2)

        # Function to compute LPS array
        def compute_lps_array(pattern):
            length = 0
            lps = [0] * len(pattern)
            i = 1
            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1
            return lps

        # Compute the LPS array for the pattern
        lps = compute_lps_array(pattern)

        # Function to highlight cells
        def highlight_cells(cells, color, wait_time=0.5, reset_color=YELLOW):
            for cell in cells:
                self.play(cell.animate.set_fill(color, opacity=1), run_time=0.5)
            self.wait(wait_time)
            # Reset color after highlighting
            for cell in cells:
                self.play(cell.animate.set_fill(reset_color, opacity=1), run_time=0.5)

        a = VGroup()
        # Process each cell of LPS array
        for i, num in enumerate(lps):
            # Determine the cells to highlight based on LPS value
            if num == 0:
                # No repetition, highlight current cell in red
                highlight_cells([pattern_rects[i]], RED)
            else:

                # Also highlight the part being compared in green
                compared_cells = [pattern_rects[j] for j in range(i - num + 1, i + 1)]
                self.play(*[cell.animate.set_fill(GREEN, opacity=1) for cell in compared_cells])
                # Pattern repeats, highlight all repeating cells in blue simultaneously
                repeating_cells = [pattern_rects[j] for j in range(num)]
                # Highlight repeating cells in blue
                self.play(*[cell.animate.set_fill(BLUE, opacity=1) for cell in repeating_cells])

                self.wait(0.5)

                # Reset colors of cells
                self.play(*[cell.animate.set_fill(YELLOW, opacity=1) for cell in repeating_cells + compared_cells])

            # Create mobject for the current LPS value and write it
            lps_text = Text(str(num), font_size=30, color=WHITE).move_to(empty_rects[i])
            # Add the lps_text to the group 'a'
            a.add(lps_text)

            self.play(Write(lps_text))

        self.wait(3)

        self.play(FadeOut(a))

        self.wait(2)

        a = pattern_with_indices.get_center()

        self.play(pattern_with_indices.animate.shift(DOWN * 0.6), )
        self.play(self.camera.frame.animate.shift(DOWN * 1.1))

        self.wait(2)

        lps_texts = []
        m = len(pattern)

        a = []

        # Initialize the LPS table with zeros and display them
        for i in range(m):
            lps_text = Text("0", font_size=30, color=WHITE).move_to(empty_rects[i])
            lps_texts.append(lps_text)
            a.append(Write(lps_text))

        self.play(*[a])

        self.wait(1)

        i_label = Text("i = 1", font_size=20, color=WHITE).next_to(pattern_rects[1], UP, buff=0.20)
        l_label = Text("l = 0", font_size=20, color=WHITE).next_to(pattern_rects[0], DOWN, buff=0.50)

        self.play(Create(i_label))
        self.play(Create(l_label))

        i = 1
        l = 0
        lps = [0] * m

        a = VGroup()

        first = Text("""
        if pattern[i] == pattern[l]:
            l += 1
            lps[i] = l
            i += 1""", t2c={'if': ORANGE, }).next_to(pattern_with_indices.get_center(), DOWN, ).scale(0.5).shift(
            DOWN * 0.23)

        second = Text("""
        else:
            if l != 0:
                l = lps[l - 1]
            else:
                i += 1
        """, t2c={'if': ORANGE, "else": ORANGE}).next_to(first, ORIGIN).scale(0.45)

        self.play(Create(first))

        c = True
        d = False

        while i < m:

            if pattern[i] == pattern[l]:

                self.play(pattern_rects[i].animate.set_fill(GREEN, opacity=1),
                          pattern_rects[l].animate.set_fill(GREEN, opacity=1)
                          , run_time=1)
                self.play(pattern_rects[i].animate.set_fill(YELLOW, opacity=1),
                          pattern_rects[l].animate.set_fill(YELLOW, opacity=1)
                          , run_time=0.7)

                if c and i > 1:
                    self.play(FadeOut(second), FadeIn(first))
                    c = False
                    d = True


                self.play(Indicate(first[:25]))
                self.play(Indicate(first[25:29]))

                l += 1
                lps[i] = l

                # Update l_label if l is within bounds
                if l < m:
                    self.play(
                        l_label.animate.become(
                            Text(f"l = {l}", font_size=20, color=WHITE).next_to(pattern_rects[l], DOWN, buff=0.50)))
                else:
                    # Hide l_label or move it off-screen if l is out of bounds
                    self.play(l_label.animate.fade_out())

                # Animate the transformation of the zero into the new value

                self.play(Indicate(first[29:37]))

                new_lps_text = Text(str(l), font_size=30, color=WHITE).move_to(empty_rects[i])
                self.play(Transform(lps_texts[i], new_lps_text))

                i += 1

                self.play(Indicate(first[37:]))

                # Update i_label if i is within bounds
                if i < m:
                    self.play(i_label.animate.become(
                        Text(f"i = {i}", font_size=20, color=WHITE).next_to(pattern_rects[i], UP, buff=0.20)))
                else:
                    # Hide i_label or move it off-screen if i is out of bounds
                    self.play(FadeOut(i_label))

            else:

                self.play(pattern_rects[i].animate.set_fill(RED, opacity=1),
                          pattern_rects[l].animate.set_fill(RED, opacity=1)
                          , run_time=1)
                self.play(pattern_rects[i].animate.set_fill(YELLOW, opacity=1),
                          pattern_rects[l].animate.set_fill(YELLOW, opacity=1)
                          , run_time=0.7)

                if d and i > 1:
                    self.play(FadeOut(first), FadeIn(second))
                    d = False
                    c = True
                if i == 1:
                    self.play(FadeIn(second), FadeOut(first))

                if l != 0:
                    l = lps[l - 1]

                    self.play(Indicate(second[5:22]))

                    # Update l_label if l is within bounds
                    if l < m:
                        self.play(
                            l_label.animate.become(
                                Text(f"l = {l}", font_size=20, color=WHITE).next_to(pattern_rects[l], DOWN, buff=0.50)))
                    else:
                        # Hide l_label or move it off-screen if l is out of bounds
                        self.play(FadeOut(l_label))

                else:
                    self.play(Indicate(second[27:]))

                    i += 1

                    # Update i_label if i is within bounds
                    if i < m:
                        self.play(i_label.animate.become(
                            Text(f"i = {i}", font_size=20, color=WHITE).next_to(pattern_rects[i], UP, buff=0.20)))
                    else:
                        # Hide i_label or move it off-screen if i is out of bounds
                        self.play(FadeOut(i_label))

        self.play(FadeOut(l_label, first))

        self.wait(2)

        self.play(pattern_with_indices.animate.shift(UP * 0.6), )
        self.play(self.camera.frame.animate.shift(UP * 1.1))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1 / 0.7).shift(DOWN*0.8))

        self.wait(2)


        self.play(Create(text3))

        self.wait(3)

        self.play(FadeIn(text_rects, text_mobjects, index_mobjects, found_at_text, title))

        self.wait(4)

        # Initialize index labels for text (i) and pattern (j) with starting values
        i_label = Text("i = 0", font_size=20, color=WHITE).next_to(text_rects[0], UP, buff=0.20)
        j_label = Text("j = 0", font_size=20, color=WHITE).next_to(pattern_rects[0], DOWN, buff=0.45)
        pattern_with_indices.add(j_label)

        index_mobjects3 = VGroup(
            *[Text(str(i), font_size=24, color=WHITE).next_to(empty_rects, UP, buff=0.14) for i, rect in
              enumerate(pattern_rects)])

        # Assuming lps is your computed LPS array and empty_rects are the squares representing the pi-table
        pi_table_mobjects = VGroup()
        for i, lps_value in enumerate(lps):
            lps_text = Text(str(lps_value), font_size=30, color=WHITE).move_to(empty_rects[i])
            pi_table_mobjects.add(lps_text)
            pi_table_mobjects.add(empty_rects, index_mobjects3)
            self.add(lps_text)  # Add each LPS text to the scene

        # Add labels to the scene
        self.play(Create(i_label), Create(j_label))

        i = 0
        j = 0
        # First, move the pattern vertically above the i-th cell of the text
        self.play(pattern_with_indices.animate.next_to(text_rects[i + 4], UP, buff=0.7))

        a = False

        b = False
        c = False

        while i < len(text):

            if i == 19:
                break

            if i >= len(text_rects):
                break

            # Then, calculate the horizontal shift required to align the j-th cell of the pattern with the i-th cell of the text
            horizontal_offset = text_rects[i].get_center()[0] - pattern_rects[j].get_center()[0]

            # Apply only the horizontal shift to the pattern
            self.play(pattern_with_indices.animate.shift(RIGHT * horizontal_offset))

            if a:
                for ii in range(j + 1, len(pattern)):
                    self.play(pattern_rects[ii].animate.set_fill(YELLOW, opacity=1), run_time=0.01)

            for ii in range(i - j):
                self.play(text_rects[ii].animate.set_fill(TEAL_B, opacity=1), run_time=0.01)

            if text[i] == pattern[j]:
                self.play(text_rects[i].animate.set_fill(GREEN, opacity=1),
                          pattern_rects[j].animate.set_fill(GREEN, opacity=1), run_time=0.5)
                if i > 0 and i < 18:
                    if c:
                        self.play(FadeOut(code3), FadeIn(code))
                        self.play(Indicate(code[2:9]))
                        self.play(Indicate(code[10:]))
                        c = False
                    elif b:
                        self.play(FadeOut(code2), FadeIn(code))
                        self.play(Indicate(code[2:9]))
                        self.play(Indicate(code[10:]))
                        b = False
                    else:
                        self.play(Indicate(code[2:9]))
                        self.play(Indicate(code[10:]))

                i += 1
                j += 1

                if j == len(pattern):

                    j = lps[j - 1] if j - 1 < len(lps) else 0
                    a = True
                    b = True
                    if i > 16:
                        match_start = i - len(pattern)

                        # Create the text for the found index
                        found_index_text = Text(str(match_start), font_size=20, color=WHITE)

                        # Position the new.py index text relative to the last one in 'found_indices'
                        if found_indices.submobjects:
                            # If there are already indices, position the new.py index to the right of the last one
                            found_index_text.next_to(found_indices, RIGHT, buff=0.2)
                        else:
                            # If this is the first index, position it next to 'found_at_text'
                            found_index_text.next_to(found_at_text, RIGHT, buff=0.2)

                        # Add animation for moving the index to the 'found_indices' group
                        self.play(TransformFromCopy(index_mobjects[match_start], found_index_text))

                        # Add the new.py index text to the 'found_indices' group
                        found_indices.add(found_index_text)
                    if i < 16:

                        # Update labels with new.py positions
                        self.play(i_label.animate.become(
                            Text(f"i = {i}", font_size=20, color=WHITE).next_to(text_rects[i], UP, buff=0.20)),
                            j_label.animate.become(
                            Text(f"j = {9}", font_size=20, color=WHITE).next_to(pattern_rects[8], DOWN, buff=0.45)))
                        match_start = i - len(pattern)

                        # Create the text for the found index
                        found_index_text = Text(str(match_start), font_size=20, color=WHITE)

                        # Position the new.py index text relative to the last one in 'found_indices'
                        if found_indices.submobjects:
                            # If there are already indices, position the new.py index to the right of the last one
                            found_index_text.next_to(found_indices, RIGHT, buff=0.2)
                        else:
                            # If this is the first index, position it next to 'found_at_text'
                            found_index_text.next_to(found_at_text, RIGHT, buff=0.2)

                        # Add animation for moving the index to the 'found_indices' group
                        self.play(TransformFromCopy(index_mobjects[match_start], found_index_text))

                        # Add the new.py index text to the 'found_indices' group
                        found_indices.add(found_index_text)

                        self.play(FadeOut(code), FadeIn(code2))
                        self.play(Indicate(code2[2:7]))
                        self.play(Indicate(code2[8:]))
                        self.play(empty_rects[j - 1 + 5].animate.set_fill(PINK, opacity=1),
                                  run_time=1) if j > 0 else None
                        self.play(empty_rects[j - 1 + 5].animate.set_fill(PINK, opacity=0),
                                  run_time=1) if j > 0 else None
                    aa = Text('STOP', color=PURE_RED).next_to(code, ORIGIN)

                    if i > 16:
                        self.play(ReplacementTransform(code, aa))












            else:
                self.play(text_rects[i].animate.set_fill(RED, opacity=1),
                          pattern_rects[j].animate.set_fill(RED, opacity=1), run_time=0.5)

                if i > 0:
                    if True:
                        self.play(FadeOut(code), FadeIn(code3))
                        self.play(Indicate(code3[2:9]))
                        self.play(Indicate(code3[12:16]))
                        self.play(Indicate(code3[17:27]))
                        c = True

                else:
                    self.play(FadeOut(title), FadeIn(code3))
                    self.play(Indicate(code3[2:9]))
                    self.play(Indicate(code3[32:36]))
                    self.play(Indicate(code3[37:40]))
                    c = True

                if j > 0 and j - 1 < len(lps):
                    j = lps[j - 1]
                    a = True
                    self.play(empty_rects[j - 1 + 2].animate.set_fill(PINK, opacity=1), run_time=1) if j > 0 else None
                    self.play(empty_rects[j - 1 + 2].animate.set_fill(PINK, opacity=0), run_time=1) if j > 0 else None


                else:
                    i += 1
            if i == 19:
                self.wait(4)
                break

            # Update i and j labels with their current values
            i_label_text = f"i = {i}"
            j_label_text = f"j = {j}"

            # Ensure i is within the bounds of text_rects
            if 0 <= i < len(text_rects):
                i_label_pos = text_rects[i]
            else:
                i_label_pos = text_rects[-1]  # Use the last rectangle if i is out of bounds

            # Ensure j is within the bounds of pattern_rects
            if 0 <= j < len(pattern_rects):
                j_label_pos = pattern_rects[j]
            else:
                j_label_pos = pattern_rects[-1]  # Use the last rectangle if j is out of bounds

            # Update labels with new.py positions
            self.play(i_label.animate.become(
                Text(i_label_text, font_size=20, color=WHITE).next_to(i_label_pos, UP, buff=0.20)))
            self.play(j_label.animate.become(
                Text(j_label_text, font_size=20, color=WHITE).next_to(j_label_pos, DOWN, buff=0.45)))

        self.wait(3)

