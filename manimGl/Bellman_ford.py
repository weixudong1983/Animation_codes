from manimlib import *
import numpy as np

PURE_RED = '#FF0000'
PURE_BLUE = PURE_RED

MAROON_C = BLUE_E




class Bellman(Scene):
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
        edges, edge_list = self.create_directed_edges(node_positions)

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
        from_nodes = ["", "", "", "", "", "", ""]


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
        
        




        self.wait(1)

        self.wait()


        self.wait(2)





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
        graph_elements = VGroup(*nodes1.values(), *edge_list, *weights.values(),)

       
        # Grouping the table elements (header texts, rows, background rectangles, etc.)
        table_elements = VGroup(header_row, rows, header_background, *row_backgrounds)



        self.play(graph_elements.animate.shift(LEFT), 
                  table_elements.animate.shift(RIGHT), 
                  self.camera.frame.animate.scale(1.2).shift(DOWN))
        
        scaling_factor = 0.8
        # Manually create a list of Text objects for each edge
        edges = [
            Text("(A-F)").scale(scaling_factor),
            Text("(A-B)").scale(scaling_factor),
            Text("(A-D)").scale(scaling_factor),
            Text("(B-E)").scale(scaling_factor),
            Text("(D-E)").scale(scaling_factor),
            Text("(E-C)").scale(scaling_factor),
            Text("(E-G)").scale(scaling_factor),
            Text("(C-B)").scale(scaling_factor),
            Text("(C-G)").scale(scaling_factor),
            Text("(G-D)").scale(scaling_factor),
            Text("(F-B)").scale(scaling_factor)
        ]

        for i in range(11):
            edges[i].set_color(BLACK)
        
        # Set the initial position for the first edge at the bottom left
        edges[0].shift(LEFT * 4.67 + DOWN * 5.5)

        # Position the rest of the edges to the right of the first one
        for i, edge in enumerate(edges[1:], 1):
            edge.next_to(edges[i-1], RIGHT, buff=0.3)  # Positioning each edge to the right of the previous one



        self.play(

            TransformFromCopy(edge_list[0], edges[0]),
            TransformFromCopy(edge_list[-1], edges[1]),

            TransformFromCopy(edge_list[4], edges[2]),
            TransformFromCopy(edge_list[2], edges[3]),

            TransformFromCopy(edge_list[5], edges[4]),
            TransformFromCopy(edge_list[-2], edges[5]),

            TransformFromCopy(edge_list[3], edges[6]),
            TransformFromCopy(edge_list[-3], edges[7]),

            TransformFromCopy(edge_list[-4], edges[8]),
            TransformFromCopy(edge_list[-5], edges[9]),

            TransformFromCopy(edge_list[1], edges[10]),

            run_time=1.9



            


        )
        


        # Wait for a moment before ending the scene
        self.wait(2)


        rect = SurroundingRectangle(edges[0], color=PURE_BLUE).scale(1.1)

        self.play(ShowCreation(rect))

        self.wait(1.4)




        arrow_a_f = edge_list[0].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_f))
        self.wait()

        a = arrow_a_f.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("0 + 3", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("3", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[5][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[5][2], color=GREEN).scale(1.5).scale(2.2)


        self.wait()

        self.play(Transform(rows[5][1], Text("3").set_color(BLACK).scale(0.8).move_to(rows[5][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[5][2], Text("A").scale(0.7).set_color(BLACK).move_to(rows[5][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_f))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[1], color=PURE_BLUE).scale(1.1)))



        self.wait(1)


        arrow_a_b = edge_list[-1].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_b))
        self.wait()

        a = arrow_a_b.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("0 + 2", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("2", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[1][2], color=GREEN).scale(1.5).scale(2.2)


        self.wait()

        self.play(Transform(rows[1][1], Text("2").set_color(BLACK).scale(0.8).move_to(rows[1][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[1][2], Text("A").scale(0.7).set_color(BLACK).move_to(rows[1][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_b))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[2], color=PURE_RED).scale(1.1)))

        self.wait(1)




        #done


        arrow_a_d = edge_list[4].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_d))
        self.wait()

        a = arrow_a_b.copy().rotate(-PI)


        text = Text("0 + 5",).next_to(a, LEFT).scale(0.66).set_color(BLACK).shift(LEFT*0.6+DOWN*1.4)
        text1 = Text("5", ).next_to(a, LEFT).scale(0.66).set_color(BLACK).shift(LEFT*1.4+DOWN*1.4)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[3][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[3][2], color=GREEN).scale(1.5).scale(2.2)


        self.wait()

        self.play(Transform(rows[3][1], Text("5").set_color(BLACK).scale(0.8).move_to(rows[3][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[3][2], Text("A").scale(0.7).set_color(BLACK).move_to(rows[3][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_d))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[3], color=PURE_RED).scale(1.1)))

        self.wait(1)


        #done



        arrow_b_e = edge_list[2].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_b_e))
        self.wait()

        a = arrow_b_e.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("2 + 1", a, )
        text1 = self.align_text_parallel_to_line("3", a, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[4][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[4][2], color=GREEN).scale(1.5).scale(2.2)


        self.wait()

        self.play(Transform(rows[4][1], Text("3").set_color(BLACK).scale(0.8).move_to(rows[4][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[4][2], Text("B").scale(0.7).set_color(BLACK).move_to(rows[4][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_b_e))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[4], color=PURE_RED).scale(1.1)))

        self.wait(1)



        #done



        arrow_d_e = edge_list[5].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_d_e))
        self.wait()

        a = arrow_d_e.copy().rotate(PI)


        text = self.align_text_parallel_to_line("5 + 1", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("6", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(2)


        self.play(FadeOut(rect1))
        self.wait()
    

        self.play(FadeOut(text), FadeOut(arrow_d_e))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[5], color=PURE_RED).scale(1.1)))

        self.wait(1)

        #done




        arrow_e_c = edge_list[-2].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_e_c))
        self.wait()

        a = arrow_e_c.copy().rotate(PI)


        text = self.align_text_parallel_to_line("3 + (-3)", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("0", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[2][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[2][2], color=GREEN).scale(1.5).scale(2.2)


        self.wait()

        self.play(Transform(rows[2][1], Text("0").set_color(BLACK).scale(0.8).move_to(rows[2][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[2][2], Text("E").scale(0.7).set_color(BLACK).move_to(rows[2][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_e_c))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[6], color=PURE_RED).scale(1.1)))

        self.wait(2)

        
        #done



        arrow_e_g = edge_list[3].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_e_g))
        self.wait()

        a = arrow_e_g.copy().rotate(PI)


        text = self.align_text_parallel_to_line("3 + 3", a, ).rotate(PI).rotate(PI/2).shift(LEFT*0.5+UP*0.2)
        text1 = self.align_text_parallel_to_line("6", a, ).rotate(PI).rotate(PI/2).shift(LEFT*0.1+UP*0.2)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[6][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[6][2], color=GREEN).scale(1.5).scale(2.2)


        self.wait()

        self.play(Transform(rows[6][1], Text("6").set_color(BLACK).scale(0.8).move_to(rows[6][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[6][2], Text("E").scale(0.7).set_color(BLACK).move_to(rows[6][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_e_g))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[7], color=PURE_RED).scale(1.1)))

        self.wait(2)


        #done



        arrow_c_b = edge_list[-3].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_c_b))
        self.wait()

        a = arrow_c_b.copy().rotate(PI)


        text = self.align_text_parallel_to_line("5 + 1", a, ).rotate(PI).rotate(-PI/2.1).shift(RIGHT)
        text1 = self.align_text_parallel_to_line("6", a, ).rotate(PI).rotate(-PI/2.1).shift(RIGHT)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(2)


        self.play(FadeOut(text), FadeOut(arrow_c_b), FadeOut(rect1))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[-3], color=PURE_RED).scale(1.1)))

        self.wait(1)


        #done



        arrow_c_g = edge_list[7].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_c_g))
        self.wait()

        a = arrow_c_g.copy().rotate(PI)


        text = self.align_text_parallel_to_line("0 + 4", a, )
        text1 = self.align_text_parallel_to_line("4", a, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[6][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[6][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[6][1], Text("4").set_color(BLACK).scale(0.8).move_to(rows[6][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[6][2], Text("C").scale(0.7).set_color(BLACK).move_to(rows[6][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_c_g))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[9], color=PURE_RED).scale(1.1)))

        self.wait(2)


        #done


        arrow_g_d = edge_list[-5].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_g_d))
        self.wait()

        a = arrow_g_d.copy()


        text = self.align_text_parallel_to_line("4 + (-1)", a,offset=0.5 ).rotate(PI)
        text1 = self.align_text_parallel_to_line("3", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[3][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[3][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[3][1], Text("3").set_color(BLACK).scale(0.8).move_to(rows[3][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[3][2], Text("G").scale(0.7).set_color(BLACK).move_to(rows[3][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_g_d))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[10], color=PURE_RED).scale(1.1)))

        self.wait(2)



        #doone



        arrow_f_b = edge_list[1].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_f_b))
        self.wait()

        a = arrow_f_b.copy()


        text = self.align_text_parallel_to_line("3 + (-4)", a, offset=0.76)
        text1 = self.align_text_parallel_to_line("-1", a, offset=0.76 )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[1][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[1][1], Text("-1").set_color(BLACK).scale(0.8).move_to(rows[1][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[1][2], Text("F").scale(0.7).set_color(BLACK).move_to(rows[1][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_f_b))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[0], color=PURE_RED).scale(1.1)))

        self.wait(2)



        #First Iteration Done Now Second





        arrow_a_f = edge_list[0].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_f))
        self.wait()

        a = arrow_a_f.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("0 + 3", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("3", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[5][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))
  
        self.wait()



        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_f))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[1], color=PURE_BLUE).scale(1.1)))



        self.wait(1)


        arrow_a_b = edge_list[-1].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_b))
        self.wait()

        a = arrow_a_b.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("0 + 2", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("2", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(1)


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_b))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[2], color=PURE_RED).scale(1.1)))

        self.wait(1)




        #done


        arrow_a_d = edge_list[4].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_d))
        self.wait()

        a = arrow_a_b.copy().rotate(-PI)


        text = Text("0 + 5",).next_to(a, LEFT).scale(0.66).set_color(BLACK).shift(LEFT*0.6+DOWN*1.4)
        text1 = Text("5", ).next_to(a, LEFT).scale(0.66).set_color(BLACK).shift(LEFT*1.4+DOWN*1.4)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[3][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait()


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_d))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[3], color=PURE_RED).scale(1.1)))

        self.wait(1)


        #DONE 



        arrow_b_e = edge_list[2].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_b_e))
        self.wait()

        a = arrow_b_e.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("-1 + 1", a, )
        text1 = self.align_text_parallel_to_line("0", a, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[4][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[4][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[4][1], Text("0").set_color(BLACK).scale(0.8).move_to(rows[4][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_b_e))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[4], color=PURE_RED).scale(1.1)))

        self.wait(1)



        #done



        arrow_d_e = edge_list[5].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_d_e))
        self.wait()

        a = arrow_d_e.copy().rotate(PI)


        text = self.align_text_parallel_to_line("3 + 1", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("4", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(2)


        self.play(FadeOut(rect1))
        self.wait()
    

        self.play(FadeOut(text), FadeOut(arrow_d_e))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[5], color=PURE_RED).scale(1.1)))

        self.wait(1)

        #done




        arrow_e_c = edge_list[-2].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_e_c))
        self.wait()

        a = arrow_e_c.copy().rotate(PI)


        text = self.align_text_parallel_to_line("0 + (-3)", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("-3", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[2][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[2][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[2][1], Text("-3").set_color(BLACK).scale(0.8).move_to(rows[2][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[2][2], Text("E").scale(0.7).set_color(BLACK).move_to(rows[2][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_e_c))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[6], color=PURE_RED).scale(1.1)))

        self.wait(2)

        
        #done



        arrow_e_g = edge_list[3].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_e_g))
        self.wait()

        a = arrow_e_g.copy().rotate(PI)


        text = self.align_text_parallel_to_line("0 + 3", a, ).rotate(PI).rotate(PI/2).shift(LEFT*0.5+UP*0.2)
        text1 = self.align_text_parallel_to_line("3", a, ).rotate(PI).rotate(PI/2).shift(LEFT*0.1+UP*0.2)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[6][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[6][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[6][1], Text("3").set_color(BLACK).scale(0.8).move_to(rows[6][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[6][2], Text("E").scale(0.7).set_color(BLACK).move_to(rows[6][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_e_g))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[7], color=PURE_RED).scale(1.1)))

        self.wait(2)


        #done



        arrow_c_b = edge_list[-3].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_c_b))
        self.wait()

        a = arrow_c_b.copy().rotate(PI)


        text = self.align_text_parallel_to_line("-3 + 7", a, ).rotate(PI).rotate(-PI/2.1).shift(RIGHT)
        text1 = self.align_text_parallel_to_line("4", a, ).rotate(PI).rotate(-PI/2.1).shift(RIGHT*0.7).scale(1.2)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(2)


        self.play(FadeOut(text), FadeOut(arrow_c_b), FadeOut(rect1))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[-3], color=PURE_RED).scale(1.1)))

        self.wait(1)


        #done



        arrow_c_g = edge_list[7].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_c_g))
        self.wait()

        a = arrow_c_g.copy().rotate(PI)


        text = self.align_text_parallel_to_line("-3 + 4", a, )
        text1 = self.align_text_parallel_to_line("1", a, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[6][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[6][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[6][1], Text("1").set_color(BLACK).scale(0.8).move_to(rows[6][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[6][2], Text("C").scale(0.7).set_color(BLACK).move_to(rows[6][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_c_g))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[9], color=PURE_RED).scale(1.1)))

        self.wait(2)


        #done


        arrow_g_d = edge_list[-5].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_g_d))
        self.wait()

        a = arrow_g_d.copy()


        text = self.align_text_parallel_to_line("1 + (-1)", a,offset=0.5 ).rotate(PI)
        text1 = self.align_text_parallel_to_line("0", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[3][1], color=GREEN).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[3][2], color=GREEN).scale(1.5)


        self.wait()

        self.play(Transform(rows[3][1], Text("0").set_color(BLACK).scale(0.8).move_to(rows[3][1])))

        self.wait()
        self.play(Transform(rect1, rect2))
        self.wait()
        self.play(Transform(rows[3][2], Text("G").scale(0.7).set_color(BLACK).move_to(rows[3][2])))
        self.wait()

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_g_d))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[10], color=PURE_RED).scale(1.1)))

        self.wait(2)




        arrow_f_b = edge_list[1].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_f_b))
        self.wait()

        a = arrow_f_b.copy()


        text = self.align_text_parallel_to_line("3 + (-4)", a, offset=0.76)
        text1 = self.align_text_parallel_to_line("-1", a, offset=0.76 )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=RED).scale(1.33)
        self.play(ShowCreation(rect1))


        self.wait()


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_f_b))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[0], color=PURE_RED).scale(1.1)))

        self.wait(2)




        #DONE with the second iteratoin


        arrow_a_f = edge_list[0].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_f))
        self.wait()

        a = arrow_a_f.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("0 + 3", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("3", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[5][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))
  
        self.wait()



        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_f))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[1], color=PURE_BLUE).scale(1.1)))



        self.wait(1)


        arrow_a_b = edge_list[-1].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_b))
        self.wait()

        a = arrow_a_b.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("0 + 2", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("2", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(1)


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_b))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[2], color=PURE_RED).scale(1.1)))

        self.wait(1)




        #done


        arrow_a_d = edge_list[4].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_a_d))
        self.wait()

        a = arrow_a_b.copy().rotate(-PI)


        text = Text("0 + 5",).next_to(a, LEFT).scale(0.66).set_color(BLACK).shift(LEFT*0.6+DOWN*1.4)
        text1 = Text("5", ).next_to(a, LEFT).scale(0.66).set_color(BLACK).shift(LEFT*1.4+DOWN*1.4)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[3][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait()


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_a_d))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[3], color=PURE_RED).scale(1.1)))

        self.wait(1)


        #DONE 



        arrow_b_e = edge_list[2].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_b_e))
        self.wait()

        a = arrow_b_e.copy().rotate(-PI)


        text = self.align_text_parallel_to_line("-1 + 1", a, )
        text1 = self.align_text_parallel_to_line("0", a, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))


        self.wait()



        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_b_e))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[4], color=PURE_RED).scale(1.1)))

        self.wait(1)



        #done



        arrow_d_e = edge_list[5].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_d_e))
        self.wait()

        a = arrow_d_e.copy().rotate(PI)


        text = self.align_text_parallel_to_line("0 + 1", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("1", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[4][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(2)


        self.play(FadeOut(rect1))
        self.wait()
    

        self.play(FadeOut(text), FadeOut(arrow_d_e))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[5], color=PURE_RED).scale(1.1)))

        self.wait(1)

        #done




        arrow_e_c = edge_list[-2].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_e_c))
        self.wait()

        a = arrow_e_c.copy().rotate(PI)


        text = self.align_text_parallel_to_line("0 + (-3)", a, ).rotate(PI)
        text1 = self.align_text_parallel_to_line("-3", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[2][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))


        self.wait()



        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_e_c))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[6], color=PURE_RED).scale(1.1)))

        self.wait(2)

        
        #done



        arrow_e_g = edge_list[3].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_e_g))
        self.wait()

        a = arrow_e_g.copy().rotate(PI)


        text = self.align_text_parallel_to_line("0 + 3", a, ).rotate(PI).rotate(PI/2).shift(LEFT*0.5+UP*0.2)
        text1 = self.align_text_parallel_to_line("3", a, ).rotate(PI).rotate(PI/2).shift(LEFT*0.1+UP*0.2)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[6][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))


        self.wait()



        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_e_g))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[7], color=PURE_RED).scale(1.1)))

        self.wait(2)


        #done



        arrow_c_b = edge_list[-3].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_c_b))
        self.wait()

        a = arrow_c_b.copy().rotate(PI)


        text = self.align_text_parallel_to_line("-3 + 7", a, ).rotate(PI).rotate(-PI/2.1).shift(RIGHT)
        text1 = self.align_text_parallel_to_line("4", a, ).rotate(PI).rotate(-PI/2.1).shift(RIGHT*0.7).scale(1.2)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))

        self.wait(2)


        self.play(FadeOut(text), FadeOut(arrow_c_b), FadeOut(rect1))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[-3], color=PURE_RED).scale(1.1)))

        self.wait(1)


        #done



        arrow_c_g = edge_list[7].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_c_g))
        self.wait()

        a = arrow_c_g.copy().rotate(PI)


        text = self.align_text_parallel_to_line("-3 + 4", a, )
        text1 = self.align_text_parallel_to_line("1", a, )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[6][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))
        rect2 = SurroundingRectangle(rows[6][2], color=GREEN).scale(1.5)


        self.wait()

 

        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_c_g))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[9], color=PURE_RED).scale(1.1)))

        self.wait(2)


        #done


        arrow_g_d = edge_list[-5].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_g_d))
        self.wait()

        a = arrow_g_d.copy()


        text = self.align_text_parallel_to_line("1 + (-1)", a,offset=0.5 ).rotate(PI)
        text1 = self.align_text_parallel_to_line("0", a, ).rotate(PI)

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[3][1], color=RED).scale(1.5)
        self.play(ShowCreation(rect1))


        self.wait()


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_g_d))



        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(edges[10], color=PURE_RED).scale(1.1)))

        self.wait(2)



        #doone



        arrow_f_b = edge_list[1].copy().set_color(PURE_RED).set_z_index(1)
        self.play(ShowCreation(arrow_f_b))
        self.wait()

        a = arrow_f_b.copy()


        text = self.align_text_parallel_to_line("3 + (-4)", a, offset=0.76)
        text1 = self.align_text_parallel_to_line("-1", a, offset=0.76 )

        self.play(ShowCreation(text))
        self.wait(1)

        self.play(Transform(text,text1))

        self.wait()

        rect1 = SurroundingRectangle(rows[1][1], color=RED).scale(1.33)
        self.play(ShowCreation(rect1))


        self.wait()


        self.play(FadeOut(text), Uncreate(rect1), FadeOut(arrow_f_b))



        self.wait(1)

        self.play(FadeOut(rect))

        self.wait(2)

        self.play(*[FadeOut(i) for i in edges])

        self.wait(2)






        #DONE NOW CONSTURCT THE PATH USING THE TABLE OUTPUT
        #Let's find the path from A to G, this would be most intersting and longgest one

        a11 = Circle(stroke_color='#FF0000', stroke_width = 8, radius=0.5).move_to(nodes1["G"]).set_z_index(3)



        self.play(ShowCreation(a11), nodes1["G"][0].animate.set_fill(YELLOW))

        self.wait()

        g = nodes1["G"][1].copy()
        self.play(g.animate.shift(DOWN*2.05 + RIGHT*9.5).scale(1.8))

        self.wait(1)

        self.play(a1[-1].animate.set_fill(BLUE, 1))
        self.wait(2)






        a12 = Circle(stroke_color='#FF0000', stroke_width = 8, radius=0.5).move_to(nodes1["C"]).set_z_index(2)



        self.play(ShowCreation(a12), nodes1["C"][0].animate.set_fill(YELLOW))
        self.play(edge_list[-4].animate.set_color(PURE_RED))

        self.wait()

        c = nodes1["C"][1].copy()
        self.play(c.animate.next_to(g, LEFT, buff=2).scale(1.8))

        self.wait(1)

        self.play(a1[-1].animate.set_fill(BLUE, 0))


        self.play(a1[2].animate.set_fill(BLUE, 1))
        self.wait(2)


        #done noe going to E

        a13 = Circle(stroke_color='#FF0000', stroke_width = 8, radius=0.5).move_to(nodes1["E"]).set_z_index(2)



        self.play(ShowCreation(a13), nodes1["E"][0].animate.set_fill(YELLOW))



        self.play(edge_list[-2].animate.set_color(PURE_RED))

        self.wait()

        e = nodes1["E"][1].copy()
        self.play(e.animate.next_to(c, LEFT, buff=2).scale(1.8))

        self.wait(1)

        self.play(a1[2].animate.set_fill(BLUE, 0))


        self.play(a1[-3].animate.set_fill(BLUE, 1))
        self.wait(2)


        a14 = Circle(stroke_color='#FF0000', stroke_width = 8, radius=0.5).move_to(nodes1["B"]).set_z_index(2)



        self.play(ShowCreation(a14), nodes1["B"][0].animate.set_fill(YELLOW))
        self.play(edge_list[2].animate.set_color(PURE_RED))

        self.wait()

        b = nodes1["B"][1].copy()
        self.play(b.animate.next_to(e, LEFT, buff=2).scale(1.8))

        self.wait(1)

        self.play(a1[-3].animate.set_fill(BLUE, 0))


        self.play(a1[1].animate.set_fill(BLUE, 1))
        self.wait(2)



        a15 = Circle(stroke_color='#FF0000', stroke_width = 8, radius=0.5).move_to(nodes1["F"]).set_z_index(2)



        self.play(ShowCreation(a15), nodes1["F"][0].animate.set_fill(YELLOW))
        self.play(edge_list[1].animate.set_color(PURE_RED))

        self.wait()

        f = nodes1["F"][1].copy()
        self.play(f.animate.next_to(b, LEFT, buff=2).scale(1.8))

        self.wait(1)

        self.play(a1[1].animate.set_fill(BLUE, 0))


        self.play(a1[-2].animate.set_fill(BLUE, 1))
        self.wait(2)

        a16 = Circle(stroke_color='#FF0000', stroke_width = 8, radius=0.5).move_to(nodes1["A"]).set_z_index(2)



        self.play(ShowCreation(a16), nodes1["A"][0].animate.set_fill(YELLOW))
        self.play(edge_list[0].animate.set_color(PURE_RED))

        self.wait()

        a = nodes1["A"][1].copy()
        self.play(a.animate.next_to(f, LEFT, buff=2).scale(1.8))

        self.wait(1)

        self.play(a1[-2].animate.set_fill(BLUE, 0))


        self.wait(2)


        a1 = [a,f,b,e,c,g]
        anime = []

        for i in range(1,6):
            arrow = Arrow(start=a1[i-1].get_right(), end=a1[i].get_left()).set_color(BLACK)
            anime.append(ShowCreation(arrow))

        self.play(*[anime[i] for i in range(5)])



       

        rect = SurroundingRectangle(Group(a,b,c,e,f,g), color="#0000ff").scale(1.23)

        self.play(ShowCreation(rect))

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
            ("C", "G"),

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
            ("A", "F", '3'),
            ("F", "B", '-4'),
            ("A", "B", '2'),
            ("A", "D", '5'),
            ("B", "E", '1'),
            ("D", "E", '1'),
            ("B", "C", '7'),
            ("E", "C", '-3'),
            ("D", "G", '-1'),
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
    

    def create_directed_edges(self, node_positions):
        """Transform undirected edges into directed edges."""
        directed_edge_list = []
        edge_pairs = [
            ("A", "F"),
            ("F", "B"),
            ("B", "E"),
            ("E", "G"),
            ("A", "D"),
            ("D", "E"),
            ("G", "D"),
            ("C", "G"),
            ("C", "B"),
            ("E", "C"),
            ("A", "B")
        ]
    
        for node1, node2 in edge_pairs:
            start_pos = node_positions[node1]
            end_pos = node_positions[node2]
            directed_edge = Arrow(
                start_pos, end_pos,
                buff=0.59,  # Adjusted buff for better alignment with nodes
                color=MAROON_C,
                stroke_width=4,
                fill_color=MAROON_C,  # Fill arrowhead with the same color
                fill_opacity=1  # Make the arrowhead completely opaque
            )
            directed_edge.z_index = -1  # Set z-index lower than nodes
            directed_edge_list.append(directed_edge)
    
        return {}, directed_edge_list




