from enum import Enum
import pygame

# MonoBehaviors have update() function
class MonoBehavior:
    def update(self):
        raise NotImplementedError(f"The updated() method is not implemented in {self}")

class Renderable:
    def __init__(self, render_index, is_active = True) -> None:
        # Decides render sequence, object with smallest index renders first
        self.render_index = render_index
        # Decides if the object need to render
        self.is_active = is_active

    def set_active(self, value):
        self.is_active = value

    def draw(self, window: pygame.Surface):
        raise NotImplementedError(f"The draw() method is not implemented in {self}")


# Collidables will be counted in the update_collision() function in the Scene
class Collidable:
    def __init__(self, need_collision_list=False) -> None:
        # All collidables should have rect
        self.rect: pygame.Rect = None
        # With this enabled, the enter/stay/exit list will be updated once per frame
        self.need_collision_list = need_collision_list
        self.collisions_enter = []
        self.collisions_stay = []
        self.collisions_exit = []


class Damageable:
    def __init__(self) -> None:
        # All Damageables should have hp
        self.hp = 0

    def handle_damage(self) -> None:
        pass
