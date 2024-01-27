import pygame
from Settings import GameState
from Attributes import Collidable


class Time:
    delta_time = 0
    time = 0


class SceneManager:
    current_scene = ""


class Input:
    key_down = {}
    key_pressed = {}

    @classmethod
    def get_key_down(cls, key):
        return key in cls.key_down.keys() and cls.key_down[key]

    @classmethod
    def get_key(cls, key):
        return key in cls.key_pressed.keys() and cls.key_pressed[key]


class CurrentState:
    state = GameState.NORMAL
    in_transition_animation = False


class CollisionChecker:
    _collidables: list[Collidable] = []

    @classmethod
    def check_rigids(cls, rect: pygame.rect.Rect):
        rigids = [c.rect for c in cls._collidables if c.is_rigid and c.rect is not rect]
        return rect.collidelist(rigids) != -1
