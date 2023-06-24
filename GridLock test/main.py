from enum import Enum
import os
import sys
# import resource   #for linux
import AlphaBeta
import GridLock
import pygame
import test

# resource.setrlimit(resource.RLIMIT_STACK, (0x10000000, resource.RLIM_INFINITY))
# sys.setrecursionlimit(0x100000)
BOARD_SIZE = 6
resolution = (480, 480)
screen = pygame.display.set_mode(resolution)
map_size = (7, 7)  # (rows, columns)
line_width = 3
# clock = pygame.time.Clock()  # to set max FPS
# clock.tick(60)  # max FPS = 60
screen.fill((255, 255, 255))


def main():
    board = GridLock.get_board()

    # Clear screen
    GridLock.clear()

    # Print the intro
    GridLock.intro()

    # print("Mode 1: Adjacent Cell Block")
    # print("Mode 2: Criss-Cross Cell Block")
    # mode = int(input("choose mode: "))


    # Get the options
    play_against_bot = GridLock.get_play_against_bot()
    user_starts = False
    bot_has_started = False
    if play_against_bot:
        user_starts = GridLock.get_user_starts()
        if not user_starts:
            bot_has_started = True

    # Main loop
    while True:
        # test.draw_squares(board)
        # Game loop
        print("Mode 0: Criss-Cross Cell Block")
        print("Mode 1: Adjacent Cell Block")
        mode = int(input("choose mode: "))
        while True:
            pygame.event.pump()
            # If the user is playing against the bot and does not want to start first and the bot has not started (
            # first move for the bot)
            if play_against_bot and not user_starts and bot_has_started:
                # Print the board
                # GridLock.print_board(board)
                test.draw_squares(board)
                pygame.display.flip()

                # Bots move (calculating the first state takes time, so just place at 0, 0 which is a winning move
                # for X) place_move(board, get_player(board), 0, 0)

                GridLock.print_bot_is_thinking()

                # Bots move
                board = AlphaBeta.alpha_beta(board, mode)

                # Set bot has started to true
                bot_has_started = False

            # Print the board
            # GridLock.print_board(board)
            test.draw_squares(board)
            pygame.display.flip()

            # Check if the user has places left to play
            if GridLock.terminal_state(board):
                test.draw_squares(board)
                pygame.display.flip()
                pygame.time.delay(1500)
                GridLock.print_winner(board)
                break

            # Users move
            board = GridLock.user_move(board, mode)

            # If the user is playing against the bot
            if play_against_bot:
                # Print the board
                # GridLock.print_board(board)
                test.draw_squares(board)
                pygame.display.flip()

                # Check if the bot has places left to play
                if GridLock.terminal_state(board):
                    test.draw_squares(board)
                    pygame.display.flip()
                    pygame.time.delay(1500)
                    GridLock.print_winner(board)
                    break

                GridLock.print_bot_is_thinking()

                # Bots move
                board = AlphaBeta.alpha_beta(board, mode)

        # If the user wants to play again
        if GridLock.play_again():
            # Reset the board
            board = GridLock.reset_board(board)

            # If the user was playing against the bot and didn't want to start first
            if play_against_bot and not user_starts:
                # Set bot has started to false
                bot_has_started = True

        # Else if the user does not want to play again
        else:

            # Break the loop
            break


if __name__ == "__main__":
    main()
