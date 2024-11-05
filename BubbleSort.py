from manim import *


# config.pixel_height = 3480  # Vertical pixels
# config.pixel_width = 2160  # Horizontal pixels
# config.frame_height = 8.0  # Manim's default frame height
# config.frame_width = (
#                                  config.frame_height * config.pixel_width) / config.pixel_height  # Adjust frame width for vertical video

# config.background_color = GREY

class Bubble(MovingCameraScene):

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
            run_time=0.6,
        )

        # Swap the elements visually (assuming a Swap function or similar effect)
        self.play(Swap(element1, element2), run_time=0.6)

        # Move the elements to each other's positions
        self.play(
            element1.animate.move_to(pos2),
            element2.animate.move_to(pos1),
            run_time=0.6,
        )

        self.wait(0.4)

    def construct(self):

        self.camera.frame.shift(UP)



        array = [6,5,4,3,1,2]
        capacity = 6

        elements = VGroup()
        index_labels = VGroup()
        outline_boxes = VGroup()


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

        elements.shift(UP*0.85)
        index_labels.shift(UP*0.85)
        outline_boxes.shift(UP*0.85)

        title = Text("Bubble Sort", color=PURPLE, font=BOLD).next_to(elements, UP*2).scale(1.8).shift(UP*2.2)
        self.play(Create(title))

        self.play(Create(outline_boxes))

        # Create the visualization for elements and outlines together
        self.play(Create(elements), Create(index_labels), )
        self.wait(2)

        # Bubble Sort Algorithm
        n = len(array)
        # Create a brace for the group
        brace = Brace(elements[0:2], direction=DOWN, buff=1.2)
        self.play(Create(brace))
        initial_y = brace.get_center()[1]

        sorted_brace = None  # Initialize the sorted brace as None
        sorted_label = None  # Initialize the sorted label as None

        a = False

        for i in range(n):
            if a:
                break
            swapped = False
            for j in range(0, n - i - 1):
                ## Calculate the new horizontal position (x-coordinate)
                new_x = elements[j:j + 2].get_center()[0]

                # Create a new target position with the original y-coordinate
                target_position = np.array([new_x, initial_y, 0])

                # Move the brace to the new position
                self.play(brace.animate.move_to(target_position), run_time=0.5)

                if array[j] > array[j + 1]:
                    swapped = True
                    self.play(
                        elements[j][0].animate.set_fill(RED, 1),  # Only change the square's color
                        elements[j + 1][0].animate.set_fill(RED, 1),  # Only change the square's color
                        run_time=1
                    )
                    self.play(
                        elements[j][0].animate.set_fill(YELLOW_C, 1),  # Only change the square's color
                        elements[j + 1][0].animate.set_fill(YELLOW_C, 1),  # Only change the square's color
                        run_time=0.4
                    )
                    array[j], array[j + 1] = array[j + 1], array[j]
                    self.swap_elements(elements[j], elements[j + 1])
                    elements[j], elements[j + 1] = elements[j + 1], elements[j]

                else:
                    self.play(
                        elements[j][0].animate.set_fill(GREEN, 1),  # Only change the square's color
                        elements[j + 1][0].animate.set_fill(GREEN, 1),  # Only change the square's color
                        run_time=1
                    )
                    self.play(
                        elements[j][0].animate.set_fill(YELLOW_C, 1),  # Only change the square's color
                        elements[j + 1][0].animate.set_fill(YELLOW_C, 1),  # Only change the square's color
                        run_time=0.4
                    )

            if not swapped and i < 2:
                self.play(FadeOut(brace))

                new_brace = Brace(elements[0:n], direction=UP, buff=0.3)

                for k in elements:
                    self.play(k[0].animate.set_fill(TEAL_B, 1),  # Only change the square's color
                              run_time=0.1)
                self.wait(1)

                self.play(
                    Create(new_brace
                           ),
                    run_time=1
                )

                # Update the position of the label
                sorted_label = Text("Sorted")

                sorted_label.next_to(new_brace, UP, buff=0.5)
                self.play(sorted_label.animate.move_to(sorted_label.get_center()))

                self.wait(3)
                a = True

                break

            self.play(
                elements[j + 1][0].animate.set_fill(TEAL_B, 1),  # Only change the square's color
                run_time=0.1
            )

            # Inside the for loop, after updating the sorted brace
            if sorted_brace is None and i < n - 1:
                # Create the sorted brace when the first element is sorted
                sorted_brace = Brace(elements[n - 1], direction=UP, buff=0.3)
                self.play(Create(sorted_brace))

                # Create and position the label
                sorted_label = Text("Sorted", )
                sorted_label.next_to(sorted_brace, UP, buff=0.3)
                self.play(Create(sorted_label))

            elif i < n - 1:
                # Update the sorted brace to cover the sorted part of the array
                new_brace = Brace(elements[n - i - 2:n], direction=UP, buff=0.3)
                self.play(
                    sorted_brace.animate.become(
                        Brace(elements[n - i - 1:n], direction=UP, buff=0.5)
                    ),
                    run_time=1
                )

                # Update the position of the label
                sorted_label.generate_target()
                sorted_label.target.next_to(sorted_brace, UP, buff=0.5)
                self.play(MoveToTarget(sorted_label))

        if not a:
            self.play(
                elements[0][0].animate.set_fill(TEAL_B, 1),  # Only change the square's color
                run_time=0.1
            )

            self.play(FadeOut(brace))

            new_brace = Brace(elements[0:n], direction=UP, buff=0.3)

            self.play(
                sorted_brace.animate.become(
                    Brace(elements[:n], direction=UP, buff=0.3)
                ),
                run_time=1
            )

            # Update the position of the label
            sorted_label.next_to(new_brace, UP, buff=0.5)
            self.play(sorted_label.animate.move_to(sorted_label.get_center()))

            self.wait(3)
