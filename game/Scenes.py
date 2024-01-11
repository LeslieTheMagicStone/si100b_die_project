# -*- coding:utf-8 -*-

import pygame
import Maps
from random import randint

from enum import Enum
from Settings import *
from NPCs import *
from PopUpBox import *
from Portal import *
from BgmPlayer import *
from Player import *
from SceneTransferData import *
from EventSystem import *
from Math import *
from Projectiles import *


class Scene:
    def __init__(self, data: SceneTransferData):
        self.window = data.window
        self.player = data.player
        self.name = data.name
        self.dialogbox = data.dialogbox
        # List of all game objects in the scene
        self._objects: list[object] = []
        # List of all collidables in the scene
        self._collidables: list[Collidable] = []
        # List of all mono behaviors in the scene
        self._mono_behaviors: list[MonoBehavior] = []
        # List of all renderables
        self._renderables: list[Renderable] = []

        # Append player to the scene object list
        self.append_object(self.player)

    # Start function called each time the scene is entered
    def start(self):
        pass

    # Update function called once per frame
    def update(self):
        # Update collision lists of the collidables
        self.update_collision()
        # Call update functions of mono behaviours
        for mb in self._mono_behaviors:
            mb.update()

    def update_collision(self):
        for collidable in self._collidables:
            # Only need to update those collidables which need collision list
            if not collidable.need_collision_list:
                continue

            # Clear all objects in exit list
            collidable.collisions_exit = []

            # Update stay list (of last frame)
            for other in collidable.collisions_stay:
                if not collidable.rect.colliderect(other):
                    collidable.collisions_stay.remove(other)
                    collidable.collisions_exit.append(other)

            # Update enter list (of last frame)
            for other in collidable.collisions_enter:
                collidable.collisions_enter.remove(other)
                if collidable.rect.colliderect(other):
                    collidable.collisions_stay.append(other)
                else:
                    collidable.collisions_exit.append(other)
            # Check new collision enters (of this frame)
            for other in self._collidables:
                if other.rect.colliderect(collidable.rect):
                    if other not in collidable.collisions_stay:
                        collidable.collisions_enter.append(other)

    # Append object to scene object list
    def append_object(self, obj):
        self._objects.append(obj)

        if isinstance(obj, Collidable):
            self._collidables.append(obj)
        if isinstance(obj, MonoBehavior):
            self._mono_behaviors.append(obj)
        if isinstance(obj, Renderable):
            self._renderables.append(obj)

    # Sort renderables from the lowest index to the highest
    def sort_renderables(self):
        self._renderables = sorted(self._renderables, key=lambda x: x.render_index)

    def update_camera(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def render(self):
        self.sort_renderables()

        for renderable in self._renderables:
            renderable.draw(self.window)

    def draw_dialogbox(self):
        self.append_object(self.dialogbox)


class MainMenuScene(Scene):
    def start(self):
        self.player_image = pygame.image.load(GamePath.player[0])
        self.icon_rect = self.player_image.get_rect()

    def update(self):
        super().update()
        # A warm-up mini game,
        # where you have to click the icon to start the main game.
        self.icon_rect = self.icon_rect.move(10, 0)
        # Check if player clicks the icon, if so, GOTO first scene.
        mouse = pygame.mouse
        if mouse.get_pressed()[0] and self.icon_rect.collidepoint(mouse.get_pos()):
            EventSystem.fire_switch_event(1)

    def render(self):
        # Fill the background with black
        background_color = (0, 0, 0)
        self.window.fill(background_color)
        # Render the character
        self.window.blit(self.player_image, self.icon_rect)


class SafeRoomScene(Scene):
    def start(self):
        self.player.reset_pos()
        # Init portals
        self.append_object(Portal(123, 123, "Mob Room"))

    def render(self):
        # Fill the background with black
        background_color = (1, 1, 1)
        self.window.fill(background_color)
        # Render renderable objects
        super().render()


class MobRoomScene(Scene):
    def start(self):
        self.player.reset_pos()

        # Init monsters, TODO: use generator to do this
        self.monster = Monster(self.player.rect, 10, 10)
        self.append_object(self.monster)

    def update(self):
        super().update()

        # DEBUG: print params
        print(self._renderables)

    def render(self):
        # Render background with black
        background_color = (0, 0, 0)
        self.window.fill(background_color)
        # Render renderable objects
        super().render()


class ToolRoomScence(Scene):
    """append_object(self.dialogNPC)"""

    pass
