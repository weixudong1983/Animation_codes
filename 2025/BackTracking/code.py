from manimlib import *

PURE_RED = "#FF0000"
PURE_GREEN = "#00FF00"
PURE_BLUE = "#0000FF"
DARK_BLUE = BLUE_E
GREEN = PURPLE

class BackTrackingDemo(Scene):
    
    def construct(self):

        self.camera.frame.scale(1).shift(UP*0.47)
        
        # Define the node properties
        def create_node(value, position, color=RED):
            circle = Circle(radius=0.68, color=color, fill_opacity=1, fill_color=color, stroke_width=8).set_color(RED)
            text = Text(str(value), color=BLACK, font_size=66)
            text.move_to(circle.get_center())
            node = VGroup(circle, text).move_to(position)
            text.set_z_index(1)
            
            return node
        
        # Create the nodes - Level 1 (Root)
        root = create_node(2, UP * 3)
        
        # Level 2 - Wider spacing
        left_child = create_node(5, UP * 1 + LEFT * 3.5)
        right_child = create_node(0, UP * 1 + RIGHT * 3.5)
        
        # Level 3 - More symmetric positioning
        left_left_grandchild = create_node(3, DOWN*1 + LEFT * 5.5)
        left_right_grandchild = create_node(4, DOWN*1 + LEFT * 1.5)
        right_left_grandchild = create_node(1, DOWN*1 + RIGHT * 1.5)
        right_right_grandchild = create_node(9, DOWN*1 + RIGHT * 5.5)
        
        # Level 4 - Symmetric alignment under each parent
        # Children of left_left_grandchild (3)
        ll_left_child = create_node(7, DOWN*3.5 + LEFT * 6.5)
        ll_right_child = create_node(8, DOWN*3.5 + LEFT * 4.5)
        
        # Children of left_right_grandchild (4)
        lr_left_child = create_node(6, DOWN*3.5 + LEFT * 2.5)
        
        # Children of right_left_grandchild (1)
        rl_left_child = create_node(5, DOWN*3.5 + RIGHT * 0.5, color=PURE_GREEN)
        rl_left_child[0].set_fill(GREEN, opacity=1).set_color(GREEN)
        rl_left_child[1].set_color(BLACK)
        rl_right_child = create_node(1, DOWN*3.5 + RIGHT * 2.5)
        
        # Children of right_right_grandchild (9)
        rr_left_child = create_node(3, DOWN*3.5 + RIGHT * 4.5)
        rr_right_child = create_node(4, DOWN*3.5 + RIGHT * 6.5)
        
        # Create the edges - Level 1 to 2
        edge_left = Line(root.get_center(), left_child.get_center(), color=WHITE)
        edge_right = Line(root.get_center(), right_child.get_center(), color=WHITE)
        
        # Level 2 to 3
        edge_left_left = Line(left_child.get_center(), left_left_grandchild.get_center(), color=WHITE)
        edge_left_right = Line(left_child.get_center(), left_right_grandchild.get_center(), color=WHITE)
        edge_right_left = Line(right_child.get_center(), right_left_grandchild.get_center(), color=WHITE)
        edge_right_right = Line(right_child.get_center(), right_right_grandchild.get_center(), color=WHITE)
        
        # Level 3 to 4 (New edges)
        edge_ll_left = Line(left_left_grandchild.get_center(), ll_left_child.get_center(), color=WHITE)
        edge_ll_right = Line(left_left_grandchild.get_center(), ll_right_child.get_center(), color=WHITE)
        edge_lr_left = Line(left_right_grandchild.get_center(), lr_left_child.get_center(), color=WHITE)
        edge_rl_left = Line(right_left_grandchild.get_center(), rl_left_child.get_center(), color=WHITE)
        edge_rl_right = Line(right_left_grandchild.get_center(), rl_right_child.get_center(), color=WHITE)
        edge_rr_left = Line(right_right_grandchild.get_center(), rr_left_child.get_center(), color=WHITE)
        edge_rr_right = Line(right_right_grandchild.get_center(), rr_right_child.get_center(), color=WHITE)
        
        # Ensure edges are behind the nodes
        edges = [edge_left, edge_right, edge_left_left, edge_left_right, edge_right_left, edge_right_right,
                edge_ll_left, edge_ll_right, edge_lr_left, 
                edge_rl_left, edge_rl_right, edge_rr_left, edge_rr_right]
        
        for edge in edges:
            edge.z_index = -2.2
                    
        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN))
        
        # Updated node list including new level 4 nodes
        node_list = [left_child, right_child, left_left_grandchild, left_right_grandchild, 
                    right_left_grandchild, right_right_grandchild,
                    ll_left_child, ll_right_child, lr_left_child,
                    rl_left_child, rl_right_child, rr_left_child, rr_right_child]
                
        self.wait(2)
        
        # Animate the scene - Fade in all nodes
        self.play(FadeIn(root), FadeIn(left_child), FadeIn(right_child), FadeIn(right_right_grandchild),
                 FadeIn(left_left_grandchild), FadeIn(left_right_grandchild), FadeIn(right_left_grandchild),
                 FadeIn(ll_left_child), FadeIn(ll_right_child), FadeIn(lr_left_child), 
                 FadeIn(rl_left_child), FadeIn(rl_right_child), FadeIn(rr_left_child), FadeIn(rr_right_child))
        
        self.play()
        
        # Animate the edges
        self.play(ShowCreation(edge_left), ShowCreation(edge_right),
                 ShowCreation(edge_right_right), ShowCreation(edge_left_left), 
                 ShowCreation(edge_left_right), ShowCreation(edge_right_left),
                 ShowCreation(edge_ll_left), ShowCreation(edge_ll_right),
                 ShowCreation(edge_lr_left), 
                 ShowCreation(edge_rl_left), ShowCreation(edge_rl_right),
                 ShowCreation(edge_rr_left), ShowCreation(edge_rr_right))
         
        self.wait(2)

        a = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(root).set_z_index(2).set_color(YELLOW_C)

        self.play(ShowCreation(a))

        a_line = Line(
            start=a.get_center(),
            end=left_child.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)

        self.play(ShowCreation(a_line))

        b = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(left_child).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(b))

        b_line = Line(
            start=b.get_center(),
            end=left_left_grandchild.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)

        self.play(ShowCreation(b_line))

        c = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(left_left_grandchild).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(c))


        c_line = Line(
            start=c.get_center(),
            end=ll_left_child.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)

        self.play(ShowCreation(c_line))

        d = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(ll_left_child).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(d))

        self.wait(2)

        self.play(Uncreate(d))
        self.play(Uncreate(c_line))

        c_line = Line(
            start=c.get_center(),
            end=ll_right_child.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)

        self.play(ShowCreation(c_line))

        d = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(ll_right_child).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(d))

        self.wait(2)

        self.play(Uncreate(d))
        self.play(Uncreate(c_line))
        self.play(Uncreate(c))
        self.play(Uncreate(b_line))

        b_line = Line(
            start=b.get_center(),
            end=left_right_grandchild.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)

        self.play(ShowCreation(b_line))
        c = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(left_right_grandchild).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(c))

        c_line = Line(
            start=c.get_center(),
            end=lr_left_child.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)
        self.play(ShowCreation(c_line))
        d = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(lr_left_child).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(d))

        self.wait(2)

        self.play(Uncreate(d))
        self.play(Uncreate(c_line))
        self.play(Uncreate(c))
        self.play(Uncreate(b_line))
        self.play(Uncreate(b))
        self.play(Uncreate(a_line))

        a_line = Line(
            start=a.get_center(),
            end=right_child.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)
        self.play(ShowCreation(a_line))

        b = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(right_child).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(b))

        b_line = Line(
            start=b.get_center(),
            end=right_left_grandchild.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)
        self.play(ShowCreation(b_line))

        c = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(right_left_grandchild).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(c))

        c_line = Line(
            start=c.get_center(),
            end=rl_left_child.get_center(),
            stroke_width=11,
            color=YELLOW_C,
        ).set_z_index(-2)
        self.play(ShowCreation(c_line))

        d = Circle(radius=0.68, fill_opacity=0, stroke_width=11).move_to(rl_left_child).set_z_index(2).set_color(YELLOW_C)
        self.play(ShowCreation(d))


        self.wait(2)



