from manim import *


class Selection(MovingCameraScene):

    def swap_elements(self, element1, element2):
        # Get the side length of the square
        side_length = element1.get_height()

        # Get the positions of element1 and element2
        pos1 = element1.get_center()
        pos2 = element2.get_center()

        # Lift both squares up by their side lengths
        self.play(
            element1.animate.shift(UP * side_length * 1.2),
            element2.animate.shift(UP * side_length * 1.2),
            run_time=0.7,
        )

        # Swap the elements visually (assuming a Swap function or similar effect)
        self.play(Swap(element1, element2), run_time=1)

        # Move the elements to each other's positions
        self.play(
            element1.animate.move_to(pos2),
            element2.animate.move_to(pos1),
            run_time=0.5,
        )

        self.wait(0.4)

    def move_pointer_to(self, pointer, element, value_text):
        self.play(
            pointer.animate.next_to(element, UP, buff=0.2),
            value_text.animate.next_to(pointer, UP, buff=0.1).set_text(str(element[1].text)), run_time=0.5
        )

    def construct(self):
        self.camera.frame.shift(UP)
        array = [32, 9, 12, 6, 0, 5]  # You can modify this array as needed


        elements = VGroup()
        index_labels = VGroup()
        outline_boxes = VGroup()

        start_address = 100  # Starting address
        element_size = 4  # Size of each element

        capacity = 6

        # Create outline boxes for the full capacity
        for i in range(capacity):
            outline_box = Square(stroke_width=6).scale(0.85).set_stroke(GRAY, opacity=0.5).set_fill(opacity=0)
            outline_boxes.add(outline_box)

        # Position outline boxes in a horizontal arrangement
        outline_boxes.arrange(RIGHT, buff=0.1)
        outline_boxes.shift(ORIGIN + DOWN)

        # Add filled squares and texts for the current elements in the array
        for i, value in enumerate(array):
            square = Square(color=DARK_BLUE, stroke_width=6).scale(0.85).set_fill(YELLOW_C, 1)
            text = Text(str(value), color=BLACK, font=BOLD).scale(1.5)
            element = VGroup(square, text)
            elements.add(element)
            element.move_to(outline_boxes[i].get_center())

            index_text = Text(str(i), color=WHITE, font=BOLD).scale(0.8)
            index_labels.add(index_text)
            index_text.next_to(outline_boxes[i], DOWN, buff=0.45)

        elements.shift(UP * 0.85)
        index_labels.shift(UP * 0.85)
        outline_boxes.shift(UP * 0.85)

        title = Text("Selection Sort", color=PURPLE, font=BOLD).next_to(elements, UP * 2).scale(1.6).shift(UP * 2.6)
        self.play(Create(title))

        self.play(Create(outline_boxes))

        # Create the visualization for elements and outlines together
        self.play(Create(elements), Create(index_labels), )
        self.wait(2)

        # Create MIN variable display
        min_var_text = Text("MIN = ").next_to(title, DOWN, buff=1)
        min_var_text.shift(LEFT * 0.26)

        min_var_value = Integer(0).next_to(min_var_text, RIGHT)  # Use Integer instead of DecimalNumber
        min_var = VGroup(min_var_text, min_var_value).scale(1.2)
        min_var.shift(UP * 0.3)

        self.play(Create(min_var))

        # Create a pointer and a value text
        pointer = Polygon(
            [0, 0.1, 0],  # Top left vertex
            [0.1, 0.1, 0],  # Top right vertex
            [0.05, 0, 0]  # Bottom vertex (pointing downwards)
        ).set_color(RED).set_fill(RED, opacity=1).next_to(elements[0], UP, buff=0.27).scale(3)

        value_text = Text("", font_size=24).next_to(pointer, UP, buff=0.1)

        self.play(Create(pointer), Create(value_text), )
        brace = Brace(elements[0:1], direction=DOWN, buff=1.1)
        label = Text("Sorted", font_size=29,).next_to(brace, DOWN, buff=0.1)
        a = False

        for i in range(len(array)):
            min_index = i
            if i > 0:
                self.move_pointer_to(pointer, elements[i], value_text)

            # Update MIN variable
            self.play(min_var_value.animate.set_value(int(elements[min_index][1].get_text())))
            # Update MIN variable only if the current value is smaller

            self.play(elements[i][0].animate.set_fill(GREEN, 1), run_time=0.633333)
            self.play(elements[i][0].animate.set_fill(YELLOW_C, 1), run_time=0.6)

            for j in range(i + 1, len(array)):
                # Move pointer to the current element

                self.move_pointer_to(pointer, elements[j], value_text)
                self.wait(0.5)  # Pause to show comparison

                current_value = int(elements[j][1].get_text())
                min_value = int(elements[min_index][1].get_text())

                # Update MIN variable only if the current value is smaller
                if current_value < min_value:
                    self.play(elements[j][0].animate.set_fill(GREEN, 1), run_time=0.63333)
                    self.play(elements[j][0].animate.set_fill(YELLOW_C, 1), run_time=0.6)
                    self.play(min_var_value.animate.set_value(current_value))
                    min_index = j
                else:
                    self.play(elements[j][0].animate.set_fill(RED, 1), run_time=0.633333)
                    self.play(elements[j][0].animate.set_fill(YELLOW_C, 1), run_time=0.6)

            # Swap if min_index is not equal to i
            if min_index != i:
                array[i], array[min_index] = array[min_index], array[i]
                self.swap_elements(elements[i], elements[min_index])
                self.play(elements[min_index][0].animate.set_fill(TEAL_B, 1))
                elements[i], elements[min_index] = elements[min_index], elements[i]
                if i == 0:
                    self.play(Create(brace), Create(label))
                else:
                    new_brace = Brace(elements[0:i + 1], direction=DOWN, buff=1.1)
                    self.play(Transform(brace, new_brace))
                    # Update the position of the label
                    label.generate_target()
                    label.target.next_to(brace, DOWN, buff=0.1)
                    self.play(MoveToTarget(label))
            else:
                a = True

            if a:
                self.play(elements[min_index][0].animate.set_fill(TEAL_B, 1))

                new_brace = Brace(elements[0:i + 1], direction=DOWN, buff=1.1)
                self.play(Transform(brace, new_brace))
                # Update the position of the label
                label.generate_target()
                label.target.next_to(brace, DOWN, buff=0.1)
                self.play(MoveToTarget(label))

        self.play(FadeOut(pointer, min_var))
        self.wait(3)

