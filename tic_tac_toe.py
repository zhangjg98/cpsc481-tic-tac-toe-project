import tkinter as tk
from tkinter import messagebox
import random
import threading

class Player:
    """Player Class for Tic Tac Toe Game"""

    def __init__(self, name: str, symbol: str, difficulty=None) -> None:
        self.name = name
        self.symbol = symbol
        self.difficulty = difficulty

class PlayerStatistics:
    """Class to track player statistics for the current session."""

    def __init__(self):
        self.statistics = {}

    def record_win(self, player_name):
        """Record a win for the player."""
        if player_name in self.statistics:   # Check if the player has already played a game
            self.statistics[player_name]["wins"] += 1   # Increment wins by 1
        else:
            self.statistics[player_name] = {"wins": 1, "losses": 0, "draws": 0}   # Create a new record of this player and increment their wins by 1

    def record_loss(self, player_name):
        """Record a loss for the player."""
        if player_name in self.statistics:   # Check if the player has already played a game
            self.statistics[player_name]["losses"] += 1   # Increment losses by 1
        else:
            self.statistics[player_name] = {"wins": 0, "losses": 1, "draws": 0}   # Create a new record of this player and increment their losses by 1

    def record_draw(self, player_name):
        """Record a draw for the player."""
        if player_name in self.statistics:   # Check if the player has already played a game
            self.statistics[player_name]["draws"] += 1   # Increment draws by 1
        else:
            self.statistics[player_name] = {"wins": 0, "losses": 0, "draws": 1}   # Create a new record of this player and increment their draws by 1

    def get_player_stats(self, player_name):
        """Get the statistics for the specified player."""
        return self.statistics.get(player_name, {"wins": 0, "losses": 0, "draws": 0})
    
class TicTacToeBoard:
    """Tic Tac Toe Board Class for GUI"""

    def __init__(self, root, board_size: int, win_condition: int, game_instance, game_board) -> None:
        self.root = root
        self.game_instance = game_instance
        self.game_board = game_board
        self.initialize_board()

    def initialize_board(self):
        """Initializes the game board"""
        self.board_size = self.game_instance.board_size
        self.win_condition = self.game_instance.win_condition

        if self.board_size is None:
            raise ValueError("Board size is not set.")
        self.board_buttons = []
        for row in range(self.board_size):
            row_buttons = []
            for col in range(self.board_size):
                button = tk.Button(self.root, text="", command=lambda r=row, c=col: self.handle_button_click(r, c))
                button.grid(row=row + 3, column=col, padx=5, pady=5, sticky="nsew")
                row_buttons.append(button)
            self.board_buttons.append(row_buttons)
        
        for i in range(self.board_size):
            self.root.grid_rowconfigure(i + 3, weight=1)
            self.root.grid_columnconfigure(i, weight=1)
    
    def update_gui_board(self, player1, player2):
        """Updates the GUI board with the player symbols"""
        if self.board_size is None or self.game_board is None:
            return  # Return if board size or board is not initialized
        
        font_size = -int(100 / self.board_size)

        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.board_buttons[row][col]
                if self.game_board[row][col] == player1.symbol:
                    button.config(text="X", font=("Arial", font_size), state='disabled', fg='blue')
                elif self.game_board[row][col] == player2.symbol:
                    button.config(text="O", font=("Arial", font_size), state='disabled', fg='red')
                    button.config(disabledforeground='red')
                else:
                    self.board_buttons[row][col].config(text="", font=("Arial", font_size), state='normal')
    
    def handle_button_click(self, row, col):
        """Handles button click event"""
        if self.game_instance.get_move(row, col):
            self.update_gui_board(self.game_instance.player1, self.game_instance.player2, row, col)

    def destroy_board_window(self):
        """Destroys the TicTacToeBoard window"""
        self.root.destroy()
            
