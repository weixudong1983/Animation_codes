from manimlib import *

class PascalsTriangle(Scene):
    def construct(self):
        # Configuration
        num_rows = 6
        triangle_scale = 0.7
        animation_speed = 0.5
        cell_size = 0.6
        
        # Colors
        background_color = "#111111"
        triangle_color = WHITE
        highlight_color = "#FF5555"
        connection_color = "#5555FF"
        
        # Set background color
        self.camera.background_color = background_color

        self.camera.frame.shift(DOWN*2)
        
        # Title
        title = Text("Pascal's Triangle", font_size=48)
        title.to_edge(UP, buff=0.5).shift(DOWN*2)
        self.play(Write(title))
        
        # Create empty Pascal's triangle
        triangle = []
        positions = []
        
        # Calculate positions for each cell in the triangle
        for i in range(num_rows):
            row = []
            row_positions = []
            for j in range(i + 1):
                # Calculate the position of each cell
                x = (j - i/2) * cell_size * 2
                y = -i * cell_size * 1.8
                row_positions.append(np.array([x, y, 0]))
            positions.append(row_positions)
        
        # Generate the triangle values
        triangle_values = [[1]]
        for i in range(1, num_rows):
            row = [1]
            for j in range(1, i):
                row.append(triangle_values[i-1][j-1] + triangle_values[i-1][j])
            row.append(1)
            triangle_values.append(row)
        
        # Create the visual representation of Pascal's triangle
        for i in range(num_rows):
            row = []
            for j in range(i + 1):
                value = triangle_values[i][j]
                cell = Integer(value)
                cell.scale(triangle_scale)
                cell.move_to(positions[i][j])
                row.append(cell)
            triangle.append(row)
        
        # Animation of building the triangle row by row
        self.play(FadeIn(triangle[0][0]))
        
        
        for i in range(1, num_rows):
            # Add first element of the row (always 1)
            self.play(FadeIn(triangle[i][0]), run_time=animation_speed)
            
            # Add middle elements with highlighting the relationship
            for j in range(1, i):
                # Highlight the two parent elements
                parent1 = triangle[i-1][j-1].copy().set_color(highlight_color)
                parent2 = triangle[i-1][j].copy().set_color(highlight_color)
                
                # Create arrows connecting parents to child
                arrow1 = Arrow(
                    positions[i-1][j-1] + 0.3*DOWN, 
                    positions[i][j] + 0.3*UP,
                    buff=0.1,
                    color=connection_color
                )
                arrow2 = Arrow(
                    positions[i-1][j] + 0.3*DOWN, 
                    positions[i][j] + 0.3*UP,
                    buff=0.1,
                    color=connection_color
                )
                
                # Show the calculation
                value1 = triangle_values[i-1][j-1]
                value2 = triangle_values[i-1][j]
                result = value1 + value2
                

                # Animation sequence
                self.play(
                    Transform(triangle[i-1][j-1], parent1),
                    Transform(triangle[i-1][j], parent2),
                    run_time=animation_speed
                )
                self.play(
                    ShowCreation(arrow1),
                    ShowCreation(arrow2),
                    run_time=animation_speed
                )
                self.play(FadeIn(triangle[i][j]), run_time=animation_speed)
                
                # Restore original colors
                self.play(
                    triangle[i-1][j-1].animate.set_color(triangle_color),
                    triangle[i-1][j].animate.set_color(triangle_color),
                    FadeOut(arrow1),
                    FadeOut(arrow2),
                    run_time=animation_speed
                )
            
            # Add last element of the row (always 1)
            if i > 0:
                self.play(FadeIn(triangle[i][i]), run_time=animation_speed)
        
        # Final touch - highlight the entire triangle
        all_cells = VGroup(*[cell for row in triangle for cell in row])
        self.play(
            all_cells.animate.set_color(YELLOW),
            run_time=1
        )
        self.play(
            all_cells.animate.set_color(WHITE),
            run_time=1
        )
        
        # Hold the final scene
        self.wait(4)


