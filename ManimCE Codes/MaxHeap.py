from manim import *

config.background_color = "#173340"


class Array(VGroup):
    def __init__(self, array_size=5, **kwargs):
        super().__init__(**kwargs)
        self.array_size = array_size
        self.square_contents = [None] * array_size
        self.array_group = self.create_array()
        self.add(self.array_group)

    def create_element(self, text):
        square = Square(side_length=1.22, fill_opacity=1, fill_color=RED, color=BLACK)
        text = Text(text, font_size=44, color=BLACK).scale(0.8)
        return VGroup(square, text)

    def create_array(self):
        squares = VGroup(*[Square(side_length=1.22, color=PURE_RED, stroke_width=6) for _ in range(self.array_size)])
        squares.arrange(RIGHT, buff=0)
        index_labels = VGroup(
            *[Text(str(i), font_size=30).next_to(square, DOWN, buff=0.23) for i, square in enumerate(squares)]
        )
        return VGroup(squares, index_labels)

    def update_element(self, scene, index, new_value):
        if 0 <= index < self.array_size:
            new_square = Square(side_length=1.12, fill_opacity=1, fill_color=YELLOW_C, color=DARK_BLUE)
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
                new_square = Square(side_length=1.22, fill_opacity=1, fill_color=ORANGE, color=PURE_RED,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def add_element(self, scene, value, color=TEAL_B):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.22, fill_opacity=1, fill_color=color, color=PURE_RED,
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
        scene.play(Create(new_array))
        return new_array

    def transfer_elements_to_new_array(self, scene, new_array):
        for i, content in enumerate(self.square_contents):
            if content is not None:
                scene.play(Transform(content, new_array.array_group[0][i]))
                new_array.square_contents[i] = content
                self.square_contents[i] = None


class Heap(MovingCameraScene):

    def construct(self):
        self.camera.frame.scale(1.2)

        # Define the node properties
        def create_node(value, position, color=YELLOW_C):
            circle = Circle(radius=0.6, color=PURE_RED, fill_opacity=1, fill_color=color, stroke_width=8)
            text = Text(str(value), color=BLACK, font_size=46)
            text.move_to(circle.get_center())
            node = VGroup(circle, text).move_to(position)
            text.set_z_index(1)

            return node

        # Create the nodes
        root = create_node(50, UP * 3.5)
        left_child = create_node(40, UP * 1.5 + LEFT * 2.5)
        right_child = create_node(30, UP * 1.5 + RIGHT * 2.5)
        left_left_grandchild = create_node(17, DOWN + LEFT * 4.5)
        left_right_grandchild = create_node(13, DOWN + LEFT * 1)
        right_left_grandchild = create_node(12, DOWN + RIGHT * 1)
        right_right_grandchild = create_node(11, DOWN + RIGHT * 4.3)

        # Fourth level nodes
        left_left_left_greatgrandchild = create_node(7, LEFT * 5.5 + DOWN * 3.5)
        left_left_right_greatgrandchild = create_node(4, LEFT * 3.5 + DOWN * 3.5)
        left_right_left_greatgrandchild = create_node(6, LEFT * 2 + DOWN * 3.5)
        left_right_right_greatgrandchild = create_node(43, LEFT * 0.06 + DOWN * 3.5, color=ORANGE)
        right_left_left_greatgrandchild = create_node(11, RIGHT * 0.2 + DOWN * 3.5)
        # right_left_right_greatgrandchild = create_node(13, RIGHT * 2 + DOWN * 3.5)
        # right_right_left_greatgrandchild = create_node(17, RIGHT * 3.5 + DOWN * 3.5)
        right_right_right_greatgrandchild = create_node(20, RIGHT * 5.5 + DOWN * 3.5)

        # Create the edges
        edge_left = Line(root.get_center(), left_child.get_center(), color=WHITE)
        edge_right = Line(root.get_center(), right_child.get_center(), color=WHITE)
        edge_left_left = Line(left_child.get_center(), left_left_grandchild.get_center(), color=WHITE)
        edge_left_right = Line(left_child.get_center(), left_right_grandchild.get_center(), color=WHITE)
        edge_right_left = Line(right_child.get_center(), right_left_grandchild.get_center(), color=WHITE)
        edge_right_right = Line(right_child.get_center(), right_right_grandchild.get_center(), color=WHITE)

        # Fourth level edges
        edge_left_left_left = Line(left_left_grandchild.get_center(), left_left_left_greatgrandchild.get_center(),
                                   color=WHITE)
        edge_left_left_right = Line(left_left_grandchild.get_center(), left_left_right_greatgrandchild.get_center(),
                                    color=WHITE)
        edge_left_right_left = Line(left_right_grandchild.get_center(), left_right_left_greatgrandchild.get_center(),
                                    color=WHITE)
        edge_left_right_right = Line(left_right_grandchild.get_center(), left_right_right_greatgrandchild.get_center(),
                                     color=WHITE)
        edge_right_left_left = Line(right_left_grandchild.get_center(), right_left_left_greatgrandchild.get_center(),
                                    color=WHITE)

        # Ensure edges are behind the nodes
        edges = [edge_left, edge_right, edge_left_left, edge_left_right, edge_right_left, edge_right_right,
                 edge_left_left_left, edge_left_left_right, edge_left_right_left, edge_left_right_right,
                 edge_right_left_left, edge_left_right_right]

        for edge in edges:
            edge.z_index = -1

        # Animate the scene (optional)
        self.play(FadeIn(root), )
        self.play(FadeIn(left_child), FadeIn(right_child))
        self.play(Create(edge_left), Create(edge_right))
        self.play(FadeIn(left_left_grandchild), FadeIn(left_right_grandchild), FadeIn(right_left_grandchild),
                  FadeIn(right_right_grandchild))
        self.play(Create(edge_left_left), Create(edge_left_right), Create(edge_right_left), Create(edge_right_right))
        self.play(FadeIn(left_left_left_greatgrandchild), FadeIn(left_left_right_greatgrandchild),
                  )
        self.play(Create(edge_left_left_left), Create(edge_left_left_right),
                  )

        self.play(Create(left_right_left_greatgrandchild))
        self.play(Create(edge_left_right_left))

        # self.play(Create(left_right_right_greatgrandchild))
        # self.play(Create(edge_left_right_right))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN))

        # Example usage:
        array = Array(array_size=11).next_to(right_left_left_greatgrandchild, DOWN).shift(DOWN * 0.4).shift(LEFT * 0.52)
        self.play(Create(array))

        array.add_element(self, "50")
        array.add_element(self, "40")
        array.add_element(self, "30")
        array.add_element(self, "17")
        array.add_element(self, "13")
        array.add_element(self, "12")
        array.add_element(self, "11")
        array.add_element(self, "7")
        array.add_element(self, "4")
        array.add_element(self, "6")

        self.play(ReplacementTransform(root.copy(), array.square_contents[0]))

        self.wait(2)

        node_list = [left_child, right_child, left_left_grandchild, left_right_grandchild, right_left_grandchild,
                     right_right_grandchild,
                     left_left_left_greatgrandchild, left_left_right_greatgrandchild, left_right_left_greatgrandchild]

        for i in range(1, 10):
            self.play(ReplacementTransform(node_list[i - 1].copy(), array.square_contents[i]))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT * 1.8))

        first = MathTex("Parent = i").next_to(right_child, RIGHT).shift(RIGHT * 2.6).scale(1.2)
        second = MathTex("Left\\ Child = 2i + 1").next_to(first, DOWN).shift(RIGHT * 1.22).shift(DOWN * 0.32).scale(1.2)
        third = MathTex("Right\\ Child = 2i + 2").next_to(second, DOWN).shift(RIGHT * 0.2).shift(DOWN * 0.32).scale(1.2)
        fourth = MathTex("i = \\frac{i_c - 1}{2}").next_to(third, DOWN).shift(DOWN * 0.32).scale(1.2).shift(LEFT * 1.39)

        self.play(Create(first))
        self.play(Create(second))
        self.play(Create(third))
        self.play(Create(fourth))

        self.wait(2)

        a = Circle(radius=0.6, stroke_width=12, color=PURE_BLUE, ).move_to(right_child)

        self.play(Create(a))

        self.wait(2)

        self.play(first[0][-1].animate.become(MathTex("2").move_to(first[0][-1])))
        self.wait(1)

        self.play(array.square_contents[2][0].animate.set_fill(YELLOW))
        self.play(array.square_contents[2][0].animate.set_fill(TEAL_B))

        self.wait(2)

        self.play(a.animate.move_to(right_left_grandchild))
        self.play(second[0][-4:].animate.become(MathTex("5").move_to(second[0][-4])))
        self.play(array.square_contents[5][0].animate.set_fill(YELLOW))
        self.play(array.square_contents[5][0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(a.animate.move_to(right_right_grandchild))

        self.play(third[0][-4:].animate.become(MathTex("6").move_to(third[0][-4])))
        self.play(array.square_contents[6][0].animate.set_fill(YELLOW))
        self.play(array.square_contents[6][0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(a.animate.move_to(root))

        self.play(fourth[0][2:4].animate.become(MathTex("2").scale(1.2).move_to(fourth[0][2:4])))
        self.wait()
        self.play(fourth[0][2:].animate.become(
            MathTex("0.5").move_to(fourth[2:]).scale(1.2).move_to(fourth[0][2:]).shift(LEFT * 0.27)))
        self.wait()
        self.play(fourth[0][2:].animate.become(MathTex("0").move_to(fourth[2:]).scale(1.2).move_to(fourth[0][2:])))
        self.wait(2)

        self.play(Uncreate(a))
        self.play(FadeOut(first, second, third, fourth))
        self.play(self.camera.frame.animate.shift(LEFT * 1.8))

        self.wait(2)

        brace = Brace(VGroup(root, right_right_right_greatgrandchild, right_right_grandchild), direction=RIGHT)

        # Label the brace with "O(log n)"
        label = brace.get_tex("\\log n")

        self.play(Create(brace))

        self.play(Create(label))

        self.wait(2)

        self.play(FadeOut(brace, label))

        self.wait(2)

        array.add_element(self, "43", color=ORANGE)
        self.play(FadeIn(array.square_contents[-1]))

        self.wait(2)

        self.play(Create(left_right_right_greatgrandchild))
        self.play(Create(edge_left_right_right))

        self.wait(2)

        self.play(Indicate(VGroup(left_right_grandchild, left_right_right_greatgrandchild, edge_left_right_right),
                           color=PURE_RED))

        self.wait(2)

        self.play(Swap(left_right_grandchild[1], left_right_right_greatgrandchild[1]),
                  left_right_grandchild[0].animate.set_fill(ORANGE),
                  left_right_right_greatgrandchild[0].animate.set_fill(YELLOW_C))
        left_right_grandchild[1], left_right_right_greatgrandchild[1] = left_right_right_greatgrandchild[1], \
                                                                        left_right_grandchild[1]

        self.wait(2)

        self.play(array.square_contents[4][0].animate.set_fill(PINK))
        self.wait(2)

        self.play(Swap(array.square_contents[4], array.square_contents[-1]))
        self.play(array.square_contents[4][0].animate.set_fill(TEAL_B))
        array.square_contents[4], array.square_contents[-1] = array.square_contents[-1], array.square_contents[4]

        self.play(Indicate(VGroup(left_right_grandchild, left_child, edge_left_right),
                           color=PURE_RED))

        self.wait(2)

        self.play(Swap(left_child[1], left_right_grandchild[1]), left_right_grandchild[0].animate.set_fill(YELLOW_C),
                  left_child[0].animate.set_fill(ORANGE))
        left_right_grandchild[1], left_child[1] = left_child[1], \
                                                  left_right_grandchild[1]

        self.wait(2)

        self.play(array.square_contents[1][0].animate.set_fill(PINK))
        self.wait(2)

        self.play(Swap(array.square_contents[4], array.square_contents[1]))
        self.play(array.square_contents[1][0].animate.set_fill(TEAL_B))

        array.square_contents[4], array.square_contents[1] = array.square_contents[1], array.square_contents[4]

        self.wait(2)

        self.play(Indicate(VGroup(root, edge_left, left_child), color=PURE_GREEN))
        self.wait(1)
        self.play(left_child[0].animate.set_fill(YELLOW_C))
        self.wait(2)

        self.play(array.square_contents[0][0].animate.set_fill(PINK))
        self.wait(2)

        self.play(array.square_contents[0][0].animate.set_fill(TEAL_B),
                  array.square_contents[1][0].animate.set_fill(TEAL_B))

        self.wait(2)

        self.play(root[1].animate.become(Text(str(13), color=BLACK, font_size=46).move_to(root[1])),
                  root[0].animate.set_fill(ORANGE))
        self.play(
            array.square_contents[0][1].animate.become(Text(str(13), color=BLACK).move_to(array.square_contents[0][1])),
            array.square_contents[0][0].animate.set_fill(ORANGE))
        self.wait(2)
        self.play(Uncreate(edge_left_right_right))
        self.play(Uncreate(left_right_right_greatgrandchild))
        self.play(FadeOut(array.square_contents[-1]))

        self.wait(2)

        self.play(left_child[0].animate.set_fill(PINK), right_child[0].animate.set_fill(PINK),
                  array.square_contents[1][0].animate.set_fill(PINK),
                  array.square_contents[2][0].animate.set_fill(PINK)
                  )

        self.wait(1)

        self.play(right_child[0].animate.set_fill(YELLOW_C), array.square_contents[2][0].animate.set_fill(TEAL_B))
        self.wait(1)

        self.play(Swap(root[1], left_child[1]), left_child[0].animate.set_fill(ORANGE),
                  root[0].animate.set_fill(YELLOW_C), Swap(array.square_contents[0], array.square_contents[1]))
        root[1], left_child[1] = left_child[1], root[1]
        self.play(array.square_contents[1][0].animate.set_fill(TEAL_B))

        array.square_contents[0], array.square_contents[1] = array.square_contents[1], array.square_contents[0]

        self.wait(2)

        self.play(left_left_grandchild[0].animate.set_fill(PINK), left_right_grandchild[0].animate.set_fill(PINK),
                  array.square_contents[3][0].animate.set_fill(PINK),
                  array.square_contents[4][0].animate.set_fill(PINK)
                  )
        self.wait(1)

        self.play(left_left_grandchild[0].animate.set_fill(YELLOW_C),
                  array.square_contents[3][0].animate.set_fill(TEAL_B))
        self.wait(1)

        self.play(Swap(left_child[1], left_right_grandchild[1]),
                  left_right_grandchild[0].animate.set_fill(ORANGE), left_child[0].animate.set_fill(YELLOW_C),
                  Swap(array.square_contents[1], array.square_contents[4]))

        self.play(array.square_contents[4][0].animate.set_fill(TEAL_B), )

        left_right_grandchild[1], left_child[1] = left_child[1], left_right_grandchild[1]
        array.square_contents[1], array.square_contents[4] = array.square_contents[4], array.square_contents[1]

        self.wait(2)

        self.play(left_right_left_greatgrandchild[0].animate.set_fill(PINK), array.square_contents[-2][0].animate.set_fill(PINK))
        self.wait(2)
        self.play(Indicate(VGroup(left_right_grandchild, left_right_left_greatgrandchild, edge_left_right_left),
                           color=PURE_GREEN))
        self.wait(1)
        self.play(left_right_left_greatgrandchild[0].animate.set_fill(YELLOW_C),
                  left_right_grandchild[0].animate.set_fill(YELLOW_C),
                  array.square_contents[-2][0].animate.set_fill(TEAL_B),
                  array.square_contents[4][0].animate.set_fill(TEAL_B)
                  )

        self.wait(2)


        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT * 1.8))

        self.wait(2)

        # Label the brace with "O(log n)"
        label = brace.get_tex("O(\\log n)").scale(2)

        self.play(Create(label))

        self.wait(2)

        self.play(FadeOut(label))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT * 1.8))

        self.wait(2)
