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

# Piece format modes
PIECE_FORMAT_MODES = ("binary", "decimal") 