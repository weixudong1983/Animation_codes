from manim import *

PURPLE = ORANGE

config.background_color = LOGO_WHITE


class AnimatedSet(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initial set: just the curly braces
        self.left_brace = Text("{", font_size=36, color=BLACK)
        self.right_brace = Text("}", font_size=36, color=BLACK)
        self.elements = VGroup()  # Group to hold elements inside the set
        self.add(self.left_brace, self.right_brace)

        # Position the braces with more space between them initially
        self.left_brace.next_to(self.right_brace, LEFT, buff=1.0)
        self.arrange(RIGHT, buff=0.1)

    def push(self, element, scene):
        # Create a new Text object for the element to be added
        new_element = Text(element, font_size=36, color=BLACK)

        # Determine the target position for the new element (before the right brace)
        if self.elements:
            last_element = self.elements[-1]
            new_element.next_to(last_element, RIGHT, buff=0.2)
        else:
            new_element.next_to(self.left_brace, RIGHT, buff=0.2)

        # Calculate the total width required for the new element and the existing elements
        total_width = new_element.get_width() + self.elements.get_width() + 0.4  # Extra space for buffers

        # Check if the right brace needs to be moved
        available_width = self.right_brace.get_center()[0] - self.left_brace.get_center()[0] - 1.0

        if total_width > available_width:
            # Move the right brace enough to make space and keep it symmetrical
            move_distance = (total_width - available_width) / 2 + 0.1
            move_brace = self.right_brace.animate.shift(RIGHT * move_distance)
            scene.play(move_brace)

        # Animate adding the new element to the set
        scene.play(Write(new_element))
        self.elements.add(new_element)

        # Update the overall group to include the new elements
        self.add(self.elements)

        # Re-arrange elements to keep symmetry between braces and elements
        self.arrange_elements(scene)

    def arrange_elements(self, scene):
        # Re-arrange the elements to keep symmetry between the left and right braces
        if self.elements:
            left_edge = self.left_brace.get_right()[0]
            right_edge = self.right_brace.get_left()[0]
            mid_point = (left_edge + right_edge) / 2

            # Shift elements to be centered between the braces
            elements_center = self.elements.get_center()[0]
            shift_distance = mid_point - elements_center

            # Animate the shifting of the elements
            if shift_distance != 0:
                shift_animation = self.elements.animate.shift(RIGHT * shift_distance)
                scene.play(shift_animation)


class StackElement(VGroup):
    def __init__(self, value, **kwargs):
        super().__init__(**kwargs)
        self.rect = Rectangle(height=0.55, width=1.41, fill_opacity=1, fill_color=TEAL, color=BLACK)
        text = Text(str(value), font_size=37, color=BLACK, font=BOLD)
        self.add(self.rect, text)


class StackElement1(VGroup):
    def __init__(self, value, opacity=1, **kwargs, ):
        super().__init__(**kwargs)
        self.rect = Rectangle(height=0.55, width=1.35, fill_opacity=opacity, fill_color=TEAL, color=DARK_BLUE, )
        text = Text(str(value), font_size=37, color=BLACK, opacity=opacity)
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
            Line(start=LEFT * 1.065 * bucket_width / 2, end=RIGHT * 1.065 * bucket_width / 2, stroke_width=10),
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
            return popped_element

        else:
            scene.play(Indicate(self.bucket, color=RED))


def create_edge(a, b):
    return Line(start=a.get_center(), end=b.get_center(), stroke_color=PURE_RED, stroke_width=12).set_z_index(-0.5)


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

        self.play(self.camera.frame.animate.scale(1.2).shift(RIGHT * 1.43).shift(DOWN * 0.66))

        stack = Stack().next_to(nodes["D"], RIGHT).shift(RIGHT * 0.8)
        stack.push(self, "A")
        self.play(FadeOut(stack[0]))
        set1 = AnimatedSet().next_to(stack, DOWN).shift(DOWN * 0.7).shift(LEFT * 2.7)

        self.play(Create(stack))
        self.play(Create(set1))

        self.wait(2)

        a = stack.pop(self)
        self.wait(2)
        set1.push("A", self)


        self.play(nodes["A"][1].copy().animate.next_to(nodes["F"], DOWN).shift(LEFT * 1.6).shift(DOWN * 0.45))
        self.play(nodes["A"][0].animate.set_fill(PURPLE))

        self.wait(2)

        self.play(FadeOut(a, ))

        self.wait(2)

        self.play(Indicate(nodes["B"], color=PURE_GREEN), Indicate(nodes["C"], color=PURE_GREEN))
        self.wait(2)

        stack.push(self, "C")
        stack.push(self, "B")

        self.wait(2)

        b = stack.pop(self)
        self.wait(2)
        set1.push("B", self)


        self.play(nodes["B"][1].copy().animate.next_to(nodes["F"], DOWN).shift(LEFT * 0.6).shift(DOWN * 0.45))
        self.play(nodes["B"][0].animate.set_fill(PURPLE))


        self.wait(2)

        self.play(FadeOut(b, ))

        self.wait(2)

        self.play(Indicate(nodes["A"], color=PURE_GREEN), Indicate(nodes["G"], color=PURE_GREEN))
        stack.push(self, "G")

        self.wait(2)

        g = stack.pop(self)

        set1.push("G", self)



        self.play(nodes["G"][1].copy().animate.next_to(nodes["F"], DOWN).shift(RIGHT * 0.4).shift(DOWN * 0.45))
        self.play(nodes["G"][0].animate.set_fill(PURPLE))

        self.play(FadeOut(g, ))

        self.wait(2)

        self.play(Indicate(nodes["C"], color=PURE_GREEN), Indicate(nodes["F"], color=PURE_GREEN),
                  Indicate(nodes["B"], color=PURE_GREEN))

        stack.push(self, "C")
        stack.push(self, "F")

        self.wait(2)

        f = stack.pop(self)

        set1.push("F", self)



        self.play(nodes["F"][1].copy().animate.next_to(nodes["F"], DOWN).shift(RIGHT * 1.4).shift(DOWN * 0.45))
        self.play(nodes["F"][0].animate.set_fill(PURPLE))

        self.play(FadeOut(f, ))

        self.wait(2)

        self.play(Indicate(nodes["C"], color=PURE_GREEN), Indicate(nodes["E"], color=PURE_GREEN),
                  Indicate(nodes["G"], color=PURE_GREEN))

        self.wait(1)

        stack.push(self, "E")
        stack.push(self, "C")

        self.wait(1)

        c = stack.pop(self)

        set1.push("C", self)



        self.play(nodes["C"][1].copy().animate.next_to(nodes["F"], DOWN).shift(RIGHT * 2.4).shift(DOWN * 0.45))
        self.play(nodes["C"][0].animate.set_fill(PURPLE))

        self.play(FadeOut(c, ))

        self.wait(2)

        self.play(Indicate(nodes["A"], color=PURE_GREEN), Indicate(nodes["G"], color=PURE_GREEN),
                  Indicate(nodes["F"], color=PURE_GREEN))

        self.wait(2)

        e = stack.pop(self)

        set1.push("E", self)

        self.play(nodes["E"][1].copy().animate.next_to(nodes["F"], DOWN).shift(RIGHT * 3.4).shift(DOWN * 0.45))
        self.play(nodes["E"][0].animate.set_fill(PURPLE))

        self.play(FadeOut(e, ))

        self.wait(2)

        self.play(Indicate(nodes["D"], color=PURE_GREEN),
                  Indicate(nodes["F"], color=PURE_GREEN))

        self.wait()

        stack.push(self, "D")

        self.wait(2)

        d = stack.pop(self)

        set1.push("D", self)

        self.play(nodes["D"][1].copy().animate.next_to(nodes["F"], DOWN).shift(RIGHT * 4.4).shift(DOWN * 0.45))
        self.play(nodes["D"][0].animate.set_fill(PURPLE))

        self.play(FadeOut(d))

        self.wait(2)

        c = stack.pop(self)
        self.play(FadeOut(c))
        c = stack.pop(self)
        self.play(FadeOut(c))

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
