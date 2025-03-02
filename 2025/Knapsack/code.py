from manimlib import *

PURE_RED = "#FF0000"
PURE_GREEN = "#00FF00"
PURE_BLUE = "#0000FF"

class Knapsack(Scene):

    def construct(self):


        knapsack = ImageMobject("knapsack.png").to_edge(DOWN).scale(0.8).shift(DOWN*0.4).set_z_index(1)
        self.play(GrowFromCenter(knapsack))
        self.wait(2)

        red = ImageMobject("red.png").scale(0.58).next_to(knapsack, UP, buff=1)
        teal = ImageMobject("teal.png").scale(0.58).next_to(red, LEFT, buff=0.78)
        brown = ImageMobject("brown.png").scale(0.58).next_to(red, RIGHT, buff=0.78)
        blue = ImageMobject("blue.png").scale(0.58).next_to(teal, LEFT, buff=0.78)
        yellow = ImageMobject("yellow.png").scale(0.58).next_to(brown, RIGHT, buff=0.78)
        self.play(GrowFromCenter(red), GrowFromCenter(teal), GrowFromCenter(brown), GrowFromCenter(blue), GrowFromCenter(yellow))
        self.wait(3)


        profit = Text("Profit = 0").set_color(BLACK).next_to(knapsack, LEFT, buff=0.7)
        weight = Text("Weight = 9").set_color(BLACK).next_to(knapsack, RIGHT, buff=0.7)
        self.play(Write(weight))
        self.wait(2)
        self.play(Write(profit))
        self.wait(2)



        self.play(Indicate(red))

        self.play(red.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("Profit = 70").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("Weight = 5").set_color(BLACK).move_to(weight)), run_time=0.5)
        self.wait()

        self.play(Indicate(teal))
        self.play(teal.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("Profit = 130").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("Weight = 2").set_color(BLACK).move_to(weight)), run_time=0.5)
        self.wait(1)

        self.play(Indicate(yellow))
        self.play(yellow.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("Profit = 160").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("Weight = 0").set_color(BLACK).move_to(weight)), run_time=0.5)
        self.wait(1)





        self.wait(2)






from manimlib import *

