from manimlib import *

class MatrixChainMultiplication(Scene):

    def construct(self):

        a = Text("A").scale(2.7).shift(LEFT*3.5+UP*2.3)
        b = Text("B").scale(2.7).next_to(a, RIGHT, buff=2.5)
        c = Text("C").scale(2.7).next_to(b, RIGHT, buff=2.5)

        self.play(ShowCreation(a), ShowCreation(b), ShowCreation(c))

        text1 = Text("10 x 30").next_to(a, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)
        text2 = Text("30 x 5").next_to(b, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)
        text3 = Text("5 x 60").next_to(c, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)

        self.play(ShowCreation(text1), ShowCreation(text2), ShowCreation(text3))

        self.wait(2)

        star1 = Text("*").scale(2).next_to(a, RIGHT, buff=0.7).shift(RIGHT*0.2)
        star2 = Text("*").scale(2).next_to(b, RIGHT, buff=0.7).shift(RIGHT*0.2)

        self.play(GrowFromCenter(star1), GrowFromCenter(star2))

        self.wait(2)



        brace1 = Brace(VGroup(text1, text2), DOWN, buff=0.66)
        brace2 = Brace(VGroup(text3), DOWN, buff=0.66)

        self.play(GrowFromCenter(brace1))
        self.wait()
        self.play(GrowFromCenter(brace2))

        self.wait(2)

        self.play(
            Transform(brace1, Brace(VGroup(text1), DOWN, buff=0.66)),
            Transform(brace2, Brace(VGroup(text2, text3), DOWN, buff=0.66)),
            )
        
        self.wait(2)
        self.play(FadeOut(VGroup(brace1, brace2)))
        self.wait(1)





        first = Text("A(BC) = 9000 + 18000").scale(1.2).shift(DOWN*2.6)
        self.play(ShowCreation(first[:6]))
        self.wait()

        self.play(GrowFromCenter(brace2))
        self.wait()
        temp = Text("30 x 5 x 60").next_to(brace2, DOWN, buff=0.6)
        
        self.play(
            TransformFromCopy(text2[0:2], temp[0:2]),
            FadeIn(temp[2]),
            TransformFromCopy(text2[-1] ,temp[3]), TransformFromCopy(text3[0], temp[3]),
            FadeIn(temp[4]),
            TransformFromCopy(text3[-2:], temp[5:])
            )
        
        self.wait(2)

        self.play(ReplacementTransform(temp, first[6:10]))
        self.wait(2)

        text4 = Text("30 x 60").scale(0.7).move_to(VGroup(text2, text3)).set_color(YELLOW)
        self.play(ReplacementTransform(VGroup(text2, text3), text4))
        self.wait(1)

        self.play(Transform(brace2, Brace(VGroup(text1, text3), DOWN, buff=0.7).shift(RIGHT*0.25)))
        self.wait(2)

        temp = Text("10 x 30 x 60").next_to(brace2, DOWN, buff=0.6)
        
        self.play(
            TransformFromCopy(text1[0:2], temp[0:2]),
            FadeIn(temp[2]),
            TransformFromCopy(text1[-2:] ,temp[3:5]), TransformFromCopy(text4[0:2], temp[3:5]),
            FadeIn(temp[5]),
            TransformFromCopy(text4[-2:], temp[6:])
            )
        
        self.wait(1)
        self.play(ReplacementTransform(temp, first[11:]), FadeIn(first[10]))

        text2 = Text("30 x 5").next_to(b, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)
        text3 = Text("5 x 60").next_to(c, DOWN, buff=0.7).set_color(YELLOW).scale(0.6)

        self.play(FadeOut(brace2), FadeOut(text4),ShowCreation(text2), ShowCreation(text3))

        self.wait()

        second = Text("A(BC) = 27000").scale(1.4).move_to(first)
        self.play(TransformMatchingTex(first, second), run_time=0.5)

        self.play(second.animate.shift(UP*1.4))

        self.wait(2)

        first = Text("(AB)C = 4500").scale(1.4).next_to(second, DOWN, buff=0.7)
        self.play(Write(first))

        self.wait(2)

        rect = SurroundingRectangle(first, color=GREEN, stroke_width=9).scale(1.25)
        self.play(ShowCreation(rect))


        self.play(self.camera.frame.animate.shift(RIGHT*16))

        a = Text("A B C D").shift(RIGHT*16).scale(2.6)
        self.play(ShowCreation(a))
        self.wait(2)

        b = Text("((AB)C)D").scale(2.6).move_to(a)
        c = Text("(AB)(CD)").scale(2.6).move_to(b)
        d = Text("(A(BC))D").scale(2.6).move_to(c)
        e = Text("((AB)C)D").scale(2.6).move_to(d)
        f = Text("A((BC)D)").scale(2.6).move_to(e)
        g = Text("A(B(CD))").scale(2.6).move_to(f)


        self.play(TransformMatchingTex(a,b), run_time=0.5)
        self.wait()
        self.play(TransformMatchingTex(b,c), run_time=0.5)
        self.wait()

        self.play(TransformMatchingTex(c,d), run_time=0.5)
        self.wait()

        self.play(TransformMatchingTex(d,e), run_time=0.5)
        self.wait()

        self.play(TransformMatchingTex(e,f), run_time=0.5)

        self.wait()

        self.play(TransformMatchingTex(f,g), run_time=0.5)

        self.wait(3)


