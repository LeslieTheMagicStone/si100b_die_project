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

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


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

    # Get the position of [top left, bottom right]
    def get_corners(self):
        # Add 1/2 to transfer center point to bottom right point
        tlx = -self.tile_width // 2
        tly = -self.tile_height // 2
        brx = int(self.tile_width * (len(self.map) - 1 / 2))
        bry = int(self.tile_height * (len(self.map[0]) - 1 / 2))
        return [(tlx, tly), (brx, bry)]

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        if not self.is_active:
            return

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                window.blit(
                    self.map[i][j],
                    (
                        self.tile_width * (i - 0.5) + dx,
                        self.tile_height * (j - 0.5) + dy,
                    ),
                )


# Generate a list of images for a tile map to draw
def gen_safe_room_map() -> TileMap:
    tile_images = [pygame.image.load(tile) for tile in GamePath.snowTiles]
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


# Generate walls around the given tiles
def gen_walls(corners) -> list[pygame.Surface]:
    [topleft, bottomright] = corners
    width = SceneSettings.tileWidth
    height = SceneSettings.tileHeight

    image = pygame.image.load(GamePath.cityWall)
    walls = []

    # Top
    for x in range(topleft[0] - width // 2, bottomright[0] + width // 2, width):
        y = topleft[1] - height // 2
        walls.append(Block(image, x, y, width, height))
    # Bottom
    for x in range(topleft[0] - width // 2, bottomright[0] + width // 2, width):
        y = bottomright[1] + height // 2
        walls.append(Block(image, x, y, width, height))
    # Left
    for y in range(topleft[1] - height // 2, bottomright[1] + height // 2 + 1, height):
        x = topleft[0] - width // 2
        walls.append(Block(image, x, y, width, height))
    # Right
    for y in range(topleft[1] - height // 2, bottomright[1] + height // 2 + 1, height):
        x = bottomright[0] + width // 2
        walls.append(Block(image, x, y, width, height))

    return walls


def gen_mob_room_map() -> TileMap:
    tile_images = [pygame.image.load(tile) for tile in GamePath.bossTiles]
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


def gen_Tool_room_map() -> TileMap:
    tile_images = [pygame.image.load(tile) for tile in GamePath.bossTiles]
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


def gen_boss_map():
    ##### Your Code Here ↓ #####
    pass
    ##### Your Code Here ↑ #####


def gen_safe_room_obstacles(rects_to_avoid: list[pygame.Rect]) -> list[Block]:
    image = pygame.image.load(GamePath.tree)

    obstacles = []
    tile_width = SceneSettings.tileWidth
    tile_height = SceneSettings.tileHeight

    # Obstacle will not generate around the rects to avoid
    # within the radius
    null_radius = 100

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
