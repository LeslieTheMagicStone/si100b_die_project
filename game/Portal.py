# -*- coding:utf-8 -*-

from Settings import *

import pygame
from Attributes import *


class Portal(pygame.sprite.Sprite, Renderable):
    def __init__(self, x, y, GOTO):
        pygame.sprite.Sprite.__init__(self)
        Renderable.__init__(self, render_index=2)

        self.image = pygame.image.load(GamePath.portal)
        self.image = pygame.transform.scale(
            self.image, (PortalSettings.width, PortalSettings.height)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.GOTO = GOTO

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)
