# -*- coding:utf-8 -*-
from enum import Enum

class Collidable:
    def __init__(self):
        self.collisions_enter = []
        self.collisions_stay = []
        self.collisions_exit = []

    
    