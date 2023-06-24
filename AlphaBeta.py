import GridLock
import main
import pygame

BOARD_SIZE = 6

depth = 6

CLI_RESET = "\033[0m"
CLI_BOLD = "\033[1m"
CLI_UNDERLINE = "\033[4m"
CLI_CYAN = "\033[36m"
CLI_BOLD_YELLOW = "\033[1;33m"
CLI_BOLD_BLUE = "\033[1;34m"
CLI_BOLD_RED = "\033[1;31m"
CLI_BOLD_GREEN = "\033[1;32m"


class BoardState:
    FREE = 0
    PLAYER_X = 1
    PLAYER_O = 2
    BLOCKED = 3


def get_max_values_index(array, size):
    index = 0

    for i in range(size):
        if array[i] >= array[index]:
            index = i

    return index


def get_min_values_index(array, size):
    index = 0

    for i in range(size):
        if array[i] < array[index]:
            index = i

    return index


def get_moves(board):
    moves = [[None] * 2 for _ in range(BOARD_SIZE * BOARD_SIZE)]
    move_index = 0

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            # print(board[y][x])
            if board[y][x] == BoardState.FREE:
                # print(board[y][x])
                moves[move_index][0] = x
                moves[move_index][1] = y
                move_index += 1
    # print(board)
    # print(moves)
    if move_index != BOARD_SIZE * BOARD_SIZE:
        for i in range(move_index, BOARD_SIZE * BOARD_SIZE):
            moves[i] = None

    return moves


def get_board_of_move(board, mode, x, y):
    # new_board = GridLock.get_board()

    # # print(board)
    #
    # for y in range(BOARD_SIZE):
    #     for x in range(BOARD_SIZE):
    #         new_board[y][x] = board[y][x]

    new_board = GridLock.place_move(board, mode,  GridLock.get_player(board), x, y)

    return new_board


def utility(board):
    winner = GridLock.get_winner(board)
    if winner == BoardState.PLAYER_X:
        return 1
    else:
        return -1


def max_value(board, depth, alpha, beta, mode):
    if GridLock.terminal_state(board) or depth == 0:
        return utility(board)

    value = -2
    moves = get_moves(board)
    # print(moves)
    # print("a")
    for i in range(BOARD_SIZE * BOARD_SIZE):
        pygame.event.pump()
        if moves[i] is None:
            break
        new_board = get_board_of_move(board, mode, moves[i][0], moves[i][1])
        # GridLock.print_board(new_board)
        value = max(value, min_value(new_board, depth-1, alpha, beta, mode))
        # GridLock.free_board(new_board)
        alpha = max(alpha, value)
        if beta <= alpha:
            break

    # free_2d_array(moves, BOARD_SIZE * BOARD_SIZE)

    return value


def min_value(board, depth, alpha, beta, mode):
    if GridLock.terminal_state(board) or depth == 0:
        return utility(board)

    value = 2
    moves = get_moves(board)
    # print(moves)
    # print("b")
    for i in range(BOARD_SIZE * BOARD_SIZE):
        pygame.event.pump()
        if moves[i] is None:
            break
        new_board = get_board_of_move(board, mode, moves[i][0], moves[i][1])
        # GridLock.print_board(new_board)
        value = min(value, max_value(new_board, depth-1, alpha, beta, mode))
        # GridLock.free_board(new_board)
        beta = min(beta, value)
        if beta <= alpha:
            break

    # free_2d_array(moves, BOARD_SIZE * BOARD_SIZE)

    return value


def alpha_beta(board, mode):
    n_board = board.copy()

    # print(board)

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            n_board[y][x] = board[y][x]
    moves = get_moves(board)
    # print(moves)
    values = [0] * (BOARD_SIZE * BOARD_SIZE)

    if GridLock.get_player(board) == BoardState.PLAYER_X:
        number_of_moves = 0
        for i in range(BOARD_SIZE * BOARD_SIZE):
            pygame.event.pump()
            if moves[i] is None:
                break
            new_board = get_board_of_move(n_board, mode, moves[i][0], moves[i][1])
            values[i] = min_value(new_board, mode, depth, -2, 2)
            # GridLock.free_board(new_board)
            number_of_moves += 1

            if values[i] == 1:
                break

        max_values_index = get_max_values_index(values, number_of_moves)
        x = moves[max_values_index][0]
        y = moves[max_values_index][1]
    else:
        number_of_moves = 0
        for i in range(BOARD_SIZE * BOARD_SIZE):
            pygame.event.pump()
            if moves[i] is None:
                break
            # print("move 0: ", moves[i][0])
            # print("move 1: ", moves[i][1])
            new_board = n_board
            new_board = get_board_of_move(n_board, mode, moves[i][0], moves[i][1])
            values[i] = max_value(new_board, depth, -2, 2, mode)
            # print("value: ", values[i])
            # GridLock.free_board(new_board)
            number_of_moves += 1

            if values[i] == -1:
                break

        min_values_index = get_min_values_index(values, number_of_moves)
        x = moves[min_values_index][0]
        y = moves[min_values_index][1]

    #free_2d_array(moves, BOARD_SIZE * BOARD_SIZE)

    a = GridLock.place_move(board, mode, GridLock.get_player(board), x, y)
    return a
