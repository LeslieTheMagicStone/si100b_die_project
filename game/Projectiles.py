import pygame
from Settings import *


class Projectile(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = pygame.image.load(GamePath.bossTiles[0])
        self.image = pygame.transform.scale(
            self.image, (SceneSettings.tileWidth / 2, SceneSettings.tileHeight / 2)
        )
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def draw(self, window: pygame.Surface):
        window.blit(self.image, self.rect)


class Bullet(Projectile):
    def __init__(self, velocity) -> None:
        super().__init__()

        self.velocity = velocity

    def update(self):
        self.rect.move_ip(self.velocity[0], self.velocity[1])
