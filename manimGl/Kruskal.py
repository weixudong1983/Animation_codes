from manimlib import *
import numpy as np

PURE_RED = '#FF0000'
PURE_BLUE = '#0000FF'

MAROON_B = "#00FF00"



class Krskl(Scene):
    def construct(self):

        self.camera.frame.scale(1.2).shift(UP*0.6).scale(0.8)

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

        self.play(self.camera.frame.animate.shift(RIGHT*2))


        ad = weights["weight_A_D"].copy()
        af = weights["weight_F_A"].copy()
        fb = weights["weight_F_B"].copy()
        bc = weights["weight_B_C"].copy()
        dc = weights["weight_C_D"].copy()
        db = weights["weight_D_B"].copy()
        ab = weights["weight_A_B"].copy()


        # Define positions
        ad_position = nodes1["B"].get_center() + RIGHT * 3.1 + UP * 2.5
        ab_position = ad_position + DOWN 
        db_position = ab_position + DOWN 
        af_position = db_position + DOWN 
        fb_position = af_position + DOWN 
        dc_position = fb_position + DOWN 
        bc_position = dc_position + DOWN

        # Create the animations
        animations = [
            ad.animate.move_to(ad_position),
            ab.animate.move_to(ab_position),
            db.animate.move_to(db_position),
            af.animate.move_to(af_position),
            fb.animate.move_to(fb_position),
            dc.animate.move_to(dc_position),
            bc.animate.move_to(bc_position),
        ]

        # Play animations simultaneously
        self.play(AnimationGroup(*animations, lag_ratio=0))
        self.wait(4)



        a = Circle(radius=0.38, stroke_width=7).set_color(PURE_BLUE).move_to(ad)
        self.play(ShowCreation(a))

        self.wait(1)


        line_a_d = edge_list[3].copy().set_color(PURE_RED)
        self.play(GrowFromCenter(line_a_d))

        aaa = Circle(radius=0.5, stroke_width=10).set_color(PURE_RED).move_to(nodes1["A"])
        d = Circle(radius=0.5, stroke_width=10).set_color(PURE_RED).move_to(nodes1["D"])
        self.play(nodes1['A'][0].animate.set_fill(YELLOW),      
                  nodes1['D'][0].animate.set_fill(YELLOW))
        self.play(ShowCreation(aaa), ShowCreation(d))

                  

        self.wait(2)  

        self.play(a.animate.move_to(ab))  

        self.wait(2)

        line_d_b = edge_list[-2].copy().set_color(PURE_RED)
        self.play(GrowFromCenter(line_d_b))
        b = Circle(radius=0.5, stroke_width=10).set_color(PURE_RED).move_to(nodes1["B"])
        self.play(nodes1['B'][0].animate.set_fill(YELLOW),)              
        
        self.play(ShowCreation(b))

        self.wait(1)

        self.play(a.animate.move_to(db))

        self.wait()

        line_a_b = edge_list[2].copy().set_color(PURE_RED)
        self.play(GrowFromCenter(line_a_b))
        self.wait(3)

        self.play(Uncreate(line_a_b))
        self.wait(2)

        self.play(a.animate.move_to(af))
        self.wait()

        line_a_f = edge_list[0].copy().set_color(PURE_RED)
        self.play(GrowFromCenter(line_a_f))
        f = Circle(radius=0.5, stroke_width=10).set_color(PURE_RED).move_to(nodes1["F"])
        self.play(nodes1['F'][0].animate.set_fill(YELLOW),)
        self.play(ShowCreation(f))

        self.wait(1)

        self.play(a.animate.move_to(fb))

        self.wait()

        line_f_b = edge_list[1].copy().set_color(PURE_RED)
        self.play(GrowFromCenter(line_f_b))
        self.wait(3)

        self.play(Uncreate(line_f_b))
        self.wait(1)

        self.play(a.animate.move_to(dc))
        self.wait(1)

        line_d_c = edge_list[-1].copy().set_color(PURE_RED)
        self.play(GrowFromCenter(line_d_c))
        c = Circle(radius=0.5, stroke_width=10).set_color(PURE_RED).move_to(nodes1["C"])
        self.play(nodes1['C'][0].animate.set_fill(YELLOW),)
        self.play(ShowCreation(c))

        self.wait(3)


        self.play(FadeOut(edge_list[2]), FadeOut(edge_list[1]), 
                FadeOut(edge_list[-3]),
                FadeOut(weights["weight_A_B"]),
                FadeOut(weights["weight_F_B"]),
                FadeOut(weights["weight_B_C"]),
                FadeOut(Group(ab, bc, af, dc, db, fb, ab, bc, a, ad))
                
                )
        
        self.play(self.camera.frame.animate.shift(LEFT*1.9))

        self.wait(3)

                                                                       
                                                                       
                                                                









        


        
        



        

       


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
            ("A", "D", '1'),
            ("D", "B", '2'),
            ("C", "D", '5'),
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


    


