from itertools import groupby
import sys
import copy


class Position:
    
    def __init__(self):
        self.board_height = 6
        self.board_width = 7
        self.num_moves = 0
        self.current_positions=[0,0]
        self.current_player = 0 
        self.last_move = -1
        self.bit_shifts = self.__get_bit_shifts()
        self.column_order = [self.board_width // 2 + (1 - 2 * (i % 2)) * (i + 1) // 2 for i in range(self.board_width)]


    def get_mask(self):
        return self.current_positions[0] | self.current_positions[1]
    
    def get_key(self):
        ''' returns unique game state identifier '''
        return self.get_mask() + self.current_positions[self.get_current_player()]
         
    def can_play(self,  col):
        if self.num_moves == self.board_height * self.board_width:
            return False
        mask = self.get_mask()
        return (mask & self.top_mask(col)) == 0
    
    def top_mask(self, col):
        height = 6
        # check top level value of col
        return (1<< (height - 1)) << col * (height + 1)
    
    def get_search_order(self):
        col_order = filter(self.can_play, self.column_order)
        return sorted(col_order, key=self.__col_sort, reverse=True)
    
    #https://github.com/lhorrell99/connect-4-solver/blob/master/board.py
    def __get_bit_shifts(self):
        return [
            1,              # | vertical
            self.board_height,         # \ diagonal
            self.board_height + 1,     # - horizontal
            self.board_height + 2      # / diagonal
        ]
    
    #https://github.com/lhorrell99/connect-4-solver/blob/master/board.py
    def __col_sort(self, col):

        mask = self.get_mask()
        player = self.get_current_player()
        position = self.current_positions[player]
        opp_position = position ^ mask
        new_mask = mask | mask + self.bottom_mask(col)
        state = opp_position ^ new_mask

        count=0

        for shift in self.bit_shifts:
            test = state & (state >> shift) & (state >> 2 * shift)
            if test:
                count += bin(test).count('1')

        return count
    

    def get_current_player(self):
        if self.num_moves % 2 == 0:
            return 0
        return 1
    
    
    def play(self, col):

        curr_player = self.get_current_player()
        mask = self.get_mask()
    
        # Get the opponent player index (1 if curr_player is 0, otherwise 0)
        opponent = 1 - curr_player  

        # Update the current positions
        self.current_positions[opponent] = self.current_positions[curr_player] ^ mask
        updated_mask = mask | (mask + self.bottom_mask(col))
        self.current_positions[curr_player] = self.current_positions[opponent] ^ updated_mask
    
        # Update move count and last move
        self.num_moves += 1
        self.last_move = col
                
    
    def bottom_mask(self, col):
        # get bottom col bit, useful for adding bits to mask to determine where
        # new token should fall
        height = 6
        return 1 << col * (height+1)
    
    def is_winning_move(self, col, position):
        mask = self.get_mask()
        opp_position = position ^ mask
        new_mask = mask | mask + self.bottom_mask(col)
        candidate_position = opp_position ^ new_mask
        if self.connected_four(candidate_position):
            return True
        return False


        
    def connected_four(self, position):
        # Horizontal check
        m = position & (position >> 7)
        if m & (m >> 14):
            return True
        # Diagonal \
        m = position & (position >> 6)
        if m & (m >> 12):
            return True
        # Diagonal /
        m = position & (position >> 8)
        if m & (m >> 16):
            return True
        # Vertical
        m = position & (position >> 1)
        if m & (m >> 2):
            return True
        # Nothing found
        return False
    
    def board_state(self):
        board = [[-1 for _ in range(7)] for _ in range(6)]
        positions = [bin(x)[2:].zfill(49) for x in self.current_positions]
        ptr = len(positions[0]) - 1
        for j in range(7):
            if j!=0:
                ptr -=1
            for i in range(5,-1,-1):
                if positions[0][ptr] == '1':
                    board[i][j] = 0
                elif positions[1][ptr] == '1':
                    board[i][j] = 1
                ptr -=1
        return board











  

