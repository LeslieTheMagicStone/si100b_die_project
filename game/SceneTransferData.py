from Player import *
import pygame


class SceneTransferData:
    def __init__(self, window: pygame.Surface, player: Player, name) -> None:
        self.window = window
        self.player = player
        self.name = name
