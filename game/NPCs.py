# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Math import *


class NPC(pygame.sprite.Sprite, Collidable, Renderable, MonoBehavior):
    def __init__(self, x, y, name, render_index=RenderIndex.npc):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        Renderable.__init__(self, render_index)
        MonoBehavior.__init__(self)

        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

    def update(self):
        raise NotImplementedError

    def reset_talkCD(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)


"""DialogNPC就是道具"""


class DialogNPC(NPC):
    def __init__(self, x, y, name, dialog, player_rect: pygame.Rect):
        super().__init__()
        self.image = pygame.image.load(GamePath.monster)
        self.image = pygame.transform.scale(
            self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.player_rect = player_rect


class Monster(NPC):
    def __init__(
        self,
        player_rect: pygame.Rect,
        x,
        y,
        speed=4,
        hp=10,
        attack=3,
        defence=1,
        money=15,
    ):
        super().__init__(x, y, name="Monster", render_index=RenderIndex.monster)
        # Image and rect related
        self.image = pygame.image.load(GamePath.monster)
        self.image = pygame.transform.scale(
            self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Save player position
        self.player_rect = player_rect
        # Attribute related
        self.speed = speed
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.money = money

    def update(self):
        # Straightly moves towards the player
        dir = (self.player_rect.x - self.rect.x, self.player_rect.y - self.rect.y)
        movement = Math.round(Math.dot(Math.normalize(dir), self.speed))
        self.rect.move_ip(movement[0], movement[1])

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
