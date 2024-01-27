from typing import Any
import pygame
from Settings import *
from Math import *
from Attributes import *
from Settings import Causality
from globals import Time
from EventSystem import *
from BgmPlayer import SoundPlayer
from random import random, randint
import generator


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
        if self.life_time != -1:
            self.life_time -= Time.delta_time
            if self.life_time < 0:
                EventSystem.fire_destroy_event(self)


class Tools(Projectile):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.need_collision_list = True

        self.image = pygame.image.load(GamePath.mask)
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth * 2, SceneSettings.tileHeight * 2)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = (0, 0)

        # Life time is infinity
        self.life_time = -1

    def update(self):
        super().update()

        for other in self.collisions_enter:
            if other.layer == "Player":
                EventSystem.fire_destroy_event(self)
                EventSystem.fire_dialog_event(
                    self.image,
                    "这是一个古老的面具，上面蕴藏着神秘的力量，可以让玩家拥有转换能力，（按E切换子弹元素：普通/冰/火）",
                    callback=self.add_causility_buff,
                )

    def add_causility_buff(self):
        EventSystem.fire_buff_event("Causality", -1)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class Bullet(Projectile):
    sound_player: SoundPlayer = None

    def __init__(
        self,
        x,
        y,
        velocity,
        damage,
        causality=Causality.NORMAL,
    ) -> None:
        super().__init__(x, y)
        self.need_collision_list = True

        # Init class sound player
        if Bullet.sound_player is None:
            Bullet.sound_player = SoundPlayer()

        self.image = pygame.image.load(GamePath.normal_bullet[causality.value])
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth // 4, SceneSettings.tileHeight // 4)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocity = velocity
        self.damage = damage
        self.causality = causality

        # Chance to play sound when hitting wall
        self.sound_chance = 0

    def update(self):
        super().update()

        # Collide rigid ones then destroy itself
        for other in self.collisions_enter:
            if other.is_rigid and other.layer != "Player":
                self.set_active(False)
                EventSystem.fire_destroy_event(self)
                if other.layer == "Default":
                    # Play hit wall sound
                    if random() < self.sound_chance:
                        Bullet.sound_player.play("hit_wall")
                    EventSystem.fire_hit_event(0, self.rect.center)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class Big_bullet(Bullet):
    def __init__(
        self,
        x,
        y,
        velocity,
        damage,
        causality=Causality.NORMAL,
    ) -> None:
        super().__init__(x, y, velocity, damage)

        self.image = pygame.image.load(GamePath.big_bullet[causality.value])
        self.image = pygame.transform.scale(
            self.image,
            (ProjectileSettings.bigBulletWidth, ProjectileSettings.bigBulletHeight),
        )
        self.image = pygame.transform.rotate(
            self.image, Math.angle_degrees(velocity) - 90
        )

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocity = velocity
        self.damage = damage
        self.causality = causality

        self.sound_chance = 1

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class EnemyBullet(Projectile):
    sound_player: SoundPlayer = None

    def __init__(
        self,
        x,
        y,
        velocity,
        damage,
        causality=Causality.NORMAL,
    ) -> None:
        super().__init__(x, y)
        self.need_collision_list = True

        # Init class sound player
        if EnemyBullet.sound_player is None:
            EnemyBullet.sound_player = SoundPlayer()

        self.image = pygame.image.load(GamePath.normal_bullet[causality.value])
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth // 2, SceneSettings.tileHeight // 2)
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocity = velocity
        self.damage = damage
        self.causality = causality

        # Chance to play sound when hitting wall
        self.sound_chance = 1

    def update(self):
        super().update()

        # Collide rigid ones then destroy itself
        for other in self.collisions_enter:
            if other.is_rigid and other.layer != "Enemy":
                self.set_active(False)
                EventSystem.fire_destroy_event(self)
                if other.layer == "Default":
                    # Play hit wall sound
                    if random() < self.sound_chance:
                        EnemyBullet.sound_player.play("hit_wall")
                    EventSystem.fire_hit_event(0, self.rect.center)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        window.blit(self.image, self.rect.move(dx, dy))


class EnemyBigBullet(EnemyBullet):
    def __init__(self, x, y, velocity, damage, causality=Causality.NORMAL) -> None:
        super().__init__(x, y, velocity, damage, causality)
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def on_destroy(self):
        # When destroyed init several small bullets

        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            generator.generate(
                EnemyBullet(
                    self.rect.centerx,
                    self.rect.centery,
                    Math.scale(direction, ProjectileSettings.bulletSpeed),
                    5,
                    self.causality,
                )
            )


class EnemyLaser(EnemyBullet):
    def __init__(self, x, y, velocity, damage, causality=Causality.NORMAL) -> None:
        super().__init__(x, y, velocity, damage)

        self.image = pygame.image.load(GamePath.big_bullet[causality.value])
        self.image = pygame.transform.scale(
            self.image,
            (ProjectileSettings.bigBulletWidth, ProjectileSettings.bigBulletHeight),
        )
        self.image = pygame.transform.rotate(
            self.image, Math.angle_degrees(velocity) - 90
        )

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.velocity = velocity
        self.damage = damage
        self.causality = causality

        self.sound_chance = 1


class EnemyLaserGenerator(EnemyBullet):
    def __init__(self, x, y, damage, life_time=10, causality=Causality.NORMAL) -> None:
        super().__init__(x, y, velocity=(0, 0), damage=damage, causality=causality)
        # Life time related
        self.life_time = life_time
        # Image and rect
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Generate Enemy Laser
        self.generate_cd = 0.4
        self.generate_timer = 0
        

    def update(self):
        super().update()

        self.generate_timer -= Time.delta_time

        if self.generate_timer <= 0:
            self.generate_timer = self.generate_cd

            for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                generator.generate(
                    EnemyLaser(
                        self.rect.centerx,
                        self.rect.centery,
                        Math.scale(direction, ProjectileSettings.bulletSpeed // 2),
                        5,
                        self.causality,
                    )
                )
