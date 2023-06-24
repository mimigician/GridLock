import pygame


class BoardState:
    FREE = 0
    PLAYER_X = 1
    PLAYER_O = 2
    BLOCKED = 3


BOARD_SIZE = 6
resolution = (500, 500)
screen = pygame.display.set_mode(resolution)
map_size = (7, 7)  # (rows, columns)
line_width = 3


# clock = pygame.time.Clock()  # to set max FPS


def evaluate_dimensions():
    # Evaluate the width and the height of the squares.
    square_width = (resolution[0] / map_size[0]) - line_width * ((map_size[0] + 1) / map_size[0])
    square_height = (resolution[1] / map_size[1]) - line_width * ((map_size[1] + 1) / map_size[1])
    # print(square_width, square_height)
    return 64, 64


def convert_column_to_x(column, square_width):
    x = line_width * (column + 1) + square_width * column
    return x


def convert_row_to_y(row, square_height):
    y = line_width * (row + 1) + square_height * row
    return y


def draw_squares(board):
    screen.fill((0, 100, 100))
    square_width, square_height = evaluate_dimensions()
    free = (200, 200, 200)  # (R, G, B)
    blocked = (255, 165, 0)
    redSquare = pygame.image.load("player_x.png")
    blueSquare = pygame.image.load("player_o.png")
    for column in range(map_size[1] - 1):
        charSquare = pygame.image.load("characters/letter-" + chr(ord('a') + column) + ".png")
        x = convert_column_to_x(column, square_width)
        y = convert_row_to_y(map_size[0] - 1, square_height)
        screen.blit(charSquare, (x, y))
        for row in range(map_size[0]):
            if row != map_size[0] - 1:
                numberSquare = pygame.image.load("digits/number-" + str(row + 1) + ".png")
                x = convert_column_to_x(map_size[1] - 1, square_width)
                y = convert_row_to_y(row, square_height)
                screen.blit(numberSquare, (x, y))
            for column in range(map_size[1]):
                x = convert_column_to_x(column, square_width)
                y = convert_row_to_y(row, square_height)
                geometry = (x, y, square_width, square_height)
                if row == map_size[0] - 1 or column == map_size[1] - 1:
                    continue
                cell = board[row][column]
                if cell == BoardState.PLAYER_X:
                    screen.blit(redSquare, (x, y))
                elif cell == BoardState.PLAYER_O:
                    screen.blit(blueSquare, (x, y))
                elif cell == BoardState.FREE:
                    pygame.draw.rect(screen, free, geometry)
                elif cell == BoardState.BLOCKED:
                    pygame.draw.rect(screen, blocked, geometry)

# while True:
#     # clock.tick(60)  # max FPS = 60
#     screen.fill((255, 255, 255))  # Fill screen with black color.
#     # draw_squares()
#     pygame.display.flip()  # Update the screen.
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             quit()
