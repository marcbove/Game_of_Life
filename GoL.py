import pygame
import numpy as np
import time

# Constants
WIDTH, HEIGHT = 500, 500
BG_COLOUR = 30, 30, 30
X_COL, Y_COL = 25, 25


if __name__ == '__main__':

    pygame.init()

    # Create screen
    screen = pygame.display.set_mode((HEIGHT, WIDTH))

    # Fill screen with bg colour
    screen.fill(BG_COLOUR)

    # Set row and column number
    dim_width = WIDTH / X_COL
    dim_height = HEIGHT / Y_COL

    # Initialize game matrix
    gameMatrix = np.zeros((X_COL, Y_COL))
    gameMatrix[5, 3] = 1
    gameMatrix[5, 4] = 1
    gameMatrix[6, 4] = 1
    gameMatrix[6, 5] = 1
    gameMatrix[7, 4] = 1
    pauseExec = True

    while True:

        newGameState = np.copy(gameMatrix)

        screen.fill(BG_COLOUR)

        events = pygame.event.get()

        for e in events:

            if e.type == pygame.KEYDOWN:
                pauseExec = not pauseExec

            mouseClick = pygame.mouse.get_pressed()

            if sum(mouseClick) != 0:
                posX, posY = pygame.mouse.get_pos()
                celX, celY = int(np.floor(posX / dim_width)), int(np.floor(posY / dim_height))
                newGameState[celX, celY] = not newGameState[celX, celY]

        for y in range(0, Y_COL):
            for x in range(0, X_COL):

                if not pauseExec:

                    n_neigh = gameMatrix[(x - 1) % X_COL, (y - 1) % Y_COL] + \
                              gameMatrix[x % X_COL, (y - 1) % Y_COL] + \
                              gameMatrix[(x + 1) % X_COL, (y - 1) % Y_COL] + \
                              gameMatrix[(x - 1) % X_COL, y % Y_COL] + \
                              gameMatrix[(x + 1) % X_COL, y % Y_COL] + \
                              gameMatrix[(x - 1) % X_COL, (y + 1) % Y_COL] + \
                              gameMatrix[x % X_COL, (y + 1) % Y_COL] + \
                              gameMatrix[(x + 1) % X_COL, (y + 1) % Y_COL]

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
