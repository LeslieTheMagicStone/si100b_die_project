from enum import Enum
import pygame
import math


# MonoBehaviors have update() function
class MonoBehavior:
    def __init__(self):
        self.start_called = False

    # Start function called the first frame after initialization
    def start(self):
        pass

    def update(self):
        raise NotImplementedError(f"The update() method is not implemented in {self}")


class Renderable:
    def __init__(self, render_index, is_active=True):
        # Decides render sequence, object with smallest index renders first
        self.render_index = render_index
        # Decides if the object need to render
        self.is_active = is_active

    def set_active(self, value):
        self.is_active = value

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        raise NotImplementedError(f"The draw() method is not implemented in {self}")


# Collidables will be operated in the update_collision() function in the Scene
class Collidable:
    def __init__(
        self, need_collision_list=False, is_rigid=False, rect: pygame.Rect = None
    ):
        # Layer is used to avoid certain collisions
        self.layer = "Default"
        # All collidables should have rect
        self.rect: pygame.Rect = rect
        # With this enabled, it will act like block
        self.is_rigid = is_rigid
        # Used to detect upcoming collision
        self.velocity = (0, 0)
        # With this enabled, the enter/stay/exit list will be updated once per frame
        self.need_collision_list = need_collision_list
        self.collisions_enter: list[Collidable] = []
        self.collisions_stay: list[Collidable] = []
        self.collisions_exit: list[Collidable] = []

    # Used to debug
    def show_rect(self, window: pygame.Surface, dx, dy, color=(0, 0, 0)):
        pygame.draw.rect(window, color, self.rect.move(dx, dy))


class Damageable:
    def __init__(self):
        # All Damageables should have hp
        self.cur_hp = 0
        self.max_hp = 0

    def handle_damage(self) -> None:
        raise NotImplementedError(
            f"The handle_damage() method is not implemented in {self}"
        )


class Levelable:
    def __init__(self) -> None:
        self.level = 1
        self.max_exp = 10
        self.cur_exp = 0

    def add_exp(self, added_value):
        self.cur_exp += added_value
        if self.cur_exp > self.max_exp:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_exp = self.get_max_exp(self.level)
        self.cur_exp = 0

    def get_max_exp(self, level):
        return (level + 1) * 10


class Buffable:
    def __init__(self) -> None:
        # 角色的BUFF状态，初始啥都是空，空即为最初的状态
        self.buffs = {}

    """buff_time 为此BUFF对应的时间，-1代表永久"""

    def add_buff(self, buff_name: str, buff_time: float):
        self.buffs[buff_name] = buff_time

    def delete_Buff(self, buff_name: str):
        if buff_name in self.buffs:
            del self.buffs[buff_name]


class reinforcable:
    def __init__(self) -> None:
        self.accumulative = 0
        self.max_ = 10
        self.cur_ = 0
        self.ready = 0

    def add_accumulative(self, added_value):
        if self.ready != 1:
            self.cur_ += added_value
        if self.cur_ >= self.max_:
            self.cur_ = self.max_
            self.ready = 1

    def finished(self):
        self.cur_ = 0
        self.ready = 0
