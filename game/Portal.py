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
        self.rect.center = (x, y)

        # Safe the image pos because the top-left corner of
        # the rect will be moved for scaling
        self.image_pos = self.rect.topleft

        # Scale the rect by 0.5x to make collision trigger more realistic
        resize_amount = [-self.rect.width // 2, -self.rect.height // 2]
        self.rect.inflate_ip(resize_amount[0], resize_amount[1])

        self.GOTO = GOTO

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, (self.image_pos[0] + dx, self.image_pos[1] + dy))
