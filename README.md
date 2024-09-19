# Chess Engine

Welcome to the Chess Engine project! This repository contains the code for a fully functional chess game with an AI opponent. The project is structured to allow easy modification and extension.

## Features

- **Human vs AI**: Challenge an AI opponent.
- **Undo Moves**: Step back to correct mistakes or try different strategies.
- **Visual Representation**: Uses images of chess pieces for a realistic game experience.

![Screenshot 2024-09-19 150919](https://github.com/user-attachments/assets/c0bae431-4b9f-4827-bc05-486b51889424)

### As the game goes on, the move list gets updated!
![Screenshot 2024-09-19 151013](https://github.com/user-attachments/assets/a855a3cc-f447-4a9d-9abe-7ebfdcc957ac)


## Installation

To run this project, you'll need to install the required packages. Follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Aditya7s/Chess-AI.git
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
# Usage
To start the game, run the ChessMain.py script. This script is the main driver for the game, handling user input and updating the game state and visuals.
```bash
python ChessMain.py
```
# Project Structure
- ```ChessMain.py```: The main script to run the game. It initializes the game, handles user input, and updates the display. It loads images from the ```images/``` directory and integrates the game logic from ```ChessEngine.py``` and AI functionality from ```SmartMoveFinder.py```.
- ```ChessEngine.py```: Contains the core logic for the game, including the board representation, move generation, and game rules.
- ```SmartMoveFinder.py```: Implements the AI logic for finding the best move.
- ```images/```: Contains images of chess pieces used in the game interface.
# How to Play
Use the mouse to select and move pieces.
The game will indicate valid moves for the selected piece.
To undo a move, press the letter Z on your keyboard.
You can restart the game at any time with R on your keyboard.
