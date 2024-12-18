from manimlib import *
import numpy as np

PURE_RED = '#FF0000'
PURE_BLUE = '#0000FF'

MAROON_B = "#00FF00"



class prim(Scene):
    def construct(self):

        self.camera.frame.scale(1.2).shift(UP*0.7).scale(0.8)

        self.camera.background_color = "#111111"


        # Square layout with F above and G below
        node_positions = {
    "F": [0, 3, 0],      # Move a bit downwards for centering
    "A": [-2, 1, 0],   # Move slightly to the left and upwards for balance
    "B": [2.3, 1, 0],    # Move slightly to the left for symmetry with A
    "D": [-2, -2, 0],  # Move slightly downwards and left for balance
    "C": [2.3, -2, 0],   # Shift slightly left and downwards for better spacing
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

        self.play(nodes1["A"][0].animate.set_fill(YELLOW_C))

        a = Circle(radius=0.5, stroke_width=8.5).move_to(nodes1["A"]).set_color("#FF0000")
        self.play(ShowCreation(a))




        temp = edge_list[0].copy().set_color(MAROON_B)
        temp1 = edge_list[2].copy().set_color(MAROON_B)
        temp2 = edge_list[3].copy().set_color(MAROON_B)

        self.wait(3)

        self.play(GrowFromCenter(temp), GrowFromCenter(temp1), GrowFromCenter(temp2))

        self.wait(2)

        edge_a_b = edge_list[2].copy().set_color("#FF0000")
        self.play(ShowCreation(edge_a_b))
        b = Circle(radius=0.5, stroke_width=8.5).move_to(nodes1["B"]).set_color("#FF0000")
        self.play(nodes1["B"][0].animate.set_fill(YELLOW),ShowCreation(b))

        self.wait(2)


        temp3 = edge_list[1].copy().set_color(MAROON_B)
        temp4 = edge_list[4].copy().set_color(MAROON_B)
        temp5 = edge_list[5].copy().set_color(MAROON_B)

        self.wait(3)

        self.play(GrowFromCenter(temp3), GrowFromCenter(temp4), GrowFromCenter(temp5))
        self.wait(2)

        edge_b_d = edge_list[-2].copy().set_color("#FF0000")
        self.play(ShowCreation(edge_b_d))
        d = Circle(radius=0.5, stroke_width=8.5).move_to(nodes1["D"]).set_color("#FF0000")
        self.play(nodes1["D"][0].animate.set_fill(YELLOW),ShowCreation(d))

        self.wait(2)

        temp6 = edge_list[-1].copy().set_color(MAROON_B)

        self.play(ShowCreation(temp6))

        self.wait(2)

        edge_d_c = edge_list[-1].copy().set_color("#FF0000")
        self.play(ShowCreation(edge_d_c))
        c = Circle(radius=0.5, stroke_width=8.5).move_to(nodes1["C"]).set_color("#FF0000")
        self.play(nodes1["C"][0].animate.set_fill(YELLOW),ShowCreation(c))

        self.wait(2)

        edge_a_f = edge_list[0].copy().set_color("#FF0000").rotate(PI)
        self.play(ShowCreation(edge_a_f))
        f = Circle(radius=0.5, stroke_width=8.5).move_to(nodes1["F"]).set_color("#FF0000")
        self.play(nodes1["F"][0].animate.set_fill(YELLOW),ShowCreation(f))

        self.wait(2)


        self.play(
                  
                    *[Uncreate(i) for i in edge_list],
                    *[Uncreate(i) for i in [temp, temp1, temp2, temp3, temp4, temp5, temp6]],
                    FadeOut(weights["weight_A_D"]),FadeOut(weights["weight_B_C"]), FadeOut(weights["weight_F_B"])
                    
                    
                    )
        
        self.wait(2)


        self.play(self.camera.frame.animate.shift(RIGHT*1.77))

        self.wait(2)


        text = Text("V - 1   \nEdges").set_color(BLACK).next_to(nodes1["B"], RIGHT).shift(RIGHT+DOWN*0.35)
        self.play(ShowCreation(text))

        self.wait(2)
        












        






        

       


        self.embed()

    

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
                stroke_width=8
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
            ("B", "C"),
            ("B", "D"),
            ("D", "C"),

        ]

        for node1, node2 in edge_pairs:
            start_pos = node_positions[node1]
            end_pos = node_positions[node2]
            edge_line = Line(start_pos, end_pos, color=DARK_BLUE, stroke_width=8)
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
            ("D", "B", '2'),
            ("C", "D", '1'),
            ("B", "C", '7'),
            

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
