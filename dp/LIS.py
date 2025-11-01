from manim import *


class ArrayArrowAnimation(Scene):
    def construct(self):
        # 参数配置
        array_values = [0, 1, 0, 3, 2, 3]
        box_width = 1.2
        box_height = 1.2

        # 绘制数组方格
        boxes = VGroup()
        labels = VGroup()

        for i, val in enumerate(array_values):
            box = Square(side_length=box_width, color=WHITE)
            box.move_to(RIGHT * i * box_width)
            text = Text(str(val), font_size=36).move_to(box.get_center())
            boxes.add(box)
            labels.add(text)

        array_group = VGroup(boxes, labels).move_to(ORIGIN)
        self.play(Create(boxes), Write(labels))
        self.wait(0.5)

        # 高亮某些格子
        highlight_indices = [0, 1, 4]
        for idx in highlight_indices:
            self.play(boxes[idx].animate.set_fill(GREEN, opacity=0.6), run_time=0.3)

        # 创建函数：绘制带动画的箭头
        def draw_arrow(start_idx, end_idx, color=ORANGE):
            start = boxes[start_idx].get_bottom()
            end = boxes[end_idx].get_bottom()
            # 控制箭头弧度（向下弯曲）
            arrow = CurvedArrow(start, end, angle=-PI / 2.5, color=color, stroke_width=6)
            self.play(Create(arrow), run_time=1)
            return arrow

        # 示例：按索引画箭头
        arrow1 = draw_arrow(1, 0)
        arrow2 = draw_arrow(4, 1)

        self.wait(1)
        self.play(FadeOut(arrow1), FadeOut(arrow2))
        self.wait()

