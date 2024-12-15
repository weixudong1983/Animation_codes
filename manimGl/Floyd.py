from manimlib import *

BLUE_E = DARK_BLUE


class SimpleGraph(Scene):

    def construct(self):

        self.camera.frame.shift(UP * 0.36).shift(RIGHT*0.12)
        self.camera.frame.scale(0.8)

        # Node positions
        node_positions = {
            "A": [-2, 2, 0],
            "B": [2, 2, 0],
            "C": [2, -2, 0],
            "D": [-2, -2, 0],
        }

        # Create the nodes
        nodes = self.create_nodes(node_positions)

        # Create the edges
        edge, edge_list = self.create_directed_edges(node_positions)

        # Add nodes and edges to the scene
        self.play(*[GrowFromCenter(node) for node in nodes.values()])

        start_pos = nodes["D"].get_corner(UL)
        end_pos = nodes["A"].get_corner(DL)
        edge_d_a = CurvedArrow(
                start_pos, end_pos,
                color=MAROON_C,
                stroke_width=8
            )
        edge_d_a.z_index = -1

        edge_d_a.flip().shift(LEFT*0.4)

        weight_d_a = Text("-2",).next_to(edge_d_a, LEFT).scale(0.6).set_color(BLACK).shift(RIGHT*0.13)


        start_pos1 = nodes["B"].get_corner(UL)
        end_pos1 = nodes["A"].get_corner(UR)
        edge_b_a = CurvedArrow(
                start_pos1, end_pos1,
                color=MAROON_C,
                stroke_width=8
            )
        edge_b_a.z_index = -1

        edge_b_a.shift(DOWN*0.4)

        weight_b_a = Text("3",).next_to(edge_b_a, UP).scale(0.6).set_color(BLACK).shift(DOWN*0.23)



        self.play(ShowCreation(edge_d_a), ShowCreation(edge_b_a),*[GrowFromCenter(edge) for edge in edge_list])
        weights = self.create_edge_weights(node_positions)
        weights["weight_D_C"].shift(UP*0.05)
        weights["weight_A_B"].shift(DOWN*0.5)
        self.play(*[Write(weight) for weight in weights.values()], ShowCreation(weight_d_a), ShowCreation(weight_b_a))


        self.wait(2)


        self.play(nodes["A"][0].animate.set_color(PURPLE_E))
        self.wait(1)
        self.play(nodes["B"][0].animate.set_color(BLUE_E), 
                  nodes["C"][0].animate.set_color(BLUE_E),
                  nodes["D"][0].animate.set_color(BLUE_E))
        self.wait(3)

        self.play(nodes["B"][0].animate.set_color(BLACK), 
                  nodes["C"][0].animate.set_color(BLACK),
                  nodes["A"][0].animate.set_color(BLACK),
                  nodes["D"][0].animate.set_color(BLACK))
        self.wait()

        self.play(nodes["B"][0].animate.set_color(PURPLE_E))
        self.wait()
        self.play(nodes["A"][0].animate.set_color(BLUE_E), 
                  nodes["C"][0].animate.set_color(BLUE_E),
                  nodes["D"][0].animate.set_color(BLUE_E))
        self.wait()

        self.play(nodes["B"][0].animate.set_color(BLACK), 
                  nodes["C"][0].animate.set_color(BLACK),
                  nodes["A"][0].animate.set_color(BLACK),
                  nodes["D"][0].animate.set_color(BLACK))
        self.wait()


        self.play(nodes["C"][0].animate.set_color(PURPLE_E))
        self.wait(1)
        self.play(nodes["B"][0].animate.set_color(BLUE_E), 
                  nodes["A"][0].animate.set_color(BLUE_E),
                  nodes["D"][0].animate.set_color(BLUE_E))
        self.wait()

        self.play(nodes["B"][0].animate.set_color(BLACK), 
                  nodes["C"][0].animate.set_color(BLACK),
                  nodes["A"][0].animate.set_color(BLACK),
                  nodes["D"][0].animate.set_color(BLACK))
        self.wait()

        self.play(nodes["D"][0].animate.set_color(PURPLE_E))
        self.wait()
        self.play(nodes["B"][0].animate.set_color(BLUE_E), 
                  nodes["C"][0].animate.set_color(BLUE_E),
                  nodes["A"][0].animate.set_color(BLUE_E))
        self.wait()

        self.play(nodes["B"][0].animate.set_color(BLACK), 
                  nodes["C"][0].animate.set_color(BLACK),
                  nodes["A"][0].animate.set_color(BLACK),
                  nodes["D"][0].animate.set_color(BLACK))
        self.wait(2)

        




        # # Transform undirected edges to directed edges
        # directed_edges, directed_edge_list = self.create_directed_edges(node_positions)
        # self.play(*[ReplacementTransform(edge_list[i], directed_edge_list[i]) for i in range(len(edge_list))])
        # self.wait(2)

        self.play(self.camera.frame.animate.scale(1.12).shift(RIGHT * 2.4))

        self.wait(2)

        # Create a 4x4 adjacency matrix for nodes A, B, C, D
        # Let's assume edges: A-B, A-D, B-C, C-D (example)
        new_var = Text("∞").scale(0.7)

        adjacency_matrix = Matrix(
            [[Text("0").scale(0.55), Text("2").scale(0.55), Text("∞").scale(0.6), Text("3").scale(0.5)],  # A connected to B, D
             [Text("3").scale(0.6), Text("0").scale(0.55), Text("2").scale(0.55), Text("∞").scale(0.6)],  # B connected to A, C
             [Text("∞").scale(0.6), Text("∞").scale(0.6), Text("0").scale(0.55), Text("4").scale(0.5)],  # C connected to B, D
             [Text("-2").scale(0.55), Text("6").scale(0.55), Text("∞").scale(0.6), Text("0").scale(0.55)]],  # D connected to A, C
        ).next_to(nodes["B"], RIGHT).set_color(BLACK).shift(DOWN * 2.2).shift(RIGHT*1.5).scale(1.2)

        # Add labels to the matrix
        labels = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(adjacency_matrix, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(adjacency_matrix, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(adjacency_matrix, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(adjacency_matrix, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(adjacency_matrix, UP).shift(LEFT * 1.55),
            Text("B", color=BLACK, font_size=40).next_to(adjacency_matrix, UP).shift(LEFT * 0.46999),
            Text("C", color=BLACK, font_size=40).next_to(adjacency_matrix, UP).shift(RIGHT * 0.5),
            Text("D", color=BLACK, font_size=40).next_to(adjacency_matrix, UP).shift(RIGHT * 1.6),
        ).set_color(BLACK)



        # Display the matrix and labels
        self.play(TransformFromCopy(VGroup(nodes["A"][1], nodes["B"][1], nodes["C"][1], nodes["D"][1]), labels[:4])
                  , TransformFromCopy(VGroup(nodes["A"][1], nodes["B"][1], nodes["C"][1], nodes["D"][1]), labels[4:]))
        self.wait()
        self.play(Write(adjacency_matrix))


    
        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.55).shift(RIGHT*2.8+DOWN*1.38+DOWN*0.8))

        M_0 = Tex("M_{0}",).next_to(adjacency_matrix, UP).set_color(BLACK).shift(UP*1.13).scale(1.23)
        self.play(ShowCreation(M_0))

        self.wait(2)


        adjacency_matrix1 = Matrix(
            [[Text("-").scale(0.55), Text("A").scale(0.55), Text("-").scale(0.55), Text("A").scale(0.55)],  # A connected to B, D
             [Text("B").scale(0.55), Text("-").scale(0.55), Text("B").scale(0.55), Text("-").scale(0.55)],  # B connected to A, C
             [Text("-").scale(0.55), Text("-").scale(0.55), Text("-").scale(0.55), Text("C").scale(0.55)],  # C connected to B, D
             [Text("D").scale(0.55), Text("D").scale(0.55), Text("-").scale(0.55), Text("-").scale(0.55)]],  # D connected to A, C
        ).next_to(adjacency_matrix, RIGHT).set_color(BLACK).scale(1.2).shift(RIGHT*1.6)

        # Add labels to the matrix
        labels1 = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(adjacency_matrix1, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(adjacency_matrix1, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(adjacency_matrix1, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(adjacency_matrix1, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(adjacency_matrix1, UP).shift(LEFT * 1.3),
            Text("B", color=BLACK, font_size=40).next_to(adjacency_matrix1, UP).shift(LEFT * 0.45),
            Text("C", color=BLACK, font_size=40).next_to(adjacency_matrix1, UP).shift(RIGHT * 0.4),
            Text("D", color=BLACK, font_size=40).next_to(adjacency_matrix1, UP).shift(RIGHT * 1.28),
        ).set_color(BLACK)

        T_0 = Tex("T_{0}",).next_to(adjacency_matrix1, UP).set_color(BLACK).shift(UP*1.13).scale(1.23)

        self.play(ShowCreation(adjacency_matrix1), ShowCreation(labels1), ShowCreation(T_0))

        self.wait(2)


        #M1 Goes here



        m1 = Matrix(
            [[Text("0").scale(0.55), Text("2").scale(0.55), Text("∞").scale(0.6), Text("3").scale(0.5)],  # A connected to B, D
             [Text("3").scale(0.6), Text("0").scale(0.55), Text("2").scale(0.55), Text("6").scale(0.55)],  # B connected to A, C
             [Text("∞").scale(0.6), Text("∞").scale(0.6), Text("0").scale(0.55), Text("4").scale(0.5)],  # C connected to B, D
             [Text("-2").scale(0.55), Text("0").scale(0.55), Text("∞").scale(0.6), Text("0").scale(0.55)]],  # D connected to A, C
        ).next_to(adjacency_matrix, DOWN).set_color(BLACK).shift(DOWN*1.45).scale(1.2)

        # Add labels to the matrix
        labels_m1 = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m1, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m1, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m1, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m1, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m1, UP).shift(LEFT * 1.55),
            Text("B", color=BLACK, font_size=40).next_to(m1, UP).shift(LEFT * 0.46999),
            Text("C", color=BLACK, font_size=40).next_to(m1, UP).shift(RIGHT * 0.5),
            Text("D", color=BLACK, font_size=40).next_to(m1, UP).shift(RIGHT * 1.6),
        ).set_color(BLACK)

        self.wait(2)


        m1_prev = Matrix(
            [[Text("-").scale(0.55), Text("A").scale(0.55), Text("-").scale(0.55), Text("A").scale(0.55)],  # A connected to B, D
             [Text("B").scale(0.55), Text("-").scale(0.55), Text("B").scale(0.55), Text("-").scale(0.55)],  # B connected to A, C
             [Text("-").scale(0.55), Text("-").scale(0.55), Text("-").scale(0.55), Text("C").scale(0.55)],  # C connected to B, D
             [Text("D").scale(0.55), Text("D").scale(0.55), Text("-").scale(0.55), Text("-").scale(0.55)]],  # D connected to A, C
        ).next_to(m1, RIGHT).set_color(BLACK).scale(1.2).shift(RIGHT*1.6)

        # Add labels to the matrix
        m1_prev_labels = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m1_prev, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m1_prev, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m1_prev, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m1_prev, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m1_prev, UP).shift(LEFT * 1.3),
            Text("B", color=BLACK, font_size=40).next_to(m1_prev, UP).shift(LEFT * 0.45),
            Text("C", color=BLACK, font_size=40).next_to(m1_prev, UP).shift(RIGHT * 0.4),
            Text("D", color=BLACK, font_size=40).next_to(m1_prev, UP).shift(RIGHT * 1.28),
        ).set_color(BLACK)



  


        self.play(Write(m1.get_brackets()), ShowCreation(labels_m1))
        self.wait(2)
        self.play(ShowCreation(m1_prev), ShowCreation(m1_prev_labels),)

        self.wait(2)
        self.play(nodes["A"][0].animate.set_color(PURPLE_E))
        self.wait(2)




        self.play(*[TransformFromCopy(adjacency_matrix[i],m1[j]) for i,j in zip([0,1,2,3,4,8,12], [0,1,2,3,4,8,12]) ])
        self.wait(2)
        self.play(*[TransformFromCopy(adjacency_matrix[i],m1[j]) for i,j in zip([5,10,15], [5,10,15]) ])

        self.wait(2)


        a = Circle(stroke_color="#0000FF", stroke_width=6).move_to(m1[6]).scale(0.4)
        self.play(ShowCreation(a))
        self.wait(2)

        self.play(a.animate.move_to(adjacency_matrix[6]))
        self.wait()
        
        text = Text("2 < 3 + ∞").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)

        self.play(TransformFromCopy(adjacency_matrix[6], text[0]))

        self.wait(1)

        self.play(a.animate.move_to(adjacency_matrix[4]))
        self.wait()
        self.play(edge_b_a.animate.set_color("#0000FF"))

        self.play(TransformFromCopy(adjacency_matrix[4], text[2]))
        self.wait(2)

        self.play(a.animate.move_to(adjacency_matrix[2]))
        self.wait(1)
        self.play(TransformFromCopy(adjacency_matrix[2], text[3:]))

        self.wait(1)

        self.play(FadeIn(text[1]))

        self.wait(2)

        self.play(a.animate.move_to(m1[6]))
        self.play(FadeIn(m1[6]))
        self.play(edge_b_a.animate.set_color(MAROON_C), FadeOut(text))
        self.wait(1)


        #next_update_B_D
        self.play(a.animate.move_to(m1[7]))
        self.wait(1)


        self.play(a.animate.move_to(adjacency_matrix[7]))
        self.wait()
        
        text = Text("∞ > 3 + 3").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)

        self.play(TransformFromCopy(adjacency_matrix[7], text[0]))

        self.wait(1)

        self.play(a.animate.move_to(adjacency_matrix[4]))
        self.play(edge_b_a.animate.set_color("#0000FF"))

        self.play(TransformFromCopy(adjacency_matrix[4], text[2]))
        self.wait(2)

        self.play(a.animate.move_to(adjacency_matrix[3]))
        self.wait()
        self.play(edge_list[-1].animate.set_color("#0000FF"))
        self.wait(1)
        self.play(TransformFromCopy(adjacency_matrix[3], text[3:]))

        self.wait(1)

        self.play(Transform(text[2:], Text("6").move_to(text[2]).set_color(BLACK)))


        self.play(FadeIn(text[1]))

        self.wait(2)

        self.play(a.animate.move_to(m1[7]))
        self.play(FadeIn(m1[7]))
        self.wait()


        self.play(a.animate.move_to(m1_prev[6]).shift(RIGHT*0.86))
        self.wait()
        self.play(Transform(m1_prev[7], Text("A").scale(0.66).set_color(BLACK).move_to(m1_prev[7]).shift(UP*0.15)))
        self.wait(1)




        self.play(edge_b_a.animate.set_color(MAROON_C), FadeOut(text), edge_list[-1].animate.set_color(MAROON_C))
        self.wait(1)


        #next 


        self.play(a.animate.move_to(m1[9]))
        self.wait(1)


        self.play(a.animate.move_to(adjacency_matrix[9]))
        self.wait()
        
        text = Text("∞ ≈ ∞ + 2").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)

        self.play(TransformFromCopy(adjacency_matrix[9], text[0]))

        self.wait(1)

        self.play(a.animate.move_to(adjacency_matrix[8]))

        self.play(TransformFromCopy(adjacency_matrix[8], text[2]))
        self.wait(2)

        self.play(a.animate.move_to(adjacency_matrix[1]))
        self.wait()
        self.play(edge_list[0].animate.set_color("#0000FF"))
        self.wait(1)
        self.play(TransformFromCopy(adjacency_matrix[1], text[3:]))

        self.wait(1)



        self.play(FadeIn(text[1]))

        self.wait(2)

        self.play(a.animate.move_to(m1[9]))
        self.play(FadeIn(m1[9]))
        self.play(edge_list[0].animate.set_color(MAROON_C), FadeOut(text),)
        self.wait(1)


        #done)here
        self.play(a.animate.move_to(m1[11]))
        self.wait(1.4)


        self.play(a.animate.move_to(adjacency_matrix[11]))
        self.wait()
        self.play(edge_list[3].animate.set_color("#0000FF"))
        self.wait(1.2)
        self.play(edge_list[3].animate.set_color(MAROON_C))
        self.wait()

        
        text = Text("4 < ∞ + 3").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)

        self.play(TransformFromCopy(adjacency_matrix[11], text[0]))

        self.wait(1)

        self.play(a.animate.move_to(adjacency_matrix[8]))

        self.play(TransformFromCopy(adjacency_matrix[8], text[2]))
        self.wait(2)

        self.play(a.animate.move_to(adjacency_matrix[3]))
        self.wait()
        self.play(edge_list[4].animate.set_color("#0000FF"))
        self.wait(1)
        self.play(TransformFromCopy(adjacency_matrix[3], text[3:]))

        self.wait(1)



        self.play(FadeIn(text[1]))

        self.wait(2)

        self.play(a.animate.move_to(m1[11]))
        self.play(FadeIn(m1[11]))
        self.play(edge_list[4].animate.set_color(MAROON_C), FadeOut(text),)
        self.wait(1)


        #DONE_DONE_DONE_DONE_DONE_DONE


        self.play(a.animate.move_to(m1[13]))
        self.wait(1.4)


        self.play(a.animate.move_to(adjacency_matrix[13]))
        self.wait()
        self.play(edge_list[1].animate.set_color("#0000FF"))
        self.wait(1.2)
        self.play(edge_list[1].animate.set_color(MAROON_C))
        self.wait(1.2)

        
        text = Text("6 > -2 + 2").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)
        self.play(TransformFromCopy(adjacency_matrix[13], text[0]))

        self.wait(1)
        self.play(a.animate.move_to(adjacency_matrix[12]))
        self.wait()
        self.play(edge_d_a.animate.set_color("#0000FF"))
        self.wait()



        self.play(TransformFromCopy(adjacency_matrix[12], text[2:4]))
        self.wait(2)

        self.play(a.animate.move_to(adjacency_matrix[1]))
        self.wait()
        self.play(edge_list[0].animate.set_color("#0000FF"))
        self.wait(1)
        self.play(TransformFromCopy(adjacency_matrix[1], text[4:]))

        self.wait(1)



        self.play(FadeIn(text[1]))

        self.wait(2)

        self.play(Transform(text[2:], Text("0").move_to(text[2]).set_color(BLACK)))


        self.play(a.animate.move_to(m1[13]))
        self.play(FadeIn(m1[13]))
        self.play(edge_list[0].animate.set_color(MAROON_C), FadeOut(text),edge_d_a.animate.set_color(MAROON_C))
        self.wait(1)



        self.play(a.animate.move_to(m1_prev[12]).shift(RIGHT*0.86))
        self.wait()
        self.play(Transform(m1_prev[13], Text("A").scale(0.66).set_color(BLACK).move_to(m1_prev[13])))
        self.wait(1)



        #DONE_DONE_FS



        self.play(a.animate.move_to(m1[14]))
        self.wait(1.4)


        self.play(a.animate.move_to(adjacency_matrix[14]))
        self.wait()




        
        text = Text("∞ ≈ -2 + ∞").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)

        self.play(TransformFromCopy(adjacency_matrix[14], text[0]))

        self.wait(1)

        self.play(a.animate.move_to(adjacency_matrix[12]))

        self.play(TransformFromCopy(adjacency_matrix[12], text[2:4]))
        self.wait(2)

        self.play(a.animate.move_to(adjacency_matrix[2]))
        self.wait()

        self.play(TransformFromCopy(adjacency_matrix[2], text[4:]))

        self.wait(1)



        self.play(FadeIn(text[1]))

        self.wait(2)

        self.play(a.animate.move_to(m1[14]))
        self.play(FadeIn(m1[14]))
        self.play(FadeOut(text))
        self.play(FadeOut(a))
        self.wait(1)






        #M1 DONE N

        T_1 = Tex("T_{1}",).move_to(T_0).scale(1.23).set_color(BLACK)
        M_1 = Tex("M_{1}",).move_to(M_0).scale(1.23).set_color(BLACK)


        self.play(FadeOut(adjacency_matrix), FadeOut(labels), FadeOut(adjacency_matrix1), FadeOut(labels1), FadeOut(M_0), FadeOut(T_0))

        self.wait(1.5)

        self.play(Group(m1, labels_m1, m1_prev, m1_prev_labels).animate.shift(UP*4.86))

        self.play(ShowCreation(M_1), ShowCreation(T_1))

        self.wait(2)

        self.play(nodes["A"][0].animate.set_color(BLACK))
        self.wait()
        self.play(nodes["B"][0].animate.set_color(PURPLE_E))
        self.wait()


        



        m2 = Matrix(
            [[Text("0").scale(0.55), Text("2").scale(0.55), Text("4").scale(0.6), Text("3").scale(0.5)],  # A connected to B, D
             [Text("3").scale(0.6), Text("0").scale(0.55), Text("2").scale(0.55), Text("6").scale(0.55)],  # B connected to A, C
             [Text("∞").scale(0.6), Text("∞").scale(0.6), Text("0").scale(0.55), Text("4").scale(0.5)],  # C connected to B, D
             [Text("-2").scale(0.55), Text("0").scale(0.55), Text("2").scale(0.6), Text("0").scale(0.55)]],  # D connected to A, C
        ).next_to(m1, DOWN).set_color(BLACK).shift(DOWN*1.45).scale(1.2)

        # Add labels to the matrix
        labels_m2 = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m2, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m2, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m2, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m2, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m2, UP).shift(LEFT * 1.55),
            Text("B", color=BLACK, font_size=40).next_to(m2, UP).shift(LEFT * 0.46999),
            Text("C", color=BLACK, font_size=40).next_to(m2, UP).shift(RIGHT * 0.5),
            Text("D", color=BLACK, font_size=40).next_to(m2, UP).shift(RIGHT * 1.6),
        ).set_color(BLACK)

        self.wait(2)


        m2_prev = Matrix(
            [[Text("-").scale(0.55), Text("A").scale(0.55), Text("-").scale(0.55), Text("A").scale(0.55)],  # A connected to B, D
             [Text("B").scale(0.55), Text("-").scale(0.55), Text("B").scale(0.55), Text("A").scale(0.55)],  # B connected to A, C
             [Text("-").scale(0.55), Text("-").scale(0.55), Text("-").scale(0.55), Text("C").scale(0.55)],  # C connected to B, D
             [Text("D").scale(0.55), Text("A").scale(0.55), Text("-").scale(0.55), Text("-").scale(0.55)]],  # D connected to A, C
        ).next_to(m2, RIGHT).set_color(BLACK).scale(1.2).shift(RIGHT*1.6)

        # Add labels to the matrix
        m2_prev_labels = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m2_prev, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m2_prev, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m2_prev, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m2_prev, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m2_prev, UP).shift(LEFT * 1.3),
            Text("B", color=BLACK, font_size=40).next_to(m2_prev, UP).shift(LEFT * 0.45),
            Text("C", color=BLACK, font_size=40).next_to(m2_prev, UP).shift(RIGHT * 0.4),
            Text("D", color=BLACK, font_size=40).next_to(m2_prev, UP).shift(RIGHT * 1.28),
        ).set_color(BLACK)



  


        self.play(Write(m2.get_brackets()), ShowCreation(labels_m2))
        self.wait(2)
        self.play(ShowCreation(m2_prev), ShowCreation(m2_prev_labels),)

        self.wait(2)




        self.play(*[TransformFromCopy(m1[i],m2[j]) for i,j in zip([4,5,6,7,1,9,13], [4,5,6,7,1,9,13]) ])
        self.wait(2)
        self.play(*[TransformFromCopy(m1[i],m2[j]) for i,j in zip([0,10,15], [0,10,15]) ])

        self.wait(2)


        a = Circle(stroke_color="#0000FF", stroke_width=6).move_to(m2[2]).scale(0.4)
        self.play(ShowCreation(a))
        self.wait(2)


        self.play(a.animate.move_to(m1[2]))
        self.wait(1)

        text = Text("∞ > 2 + 2").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)

        self.play(TransformFromCopy(m1[2], text[0]))

        self.wait(1)

        self.play(a.animate.move_to(m1[1]))
        self.wait()

        self.play(edge_list[0].animate.set_color("#0000FF"))
        self.wait()

        self.play(TransformFromCopy(m1[1], text[2]))
        self.wait(2)







        self.play(a.animate.move_to(m1[6]))
        self.play(edge_list[2].animate.set_color("#0000FF"))

        self.wait()

        self.play(TransformFromCopy(m1[6], text[3:]))

        self.wait()



        




        self.play(Transform(text[2:], Text("4").move_to(text[2]).set_color(BLACK)))

        self.play(FadeIn(text[1]))

        self.wait(1)

        self.play(a.animate.move_to(m2[2]))
        self.play(FadeIn(m2[2]))

        self.wait(1)

        self.play(a.animate.move_to(m2_prev[2]).shift(UP*0.056))
        self.wait()


        self.play(Transform(m2_prev[2], Text("B").scale(0.66).set_color(BLACK).move_to(m2_prev[2]).shift(UP*0.15)))


        self.wait(2)



        self.play(edge_list[0].animate.set_color(MAROON_C), edge_list[2].animate.set_color(MAROON_C), FadeOut(text))


        self.play(a.animate.move_to(m2[3]))

        self.wait(2)



        #DONE_DONE_DONE_DONE



        self.play(a.animate.move_to(m1[3]))
        self.wait()

        self.play(edge_list[-1].animate.set_color("#0000FF"))
        self.wait()
        self.play(edge_list[-1].animate.set_color(MAROON_C))

        self.wait(1)

        text = Text("3 < 2 + ∞").next_to(nodes["D"], DOWN, buff=1).set_color(BLACK).shift(DOWN*1.1).shift(RIGHT)

        self.play(TransformFromCopy(m1[3], text[0]))

        self.wait(1)

        self.play(a.animate.move_to(m1[1]))
        self.wait()

        self.play(edge_list[0].animate.set_color("#0000FF"))
        self.wait()

        self.play(TransformFromCopy(m1[1], text[2]))
        self.wait(2)







        self.play(a.animate.move_to(m1[7]))
        self.wait(1)
        self.play(edge_list[4].animate.set_color("#0000FF"),edge_b_a.animate.set_color("#0000FF"))

        self.wait()

        self.play(TransformFromCopy(m1[7], text[3:]))

        self.wait()



        




        self.play(Transform(text[2:], Text("8").move_to(text[2]).set_color(BLACK)))

        self.play(FadeIn(text[1]))

        self.wait(1)

        self.play(a.animate.move_to(m2[3]))
        self.play(FadeIn(m2[3]))

        self.wait(1)


        self.play(edge_list[0].animate.set_color(MAROON_C), edge_list[4].animate.set_color(MAROON_C),edge_b_a.animate.set_color(MAROON_C), FadeOut(text), FadeOut(a))


        self.wait(2)


        self.play(FadeIn(m2[8]), FadeIn(m2[11]), FadeIn(m2[12]), FadeIn(m2[14]))
        self.play(Transform(m2_prev[14], Text("B").scale(0.66).set_color(BLACK).move_to(m2_prev[14]).shift(UP*0.15)))




        self.wait(2)

        self.play(FadeOut(Group(m1, labels_m1, m1_prev, m1_prev_labels, M_1, T_1)))
        self.play(Group(m2, labels_m2, m2_prev, m2_prev_labels).animate.shift(UP*4.86))

        T_2 = Tex("T_{2}",).move_to(T_0).scale(1.23).set_color(BLACK)
        M_2 = Tex("M_{2}",).move_to(M_0).scale(1.23).set_color(BLACK)

        self.play(FadeIn(M_2), FadeIn(T_2))
        self.wait(1.999)

        self.play(nodes["C"][0].animate.set_color(PURPLE_E),nodes["B"][0].animate.set_color(BLACK))

        self.wait(1)



        m3 = Matrix(
            [[Text("0").scale(0.55), Text("2").scale(0.55), Text("4").scale(0.6), Text("3").scale(0.5)],  # A connected to B, D
             [Text("3").scale(0.6), Text("0").scale(0.55), Text("2").scale(0.55), Text("6").scale(0.55)],  # B connected to A, C
             [Text("∞").scale(0.6), Text("∞").scale(0.6), Text("0").scale(0.55), Text("4").scale(0.5)],  # C connected to B, D
             [Text("-2").scale(0.55), Text("0").scale(0.55), Text("2").scale(0.6), Text("0").scale(0.55)]],  # D connected to A, C
        ).next_to(m2, DOWN).set_color(BLACK).shift(DOWN*1.45).scale(1.2)

        # Add labels to the matrix
        labels_m3 = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m3, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m3, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m3, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m3, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m3, UP).shift(LEFT * 1.55),
            Text("B", color=BLACK, font_size=40).next_to(m3, UP).shift(LEFT * 0.46999),
            Text("C", color=BLACK, font_size=40).next_to(m3, UP).shift(RIGHT * 0.5),
            Text("D", color=BLACK, font_size=40).next_to(m3, UP).shift(RIGHT * 1.6),
        ).set_color(BLACK)

        self.wait(2)


        m3_prev = Matrix(
            [[Text("-").scale(0.55), Text("A").scale(0.55), Text("B").scale(0.55), Text("A").scale(0.55)],  # A connected to B, D
             [Text("B").scale(0.55), Text("-").scale(0.55), Text("B").scale(0.55), Text("A").scale(0.55)],  # B connected to A, C
             [Text("-").scale(0.55), Text("-").scale(0.55), Text("-").scale(0.55), Text("C").scale(0.55)],  # C connected to B, D
             [Text("D").scale(0.55), Text("A").scale(0.55), Text("B").scale(0.55), Text("-").scale(0.55)]],  # D connected to A, C
        ).next_to(m3, RIGHT).set_color(BLACK).scale(1.2).shift(RIGHT*1.6)

        # Add labels to the matrix
        m3_prev_labels = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m3_prev, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m3_prev, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m3_prev, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m3_prev, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m3_prev, UP).shift(LEFT * 1.3),
            Text("B", color=BLACK, font_size=40).next_to(m3_prev, UP).shift(LEFT * 0.45),
            Text("C", color=BLACK, font_size=40).next_to(m3_prev, UP).shift(RIGHT * 0.4),
            Text("D", color=BLACK, font_size=40).next_to(m3_prev, UP).shift(RIGHT * 1.28),
        ).set_color(BLACK)



  


        self.play(Write(m3), ShowCreation(labels_m3))
        self.wait(2)
        self.play(ShowCreation(m3_prev), ShowCreation(m3_prev_labels),)

        self.wait(2)


        #Done till node C

        self.play(FadeOut(Group(m2, labels_m2, m2_prev, m2_prev_labels, M_2, T_2)))
        self.play(Group(m3, labels_m3, m3_prev, m3_prev_labels).animate.shift(UP*4.86))

        T_3 = Tex("T_{3}",).move_to(T_2).scale(1.23).set_color(BLACK)
        M_3 = Tex("M_{3}",).move_to(M_2).scale(1.23).set_color(BLACK)

        self.play(FadeIn(M_3), FadeIn(T_3))
        self.wait(1.999)

        self.play(nodes["C"][0].animate.set_color(BLACK),nodes["D"][0].animate.set_color(PURPLE_E))

        self.wait(1)



        m4 = Matrix(
            [[Text("0").scale(0.55), Text("2").scale(0.55), Text("4").scale(0.6), Text("3").scale(0.5)],  # A connected to B, D
             [Text("3").scale(0.6), Text("0").scale(0.55), Text("2").scale(0.55), Text("6").scale(0.55)],  # B connected to A, C
             [Text("2").scale(0.6), Text("4").scale(0.6), Text("0").scale(0.55), Text("4").scale(0.5)],  # C connected to B, D
             [Text("-2").scale(0.55), Text("0").scale(0.55), Text("2").scale(0.6), Text("0").scale(0.55)]],  # D connected to A, C
        ).next_to(m3, DOWN).set_color(BLACK).shift(DOWN*1.45).scale(1.2)

        # Add labels to the matrix
        labels_m4 = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m4, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m4, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m4, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m4, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m4, UP).shift(LEFT * 1.55),
            Text("B", color=BLACK, font_size=40).next_to(m4, UP).shift(LEFT * 0.46999),
            Text("C", color=BLACK, font_size=40).next_to(m4, UP).shift(RIGHT * 0.5),
            Text("D", color=BLACK, font_size=40).next_to(m4, UP).shift(RIGHT * 1.6),
        ).set_color(BLACK)

        self.wait(2)


        m4_prev = Matrix(
            [[Text("-").scale(0.55), Text("A").scale(0.55), Text("B").scale(0.55), Text("A").scale(0.55)],  # A connected to B, D
             [Text("B").scale(0.55), Text("-").scale(0.55), Text("B").scale(0.55), Text("A").scale(0.55)],  # B connected to A, C
             [Text("D").scale(0.55), Text("A").scale(0.55), Text("-").scale(0.55), Text("C").scale(0.55)],  # C connected to B, D
             [Text("D").scale(0.55), Text("A").scale(0.55), Text("B").scale(0.55), Text("-").scale(0.55)]],  # D connected to A, C
        ).next_to(m4, RIGHT).set_color(BLACK).scale(1.2).shift(RIGHT*1.6)

        # Add labels to the matrix
        m4_prev_labels = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(m4_prev, LEFT).shift(UP * 1.36),
            Text("B", color=BLACK, font_size=40).next_to(m4_prev, LEFT).shift(UP * 0.4),
            Text("C", color=BLACK, font_size=40).next_to(m4_prev, LEFT).shift(DOWN * 0.52),
            Text("D", color=BLACK, font_size=40).next_to(m4_prev, LEFT).shift(DOWN * 1.33),
            Text("A", color=BLACK, font_size=40).next_to(m4_prev, UP).shift(LEFT * 1.3),
            Text("B", color=BLACK, font_size=40).next_to(m4_prev, UP).shift(LEFT * 0.45),
            Text("C", color=BLACK, font_size=40).next_to(m4_prev, UP).shift(RIGHT * 0.4),
            Text("D", color=BLACK, font_size=40).next_to(m4_prev, UP).shift(RIGHT * 1.28),
        ).set_color(BLACK)



  


        self.play(Write(m4), ShowCreation(labels_m4))
        self.wait(2)
        self.play(ShowCreation(m4_prev), ShowCreation(m4_prev_labels),)

        self.wait(2)

        self.play(FadeOut(m3), FadeOut(m3_prev), FadeOut(labels_m3), FadeOut(m3_prev_labels), FadeOut(M_3), FadeOut(T_3))

        self.play(Group(m4, labels_m4, m4_prev, m4_prev_labels).animate.shift(UP*4.45))


        T_4 = Tex("T_{4}",).move_to(T_2).scale(1.23).set_color(BLACK).shift(DOWN*0.25)
        M_4 = Tex("M_{4}",).move_to(M_2).scale(1.23).set_color(BLACK).shift(DOWN*0.25)

        self.play(FadeIn(M_4), FadeIn(T_4))
        self.wait(1.999)

        self.play(nodes["D"][0].animate.set_color(BLACK))

        self.wait(2)

        self.play(nodes["C"][0].animate.set_color(GREEN_E), nodes["C"][1].animate.set_color(BLACK))

        self.wait()

        c = nodes["C"][1].copy()

        self.play(c.animate.scale(1.5).shift(DOWN*3+LEFT*3.3))

        self.wait(2)

        self.play(nodes["B"][0].animate.set_color(GREEN_E), nodes["B"][1].animate.set_color(BLACK))
        self.wait()

        b = nodes["B"][1].copy()

        self.play(b.animate.scale(1.5).next_to(c, RIGHT, buff=11.6))

        self.wait(2)

        a = Circle(stroke_color="#0000FF", stroke_width=6).move_to(m4[9]).scale(0.4)

        self.play(ShowCreation(a))

        self.wait(2)

        self.play(a.animate.move_to(m4_prev[9]))

        self.wait(1)

        aa = nodes["A"][1].copy().set_color(BLACK)

        self.play(aa.animate.scale(1.5).next_to(b, LEFT, buff=3.77))
        self.wait(1)

        self.play(a.animate.move_to(m4_prev[8]))
        self.wait(2)

        d = nodes["D"][1].copy().set_color(BLACK)

        self.play(d.animate.scale(1.5).next_to(aa, LEFT, buff=3.77))
        self.wait(1)


        arrow = Arrow(c.get_right(), d.get_left()).set_color(BLACK)
        arrow1 = Arrow(d.get_right(), aa.get_left()).set_color(BLACK)

        arrow2 = Arrow(aa.get_right(), b.get_left()).set_color(BLACK)



        self.play(ShowCreation(arrow), ShowCreation(arrow1), ShowCreation(arrow2))

        self.wait(2)

        rect = SurroundingRectangle(Group(c,d,b), color="#0000FF").scale(1.22)

        self.play(ShowCreation(rect), FadeOut(a))


        self.wait(2)







        



        




























        
        





        self.embed()



    def create_nodes(self, node_positions):
        """Create nodes at specified positions with labels."""
        nodes = {}
        for label, position in node_positions.items():
            node_circle = Circle(
                radius=0.5,
                fill_color=TEAL,
                fill_opacity=1,
                color=MAROON_C,
                stroke_width=10
            ).set_color(GREY_E)
            node_circle.move_to(position)

            node_label = Text(label, ).move_to(position).set_color(WHITE).set_z_index(2)

            node_group = VGroup(node_circle, node_label)
            nodes[label] = node_group

        return nodes



    def create_edges(self, node_positions):
        """Create undirected edges between nodes."""
        edge_list = []
        edge_pairs = [
            ("A", "B"),
            ("B", "D"),
            ("B", "C"),
            ("C", "D"),
            
        ]

        for node1, node2 in edge_pairs:
            start_pos = node_positions[node1]
            end_pos = node_positions[node2]
            edge_line = Line(start_pos, end_pos, color=DARK_BLUE, stroke_width=5).set_z_index(-1)
            edge_list.append(edge_line)

        return edge_list



    def create_directed_edges(self, node_positions):
        """Transform undirected edges into directed edges."""
        directed_edge_list = []

        edge_pairs = [
            ("A", "B"),
            ("D", "B"),
            ("B", "C"),
            ("C", "D"),
            ("A", "D"),


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

    def create_edge_weights(self, node_positions):
        """Create weights for each edge and place them at the center of the edge, adjusting for orientation."""
        weights = {}
        edge_pairs = [
            ("A", "B", "2"),
            ("B", "C", "2"),
            ("B", "D", "6"),
            ("A", "D", "3"),
            ("D", "C", "4"),

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

            # Adjust the weight's position based on the edge's orientation
            if abs(direction_unit[0]) > abs(direction_unit[1]):  # More horizontal
                weight_offset = UP * 0.2  # Shift up for horizontal edges
            else:  # More vertical
                weight_offset = RIGHT * 0.2  # Shift right for vertical edges

            # For sloped edges, slightly shift the weight in the direction perpendicular to the edge
            perpendicular_unit = np.array([-direction_unit[1], direction_unit[0], 0]) * 0.2

            # Create the weight label and apply the calculated offset
            weight_label = Text(weight, color=BLACK).move_to(edge_center + perpendicular_unit).scale(0.6).set_color(BLACK)

            # Store the weight
            weights[f"weight_{node1}_{node2}"] = weight_label

        return weights
    

