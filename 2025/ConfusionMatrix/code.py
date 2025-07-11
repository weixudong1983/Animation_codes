from manimlib import *

class ConfusionMatrixAnimation(Scene):
    def construct(self):

        self.camera.frame.shift(UP*0.7+LEFT*0.9).scale(0.8)

        # Create larger 2x2 grid using rectangles
        cell_size = 2
        cells = VGroup()
        for i in range(2):
            for j in range(2):
                rect = Square(side_length=cell_size)
                rect.shift(RIGHT * j * cell_size + DOWN * i * cell_size)
                cells.add(rect)

        # Center whole matrix
        cells.move_to(ORIGIN)
        self.play(LaggedStartMap(ShowCreation, cells, lag_ratio=0.2))
        self.wait(1)

        # Add row and column labels
        actual = Text("Actual").scale(0.8).next_to(cells, LEFT, buff=0.8).shift(LEFT)
        actual.rotate(PI / 2)  # Rotate 90 degrees left

        predicted = Text("Predicted").scale(0.7).next_to(cells, UP, buff=0.7)
        predicted.shift(UP * 0.3)  # Move slightly up

        actual_pos = Text("Positive").scale(0.5)
        actual_neg = Text("Negative").scale(0.5)
        predicted_pos = Text("Positive").scale(0.5)
        predicted_neg = Text("Negative").scale(0.5)

        # Positioning row labels
        actual_pos.next_to(cells[0], LEFT, buff=0.3)
        actual_neg.next_to(cells[2], LEFT, buff=0.3)

        # Positioning column labels
        predicted_pos.next_to(cells[0], UP, buff=0.3)
        predicted_neg.next_to(cells[1], UP, buff=0.21)

        self.play(Write(actual_pos), Write(actual_neg), Write(predicted_pos), Write(predicted_neg), Write(actual), Write(predicted))
        self.wait(2)

        # Highlight TP
        row_highlight = SurroundingRectangle(actual_pos, color=YELLOW, buff=0.1).scale(1.1)
        col_highlight = SurroundingRectangle(predicted_pos, color=YELLOW, buff=0.1).scale(1.1)
        self.play(ShowCreation(row_highlight), ShowCreation(col_highlight))
        self.wait(0.5)

        # Fill TP cell
        tp_fill = cells[0].copy().set_fill(color=GREEN, opacity=0.6)
        self.play(FadeIn(tp_fill))
        tp_text = Text("TP").scale(1.5).move_to(cells[0])
        self.play(FadeIn(tp_text))
        self.wait(1)

        # Transform highlights to FN
        new_row_highlight = SurroundingRectangle(actual_pos, color=YELLOW, buff=0.1).scale(1.1)
        new_col_highlight = SurroundingRectangle(predicted_neg, color=YELLOW, buff=0.1).scale(1.1)
        self.play(
            Transform(row_highlight, new_row_highlight),
            Transform(col_highlight, new_col_highlight),
        )
        fn_fill = cells[1].copy().set_fill(color=RED, opacity=0.6)
        self.play(FadeIn(fn_fill))
        fn_text = Text("FN").scale(1.5).move_to(cells[1])
        self.play(FadeIn(fn_text))
        self.wait(1)

        # Transform highlights to FP
        new_row_highlight2 = SurroundingRectangle(actual_neg, color=YELLOW, buff=0.1).scale(1.1)
        new_col_highlight2 = SurroundingRectangle(predicted_pos, color=YELLOW, buff=0.1).scale(1.1)
        self.play(
            Transform(row_highlight, new_row_highlight2),
            Transform(col_highlight, new_col_highlight2),
        )
        fp_fill = cells[2].copy().set_fill(color=ORANGE, opacity=0.6)
        self.play(FadeIn(fp_fill))
        fp_text = Text("FP").scale(1.5).move_to(cells[2])
        self.play(FadeIn(fp_text))
        self.wait(1)

        # Transform highlights to TN
        new_row_highlight3 = SurroundingRectangle(actual_neg, color=YELLOW, buff=0.1).scale(1.1)
        new_col_highlight3 = SurroundingRectangle(predicted_neg, color=YELLOW, buff=0.1).scale(1.1)
        self.play(
            Transform(row_highlight, new_row_highlight3),
            Transform(col_highlight, new_col_highlight3),
        )
        tn_fill = cells[3].copy().set_fill(color=BLUE, opacity=0.6)
        self.play(FadeIn(tn_fill))
        tn_text = Text("TN").scale(1.5).move_to(cells[3])
        self.play(FadeIn(tn_text))
        self.wait(1)

        # Fade out highlights
        self.play(FadeOut(row_highlight), FadeOut(col_highlight))
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1).shift(RIGHT*3.79+DOWN*0.5), FadeOut(VGroup(actual, predicted, actual_neg, actual_pos, predicted_neg, predicted_pos)))

        temp1 = Text("Accuracy").next_to(cells, RIGHT).shift(UP).shift(RIGHT*1.56+UP*0.67).set_color(YELLOW)
        self.play(ShowCreation(temp1))

        temp2 = Text("TP + TN").next_to(temp1, DOWN).shift(DOWN*0.6).scale(0.77)
        self.play(TransformFromCopy(tp_text, temp2[:2]), TransformFromCopy(tn_text, temp2[3:5]), FadeIn(temp2[2]))

        line = Line(tn_text.get_center(), tn_text.get_center()+RIGHT*5.8, stroke_width=5).shift(RIGHT*1.32+UP*0.766)
        self.play(ShowCreation(line))

        temp3 = Text("TP + FN + FP + TN").next_to(line, DOWN).scale(0.77)

        self.play(
            TransformFromCopy(tp_text, temp3[:2]),
            TransformFromCopy(fn_text, temp3[3:5]),
            TransformFromCopy(fp_text, temp3[6:8]),
            TransformFromCopy(tn_text, temp3[9:]),
            FadeIn(VGroup(temp3[2], temp3[5], temp3[8]))
           
                  )
        
        self.wait(2)

        temp = Text("Precision").move_to(temp1).set_color(YELLOW)
        self.play(Transform(temp1, temp), FadeOut(VGroup(temp2, temp3, line)))
        self.wait(2)

        temp2 = Text("TP").next_to(temp1, DOWN).shift(DOWN*0.88)
        self.play(TransformFromCopy(tp_text, temp2))

        line = Line(tn_text.get_center(), tn_text.get_center()+RIGHT*3.5, stroke_width=8).shift(RIGHT*2.62+UP*0.566)
        self.play(ShowCreation(line))

        temp3 = Text("TP + FP").next_to(line, DOWN)

        self.play(

            TransformFromCopy(tp_text, temp3[:2]),
            TransformFromCopy(fp_text, temp3[3:5]),
            FadeIn(VGroup(temp3[2])
           
                  ))
        
        self.wait(2)

        temp = Text("Recall").move_to(temp1).set_color(YELLOW)
        self.play(Transform(temp1, temp), FadeOut(VGroup(temp2, temp3, line)))
        self.wait(2)

        temp2 = Text("TP").next_to(temp1, DOWN).shift(DOWN*0.88)
        self.play(TransformFromCopy(tp_text, temp2))

        line = Line(tn_text.get_center(), tn_text.get_center()+RIGHT*3.5, stroke_width=8).shift(RIGHT*2.62+UP*0.566)
        self.play(ShowCreation(line))

        temp3 = Text("TP + FP").next_to(line, DOWN)

        self.play(

            TransformFromCopy(tp_text, temp3[:2]),
            TransformFromCopy(fp_text, temp3[3:5]),
            FadeIn(VGroup(temp3[2])
           
                  ))
        
        self.wait(2)

        temp = Text("Specificity ").move_to(temp1).set_color(YELLOW)
        self.play(Transform(temp1, temp), FadeOut(VGroup(temp2, temp3, line)))
        self.wait(2)

        temp2 = Text("TN").next_to(temp1, DOWN).shift(DOWN*0.88)
        self.play(TransformFromCopy(tn_text, temp2))

        line = Line(tn_text.get_center(), tn_text.get_center()+RIGHT*3.5, stroke_width=8).shift(RIGHT*2.62+UP*0.566)
        self.play(ShowCreation(line))

        temp3 = Text("TN + FP").next_to(line, DOWN)

        self.play(

            TransformFromCopy(tn_text, temp3[:2]),
            TransformFromCopy(fp_text, temp3[3:5]),
            FadeIn(VGroup(temp3[2])
           
                  ))
        
        self.wait(2)

        temp = Text("F1-score ").move_to(temp1).set_color(YELLOW)
        self.play(Transform(temp1, temp), FadeOut(VGroup(temp2, temp3, line)))
        self.wait(2) 

        last = Tex(r"2 \times \frac{Precision \times Recall}{Precision + Recall}").next_to(temp1, DOWN, buff=1.3).scale(1.06)
        self.play(ShowCreation(last))

        self.wait(2)



