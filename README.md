
# Connect 4 Player

This project implements a Connect 4 game with a Flask backend and a bot opponent powered by AI. The application allows players to interact with the game board, make moves, and play against an AI bot. The bot's moves are calculated using a custom AI algorithm that evaluates board states and selects optimal moves based on game progress.

Key Features:

Connect 4 Game Logic: The game is modeled as a class extending a Position class to handle game state, player turns, move validation, and win condition checks.
Bot AI: The bot selects its moves using a subprocess that runs a Python script (solve_pypy.py) via PyPy, utilizing a search algorithm that adjusts depth and iterations based on the number of moves made in the game.
Flask API: A RESTful API is provided to manage game operations such as fetching the board state, making player and bot moves, and resetting the game.
Dynamic Gameplay: The application supports both player vs player and player vs bot modes, where the bot calculates its next move based on an intelligent search of the current board state.
Backend Communication: The frontend communicates with the Flask backend via HTTP requests, ensuring a smooth game experience.
Technologies:

Flask: Used for the web framework to handle HTTP routes and manage the game's logic.
Python: Core programming language used for backend development and AI implementation.
PyPy: Utilized for its speed in running the AI script (solve_pypy.py) to calculate the bot's optimal moves.
JavaScript & HTML: For the frontend to visualize the game and display the current board.



## Deployment

Deployed link: https://connect4-service-768895558000.northamerica-northeast1.run.app/

