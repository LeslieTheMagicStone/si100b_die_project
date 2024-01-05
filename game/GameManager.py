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
        # Initialize game window
        self.window = pygame.display.set_mode(
            (WindowSettings.width, WindowSettings.height)
        )
        pygame.display.set_caption(WindowSettings.name)

        # Initialize player, todo
        self.player = None

        # Initialize scenes
        self.scenes: Dict[SceneIndex:Scene] = {}
        self.scenes[SceneIndex.MAIN_MENU] = MainMenuScene(self.pack_scene_transfer_data())
        self.scenes[SceneIndex.DEMO] = DemoScene(self.pack_scene_transfer_data())

        # Default scene is main menu
        self.flush_scene(SceneIndex.MAIN_MENU)

    def game_reset(self):
        # TODO reset the scenes

        self.flush_scene(SceneIndex.DEMO)

    """ Necessary game components """

    def tick(self, fps):
        self.clock.tick(fps)

    def get_time(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    """ Scene-related update functions """

    def flush_scene(self, GOTO: SceneIndex):
        if GOTO in self.scenes.keys():
            self.scene: Scene = self.scenes[GOTO]
            self.scene.start()
            self.game_state = GameState.GAME_PLAY
        else:
            raise NotImplementedError(
                f"The game scene: {GOTO.name} is not implemented yet."
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

    def pack_scene_transfer_data(self) -> SceneTransferData:
        return SceneTransferData(player=self.player, window=self.window)

    def render(self):
        self.scene.render()
