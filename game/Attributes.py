# -*- coding:utf-8 -*-
from enum import Enum


class Collidable:
    def __init__(self) -> None:
        self.collisions_enter = []
        self.collisions_stay = []
        self.collisions_exit = []


class Damageable:
    def __init__(self) -> None:
        self.hp = 0

    def handle_damage(self) -> None:
        pass
