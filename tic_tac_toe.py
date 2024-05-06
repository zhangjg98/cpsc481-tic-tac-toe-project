import tkinter as tk
from tkinter import messagebox
import threading

class Player:
    """Player Class for Tic Tac Toe Game"""

    def __init__(self, name: str, symbol: str, difficulty=None) -> None:
        self.name = name
        self.symbol = symbol
        self.difficulty = difficulty

class TicTacToeBoard:
    """Tic Tac Toe Board Class for GUI"""

    def __init__(self, root, board_size: int, win_condition: int, game_instance, game_board) -> None:
        self.root = root
        self.game_instance = game_instance
        self.game_board = game_board
        self.board_initialized = False
        self.initialize_board()

    def initialize_board(self):
        if self.board_initialized:
            return # Skip initialization if the board has already been initialized
        self.board_size = self.game_instance.board_size
        self.win_condition = self.game_instance.win_condition
        """Initializes the game board"""
        if self.board_size is None:
            raise ValueError("Board size is not set.")
        self.board_buttons = []
        for row in range(self.board_size):
            row_buttons = []
            for col in range(self.board_size):
                button = tk.Button(self.root, text="", width=5, height=2, command=lambda r=row, c=col: self.handle_button_click(r, c))
                button.grid(row=row + 3, column=col, padx=5, pady=5)
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)
        self.board_initialized = True
    
    def update_gui_board(self, player1, player2):
        """Updates the GUI board with the player symbols"""
        if self.board_size is None or self.game_board is None:
            return  # Return if board size or board is not initialized

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.game_board[row][col] == player1.symbol:
                    self.board_buttons[row][col].config(text="X", state='disabled', disabledforeground='blue')
                elif self.game_board[row][col] == player2.symbol:
                    self.board_buttons[row][col].config(text="O", state='disabled', disabledforeground='red')
                else:
                    self.board_buttons[row][col].config(text="", state='normal')
    
    def handle_button_click(self, row, col):
        """Handles button click event"""
        if self.game_instance.get_move(row, col):
            threading.Thread(target=lambda: self.update_gui_board(self.game_instance.player1, self.game_instance.player2, row, col)).start()
            
