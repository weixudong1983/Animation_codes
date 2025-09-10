PURE_RED = "#FF0000"
from manimlib import *
import numpy as np
from scipy.spatial import ConvexHull


class PCA(Scene):
    def construct(self):

        self.camera.frame.scale(1.2).shift(UP*0.07)

        # ---------------------------------------------------------------- #
        # 1. Dataset
        # ---------------------------------------------------------------- #
        data_points = [
            [0.8, 1.8],
            [1.68, 2.0],
            [2.6, 1.9],
            [3.46, 2.2],
            [4.25, 2.1],
            [5.0, 1.8],
            [5.8, 2.0],
            [6.4, 1.9]
        ]

        # Build table data structure with headers
        # Note: Headers for X1 and X2 will be Tex
        data = [["Sample", "x_1", "x_2"]]
        for i, point in enumerate(data_points, start=1):
            data.append([str(i), str(point[0]), str(point[1])])

        # ------------------------------------------------------------- #
        # 2. Colors for columns
        # ------------------------------------------------------------- #
        column_colors = [BLUE, ORANGE, PURPLE]

        # ------------------------------------------------------------- #
        # 3. Build text objects
        # ------------------------------------------------------------- #
        text_rows = []
        for r, row in enumerate(data):
            current_row = []
            for c, cell in enumerate(row):
                # First row special handling
                if r == 0:
                    # First column header is Text
                    if c == 0:
                        current_row.append(Text(cell, font_size=52, weight=BOLD).set_color(BLACK))
                    # Second & Third column headers are Tex (math notation)
                    else:
                        current_row.append(Tex(cell, font_size=82, stroke_width=1).set_color(BLACK))
                else:
                    # All non-header rows use Text
                    current_row.append(Text(cell, font_size=54, weight=BOLD).set_color(BLACK))
            text_rows.append(current_row)

        n_rows, n_cols = len(text_rows), len(text_rows[0])

        # ------------------------------------------------------------- #
        # 4. Calculate cell sizes
        # ------------------------------------------------------------- #
        col_w = [max(text_rows[r][c].get_width() for r in range(n_rows)) + 0.8
                 for c in range(n_cols)]
        row_h = max(m.get_height() for row in text_rows for m in row) + 0.6
        tot_w, tot_h = sum(col_w), n_rows * row_h

        # ------------------------------------------------------------- #
        # 5. Build backgrounds and position text
        # ------------------------------------------------------------- #
        cell_bgs, cell_txts = VGroup(), VGroup()

        for r in range(n_rows):
            for c in range(n_cols):
                # Position of each cell
                x = -tot_w/2 + sum(col_w[:c]) + col_w[c]/2
                y = tot_h/2 - (r + 0.5)*row_h

                txt = text_rows[r][c].move_to([x, y, 0])

                # Background rectangle for each cell
                bg = Rectangle(width=col_w[c], height=row_h, stroke_width=2).move_to([x, y, 0]).set_color(BLACK)

                # Coloring rules
                if r == 0:  # Header row
                    bg.set_fill(YELLOW, opacity=0.66)
                else:
                    bg.set_fill(column_colors[c], opacity=0.3)

                cell_bgs.add(bg)
                cell_txts.add(txt)

        # ------------------------------------------------------------- #
        # 6. Grid lines
        # ------------------------------------------------------------- #
        grid = VGroup(Rectangle(width=tot_w, height=tot_h, stroke_width=2))
        # Vertical lines
        x_cur = -tot_w/2
        for w in col_w[:-1]:
            x_cur += w
            grid.add(Line([x_cur,  tot_h/2, 0], [x_cur, -tot_h/2, 0], stroke_width=1.5))
        # Horizontal lines
        y_cur = tot_h/2
        for _ in range(n_rows-1):
            y_cur -= row_h
            grid.add(Line([-tot_w/2, y_cur, 0], [tot_w/2, y_cur, 0], stroke_width=1.5))

        # ------------------------------------------------------------- #
        # 7. Assemble table and animate
        # ------------------------------------------------------------- #
        table = VGroup(cell_bgs, grid, cell_txts).scale(0.8).center()
        title = Text("Example Dataset", font_size=64, weight=BOLD).next_to(table, UP, buff=0.44).set_color(BLACK)

        self.play(ShowCreation(grid), run_time=1)
        self.play(FadeIn(cell_bgs), run_time=1.2)
        self.play(LaggedStartMap(FadeIn, cell_txts, shift=0.1*UP, lag_ratio=0.06), run_time=2)
        self.wait(2)


        # Helper function to get a full column group
        def get_column_group(col_index):
            return VGroup(*[
                cell_bgs[i] if i < len(cell_bgs) else cell_txts[i]  # just a safeguard
                for i in range(col_index, n_rows * n_cols, n_cols)
            ])

        # Combine both text and background for a full column
        last_column_group = VGroup(*[
            cell_bgs[i] for i in range(2, n_rows * n_cols, n_cols)
        ], *[
            cell_txts[i] for i in range(2, n_rows * n_cols, n_cols)
        ])

        middle_column_group = VGroup(*[
            cell_bgs[i] for i in range(1, n_rows * n_cols, n_cols)
        ], *[
            cell_txts[i] for i in range(1, n_rows * n_cols, n_cols)
        ])

        # Create a surrounding rectangle for the last column (X2)
        highlight_rect = SurroundingRectangle(
            last_column_group,
            color=PURE_RED,
            fill_color=PURE_RED,
            fill_opacity=0.25,
            buff=0.08  # Small padding for a clean look
        )

        # Step 1: Highlight the last column
        self.play(FadeIn(highlight_rect), run_time=1)

        self.wait(2)

        # Step 2: Move smoothly to the middle column (X1)
        new_highlight_rect = SurroundingRectangle(
            middle_column_group,
            color=PURE_RED,
            fill_color=PURE_RED,
            fill_opacity=0.23,
            buff=0.08
        )
        self.play(Transform(highlight_rect, new_highlight_rect), run_time=1.2)
        self.wait(2)


        # Create custom axes without ticks, in first quadrant
        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 4, 1],
            axis_config={
                "stroke_width": 7,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            }
        ).set_color(GREY_E).shift(RIGHT*14)
        
        # Create axis labels (at the end of axes)
        x_label = Tex("x_1").next_to(axes.x_axis.get_end(), RIGHT, buff=0.2).set_color(BLACK)
        y_label = Tex("x_2").next_to(axes.y_axis.get_end(), UP, buff=0.2).set_color(BLACK)
        
        # Create 8 data points with high variance in x1 and low variance in x2 (in first quadrant)
        data_points = [
            [0.8, 1.8],
            [1.68, 2.0],
            [2.6, 1.9],
            [3.46, 2.2],
            [4.25, 2.1],
            [5.0, 1.8],
            [5.8, 2.0],
            [6.4, 1.9]
        ]
        
        # Create blue dots for data points (bigger and using set_color)
        dots = VGroup()
        for x, y in data_points:
            dot = Dot(axes.c2p(x, y), radius=0.123)
            dot.set_color(BLUE_D)
            dots.add(dot).set_z_index(1)
        
        # Create green dotted lines to x-axis and projection dots
        x_projection_lines = VGroup()
        x_projection_dots = VGroup()
        for x, y in data_points:
            line = DashedLine(
                axes.c2p(x, y),
                axes.c2p(x, 0),
                dash_length=0.1,
                stroke_width=4
            )
            line.set_color(GREEN)  
            line.set_z_index(-1)
            x_projection_lines.add(line).set_z_index(-1)
            
            # Small green dot at projection point
            proj_dot = Dot(axes.c2p(x, 0), radius=0.12)
            proj_dot.set_color(GREEN)  # Pure green
            x_projection_dots.add(proj_dot)
        
        # Create red dotted lines to y-axis and projection dots
        y_projection_lines = VGroup()
        y_projection_dots = VGroup()
        for x, y in data_points:
            line = DashedLine(
                axes.c2p(x, y),
                axes.c2p(0, y),
                dash_length=0.1,
                stroke_width=4
            )
            line.set_color(RED) 
            y_projection_lines.add(line).set_z_index(-1)
            
            # Small red dot at projection point
            proj_dot = Dot(axes.c2p(0, y), radius=0.12)
            proj_dot.set_color(RED)  # Pure red
            y_projection_dots.add(proj_dot)

        

        # Step 3: Fade out at the end
        self.play(FadeOut(highlight_rect), 
                  self.camera.frame.animate.shift(RIGHT*14).scale(0.65),
                              ShowCreation(axes.x_axis),
            ShowCreation(axes.y_axis),run_time=1.8)
        

        
        self.play(
            Write(x_label),
            Write(y_label),
            run_time=1
        )

        
        self.wait(1.5)
        
        # Show data points
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.2),
            run_time=2
        )
        
        self.wait(1)
        
        # Show projections to x-axis with small green dots
        self.play(
            LaggedStart(*[ShowCreation(line) for line in x_projection_lines], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(dot) for dot in x_projection_dots], lag_ratio=0.2),
            run_time=2
        )
        
        self.wait(1)
        
        # Show projections to y-axis with small red dots
        self.play(
            LaggedStart(*[ShowCreation(line) for line in y_projection_lines], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(dot) for dot in y_projection_dots], lag_ratio=0.2),
            run_time=2
        )

        
        self.wait(2)
        
        # ------------------ NEW ADDITIONS ------------------

        # Uncreate the projection lines, keep only the dots
        self.play(
            Uncreate(x_projection_lines),
            Uncreate(y_projection_lines),
            run_time=2
        )

        self.wait(1)

        # Create horizontal brace for x-axis projections (High Variance)
        x_proj_points = [axes.c2p(x, 0) for x, _ in data_points]
        leftmost_x = min(x_proj_points, key=lambda p: p[0])
        rightmost_x = max(x_proj_points, key=lambda p: p[0])

        x_brace = Brace(
            Line(leftmost_x, rightmost_x),
            direction=DOWN,
            color=GREEN
        ).set_color(GREEN)
        x_brace_label = Text("High Variance").next_to(x_brace, DOWN).set_color(GREEN)

        # Create vertical brace for y-axis projections (Low Variance)
        y_proj_points = [axes.c2p(0, y) for _, y in data_points]
        bottom_y = min(y_proj_points, key=lambda p: p[1])
        top_y = max(y_proj_points, key=lambda p: p[1])

        y_brace = Brace(
            Line(bottom_y, top_y),
            direction=LEFT,
            color=RED
        ).set_color(RED)
        y_brace_label = Text("Low Variance", color=RED).rotate(PI/2).next_to(y_brace, LEFT).set_color(RED)
        
        self.play(self.camera.frame.animate.shift(DOWN*0.29))

        # Animate braces and labels
        self.play(
            GrowFromCenter(x_brace),
            Write(x_brace_label),
            GrowFromCenter(y_brace),
            Write(y_brace_label),
            run_time=1.5
        )

        self.wait(2)

        self.play(FadeOut(VGroup(x_brace, x_brace_label, y_brace, y_brace_label,y_projection_dots, dots,  )))
        self.play(FadeOut(VGroup(axes.get_y_axis(), y_label)))

        self.play(self.camera.frame.animate.scale(0.82).shift(DOWN*1.6+RIGHT*0.3))
        self.wait(2)


        self.play(self.camera.frame.animate.shift(LEFT*14).scale(1.2*1.5).shift(UP*1.87), run_time=1.77)

        self.wait(2)


        # New data points
        new_data_points = [
            [0.8, 0.9],
            [1.4, 1.58],
            [2.1, 2.2],
            [2.9, 1.7],
            [3.5, 2.75],
            [4.2, 2.25],
            [5, 3.28],
            [5.8, 2.67]
        ]
        
        # Build new text rows for the new dataset
        new_text_rows = [["Sample", "x_1", "x_2"]]
        for i, point in enumerate(new_data_points, start=1):
            new_text_rows.append([str(i), str(point[0]), str(point[1])])
        
        # Create new Text objects for all cells
        new_cell_txts = VGroup()
        for r, row in enumerate(new_text_rows):
            for c, cell in enumerate(row):
                if r == 0:  # header row
                    if c == 0:
                        txt = Text(cell, font_size=52, weight=BOLD).set_color(BLACK)
                    else:
                        txt = Tex(cell, font_size=82, stroke_width=1).set_color(BLACK)
                else:
                    txt = Text(cell, font_size=54, weight=BOLD).set_color(BLACK)
                # scale down slightly
                txt.scale(0.88)
                # move to original cell position
                txt.move_to(text_rows[r][c].get_center())
                new_cell_txts.add(txt)
        
        # Transform old cell texts to new ones at once
        self.play(Transform(cell_txts, new_cell_txts),  run_time=1)

        self.play(FadeOut(VGroup(x_brace, x_brace_label, y_brace, y_brace_label,x_projection_dots, dots,  )))
        self.play(FadeOut(VGroup(axes.get_x_axis(), x_label)))




        #######################################################################
       

        # Create axes with extended range
        axes1 = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 4, 1],
            axis_config={
                "stroke_width": 7,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            }
        ).set_color(GREY_E).shift(RIGHT*14)
        
        # Create axis labels
        x1_label = Tex("x_1").next_to(axes1.x_axis.get_end(), RIGHT, buff=0.2).set_color(BLACK)
        y1_label = Tex("x_2").next_to(axes1.y_axis.get_end(), UP, buff=0.2).set_color(BLACK)

        # Create 8 data points with linear relationship and slight noise
        data_points = [
            [0.8, 0.9],
            [1.4, 1.58],
            [2.1, 2.2],
            [2.9, 1.7],
            [3.5, 2.75],
            [4.2, 2.25],
            [5, 3.28],
            [5.8, 2.67]
        ]
        
        # Create blue dots for data points
        dots1 = VGroup()
        for x, y in data_points:
            dot = Dot(axes1.c2p(x, y), radius=0.123)
            dot.set_color(BLUE_E)
            dots1.add(dot).set_z_index(1)
        
        # Create green dotted lines to x-axis and projection dots
        x_projection_lines = VGroup()
        x_projection_dots = VGroup()
        for x, y in data_points:
            line = DashedLine(
                axes1.c2p(x, y),
                axes1.c2p(x, 0),
                dash_length=0.1,
                stroke_width=4
            )
            line.set_color(GREEN)  
            line.set_z_index(-1)
            x_projection_lines.add(line).set_z_index(-1)
            
            # Small green dot at projection point
            proj_dot = Dot(axes1.c2p(x, 0), radius=0.12)
            proj_dot.set_color(GREEN)
            x_projection_dots.add(proj_dot)
        
        # Create red dotted lines to y-axis and projection dots
        y_projection_lines = VGroup()
        y_projection_dots = VGroup()
        for x, y in data_points:
            line = DashedLine(
                axes1.c2p(x, y),
                axes1.c2p(0, y),
                dash_length=0.1,
                stroke_width=4
            )
            line.set_color(RED) 
            y_projection_lines.add(line).set_z_index(-1)
            
            # Small red dot at projection point
            proj_dot = Dot(axes.c2p(0, y), radius=0.12)
            proj_dot.set_color(RED)
            y_projection_dots.add(proj_dot)
        
        # Animation sequence
        self.play(
            self.camera.frame.animate.shift(RIGHT*13.6).scale(0.65),
            ShowCreation(axes1.x_axis),
            ShowCreation(axes1.y_axis),
            run_time=1.5
        )

        
        self.play(
            Write(x1_label),
            Write(y1_label),
            run_time=1
        )

        self.wait(0.5)
        
        # Show data points
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in dots1], lag_ratio=0.2),
            run_time=2
        )
        
        self.wait(1)
        
        # Show projections to x-axis with small green dots
        self.play(
            LaggedStart(*[ShowCreation(line) for line in x_projection_lines], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(dot) for dot in x_projection_dots], lag_ratio=0.2),
            run_time=2
        )
        
        
        # Show projections to y-axis with small red dots
        self.play(
            LaggedStart(*[ShowCreation(line) for line in y_projection_lines], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(dot) for dot in y_projection_dots], lag_ratio=0.2),
            run_time=2
        )

        self.wait(0.4)

        self.play(
            *[Uncreate(i) for i in x_projection_lines],
            *[Uncreate(i) for i in y_projection_lines],
            run_time=1.2
                  )
        
        # ------------------ BRACES ------------------
        
        # Create horizontal brace for x-axis projections
        x_proj_points = [axes1.c2p(x, 0) for x, _ in data_points]
        leftmost_x = min(x_proj_points, key=lambda p: p[0])
        rightmost_x = max(x_proj_points, key=lambda p: p[0])

        x_brace = Brace(
            Line(leftmost_x, rightmost_x),
            direction=DOWN,
            color=GREEN
        ).set_color(GREEN).shift(DOWN*0.23)

        # Create vertical brace for y-axis projections
        y_proj_points = [axes1.c2p(0, y) for _, y in data_points]
        bottom_y = min(y_proj_points, key=lambda p: p[1])
        top_y = max(y_proj_points, key=lambda p: p[1])

        y_brace = Brace(
            Line(bottom_y, top_y),
            direction=LEFT,
            color=RED
        ).set_color(RED).shift(LEFT*0.23)
        
        # Animate braces
        self.play(
            GrowFromCenter(x_brace),
            GrowFromCenter(y_brace),
            run_time=1.5
        )

        self.wait(2)


        cov_tex = Tex(r"\mathrm{Cov}(X, Y) = \frac{1}{n} \sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})",font_size=48).set_color(BLACK).shift(UP*0.9)

        self.play(FadeOut(VGroup(x_brace, y_brace,y_projection_dots, x_projection_dots, grid, cell_bgs, cell_txts, title)),
                  self.camera.frame.animate.shift(LEFT*14),
                  Write(cov_tex)
                  )
        
        self.wait(2)
        
        mean_tex = Tex(r"\bar{X} = \frac{1}{n} \sum_{i=1}^{n} X_i \quad,\quad "r"\bar{Y} = \frac{1}{n} \sum_{i=1}^{n} Y_i",font_size=42)

        mean_tex.next_to(cov_tex, DOWN, buff=0.64).set_color(BLACK)

        self.play(Write(mean_tex), run_time=1)


        self.wait(2)


        expanded_corr_tex = Tex(r"\rho_{XY} = \frac{\frac{1}{n} \sum_{i=1}^{n} (X_i - \bar{X})(Y_i - \bar{Y})}"r"{\sqrt{\frac{1}{n} \sum_{i=1}^{n} (X_i - \bar{X})^2} \sqrt{\frac{1}{n} \sum_{i=1}^{n} (Y_i - \bar{Y})^2}}",font_size=30).move_to(VGroup(cov_tex, mean_tex).get_center()).set_color(BLACK)
        
        expanded_corr_tex.scale(1.25*1.1)

        self.play(ReplacementTransform(VGroup(cov_tex, mean_tex), expanded_corr_tex),)
        self.wait(0.66)


        self.embed()

        brace = Brace(expanded_corr_tex[4:26], UP, buff=0.3).set_color(GREEN_E)
        text = Text("Cov(X, Y)", font_size=46, weight=BOLD).set_color(GREEN_E).next_to(brace, UP, buff=0.23)
        self.play(GrowFromCenter(brace), Write(text), run_time=1)
        self.wait(2)

        brace1 = Brace(expanded_corr_tex[27:34], DOWN, buff=0.3).set_color(BLUE_E)
        text1 = Text("S.D. Of X", font_size=46, weight=BOLD).set_color(BLUE_E).next_to(brace1, DOWN, buff=0.23)
        self.play(GrowFromCenter(brace1), Write(text1), run_time=1)

        brace2 = Brace(expanded_corr_tex[45:], DOWN, buff=0.3).set_color(RED_E)
        text2 = Text("S.D. Of Y", font_size=46, weight=BOLD).set_color(RED_E).next_to(brace2, DOWN, buff=0.23)
        self.play(GrowFromCenter(brace2), Write(text2), run_time=1)

        self.wait(2)

        cov_tex = Tex(r"\rho_{XY} = \frac{\mathrm{Cov}(X, Y)}{\sigma_X \sigma_Y}", font_size=56).set_color(BLACK).move_to(expanded_corr_tex.get_center()).scale(1.2)

        self.play(ReplacementTransform(VGroup(expanded_corr_tex, brace, text, brace1, text1, brace2, text2), cov_tex), run_time=1.13)
        self.wait(2)




        # Calculate correlation coefficient
        def calculate_correlation(x_data, y_data):
            n = len(x_data)
            mean_x = sum(x_data) / n
            mean_y = sum(y_data) / n
            
            numerator = sum((x_data[i] - mean_x) * (y_data[i] - mean_y) for i in range(n))
            sum_sq_x = sum((x_data[i] - mean_x) ** 2 for i in range(n))
            sum_sq_y = sum((y_data[i] - mean_y) ** 2 for i in range(n))
            
            if sum_sq_x == 0 or sum_sq_y == 0:
                return 0
            
            correlation = numerator / (sum_sq_x ** 0.5 * sum_sq_y ** 0.5)
            return round(correlation, 3)

        # Data for three scenarios
        # 1. Near zero correlation (original data)
        data1 = [
            [0.8, 1.8],
            [1.68, 2.0],
            [2.6, 1.9],
            [3.46, 2.2],
            [4.25, 2.1],
            [5.0, 1.8],
            [5.8, 2.0],
            [6.4, 1.9]
        ]
        x1_data, y1_data = zip(*data1)
        corr1 = calculate_correlation(x1_data, y1_data)

        # 2. Positive correlation (second data)
        data2 = [
            [0.8, 0.9],
            [1.4, 1.58],
            [2.1, 2.2],
            [2.9, 1.7],
            [3.5, 2.75],
            [4.2, 2.25],
            [5, 3.28],
            [5.8, 2.67]
        ]
        x2_data, y2_data = zip(*data2)
        corr2 = calculate_correlation(x2_data, y2_data)

        # 3. Negative correlation (custom data)
        data3 = [
            [1.0, 3.2],
            [1.8, 2.8],
            [2.5, 2.5],
            [3.2, 2.1],
            [4.0, 1.8],
            [4.7, 1.5],
            [5.3, 1.2],
            [6.0, 0.9]
        ]
        x3_data, y3_data = zip(*data3)
        corr3 = calculate_correlation(x3_data, y3_data)

        # Create three axes
        axes_group = VGroup()
        dots_group = VGroup()
        labels_group = VGroup()
        corr_labels_group = VGroup()
        titles = VGroup()

        # Position for three graphs
        positions = [LEFT*4.5, ORIGIN, RIGHT*4.5]
        datasets = [data1, data2, data3]
        correlations = [corr1, corr2, corr3]
        titles = ["Near Zero Correlation", "Positive Correlation", "Negative Correlation"]

        for i, (pos, data, corr, title) in enumerate(zip(positions, datasets, correlations, titles)):
            # Create axes
            axes = Axes(
                x_range=[0, 7, 1],
                y_range=[0, 4, 1],
                axis_config={
                    "stroke_width": 2.6,
                    "include_tip": True,
                    "include_ticks": False,
                    "numbers_to_exclude": [0],
                }
            ).set_color(GREY_E).scale(0.5).move_to(pos + DOWN*2.6)
            
            # Create axis labels
            x_label = Tex("x_1").next_to(axes.x_axis.get_end(), RIGHT, buff=0.1).set_color(BLACK).scale(0.7)
            y_label = Tex("x_2").next_to(axes.y_axis.get_end(), UP, buff=0.1).set_color(BLACK).scale(0.7)
            
            # Create dots
            dots = VGroup()
            for x, y in data:
                dot = Dot(axes.c2p(x, y), radius=0.08)
                dot.set_color(BLUE_E)
                dots.add(dot)
            
            # Create correlation label

            corr_label = Tex(r"\rho_{x_1, x_2} = \ ",  f" {corr:.2f}",          font_size=48).set_color(BLACK)

            corr_label.next_to(axes, UP, buff=0.87)
            
            # Create title
            title_text = Text(title, font_size=33).set_color(BLACK)
            title_text.next_to(axes, DOWN, buff=0.66)
            
            axes_group.add(axes)
            dots_group.add(dots)
            labels_group.add(x_label, y_label, title_text)
            corr_labels_group.add(corr_label)
         
        # Position the formula at the top
        self.play(
            FadeOut(cov_tex),
            self.camera.frame.animate.shift(DOWN*1.26).scale(1.36).shift(DOWN),
            LaggedStart(*[ShowCreation(axes) for axes in axes_group], lag_ratio=0.3),
            LaggedStart(*[Write(label) for label in labels_group], lag_ratio=0.3),
            run_time=2
        )

        
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dots in dots_group for dot in dots], lag_ratio=0.1),
            run_time=2
        )
        
        self.play(
            LaggedStart(*[Write(label) for label in corr_labels_group], lag_ratio=0.3),
            run_time=1.5
        )

        self.wait(3)


        rect = SurroundingRectangle(VGroup(axes_group[0], dots_group[0], labels_group[0:3], corr_labels_group[0]), color=PURE_RED, fill_color=PURE_RED, fill_opacity=0.18, buff=0.3)
        self.play(ShowCreation(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(VGroup(axes_group[1], dots_group[1], labels_group[3:6], corr_labels_group[1]), color=PURE_RED, fill_color=PURE_RED, fill_opacity=0.18, buff=0.3)))
        
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(VGroup(axes_group[2], dots_group[2], labels_group[6:9], corr_labels_group[2]), color=PURE_RED, fill_color=PURE_RED, fill_opacity=0.18, buff=0.3)))
        self.wait(2)

        self.play(
            FadeOut(rect),
            FadeOut(VGroup(axes_group, dots_group, labels_group, corr_labels_group)),
            self.camera.frame.animate.shift(RIGHT*14+UP*2.43+RIGHT*0.33).scale(0.8*0.97*0.97) ,
            run_time=1.5
        )


        self.wait(2)

        self.camera.frame.save_state()




        # Calculate mean point
        mean_x = sum(x for x, y in data_points) / len(data_points)
        mean_y = sum(y for x, y in data_points) / len(data_points)
        mean_point = axes1.c2p(mean_x, mean_y)
        
        # Create mean point (blue dot with "X")
        PURE_BLUE = "#0000FF"
        mean_dot = Dot(mean_point, radius=0.19).set_color(PURE_BLUE)
        mean_text = Text("X", font_size=36, weight=BOLD).set_color(WHITE).move_to(mean_point)
        mean_group = VGroup(mean_dot, mean_text)



        self.wait(2)



    
        # Create PCA line (will rotate around mean)
        line_length = 3.03
        angle_tracker = ValueTracker(0)  # Track rotation angle
        pca_line = always_redraw(lambda: Line(
            mean_point + line_length * np.cos(angle_tracker.get_value()) * RIGHT + line_length * np.sin(angle_tracker.get_value()) * UP,
            mean_point - line_length * np.cos(angle_tracker.get_value()) * RIGHT - line_length * np.sin(angle_tracker.get_value()) * UP,
            stroke_width=7,
            color=PURE_RED
        ))
        
        # Create projection lines (purple) - these update dynamically
        projection_lines = always_redraw(lambda: VGroup(*[
            Line(
                axes1.c2p(x, y),
                # Project point onto line
                mean_point + np.dot(
                    np.array(axes1.c2p(x, y)) - mean_point,
                    np.array([np.cos(angle_tracker.get_value()), np.sin(angle_tracker.get_value()), 0])
                ) * np.array([np.cos(angle_tracker.get_value()), np.sin(angle_tracker.get_value()), 0]),
                stroke_width=4,
                color=PURPLE
            ) for x, y in data_points
        ]))
        
        # Variance calculation function
        def calculate_projected_variance():
            angle = angle_tracker.get_value()
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            projections = []
            
            for x, y in data_points:
                point = np.array(axes1.c2p(x, y))
                projection_scalar = np.dot(point - mean_point, direction)
                projections.append(projection_scalar)
            
            variance = np.var(projections)
            return variance
        
        
        # Get projection points for brace
        def get_projection_points():
            angle = angle_tracker.get_value()
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            projections = []
            
            for x, y in data_points:
                point = np.array(axes1.c2p(x, y))
                projection_scalar = np.dot(point - mean_point, direction)
                projection_point = mean_point + projection_scalar * direction
                projections.append(projection_point)
            
            return projections
        
        # Brace for measuring variance - updates dynamically
        variance_brace = always_redraw(lambda: Brace(
            Line(
                min(get_projection_points(), key=lambda p: np.dot(p - mean_point, np.array([np.cos(angle_tracker.get_value()), np.sin(angle_tracker.get_value()), 0]))),
                max(get_projection_points(), key=lambda p: np.dot(p - mean_point, np.array([np.cos(angle_tracker.get_value()), np.sin(angle_tracker.get_value()), 0])))
            ),
            direction=np.array([-np.sin(angle_tracker.get_value()), np.cos(angle_tracker.get_value()), 0]),
            buff=0.6  # Much larger buff to keep brace well away from dots and line
        ).set_color(GREEN_E))
        


        self.play(GrowFromCenter(pca_line))
        
        self.play(
            ShowCreation(projection_lines),
            GrowFromCenter(variance_brace),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Move line clockwise and counterclockwise with smooth animations to find maximum variance
        angles_to_try = [0, PI/8,  PI/4, 0, -PI/8, -PI/6, PI/8, PI/6, PI/4]
        max_variance = 0
        best_angle = 0
        
        for angle in angles_to_try:
            self.play(angle_tracker.animate.set_value(angle), run_time=1.5)
            current_variance = calculate_projected_variance()
            if current_variance > max_variance:
                max_variance = current_variance
                best_angle = angle
        
        # Set to optimal angle with smooth animation
        self.play(angle_tracker.animate.set_value(best_angle), run_time=1.7)
        self.wait(2)
        
        # Remove projection lines, variance text, and brace with smooth animations
        self.play(
            FadeOut(projection_lines),
            FadeOut(variance_brace),
            run_time=1
        )
        self.wait(2)

        arrow = Arrow(mean_group , mean_group.get_left()+UP+RIGHT*1.23, stroke_width=6).set_color(BLACK)
        arrow.shift(RIGHT*3).rotate(PI/2.55).shift(LEFT*0.56)
        self.play(GrowArrow(arrow))

        # Calculate direction vector: from start to end, then point 'downward' relative to arrow
        direction_vec = arrow.get_unit_vector()  # points from start to end
        
        # Want "below" the arrow, so take negative direction_vec
        pc1 = Tex(r"\mathbf{PC}_1", font_size=38).set_color(BLACK)
        pc1.next_to(arrow.get_end(), -direction_vec, buff=0.98).shift(LEFT*0.33)  # positions PC₁ "below" the arrow tip
        
        self.play(Write(pc1))

        self.wait(2)


        self.play(FadeOut(arrow), run_time=0.7)
        

        # Animate moving PC₁ label to the right of the PCA line (relative, not absolute right)
        self.play(pc1.animate.next_to(pca_line.get_right(), RIGHT, buff=0.27).shift(UP*1.3).rotate(PI/9))

        self.wait(2)


        PURE_BLUE = "#0000FF"
        shorter_length = 2.3  # shorter length than original 3.03
        
        pca_line2 = Line(
            mean_point + shorter_length * np.cos(angle_tracker.get_value() + PI/2) * RIGHT + shorter_length * np.sin(angle_tracker.get_value() + PI/2) * UP,
            mean_point - shorter_length * np.cos(angle_tracker.get_value() + PI/2) * RIGHT - shorter_length * np.sin(angle_tracker.get_value() + PI/2) * UP,
            stroke_width=7,
            color=PURE_BLUE
        )


        self.play(ShowCreation(pca_line2), run_time=1.3)

        pc2 = Tex(r"\mathbf{PC}_2", font_size=38).set_color(BLACK)
        pc2.next_to(pca_line2.get_top(), UP, buff=0.08).shift(LEFT).rotate(PI/15).rotate(PI/20)
        self.play(ShowCreation(pc2))

        self.wait(2)

        temp = Tex(r"\mathbf{PC}_1 \ = \ ax_1 + bx_2" ,).next_to(arrow, RIGHT, buff=1.3).set_color(BLACK)
        temp1 = Tex(r"\mathbf{PC}_2 \ = \ cx_1 + dx_2" ,).next_to(temp, DOWN).set_color(BLACK)

        self.play(ShowCreation(temp), ShowCreation(temp1), self.camera.frame.animate.shift(RIGHT*3.8))
        self.wait(2)
        self.play(Uncreate(temp), Uncreate(temp1), self.camera.frame.animate.shift(LEFT*3.8))
        self.wait(2)

        self.camera.frame.save_state()
        self.camera.frame.restore()

        a = pca_line.copy().set_color(BLACK)
        
        self.play(self.camera.frame.animate.rotate(PI/7.85).shift(UP*0.3+LEFT*0.3).scale(0.9), FadeOut(VGroup(axes1, x1_label, y1_label)), pca_line2.animate.set_color(BLACK), FadeIn(a), FadeOut(pca_line))

        self.wait(2)


        

        # ----- helper: orthogonal projection of point P onto line L (in scene coords)
        def project_point_to_line(P, L):
            A = L.get_start()
            B = L.get_end()
            u = B - A
            t = np.dot(P - A, u) / np.dot(u, u)
            return A + t * u  # projected point Q
        


        pc1_line = a  # your black PC1 line
        pc1_proj_lines = VGroup()
        pc1_proj_dots  = VGroup()
        
        for d in dots1:  # reuse your data points VGroup
            P = d.get_center()
            Q = project_point_to_line(P, pc1_line)
        
            seg = Line(P, Q, stroke_width=4).set_color(GREEN_E)
            seg.set_z_index(-1)  # keep dashed lines below data dots
            pc1_proj_lines.add(seg)
        
            qdot = Dot(Q, radius=0.09).set_color(GREEN_E)
            pc1_proj_dots.add(qdot)
        
        self.play(
            LaggedStart(*[ShowCreation(l) for l in pc1_proj_lines], lag_ratio=0.15),
            LaggedStart(*[GrowFromCenter(dd) for dd in pc1_proj_dots], lag_ratio=0.15),
            run_time=1.8
        )
        self.wait(1.0)
        


        pc2_line = pca_line2  # your black PC2 line
        pc2_proj_lines = VGroup()
        pc2_proj_dots  = VGroup()
        
        for d in dots1:
            P = d.get_center()
            Q = project_point_to_line(P, pc2_line)
        
            seg = Line(P, Q, stroke_width=4).set_color(RED_E)
            seg.set_z_index(-1)
            pc2_proj_lines.add(seg)
        
            qdot = Dot(Q, radius=0.09).set_color(RED_E)
            pc2_proj_dots.add(qdot)
        
        self.play(
            LaggedStart(*[ShowCreation(l) for l in pc2_proj_lines], lag_ratio=0.15),
            LaggedStart(*[GrowFromCenter(dd) for dd in pc2_proj_dots], lag_ratio=0.15),
            run_time=1.8
        )
        self.wait(1.0)
        
        # Optional cleanup
        self.play(
            *[Uncreate(l) for l in pc2_proj_lines],
            *[FadeOut(dd) for dd in pc2_proj_dots],
            *[Uncreate(l) for l in pc1_proj_lines],
            *[FadeOut(dd) for dd in dots1],
            FadeOut(pc2),
            FadeOut(pc2_line),
            self.camera.frame.animate.scale(0.9*0.9).shift(RIGHT*0.06),
            run_time=1.0
        )

        self.wait(2)

        text = Text("For D dimentions -> D PCs", weight=BOLD).next_to(pc1_line, UP).set_color(BLACK).shift(DOWN*0.23)

        self.play(self.camera.frame.animate.rotate(-PI/7.85).shift(LEFT*0.2), ShowCreation(text), FadeOut(VGroup(pc1, a), ),
                  *[FadeOut(dd) for dd in pc1_proj_dots],)
        
        self.wait(2)

        text1 = Text("Pick Top k PCs", weight=BOLD).next_to(text, DOWN).shift(DOWN*0.4).set_color(BLACK).scale(0.9)
        self.play(ShowCreation(text1))
        text2 = Text("That Captures Most varience", weight=BOLD).set_color(BLACK).next_to(text1, DOWN, buff=0.44).scale(0.9)
        self.play(ShowCreation(text2))

        self.wait(2)





class PCA_MATH(Scene):
    def construct(self):

        self.camera.frame.scale(0.88)

        
        # 8 data points spread widely across quadrants with rough linear correlation (not perfect)
        data_points = [
               [0.5, 0.46],   # 1st quadrant - rotated lower left
               [1, -0.12],   # 1st quadrant - rotated lower right
               [4, 3],   # 1st quadrant - rotated lower right
               [2.69, 1.69],   # 1st quadrant - rotated upper right
               [3.14, 1.05]     ]

        
        # Create axes extending beyond all quadrants for wide spread
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={
                "stroke_width": 6,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            }
        ).set_color(GREY_D)
        
        # Scale factor for wider positioning
        scale_factor = 1.0  # Full scale for maximum spread
        
        # Scale all data points
        scaled_points = [[x * scale_factor, y * scale_factor] for x, y in data_points]
        
        # Create blue dots for data points
        dots = VGroup()
        for x, y in scaled_points:
            dot = Dot(axes.c2p(x, y), radius=0.12)
            dot.set_color(BLUE_D)
            dots.add(dot)
        
        # Calculate mean position precisely
        mean_x = sum(x for x, y in scaled_points) / len(scaled_points)
        mean_y = sum(y for x, y in scaled_points) / len(scaled_points)
        mean_point = axes.c2p(mean_x, mean_y)
        
        # Create mean point
        PURE_BLUE = "#0000FF"
        mean_dot = Dot(mean_point, radius=0.19).set_color(PURE_BLUE)
        mean_text = Text("X", font_size=36, weight=BOLD).set_color(WHITE).move_to(mean_point)
        mean_group = VGroup(mean_dot, mean_text)
        
        # Show axes first
        self.play(
            ShowCreation(axes.x_axis),
            ShowCreation(axes.y_axis),
            run_time=1.5
        )
        
        # Show data points spread widely
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.2),
            run_time=2.5
        )
        
        self.wait(1)
        
        # Show mean point
        self.play(GrowFromCenter(mean_group), run_time=1.2)
        
        self.wait(2)
        
        # Center the data precisely - move mean to exact center
        centered_dots = VGroup()
        for i, (x, y) in enumerate(scaled_points):
            # Subtract mean to center each point
            new_x = x - mean_x
            new_y = y - mean_y
            new_position = axes.c2p(new_x, new_y)
            new_dot = Dot(new_position, radius=0.12).set_color(BLUE_D)
            centered_dots.add(new_dot)
        
        # Mean goes to exact axes origin
        centered_mean = VGroup(
            Dot(axes.c2p(0, 0), radius=0.19).set_color(PURE_BLUE),
            Text("X", font_size=36, weight=BOLD).set_color(WHITE).move_to(axes.c2p(0, 0))
        )
        
        # Animate precise centering
        self.play(
            Transform(dots, centered_dots),
            Transform(mean_group, centered_mean),
            run_time=2.5
        )
        
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*3.2))

        mean = Tex(r"\bar{x} = \frac{1}{n} \sum_{i=1}^n x_i").next_to(axes, RIGHT, buff=1.5).set_color(BLACK).scale(1.23).shift(UP*0.3)
        center = Tex(r"x_i \;\leftarrow\; x_i - \bar{x}").next_to(mean, DOWN).set_color(BLACK).scale(1.23).shift(DOWN*0.3)

        self.play(ShowCreation(mean))
        self.wait()
        self.play(ShowCreation(center))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*3.2), FadeOut(VGroup(mean, center , mean_group)))
        self.wait(2)



        # Calculate which dot is the upper one in first quadrant (after centering)
        # From your centered data: [2.69, 1.69] is the upper-right point (index 2)
        upper_dot_index = 2
        
        # Keep only the upper-right dot, fade out others
        dots_to_remove = VGroup()
        for i, dot in enumerate(dots):
            if i != upper_dot_index:
                dots_to_remove.add(dot)
        
        self.play(FadeOut(dots_to_remove), run_time=1.5)
        
        # Get the remaining dot position (centered coordinates)
        remaining_x = 2.69 - mean_x
        remaining_y = 1.69 - mean_y
        remaining_dot = dots[upper_dot_index]
        
        self.wait(1)
        
        # Create unit vector in PURE_RED with smaller angle for clear separation
        PURE_RED = "#FF0000"
        unit_length = 1.8  # Slightly longer for better visibility
        unit_angle = PI/10  # Smaller angle (18 degrees) for clear separation
        
        # Unit vector components
        u_x = np.cos(unit_angle)
        u_y = np.sin(unit_angle)
        
        # Create unit vector arrow with stroke_width = 4
        unit_vector = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(u_x * unit_length, u_y * unit_length),
            buff=0,
            stroke_width=4
        ).set_color(PURE_RED)
        
        # Unit vector label
        u_label = Tex(r"\vec{u}", font_size=52).set_color(PURE_RED)
        u_label.next_to(unit_vector.get_end(), UR, buff=0.1)
        
        # Show unit vector
        self.play(
            GrowFromCenter(unit_vector),
            ShowCreation(u_label),
            run_time=2
        )
        
        self.wait(1)
        
        # Create purple vector for the data point with stroke_width = 4
        PURPLE = "#800080"
        data_vector = Arrow(
            start=axes.c2p(0, 0),
            end=remaining_dot.get_center(),
            buff=0,
            stroke_width=4
        ).set_color(PURPLE).set_z_index(1)
        
        # Data vector label
        x_label = Tex(r"\vec{x_i}", font_size=42).set_color(PURPLE)
        x_label.next_to(data_vector.get_end(), UL, buff=0.1)
        
        # Show data vector
        self.play(
            GrowFromCenter(data_vector),
            ShowCreation(x_label),
            run_time=2
        )
        
        self.wait(1)
        
        # Calculate projection length (dot product)
        dot_product = u_x * remaining_x + u_y * remaining_y
        
        # Projection point coordinates on the unit vector
        proj_x = dot_product * u_x
        proj_y = dot_product * u_y
        proj_point = axes.c2p(proj_x, proj_y)
        
        # Create a copy of the data vector to rotate
        rotating_vector = data_vector
        
        # Calculate angles for rotation
        data_angle = np.arctan2(remaining_y, remaining_x)
        rotation_angle = unit_angle - data_angle
        
        # Rotate the purple vector to align with unit vector
        self.play(
            rotating_vector.animate.rotate(
                rotation_angle,
                about_point=axes.c2p(0, 0)
            ).rotate(PI/50).shift(UP*0.06).set_color(GREEN_D),
            u_label.animate.shift(UP*0.23),
            run_time=1
        )
        
        self.wait(2)

        dot_proj = Tex(r"z_i = \vec{u} \cdot \vec{x}_i").next_to(rotating_vector, RIGHT).set_color(GREEN_E).shift(UP*0.5)
        
        self.play(ShowCreation(dot_proj))

        self.wait(2)

        self.play(Transform(dot_proj, Tex(r"z_i = u^\top x_i").set_color(GREEN_E).move_to(dot_proj)))

        self.wait(2)

        var = Tex(r"\mathrm{Var}(u) = \frac{1}{n} \sum_{i=1}^n (u^\top x_i)^2").next_to(axes, RIGHT).set_color(BLACK).scale(1.5).shift(RIGHT*1.9)
        var[-6:-2].set_color(GREEN_E)
 

        self.play(self.camera.frame.animate.shift(RIGHT*8.5), ShowCreation(var), FadeOut(VGroup(axes, dot_proj)))

        self.wait(2)

        brace = Brace(var[-6:-2], UP).set_color(BLUE_E).shift(UP*0.3)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        self.play(Transform(brace, Brace(var[7:], UP).set_color(BLUE_E).shift(UP*0.3) ))
        self.wait(2)

        self.play(
            FadeOut(brace),
            Transform(var, Tex(r"\mathrm{Var}(u) = \frac{1}{n} \sum_{i=1}^n u^\top x_i x_i^\top u").move_to(var).set_color(BLACK).scale(1.56)))
        self.wait(2)

        self.play(
            Transform(var, Tex(r"\mathrm{Var}(u) = u^\top \left[\frac{1}{n} \sum_{i=1}^n x_i x_i^\top \right] u").move_to(var).set_color(BLACK).scale(1.56)))
        
        self.wait(2)

        brace = Brace(var[9:-1], UP, ).set_color(BLUE_E).shift(UP*0.3)
        self.play(GrowFromCenter(brace), self.camera.frame.animate.shift(UP*0.6))
        tex = Tex(r"\mathrm{Cov}(x, x^\top)").next_to(brace, UP).scale(1.3).set_color(BLACK).shift(UP*0.1)
        self.play(ShowCreation(tex))

        self.wait(2)


        mat = Tex(r"C = \begin{bmatrix} \mathrm{Cov}(x_1, x_1) & \mathrm{Cov}(x_1, x_2) & \cdots & \mathrm{Cov}(x_1, x_d) \\[6pt] \mathrm{Cov}(x_2, x_1) & \mathrm{Cov}(x_2, x_2) & \cdots & \mathrm{Cov}(x_2, x_d) \\[6pt] \vdots & \vdots & \ddots & \vdots \\[6pt] \mathrm{Cov}(x_d, x_1) & \mathrm{Cov}(x_d, x_2) & \cdots & \mathrm{Cov}(x_d, x_d) \end{bmatrix}")
        mat.next_to(var, RIGHT).set_color(BLACK).shift(RIGHT*1.2).scale(0.8)


        self.play(ShowCreation(mat), self.camera.frame.animate.shift(RIGHT*11.5 + DOWN*0.6))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*11.5 + UP*0.6), FadeOut(mat))
        self.wait(2)

        self.play(
            Transform(var, Tex(r"\mathrm{Var}(u) = u^\top C u").move_to(var).set_color(BLACK).scale(1.8)),
            FadeOut(brace),
            FadeOut(tex),
            self.camera.frame.animate.shift(DOWN*1.2)
            )
        
        self.wait(2)

        self.play(
            Transform(var, Tex(r"Max \ f(u)=u^\top C u").move_to(var).set_color(BLACK).scale(1.8)),
            )  
        self.wait(2)
        self.play(var.animate.shift(UP*0.8))  

        constraint = Tex(r"s. t. \ u^\top u = 1").set_color(BLACK).next_to(var, DOWN).scale(2).shift(DOWN*0.6)
        self.play(ShowCreation(constraint))
        self.wait(2)

        rect11 = SurroundingRectangle(constraint, stroke_width=6, color=BLUE_E).scale(1.2)
        self.play(ShowCreation(rect11))
        self.wait(2)


        lagrangian = Tex(r"\mathcal{L}(u,\lambda) = u^\top C u - \lambda\big(u^\top u - 1\big)").next_to(VGroup(constraint, rect11), RIGHT).shift(RIGHT*2)
        
        lagrangian.shift(RIGHT*1.5+UP*0.48).set_color(BLACK).scale(1.44)


        self.play(self.camera.frame.animate.shift(RIGHT*10), ShowCreation(lagrangian))
        self.wait(2)

        brace = Brace(lagrangian[:6], DOWN, ).set_color(BLUE_E).shift(DOWN*0.17)
        self.play(GrowFromCenter(brace))


        temp = Text("Lagrangian").next_to(brace, DOWN, buff=0.47).set_color(BLUE_E)
        self.play(ShowCreation(temp))



        self.wait(2)


        self.play(Transform(brace, Brace(lagrangian[7:11], DOWN, ).set_color(BLUE_E).shift(DOWN*0.17) ),
                  )
        self.play(Transform(temp, Text("Cost Function").next_to(brace, DOWN, buff=0.47).set_color(BLUE_E)))
        self.wait(2)

        
        self.play(Transform(brace, Brace(lagrangian[13:], DOWN, ).set_color(BLUE_E).shift(DOWN*0.17) ))
        self.play(Transform(temp, Text("Constraint").next_to(brace, DOWN, buff=0.47).set_color(BLUE_E)))

        self.wait(2)

        self.play(Transform(brace, Brace(lagrangian[12], DOWN, ).set_color(BLUE_E).shift(DOWN*0.17) ))
        self.play(Transform(temp, Text("Lagrange Multiplier").next_to(brace, DOWN, buff=0.47).set_color(BLUE_E)))

        self.wait(2)



        self.play(FadeOut(brace),FadeOut(temp), Transform(lagrangian, Tex(r"\frac{\partial \mathcal{L}}{\partial u} = 2 C u - 2\lambda u = 0").move_to(lagrangian).set_color(BLACK).scale(1.65)))
        self.wait(2)

        self.play(Transform(lagrangian, Tex(r"\boxed{C u = \lambda u}").move_to(lagrangian).set_color(BLACK).scale(1.5)))

        self.play(lagrangian.animate.scale(1.7))

        self.wait(2)

        self.play(Transform(lagrangian, Tex(r"(C - \lambda I)\,u = 0").scale(1.7).set_color(BLACK).move_to(lagrangian)))
        self.wait(2)

        eigen = Tex(r"\det\big(C - \lambda I\big) = 0").set_color(BLACK).move_to(lagrangian).scale(1.7)
        self.play(ReplacementTransform(lagrangian, eigen))
        self.wait(2)

        self.play(eigen.animate.shift(UP*0.66))

        lambdas = Tex(r"\lambda_1, \lambda_2, \dots, \lambda_D").set_color(BLACK).next_to(eigen, DOWN, buff=0.84).scale(1.3)
        self.play(TransformFromCopy(eigen, lambdas))
        self.wait(2)

        self.play(Transform(eigen, Tex(r"(C - \lambda_i I)\,u = 0").scale(1.7).set_color(BLACK).move_to(eigen)))
        self.wait(2)

        self.play(lambdas.copy().animate.scale(0.00000000000000001).move_to(eigen))
        
        

        unit_vectors = Tex(r"u_1, u_2, \dots, u_D").set_color(BLACK).next_to(lambdas, DOWN, buff=0.84).scale(1.3)
        self.play(TransformFromCopy(eigen, unit_vectors))

        self.play(self.camera.frame.animate.scale(0.8).shift(DOWN), FadeOut(eigen))
        self.wait(2)

        rect = SurroundingRectangle(lambdas, color=GREEN_D, stroke_width=7).scale(1.2)
        self.play(ShowCreation(rect))
        text = Text("Varience").next_to(rect, UP).shift(UP*0.34).set_color(GREEN_D).scale(1.34)
        self.play(Write(text))
        self.wait(2)

        rect1 = SurroundingRectangle(unit_vectors, color=PURPLE_D, stroke_width=7).scale(1.2)
        self.play(ShowCreation(rect1))
        text1 = Text("Principle Components").next_to(rect1, DOWN).shift(DOWN*0.34).set_color(PURPLE_D).scale(1.04)
        self.play(Write(text1))
        self.wait(2) 



        final_proj = Tex(r"Z_D = X \, U_D").set_color(BLACK).scale(2).move_to(VGroup(lambdas, unit_vectors))   

        self.play(
            FadeOut(VGroup(lambdas, unit_vectors, rect, rect1, text, text1 )),
            FadeIn(final_proj)
            )
        
        rect = SurroundingRectangle(final_proj[:2], color=GREEN_E, stroke_width=9).scale(1.1)

        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(final_proj[3], color=GREEN_E, stroke_width=9).scale(1.1)))
        
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(final_proj[-2:], color=GREEN_E, stroke_width=9).scale(1.1)))
        
        self.wait(2)

        self.play(Uncreate(rect))

        self.wait(2)

        self.play(Transform(final_proj, Tex(r"Z_K = X \, U_K").set_color(BLACK).scale(2).move_to(final_proj)))
        
        self.play(final_proj.animate.shift(UP*0.8))

        temp = Text("K << D").set_color(BLACK).next_to(final_proj, DOWN, buff=0.667)
        temp.shift(DOWN*0.6).scale(2)
        self.play(ShowCreation(temp))
        self.wait(2)

        self.play(
            FadeOut(temp),
            Transform(final_proj, Tex(r"\hat{X} = Z_k \, U_k^T").set_color(BLACK).scale(2).move_to(final_proj).shift(DOWN*0.82))
                  )
        
        self.wait(2)

        self.play(
            Transform(final_proj, Tex(r"\hat{X} = Z_k \, U_k^T + \mathbf{1} \, \mu^T").set_color(BLACK).scale(1.6).move_to(final_proj))
                  )        
        
        self.wait(2)
        
        self.play(
            Transform(final_proj, Tex(r"\frac{\lambda_1 + \lambda_2 + \dots + \lambda_k}{\lambda_1 + \lambda_2 + \dots + \lambda_D} \ge \phi").set_color(BLACK).move_to(final_proj).scale(1.3))
                  )        
        
        self.wait(2)

        self.play(
            Transform(final_proj, Tex(r"\frac{\lambda_1 + \lambda_2 + \dots + \lambda_k}{\lambda_1 + \lambda_2 + \dots + \lambda_D} \ge 0.90").set_color(BLACK).move_to(final_proj).scale(1.3))
                  )    

        self.wait(2)

        self.play(
            Transform(final_proj, Tex(r"\frac{\lambda_1 + \lambda_2 + \dots + \lambda_k}{\lambda_1 + \lambda_2 + \dots + \lambda_D} \ge 0.95").set_color(BLACK).move_to(final_proj).scale(1.3))
                  )     
        
        self.play(FadeOut(u_label), FadeOut(unit_vector), FadeOut(rotating_vector), FadeOut(x_label), FadeOut(Group(constraint, var, rect11)))
        self.play(FadeIn(axes), FadeIn(dots))

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.restore())


        self.play(self.camera.frame.animate.shift(LEFT*18.4).scale(1.18).shift(UP*1.54))

        self.wait(2)


        # Define PCA1 and PCA2 unit vectors (perpendicular)
        # PCA1 angle roughly aligned with the data spread
        PCA1_angle = PI/8  # 22.5 degrees for good visibility
        PCA1_unit_x = np.cos(PCA1_angle)
        PCA1_unit_y = np.sin(PCA1_angle)
        
        # PCA2 is perpendicular to PCA1
        PCA2_angle = PCA1_angle + PI/2
        PCA2_unit_x = np.cos(PCA2_angle)
        PCA2_unit_y = np.sin(PCA2_angle)
        
        # Create PCA1 vector (RED) - half the original size
        PURE_RED = "#FF0000"
        PCA1_length = 1.25  # Half of 2.5
        PCA1_vector = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(PCA1_unit_x * PCA1_length, PCA1_unit_y * PCA1_length),
            buff=0,
            stroke_width=4  # Reduced from 6
        ).set_color(PURE_RED)
        
        # Create PCA2 vector (PURE_BLUE) - half the original size
        PURE_BLUE_HEX = "#0000FF"
        PCA2_length = 1.25  # Half of 2.5
        PCA2_vector = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(PCA2_unit_x * PCA2_length, PCA2_unit_y * PCA2_length),
            buff=0,
            stroke_width=4  # Reduced from 6
        ).set_color(PURE_BLUE_HEX)
        
        # Create dotted lines along both vectors
        PCA1_dotted_line = DashedLine(
            axes.c2p(-PCA1_unit_x * 3, -PCA1_unit_y * 3),
            axes.c2p(PCA1_unit_x * 3, PCA1_unit_y * 3),
            stroke_width=3
        ).set_color(PURE_RED)
        
        PCA2_dotted_line = DashedLine(
            axes.c2p(-PCA2_unit_x * 3, -PCA2_unit_y * 3),
            axes.c2p(PCA2_unit_x * 3, PCA2_unit_y * 3),
            stroke_width=3
        ).set_color(PURE_BLUE_HEX)
        
        # Labels for PCA vectors
        PCA1_label = Tex(r"PC_1", font_size=48).set_color(PURE_RED)
        PCA1_label.next_to(PCA1_vector.get_end(), UR, buff=0.15).shift(UP*0.5)
        
        PCA2_label = Tex(r"PC_2", font_size=48).set_color(PURE_BLUE_HEX)
        PCA2_label.next_to(PCA2_vector.get_end(), UL, buff=0.15).shift(LEFT*0.3)
        
        # Show dotted lines first (they go behind the vectors)
        self.play(
            ShowCreation(PCA1_dotted_line),
            ShowCreation(PCA2_dotted_line),
            run_time=1.5
        )
        
        # Show PCA vectors
        self.play(
            GrowFromCenter(PCA1_vector),
            GrowFromCenter(PCA2_vector),
            ShowCreation(PCA1_label),
            ShowCreation(PCA2_label),
            run_time=2
        )
        
        self.wait(1)
        
        # Get centered data points coordinates
        centered_coords = []
        for x, y in scaled_points:
            centered_x = x - mean_x
            centered_y = y - mean_y
            centered_coords.append([centered_x, centered_y])
        
        # Project dots onto PCA1 line using Transform from copy()
        PCA1_projections = VGroup()
        for centered_x, centered_y in centered_coords:
            # Calculate dot product (projection length)
            proj_length = PCA1_unit_x * centered_x + PCA1_unit_y * centered_y
            
            # Project onto PCA1 direction
            proj_x = proj_length * PCA1_unit_x
            proj_y = proj_length * PCA1_unit_y
            
            proj_dot = Dot(axes.c2p(proj_x, proj_y), radius=0.12)  # Same radius as original dots
            proj_dot.set_color(RED_D)
            PCA1_projections.add(proj_dot)
        
        # Project dots onto PCA2 line using Transform from copy()
        PCA2_projections = VGroup()
        for centered_x, centered_y in centered_coords:
            # Calculate dot product (projection length)
            proj_length = PCA2_unit_x * centered_x + PCA2_unit_y * centered_y
            
            # Project onto PCA2 direction
            proj_x = proj_length * PCA2_unit_x
            proj_y = proj_length * PCA2_unit_y
            
            proj_dot = Dot(axes.c2p(proj_x, proj_y), radius=0.12)  # Same radius as original dots
            proj_dot.set_color(BLUE_E)
            PCA2_projections.add(proj_dot)
        
        # Animate projections onto PCA1 using Transform from copy
        self.play(
            ReplacementTransform(dots.copy(), PCA1_projections),
            run_time=2
        )
        
        self.wait(1)
        
        # Animate projections onto PCA2 using Transform from copy
        self.play(
            ReplacementTransform(dots.copy(), PCA2_projections),
            run_time=2
        )
        
        

        self.play(FadeOut(dots))

        self.wait(3)

        self.wait(1)

        self.play(FadeIn(Group(PCA2_dotted_line, PCA2_label, PCA2_vector)))


        self.wait(2)




