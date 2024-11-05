from manim import *

config.background_color = LOGO_WHITE

class StackElement(VGroup):
    def __init__(self, value, **kwargs, ):
        super().__init__(**kwargs)
        self.rect = Rectangle(height=0.55, width=1.41, fill_opacity=1, fill_color=TEAL, color=BLACK)
        text = Text(str(value), font_size=27, color=BLACK,font=BOLD )
        self.add(self.rect, text)

class StackElement1(VGroup):
    def __init__(self, value, opacity=1 ,**kwargs, ):
        super().__init__(**kwargs)
        self.rect = Rectangle(height=0.55, width=1.35, fill_opacity=opacity, fill_color=TEAL, color=DARK_BLUE,)
        text = Text(str(value), font_size=27, color=BLACK,opacity=opacity )
        self.add(self.rect, text)


class Stack(VGroup):
    def __init__(self, max_size=5, **kwargs):
        super().__init__(**kwargs)
        self.max_size = max_size
        self.elements = []

        # Create the open-top bucket with filled interior
        bucket_width = 1.5
        bucket_height = self.max_size * 0.9

        # Create the filled interior
        bucket_interior = Rectangle(
            width=bucket_width,
            height=bucket_height,
            stroke_width=0
        )
        bucket_interior.move_to(UP * bucket_height / 2)

        # Create the bucket outline
        bucket_outline = VGroup(
            Line(start=LEFT*1.065 * bucket_width / 2, end=RIGHT*1.065 * bucket_width / 2, stroke_width=10),
            Line(start=LEFT * bucket_width / 2, end=LEFT * bucket_width / 2 + UP * bucket_height, stroke_width=10),
            Line(start=RIGHT * bucket_width / 2, end=RIGHT * bucket_width / 2 + UP * bucket_height, stroke_width=10)
        )
        bucket_outline.set_stroke(color=DARK_BLUE, opacity=5)

        self.bucket = VGroup(bucket_interior, bucket_outline).shift(DOWN * 2.3)
        self.add(self.bucket)

    def push(self, scene, value, time=1, ):
        if 5:
            new_element = StackElement(value)
            new_element.next_to(self.bucket, UP)
            scene.play(Create(new_element))

            if self.elements:
                target_position = self.elements[-1].get_top() + UP * 0.32
            else:
                target_position = self.bucket[0].get_bottom() + UP * 0.32

            scene.play(new_element.animate.move_to(target_position), run_time=time)
            self.elements.append(new_element)
            self.add(new_element)

    def push1(self, scene, value, time=1, ):
        if 5:
            new_element = StackElement1(value, opacity=0.66)
            new_element.next_to(self.bucket, UP)
            scene.play(Create(new_element))

            if self.elements:
                target_position = self.elements[-1].get_top() + UP * 0.43
            else:
                target_position = self.bucket[0].get_bottom() + UP * 0.44

            scene.play(new_element.animate.move_to(target_position), run_time=time)
            self.elements.append(new_element)
            self.add(new_element)

    def pop(self, scene):
        if self.elements:
            popped_element = self.elements.pop()
            scene.play(popped_element.animate.next_to(self.bucket, UP))
            scene.play(FadeOut(popped_element))
        else:
            scene.play(Indicate(self.bucket, color=RED))


def create_edge(a, b):
    return Line(start=a.get_center(), end=b.get_center(),stroke_color=PURE_RED, stroke_width=12).set_z_index(-0.5)


