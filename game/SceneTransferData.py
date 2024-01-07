from Player import *

class SceneTransferData:
    def __init__(self, window: pygame.Surface, player: Player) -> None:
        self.window = window
        self.player = player