class Game:
    """Game Class for Tic Tac Toe Game"""

    def __init__(self, root, settings_window, player1: Player, tic_tac_toe_board : TicTacToeBoard, board_size: int = None) -> None:
        self.root = root
        self.settings_window = settings_window
        self.player1 = player1
        self.player2 = None
        self.player_var = tk.StringVar(value="ai")
        self.difficulty_var = tk.StringVar(value="hard")
        self.board_size = board_size
        self.win_condition = None
        self.board = None
        self.tic_tac_toe_board = tic_tac_toe_board
        self.current_player = 1
        
    def initialize_game_board(self):
        """Initialize the game board after receiving input"""
        self.board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Set player2 based on selected player type
        player_type = self.player2.name
        if player_type == "AI":
            self.player2 = Player("AI", "O", self.player2.difficulty) # Sets to AI with inputted difficulty
        else:
            self.player2 = Player("Player 2", "O") # Default human player 2

        # Start the game
        self.show_game_board()

        
    def show_game_board(self):
            """Updates the GUI board at the beginning of the game"""
            self.board_window = tk.Toplevel(self.root)
            self.board_window.title("Tic Tac Toe Board")
            self.tic_tac_toe_board = TicTacToeBoard(self.board_window, self.board_size, self.win_condition, self, self.board)
            self.tic_tac_toe_board.board_size = self.board_size
            self.tic_tac_toe_board.win_condition = self.win_condition
            self.board_window.deiconify()
            self.settings_window.withdraw()

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

        # Check rows and columns
        for i in range(self.board_size):
            for j in range(self.board_size - win_condition + 1):
                # Check rows
                if all(self.board[i][j + k] == player_symbol for k in range(win_condition)):
                    return True
                # Check columns
                if all(self.board[j + k][i] == player_symbol for k in range(win_condition)):
                    return True

        # Check diagonals
        for i in range(self.board_size - win_condition + 1):
            for j in range(self.board_size - win_condition + 1):
                # Check diagonal from top-left to bottom-right
                if all(self.board[i + k][j + k] == player_symbol for k in range(win_condition)):
                    return True
                # Check diagonal from top-right to bottom-left
                if all(self.board[i + k][self.board_size - 1 - j - k] == player_symbol for k in range(win_condition)):
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

        # Makes sure the current player is correct
        if self.current_player == 1:
            current_player = self.player1
        else:
            current_player = self.player2

        self.update_board(row, col, current_player)

        # Checks if the game is over. If not, switches the current_player to the next player
        if self.evaluate(current_player.symbol):
            # Check if a win has been achieved
            self.game_over_dialog(current_player)

        elif len(self.get_empty_spaces()) == 0:
            # Check if a draw has occured
            self.game_over_dialog(None)
        
        else:
            # Checks if Player 2 is a human or AI if the game is not over.
            if self.current_player == 1:
                self.current_player = 2
                if self.player2.name == "AI":
                    self.ai_turn()
                    self.current_player = 1
            else:
                self.current_player = 1      # Executes when Player 2 is human so that Player 1 is now the current player
                    
    def get_best_move(self, player_symbol: str, opponent_symbol: str, win_condition: int, max_depth: int) -> tuple:
        """Uses the minimax algorithm with alpha-beta pruning to determine the best move for the AI player"""
        empty_spaces = self.get_empty_spaces()

        # Check if the AI difficulty is easy
        if self.player2.difficulty == "easy":
            # Add randomness to the decision-making process so that AI will be more prone to mistakes
            return random.choice(empty_spaces) if empty_spaces else None    
        
        elif self.player2.difficulty == "hard":
            # Proceed with setting up the minimax algorithm using alpha-beta pruning for the AI
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
        
        elif self.player2.difficulty == "very_hard":
            # Proceed with setting up the minimax algorithm using alpha-beta pruning and a move ordering heuristic for the AI
            best_score = -float("inf")
            best_move = None
            alpha = -float("inf")
            beta = float("inf")

            # Generate a list of moves sorted by a heuristic function
            ordered_moves = self.order_moves(empty_spaces, player_symbol, opponent_symbol)

            for row, column in ordered_moves:
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
        
    def order_moves(self, empty_spaces: list, player_symbol: str, opponent_symbol: str) -> list:
        """Orders the available moves based on a heuristic function (only for Very Hard difficulty)"""
        ordered_moves = []

        # Group moves by their impact on the game
        winning_moves = []
        blocking_moves = []

        for row, col in empty_spaces:
            self.board[row][col] = player_symbol
            if self.is_win(player_symbol, self.win_condition):
                winning_moves.append((row, col))
            self.board[row][col] = " "

            self.board[row][col] = opponent_symbol
            if self.is_win(opponent_symbol, self.win_condition):
                blocking_moves.append((row, col))
            self.board[row][col] = " "

        # Add winning moves first, then blocking moves, then other moves
        ordered_moves.extend(winning_moves)
        ordered_moves.extend(blocking_moves)
        ordered_moves.extend([move for move in empty_spaces if move not in winning_moves and move not in blocking_moves])

        return ordered_moves

    def ai_thread(self) -> None:
        """Thread for AI commands"""
        player_symbol = self.player2.symbol
        opponent_symbol = self.player1.symbol
        win_condition = self.win_condition

        # Disable all buttons so player cannot press them during AI's turn
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.tic_tac_toe_board.board_buttons[row][col].config(state='disabled')

        # Set a maximum depth based on board size (important for gameplay reasons to ensure an AI does not take too long for bigger boards)
        if self.board_size >= 6:
            max_depth = 2
        else:
            max_depth = 3

        best_move = self.get_best_move(player_symbol, opponent_symbol, win_condition, max_depth)
        if best_move is not None:
            row, col = best_move
            self.update_board(row, col, self.player2)

            if self.evaluate(player_symbol):
                self.game_over_dialog(self.player2)

        if not self.get_empty_spaces() and not self.evaluate(player_symbol) and not self.evaluate(opponent_symbol):
            self.game_over_dialog(None)
        
        # Re-enable all buttons after AI has made its move
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.tic_tac_toe_board.board_buttons[row][col].config(state='normal')
            
    def ai_turn(self):
        """Handles the AI player's turn"""
        threading.Thread(target=self.ai_thread).start()

    def evaluate(self, player_symbol: str) -> int:
        """Evaluates the current state of the board"""
        if self.is_win(player_symbol, self.win_condition):
            return 1
        else:
            return 0
                
    def game_over_dialog(self, winner):
        """Displays a message box when the game is over, which allows for the player to choose their next action."""
        
        # Separate message box to declare a winner/loser or draw result
        if winner:
            if winner.name == "AI":
                messagebox.showinfo("Loser", "Sorry, you lose!")
            else:
                messagebox.showinfo("Winner", f"Congratulations! {winner.name} wins!")
        else:
            messagebox.showinfo("Draw", "It's a draw!")

        # Record player statistics
        if winner:
            player_stats.record_win(winner.name)
            player_stats.record_loss(self.player1.name if winner.name == self.player2.name else self.player2.name)
        else:
            player_stats.record_draw("Player 1")

            # If statement determining whether the Player 2 was an AI or human
            if self.player2.name == "AI":
                player_stats.record_draw("AI")
            else:
                player_stats.record_draw("Player 2")
    
        # New message box that asks the player if they want to play again with the same settings
        choice = messagebox.askquestion("Game Over", "Do you want to play again with the same settings?", icon='question')
        if choice == 'yes':
            self.restart_game()
        else:
            self.tic_tac_toe_board.destroy_board_window() # Destroy the game board window
            self.settings_window.deiconify()  # Show the settings window

    def restart_game(self):
        """Restarts the game with the same settings."""
        # Clear the game board
        self.board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        # Reset current player
        self.current_player = 1
        # Update GUI board
        self.tic_tac_toe_board.update_gui_board(self.player1, self.player2)
        # Destroy the existing game board window
        self.tic_tac_toe_board.destroy_board_window()
        # Show the new game board window
        self.show_game_board()

