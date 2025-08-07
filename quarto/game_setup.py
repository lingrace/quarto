from typing import List, Optional, Literal
from bitarray import bitarray
from enum import Enum
from .constants import (
    EDGE_SIZE, NUM_PIECES, NUM_PROPERTIES, NUM_DIAGONALS,
    ALL_BITS_SET, NO_BITS_SET, PIECES_FOR_WIN, INSTRUCTIONS
)

# See technical design notes in README.md


class PieceFormatMode(Enum):
    BINARY = "binary"
    DECIMAL = "decimal"

class Player(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2

class LineData:
    def __init__(self) -> None:
        self.cumulative_bit_and: int = ALL_BITS_SET  # 1111
        self.cumulative_bit_or: int = NO_BITS_SET    # 0000
        self.number_of_pieces = 0
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"cumulative_bit_and={self.cumulative_bit_and:04b}, "
            f"cumulative_bit_or={self.cumulative_bit_or:04b}, "
            f"number_of_pieces={self.number_of_pieces})"
        )
        
    def add_piece(self, piece: int) -> None:
        self.cumulative_bit_and &= piece
        self.cumulative_bit_or |= piece
        self.number_of_pieces += 1

    def is_winning_line(self) -> bool:
        if self.number_of_pieces == PIECES_FOR_WIN:
            # If the cumulative bit and is not 0, then there is a bit position where all the pieces have a 1
            # If the cumulative bit or is not 15, then there is a bit position where all the pieces have a 0
            return self.cumulative_bit_and != NO_BITS_SET or self.cumulative_bit_or != ALL_BITS_SET
        return False

class GameState:
    def __init__(self, player_1_name: str, player_2_name: str, piece_format_mode:  PieceFormatMode) -> None:
        self.player_1_name: str = player_1_name
        self.player_2_name: str = player_2_name
        self.pieces: bitarray = bitarray(NUM_PIECES)
        # Note that keeping the board state is not necessary to check the win conditions. We retain the board purely for display purposes.
        self.board: List[List[Optional[int]]] = [[None for _ in range(EDGE_SIZE)] for _ in range(EDGE_SIZE)]  
        self.current_player: Player =  Player.PLAYER_1
        self.selected_piece: Optional[int] = None 
        self.columns_data: List[LineData] = [LineData() for _ in range(EDGE_SIZE)]
        self.rows_data: List[LineData] = [LineData() for _ in range(EDGE_SIZE)]
        self.diagonals_data: List[LineData] = [LineData() for _ in range(NUM_DIAGONALS)]
        self.winner: Optional[Player] = None # None if the game is not over, player_1 or player_2 if a player has won
        self.piece_format_mode = piece_format_mode
    
    def get_current_player_name(self) -> str:
        if self.current_player == Player.PLAYER_1:
            return self.player_1_name
        elif self.current_player == Player.PLAYER_2:
            return self.player_2_name
        else:
            raise ValueError("Additional players unsupported.")

    def is_game_over(self) -> bool:
        return self.winner is not None or self.pieces.count(1) == NUM_PIECES
    
    def is_stalemate(self) -> bool:
        return self.is_game_over() and self.winner is None

    def place_piece(self, row: int, col: int) -> None:
        if self.selected_piece is None:
            raise ValueError("No piece selected")
        
        self.board[row][col] = self.selected_piece
        self.pieces[self.selected_piece] = 1
        self.columns_data[col].add_piece(self.selected_piece)
        self.rows_data[row].add_piece(self.selected_piece)
        
        # Add to diagonals if applicable
        if row == col:
            self.diagonals_data[0].add_piece(self.selected_piece)
        if row + col == EDGE_SIZE - 1:
            self.diagonals_data[1].add_piece(self.selected_piece)
            
        # Check for win
        if (
            self.columns_data[col].is_winning_line()
            or self.rows_data[row].is_winning_line()
            or self.diagonals_data[0].is_winning_line()
            or self.diagonals_data[1].is_winning_line()
        ):
            self.winner = self.current_player
    
    def select_piece(self, piece_index: int) -> None:
        self.selected_piece = piece_index
        self.pieces[piece_index] = 1
    
    def switch_player(self) -> None:
        if self.current_player == Player.PLAYER_1:
            self.current_player = Player.PLAYER_2
        elif self.current_player == Player.PLAYER_2:
            self.current_player = Player.PLAYER_1
    
    def print_board(self) -> None:
        print("Current board:")
        for row in self.board:
            # Convert each cell to string and pad with spaces for alignment
            formatted_row = []
            for cell in row:
                cell_str = self.format_piece(cell) if cell is not None else "."
                formatted_row.append(f"{cell_str:>6}")  # Right-align with 6 character width
            print(" ".join(formatted_row))
    
    # for debug usage
    def print_line_data(self) -> None:
        for i, line_data in enumerate(self.columns_data):
            print(f"Column {i}: {line_data}")
        for i, line_data in enumerate(self.rows_data):
            print(f"Row {i}: {line_data}")
        for i, line_data in enumerate(self.diagonals_data):
            print(f"Diagonal {i}: {line_data}")

    def format_piece(self, piece_index: int) -> str:
        format_str: str
        if self.piece_format_mode == PieceFormatMode.BINARY:
            format_str = f'0{NUM_PROPERTIES}b' 
        elif self.piece_format_mode == PieceFormatMode.DECIMAL:
            format_str = 'd'
        else:
            raise ValueError ("Format mode is unsupported.")
        
        return format(piece_index, format_str)
    
    def print_available_pieces(self) -> None:
        print("Available pieces:", ", ".join(self.format_piece(i) for i in range(NUM_PIECES) if self.pieces[i] == 0))

