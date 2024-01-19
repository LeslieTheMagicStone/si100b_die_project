# -*- coding:utf-8 -*-

import pygame

import generator


from Settings import *
from Attributes import *
from Portal import *
from EventSystem import *
from Math import *
from NPCs import *
from globals import *
from Projectiles import *
from UI import *


class Player(pygame.sprite.Sprite, Collidable, Damageable, MonoBehavior, Renderable):
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, need_collision_list=True, is_rigid=True)
        Damageable.__init__(self)
        MonoBehavior.__init__(self)
        Renderable.__init__(self, render_index=RenderIndex.player)

        # Animation related
        self.images = [
            pygame.transform.scale(
                pygame.image.load(path), (PlayerSettings.width, PlayerSettings.height)
            )
            for path in GamePath.player
        ]
        self.anim_interval_second = PlayerSettings.animIntervalSecond
        self.anim_frame = 0
        self.image = self.images[0]
        self.anim_timer = 0

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Scale the rect by 0.5x to make collision trigger more realistic
        resize_amount = [-self.rect.width // 2, -self.rect.height // 2]
        self.rect.inflate_ip(resize_amount[0], resize_amount[1])
        # Attribute related
        self.speed = PlayerSettings.speed
        self.coins = 0
        self.attack = PlayerSettings.attack
        self.defence = PlayerSettings.defence
        # Combat related
        self.max_hp = PlayerSettings.hp
        self.cur_hp = self.max_hp
        # Fire related
        self.fire_cd = 0.5
        self.fire_timer = 0

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        self.rect.center = (x, y)

    def update(self):
        self.handle_fire()
        self.handle_movement()
        self.handle_collisions()
        self.handle_animation()

    def handle_animation(self):
        # Only need to play run animation when running
        if self.velocity == (0, 0):
            self.image = self.images[2]
            return

        if self.anim_timer < 0:
            self.anim_timer = self.anim_interval_second
            self.anim_frame += 1
            self.anim_frame = min(self.anim_frame, self.anim_frame % len(self.images))
            self.image = self.images[self.anim_frame]

        self.anim_timer -= Time.delta_time

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

        velocity = Math.scale(Math.normalize((dx, dy)), self.speed)

        self.velocity = velocity

    def handle_fire(self):
        if self.fire_timer > 0:
            self.fire_timer -= Time.delta_time
            return

        keys = pygame.key.get_pressed()

        dx = dy = 0

        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1

        if (dx, dy) != (0, 0):
            bullet_velocity = Math.scale(
                Math.normalize((dx, dy)), ProjectileSettings.bulletSpeed
            )
            bullet = generator.generate(
                Bullet(self.rect.centerx, self.rect.centery, bullet_velocity)
            )

            self.fire_timer = self.fire_cd

    def handle_damage(self, damage):
        if self.is_invulnerable:
            return 0

        damage = max(0, damage - self.defence)
        self.cur_hp = max(0, self.cur_hp - damage)
        EventSystem.fire_hurt_event(damage)

        return damage

    def handle_collisions(self):
        for enter in self.collisions_enter:
            if isinstance(enter, Portal):
                if enter.GOTO != SceneManager.current_scene:
                    EventSystem.fire_switch_event(enter.GOTO)
            if isinstance(enter, DialogNPC):
                EventSystem.fire_dialog_event("接触DialogNPC之后Event")

        for stay in self.collisions_stay:
            if isinstance(stay, Monster):
                damage = self.handle_damage(stay.attack)
                EventSystem.fire_hurt_event(damage)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        # Calculate top-left corner of the picture separately
        # because that of the rect has been changed when scaling
        image_pos_x = self.rect.centerx - self.image.get_width() // 2 - 8 # tiny offset to look more realistic
        image_pos_y = self.rect.centery - self.image.get_height() // 2
        window.blit(self.image, (image_pos_x + dx, image_pos_y + dy))