class LISVisualization(MovingCameraScene):
    def construct(self):

        self.camera.frame.shift(UP*0.3).scale(0.93)
        # Define the input array
        nums = [0, 1, 0, 3, 2, 3]
        n = len(nums)
        
        # Initialize DP array
        dp = [1] * n
        
        # Create title
        title = Text("Longest Increasing Subsequence", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create continuous connected arrays
        cell_size = 0.8
        
        # Position for arrays - input array on top, dp array below
        array_y = 1.5
        dp_y = 0
        arrays_center_x = 0
        
        # Create the arrays as connected squares
        nums_squares = []
        nums_labels = []
        dp_squares = []
        dp_labels = []
        index_labels = []
        
        for i in range(n):
            # Position calculations
            x_pos = arrays_center_x - ((n-1)/2 * cell_size) + i * cell_size
            
            # Input array squares
            nums_square = Square(side_length=cell_size)
            nums_square.set_stroke(WHITE, 2)
            nums_square.move_to([x_pos, array_y, 0])
            nums_squares.append(nums_square)
            
            # DP array squares
            dp_square = Square(side_length=cell_size)
            dp_square.set_stroke(WHITE, 2)
            dp_square.move_to([x_pos, dp_y, 0])
            dp_squares.append(dp_square)
            
            # Index labels (below dp array)
            index_label = Text(str(i), font_size=20)
            index_label.move_to([x_pos, dp_y - cell_size, 0])
            index_labels.append(index_label)
        
        # Create explanation box higher up to allow room for zooming
        explanation_box = Rectangle(width=12, height=1.5, fill_color=BLACK, fill_opacity=0.8)
        explanation_box.move_to([0, -2, 0])  # Positioned higher than before
        explanation = Text("Starting LIS algorithm...", font_size=24)
        explanation.move_to(explanation_box.get_center())



        
        # Create i and j pointers between the arrays - just text, no triangles
        pointer_y = (array_y + dp_y) / 2
        
        i_label = Text("i", font_size=28, color=YELLOW)
        i_group = i_label  # Now just the text
        i_group.move_to([arrays_center_x - ((n-1)/2 * cell_size) - cell_size, pointer_y, 0])
        
        j_label = Text("j", font_size=25, color=BLUE)
        j_group = j_label  # Now just the text
        j_group.move_to([arrays_center_x - ((n-1)/2 * cell_size) - cell_size, pointer_y, 0])
        j_group.next_to(i_group, LEFT)
        # Display arrays (squares first)
        self.play(
            *[Create(square) for square in nums_squares],
            *[Create(square) for square in dp_squares]
        )
        
        # Create labels for array values - after squares so they're at higher z-index
        for i in range(n):
            x_pos = arrays_center_x - ((n-1)/2 * cell_size) + i * cell_size
            
            # Input array values
            nums_label = Text(str(nums[i]), font_size=28)
            nums_label.move_to([x_pos, array_y, 0])
            nums_labels.append(nums_label)
            
            # DP array values
            dp_label = Text(str(dp[i]), font_size=28)
            dp_label.move_to([x_pos, dp_y, 0])
            dp_labels.append(dp_label)
        
        # Now add the value labels and index labels
        self.play(
            *[Write(label) for label in nums_labels],
            *[Write(label) for label in dp_labels],
            *[Write(label) for label in index_labels]
        )
        
        # Add array labels on the side
        input_label = Text("Input", font_size=20).next_to(nums_squares[0], LEFT, buff=0.5)
        dp_label = Text("DP", font_size=20).next_to(dp_squares[0], LEFT, buff=0.5)
        
        self.play(Write(input_label), Write(dp_label))
        
        # Add explanation box and pointers
        self.play(
            Create(explanation_box),
            Write(explanation),
            Create(i_group),
            Create(j_group)
        )


        
        # Run algorithm with animations
        for i in range(n):
            # Calculate i pointer position
            i_x = arrays_center_x - ((n-1)/2 * cell_size) + i * cell_size
            
            # Move i pointer to position i
            new_explanation = Text(f"Checking element at index i={i}", font_size=24)
            new_explanation.move_to(explanation_box.get_center())
            
            self.play(
                i_group.animate.move_to([i_x, pointer_y, 0]),
                ReplacementTransform(explanation, new_explanation)
            )
            explanation = new_explanation
            
            # Highlight current element in both arrays
            nums_highlight = nums_squares[i].copy().set_fill(YELLOW, opacity=0.3)
            dp_highlight = dp_squares[i].copy().set_fill(YELLOW, opacity=0.3)
            
            self.play(
                Create(nums_highlight),
                Create(dp_highlight)
            )
            
            for j in range(i):
                # Calculate j pointer position
                j_x = arrays_center_x - ((n-1)/2 * cell_size) + j * cell_size
                
                # Move j pointer to position j
                new_explanation = Text(f"Compare nums[{j}]={nums[j]} with nums[{i}]={nums[i]}", font_size=24)
                new_explanation.move_to(explanation_box.get_center())
                
                self.play(
                    j_group.animate.move_to([j_x, pointer_y, 0]),
                    ReplacementTransform(explanation, new_explanation)
                )
                explanation = new_explanation
                
                # Highlight element j
                j_nums_highlight = nums_squares[j].copy().set_fill(BLUE, opacity=0.3)
                j_dp_highlight = dp_squares[j].copy().set_fill(BLUE, opacity=0.3)
                
                self.play(
                    Create(j_nums_highlight),
                    Create(j_dp_highlight)
                )
                
                if nums[j] < nums[i]:
                    # Valid increasing subsequence
                    comp_color = GREEN
                    new_explanation = Text(f"nums[{j}]={nums[j]} < nums[{i}]={nums[i]}, can extend LIS", font_size=24)
                    new_explanation.move_to(explanation_box.get_center())
                    
                    self.play(
                        ReplacementTransform(explanation, new_explanation),
                        j_nums_highlight.animate.set_fill(GREEN, opacity=0.4),
                        j_dp_highlight.animate.set_fill(GREEN, opacity=0.4)
                    )
                    self.wait()
                    explanation = new_explanation
                    
                    # Show potential dp value
                    potential_dp = dp[j] + 1
                    potential_text = Text(f"dp[{i}] = max({dp[i]}, dp[{j}]+1) = max({dp[i]}, {potential_dp})", font_size=24)
                    potential_text.move_to(explanation_box.get_center())
                    
                    self.play(ReplacementTransform(explanation, potential_text))
                    self.wait()
                    explanation = potential_text
                    
                    if potential_dp > dp[i]:
                        # Update dp[i]
                        old_dp = dp[i]
                        dp[i] = potential_dp
                        
                        update_text = Text(f"Update dp[{i}] from {old_dp} to {dp[i]}", font_size=24)
                        update_text.move_to(explanation_box.get_center())
                        
                        self.play(ReplacementTransform(explanation, update_text))
                        self.wait()
                        explanation = update_text
                        
                        # Update dp value - create new label to ensure it stays on top
                        new_dp_label = Text(str(dp[i]), font_size=28)
                        new_dp_label.move_to(dp_squares[i].get_center())
                        
                        self.play(
                            ReplacementTransform(dp_labels[i], new_dp_label),
                            Flash(dp_squares[i], color=PINK, flash_radius=0.7)
                        )
                        dp_labels[i] = new_dp_label
                    else:
                        no_update = Text(f"No update needed: {potential_dp} <= {dp[i]}", font_size=24)
                        no_update.move_to(explanation_box.get_center())
                        
                        self.play(ReplacementTransform(explanation, no_update))
                        explanation = no_update
                else:
                    # Not valid for increasing subsequence
                    new_explanation = Text(f"nums[{j}]={nums[j]} >= nums[{i}]={nums[i]}, cannot extend", font_size=24)
                    new_explanation.move_to(explanation_box.get_center())
                    
                    self.play(
                        ReplacementTransform(explanation, new_explanation),
                        j_nums_highlight.animate.set_fill(RED, opacity=0.4),
                        j_dp_highlight.animate.set_fill(RED, opacity=0.4)
                    )
                    self.wait()
                    explanation = new_explanation
                
                # Remove j highlights (but don't fade out pointer)
                self.play(
                    FadeOut(j_nums_highlight),
                    FadeOut(j_dp_highlight)
                )
            
            # Inner loop complete
            i_done_text = Text(f"Completed processing for i={i}, dp[{i}]={dp[i]}", font_size=24)
            i_done_text.move_to(explanation_box.get_center())
            
            self.play(ReplacementTransform(explanation, i_done_text))
            explanation = i_done_text
            
            # Remove i highlights but keep the pointer
            self.play(
                FadeOut(nums_highlight),
                FadeOut(dp_highlight)
            )
        
        # Algorithm complete
        result_text = Text(f"Final DP array. LIS length = {max(dp)}", font_size=24)
        result_text.move_to(explanation_box.get_center())
        
        self.play(ReplacementTransform(explanation, result_text))
        
        # Highlight max dp values
        max_dp = max(dp)
        max_highlights = []
        
        for i, val in enumerate(dp):
            if val == max_dp:
                highlight = dp_squares[i].copy().set_fill(GREEN, opacity=0.5)
                max_highlights.append(highlight)
        
        self.play(*[Create(h) for h in max_highlights])
        
        # Find and display one possible LIS
        lis_indices = self.get_lis_indices(nums, dp)
        lis = [nums[i] for i in lis_indices]

        self.play(self.camera.frame.animate.scale(1/0.93).shift(DOWN*0.3))

        
        lis_text = Text(f"One possible LIS: {lis}", font_size=24)
        lis_text.next_to(explanation_box, DOWN, buff=0.5)
        self.play(Write(lis_text))
        
        # Highlight LIS in the input array
        lis_highlights = []
        
        for idx in lis_indices:
            highlight = nums_squares[idx].copy().set_fill(PURPLE, opacity=0.5)
            lis_highlights.append(highlight)
        
        self.play(*[Create(h) for h in lis_highlights])
        
        # Pause at the end
        self.wait(3)
    
    def get_lis_indices(self, nums, dp):
        """Get the indices of one possible Longest Increasing Subsequence"""
        max_length = max(dp)
        end_index = dp.index(max_length)
        
        result = [end_index]
        current_length = max_length
        current_index = end_index
        
        for i in range(end_index - 1, -1, -1):
            if dp[i] == current_length - 1 and nums[i] < nums[current_index]:
                result.append(i)
                current_length -= 1
                current_index = i
        
        return result[::-1]  # Reverse to get correct order
