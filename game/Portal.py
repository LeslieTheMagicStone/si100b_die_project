# -*- coding:utf-8 -*-

from Settings import *

import pygame
from Attributes import *


class Portal(pygame.sprite.Sprite, Renderable, Collidable):
    def __init__(self, x, y, GOTO):
        pygame.sprite.Sprite.__init__(self)
        Renderable.__init__(self, render_index=RenderIndex.portal)
        Collidable.__init__(self)

        self.image = pygame.image.load(GamePath.portal)
        self.image = pygame.transform.scale(
            self.image, (PortalSettings.width, PortalSettings.height)
        )
        self.rect = self.image.get_rect()
        # Scale the rect by 0.5x to make collision trigger more realistic
        self.rect.inflate_ip(-self.rect.width // 2, -self.rect.height // 2)
        self.rect.center = (x, y)
        self.GOTO = GOTO

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)
