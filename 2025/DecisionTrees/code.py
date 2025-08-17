from manimlib import *

class DecisionTree(Scene):
    def construct(self):

        self.camera.frame.scale(1.31).shift(0.7*UP)

        # ------------------------------------------------------------- #
        # 1. data (animal dataset, emojis removed)
        # ------------------------------------------------------------- #
        data = [
            ["Name",      "CanFly", "EatsMeat", "LaysEggs", "Bird"],
            ["Eagle",     "Yes",    "Yes",      "Yes",      "Yes"],
            ["Bat",       "Yes",    "Yes",      "No",       "No"],
            ["Butterfly", "Yes",    "No",       "Yes",      "No"],
            ["Penguin",   "No",     "Yes",      "Yes",      "Yes"],
            ["Elephant",  "No",     "No",       "No",       "No"],
            ["Ostrich",   "No",     "Yes",       "Yes",      "Yes"],
            ["Peacock",   "Yes",     "Yes",       "Yes",      "Yes"],
            ["Cat",   "No",     "Yes",       "No",      "No"],
        ]

        # Column colors
        column_colors = [BLUE, PURPLE, PINK, ORANGE, TEAL]
        yes_color, no_color = GREEN, RED

        # ------------------------------------------------------------- #
        # 2. build Text objects
        # ------------------------------------------------------------- #
        text_rows = [
            [
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

                # coloring rules
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
        # 6. assemble & animate
        # ------------------------------------------------------------- #
        table = VGroup(cell_bgs, grid, cell_txts).scale(0.8).center()
        title = Text("Animal Dataset", font_size=86, weight=BOLD).next_to(table, UP, buff=0.88)

        self.play(Write(title))
        self.play(ShowCreation(grid), run_time=1)
        self.play(FadeIn(cell_bgs), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, cell_txts, shift=0.1*UP, lag_ratio=0.06), run_time=2)
        self.wait(2)

        def get_cell(r, c):
            return cell_bgs[r*n_cols + c]

        rect = SurroundingRectangle(VGroup(get_cell(0,0), get_cell(8,0)), fill_color=WHITE, color=WHITE, fill_opacity=0.3)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(VGroup(get_cell(0,1), get_cell(8,1)), fill_color=WHITE, color=WHITE, fill_opacity=0.3)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(VGroup(get_cell(0,2), get_cell(8,2)), fill_color=WHITE, color=WHITE, fill_opacity=0.3)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(VGroup(get_cell(0,3), get_cell(8,3)), fill_color=WHITE, color=WHITE, fill_opacity=0.3)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(VGroup(get_cell(0,4), get_cell(8,4)), fill_color=WHITE, color=WHITE, fill_opacity=0.3)))
        self.wait(2)
        self.play(Uncreate(rect))

        peacock = ImageMobject("peacock.png").shift(RIGHT*16.45).scale(0.4)
        eagle = ImageMobject("eagle.png").scale(0.4).next_to(peacock, RIGHT)
        elephant = ImageMobject("elephant.png").scale(0.4).next_to(eagle, RIGHT)
        bat = ImageMobject("bat.png").scale(0.4).next_to(peacock, LEFT)
        butterfly = ImageMobject("butterfly.png").scale(0.6).next_to(bat, LEFT)
        ostrich = ImageMobject("ostrich.png").scale(0.4).next_to(butterfly, LEFT)
        penguin = ImageMobject("penguin.png").scale(0.606).next_to(elephant, RIGHT)
        cat = ImageMobject("cat.png").scale(0.6).next_to(ostrich, LEFT)

        self.play(self.camera.frame.animate.shift(RIGHT*15))
        self.add(eagle, peacock, elephant, bat, butterfly, ostrich, penguin, cat)
        self.wait(2)
        
        total = Group(eagle, cat, ostrich, butterfly, bat, peacock, elephant, penguin)

        self.play(total.animate.scale(0.85).shift(UP*4.1))
 
        
        
        # Create ellipse with full opacity fill
        ellipse = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=BLUE, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(total, DOWN, buff=1).shift(UP*0.8)
        
        # Text inside ellipse
        feature_text = Text(
            "CanFly", 
            font_size=68, 
            weight=BOLD, 
        ).move_to(ellipse.get_center()).set_color(BLACK)
        # Arrows with z_index = -1 (behind other elements)
        arrow_left = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + LEFT*4 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + RIGHT*4 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse), Write(feature_text))
        self.wait(1)
        self.play(GrowArrow(arrow_left), GrowArrow(arrow_right))
        self.play(FadeIn(no_label), FadeIn(yes_label))
        self.wait(2)

        self.play(cat.animate.next_to(arrow_left.get_bottom(), DOWN).shift(LEFT*0.7))
        self.play(ostrich.animate.next_to(cat, LEFT).shift(RIGHT*0.398))
        self.play(elephant.animate.next_to(ostrich, LEFT).shift(RIGHT*0.76))
        self.play(penguin.animate.next_to(elephant, LEFT).shift(RIGHT*0.37))
        self.wait(2)
        self.play(butterfly.animate.next_to(arrow_right.get_bottom(), DOWN).shift(RIGHT*0.7))
        self.play(eagle.animate.next_to(butterfly, RIGHT).shift(LEFT*0.18))
        self.play(bat.animate.next_to(eagle, RIGHT).shift(LEFT*0.33))
        self.play(peacock.animate.next_to(bat, RIGHT).shift(LEFT*0.33))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*2))
        self.wait(1.3)

        self.play(
            ostrich.animate.next_to(penguin, DOWN).shift(UP*0.2),
            cat.animate.next_to(elephant, DOWN).shift(UP*0.2),
            butterfly.animate.next_to(bat, DOWN).shift(UP*0.2),
            eagle.animate.next_to(peacock, DOWN).shift(DOWN*0.07),
            FadeOut(grid), FadeOut(table)
            )

        left_half = Group(penguin, elephant, ostrich, cat)
        right_half = Group(butterfly, bat, peacock, eagle)

        self.play(self.camera.frame.animate.scale(1.15).shift(DOWN*0.9+RIGHT*0.25), left_half.animate.shift(LEFT*1.5+UP*0.23), right_half.animate.shift(RIGHT*1.7+UP*0.12))
        self.wait(2)
        
        # Create ellipse with full opacity fill
        ellipse_left = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=YELLOW, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(arrow_left.get_center(), DOWN, buff=1.23).shift(LEFT*2)
        
        # Text inside ellipse
        feature_text_left = Text(
            "LaysEggs", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse_left.get_center()).set_color(BLACK)
        # Arrows with z_index = -1 (behind other elements)
        arrow_left_left = Arrow(
            start=ellipse_left.get_center(), 
            end=ellipse_left.get_center() + LEFT*2 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_left_right = Arrow(
            start=ellipse_left.get_center(), 
            end=ellipse_left.get_center() + RIGHT*2 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label_left = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_left_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label_left = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_left_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse_left), Write(feature_text_left))
        self.wait(1)
        self.play(GrowArrow(arrow_left_left), GrowArrow(arrow_left_right))
        self.play(FadeIn(no_label_left), FadeIn(yes_label_left))
        self.wait(2)

        self.play(elephant.animate.next_to(arrow_left_left, DOWN, buff=0.5).shift(LEFT*0.7).scale(1.4) )
        self.play(cat.animate.next_to(elephant, LEFT, buff=0.5).shift(RIGHT*0.8).scale(1.4))
        self.wait()
        self.play(penguin.animate.next_to(arrow_left_right, DOWN, buff=0.5).shift(RIGHT*0.47+UP*0.22).scale(1.4))
        self.play(ostrich.animate.next_to(penguin, RIGHT, buff=0).shift(LEFT*0.28).scale(1.4))
        self.wait()
        
        not_bird = Rectangle(color=RED, fill_color=RED, fill_opacity=0.65, height=1.1, width=5).next_to(Group(cat, elephant), DOWN, buff=0.6)
        not_bird_text = Text("Not Bird", weight=BOLD).move_to(not_bird).scale(2).set_color(WHITE)
        not_bird = VGroup(not_bird, not_bird_text)

        bird_rect = Rectangle(color=GREEN, fill_color=GREEN, fill_opacity=0.65, height=1.1, width=2.5).next_to(Group(penguin, ostrich), DOWN, buff=0.6)
        bird_text = Text("Bird", weight=BOLD).scale(2).move_to(bird_rect).set_color(WHITE)
        bird = VGroup(bird_rect, bird_text).shift(UP*0.125)
        self.play(ShowCreation(not_bird), ShowCreation(bird))
        self.wait(2)


        # Create ellipse with full opacity fill
        ellipse_right = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=YELLOW, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(arrow_right.get_center(), DOWN, buff=1.23).shift(RIGHT*2)
        
        # Text inside ellipse
        feature_text_right = Text(
            "LaysEggs", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse_right.get_center()).set_color(BLACK).set_z_index(1)
        # Arrows with z_index = -1 (behind other elements)
        arrow_right_left = Arrow(
            start=ellipse_right.get_center(), 
            end=ellipse_right.get_center() + LEFT*2 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right_right = Arrow(
            start=ellipse_right.get_center(), 
            end=ellipse_right.get_center() + RIGHT*2 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label_left = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_right_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label_left = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse_right), Write(feature_text_right))
        self.wait(1)
        self.play(GrowArrow(arrow_right_right), GrowArrow(arrow_right_left))
        self.play(FadeIn(no_label_left), FadeIn(yes_label_left))
        self.wait(2)

        self.play(bat.animate.next_to(arrow_right_left, DOWN).scale(1.4).shift(DOWN*0.4+LEFT*0.9))
        self.wait()
        bat_text = not_bird.copy().next_to(bat, DOWN, buff=0.1).scale(0.7)
        self.play(GrowFromCenter(bat_text))

        self.play(butterfly.animate.next_to(arrow_right_right, DOWN).scale(1.4).shift(UP*0.18+RIGHT*1.6).scale(0.7))
        self.play(peacock.animate.next_to(butterfly, RIGHT).scale(1.4))
        self.play(eagle.animate.scale(1.38).next_to(Group(butterfly, peacock), DOWN).shift(UP*0.6+LEFT*0.5))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*4.7+RIGHT*5.5))
        self.wait(2)


        # Create ellipse with full opacity fill
        ellipse_right_right = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=PURPLE, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(arrow_right_right.get_center(), DOWN, buff=1.23).shift(RIGHT*2)
        
        # Text inside ellipse
        feature_text_right_right = Text(
            "EatsMeat", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse_right_right.get_center()).set_color(WHITE).set_z_index(1)
        # Arrows with z_index = -1 (behind other elements)
        arrow_right_right_left = Arrow(
            start=ellipse_right_right.get_center(), 
            end=ellipse_right_right.get_center() + LEFT*2 + DOWN*3.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right_right_right = Arrow(
            start=ellipse_right_right.get_center(), 
            end=ellipse_right_right.get_center() + RIGHT*2 + DOWN*3.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label_left = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_right_right_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label_left = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right_right_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        self.play(Group(eagle, butterfly, peacock).animate.shift(RIGHT*4.7))

        # Animate the decision tree elements
        self.play(FadeIn(ellipse_right_right), Write(feature_text_right_right))
        self.wait(1)
        self.play(GrowArrow(arrow_right_right_left), GrowArrow(arrow_right_right_right))
        self.play(FadeIn(no_label_left), FadeIn(yes_label_left))
        self.wait(2)

        self.play(butterfly.animate.next_to(arrow_right_right_left, DOWN).shift(LEFT+DOWN*0.4).scale(1.34))
        self.wait(2)

        self.play(eagle.animate.next_to(arrow_right_right_right, DOWN, ).shift(DOWN*0.47+RIGHT*0.67))
        self.play(peacock.animate.next_to(eagle, RIGHT, ).shift(LEFT*0.2))

        self.wait(2)

        a = not_bird.copy().next_to(butterfly, DOWN).scale(0.75)
        b = bird.copy().next_to(Group(eagle, peacock), DOWN).scale(0.75).shift(DOWN*0.29)

        self.play(GrowFromCenter(a), GrowFromCenter(b))
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.5).shift(UP*2+LEFT*4))

        self.wait()

        self.play(FadeOut(Group(right_half ,left_half)), FadeOut(title))

        self.play(
            a.animate.next_to(arrow_right_right_left, DOWN, buff=0.56).shift(LEFT*0.8),
            b.animate.next_to(arrow_right_right_right, DOWN, buff=0.56).shift(RIGHT*1.2),
            bat_text.animate.next_to(arrow_right_left, DOWN, buff=0.56).shift(LEFT*0.5),
            not_bird.animate.next_to(arrow_left_left, DOWN, buff=0.56).shift(LEFT*0.5).scale(0.75),
            bird.animate.next_to(arrow_left_right, DOWN, buff=0.56).shift(RIGHT*0.82).scale(0.75),
            self.camera.frame.animate.shift(UP*2).scale(0.8)
              )
        
        chicken = ImageMobject("chicken.png").scale(0.7).next_to(ellipse, UP)
        self.add(chicken)
        self.play(self.camera.frame.animate.shift(UP*1.5))

        self.wait(2)

        self.play(chicken.animate.next_to(ellipse_left, LEFT))
        self.wait(2)
        self.play(chicken.animate.next_to(bird, DOWN), self.camera.frame.animate.shift(DOWN*1.5))
        self.play(FadeOut(chicken))

        self.wait(2)

        snake = ImageMobject("snake.png").scale(0.5).next_to(ellipse, UP).shift(UP*0.1)
        self.add(snake)
        self.play(self.camera.frame.animate.shift(UP*1.5))

        self.wait(2)

        self.play(snake.animate.next_to(ellipse_left, LEFT).shift(LEFT*0.1))
        self.wait(2)
        self.play(snake.animate.next_to(bird, DOWN).shift(DOWN*0.2), self.camera.frame.animate.shift(DOWN*1.5))
        self.play(FadeOut(snake))

        self.wait(2)

        c = VGroup(ellipse_right_right, feature_text_right_right).copy().move_to(ellipse)
        b = VGroup(ellipse_right, feature_text_right).copy().move_to(ellipse)

        arrow = Arrow(ellipse.get_right(), ellipse.get_right()+RIGHT*1.5, stroke_width=6).set_color(PINK).rotate(PI).shift(RIGHT*1.9)
        self.play(ShowCreation(arrow))

        self.play(ReplacementTransform(VGroup(ellipse, feature_text), c))
        self.wait(2)
        self.play(ReplacementTransform(c, b))
        self.wait(2)


