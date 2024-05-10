# Highly Customizable Tic-Tac-Toe

In this Python GUI implementation of the classic game Tic-Tac-Toe, you can choose between playing against another human opponent or an AI opponent. There are various difficulties that you can choose from for an AI opponent. You can also choose customizable board sizes and win conditions. By allowing players to choose their own rules, the program provides a more intriguing player experience for those who can find the normal version of Tic-Tac-Toe to be stale. However, if you do enjoy the normal game of Tic-Tac-Toe, you can also play in that format.

## How to Run

The program can be started with the command line using a Python command with the file name.

* To start the game

```python
$ python tic_tac_toe.py
```

## Functions

When the program is started, the player is greeted by a window that provides several options to choose from. The player can choose to play against an AI or human opponent, choose the difficulty of the AI opponent (Easy, Hard, and Very Hard), choose a board size (up to 8x8), and choose a win condition (must be between 3 and the board size that the player chooses). Once all inputs have been confirmed, the player will be able to start the game. 

In the startup window, the player can also view statistics that track wins, losses, and draws for Player 1, Player 2, and the AI. These are tracked for each session and reset once the program has been closed.

## Board Representation

The game board is represented on a Python GUI built using the Python tkinter library. The board will be of the board size that the player sets in the startup window. "X" represents Player 1's move, "O" represents the AI's or Player 2's move.

## AI opponent

The AI opponent on Easy difficulty will pick moves at random. They are by far the easiest opponent to beat.

The AI opponent on Hard difficulty uses the minimax algorithm with alpha beta pruning to calculate the best move. Typically, the minimax algorithm recursively explores all possible moves to a certain depth, and then returns the score for each move. The alpha beta pruning algorithm improves the minimax algorithm by pruning any moves when the algorithm has already found at least one possibility that is worse than a previously examined move.

The AI opponent on Very Hard difficulty uses the same algorithm as the Hard AI opponent but also prioritizes moves that would be considered game-winning or prevent a loss. This improves the performance of the algorithm even further, making it harder for the human player to defeat them.

## Classes

In the code, there are four classes.
- 'Player' class sets the name, symbol (X or O), and AI difficulty (if one chooses to play against an AI opponent).
- 'PlayerStatistics' is the class that contains functions that help with tracking statistics for the current session.
- 'TicTacToeBoard' is the class that contains functions that initialize, update, and close the game board in the Tkinter GUI interface. It also handles button clicks on the board.
- 'Game' is the class that handles much of the game logic, including the handling of player moves, identifying wins/losses/draws, and the incorporation of the AI algorithm.

## Functions

This section will detail the relevant functions for the classes that were listed in the previous section as well as any functions that did not fall under a class.

**PlayerStatistics:**
- record_win - records a win for the respective player.
- record_loss - records a loss for the respective player.
- record_draw - records a draw for the respective player.
- get_player_stats - gets the statistics for the specified player.

**TicTacToeBoard:**
- initialize_board - initializes the GUI game board based on win condition and board size inputs.
- update_gui_board - updates the GUI game board with the player symbols once a move has been made.
- handle_button_click - handles the button click event.
- destroy_board_window - destroys the Tic-Tac-Toe board window when it is no longer needed.

**Game:**
- initialize_game_board - initializes the game board layout for other functions in the Game class to use
- show_game_board - generates the GUI board at the beginning of the game so the game can start
- update_board - updates the game board layout and calls the update_gui_board function to update the GUI board
- get_empty_spaces - retrieves all of the empty spaces left on the board
- is_win - checks if the specified player has won the game
- check_consecutive - checks for a sufficient number of consecutive symbols
- get_move - handles the player moves and turn switching
- get_best_move - handles the AI difficulty input and calls the minimax function to determine the best move for the AI
- minimax - the minimax algorithm with alpha-beta pruning which helps the decision making for the AI.
- order_moves - a heuristic function to help sort out optimal moves for the 'Very Hard' difficulty AI.
- ai_thread - thread for AI commands.
- ai_turn - handles the AI's turn.
- evaluate - evaluates the current state of the board.
- game_over_dialog - displays a message box when the game is over and prompts the player to make a decision on whether they'd like to play again with the same settings.
- restart_game - restarts the game with the same settings already inputted.

**Other Functions (for the GUI settings window):**
- create_radio_button - creates a radio button with the given text, variable, and value.
- create_label - creates a label with the given text.
- initialize_settings_window - Creates the settings window for selecting player type, difficulty, board size, and win condition.
- view_statistics - displays a new GUI window to show player statistics.
- on_close - function within the view_statistics function that clear the references to the statistics window in the parent_window.
- start_game - starts the game with the selected settings that the player confirmed and handles invalid inputs.
- main - calls the settings_window function and starts a main loop to display the initial settings window.

## References and Credits

The original implementation of the Tic-Tac-Toe game that this program built upon is from [this repository](https://github.com/mariahrucker/Tic-Tac-Toe). Their implementation of Tic Tac Toe is licensed under the MIT License. See the LICENSE file for more information. This implementation of Tic-Tac-Toe was created by Jason Zhang.