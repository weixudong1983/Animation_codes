from manimlib import *
import random


# Define a custom Star class since it's not a default Mobject
class Star(Polygon):
    def __init__(self, n=5, **kwargs):
        # Calculate vertices for a regular n-pointed star
        outer_radius = 1
        inner_radius = 0.5 # Adjust for pointiness
        
        outer_vertices = [
            np.array([
                outer_radius * np.cos(2 * PI * k / n),
                outer_radius * np.sin(2 * PI * k / n),
                0
            ]) for k in range(n)
        ]
        
        inner_vertices = [
            np.array([
                inner_radius * np.cos(2 * PI * (k + 0.5) / n),
                inner_radius * np.sin(2 * PI * (k + 0.5) / n),
                0
            ]) for k in range(n)
        ]

        # Interleave vertices to form the star shape
        vertices = []
        for i in range(n):
            vertices.append(outer_vertices[i])
            vertices.append(inner_vertices[i])
        
        # Set fill properties to match the stroke color by default
        if 'color' in kwargs and 'fill_color' not in kwargs:
            kwargs['fill_color'] = kwargs['color']
        if 'fill_opacity' not in kwargs:
            kwargs['fill_opacity'] = 1.0
            
        super().__init__(*vertices, **kwargs)
        self.scale(0.5) # Default scale to match Circle size better


