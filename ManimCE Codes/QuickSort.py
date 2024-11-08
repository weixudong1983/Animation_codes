from manim import *

class Array:
    def __init__(self, scene, values, name, position=ORIGIN, max_size=6):
        self.scene = scene
        self.values = values
        self.name = name
        self.max_size = max_size
        self.elements = VGroup()
        self.create_array(position)
        self.i_pointer = None
        self.j_pointer = None

    def create_array(self, position):
        # Create the rectangular base
        self.base = Rectangle(height=1, width=self.max_size, color=DARK_BLUE)
        self.base.move_to(position)

        # Create cells
        self.cells = VGroup(*[
            Square(side_length=1, color=DARK_BLUE)
            for _ in range(self.max_size)
        ])
        self.cells.arrange(RIGHT, buff=0)
        self.cells.move_to(self.base.get_center())

        # Create elements (squares with numbers)
        for i, value in enumerate(self.values):
            square = Square(side_length=1, fill_opacity=1, fill_color=YELLOW_C, color=DARK_BLUE)
            text = Text(str(value), font_size=40, color=BLACK)
            element = VGroup(square, text)
            element.move_to(self.cells[i].get_center())
            self.elements.add(element)

        self.name_label = Text(self.name, font_size=24).next_to(self.base, UP, buff=0.5)
        self.index_labels = VGroup(*[
            Text(str(i), font_size=20).next_to(cell, DOWN, buff=0.3)
            for i, cell in enumerate(self.cells)
        ])

        self.array_group = VGroup(self.base, self.cells, self.elements, self.name_label, self.index_labels)

    def show(self):
        self.scene.play(
            Create(self.base),
            Create(self.cells),
            Create(self.name_label),
            Create(self.index_labels),
            *[Create(elem) for elem in self.elements]
        )


    def highlight_element(self, index, color):
        # Highlight a specific element in the array by changing its color
        element = self.elements[index]
        square = element[0]  # The square part of the element
        self.scene.play(square.animate.set_fill(color, opacity=1))

    def unhighlight_element(self, index):
        # Reset the highlight of a specific element in the array
        element = self.elements[index]
        square = element[0]
        self.scene.play(square.animate.set_fill(YELLOW_C, opacity=1))

    def show_pointers(self, i, j):
        # Create and show pointers above the array
        if self.i_pointer is None:
            self.i_pointer = Text("i", font_size=34).set_z_index(-1).next_to(self.cells[i], UP, buff=0.2).shift(LEFT)
            self.j_pointer = Text("j", font_size=30).next_to(self.cells[j], UP, buff=0.2).set_z_index(-1)
            self.scene.play(Create(self.i_pointer), Create(self.j_pointer))


    def move_i(self, i):

        self.scene.play(
            self.i_pointer.animate.next_to(self.cells[i], UP, buff=0.2),
        )

    def move_j(self, j):

        self.scene.play(
            self.j_pointer.animate.next_to(self.cells[j], UP, buff=0.2)
        )

    def swap_elements(self, i, j):
        # Get the elements to be swapped
        element1 = self.elements[i]
        element2 = self.elements[j]

        # Get the side length of the square (height of the element)
        side_length = element1[0].get_height()

        # Get the positions of element1 and element2
        pos1 = element1.get_center()
        pos2 = element2.get_center()

        # Lift both elements up by their side lengths
        self.scene.play(
            element1.animate.shift(UP * side_length * 1.2),
            element2.animate.shift(UP * side_length * 1.2),
            run_time=0.7,
        )

        self.scene.play(Swap(element1, element2), run_time=1)

        # Lower the elements to their new positions
        self.scene.play(
            element1.animate.shift(DOWN * side_length * 1.2),
            element2.animate.shift(DOWN * side_length * 1.2),
            run_time=0.5,
        )

        # Finally, swap the elements in the array group
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]

        self.scene.wait(0.4)

    def hide_pointers(self, i=False):
        # Hide the pointers
        if not i:
            self.scene.play(FadeOut(self.j_pointer))
            self.j_pointer = None
        else:
            self.scene.play(FadeOut(self.i_pointer))
            self.i_pointer = None


class QuickSort_partitionf(MovingCameraScene):




    def construct(self):
        self.camera.frame.scale(0.6).shift(UP*0.4)

        # Create the array
        array = Array(self, [15, 9, 3, 5, -1, 7], "", ORIGIN)
        array.show()
        self.wait(2)

        # Perform partitioning
        def partition(arr, low, high):
            pivot = arr[high]
            i = low - 1
            array.highlight_element(high, PINK)  # Highlight pivot
            for j in range(low, high):
                if j < low+1:
                    array.show_pointers(i + 1, j)  # Show i and j pointers
                else:
                    array.move_j(j)


                self.wait(1)

                if arr[j] <= pivot:
                    self.play(Indicate(VGroup(array.elements[j], array.cells[j]), color=PURE_GREEN))
                    i += 1
                    array.move_i(i)
                    self.wait()
                    array.swap_elements(i, j)  # Visualize the swap
                    self.wait(1)
                else:
                    self.play(Indicate(VGroup(array.elements[j], array.cells[j]), color=PURE_RED))

            array.hide_pointers()
            array.swap_elements(i+1, high)
            array.hide_pointers(i=True)
            array.highlight_element(i+1, TEAL_B)  # Unhighlight pivot

            return i + 1

        # Example partition call
        partition(array.values, 0, len(array.values) - 1)
        self.wait(2)


