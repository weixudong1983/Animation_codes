from manimlib import *


PURE_RED = "#FF0000"
PURE_GREEN = "#00FF00"
PURE_BLUE = "#0000FF"
DARK_BLUE = BLUE_E
TEAL_B, GREEN = GREEN, TEAL_B


class Array(VGroup):
    def __init__(self, array_size=5, **kwargs):
        super().__init__(**kwargs)
        self.array_size = array_size
        self.square_contents = [None] * array_size
        self.array_group = self.create_array()
        self.add(self.array_group)

    def create_element(self, text):
        square = Square(side_length=1.72, fill_opacity=1, fill_color=RED, color=BLACK)
        text = Text(text, font_size=44, color=BLACK).scale(0.8).set_color(BLACK)
        return VGroup(square, text)

    def create_array(self):
        squares = VGroup(*[Square(side_length=1.72, color=PURE_RED, stroke_width=6) for _ in range(self.array_size)])
        squares.arrange(RIGHT, buff=0)
        return VGroup(squares,)

    def update_element(self, scene, index, new_value):
        if 0 <= index < self.array_size:
            new_square = Square(side_length=1.72, fill_opacity=1, fill_color=YELLOW_C, color=DARK_BLUE)
            new_number = Text(str(new_value), color=BLACK)
            new_square.add(new_number)
            new_square.move_to(self.array_group[0][index].get_center())
            if self.square_contents[index] is None:
                scene.play(FadeIn(new_square))
            else:
                scene.play(Transform(self.square_contents[index], new_square))
            self.square_contents[index] = new_square
        else:
            scene.play(Indicate(self.array_group, color=RED))
            print(f"Index {index} is out of bounds")

    def append_element(self, scene, value):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.72, fill_opacity=1, fill_color=YELLOW, color=PURE_RED,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1).set_color(BLACK).scale(1.6)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                scene.play(ShowCreation(self.square_contents[i]))
                break
        else:
            pass

    def add_element(self, scene, value, color=TEAL_B):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.72, fill_opacity=1, fill_color=color, color=PURE_RED,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def pop_element(self, scene):
        for i in range(self.array_size - 1, -1, -1):
            if self.square_contents[i] is not None:
                scene.play(FadeOut(self.square_contents[i]))
                self.square_contents[i] = None
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def delete_from_front(self, scene):
        if self.square_contents[0] is not None:
            scene.play(FadeOut(self.square_contents[0]))
            self.square_contents[0] = None
            animations = []
            for i in range(1, self.array_size):
                if self.square_contents[i] is not None:
                    animations.append(
                        self.square_contents[i].animate.move_to(self.array_group[0][i - 1].get_center())
                    )
                    self.square_contents[i - 1] = self.square_contents[i]
                    self.square_contents[i] = None
            if animations:
                scene.play(*animations)
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def create_new_array(self, scene, new_size):
        new_array = Array(array_size=new_size)
        new_array.next_to(self, DOWN, buff=0.7)
        scene.play(ShowCreation(new_array))
        return new_array

    def transfer_elements_to_new_array(self, scene, new_array):
        for i, content in enumerate(self.square_contents):
            if content is not None:
                scene.play(Transform(content, new_array.array_group[0][i]))
                new_array.square_contents[i] = content
                self.square_contents[i] = None


