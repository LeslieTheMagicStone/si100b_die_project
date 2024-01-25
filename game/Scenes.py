# -*- coding:utf-8 -*-

import pygame
import Maps
from random import randint
from SceneTransferData import SceneTransferData

import generator

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
from Maps import *
from UI import *
from Effects import EffectManager


class Scene:
    def __init__(self, data: SceneTransferData):
        self.window = data.window
        self.player = data.player
        self.name = data.name
        # List of all game objects in the scene
        self._objects: list[object] = []
        # List of all collidables in the scene
        self._collidables: list[Collidable] = []
        # List of all mono behaviors in the scene
        self._mono_behaviors: list[MonoBehavior] = []
        # List of all renderables
        self._renderables: list[Renderable] = []
        # List of all portals
        self._portals: list[Portal] = []

        # Initialize a global dialog box
        self.dialog_box = DialogBox()
        self.hide_dialog_box()

        # Initialize game camera
        self.camera = pygame.Rect((0, 0), self.window.get_size())

        # Append player to the scene object list
        self.append_object(self.player)

        # Append player health bar
        self.health_bar = generator.generate(
            HealthBar(self.player, self.player.rect, dy=20), self
        )
        self.append_object(self.health_bar)

    # Start function called each time the scene is entered
    def start(self):
        pass

    # Update function called once per frame
    def update(self):
        # Call start/update functions of mono behaviours
        self.update_mono_behaviors()

        # Update collision lists of the collidables
        self.update_collision_list()

        # Update movement of collidables with velocity
        self.update_velocity_movement()

        # Update game camera at last to assure smooth cam movement
        self.update_camera(self.player)

    # Update the collision list of the collidables needing it
    def update_collision_list(self):
        # Assume they all move without bumping into others
        for c in self._collidables:
            (dx, dy) = c.velocity
            c.rect.move_ip(2 * dx, 2 * dy)

        for c in self._collidables:
            # Only need to update those collidables which need collision list
            if not c.need_collision_list:
                continue

            # Clear all objects in exit list
            c.collisions_exit = []

            # Update stay list (of last frame)
            for other in c.collisions_stay:
                if not c.rect.colliderect(other):
                    c.collisions_stay.remove(other)
                    c.collisions_exit.append(other)

            # Update enter list (of last frame)
            for other in c.collisions_enter:
                c.collisions_enter.remove(other)
                if c.rect.colliderect(other):
                    c.collisions_stay.append(other)
                else:
                    c.collisions_exit.append(other)
            # Check new collision enters (of this frame)
            for other in self._collidables:
                # Of course collision of itself does not count
                if other is c:
                    continue

                if other.rect.colliderect(c.rect):
                    if other not in c.collisions_stay:
                        c.collisions_enter.append(other)

        # Don't forget to set the position back to original
        for c in self._collidables:
            (dx, dy) = c.velocity
            c.rect.move_ip(-2 * dx, -2 * dy)

    # Call start/update functions of mono behaviours
    def update_mono_behaviors(self):
        for mb in self._mono_behaviors:
            if not mb.start_called:
                mb.start()
                mb.start_called = True
            else:
                mb.update()

    # Update the movement of the collidables with velocity,
    # avoiding collisions between rigid ones
    def update_velocity_movement(self):
        for c in self._collidables:
            # Only need to update collidables with velocity
            if c.velocity == (0, 0):
                continue

            dx = c.velocity[0]
            dy = c.velocity[1]

            target_pos_x = c.rect.move(dx, 0)
            target_pos_y = c.rect.move(0, dy)

            # Only need to detect collisions between rigid collidables
            if c.is_rigid:
                for other in self._collidables:
                    if other is not c and other.is_rigid:
                        # Avoid x and y movement separately
                        # to get smoother movement
                        if other.rect.colliderect(target_pos_x):
                            dx = 0

                        if other.rect.colliderect(target_pos_y):
                            dy = 0

            # Finally, update movement based on velocity
            c.rect.move_ip(dx, dy)

            # Also updates velocity
            c.velocity = (dx, dy)

    # Append object to scene object list
    def append_object(self, obj):
        self._objects.append(obj)

        if isinstance(obj, Collidable):
            self._collidables.append(obj)
        if isinstance(obj, MonoBehavior):
            self._mono_behaviors.append(obj)
        if isinstance(obj, Renderable):
            self._renderables.append(obj)
        if isinstance(obj, Portal):
            self._portals.append(obj)

    # Remove object from scene object list
    def remove_object(self, obj):
        if obj not in self._objects:
            return

        self._objects.remove(obj)

        if isinstance(obj, Collidable):
            self._collidables.remove(obj)
        if isinstance(obj, MonoBehavior):
            self._mono_behaviors.remove(obj)
        if isinstance(obj, Renderable):
            self._renderables.remove(obj)
        if isinstance(obj, Portal):
            self._portals.remove(obj)

    # Sort renderables from the lowest index to the highest
    def sort_renderables(self):
        self._renderables = sorted(self._renderables, key=lambda x: x.render_index)

    def update_camera(self, player: Collidable):
        self.camera.move_ip(player.velocity[0], player.velocity[1])

    #  Get the offset to be added to the position of the renderables when rendered
    def get_render_offset(self):
        dx = -self.camera.x
        dy = -self.camera.y
        return (dx, dy)

    def render(self):
        self.sort_renderables()

        offset = self.get_render_offset()
        for renderable in self._renderables:
            renderable.draw(self.window, offset[0], offset[1])

    def show_dialog_box(self, message):
        npc = message[0]
        text = message[1]

        self.dialog_box.set_npc(npc)
        self.dialog_box.set_text(text)
        self.dialog_box.set_active(True)

    def hide_dialog_box(self):
        self.dialog_box.set_active(False)


