from manim import *


class ArrayScene(Scene):
    CONFIG = {
        "background_color": "#FFFFFF",  # Set your desired background color
    }

    def construct(self):
        title = Text("Insertion Sort", font_size=56, color=WHITE).set_buff(2).to_edge(UP)
        self.play(Write(title))

        numbers = [12, 2, 1, 123, 0, -7, -22, 4]

        # Create circles with numbers embedded
        original_circles = self.create_circles(numbers)

        # Display the original array
        self.play(Create(original_circles))

        self.wait(1)

        # Sort the array using Insertion Sort
        self.insertion_sort(original_circles)

    def create_circles(self, numbers):
        circles = VGroup()

        # Create a circle for each number
        for number in numbers:
            circle = Circle(radius=0.61, color=BLUE_D, stroke_width=6)
            text = Text(str(number), color=WHITE)
            number_circle = VGroup(circle, text)
            circles.add(number_circle)

        # Arrange circles horizontally
        circles.arrange(RIGHT, buff=0.5)

        return circles

    def insertion_sort(self, circles):
        n = len(circles)

        brace = Brace(circles, direction=DOWN * 10, color=RED, buff=0.8)
        unsorted_text = Text("Unsorted", color=RED).next_to(brace, DOWN)
        unsorted_group = VGroup(brace, unsorted_text)
        self.play(GrowFromCenter(unsorted_group))

        brace2 = Brace(circles[0], direction=DOWN * 10, color=GREEN, buff=0.8)
        sorted_text = Text("Sorted", color=GREEN).next_to(brace2, DOWN)
        sorted_group = VGroup(brace2, sorted_text)

        # Create curly brace outside the loop
        curly_brace = Brace(circles[0:2], UP, color=YELLOW_C, buff=0.55)
        self.play(GrowFromCenter(curly_brace), run_time=0.5)

        for i in range(0, n):
            for j in range(i, 0, -1):
                # Highlight the circles being compared
                # Update curly brace position
                self.play(
                    Transform(curly_brace, Brace(circles[j - 1:j + 1], UP, color=YELLOW_C, buff=0.55), run_time=0.5))
                self.wait(0.5)

                self.play(
                    circles[j].animate.set_color(PINK),
                    circles[j - 1].animate.set_color(PINK),
                    run_time=0.5,
                )

                # Restoring the original color after highlighting
                self.play(
                    circles[j].animate.set_color(BLUE_D),
                    circles[j][1].animate.set_color(WHITE),  # Set text color to white
                    circles[j - 1].animate.set_color(BLUE_D),
                    circles[j - 1][1].animate.set_color(WHITE),  # Set text color to white

                    run_time=0.1,
                )

                # Compare adjacent elements
                current_value = int(circles[j][1].get_text())
                prev_value = int(circles[j - 1][1].get_text())

                # Swap elements if they are in the wrong order
                if current_value > prev_value:
                    break
                elif current_value < prev_value:
                    pos_current = circles[j].get_center()
                    pos_prev = circles[j - 1].get_center()
                    self.play(circles[j].animate.move_to(pos_prev), circles[j - 1].animate.move_to(pos_current),
                              run_time=1)
                    circles[j], circles[j - 1] = circles[j - 1], circles[j]

                self.wait(0.2)  # Adjust the wait time as needed

            # Remove the curly brace after the key element comparison
            # self.play(FadeOut(curly_brace))

            if i == n-1:
                self.play(FadeOut(unsorted_group))
            if i < n - 1:

                if i < n - 1:
                    new_brace = Brace(circles[i + 1:], direction=DOWN, color=RED, buff=0.8)
                    new_unsorted_text = Text("Unsorted", color=RED).next_to(new_brace, DOWN)
                    new_unsorted_group = VGroup(new_brace, new_unsorted_text)
                    self.play(Transform(unsorted_group, new_unsorted_group))
                else:
                    self.play(FadeOut(unsorted_group))

            brace2new = Brace(circles[:i + 1], direction=DOWN, color=GREEN, buff=0.8)
            new_sorted_text = Text("Sorted", color=GREEN).next_to(brace2new, DOWN)
            new_sorted_group = VGroup(brace2new, new_sorted_text)
            self.play(Transform(sorted_group, new_sorted_group))
        self.play(FadeOut(curly_brace))
        self.wait(4)


# Run the animation with the command:
# manim -pql your_script_name.py ArrayScene
