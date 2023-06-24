import os
import numpy as np
import main
import AlphaBeta
from enum import Enum
import pygame
from pygame.locals import *

BOARD_SIZE = 6
resolution = (500, 500)
screen = pygame.display.set_mode(resolution)
map_size = (7, 7)  # (rows, columns)
line_width = 3
clock = pygame.time.Clock()  # to set max FPS
clock.tick(60)  # max FPS = 60
screen.fill((255, 255, 255))

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


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_title():
    print(CLI_CYAN)
    print()
    print(CLI_BOLD + "\t\t\t\t****GridLock****\n\n" + CLI_RESET + CLI_BOLD)


def intro():
    # print_title() print( CLI_BOLD_YELLOW + CLI_UNDERLINE + "\n\nDescription:\n" + CLI_RESET + "First player is " +
    # CLI_BOLD_BLUE + "X" + CLI_RESET + CLI_BOLD + " and the second player is " + CLI_BOLD_RED + "O" + CLI_RESET +
    # CLI_BOLD + ".") print("When a player enters their symbol on a cell, the adjacent cells are blocked, preventing
    # the other player " "from playing their move on those cells.") print(CLI_BOLD_YELLOW + "To write your symbol in
    # a cell you must specify the location.") print(CLI_BOLD_YELLOW + "Ex:") print(CLI_RESET + CLI_BOLD + " a1 c4
    # b6\n\n")
    pygame.init()
    pygame.font.init()
    # screen.fill((0, 100, 100))
    pygame.display.set_caption('GridLock')
    Icon = pygame.image.load('icon.jpg')
    pygame.display.set_icon(Icon)
    logo = pygame.image.load("logo.jpg").convert()
    screen.blit(logo, (0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('GridLock', True, (0, 0, 0))
    # start_button = font.render('Start', True, (255, 255, 255))
    screen.blit(title, (500 / 2 - title.get_width() / 2, 500 / 2 - title.get_height() / 2))
    # screen.blit(start_button,
    #             (500 / 2 - start_button.get_width() / 2, 500 / 2 + start_button.get_height() / 2))
    pygame.display.update()


def get_play_against_bot():
    input_str = input(CLI_BOLD + "play against the bot? [y/n]: ")
    return input_str.lower() in ['y', 'yes']


def get_user_starts():
    input_str = input(CLI_BOLD + "be the starting player? (player X) [y/n]: ")
    return input_str.lower() in ['y', 'yes']


def get_board():
    board = np.zeros([BOARD_SIZE, BOARD_SIZE], dtype=int)
    # print(board)
    return board


def reset_board(board):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            board[y][x] = BoardState.FREE
    return board


def print_board(board):
    clear()
    print(CLI_RESET)
    print_title()
    print("\t\t\t      a   b   c   d   e   f")
    print(CLI_BOLD_GREEN)
    print("\t\t\t    |---*---*---*---*---*---|")
    for y in range(BOARD_SIZE):
        print(CLI_RESET + CLI_BOLD + "\t\t\t  " + str(y + 1) + " " + CLI_BOLD_GREEN + "|", end="")
        for x in range(BOARD_SIZE):
            cell = board[y][x]
            if cell == BoardState.PLAYER_X:
                print(CLI_BOLD_BLUE + " X ", end="")
            elif cell == BoardState.PLAYER_O:
                print(CLI_BOLD_RED + " O ", end="")
            elif cell == BoardState.FREE:
                print("   ", end="")
            elif cell == BoardState.BLOCKED:
                print(CLI_RESET + CLI_BOLD + " # ", end="")
            if x != BOARD_SIZE - 1:
                print(CLI_BOLD_GREEN + "|", end="")
        print(CLI_BOLD_GREEN + "|")
        if y != BOARD_SIZE - 1:
            print("\t\t\t    |---*---*---*---*---*---|")
    print("\t\t\t    |---*---*---*---*---*---|\n")
    print(CLI_RESET + CLI_BOLD)
    # print("\t\t    ==+==+==+==+==+==+==+==+==+==+==+==+==+==\n\n")


def terminal_state(board):
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == BoardState.FREE:
                return False
    return True


def get_winner(board):
    player = get_player(board)
    if player == BoardState.PLAYER_X:
        return BoardState.PLAYER_O
    else:
        return BoardState.PLAYER_X


def get_player(board):
    x_count = (board == BoardState.PLAYER_X).sum()
    o_count = (board == BoardState.PLAYER_O).sum()
    if x_count > o_count:
        return BoardState.PLAYER_O
    return BoardState.PLAYER_X


def place_move(board, mode, player, x, y):
    n_board = board.copy()
    if mode:
        for i in range(max(y - 1, 0), min(y + 2, BOARD_SIZE)):
            for j in range(max(x - 1, 0), min(x + 2, BOARD_SIZE)):
                n_board[i][j] = BoardState.BLOCKED
    else:
        if y - 1 >= 0 and x - 1 >= 0:
            n_board[y - 1][x - 1] = BoardState.BLOCKED
        if y - 1 >= 0 and x + 1 <= BOARD_SIZE - 1:
            n_board[y - 1][x + 1] = BoardState.BLOCKED
        if y + 1 <= BOARD_SIZE - 1 and x - 1 >= 0:
            n_board[y + 1][x - 1] = BoardState.BLOCKED
        if y + 1 <= BOARD_SIZE - 1 and x + 1 <= BOARD_SIZE - 1:
            n_board[y + 1][x + 1] = BoardState.BLOCKED
    n_board[y][x] = player
    return n_board


def user_move(board, mode):
    player = get_player(board)

    while True:
        move = input(
            "\t\t\t    Player " + CLI_BOLD_RED + "X" + CLI_RESET + CLI_BOLD + " > " if player == BoardState.PLAYER_X else "\t\t\t    Player " + CLI_BOLD_BLUE + "O" + CLI_RESET + CLI_BOLD + " > ")
        move = move.strip().lower()

        if len(move) != 2 or move[0] not in 'abcdef' or move[1] not in '123456':
            print_board(board)
            continue

        x = ord(move[0]) - ord('a')
        y = int(move[1]) - 1

        if board[y][x] != BoardState.FREE:
            print_board(board)
            print(CLI_BOLD_RED + "\t\t\tYou are trying to access a blocked square\n" + CLI_RESET)
            continue

        break

    board = place_move(board, mode, get_player(board), x, y)
    return board


def print_winner(board):
    winner = get_winner(board)
    # print(CLI_BOLD_YELLOW)
    if winner == BoardState.PLAYER_X:
        msg = "Player X wins!"
        # print("\t\t\t\t Player " + CLI_BOLD_BLUE + "X" + CLI_BOLD_YELLOW + " wins.\n\n")
    elif winner == BoardState.PLAYER_O:
        msg = "Player O wins!"
        # print("\t\t\t\t Player " + CLI_BOLD_RED + "O" + CLI_BOLD_YELLOW + " wins.\n\n")
    # print(CLI_RESET)

    screen.fill((0, 100, 100))
    font = pygame.font.SysFont('arial', 40)
    font2 = pygame.font.SysFont('arial', 20)
    title = font.render(msg, True, (255, 255, 255))
    trophy = pygame.image.load("trophy.png")
    screen.blit(trophy, (250 - 32, 125 - 32))
    restart_button = font2.render('R - Restart', True, (255, 255, 255))
    quit_button = font2.render('Q - Quit', True, (255, 255, 255))
    screen.blit(title, (500 / 2 - title.get_width() / 2, 500 / 2 - title.get_height() / 2 - 50))
    screen.blit(restart_button,
                (500 / 2 - restart_button.get_width() / 2, 500 / 2 + restart_button.get_height() + 30))
    screen.blit(quit_button,
                (500 / 2 - quit_button.get_width() / 2, 500 / 2 + quit_button.get_height() / 2 + 15))
    pygame.display.update()


def print_bot_is_thinking():
    print(CLI_BOLD_YELLOW)
    print("\t\t   The bot is thinking...")
    print("\t  (first move may take longer)\n\n")


def play_again():
    input_str = input(CLI_BOLD + "\t\t\t\t\n" + "\t\t\t\t\n\n" + "\t\t\t\t    > ")
    return input_str.lower() in ['r', 'replay']
    # for event in pygame.event.get():
    #     if event.type == QUIT:
    #         pygame.quit()
    #         # sys.exit()
    #     elif event.type == KEYDOWN:
    #         if event.key == K_r:
    #             return True
    #         elif event.key == K_q:
    #             return False