class KnapsackTable(Scene):
    def construct(self):
        # Define parameters
        capacity = 9
        num_items = 5
        
        # Example item values and weights
        values = [0, 20, 15, 30, 60, 70]  # Item 0 is a placeholder
        weights = [0, 2, 1, 2, 3, 4]      # Item 0 is a placeholder
        
        # Cell size
        cell_width = 0.8
        cell_height = 0.8
        
        # Create item details as a two-column table
        item_table = VGroup()
        
        # Create headers
        weight_header = Text("W", font_size=24)
        value_header = Text("$", font_size=24)
        headers = VGroup(weight_header, value_header)
        headers.arrange(RIGHT, buff=0.7)
        item_table.add(headers)
        
        # Add rows for weights and values
        for i in range(1, num_items + 1):
            weight_text = Text(f"{weights[i]}", font_size=22)
            value_text = Text(f"{values[i]}", font_size=22)
            row = VGroup(weight_text, value_text)
            row.arrange(RIGHT, buff=0.5)
            item_table.add(row)
        
        # Arrange item table vertically
        item_table.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        item_table.to_edge(LEFT, buff=1)
        item_table.shift(UP * 0.5)  # Adjust vertical position
        
        # Create table structure - position on right side
        table = VGroup()
        cells = {}
        cell_texts = {}
        
        # Calculate table width and height
        table_width = (capacity + 1) * cell_width
        table_height = (num_items + 1) * cell_height
        
        # Create cells
        for i in range(num_items + 1):
            for j in range(capacity + 1):
                cell = Rectangle(width=cell_width, height=cell_height)
                cell.set_stroke(WHITE, 1)
                
                # Position cells to the right of the item details
                x_pos = j * cell_width
                y_pos = -i * cell_height
                cell.move_to(np.array([x_pos, y_pos, 0]))
                
                # Add cell to table
                table.add(cell)
                cells[(i, j)] = cell
                
                # Add initial text (will be updated for DP calculation)
                if i == 0 or j == 0:
                    text = Text("0", font_size=22)
                    text.move_to(cell.get_center())
                    table.add(text)
                    cell_texts[(i, j)] = text
        
        # Add row labels (item numbers)
        for i in range(num_items + 1):
            label = Text(f"{i}" if i > 0 else "0", font_size=18)
            label.next_to(cells[(i, 0)], LEFT, buff=0.25)
            table.add(label)
        
        # Add column labels (weights)
        for j in range(capacity + 1):
            label = Text(f"{j}", font_size=18)
            label.next_to(cells[(0, j)], UP, buff=0.25)
            table.add(label)
        
        # Position table properly
        table.scale(1.1)  # Scale up for better visibility
        table.move_to(RIGHT * 2.5)  # Move to right side
                
        # Create title
        title = Text("Knapsack Problem (Capacity = 9, 5 items)", font_size=34)
        title.to_edge(UP, buff=0.5)
        
        # Create a section title for items
        items_title = Text("Items:", font_size=24)
        items_title.next_to(item_table, UP, buff=0.3)
        items_title.align_to(item_table, LEFT)

        items_title.scale(1.4)
        item_table.scale(1.4)

        table.shift(LEFT*1.1+DOWN*0.5)


        item_table.shift(DOWN*1.4+RIGHT*0.3)

        items_title.shift(DOWN*0.5+RIGHT*0.3)

        value_header.shift(LEFT*0.2)
        

        
        
        # Animation sequence
        self.play(Write(title))
        self.play(Write(items_title))
        self.play(FadeIn(item_table))
        self.play(ShowCreation(table))

        self.wait(2)



        
        # Fill the table with DP values (animate the calculation)
        dp = [[0 for _ in range(capacity + 1)] for _ in range(num_items + 1)]
        
        # Base case already filled with 0s
        
        # Fill the DP table
        for i in range(1, num_items + 1):
            for j in range(1, capacity + 1):
                # Highlight current cell
                current_cell = cells[(i, j)]
                self.play(current_cell.animate.set_fill(BLUE, opacity=0.3), run_time=0.3)
                
                if weights[i] <= j:
                    # Two options: include or exclude current item
                    value1 = dp[i-1][j]  # Exclude
                    value2 = values[i] + dp[i-1][j-weights[i]]  # Include
                    
                    # Highlight the cells we're comparing
                    above_cell = cells[(i-1, j)]
                    prev_cell = cells[(i-1, j-weights[i])] if j-weights[i] >= 0 else None
                    
                    self.play(above_cell.animate.set_fill(GREEN, opacity=0.3), run_time=0.7)
                    if prev_cell:
                        self.play(prev_cell.animate.set_fill(YELLOW, opacity=0.3), run_time=0.7)
                    
                    # Update current cell value
                    dp[i][j] = max(value1, value2)
                    new_text = Text(str(dp[i][j]), font_size=22)
                    new_text.move_to(current_cell.get_center())
                    
                    # Add the new text directly to the scene
                    self.play(FadeIn(new_text), run_time=0.3)
                    cell_texts[(i, j)] = new_text
                    
                    # Reset cell colors
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
                    # Just take the value from above
                    above_cell = cells[(i-1, j)]
                    self.play(above_cell.animate.set_fill(GREEN, opacity=0.3), run_time=0.7)
                    
                    dp[i][j] = dp[i-1][j]
                    new_text = Text(str(dp[i][j]), font_size=22)
                    new_text.move_to(current_cell.get_center())
                    
                    # Add the new text directly to the scene
                    self.play(FadeIn(new_text), run_time=0.3)
                    cell_texts[(i, j)] = new_text
                    
                    # Reset above cell color
                    self.play(
                        above_cell.animate.set_fill(opacity=0),
                        run_time=0.2
                    )
                
                # Reset current cell
                self.play(current_cell.animate.set_fill(opacity=0), run_time=0.2)
        
        # Highlight final answer
        final_cell = cells[(num_items, capacity)]
        self.play(
            final_cell.animate.set_fill(RED, opacity=0.5),
            run_time=1
        )
        
        self.wait(2)
