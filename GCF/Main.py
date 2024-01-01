import pygame
import sys

from random import randint
from Settings import *
from Player import Player


def run_game():
    pygame.init()
    # Initialize window
    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    pygame.display.set_caption(WindowSettings.name)
    # Initialize player
    player = Player(WindowSettings.width // 2, WindowSettings.height // 2)

    bg = pygame.image.load(GamePath.player[0])

    clock = pygame.time.Clock()

    # Main loop
    while True:
        clock.tick(GameSettings.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        player.update()

        player.draw(window)
        window.blit(bg,(0,0))

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