class CombinationSum(Scene):
    def construct(self):

        title = Text("Combination Sum | Leetcode 39", font_size=48, color=PURE_RED).to_edge(UP).shift(DOWN*0.44)
        self.play(Write(title))

        text = Text("[2, 3, 5]").scale(1.3).shift(LEFT*2.75 + UP*0.5)
        self.play(Write(text))
        self.wait(2)

        target = Text("Target: 8", font_size=36, color=PURE_BLUE).next_to(text, RIGHT, buff=1).scale(1.5*1.1).shift(RIGHT)
        self.play(Write(target))
        self.wait(2)


        text1 = Text("Repitition is allowed", font_size=36, color=PURE_GREEN).next_to(target, DOWN).scale(1.45).shift(DOWN*0.89 + LEFT*2.55)
        self.play(Write(text1))
        text2 = Text("Order does not matter", font_size=36, color=PURE_GREEN).next_to(text1, DOWN).scale(1.45).shift(DOWN*0.49)
        self.play(Write(text2))

        self.wait(2)

        self.play(FadeOut(text1), FadeOut(text2))
        



        text1 = Text("2 + 2 + 2 + 2", font_size=36, color=PURE_GREEN).next_to(text, DOWN).scale(1.7).shift(DOWN*1.55+RIGHT*2.59)        
        self.play(Write(text1))
        self.wait(2)
        text2 = Text("2 + 3 + 3", font_size=36, color=PURE_GREEN).move_to(text1).scale(1.7)
        self.play(TransformMatchingTex(text1, text2), run_time=0.5)
        self.wait(1)

        text1 = Text("3 + 5", font_size=36, color=PURE_GREEN).move_to(text2).scale(1.7)
        self.play(TransformMatchingTex(text2, text1), run_time=0.5)
        self.wait(2)