class Game:
    """Game Class for Tic Tac Toe Game"""

    def __init__(self, root, settings_window, player1: Player, tic_tac_toe_board : TicTacToeBoard) -> None:
        self.root = root
        self.settings_window = settings_window
        self.player1 = player1
        self.player2 = None
        self.player_var = tk.StringVar(value="ai")
        self.difficulty_var = tk.StringVar(value="hard")
        self.board_size = None
        self.win_condition = None
        self.board = None
        self.winner = None
        self.tic_tac_toe_board = tic_tac_toe_board
        self.current_player = 1

    def initialize_game_board(self):
        """Initialize the game board after receiving input"""
        self.board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Set player2 based on selected player type
        player_type = self.player2.name
        if player_type == "AI":
            self.player2 = Player("AI", "O", self.difficulty_var.get())
        else:
            self.player2 = Player("Player 2", "O") # Default human player 2

        # Start the game
        self.play_game()

    def play_game(self) -> None:
        """Tic Tac Toe game with AI or another player"""
        self.show_game_board()  # Update the GUI board at the beginning of the game

    def show_game_board(self):
        """Displays the Tic Tac Toe board window"""
        if self.board_size is not None and self.win_condition is not None:
            board_root = tk.Tk()
            board_root.title("Tic Tac Toe Board")
            self.tic_tac_toe_board = TicTacToeBoard(board_root, self.board_size, self.win_condition, self, self.board)
            self.tic_tac_toe_board.board_size = self.board_size
            self.tic_tac_toe_board.win_condition = self.win_condition
            board_root.mainloop()
        else:
            messagebox.showerror("Error", "Please set the board size and win condition first.")

    def update_board(self, row: int, col: int, current_player: Player) -> None:
        """Updates the game board with the player's move"""
        self.board[row][col] = current_player.symbol
        self.tic_tac_toe_board.game_board = self.board
        self.tic_tac_toe_board.update_gui_board(self.player1, self.player2)

    def get_empty_spaces(self) -> list:
        """Returns a list of coordinates for all empty spaces on the board"""
        empty_spaces = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == " ":
                    empty_spaces.append((row, col))
        return empty_spaces

    def is_win(self, player_symbol: str, win_condition: int) -> bool:
        """Checks if the specified player has won the game"""

        # Check rows
        for row in self.board:
            if self.check_consecutive(row, player_symbol, win_condition):
                return True

        # Check columns
        for i in range(len(self.board)):
            column = [self.board[j][i] for j in range(len(self.board))]
            if self.check_consecutive(column, player_symbol, win_condition):
                return True

        # Check diagonals
        diagonal1 = [self.board[i][i] for i in range(len(self.board))]
        diagonal2 = [self.board[i][len(self.board) - 1 - i] for i in range(len(self.board))]
        if self.check_consecutive(diagonal1, player_symbol, win_condition) or self.check_consecutive(diagonal2, player_symbol, win_condition):
            return True

        return False

    def check_consecutive(self, line: list, player_symbol: str, win_condition: int) -> bool:
        """Checks if there are consecutive symbols of a player in a line"""
        count = 0
        for symbol in line:
            if symbol == player_symbol:
                count += 1
                if count == win_condition:
                    return True
            else:
                count = 0
        return False

    def get_move(self, row, col):
        """Handles the player's move"""
        if self.current_player == 1:
            current_player = self.player1
        else:
            current_player = self.player2

        self.update_board(row, col, current_player)
        if self.evaluate(current_player.symbol):
            messagebox.showinfo("Winner", f"Congratulations! {current_player.name} wins!")
        else:
            if self.current_player == 1:
                self.current_player = 2
                if self.player2.name == "AI":
                    self.ai_turn()
                    self.current_player = 1
            else:
                self.current_player = 1
                    
    def get_best_move(self, player_symbol: str, opponent_symbol: str, win_condition: int, max_depth: int) -> tuple:
        """Uses the minimax algorithm with alpha-beta pruning to determine the best move for the AI player"""
        empty_spaces = self.get_empty_spaces()
        best_score = -float("inf")
        best_move = None
        alpha = -float("inf")
        beta = float("inf")

        for row, column in empty_spaces:
            self.board[row][column] = player_symbol
            score = self.minimax(self.board, 0, alpha, beta, False, win_condition, player_symbol, opponent_symbol, max_depth)
            self.board[row][column] = " "

            if score > best_score:
                best_score = score
                best_move = (row, column)

        return best_move

    def minimax(self, board: list, depth: int, alpha: int, beta: int, is_maximizing: bool, win_condition: int, player_symbol: str, opponent_symbol: str, max_depth: int):
        """Minimax algorithm with alpha-beta pruning for AI player"""
        # Base case: check if the game is over or the depth limit has been reached

        if depth == max_depth or self.evaluate(player_symbol) or self.evaluate(opponent_symbol):
            return self.evaluate(player_symbol) - self.evaluate(opponent_symbol)
        
        empty_spaces = [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == " "]
        if not empty_spaces:
            return 0

        # Recursive case: evaluate all possible moves and choose the best one
        if is_maximizing:
            best_score = -float("inf")
            for i, j in empty_spaces:
                board[i][j] = player_symbol
                score = self.minimax(board, depth + 1, alpha, beta, False, win_condition, player_symbol, opponent_symbol, max_depth)
                board[i][j] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break  # Beta cut-off
            return best_score
        else:
            best_score = float("inf")
            for i, j in empty_spaces:
                board[i][j] = opponent_symbol
                score = self.minimax(board, depth + 1, alpha, beta, True, win_condition, player_symbol, opponent_symbol, max_depth)
                board[i][j] = " "
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break  # Alpha cut-off
            return best_score

    def ai_thread(self) -> None:
        """Thread for AI commands"""
        player_symbol = self.player2.symbol
        opponent_symbol = self.player1.symbol
        win_condition = self.win_condition
        max_depth = 3

        best_move = self.get_best_move(player_symbol, opponent_symbol, win_condition, max_depth)
        if best_move is not None:
            row, col = best_move
            self.update_board(row, col, self.player2)

            if self.evaluate(player_symbol):
                messagebox.showinfo("Loser", "Sorry, you lose!")
        else:
            print("AI couldn't find a move.")

        if not self.get_empty_spaces() and not self.evaluate(player_symbol) and not self.evaluate(opponent_symbol):
            messagebox.showinfo("Tie", "It's a tie!")
            
    def ai_turn(self):
        """Handles the AI player's turn"""
        threading.Thread(target=self.ai_thread).start()

    def evaluate(self, player_symbol: str) -> int:
        """Evaluates the current state of the board"""
        if self.is_win(player_symbol, self.win_condition):
            return 1
        else:
            return 0

