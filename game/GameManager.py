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

        self.game_reset()

    def game_reset(self):
        # Reset BGM Player
        BgmPlayer.set_volume(1)
        # Reset Sound Player
        SoundPlayer.reset()
        # Initialize player
        self.player = Player(0, 0)
        self.player.reset_pos()

        # Initialize scenes
        self.scenes: list[Scene] = []
       
        self.scenes.append(MainMenuScene(self.pack_scene_transfer_data("Main Menu")))
        
        self.scenes.append(SafeRoomScene(self.pack_scene_transfer_data("Safe Room")))
        
        self.scenes.append(
            MobRoomScene(self.pack_scene_transfer_data("Mob Room"), 5, 1)
        )
        self.scenes.append(ToolRoomScence(self.pack_scene_transfer_data("Tool Room")))
        self.scenes.append(
            MobRoomScene(self.pack_scene_transfer_data("Another Mob Room"), 6, 3)
        )
        self.scenes.append(
            MobRoomScene(self.pack_scene_transfer_data("Mob Room 3"), 8, 10)
        )
        self.scenes.append(
            MobRoomScene(self.pack_scene_transfer_data("Why So Many Mob Rooms?"), 8, 12)
        )
        self.scenes.append(
            BossRoomScene(self.pack_scene_transfer_data("FINALE: THE BOSS"))
        )
        self.scenes.append(
            InfiniteMobRoomScene(self.pack_scene_transfer_data("Infinite Mob Room"))
        )

        # Default scene is main menu
        self.flush_scene("Main Menu")

    """ Necessary game components """

    def tick(self, fps):
        Time.delta_time = self.clock.tick(fps) / 1000
        Time.time += Time.delta_time * self.time_scale

    def get_time(self):
        return pygame.time.get_ticks() / 1000

    """ Scene-related update functions """

    def flush_scene(self, GOTO):
        if GOTO == "next":
            self.flush_scene(self.get_scene_index(self.scene.name) + 1)
        elif GOTO == "last":
            self.flush_scene(self.get_scene_index(self.scene.name) - 1)
        elif isinstance(GOTO, str):
            self.flush_scene(self.get_scene_index(GOTO))
        elif isinstance(GOTO, int):
            if 0 <= GOTO < len(self.scenes):
                # Private scene instance
                self.scene: Scene = self.scenes[GOTO]
                # Global scene name
                SceneManager.current_scene = self.scene.name
                CurrentState.state = GameState.NORMAL
                self.scene.start()
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

        # Update key_down
        for key in Input.key_down:
            Input.key_down[key] = False
        # Handle event several times to fetch all events
        # (I know it seems dirty, but it works)
        for i in range(20):
            self.handle_events()

        # Call update function of current game state
        self.scene.update()

        if Input.get_key(pygame.K_LSHIFT):
            self.time_scale = 2
        else:
            self.time_scale = 1

    def handle_events(self):
        # Get events of current frame
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                # No need to sys.exit(), right?
            elif event.type == pygame.KEYDOWN:
                Input.key_down[event.key] = True
                Input.key_pressed[event.key] = True
            elif event.type == pygame.KEYUP:
                # Reset the key state when the key is released
                Input.key_down[event.key] = False
                Input.key_pressed[event.key] = False
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
                CurrentState.state = GameState.DIALOG
                self.scene.show_dialog_box(event.portrait, event.text, event.callback)
            elif event.type == GameEvent.EVENT_SHOP:
                CurrentState.state = GameState.DIALOG
                self.scene.show_shop_box(event.portrait, event.items, event.callback)
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
                if damage > 0:
                    EffectManager.generate(f"text: {damage}", position[0], position[1])
                EffectManager.generate("smoke", position[0], position[1])
            elif event.type == GameEvent.EVENT_BUFF:
                # Add buff to player
                self.player.add_buff(event.buff_name, event.buff_time)
            elif event.type == GameEvent.EVENT_GAME_OVER:
                # Set current gamestate to gameover
                CurrentState.state = GameState.GAME_OVER

    def pack_scene_transfer_data(self, name) -> SceneTransferData:
        return SceneTransferData(player=self.player, window=self.window, name=name)

    def render(self):
        self.scene.render()
