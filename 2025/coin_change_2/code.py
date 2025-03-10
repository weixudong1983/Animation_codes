from manimlib import *


class CoinChangeWays(Scene):
    def construct(self):
        # Define parameters
        coins = [1, 2, 5]  # Available coin denominations
        amount = 5  # Target amount
        
        # Cell size
        cell_width = 0.8
        cell_height = 0.8
        
        # Create coin details
        coin_table = VGroup()
        
        # Create header
        coin_header = Text("Coins", font_size=24)
        coin_table.add(coin_header)
        
        # Add rows for coin denominations
        for i in range(len(coins)):
            coin_text = Text(f"{i+1}: ${coins[i]}", font_size=22)
            coin_table.add(coin_text)
        
        # Arrange coin table vertically
        coin_table.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        coin_table.to_edge(LEFT, buff=1)
        coin_table.shift(UP * 0.5)
        
        # Create table structure - position on right side
        table = VGroup()
        cells = {}
        cell_texts = {}
        
        # Initialize DP array
        dp = [0] * (amount + 1)
        dp[0] = 1  # Base case
        
        # Create cells
        for j in range(amount + 1):
            cell = Rectangle(width=cell_width, height=cell_height)
            cell.set_stroke(WHITE, 1)
            
            x_pos = j * cell_width
            y_pos = 0
            cell.move_to(np.array([x_pos, y_pos, 0]))
            
            table.add(cell)
            cells[j] = cell
            
            # Initial DP values
            text = Text(str(dp[j]), font_size=34)
            text.move_to(cell.get_center())
            table.add(text)
            cell_texts[j] = text
        
        # Add column labels
        for j in range(amount + 1):
            label = Text(f"${j}", font_size=23)
            label.next_to(cells[j], UP, buff=0.25)
            table.add(label)
        
        # Position table properly
        table.scale(1.1)
        table.move_to(RIGHT * 2.5 + DOWN * 1)
        
        # Title
        title = Text(f"Coin Change Problem: Ways to Make ${amount}", font_size=30)
        title.to_edge(UP, buff=0.5)
        
        coin_table.scale(1.4)
        coin_table.shift(DOWN * 0.94 + RIGHT * 0.3)
        
        # Animation sequence
        self.play(Write(title))
        self.play(FadeIn(coin_table))
        table.scale(1.45).shift(LEFT+UP*0.84)
        self.play(ShowCreation(table))
        self.wait(1)

        
        explanation = Text("Step 1: Initialize DP[0] = 1", font_size=34)
        explanation.to_edge(DOWN, buff=1)
        self.play(Write(explanation))
        self.wait(1)
        
        rect = SurroundingRectangle(coin_table[1], color=YELLOW, stroke_width=7).scale(1.22)
        self.play(ShowCreation(rect))
        
        # Fill DP table for number of ways
        for i, coin in enumerate(coins):
            new_explanation = Text(f"Using Coin ${coin}", font_size=40)
            new_explanation.to_edge(DOWN, buff=1)
            self.play(Transform(explanation, new_explanation))
            self.play(Transform(rect, SurroundingRectangle(coin_table[i+1], color=YELLOW, stroke_width=7).scale(1.22)))
            
            for j in range(coin, amount + 1):
                # Highlight cells
                current_cell = cells[j]
                prev_cell = cells[j - coin]
                self.play(current_cell.animate.set_fill(BLUE, opacity=0.4), run_time=1.2)
                self.play(prev_cell.animate.set_fill(GREEN, opacity=0.3), run_time=1.2)
                
                # Update DP value
                dp[j] += dp[j - coin]
                new_text = Text(str(dp[j]), font_size=34).scale(1.55)
                new_text.move_to(current_cell.get_center())
                
                self.play(FadeOut(cell_texts[j]), run_time=0.5)
                self.play(FadeIn(new_text), run_time=0.5)
                cell_texts[j] = new_text
                
                # Reset cell colors
                self.play(
                    prev_cell.animate.set_fill(opacity=0),
                    run_time=0.2
                )
                self.play(current_cell.animate.set_fill(opacity=0), run_time=0.2)
        
        # Highlight final answer
        final_cell = cells[amount]
        self.play(
            final_cell.animate.set_fill(RED, opacity=0.5),
            run_time=1
        )
        
        # Show final result explanation
        final_explanation = Text(f"Ways to make ${amount}: {dp[amount]}", font_size=38)
        final_explanation.to_edge(DOWN, buff=1)
        self.play(Transform(explanation, final_explanation), Uncreate(rect))
        self.wait(2)




class Coins1(Scene):

    def construct(self):
        
        coins = Text("coins = [1, 2, 5]").to_edge(UP).shift(DOWN*0.3)
        amount = Text("Target = 5").next_to(coins, DOWN, buff=0.7)

        self.play(ShowCreation(coins))
        self.wait(2)
        self.play(ShowCreation(amount))
        self.wait()
        self.play(self.camera.frame.animate.shift(RIGHT*2.2))
        text = Text("infinite supply").next_to(coins, RIGHT).scale(0.66).set_color(GREEN)
        self.play(ShowCreation(text))

        self.wait(2)

        temp_1 = Text("1, 1, 1, 1, 1").scale(0.9).shift(RIGHT*2)
        temp_2 = Text("1, 1, 1, 2").scale(0.9).next_to(temp_1, DOWN, buff=0.5)
        temp_3 = Text("1, 2, 2").scale(0.9).next_to(temp_2, DOWN, buff=0.5)
        temp_4 = Text("5").scale(0.9).next_to(temp_3, DOWN, buff=0.5)
        self.play(Write(temp_1))
        self.wait(2)

        self.play(Write(temp_2))
        self.wait(2)
        self.play(Write(temp_3))
        self.wait()
        self.play(Write(temp_4))
        self.wait(2)

        brace = Brace(VGroup(temp_1, temp_4), RIGHT, buff=0.5)
        self.play(GrowFromCenter(brace))
        text = Text("4 ways").next_to(brace, RIGHT, buff=0.5)
        self.play(Write(text))

        self.wait(2)










        self.embed()