class GameEngine:
    def __init__(self) -> None:
        self.game_started = False

    def _validate_piece_input(self, selected_piece: str) -> int:
        piece_index: int
        try:
            if self.game_state.piece_format_mode == PieceFormatMode.DECIMAL:
                piece_index = int(selected_piece)
            elif self.game_state.piece_format_mode == PieceFormatMode.BINARY:
                self._validate_binary_format(selected_piece)
                piece_index = int(selected_piece, 2)
            else:
                raise ValueError("Given format mode is unsupported.")
        except ValueError:
            raise ValueError("Selected piece was an invalid format.")
        
        if piece_index < 0 or piece_index >= NUM_PIECES:
            raise ValueError(
                f"Piece {self.game_state.format_piece(piece_index)} is out of range "
                f"(0-{NUM_PIECES-1})"
            )
        
        if self.game_state.pieces[piece_index] == 1:
            raise ValueError(f"Piece {self.game_state.format_piece(piece_index)} has already been used")
        
        return piece_index
    
    def _validate_piece_placement(self, row_input: str, col_input: str) -> tuple[int, int]: # returns row, col
        try:
            row = int(row_input)
            col = int(col_input)
        except ValueError:
            raise ValueError("Invalid input. Please enter a valid integer") 

        if row < 0 or row >= EDGE_SIZE or col < 0 or col >= EDGE_SIZE:
            raise ValueError(f"Invalid row or column: {row}, {col}")
        if self.game_state.board[row][col] is not None:
            raise ValueError(f"Position ({row}, {col}) is already occupied")
        
        return (row, col)
    
    def _validate_binary_format(self, piece_input: str) -> None:
        if not all(bit in '01' for bit in piece_input):
            raise ValueError(
                "Invalid binary format. Please enter a binary number (e.g., 0000, 0001)"
            )

    def _validate_piece_format_mode(self, mode_input: str) -> PieceFormatMode:
        mode = mode_input.lower().strip()
        if mode == "binary":
            return PieceFormatMode.BINARY
        elif mode == "decimal":
            return PieceFormatMode.DECIMAL
        else:
            raise ValueError(f"Invalid piece format mode '{mode_input}'. Please enter 'binary' or 'decimal'.")

    def print_game_instructions(self) -> None:
       print(INSTRUCTIONS)

    def _select_piece(self) -> None:
        while True:
            try:
                self.game_state.print_available_pieces()
                piece_input = input(f"[{self.game_state.get_current_player_name()}] Select a piece: ")
                
                validated_piece_input = self._validate_piece_input(piece_input)
                
                self.game_state.select_piece(validated_piece_input)
                break
            except ValueError as e:
                print(e)

    def _place_piece(self) -> None:
        while True:
            try:
                self.game_state.print_board()
                row_input = input(f"[{self.game_state.get_current_player_name()}] Place piece in row (0-{EDGE_SIZE-1}): ")
                col_input = input(f"[{self.game_state.get_current_player_name()}] Place piece in column (0-{EDGE_SIZE-1}): ")
                
                row, col = self._validate_piece_placement(row_input, col_input)
                break
            except ValueError as e:
                print(e)

        self.game_state.place_piece(row, col)
        self.game_state.print_board()

    def _init_game_state(self, player_1_name: str, player_2_name: str) -> None:
        while True:
            piece_format_mode_input = input("Enter the format of the pieces (binary or decimal): ").lower().strip()
            try:
                piece_format_mode = self._validate_piece_format_mode(piece_format_mode_input)
                break
            except ValueError as e:
                print(e)
            
        if not self.game_started:
            self.game_started = True
            self.game_state = GameState(player_1_name, player_2_name, piece_format_mode)
    
    def run_game(self,  player_1_name: str, player_2_name: str) -> None:
        self._init_game_state(player_1_name, player_2_name)
        # This game loop follows the lifecycle of a piece, not a player
        while not self.game_state.is_game_over():
            self._select_piece()
            self.game_state.switch_player()
            self._place_piece()
            if self.game_state.winner is not None:
                self.game_state.print_board()
                print(f"Game over! {self.game_state.get_current_player_name()} wins!")
                return
        self.game_state.print_board()
        print("Game over! It's a tie!")
