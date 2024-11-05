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
                number = Text(str(value), color=BLACK, font_size=50).set_z_index(1)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                scene.play(FadeIn(new_square1))
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


class Heap123(MovingCameraScene):

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
        root = create_node(-1, UP * 3.5)
        left_child = create_node(1, UP * 1.5 + LEFT * 2.5)
        right_child = create_node(5, UP * 1.5 + RIGHT * 2.5)
        left_left_grandchild = create_node(0, DOWN + LEFT * 4.5)
        left_right_grandchild = create_node(0, DOWN + LEFT * 1)
        right_left_grandchild = create_node(4, DOWN + RIGHT * 1)
        right_right_grandchild = create_node(6, DOWN + RIGHT * 4.3)

        # Fourth level nodes
        left_left_left_greatgrandchild = create_node(7, LEFT * 5.5 + DOWN * 3.5)

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

        # Ensure edges are behind the nodes
        edges = [edge_left, edge_right, edge_left_left, edge_left_right, edge_right_left, edge_right_right,
                 edge_left_left_left, ]

        for edge in edges:
            edge.z_index = -1

        # Animate the scene (optional)
        self.play(FadeIn(root), )
        self.play(FadeIn(left_child), FadeIn(right_child))
        self.play(Create(edge_left), Create(edge_right))
        self.play(FadeIn(left_left_grandchild), FadeIn(left_right_grandchild), FadeIn(right_left_grandchild),
                  FadeIn(right_right_grandchild))
        self.play(Create(edge_left_left), Create(edge_left_right), Create(edge_right_left), Create(edge_right_right))
        self.play(FadeIn(left_left_left_greatgrandchild),
                  )
        self.play(Create(edge_left_left_left),
                  )

        # self.play(Create(left_right_right_greatgrandchild))
        # self.play(Create(edge_left_right_right))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN))

        # Example usage:
        array = Array(array_size=8).next_to(left_left_left_greatgrandchild, DOWN).shift(DOWN * 0.4).shift(RIGHT * 5.25)
        self.play(Create(array))

        array.add_element(self, "-1")
        array.add_element(self, "1")
        array.add_element(self, "5")
        array.add_element(self, "0")
        array.add_element(self, "0")
        array.add_element(self, "4")
        array.add_element(self, "6")
        array.add_element(self, "7")

        self.play(FadeOut(array, root, left_child, right_child, left_left_grandchild, left_right_grandchild,
                          right_left_grandchild, right_right_grandchild, left_left_left_greatgrandchild,
                          ), *[FadeOut(i) for i in edges], *[FadeOut(array.square_contents[i]) for i in range(8)])

        self.wait(2)

        self.play(Create(array), *[Create(array.square_contents[i]) for i in range(8)])
        self.wait(1)
        list1 = [root, left_child, right_child, left_left_grandchild, left_right_grandchild,
                 right_left_grandchild, right_right_grandchild, left_left_left_greatgrandchild, ]

        self.play(*[Create(i) for i in list1])
        self.wait(1)

        self.play(*[Create(i) for i in edges], )

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT * 1.8))

        # Define the text and formula separately
        text_label = MathTex(r"\text{Last Non-Leaf Index}").scale(1.2).shift(DOWN * 4.5)
        formula = MathTex(r"\left\lfloor \frac{n}{2} \right\rfloor - 1").scale(1.7).shift(RIGHT * 3)

        # Group them vertically
        last_non_leaf = VGroup(text_label, formula).arrange(DOWN, aligned_edge=LEFT, buff=1.5)

        # Positioning the group
        last_non_leaf.next_to(right_child, RIGHT).shift(RIGHT * 2.6)
        formula.shift(RIGHT * 1.63)

        last_non_leaf.shift(DOWN * 2.3)

        self.play(Create(last_non_leaf))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT * 1.8), FadeOut(last_non_leaf))
        self.wait(2)

        i = Text("i", font_size=45).next_to(array.square_contents[3], UP)
        self.play(Create(i))

        a = Circle(radius=0.6, color=PURE_GREEN, stroke_width=12).move_to(left_left_grandchild)
        self.play(Create(a))
        self.play(array.square_contents[3][0].animate.set_fill(PURE_GREEN))

        self.wait(2)

        self.play(left_left_left_greatgrandchild[0].animate.set_fill(ORANGE),
                  array.square_contents[-1][0].animate.set_fill(ORANGE))

        self.wait(2)

        self.play(Swap(left_left_left_greatgrandchild[1], left_left_grandchild[1]),
                  left_left_left_greatgrandchild[0].animate.set_fill(YELLOW_C))
        left_left_left_greatgrandchild[1], left_left_grandchild[1] = left_left_grandchild[1], \
                                                                     left_left_left_greatgrandchild[1]

        self.play(Swap(array.square_contents[-1], array.square_contents[3]))
        array.square_contents[-1], array.square_contents[3] = array.square_contents[3], array.square_contents[-1]
        self.play(array.square_contents[-1][0].animate.set_fill(TEAL_B),
                  array.square_contents[3][0].animate.set_fill(TEAL_B))

        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[2], UP))
        self.wait()

        self.play(a.animate.move_to(right_child))
        self.play(array.square_contents[2][0].animate.set_fill(PURE_GREEN))

        self.wait(2)

        self.play(right_left_grandchild[0].animate.set_fill(ORANGE), right_right_grandchild[0].animate.set_fill(ORANGE))
        self.play(array.square_contents[5][0].animate.set_fill(ORANGE),
                  array.square_contents[6][0].animate.set_fill(ORANGE))

        self.wait(2)

        self.play(right_left_grandchild[0].animate.set_fill(YELLOW_C),
                  array.square_contents[5][0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(Swap(right_child[1], right_right_grandchild[1]), right_right_grandchild[0].animate.set_fill(YELLOW_C))
        right_child[1], right_right_grandchild[1] = right_right_grandchild[1], right_child[1]
        self.wait()
        self.play(Swap(array.square_contents[6], array.square_contents[2]))
        array.square_contents[6], array.square_contents[2] = array.square_contents[2], array.square_contents[6]
        self.play(array.square_contents[6][0].animate.set_fill(TEAL_B),
                  array.square_contents[2][0].animate.set_fill(TEAL_B))

        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[1], UP))
        self.wait()


        self.play(a.animate.move_to(left_child))
        self.play(array.square_contents[1][0].animate.set_fill(PURE_GREEN))
        self.wait(2)

        self.play(left_left_grandchild[0].animate.set_fill(ORANGE), left_right_grandchild[0].animate.set_fill(ORANGE))
        self.play(array.square_contents[3][0].animate.set_fill(ORANGE),
                  array.square_contents[4][0].animate.set_fill(ORANGE))

        self.wait(2)

        self.play(left_right_grandchild[0].animate.set_fill(YELLOW_C),
                  array.square_contents[4][0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(Swap(left_child[1], left_left_grandchild[1]), left_left_grandchild[0].animate.set_fill(YELLOW_C))
        left_child[1], left_left_grandchild[1] = left_left_grandchild[1], left_child[1]
        self.wait()
        self.play(Swap(array.square_contents[3], array.square_contents[1]))
        array.square_contents[3], array.square_contents[1] = array.square_contents[1], array.square_contents[3]
        self.play(array.square_contents[3][0].animate.set_fill(TEAL_B),
                  array.square_contents[1][0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(left_left_grandchild[0].animate.set_fill(YELLOW_C))
        self.wait()

        self.play(a.animate.move_to(left_left_grandchild))
        self.play(array.square_contents[3][0].animate.set_fill(PURE_GREEN))
        self.wait(1)
        self.play(left_left_left_greatgrandchild[0].animate.set_fill(ORANGE),
                  array.square_contents[7][0].animate.set_fill(ORANGE))
        self.wait()
        self.play(left_left_left_greatgrandchild[0].animate.set_fill(YELLOW_C),
                  array.square_contents[7][0].animate.set_fill(TEAL_B),
                  array.square_contents[3][0].animate.set_fill(TEAL_B))

        self.wait(2)

        self.play(i.animate.next_to(array.square_contents[0], UP))
        self.play(a.animate.move_to(root))
        self.play(array.square_contents[0][0].animate.set_fill(PURE_GREEN))
        self.wait(2)

        self.play(left_child[0].animate.set_fill(ORANGE), right_child[0].animate.set_fill(ORANGE))
        self.play(array.square_contents[1][0].animate.set_fill(ORANGE),
                  array.square_contents[2][0].animate.set_fill(ORANGE))

        self.wait(2)

        self.play(right_child[0].animate.set_fill(YELLOW_C),
                  array.square_contents[2][0].animate.set_fill(TEAL_B))
        self.wait(2)

        self.play(Swap(left_child[1], root[1]), left_child[0].animate.set_fill(YELLOW_C))
        left_child[1], root[1] = root[1], left_child[1]
        self.wait()
        self.play(Swap(array.square_contents[0], array.square_contents[1]))
        array.square_contents[0], array.square_contents[1] = array.square_contents[1], array.square_contents[0]
        self.play(array.square_contents[1][0].animate.set_fill(TEAL_B),
                  array.square_contents[0][0].animate.set_fill(TEAL_B))

        self.wait(2)

        self.play(a.animate.move_to(left_child))
        self.play(array.square_contents[1][0].animate.set_fill(PURE_GREEN))
        self.wait(2)
        self.play(left_left_grandchild[0].animate.set_fill(ORANGE),
                  array.square_contents[3][0].animate.set_fill(ORANGE),
                  left_right_grandchild[0].animate.set_fill(ORANGE),
                  array.square_contents[4][0].animate.set_fill(ORANGE))
        self.wait(1)
        self.play(left_right_grandchild[0].animate.set_fill(YELLOW_C),
                  array.square_contents[4][0].animate.set_fill(TEAL_B))
        self.wait(2)
        self.play(Swap(left_left_grandchild[1], left_child[1]), left_left_grandchild[0].animate.set_fill(YELLOW_C))
        left_left_grandchild[1], left_child[1] = left_child[1], left_left_grandchild[1]
        self.play(Swap(array.square_contents[1], array.square_contents[3]))
        array.square_contents[1], array.square_contents[3] = array.square_contents[3], array.square_contents[1]
        self.play(array.square_contents[1][0].animate.set_fill(TEAL_B),
                  array.square_contents[3][0].animate.set_fill(TEAL_B))

        self.wait(1)
        self.play(a.animate.move_to(left_left_grandchild))
        self.play(array.square_contents[3][0].animate.set_fill(PURE_GREEN))
        self.wait(1)

        self.play(left_left_left_greatgrandchild[0].animate.set_fill(ORANGE),
                  array.square_contents[-1][0].animate.set_fill(ORANGE))
        self.wait()

        self.play(Swap(left_left_grandchild[1], left_left_left_greatgrandchild[1]),
                  left_left_left_greatgrandchild[0].animate.set_fill(YELLOW_C))
        left_left_grandchild[1], left_left_left_greatgrandchild[1] = left_left_left_greatgrandchild[1], left_left_grandchild[1]
        self.play(Swap(array.square_contents[3], array.square_contents[-1]))
        array.square_contents[-1], array.square_contents[3] = array.square_contents[3], array.square_contents[-1]
        self.play(array.square_contents[-1][0].animate.set_fill(TEAL_B),
                  array.square_contents[3][0].animate.set_fill(TEAL_B))

        self.wait(2)

        self.play(Uncreate(a), Uncreate(i))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT * 1.8))

        # Define the initial expression and its transformation
        initial_expression = MathTex(r"\frac{n}{2} \cdot \log(n)").move_to(last_non_leaf).scale(1.4)
        big_o_notation = MathTex(r"O(n \log n)").move_to(initial_expression).scale(1.4)

        self.play(Create(initial_expression))
        self.wait(2)

        self.play(ReplacementTransform(initial_expression, big_o_notation))
        self.wait(2)

        self.play(FadeOut(big_o_notation))
        self.wait(2)

        a5 = Circle(radius=0.6, stroke_width=12, color=PURE_GREEN).next_to(left_left_left_greatgrandchild, ORIGIN)
        a2 = Circle(radius=0.6, stroke_width=12, color=PURE_GREEN).move_to(left_right_grandchild)
        a3 = Circle(radius=0.6, stroke_width=12, color=PURE_GREEN).move_to(right_right_grandchild)
        a4 = Circle(radius=0.6, stroke_width=12, color=PURE_GREEN).move_to(right_left_grandchild)

        list2 = [a2, a3, a4, a5]

        self.play(*[Create(i) for i in list2])

        self.wait(2)

        self.play(a5.animate.move_to(left_left_grandchild), a2.animate.move_to(left_left_grandchild),
                  a3.animate.move_to(right_child), a4.animate.move_to(right_child))
        self.remove(a5, a3)
        self.wait(2)

        self.play(a2.animate.move_to(left_child), a4.animate.move_to(left_child))
        self.remove(a4)
        self.wait(2)

        self.play(a2.animate.move_to(root))

        # Step-by-step transformations
        step_1 = MathTex(r"\sum_{k=0}^{\log n} \left( \frac{n}{2^{k+1}} \times k \right)").move_to(
            big_o_notation).scale(1.4)
        step_2 = MathTex(r"n \sum_{k=0}^{\log n} \frac{k}{2^{k+1}}").scale(1.4).move_to(step_1)
        step_3 = MathTex(r"\approx n \cdot C").scale(1.4).move_to(step_1)
        step_4 = MathTex(r"O(n)").scale(2.2).move_to(step_1)

        self.wait(2)
        self.play(Uncreate(a2))

        self.play(Create(step_1))
        self.wait(2)

        self.play(ReplacementTransform(step_1, step_2))
        self.wait(2)

        self.play(ReplacementTransform(step_2, step_3))
        self.wait(2)

        self.play(ReplacementTransform(step_3, step_4))
        self.wait(2)
