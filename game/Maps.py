# -*- coding:utf-8 -*-

import pygame

import generator

from Settings import *
from random import random, randint
from Math import *

from Attributes import Renderable, Collidable


class Block(pygame.sprite.Sprite, Renderable, Collidable):
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
        Collidable.__init__(self, is_rigid=True)

        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, window: pygame.Surface):
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
        Renderable.__init__(self, render_index, is_active)

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
def gen_safe_room_map() -> TileMap:
    tile_images = [pygame.image.load(tile) for tile in GamePath.groundTiles]
    tile_width = SceneSettings.tileWidth
    tile_height = SceneSettings.tileHeight
    tile_images = [
        pygame.transform.scale(image, (tile_width, tile_height))
        for image in tile_images
    ]

    map_obj = []
    for i in range(SceneSettings.tileXnum):
        column = []
        for j in range(SceneSettings.tileYnum):
            column.append(tile_images[randint(0, len(tile_images) - 1)])
        map_obj.append(column)

    return TileMap(map_obj)


def gen_city_map():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_boss_map():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_safe_room_obstacles(rects_to_avoid: list[pygame.Rect]) -> list[pygame.Surface]:
    image = pygame.image.load(GamePath.tree)

    obstacles = []
    tile_width = SceneSettings.tileWidth
    tile_height = SceneSettings.tileHeight

    # Obstacle will not generate around the rects to avoid
    # within the radius
    null_radius = 100

    for item in rects_to_avoid:
        print(item.center)

    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            tile_pos = (tile_width * i, tile_height * j)
            # Avoid generating around the rects to avoid
            if random() < SceneSettings.obstacleDensity and all(
                Math.distance(rect.center, tile_pos) > null_radius
                for rect in rects_to_avoid
            ):
                obstacles.append(
                    Block(image, tile_pos[0], tile_pos[1], tile_width, tile_height)
                )
    return obstacles


def gen_wild_obstacle():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_boss_obstacle():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####