class HeapSort(Scene):

    def construct(self):
        self.camera.frame.scale(1.2)

        # Define the node properties
        def create_node(value, position, color=YELLOW_C):
            circle = Circle(radius=0.68, color=PURE_RED, fill_opacity=1, fill_color=color, stroke_width=8).set_color(RED)
            text = Text(str(value), color=BLACK, font_size=66)
            text.move_to(circle.get_center())
            node = VGroup(circle, text).move_to(position)
            text.set_z_index(1)

            return node

        # Create the nodes
        root = create_node(2, UP * 3)
        left_child = create_node(5, UP * 1 + LEFT * 2.5)
        right_child = create_node(0, UP * 1 + RIGHT * 2.5)
        left_left_grandchild = create_node(3, DOWN*1.5 + LEFT * 4.5)
        left_right_grandchild = create_node(4, DOWN*1.5 + LEFT * 1)
        right_left_grandchild = create_node(1, DOWN*1.5 + RIGHT * 1)
        right_right_grandchild = create_node(9, DOWN*1.5 + RIGHT * 4.5)
        

        
        # Create the edges
        edge_left = Line(root.get_center(), left_child.get_center(), color=WHITE)
        edge_right = Line(root.get_center(), right_child.get_center(), color=WHITE)
        edge_left_left = Line(left_child.get_center(), left_left_grandchild.get_center(), color=WHITE)
        edge_left_right = Line(left_child.get_center(), left_right_grandchild.get_center(), color=WHITE)
        edge_right_left = Line(right_child.get_center(), right_left_grandchild.get_center(), color=WHITE)
        edge_right_right = Line(right_child.get_center(), right_right_grandchild.get_center(), color=WHITE)

        # Fourth level edges
     

        # Ensure edges are behind the nodes
        edges = [edge_left, edge_right, edge_left_left, edge_left_right, edge_right_left,edge_right_right]

        for edge in edges:
            edge.z_index = -1

             

        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN))

        # Example usage:
        array = Array(array_size=7).next_to(right_left_grandchild, DOWN).shift(DOWN * 0.8).shift(LEFT * 0.97 + DOWN*0.7)
        self.play(ShowCreation(array))

        array.append_element(self, "2")
        array.append_element(self, "5")
        array.append_element(self, "0")
        array.append_element(self, "3")
        array.append_element(self, "4")
        array.append_element(self, "1")
        array.append_element(self, "9")


        self.wait(2)

        node_list = [left_child, right_child, left_left_grandchild, left_right_grandchild, right_left_grandchild,
                     ]
        
        self.wait(2)

 


        # Animate the scene (optional)
        self.play(FadeIn(root),FadeIn(left_child), FadeIn(right_child),FadeIn(right_right_grandchild) ,FadeIn(left_left_grandchild), FadeIn(left_right_grandchild), FadeIn(right_left_grandchild) )
        self.play()
        self.play(ShowCreation(edge_left), ShowCreation(edge_right),
                  ShowCreation(edge_right_right), ShowCreation(edge_left_left), ShowCreation(edge_left_right), ShowCreation(edge_right_left),)


        self.wait(2)



        






        a = array.square_contents[2]
        b = array.square_contents[3]
        c = array.square_contents[0]
        d = array.square_contents[-1]

        self.play(Swap(a, b), Swap(c, d))

        array.square_contents[2], array.square_contents[3] = array.square_contents[3], array.square_contents[2]
        array.square_contents[0], array.square_contents[-1] = array.square_contents[-1], array.square_contents[0]

        self.wait(2)

        arrow1 = Arrow(start=root.get_center()+LEFT*1.9, end=root.get_center(), color=PURE_GREEN, stroke_width=7).shift(LEFT*0.8)
        arrow2 = Arrow(right_right_grandchild.get_center()+RIGHT*1.9, right_right_grandchild.get_center(), color=PURE_GREEN, stroke_width=7).shift(RIGHT*0.8)
        arrow3 = Arrow(left_left_grandchild.get_center()+LEFT*1.9, left_left_grandchild.get_center(), color=PURE_GREEN, stroke_width=7).shift(LEFT*0.8)
        arrow4 = Arrow(right_child.get_center()+RIGHT*1.9, right_child.get_center(), color=PURE_GREEN, stroke_width=7).shift(RIGHT*0.8)
        self.play(ShowCreation(arrow1), ShowCreation(arrow2), ShowCreation(arrow3), ShowCreation(arrow4))


        self.play(
            root[1].animate.become(Text("9", color=BLACK, font_size=66).move_to(root[1].get_center())),
            right_right_grandchild[1].animate.become(Text("2", color=BLACK, font_size=66).move_to(right_right_grandchild[1].get_center())),
            right_child[1].animate.become(Text("3", color=BLACK, font_size=66).move_to(right_child[1].get_center())),
            left_left_grandchild[1].animate.become(Text("0", color=BLACK, font_size=66).move_to(left_left_grandchild[1].get_center())),

        )

        self.wait()

        self.play(Uncreate(arrow1), Uncreate(arrow2), Uncreate(arrow3), Uncreate(arrow4))

        self.wait(2)


        self.play(
            root[0].animate.set_fill(TEAL_B, 1).set_color(TEAL_B),
            root[1].animate.set_color(BLACK),
            right_right_grandchild[0].animate.set_fill(GREEN, 1).set_color(GREEN),
            right_right_grandchild[1].animate.set_color(BLACK),
            array.square_contents[0][0].animate.set_fill(TEAL_B, 1),
            array.square_contents[-1][0].animate.set_fill(GREEN, 1),
            array.square_contents[-1][1].animate.set_color(BLACK),
                  )
        
        self.wait(2)

        self.play(
            Swap(array.square_contents[0], array.square_contents[-1]),
            Swap(root, right_right_grandchild),
        )

        array.square_contents[0], array.square_contents[-1] = array.square_contents[-1], array.square_contents[0]
        root, right_right_grandchild = right_right_grandchild, root

        self.wait(2)

        self.play(Uncreate(edge_right_right), Uncreate(right_right_grandchild), )

        self.wait(2)

        self.play(Swap(root, left_child))
        root, left_child = left_child, root
        self.play(Swap(array.square_contents[0], array.square_contents[1]))
        array.square_contents[0], array.square_contents[1] = array.square_contents[1], array.square_contents[0]
        self.wait()


        self.play(Swap(left_child, left_right_grandchild))
        left_child, left_right_grandchild = left_right_grandchild, left_child
        self.play(Swap(array.square_contents[1], array.square_contents[4]))
        array.square_contents[1], array.square_contents[4] = array.square_contents[4], array.square_contents[1]
        self.play(
            left_right_grandchild[0].animate.set_color(RED),
                  left_right_grandchild[1].animate.set_color(WHITE),
                  array.square_contents[4][0].animate.set_fill(YELLOW, 1),
                  array.square_contents[4][0].animate.set_fill(YELLOW, 1),
        )

        self.wait(2)



        #2nd iteration 

        self.play(
            root[0].animate.set_fill(TEAL_B, 1).set_color(TEAL_B),
            root[1].animate.set_color(BLACK),
            right_left_grandchild[0].animate.set_fill(GREEN, 1).set_color(GREEN),
            right_left_grandchild[1].animate.set_color(BLACK),
            array.square_contents[0][0].animate.set_fill(TEAL_B, 1),
            array.square_contents[-2][0].animate.set_fill(GREEN, 1),
            array.square_contents[-2][1].animate.set_color(BLACK),
                  )

        self.wait(2)

        self.play(
            Swap(array.square_contents[0], array.square_contents[-2]),
            Swap(root, right_left_grandchild),
        )

        array.square_contents[0], array.square_contents[-2] = array.square_contents[-2], array.square_contents[0]
        root, right_left_grandchild = right_left_grandchild, root

        self.wait(2)

        self.play(Uncreate(edge_right_left), Uncreate(right_left_grandchild), )

        self.wait(2)

        self.play(Swap(root, left_child))
        root, left_child = left_child, root
        self.play(Swap(array.square_contents[0], array.square_contents[1]))
        array.square_contents[0], array.square_contents[1] = array.square_contents[1], array.square_contents[0]
        self.wait()


        self.play(Swap(left_child, left_right_grandchild))
        left_child, left_right_grandchild = left_right_grandchild, left_child
        self.play(Swap(array.square_contents[1], array.square_contents[4]))
        array.square_contents[1], array.square_contents[4] = array.square_contents[4], array.square_contents[1]

        self.play(
            left_right_grandchild[0].animate.set_color(RED),
                  left_right_grandchild[1].animate.set_color(WHITE),
                  array.square_contents[4][0].animate.set_fill(YELLOW, 1),
                  array.square_contents[4][0].animate.set_fill(YELLOW, 1),
        )

        self.wait(2)

  

        # 3rd iteration     


        self.play(
            root[0].animate.set_fill(TEAL_B, 1).set_color(TEAL_B),
            root[1].animate.set_color(BLACK),
            left_right_grandchild[0].animate.set_fill(GREEN, 1).set_color(GREEN),
            left_right_grandchild[1].animate.set_color(BLACK),
            array.square_contents[0][0].animate.set_fill(TEAL_B, 1),
            array.square_contents[-3][0].animate.set_fill(GREEN, 1),
            array.square_contents[-3][1].animate.set_color(BLACK),
                  )

        self.wait(2)

        self.play(
            Swap(array.square_contents[0], array.square_contents[4]),
            Swap(root, left_right_grandchild),
        )

        self.wait()

        array.square_contents[0], array.square_contents[4] = array.square_contents[4], array.square_contents[0]
        root, left_right_grandchild = left_right_grandchild, root


        self.play(Uncreate(edge_left_right), Uncreate(left_right_grandchild), )

        self.wait()  




        self.play(Swap(root, right_child))
        root, right_child = right_child, root
        self.play(Swap(array.square_contents[0], array.square_contents[2]))
        array.square_contents[0], array.square_contents[2] = array.square_contents[2], array.square_contents[0]
        self.wait()


        self.play(
            right_child[0].animate.set_color(RED),
            right_child[1].animate.set_color(WHITE),
                  array.square_contents[2][0].animate.set_fill(YELLOW, 1),
      )

        self.wait(2)


        #4th iteration




        self.play(
            root[0].animate.set_fill(TEAL_B, 1).set_color(TEAL_B),
            root[1].animate.set_color(BLACK),
            left_left_grandchild[0].animate.set_fill(GREEN, 1).set_color(GREEN),
            left_left_grandchild[1].animate.set_color(BLACK),
            array.square_contents[0][0].animate.set_fill(TEAL_B, 1),
            array.square_contents[3][0].animate.set_fill(GREEN, 1),
            array.square_contents[3][1].animate.set_color(BLACK),
                  )

        self.wait()

        self.play(
            Swap(array.square_contents[0], array.square_contents[3]),
            Swap(root, left_left_grandchild),
        )


        array.square_contents[0], array.square_contents[3] = array.square_contents[3], array.square_contents[0]
        root, left_left_grandchild = left_left_grandchild, root


        self.play(Uncreate(edge_left_left), Uncreate(left_left_grandchild), )

        self.wait()  



        self.play(Swap(root, left_child))
        root, left_child = left_child, root
        self.play(Swap(array.square_contents[0], array.square_contents[1]))
        array.square_contents[0], array.square_contents[1] = array.square_contents[1], array.square_contents[0]
        self.wait()



        self.play(
            left_child[0].animate.set_color(RED),
            left_child[1].animate.set_color(WHITE),
                  array.square_contents[1][0].animate.set_fill(YELLOW, 1),
      )

        self.wait(2)

        # Finfth iteration
        self.play(
            root[0].animate.set_fill(TEAL_B, 1).set_color(TEAL_B),
            root[1].animate.set_color(BLACK),
            right_child[0].animate.set_fill(GREEN, 1).set_color(GREEN),
            right_child[1].animate.set_color(BLACK),
            array.square_contents[0][0].animate.set_fill(TEAL_B, 1),
            array.square_contents[2][0].animate.set_fill(GREEN, 1),
            array.square_contents[2][1].animate.set_color(BLACK),
                  )

        self.play(
            Swap(array.square_contents[0], array.square_contents[2]),
            Swap(root, right_child),
        )

        array.square_contents[0], array.square_contents[2] = array.square_contents[2], array.square_contents[0]
        root, right_child = right_child, root

        self.play(Uncreate(edge_right), Uncreate(right_child), )

        self.play(
            root[0].animate.set_color(RED),
            root[1].animate.set_color(WHITE),
            )
        
        self.play(
            array.square_contents[0][0].animate.set_fill(YELLOW, 1),
        )

        self.wait(1)


        #Final iteration


        self.play(
            root[0].animate.set_fill(TEAL_B, 1).set_color(TEAL_B),
            root[1].animate.set_color(BLACK),
            left_child[0].animate.set_fill(GREEN, 1).set_color(GREEN),
            left_child[1].animate.set_color(BLACK),
            array.square_contents[0][0].animate.set_fill(TEAL_B, 1),
            array.square_contents[1][0].animate.set_fill(GREEN, 1),
            array.square_contents[1][1].animate.set_color(BLACK),
                  )
        
        self.wait()


        self.play(
            Swap(array.square_contents[0], array.square_contents[1]),
            Swap(root, left_child),
        )

        array.square_contents[0], array.square_contents[1] = array.square_contents[1], array.square_contents[0]
        root, left_child = left_child, root

        self.play(Uncreate(edge_left), Uncreate(left_child), )

        self.wait(1)

        self.play(
            root[0].animate.set_color(TEAL_B),
            array.square_contents[0][0].animate.set_fill(TEAL_B, 1),
        )

        self.wait()

        self.play(FadeOut(root))

        self.play(
            self.camera.frame.animate.shift(DOWN*3.6).scale(0.7)
        )

        self.wait(2)

        title = Text("Time Complexity").next_to(array, UP).shift(UP * 1.42 + LEFT*14).scale(1.5).set_color(PURE_GREEN)
        self.play(
            Write(title),
                  self.camera.frame.animate.shift(LEFT*14))
        
        self.wait(1)

        a = Text("O(n) + O(n)*O(log(n))").next_to(title, DOWN).shift(DOWN * 0.5 ).scale(1.2)
        self.play(Write(a))
        self.wait(3)

        brace = Brace(a[:4], DOWN, buff=0.4).set_color(YELLOW)
        brace_text = Text("Build Heap", font_size=36).next_to(brace, DOWN, buff=0.5)

        self.play(ShowCreation(brace), ShowCreation(brace_text))

        temp_brace = Brace(a[5:9], DOWN, buff=0.4).set_color(YELLOW)
        temp_brace_text = Text("Iteration", font_size=36).next_to(temp_brace, DOWN, buff=0.5)

        self.play(Transform(brace, temp_brace), Transform(brace_text, temp_brace_text))

        self.wait(2.5)

        temp_brace = Brace(a[10:], DOWN, buff=0.4).set_color(YELLOW)
        temp_brace_text = Text("Heapify", font_size=36).next_to(temp_brace, DOWN, buff=0.5)

        self.play(Transform(brace, temp_brace), Transform(brace_text, temp_brace_text))

        self.wait(2.5)

        self.play(FadeOut(brace), FadeOut(brace_text))

        space_title = Text("Space Complexity").next_to(a, DOWN).shift(DOWN * 0.9).scale(1.5).set_color(PURE_GREEN)
        self.play(Write(space_title))
        self.wait(1)

        space_text = Text("O(1)", font_size=36).next_to(space_title, DOWN).shift(DOWN * 0.8).scale(1.8)
        self.play(Write(space_text))

        self.wait(3)





    

       
