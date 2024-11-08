from manim import *

config.background_color = WHITE


class SimpleGraph(MovingCameraScene):
    def construct(self):
        self.camera.frame.shift(UP * 0.23)
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
        edge_list = self.create_edges(node_positions)

        # Add nodes and edges to the scene
        self.play(*[GrowFromCenter(node) for node in nodes.values()])
        self.play(*[GrowFromCenter(edge) for edge in edge_list])

        self.wait(2)

        # # Transform undirected edges to directed edges
        # directed_edges, directed_edge_list = self.create_directed_edges(node_positions)
        # self.play(*[ReplacementTransform(edge_list[i], directed_edge_list[i]) for i in range(len(edge_list))])
        # self.wait(2)

        self.play(self.camera.frame.animate.scale(1.12).shift(RIGHT * 2.4))

        self.wait(2)

        # Create a 4x4 adjacency matrix for nodes A, B, C, D
        # Let's assume edges: A-B, A-D, B-C, C-D (example)
        adjacency_matrix = Matrix(
            [[0, 1, 0, 0],  # A connected to B, D
             [1, 0, 1, 1],  # B connected to A, C
             [0, 1, 0, 1],  # C connected to B, D
             [0, 1, 1, 0]],  # D connected to A, C
            element_to_mobject_config={"color": BLACK},  # Set the color of the matrix elements
            left_bracket="[", right_bracket="]", h_buff=0.9
        ).next_to(nodes["B"], RIGHT).set_color(BLACK).shift(DOWN * 2.2).shift(RIGHT)

        # Add labels to the matrix
        labels = VGroup(
            Text("A", color=BLACK, font_size=30).next_to(adjacency_matrix, LEFT).shift(UP * 1.2),
            Text("B", color=BLACK, font_size=30).next_to(adjacency_matrix, LEFT).shift(UP * 0.356),
            Text("C", color=BLACK, font_size=30).next_to(adjacency_matrix, LEFT).shift(DOWN * 0.4),
            Text("D", color=BLACK, font_size=30).next_to(adjacency_matrix, LEFT).shift(DOWN * 1.25),
            Text("A", color=BLACK, font_size=30).next_to(adjacency_matrix, UP).shift(LEFT * 1.33),
            Text("B", color=BLACK, font_size=30).next_to(adjacency_matrix, UP).shift(LEFT * 0.46),
            Text("C", color=BLACK, font_size=30).next_to(adjacency_matrix, UP).shift(RIGHT * 0.43),
            Text("D", color=BLACK, font_size=30).next_to(adjacency_matrix, UP).shift(RIGHT * 1.37),
        )

        # Display the matrix and labels
        self.play(TransformFromCopy(VGroup(nodes["A"][1], nodes["B"][1], nodes["C"][1], nodes["D"][1]), labels[:4])
                  , TransformFromCopy(VGroup(nodes["A"][1], nodes["B"][1], nodes["C"][1], nodes["D"][1]), labels[4:]))
        self.wait()
        self.play(Write(adjacency_matrix.get_brackets()), )
        self.wait(2)

        # Get individual matrix elements
        matrix_entries = adjacency_matrix.get_entries()

        # Create a surrounding rectangle around the first element (top-left, row 1, col 1)
        first_element_rect = SurroundingCircle(matrix_entries[0], color=BLUE, buff=0.2)
        self.play(Create(first_element_rect))

        # Animate the creation of the first matrix element (top-left corner)
        self.play(Create(matrix_entries[0]))

        self.wait(1)

        # Create surrounding rectangles and animate the diagonal elements one by one
        diagonal_indices = [5, 10,
                            15]  # These are the diagonal elements' indices (row 2 col 2, row 3 col 3, row 4 col 4)

        for index in diagonal_indices:
            rect = SurroundingCircle(matrix_entries[index], color=BLUE, buff=0.2)
            self.play(ReplacementTransform(first_element_rect, rect))  # Move the rectangle to the next diagonal element
            self.play(Create(matrix_entries[index]))  # Create the diagonal element
            first_element_rect = rect  # Update the rectangle to stay on the current diagonal element

        self.wait(2)

        self.play(first_element_rect.animate.move_to(matrix_entries[1]))

        for i in range(1, 5):
            self.play(first_element_rect.animate.move_to(matrix_entries[i]))
            self.wait(2)
            self.play(Create(matrix_entries[i]))
        self.wait(2)

        for i in range(6, 10):
            self.play(first_element_rect.animate.move_to(matrix_entries[i]))
            self.play(Create(matrix_entries[i]))

        for i in range(11, 15):
            self.play(first_element_rect.animate.move_to(matrix_entries[i]))
            self.play(Create(matrix_entries[i]))

        self.play(Uncreate(first_element_rect))

        self.wait(2)

        # Transform undirected edges to directed edges
        directed_edges, directed_edge_list = self.create_directed_edges(node_positions)
        self.play(*[ReplacementTransform(edge_list[i], directed_edge_list[i]) for i in range(len(edge_list))])
        self.play(FadeOut(matrix_entries))
        self.wait(2)

        # Let's assume edges: A-B, A-D, B-C, C-D (example)
        adjacency_matrix1 = Matrix(
            [[0, 1, 0, 0],  # A connected to B, D
             [0, 0, 1, 1],  # B connected to A, C
             [0, 0, 0, 1],  # C connected to B, D
             [0, 0, 0, 0]],  # D connected to A, C
            element_to_mobject_config={"color": BLACK},  # Set the color of the matrix elements
            left_bracket="[", right_bracket="]", h_buff=0.9
        ).next_to(nodes["B"], RIGHT).set_color(BLACK).shift(DOWN * 2.2).shift(RIGHT)

        matrix_entries = adjacency_matrix1.get_entries()

        first_element_rect = SurroundingCircle(matrix_entries[1], color=BLUE, buff=0.2)

        # Create surrounding rectangles and animate the diagonal elements one by one
        diagonal_indices = [0, 5, 10,
                            15]  # These are the diagonal elements' indices (row 2 col 2, row 3 col 3, row 4 col 4)

        self.play(*[Create(matrix_entries[i]) for i in diagonal_indices])

        self.wait(2)

        self.play(Create(first_element_rect))

        for i in range(1, 5):
            self.play(first_element_rect.animate.move_to(matrix_entries[i]))
            self.play(FadeIn(matrix_entries[i]))
            if i == 4:
                self.wait(4)

        self.wait()

        for i in range(6, 10):
            self.play(first_element_rect.animate.move_to(matrix_entries[i]))
            self.play(FadeIn(matrix_entries[i]))

        for i in range(11, 15):
            self.play(first_element_rect.animate.move_to(matrix_entries[i]))
            self.play(FadeIn(matrix_entries[i]))

        self.play(Uncreate(first_element_rect))

        self.wait(2)

        # Add weights to the directed edges
        weights = self.create_edge_weights(node_positions)
        self.play(*[Write(weight) for weight in weights.values()])
        self.wait(2)

        self.play(
            *[Transform(matrix_entries[i], Text("*", color=BLACK).move_to(matrix_entries[i])) for i, entry in
              enumerate(matrix_entries) if i not in [1, 6, 7, 11]]
        )

        self.wait(2)

        # Define the new values for the specific indices
        new_values = {1: "3", 6: "4", 7: "7", 11: "5"}

        # Play the replacement for each specified index
        self.play(
            *[FadeOut(matrix_entries[i]) for i
              in new_values]
        )

        self.wait(2)

        # Accessing the weight for the edge between A and B
        weight_A_B = weights["weight_A_B"]
        weight_B_C = weights["weight_B_C"]
        weight_B_D = weights["weight_B_D"]
        weight_C_D = weights["weight_C_D"]

        w1 = weight_A_B.copy()
        w2 = weight_B_C.copy()
        w3 = weight_B_D.copy()
        w4 = weight_C_D.copy()

        # Play the replacement for each specified index
        self.play(
            w1.animate.move_to(matrix_entries[1].get_center()),
            w2.animate.move_to(matrix_entries[6].get_center()),
            w3.animate.move_to(matrix_entries[7].get_center()),
            w4.animate.move_to(matrix_entries[11].get_center()),
        )

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT))

        # Create the curly brace on the right side of the matrix
        brace_right = Brace(adjacency_matrix, direction=RIGHT, color=BLACK)

        # Create the curly brace at the bottom of the matrix
        brace_bottom = Brace(adjacency_matrix, direction=DOWN, color=BLACK)

        # Add labels "n" to both braces
        label_right = brace_right.get_text("n").set_color(BLACK)
        label_bottom = brace_bottom.get_text("n").set_color(BLACK)

        # Display the braces and labels
        self.play(GrowFromCenter(brace_right), GrowFromCenter(brace_bottom))
        self.play(FadeIn(label_right), FadeIn(label_bottom))

        self.wait(2)

        # Create the O(n^2) expression using MathTex
        big_o_n_squared = MathTex("O(n^2)", color=BLACK).next_to(adjacency_matrix1.get_right(), RIGHT).shift(
            RIGHT * 0.3)

        # Apply ReplacementTransform to transform the braces and labels into O(n^2)
        self.play(
            ReplacementTransform(VGroup(label_bottom, label_right, brace_right, brace_bottom), big_o_n_squared)
        )

        self.wait(2)

        self.play(Uncreate(big_o_n_squared))

        self.wait()
        self.play(self.camera.frame.animate.shift(LEFT))

        self.wait(2)

        a = SurroundingCircle(matrix_entries[4], color=PURE_BLUE)
        self.play(Create(a))

        for i in range(4, 8):
            self.play(a.animate.move_to(matrix_entries[i]))

        self.wait(2)

        edge0 = Arrow(start=nodes["A"].get_center(), end=nodes["D"].get_top() + DOWN * 0.23,
                      color=DARK_BLUE, stroke_width=5.5).set_z_index(-1)
        weight0 = Text("2", color=BLACK, font_size=30).next_to(edge0.get_center(), RIGHT * 0.33)

        self.play(FadeOut(a))

        a = SurroundingCircle(matrix_entries[3], color=PURE_BLUE)

        self.play(Create(edge0), Create(weight0))

        self.play(Create(a))
        self.wait()

        self.play(Transform(
            matrix_entries[3], Text("2", color=BLACK, font_size=30).move_to(matrix_entries[3])

        ))

        self.wait()

        self.play(Uncreate(a))

        self.wait(2)

        self.play(Uncreate(weight_A_B, ), Uncreate(directed_edge_list[0]))

        a = SurroundingCircle(matrix_entries[1], color=PURE_BLUE)

        self.play(Create(a))

        self.wait(1)

        self.play(Transform(w1, Text("*", font_size=40, color=BLACK).move_to(w1)))
        self.wait()

        self.play(Uncreate(a))

        self.play(Uncreate(directed_edge_list[1]), Uncreate(directed_edge_list[2]))
        self.play(FadeOut(nodes["B"], weight_B_C, weight_B_D))

        self.wait(2)

        self.play(*[matrix_entries[i].animate.set_opacity(0.24) for i in range(4, 6)],
                  VGroup(w2, w3).animate.set_opacity(0.24))
        self.play(*[matrix_entries[i].animate.set_opacity(0.24) for i in [9, 13]], w1.animate.set_opacity(0.24))

        matrix_entries[6] = w2
        matrix_entries[7] = w3
        matrix_entries[11] = w4
        matrix_entries[1] = w1

        self.play(FadeOut(adjacency_matrix.get_brackets()), run_time=0.00001)

        a = VGroup(matrix_entries, adjacency_matrix1.get_brackets(), labels)
        self.play(a.animate.scale(0.67).shift(UP * 1.77))

        self.wait(2)

        adjacency_matrix = Matrix(
            [['*', '*', 2],  # A connected to B, D
             ['*', '*', 5],  # B connected to A, C
             ['*', '*', '*'],  # C connected to B, D
             ],  # D connected to A, C
            element_to_mobject_config={"color": BLACK},  # Set the color of the matrix elements
            left_bracket="[", right_bracket="]", h_buff=0.9
        ).next_to(adjacency_matrix1, DOWN).set_color(BLACK).scale(0.87).shift(DOWN * 0.4239)

        labels2 = VGroup(
            Text("A", color=BLACK, font_size=20).next_to(adjacency_matrix, LEFT).shift(UP * 0.63),
            Text("C", color=BLACK, font_size=20).next_to(adjacency_matrix, LEFT).shift(DOWN * 0.1),
            Text("D", color=BLACK, font_size=20).next_to(adjacency_matrix, LEFT).shift(DOWN * 0.75),
            Text("A", color=BLACK, font_size=20).next_to(adjacency_matrix, UP).shift(LEFT * 0.95),
            Text("C", color=BLACK, font_size=20).next_to(adjacency_matrix, UP).shift(LEFT * 0.06),
            Text("D", color=BLACK, font_size=20).next_to(adjacency_matrix, UP).shift(RIGHT * 0.83),
        )

        matrix_entries1 = adjacency_matrix.get_entries()

        self.play(Create(adjacency_matrix.get_brackets()), Create(labels2))
        self.wait(1)

        self.play(*[TransformFromCopy(matrix_entries[i], matrix_entries1[j]) for i, j in
                    zip([0, 2, 3, 8, 10, 11, 12, 14, 15], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])], run_time=2)

        self.wait(2)

        self.play(FadeOut(a))

        self.play(VGroup(adjacency_matrix, labels2).animate.shift(UP * 1.1).scale(1.3))

        self.wait(2)

        node_circle = Circle(
            radius=0.5,
            fill_color=TEAL_B,
            fill_opacity=1,
            color=DARK_BLUE,
            stroke_width=5.6
        )
        node_circle.move_to(nodes["B"])

        node_label = Text("E", color=BLACK).move_to(node_circle)

        node_group = VGroup(node_circle, node_label)



        self.play(Create(node_group))

        self.wait(3)

        self.play(VGroup(adjacency_matrix, labels2).animate.shift(DOWN * 1.1).scale(1 / 1.4))

        self.wait(1)

        # Update the text of each label directly
        labels[0].become(Text("A", color=BLACK, font_size=20).move_to(labels[0].get_center()))
        labels[1].become(Text("C", color=BLACK, font_size=20).move_to(labels[1].get_center()))
        labels[2].become(Text("D", color=BLACK, font_size=20).move_to(labels[2].get_center()))
        labels[3].become(Text("E", color=BLACK, font_size=20).move_to(labels[3].get_center()))
        labels[4].become(Text("A", color=BLACK, font_size=20).move_to(labels[4].get_center()))
        labels[5].become(Text("C", color=BLACK, font_size=20).move_to(labels[5].get_center()))
        labels[6].become(Text("D", color=BLACK, font_size=20).move_to(labels[6].get_center()))
        labels[7].become(Text("E", color=BLACK, font_size=20).move_to(labels[7].get_center()))

        self.play(Create(adjacency_matrix1.get_brackets(), ), Create(labels))

        # Define the desired values in a list, using "*" where the value should be an asterisk
        values = ["*", "*", "2", "*", "*", "*", "5", "*", "*", "*", "*", "*", "*", "*", "*", "*"]

        a = VGroup()

        for i in range(16):
            b = Text(f"{values[i]}", color=BLACK, font_size=20).move_to(matrix_entries[i])
            a.add(b)

        self.play(*[TransformFromCopy(matrix_entries1[i], a[j]) for i, j in
                    zip([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 4, 5, 6, 8, 9, 10])], run_time=2)
        self.wait(2)

        self.play(*[FadeIn(a[i]) for i in [3,7,11,15,12,13,14]])

        self.wait(2)

        self.play(FadeOut(adjacency_matrix, labels2))
        self.play(VGroup(adjacency_matrix1.get_brackets(), a, labels).animate.scale(1.1).shift(DOWN*1.56))




        self.wait(2)



    def create_nodes(self, node_positions):
        """Create nodes at specified positions with labels."""
        nodes = {}
        for label, position in node_positions.items():
            node_circle = Circle(
                radius=0.5,
                fill_color=TEAL_B,
                fill_opacity=1,
                color=DARK_BLUE,
                stroke_width=5.6
            )
            node_circle.move_to(position)

            node_label = Text(label, color=BLACK).move_to(position)

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
            ("B", "D"),
            ("B", "C"),
            ("C", "D"),

        ]

        for node1, node2 in edge_pairs:
            start_pos = node_positions[node1]
            end_pos = node_positions[node2]
            directed_edge = Arrow(
                start_pos, end_pos,
                buff=0.5,  # Adjusted buff to ensure arrow touches the circle but does not penetrate
                color=DARK_BLUE,
                stroke_width=5
            )
            directed_edge.z_index = -1  # Set z-index lower than nodes
            directed_edge_list.append(directed_edge)

        return {}, directed_edge_list

    def create_edge_weights(self, node_positions):
        """Create weights for each edge and place them at the center of the edge, adjusting for orientation."""
        weights = {}
        edge_pairs = [
            ("A", "B", "3"),
            ("B", "C", "4"),
            ("B", "D", "7"),
            ("C", "D", "5"),

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
            weight_label = Text(weight, color=BLACK).move_to(edge_center + perpendicular_unit).scale(0.6)

            # Store the weight
            weights[f"weight_{node1}_{node2}"] = weight_label

        return weights


class SurroundingCircle(Circle):
    def __init__(self, mobject, color=BLUE, buff=0.2, **kwargs):
        # Calculate the radius based on the object's width and height
        radius = max(mobject.width, mobject.height) / 2 + buff
        super().__init__(radius=radius, color=color, **kwargs)
        self.move_to(mobject.get_center())
