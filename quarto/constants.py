"""Constants for the Quarto game."""

# Board and game configuration
EDGE_SIZE = 4
NUM_PIECES = EDGE_SIZE ** 2
NUM_PROPERTIES = EDGE_SIZE
NUM_DIAGONALS = 2

# Bitwise constants for win detection
ALL_BITS_SET = (1 << NUM_PROPERTIES) - 1  # 1111, or 15 in decimal
NO_BITS_SET = 0  # 0000

# Win condition constants
PIECES_FOR_WIN = EDGE_SIZE  # 4 pieces in a line to win

INSTRUCTIONS = """
Welcome to Quarto!

Quarto is a 2 player game where each player takes turns placing a piece on the board.
There are 16 pieces, each with a unique combination of 4 properties: height, color, shape, and number of holes.
For each of these properties, there are 2 options, e.g., tall or short.

The board is a square 4 by 4 grid. At the start of the game, the board is empty.
Each piece can be used once and each square can be occupied once.
The game is won by creating a line of 4 pieces that share a common property,
e.g., all the pieces in that line are tall.

The order of play is as follows:
1. Player 1 selects a piece
2. Player 2 places that piece on the board
3. Player 2 selects a piece
4. Player 1 places that piece on the board

The game continues until a player wins or the board is full.

Pieces can be displayed in binary (e.g., 0000, 0001, 0010) or decimal (e.g., 0, 1, 2) format.
You will be asked to choose your preferred format when setting up the game.

To set up this game, enter the names of the players.
"""