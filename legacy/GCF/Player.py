import pygame
from Math import Math
from Settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        # Get animation images
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (PlayerSettings.width, PlayerSettings.height)) for img in GamePath.player]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = PlayerSettings.speed
        

    def update(self):
        self.handle_movement()

    def handle_movement(self):
        keys = pygame.key.get_pressed()

        dir_x = dir_y = 0
        if keys[pygame.K_w]:
            dir_y = -1
        if keys[pygame.K_s]:
            dir_y = 1
        if keys[pygame.K_a]:
            dir_x = -1
        if keys[pygame.K_d]:
            dir_x = 1

        direction = Math.normalize((dir_x, dir_y))
        movement = (round(direction[0] * self.speed), round(direction[1] * self.speed))
        self.rect = self.rect.move(movement)

    def draw(self, window):
        window.blit(self.image, self.rect)
