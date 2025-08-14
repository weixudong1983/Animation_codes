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



    
