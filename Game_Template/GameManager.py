# -*- coding:utf-8 -*-

import sys
import pygame

from Player import Player
from Scenes import *
from Settings import *
from PopUpBox import *


class GameManager:
    def __init__(self):
        # Initialize clock
        self.clock = pygame.time.Clock()
        # Initialize game window
        self.window = pygame.display.set_mode(
            (WindowSettings.width, WindowSettings.height)
        )
        pygame.display.set_caption(WindowSettings.name)

        # Initialize scenes
        # (Currently each scene is initialized each time it is entered)

        # Default scene is main menu
        self.flush_scene(SceneIndex.MAIN_MENU)

    def game_reset(self):
        # TODO reset the scenes

        self.flush_scene(SceneIndex.MAIN_MENU)

    """ Necessary game components """

    def tick(self, fps):
        self.clock.tick(fps)

    def get_time(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    """ Scene-related update functions """

    def flush_scene(self, GOTO: SceneIndex):
        if GOTO == SceneIndex.MAIN_MENU:
            self.main_menu_scene = MainMenuScene(self.window)
            self.main_menu_scene.start()
            self.game_state = GameState.GAME_MAIN_MENU
        elif GOTO == SceneIndex.CITY:
            self.city_scene = CityScene(self.window)
            self.city_scene.start()
            self.game_state = GameState.GAME_PLAY_CITY
        else:
            raise NotImplementedError(
                f"The update function of game state: {self.game_state.name} is not implemented yet."
            )

    # Update function called once per frame
    def update(self):
        # Wait for delta time between each frame
        self.tick(30)

        # Get events of current frame
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                # No need to sys.exit(), right?
            elif event.type == GameEvent.EVENT_RESTART:
                self.game_reset()

        # Call update function of current game state
        if self.game_state == GameState.GAME_MAIN_MENU:
            self.main_menu_scene.update()
        if self.game_state == GameState.GAME_PLAY_CITY:
            self.city_scene.update()

    # Collision-relate update funtions here ↓
    def update_collide(self):
        # Player -> Obstacles
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> NPCs; if multiple NPCs collided, only first is accepted and dealt with.
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> Monsters
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> Portals
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> Boss
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_NPCs(self):
        # This is not necessary. If you want to re-use your code you can realize this.
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    """ Rendering-related update functions """

    def render(self):
        if self.game_state == GameState.GAME_MAIN_MENU:
            self.main_menu_scene.render()
        elif self.game_state == GameState.GAME_PLAY_CITY:
            self.city_scene.render()
        else:
            raise NotImplementedError(
                f"The render function of game state: {self.game_state.name} is not implemented yet."
            )
