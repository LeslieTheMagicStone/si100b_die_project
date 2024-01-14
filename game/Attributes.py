from enum import Enum
import pygame


# MonoBehaviors have update() function
class MonoBehavior:
    def __init__(self):
        self.start_called = False

    # Start function called the first frame after initialization
    def start(self):
        pass

    def update(self):
        raise NotImplementedError(f"The updated() method is not implemented in {self}")


class Renderable:
    def __init__(self, render_index, is_active=True) -> None:
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
    def __init__(self, need_collision_list=False, is_rigid=False) -> None:
        # All collidables should have rect
        self.rect: pygame.Rect = None
        # With this enabled, it will act like block
        self.is_rigid = is_rigid
        # Used to detect upcoming collision
        self.velocity = (0, 0)
        # With this enabled, the enter/stay/exit list will be updated once per frame
        self.need_collision_list = need_collision_list
        self.collisions_enter = []
        self.collisions_stay = []
        self.collisions_exit = []


class Damageable:
    def __init__(self) -> None:
        # All Damageables should have hp
        self.cur_hp = 0
        self.max_hp = 0
        # If is invulnerable, it will not take any damage
        self.is_invulnerable = False

    def handle_damage(self) -> None:
        raise NotImplementedError(f"The handle_damge() method is not implemented in {self}")
