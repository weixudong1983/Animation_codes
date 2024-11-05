from manim import *

config.background_color = WHITE


class List(MovingCameraScene):
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

        # Add labels to the matrix
        labels = VGroup(
            Text("A", color=BLACK, font_size=40).next_to(nodes["B"], RIGHT).shift(UP * 2.1).shift(DOWN * 2).shift(
                RIGHT * 0.7),
            Text("B", color=BLACK, font_size=40).next_to(nodes["B"], RIGHT).shift(UP * 0.756).shift(DOWN * 2).shift(
                RIGHT * 0.7),
            Text("C", color=BLACK, font_size=40).next_to(nodes["B"], RIGHT).shift(DOWN * 0.8).shift(DOWN * 2).shift(
                RIGHT * 0.7),
            Text("D", color=BLACK, font_size=40).next_to(nodes["B"], RIGHT).shift(DOWN * 2.1).shift(DOWN * 2).shift(
                RIGHT * 0.7),

        )

        # Display the matrix and labels
        self.play(TransformFromCopy(VGroup(nodes["A"][1], nodes["B"][1], nodes["C"][1], nodes["D"][1]), labels[:4])
                  )
        self.wait()

        a = Text(": [ B ]", color=BLACK, font_size=40).next_to(labels[0])
        b = Text(": [ A, C, D ]", color=BLACK, font_size=40).next_to(labels[1])
        c = Text(": [ B, D ]", color=BLACK, font_size=40).next_to(labels[2])
        d = Text(": [ B ]", color=BLACK, font_size=40).next_to(labels[3])

        z = Circle(color=PURE_RED, stroke_width=5, radius=0.5).move_to(nodes["A"], )

        self.wait(2)

        self.play(Create(z))
        self.wait()

        self.play(Create(a))
        self.wait(2)

        self.play(z.animate.move_to(nodes["B"]))
        self.wait()

        self.play(Create(b))
        self.wait(2)

        self.play(z.animate.move_to(nodes["C"]))
        self.wait()

        self.play(Create(c))
        self.wait(1)

        self.play(z.animate.move_to(nodes["D"]))

        self.play(Create(d))

        self.wait(2)
        self.play(Uncreate(z))

        # Transform undirected edges to directed edges
        directed_edges, directed_edge_list = self.create_directed_edges(node_positions)
        self.play(*[ReplacementTransform(edge_list[i], directed_edge_list[i]) for i in range(len(edge_list))])
        self.play(FadeOut(a, b, c, d, ))
        self.wait(2)

        z = Circle(color=PURE_RED, stroke_width=5, radius=0.5).move_to(nodes["A"], )

        a = Text(": [ B ]", color=BLACK, font_size=40).next_to(labels[0])
        b = Text(": [ C, D ]", color=BLACK, font_size=40).next_to(labels[1])
        c = Text(": [ D ]", color=BLACK, font_size=40).next_to(labels[2])
        d = Text(": [ ]", color=BLACK, font_size=40).next_to(labels[3])

        self.play(Create(z))

        self.play(Create(a))
        self.wait(2)

        self.play(z.animate.move_to(nodes["B"]))
        self.wait()

        self.play(Create(b))
        self.wait(2)

        self.play(z.animate.move_to(nodes["C"]))
        self.wait()

        self.play(Create(c))
        self.wait(1)

        self.play(z.animate.move_to(nodes["D"]))
        self.wait()

        self.play(Create(d))

        self.wait(2)
        self.play(Uncreate(z))

        # Add weights to the directed edges
        weights = self.create_edge_weights(node_positions)
        self.play(*[Write(weight) for weight in weights.values()])
        self.wait(2)

        self.play(FadeOut(a, b, c, d, ))
        self.wait(2)

        a = Text(": [ (B, 3) ]", color=BLACK, font_size=40).next_to(labels[0])
        b = Text(": [ (C, 4), (D, 7) ]", color=BLACK, font_size=40).next_to(labels[1])
        c = Text(": [ (D, 5) ]", color=BLACK, font_size=40).next_to(labels[2])
        d = Text(": [ ]", color=BLACK, font_size=40).next_to(labels[3])

        z = Circle(color=PURE_RED, stroke_width=5, radius=0.5).move_to(nodes["A"], )

        self.play(Create(z))
        self.wait()

        self.play(Create(a))
        self.wait(2)

        self.play(z.animate.move_to(nodes["B"]))
        self.wait()

        self.play(Create(b))
        self.wait()
        self.wait(2)

        self.play(z.animate.move_to(nodes["C"]))
        self.wait()

        self.play(Create(c))
        self.wait(1)

        self.play(z.animate.move_to(nodes["D"]))
        self.wait()

        self.play(Create(d))

        self.wait(2)

        self.play(Uncreate(z))

        self.play(self.camera.frame.animate.shift(UP * 0.6))
        self.wait()

        # Create the O(n^2) expression using MathTex
        big_o_n_squared = MathTex("O(n + e)", color=BLACK).to_edge(UP).scale(1.6).shift(RIGHT * 2)

        self.play(Create(big_o_n_squared))

        self.wait(2)

        self.play(big_o_n_squared.animate.become(MathTex("O(n + n^2)", color=BLACK).to_edge(UP).scale(1.6).shift(RIGHT * 2)))

        self.wait(1)

        self.play(big_o_n_squared.animate.become(MathTex("O(n^2)", color=BLACK).to_edge(UP).scale(1.6).shift(RIGHT * 2)))



        self.wait(2)

        self.play(Uncreate(big_o_n_squared))
        self.play(self.camera.frame.animate.shift(DOWN * 0.6))

        self.wait(2)

        edge0 = Arrow(start=nodes["A"].get_center(), end=nodes["D"].get_top() + DOWN * 0.23,
                      color=DARK_BLUE, stroke_width=5.5).set_z_index(-1)

        weight0 = Text("2", color=BLACK, font_size=30).next_to(edge0.get_center(), RIGHT * 0.33)

        self.play(Create(edge0), Create(weight0))

        self.wait(2)

        aa = Text(" ,(D, 2)", color=BLACK, font_size=40).next_to(a[6], RIGHT, buff=0.17)

        self.play(a[7].animate.shift(RIGHT * 1.55))

        self.play(Write(aa))

        self.wait(2)

        self.play(Uncreate(edge0), Uncreate(weight0))

        pointer = Arrow(start=a.get_top() + UP, end=a.get_top(), color=PURE_BLUE).shift(LEFT)

        self.play(Create(pointer))

        self.wait(1)

        self.play(pointer.animate.shift(RIGHT * 2))

        self.wait()

        self.play(Uncreate(aa))

        self.play(a[7].animate.shift(LEFT * 1.55))
        self.wait()

        self.play(Uncreate(pointer))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.2).shift(UP * 0.3))

        comp = MathTex(r"O(\text{out-degree of the connected node})", color=BLACK).to_edge(UP).scale(1.6).shift(
            RIGHT * 2)

        self.play(Create(comp))

        self.wait(2)

        self.play(Uncreate(comp), self.camera.frame.animate.scale(1 / 1.2).shift(DOWN * 0.3))

        # Create the edges
        edge_list = self.create_edges(node_positions)

        self.play(*[ReplacementTransform(directed_edge_list[i], edge_list[i]) for i in range(len(edge_list))])
        self.play(FadeOut(weights["weight_A_B"], weights["weight_B_D"], weights["weight_B_C"], weights["weight_C_D"]))

        self.play(FadeOut(a, b, c, d))

        a = Text(": [ B ]", color=BLACK, font_size=40).next_to(labels[0])
        b = Text(": [ A, C, D ]", color=BLACK, font_size=40).next_to(labels[1])
        c = Text(": [ B, D ]", color=BLACK, font_size=40).next_to(labels[2])
        d = Text(": [ B ]", color=BLACK, font_size=40).next_to(labels[3])

        self.play(*[Create(i) for i in [a, b, c, d]])

        self.wait(2)

        self.play(Uncreate(edge_list[1]))

        self.wait(2)

        pointer1 = Arrow(start=b.get_top() + UP, end=b.get_top(), color=PURE_BLUE).shift(DOWN * 0.12).shift(LEFT * 0.49)
        pointer2 = Arrow(start=d.get_top() + UP, end=d.get_top(), color=PURE_BLUE).shift(DOWN * 0.12).shift(
            RIGHT * 0.15)

        self.play(Create(pointer2), Create(pointer1))

        self.wait(2)

        self.play(pointer1.animate.shift(RIGHT * 0.57))

        self.play(pointer1.animate.shift(RIGHT * 0.67))

        self.play(FadeOut(b[6]))
        self.play(b[7].animate.shift(LEFT * 0.67))

        self.wait(1)

        self.play((FadeOut(d[2])))
        self.play(d[3].animate.shift(LEFT * 0.1))

        self.play(FadeOut(pointer2, pointer1))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.2).shift(UP * 0.6))

        comp = MathTex(r"O(\text{degree of node(1) + degree of node(2)})", color=BLACK).to_edge(UP).scale(1.1).shift(
            RIGHT * 2).shift(UP)

        self.play(Create(comp))

        self.wait(2)

        self.play(Uncreate(comp), self.camera.frame.animate.scale(1 / 1.2).shift(DOWN * 0.6))

        self.wait(2)

        self.play(Uncreate(edge_list[2]), Uncreate(edge_list[0]))

        b[6].shift(RIGHT*8)

        self.play(FadeOut(nodes["B"]))

        self.wait(2)

        self.play(Uncreate(b, ), Uncreate(labels[1]))

        self.wait(1)

        self.play(FadeOut(a[2]))
        self.play(a[3].animate.shift(LEFT*0.2234))
        self.wait(1)

        self.play(FadeOut(c[2:4]))
        self.play(c[4:].animate.shift(LEFT * 0.7234))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.2).shift(UP * 0.6))

        comp = MathTex(r"O(\text{n + e})", color=BLACK).to_edge(UP).scale(1.1).shift(
            RIGHT * 2).shift(UP*0.23).scale(1.4)

        self.play(Create(comp))

        self.wait(2)

        self.play(Uncreate(comp), self.camera.frame.animate.scale(1 / 1.2).shift(DOWN * 0.6))

        self.wait(2)

        node_circle = Circle(
            radius=0.5,
            fill_color=TEAL_B,
            fill_opacity=1,
            color=DARK_BLUE,
            stroke_width=5.6
        )
        node_circle.move_to(nodes["B"].get_center() + DOWN + LEFT)

        node_label = Text("E ", color=BLACK).move_to(node_circle)

        node_group = VGroup(node_circle, node_label)

        self.play(Create(node_group))

        self.wait(2)

        c = Text("E ", color=BLACK, font_size=40).next_to(labels[1], ORIGIN)
        a = Text(": [ ]", color=BLACK, font_size=40).next_to(labels[1])

        self.play(Create(c), Create(a))

        self.wait(2)








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
        super().__init__(radius=0.5, color=PURE_RED, **kwargs)
        self.move_to(mobject.get_center())
