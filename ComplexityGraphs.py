# %%manim -pqk -v WARNING BigOGraphs


from manim import *

class BigOGraphs(Scene):
    def construct(self):
        # Initial Axes
        axes = Axes(
            x_range=[0, 50, 1],
            y_range=[0, 50, 1],
            axis_config={"include_numbers": False, "include_ticks": False},

        )

        # Labels for axes
        labels = axes.get_axis_labels(x_label="n", y_label="Operations")
        labels.set_z_index(1)

        # Define the Big O functions
        O_1 = axes.plot(lambda x: 1, color=BLUE, x_range=[0, 20], use_smoothing=False)
        O_log_n = axes.plot(lambda x: np.log(x), color=GREEN, x_range=[1, 20], use_smoothing=False)
        O_n = axes.plot(lambda x: x, color=RED, x_range=[0, 20], use_smoothing=False)
        O_n_log_n = axes.plot(lambda x: x * np.log(x), color=PURPLE, x_range=[1, 20], use_smoothing=False)
        O_n_squared = axes.plot(lambda x: x**2, color=ORANGE, x_range=[0, 20], use_smoothing=False)
        O_2_power_n = axes.plot(lambda x: 2**x, color=YELLOW, x_range=[0, 10], use_smoothing=False)
        x_values = range(0, 8)
        y_values = [np.math.factorial(x) for x in x_values]
        O_n_factorial = axes.plot_line_graph(x_values, y_values, line_color=PINK)

        # Create labels for the functions
        labels_O_1 = MathTex("O(1)", color=BLUE).to_edge(UP).shift(RIGHT*2.6)
        labels_O_log_n = MathTex("O(\\log n)", color=GREEN).next_to(labels_O_1, DOWN)
        labels_O_n = MathTex("O(n)", color=RED).next_to(labels_O_log_n, DOWN)
        labels_O_n_log_n = MathTex("O(n \\log n)", color=PURPLE).next_to(labels_O_n, DOWN)
        labels_O_n_squared = MathTex("O(n^2)", color=ORANGE).next_to(labels_O_n_log_n, DOWN)
        labels_O_2_power_n = MathTex("O(2^n)", color=YELLOW).next_to(labels_O_n_squared, DOWN)
        labels_O_n_factorial = MathTex("O(n!)", color=PINK).next_to(labels_O_2_power_n, DOWN)

        # Add all the elements to the scene
        self.play(Create(axes), Write(labels))
        self.play(Create(O_1), Write(labels_O_1))
        self.wait(2)
        self.play(Create(O_log_n), Write(labels_O_log_n))
        self.wait(2)

        self.play(Create(O_n), Write(labels_O_n))
        self.wait(2)

        self.play(Create(O_n_log_n), Write(labels_O_n_log_n))
        self.wait(2)

        self.play(Create(O_n_squared), Write(labels_O_n_squared))
        self.wait(2)

        self.play(Create(O_2_power_n), Write(labels_O_2_power_n))
        self.wait(2)

        self.play(Create(O_n_factorial), Write(labels_O_n_factorial))
        self.wait(2)

        # Update Axes
        new_axes = Axes(
            x_range=[0, 50, 5],
            y_range=[0, 900, 500],
            axis_config={"include_numbers": False, "include_ticks": False},
        )

        self.play(FadeOut(labels_O_1, labels_O_n_factorial, labels_O_n, labels_O_2_power_n, labels_O_n_squared, labels_O_log_n, labels_O_n_log_n))

        # Define the Big O functions with the new range
        new_O_1 = new_axes.plot(lambda x: 1, color=BLUE, x_range=[0, 50], use_smoothing=False)
        new_O_log_n = new_axes.plot(lambda x: np.log(x), color=GREEN, x_range=[1, 50], use_smoothing=False)
        new_O_n = new_axes.plot(lambda x: x, color=RED, x_range=[0, 50], use_smoothing=False)
        new_O_n_log_n = new_axes.plot(lambda x: x * np.log(x), color=PURPLE, x_range=[1, 50], use_smoothing=False)
        new_O_n_squared = new_axes.plot(lambda x: x**2, color=ORANGE, x_range=[0, 50], use_smoothing=False)
        new_O_2_power_n = new_axes.plot(lambda x: 2**x, color=YELLOW, x_range=[0, 12], use_smoothing=False)
        new_x_values = range(0, 10)
        new_y_values = [np.math.factorial(x) for x in new_x_values]
        new_O_n_factorial = new_axes.plot_line_graph(new_x_values, new_y_values, line_color=PINK)

        # Transform old axes and functions to new axes and functions
        self.play(
            Transform(axes, new_axes),
            Transform(O_1, new_O_1),
            Transform(O_log_n, new_O_log_n),
            Transform(O_n, new_O_n),
            Transform(O_n_log_n, new_O_n_log_n),
            Transform(O_n_squared, new_O_n_squared),
            Transform(O_2_power_n, new_O_2_power_n),
            Transform(O_n_factorial, new_O_n_factorial),run_time=5
        )
        self.wait(2)
