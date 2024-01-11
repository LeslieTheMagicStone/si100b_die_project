# -*- coding:utf-8 -*-

import sys
import pygame

from Player import Player
from Scenes import *
from Settings import *
from PopUpBox import *
from SceneTransferData import *


class GameManager:
    def __init__(self):
        # Initialize clock
        self.clock = pygame.time.Clock()
        # Time scale used for pause or speeding
        self.time_scale = 1
        # Initialize game window
        self.window = pygame.display.set_mode(
            (WindowSettings.width, WindowSettings.height)
        )
        pygame.display.set_caption(WindowSettings.name)

        # Initialize player
        self.player = Player(0, 0)

        # Initialize scenes
        self.scenes: List[Scene] = []
        self.scenes.append(MainMenuScene(self.pack_scene_transfer_data("Main Menu")))
        self.scenes.append(SafeRoomScene(self.pack_scene_transfer_data("Safe Room")))
        self.scenes.append(MobRoomScene(self.pack_scene_transfer_data("Mob Room")))

        # Default scene is main menu
        self.flush_scene("Mob Room")

    def game_reset(self):
        # TODO reset the scenes

        self.flush_scene("Main Menu")

    """ Necessary game components """

    def tick(self, fps):
        Time.delta_time = self.clock.tick(fps) / 1000
        Time.time += Time.delta_time * self.time_scale

    def get_time(self):
        return pygame.time.get_ticks() / 1000

    """ Scene-related update functions """

    def flush_scene(self, GOTO):
        if isinstance(GOTO, str):
            self.flush_scene(self.get_scene_index(GOTO))
        elif isinstance(GOTO, int):
            if 0 <= GOTO < len(self.scenes):
                self.scene: Scene = self.scenes[GOTO]
                self.scene.start()
                self.game_state = GameState.GAME_PLAY
                pygame.display.set_caption(f"{WindowSettings.name} - {self.scene.name}")
            else:
                raise IndexError(f"Scene index: {GOTO} out of range")

    def get_scene_index(self, name: str):
        for index, scene in enumerate(self.scenes):
            if scene.name == name:
                return index

        raise NameError(f"Scene name: {name} not found")

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
            elif event.type == GameEvent.EVENT_SWITCH:
                self.flush_scene(event.message)
            elif event.type == GameEvent.EVENT_GENERATE:
                self.scene.append_object(event.message)

        # Call update function of current game state
        self.scene.update()

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

    """ Rendering-related update functions """

    def pack_scene_transfer_data(self, name) -> SceneTransferData:
        return SceneTransferData(player=self.player, window=self.window, name=name)

    def render(self):
        self.scene.render()

    def text_one(self):
        pass