BLUE, YELLOW = YELLOW, BLUE


class MatrixMultiplication(Scene):

    def construct(self):

        self.camera.frame.shift(RIGHT*1.05+DOWN*0.5)
        
        matrix1 = Matrix([["a", "b", "c"], ["d", "e", "f"]]).shift(LEFT).scale(1.3)
        matrix2 = Matrix([["g", "h", ], ["i", "j", ], ["k", "l",]]).next_to(matrix1, RIGHT).shift(RIGHT).scale(1.3)

        self.play(Write(matrix1), Write(matrix2))
        self.wait(1)

        text_1 = Text("2 x 3").next_to(matrix1, DOWN).shift(DOWN*0.3).scale(0.77).set_color(BLUE)
        text_2 = Text("3 x 2").next_to(matrix2, DOWN).shift(DOWN*0.3).scale(0.77).set_color(BLUE)

        self.play(Write(text_1))
        self.wait(2)
        self.play(Write(text_2))
        self.wait(2)

        a = Circle(radius=0.37, stroke_width=7, color=RED).move_to(text_1[-1])
        b = Circle(radius=0.37, stroke_width=7, color=RED).move_to(text_2[0])
        self.play(ShowCreation(a))
        self.play(ShowCreation(b))
        self.wait(2)

        self.play(Uncreate(a), Uncreate(b), self.camera.frame.animate.shift(DOWN*1.36))

        self.wait()

        matrix3 = Matrix([["ag+bi+ck", "ah+bj+cl"], ["dg+ei+fk", "dh+ej+fl"]]).scale(1.3).shift(DOWN*4+RIGHT*1.17)
        self.play(Write(matrix3.get_brackets()))
        self.wait()

        text_3 = Text("2 x 2").next_to(matrix3, DOWN).shift(DOWN*0.1).scale(0.77).set_color(BLUE)
        self.play(TransformFromCopy(text_1[0], text_3[0]), TransformFromCopy(text_2[-1], text_3[2]), FadeIn(text_3[1]),
                  self.camera.frame.animate.scale(1.1).shift(DOWN*0.16))
        
        self.wait(2)

        final_rect = SurroundingRectangle(matrix3.get_entries()[0],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)
        self.play(ShowCreation(final_rect))

        self.wait(2)

        row_rect = SurroundingRectangle(matrix1.get_rows()[0], 
                                                 color=YELLOW, 
                                                 buff=0.1).scale(1.07)
        
        col_rect = SurroundingRectangle(matrix2.get_columns()[0],
                                                 color=GREEN, 
                                                 buff=0.1).scale(1.07)
        
        self.play(ShowCreation(row_rect), ShowCreation(col_rect))

        self.wait(1)


        self.play(
            TransformFromCopy(matrix1.get_entries()[0], matrix3.get_entries()[0][0]),
            TransformFromCopy(matrix2.get_entries()[0], matrix3.get_entries()[0][1]),
            
            TransformFromCopy(matrix1.get_entries()[1], matrix3.get_entries()[0][3]),
            TransformFromCopy(matrix2.get_entries()[2], matrix3.get_entries()[0][4]),
            
            TransformFromCopy(matrix1.get_entries()[2], matrix3.get_entries()[0][6]),
            TransformFromCopy(matrix2.get_entries()[4], matrix3.get_entries()[0][7]),

            FadeIn(matrix3.get_entries()[0][2]),

            FadeIn(matrix3.get_entries()[0][5])

            
            )
        
        self.wait(2)

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[1],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.wait()

        self.play(Transform(col_rect, SurroundingRectangle(matrix2.get_columns()[1], color=GREEN).scale(1.07)))
        self.wait(1)


        self.play(
            TransformFromCopy(matrix1.get_entries()[0], matrix3.get_entries()[1][0]),
            TransformFromCopy(matrix2.get_entries()[1], matrix3.get_entries()[1][1]),
            
            TransformFromCopy(matrix1.get_entries()[1], matrix3.get_entries()[1][3]),
            TransformFromCopy(matrix2.get_entries()[3], matrix3.get_entries()[1][4]),
            
            TransformFromCopy(matrix1.get_entries()[2], matrix3.get_entries()[1][6]),
            TransformFromCopy(matrix2.get_entries()[5], matrix3.get_entries()[1][7]),

            FadeIn(matrix3.get_entries()[1][2]),

            FadeIn(matrix3.get_entries()[1][5])

            
            )
        
        self.wait(2)

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[2],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.wait()

        self.play(
            Transform(col_rect, SurroundingRectangle(matrix2.get_columns()[0], color=GREEN).scale(1.07)),
            Transform(row_rect, SurroundingRectangle(matrix1.get_rows()[1], color=YELLOW).scale(1.07))
            
            )
        self.wait(1)


        self.play(
            TransformFromCopy(matrix1.get_entries()[3], matrix3.get_entries()[2][0]),
            TransformFromCopy(matrix2.get_entries()[0], matrix3.get_entries()[2][1]),
            
            TransformFromCopy(matrix1.get_entries()[4], matrix3.get_entries()[2][3]),
            TransformFromCopy(matrix2.get_entries()[2], matrix3.get_entries()[2][4]),
            
            TransformFromCopy(matrix1.get_entries()[5], matrix3.get_entries()[2][6]),
            TransformFromCopy(matrix2.get_entries()[4], matrix3.get_entries()[2][7]),

            FadeIn(matrix3.get_entries()[2][2]),

            FadeIn(matrix3.get_entries()[2][5])

            
            )
        

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[3],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        

        self.play(
            Transform(col_rect, SurroundingRectangle(matrix2.get_columns()[1], color=GREEN).scale(1.07)),
            Transform(row_rect, SurroundingRectangle(matrix1.get_rows()[1], color=YELLOW).scale(1.07))
            
            )
        self.wait()


        self.play(
            TransformFromCopy(matrix1.get_entries()[3], matrix3.get_entries()[3][0]),
            TransformFromCopy(matrix2.get_entries()[1], matrix3.get_entries()[3][1]),
            
            TransformFromCopy(matrix1.get_entries()[4], matrix3.get_entries()[3][3]),
            TransformFromCopy(matrix2.get_entries()[3], matrix3.get_entries()[3][4]),
            
            TransformFromCopy(matrix1.get_entries()[5], matrix3.get_entries()[3][6]),
            TransformFromCopy(matrix2.get_entries()[5], matrix3.get_entries()[3][7]),

            FadeIn(matrix3.get_entries()[3][2]),

            FadeIn(matrix3.get_entries()[3][5])

            
            )
        
        self.wait()

        self.play(
            Uncreate(row_rect), Uncreate(col_rect),
                  self.camera.frame.animate.shift(RIGHT*1.7)
                  )
        
        self.wait()

        self.play(Indicate(final_rect))

        text = Text("3").next_to(matrix2, RIGHT, buff=0.8).scale(1.7).shift(RIGHT*2.88+DOWN)
        self.play(Write(text))

        self.wait(1)

        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[2],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        
        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[1],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.play(Transform(final_rect,  SurroundingRectangle(matrix3.get_entries()[0],
                                                 color=RED, 
                                                 buff=0.1).scale(1.07)))
        
        self.wait()

        
        text1 = Text("3 * 4").scale(1.7).move_to(text)

        self.play(TransformMatchingTex(text, text1), run_time=0.5)

        self.wait()

        text = Text("12").scale(1.7).move_to(text)
        self.play(TransformMatchingTex(text1, text), Uncreate(final_rect),run_time=0.5)

        self.wait(1)

        rect_1 = SurroundingRectangle(text_1, color=RED).scale(1.1)
        rect_2 = SurroundingRectangle(text_2, color=RED).scale(1.1)
       
        self.play(ShowCreation(rect_1), ShowCreation(rect_2))

        self.wait()

        text11 = Text("2 * 3 * 2").scale(1.2).next_to(text, DOWN, buff=0.9).shift(RIGHT*0.2)

        self.play(TransformFromCopy(text_1[0], text11[0]), FadeIn(text11[1]))
        self.wait(1)
        self.play(TransformFromCopy(text_1[2], text11[2]), FadeIn(text11[3]))
        self.wait(1)
        self.play(TransformFromCopy(text_2[-1], text11[-1]))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*16.8))

        a = Text("A").scale(4).shift(RIGHT*16)
        b = Text("B").scale(4).next_to(a, RIGHT, buff=0.8).shift(RIGHT*3.8)

        self.play(ShowCreation(a), ShowCreation(b))

        text1 = Text("p x q").next_to(a, DOWN+RIGHT).set_color(BLUE)
        text2 = Text("q x r").next_to(b, DOWN+RIGHT).set_color(BLUE)

        self.play(ShowCreation(text1), ShowCreation(text2))
        self.wait(2)

        star = Text("*").scale(3).next_to(a, RIGHT).shift(RIGHT*1.5)
        self.play(ShowCreation(star))

        self.wait(2)


        dimention = Text("p x r").next_to(text1, DOWN, buff=0.7).scale(1.4).shift(DOWN*0.7+LEFT*1.8)

        self.play(TransformFromCopy(text1[0], dimention[0]))
        self.play(FadeIn(dimention[1]))
        self.play(TransformFromCopy(text2[-1], dimention[-1]))
        self.wait(2)

        rect = SurroundingRectangle(dimention, color=PINK, stroke_width=8).scale(1.3)
        self.play(ShowCreation(rect))
        rect_text = Text("Dimention").next_to(rect, RIGHT, buff=1.4)
        self.play(Write(rect_text))
        self.wait(2)



        final = Text("p x q x r").next_to(text1, DOWN).shift(DOWN*2+RIGHT*2).scale(1.2).shift(LEFT*3.9+DOWN)


        self.play(TransformFromCopy(text1[0], final[0]))
        self.play(FadeIn(final[1]))

        self.play(TransformFromCopy(text1[2], final[2]), TransformFromCopy(text2[0], final[2]))
        self.play(FadeIn(final[3]))

        self.play(TransformFromCopy(text2[-1], final[-1]))

        rect = SurroundingRectangle(final, color=PINK, stroke_width=7).scale(1.35)
        self.play(ShowCreation(rect))
        self.wait()

        rect_text = Text("Number of Operations").scale(0.9).next_to(rect, RIGHT, buff=0.5)
        self.play(Write(rect_text))


        self.wait(2)








