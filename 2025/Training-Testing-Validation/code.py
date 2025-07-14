from manimlib import *
import numpy as np

DARK_BLUE = BLUE_E

class TrainingDemo(Scene):
    def construct(self):
        self.camera.frame.scale(1.4)  # Zoom out
        
        # Axes
        axes = Axes(
            x_range=[0, 15],
            y_range=[0, 8],
            axis_config={"include_ticks": False, "include_numbers": False, "stroke_width": 8},
        )
        axes.set_color(BLACK)
        
        x_label = Text("x", weight=BOLD).next_to(axes.x_axis, DOWN).shift(RIGHT * 7.6 + DOWN * 0.4).scale(1.77)
        x_label.set_color(BLACK)
        
        y_label = Text("y", weight=BOLD).next_to(axes.y_axis, UP).shift(UP * 0.1).scale(1.7)
        y_label.set_color(BLACK)
        
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        self.wait(1)
        
        # Create fewer but more spaced points
        np.random.seed(10)
        x_values = np.array([
            # Well-spaced points across the range
            1.5, 2.8, 4.2, 5.6, 7.0, 8.4, 9.8, 11.2, 12.6, 14.0,
            2.0, 3.5, 5.0, 6.5, 8.0, 9.5, 11.0, 12.5, 13.8,
            1.8, 3.2, 4.8, 6.2, 7.5, 9.0, 10.5, 12.0, 13.5,
            2.5, 4.0, 5.5, 7.2, 8.8, 10.2, 11.8, 13.2
        ])  # 35 points total - fewer but well distributed
        
        # Create a rough sinusoidal pattern with more variation and noise
        # Base pattern with multiple frequency components and random variations
        y_base = 1.5 * np.sin(0.7 * x_values) + 0.8 * np.sin(1.2 * x_values) + 4
        y_values = y_base + np.random.normal(0, 0.5, size=len(x_values))  # More noise for roughness
        
        # Add some random outliers to make it less strictly sinusoidal
        outlier_indices = [3, 8, 15, 22, 28]
        for idx in outlier_indices:
            if idx < len(y_values):
                y_values[idx] += np.random.normal(0, 0.8)
        
        # Keep y values within bounds
        y_values = np.clip(y_values, 1, 7)
        
        dots = VGroup(*[
            Dot(axes.coords_to_point(x_values[i], y_values[i]), radius=0.20*1.23).set_color(GREY_C)
            for i in range(len(x_values))
        ])
        
        # Fade in all points initially as GREY
        self.play(LaggedStart(*[ShowCreation(dot) for dot in dots], lag_ratio=0.05), run_time=2)
        self.wait(1)
        
        # Define indices for splits - 6:2:2 ratio with strategic distribution
        # Train: 60% (21 points), Val: 20% (7 points), Test: 20% (7 points)
        total_points = len(x_values)
        train_count = int(0.6 * total_points)  # 21 points
        val_count = int(0.2 * total_points)    # 7 points
        test_count = total_points - train_count - val_count  # 7 points
        
        # Strategic distribution instead of random
        # Sort points by x-value for better distribution
        sorted_indices = np.argsort(x_values)
        
        # Distribute validation and test points evenly across x-range
        train_idx = []
        val_idx = []
        test_idx = []
        
        # Take every 5th point for validation, every 5th+1 for test, rest for training
        for i, idx in enumerate(sorted_indices):
            if i % 5 == 0 and len(val_idx) < val_count:
                val_idx.append(idx)
            elif i % 5 == 1 and len(test_idx) < test_count:
                test_idx.append(idx)
            else:
                train_idx.append(idx)
        
        # Fill remaining slots with training data
        remaining_indices = [idx for idx in sorted_indices if idx not in val_idx + test_idx]
        train_idx.extend(remaining_indices[:train_count - len(train_idx)])
        
        # Sort indices for cleaner visualization
        train_idx.sort()
        val_idx.sort()
        test_idx.sort()
        
        # Animate color changes
        train_dots = [dots[i] for i in train_idx]
        val_dots = [dots[i] for i in val_idx]
        test_dots = [dots[i] for i in test_idx]
        
        self.play(*[dot.animate.set_color(GREEN) for dot in train_dots])
        self.play(*[dot.animate.set_color(BLUE) for dot in val_dots])
        self.play(*[dot.animate.set_color(RED) for dot in test_dots])
        self.wait(1)

        # Create labels for data types
        training_label = Text("Training", weight=BOLD).scale(1).set_color(GREEN)
        validation_label = Text("Validation", weight=BOLD, color=BLUE).scale(1).set_color(BLUE)
        testing_label = Text("Testing", weight=BOLD, color=RED).scale(1).set_color(RED)
        
        # Stack them vertically at the top of the screen
        labels = VGroup(training_label, validation_label, testing_label).arrange(RIGHT, buff=0.7).scale(1.2)
        labels.to_corner(UL).shift(RIGHT*0.3 + UP * 1)
        
        # Show the labels
        self.play(ShowCreation(labels))
        self.wait(2)
        
        # Fade out validation and test points - only keep training
        self.play(FadeOut(VGroup(*val_dots)), FadeOut(VGroup(*test_dots)), FadeOut(labels), run_time=1.5)
        
        # Create curve fitting iterations
        curve_x = np.linspace(1.5, 15, 200)  # Extended range to cover new points
        
        def create_curve(fit_y, color=DARK_BLUE, stroke_width=10):
            curve_points = [
                axes.coords_to_point(curve_x[i], fit_y[i])
                for i in range(len(curve_x))
            ]
            curve = VMobject()
            curve.set_color(color)
            curve.set_stroke(width=stroke_width)
            curve.set_points_smoothly(curve_points)
            return curve
        
        # Training iterations - faster transforms
        # Iteration 1: Start with a straight line (linear fit)
        iteration1_fit_y = 4 + 0.1 * (curve_x - 7.5)  # Slight slope
        current_curve = create_curve(iteration1_fit_y, DARK_BLUE, 10)
        self.play(ShowCreation(current_curve), run_time=1)
        self.wait(0.5)
        
        # Iteration 2: Add some curvature but wrong frequency
        iteration2_fit_y = 4 + 0.3 * np.sin(0.3 * curve_x)  # Too low frequency
        new_curve2 = create_curve(iteration2_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve2), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 3: Better frequency but wrong amplitude
        iteration3_fit_y = 4 + 0.8 * np.sin(0.6 * curve_x)  # Getting closer
        new_curve3 = create_curve(iteration3_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve3), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 4: Almost there - correct frequency, close amplitude
        iteration4_fit_y = 4 + 1.2 * np.sin(0.7 * curve_x) + 0.3 * np.sin(1.1 * curve_x)  # Multi-frequency
        new_curve4 = create_curve(iteration4_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve4), run_time=0.5)
        self.wait(0.5)
        
        # Now bring in validation set for evaluation (fade out training)
        validation_label_solo = Text("Validation", weight=BOLD, color=BLUE).scale(1.2).set_color(BLUE)
        validation_label_solo.to_corner(UL).shift(RIGHT*0.3 + UP * 1)
        
        self.play(
            FadeOut(VGroup(*train_dots)), 
            FadeIn(VGroup(*val_dots)), 
            ShowCreation(validation_label_solo), 
            run_time=1.5
        )
        self.wait(2)  # Wait 2 seconds to check validation performance
        
        # Fade out validation data and bring back training data
        training_label_solo = Text("Training", weight=BOLD, color=GREEN).scale(1.2).set_color(GREEN)
        training_label_solo.to_corner(UL).shift(RIGHT*0.3 + UP * 1)
        
        self.play(
            FadeOut(VGroup(*val_dots)), 
            FadeOut(validation_label_solo),
            FadeIn(VGroup(*train_dots)),
            ShowCreation(training_label_solo),
            run_time=1
        )
        
        # More precise fitting iterations based on validation feedback
        # Iteration 5: Adjust based on validation
        iteration5_fit_y = 4 + 1.4 * np.sin(0.7 * curve_x) + 0.5 * np.sin(1.2 * curve_x)
        new_curve5 = create_curve(iteration5_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve5), run_time=0.5)
        self.wait(0.5)
        
        # Iteration 6: Fine-tune amplitude
        iteration6_fit_y = 4 + 1.3 * np.sin(0.7 * curve_x) + 0.6 * np.sin(1.2 * curve_x) + 0.1 * np.sin(2.0 * curve_x)
        new_curve6 = create_curve(iteration6_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, new_curve6), run_time=0.5)
        self.wait(0.5)
        
        # Check validation again (fade out training, fade in validation)
        self.play(
            FadeOut(VGroup(*train_dots)),
            FadeOut(training_label_solo),
            FadeIn(VGroup(*val_dots)), 
            ShowCreation(validation_label_solo), 
            run_time=1.5
        )
        self.wait(2)  # Wait 2 seconds to check validation performance again
        
        # Fade out validation data and bring back training for final iteration
        self.play(
            FadeOut(VGroup(*val_dots)), 
            FadeOut(validation_label_solo),
            FadeIn(VGroup(*train_dots)),
            ShowCreation(training_label_solo),
            run_time=1
        )
        
        # Final training iteration
        final_fit_y = 4 + 1.35 * np.sin(0.7 * curve_x) + 0.65 * np.sin(1.2 * curve_x) + 0.15 * np.sin(1.8 * curve_x)
        final_curve = create_curve(final_fit_y, DARK_BLUE, 10)
        self.play(Transform(current_curve, final_curve), run_time=0.5)
        self.wait(1)
        
        # Fade out training data only
        self.play(FadeOut(VGroup(*train_dots)), FadeOut(training_label_solo), run_time=1.5)
        self.wait(1)
        
        # Final testing phase
        testing_label_solo = Text("Testing", weight=BOLD, color=RED).scale(1.2).set_color(RED)
        testing_label_solo.to_corner(UL).shift(RIGHT*0.3 + UP * 1)
        
        self.play(FadeIn(VGroup(*test_dots)), ShowCreation(testing_label_solo), run_time=1.5)
        self.wait(3)  # Give time to observe how well the model performs on test data
