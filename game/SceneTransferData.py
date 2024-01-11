from Player import *
import pygame

from PopUpBox import *


class SceneTransferData:
    def __init__(
        self,
        window: pygame.Surface,
        player: Player,
        name,
    ) -> None:
        self.window = window
        self.player = player
        self.name = name