from manimlib import *

class MatrixChainMultiplication(Scene):
    def construct(self):
        # Matrix names
        a = Text("A  B  C  D", font_size=122).shift(UP*2.76)
        self.play(Write(a))

        # Dimension texts
        text1 = Text("2 x 3").next_to(a[0], DOWN, buff=0.36).scale(0.7).set_color(YELLOW)
        text2 = Text("3 x 4").next_to(a[1], DOWN, buff=0.36).scale(0.7).set_color(YELLOW)
        text3 = Text("4 x 5").next_to(a[2], DOWN, buff=0.36).scale(0.7).set_color(YELLOW)
        text4 = Text("5 x 6").next_to(a[3], DOWN, buff=0.36).scale(0.7).set_color(YELLOW)
        
        self.play(Write(text1), Write(text2), Write(text3), Write(text4))
        self.wait(2)

        # Dimension array
        dimension_array = Text("[2, 3, 4, 5, 6]", font_size=62).next_to(text3, DOWN, buff=0.86).shift(LEFT*1.12+DOWN)
        self.play(Write(dimension_array))
        self.wait(2)
        
        self.play(FadeOut(dimension_array))
        self.wait(1)

        # Create tables for operations count and order - now positioned lower
        labels = ["A", "B", "C", "D"]
        
        # Create operations count table (left)
        operations_table = self.create_table(labels, "", LEFT*3 + DOWN*1.76)
        
        # Create order table (right)
        order_table = self.create_table(labels, "", RIGHT*3 + DOWN*1.76)
        
        self.play(
            ShowCreation(operations_table),
            ShowCreation(order_table),
            VGroup(a, text1, text2, text3, text4).animate.shift(DOWN*0.76).scale(0.8)
        )

        self.play(self.camera.frame.animate.scale(0.94).shift(DOWN*0.66).scale(1.15).shift(DOWN*0.68))
        
        self.wait(2)
  
        # Create a blackbox for showing calculations
        calculation_box = Rectangle(width=12, height=0.9, fill_opacity=1, color=YELLOW, fill_color=BLACK)
        calculation_box.next_to(VGroup(operations_table, order_table), DOWN, buff=0.67)
        calculation_text = Text("", font_size=24).move_to(calculation_box.get_center())
        self.play(FadeIn(calculation_box))

        # Initialize matrices for cost and parenthesization
        n = 4  # Number of matrices
        inf = float('inf')
        m = {}  # Cost matrix
        s = {}  # Parenthesization matrix
        dimensions = [2, 3, 4, 5, 6]  # From the dimensions shown earlier
        
        # Initialize operations and order cell texts for later updates
        operations_cells = {}
        order_cells = {}
        
        # Create initial highlighting objects (but don't add them to scene yet)
        row_highlight = None
        col_highlight = None
        row_highlight2 = None
        col_highlight2 = None
        
        # Highlight the diagonal cells first (i == j cases)
        for i in range(n):
            # Get the row and column label objects
            row_label_obj = operations_table[3][i]
            col_label_obj = operations_table[4][i]
            row_label_obj2 = order_table[3][i]
            col_label_obj2 = order_table[4][i]
            
            # Get the cell object
            cell_obj = operations_table[1][i*n + i]
            cell_obj2 = order_table[1][i*n + i]
            
            # Create new highlight rectangles or transform existing ones for labels
            if row_highlight is None:
                # First time - create the highlight objects for row/column labels
                row_highlight = SurroundingRectangle(row_label_obj, buff=0.05, color=BLUE, stroke_width=2)
                row_highlight.scale(1.15)
                col_highlight = SurroundingRectangle(col_label_obj, buff=0.05, color=BLUE, stroke_width=2)
                col_highlight.scale(1.15)
                row_highlight2 = SurroundingRectangle(row_label_obj2, buff=0.05, color=BLUE, stroke_width=2)
                row_highlight2.scale(1.15)
                col_highlight2 = SurroundingRectangle(col_label_obj2, buff=0.05, color=BLUE, stroke_width=2)
                col_highlight2.scale(1.15)
                
                # Add them to the scene
                self.play(
                    ShowCreation(row_highlight),
                    ShowCreation(col_highlight),
                    ShowCreation(row_highlight2),
                    ShowCreation(col_highlight2)
                )
            else:
                # Transform existing highlights for row/column labels
                new_row_highlight = SurroundingRectangle(row_label_obj, buff=0.05, color=BLUE, stroke_width=2)
                new_row_highlight.scale(1.15)
                new_col_highlight = SurroundingRectangle(col_label_obj, buff=0.05, color=BLUE, stroke_width=2)
                new_col_highlight.scale(1.15)
                new_row_highlight2 = SurroundingRectangle(row_label_obj2, buff=0.05, color=BLUE, stroke_width=2)
                new_row_highlight2.scale(1.15)
                new_col_highlight2 = SurroundingRectangle(col_label_obj2, buff=0.05, color=BLUE, stroke_width=2)
                new_col_highlight2.scale(1.15)
                
                self.play(
                    Transform(row_highlight, new_row_highlight),
                    Transform(col_highlight, new_col_highlight),
                    Transform(row_highlight2, new_row_highlight2),
                    Transform(col_highlight2, new_col_highlight2)
                )
            
            # Fill the cell color for highlighting
            cell_highlight = cell_obj.copy().set_fill(BLUE, opacity=0.3)
            cell_highlight2 = cell_obj2.copy().set_fill(BLUE, opacity=0.3)
            
            # Update calculation text simultaneously with highlighting
            diag_calc_text = Text(f"Cost[{i},{i}] = 0 (single matrix)", font_size=24).move_to(calculation_box.get_center())
            
            if calculation_text.text == "":
                self.play(
                    ShowCreation(cell_highlight),
                    ShowCreation(cell_highlight2),
                    FadeIn(diag_calc_text)
                )
            else:
                self.play(
                    ShowCreation(cell_highlight),
                    ShowCreation(cell_highlight2),
                    FadeOut(calculation_text), 
                    FadeIn(diag_calc_text)
                )
            calculation_text = diag_calc_text
            self.wait(1)  # Pause to read the text
            
            # Get the exact cell position from the cell itself
            cell_pos = cell_obj.get_center()
            order_cell_pos = cell_obj2.get_center()
            
            # Create and display the value "0" for diagonal elements
            diag_text = Text("0", font_size=24, color=WHITE).move_to(cell_pos)
            diag_text2 = Text("-", font_size=24, color=WHITE).move_to(order_cell_pos)
            
            self.play(FadeIn(diag_text), FadeIn(diag_text2))
            operations_cells[(i, i)] = diag_text
            order_cells[(i, i)] = diag_text2
            
            # Store the values
            m[(i, i)] = 0
            
            # Remove cell highlighting
            self.play(
                FadeOut(cell_highlight),
                FadeOut(cell_highlight2)
            )
            
            self.wait(0.5)
        
        # Fill the table for l >= 1 (chain length)
        for l in range(1, n):
            # Update calculation text to show what we're calculating now
            chain_calc_text = Text(f"Calculating for chain length {l+1}", font_size=24).move_to(calculation_box.get_center())
            self.play(FadeOut(calculation_text), FadeIn(chain_calc_text))
            calculation_text = chain_calc_text
            self.wait(1)  # Pause to read the text
            
            if l == 2:  # For 3-chain (like ABC), add a special explanation
                explain_text = Text(f"For 3 matrices (like ABC), we need to check all possible groupings:", font_size=20).move_to(calculation_box.get_center())
                self.play(FadeOut(calculation_text), FadeIn(explain_text))
                calculation_text = explain_text
                self.wait(1.5)
                
                options_text = Text(f"(A(BC)) vs ((AB)C)", font_size=20).move_to(calculation_box.get_center())
                self.play(FadeOut(calculation_text), FadeIn(options_text))
                calculation_text = options_text
                self.wait(1.5)
                
                choose_text = Text(f"We'll choose the grouping with minimum number of operations", font_size=20).move_to(calculation_box.get_center())
                self.play(FadeOut(calculation_text), FadeIn(choose_text))
                calculation_text = choose_text
                self.wait(1.5)
                
                chain_calc_text = Text(f"Calculating for chain length {l+1}", font_size=24).move_to(calculation_box.get_center())
                self.play(FadeOut(calculation_text), FadeIn(chain_calc_text))
                calculation_text = chain_calc_text
                self.wait(1)
            
            for i in range(n-l):
                j = i + l
                
                # Get the row and column label objects
                row_label_obj = operations_table[3][i]
                col_label_obj = operations_table[4][j]
                row_label_obj2 = order_table[3][i]
                col_label_obj2 = order_table[4][j]
                
                # Get the cell object
                cell_obj = operations_table[1][i*n + j]
                cell_obj2 = order_table[1][i*n + j]
                
                # For display purposes, create a more descriptive text for what we're calculating
                matrix_range = "".join(labels[i:j+1])
                calc_desc_text = Text(f"Calculating optimal cost for {matrix_range}", font_size=22).move_to(calculation_box.get_center())
                
                # Transform highlights to new positions - keep BLUE color
                new_row_highlight = SurroundingRectangle(row_label_obj, buff=0.05, color=BLUE, stroke_width=2)
                new_row_highlight.scale(1.15)
                new_col_highlight = SurroundingRectangle(col_label_obj, buff=0.05, color=BLUE, stroke_width=2)
                new_col_highlight.scale(1.15)
                new_row_highlight2 = SurroundingRectangle(row_label_obj2, buff=0.05, color=BLUE, stroke_width=2)
                new_row_highlight2.scale(1.15)
                new_col_highlight2 = SurroundingRectangle(col_label_obj2, buff=0.05, color=BLUE, stroke_width=2)
                new_col_highlight2.scale(1.15)
                
                # Fill the cell color for highlighting
                cell_highlight = cell_obj.copy().set_fill(BLUE, opacity=0.3)
                cell_highlight2 = cell_obj2.copy().set_fill(BLUE, opacity=0.3)
                
                # Do all transformations simultaneously
                self.play(
                    Transform(row_highlight, new_row_highlight),
                    Transform(col_highlight, new_col_highlight),
                    Transform(row_highlight2, new_row_highlight2),
                    Transform(col_highlight2, new_col_highlight2),
                    ShowCreation(cell_highlight),
                    ShowCreation(cell_highlight2),
                    FadeOut(calculation_text),
                    FadeIn(calc_desc_text)
                )
                calculation_text = calc_desc_text
                self.wait(1)
                
                # Initialize min_cost and split point
                min_cost = inf
                min_k = -1
                
                # Enhanced display for showing each possible way to group matrices
                if l > 1:  # Only for chain length > 2 (3 or more matrices)
                    grouping_text = Text(f"Possible ways to group {matrix_range}:", font_size=22).move_to(calculation_box.get_center())
                    self.play(FadeOut(calculation_text), FadeIn(grouping_text))
                    calculation_text = grouping_text
                    self.wait(1)
                    
                    # Show all possible groupings first
                    grouping_examples = []
                    for k in range(i, j):
                        left_part = "".join(labels[i:k+1])
                        right_part = "".join(labels[k+1:j+1])
                        grouping = f"({left_part})({right_part})"
                        grouping_examples.append(grouping)
                    
                    groupings_display = Text(", ".join(grouping_examples), font_size=20).move_to(calculation_box.get_center())
                    self.play(FadeOut(calculation_text), FadeIn(groupings_display))
                    calculation_text = groupings_display
                    self.wait(1.5)
                    
                    testing_text = Text(f"Testing each split point...", font_size=22).move_to(calculation_box.get_center())
                    self.play(FadeOut(calculation_text), FadeIn(testing_text))
                    calculation_text = testing_text
                    self.wait(1)
                
                # For each possible split point k between i and j
                for k in range(i, j):
                    # Get the cell objects for the left and right parts
                    left_cell_obj = operations_table[1][i*n + k]
                    right_cell_obj = operations_table[1][(k+1)*n + j]
                    
                    # Highlight the cells used for calculation
                    left_cell = left_cell_obj.copy().set_fill(GREEN, opacity=0.3)
                    right_cell = right_cell_obj.copy().set_fill(GREEN, opacity=0.3)
                    
                    # Create grouping visualization
                    left_part = "".join(labels[i:k+1])
                    right_part = "".join(labels[k+1:j+1])
                    
                    split_desc = Text(f"Testing split: ({left_part})({right_part})", font_size=20).move_to(calculation_box.get_center())
                    
                    # Perform both actions simultaneously
                    self.play(
                        ShowCreation(left_cell),
                        ShowCreation(right_cell),
                        FadeOut(calculation_text),
                        FadeIn(split_desc)
                    )
                    calculation_text = split_desc
                    self.wait(1)
                    
                    # Show calculation with more details for clarity
                    left_cost = m.get((i,k), 0)
                    right_cost = m.get((k+1,j), 0)
                    mult_cost = dimensions[i] * dimensions[k+1] * dimensions[j+1]
                    
                    cost_calc_text = Text(
                        f"Cost = {left_cost} + {right_cost} + {mult_cost} = {left_cost + right_cost + mult_cost}",
                        font_size=20
                    ).move_to(calculation_box.get_center())
                    
                    # Explain the components of the cost calculation
                    cost_explanation = Text(
                        f"({left_cost}: cost of {left_part}) + ({right_cost}: cost of {right_part}) + {mult_cost}",
                        font_size=18
                    ).move_to(calculation_box.get_center())
                    
                    # Show the components first
                    self.play(FadeOut(calculation_text), FadeIn(cost_explanation))
                    calculation_text = cost_explanation
                    self.wait(1.5)
                    
                    # Then show the actual calculation
                    self.play(FadeOut(calculation_text), FadeIn(cost_calc_text))
                    calculation_text = cost_calc_text
                    self.wait(1.5)
                    
                    # Calculate the cost for this split
                    cost = left_cost + right_cost + mult_cost
                    
                    # Update min_cost if this is better
                    if cost < min_cost:
                        min_cost = cost
                        min_k = k
                        
                        min_text = Text(f"New minimum cost: {min_cost} at split: ({left_part})({right_part})", 
                                       font_size=20).move_to(calculation_box.get_center())
                        self.play(FadeOut(calculation_text), FadeIn(min_text))
                        calculation_text = min_text
                        self.wait(1)  # Pause to read the text
                    
                    # Remove the highlighting for these cells
                    self.play(
                        FadeOut(left_cell),
                        FadeOut(right_cell)
                    )
                
                # Store the computed values
                m[(i, j)] = min_cost
                s[(i, j)] = min_k
                
                # Get the exact cell positions
                cell_pos = cell_obj.get_center()
                order_cell_pos = cell_obj2.get_center()
                
                # Create and display the final values for this cell
                cost_text = Text(str(min_cost), font_size=24, color=WHITE).move_to(cell_pos)
                split_text = Text(str(min_k), font_size=24, color=WHITE).move_to(order_cell_pos)
                
                # Show the optimal split for this subproblem
                left_part = "".join(labels[i:min_k+1])
                right_part = "".join(labels[min_k+1:j+1])
                final_text = Text(f"Optimal for {matrix_range}: ({left_part})({right_part}) with cost {min_cost}", 
                                 font_size=20).move_to(calculation_box.get_center())
                
                self.play(
                    FadeOut(calculation_text), 
                    FadeIn(final_text),
                    FadeIn(cost_text), 
                    FadeIn(split_text)
                )
                calculation_text = final_text
                self.wait(1.5)  # Pause to read the text
                
                operations_cells[(i, j)] = cost_text
                order_cells[(i, j)] = split_text
                
                # Remove cell highlighting
                self.play(
                    FadeOut(cell_highlight),
                    FadeOut(cell_highlight2)
                )
                
                self.wait(0.5)
        
        # Remove all highlights for the row and column labels
        self.play(
            FadeOut(row_highlight), 
            FadeOut(col_highlight),
            FadeOut(row_highlight2), 
            FadeOut(col_highlight2)
        )
        
        # Show the final optimal solution
        optimal_cost = m.get((0, n-1), 0)
        final_result = Text(f"Optimal multiplication cost: {optimal_cost}", font_size=32).move_to(calculation_box.get_center())
        self.play(FadeOut(calculation_text), FadeIn(final_result))
        calculation_text = final_result
        self.wait(2)  # Pause to read the text
        
        # Highlight the final answer in the table
        final_cell_obj = operations_table[1][0*n + (n-1)]
        final_cell_highlight = final_cell_obj.copy().set_fill(RED, opacity=0.3)
        self.play(ShowCreation(final_cell_highlight))
        
        # Step through the optimal parenthesization with improved tracing
        step_text = Text("Tracing optimal parenthesization...", font_size=24).move_to(calculation_box.get_center())
        self.play(FadeOut(calculation_text), FadeIn(step_text))
        calculation_text = step_text
        self.wait(1.5)  # Pause to read the text
        
        # Improved tracing of the optimal parenthesization
        def trace_parenthesization(i, j, depth=0):
            nonlocal calculation_text
            
            if i == j:
                step = Text(f"Matrix {labels[i]} (single matrix)", font_size=24).move_to(calculation_box.get_center())
                self.play(FadeOut(calculation_text), FadeIn(step))
                calculation_text = step
                self.wait(1)  # Pause to read the text
                return labels[i]
                
            k = s.get((i, j), -1)
            
            # Highlight the split point cell
            split_cell_obj = order_table[1][i*n + j]
            split_cell_highlight = split_cell_obj.copy().set_fill(GREEN, opacity=0.5)
            
            # Show the split info with more details
            matrix_range = "".join(labels[i:j+1])
            left_part = "".join(labels[i:k+1])
            right_part = "".join(labels[k+1:j+1])
            
            step = Text(f"For {matrix_range}, split at k={k}: ({left_part})({right_part})", font_size=20).move_to(calculation_box.get_center())
            
            self.play(
                ShowCreation(split_cell_highlight),
                FadeOut(calculation_text), 
                FadeIn(step)
            )
            calculation_text = step
            self.wait(1.5)  # Pause to read the text
            
            self.play(FadeOut(split_cell_highlight))
            
            # Process left part
            left_step = Text(f"Process left part: {left_part}", font_size=24).move_to(calculation_box.get_center())
            self.play(FadeOut(calculation_text), FadeIn(left_step))
            calculation_text = left_step
            self.wait(1)  # Pause to read the text
            
            left = trace_parenthesization(i, k, depth+1)
            
            # Process right part
            right_step = Text(f"Process right part: {right_part}", font_size=24).move_to(calculation_box.get_center())
            self.play(FadeOut(calculation_text), FadeIn(right_step))
            calculation_text = right_step
            self.wait(1)  # Pause to read the text
            
            right = trace_parenthesization(k+1, j, depth+1)
            
            result = f"({left}{right})"
            
            # Show the combination result
            combine_step = Text(f"Combine: {result}", font_size=24).move_to(calculation_box.get_center())
            self.play(FadeOut(calculation_text), FadeIn(combine_step))
            calculation_text = combine_step
            self.wait(1.5)  # Pause to read the text
            
            return result
        
        # Trace the optimal parenthesization
        optimal_parens = trace_parenthesization(0, n-1)
        
        # Show the final parenthesization
        final_parens = Text(f"Optimal parenthesization: {optimal_parens}", font_size=24).move_to(calculation_box.get_center())
        self.play(FadeOut(calculation_text), FadeIn(final_parens))
        
        # Wait for 2 seconds and stop (as requested)
        self.wait(2)
        
        self.embed()
    
    def create_table(self, labels, title_text, position_shift):
        # Create a table with cells
        rows = 4  # Just the 4x4 grid
        cols = 4
        cell_width = 0.8
        cell_height = 0.8
        
        # Create the title
        title = Text(title_text, font_size=30).shift(UP + position_shift)
        
        # Create cells group
        cells_group = VGroup()
        cell_contents = VGroup()
        
        # Create the grid cells for the main table (not including labels)
        for i in range(rows):
            for j in range(cols):
                # Calculate position - center the grid
                pos_x = (j - cols/2 + 0.5) * cell_width + position_shift[0]
                pos_y = (rows/2 - i - 0.5) * cell_height + position_shift[1]
                
                # Create cell rectangle
                cell = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    stroke_width=1,
                    color=WHITE
                ).move_to([pos_x, pos_y, 0])
                
                cells_group.add(cell)
                
                # Add cell content
                content = Text("", font_size=20) if i != j else Text("", font_size=20)
                content.move_to(cell.get_center())
                cell_contents.add(content)
        
        # Add row labels (left of table)
        row_labels = VGroup()
        for i in range(rows):
            pos_y = (rows/2 - i - 0.5) * cell_height + position_shift[1]
            label = Text(labels[i], font_size=24).move_to([
                position_shift[0] - cols/2 * cell_width - 0.4,
                pos_y,
                0
            ])
            row_labels.add(label)
        
        # Add column labels (above table)
        col_labels = VGroup()
        for j in range(cols):
            pos_x = (j - cols/2 + 0.5) * cell_width + position_shift[0]
            label = Text(labels[j], font_size=24).move_to([
                pos_x,
                position_shift[1] + rows/2 * cell_height + 0.4,
                0
            ])
            col_labels.add(label)
            
        return VGroup(title, cells_group, cell_contents, row_labels, col_labels)