# End of Game Class

def initialize_settings_window(root):
    """Creates the settings window for selecting player type, difficulty, board size, and win condition"""
    settings_window = tk.Toplevel(root)
    settings_window.title("Tic Tac Toe Settings")

    player_var = tk.StringVar(value="ai")
    tk.Label(settings_window, text="Choose player type:").grid(row=0, column=0, padx=10, pady=5)
    tk.Radiobutton(settings_window, text="AI", variable=player_var, value="ai").grid(row=0, column=1, padx=10, pady=5)
    tk.Radiobutton(settings_window, text="Human", variable=player_var, value="human").grid(row=0, column=2, padx=10, pady=5)

    difficulty_var = tk.StringVar(value="hard")
    tk.Label(settings_window, text="Choose difficulty level:").grid(row=1, column=0, padx=10, pady=5)
    tk.Radiobutton(settings_window, text="Easy", variable=difficulty_var, value="easy").grid(row=1, column=1, padx=10, pady=5)
    tk.Radiobutton(settings_window, text="Hard", variable=difficulty_var, value="hard").grid(row=1, column=2, padx=10, pady=5)

    board_size_label = tk.Label(settings_window, text="Enter the size of the board (3-5):")
    board_size_label.grid(row=2, column=0, padx=10, pady=5)
    board_size_entry = tk.Entry(settings_window)
    board_size_entry.grid(row=2, column=1, padx=10, pady=5)

    win_condition_label = tk.Label(settings_window, text="Enter the desired number of consecutive symbols for your win condition (should not exceed board size):")
    win_condition_label.grid(row=3, column=0, padx=10, pady=5)
    win_condition_entry = tk.Entry(settings_window)
    win_condition_entry.grid(row=3, column=1, padx=10, pady=5)

    start_button = tk.Button(settings_window, text="Start Game", command=lambda: start_game(settings_window, board_size_entry, win_condition_entry, player_var, difficulty_var))
    start_button.grid(row=4, column=1, padx=10, pady=10)

def start_game(settings_window, board_size_entry, win_condition_entry, player_var, difficulty_var):
    """Starts the Tic Tac Toe game with the selected settings"""

    board_size_text = board_size_entry.get()
    win_condition_text = win_condition_entry.get()

    if not board_size_text.isdigit() or not win_condition_text.isdigit():
        messagebox.showerror("Error", "Please enter valid integers for board size and win condition.")
        return
    
    board_size = int(board_size_text)
    win_condition = int(win_condition_text)

    if board_size < 3 or board_size > 5:
        messagebox.showerror("Error", "Board size must be between 3 and 5.")
        return

    if win_condition < 3 or win_condition > board_size:
        messagebox.showerror("Error", "Win condition must be between 3 and the board size.")
        return

    player_type = player_var.get()
    difficulty = difficulty_var.get()
    player1 = Player("Player 1", "X")  # Default human player

    tic_tac_toe_game = Game(settings_window, settings_window, player1, None)

    if player_type == "ai":
        tic_tac_toe_game.player2 = Player("AI", "O", difficulty)
    else:
        tic_tac_toe_game.player2 = Player("Player 2", "O")

    tic_tac_toe_game.board_size = board_size
    tic_tac_toe_game.win_condition = win_condition

    tic_tac_toe_board = TicTacToeBoard(settings_window, board_size, win_condition, tic_tac_toe_game, None)  # Initialize with a temporary root

    tic_tac_toe_board.game_instance = tic_tac_toe_game
    tic_tac_toe_game.tic_tac_toe_board = tic_tac_toe_board

    settings_window.withdraw()  # Hide the settings window
    tic_tac_toe_game.initialize_game_board()

def main():
    root = tk.Tk()
    root.withdraw()                     
    # Initialize the Game object
    threading.Thread(target=initialize_settings_window, args=(root,)).start()

    # Start the main event loop to display the initial player settings window
    root.mainloop()
        
if __name__ == "__main__":
    main()
