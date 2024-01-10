import pygame
from Settings import GameEvent


class EventSystem:
    @classmethod
    def fire_switch_event(cls, GOTO):
        switch_event = pygame.event.Event(GameEvent.EVENT_SWITCH, message=GOTO)
        pygame.event.post(switch_event)

    @classmethod
    def fire_hurt_event(cls, damage):
        hurt_event = pygame.event.Event(GameEvent.EVENT_HURT, message=damage)
        pygame.event.post(hurt_event)

    @classmethod
    def fire_generate_event(cls, obj):
        generate_event = pygame.event.Event(GameEvent.EVENT_GENERATE, message=obj)
        pygame.event.post(generate_event)