class MainMenuScene(Scene):
    def start(self):
        self.images = [
            pygame.image.load(
                r".\assets\main_menu\niu_niu\frame_"
                + "{:02d}".format(i)
                + "_delay-0.04s.gif"
            )
            for i in range(0, 75)
        ]
        self.images = [
            pygame.transform.scale(image, (120, 120)) for image in self.images
        ]
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.move_right = 1
        self.move_down = 1

    def update(self):
        super().update()
        # A warm-up mini game,
        # where you have to click the icon to start the main game.
        self.rect.move_ip(20 * self.move_right, 0)
        # The icon run repeatedly between left and right
        if self.rect.right > WindowSettings.width or self.rect.left < 0:
            self.move_right *= -1
            self.rect.move_ip(0, self.move_down * 75)
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)

        if self.rect.bottom > WindowSettings.height or self.rect.top < 0:
            self.move_down *= -1
            self.rect.move_ip(0, self.move_down * 75)
            self.image = pygame.transform.flip(self.image, flip_x=False, flip_y=True)

        # Check if player clicks the icon, if so, GOTO first scene.
        mouse = pygame.mouse
        if mouse.get_pressed()[0] and self.rect.collidepoint(mouse.get_pos()):
            EventSystem.fire_switch_event(1)

    def render(self):
        # Fill the background with black
        background_color = (0, 0, 0)
        self.window.fill(background_color)
        # Render the character
        # Handle animation
        self.frame = (self.frame + 1) % len(self.images)
        self.image = self.images[self.frame]
        self.window.blit(self.image, self.rect)


class SafeRoomScene(Scene):
    def __init__(self, data: SceneTransferData):
        super().__init__(data)

        # Init tile map
        tile_map = Maps.gen_safe_room_map()
        self.tile_map = generator.generate(tile_map, scene=self)

        # Init portals
        generator.generate(Portal(123, 123, "Mob Room"), scene=self)

        # Init obstacles
        rects_to_avoid = [portal.rect for portal in self._portals] + [self.player.rect]
        self.obstacles = Maps.gen_safe_room_obstacles(rects_to_avoid)
        for obstacle in self.obstacles:
            generator.generate(obstacle, scene=self)

        # Init walls
        self.walls = Maps.gen_walls(self.tile_map.get_corners())
        for wall in self.walls:
            generator.generate(wall, scene=self)

    def start(self):
        super().start()
        self.player.reset_pos()

        # Generate teleport anim
        EffectManager.generate(
            "teleport", self.player.rect.centerx, self.player.rect.centery - 20
        )

    def render(self):
        # Fill the background with black
        background_color = (1, 1, 1)
        self.window.fill(background_color)
        # Render renderable objects
        super().render()


class MobRoomScene(Scene):
    def __init__(self, data: SceneTransferData):
        super().__init__(data)

        # Init tile map
        tile_map = Maps.gen_mob_room_map()
        self.tile_map = generator.generate(tile_map, scene=self)

        # Init monsters
        monster = Monster(self.player.rect, 100, 100)
        generator.generate(monster, scene=self)

        # Init walls
        self.walls = Maps.gen_walls(self.tile_map.get_corners())
        for wall in self.walls:
            generator.generate(wall, scene=self)

        # Init monsters
        monster_count = randint(5, 10)
        for i in range(monster_count):
            [(left, top), (right, bottom)] = self.tile_map.get_corners()
            x = randint(left + 50, right - 50)
            y = randint(top + 50, bottom - 50)
            causality = Causality(randint(1, 2))
            monster = Monster(self.player.rect, x, y, causality=causality)
            generator.generate(monster, scene=self)

    def start(self):
        super().start()
        self.player.reset_pos()

        # Generate teleport anim
        EffectManager.generate(
            "teleport", self.player.rect.centerx, self.player.rect.centery - 20
        )

    def update(self):
        super().update()

    def render(self):
        # Render background with black
        background_color = (0, 0, 0)
        self.window.fill(background_color)
        # Render renderable objects
        super().render()


class ToolRoomScence(Scene):
    """append_object(self.dialogNPC)"""

    def start(self):
        super().start()
        self.player.reset_pos()

        self.dialogNPC = DialogNPC(self.player)
