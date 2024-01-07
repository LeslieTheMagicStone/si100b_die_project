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


class Scene:
    def __init__(self, data: SceneTransferData):
        self.window = data.window
        self.player = data.player
        self.name = data.name

        self.portals: list[Portal] = []

    # Start function called each time the scene is entered
    def start(self):
        pass

    # Update function called once per frame
    def update(self):
        pass

    def update_collision(self):
        # Clear all objects in exit list
        self.player.collisions_exit = []

        # Update stay list
        for other in self.player.collisions_stay:
            if not self.player.rect.colliderect(other):
                self.player.collisions_stay.remove(other)
                self.player.collisions_exit.append(other)

        # Update enter list
        for other in self.player.collisions_enter:
            self.player.collisions_enter.remove(other)
            if self.player.rect.colliderect(other):
                self.player.collisions_stay.append(other)
            else:
                self.player.collisions_exit.append(other)
        # Check portal collision
        for portal in self.portals:
            if portal.rect.colliderect(self.player.rect):
                if portal not in self.player.collisions_stay:
                    self.player.collisions_enter.append(portal)
            

    def trigger_dialog(self, npc):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_dialog(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def trigger_battle(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_battle(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def trigger_shop(self, npc, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_shop(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_camera(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def render(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####


class MainMenuScene(Scene):
    def start(self):
        self.player_image = pygame.image.load(GamePath.player[0])
        self.icon_rect = self.player_image.get_rect()

    def update(self):
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
        self.portals.append(Portal(123, 123, "Mob Room"))

    def update(self):
        self.update_collision()
        self.player.update()

    def render(self):
        # Fill the background with black
        background_color = (1, 1, 1)
        self.window.fill(background_color)
        # Render player
        self.player.draw(self.window)
        # Render portal
        for portal in self.portals:
            portal.draw(self.window)


class MobRoomScene(Scene):
    def start(self):
        self.player.reset_pos()

    def update(self):
        self.update_collision()
        self.player.update()

    def render(self):
        background_color = (0, 0, 0)
        self.window.fill(background_color)
        self.player.draw(self.window)
