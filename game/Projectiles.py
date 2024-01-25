from typing import Any
import pygame
from Settings import *
from Math import *
from Attributes import *
from globals import Time
from EventSystem import *


class Projectile(pygame.sprite.Sprite, MonoBehavior, Renderable, Collidable):
    def __init__(
        self,
        x,
        y,
        render_index=RenderIndex.projectile,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        MonoBehavior.__init__(self)
        Renderable.__init__(self, render_index=render_index)
        Collidable.__init__(self)

        # All projectiles have a life time and will be destroyed after that
        self.life_time = 5

    def update(self):
        self.life_time -= Time.delta_time
        if self.life_time < 0:
            EventSystem.fire_destroy_event(self)


class Tools(Projectile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.need_collision_list = True

        self.image = pygame.image.load(GamePath.player[0])
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth // 4, SceneSettings.tileHeight // 4)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 0

    def update(self):
        super().update()

        for other in self.collisions_enter:
            if other.layer == "Player":
                EventSystem.fire_destroy_event(self)
                EventSystem.fire_dialog_event(self, "这是一个古老的面具，上面蕴藏着神秘的力量，可以让玩家拥有转换能力")

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class Bullet(Projectile):
    def __init__(
        self, x, y, velocity, damage=ProjectileSettings.bulletDamage, attribute=Causality.NORMAL
    ) -> None:
        super().__init__(x, y)
        self.need_collision_list = True

        self.image = pygame.image.load(GamePath.player[0])
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth // 4, SceneSettings.tileHeight // 4)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocity = velocity
        self.damage = damage
        self.attribute = attribute

    def update(self):
        super().update()

        # Collide rigid ones then destroy it self
        for other in self.collisions_enter:
            if other.is_rigid and other.layer != "Player":
                self.set_active(False)
                EventSystem.fire_destroy_event(self)
                if other.layer == "Default":
                    EventSystem.fire_hit_event(0, self.rect.center)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class Big_bullet(Bullet):
    def __init__(
        self, x, y, velocity, damage=ProjectileSettings.bulletDamage * 4
    ) -> None:
        super().__init__(x, y, velocity, damage)

        self.image = pygame.image.load(GamePath.player[0])
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth // 2, SceneSettings.tileHeight // 2)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocity = velocity
        self.damage = damage

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


"""Laser通过普通子弹在循环中生成连续的多个子弹传实现"""
