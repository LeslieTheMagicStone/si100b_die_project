# -*- coding:utf-8 -*-

import sys
import pygame

from Player import Player
from Scenes import *
from Settings import *
from SceneTransferData import *
from Effects import EffectManager


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
        self.player.reset_pos()

        # Initialize scenes
        self.scenes: List[Scene] = []
        self.scenes.append(MainMenuScene(self.pack_scene_transfer_data("Main Menu")))
        self.scenes.append(SafeRoomScene(self.pack_scene_transfer_data("Safe Room")))
        self.scenes.append(MobRoomScene(self.pack_scene_transfer_data("Mob Room")))

        # Default scene is main menu
        self.flush_scene("Main Menu")

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
                # Private scene instance
                self.scene: Scene = self.scenes[GOTO]
                # Global scene name
                SceneManager.current_scene = self.scene.name
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

        # Handle event
        self.handle_event()

        # Call update function of current game state
        self.scene.update()

    def handle_event(self):
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
                # Append object to the scene object list
                scene = event.message[1]
                # Default Scene is current scene
                if scene is None:
                    scene = self.scene
                scene.append_object(event.message[0])
            elif event.type == GameEvent.EVENT_DIALOG:
                self.scene.show_dialog_box(event.message)
            elif event.type == GameEvent.EVENT_DESTROY:
                # Append object to the scene object list
                scene = event.message[1]
                # Default Scene is current scene
                if scene is None:
                    scene = self.scene
                scene.remove_object(event.message[0])
            elif event.type == GameEvent.EVENT_HIT:
                # Generate smoke animation
                damage = event.message[0]
                position = event.message[1]
                EffectManager.generate(f"text: {damage}", position[0], position[1])
                EffectManager.generate("smoke", position[0], position[1])

    def pack_scene_transfer_data(self, name) -> SceneTransferData:
        return SceneTransferData(player=self.player, window=self.window, name=name)

    def render(self):
        self.scene.render()
