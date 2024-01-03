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


class Scene:
    def __init__(self, window: pygame.Surface):
        ##### Your Code Here ↓ #####
        self.window = window
        ##### Your Code Here ↑ #####

    # Start function called each time the scene is entered
    def start(self):
        pass

    # Update function called once per frame
    def update(self):
        pass

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
    def __init__(self, window: pygame.Surface):
        super().__init__(window)

    def start(self):
        self.player_image = pygame.image.load(GamePath.player[0])
        self.icon_rect = self.player_image.get_rect()

    def update(self):
        # A warm-up mini game,
        # where you have to click the icon to start the main game.
        self.icon_rect = self.icon_rect.move(10, 0)
        # Check if player clicks the icon
        mouse = pygame.mouse
        if mouse.get_pressed()[0] and self.icon_rect.collidepoint(mouse.get_pos()):
            restart_event = pygame.event.Event(GameEvent.EVENT_RESTART)
            pygame.event.post(restart_event)

    def render(self):
        # Fill the background with black
        background_color = (0, 0, 0)
        self.window.fill(background_color)
        # Render the character
        self.window.blit(self.player_image, self.icon_rect)


class CityScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def gen_CITY(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####


class WildScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def gen_WILD(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def gen_monsters(self, num=10):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####


class BossScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Overwrite Scene's function
    def trigger_battle(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def gen_BOSS(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