class GiniFormula(Scene):
    def construct(self):
       
        self.camera.frame.shift(DOWN)

        title = Tex(r"\textbf{Gini Impurity}").scale(0.9).to_edge(UP)

        # Formula: only "Gini" is wrapped in \text{}, math stays in math mode
        formula = Tex(
            r"Gini = 1 - \sum_{i=1}^{C} p_i^2"
        ).scale(1.66)

        terms = VGroup(
            Tex(r"C"),
            Tex(r"p_i")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.65).scale(0.9).next_to(formula, DOWN, buff=1.12).shift(LEFT*4.25)
        
        a = Text("= Number of classes").next_to(terms[0], RIGHT)
        b = Text("= Proportion of class i in the Node").next_to(terms[1], RIGHT)

        self.play(Write(formula))
        self.play(FadeIn(terms))
        self.play(Write(a), Write(b))
        self.wait(2)

        rect = SurroundingRectangle(formula, color=RED, stroke_width=8).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)


        self.play(Transform(rect, SurroundingRectangle(VGroup(a, terms[0]), color=RED, stroke_width=5, ).scale(1.19)))
        self.play(formula[7].animate.set_color(RED))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(VGroup(b, terms[1]), color=RED, stroke_width=5, ).scale(1.12)))
        self.play(formula[12:14].animate.set_color(RED))

        self.wait(2)

        self.play(Uncreate(rect), formula[7:].animate.set_color(RED))
        self.wait(2)

        rect = SurroundingRectangle(formula[5:], color=YELLOW, stroke_width=8).scale(1.1)
        self.play(ShowCreation(rect))

        self.wait(2)


    class GiniImpurityAnimation(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 1.2, 0.2], # x-axis longer, ends at 1.2
            y_range=[0, 0.6, 0.1],
            width=9, # make it wide!
            height=5,
            axis_config={"color": WHITE, "include_tip": True},
            x_axis_config={"include_tip": True},
            y_axis_config={"include_tip": True},
        )

        # Axis labels outside last tick
        x_label = Tex("p_i")
        x_label.next_to(axes.c2p(1.2, 0), RIGHT, buff=0.6)
        y_label = Tex("Gini")
        y_label.next_to(axes.c2p(0, 0.6), UP, buff=0.3).shift(UP*0.3).scale(1.2)

        # Custom tick labels
        x_one_label = Tex("1")
        x_one_label.next_to(axes.c2p(1, 0), DOWN, buff=0.2).shift(DOWN*0.1)
        y_half_label = Tex("0.5")
        y_half_label.next_to(axes.c2p(0, 0.5), LEFT, buff=0.2).shift(LEFT*0.1)

        # Graph only from x=0 to x=1!
        graph = axes.get_graph(lambda x: 2 * x * (1 - x), x_range=[0, 1], stroke_width=7)
        graph.set_color(BLUE)

        dot = Dot().scale(2)
        dot.set_color(YELLOW)
        dot.move_to(axes.c2p(0, 0))

        gini_value_text = DecimalNumber(0, num_decimal_places=3)
        gini_label_prefix = Tex("Gini = ")

        def text_updater(text_mobject):
            current_p_value = axes.p2c(dot.get_center())[0]
            if current_p_value > 1:
                current_p_value = 1
            new_gini_value = 2 * current_p_value * (1 - current_p_value)
            text_mobject.set_value(new_gini_value)
            text_mobject.next_to(dot, UR, buff=0.2)

        gini_value_text.add_updater(text_updater)
        gini_label_prefix.add_updater(lambda m: m.next_to(gini_value_text, LEFT))

        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.play(Write(x_one_label), Write(y_half_label))
        self.play(ShowCreation(graph))
        self.wait(1)

        self.add(dot, gini_value_text, gini_label_prefix)
        self.wait(2)
        
        self.play(
            MoveAlongPath(dot, graph),
            run_time=4,
            rate_func=there_and_back
        )

        self.wait(2)


