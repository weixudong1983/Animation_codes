
from manimlib import *
import numpy as np

PURE_RED = '#FF0000'
PURE_BLUE = '#0000FF'



class GraphAnimation(Scene):
    def construct(self):

        self.camera.frame.scale(1.2).shift(RIGHT*4)

        self.camera.background_color = "#111111"

        # Square layout with F above and G below
        node_positions = {
    "F": [0, 3.5, 0],      # Move a bit downwards for centering
    "A": [-2.5, 1.5, 0],   # Move slightly to the left and upwards for balance
    "B": [2.8, 1.5, 0],    # Move slightly to the left for symmetry with A
    "D": [-2.5, -1.5, 0],  # Move slightly downwards and left for balance
    "E": [0.6, -0.5, 0],   # Move slightly right and downwards for symmetry with D
    "C": [3.5, -2.8, 0],   # Shift slightly left and downwards for better spacing
    "G": [0, -3.5, 0]      # Center vertically with D and E, and horizontally with F
}


        # Create the nodes
        nodes1 = self.create_nodes(node_positions)

        # Create the edges
        edges, edge_list = self.create_edges(node_positions)

        # Store the original edges for later transformation back
        original_edges = [edge.copy() for edge in edge_list]

        # Add nodes and edges to the scene
        self.play(*[GrowFromCenter(node) for node in nodes1.values()])
        self.play(*[GrowFromCenter(edge) for edge in edge_list])

        weights = self.create_edge_weights(node_positions)
        self.play(*[Write(weight) for weight in weights.values()])


        self.wait(2)

        # Table data with initial weights set to infinity
        nodes = ["A", "B", "C", "D", "E", "F", "G"]
        initial_weights = ["0", "∞", "∞", "∞", "∞", "∞", "∞"]  # Set initial weights to infinity, except "F" as 0
        from_nodes = ["D", "A", "B", "A", "B", "A", "E"]

        # Column headers
        headers = ["Node", "Cost", "Previous"]
        header_texts = [Text(header) for header in headers]

        # Create table header row
        header_row = VGroup(*header_texts).scale(0.7).arrange(RIGHT, buff=0.93)

        # Create table rows for each node
        rows = VGroup()
        for i in range(len(nodes)):
            node_text = Text(nodes[i]).scale(0.56)
            weight_text = Text(initial_weights[i]).scale(0.69)
            from_text = Text(from_nodes[i]).scale(0.56)

            # Arrange each row horizontally
            row = VGroup(node_text, weight_text, from_text).arrange(RIGHT, buff=1.5)
            rows.add(row)

        # Arrange all rows vertically with some spacing
        table = VGroup(header_row, rows.arrange(DOWN, buff=0.6)).set_color(BLACK).move_to(ORIGIN).shift(RIGHT*4)

        # Display the table on the scene
        table.shift(RIGHT*4).scale(1.2)
        header_row.shift(UP*3).scale(0.66)
        rows.animate.shift(DOWN)
        rows.shift(DOWN)
        table.shift(UP*0.5)
        table.shift(RIGHT*0.4).shift(LEFT*0.6)
        header_row[2].shift(RIGHT*0.24)
        header_row[0].shift(LEFT*0.24)
        table.shift(RIGHT*0.2)
        header_row[2].shift(RIGHT*0.23)
        header_row[1].shift(RIGHT*0.46)
        header_row[0].shift(RIGHT*0.23)
        # Define colors for header and rows
        header_color = GREY
        row_color = GREY
        
        # Create and add background for header row
        header_background = Rectangle(
            width=6,
            height=0.8,
            fill_color=header_color,
            fill_opacity=0.3,
            stroke_color=GREY,
            stroke_width=5
        ).move_to(header_row.get_center()).set_z_index(-1).shift(RIGHT*0.2)
        header_background.shift(LEFT*0.23).shift(UP*0.05)  # Position behind the header row
        self.add(header_background)  # Add behind the header row



        # Create and add background rectangles for each row in 'rows'
        row_backgrounds = []
        a1 = VGroup()
        count=0
        for row in rows:
            row_bg = Rectangle(
                width=6,
                height=1.06,
                fill_color=row_color,
                fill_opacity=0,  # Adjust opacity for visibility
                stroke_color=GREY,
                stroke_width=5
            ).move_to(row.get_center()).set_z_index(-1).shift(RIGHT*0.2)
            row_backgrounds.append(row_bg)
            a1.add(row_bg)
            count += 1
        self.add(a1)

        # Align the columns
        for row in rows:
            for i in range(3):
                row[i].align_to(header_row[i], LEFT).shift(RIGHT*0.3)

        for row in rows: row[2].shift(RIGHT * 0.4)

        
        self.play(Write(header_row))
        self.play(*[FadeIn(rows[i][0]) for i in range(7)])
        


        self.wait(2)

        a = SurroundingRectangle(header_row[0], color=RED).scale(1.2)
        self.play(ShowCreation(a))

        self.wait(2)
        self.play(Transform(a,SurroundingRectangle(header_row[1], color=RED).scale(1.2) ))

        self.wait(2)

        self.play(Transform(a,SurroundingRectangle(header_row[2], color=RED).scale(1.1) ))
        self.wait(2)

        self.play(Uncreate(a))

        
        
        self.wait(2)
        a = Circle(
                radius=0.5,
                fill_color=TEAL,  # Use TEAL in ManimGL (no TEAL_B)
                fill_opacity=0,
                stroke_color="#FF0000",  # Edge color for the circle
                stroke_width=7
            ).move_to(nodes1["A"]).set_z_index(2)
        
        
        self.play(nodes1["A"][0].animate.set_fill(YELLOW_C),)

        self.wait(2)

        self.play(a1[0].animate.set_fill(BLUE, 1).set_z_index(-1))

        self.play(FadeIn(rows[0][1]))
        self.wait(2)
        self.play(*[FadeIn(rows[i][1]) for i in range(1,7)])
        self.wait(1)
        self.play(a1[0].animate.set_fill(BLUE, 0).set_z_index(-1))
        self.wait(1)

        # Grouping the graph elements (nodes, edges, and weights)
        graph_elements = VGroup(*nodes1.values(), *edge_list, *weights.values(),a)

       
        # Grouping the table elements (header texts, rows, background rectangles, etc.)
        table_elements = VGroup(header_row, rows, header_background, *row_backgrounds)

        

        
        graph_elements.scale(0.85),
        table_elements.scale(0.8).shift(UP*0.1),
        self.play(
        self.camera.frame.animate.shift(DOWN*0.6))

        self.wait(1)


        queue = PriorityQueue().next_to(nodes1["G"], DOWN).shift(RIGHT*3.6).shift(DOWN*0.4)

        self.play(ShowCreation(queue))

        self.wait(1)

        queue.push("A,0", self)

        self.wait(2)

        queue.pop(self)

        self.wait()

        self.play(ShowCreation(a))

        self.wait(1.4)

        line_a_f = self.create_line(nodes1["A"], nodes1["F"])
        self.play(ShowCreation(line_a_f))
        circle_f = a.copy().move_to(nodes1["F"])
        self.play(ShowCreation(circle_f))

        text = self.align_text_parallel_to_line("0 + 3", line_a_f, )
        text1 = self.align_text_parallel_to_line("3", line_a_f, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, self.align_text_parallel_to_line("3", line_a_f)))

        self.wait()

        rect = SurroundingRectangle(rows[5][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()

        self.play(Transform(rows[5][1], Text("3").set_color(BLACK).scale(0.62).move_to(rows[5][1])))

        self.wait()
        self.play(FadeIn(rows[5][2]))
        self.wait()
        queue.push("F,3",self )

        self.play(FadeOut(text), Uncreate(rect))


        self.wait(1)

        self.play(Uncreate(circle_f))
        self.play(Uncreate(line_a_f))

        circle = a.copy().move_to(nodes1["B"])
        line1 = self.create_line(nodes1["A"], nodes1["B"])

        self.play(ShowCreation(line1))
        self.play(ShowCreation(circle))

        self.wait()

        text = self.align_text_parallel_to_line("0 + 2", line1, ).shift(DOWN*0.66)
        text1 = self.align_text_parallel_to_line("2", line1, ).shift(DOWN*0.66)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[1][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()

        self.play(Transform(rows[1][1], Text("2").set_color(BLACK).scale(0.62).move_to(rows[1][1])))

        self.wait()
        self.play(FadeIn(rows[1][2]))
        self.wait()
        queue.push("B,2",self )

        self.play(FadeOut(text), Uncreate(rect))



        self.play(Uncreate(circle))
        self.play(Uncreate(line1))


        circle = a.copy().move_to(nodes1["D"])
        line = self.create_line(nodes1["A"], nodes1["D"])

        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))

        self.wait()

        text = Text("0 + 5", line, ).next_to(line, LEFT).scale(0.66).set_color(BLACK)
        text1 = Text("5", line, ).next_to(line, LEFT).scale(0.66).set_color(BLACK)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait()

        rect = SurroundingRectangle(rows[3][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()

        self.play(Transform(rows[3][1], Text("5").set_color(BLACK).scale(0.62).move_to(rows[3][1])))

        self.wait(1)
        self.play(FadeIn(rows[3][2]))
        self.wait(1)
        queue.push("D,5",self )

        self.play(FadeOut(text), Uncreate(rect))



        self.play(Uncreate(circle))
        self.play(Uncreate(line))

        self.wait()

        queue.pop(self)
        self.wait()

        self.play(a.animate.move_to(nodes1["B"]))
        self.play(nodes1["B"][0].animate.set_fill(YELLOW))

        self.wait(1)

        circle = a.copy().move_to(nodes1["F"])
        line = self.create_line(nodes1["B"], nodes1["F"])

        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))

        

        

        text = self.align_text_parallel_to_line("2 + 4", line, )
        reflected_text = self.reflect_mobject_across_line(text.copy(), line).rotate(PI/1.6)
        text1 = self.align_text_parallel_to_line("6", line, )
        reflected_text1 = self.reflect_mobject_across_line(text1.copy(), line).rotate(PI/1.6)

        self.play(ShowCreation(reflected_text))
        self.wait(1)

        self.play(Transform(reflected_text, reflected_text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[5][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()


        self.play(FadeOut(reflected_text), Uncreate(rect))

        self.wait()

        self.play(Uncreate(circle))
        self.play(Uncreate(line))

        circle = a.copy().move_to(nodes1["A"])
        line = self.create_line(nodes1["B"], nodes1["A"])
        line1 = self.create_line(nodes1["A"], nodes1["B"])

        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("2 + 2", line1, ).shift(DOWN*0.66)
        text1 = self.align_text_parallel_to_line("4", line1, ).shift(DOWN*0.66)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[0][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()
 

        self.play(FadeOut(text), Uncreate(rect))



        self.play(Uncreate(circle))
        self.play(Uncreate(line))


        circle = a.copy().move_to(nodes1["E"])
        line = self.create_line(nodes1["B"], nodes1["E"])
        line1 = self.create_line(nodes1["E"], nodes1["B"])

        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))

        self.wait()

        text = self.align_text_parallel_to_line("2 + 1", line1, )
        text1 = self.align_text_parallel_to_line("3", line1, )

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[4][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()

        self.play(Transform(rows[4][1], Text("3").set_color(BLACK).scale(0.62).move_to(rows[4][1])))

        self.wait()
        self.play(FadeIn(rows[4][2]))
        self.wait()
        queue.push("E,3",self )

        self.play(FadeOut(text), Uncreate(rect))


        self.wait(1)

        self.play(Uncreate(circle))
        self.play(Uncreate(line))

        circle = a.copy().move_to(nodes1["C"])
        line = self.create_line(nodes1["B"], nodes1["C"])

        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))

        self.wait()

        text = Text("2 + 7").scale(0.55).set_color(BLACK).next_to(line, RIGHT)
        text1 = Text("9").scale(0.55).set_color(BLACK).next_to(line, RIGHT)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[2][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()

        self.play(Transform(rows[2][1], Text("9").set_color(BLACK).scale(0.62).move_to(rows[2][1])))

        self.wait()
        self.play(FadeIn(rows[2][2]))
        self.wait(1)
        queue.push("C,9",self )

        self.play(FadeOut(text), Uncreate(rect))


        self.wait(1)

        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait(1)

        queue.pop(self)

        self.play(a.animate.move_to(nodes1["E"]))
        self.play(nodes1["E"][0].animate.set_fill(YELLOW))


        self.wait(1)

        circle = a.copy().move_to(nodes1["G"])
        line = self.create_line(nodes1["E"], nodes1["G"])

        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))

        self.wait()

        text = Text("3 + 3").scale(0.5).set_color(BLACK).next_to(line, LEFT, buff=0.07).shift(RIGHT*0.23).shift(UP*0.1)
        text1 = Text("6").scale(0.5).set_color(BLACK).next_to(line, LEFT)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)


        rect = SurroundingRectangle(rows[6][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait()

        self.play(Transform(rows[6][1], Text("6").set_color(BLACK).scale(0.62).move_to(rows[6][1])))

        self.wait(1)
        self.play(FadeIn(rows[6][2]))
        self.wait(1)
        queue.push("G,6",self )

        self.play(FadeOut(text), Uncreate(rect))



        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait(1)


        circle = a.copy().move_to(nodes1["D"])
        line = self.create_line(nodes1["E"], nodes1["D"])
        line1 = self.create_line(nodes1["D"], nodes1["E"])
        

        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("3 + 1", line1, ).shift(DOWN*0.7)
        text1 = self.align_text_parallel_to_line("4", line1, ).shift(DOWN*0.7)

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[3][1], color=GREEN).scale(1.4)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(Transform(rows[3][1],Text("4").set_color(BLACK).scale(0.62).move_to(rows[3][1])))

        self.wait(1)

        rect1 = SurroundingRectangle(rows[3][2], color=GREEN).scale(1.4)


        self.play(Transform(rect, rect1))

        self.play(Transform(rows[3][2],Text("E").set_color(BLACK).scale(0.56).move_to(rows[3][2])))
        self.wait(1)





        queue.update_element1(index=1,value="D,4", scene=self)


        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait(1)


        circle = a.copy().move_to(nodes1["B"])
        line = self.create_line(nodes1["E"], nodes1["B"])


        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("3 + 1", line, )
        text1 = self.align_text_parallel_to_line("4", line, )

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[1][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)


        self.play(FadeOut(text), Uncreate(rect))



        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()

        #DONE

        circle = a.copy().move_to(nodes1["C"])
        line = self.create_line(nodes1["E"], nodes1["C"])


        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("3 + 3", line, ).shift(LEFT*0.5).shift(DOWN*0.4)
        text1 = self.align_text_parallel_to_line("6", line, ).rotate(2*PI).shift(LEFT*0.5).shift(DOWN*0.4)

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[2][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(Transform(rows[2][1],Text("6").set_color(BLACK).scale(0.62).move_to(rows[2][1])))

        self.wait(1)

        rect1 = SurroundingRectangle(rows[2][2], color=GREEN).scale(1.5)


        self.play(Transform(rect, rect1))

        self.play(Transform(rows[2][2],Text("E").set_color(BLACK).scale(0.56).move_to(rows[2][2])))
        self.wait(1)





        queue.update_element(index=2, scene=self)




        self.play(FadeOut(text), Uncreate(rect))



        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()

        queue.pop(self)

        self.play(a.animate.move_to(nodes1["F"]))
        self.play(nodes1["F"][0].animate.set_fill(YELLOW))

        self.wait()


        circle = a.copy().move_to(nodes1["A"])
        line = self.create_line(nodes1["F"], nodes1["A"])
        line1 = self.create_line(nodes1["A"], nodes1["F"])



        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("3 + 3", line1, )
        text1 = self.align_text_parallel_to_line("6", line1, )

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[0][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()



        circle = a.copy().move_to(nodes1["B"])
        line1 = self.create_line(nodes1["F"], nodes1["B"])
        line = self.create_line(nodes1["A"], nodes1["F"])



        self.play(ShowCreation(line1))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("3 + 4", line1, offset=0.7 )
        text1 = self.align_text_parallel_to_line("7", line1, offset=0.7)

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[1][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))



        self.play(Uncreate(circle))
        self.play(Uncreate(line1))
        self.wait()


        queue.pop(self)

        #DONE LAST


        self.play(a.animate.move_to(nodes1["D"]))
        self.play(nodes1["D"][0].animate.set_fill(YELLOW))


        self.wait(1)


        circle = a.copy().move_to(nodes1["A"])
        line = self.create_line(nodes1["D"], nodes1["A"])
        line1 = self.create_line(nodes1["A"], nodes1["D"])



        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = Text("4 + 5").set_color(BLACK).next_to(line1, LEFT, buff=0.1).scale(0.75)
        text1 = Text("9").set_color(BLACK).next_to(line1, LEFT, buff=0.25).scale(0.75)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[0][1], color=RED).scale(1.4)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))
        self.play(FadeOut(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()


        #DONE2


        circle = a.copy().move_to(nodes1["E"])
        line = self.create_line(nodes1["D"], nodes1["E"])



        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = Text("4 + 1").set_color(BLACK).scale(0.5).next_to(line, DOWN, buff=0).rotate(PI/8.4)
        text1 = Text("5").set_color(BLACK).scale(0.5).next_to(line, DOWN, buff=0).rotate(PI/8.4)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()


        circle = a.copy().move_to(nodes1["G"])
        line = self.create_line(nodes1["D"], nodes1["G"])
        line1 = self.create_line(nodes1["G"], nodes1["D"])




        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("4 + 1", line1, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("5", line1, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[6][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect))

        self.play(Transform(rows[6][1], Text("5").set_color(BLACK).scale(0.62).move_to(rows[6][1])))

        self.wait(1)



        rect1 = SurroundingRectangle(rows[6][2], color=GREEN).scale(1.5)
        
        self.play(Transform(rect, rect1))

        self.play(Transform(rows[6][2], Text("D").set_color(BLACK).scale(0.62).move_to(rows[6][2])))



        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()

        queue.update_element1(index=1, value="G,5", scene=self)
        self.wait(1)
        queue.pop(self)

        self.wait(1)


        self.play(a.animate.move_to(nodes1["G"]))
        self.play(nodes1["G"][0].animate.set_fill(YELLOW))

        self.wait()


        circle = a.copy().move_to(nodes1["D"])
        line = self.create_line(nodes1["G"], nodes1["D"])
        line1 = self.create_line(nodes1["A"], nodes1["F"])



        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("5 + 1", line, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("6", line, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[3][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()


        circle = a.copy().move_to(nodes1["E"])
        line = self.create_line(nodes1["G"], nodes1["E"])
        line1 = self.create_line(nodes1["E"], nodes1["G"])



        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = Text("5 + 3").set_color(BLACK).next_to(line1, LEFT, buff=0).scale(0.5).shift(RIGHT*0.5).shift(UP*0.2)
        text1 = Text("8").set_color(BLACK).next_to(line1, LEFT, buff=0).scale(0.5)

        self.play(ShowCreation(text))
        self.wait()

        self.play(Transform(text, text1))
        self.wait(1)



        rect = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()


        circle = a.copy().move_to(nodes1["C"])
        line = self.create_line(nodes1["G"], nodes1["C"])



        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("5 + 4", line, )
        text1 = self.align_text_parallel_to_line("9", line, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[2][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()

        self.wait(2)

        #Done

        queue.pop(self)



        self.play(a.animate.move_to(nodes1["C"]))
        self.play(nodes1["C"][0].animate.set_fill(YELLOW))


        self.wait()

        circle = a.copy().move_to(nodes1["G"])
        line = self.create_line(nodes1["C"], nodes1["G"])
        line1 = self.create_line(nodes1["G"], nodes1["C"])




        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("6 + 4", line1, )
        text1 = self.align_text_parallel_to_line("10", line1, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[6][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        #done

        self.play(FadeOut(text), Uncreate(rect))


        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()

        circle = a.copy().move_to(nodes1["E"])
        line = self.create_line(nodes1["C"], nodes1["E"])
        line1 = self.create_line(nodes1["C"], nodes1["E"])




        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = self.align_text_parallel_to_line("6 + 3", line1, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("9", line1, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        #done

        self.play(FadeOut(text), Uncreate(rect))

        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait()

        circle = a.copy().move_to(nodes1["B"])
        line = self.create_line(nodes1["C"], nodes1["B"])
        line1 = self.create_line(nodes1["B"], nodes1["C"])




        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))


        text = Text("6 + 7").set_color(BLACK).scale(0.6).next_to(line, RIGHT, buff=0.22)
        text1 = Text("13").set_color(BLACK).scale(0.6).next_to(line, RIGHT, buff=0.2)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text, text1))
        self.wait(1)

        rect = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect))

        self.wait(1)

        self.play(FadeOut(text), Uncreate(rect))

        self.play(Uncreate(circle))
        self.play(Uncreate(line))
        self.wait(2)


        self.play(FadeOut(a), FadeOut(queue))

        self.wait(2)


        

        self.play(ShowCreation(a))

        self.wait()

        self.play(a1[2].animate.set_fill(BLUE, 1))

        self.wait(1)

        b1 = nodes1["C"][1].copy()

        self.play(b1.animate.shift(DOWN*2.1).shift(RIGHT*2).scale(1.4))

        self.wait(1)

        rect = SurroundingRectangle(rows[2][2]).scale(1.23)
        self.play(ShowCreation(rect))
        self.wait(1)
        circle = a.copy().move_to(nodes1["E"])
        line = self.create_line(nodes1["C"], nodes1["E"])
        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))
        self.play(a1[2].animate.set_fill(BLUE, 0), FadeOut(rect))
        self.wait()
        b2 = nodes1["E"][1].copy()

        self.play(b2.animate.next_to(b1, LEFT).scale(1.4).shift(LEFT*1.5))

        self.wait(2)


        self.play(a1[4].animate.set_fill(BLUE, 1))

        self.wait(1)

        rect = SurroundingRectangle(rows[4][2]).scale(1.23)
        self.play(ShowCreation(rect))

        self.wait(1)

        circle = a.copy().move_to(nodes1["B"])
        line = self.create_line(nodes1["E"], nodes1["B"])
        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))
        b3 = nodes1["B"][1].copy()

        self.play(b3.animate.next_to(b2, LEFT).scale(1.4).shift(LEFT*2.1))

        self.wait(2)

        self.play(a1[4].animate.set_fill(BLUE, 0), FadeOut(rect))

        self.wait(1)

        self.play(a1[1].animate.set_fill(BLUE, 1))

        self.wait(1)

        rect = SurroundingRectangle(rows[1][2]).scale(1.23)
        self.play(ShowCreation(rect))

        self.wait(1)

        circle = a.copy().move_to(nodes1["A"])
        line = self.create_line(nodes1["B"], nodes1["A"])
        self.play(ShowCreation(line))
        self.play(ShowCreation(circle))
        b4 = nodes1["A"][1].copy()

        self.play(b4.animate.next_to(b3, LEFT).scale(1.4).shift(LEFT*1.7))

        self.wait(2)

        self.play(a1[1].animate.set_fill(BLUE, 0), FadeOut(rect))

        self.wait(1)

        c1 = Arrow(start=b4, end=b3,).set_color(BLACK)
        c2 = Arrow(start=b3, end=b2,).set_color(BLACK)
        c3 = Arrow(start=b2, end=b1,).set_color(BLACK)



        self.play(ShowCreation(c1), ShowCreation(c2), ShowCreation(c3))


        self.wait(2)

        a = SurroundingRectangle(Group(b1,b2,b3,b4), color='#0000ff').scale(1.2)
        self.play(ShowCreation(a))

        self.wait(2)













        




        


        
        

        

    

    def align_text_parallel_to_line(self, text_str, line, offset=0.37):
        # Create the TextMobject from the input string
        text = Text(text_str).set_color(BLACK)
    
        # Get the angle of the line
        angle = line.get_angle()

        # Rotate the text to match the line's angle
        text.rotate(angle)

        # Calculate the perpendicular direction to offset the text from the line
        normal_direction = rotate_vector(line.get_unit_vector(), PI / 2)

        # Position the text at the center of the line with an offset
        text.move_to(line.get_center() + normal_direction * offset)

        return text.scale(0.6)
    
    def reflect_mobject_across_line(self, mobject, line):
        # Get the center of the line as the point of reflection
        line_center = line.get_center()

        # Calculate the angle of the line to use for rotation alignment
        line_angle = line.get_angle()

        # Step 1: Translate the mobject to center it relative to the line’s center
        mobject.shift(-line_center)

        # Step 2: Rotate the mobject 180 degrees (PI radians) around the Z-axis
        # to mirror it on the opposite side of the line
        mobject.rotate(2 * (PI - line_angle), axis=OUT)

        # Step 3: Translate the mobject back to the line’s center
        mobject.shift(line_center)

        return mobject



    def create_circle(self,node):
        a = Circle(
                radius=0.5,
                fill_color=TEAL,  # Use TEAL in ManimGL (no TEAL_B)
                fill_opacity=0,
                stroke_color="#FF0000",  # Edge color for the circle
                stroke_width=7
            ).move_to(node)
        return a.set_z_index(2)
    
    def create_line(self, a,b):
        line1 = Line(start=a.get_center(), end=b.get_center(), color=PURE_RED, stroke_width=6.6).set_z_index(-0.5)
        return line1
    
    def create_nodes(self, node_positions):
        """Create nodes at specified positions with labels."""
        nodes = {}
        for label, position in node_positions.items():
            # Create a circle for the node
            node_circle = Circle(
                radius=0.5,
                fill_color=TEAL,  # Use TEAL in ManimGL (no TEAL_B)
                fill_opacity=1,
                stroke_color=DARK_BLUE,  # Edge color for the circle
                stroke_width=5.6
            )
            node_circle.move_to(position)

            # Create the label (text) for the node with black color
            node_label = Text(label,).move_to(position).set_color(BLACK).set_z_index(1)

            # Group the circle and the text together
            node_group = VGroup(node_circle, node_label)
            nodes[label] = node_group  # Store with direct label access (e.g., "A")

        return nodes

    def create_edges(self, node_positions):
        """Create undirected edges between nodes."""
        edge_list = []
        edge_pairs = [
            ("F", "A"),
            ("F", "B"),
            ("A", "B"),
            ("A", "D"),
            ("B", "E"),
            ("D", "E"),
            ("B", "C"),
            ("E", "C"),
            ("D", "G"),
            ("E", "G"),
            ("C", "G")
        ]

        for node1, node2 in edge_pairs:
            start_pos = node_positions[node1]
            end_pos = node_positions[node2]
            edge_line = Line(start_pos, end_pos, color=DARK_BLUE, stroke_width=5)
            edge_line.set_z_index(-5)  # Set z-index lower than nodes
            edge_list.append(edge_line)

        return {}, edge_list

    def create_edge_weights(self, node_positions):
        """Create weights for each edge and place them at the center of the edge, adjusting for orientation."""
        weights = {}
        edge_pairs = [
            ("F", "A", '3'),
            ("F", "B", '4'),
            ("A", "B", '2'),
            ("A", "D", '5'),
            ("B", "E", '1'),
            ("D", "E", '1'),
            ("B", "C", '7'),
            ("E", "C", '3'),
            ("D", "G", '1'),
            ("E", "G", '3'),
            ("C", "G", '4')
        ]
    
        for node1, node2, weight in edge_pairs:
            start_pos = np.array(node_positions[node1])
            end_pos = np.array(node_positions[node2])
            edge_center = (start_pos + end_pos) / 2
    
            # Calculate the direction of the edge
            direction = end_pos - start_pos
            direction_norm = np.linalg.norm(direction)
    
            # Normalize the direction vector to get the unit vector for the edge
            direction_unit = direction / direction_norm
    
            # Adjust the weight's position based on the edge's orientation with a larger offset
            if abs(direction_unit[0]) > abs(direction_unit[1]):  # More horizontal
                weight_offset = UP * 0.3  # Slightly more shift up for horizontal edges
            else:  # More vertical
                weight_offset = RIGHT * 0.3  # Slightly more shift right for vertical edges
    
            # For sloped edges, slightly shift the weight in the direction perpendicular to the edge
            perpendicular_unit = np.array([-direction_unit[1], direction_unit[0], 0]) * 0.3
    
            # Create the weight label and apply the calculated offset
            weight_label = Text(weight).move_to(edge_center + perpendicular_unit).scale(0.7).set_color(BLACK)
    
            # Store the weight
            weights[f"weight_{node1}_{node2}"] = weight_label
    
        return weights


    




class PriorityQueue(VGroup):
    def __init__(self):
        super().__init__()

        # Background pipe rectangle to hold the elements
        self.pipe = Rectangle(
            width=8,  # Increased width for larger queue
            height=1,  # Increased height for larger rectangle
            fill_color=GREY,
            fill_opacity=0.35,
            stroke_color=GREY,
            stroke_width=2
        )
        self.pipe.set_z_index(-1)

        # Elements within the priority queue
        self.elements = VGroup()
        self.add(self.pipe, self.elements)

    def push(self, element_str, scene):
        """Push an element into the priority queue with animation."""
        label, value = element_str.split(',')
        value = int(value)

        # Create an element to add to the pipe, matching rectangle height and scaling width
        element = Text(f"{label},{value}").scale(0.7).set_color(BLACK)
        element.rect = Rectangle(
            width=1.2,  # Keep width small for alignment
            height=self.pipe.get_height()*0.85,  # Match height to pipe
            fill_color=ORANGE,
            fill_opacity=1,
            stroke_color=GREY,
            stroke_width=1
        )
        
        # Group the text and rectangle together
        element_group = VGroup(element.rect, element)
        
        # Position the element on the far right initially
        element_group.next_to(self.pipe, RIGHT, buff=0.2)
        
        # Fade in on the right side of the pipe
        scene.play(FadeIn(element_group))
        
        # Add the new element to the queue structure
        self.elements.add(element_group)

        # Shift all elements to the left to ensure alignment
        self.realign_elements(scene)

    def pop(self, scene):
        """Pop the element with the smallest value and shift remaining elements."""
        # Find the element with the smallest value, prioritizing the last added element in case of ties
        min_element = min(
            enumerate(self.elements),
            key=lambda e: (int(e[1][1].get_text().split(',')[1]), -e[0])  # Prioritize by value, then by last added
        )[1]  # Extract the element itself
    
        # Move the minimum element upwards and fade it out
        scene.play(min_element.animate.move_to(self.pipe.get_left() + LEFT))
        
    
        # Remove the minimum element from the queue
        self.elements.remove(min_element)
    
        # Shift remaining elements to the left to close the gap
        self.realign_elements(scene)

        scene.play(FadeOut(min_element))


    def realign_elements(self, scene, simultaneous=False):
        """Shift all elements to align to the left within the pipe, with a small buffer between them.
        If `simultaneous` is True, all shifts occur at once (useful for pop operation)."""
        buffer = 0.2  # Adjust this value to control the spacing between elements
        animations = []
        
        for i, element in enumerate(self.elements):
            target_position = self.pipe.get_left() + RIGHT * (i * element.get_width() + i * buffer + 0.6 * element.get_width())
            anim = element.animate.move_to(target_position)
            
            if simultaneous:
                animations.append(anim)
            else:
                scene.play(anim)
        
        # Play all animations simultaneously if specified
        if simultaneous:
            scene.play(*animations)


    def update_element(self, index, scene):
        """Update the value to '^' and set the fill color to YELLOW for an element at a specified index."""
        if index < 0 or index >= len(self.elements):
            raise IndexError("Element index out of range.")

        element_group = self.elements[index]
        old_text = element_group[1].set_z_index(2)
        old_rect = element_group[0]

        # Create the new text with the "^" value
        new_text = Text(f"C,6").scale(0.7).set_color(BLACK).move_to(self.elements[index]).set_z_index(2)

        a = SurroundingRectangle(element_group, color=PURE_BLUE)

        # Animate color change and text update
        scene.play(
            ShowCreation(a)

        )
        scene.wait(2)

        scene.play(
            Transform(old_text, new_text)  # Update the text to "^"
        )

        scene.wait(2)

        scene.play(
            Uncreate(a)
        )



    def update_element1(self, index, value , scene):
        """Update the value to '^' and set the fill color to YELLOW for an element at a specified index."""
        if index < 0 or index >= len(self.elements):
            raise IndexError("Element index out of range.")

        element_group = self.elements[index]
        old_text = element_group[1].set_z_index(2)
        old_rect = element_group[0]

        # Create the new text with the "^" value
        new_text = Text(value).scale(0.7).set_color(BLACK).move_to(self.elements[index]).set_z_index(2)

        a = SurroundingRectangle(element_group, color=PURE_BLUE)

        # Animate color change and text update
        scene.play(
            ShowCreation(a)

        )
        scene.wait(2)

        scene.play(
            Transform(old_text, new_text)  # Update the text to "^"
        )

        scene.wait(2)

        scene.play(
            Uncreate(a)
        )