class PCA_MultiplePoints(Scene):
    def construct(self):
        # Camera frame adjustment
        self.camera.frame.scale(0.88)

        # Generate 5x more data points (150) spread diagonally
        np.random.seed(42)
        n_points = 150  # 5x more than 30
        
        # Create diagonal spread from corner to corner, already centered at origin
        # Diagonal from (-2.5, -2) to (2.5, 2) 
        x_vals = np.linspace(-2.5, 2.5, n_points)
        y_vals = np.linspace(-2, 2, n_points)
        
        # Add slight noise for realistic spread
        noise_x = np.random.normal(scale=0.1, size=n_points)
        noise_y = np.random.normal(scale=0.1, size=n_points)
        
        x_vals += noise_x
        y_vals += noise_y
        
        data_points = list(zip(x_vals, y_vals))

        # Create axes with same style as before
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={
                "stroke_width": 6,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            }
        ).set_color(GREY_D)

        # Create visible dots - bigger than before
        dots = VGroup()
        for x, y in data_points:
            dot = Dot(axes.c2p(x, y), radius=0.035).set_color(BLUE_D)  # More visible size
            dots.add(dot)

        # Show axes first
        self.play(
            ShowCreation(axes.x_axis),
            ShowCreation(axes.y_axis),
            run_time=1.5
        )

        # Show all data points (already at mean/centered)
        self.play(
            LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.05),
            run_time=3
        )

        self.wait(1)

        # Create convex hull cloud - PURE RED AURA with higher opacity
        points_np = np.array([[x, y] for x, y in data_points])
        hull = ConvexHull(points_np)
        hull_points = [axes.c2p(points_np[i][0], points_np[i][1]) for i in hull.vertices]

        # Create RED aura cloud polygon - no stroke, only fill with higher opacity
        PURE_RED = "#FF0000"
        cloud_polygon = Polygon(
            *hull_points,
            stroke_width=0,  # No outer stroke
            fill_color=PURE_RED,
            fill_opacity=0.4  # Higher opacity for more visible aura
        ).scale(1.3)
        


        # Show the RED aura
        self.play(FadeIn(cloud_polygon), run_time=1.5)
        self.wait(2)  # Wait 2 seconds

        # Fade out the red aura
        self.play(FadeOut(cloud_polygon), run_time=1.5)
        self.wait(1)

        # Since data is already centered, calculate PCA directly
        centered_coords = [[x, y] for x, y in data_points]

        # Calculate PCA using covariance matrix
        data_matrix = np.array(centered_coords).T
        cov_matrix = np.cov(data_matrix)
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Sort by eigenvalues (descending order)
        sorted_indices = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[sorted_indices]
        eigenvectors = eigenvectors[:, sorted_indices]

        # Get principal components
        pc1_vector = eigenvectors[:, 0]  # Higher variance
        pc2_vector = eigenvectors[:, 1]  # Lower variance

        # Create PC vectors
        PURE_BLUE = "#0000FF"
        vector_length = 1.8

        pc1_arrow = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(pc1_vector[0] * vector_length, pc1_vector[1] * vector_length),
            buff=0,
            stroke_width=4
        ).set_color(PURE_RED)

        pc2_arrow = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(pc2_vector[0] * vector_length, pc2_vector[1] * vector_length),
            buff=0,
            stroke_width=4
        ).set_color(PURE_BLUE)

        # Create dotted lines along both PC vectors
        pc1_dotted_line = DashedLine(
            axes.c2p(-pc1_vector[0] * 3, -pc1_vector[1] * 3),
            axes.c2p(pc1_vector[0] * 3, pc1_vector[1] * 3),
            stroke_width=3
        ).set_color(PURE_RED)

        pc2_dotted_line = DashedLine(
            axes.c2p(-pc2_vector[0] * 3, -pc2_vector[1] * 3),
            axes.c2p(pc2_vector[0] * 3, pc2_vector[1] * 3),
            stroke_width=3
        ).set_color(PURE_BLUE)

        # Show dotted lines first
        self.play(
            ShowCreation(pc1_dotted_line),
            ShowCreation(pc2_dotted_line),
            run_time=1.5
        )

        # Show PC vectors (no labels)
        self.play(
            GrowFromCenter(pc1_arrow),
            GrowFromCenter(pc2_arrow),
            run_time=2
        )

        self.wait(1)

        # Create projections for both PCs with respective colors
        pc1_projections = VGroup()
        pc2_projections = VGroup()

        for x, y in data_points:
            # Project onto PC1 - RED dots
            proj_length_1 = np.dot([x, y], pc1_vector)
            proj_x1 = proj_length_1 * pc1_vector[0]
            proj_y1 = proj_length_1 * pc1_vector[1]
            proj_dot1 = Dot(axes.c2p(proj_x1, proj_y1), radius=0.025).set_color(PURE_RED)  # RED for PC1
            pc1_projections.add(proj_dot1)

            # Project onto PC2 - BLUE dots
            proj_length_2 = np.dot([x, y], pc2_vector)
            proj_x2 = proj_length_2 * pc2_vector[0]
            proj_y2 = proj_length_2 * pc2_vector[1]
            proj_dot2 = Dot(axes.c2p(proj_x2, proj_y2), radius=0.025).set_color(PURE_BLUE)  # BLUE for PC2
            pc2_projections.add(proj_dot2)

        # First projection: Transform original data to PC1
        self.play(
            ReplacementTransform(dots.copy(), pc1_projections),
            run_time=2
        )

        self.wait(1)

        # Second projection: Transform original data to PC2
        self.play(
            ReplacementTransform(dots.copy(), pc2_projections),
            run_time=2
        )

        self.wait(2)

        # Add both projections as separate objects
        self.add(pc1_projections, pc2_projections)

        # Fade out PC2 everything AND original dots
        self.play(
            FadeOut(pc2_arrow),
            FadeOut(pc2_dotted_line),
            FadeOut(pc2_projections),
            FadeOut(dots),
            run_time=2
        )

        self.wait(3)