class BayesRule(Scene):
    
    def construct(self):
        self.camera.frame.scale(1.4).shift(DOWN*2.1)
        # Create all shapes
        all_shapes = []
        
        # Create 3 stars: 2 green, 1 red
        for i in range(2):
            star = Star(color=GREEN, fill_opacity=1)
            all_shapes.append(star)
        
        star = Star(color=RED, fill_opacity=1)
        all_shapes.append(star)
        
        # Create 7 circles: 2 green, 5 red
        for i in range(2):
            circle = Circle(color=GREEN, fill_opacity=1, stroke_color=GREEN)
            circle.scale(0.5)
            all_shapes.append(circle)
        
        for i in range(5):
            circle = Circle(color=RED, fill_opacity=1, stroke_color=RED)
            circle.scale(0.5)
            all_shapes.append(circle)
        
        # Shuffle shapes randomly
        random.shuffle(all_shapes)
        
        # Define 2x5 grid parameters
        rows = 2
        cols = 5
        x_spacing = 2.5
        y_spacing = 1.6
        
        # Calculate grid positions
        x_positions = np.linspace(-x_spacing * (cols-1)/2, x_spacing * (cols-1)/2, cols)
        y_positions = [y_spacing / 2, -y_spacing / 2]  # Top row, bottom row
        
        # Create grid coordinates
        grid_positions = []
        for y in y_positions:
            for x in x_positions:
                grid_positions.append([x, y, 0])
        
        # Create the enclosing box
        box_width = x_spacing * (cols - 1) + 2.0  # Grid width + padding
        box_height = y_spacing + 2.0  # Grid height + padding
        
        enclosing_box = Rectangle(
            width=box_width,
            height=box_height,
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=0  # Transparent fill so shapes are visible
        )
        enclosing_box.move_to(ORIGIN).set_color(GREY)
        
        # Display the box first
        self.play(ShowCreation(enclosing_box), run_time=1)
        self.wait(0.5)
        
        # Assign shapes to grid positions
        for i, shape in enumerate(all_shapes):
            shape.move_to(grid_positions[i])
        
        # Display all shapes using GrowFromCenter
        for shape in all_shapes:
            self.play(GrowFromCenter(shape), run_time=0.3)
        
        self.wait(2)


        probability_text = Tex(r"P(star) = \frac{3}{10}",color=BLACK).set_color(WHITE)
        probability_text.next_to(enclosing_box, DOWN, buff=1.5).shift(DOWN).scale(3)

        self.play(Write(probability_text[:7]))
        self.wait(2)

        rect = SurroundingRectangle(all_shapes[2], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect2 = SurroundingRectangle(all_shapes[6], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect3 = SurroundingRectangle(all_shapes[7], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        self.play(ShowCreation(rect), ShowCreation(rect2), ShowCreation(rect3), run_time=1.5)
        self.wait(2)

        self.play(FadeIn(probability_text[7:]), run_time=1.8)
        self.wait(2)

        self.play(FadeOut(probability_text), 
                  FadeOut(rect), FadeOut(rect2), FadeOut(rect3), run_time=1.5)


        probability_text = Tex(r"P(Green) = \frac{4}{10}",color=BLACK).set_color(WHITE)
        probability_text.next_to(enclosing_box, DOWN, buff=1.5).shift(DOWN).scale(3)

        self.play(Write(probability_text[:8]))
        self.wait(2)

        rect = SurroundingRectangle(all_shapes[2], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect2 = SurroundingRectangle(all_shapes[4], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect3 = SurroundingRectangle(all_shapes[5], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect4 = SurroundingRectangle(all_shapes[7], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        self.play(ShowCreation(rect), ShowCreation(rect2), ShowCreation(rect3), ShowCreation(rect4), run_time=1.5)
        self.wait(2)


        self.play(FadeIn(probability_text[8:]), run_time=1.8)
        self.wait(2)

        self.play(FadeOut(probability_text), 
                  FadeOut(rect), FadeOut(rect2), FadeOut(rect3), FadeOut(rect4), run_time=1.5)
        
        self.play(self.camera.frame.animate.shift(RIGHT*2))

        question = ImageMobject("question.png").next_to(enclosing_box, RIGHT, buff=0).scale(0.8)

        self.play(FadeIn(question))

        self.wait(2)

        text = Text("P(star|Green) = ").next_to(enclosing_box, DOWN, buff=1.8).shift(DOWN+LEFT*3.06).scale(2)

        self.play(Write(text))
        self.wait(2)

        temp = Text("Total Green Stars").next_to(text, RIGHT, buff=1).scale(2).shift(UP*0.5+RIGHT*2.2)
        line = Line(LEFT*3, RIGHT*3, stroke_width=6).next_to(temp, DOWN, buff=0.4).scale(1.6)
        temp_1 = Text("Total Green").next_to(line, DOWN, buff=0.1).scale(2).shift(DOWN*0.3)

        self.play(Write(temp), Write(line), )
        self.play(Write(temp_1))

        self.wait(2)

        rect = SurroundingRectangle(all_shapes[2], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)
        rect2 = SurroundingRectangle(all_shapes[7], color=YELLOW, buff=0.1, stroke_width=5).scale(1.13)

        self.play(ShowCreation(rect), ShowCreation(rect2), run_time=1.5)
        self.wait(2)

        a = rect.copy()
        b = rect2.copy()

        self.play(a.animate.move_to(all_shapes[4]), b.animate.move_to(all_shapes[5]), run_time=1.5)

        self.wait(2)

        self.play(Transform(temp, Text("2").scale(2).move_to(temp.get_center())),
                  Transform(temp_1, Text("4").scale(2).move_to(temp_1.get_center())),
                  Transform(line, Line(LEFT*0.4, RIGHT*0.4, stroke_width=6).move_to(line).scale(1.6)),
                  text.animate.shift(RIGHT*4),
                  run_time=1.5)
        
        self.wait(2)



from manimlib import *

class BayesTheoremDerivation(Scene):
    def construct(self):
        self.camera.frame.scale(0.8).shift(UP*1.73)
        # STEP 1: Complete equation in one line
        eq1 = Tex(r"P(Star \mid Green) = \frac{P(Star \cap Green)}{P(Green)}").scale(1.2).to_edge(UP)
        self.play(Write(eq1))
        self.wait(1)

        # STEP 2: Second complete equation in one line
        eq2 = Tex(r"P(Green \mid Star) = \frac{P(Green \cap Star)}{P(Star)}").scale(1.1).next_to(eq1, DOWN, buff=1.2)
        self.play(Write(eq2))
        self.wait(1.2)


        # STEP 3: Isolate intersection - complete equation
        isolate = Tex(r"P(Green \cap Star) = P(Green \mid Star) \cdot P(Star)")
        isolate.move_to(eq1)
        self.play(Transform(eq1, isolate))
        self.wait(1.5)

        # STEP 4: Final Bayes theorem - complete equation
        final_eq = Tex(r"P(Star \cap Green) = P(Star \mid Green) \cdot P(Green)").move_to(eq2)
        self.play(Transform(eq2, final_eq))
        self.wait(2)

        rect1 = SurroundingRectangle(eq1[:14], color=YELLOW, stroke_width=6)
        rect2 = SurroundingRectangle(eq2[:13], color=YELLOW, stroke_width=6)

        self.play(
            ShowCreation(rect1),
            ShowCreation(rect2),
            run_time=1
        )

        self.wait(2)

        self.play(
            Transform(rect1, SurroundingRectangle(eq1[15:], color=YELLOW)),
            Transform(rect2, SurroundingRectangle(eq2[14:], color=YELLOW)), run_time=1)

        # Box it

        self.wait(2)

        final_eq = Tex(r"P(Star \mid Green) = \frac{P(Green \mid Star) \cdot P(Star)}{P(Green)}").move_to(VGroup(eq1, eq2).get_center()).scale(1)
        self.play(ReplacementTransform(VGroup(eq2, eq1), final_eq),Uncreate(rect1), Uncreate(rect2))
        self.wait(1.5)

        box = SurroundingRectangle(final_eq, color="#00FF00", stroke_width=6).scale(1.06)
        self.play(ShowCreation(box))
        self.wait(2)
        self.play(Uncreate(box))


        # STEP 5: Explain the Denominator
        denom_explain = Tex(r"P(Green) = P(Green \mid Star) \cdot P(Star) + P(Green \mid \neg Star) \cdot P(\neg Star)").scale(0.95*0.7)
        denom_explain.next_to(final_eq, DOWN, buff=1.5)
        self.play(Write(denom_explain), self.camera.frame.animate.shift(DOWN))
        self.wait(3)

        brace = Brace(denom_explain[:8], DOWN, buff=0.2).set_color(YELLOW)
        self.play(GrowFromCenter(brace))

        self.wait(1.5)

        self.play(Transform(brace, Brace(denom_explain[9:30], DOWN, buff=0.2).set_color(YELLOW)))
        
        self.wait(1.5)

        self.play(Transform(brace, Brace(denom_explain[31:], DOWN, buff=0.2).set_color(YELLOW)))

        self.wait(1.5)


        # STEP 6: Final transformed full Bayes Equation with expanded denominator
        expanded_bayes = Tex(
            r"P(Star \mid Green) = \frac{P(Green \mid Star) \cdot P(Star)}{P(Green \mid Star) \cdot P(Star) + P(Green \mid \neg Star) \cdot P(\neg Star)}"
        ).scale(0.9)
        expanded_bayes.move_to(final_eq.get_center()).scale(0.9*0.9*0.87)

        self.play(
            ReplacementTransform(VGroup(final_eq, denom_explain), expanded_bayes),
            self.camera.frame.animate.shift(UP),
            FadeOut(brace)
        )
        self.wait(2)



        equation_A_B = Tex(r"P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B \mid A) \cdot P(A) + P(B \mid \neg A) \cdot P(\neg A)}").scale(1.3*0.9*0.9*0.9).move_to(expanded_bayes)
        self.play(Transform(expanded_bayes, equation_A_B))
        self.wait(2)

        self.play(expanded_bayes[-16].animate.set_color(RED), 
                  expanded_bayes[-5].animate.set_color(RED),)
        
        self.wait(2)


        temp  =  Tex(r"P(A \mid x_1, x_2, \ldots, x_n) = \frac{P(x_1, x_2, \ldots, x_n \mid A) \cdot P(A)}{P(x_1, x_2, \ldots, x_n)}").scale(0.9).move_to(expanded_bayes)
        self.play(Transform(expanded_bayes, temp))
        self.wait(2)


        
        # STEP 7: Clear for new example
        self.play(FadeOut(expanded_bayes))


        # STEP 1: General form with 3 features
        general_eq = Tex(
            r"P(A \mid x_1, x_2, x_3) = \frac{P(x_1, x_2, x_3 \mid A) \cdot P(A)}{P(x_1, x_2, x_3)}"
        ).scale(1.2).move_to(expanded_bayes)
        self.play(Write(general_eq) ,self.camera.frame.animate.scale(1.1))
        self.wait(2)


        # Expand the numerator of non-naive Bayes
        full_non_naive = Tex(
            r"P(A \mid x_1, x_2, x_3) = \frac{P(x_1 \mid A) \cdot P(x_2 \mid x_1, A) \cdot P(x_3 \mid x_1, x_2, A) \cdot P(A)}{P(x_1, x_2, x_3)}"
        ).scale(1.1).move_to(general_eq)
        self.play(ReplacementTransform(general_eq, full_non_naive), self.camera.frame.animate.scale(1.1**3))
        self.wait(3)

        brace = Brace(full_non_naive[14:21], UP, buff=0.2).set_color(YELLOW)
        self.play(GrowFromCenter(brace))

        self.wait(2)

        self.play(Transform(brace, Brace(full_non_naive[22:32], UP, buff=0.2).set_color(YELLOW)))
        self.wait(2)
        self.play(Transform(brace, Brace(full_non_naive[33:46], UP, buff=0.2).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace, Brace(VGroup(full_non_naive[-11:-1], full_non_naive[-1]), DOWN, buff=0.2).set_color(YELLOW)))

        # Voiceover explanation point: explain full dependencies in numerator
        # Now expand the denominator explicitly

        denom_expanded = Tex(r"P(x_1, x_2, x_3) = P(x_1, x_2, x_3 \mid A) \cdot P(A) + P(x_1, x_2, x_3 \mid \neg A) \cdot P(\neg A)").scale(0.9).next_to(full_non_naive, DOWN, buff=1).shift(DOWN).scale(1.2)
        self.play(Write(denom_expanded), self.camera.frame.animate.shift(DOWN))
        self.wait(2)

        self.play(Transform(brace, Brace(denom_expanded[12:30], DOWN, buff=0.2).set_color(YELLOW)))
        self.wait(2)
        self.play(Transform(brace, Brace(denom_expanded[31:], DOWN, buff=0.2).set_color(YELLOW)))
        self.wait(2)


        self.play(FadeOut(denom_expanded), FadeOut(brace), self.camera.frame.animate.shift(UP))

        # Now simplify into Naive form
        naive_eq = Tex(
            r"P(A \mid x_1, x_2, x_3) = \frac{P(x_1 \mid A) \cdot P(x_2 \mid A) \cdot P(x_3 \mid A) \cdot P(A)}{P(x_1, x_2, x_3)}"
        ).scale(1.1).move_to(full_non_naive)
        self.play(ReplacementTransform(full_non_naive, naive_eq), self.camera.frame.animate.scale(0.9*0.9*1.08))
        self.wait(3)

        brace = Brace(naive_eq[14:21], UP, buff=0.2).set_color(YELLOW)
        self.play(GrowFromCenter(brace))

        self.wait()

        self.play(Transform(brace, Brace(naive_eq[22:29], UP, buff=0.2).set_color(YELLOW)))
        self.wait()

        self.play(Transform(brace, Brace(naive_eq[30:37], UP, buff=0.2).set_color(YELLOW)))
        self.wait(3)



class NaiveBayesTableScene(Scene):
    def construct(self):

        self.camera.frame.scale(1.31).shift(0.7*UP)
        # ------------------------------------------------------------- #
        # 1. data (updated to match spreadsheet with Humidity column)
        # ------------------------------------------------------------- #
        data = [
            ["Day",  "Outlook",   "Humidity", "Windy", "Play"],
            ["1",    "Sunny",     "High",     "False", "No"],
            ["2",    "Sunny",     "Normal",   "True",  "Yes"],
            ["3",    "Overcast",  "High",     "False", "Yes"],
            ["4",    "Rain",      "Normal",   "False", "Yes"],
            ["5",    "Rain",      "Normal",   "True",  "No"],
            ["6",    "Overcast",  "Low",      "True",  "Yes"],
            ["7",    "Sunny",     "High",     "True",  "No"],
            ["8",    "Rain",      "Low",      "True",  "Yes"],
        ]

        # Updated to include color for Humidity column
        column_colors = [BLUE, PURPLE, PINK, ORANGE, TEAL]
        yes_color, no_color = GREEN, RED

        # ------------------------------------------------------------- #
        # 2. build Text objects (headers already bold + black)
        # ------------------------------------------------------------- #
        text_rows = [
            [
                # Row 0 (headers) → bold & black in constructor
                Text(str(cell), weight="BOLD", color=BLACK).set_color(BLACK) if r == 0 else Text(str(cell))
                for c, cell in enumerate(row)
            ]
            for r, row in enumerate(data)
        ]
        n_rows, n_cols = len(text_rows), len(text_rows[0])

        # ------------------------------------------------------------- #
        # 3. geometry
        # ------------------------------------------------------------- #
        col_w = [max(text_rows[r][c].get_width() for r in range(n_rows)) + 0.8
                 for c in range(n_cols)]
        row_h = max(m.get_height() for row in text_rows for m in row) + 0.6
        tot_w, tot_h = sum(col_w), n_rows * row_h

        # ------------------------------------------------------------- #
        # 4. build backgrounds & position text
        # ------------------------------------------------------------- #
        cell_bgs, cell_txts = VGroup(), VGroup()

        for r in range(n_rows):
            for c in range(n_cols):
                x = -tot_w/2 + sum(col_w[:c]) + col_w[c]/2
                y =  tot_h/2 - (r + 0.5)*row_h

                txt = text_rows[r][c].move_to([x, y, 0])

                bg = Rectangle(width=col_w[c], height=row_h, stroke_width=0).move_to([x, y, 0])

                # colouring rules
                if r == 0:                   # header row
                    bg.set_fill(YELLOW, opacity=0.66)
                else:
                    bg.set_fill(column_colors[c], opacity=0.3)
                    if data[r][c] == "Yes":
                        bg.set_fill(yes_color, opacity=0.5)
                    elif data[r][c] == "No":
                        bg.set_fill(no_color, opacity=0.5)

                cell_bgs.add(bg)
                cell_txts.add(txt)

        # ------------------------------------------------------------- #
        # 5. grid lines
        # ------------------------------------------------------------- #
        grid = VGroup(Rectangle(width=tot_w, height=tot_h, stroke_width=2))
        x_cur = -tot_w/2
        for w in col_w[:-1]:
            x_cur += w
            grid.add(Line([x_cur,  tot_h/2, 0], [x_cur, -tot_h/2, 0], stroke_width=1.5))
        y_cur = tot_h/2
        for _ in range(n_rows-1):
            y_cur -= row_h
            grid.add(Line([-tot_w/2, y_cur, 0], [tot_w/2, y_cur, 0], stroke_width=1.5))

        # ------------------------------------------------------------- #
        # 6. assemble & animate (grid → fills → text)
        # ------------------------------------------------------------- #
        table = VGroup(cell_bgs, grid, cell_txts).scale(0.8).center()
        title = Text("Training Data", font_size=86, weight=BOLD).next_to(table, UP, buff=0.88)

        self.play(Write(title))
        self.play(ShowCreation(grid), run_time=1)
        self.play(FadeIn(cell_bgs), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, cell_txts, shift=0.1*UP, lag_ratio=0.06), run_time=2)
        self.wait(2)

        # 1. brace + label (unchanged)
        brace = Brace(table, LEFT).shift(LEFT*0.2)
        label = brace.get_text("8 days")
        self.play(GrowFromCenter(brace), FadeIn(label))
        
        # Helper to grab every text mobject in a column (header + 8 rows)
        def column_group(col_index):
            return VGroup(*[text_rows[r][col_index] for r in range(n_rows)])
        
        # 2. highlight Outlook
        outlook_group = column_group(1)
        outlook_rect = Rectangle(
            width=outlook_group.get_width() + 0.4,
            height=outlook_group.get_height() + 0.413,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.4
        ).move_to(outlook_group)
        self.play(FadeIn(outlook_rect, run_time=0.5))
        self.wait(2)
        
        # 3. highlight Humidity (new column)
        humidity_group = column_group(2)
        humidity_rect = Rectangle(
            width=humidity_group.get_width() + 0.45,
            height=humidity_group.get_height() + 0.4,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.4
        ).move_to(humidity_group)
        self.play(ReplacementTransform(outlook_rect, humidity_rect))
        self.wait(2)
        
        # 4. highlight Windy (now column index 3)
        windy_group = column_group(3)
        windy_rect = Rectangle(
            width=windy_group.get_width() + 0.45,
            height=windy_group.get_height() + 0.4,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.4
        ).move_to(windy_group)
        self.play(ReplacementTransform(humidity_rect, windy_rect))
        self.wait(2)
        
        # 5. highlight Play (now column index 4)
        play_group = column_group(4)
        play_rect = Rectangle(
            width=play_group.get_width() + 0.46,
            height=play_group.get_height() + 0.4,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.4
        ).move_to(play_group)
        self.play(ReplacementTransform(windy_rect, play_rect))
        self.wait(2)
        
        # 6. cleanup
        self.play(FadeOut(VGroup(brace, label, play_rect)))
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.1).shift(RIGHT*4.599))
        self.wait(2)

        title = Text("Outlook: Rain \nHumidity: High \nWindy: False", font_size=80,).next_to(table, RIGHT, buff=0.5).shift(UP*4.25+RIGHT*2)
        self.play(Write(title))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(11*RIGHT), title.animate.shift(RIGHT*5+UP*0.2))


        self.wait(2)

        naive_bayes_formula =  Tex(r"P(Yes \mid Rain, High, False) = \frac{P(Rain \mid Yes) \cdot P(High \mid Yes) \cdot P(False \mid Yes) \cdot P(Yes)}{P(Rain, High, False)}").next_to(title, DOWN, buff=0.5).shift(DOWN*1.4).set_color(GREEN)

        self.play(Write(naive_bayes_formula))
        self.wait()



        naive_bayes_formula_no =  Tex(r"P(No \mid Rain, High, False) = \frac{P(Rain \mid No) \cdot P(High \mid No) \cdot P(False \mid No) \cdot P(No)}{P(Rain, High, False)}").next_to(naive_bayes_formula, DOWN, buff=0.5).shift(DOWN*1.4).set_color(RED)

        self.play(Write(naive_bayes_formula_no))
        self.wait(2)

        brace = Brace(naive_bayes_formula[:22], DOWN).shift(DOWN*0.2).set_color(YELLOW)
        self.play(GrowFromCenter(brace))

        self.wait(2)

        self.play(Transform(brace, Brace(naive_bayes_formula[23:], DOWN).shift(DOWN*0.2).set_color(YELLOW)))

        self.wait(2)

        self.play(Transform(brace, Brace(naive_bayes_formula_no[:21], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace, Brace(naive_bayes_formula_no[22:], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace, Brace(naive_bayes_formula_no[62:], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.wait(1)
        self.play(Transform(brace, Brace(naive_bayes_formula[67:], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.wait(2)

        temp = Tex("Score(Yes) = P(Rain \mid Yes) \cdot P(High \mid Yes) \cdot P(False \mid Yes) \cdot P(Yes)  ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN)
        
        temp1 = Tex("Score(No) = P(Rain \mid No) \cdot P(High \mid No) \cdot P(False \mid No) \cdot P(No)", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED)

        self.play(Transform(naive_bayes_formula_no, temp1), Transform(naive_bayes_formula, temp), FadeOut(brace))

        self.wait(2)

        brace = Brace(naive_bayes_formula[18:35], DOWN).shift(DOWN*0.2).set_color(YELLOW)
        self.play(GrowFromCenter(brace))
        self.wait()

        self.play(Transform(brace, Brace(naive_bayes_formula[37:53], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.play(Transform(brace, Brace(naive_bayes_formula[56:74], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.play(Transform(brace, Brace(naive_bayes_formula[75:], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.play(Transform(brace, Brace(naive_bayes_formula_no[17:33], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.play(Transform(brace, Brace(naive_bayes_formula_no[35:50], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.play(Transform(brace, Brace(naive_bayes_formula_no[53:70], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
        self.play(Transform(brace, Brace(naive_bayes_formula_no[72:], DOWN).shift(DOWN*0.2).set_color(YELLOW)))
       
        self.wait()


        self.play(FadeOut(brace), self.camera.frame.animate.shift(LEFT*20.2))
  
        self.wait(2)

        p_yes = Tex(r"P(Yes) = \frac{5}{8}", font_size=60).next_to(table, LEFT, buff=1.5).shift(2.78*LEFT).scale(1.3)
        self.play(Write(p_yes[:7]))

        self.wait(2)

        # Create a list of all "Yes" cell background objects
        yes_cells = []
        for r in range(1, n_rows):
            for c in range(n_cols):
                if data[r][c] == "Yes":
                    cell_index = r * n_cols + c
                    yes_cells.append(cell_bgs[cell_index])
        
        # Fill them all with orange
        for cell in yes_cells:
            cell.set_fill(WHITE, opacity=0.7)
        
        # Or animate the change:
        self.play(*[cell.animate.set_fill(WHITE, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(GREEN, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(WHITE, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(GREEN, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(WHITE, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(GREEN, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(WHITE, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(GREEN, opacity=0.5) for cell in yes_cells], run_time=0.5)

        self.play(Write(p_yes[7:]), run_time=1)
        self.wait(2)

        self.play(Transform(p_yes, Tex(r"P(Yes) = 0.625", font_size=60).move_to(p_yes).scale(1.3)))
        self.play(p_yes.animate.shift(UP*4.84+RIGHT*0.48))

        p_no = Tex(r"P(No) = \frac{3}{8}", font_size=60).next_to(table, LEFT, buff=1.5).shift(2.78*LEFT).scale(1.3)
        self.play(Write(p_no[:6]))


        # Create a list of all "Yes" cell background objects
        yes_cells = []
        for r in range(1, n_rows):
            for c in range(n_cols):
                if data[r][c] == "No":
                    cell_index = r * n_cols + c
                    yes_cells.append(cell_bgs[cell_index])
        
        # Fill them all with orange
        for cell in yes_cells:
            cell.set_fill(WHITE, opacity=0.7)
        
        # Or animate the change:
        self.play(*[cell.animate.set_fill(WHITE, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(RED, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(WHITE, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(RED, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(WHITE, opacity=0.5) for cell in yes_cells], run_time=0.5)
        self.play(*[cell.animate.set_fill(RED, opacity=0.5) for cell in yes_cells], run_time=0.5)

        self.wait()

        self.play(Write(p_no[6:]), run_time=1)
        self.wait(1)

        self.play(Transform(p_no, Tex(r"P(No) = 0.375", font_size=60).move_to(p_no).scale(1.3)))
        self.play(p_no.animate.next_to(p_yes, DOWN, buff=0.5))
        self.wait(2)

        p_rain_yes = Tex(r"P(Rain \mid Yes) = \frac{2}{5}", font_size=60).next_to(table, LEFT, buff=1.5).shift(1.8*LEFT).scale(1.3)
        self.play(Write(p_rain_yes[:12]))
        self.wait()

        # Create a list of all "Rain" cell background objects for "Yes"

        self.play(cell_bgs[21].animate.set_fill(BLACK, opacity=0.7),
                  cell_bgs[41].animate.set_fill(BLACK, opacity=0.7))
        
        self.wait(2)

        self.play(cell_bgs[21].animate.set_fill(PURPLE, opacity=0.3),
                  cell_bgs[41].animate.set_fill(PURPLE, opacity=0.3))
                


        self.play(Write(p_rain_yes[12:]), run_time=1)
        self.wait()
        self.play(Transform(p_rain_yes, Tex(r"P(Rain \mid Yes) = 0.4", font_size=60).move_to(p_rain_yes).scale(1.3)))
        self.play(p_rain_yes.animate.next_to(p_no, DOWN, buff=0.5))
        self.wait(2)

        p_rain_no = Tex(r"P(Rain \mid No) = \frac{1}{3}", font_size=60).next_to(table, LEFT, buff=1.5).shift(1.8*LEFT).scale(1.3)
        self.play(Write(p_rain_no[:11]))
        self.wait()

        # Create a list of all "Rain" cell background objects for "No"
        self.play(cell_bgs[26].animate.set_fill(BLACK, opacity=0.3))

        self.wait(2)

        self.play(cell_bgs[26].animate.set_fill(PURPLE, opacity=0.3),
                  )
        

        self.play(Write(p_rain_no[11:]), run_time=1)
        self.wait()
        self.play(Transform(p_rain_no, Tex(r"P(Rain \mid No) = 0.333", font_size=60).move_to(p_rain_no).scale(1.3)))
        self.play(p_rain_no.animate.next_to(p_rain_yes, DOWN, buff=0.5))
        self.wait(2)

        p_humidity_yes = Tex(r"P(High \mid Yes) = 0.2", font_size=60).next_to(p_rain_no, DOWN, buff=0.5).scale(1.3)
        self.play(Write(p_humidity_yes))
        p__humidity_no = Tex(r"P(High \mid No) = 0.666", font_size=60).next_to(p_humidity_yes, DOWN, buff=0.5).scale(1.3)
        self.play(Write(p__humidity_no))
        p_windy_yes = Tex(r"P(False \mid Yes) = 0.4", font_size=60).next_to(p__humidity_no, DOWN, buff=0.5).scale(1.3)
        self.play(Write(p_windy_yes))
        p_windy_no = Tex(r"P(False \mid No) = 0.333", font_size=60).next_to(p_windy_yes, DOWN, buff=0.5).scale(1.3)
        self.play(Write(p_windy_no))

        self.wait(2)
 
        self.play(self.camera.frame.animate.shift(RIGHT*20))

        self.wait(2)


        temp = Tex("Score(Yes) = 0.4 \\times 0.2 \\times 0.4 \\times 0.625  ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(1.5)
        
        temp1 = Tex("Score(No) = 0.333 \\times 0.667 \\times 0.333 \\times 0.375", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED).scale(1.5)

        self.play(Transform(naive_bayes_formula_no, temp1), Transform(naive_bayes_formula, temp),)

        self.wait(2)

        temp = Tex("Score(Yes) = 0.0200 ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(2).shift(DOWN*0.3)
        
        temp1 = Tex("Score(No) = 0.0277", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED).scale(2)

        self.play(Transform(naive_bayes_formula_no, temp1), Transform(naive_bayes_formula, temp),)

        self.wait(2)

        rect = SurroundingRectangle(naive_bayes_formula_no, color=YELLOW, stroke_width=7).scale(1.23)
        self.play(ShowCreation(rect))

        self.wait(2)
        self.play(Uncreate(rect))

        temp = Tex("P(Yes) = \\frac{0.0200}{0.0200 + 0.0277}", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(1.6).shift(UP*0.4)

        temp1 = Tex("P(No) = \\frac{0.0277}{0.0200 + 0.0277}", font_size=60).next_to(naive_bayes_formula_no, ORIGIN).set_color(RED).scale(1.6).shift(DOWN*0.4)

        self.play(Transform(naive_bayes_formula_no, temp1), Transform(naive_bayes_formula, temp),)

        self.wait(2)

        temp = Tex("P(Yes) = 0.419", font_size=50).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(2).shift(DOWN*0.4)

        temp1 = Tex("P(No) = 0.581", font_size=60).next_to(naive_bayes_formula_no, ORIGIN).set_color(RED).scale(2).shift(UP*0.4)

        self.play(Transform(naive_bayes_formula_no, temp1), Transform(naive_bayes_formula, temp),)

        self.wait(2)


        self.play(self.camera.frame.animate.shift(LEFT*20), FadeOut(VGroup(naive_bayes_formula, naive_bayes_formula_no)))
        self.wait(2)

        self.play(cell_bgs[8].animate.set_fill(BLACK, opacity=0.3))

        self.wait(2)

        self.play(Transform(cell_txts[8], Text("True").move_to(cell_txts[8]).scale(0.84)))

        self.play(cell_bgs[8].animate.set_fill(ORANGE, opacity=0.3),) 

        self.wait(2)   

        rect = SurroundingRectangle(p_windy_no, color=YELLOW, stroke_width=5).scale(1.08)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(p_windy_no, Tex(r"P(False \mid No) = 0", font_size=60).move_to(p_windy_no).scale(1.3)))

        self.wait(2)

        self.play(FadeOut(rect), self.camera.frame.animate.shift(20*RIGHT))

        
        temp = Tex("Score(Yes) = P(Rain \mid Yes) \cdot P(High \mid Yes) \cdot P(False \mid Yes) \cdot P(Yes)  ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN)
        
        temp1 = Tex("Score(No) = P(Rain \mid No) \cdot P(High \mid No) \cdot P(False \mid No) \cdot P(No)", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED)

        self.play(ShowCreation(temp), ShowCreation(temp1))

        self.wait(2)

        yes = Tex("Score(Yes) = 0.4 \\times 0.2 \\times 0.4 \\times 0.625  ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(1.5)
        
        no = Tex("Score(No) = 0.333 \\times 0.667 \\times 0 \\times 0.375", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED).scale(1.5)

        self.play(ReplacementTransform(temp, yes), ReplacementTransform(temp1, no),)

        self.wait(2)

        temp = Tex("Score(Yes) = 0.0200 ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(2).shift(DOWN*0.3)
        
        temp1 = Tex("Score(No) = 0", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED).scale(2)

        self.play(Transform(no, temp1), Transform(yes, temp),)

        self.wait(2)

        temp = Tex("P(Yes) = \\frac{0.0200}{0.0200 + 0}", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(1.6).shift(UP*0.4)

        temp1 = Tex("P(No) = \\frac{0}{0.0200 + 0}", font_size=60).next_to(naive_bayes_formula_no, ORIGIN).set_color(RED).scale(1.6).shift(DOWN*0.4)

        self.play(Transform(no, temp1), Transform(yes, temp),)

        self.wait(2)

        temp = Tex("P(Yes) = 1", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(2)

        temp1 = Tex("P(No) = 0", font_size=60).next_to(naive_bayes_formula_no, ORIGIN).set_color(RED).scale(2).shift(DOWN*0.4)

        self.play(Transform(no, temp1), Transform(yes, temp),)

        self.wait(2)

        self.play(FadeOut(VGroup(yes, no, title)), )

        formula = Tex(
            r"P(F = v \mid Y = y) = \frac{\#\{F=v, Y=y\} + 1}{n_y + |V_F|}"
        )
        formula[0].set_color(BLUE)
        formula[2].set_color(GREEN)
        formula[29].set_color(GREEN)
        formula[6].set_color(RED)
        formula[17].set_color(RED)
        formula[13].set_color(BLUE)


        formula.scale(1.2*1.5).move_to(yes)
        laplacian = Text("Laplacian Smoothing").move_to(title).scale(2.2)
        self.play(Write(formula), Write(laplacian))
        self.wait(2)

        brace = Brace(formula[:10], DOWN, buff=0.5).set_color(YELLOW)

        self.play(ShowCreation(brace))

        self.wait(2)

        self.play(Transform(brace, Brace(formula[11:21], UP, buff=0.5).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace, Brace(formula[24:26], DOWN, buff=0.5).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace, Brace(formula[11:23], UP, buff=0.5).set_color(YELLOW)))
        self.wait(2)

        self.play(Transform(brace, Brace(formula[-4:32], DOWN, buff=0.5).set_color(YELLOW)))

        temp = Text("Total distinct values of feature F").next_to(formula, DOWN, buff=0.8).scale(1.4).shift(DOWN)
        self.play(ShowCreation(temp))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*20))


        humidity_group = column_group(2)
        humidity_rect = Rectangle(
            width=humidity_group.get_width() + 0.45,
            height=humidity_group.get_height() + 0.4,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.4
        ).move_to(humidity_group)
        self.play(ShowCreation(humidity_rect))
        self.wait(2)
        
        windy_group = column_group(3)
        windy_rect = Rectangle(
            width=windy_group.get_width() + 0.45,
            height=windy_group.get_height() + 0.4,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=0.4
        ).move_to(windy_group)
        self.play(ReplacementTransform(humidity_rect, windy_rect))
        self.wait(2)
        self.play(FadeOut(VGroup(windy_rect, laplacian, formula, temp)))
        self.wait(2)


        self.play(FadeOut(VGroup(p_rain_no, p_rain_yes, p_windy_no, p_windy_yes, p_humidity_yes, p__humidity_no)))

        rect = SurroundingRectangle(VGroup(p_no, p_yes), color=YELLOW, stroke_width=5).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)
        self.play(Uncreate(rect))







        p_rain_yes = Tex(r"P(Rain \mid Yes) = \frac{2 + 1}{5 + 3}", font_size=60).next_to(table, LEFT, buff=1.5).shift(1*LEFT).scale(1.3)
        self.play(Write(p_rain_yes))
        self.wait()

        # Create a list of all "Rain" cell background objects for "Yes"


        self.play(Transform(p_rain_yes, Tex(r"P(Rain \mid Yes) = 0.375", font_size=60).next_to(table, LEFT, buff=1.5).move_to(p_rain_yes).scale(1.3)), run_time=1)
        self.wait()
        self.play(p_rain_yes.animate.next_to(p_no, DOWN, buff=0.5))
        self.wait(2)

        p_rain_no = Tex(r"P(Rain \mid No) = \frac{1 + 1}{3 + 3}", font_size=60).next_to(table, LEFT, buff=1.5).shift(1*LEFT).scale(1.3)
        self.play(Write(p_rain_no))
        self.wait()
        
        self.play(Transform(p_rain_no, Tex(r"P(Rain \mid No) = 0.333", font_size=60).move_to(p_rain_no).scale(1.3)))
        self.play(p_rain_no.animate.next_to(p_rain_yes, DOWN, buff=0.5))
        self.wait(2)

        p_windy_no = Tex(r"P(False \mid No) = \frac{0 + 1}{3 + 2}", font_size=60).next_to(p_rain_no, DOWN, buff=1.5).scale(1.3)
        self.play(Write(p_windy_no))
        self.wait(2)

        self.play(Transform(p_windy_no, Tex(r"P(False \mid No) = 0.2", font_size=60).move_to(p_windy_no).scale(1.3)))
        self.play(p_windy_no.animate.next_to(p_rain_no, DOWN, buff=0.5))
        self.wait(2)

        p_windy_yes = Tex(r"P(False \mid Yes) = 0.428", font_size=60).next_to(p_windy_no, DOWN, buff=0.5).scale(1.3)
        self.play(Write(p_windy_yes))

        p_humidity_yes = Tex(r"P(High \mid Yes) = 0.25", font_size=60).next_to(p_windy_yes, DOWN, buff=0.5).scale(1.3)
        self.play(Write(p_humidity_yes))
        p__humidity_no = Tex(r"P(High \mid No) = 0.5", font_size=60).next_to(p_humidity_yes, DOWN, buff=0.5).scale(1.3)
        self.play(Write(p__humidity_no), FadeOut(brace))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*20), FadeIn(title))




        temp = Tex("Score(Yes) = P(Rain \mid Yes) \cdot P(High \mid Yes) \cdot P(False \mid Yes) \cdot P(Yes)  ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN)
        
        temp1 = Tex("Score(No) = P(Rain \mid No) \cdot P(High \mid No) \cdot P(False \mid No) \cdot P(No)", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED)

        self.play(ShowCreation(temp), ShowCreation(temp1))

        self.wait(2)

        yes = Tex("Score(Yes) = 0.375 \\times 0.25 \\times 0.428 \\times 0.625  ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(1.5)
        
        no = Tex("Score(No) = 0.333 \\times 0.5 \\times 0.2 \\times 0.375", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED).scale(1.5)

        self.play(ReplacementTransform(temp, yes), ReplacementTransform(temp1, no),)

        self.wait(2)

        temp = Tex("Score(Yes) = 0.0251 ", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(2).shift(DOWN*0.3)
        
        temp1 = Tex("Score(No) = 0.0125", font_size=60).next_to(naive_bayes_formula_no, ORIGIN, ).set_color(RED).scale(2)

        self.play(Transform(no, temp1), Transform(yes, temp),)

        self.wait(2)

        temp = Tex("P(Yes) = \\frac{0.0251}{0.0125 + 0.0251}", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(1.6).shift(UP*0.4)

        temp1 = Tex("P(No) = \\frac{0.0125}{0.0125 + 0.0251}", font_size=60).next_to(naive_bayes_formula_no, ORIGIN).set_color(RED).scale(1.6).shift(DOWN*0.4)

        self.play(Transform(no, temp1), Transform(yes, temp),)

        self.wait(2)

        temp = Tex("P(Yes) = 0.67", font_size=60).next_to(naive_bayes_formula, ORIGIN).set_color(GREEN).scale(2)

        temp1 = Tex("P(No) = 0.33", font_size=60).next_to(naive_bayes_formula_no, ORIGIN).set_color(RED).scale(2).shift(DOWN*0.4)

        self.play(Transform(no, temp1), Transform(yes, temp),)

        self.wait(2)

        rect = SurroundingRectangle(yes, color=YELLOW, stroke_width=6).scale(1.2)
        self.play(ShowCreation(rect))

        self.wait(2)

 