class GraphAnimation(MovingCameraScene):

    def construct(self):
        self.camera.frame.shift(UP * 0.23)
        self.camera.frame.scale(0.8)

        # Define the positions for the 7 nodes based on the image layout
        node_positions = {
            "A": [-2, 2, 0],
            "B": [2, 2, 0],
            "D": [4, 0, 0],
            "E": [2, -2, 0],
            "F": [-2, -2, 0],
            "G": [0, 0, 0],
            "C": [-4, 0, 0]
        }

        # Create the nodes
        nodes = self.create_nodes(node_positions)

        # Create the edges
        edges, edge_list = self.create_edges(node_positions)

        # Store the original edges for later transformation back
        original_edges = [edge.copy() for edge in edge_list]

        # Add nodes and edges to the scene
        self.play(*[GrowFromCenter(node) for node in nodes.values()])
        self.play(*[GrowFromCenter(edge) for edge in edge_list])

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.2).shift(RIGHT*1.43).shift(DOWN*0.6))

        stack = Stack().next_to(nodes["D"], RIGHT).shift(RIGHT*0.8)
        self.play(Create(stack))

        self.wait(2)

        stack.push(self, "DFS(A)")

        self.wait(2)

        a = Circle(radius=0.5, color=PURE_RED, stroke_width=12, ).move_to(nodes["A"])

        self.play(Create(a))

        self.wait()

        self.play(nodes["A"][1].copy().animate.scale(1.2).next_to(nodes["F"], DOWN).shift(DOWN*0.3))

        self.wait(2)

        self.play(Indicate(nodes["C"], color=PURE_GREEN), Indicate(nodes["B"], color=PURE_GREEN))
        self.wait(2)

        stack.push(self, "DFS(B)")

        edge_a_b = create_edge(nodes["A"], nodes["B"])

        self.play(Create(edge_a_b))

        b = Circle(radius=0.5, color=PURE_RED, stroke_width=12, ).move_to(nodes["B"])
        self.play(Create(b))

        self.play(nodes["B"][1].copy().animate.scale(1.2).next_to(nodes["F"], DOWN).shift(RIGHT).shift(DOWN*0.3))


        self.wait(2)

        stack.push(self, "DFS(G)")

        self.wait(1)

        edge_b_g = create_edge(nodes["B"], nodes["G"])

        self.play(Create(edge_b_g))

        g = Circle(radius=0.5, color=PURE_RED, stroke_width=12, ).move_to(nodes["G"])
        self.play(Create(g))

        self.play(nodes["G"][1].copy().animate.scale(1.2).next_to(nodes["F"], DOWN).shift(RIGHT*2).shift(DOWN * 0.3))

        self.wait(2)

        self.play(Indicate(nodes["C"], color=PURE_GREEN), Indicate(nodes["F"], color=PURE_GREEN))

        self.wait(2)

        stack.push(self, "DFS(F)")

        self.wait(1)

        edge_g_f = create_edge(nodes["G"], nodes["F"])

        self.play(Create(edge_g_f))

        f = Circle(radius=0.5, color=PURE_RED, stroke_width=12, ).move_to(nodes["F"])
        self.play(Create(f))

        self.play(nodes["F"][1].copy().animate.scale(1.2).next_to(nodes["F"], DOWN).shift(RIGHT * 3).shift(DOWN * 0.3))

        self.wait(2)

        stack.push(self, "DFS(C)")

        self.wait(1)

        edge_f_c = create_edge(nodes["F"], nodes["C"])

        self.play(Create(edge_f_c))

        c = Circle(radius=0.5, color=PURE_RED, stroke_width=12, ).move_to(nodes["C"])
        self.play(Create(c))

        self.play(nodes["C"][1].copy().animate.scale(1.2).next_to(nodes["F"], DOWN).shift(RIGHT * 4).shift(DOWN * 0.3))

        self.wait(2)

        stack.pop(self)

        self.play(Uncreate(c))
        self.play(Uncreate(edge_f_c))

        self.wait(2)

        stack.push(self, "DFS(E)")

        self.wait(1)

        edge_f_e = create_edge(nodes["F"], nodes["E"])

        self.play(Create(edge_f_e))

        e = Circle(radius=0.5, color=PURE_RED, stroke_width=12, ).move_to(nodes["E"])
        self.play(Create(e))

        self.play(nodes["E"][1].copy().animate.scale(1.2).next_to(nodes["F"], DOWN).shift(RIGHT * 5).shift(DOWN * 0.3))

        self.wait(2)

        stack.push(self, "DFS(D)")

        self.wait(1)

        edge_e_d = create_edge(nodes["E"], nodes["D"])

        self.play(Create(edge_e_d))

        d = Circle(radius=0.5, color=PURE_RED, stroke_width=12, ).move_to(nodes["D"])
        self.play(Create(d))

        self.play(nodes["D"][1].copy().animate.scale(1.2).next_to(nodes["F"], DOWN).shift(RIGHT * 6).shift(DOWN * 0.3))

        self.wait(2)

        stack.pop(self)
        self.play(Uncreate(d))
        self.play(Uncreate(edge_e_d))

        stack.pop(self)
        self.play(Uncreate(e))
        self.play(Uncreate(edge_f_e))

        stack.pop(self)
        self.play(Uncreate(f))
        self.play(Uncreate(edge_g_f))

        stack.pop(self)
        self.play(Uncreate(g))
        self.play(Uncreate(edge_b_g))

        stack.pop(self)
        self.play(Uncreate(b))
        self.play(Uncreate(edge_a_b))

        stack.pop(self)
        self.play(Uncreate(a))

        self.wait(2)

    def create_nodes(self, node_positions):
        """Create nodes at specified positions with labels."""
        nodes = {}
        for label, position in node_positions.items():
            # Create a circle for the node
            node_circle = Circle(
                radius=0.5,
                fill_color=TEAL_B,
                fill_opacity=1,
                color=DARK_BLUE,
                stroke_width=5.6
            )
            node_circle.move_to(position)

            # Create the label (text) for the node with black color
            node_label = Text(label, color=BLACK).move_to(position)

            # Group the circle and the text together
            node_group = VGroup(node_circle, node_label)
            nodes[label] = node_group  # Store with direct label access (e.g., "A")

        return nodes

    def create_edges(self, node_positions):
        """Create undirected edges between nodes."""
        edge_list = []
        edge_pairs = [
            ("A", "B"),
            ("A", "C"),
            ("B", "G"),
            ("D", "E"),
            ("E", "F"),
            ("F", "G"),
            ("C", "G"),
            ("C", "F")
        ]

        for node1, node2 in edge_pairs:
            start_pos = node_positions[node1]
            end_pos = node_positions[node2]
            edge_line = Line(start_pos, end_pos, color=DARK_BLUE, stroke_width=5)
            edge_line.z_index = -1  # Set z-index lower than nodes
            edge_list.append(edge_line)

        return {}, edge_list

    def create_directed_edges(self, node_positions):
        """Transform undirected edges into directed edges."""
        directed_edge_list = []
        edge_pairs = [
            ("A", "B"),
            ("C", "A"),
            ("B", "G"),
            ("E", "D"),
            ("F", "E"),
            ("F", "G"),
            ("G", "C"),
            ("C", "F")
        ]

        for node1, node2 in edge_pairs:
            start_pos = node_positions[node1]
            end_pos = node_positions[node2]
            directed_edge = Arrow(
                start_pos, end_pos,
                buff=0.5,  # Adjusted buff to ensure arrow touches the circle but does not penetrate
                color=MAROON_B,
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
            ("A", "C", "4"),
            ("B", "G", "7"),
            ("D", "E", "5"),
            ("E", "F", "6"),
            ("F", "G", "2"),
            ("C", "G", "8"),
            ("C", "F", "9")
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
