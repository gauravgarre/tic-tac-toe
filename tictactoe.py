import random
from math import inf as infinity

def print_board(board):
    print("---------")
    print(f"| {' '.join(board[2])} |")
    print(f"| {' '.join(board[1])} |")
    print(f"| {' '.join(board[0])} |")
    print("---------")


def choose_move(board):
    x_count = 0
    o_count = 0
    for row in board:
        x_count += row.count('X')
        o_count += row.count('O')
    if x_count == o_count:
        return 'X'
    return 'O'


def anti_mover(move):
    if move == 'X':
        return 'O'
    else:
        return 'X'


def medium_ai(board, move):
    anti_move = anti_mover(move)

    open_cells = find_open_cells(board)
    for index, row in enumerate(open_cells):
        if len(row) == 1 and board[index].count(move) == 2:
            return row[0]
    for i in range(3):
        column = [board[0][i], board[1][i], board[2][i]]
        if column.count(' ') == 1 and column.count(move) == 2:
            ind = column.index(' ')
            return ind, i
    cross = [board[2][0], board[1][1], board[0][2]]
    if cross.count(' ') == 1 and cross.count(move) == 2:
        ind = cross.index(' ')
        rev_ind = 2 - ind
        return rev_ind, ind
    if cross.count(' ') == 1 and cross.count(move) == 2:
        ind = cross.index(' ')
        return ind, ind

    for index, row in enumerate(open_cells):
        if len(row) == 1 and board[index].count(anti_move) == 2:
            return row[0]
    for i in range(3):
        column = [board[0][i], board[1][i], board[2][i]]
        if column.count(' ') == 1 and column.count(anti_move) == 2:
            ind = column.index(' ')
            return ind, i

    if cross.count(' ') == 1 and cross.count(anti_move) == 2:
        ind = cross.index(' ')
        rev_ind = 2 - ind
        return rev_ind, ind
    if cross.count(' ') == 1 and cross.count(anti_move) == 2:
        ind = cross.index(' ')
        return ind, ind

    cmp_row = []
    while len(cmp_row) == 0:
        cmp_row = random.choice(open_cells)
    cmp_move = random.choice(cmp_row)
    return cmp_move


def check_board(board):
    for row in board:
        if all(space == "X" for space in row):
            return True, 'X'
        elif all(space == "O" for space in row):
            return True, 'O'
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
            return True, board[0][i]
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != " ":
        return True, board[2][0]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return True, board[0][0]
    empty_spaces = 0
    for row in board:
        for cell in row:
            if cell == " ":
                empty_spaces += 1
    if empty_spaces == 0:
        return False, "Draw"
    else:
        return False, None


def find_open_cells(board):
    open_cells = []
    for index1, row in enumerate(board):
        row_cells = []
        for index2, cell in enumerate(row):
            if cell == " ":
                row_cells.append((index1, index2))
        open_cells.append(row_cells)
    return open_cells


def check_finished(board):
    print_board(board)
    result = check_board(board)
    if result[0]:
        print(f"{result[1]} wins")
        return True
    elif result[1] is not None:
        print(result[1])
        return True


def minimax(newBoard, player, count=0):
    minimax.fc += 1

    checknewboard = [' ' if isinstance(space, int) else space for space in newBoard]
    checknewboard1 = [[checknewboard[6], checknewboard[7], checknewboard[8]],
                      [checknewboard[3], checknewboard[4], checknewboard[5]],
                      [checknewboard[0], checknewboard[1], checknewboard[2]]]
    minimaxfc = check_board(checknewboard1)

    if minimaxfc[0] == True and minimaxfc[1] == huPlayer:
        return -1
    elif minimaxfc[0] == True and minimaxfc[1] == aiPlayer:
        return 1
    elif minimaxfc[1] == "Draw":
        return 0

    moves = []
    availSpots = [spot for spot in newBoard if isinstance(spot, int)]
    for spot in availSpots:
        move = {}
        move['index'] = spot
        new_state = newBoard[:]
        new_state[spot] = player

        if player == aiPlayer:
            result = minimax(new_state, huPlayer)
            move['score'] = result
        else:
            result = minimax(new_state, aiPlayer)
            move['score'] = result

        #new_state[spot] = spot
        moves.append(move)

    bestMove = None
    if player == aiPlayer:
        bestScore = -infinity
        for move in moves:
            if move['score'] > bestScore:
                bestScore = move['score']
                bestMove = move['index']
    else:
        bestScore = infinity
        for move in moves:
            if move['score'] < bestScore:
                bestScore = move['score']
                bestMove = move['index']

    return bestMove


minimax.fc = 0
user_input = None

while user_input != "exit":
    random.seed()
    user_input = input("Input command: ").split()
    if user_input[0] == 'start' and len(user_input) == 3:
        board = [[" "] * 3 for _ in range(3)]
        #board = [[' ', 'O', 'O'], ['X', ' ', 'X'], ['O', ' ', 'X']]
        move = 'X'
        finished = False
        turn_counter = 1
        turn = user_input[1]

        while not finished:
            move = choose_move(board)

            if turn == 'user':
                coord = input("Enter the coordinates: ").split()
                if any(num.isalpha() for num in coord):
                    print("You should enter numbers!")
                    continue
                elif any(int(n) > 3 or int(n) < 1 for n in coord):
                    print("Coordinates should be from 1 to 3!")
                    continue
                elif len(coord) != 2:
                    print("Not the correct amount of coordinates!")
                    continue
                elif board[int(coord[1]) - 1][int(coord[0]) - 1] != " ":
                    print("This cell is occupied! Choose another one!")
                    continue
                else:
                    board[int(coord[1]) - 1][int(coord[0]) - 1] = move
                    finished = check_finished(board)

            elif turn == 'easy':
                open_cells = find_open_cells(board)
                cmp_row = []
                while len(cmp_row) == 0:
                    cmp_row = random.choice(open_cells)
                cmp_move = random.choice(cmp_row)
                board[cmp_move[0]][cmp_move[1]] = move
                print('Making move level "easy"')
                finished = check_finished(board)

            elif turn == 'medium':
                cmp_move = medium_ai(board, move)
                board[cmp_move[0]][cmp_move[1]] = move
                print('Making move level "medium"')
                finished = check_finished(board)

            elif turn == 'hard':
                originalBoard = []
                for i in range(2, -1, -1):
                    for space in board[i]:
                        originalBoard.append(space)
                for c, space in enumerate(originalBoard):
                    if space == ' ':
                        originalBoard[c] = originalBoard.index(space)
                aiPlayer = move
                huPlayer = anti_mover(move)
                bestSpot = minimax(originalBoard, aiPlayer)
                if bestSpot < 3:
                    board[2][bestSpot] = move
                elif bestSpot < 6:
                    board[1][bestSpot - 3] = move
                elif bestSpot < 9:
                    board[0][bestSpot - 6] = move
                print('Making move level "hard"')
                finished = check_finished(board)

            turn_counter += 1
            if turn_counter % 2 == 0:
                turn = user_input[2]
            else:
                turn = user_input[1]

    elif user_input[0] == 'exit':
        break
    else:
        print("Bad parameters!")
