from manim import *

PURE_RED = "#FF0000"
PURE_GREEN = "#00FF00"
PURE_BLUE = "#0000FF"

class Knapsack(Scene):

    def construct(self):

        knapsack = ImageMobject("knapsack.png").scale(0.5)
        knapsack.to_edge(DOWN, buff=0.5)  # 增加buff距离底部
        knapsack.shift(DOWN * 0.4)  # 再向下移动
        knapsack.set_z_index(1)
        self.play(GrowFromCenter(knapsack))
        self.wait(2)

        red = ImageMobject("red.png").scale(0.58).next_to(knapsack, UP, buff=1)
        teal = ImageMobject("teal.png").scale(0.58).next_to(red, LEFT, buff=0.78)
        brown = ImageMobject("brown.png").scale(0.58).next_to(red, RIGHT, buff=0.78)
        blue = ImageMobject("blue.png").scale(0.58).next_to(teal, LEFT, buff=0.78)
        yellow = ImageMobject("yellow.png").scale(0.58).next_to(brown, RIGHT, buff=0.78)
        self.play(GrowFromCenter(red), GrowFromCenter(teal), GrowFromCenter(brown), 
                  GrowFromCenter(blue), GrowFromCenter(yellow))
        self.wait(3)
        

        profit = Text("利润 = 0", color=BLACK).next_to(knapsack, LEFT, buff=0.7)
        weight = Text("重量 = 9", color=BLACK).next_to(knapsack, RIGHT, buff=0.7)
        self.play(Write(weight))
        self.wait(2)
        self.play(Write(profit))
        self.wait(2)

        self.play(Indicate(red))

        self.play(red.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("利润 = 70", color=BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("重量 = 5", color=BLACK).move_to(weight)), run_time=0.5)
        self.wait()

        self.play(Indicate(teal))
        self.play(teal.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("利润 = 130", color=BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("重量 = 2", color=BLACK).move_to(weight)), run_time=0.5)
        self.wait(1)

        self.play(Indicate(yellow))
        self.play(yellow.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("利润 = 160", color=BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("重量 = 0", color=BLACK).move_to(weight)), run_time=0.5)
        self.wait(1)

        self.wait(2)


