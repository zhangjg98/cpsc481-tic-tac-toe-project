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

## References and Credits

The original implementation of the Tic-Tac-Toe game that this program built upon is from [this repository](https://github.com/mariahrucker/Tic-Tac-Toe). Their implementation of Tic Tac Toe is licensed under the MIT License. See the LICENSE file for more information. This implementation of Tic-Tac-Toe was created by Jason Zhang.