# End of Game Class

def create_radio_button(parent, text, var, value):
    """Create a radio button with the given text, variable, and value."""
    return tk.Radiobutton(parent, text=text, variable=var, value=value)

def create_label(parent, text):
    """Create a label with the given text."""
    return tk.Label(parent, text=text)

def initialize_settings_window(root):
    """Creates the settings window for selecting player type, difficulty, board size, and win condition"""
    settings_window = tk.Toplevel(root)
    settings_window.title("Tic Tac Toe Settings")

    player_var = tk.StringVar(value="ai")
    create_label(settings_window, "Choose player type:").grid(row=0, column=0, padx=10, pady=5)
    create_radio_button(settings_window, "AI", player_var, "ai").grid(row=0, column=1, padx=10, pady=5)
    create_radio_button(settings_window, "Human", player_var, "human").grid(row=0, column=2, padx=10, pady=5)

    difficulty_var = tk.StringVar(value="hard")
    create_label(settings_window, "Choose difficulty level:").grid(row=1, column=0, padx=10, pady=5)
    create_radio_button(settings_window, "Easy", difficulty_var, "easy").grid(row=1, column=1, padx=10, pady=5)
    create_radio_button(settings_window, "Hard", difficulty_var, "hard").grid(row=1, column=2, padx=10, pady=5)
    create_radio_button(settings_window, "Very Hard", difficulty_var, "very_hard").grid(row=1, column=3, padx=10, pady=5)

    create_label(settings_window, "Enter the size of the board (3-8):").grid(row=2, column=0, padx=10, pady=5)
    board_size_entry = tk.Entry(settings_window)
    board_size_entry.grid(row=2, column=1, padx=10, pady=5)

    create_label(settings_window, "Enter the desired number of consecutive symbols for your win condition (should not exceed board size):").grid(row=3, column=0, padx=10, pady=5)
    win_condition_entry = tk.Entry(settings_window)
    win_condition_entry.grid(row=3, column=1, padx=10, pady=5)

    start_button = tk.Button(settings_window, text="Start Game", command=lambda: start_game(settings_window, board_size_entry, win_condition_entry, player_var, difficulty_var))
    start_button.grid(row=4, column=1, padx=10, pady=10)

    view_stats_button = tk.Button(settings_window, text="View Statistics", command=lambda: view_statistics(settings_window))
    view_stats_button.grid(row=5, column=1, padx=10, pady=10)

    return settings_window

