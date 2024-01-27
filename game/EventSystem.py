import pygame
from Settings import GameEvent


class EventSystem:
    @staticmethod
    def fire_switch_event(GOTO):
        switch_event = pygame.event.Event(GameEvent.EVENT_SWITCH, message=GOTO)
        pygame.event.post(switch_event)

    @staticmethod
    def fire_hurt_event(damage):
        hurt_event = pygame.event.Event(GameEvent.EVENT_HURT, message=damage)
        pygame.event.post(hurt_event)

    @staticmethod
    def fire_generate_event(obj, scene=None):
        generate_event = pygame.event.Event(
            GameEvent.EVENT_GENERATE, message=(obj, scene)
        )
        pygame.event.post(generate_event)

    @staticmethod
    def fire_dialog_event(portrait, text, callback=None):
        dialog_event = pygame.event.Event(
            GameEvent.EVENT_DIALOG, portrait=portrait, text=text, callback=callback
        )
        pygame.event.post(dialog_event)

    @staticmethod
    def fire_shop_event(portrait, items, callback=None):
        shop_event = pygame.event.Event(
            GameEvent.EVENT_SHOP, portrait=portrait, items=items, callback=callback
        )
        pygame.event.post(shop_event)

    @staticmethod
    def fire_hit_event(damage, position):
        hit_event = pygame.event.Event(GameEvent.EVENT_HIT, message=(damage, position))
        pygame.event.post(hit_event)

    @staticmethod
    def fire_destroy_event(obj, scene=None):
        destroy_event = pygame.event.Event(
            GameEvent.EVENT_DESTROY, message=(obj, scene)
        )
        pygame.event.post(destroy_event)

    @staticmethod
    def fire_buff_event(buff_name, buff_time):
        buff_event = pygame.event.Event(
            GameEvent.EVENT_BUFF, buff_name=buff_name, buff_time=buff_time
        )
        pygame.event.post(buff_event)

    @staticmethod
    def fire_game_over_event():
        game_over_event = pygame.event.Event(GameEvent.EVENT_GAME_OVER)
        pygame.event.post(game_over_event)

    @staticmethod
    def fire_restart_event():
        restart_event = pygame.event.Event(GameEvent.EVENT_RESTART)
        pygame.event.post(restart_event)
