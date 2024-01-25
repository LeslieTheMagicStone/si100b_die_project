# -*- coding:utf-8 -*-

import pygame
import generator

from Settings import *
from Attributes import *
from Math import *
from EventSystem import *
from Projectiles import *
from UI import *
from random import randint


class NPC(pygame.sprite.Sprite, Collidable, Renderable, MonoBehavior):
    def __init__(self, x, y, name, render_index=RenderIndex.npc):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, is_rigid=True)
        Renderable.__init__(self, render_index)
        MonoBehavior.__init__(self)

        self.image: pygame.Surface = None
        self.rect: pygame.Rect = None

    def update(self):
        raise NotImplementedError

    def reset_talkCD(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class Monster(NPC, Damageable):
    def __init__(
        self,
        player_rect: pygame.Rect,
        x,
        y,
        speed=4,
        hp=10,
        attack=3,
        defence=1,
        money=15,
    ):
        NPC.__init__(self, x, y, name="Monster", render_index=RenderIndex.monster)
        Damageable.__init__(self)

        # Collision Layer is enemy
        self.layer = "Enemy"
        # Need collision list to detect hurt
        self.need_collision_list = True
        # Image and rect related
        self.image = pygame.image.load(GamePath.monster)
        self.image = pygame.transform.scale(
            self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Save player position
        self.player_rect = player_rect
        # Attribute related
        self.speed = speed
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.money = money
        # Combat related
        self.is_dead = False
        self.cur_hp = self.max_hp

    def start(self):
        # Init health bar
        self.health_bar = HealthBar(self, self.rect)
        generator.generate(self.health_bar)

    def update(self):
        if self.is_dead:
            return

        self.handle_movement()
        self.handle_collisions()

    def handle_movement(self):
        # Straightly moves towards the player
        dir = (self.player_rect.x - self.rect.x, self.player_rect.y - self.rect.y)
        movement = Math.round(Math.scale(Math.normalize(dir), self.speed))
        self.velocity = (movement[0], movement[1])

    def handle_damage(self, damage):
        damage = max(1, damage - self.defence)
        self.cur_hp = max(0, self.cur_hp - damage)

        if self.cur_hp == 0:
            self.handle_death()

        return damage

    def handle_death(self):
        EventSystem.fire_destroy_event(self.health_bar)
        EventSystem.fire_destroy_event(self)

    def handle_collisions(self):
        # if len(self.collisions_enter) != 0:
        #     print("enter", self.collisions_enter, self.velocity)
        # if len(self.collisions_stay) != 0:
        #     print("stay", self.collisions_stay, self.velocity)
        # if len(self.collisions_exit) != 0:
        #     print("exit", self.collisions_exit, self.velocity)
        for enter in self.collisions_enter:
            if isinstance(enter, Projectile):
                if isinstance(enter, Bullet):
                    damage = self.handle_damage(enter.damage)
                    # Generate random offset of the hit point to make the game juicier
                    ortho_normal = Math.ortho_normal(enter.velocity)
                    random_offset = Math.scale(ortho_normal, randint(-20, 20))
                    EventSystem.fire_hit_event(
                        damage, Math.add(random_offset, enter.rect.center)
                    )
                    EventSystem.fire_destroy_event(enter)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def draw(self, window, dx=0, dy=0):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
