from manimlib import *
PURE_RED = "#FF0000"
PURE_BLUE = "#00FF00"
PURE_GREEN = "#0000FF"

class Array(VGroup):
    def __init__(self, array_size=5, **kwargs):
        super().__init__(**kwargs)
        self.array_size = array_size
        self.square_contents = [None] * array_size
        self.array_group = self.create_array()
        self.add(self.array_group)

    def create_element(self, text):
        square = Square(side_length=1.22, fill_opacity=1, fill_color=BLACK, color=BLACK).set_color(BLACK)
        text = Text(text, font_size=44, color=BLACK).scale(0.8).set_color(BLACK)
        return VGroup(square, text)

    def create_array(self):
        squares = VGroup(*[Square(side_length=1.22, color=PURE_RED, stroke_width=6).set_color(BLACK) for _ in range(self.array_size)])
        squares.arrange(RIGHT, buff=0)
        index_labels = VGroup(
            *[Text(str(i), font_size=30).next_to(square, DOWN, buff=0.23).set_color(BLACK) for i, square in enumerate(squares)]
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
                new_square = Square(side_length=1.22, fill_opacity=1, fill_color=YELLOW, color=BLACK,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK).set_z_index(1).set_color(BLACK)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def add_element(self, scene, value, color=YELLOW):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.22, fill_opacity=1, fill_color=color, color=BLACK,
                                    stroke_width=6)
                number = Text(str(value), color=BLACK, font_size=50).set_z_index(1).set_color(BLACK)
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
        scene.play(ShowCreation(new_array))
        return new_array

    def transfer_elements_to_new_array(self, scene, new_array):
        for i, content in enumerate(self.square_contents):
            if content is not None:
                scene.play(Transform(content, new_array.array_group[0][i]))
                new_array.square_contents[i] = content
                self.square_contents[i] = None



class LeetCode1(Scene):

    def construct(self):

        self.camera.frame.scale(0.88).shift(UP*0.83)

        
        # Example usage:
        array = Array(array_size=7)

        array.append_element(self, "1")
        array.append_element(self, "2")
        array.append_element(self, "3")
        array.append_element(self, "4")
        array.append_element(self, "5")
        array.append_element(self, "6")
        array.append_element(self, "7")



        self.wait(2)

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(7)])
        self.wait(2)

        k = Text("k = 3").set_color(BLACK).next_to(array, UP, buff=2.22)
        self.play(ShowCreation(k))
        self.wait(2)

        brace = Brace(array.array_group[0][4:], DOWN, buff=0.1).set_color(BLACK).shift(DOWN*0.8)

        # 2. (Optional) Create a label for the brace if desired
        brace_label = Text("k", color=BLACK, font_size=30).next_to(
            brace, DOWN, buff=0.2
        ).set_color(BLACK)

        # 3. Animate the brace and label onto the screen
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_label)
        )

        self.play(array.square_contents[-1][0].animate.set_fill(TEAL_B),
                  array.square_contents[-2][0].animate.set_fill(TEAL_B),
                  array.square_contents[-3][0].animate.set_fill(TEAL_B))


        self.wait(2)

        def create_parabola(start, end, direction="up", height=2.0):
            """
            Creates a smooth 3-point curve from `start` to `end`.
              - direction = "up" or "down"
              - height = how tall the parabola is
            """
            path = VMobject()
            midpoint = (start + end) / 2
            if direction == "up":
                midpoint += height * UP
            else:
                midpoint += height * DOWN
            
            # Use set_points_smoothly to create a nice quadratic curve
            path.set_points_smoothly([start, midpoint, end])
            return path

        # 4) We want to rotate the array by k=3
        k = 3
        move_animations = []
        for i in range(7):
            new_index = (i + k) % 7

            start_pos = array.square_contents[i].get_center()
            end_pos   = array.array_group[0][new_index].get_center()

            # Decide if it goes "up" or "down"
            direction = "up" if i < 4 else "down"

            # Create the parabola path
            path = create_parabola(start_pos, end_pos, direction=direction, height=1.5)

            # Animate moving along that path
            # We'll do all animations simultaneously, so we just collect them.
            move_animations.append(
                MoveAlongPath(array.square_contents[i], path, run_time=2)
            )

        # 5) Animate all moves at once (no vanish!)
        self.play(*move_animations)
        self.wait()

        # 6) Update array.square_contents references
        new_contents = [None] * 7
        for i in range(7):
            new_index = (i + k) % 7
            new_contents[new_index] = array.square_contents[i]
        array.square_contents = new_contents

        self.play(FadeOut(VGroup(brace, brace_label)),
                  array.square_contents[0][0].animate.set_fill(YELLOW),
                  array.square_contents[1][0].animate.set_fill(YELLOW),
                  array.square_contents[2][0].animate.set_fill(YELLOW))


        self.wait(2)



        self.embed()

