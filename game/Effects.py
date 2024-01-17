import pygame
import generator

from Attributes import Renderable
from Settings import RenderIndex, GamePath
from EventSystem import *


class Effect(pygame.sprite.Sprite, Renderable):
    def __init__(
        self,
        images: list[str] | list[pygame.Surface],
        x,
        y,
        width,
        height,
        looping=False,
        tpf=1,
    ) -> None:
        pygame.sprite.Sprite.__init__(self)
        Renderable.__init__(self, render_index=RenderIndex.effect)

        # If the images argument is the paths of images, load them first
        if isinstance(images[0], str):
            self.images = [
                pygame.transform.scale(pygame.image.load(path), (width, height))
                for path in images
            ]
        else:
            self.images = images

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Tick per Frame
        # Update animation frame every (tpf) render() tick
        self.tpf = tpf
        self.frame_index = 0
        self.tpf_timer = self.tpf
        # If not looping, then destroy it after playing one loop
        self.looping = looping

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        # Update animation every (tpf) render() frame
        if self.tpf_timer <= 0:
            self.tpf_timer = self.tpf
            self.frame_index += 1

            # If not looping, then destroy it after playing one loop
            if self.frame_index == len(self.images) and not self.looping:
                EventSystem.fire_destroy_event(self)
                return

            self.frame_index = self.frame_index % len(self.images)
            self.image = self.images[self.frame_index]

        self.tpf_timer -= 1

        window.blit(self.image, self.rect.move(dx, dy))


class EffectManager:
    @classmethod
    def generate(cls, effect_name: str, x, y):
        if effect_name.startswith("text: "):
            text = effect_name.removeprefix("text: ")
            generator.generate(TextEffect(x, y, text))
        elif effect_name == "smoke":
            generator.generate(SmokeEffect(x, y))
        elif effect_name == "teleport":
            generator.generate(TeleportEffect(x, y))
        else:
            raise ValueError(f"no effect named {effect_name}")


class TextEffect(Effect):
    def __init__(
        self, x, y, text, size=36, color=(255, 255, 255), duration_ticks=30
    ) -> None:
        font = pygame.font.Font(None, size)
        image = font.render(text, True, color)

        super().__init__([image], x, y, size, size, looping=False, tpf=duration_ticks)


class SmokeEffect(Effect):
    def __init__(self, x, y, width=32, height=32, looping=False) -> None:
        super().__init__(GamePath.smoke, x, y, width, height, looping)


class TeleportEffect(Effect):
    def __init__(self, x, y, width=100, height=100, looping=False) -> None:
        super().__init__(GamePath.teleport, x, y, width, height, looping, tpf=2)
