from position import Position
from solver import solve


def test(testfile):
    failed_tests = 0
    moves_to_result = {}
    with open(testfile, "r") as file:  
        for line in file:
            parts = line.strip().split()  
            if len(parts) == 2:  
                moves = parts[0]  
                result = int(parts[1])  
                moves_to_result[moves] = result  
    total_tests = len(moves_to_result)
    for moves in moves_to_result:
        player1_bs=["0"] * 49
        player2_bs=["0"] * 49
        start_pos = 48
        col_heights = [0,0,0,0,0,0,0]
        #print("moves list: ", moves)
        for ind,move in enumerate(moves):
            col = int(move)-1
            col_shift = col if col!=0 else 0
            if ind % 2 ==0:
                player1_bs[start_pos - ((col*6) +col_shift + col_heights[col]) ] = "1"
                col_heights[col] += 1
            else:
                player2_bs[start_pos - ((col*6)+ col_shift + col_heights[col])] = "1"
                col_heights[col] +=1
        #print("bitstring 1: ",''.join(player1_bs))
        #print("bitstring 2: ",''.join(player2_bs))
        player1_bs = int(''.join(player1_bs), 2)
        player2_bs = int(''.join(player2_bs),2)
        pos = Position()
        pos.num_moves = len(moves)
        #print(f"num moves {pos.num_moves}")
        pos.current_positions = [player1_bs, player2_bs]
        if len(moves)%2 == 0:
            #print("1 goes first")
            pos.current_player = 0
        else:
            #print("2 goes first")
            pos.current_player = 1
        #res = Negamax(pos, -40, 40)
        #res = solve(pos, weak=True)
        res = solve(pos)
        print(f"current positions: {pos.current_positions}")
        print(f"result is {res} and expected is {moves_to_result[moves]}")
        if res[0] != moves_to_result[moves]:
            failed_tests += 1
    print(f"{total_tests - failed_tests}/{total_tests} passed")

    
test("tests/mini_test.txt")
#test("tests/hard_test.txt")
#test("tests/test.txt")