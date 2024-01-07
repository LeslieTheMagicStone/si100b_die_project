# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *


class Player(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)

        # Image related
        self.image = pygame.image.load(GamePath.player[0])
        self.rect = self.image.get_rect()
        # Attribute related
        self.speed = PlayerSettings.playerSpeed

    def attr_update(self, addCoins=0, addHP=0, addAttack=0, addDefence=0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def try_move(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update(self, width, height):
        keys = pygame.key.get_pressed()

        dx, dy = 0
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_d]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        norm = pow((dx ^ 2 + dy ^ 2), 0.5)
        if norm != 0:
            dx /= norm
            dy /= norm

        dx *= self.speed
        dy *= self.speed

        self.rect = self.rect.move(dx, dy)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)