class cycle(Scene):
    def construct(self):

        self.camera.frame.shift(RIGHT*1.3)

        # Define node positions for multiple disconnected subgraphs
        node_positions_disconnected = {
            # Subgraph 1: Single node
            "X": [-4, 2, 0],

            # Subgraph 2: Two connected nodes
            "Y": [-4, -1, 0],
            "Z": [-2, -2.3, 0],

            # Subgraph 3: Two disconnected nodes
            "P": [-1.29, 2.3, 0],
            "Q": [0, 0, 0],

            # Subgraph 4: Two disconnected nodes
            "M": [1, -2.3, 0],
            "N": [2, 0, 0],
        }

        # Create the nodes
        nodes = self.create_nodes(node_positions_disconnected)

        # Create the edges for the disconnected subgraphs
        edges, edge_list = self.create_edges(node_positions_disconnected)

        # Add nodes and edges to the scene
        self.play(*[GrowFromCenter(node) for node in nodes.values()])
        self.play(*[GrowFromCenter(edge) for edge in edge_list])

        self.wait(2)

        x = Text("{X}").set_color(BLACK).next_to(nodes["N"], RIGHT).shift(UP*1+RIGHT).shift(RIGHT+UP)
        pq = Text("{P,Q}").set_color(BLACK).next_to(x, DOWN, buff=0.7)
        yz = Text("{Y,Z}").set_color(BLACK).next_to(pq, DOWN, buff=0.7)
        mn = Text("{N,M}").set_color(BLACK).next_to(yz, DOWN, buff=0.7)



        self.play(TransformFromCopy(nodes['X'][1], x))
        self.wait(3)
        self.play(TransformFromCopy(VGroup(nodes['P'][1], nodes["Q"][1]), pq))

        self.wait(2)

        self.play(TransformFromCopy(VGroup(nodes['Y'][1], nodes["Z"][1]), yz))
        self.wait(3)
        self.play(TransformFromCopy(VGroup(nodes['M'][1], nodes["N"][1]), mn))
        self.wait(2)


        edge_x_p = Line(nodes["X"].get_center(), nodes["P"].get_center(), color=DARK_BLUE, stroke_width=8).set_z_index(-1)
        self.play(ShowCreation(edge_x_p))
        self.wait(1)

        a = SurroundingRectangle(Group(x, pq), color=PURE_BLUE)
        self.play(ShowCreation(a))
        self.wait(2)
        self.play(Uncreate(a))

        pqx = Text("{X,P,Q}").set_color(BLACK).move_to(pq)
        self.play(ReplacementTransform(VGroup(x,pq), pqx))
        self.wait(2)

        edge_q_m = Line(nodes["Q"].get_center(), nodes["M"].get_center(), color=DARK_BLUE, stroke_width=8).set_z_index(-1)
        self.play(ShowCreation(edge_q_m))
        self.wait(1)

        a = SurroundingRectangle(pqx, color=PURE_BLUE)
        b = SurroundingRectangle(mn, color=PURE_BLUE)
        self.play(ShowCreation(a), ShowCreation(b))
        self.wait(2)
        self.play(Uncreate(a), Uncreate(b))
        self.wait(2)

        pqxnm = Text("{X,P,Q,N,M}").set_color(BLACK).move_to(pqx)
        self.play(ReplacementTransform(VGroup(pqx,mn), pqxnm))
        self.wait(2)

        edge_p_n = Line(nodes["P"].get_center(), nodes["N"].get_center(), color=DARK_BLUE, stroke_width=8).set_z_index(-1)
        self.play(ShowCreation(edge_p_n))
        self.wait(2)

        a = SurroundingRectangle(pqxnm, color=PURE_BLUE)
        self.play(ShowCreation(a))
        self.wait(2)

        self.play(Uncreate(a))

        self.wait(2)













