import pygame
from Settings import GameEvent


class EventSystem:
    @classmethod
    def fire_switch_event(cls, GOTO):
        switch_event = pygame.event.Event(GameEvent.EVENT_SWITCH, message=GOTO)
        pygame.event.post(switch_event)
