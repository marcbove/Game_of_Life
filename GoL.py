import pygame
import numpy as np
import time

pygame.init()

# Create screen
width, height = 500, 500
screen = pygame.display.set_mode((height, width))

# Fill screen with bg colour
bg = 30, 30, 30
screen.fill(bg)

# Set row and column number
x_col, y_col = 25, 25
dim_width = width / x_col
dim_height = height / y_col

# Initialize game matrix
gameMatrix = np.zeros((x_col, y_col))
gameMatrix[5, 3] = 1
gameMatrix[5, 4] = 1
gameMatrix[6, 4] = 1
gameMatrix[6, 5] = 1
gameMatrix[7, 4] = 1
pauseExec = True

while True:

    newGameState = np.copy(gameMatrix)

    screen.fill(bg)

    events = pygame.event.get()

    for e in events:

        if e.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) != 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dim_width)), int(np.floor(posY / dim_height))
            newGameState[celX, celY] = not newGameState[celX, celY]

    for y in range(0, y_col):
        for x in range(0, x_col):

            if not pauseExec:

                n_neigh = gameMatrix[(x - 1) % x_col, (y - 1) % y_col] + \
                          gameMatrix[x % x_col,       (y - 1) % y_col] + \
                          gameMatrix[(x + 1) % x_col, (y - 1) % y_col] + \
                          gameMatrix[(x - 1) % x_col, y % y_col] + \
                          gameMatrix[(x + 1) % x_col, y % y_col] + \
                          gameMatrix[(x - 1) % x_col, (y + 1) % y_col] + \
                          gameMatrix[x % x_col,       (y + 1) % y_col] + \
                          gameMatrix[(x + 1) % x_col, (y + 1) % y_col]

                if gameMatrix[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                elif gameMatrix[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            polygon = [(x * dim_width, y * dim_height),
                       ((x + 1) * dim_width, y * dim_height),
                       ((x + 1) * dim_width, (y + 1) * dim_height),
                       (x * dim_width, (y + 1) * dim_height)]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), polygon, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), polygon, 0)

    gameMatrix = np.copy(newGameState)

    pygame.display.flip()

    time.sleep(0.1)