class UnionFindTable(Scene):

    def create_custom_table(
        self,
        data,
        cell_width=1.0,
        cell_height=0.6,
        line_color=BLACK,
        text_color=BLACK,
        font_size=28
    ):
        """
        Creates a grid (table) of lines, rectangular backgrounds, and text
        objects manually.
        
        Parameters
        ----------
        data : list of lists of str
            2D list of string data to fill the cells (rows × columns).
            Example (3x7):
              [
                ["A", "B", "C", "D", "E", "F", "G"],
                ["A", "B", "C", "D", "E", "F", "G"],
                ["0", "0", "0", "0", "0", "0", "0"]
              ]
        cell_width : float
            The width of each cell.
        cell_height : float
            The height of each cell.
        line_color : Color
            The color of the grid lines.
        text_color : Color
            The color of the text in each cell.
        font_size : int
            The font size for text in each cell.

        Returns
        -------
        VGroup
            A VGroup containing all lines, rectangles, and text mobjects for the table.
        """
        rows = len(data)
        cols = len(data[0]) if rows > 0 else 0

        # Group to hold everything (lines + background rects + text)
        table_group = VGroup()

        # 2D lists to keep track of rectangles and texts in each cell
        self.cell_mobjects = [[None for _ in range(cols)] for _ in range(rows)]
        self.cell_rect_mobjects = [[None for _ in range(cols)] for _ in range(rows)]

        # -------------------------
        # Draw horizontal lines
        # -------------------------
        for row_idx in range(rows + 1):
            y = (rows * cell_height / 2) - (row_idx * cell_height)
            start = np.array([-(cols * cell_width) / 2, y, 0])
            end   = np.array([ (cols * cell_width) / 2, y, 0])
            line  = Line(start, end, color=line_color)
            table_group.add(line)

        # -------------------------
        # Draw vertical lines
        # -------------------------
        for col_idx in range(cols + 1):
            x = -(cols * cell_width) / 2 + (col_idx * cell_width)
            start = np.array([x,  (rows * cell_height) / 2, 0])
            end   = np.array([x, -(rows * cell_height) / 2, 0])
            line  = Line(start, end, color=line_color)
            table_group.add(line)

        # -------------------------
        # Create rectangle + text for each cell
        # -------------------------
        for r in range(rows):
            for c in range(cols):
                # Compute the center of the cell
                center_x = -(cols * cell_width) / 2 + (c + 0.5) * cell_width
                center_y =  (rows * cell_height) / 2 - (r + 0.5) * cell_height

                # 1) Background rectangle
                rect = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    stroke_width=0,
                    fill_color=WHITE,       # default fill color
                    fill_opacity=0          # default: transparent
                )
                rect.move_to([center_x, center_y, 0])
                table_group.add(rect)
                self.cell_rect_mobjects[r][c] = rect

                # 2) Text
                text_str = data[r][c]
                text_mob = Text(
                    text_str,
                    color=text_color,
                    font_size=font_size
                ).set_color(BLACK).set_z_index(1)
                text_mob.move_to([center_x, center_y, 0])
                table_group.add(text_mob)
                self.cell_mobjects[r][c] = text_mob

        return table_group


    def construct(self):
        self.camera.frame.scale(0.85).shift(LEFT*1.15+UP*0.1)

        # Define table data (3 rows × 7 columns in this example)
        table_data = [
            ["A", "B", "C", "D", "E", "F", "G"],
            ["A", "B", "C", "D", "E", "F", "G"],
            ["0", "0", "0", "0", "0", "0", "0"],
        ]

        # Create the table with smaller cells
        table = self.create_custom_table(
            data=table_data,
            cell_width=1.0,   # smaller
            cell_height=0.6,  # smaller
            line_color=BLACK,
            text_color=BLACK,
            font_size=28      # slightly smaller text
        )

        # Shift the table up so we have space below for trees
        table.shift(2 * UP)

        # Create labels (Elements, Parent, Rank) on the left
        elements_label = Text("Elements:").set_color(BLACK).scale(0.62)
        parent_label   = Text("Parent:  ").set_color(BLACK).scale(0.62)
        rank_label     = Text("Rank:    ").set_color(BLACK).scale(0.62)

        labels = VGroup(elements_label, parent_label, rank_label)
        labels.arrange(DOWN, aligned_edge=LEFT, buff=0.4)  
        
        # Position labels relative to the table
        labels.next_to(self.cell_mobjects[0][0], LEFT, buff=0.5).scale(0.9).shift(DOWN*0.6)
        
        # Show table + labels
        self.play(ShowCreation(table), ShowCreation(labels))
        self.wait(2)

        # Create 7 node circles (A, B, C, D, E, F, G)
        a = create_nodes(self, "A")
        b = create_nodes(self, "B")
        c = create_nodes(self, "C")
        d = create_nodes(self, "D")
        e = create_nodes(self, "E")
        f = create_nodes(self, "F")
        g = create_nodes(self, "G")

        nodes = VGroup(a, b, c, d, e, f, g)
        nodes.arrange(RIGHT, aligned_edge=LEFT, buff=1.15).shift(DOWN*0.44+ LEFT)

        # Show the circles on screen
        self.play(ShowCreation(nodes))
        self.wait()

        # --------------------------------------------------------
        # EXAMPLE: Fill a cell with color after everything is shown
        # Let's fill cell (row=1, col=2) (the "C" in the middle row)
        # --------------------------------------------------------
        
        c1 = SurroundingRectangle(self.cell_rect_mobjects[0][2], color='#0000FF', stroke_width=7).scale(0.756)
        c2 = SurroundingRectangle(self.cell_rect_mobjects[1][2], color='#0000FF', stroke_width=7).scale(0.756)
        a1 = SurroundingRectangle(self.cell_rect_mobjects[0][0], color='#0000FF', stroke_width=7).scale(0.756)
        a2 = SurroundingRectangle(self.cell_rect_mobjects[1][0], color='#0000FF', stroke_width=7).scale(0.756)
        self.play(a[0].animate.set_fill(TEAL_B), c[0].animate.set_fill(TEAL_B) )

        self.wait(2)

        self.play(ShowCreation(c1), ShowCreation(a1))
        self.wait(1)
        self.play(ReplacementTransform(c1,c2), ReplacementTransform(a1,a2))

        self.wait(2)

        self.play(Uncreate(c2), Uncreate(a2), a[0].animate.set_fill(YELLOW), c[0].animate.set_fill(YELLOW))



        self.wait(2)

        b1 = SurroundingRectangle(self.cell_rect_mobjects[0][1], color='#0000FF', stroke_width=7).scale(0.756)
        b2 = SurroundingRectangle(self.cell_rect_mobjects[1][1], color='#0000FF', stroke_width=7).scale(0.756)
        b3 = SurroundingRectangle(self.cell_rect_mobjects[2][1], color='#0000FF', stroke_width=7).scale(0.756)
        a3 = SurroundingRectangle(self.cell_rect_mobjects[2][0], color='#0000FF', stroke_width=7).scale(0.756)
        a1 = SurroundingRectangle(self.cell_rect_mobjects[0][0], color='#0000FF', stroke_width=7).scale(0.756)
        a2 = SurroundingRectangle(self.cell_rect_mobjects[1][0], color='#0000FF', stroke_width=7).scale(0.756)


        self.play(a[0].animate.set_fill(TEAL_B), b[0].animate.set_fill(TEAL_B) )
        self.play(ShowCreation(a1), ShowCreation(b1))

        self.play(ReplacementTransform(a1,a2), ReplacementTransform(b1,b2))
        self.wait(2)
        self.play(ReplacementTransform(a2,a3), ReplacementTransform(b2,b3))
        self.wait(2)

        edge_b_a = always_redraw(lambda: Line(b.get_center(), a.get_center(), stroke_width=8).set_color(DARK_BLUE).set_z_index(-1))
        self.play(b.animate.next_to(a, DOWN, buff=0.75))
        self.play(a.animate.shift(RIGHT*0.6))
        self.play(ShowCreation(edge_b_a))




        row_idx = 2  # second row in the data
        col_idx = 0  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "1"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.85)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)

        self.play(a3.animate.move_to(self.cell_mobjects[1][0]), b3.animate.move_to(self.cell_mobjects[1][1]))
        self.wait()


        row_idx = 1  # second row in the data
        col_idx = 1  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "A"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.75)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)


        self.play(a[0].animate.set_fill(YELLOW), b[0].animate.set_fill(YELLOW))

        self.play(a3.animate.move_to(self.cell_mobjects[0][0]), b3.animate.move_to(self.cell_mobjects[0][2]))
        self.wait()
        self.play(a[0].animate.set_fill(TEAL_B), c[0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(a3.animate.move_to(self.cell_mobjects[1][0]), b3.animate.move_to(self.cell_mobjects[1][2]))
        self.wait(1)
        self.play(a3.animate.move_to(self.cell_mobjects[2][0]), b3.animate.move_to(self.cell_mobjects[2][2]))
        self.wait(2)


        self.play(c.animate.next_to(b, RIGHT, buff=0.625))
        edge_c_a = always_redraw(lambda: Line(c.get_center(), a.get_center(), stroke_width=8).set_color(DARK_BLUE).set_z_index(-1))
        self.play(ShowCreation(edge_c_a))
        self.play(b.animate.shift(LEFT*0.1))
        self.play(a3.animate.move_to(self.cell_mobjects[1][0]), b3.animate.move_to(self.cell_mobjects[1][2]))
        self.wait(2)

        row_idx = 1  # second row in the data
        col_idx = 2  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "A"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.75)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)


        self.wait()

        self.play(a[0].animate.set_fill(YELLOW), c[0].animate.set_fill(YELLOW))
        self.wait(2)

        self.play(a3.animate.move_to(self.cell_mobjects[0][3]), b3.animate.move_to(self.cell_mobjects[0][6]))
        self.wait(1.6)
        self.play(d[0].animate.set_fill(TEAL_B), g[0].animate.set_fill(TEAL_B))
        self.wait(1)

        self.play(a3.animate.move_to(self.cell_mobjects[1][3]), b3.animate.move_to(self.cell_mobjects[1][6]))
        self.wait(2)
        self.play(a3.animate.move_to(self.cell_mobjects[2][3]), b3.animate.move_to(self.cell_mobjects[2][6]))
        self.wait(2)

        self.play(g.animate.next_to(d, DOWN, buff=0.7).shift(LEFT*0.6))
        edge_g_d = always_redraw(lambda: Line(d.get_center(), g.get_center(), stroke_width=8).set_color(DARK_BLUE).set_z_index(-1))
        self.play(ShowCreation(edge_g_d))

        self.wait(2)



        row_idx = 2  # second row in the data
        col_idx = 3  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "1"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.85)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)

        self.play(a3.animate.move_to(self.cell_mobjects[1][3]), b3.animate.move_to(self.cell_mobjects[1][6]))
        self.wait()


        row_idx = 1  # second row in the data
        col_idx = 6  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "D"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.75)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)

        self.play(d[0].animate.set_fill(YELLOW), g[0].animate.set_fill(YELLOW))
        self.wait()

        self.play(a3.animate.move_to(self.cell_mobjects[0][0]), b3.animate.move_to(self.cell_mobjects[0][3]))
        self.play(d[0].animate.set_fill(TEAL_B), a[0].animate.set_fill(TEAL_B))

        self.wait(1)

        self.play(a3.animate.move_to(self.cell_mobjects[1][0]), b3.animate.move_to(self.cell_mobjects[1][3]))
        self.wait(2)
        self.play(a3.animate.move_to(self.cell_mobjects[2][0]), b3.animate.move_to(self.cell_mobjects[2][3]))
        self.wait(2)
        edge_d_a = always_redraw(lambda: Line(d.get_center(), a.get_center(), stroke_width=8).set_color(DARK_BLUE).set_z_index(-1))
        self.play(ShowCreation(edge_d_a), g.animate.shift(RIGHT))
        self.play(VGroup(a,b,c).animate.shift(UP*0.53+RIGHT))
        self.play(VGroup(d,g).animate.shift(DOWN+LEFT))
        self.play(b.animate.shift(LEFT*0.3) , c.animate.shift(LEFT*0.75) , d.animate.shift(LEFT*0.85), g.animate.shift(LEFT*1.13))
        self.play(VGroup(a,b,c,d,g).animate.scale(0.88).shift(UP*0.3))

        self.wait(2)

        row_idx = 2  # second row in the data
        col_idx = 0  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "2"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.85)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)

        self.play(a3.animate.move_to(self.cell_mobjects[1][0]), b3.animate.move_to(self.cell_mobjects[1][3]))
        self.wait()


        row_idx = 1  # second row in the data
        col_idx = 3  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "A"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.75)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)

        self.play(d[0].animate.set_fill(YELLOW), a[0].animate.set_fill(YELLOW), FadeOut(a3), FadeOut(b3))

        self.wait(1)

        z = a
        x = b

        xx = Circle(radius=0.45, stroke_width=10).set_color("#FF0000").move_to(e)
        a3.move_to(self.cell_rect_mobjects[0][4])
        self.play(ShowCreation(xx), ShowCreation(a3))
        self.wait(2)
        self.play(a3.animate.move_to(self.cell_rect_mobjects[1][4]))

        self.wait(2)

        vv = Circle(radius=0.45, stroke_width=10).set_color("#FF0000").move_to(g).scale(0.88)

        self.play(Transform(xx,vv))
        self.play(a3.animate.move_to(self.cell_rect_mobjects[0][-1]))
        self.wait()
        self.play(a3.animate.move_to(self.cell_rect_mobjects[1][-1]))
        self.play(xx.animate.move_to(d))
        self.wait()
        self.play(a3.animate.move_to(self.cell_rect_mobjects[0][3]))
        self.play(a3.animate.move_to(self.cell_rect_mobjects[1][3]))
        self.wait()
        self.play(xx.animate.move_to(z))
        self.wait()
        self.play(FadeOut(xx))

        self.wait(4)

        edge_g_a = Line(g.get_center(), z.get_center(), stroke_width=8).set_color(DARK_BLUE).set_z_index(-1)

        self.play(x.animate.shift(LEFT*0.5), c.animate.shift(LEFT*0.5), d.animate.shift(RIGHT*0.4))

        self.wait(1)

        self.play(Uncreate(edge_g_d))
        self.play(ShowCreation(edge_g_a))
        self.wait()

        self.play(a3.animate.move_to(self.cell_rect_mobjects[1][-1]))

        row_idx = 1  # second row in the data
        col_idx = -1  # second column in the data
        old_mob = self.cell_mobjects[row_idx][col_idx]
        new_text = "A"

        new_mob = Text(
            new_text,
            color=BLACK,
            font_size=36
        ).move_to(old_mob.get_center()).set_color(BLACK).scale(0.75)

        # Animate the transformation
        self.play(Transform(old_mob, new_mob))
        self.wait(2)


        self.wait(2)




