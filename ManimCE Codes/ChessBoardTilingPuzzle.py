from manim import *
import numpy as np

config.background_color = "#173340"


class ChessBoard(MovingCameraScene):
    def construct(self):
        rows, cols = 8, 8
        square_size = 1
        scale_factor = 0.688888

        board = VGroup()
        colors = [WHITE, MAROON_B]

        for row in range(rows):
            for col in range(cols):
                color = colors[(row + col) % 2]
                square = Square(
                    side_length=square_size, fill_color=color, fill_opacity=1
                )
                square.move_to(
                    np.array([col * square_size, row * square_size, 0])
                    - np.array(
                        [
                            cols / 2 * square_size - square_size / 2,
                            rows / 2 * square_size - square_size / 2,
                            0,
                        ]
                    )
                )
                square.set_stroke(color=BLACK, width=1)
                board.add(square)

        board.scale(scale_factor).move_to(ORIGIN)
        self.play(Create(board))
        self.wait(2)


        # Add brace and label on the left side
        left_brace = Brace(board, RIGHT)
        left_label = left_brace.get_text("8")

        # Add brace and label on the bottom side
        bottom_brace = Brace(board, DOWN)
        bottom_label = bottom_brace.get_text("8")

        # Display the braces and labels
        self.play(Create(left_brace), Write(left_label), Create(bottom_brace), Write(bottom_label))

        self.wait(2)

        self.play(FadeOut(left_label, left_brace, bottom_label, bottom_brace))
        self.wait(2)



        # Keep track of tiled cells
        tiled_cells = set()
        # Collect all the dominoes
        dominoes = VGroup()

        # Function to tile two neighboring cells with animation
        def tile_cells(row1, col1, row2, col2, animate=True):
            # Check if the cells are adjacent horizontally or vertically
            if (
                    (abs(row1 - row2) == 0 and abs(col1 - col2) == 1)
                    or (abs(row1 - row2) == 1 and abs(col1 - col2) == 0)
            ):
                # Calculate indices in the board VGroup
                index1 = row1 * cols + col1
                index2 = row2 * cols + col2

                # Get the squares
                square1 = board[index1]
                square2 = board[index2]

                # Determine orientation and create the domino tile
                if row1 == row2:
                    # Horizontal domino
                    domino = Rectangle(
                        width=2 * square_size * scale_factor,
                        height=square_size * scale_factor,
                        fill_color=GREEN,
                        stroke_width=0.23,
                        stroke_color=BLACK ,
                        fill_opacity=1,
                        # Remove stroke for seamless lookmove stroke for seamless look
                    )
                else:
                    # Vertical domino
                    domino = Rectangle(
                        width=square_size * scale_factor,
                        height=2 * square_size * scale_factor,
                        fill_color=GREEN,
                        stroke_width=0.23,
                        fill_opacity=1,

                        stroke_color=BLACK  # Remove stroke for seamless look# Remove stroke for seamless look
                    )

                # Randomly choose to start from left or right
                side = np.random.choice(['left', 'right'])
                if side == 'left':
                    off_screen_x = board.get_left()[0] - 1
                else:
                    off_screen_x = board.get_right()[0] + 1

                # Start position off-screen
                domino.move_to(np.array([off_screen_x, square1.get_center()[1], 0]))

                # Target position at the midpoint between the two squares
                pos1 = square1.get_center()
                pos2 = square2.get_center()
                target_position = (pos1 + pos2) / 2

                # Animate the domino moving to the target position
                if animate:
                    self.play(domino.animate.move_to(target_position), run_time=1)
                else:
                    # For simultaneous animations, we'll handle animations later
                    domino.move_to(target_position)

                # Update the set of tiled cells
                tiled_cells.update({(row1, col1), (row2, col2)})

                # Add the domino to the group
                dominoes.add(domino)

                return domino
            else:
                print("Cells are not adjacent horizontally or vertically.")

        # Function to create dominoes without immediate animation
        def create_domino(row1, col1, row2, col2):
            # Similar to tile_cells but without immediate animation
            index1 = row1 * cols + col1
            index2 = row2 * cols + col2

            square1 = board[index1]
            square2 = board[index2]

            if row1 == row2:
                # Horizontal domino
                domino = Rectangle(
                    width=2 * square_size * scale_factor,
                    height=square_size * scale_factor,
                    fill_color=GREEN,
                    fill_opacity=1,
                    stroke_width=0.23,
                    stroke_color=BLACK  # Remove stroke for seamless look
                )
            else:
                # Vertical domino
                domino = Rectangle(
                    width=square_size * scale_factor,
                    height=2 * square_size * scale_factor,
                    fill_color=GREEN,
                    fill_opacity=1,
                    stroke_width=0.23,
                    stroke_color=BLACK  # Remove stroke for seamless look
                )

            # Randomly choose to start from left or right
            side = np.random.choice(['left', 'right'])
            if side == 'left':
                off_screen_x = board.get_left()[0] - 1
            else:
                off_screen_x = board.get_right()[0] + 1

            # Start position off-screen at the same y as the squares
            domino.move_to(np.array([off_screen_x, square1.get_center()[1], 0]))

            # Target position at the midpoint between the two squares
            pos1 = square1.get_center()
            pos2 = square2.get_center()
            target_position = (pos1 + pos2) / 2

            # Prepare the animation but don't play it yet
            animations.append(domino.animate.move_to(target_position))

            # Update the set of tiled cells
            tiled_cells.update({(row1, col1), (row2, col2)})

            # Add the domino to the group
            dominoes.add(domino)

            return domino

        # Place initial tiles with animation
        a = tile_cells(1, 2, 2, 2)
        self.wait(2)
        b = tile_cells(2, 4, 2, 3)
        self.wait(2)
        c = tile_cells(3, 6, 4, 6)
        self.wait(2)

        # Now tile all the remaining cells, preparing animations
        remaining_dominoes = VGroup()
        animations = []

        # Go through all cells and tile untiled adjacent pairs
        for row in range(rows):
            for col in range(cols):
                # If cell is already tiled, skip
                if (row, col) in tiled_cells:
                    continue

                # Try to tile with the right neighbor
                if col < cols - 1 and (row, col + 1) not in tiled_cells:
                    # Tile (row, col) and (row, col + 1)
                    domino = create_domino(row, col, row, col + 1)
                    remaining_dominoes.add(domino)
                # Else, try to tile with the bottom neighbor
                elif row < rows - 1 and (row + 1, col) not in tiled_cells:
                    # Tile (row, col) and (row + 1, col)
                    domino = create_domino(row, col, row + 1, col)
                    remaining_dominoes.add(domino)

        # Animate all remaining dominoes moving to their positions simultaneously
        self.play(AnimationGroup(*animations, lag_ratio=0), run_time=2)
        self.wait(2)

        # Fade out all dominoes including a, b, c
        self.play(FadeOut(dominoes))
        self.wait(2)

        self.play(FadeOut(board[0], board[-1]
                          ))

        self.wait(2)

        # Mark the squares as removed by setting their fill opacity to 0
        board[0].set_fill(opacity=0)
        board[-1].set_fill(opacity=0)

        # Start filling tiles one by one after removing the corners
        # Reset tiled_cells and dominoes
        tiled_cells = set()
        dominoes = VGroup()
        removed_cells = {(0, 0), (rows - 1, cols - 1)}  # Keep track of removed cells

        # Function to tile two neighboring cells with animation
        def tile_cells(row1, col1, row2, col2, run_time=0.7):
            if (
                    (abs(row1 - row2) == 0 and abs(col1 - col2) == 1)
                    or (abs(row1 - row2) == 1 and abs(col1 - col2) == 0)
            ):
                index1 = row1 * cols + col1
                index2 = row2 * cols + col2

                square1 = board[index1]
                square2 = board[index2]

                if row1 == row2:
                    # Horizontal domino
                    domino = Rectangle(
                        width=2 * square_size * scale_factor,
                        height=square_size * scale_factor,
                        fill_color=GREEN,
                        fill_opacity=1,
                        stroke_width=0.23,
                        stroke_color=BLACK  # Remove stroke for seamless look
                    )
                else:
                    # Vertical domino
                    domino = Rectangle(
                        width=square_size * scale_factor,
                        height=2 * square_size * scale_factor,
                        fill_color=GREEN,
                        fill_opacity=1,
                        stroke_width=0.23,
                        stroke_color=BLACK  # Remove stroke for seamless look
                    )

                # Start position off-screen to the left
                off_screen_x = board.get_left()[0] - 1
                domino.move_to(np.array([off_screen_x, square1.get_center()[1], 0]))

                # Target position at the midpoint between the two squares
                pos1 = square1.get_center()
                pos2 = square2.get_center()
                target_position = (pos1 + pos2) / 2

                # Animate the domino moving to the target position
                self.play(domino.animate.move_to(target_position), run_time=run_time)

                # Update the set of tiled cells
                tiled_cells.update({(row1, col1), (row2, col2)})

                # Add the domino to the group
                dominoes.add(domino)

                return domino
            else:
                print("Cells are not adjacent horizontally or vertically.")

        # Go through all cells and tile untiled adjacent pairs one by one
        for row in range(rows):
            for col in range(cols):
                # If cell is removed, skip
                if (row, col) in removed_cells:
                    continue
                # If cell is already tiled, skip
                if (row, col) in tiled_cells:
                    continue

                # Try to tile with the right neighbor
                if (
                        col < cols - 1
                        and (row, col + 1) not in tiled_cells
                        and (row, col + 1) not in removed_cells
                ):
                    domino = tile_cells(
                        row, col, row, col + 1, run_time=0.7  # Faster animation
                    )
                # Else, try to tile with the bottom neighbor
                elif (
                        row < rows - 1
                        and (row + 1, col) not in tiled_cells
                        and (row + 1, col) not in removed_cells
                ):
                    domino = tile_cells(
                        row, col, row + 1, col, run_time=0.7  # Faster animation
                    )

        self.wait(2)

        # Highlight that it's not possible to tile the entire board
        # Find remaining untiled cells
        remaining_cells = []
        for row in range(rows):
            for col in range(cols):
                if (
                        (row, col) not in tiled_cells
                        and (row, col) not in removed_cells
                ):
                    index = row * cols + col
                    remaining_cells.append(board[index])
