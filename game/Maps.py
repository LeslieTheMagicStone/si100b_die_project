# -*- coding:utf-8 -*-

import pygame

import generator

from Settings import *
from random import random, randint

from Attributes import Renderable


class Block(pygame.sprite.Sprite, Renderable):
    def __init__(
        self,
        image,
        x=0,
        y=0,
        width=SceneSettings.tileWidth,
        height=SceneSettings.tileHeight,
    ):
        pygame.sprite.Sprite.__init__(self)
        Renderable.__init__(self, render_index=RenderIndex.block)

        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)


class TileMap(Renderable):
    def __init__(
        self,
        map: list[pygame.Surface],
        render_index=RenderIndex.tileMap,
        is_active=True,
        tile_width=SceneSettings.tileWidth,
        tile_height=SceneSettings.tileHeight,
    ):
        super().__init__(render_index, is_active)

        self.map = map
        self.tile_width = tile_width
        self.tile_height = tile_height

    def draw(self, window):
        if not self.is_active:
            return

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                window.blit(
                    self.map[i][j],
                    (self.tile_width * i, self.tile_height * j),
                )


# Generate a list of images for a tile map to draw
def gen_safety_room_map() -> list:
    block_images = [pygame.image.load(tile) for tile in GamePath.groundTiles]
    tile_width = SceneSettings.tileWidth
    tile_height = SceneSettings.tileHeight
    block_images = [
        pygame.transform.scale(image, (tile_width, tile_height))
        for image in block_images
    ]

    map_obj = []
    for i in range(SceneSettings.tileXnum):
        column = []
        for j in range(SceneSettings.tileYnum):
            column.append(block_images[randint(0, len(block_images) - 1)])
        map_obj.append(column)

    return map_obj


def gen_city_map():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_boss_map():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_city_obstacle():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_wild_obstacle():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_boss_obstacle():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####
