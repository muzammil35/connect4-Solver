from flask import Flask, jsonify, request
from solver.position import Position
import subprocess
import os

app = Flask(__name__)

class Connect4(Position):
    def __init__(self):
        super().__init__()
        
    
    def reset(self):
        self.current_player = 0
        self.num_moves = 0
        self.current_positions = [0,0]
        self.last_move = -1
    
    def drop_token(self, col):
        if self.can_play(col):
            self.play(col)
            return True
        else:
            return False
    
    def get_board(self):
        return self.board_state()

    def check_winner(self):
        for position in self.current_positions:
            if self.connected_four(position):
                return True
        return False
    
    def get_bot_move(self):
        if self.num_moves == 0:
            return 3  # Play middle row as first move
    
        loop_iters = 2 if self.num_moves <= 15 else 4
        search_depth = 13 if self.num_moves <= 11 else 16

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "solve_pypy.py"))
        print("script path", script_path)
    
        # Run the solve function using PyPy
        print(self.current_positions)
        result = subprocess.run(
            ["pypy3", script_path, str(self.current_positions[0]),str(self.current_positions[1]), str(self.num_moves), str(loop_iters), str(search_depth)],
            capture_output=True,
            text=True
        )

        stdout = result.stdout.strip()
        lines = stdout.split("\n")
        last_line = lines[-1].strip()
        values = last_line.strip('()').split(', ')
        move = int(values[1])


        return move



# Initialize game
game = Connect4()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify(game.get_board())

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    col = data.get('col')
    if game.drop_token(col):
        winner = game.check_winner()
        return jsonify({
            'board': game.get_board(),
            'winner': winner
        })
    return jsonify({'error': 'Invalid move'}), 400

@app.route('/bot_play', methods=['POST'])
def bot_play():
    col = game.get_bot_move()  # Implement bot logic to choose a move
    if game.drop_token(col):
        winner = game.check_winner()
        return jsonify({
            'board': game.get_board(),
            'winner': winner
        })
    return jsonify({'error': 'Invalid move'}), 400


@app.route('/reset', methods=['POST'])
def reset():
    game.reset()
    return jsonify({'board': game.get_board()})

    
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Get the port from environment, default to 5000
    app.run(host="0.0.0.0", port=port)  # Bind to 0.0.0.0 for external access
