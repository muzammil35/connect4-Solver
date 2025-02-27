#from position_fallback import Position
from solver.Transposition import TranspositionTable

from solver.position import Position


def get_tt_entry(value, col, UB=False, LB=False):
    return {'value': value, 'col':col, 'UB': UB, 'LB': LB}


def get_win_score(position):
    return(((position.board_width * position.board_height + 1) - position.num_moves) // 2)

def tie_game(position):
    if position.num_moves == position.board_height * position.board_width:
        return True
    return False


def Negamax(position, alpha, beta, transposition_table, max_depth=None):

    if max_depth==0:
        return 0,0
    
    max_score = (((position.board_width * position.board_height) - 1) - position.num_moves) // 2
    key = position.get_key()
    cached_entry = transposition_table.get(key)
    if cached_entry is not None:
        if cached_entry['LB']:
            alpha = max(alpha, cached_entry['value'])
            if alpha >= beta:
                return cached_entry['value'], cached_entry['col']
        else:
            #if beta > max_score:
                #beta = max_score
                #if alpha >= beta:
                    #return beta, position.last_move
            return cached_entry['value'], cached_entry['col']

    if tie_game(position):
        return 0, position.last_move
    
    if position.connected_four(position.current_positions[1 if position.get_current_player()==0 else 0]):
        #print(f"case 1 {-1*get_win_score(position)}")
        return -1*get_win_score(position), position.last_move
    
    
    for col in position.get_search_order():
        if position.can_play(col):
            if position.is_winning_move(col, position.current_positions[position.get_current_player()]):
                #position.num_moves += 1
                #print(f"case 2 {get_win_score(position)}")
                #draw_board(position.current_positions)
                return get_win_score(position), col
            #if best_col is None:  # Set first playable column as fallback
                #best_col = col
     


    #if beta > max_score:
        #beta = max_score
        #if alpha >= beta:
            #return beta, best_col

    best_col = None
    best_score = float('-inf') 
    
    for col in position.get_search_order():

        if position.can_play(col):
            new_position = Position()
            new_position.current_positions = position.current_positions.copy()
            new_position.num_moves = position.num_moves
            new_position.play(col)

            score, move = Negamax(new_position, -beta, -alpha, transposition_table, max_depth-1)
            score *= -1
            # prune this tree as it will be avoided by minimizer
            if score >= beta:
                transposition_table[position.get_key()] = get_tt_entry(score, col, LB=True)
                return score, col
            
            
            if score > alpha:
                alpha = score
                best_col = col
                transposition_table[position.get_key()] = get_tt_entry(score, best_col)

            elif score > best_score:
                best_score = score
                best_col = col

    return alpha, best_col


def solve(position, weak=False, loop_iters=5, search_depth=16):
    min_val = -(position.board_width * position.board_height - position.num_moves) // 2
    max_val = (position.board_width * position.board_height + 1 - position.num_moves) // 2
    best_move = -8
    
    if weak:
        min_val = -3
        max_val = 3


    #draw_board(position.current_positions)
    t_t = TranspositionTable()

    for _ in range(loop_iters):  
        mid = min_val + (max_val - min_val) // 2
        if mid <= 0 and min_val // 2 < mid:
            mid = min_val // 2
        elif mid >= 0 and max_val // 2 > mid:
            mid = max_val // 2

        r, best_move = Negamax(position, mid, mid + 1, t_t, max_depth=search_depth)  # use a null depth window to know if the actual score is greater or smaller than mid

        if r <= mid:
            max_val = r
        else:
            min_val = r

    return min_val, best_move





def draw_board(positions):
        board = [[-1 for _ in range(7)] for _ in range(6)]
        positions = [bin(x)[2:].zfill(49) for x in positions]
        ptr = len(positions[0]) - 1
        for j in range(7):
            if j!=0:
                ptr -=1
            for i in range(5,-1,-1):
                if positions[0][ptr] == 'R':
                    board[i][j] = 0
                elif positions[1][ptr] == 'Y':
                    board[i][j] = 1
                ptr -=1
        print("\n".join([" ".join(["." if cell == -1 else str(cell) for cell in row]) for row in board]))
        

    
    