class LeetCode2(Scene):

    def construct(self):
        
        self.camera.frame.scale(0.88).shift(UP*0.83)

        
        # Example usage:
        array = Array(array_size=7)

        array.append_element(self, "1")
        array.append_element(self, "2")
        array.append_element(self, "3")
        array.append_element(self, "4")
        array.append_element(self, "5")
        array.append_element(self, "6")
        array.append_element(self, "7")



        self.wait(2)

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(7)])
        self.wait(2)

        k = Text("k = 3").set_color(BLACK).next_to(array, UP, buff=2.22)
        self.play(ShowCreation(k))
        self.wait(2)

        self.play(array.square_contents[-1][0].animate.set_fill(TEAL_B),
                  array.square_contents[-2][0].animate.set_fill(TEAL_B),
                  array.square_contents[-3][0].animate.set_fill(TEAL_B))
        

        self.wait(2)




        #  AFTER THIS, WE REVERSE THE ARRAY IN A FANCY WAY
        # ---------------------------------------------------------------
        # 1) We'll reuse the "create_parabola" approach from before:
        def create_parabola(start, end, direction="up", height=2.0):
            """
            Creates a smooth 3-point curve from `start` to `end`.
            direction = "up" or "down"
            height = how tall the parabola arcs
            """
            path = VMobject()
            midpoint = (start + end) / 2
            if direction == "up":
                midpoint += height * UP
            else:
                midpoint += height * DOWN
            path.set_points_smoothly([start, midpoint, end])
            return path

        # 2) Reverse the array in place:
        #    For each i in range(n//2), we swap element i with element (n-1 - i).
        n = 7
        reverse_animations = []
        for i in range(n // 2):
            j = n - 1 - i

            # Current positions
            start_i = array.square_contents[i].get_center()
            start_j = array.square_contents[j].get_center()
            
            # We'll move i's object to j, and j's object to i
            # Decide the path direction.  Let's do:
            #  - "up" if i is in the lower half
            #  - "down" if j is in the upper half
            # Feel free to choose your own logic for direction.
            path_i = create_parabola(start_i, start_j, direction="up",   height=1.5)
            path_j = create_parabola(start_j, start_i, direction="down", height=1.5)

            reverse_animations.append(
                MoveAlongPath(array.square_contents[i], path_i, run_time=2)
            )
            reverse_animations.append(
                MoveAlongPath(array.square_contents[j], path_j, run_time=2)
            )

        # 3) Animate these all at once
        self.play(*reverse_animations)
        self.wait()

        # 4) Swap references in array.square_contents
        #    We only need to do a simple Python-level in-place swap for i in [0..n//2)
        for i in range(n // 2):
            j = n - 1 - i
            array.square_contents[i], array.square_contents[j] = (
                array.square_contents[j],
                array.square_contents[i]
            )

        self.wait(2)

        brace = Brace(array.array_group[0][:3], DOWN, buff=0.1).set_color(BLACK).shift(DOWN*0.8)
        self.play(GrowFromCenter(brace))
        self.wait(4)

        self.play(Swap(array.square_contents[0], array.square_contents[2]))

        self.wait(2)

        self.play(Transform(brace, Brace(array.array_group[0][3:], DOWN, buff=0.1).set_color(BLACK).shift(DOWN*0.8)))
        self.wait(2)

        self.play(Swap(array.square_contents[3], array.square_contents[6]),
                  Swap(array.square_contents[4], array.square_contents[5]))
        
        self.wait()

        self.play(array.square_contents[0][0].animate.set_fill(YELLOW),
                  array.square_contents[1][0].animate.set_fill(YELLOW),
                  array.square_contents[2][0].animate.set_fill(YELLOW))
        
        self.play(FadeOut(brace))

        self.wait(2)
        
class LeetCode3(Scene):

    def construct(self):
        
        self.camera.frame.scale(0.88).shift(UP*0.83)

        
        # Example usage:
        array = Array(array_size=7)

        array.append_element(self, "1")
        array.append_element(self, "2")
        array.append_element(self, "3")
        array.append_element(self, "4")
        array.append_element(self, "5")
        array.append_element(self, "6")
        array.append_element(self, "7")



        self.wait(2)

        self.play(ShowCreation(array), *[ShowCreation(array.square_contents[i]) for i in range(7)])
        self.wait(2)


        source_code = r'''

        def reverse(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                r -= 1

        
'''

        # Map each substring to a desired color
        color_map = {
            
            "class": BLUE_E,
            "def": BLUE_E,
            "if": BLUE_E,
            "elif": BLUE_E,
            "else": BLUE_E,
            "l": PURPLE_E,
            "r": PURPLE_E,
            "self": PURPLE_E,
            "__init__":PURE_RED,
            "kruskal": PURE_RED,
            "find": PURE_RED,
            "append":PURE_RED,
            "sort":PURE_RED,
            "lambda":BLUE_E,
            "list":BLUE_E,
            "DisjointSet":PURE_RED,
            "not":BLUE_E,
            "disjoint":BLACK,
            "chain":BLACK,
            "__str__":PURE_RED,
            "enumerate":PURE_RED,
            "return":BLUE_E,
            "index":BLACK,
            "HashTable":PURE_RED,
            "_hash":PURE_RED,
            "insert":PURE_RED,
            "None":BLUE_E,
            "get":PURE_RED,
            "remove":PURE_RED,
            "join":PURE_RED,
            "while":BLUE_E,
            "reverse":PURE_RED,
            "del":BLUE_E
        }

        

        # Create a Code mobject with syntax highlighting
        code = Text(source_code).set_color(BLACK).scale(0.6).shift(UP*0.6)

        # Apply color for each key-value in the map
        for word, color in color_map.items():
            code.set_color_by_text(word, color)

        self.play(self.camera.frame.animate.shift(UP*0.8))

        code.next_to(array, UP, buff=0.7).shift(UP*0.4).scale(1.1)


        # Animate it onto the scene
        self.play(Write(code))
        self.wait(1)

        rect = SurroundingRectangle(code[:16], color=PURE_GREEN, stroke_width=6.9)
        self.play(ShowCreation(rect))
        
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[16:25], color=PURE_GREEN, stroke_width=6.9)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(code[25:56], color=PURE_GREEN, stroke_width=6.9)))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(code[56:], color=PURE_GREEN, stroke_width=6.9)))
        self.wait(2)
        self.play(Uncreate(rect), FadeOut(code) , self.camera.frame.animate.shift(DOWN*0.78))
        self.wait(2)

        l = Text("l").set_color(PURPLE_E).next_to(array.square_contents[0], UP, buff=0.77)
        r = Text("r").set_color(PURPLE_E).next_to(array.square_contents[-1], UP, buff=0.77)

        self.play(ShowCreation(l), ShowCreation(r))
        self.wait(2)

        self.play(array.square_contents[0][0].animate.set_fill(TEAL_B),
        array.square_contents[-1][0].animate.set_fill(TEAL_B))
        self.play(Swap(array.square_contents[0], array.square_contents[-1]))
        self.wait(2)
        self.play(l.animate.next_to(array.square_contents[1], UP, buff=0.77), r.animate.next_to(array.square_contents[-2], UP, buff=0.77))
        self.play(array.square_contents[1][0].animate.set_fill(TEAL_B),
        array.square_contents[-2][0].animate.set_fill(TEAL_B))
        self.play(Swap(array.square_contents[1], array.square_contents[-2]))
        self.wait(2)

        self.play(l.animate.next_to(array.square_contents[2], UP, buff=0.77), r.animate.next_to(array.square_contents[-3], UP, buff=0.77))
        self.play(array.square_contents[2][0].animate.set_fill(TEAL_B),
        array.square_contents[-3][0].animate.set_fill(TEAL_B))
        self.play(Swap(array.square_contents[2], array.square_contents[-3]))
        self.wait(2)
        self.play(l.animate.next_to(array.square_contents[3], UP, buff=0.77).shift(LEFT*0.2), r.animate.next_to(array.square_contents[3], UP, buff=0.77).shift(RIGHT*0.2))
        self.play(array.square_contents[3][0].animate.set_fill(TEAL_B), FadeOut(VGroup(l,r)), self.camera.frame.animate.shift(DOWN*0.78))

        self.wait(2)













        self.embed()

