import random
import copy


def empty_board(): 
    return [
[[" "], [" "], [" "]], 
[[" "], [" "], [" "]], 
[[" "], [" "], [" "]]
]

player_token = ['X', 'O']

def is_playable(board, position):
    """
    is_playable says id a position in a board is playable
    
    :param board: a list of three list of one list of a string
    :param position: position of slot (x,y) with x and y two int
    
    """
    return board[position[0]][position[1]] == [" "]

def are_playable(board):
    playable = []
    for i in range (3):
        for j in range(3):
            if is_playable(board, [i, j]):
                playable.append([i, j])
    return playable
    
def play_at(board, position, player):
    board[position[0]][position[1]] = [player]

def is_winning_position(board, move, player_token):
    #column
    if board[(move[0] - 1) % 3][move[1]] == board[(move[0] + 1) % 3][move[1]] == [player_token]:
        return True
    #line
    if board[move[0]][(move[1] - 1) % 3] == board[move[0]][(move[1] + 1) % 3] == [player_token]:
        return True
    #diag
    if move[0] == move[1]:
        if board[(move[0] - 1) % 3][(move[1] - 1) % 3] ==  board[(move[0] + 1) % 3][(move[1] + 1) % 3] == [player_token]:
            return True
    if move[0] + move[1] == 2:
        if board[(move[0] - 1) % 3][(move[1] + 1) % 3] ==  board[(move[0] + 1) % 3][(move[1] - 1) % 3] == [player_token]:
            return True
    return False

def display_board(board):
    for i in range (3):
        print(board[i])
        
def make_a_game(board, player):   
    while True:
        playable = are_playable(board)
        if playable == []:
            return None
        next_position = playable[random.randint(0,len(playable) - 1)]
        play_at(board, next_position, player_token[player])
        if is_winning_position(board, next_position, player_token[player]):
            return player_token[player]
        player = (player + 1) % 2

        
def temp(board, playable_win_rate, iteration):
    win_board = copy.deepcopy(board)
    n = 0
    for i in range(3):
        for j in range(3):
            if win_board[i][j] == [" "]:
                win_board[i][j] = [int(playable_win_rate[n]/iteration*100)]
                n += 1
    display_board(win_board)

def calculate_best_move(board, player, iteration):
    playable = are_playable(board)
    playable_win_rate = []
    playable_lose_rate = []
    for i in range (len(playable)):
        win_rate = 0
        lose_rate = 0
        for j in range (iteration):
            random_board = copy.deepcopy(board)
            if is_winning_position(random_board, playable[i], player_token[player]):
                win_rate += iteration
                break
            play_at(random_board, playable[i], player_token[player])
            game = make_a_game(random_board, (player + 1) % 2)
            win_rate += game == player_token[player]
            lose_rate += game == player_token[(player + 1) % 2]
        playable_win_rate.append(win_rate)
        playable_lose_rate.append(lose_rate)
    #temp(board,playable_lose_rate, iteration)
    #temp(board,playable_win_rate, iteration)
    return playable[playable_lose_rate.index(min(playable_lose_rate))]
    #return playable[playable_win_rate.index(max(playable_win_rate))]

def ia(iteration):
    playing_board = empty_board()
    human_player = int(input('Do you want to play as 0 or 1 ?\n'))
    ia_player = (human_player + 1) % 2
    player = 0
    position = [0,0]
    while not is_winning_position(playing_board, position, player_token[(player + 1) % 2]):
        if ia_player == player:
            position = calculate_best_move(playing_board, ia_player, iteration)
        else:
            position = input('Where do you want to play ?\n').split(',')
            position = [int(i) for i in position]
        play_at(playing_board, position, player_token[player])
        player = (player + 1) % 2
        display_board(playing_board)
        print('\n\n')
    display_board(playing_board)
    if not are_playable(playing_board):
        print('draw')
    else:
        print(player_token[(player + 1) % 2], 'has win the game')
    return False

ia(1000)