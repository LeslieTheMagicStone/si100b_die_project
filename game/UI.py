import pygame
from Attributes import Renderable, Damageable
from Settings import RenderIndex, HealthBarSettings


class HealthBar(Renderable):
    def __init__(
        self,
        owner: Damageable,
        owner_rect: pygame.Rect,
        width=HealthBarSettings.width,
        height=HealthBarSettings.height,
        render_index=RenderIndex.ui,
        is_active=True,
        dy=HealthBarSettings.dy,
    ):
        super().__init__(render_index, is_active)

        self.owner = owner
        self.owner_rect = owner_rect

        self.width = width
        self.height = height

        self.dy = dy

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        # Calculate the width of the health bar based on current health
        bar_fill = (self.owner.cur_hp / self.owner.max_hp) * self.width

        # Draw the background bar
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                self.owner_rect.centerx - self.width // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
                self.width,
                self.height,
            ),
        )

        # Draw the filled portion of the health bar
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                self.owner_rect.centerx - self.width // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
                bar_fill,
                self.height,
            ),
        )
