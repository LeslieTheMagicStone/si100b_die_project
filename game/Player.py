# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Portal import *
from EventSystem import *


class Player(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)

        # Image related
        self.image = pygame.image.load(GamePath.player[0])
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.width, PlayerSettings.height)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Attribute related
        self.speed = PlayerSettings.speed
        self.coins = 0
        self.hp = PlayerSettings.hp
        self.attack = PlayerSettings.attack
        self.defence = PlayerSettings.defence

    def attr_update(self, addCoins=0, addHP=0, addAttack=0, addDefence=0):
        self.coins += addCoins
        self.hp += addHP
        self.attack += addAttack
        self.defence += addDefence

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        self.rect.center = (x, y)

    def try_move(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update(self):
        self.handle_movement()
        self.handle_collisions()

    def handle_movement(self):
        keys = pygame.key.get_pressed()

        dx = dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        norm = (dx**2 + dy**2) ** 0.5
        if norm != 0:
            dx /= norm
            dy /= norm

        dx *= self.speed
        dy *= self.speed

        self.rect = self.rect.move(dx, dy)

    def handle_collisions(self):
        for enter in self.collisions_enter:
            if isinstance(enter, Portal):
                EventSystem.fire_switch_event(enter.GOTO)
                

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)
