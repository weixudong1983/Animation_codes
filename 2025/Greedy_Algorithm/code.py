from manimlib import *

class Greedy(Scene):

    def construct(self):
        self.camera.frame.scale(0.78).shift(UP*0.65)
        # Define positions for each node in the tree
        positions = {
            "root": ORIGIN + UP * 3,                           # (Start)
            "L1": ORIGIN + UP * 1.5 + LEFT * 2,                # Left child of root
            "R1": ORIGIN + UP * 1.5 + RIGHT * 2,               # Right child of root
            "LL2": ORIGIN + LEFT * 3,                          # Left child of L1
            "LR2": ORIGIN + LEFT * 1,                          # Right child of L1
            "RL2": ORIGIN + RIGHT * 1,                         # Left child of R1
            "RR2": ORIGIN + RIGHT * 3,                         # Right child of R1
            "LLL3": ORIGIN + LEFT * 3.5 + DOWN * 1.5,          # Left child of LL2
            "LLR3": ORIGIN + LEFT * 2.5 + DOWN * 1.5,          # Right child of LL2
            "LRL3": ORIGIN + LEFT * 1.5 + DOWN * 1.5,          # Left child of LR2
            "LRR3": ORIGIN + LEFT * 0.5 + DOWN * 1.5,          # Right child of LR2
            "RLL3": ORIGIN + RIGHT * 0.5 + DOWN * 1.5,         # Left child of RL2
            "RLR3": ORIGIN + RIGHT * 1.5 + DOWN * 1.5,         # Right child of RL2
            "RRL3": ORIGIN + RIGHT * 2.5 + DOWN * 1.5,         # Left child of RR2
            "RRR3": ORIGIN + RIGHT * 3.5 + DOWN * 1.5,         # Right child of RR2
        }

        # Create nodes. The root gets labeled "Start" and is moved slightly up
        nodes = {}
        start = None
        for key, pos in positions.items():
            if key == "root":
                label = Text("", font_size=24).set_color(BLACK)
            else:
                label = Text("", font_size=24).set_color(BLACK)
            label.move_to(pos)
            node = VGroup(label)
            nodes[key] = node
            start = label

        # Add all the nodes to the scene
        for node in nodes.values():
            self.add(node)

        # Define edges between nodes as tuples: (start_node, end_node, weight)
        edges = [
            ("root", "L1", "4"),
            ("root", "R1", "2"),
            ("L1", "LL2", "1"),
            ("L1", "LR2", "3"),
            ("R1", "RL2", "5"),
            ("R1", "RR2", "6"),
            ("LL2", "LLL3", "7"),
            ("LL2", "LLR3", "9"),
            ("LR2", "LRL3", "8"),
            ("LR2", "LRR3", "2"),
            ("RL2", "RLL3", "3"),
            ("RL2", "RLR3", "4"),
            ("RR2", "RRL3", "1"),
            ("RR2", "RRR3", "5"),
        ]

        # Dictionary to store weight labels
        self.weight_labels = {}

        # Draw edges and label them with offset weights
        for start_key, end_key, weight in edges:
            start_pos = positions[start_key]
            end_pos = positions[end_key]
            
            # Draw the edge as a black line
            edge_line = Line(start_pos, end_pos, color=BLACK)
            self.play(ShowCreation(edge_line), run_time=0.15)
            
            # Calculate midpoint
            mid_point = (start_pos + end_pos) / 2
            
            # Determine if this is a left or right edge
            is_left_edge = end_pos[0] < start_pos[0]
            
            # Offset the weight label based on whether it's a left or right edge
            offset = LEFT * 0.3 if is_left_edge else RIGHT * 0.3
            weight_label = Text(weight, font_size=20).move_to(mid_point + offset).set_color(BLACK)
            self.play(Write(weight_label), run_time=0.15)
            
            # Store the weight label
            label_key = f"{start_key}_{end_key}"
            self.weight_labels[label_key] = weight_label

        self.wait(3)

        # Add a decorative floor line
        floor_y = min(pos[1] for pos in positions.values()) - 0.5
        floor_left_x = min(pos[0] for pos in positions.values()) - 1
        floor_right_x = max(pos[0] for pos in positions.values()) + 1
        
        # Create main floor line
        floor_line = Line(
            LEFT * abs(floor_left_x) + DOWN * abs(floor_y),
            RIGHT * abs(floor_right_x) + DOWN * abs(floor_y),
            color=GREY_E
        )

        temp =[]
        
        # Add some decorative parallel lines to create a "reflection" effect
        for i in range(1, 4):
            reflection_line = Line(
                LEFT * abs(floor_left_x) + DOWN * (abs(floor_y) + i * 0.1),
                RIGHT * abs(floor_right_x) + DOWN * (abs(floor_y) + i * 0.1),
                color=GREY_E,
                stroke_opacity=0.5 / i
            )
            temp.append(ShowCreation(reflection_line))
        
        temp.append(ShowCreation(floor_line))
        self.play(*temp, run_time=0.8)

        self.wait(2)

        start = Text("Bob", font_size=24).set_color(BLACK).to_edge(UP)
        self.play(Write(start), run_time=0.5)
        self.wait(2)

        # Highlight the left weight (root to L1)
        left_weight = self.weight_labels["root_L1"]
        right_weight = self.weight_labels["root_R1"]

        circle1 = Circle(stroke_color="#0000FF", stroke_width=7).move_to(left_weight).scale(0.3)
        circle2 = Circle(stroke_color="#0000FF", stroke_width=7).move_to(right_weight).scale(0.3)
        self.play(ShowCreation(circle1),ShowCreation(circle2),)
        self.wait(2)
        self.play(Uncreate(circle1),Uncreate(circle2),) 

        line_right = Line(start=positions["root"], end=positions["R1"], color="#FF0000", stroke_width=7)
        self.play(ShowCreation(line_right), start.animate.move_to(positions["R1"]+RIGHT*0.6+UP*0.15),
        self.camera.frame.animate.shift(DOWN*0.15))

        self.wait(1)

        line_right_left = Line(start=positions["R1"], end=positions["RL2"], color="#FF0000", stroke_width=7)
        self.play(ShowCreation(line_right_left),
        start.animate.move_to(positions["RL2"]+RIGHT*0.5))

        self.wait(2)

        line_right_left1 = Line(start=positions["RL2"], end=positions["RLL3"], color="#FF0000", stroke_width=7)
        self.play(ShowCreation(line_right_left1), start.animate.move_to(positions["RLL3"]+DOWN*0.23),)

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*0.6))
        self.wait(2)

        temp = self.weight_labels["root_R1"]
        temp1 = self.weight_labels["R1_RL2"]
        temp2 = self.weight_labels["RL2_RLL3"]


        text = Text("2 + 5 + 3", font_size=24).set_color(BLACK).to_edge(RIGHT).shift(LEFT*1.5+UP*2)
        self.play(FadeIn(Group(text[1], text[3])),
        TransformFromCopy(temp, text[0]),TransformFromCopy(temp1, text[2]),
        TransformFromCopy(temp2, text[4]),)

        self.wait(2)

        self.play(text.animate.become(Text("10", font_size=24).set_color(BLACK).move_to(text).scale(1.2)),)
        self.wait(2)
        self.play(FadeOut(text))
        self.wait(1)

        line = Line(start=positions["root"], end=positions["L1"], color="#00FF00", stroke_width=7)
        line1 = Line(start=positions["L1"], end=positions["LR2"], color="#00FF00", stroke_width=7)
        line2 = Line(start=positions["LR2"], end=positions["LRR3"], color="#00FF00", stroke_width=7)

        self.play(ShowCreation(line))
        self.play(ShowCreation(line1))
        self.play(ShowCreation(line2))

        temp = self.weight_labels["root_L1"]
        temp1 = self.weight_labels["L1_LR2"]
        temp2 = self.weight_labels["LR2_LRR3"]


        text = Text("4 + 3 + 2", font_size=24).set_color(BLACK).to_edge(RIGHT).shift(LEFT*1.5+UP*2)
        self.play(FadeIn(Group(text[1], text[3])),
        TransformFromCopy(temp, text[0]),TransformFromCopy(temp1, text[2]),
        TransformFromCopy(temp2, text[4]),)

        self.wait(2)

        self.play(text.animate.become(Text("9", font_size=24).set_color(BLACK).move_to(text).scale(1.2)),)
        self.wait(2)
        self.wait(1)



        self.embed()
