# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Portal import *
from EventSystem import *
from Math import *
from NPCs import *
from globals import *
from Generator import *


class Player(pygame.sprite.Sprite, Collidable, Damageable, MonoBehavior, Renderable):
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, need_collision_list=True)
        Damageable.__init__(self)
        MonoBehavior.__init__(self)
        Renderable.__init__(self, render_index=1)

        # Image related
        self.image = pygame.image.load(GamePath.player[0])
        self.image = pygame.transform.scale(
            self.image, (PlayerSettings.width, PlayerSettings.height)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Attribute related
        self.speed = PlayerSettings.speed
        self.coins = 0
        self.hp = PlayerSettings.hp
        self.attack = PlayerSettings.attack
        self.defence = PlayerSettings.defence
        # Fire related
        self.fire_cd = 0.5
        self.fire_timer = 0

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        self.rect.center = (x, y)

    def try_move(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update(self):
        self.handle_movement()
        self.handle_collisions()

    def handle_movement(self):
        keys = pygame.key.get_pressed()

        dx = dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        movement = Math.dot(Math.normalize((dx, dy)), self.speed)

        self.rect.move_ip(movement[0], movement[1])

    def handle_fire(self):
        if self.fire_timer > 0:
            self.fire_timer -= Time.delta_time
            return

        keys = pygame.key.get_pressed()

        dx = dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        velocity = Math.dot(Math.normalize((dx, dy)), ProjectileSettings.bulletSpeed)
        bullet = Generator.generate(GeneratableType.BULLET, velocity)

    def handle_damage(self, damage):
        damage = max(0, damage - self.defence)
        self.hp = max(0, self.hp - damage)
        EventSystem.fire_hurt_event(damage)

    def handle_collisions(self):
        for enter in self.collisions_enter:
            if isinstance(enter, Portal):
                EventSystem.fire_switch_event(enter.GOTO)
            if isinstance(enter, DialogNPC):
                EventSystem.fire_dialog_event("接触DialogNPC之后Event")
            """接触DialogNPC之后Event"""

        for stay in self.collisions_stay:
            if isinstance(stay, Monster):
                self.handle_damage(stay.attack)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect)