class Training(Scene):
    def construct(self):

        self.camera.frame.scale(1.31).shift(0.7*UP)

        # ------------------------------------------------------------- #
        # 1. data (animal dataset, emojis removed)
        # ------------------------------------------------------------- #
        data = [
            ["Name",      "CanFly", "EatsMeat", "LaysEggs", "Bird"],
            ["Eagle",     "Yes",    "Yes",      "Yes",      "Yes"],
            ["Bat",       "Yes",    "Yes",      "No",       "No"],
            ["Butterfly", "Yes",    "No",       "Yes",      "No"],
            ["Penguin",   "No",     "Yes",      "Yes",      "Yes"],
            ["Elephant",  "No",     "No",       "No",       "No"],
            ["Ostrich",   "No",     "Yes",       "Yes",      "Yes"],
            ["Peacock",   "Yes",     "Yes",       "Yes",      "Yes"],
            ["Cat",   "No",     "Yes",       "No",      "No"],
        ]

        # Column colors
        column_colors = [BLUE, PURPLE, PINK, ORANGE, TEAL]
        yes_color, no_color = GREEN, RED

        # ------------------------------------------------------------- #
        # 2. build Text objects
        # ------------------------------------------------------------- #
        text_rows = [
            [
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

                # coloring rules
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
        # 6. assemble & animate
        # ------------------------------------------------------------- #
        table = VGroup(cell_bgs, grid, cell_txts).scale(0.8).center()
        title = Text("Animal Dataset", font_size=86, weight=BOLD).next_to(table, UP, buff=0.88)

        self.play(Write(title))
        self.play(ShowCreation(grid), run_time=1)
        self.play(FadeIn(cell_bgs), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, cell_txts, shift=0.1*UP, lag_ratio=0.06), run_time=2)
        self.wait(2)

        def get_cell(r, c):
            return cell_bgs[r*n_cols + c]


        peacock = ImageMobject("peacock.png").shift(RIGHT*16.45).scale(0.4)
        eagle = ImageMobject("eagle.png").scale(0.4).next_to(peacock, RIGHT)
        elephant = ImageMobject("elephant.png").scale(0.4).next_to(eagle, RIGHT)
        bat = ImageMobject("bat.png").scale(0.4).next_to(peacock, LEFT)
        butterfly = ImageMobject("butterfly.png").scale(0.6).next_to(bat, LEFT)
        ostrich = ImageMobject("ostrich.png").scale(0.4).next_to(butterfly, LEFT)
        penguin = ImageMobject("penguin.png").scale(0.606).next_to(elephant, RIGHT)
        cat = ImageMobject("cat.png").scale(0.6).next_to(ostrich, LEFT)

        self.add(eagle, peacock, elephant, bat, butterfly, ostrich, penguin, cat)
        self.wait(2)
        self.play(self.camera.frame.animate.shift(RIGHT*15))
        
        total = Group(eagle, cat, ostrich, butterfly, bat, peacock, elephant, penguin)

        self.play(total.animate.scale(0.95).shift(UP*3.1))
        temp_a = bat.get_center()
        temp_b = peacock.get_center()
        self.play(peacock.animate.move_to(temp_a).shift(RIGHT*0.1), bat.animate.move_to(temp_b))
        self.wait(2)

        brace = Brace(Group(cat,  penguin), DOWN, buff=0.3)
        self.play(GrowFromCenter(brace))
        text = Text("8").next_to(brace, DOWN).scale(2).shift(DOWN*0.3).set_color(YELLOW)
        self.play(ShowCreation(text))
        self.wait(2)

        a = Circle(stroke_color="#00ff00", stroke_width=4).move_to(ostrich)
        b = a.copy().move_to(peacock)
        c = b.copy().move_to(eagle)
        d = c.copy().move_to(penguin)

        self.play(ShowCreation(a), ShowCreation(b), ShowCreation(c), ShowCreation(d))
        self.wait(2)

        self.play(Uncreate(a), Uncreate(b), Uncreate(c), Uncreate(d), Uncreate(brace), Uncreate(text))

        formula = Tex(r"Gini = 1 - \left(p_{yes}^{2} + p_{no}^{2}\right)").scale(2.6).next_to(total, DOWN, buff=1.6)
        self.play(ShowCreation(formula))
        self.wait(2)

        self.play(Transform(formula, Tex(r"Gini = 1 - \left(\left(\tfrac{4}{8}\right)^{2} + \left(\tfrac{4}{8}\right)^{2}\right)").scale(2.6).move_to(formula)))
        self.wait(2)
        
        self.play(Transform(formula, Tex(r"Gini = 0.5").scale(2.6).move_to(formula)))
        self.wait(2)

        self.play(FadeOut(formula), total.animate.shift(UP*1.2))
        self.wait()

        # Create ellipse with full opacity fill
        ellipse = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=BLUE, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(total, DOWN, buff=1).shift(UP*0.8)
        
        # Text inside ellipse
        feature_text = Text(
            "CanFly", 
            font_size=68, 
            weight=BOLD, 
        ).move_to(ellipse.get_center()).set_color(BLACK)
        # Arrows with z_index = -1 (behind other elements)
        arrow_left = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + LEFT*2 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + RIGHT*2 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse), Write(feature_text))
        self.wait(1)
        self.play(GrowArrow(arrow_left), GrowArrow(arrow_right))
        self.play(FadeIn(no_label), FadeIn(yes_label))
        self.wait(2)


        self.play(cat.animate.next_to(arrow_left, DOWN).shift(LEFT*2.3+UP*0.29), run_time=0.5)
        self.play(ostrich.animate.next_to(cat, DOWN).shift(UP*0.4), run_time=0.5)
        self.play(elephant.animate.next_to(cat, RIGHT).shift(LEFT*0.46), run_time=0.5)
        self.play(penguin.animate.next_to(ostrich, RIGHT).shift(LEFT*0.56), run_time=0.5)
        
        self.play(butterfly.animate.next_to(arrow_right, DOWN).shift(RIGHT*0.6), run_time=0.5)
        self.play(peacock.animate.next_to(butterfly, RIGHT).shift(LEFT*0.35), run_time=0.5)
        self.play(bat.animate.next_to(butterfly, DOWN).shift(UP*0.46), run_time=0.5)
        self.play(eagle.animate.next_to(peacock, DOWN).shift(UP*0), run_time=0.5)

        self.play(self.camera.frame.animate.scale(0.8).shift(DOWN+RIGHT*3))
        self.wait(2)

        gini_left = Tex(r"Gini_{No} = 1 - (p_{yes}^2 + p_{no}^2)").next_to(ellipse, RIGHT).shift(RIGHT*1.28).scale(1.2)
        self.play(ShowCreation(gini_left))
        self.wait()

        rect = SurroundingRectangle(Group(cat, elephant, penguin, ostrich), stroke_width=6).scale(0.94)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(Group(cat, elephant,), stroke_width=6).scale(0.9).shift(UP*0.15)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(Group( penguin, ostrich), stroke_width=6).scale(0.9).shift(DOWN*0.15+RIGHT*0.14)))
 
        self.wait(2)


        self.play(Transform(gini_left, Tex(r"Gini_{No} = 1 - \left(\left(\tfrac{2}{4}\right)^{2} + \left(\tfrac{2}{4}\right)^{2}\right)").move_to(gini_left).scale(1.2)), Uncreate(rect))
        self.wait(2)

        self.play(Transform(gini_left, Tex(r"Gini_{No} = 0.5").scale(1.36).move_to(gini_left)))

        self.wait(2)

        gini_right = Tex(r"Gini_{Yes} = 1 - (p_{yes}^2 + p_{no}^2)").next_to(gini_left, DOWN).scale(1.02).shift(DOWN*0.32)
        self.play(ShowCreation(gini_right))
        self.wait(1)

        rect = SurroundingRectangle(Group(butterfly, peacock, bat, eagle), stroke_width=6).scale(0.94).shift(DOWN*0.14)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(Group(butterfly, bat,), stroke_width=6).scale(0.9).shift(DOWN*0.25)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(Group( peacock, eagle), stroke_width=6).scale(0.99)))
 
        self.wait(2)


        self.play(Transform(gini_right, Tex(r"Gini_{Yes} = 1 - \left(\left(\tfrac{2}{4}\right)^{2} + \left(\tfrac{2}{4}\right)^{2}\right)").move_to(gini_right).scale(1.02)), Uncreate(rect))
        self.wait(2)

        self.play(Transform(gini_right, Tex(r"Gini_{Yes} = 0.5").scale(1.36).move_to(gini_right)))

        self.wait(2)   

        rect_left = SurroundingRectangle(Group(cat, elephant, penguin, ostrich), stroke_width=6).scale(0.94).set_color(RED).shift(RIGHT*0.13)
        rect_gini_left = SurroundingRectangle(gini_left, color=RED, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect_left), ShowCreation(rect_gini_left))
        self.wait(2)

        rect_right = SurroundingRectangle(Group(butterfly, peacock, bat, eagle), stroke_width=6).scale(0.94).set_color(GREEN).shift(RIGHT*0.13+DOWN*0.14)
        rect_gini_right = SurroundingRectangle(gini_right, color=GREEN, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect_right), ShowCreation(rect_gini_right))
        self.wait(2)

        final_canfly = Tex(r"\left(\tfrac{4}{8}\right)\cdot 0.5 + \left(\tfrac{4}{8}\right)\cdot 0.5").next_to(Group(peacock, eagle), RIGHT).scale(1.1*1.1).shift(RIGHT*0.44)
        self.play(ShowCreation(final_canfly), Uncreate(VGroup(rect_right, rect_left, rect_gini_right, rect_gini_left)))
        self.wait(2)

        self.play(Transform(final_canfly, Tex("Gini_{CanFly} = 0.5").move_to(final_canfly).scale(1.15)))

        self.wait(2)

        self.play(FadeOut(Group(gini_left, gini_right)), final_canfly.animate.shift(UP*4.7) )
        self.wait(2)

        self.play(FadeOut(final_canfly))

        self.play(Transform(ellipse, Ellipse(
            width=4, 
            height=1.5, 
            fill_color=YELLOW, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).move_to(ellipse)),
        Transform(feature_text,  Text(
            "LaysEggs", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse).set_color(BLACK)))

        self.wait()

        temp_a = penguin.get_center()
        temp_b = bat.get_center()


        self.play(bat.animate.move_to(temp_a), penguin.animate.next_to(temp_b, LEFT).shift(RIGHT*0.26), ostrich.animate.next_to(peacock, DOWN).shift(RIGHT*0.37), eagle.animate.shift(LEFT*1.2))
        self.wait(2)

        gini_left = Tex(r"Gini_{No} = 1 - (p_{yes}^2 + p_{no}^2)").next_to(ellipse, RIGHT).shift(RIGHT*1.28).scale(1.2)
        self.play(ShowCreation(gini_left))
        self.wait()

        rect = SurroundingRectangle(Group(cat, elephant, bat,), stroke_width=6).scale(0.94)
        self.play(ShowCreation(rect))

        self.wait(2)



        self.play(Transform(gini_left, Tex(r"Gini_{No} = 1 - (0^2 + 1^2)").move_to(gini_left).scale(1.2)), Uncreate(rect))
        self.wait(2)

        self.play(Transform(gini_left, Tex(r"Gini_{No} = 0").scale(1.36).move_to(gini_left).scale(1.13)))

        self.wait(2)

        gini_right = Tex(r"Gini_{Yes} = 1 - (p_{yes}^2 + p_{no}^2)").next_to(gini_left, DOWN).scale(1.02).shift(DOWN*0.32)
        self.play(ShowCreation(gini_right))
        self.wait(1)

        rect = SurroundingRectangle(Group(butterfly, peacock, penguin, ostrich,eagle), stroke_width=6).scale(0.94).shift(DOWN*0.14)
        self.play(ShowCreation(rect))

        self.wait(2)


        self.play(Transform(gini_right, Tex(r"Gini_{Yes} = 1 - \left(\left(\tfrac{4}{5}\right)^{2} + \left(\tfrac{1}{5}\right)^{2}\right)").move_to(gini_right).scale(1.02)), Uncreate(rect))
        self.wait(2)

        self.play(Transform(gini_right, Tex(r"Gini_{Yes} = 0.32").scale(1.36).move_to(gini_right)))

        self.wait(2)   

        rect_left = SurroundingRectangle(Group(cat, elephant, bat, ), stroke_width=6).scale(0.94).set_color(RED).shift(RIGHT*0)
        rect_gini_left = SurroundingRectangle(gini_left, color=RED, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect_left), ShowCreation(rect_gini_left))
        self.wait(2)

        rect_right = SurroundingRectangle(Group(butterfly, peacock,penguin, eagle, ostrich), stroke_width=6).scale(0.94).set_color(GREEN).shift( DOWN*0.14)
        rect_gini_right = SurroundingRectangle(gini_right, color=GREEN, stroke_width=6).scale(1.1)
        self.play(ShowCreation(rect_right), ShowCreation(rect_gini_right))
        self.wait(2)

        final_layeggs = Tex(r"\left(\tfrac{3}{8}\right)\cdot 0 + \left(\tfrac{5}{8}\right)\cdot 0.32").next_to(Group(peacock, eagle), RIGHT).scale(1.1*1.1).shift(RIGHT*0.44)
        self.play(ShowCreation(final_layeggs), Uncreate(VGroup(rect_right, rect_left, rect_gini_right, rect_gini_left)))
        self.wait(2)

        self.play(Transform(final_layeggs, Tex("Gini_{LayEggs} = 0.2").move_to(final_layeggs).scale(1.15)))

        self.wait(2)

        self.play(FadeOut(Group(gini_left, gini_right)), final_layeggs.animate.next_to(final_canfly, DOWN).shift(DOWN*0.13) )
        self.play(FadeIn(final_canfly))


        self.wait(2)

        final_eatmeat = Tex("Gini_{EatsMeat} = 0.333").next_to(final_layeggs, DOWN).scale(1.15).shift(DOWN*0.13)
        self.play(ShowCreation(final_eatmeat))
        self.wait(2)

        rect = SurroundingRectangle(final_layeggs, stroke_width=6, color=BLUE).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(3)

        self.play(Uncreate(VGroup(final_canfly, final_eatmeat, final_layeggs, rect)), self.camera.frame.animate.shift(LEFT*2.6))
        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN))

        not_bird = Rectangle(color=RED, fill_color=RED, fill_opacity=0.65, height=1, width=4.4).next_to(Group(cat, elephant, bat), DOWN, buff=0.6)
        not_bird_text = Text("Not Bird", weight=BOLD).move_to(not_bird).scale(1.8).set_color(WHITE)
        not_bird = VGroup(not_bird, not_bird_text).next_to(bat, DOWN).scale(0.7).shift(LEFT*0.5)
        self.play(GrowFromCenter(not_bird))
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN+RIGHT*3.46))

        rect = SurroundingRectangle(Group(peacock, penguin, ostrich,), stroke_width=6).set_color(BLUE)
        self.play(ShowCreation(rect))
        self.wait(2)

        gini = Tex(r"Gini = 1 - (p_{no}^2 + p_{yes}^2)").next_to(rect, RIGHT).scale(1.5).shift(RIGHT*1.9)

        self.play(ShowCreation(gini))
        self.wait(2)

        self.play(Transform(gini, Tex(r"Gini = 1 - \left(\left(\tfrac{1}{5}\right)^2 + \left(\tfrac{4}{5}\right)^2\right)").scale(1.5).move_to(gini)))
        self.wait(2)

        self.play(Transform(gini, Tex(r"Gini = 0.32").scale(2).move_to(gini)))

        self.play(gini.animate.shift(UP*4), Uncreate(rect))
        self.wait(2)

        gini_canfly = Tex(r"Gini_{CanFly} = 0.266").scale(2).next_to(gini, DOWN).shift(DOWN*0.45)
        self.play(ShowCreation(gini_canfly))
        self.wait(2)
        gini_eatmeat = Tex(r"Gini_{EatsMeat} = 0").scale(2).next_to(gini_canfly, DOWN).shift(DOWN*0.45)
        self.play(ShowCreation(gini_eatmeat))
        self.wait(2)

        rect = SurroundingRectangle(gini_eatmeat, color=GREEN, stroke_width=6).scale(1.17)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(FadeOut(VGroup(rect, gini_canfly, gini_eatmeat, gini)))


        self.play(Group(butterfly, peacock, penguin, eagle, ostrich).animate.shift(RIGHT*6.6))



        # Create ellipse with full opacity fill
        ellipse_right = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=PURPLE, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(arrow_right.get_center(), DOWN, buff=1.23).shift(RIGHT*2+UP*0.3)
        
        # Text inside ellipse
        feature_text_right = Text(
            "EatsMeat", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse_right.get_center()).set_color(WHITE).set_z_index(1)
        # Arrows with z_index = -1 (behind other elements)
        arrow_right_left = Arrow(
            start=ellipse_right.get_center(), 
            end=ellipse_right.get_center() + LEFT*2 + DOWN*3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right_right = Arrow(
            start=ellipse_right.get_center(), 
            end=ellipse_right.get_center() + RIGHT*2 + DOWN*3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label_left = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_right_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label_left = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse_right), Write(feature_text_right))
        self.wait(1)
        self.play(GrowArrow(arrow_right_right), GrowArrow(arrow_right_left))
        self.play(FadeIn(no_label_left), FadeIn(yes_label_left))
        self.wait(2)

        self.play(butterfly.animate.next_to(arrow_right_left, DOWN).shift(LEFT+UP*0.1))
        a = not_bird.copy().scale(0.76).next_to(butterfly, DOWN, buff=0.4).shift(UP*0.45)
        self.play(ShowCreation(a))
        self.wait(2)

        self.play(Group(penguin, peacock, eagle, ostrich).animate.next_to(arrow_right_right, DOWN,).shift(RIGHT))
        self.play(penguin.animate.next_to(peacock, LEFT, buff=0.2).shift(RIGHT*0.4), Group(eagle, ostrich).animate.shift(LEFT*0.45))
         
        bird_rect = Rectangle(color=GREEN, fill_color=GREEN, fill_opacity=0.65, height=1.1, width=2.5).next_to(Group(penguin, ostrich), DOWN, buff=0.6)
        bird_text = Text("Bird", weight=BOLD).scale(2).move_to(bird_rect).set_color(WHITE)
        bird = VGroup(bird_rect, bird_text).next_to(Group(eagle, ostrich), DOWN).shift(UP*0.2).scale(0.65)
        self.play(ShowCreation(bird))
        self.wait(2)

        self.play(FadeOut(Group(cat,elephant, bat, butterfly, penguin, peacock, eagle, ostrich)),
        not_bird.animate.move_to(Group(cat, elephant)), a.animate.next_to(butterfly, ORIGIN).shift(UP*0.3).scale(1.5),
        bird.animate.move_to(Group(penguin, peacock)))

        self.wait(1)




    class FeatureTypes(Scene):
    def construct(self):
        self.camera.frame.scale(1.31).shift(0.7*UP)

        # ------------------------------------------------------------- #
        # 1. data v1 (replace EatsMeat with Weight: Low/Medium/High)
        # ------------------------------------------------------------- #
        # Legend:
        # - Weight: Low/Medium/High (categorical, non-binary)
        # - Keep CanFly, LaysEggs, Bird as Yes/No
        data_v1 = [
            ["Name",      "CanFly", "Weight",  "LaysEggs", "Bird"],
            ["Eagle",     "Yes",    "Medium",  "Yes",      "Yes"],
            ["Bat",       "Yes",    "Low",     "No",       "No"],
            ["Butterfly", "Yes",    "Low",     "Yes",      "No"],
            ["Penguin",   "No",     "Medium",  "Yes",      "Yes"],
            ["Elephant",  "No",     "High",    "No",       "No"],
            ["Ostrich",   "No",     "High",    "Yes",      "Yes"],
            ["Peacock",   "Yes",    "Medium",  "Yes",      "Yes"],
            ["Cat",       "No",     "Low",     "No",       "No"],
        ]

        # Colors
        column_colors_v1 = [BLUE, PURPLE, PINK, ORANGE, TEAL]
        yes_color, no_color = GREEN, RED
        # Weight category colors
        weight_low_color = YELLOW
        weight_med_color = GOLD
        weight_high_color = MAROON_B

        # ------------------------------------------------------------- #
        # 2. build Text objects v1
        # ------------------------------------------------------------- #
        text_rows_v1 = [
            [
                Text(str(cell), weight="BOLD", color=BLACK).set_color(BLACK) if r == 0 else Text(str(cell))
                for c, cell in enumerate(row)
            ]
            for r, row in enumerate(data_v1)
        ]
        n_rows_v1, n_cols_v1 = len(text_rows_v1), len(text_rows_v1[0])

        # ------------------------------------------------------------- #
        # 3. geometry v1
        # ------------------------------------------------------------- #
        col_w_v1 = [max(text_rows_v1[r][c].get_width() for r in range(n_rows_v1)) + 0.8
                    for c in range(n_cols_v1)]
        row_h_v1 = max(m.get_height() for row in text_rows_v1 for m in row) + 0.6
        tot_w_v1, tot_h_v1 = sum(col_w_v1), n_rows_v1 * row_h_v1

        # ------------------------------------------------------------- #
        # 4. build backgrounds & position text v1
        # ------------------------------------------------------------- #
        cell_bgs_v1, cell_txts_v1 = VGroup(), VGroup()

        for r in range(n_rows_v1):
            for c in range(n_cols_v1):
                x = -tot_w_v1/2 + sum(col_w_v1[:c]) + col_w_v1[c]/2
                y =  tot_h_v1/2 - (r + 0.5)*row_h_v1

                txt = text_rows_v1[r][c].move_to([x, y, 0])
                bg = Rectangle(width=col_w_v1[c], height=row_h_v1, stroke_width=0).move_to([x, y, 0])

                # coloring rules
                if r == 0:  # header row
                    bg.set_fill(YELLOW, opacity=0.66)
                else:
                    # default column tint
                    bg.set_fill(column_colors_v1[c], opacity=0.3)
                    val = data_v1[r][c]
                    # Binary columns: Yes/No
                    if c in [1, 3, 4]:
                        if val == "Yes":
                            bg.set_fill(yes_color, opacity=0.5)
                        elif val == "No":
                            bg.set_fill(no_color, opacity=0.5)
                    # Weight categorical column
                    if c == 2:
                        if val == "Low":
                            bg.set_fill(PURPLE, opacity=0.5)
                        elif val == "Medium":
                            bg.set_fill(weight_med_color, opacity=0.5)
                        elif val == "High":
                            bg.set_fill(weight_high_color, opacity=0.5)

                cell_bgs_v1.add(bg)
                cell_txts_v1.add(txt)

        # ------------------------------------------------------------- #
        # 5. grid v1
        # ------------------------------------------------------------- #
        grid_v1 = VGroup(Rectangle(width=tot_w_v1, height=tot_h_v1, stroke_width=2))
        x_cur = -tot_w_v1/2
        for w in col_w_v1[:-1]:
            x_cur += w
            grid_v1.add(Line([x_cur,  tot_h_v1/2, 0], [x_cur, -tot_h_v1/2, 0], stroke_width=1.5))
        y_cur = tot_h_v1/2
        for _ in range(n_rows_v1-1):
            y_cur -= row_h_v1
            grid_v1.add(Line([-tot_w_v1/2, y_cur, 0], [tot_w_v1/2, y_cur, 0], stroke_width=1.5))

        # ------------------------------------------------------------- #
        # 6. assemble & animate v1
        # ------------------------------------------------------------- #
        table_v1 = VGroup(cell_bgs_v1, grid_v1, cell_txts_v1).scale(0.8).center()
        title_v1 = Text("Animal Dataset (Weight categorical)", font_size=64, weight=BOLD).next_to(table_v1, UP, buff=0.6)

        self.play(Write(title_v1))
        self.play(ShowCreation(grid_v1), run_time=1)
        self.play(FadeIn(cell_bgs_v1), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, cell_txts_v1, shift=0.1*UP, lag_ratio=0.06), run_time=2)
        self.wait(1.5)


        # Optional highlight Name column
        def get_cell_v1(r, c):
            return cell_bgs_v1[r*n_cols_v1 + c]

        rect = SurroundingRectangle(VGroup(get_cell_v1(0,2), get_cell_v1(n_rows_v1-1,2)),
                                    fill_color=WHITE, color=WHITE, fill_opacity=0.3)
        self.play(ShowCreation(rect))
        self.wait(1)
        self.play(FadeOut(rect))

        # ------------------------------------------------------------- #
        # 7. Build one-hot version (Weight -> 3 binary columns)
        # ------------------------------------------------------------- #
        # New columns: W=Low, W=Medium, W=High, keep others
        # Order: Name, CanFly, W=Low, W=Medium, W=High, LaysEggs, Bird
        def one_hot_weight(val):
            return ["Yes" if val=="Low" else "No",
                    "Yes" if val=="Medium" else "No",
                    "Yes" if val=="High" else "No"]

        data_v2 = []
        # Header
        data_v2.append(["Name", "CanFly", "W=Low", "W=Medium", "W=High", "LaysEggs", "Bird"])
        for r in range(1, len(data_v1)):
            name, canfly, weight, lay, bird = data_v1[r]
            w_low, w_med, w_high = one_hot_weight(weight)
            data_v2.append([name, canfly, w_low, w_med, w_high, lay, bird])

        # Colors per column for v2
        # Keep consistent base hues, and let Yes/No override for binary columns
        column_colors_v2 = [BLUE, PURPLE, YELLOW, GOLD, MAROON_B, ORANGE, TEAL]

        # Build text objects v2
        text_rows_v2 = [
            [
                Text(str(cell), weight="BOLD", color=BLACK).set_color(BLACK) if r == 0 else Text(str(cell))
                for c, cell in enumerate(row)
            ]
            for r, row in enumerate(data_v2)
        ]
        n_rows_v2, n_cols_v2 = len(text_rows_v2), len(text_rows_v2[0])

        # Geometry v2
        col_w_v2 = [max(text_rows_v2[r][c].get_width() for r in range(n_rows_v2)) + 0.8
                    for c in range(n_cols_v2)]
        row_h_v2 = max(m.get_height() for row in text_rows_v2 for m in row) + 0.6
        tot_w_v2, tot_h_v2 = sum(col_w_v2), n_rows_v2 * row_h_v2

        # Build backgrounds & text v2
        cell_bgs_v2, cell_txts_v2 = VGroup(), VGroup()
        for r in range(n_rows_v2):
            for c in range(n_cols_v2):
                x = -tot_w_v2/2 + sum(col_w_v2[:c]) + col_w_v2[c]/2
                y =  tot_h_v2/2 - (r + 0.5)*row_h_v2
                txt = text_rows_v2[r][c].move_to([x, y, 0])
                bg = Rectangle(width=col_w_v2[c], height=row_h_v2, stroke_width=0).move_to([x, y, 0])

                if r == 0:
                    bg.set_fill(YELLOW, opacity=0.66)
                else:
                    # default base tint
                    bg.set_fill(column_colors_v2[c], opacity=0.3)
                    val = data_v2[r][c]
                    # All non-name columns in v2 are binary Yes/No
                    if c != 0:
                        if val == "Yes":
                            bg.set_fill(yes_color, opacity=0.5)
                        elif val == "No":
                            bg.set_fill(no_color, opacity=0.5)

                cell_bgs_v2.add(bg)
                cell_txts_v2.add(txt)

        # Grid v2
        grid_v2 = VGroup(Rectangle(width=tot_w_v2, height=tot_h_v2, stroke_width=2))
        x_cur = -tot_w_v2/2
        for w in col_w_v2[:-1]:
            x_cur += w
            grid_v2.add(Line([x_cur,  tot_h_v2/2, 0], [x_cur, -tot_h_v2/2, 0], stroke_width=1.5))
        y_cur = tot_h_v2/2
        for _ in range(n_rows_v2-1):
            y_cur -= row_h_v2
            grid_v2.add(Line([-tot_w_v2/2, y_cur, 0], [tot_w_v2/2, y_cur, 0], stroke_width=1.5))

        table_v2 = VGroup(cell_bgs_v2, grid_v2, cell_txts_v2).scale(0.8).center()
        title_v2 = Text("One-Hot Encoded Weight", font_size=64, weight=BOLD).next_to(table_v2, UP, buff=0.6)

        # ------------------------------------------------------------- #
        # 8. Transform animation: table_v1 -> table_v2
        # ------------------------------------------------------------- #
        # Strategy:
        # - Fade out old title, bring in new title
        # - Morph table position/scale if needed, crossfade old group to new
        self.play(FadeOut(title_v1))
        self.play(ReplacementTransform(table_v1, table_v2), run_time=0.7)
        self.play(Write(title_v2))
        self.wait(2)

        # Optionally, emphasize the new three columns
        def get_cell_v2(r, c):
            return cell_bgs_v2[r*n_cols_v2 + c]
        # Surround the three new columns across all rows
        col_group = VGroup(
            *[get_cell_v2(r, 2) for r in range(n_rows_v2)],
            *[get_cell_v2(r, 3) for r in range(n_rows_v2)],
            *[get_cell_v2(r, 4) for r in range(n_rows_v2)],
        )
        brace = Brace(col_group, direction=UP)
        brace_label = Text("Weight one-hot: Low / Medium / High", font_size=36)
        brace_label.next_to(brace, UP, buff=0.2)
        

        rect = SurroundingRectangle(VGroup(get_cell_v1(0,2), get_cell_v1(0,4),),
                                    fill_color=WHITE, color=WHITE, fill_opacity=0.3)
        self.play(ShowCreation(rect))

        self.wait(2)

        # Group the three weight columns across all rows (v2)
        full_cols_group = VGroup(
            *[get_cell_v2(r, 2) for r in range(n_rows_v2)],
            *[get_cell_v2(r, 3) for r in range(n_rows_v2)],
            *[get_cell_v2(r, 4) for r in range(n_rows_v2)],
        )
        # Target rectangle covering all rows of columns 2–4 in v2
        target_rect = SurroundingRectangle(
            full_cols_group,
            fill_color=WHITE, color=WHITE, fill_opacity=0.3
        )
        # Animate the rectangle to expand to the full three-column block
        self.play(ReplacementTransform(rect, target_rect), run_time=0.9)
        self.wait(2)

        self.play(FadeOut(target_rect))

        # ------------------------------------------------------------- #
        # 9. Transform to a new table (continuous Weight + binary target)
        #    Features: Name, Weight(kg), CanFly, LaysEggs
        #    Target: Bird (binary Yes/No)
        # ------------------------------------------------------------- #

        data_v3 = [
            ["Name", "Weight(kg)", "CanFly", "LaysEggs", "Bird"],  # keep Bird as binary output
            ["Eagle",     "6.5",    "Yes", "Yes", "Yes"],
            ["Bat",       "0.03",   "Yes", "No",  "No"],
            ["Butterfly", "0.0005", "Yes", "Yes", "No"],
            ["Penguin",   "10.0",   "No",  "Yes", "Yes"],
            ["chicken",   "2.0",  "No",  "Yes", "Yes"],
            ["Peacock",   "4.5",    "Yes", "Yes", "Yes"],
            ["Cat",       "4.0",    "No",  "No",  "No"],
            ["Snake",       "3.0",    "No",  "Yes",  "No"],
        ]

        # Column base colors for v3 (Weight neutral tint; Bird highlighted)
        column_colors_v3 = [BLUE, GREY, PURPLE, ORANGE, TEAL]
        yes_color, no_color = GREEN, RED

        title_v3 = Text("Continuous Weight", font_size=64, weight=BOLD)

        # Build text objects v3
        text_rows_v3 = [
            [
                Text(str(cell), weight="BOLD", color=BLACK).set_color(BLACK) if r == 0 else Text(str(cell))
                for c, cell in enumerate(row)
            ]
            for r, row in enumerate(data_v3)
        ]
        n_rows_v3, n_cols_v3 = len(text_rows_v3), len(text_rows_v3[0])

        # Geometry v3
        col_w_v3 = [max(text_rows_v3[r][c].get_width() for r in range(n_rows_v3)) + 0.8
                    for c in range(n_cols_v3)]
        row_h_v3 = max(m.get_height() for row in text_rows_v3 for m in row) + 0.6
        tot_w_v3, tot_h_v3 = sum(col_w_v3), n_rows_v3 * row_h_v3

        # Build backgrounds & text v3
        cell_bgs_v3, cell_txts_v3 = VGroup(), VGroup()
        for r in range(n_rows_v3):
            for c in range(n_cols_v3):
                x = -tot_w_v3/2 + sum(col_w_v3[:c]) + col_w_v3[c]/2
                y =  tot_h_v3/2 - (r + 0.5)*row_h_v3
                txt = text_rows_v3[r][c].move_to([x, y, 0])
                bg = Rectangle(width=col_w_v3[c], height=row_h_v3, stroke_width=0).move_to([x, y, 0])

                if r == 0:
                    bg.set_fill(YELLOW, opacity=0.66)
                else:
                    # Base tint
                    bg.set_fill(column_colors_v3[c], opacity=0.3)
                    val = data_v3[r][c]
                    # Binary columns: CanFly (2), LaysEggs (3), Bird (4)
                    if c in [2, 3, 4]:
                        if val == "Yes":
                            bg.set_fill(yes_color, opacity=0.5)
                        elif val == "No":
                            bg.set_fill(no_color, opacity=0.5)

                cell_bgs_v3.add(bg)
                cell_txts_v3.add(txt)

        # Grid v3
        grid_v3 = VGroup(Rectangle(width=tot_w_v3, height=tot_h_v3, stroke_width=2))
        x_cur = -tot_w_v3/2
        for w in col_w_v3[:-1]:
            x_cur += w
            grid_v3.add(Line([x_cur,  tot_h_v3/2, 0], [x_cur, -tot_h_v3/2, 0], stroke_width=1.5))
        y_cur = tot_h_v3/2
        for _ in range(n_rows_v3-1):
            y_cur -= row_h_v3
            grid_v3.add(Line([-tot_w_v3/2, y_cur, 0], [tot_w_v3/2, y_cur, 0], stroke_width=1.5))

        table_v3 = VGroup(cell_bgs_v3, grid_v3, cell_txts_v3).scale(0.8).center()
        title_v3.next_to(table_v3, UP, buff=0.6)

        # Animate transform from v2 -> v3
        self.play(FadeOut(title_v2))
        self.play(Transform(table_v2, table_v3), run_time=1.0)
        self.play(Write(title_v3))
        self.wait(2)

        peacock = ImageMobject("peacock.png").shift(RIGHT*16.45).scale(0.4)
        eagle = ImageMobject("eagle.png").scale(0.4).next_to(peacock, RIGHT)
        elephant = ImageMobject("snake.png").scale(0.4).next_to(eagle, RIGHT)
        bat = ImageMobject("bat.png").scale(0.4).next_to(peacock, LEFT)
        butterfly = ImageMobject("butterfly.png").scale(0.6).next_to(bat, LEFT)
        ostrich = ImageMobject("chicken.png").scale(0.6).next_to(butterfly, LEFT)
        penguin = ImageMobject("penguin.png").scale(0.606).next_to(elephant, RIGHT)
        cat = ImageMobject("cat.png").scale(0.6).next_to(ostrich, LEFT)

        self.play(self.camera.frame.animate.shift(RIGHT*15))
        self.add(eagle, peacock, elephant, bat, butterfly, ostrich, penguin, cat)
        self.wait(2)
        
        total = Group(eagle, cat, ostrich, butterfly, bat, peacock, elephant, penguin)

        self.play(total.animate.scale(0.85).shift(UP*4.1))
 
        
        
        # Create ellipse with full opacity fill
        ellipse = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=YELLOW, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(total, DOWN, buff=1).shift(UP*0.8)
        
        # Text inside ellipse
        feature_text = Tex(
            r"weight \geq X", 
            font_size=60, 
        ).move_to(ellipse.get_center()).set_color(BLACK)
        # Arrows with z_index = -1 (behind other elements)
        arrow_left = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + LEFT*3 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + RIGHT*3 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse), Write(feature_text))
        self.wait(1)
        self.play(GrowArrow(arrow_left), GrowArrow(arrow_right))
        self.play(FadeIn(no_label), FadeIn(yes_label))
        self.wait(2)

        self.play(Transform(feature_text, Tex(r'weight \geq 4.25', font_size = 50,  ).set_color(BLACK).move_to(feature_text)))
        self.wait(2)

        self.play(butterfly.animate.next_to(arrow_left, DOWN).shift(LEFT*2.7+UP*0.2), run_time=0.5)
        self.play(cat.animate.next_to(butterfly, DOWN).shift(UP*0.77+LEFT*0.4), run_time=0.5)
        self.play(bat.animate.next_to(butterfly, RIGHT), run_time=0.5)
        self.play(elephant.animate.next_to(cat, RIGHT).shift(LEFT*0.29), run_time=0.5)
        self.play(ostrich.animate.next_to(elephant, RIGHT).shift(LEFT*0.29), run_time=0.5)
        self.play(eagle.animate.next_to(arrow_right, DOWN).shift(RIGHT*0.7+DOWN*0.2), run_time=0.5)
        self.play(peacock.animate.next_to(eagle, RIGHT), run_time=0.5)
        self.play(penguin.animate.next_to(Group(eagle, peacock), DOWN).shift(UP*0.4), run_time=0.5)
        self.play(self.camera.frame.animate.scale(0.8).shift(DOWN))
        self.wait(2)


        self.play(FadeOut(Group(ellipse, feature_text, no_label, yes_label, arrow_left, arrow_right, butterfly, bat, cat, elephant, ostrich, eagle, peacock, penguin)))

        # Extract (name, weight, is_bird) from data_v3 (skip header)
        rows_v3 = data_v3[1:]
        parsed = []
        for name, w_str, canfly, lay, bird in rows_v3:
            try:
                w_val = float(w_str)
            except:
                w_val = 0.0
            is_bird = (bird == "Yes")
            parsed.append((name, w_val, is_bird))

        # Sort ascending by weight
        parsed.sort(key=lambda t: t[1])

        # Build Text labels ONLY for weights in increasing order
        weight_texts = []
        weight_font_size = 44
        for name, w, is_bird in parsed:
            # show just the numeric weight
            weight_texts.append(Text(f"{w:g}", font_size=weight_font_size))

        # Arrange vertically: smallest on top, then increasing downwards
        weights_column = VGroup(*weight_texts)
        # spacing between lines
        vertical_gap = 0.6
        # Arrange uses DOWN so items go top -> bottom
        if len(weights_column) > 1:
            weights_column.arrange(DOWN, buff=vertical_gap)
        # Position near the old ellipse location; adjust as desired
        # Center on screen and lift slightly
        weights_column.move_to(ellipse).shift(DOWN*2.2+LEFT*4)
        

        self.play(ShowCreation(weights_column))
        self.wait(2)


        # 1) Parse and sort weights ascending from data_v3 (skip header)
        rows_v3 = data_v3[1:]
        weights_only = []
        for name, w_str, canfly, lay, bird in rows_v3:
            try:
                weights_only.append(float(w_str))
            except:
                pass  # skip non-numeric

        weights_only.sort()

        # 2) Compute consecutive midpoints: (w0+w1)/2, (w1+w2)/2, ...
        mid_values = []
        for i in range(len(weights_only) - 1):
            mid_values.append(0.5 * (weights_only[i] + weights_only[i+1]))

        # 3) Build a vertical VGroup of Text for these midpoints
        midpoint_font_size = 42
        midpoint_texts = [Text(f"{m:.4g}", font_size=midpoint_font_size) for m in mid_values]
        midpoints_column = VGroup(*midpoint_texts)

        # Arrange vertically, top = first midpoint (between two smallest weights)
        if len(midpoints_column) > 1:
            midpoints_column.arrange(DOWN, buff=0.6)

        # Position on screen (adjust as desired)
        # If you want it exactly where the ellipse was, tweak these offsets.
        midpoints_column.next_to(weights_column, RIGHT, buff=1).shift(RIGHT)

        brace = Brace(weights_column[:2], RIGHT).set_color(YELLOW).shift(RIGHT*0.75)
        self.play(ShowCreation(brace))
        self.wait(1)

        self.play(ShowCreation(midpoints_column[0]))
        self.wait(1)

        self.play(Transform(brace, Brace(weights_column[1:3], RIGHT).set_color(YELLOW).shift(RIGHT*0.75) ))
        self.play(ShowCreation(midpoints_column[1]))
        
        self.play(Transform(brace, Brace(weights_column[2:4], RIGHT).set_color(YELLOW).shift(RIGHT*0.75) ))
        self.play(ShowCreation(midpoints_column[2]))

        self.play(Transform(brace, Brace(weights_column[3:5], RIGHT).set_color(YELLOW).shift(RIGHT*0.75) ))
        self.play(ShowCreation(midpoints_column[3]))

        self.play(ShowCreation(midpoints_column[4:]), Uncreate(brace))

        self.wait()

        rect = SurroundingRectangle(midpoints_column[0]).scale(1.1)

        self.play(ShowCreation(rect))

        self.wait()

        for i in range(1,7):
            self.play(Transform(rect, SurroundingRectangle(midpoints_column[i]).scale(1.17) ), run_time=0.97)

        self.wait(2)


        # YOUR PRECOMPUTED GINI VALUES (strings or numbers are fine)
        # If they are numbers, we’ll format them; if strings, we leave as-is.
        gini_values = [0.428, 0.333, 0.466, 0.375, 0.20, 0.333, 0.428]

        # Build Texts; keep numeric formatting consistent with your display
        gini_font_size = 42
        gini_texts = []
        for g in gini_values:
            if isinstance(g, (int, float)):
                gini_texts.append(Text(f"{g:.4g}", font_size=gini_font_size))
            else:
                gini_texts.append(Text(str(g), font_size=gini_font_size))

        ginis_column = VGroup(*gini_texts)

        # Arrange vertically with the same buff as midpoints_column to align rows
        if len(ginis_column) > 1:
            ginis_column.arrange(DOWN, buff=0.6)

        # Place to the RIGHT of midpoints_column
        ginis_column.next_to(midpoints_column, RIGHT, buff=1).shift(RIGHT)


        self.play(FadeOut(rect), FadeIn(ginis_column))
        self.wait(2)

        rect = SurroundingRectangle(ginis_column).scale(1.17)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(ginis_column[4]).scale(1.17) ), run_time=0.97)

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(midpoints_column[4]).scale(1.17) ), run_time=0.97)
        
        self.wait(2)
        self.play(self.camera.frame.animate.shift(LEFT*3+UP*1.14).scale(0.8))
        self.wait(2)

