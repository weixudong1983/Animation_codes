from manimlib import *


class Coins(Scene):

    def construct(self):
        
        coins = Text("coins = [1, 4, 6]").to_edge(UP).shift(DOWN*0.3)
        amount = Text("Amount = 9").next_to(coins, DOWN, buff=0.7)

        self.play(ShowCreation(coins))
        self.wait(2)
        self.play(ShowCreation(amount))
        self.wait()
        self.play(self.camera.frame.animate.shift(RIGHT*2.2))
        text = Text("infinite supply").next_to(coins, RIGHT).scale(0.66).set_color(GREEN)
        self.play(ShowCreation(text))

        self.wait(2)

        greedy = Text("6, 1, 1, 1").shift(DOWN*1.1+RIGHT*2.01).scale(1.55)

        self.play(TransformFromCopy(coins[-2], greedy[0]))
        self.wait(2)

        self.play(Transform(amount, Text("Amount = 3").next_to(coins, DOWN, buff=0.7)))

        self.wait(2)

        self.play(TransformFromCopy(coins[7], greedy[2]), FadeIn(greedy[1]))
        self.wait(1)
        self.play(Transform(amount, Text("Amount = 2").next_to(coins, DOWN, buff=0.7)))
        self.wait(1)
        self.play(TransformFromCopy(coins[7], greedy[4]), FadeIn(greedy[3]))
        self.wait()
        self.play(Transform(amount, Text("Amount = 1").next_to(coins, DOWN, buff=0.7)))
        self.wait()

        self.play(TransformFromCopy(coins[7], greedy[6]), FadeIn(greedy[5]))
        self.wait()
        self.play(Transform(amount, Text("Amount = 0").next_to(coins, DOWN, buff=0.7)))

        self.wait()

        rect = SurroundingRectangle(greedy, stroke_width=8).scale(1.32)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(TransformMatchingTex(greedy, Text("1, 4, 4").scale(1.55).move_to(greedy)), run_time=0.5)

        self.wait(2)