class KnapsackTable(Scene):
    def construct(self):
        # 定义参数
        capacity = 7
        num_items = 5
        
        # 示例物品价值和重量
        values = [0, 50, 40, 70, 80, 10]  # 物品0是占位符
        weights = [0, 3, 2, 4, 5, 1]     # 物品0是占位符
        
        # 添加C++代码说明
        cpp_code = """
        // C++背包问题动态规划算法
        int knapsack(int W, vector<int>& weights, vector<int>& values, int n) {
            vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
            
            for (int i = 1; i <= n; i++) {
                for (int w = 1; w <= W; w++) {
                    if (weights[i-1] <= w) {
                        dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], 
                                      dp[i-1][w]);
                    } else {
                        dp[i][w] = dp[i-1][w];
                    }
                }
            }
            return dp[n][W];
        }
        """
        
        # 单元格大小
        cell_width = 0.8
        cell_height = 0.8
        
        # 创建物品详情表格
        item_table = VGroup()
        
        # 创建表头
        weight_header = Text("重量", font_size=24)
        value_header = Text("价值", font_size=24)
        headers = VGroup(weight_header, value_header)
        headers.arrange(RIGHT, buff=0.7)
        item_table.add(headers)
        
        # 添加重量和价值行
        for i in range(1, num_items + 1):
            weight_text = Text(f"物品 {i}: {weights[i]}  {values[i]}", font_size=22)
            row = VGroup(weight_text)
            row.arrange(RIGHT, buff=0.5)
            item_table.add(row)
        
        # 垂直排列物品表格
        item_table.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        item_table.to_edge(LEFT, buff=1)
        item_table.shift(UP * 0.5)
        
        # 创建表格结构 - 位置在右侧
        table = VGroup()
        cells = {}
        cell_texts = {}
        
        # 计算表格宽度和高度
        table_width = (capacity + 1) * cell_width
        table_height = (num_items + 1) * cell_height
        
        # 创建单元格
        for i in range(num_items + 1):
            for j in range(capacity + 1):
                cell = Rectangle(width=cell_width, height=cell_height)
                cell.set_stroke(WHITE, 1)
                
                # 将单元格定位到物品详情的右侧
                x_pos = j * cell_width
                y_pos = -i * cell_height
                cell.move_to(np.array([x_pos, y_pos, 0]))
                
                # 将单元格添加到表格
                table.add(cell)
                cells[(i, j)] = cell
                
                # 添加初始文本（将在DP计算中更新）
                if i == 0 or j == 0:
                    text = Text("0", font_size=22)
                    text.move_to(cell.get_center())
                    table.add(text)
                    cell_texts[(i, j)] = text
        
        # 添加行标签（物品编号）
        for i in range(num_items + 1):
            label = Text(f"{i}" if i > 0 else "0", font_size=18)
            label.next_to(cells[(i, 0)], LEFT, buff=0.25)
            table.add(label)
        
        # 添加列标签（重量）
        for j in range(capacity + 1):
            label = Text(f"{j}", font_size=18)
            label.next_to(cells[(0, j)], UP, buff=0.25)
            table.add(label)
        
        # 正确定位表格
        table.scale(1.1)  # 放大以便更好地查看
        table.move_to(RIGHT * 2.5)  # 移动到右侧
                
        # 创建标题
        title = Text("背包问题 (容量 = 9, 5个物品)", font_size=34)
        title.to_edge(UP, buff=0.5)
        
        item_table.scale(1.4)
        table.shift(LEFT*0.5+DOWN*0.5)
        item_table.shift(DOWN*0.94+RIGHT*0.3)
        value_header.shift(RIGHT*1.7)
        weight_header.next_to(value_header, LEFT, buff=0.7)
        
        # 动画序列
        self.play(Write(title))
        self.play(FadeIn(item_table))
        self.play(Create(table))

        self.wait(2)

        rect = SurroundingRectangle(item_table[1], color=YELLOW, stroke_width=7).scale(1.234)
        self.play(Create(rect))

        # 用DP值填充表格（动画化计算过程）
        dp = [[0 for _ in range(capacity + 1)] for _ in range(num_items + 1)]
        
        # 基础情况已经用0填充
        
        # 填充DP表格
        for i in range(1, num_items + 1):
            if i >= 2:
                self.play(Transform(rect, SurroundingRectangle(item_table[i], color=YELLOW, stroke_width=7).scale(1.234)))
            for j in range(1, capacity + 1):
                # 高亮当前单元格
                current_cell = cells[(i, j)]
                self.play(current_cell.animate.set_fill(BLUE, opacity=0.39), run_time=1)
                
                if weights[i] <= j:
                    # 两个选择：包含或排除当前物品
                    value1 = dp[i-1][j]  # 排除
                    value2 = values[i] + dp[i-1][j-weights[i]]  # 包含
                    
                    # 高亮我们正在比较的单元格
                    above_cell = cells[(i-1, j)]
                    prev_cell = cells[(i-1, j-weights[i])] if j-weights[i] >= 0 else None
                    
                    self.play(above_cell.animate.set_fill(GREEN, opacity=0.3), run_time=1)
                    if prev_cell:
                        self.play(prev_cell.animate.set_fill(YELLOW, opacity=0.3), run_time=1)
                    
                    # 更新当前单元格值
                    dp[i][j] = max(value1, value2)
                    new_text = Text(str(dp[i][j]), font_size=22)
                    new_text.move_to(current_cell.get_center())
                    
                    # 直接将新文本添加到场景
                    self.play(FadeIn(new_text), run_time=0.9)
                    cell_texts[(i, j)] = new_text
                    
                    # 重置单元格颜色
                    self.play(
                        above_cell.animate.set_fill(opacity=0),
                        run_time=0.2
                    )
                    if prev_cell:
                        self.play(
                            prev_cell.animate.set_fill(opacity=0),
                            run_time=0.2
                        )
                else:
                    # 只取上面的值
                    above_cell = cells[(i-1, j)]
                    self.play(above_cell.animate.set_fill(GREEN, opacity=0.35), run_time=1)
                    
                    dp[i][j] = dp[i-1][j]
                    new_text = Text(str(dp[i][j]), font_size=22)
                    new_text.move_to(current_cell.get_center())
                    
                    # 直接将新文本添加到场景
                    self.play(FadeIn(new_text), run_time=1)
                    cell_texts[(i, j)] = new_text
                    
                    # 重置上面单元格颜色
                    self.play(
                        above_cell.animate.set_fill(opacity=0),
                        run_time=0.2
                    )
                
                # 重置当前单元格
                self.play(current_cell.animate.set_fill(opacity=0), run_time=0.2)
        
        # 高亮最终答案
        final_cell = cells[(num_items, capacity)]
        self.play(
            final_cell.animate.set_fill(RED, opacity=0.5),
            run_time=1
        )
        
        self.wait(2)

        self.play(cells[(4,7)].animate.set_fill(YELLOW, opacity=0.5))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(item_table[4], color=YELLOW, stroke_width=7).scale(1.234)),
            cells[(4,7)].animate.set_fill(RED, opacity=0.5),
            cells[(5,7)].animate.set_fill(YELLOW, opacity=0),
        )
        
        self.wait()

        self.play(cells[(3,7)].animate.set_fill(YELLOW, opacity=0.5))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(item_table[3], color=YELLOW, stroke_width=7).scale(1.234)),
            cells[(3,7)].animate.set_fill(RED, opacity=0.5),
            cells[(4,7)].animate.set_fill(YELLOW, opacity=0),
        )
        
        self.wait()

        self.play(cells[(2,7)].animate.set_fill(YELLOW, opacity=0.5))
        self.wait(2)

        self.play(
            cells[(3,7)].animate.set_fill(GREEN, opacity=0.5),
            cells[(2,7)].animate.set_fill(GREEN, opacity=0),
        )
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(item_table[2], color=YELLOW, stroke_width=7).scale(1.234)),
            cells[(2,3)].animate.set_fill(RED, opacity=0.5),
        )
        self.wait(1)

        self.play(cells[(1,3)].animate.set_fill(YELLOW, opacity=0.5))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(item_table[1], color=YELLOW, stroke_width=7).scale(1.234)),
            cells[(1,3)].animate.set_fill(RED, opacity=0.5),
            cells[(2,3)].animate.set_fill(RED, opacity=0),
        )
        self.wait()

        self.play(cells[(0,3)].animate.set_fill(YELLOW, opacity=0.5))

        self.wait(2)

        self.play(
            cells[(0,3)].animate.set_fill(RED, opacity=0),
            cells[(1,3)].animate.set_fill(GREEN, opacity=0.5),
            Unwrite(rect)
        )

        self.wait(2)