class Regression(Scene):
    def construct(self):

        self.camera.frame.scale(1.31).shift(0.7*UP)

        # Columns:
        # - Name (string)
        # - CanFly (Yes/No)
        # - Weight_cat (Low/Medium/High) for categorical display
        # - LaysEggs (Yes/No)
        # - Weight_kg (numeric) for regression

        # Replacements: Elephant -> Snake, Ostrich -> Chicken

        data_v2 = [
            ["Name",      "CanFly", "EatsMeat", "LaysEggs", "Weight"],
            ["Eagle",     "Yes",    "Yes",     "Yes",      4.0],
            ["Bat",       "Yes",    "Yes",        "No",       0.03],
            ["Butterfly", "Yes",    "No",        "Yes",      0.0005],
            ["Penguin",   "No",     "Yes",     "Yes",      10.0],
            ["Snake",     "No",     "Yes",        "Yes",      2.0],
            ["Chicken",   "No",     "Yes",        "Yes",      2.5],
            ["Peacock",   "Yes",    "Yes",     "Yes",      4.5],
            ["Cat",       "No",     "Yes",        "No",       4.0],
        ]

        # Colors
        column_colors_v2 = [BLUE, PURPLE, PINK, ORANGE, TEAL]
        yes_color, no_color = GREEN, RED
        # Weight categorical colors
        weight_low_color  = YELLOW
        weight_med_color  = GOLD
        weight_high_color = MAROON_B

        # Numeric weight color scale (low->high): BLUE_E to BLUE_A
        def weight_to_color(w, w_min, w_max):
            # Normalize 0..1
            t = 0 if w_max == w_min else (w - w_min) / (w_max - w_min)
            # Interpolate between darker to lighter blue
            return interpolate_color(PURPLE_E, PURPLE_E, t)

        # ------------------------------------------------------------- #
        # 2) Build Text objects (header bold)
        # ------------------------------------------------------------- #
        text_rows_v2 = [
            [
                Text(str(cell), weight="BOLD", color=BLACK).set_color(BLACK) if r == 0
                else Text(str(cell))
                for c, cell in enumerate(row)
            ]
            for r, row in enumerate(data_v2)
        ]
        n_rows_v2, n_cols_v2 = len(text_rows_v2), len(text_rows_v2[0])

        # ------------------------------------------------------------- #
        # 3) Geometry
        # ------------------------------------------------------------- #
        col_w_v2 = [
            max(text_rows_v2[r][c].get_width() for r in range(n_rows_v2)) + 0.8
            for c in range(n_cols_v2)
        ]
        row_h_v2 = max(m.get_height() for row in text_rows_v2 for m in row) + 0.6
        tot_w_v2, tot_h_v2 = sum(col_w_v2), n_rows_v2 * row_h_v2

        # Precompute numeric weight domain
        weight_col_idx = 4
        weights = [row[weight_col_idx] for row in data_v2[1:]]
        w_min, w_max = min(weights), max(weights)

        # ------------------------------------------------------------- #
        # 4) Build backgrounds & position text with coloring rules
        # ------------------------------------------------------------- #
        cell_bgs_v2, cell_txts_v2 = VGroup(), VGroup()

        for r in range(n_rows_v2):
            for c in range(n_cols_v2):
                x = -tot_w_v2/2 + sum(col_w_v2[:c]) + col_w_v2[c]/2
                y =  tot_h_v2/2 - (r + 0.5)*row_h_v2

                txt = text_rows_v2[r][c].move_to([x, y, 0])
                bg  = Rectangle(width=col_w_v2[c], height=row_h_v2, stroke_width=0).move_to([x, y, 0])

                if r == 0:  # header
                    bg.set_fill(YELLOW, opacity=0.66)
                else:
                    # Base tint
                    bg.set_fill(column_colors_v2[c], opacity=0.25)
                    val = data_v2[r][c]

                    # Binary columns: CanFly (1), LaysEggs (3)
                    if c in [1, 3]:
                        if val == "Yes":
                            bg.set_fill(yes_color, opacity=0.5)
                        elif val == "No":
                            bg.set_fill(no_color, opacity=0.5)

                    # Categorical weight column: Weight_cat (2)
                    if c == 2:
                        if val == "Yes":
                            bg.set_fill(GREEN, opacity=0.5)
                        elif val == "No":
                            bg.set_fill(RED, opacity=0.5)
                        elif val == "High":
                            bg.set_fill(weight_high_color, opacity=0.5)

                    # Numeric weight column: Weight_kg (4)
                    if c == 4:
                        w = float(val)
                        bg.set_fill(weight_to_color(w, w_min, w_max), opacity=0.55)

                cell_bgs_v2.add(bg)
                cell_txts_v2.add(txt)

        # ------------------------------------------------------------- #
        # 5) Grid
        # ------------------------------------------------------------- #
        grid_v2 = VGroup(Rectangle(width=tot_w_v2, height=tot_h_v2, stroke_width=2))
        x_cur = -tot_w_v2/2
        for w in col_w_v2[:-1]:
            x_cur += w
            grid_v2.add(Line([x_cur,  tot_h_v2/2, 0], [x_cur, -tot_h_v2/2, 0], stroke_width=1.5))
        y_cur = tot_h_v2/2
        for _ in range(n_rows_v2-1):
            y_cur -= row_h_v2
            grid_v2.add(Line([-tot_w_v2/2, y_cur, 0], [tot_w_v2/2, y_cur, 0], stroke_width=1.5))

        # ------------------------------------------------------------- #
        # 6) Assemble & animate table
        # ------------------------------------------------------------- #
        table_v2 = VGroup(cell_bgs_v2, grid_v2, cell_txts_v2).scale(0.8).center()
        title_v2 = Text("Animal Dataset (For Regression)", font_size=64, weight=BOLD).next_to(table_v2, UP, buff=0.6)

        self.play(Write(title_v2))
        self.play(ShowCreation(grid_v2), run_time=1)
        self.play(FadeIn(cell_bgs_v2), run_time=1.5)
        self.play(LaggedStartMap(FadeIn, cell_txts_v2, shift=0.1*UP, lag_ratio=0.06), run_time=2)
        self.wait(1.0)

        # ------------------------------------------------------------- #
        # 7) Optional: highlight numeric Weight_kg column
        # ------------------------------------------------------------- #
        def get_bg_cell(r, c):
            return cell_bgs_v2[r*n_cols_v2 + c]

        num_col = weight_col_idx
        rect = SurroundingRectangle(
            VGroup(get_bg_cell(0,num_col), get_bg_cell(n_rows_v2-1,num_col)),
            fill_color=WHITE, color=WHITE, fill_opacity=0.2
        )
        self.play(ShowCreation(rect), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(rect), run_time=0.5)

        self.wait(2)

        peacock = ImageMobject("peacock.png").shift(RIGHT*16.45).scale(0.4)
        eagle = ImageMobject("eagle.png").scale(0.4).next_to(peacock, RIGHT)
        snake = ImageMobject("snake.png").scale(0.4).next_to(eagle, RIGHT)
        bat = ImageMobject("bat.png").scale(0.4).next_to(peacock, LEFT)
        butterfly = ImageMobject("butterfly.png").scale(0.6).next_to(bat, LEFT)
        chicken = ImageMobject("chicken.png").scale(0.6).next_to(butterfly, LEFT)
        penguin = ImageMobject("penguin.png").scale(0.606).next_to(snake, RIGHT)
        cat = ImageMobject("cat.png").scale(0.6).next_to(chicken, LEFT)

        self.play(self.camera.frame.animate.shift(RIGHT*15))
        self.add(eagle, peacock, snake, bat, butterfly, chicken, penguin, cat)
        self.wait(2)
        
        total = Group(eagle, cat, chicken, butterfly, bat, peacock, snake, penguin)

        self.play(total.animate.scale(0.85).shift(UP*4.2))

        self.wait(2)

        brace = Brace(total, DOWN, buff=0.6)
        self.play(ShowCreation(brace))

        text = Text("variance = 8.89").next_to(brace, DOWN).shift(DOWN*0.62).scale(1.5)
        self.play(ShowCreation(text))
        self.wait(2)

        self.play(FadeOut(VGroup(brace, text)))

        # Create ellipse with full opacity fill
        ellipse = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=BLUE, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(total, DOWN, buff=1).shift(UP*0.8).shift(LEFT*6)
        
        # Text inside ellipse
        feature_text = Text(
            "EatsMeat", font_size=64, weight=BOLD
        ).move_to(ellipse.get_center()).set_color(BLACK)
        # Arrows with z_index = -1 (behind other elements)

        arrow_left = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + LEFT*2 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right = Arrow(
            start=ellipse.get_center(), 
            end=ellipse.get_center() + RIGHT*2 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse), Write(feature_text))
        self.wait(1)
        self.play(GrowArrow(arrow_left), GrowArrow(arrow_right))
        self.play(FadeIn(no_label), FadeIn(yes_label))
        self.wait()

        cat_a = cat.copy()
        chicken_a = chicken.copy()
        butterfly_a = butterfly.copy()
        bat_a = bat.copy()
        peacock_a = peacock.copy()
        eagle_a = eagle.copy()
        snake_a = snake.copy()
        penguin_a = penguin.copy()

        self.play(butterfly_a.animate.next_to(arrow_right, DOWN+LEFT).shift(LEFT*1.2),self.camera.frame.animate.shift(DOWN*0.7),  run_time=1)
        self.play(cat_a.animate.next_to(arrow_right.get_bottom(), RIGHT).shift(LEFT*1.33+DOWN*1.34).shift(LEFT*0.3),
                  chicken_a.animate.next_to(arrow_right.get_bottom(), RIGHT).shift(LEFT*0.16+DOWN*1.34).shift(LEFT*0.3),
                  bat_a.animate.next_to(arrow_right.get_bottom(), RIGHT).shift(RIGHT*1.+DOWN*1.34).shift(LEFT*0.3),
                  peacock_a.animate.next_to(arrow_right.get_bottom(), RIGHT).shift(LEFT*2.3+DOWN*2.74).shift(RIGHT*1.64).shift(LEFT*0.3),
                  eagle_a.animate.next_to(arrow_right.get_bottom(), RIGHT).shift(LEFT*0.87+DOWN*2.74).shift(RIGHT*1.64).shift(LEFT*0.3),
                  snake_a.animate.next_to(arrow_right.get_bottom(), RIGHT).shift(DOWN*2.74+RIGHT*0.18).shift(LEFT*0.73+DOWN*1.48).shift(LEFT*0.3),
                penguin_a.animate.next_to(arrow_right.get_bottom(), RIGHT).shift(DOWN*2.74+RIGHT*1.38).scale(1).shift(LEFT*0.73+DOWN*1.48).shift(LEFT*0.3),
                              run_time=1)
        
        self.wait(2)


        ellipse2 = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(ellipse, RIGHT, buff=1.8).shift(RIGHT)

        
        feature_text2 = Text(
            "LaysEggs", font_size=64, weight=BOLD
        ).move_to(ellipse2.get_center()).set_color(BLACK)
        
        arrow2_left = Arrow(
            start=ellipse2.get_center(),
            end=ellipse2.get_center() + LEFT*2 + DOWN*2.3,
            color=RED,
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow2_right = Arrow(
            start=ellipse2.get_center(),
            end=ellipse2.get_center() + RIGHT*2 + DOWN*2.3,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        no_label2 = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow2_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label2 = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow2_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        self.play(FadeIn(ellipse2), Write(feature_text2))
        self.wait(1)
        self.play(GrowArrow(arrow2_left), GrowArrow(arrow2_right))
        self.play(FadeIn(no_label2), FadeIn(yes_label2))
        self.wait(2)
        
        # Animal groupings for LaysEggs
        # Use .copy() for these images!
        cat_b = cat.copy()
        bat_b = bat.copy()
        eagle_b = eagle.copy()
        penguin_b = penguin.copy()
        snake_b = snake.copy()
        peacock_b = peacock.copy()
        chicken_b = chicken.copy()
        butterfly_b = butterfly.copy()
        

        
        self.play(cat_b.animate.next_to(arrow2_right, DOWN+LEFT).shift(LEFT*1), 
                  bat_b.animate.next_to(arrow2_right, DOWN+LEFT).shift(LEFT*0.7+DOWN*1.65),run_time=1)
        

        self.play(
                  chicken_b.animate.next_to(arrow2_right.get_bottom(), RIGHT).shift(LEFT*0.56+DOWN*1.34).shift(LEFT),
                  butterfly_b.animate.next_to(arrow2_right.get_bottom(), RIGHT).shift(RIGHT*0.6+DOWN*1.34).shift(LEFT*0.9),
                  peacock_b.animate.next_to(arrow2_right.get_bottom(), RIGHT).shift(RIGHT*0.6+DOWN*1.34).shift(RIGHT*0.25),
                  eagle_b.animate.next_to(arrow2_right.get_bottom(), RIGHT).shift(LEFT*0.87+DOWN*2.74).shift(LEFT*0.8),
                  snake_b.animate.next_to(arrow2_right.get_bottom(), RIGHT).shift(DOWN*2.74+RIGHT*0.18).shift(LEFT*0.8),
                penguin_b.animate.next_to(arrow2_right.get_bottom(), RIGHT).shift(DOWN*2.74+RIGHT*1.38).scale(1.2).shift(LEFT*0.8),
                              run_time=1)
        
        self.wait(2)


        ### --- Feature 3: CanFly (ellipse: PURPLE_A, text: "CanFly") --- ###
        
        ellipse3 = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=PURPLE_A,
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(ellipse2, RIGHT, buff=1.8).shift(RIGHT)
        
        feature_text3 = Text(
            "CanFly", font_size=64, weight=BOLD
        ).move_to(ellipse3.get_center()).set_color(BLACK)
        
        arrow3_left = Arrow(
            start=ellipse3.get_center(),
            end=ellipse3.get_center() + LEFT*2 + DOWN*2.3,
            color=RED,
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow3_right = Arrow(
            start=ellipse3.get_center(),
            end=ellipse3.get_center() + RIGHT*2 + DOWN*2.3,
            color=GREEN,
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        no_label3 = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow3_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label3 = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow3_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        self.play(FadeIn(ellipse3), Write(feature_text3), self.camera.frame.animate.scale(1.1).shift(RIGHT*1.16))
        self.wait(1)
        self.play(GrowArrow(arrow3_left), GrowArrow(arrow3_right))
        self.play(FadeIn(no_label3), FadeIn(yes_label3), FadeOut(table_v2))

        
        self.play(cat.animate.next_to(arrow3_right, DOWN+LEFT).shift(LEFT*1.2), 
                  snake.animate.next_to(arrow3_right, DOWN+LEFT).shift(LEFT*1.23+DOWN*1.8),
                  penguin.animate.next_to(arrow3_right, DOWN+LEFT).shift(LEFT*1.18+DOWN*2.86).scale(1.2),run_time=1)
        

        self.play(
                  chicken.animate.next_to(arrow3_right.get_bottom(), RIGHT).shift(LEFT*0.16+DOWN*1.34).shift(LEFT),
                  butterfly.animate.next_to(arrow3_right.get_bottom(), RIGHT).shift(RIGHT*1.2+DOWN*1.34).shift(LEFT*0.9),
                  peacock.animate.next_to(arrow3_right.get_bottom(), RIGHT).shift(RIGHT*1.+DOWN*1.34).shift(LEFT*0.85+DOWN*1.4),
                  eagle.animate.next_to(arrow3_right.get_bottom(), RIGHT).shift(LEFT*1.67+DOWN*2.74).shift(RIGHT*0.4),
                bat.animate.next_to(arrow3_right.get_bottom(), RIGHT).shift(DOWN*4.2+RIGHT*1.38).scale(1).shift(LEFT*2.8),
                              run_time=1)
        
        self.play(self.camera.frame.animate.shift(DOWN*2))
        
        self.wait(2)

        tex = Tex(r"\left(\frac{1}{8}\right) \times 0 + \left(\frac{7}{8}\right) \times 8.3").next_to(snake_a, DOWN)
        tex.shift(DOWN*0.6+LEFT*0.65).scale(1.2)

        rect = SurroundingRectangle(butterfly_a).scale(1).set_color("#00ff00")

        self.play(ShowCreation(rect))

        self.wait()

        self.play(FadeIn(tex[6]))
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(Group(cat_a, snake_a, bat_a)).set_color("#00ff00")))
        self.wait(1)

        self.play(FadeIn(tex[-3:]))
        self.wait(2)

        self.play(FadeIn(tex[:6]))
        self.wait(2)
        self.play(FadeIn(tex[7:-3]))
        self.wait(2)

        self.play(Transform(tex, Text("7.26").move_to(tex).scale(2)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(Group(cat_b, peacock_b, bat_b, eagle_b)).set_color("#00ff00").scale(0.97).shift(DOWN*0.15)))
        self.wait(1)

        tex1 = Text("8.27").next_to(tex, RIGHT, buff=2.9).scale(2).shift(RIGHT*2)
        self.play(ShowCreation(tex1))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(Group(cat, peacock, bat, cat)).set_color("#00ff00").scale(0.97).shift(DOWN*0.15+LEFT*0.1)))
        self.wait(1)

        tex2 = Text("7.34").next_to(tex1, RIGHT, buff=2.9).scale(2).shift(RIGHT*2.23)
        self.play(ShowCreation(tex2))
        self.wait(2)


        self.play(Transform(rect, SurroundingRectangle(tex).scale(1.23)), FadeOut(title_v2))
        self.wait(2)


        self.play(self.camera.frame.animate.shift(UP*1.1 + LEFT*6.6).scale(0.82),FadeOut(Group(cat, snake, chicken, butterfly, peacock, bat, eagle, penguin, ellipse3, feature_text3, no_label3, yes_label3, arrow3_left, arrow3_right, tex2, tex1, rect, tex, cat_b, bat_b, chicken_b, eagle_b, snake_b, penguin_b, peacock_b , butterfly_b, ellipse2, feature_text2, arrow2_left, arrow2_right, no_label2, yes_label2)))

        self.wait(2)

        rect = SurroundingRectangle(butterfly_a)
        self.play(ShowCreation(rect))
        self.wait(2)

        not_bird = Rectangle(color="#00ff00", fill_color="#00ff00", fill_opacity=0.35, height=1, width=4.4)
        not_bird_text = Text("0.0005", weight=BOLD).move_to(not_bird).scale(1.8).set_color(WHITE)
        not_bird = VGroup(not_bird, not_bird_text).move_to(butterfly_a).scale(0.58).shift(UP*0.5)
        self.play(FadeIn(not_bird), FadeOut(butterfly_a), FadeOut(rect))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*3.3))

        brace = Brace(Group(bat_a, penguin_a), RIGHT, buff=0.6)
        self.play(GrowFromCenter(brace))
        text = Text("8.3").next_to(brace, RIGHT, buff=1.3).scale(2)
        self.play(ShowCreation(text))
        self.wait(2)

        self.play(FadeOut(Group(brace, text)))

        temp_a = Text("LaysEggs = 6.94").next_to(brace , RIGHT, buff=0.9).scale(1.2).shift(LEFT*0.3)
        temp_b = Text("CanFly = 7.52").next_to(temp_a, DOWN, buff=0.45).scale(1.2)

        self.play(ShowCreation(Group(temp_a, temp_b)))
        
        rect = SurroundingRectangle(temp_a).scale(1.15)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Uncreate(rect), Uncreate(Group(temp_a, temp_b)))

        self.play(Group(cat_a, chicken_a, bat_a, peacock_a, eagle_a, eagle_a, snake_a, penguin_a).animate.shift(RIGHT*7))

        # Create ellipse with full opacity fill
        ellipse_right = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=PURPLE, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(arrow_right.get_center(), DOWN, buff=1.23).shift(RIGHT*2+UP*0.3)
        
        # Text inside ellipse
        feature_text_right = Text(
            "LaysEggs", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse_right.get_center()).set_color(BLACK).set_z_index(1)
        # Arrows with z_index = -1 (behind other elements)
        arrow_right_left = Arrow(
            start=ellipse_right.get_center(), 
            end=ellipse_right.get_center() + LEFT*2 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right_right = Arrow(
            start=ellipse_right.get_center(), 
            end=ellipse_right.get_center() + RIGHT*2 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label_left = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_right_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label_left = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse_right), Write(feature_text_right))
        self.wait(1)
        self.play(GrowArrow(arrow_right_right), GrowArrow(arrow_right_left))
        self.play(FadeIn(no_label_left), FadeIn(yes_label_left))
        
        self.play(
            cat_a.animate.next_to(arrow_right_left, DOWN).shift(LEFT*1.6+UP*0.4),
            bat_a.animate.next_to(arrow_right_left, DOWN),
            Group(peacock_a, eagle_a, snake_a, penguin_a).animate.next_to(arrow_right_right, DOWN).shift(RIGHT*0.8),
            chicken_a.animate.next_to(arrow_right_right, DOWN).shift(DOWN*1.15+RIGHT*2.5)
            ,self.camera.frame.animate.shift(DOWN*0.4)
        )

        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*2.6))

        self.play(
             Group(cat_a, bat_a).animate.shift(LEFT*3.5),
            Group(peacock_a, eagle_a, snake_a, penguin_a, chicken_a).animate.shift(RIGHT*4.7)
        )

        self.wait(1)

        # Create ellipse with full opacity fill
        ellipse_right_right = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=YELLOW, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(arrow_right_right.get_center(), DOWN, buff=1.23).shift(RIGHT*2.07+UP*0.3)
        
        # Text inside ellipse
        feature_text_right_right = Text(
            "CanFly", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse_right_right.get_center()).set_color(BLACK).set_z_index(1)
        # Arrows with z_index = -1 (behind other elements)
        arrow_right_right_left = Arrow(
            start=ellipse_right_right.get_center(), 
            end=ellipse_right_right.get_center() + LEFT*1.7 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right_right_right = Arrow(
            start=ellipse_right_right.get_center(), 
            end=ellipse_right_right.get_center() + RIGHT*1.7 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label_right_left = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_right_right_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label_right_right = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right_right_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(FadeIn(ellipse_right_right), Write(feature_text_right_right))
        self.wait(1)
        self.play(GrowArrow(arrow_right_right_right), GrowArrow(arrow_right_right_left))
        self.play(FadeIn(no_label_right_left), FadeIn(yes_label_right_right))
        self.wait(0.12)

        self.play(
            snake_a.animate.next_to(arrow_right_right_left, DOWN).shift(LEFT*1.39)
            ,penguin_a.animate.next_to(arrow_right_right_left, DOWN).shift(UP*0.45).shift(LEFT*0),
            peacock_a.animate.next_to(arrow_right_right_right, DOWN).shift(RIGHT*0.6),
            eagle_a.animate.next_to(arrow_right_right_right, DOWN).shift(RIGHT*1.2).shift(RIGHT*0.6),
            chicken_a.animate.next_to(arrow_right_right_left, DOWN).shift(LEFT*1.39).shift(DOWN*1.18+RIGHT*0.5)
            
                                 ) 

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*1.1+DOWN*0.99))       

        # Create ellipse with full opacity fill
        ellipse_right_left = Ellipse(
            width=4, 
            height=1.5, 
            fill_color=YELLOW, 
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=2
        ).next_to(arrow_right_left.get_center(), DOWN, buff=1.23).shift(LEFT*2.07+UP*0.3)
        
        # Text inside ellipse
        feature_text_right_left = Text(
            "CanFly", 
            font_size=62, 
            weight=BOLD, 
        ).move_to(ellipse_right_left.get_center()).set_color(BLACK).set_z_index(1)
        # Arrows with z_index = -1 (behind other elements)
        arrow_right_left_left = Arrow(
            start=ellipse_right_left.get_center(), 
            end=ellipse_right_left.get_center() + LEFT*1.7 + DOWN*2.3, 
            color=RED, 
            fill_color=RED,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        arrow_right_left_right = Arrow(
            start=ellipse_right_left.get_center(), 
            end=ellipse_right_left.get_center() + RIGHT*1.7 + DOWN*2.3, 
            color=GREEN, 
            fill_color=GREEN,
            fill_opacity=1,
            stroke_width=6
        ).set_z_index(-1)
        
        # Labels for the arrows
        no_label_right_left = Text("No", color=RED, font_size=50, weight=BOLD).next_to(arrow_right_left_left.get_center(), LEFT).shift(LEFT*0.19)
        yes_label_right_right = Text("Yes", color=GREEN, font_size=50, weight=BOLD).next_to(arrow_right_left_right.get_center(), RIGHT).shift(RIGHT*0.19)
        
        # Animate the decision tree elements
        self.play(Group(cat_a, bat_a).animate.shift(LEFT*1.8))
        self.play(FadeIn(ellipse_right_left), Write(feature_text_right_left))
        self.wait(1)
        self.play(GrowArrow(arrow_right_left_right), GrowArrow(arrow_right_left_left))
        self.play(FadeIn(no_label_right_left), FadeIn(yes_label_right_right))
        self.wait(0.12)

        self.play(
            cat_a.animate.next_to(arrow_right_left_left, DOWN).shift(DOWN).shift(UP*1.5+LEFT*1.1),
            bat_a.animate.next_to(arrow_right_left_right, DOWN).shift(DOWN).shift(UP*1+RIGHT*0.75)

        )

        self.wait(2)

        rect = SurroundingRectangle(cat_a)
        rect1 = SurroundingRectangle(bat_a)

        self.play(ShowCreation(rect), ShowCreation(rect1))
        self.wait(1.8)

        not_bird1 = Rectangle(color="#00ff00", fill_color="#00ff00", fill_opacity=0.35, height=1, width=4.4)
        not_bird_text = Text("4.0", weight=BOLD).move_to(not_bird1).scale(1.8).set_color(WHITE)
        a = VGroup(not_bird1, not_bird_text).move_to(cat_a).scale(0.58).shift(UP*0.1)
        not_bird1 = Rectangle(color="#00ff00", fill_color="#00ff00", fill_opacity=0.35, height=1, width=4.4)
        not_bird_text = Text("0.03", weight=BOLD).move_to(not_bird1).scale(1.8).set_color(WHITE)
        b = VGroup(not_bird1, not_bird_text).move_to(bat_a).scale(0.58).shift(UP*0.19)
      
        self.play(FadeIn(a), FadeOut(cat_a), FadeOut(rect), FadeIn(b), FadeOut(bat_a), FadeOut(rect1))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*2))

        rect = SurroundingRectangle(Group(snake_a, penguin_a, chicken_a)).scale(0.85)
        rect1 = SurroundingRectangle(Group(peacock_a, eagle_a))

        self.play(ShowCreation(rect), ShowCreation(rect1))
        self.wait(1.8)

        not_bird1 = Rectangle(color="#00ff00", fill_color="#00ff00", fill_opacity=0.35, height=1, width=4.4)
        not_bird_text = Text("4.83", weight=BOLD).move_to(not_bird1).scale(1.8).set_color(WHITE)
        a = VGroup(not_bird1, not_bird_text).move_to(Group(snake_a, chicken_a, penguin_a)).scale(0.58).shift(UP*0.89)
        not_bird1 = Rectangle(color="#00ff00", fill_color="#00ff00", fill_opacity=0.35, height=1, width=4.4)
        not_bird_text = Text("4.25", weight=BOLD).move_to(not_bird1).scale(1.8).set_color(WHITE)
        b = VGroup(not_bird1, not_bird_text).move_to(Group(peacock_a, eagle_a)).scale(0.58).shift(UP*0.19)
      
        self.play(FadeIn(a), FadeOut(Group(snake_a, penguin_a, chicken_a, peacock_a, eagle_a)), FadeOut(rect), FadeIn(b), FadeOut(rect1))
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.3).shift(UP*2.66+LEFT*1.74))

        self.wait(2)

        a = Text("?", weight=BOLD).next_to(ellipse, RIGHT, buff=1.5).scale(3).set_color("#ff0000")
        self.play(ShowCreation(a))
        self.wait(2)

        self.play(a.animate.next_to(ellipse_right, RIGHT, buff=1.5))
        self.wait()
        self.play(a.animate.next_to(ellipse_right_right, RIGHT, buff=1.5))
        self.wait()
        self.play(a.animate.next_to(b, DOWN, buff=0.5))

        self.wait(2)
