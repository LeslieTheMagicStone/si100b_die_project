from enum import Enum
import pygame

# MonoBehaviors have update() function
class MonoBehavior:
    def update(self):
        pass



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
