from typing import Any
import pygame
from Settings import *
from Math import *
from Attributes import *


class Projectile(pygame.sprite.Sprite, MonoBehavior, Renderable, Collidable):
    def __init__(self, x, y, render_index=RenderIndex.projectile) -> None:
        pygame.sprite.Sprite.__init__(self)
        MonoBehavior.__init__(self)
        Renderable.__init__(self, render_index=render_index)
        Collidable.__init__(self)

        self.image = pygame.image.load(GamePath.player[0])
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth // 4, SceneSettings.tileHeight / 4)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, window: pygame.Surface):
        window.blit(self.image, self.rect)


class Bullet(Projectile):
    def __init__(self, x, y, velocity, damage=ProjectileSettings.bulletDamage) -> None:
        super().__init__(x, y)

        self.velocity = velocity
        self.damage = damage

    def update(self):
        self.rect.move_ip(self.velocity[0], self.velocity[1])


"""此处NPC可以是monster也可以是player,当player发出时,锁定最近的敌人。(计划书中没有player发出的情况,有时间再添加)"""


class Tracking_bullet(Projectile):
    def __init__(self, npc_rect: pygame.Rect, speed=8) -> None:
        super().__init__()

        self.speed = speed
        self.player_rect = npc_rect

    def update(self) -> None:
        dir = (self.player_rect.x - self.rect.x, self.player_rect.y - self.rect.y)
        movement = Math.round(Math.dot(Math.normalize(dir), self.speed))
        self.rect.move_ip(movement[0], movement[1])


class Big_bullet(Projectile):
    def __init__(self, velocity) -> None:
        super().__init__()
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth / 2, SceneSettings.tileHeight / 2)
        )
        self.velocity = velocity

    def update(self) -> None:
        self.rect.move_ip(self.velocity[0], self.velocity[1])


"""Laser通过普通子弹在循环中生成连续的多个子弹传实现"""


class Laser(Projectile):
    def __init__(self, velocity) -> None:
        super().__init__()

        self.velocity = velocity


class tantanle(Projectile):
    def __init__(self, velocity) -> None:
        super().__init__()

        self.velocity = velocity