def view_statistics(parent_window):
    """Displays a new window to show player statistics"""

    # Check if the player statistics window is already open
    if hasattr(parent_window, 'stats_window') and parent_window.stats_window:
        try:
            parent_window.stats_window.lift()
        except tk.TclError:
            # If the window no longer exists, recreate it
            del parent_window.stats_window
            view_statistics(parent_window)
        return

    stats_window = tk.Toplevel(parent_window)
    stats_window.title("Player Statistics")

    # Store the reference to the statistics window in the parent_window
    parent_window.stats_window = stats_window

    # Retrieve player statistics
    player1_stats = player_stats.get_player_stats("Player 1")
    player2_stats = player_stats.get_player_stats("Player 2")
    ai_stats = player_stats.get_player_stats("AI")

    # Populate statistics window with player statistics
    create_label(stats_window, text="Player 1 Statistics").grid(row=0, column=0, padx=10, pady=5)
    create_label(stats_window, text=f"Wins: {player1_stats['wins']}").grid(row=1, column=0, padx=10, pady=5)
    create_label(stats_window, text=f"Losses: {player1_stats['losses']}").grid(row=2, column=0, padx=10, pady=5)
    create_label(stats_window, text=f"Draws: {player1_stats['draws']}").grid(row=3, column=0, padx=10, pady=5)

    create_label(stats_window, text="Player 2 Statistics").grid(row=0, column=1, padx=10, pady=5)
    create_label(stats_window, text=f"Wins: {player2_stats['wins']}").grid(row=1, column=1, padx=10, pady=5)
    create_label(stats_window, text=f"Losses: {player2_stats['losses']}").grid(row=2, column=1, padx=10, pady=5)
    create_label(stats_window, text=f"Draws: {player2_stats['draws']}").grid(row=3, column=1, padx=10, pady=5)

    create_label(stats_window, text="AI Player Statistics").grid(row=0, column=2, padx=10, pady=5)
    create_label(stats_window, text=f"Wins: {ai_stats['wins']}").grid(row=1, column=2, padx=10, pady=5)
    create_label(stats_window, text=f"Losses: {ai_stats['losses']}").grid(row=2, column=2, padx=10, pady=5)
    create_label(stats_window, text=f"Draws: {ai_stats['draws']}").grid(row=3, column=2, padx=10, pady=5)

    def on_close():
        # Clear the reference to the statistics window in the parent_window
        parent_window.stats_window = None
        stats_window.destroy()

    # Button to close the statistics window
    close_button = tk.Button(stats_window, text="Close", command=on_close)
    close_button.grid(row=4, column=1, padx=10, pady=10)

def start_game(settings_window, board_size_entry, win_condition_entry, player_var, difficulty_var):
    """Starts the Tic Tac Toe game with the selected settings"""

    board_size_text = board_size_entry.get()
    win_condition_text = win_condition_entry.get()

    if not board_size_text.isdigit() or not win_condition_text.isdigit():
        messagebox.showerror("Error", "Please enter valid integers for board size and win condition.")
        return
    
    board_size = int(board_size_text)
    win_condition = int(win_condition_text)

    if board_size < 3 or board_size > 8:
        messagebox.showerror("Error", "Board size must be between 3 and 8.")
        return

    if win_condition < 3 or win_condition > board_size:
        messagebox.showerror("Error", "Win condition must be between 3 and the board size.")
        return

    # Close the statistics window if it's open
    if hasattr(settings_window, 'stats_window') and settings_window.stats_window:
        settings_window.stats_window.destroy()

    player_type = player_var.get()
    difficulty = difficulty_var.get()
    player1 = Player("Player 1", "X")  # Default human player

    tic_tac_toe_game = Game(settings_window, settings_window, player1, None, board_size)

    if player_type == "ai":
        tic_tac_toe_game.player2 = Player("AI", "O", difficulty)
    else:
        tic_tac_toe_game.player2 = Player("Player 2", "O")

    tic_tac_toe_game.board_size = board_size
    tic_tac_toe_game.win_condition = win_condition

    # Check if the Tic-Tac-Toe board is already initialized (for cases when a player might want to play again but would change settings)
    if not hasattr(tic_tac_toe_game, 'tic_tac_toe_board'):
        tic_tac_toe_board = TicTacToeBoard(settings_window, board_size, win_condition, tic_tac_toe_game, None)  # Initialize with a temporary root
        tic_tac_toe_board.game_instance = tic_tac_toe_game
        tic_tac_toe_game.tic_tac_toe_board = tic_tac_toe_board

    settings_window.withdraw()  # Hide the settings window
    settings_window.update()
    
    tic_tac_toe_game.initialize_game_board()

def main():
    root = tk.Tk()
    root.withdraw()                     
    # Initialize the Game object
    settings_window = initialize_settings_window(root)

    # Start the main event loop to display the initial player settings window
    root.mainloop()

player_stats = PlayerStatistics()                       # Global variable to track player statistics

if __name__ == "__main__":
    main()
