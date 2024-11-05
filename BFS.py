from manim import *
from collections import deque

PURPLE = ORANGE

config.background_color = LOGO_WHITE


class AnimatedSet(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initial set: just the curly braces
        self.left_brace = Text("{", font_size=50, color=BLACK)
        self.right_brace = Text("}", font_size=50, color=BLACK)
        self.elements = VGroup()  # Group to hold elements inside the set
        self.add(self.left_brace, self.right_brace)

        # Position the braces with more space between them initially
        self.left_brace.next_to(self.right_brace, LEFT, buff=1.0)
        self.arrange(RIGHT, buff=0.1)

    def push(self, element, scene):
        # Create a new Text object for the element to be added
        new_element = Text(element, font_size=50, color=BLACK)

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


class Queue(Mobject):
    def __init__(self, element_width=0.8, fill_opacity=0.5, fill_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.element_width = element_width
        self.elements = []

        # Create the queue structure with lines and fill area
        self.top_line = Line(start=LEFT * 2.7, end=RIGHT * 2.7, stroke_color=BLACK)
        self.bottom_line = Line(start=LEFT * 2.7, end=RIGHT * 2.7, stroke_color=BLACK)
        self.fill_area = Rectangle(width=5.4, height=0.8, fill_opacity=fill_opacity, fill_color=fill_color,
                                   stroke_width=0)

        self.queue_structure = VGroup(self.top_line, self.fill_area, self.bottom_line)
        self.queue_structure.arrange(DOWN, buff=0)
        self.queue_structure.shift(DOWN)

    def create_element(self, text):
        square = Square(side_length=self.element_width, fill_opacity=1, fill_color=RED, color=BLACK).scale(0.8)
        text = Text(text, font_size=44, color=BLACK).scale(0.8)
        return VGroup(square, text)

    def push(self, text, scene):
        element = self.create_element(text)
        element.next_to(self.queue_structure, RIGHT, buff=0.4)

        # Animate the new element into the queue
        scene.play(Create(element))
        if self.elements:
            # Shift all existing elements to the left
            shift_amount = self.element_width
            animations = [e.animate.shift(LEFT * shift_amount) for e in self.elements]
            scene.play(*animations)

        scene.play(element.animate.move_to(self.queue_structure.get_right() + LEFT * 0.4))
        self.elements.append(element)
        scene.wait(0.2)

    def pop(self, scene):
        if self.elements:
            element = self.elements.pop(0)
            scene.play(element.animate.next_to(self.fill_area.get_left() + LEFT * 1.34), run_time=2)
            scene.wait(0.2)
            return element
        else:
            print("Queue is empty, cannot pop")


def create_edge(a, b):
    return Line(start=a.get_center(), end=b.get_center(), stroke_color=PURE_RED, stroke_width=12).set_z_index(-0.5)


class GraphAnimation(MovingCameraScene):

    def construct(self):

        self.camera.frame.shift(UP * 0.23)
        self.camera.frame.scale(0.8)

        graph = {
            'A': ['B', 'C'],
            'B': ['G', 'A'],
            'C': ['A', "G", 'F'],
            'D': ['E'],
            'E': ['D', 'F'],
            'F': ['C', "G", 'E'],
            "G": ["B", "F", "C"]
        }

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

        self.play(self.camera.frame.animate.scale(1.3).shift(UP * 0.3))

        queue = Queue()
        queue.queue_structure.shift(UP * 4.46).shift(LEFT * 3)

        set1 = AnimatedSet().next_to(queue.queue_structure, RIGHT).shift(RIGHT * 1.4)

        self.play(Create(queue.queue_structure), )

        self.wait(2)

        queue.push("A", self)
        self.play(FadeOut(queue.queue_structure, queue.elements[0]))

        self.wait(2)

        self.play(Create(queue.queue_structure), Create(set1), Create(queue.elements[0]))

        self.wait(2)

        A, B, C, D, E, F, G = [nodes[f"{i}"][1].copy() for i in ["A", "B", "C", "D", "E", "F", "G"]]

        z = [A, B, C, G, F, E, D]

        visited = set()  # Set to keep track of visited nodes
        queue1 = deque(["A"])  # Queue for BFS traversal
        traversal = []  # List to store traversal order

        x = 1


        while queue1:
            node = queue1.popleft()  # Remove the first node in the queue
            a = queue.pop(self)
            if node not in visited:
                visited.add(node)  # Mark the node as visited
                set1.push(f"{node}", self)
                traversal.append(node)  # Add the node to traversal order
                self.play(nodes[f"{node}"][1].copy().animate.next_to(nodes["F"], DOWN).shift(LEFT*2).shift(DOWN*0.12).shift(RIGHT * x))
                self.play(nodes[f"{node}"][0].animate.set_fill(ORANGE))
                x += 1
                self.play(FadeOut(a))

                # Add neighbors to the queue if they haven't been visited
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue1.append(neighbor)
                        queue.push(f"{neighbor}", self)

            else:
                self.play(FadeOut(a))







        self.wait(2)

    def create_nodes(self, node_positions):
        """Create nodes at specified positions with labels."""
        nodes = {}
        for label, position in node_positions.items():
            # Create a circle for the node
            node_circle = Circle(
                radius=0.5,
                fill_color=GREEN,
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