class CoinChangeTable(Scene):
    def construct(self):
        # Define parameters
        coins = [1, 4, 6]  # Available coin denominations
        amount = 9  # Target amount
        
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
        coin_table.shift(UP * 0.5)  # Adjust vertical position
        
        # Create table structure - position on right side
        table = VGroup()
        cells = {}
        cell_texts = {}
        
        # Calculate table width and height
        table_width = (amount + 1) * cell_width
        table_height = cell_height
        
        # Create cells - for coin changing, we need only one row per amount
        for j in range(amount + 1):
            cell = Rectangle(width=cell_width, height=cell_height)
            cell.set_stroke(WHITE, 1)
            
            # Position cells to the right of the coin details
            x_pos = j * cell_width
            y_pos = 0
            cell.move_to(np.array([x_pos, y_pos, 0]))
            
            # Add cell to table
            table.add(cell)
            cells[j] = cell
            
            # Add initial text (will be updated for DP calculation)
            if j == 0:
                text = Text("0", font_size=34)
            else:
                text = Text("∞", font_size=34)  # Start with infinity for DP
            text.move_to(cell.get_center())
            table.add(text)
            cell_texts[j] = text
        
        # Add column labels (amounts)
        for j in range(amount + 1):
            label = Text(f"${j}", font_size=23)
            label.next_to(cells[j], UP, buff=0.25)
            table.add(label)
        
        # Position table properly
        table.scale(1.1)  # Scale up for better visibility
        table.move_to(RIGHT * 2.5 + DOWN * 1)  # Move to right side
                
        # Create title
        title = Text(f"Coin Change Problem (Target = ${amount})", font_size=34)
        title.to_edge(UP, buff=0.5)
        
        coin_table.scale(1.4)
        coin_table.shift(DOWN * 0.94 + RIGHT * 0.3)
        
        # Animation sequence
        self.play(Write(title))
        coin_table.shift(UP*0.3+RIGHT*0.12)
        self.play(FadeIn(coin_table))
        table.shift(UP+LEFT*1.1).scale(1.06)
        self.play(ShowCreation(table))
        self.wait(2)




        
        # Initialize DP array
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0  # Base case
        
        # Text for explaining states
        explanation = Text("Step 1: Compute how to make $0 (base case = 0 coins)", font_size=24)
        explanation.to_edge(DOWN, buff=1)
        self.play(Write(explanation))
        self.wait(1)


        rect = SurroundingRectangle(coin_table[1], color=YELLOW, stroke_width=7).scale(1.22)

        i = 1
        
        # Fill the DP table
        for coin_index, coin in enumerate(coins):

            if i == 1:
                self.play(ShowCreation(rect)) 
            # Highlight current coin
            



            
            # Update explanation
            new_explanation = Text(f"Step {coin_index + 2}: Using coin ${coin}", font_size=34)
            new_explanation.to_edge(DOWN, buff=1)
            self.play(Transform(explanation, new_explanation))

            if i >= 2:
                self.play(Transform(rect, SurroundingRectangle(coin_table[i], color=YELLOW, stroke_width=7).scale(1.22)))
            i+=1

    
            
            # Update dp values
            for j in range(coin, amount + 1):
                # Highlight current cell
                current_cell = cells[j]
                self.play(current_cell.animate.set_fill(BLUE, opacity=0.39), run_time=1.2)
                
                # Highlight the cell we're comparing against
                prev_cell = cells[j - coin]
                self.play(prev_cell.animate.set_fill(GREEN, opacity=0.3), run_time=1.2)
                
                # Update current cell value
                dp[j] = min(dp[j], dp[j - coin] + 1)
                new_text = Text(str(dp[j]) if dp[j] != float('inf') else "∞", font_size=34)
                new_text.move_to(current_cell.get_center())
                
                # Add the new text directly to the scene
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
        final_explanation = Text(f"Minimum coins needed for ${amount}: {dp[amount]}", font_size=28)
        final_explanation.to_edge(DOWN, buff=1)
        self.play(Transform(explanation, final_explanation))
        
        # Show coin selection (backtracking)
        self.wait(2)
        self.play(Uncreate(rect), Uncreate(explanation))
                

        # Backtracking to find which coins were used
        remaining = amount
        used_coins = []
        
        backtrack_explanation = Text("Backtracking to find which coins were used:", font_size=24)
        backtrack_explanation.to_edge(DOWN, buff=1.5).shift(DOWN*0.6).scale(1.3)
        self.play(Write(backtrack_explanation))
        self.wait(2)
        self.play(Uncreate(backtrack_explanation))
        
        while remaining > 0:
            for coin in coins:
                if remaining >= coin and dp[remaining] == dp[remaining - coin] + 1:
                    used_coins.append(coin)
                    
                    # Highlight the coin being used
                    coin_index = coins.index(coin)
                    coin_rect = SurroundingRectangle(coin_table[coin_index + 1], color=GREEN, stroke_width=7).scale(1.1)
                    self.play(ShowCreation(coin_rect))
                    
                    # Update remaining amount
                    old_remaining = remaining
                    remaining -= coin
                    
                    # Highlight cells in backtracking
                    self.play(
                        cells[old_remaining].animate.set_fill(YELLOW, opacity=0.5),
                        run_time=1.2
                    )
                    self.play(
                        cells[remaining].animate.set_fill(GREEN, opacity=0.5),
                        run_time=1.2
                    )
                    
                    coin_used_text = Text(f"Used coin ${coin}, remaining: ${remaining}", font_size=24)
                    coin_used_text.to_edge(DOWN, buff=0.8)
                    self.play(Transform(explanation, coin_used_text))
                    
                    self.wait(1)
                    self.play(Uncreate(coin_rect))
                    
                    # Reset previous highlighted cell
                    self.play(
                        cells[old_remaining].animate.set_fill(opacity=0),
                        run_time=0.2
                    )
                    
                    break
        
        # Show the final set of coins used
        final_coins_text = Text(f"Coins used: {' + '.join(['$' + str(c) for c in used_coins])} = ${amount}", font_size=38)
        final_coins_text.to_edge(DOWN, buff=0.8)
        self.play(Transform(explanation, final_coins_text))
        
        self.wait(2)

        self.play(FadeOut(VGroup(coin_table, title, explanation)),
                  self.camera.frame.animate.shift(RIGHT*1.28+DOWN*1.3).scale(0.8))

        time = Text("Space:- O(Amount)").next_to(table, DOWN, buff=0.8)
        self.play(Write(time))
        self.wait(2)

        space = Text("Time:- O(Amount*Coins)").next_to(time, DOWN, buff=0.7)
        self.play(Write(space))
        self.wait(2)

        



