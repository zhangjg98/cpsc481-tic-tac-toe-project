import random
import argparse


class Player:
    """Player Class for Tic Tac Toe Game"""

    def __init__(self, name: str, symbol: str, difficulty=None) -> None:
        self.name = name
        self.symbol = symbol
        self.difficulty = difficulty


class Game:
    """Game Class for Tic Tac Toe Game"""

    def __init__(self, player1: Player, player2: Player, board_size: int, consecutive_symbols: int) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board_size = board_size
        self.consecutive_symbols = consecutive_symbols
        self.board = [[" " for _ in range(board_size)] for _ in range(board_size)]
        self.winner = None

    @staticmethod
    def get_board_size_from_player() -> int:
        """Prompts the player to input the desired board size"""
        while True:
            try:
                board_size = int(input("Enter the size of the board (e.g., 3 for 3x3): "))
                if board_size < 3:
                    print("Board size must be at least 3.")
                elif board_size > 8:
                    print("Board size should not exceed 8.")
                else:
                    return board_size
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def get_win_condition_from_player() -> int:
        """Prompts the player to input the desired win condition"""
        while True:
            try:
                consecutive_symbols = int(input("Enter the desired number of consecutive symbols you would like as your win condition (e.g., 3 for 3 in a row): "))
                if consecutive_symbols < 3:
                    print("Win condition must be at least 3.")
                elif consecutive_symbols > board_size:
                    print("Win condition cannot exceed the board size.")
                elif consecutive_symbols > 8:
                    print("Win condition should not exceed 8.")
                else:
                    return consecutive_symbols
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def print_board(self) -> None:
        """Prints the game board"""
        for row in self.board:
            print("|".join(row))

    def update_board(self, row: int, col: int, current_player: Player) -> None:
        """Updates the game board with the player's move"""
        self.board[row][col] = current_player.symbol

    def get_empty_spaces(self) -> list:
        """Returns a list of coordinates for all empty spaces on the board"""
        empty_spaces = [
            (row, col)
            for row in range(self.board_size)
            for col in range(self.board_size)
            if self.board[row][col] == " "
        ]

        return empty_spaces

    def is_win(self, player_symbol: str, consecutive_symbols: int) -> bool:
        """Checks if the specified player has won the game"""

        # Check rows
        for row in self.board:
            if self.check_consecutive(row, player_symbol, consecutive_symbols):
                return True

        # Check columns
        for i in range(len(self.board)):
            column = [self.board[j][i] for j in range(len(self.board))]
            if self.check_consecutive(column, player_symbol, consecutive_symbols):
                return True

        # Check diagonals
        for i in range(len(self.board) - consecutive_symbols + 1):
            for j in range(len(self.board) - consecutive_symbols + 1):
                diagonal1 = [self.board[i + k][j + k] for k in range(consecutive_symbols)]
                diagonal2 = [self.board[i + k][j + consecutive_symbols - 1 - k] for k in range(consecutive_symbols)]
                if self.check_consecutive(diagonal1, player_symbol, consecutive_symbols) or self.check_consecutive(diagonal2, player_symbol, consecutive_symbols):
                    return True

        return False

    def check_consecutive(self, line: list, player_symbol: str, consecutive_symbols: int) -> bool:
        """Checks if there are consecutive symbols of a player in a line"""
        count = 0
        for symbol in line:
            if symbol == player_symbol:
                count += 1
                if count == consecutive_symbols:
                    return True
            else:
                count = 0
        return False

    def get_move(self):
        """Gets the player's move and validates it"""
        while True:
            player_row = input(f"Enter row number (1-{self.board_size}): ")

            if not player_row.isdigit() or int(player_row) not in range(1, self.board_size + 1):
                print("Invalid row number, please try again.")
                continue
            else:
                player_row = int(player_row) - 1
                break

        while True:
            player_col = input(f"Enter column number (1-{self.board_size}): ")

            if not player_col.isdigit() or int(player_col) not in range(1, self.board_size + 1):
                print("Invalid column number, please try again.")
                continue
            else:
                player_col = int(player_col) - 1
                break

        return player_row, player_col

    def is_valid_move(self, row: int, col: int) -> bool:
        """Checks if the player's move is valid"""
        if self.board[row][col] != " ":
            return False

        return True

    def get_best_move(self, difficulty: str, player_symbol: str, opponent_symbol: str, consecutive_symbols: int) -> tuple:
        """Uses the minimax algorithm to determine the best move for the AI player"""
        empty_spaces = self.get_empty_spaces()
        best_score = -float("inf")
        best_move = None

        for row, column in empty_spaces:
            self.board[row][column] = player_symbol
            score = self.minimax(self.board, 0, False, consecutive_symbols, player_symbol, opponent_symbol)
            self.board[row][column] = " "

            if score > best_score:
                best_score = score
                best_move = (row, column)

        return best_move

    def minimax(self, board: list, depth: int, is_maximizing: bool, consecutive_symbols: int, player_symbol: str, opponent_symbol: str):
        """Minimax algorithm for AI player"""
        # Base case: check if the game is over and return the score
        if self.is_win(player_symbol, consecutive_symbols):
            return 1
        elif self.is_win(opponent_symbol, consecutive_symbols):
            return -1
        empty_spaces = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == " "]
        if not empty_spaces:
            return 0

        # Recursive case: evaluate all possible moves and choose the best one
        if is_maximizing:
            best_score = -float("inf")
            for i, j in empty_spaces:
                board[i][j] = player_symbol
                score = self.minimax(board, depth + 1, False, consecutive_symbols, player_symbol, opponent_symbol)
                board[i][j] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i, j in empty_spaces:
                board[i][j] = opponent_symbol
                score = self.minimax(board, depth + 1, True, consecutive_symbols, player_symbol, opponent_symbol)
                board[i][j] = " "
                best_score = min(score, best_score)
            return best_score

    def play_game(self) -> None:
        """Tic Tac Toe game with AI or another player"""
        print("Welcome to Tic Tac Toe!")
        self.print_board()

        while True:
            # Player 1's turn
            self.player_turn(self.player1)

            # Player 2's turn
            if self.player2.name == "ai":
                self.ai_turn()
            else:
                self.player_turn(self.player2)

    def ai_turn(self) -> None:
        # Self.player2 is the AI player
        player_symbol = self.player2.symbol
        opponent_symbol = self.player1.symbol
        consecutive_symbols = 3  # Assuming 3 in a row as default
        difficulty = self.player2.difficulty
        print("AI is thinking...")
        ai_row, ai_col = self.get_best_move(difficulty, player_symbol, opponent_symbol, consecutive_symbols)
        self.update_board(ai_row, ai_col, self.player2)
        self.print_board()

        if self.is_win(player_symbol, consecutive_symbols):
            print("Sorry, you lose!")
            exit()

        if not self.get_empty_spaces():
            print("It's a tie!")
            exit()

    def evaluate(self, player_symbol: str, opponent_symbol: str, consecutive_symbols: int) -> int:
        """Evaluates the current state of the board from the perspective of the AI player"""
        if self.is_win(player_symbol, consecutive_symbols):
            return 1
        elif self.is_win(opponent_symbol, consecutive_symbols):
            return -1
        else:
            return 0

    def player_turn(self, player: Player):
        while True:
            player_row, player_col = self.get_move()

            if not self.is_valid_move(player_row, player_col):
                print("Space is already taken, please try again.")
                self.print_board()

            else:
                self.update_board(player_row, player_col, player)
                self.print_board()

                if self.is_win(player.symbol, self.consecutive_symbols):
                    print(f"{player.name} Wins!")
                    exit()

                if not self.get_empty_spaces():
                    print("It's a tie!")
                    exit()

                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Tic Tac Toe", description="Tic Tac Toe game with AI or another player."
    )

    parser.add_argument(
        "-p",
        "--player",
        choices=["ai", "human"],
        default="ai",
        help="Play against the AI or another player.",
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        choices=["easy", "hard"],
        default="hard",
        help="Difficulty level of the AI player.",
    )

    args = parser.parse_args()

    player1 = Player("Player 1", "X")
    player2 = Player(args.player, "O", args.difficulty)
    board_size = Game.get_board_size_from_player()
    consecutive_symbols = Game.get_win_condition_from_player()
    tic_tac_toe = Game(player1, player2, board_size, consecutive_symbols)
    tic_tac_toe.play_game()
