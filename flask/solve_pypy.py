import sys
import os

# Add the parent directory to sys.path so Python can find solver
current_directory = os.getcwd()
# Print the current working directory
print("Current working directory:", current_directory)
  # Adds parent directory

print("Sys.path:", sys.path)

import solver.algo
import solver.position

if __name__ == "__main__":
    positions_1 = (sys.argv[1])
    positions_2 = (sys.argv[2])
    num_moves = int(sys.argv[3])
    loop_iters = int(sys.argv[4])
    search_depth = int(sys.argv[5])

    pos = solver.position.Position()
    pos.current_positions = [int(positions_1), int(positions_2)]
    print("HELLLOOO", pos.current_positions)
    pos.num_moves = num_moves
    
    
    move = solver.algo.solve(pos, loop_iters=loop_iters, search_depth=search_depth)
    print(move)  # This output is captured in subprocess
    
