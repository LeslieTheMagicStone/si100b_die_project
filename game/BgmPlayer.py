import pygame
from Settings import *


class BgmPlayer:
    current_bgm = None
    is_playing = False

    @classmethod
    def play(cls, name, loop=-1):
        if cls.current_bgm == name:
            return

        if cls.is_playing:
            cls.stop()

        bgm_path = cls.get_bgm_path(name)
        if bgm_path:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(loop)
            cls.current_bgm = name
            cls.is_playing = True
        else:
            print(f"Error: BGM file '{name}' not found")

    @classmethod
    def stop(cls):
        pygame.mixer.music.stop()
        cls.current_bgm = None
        cls.is_playing = False

    @staticmethod
    def get_bgm_path(name):
        bgm_root = r".\assets\bgm"
        bgm_file_path = f"{bgm_root}\{name}.mp3"
        if bgm_file_path in GamePath.bgm:
            return bgm_file_path
        else:
            return None


class SoundPlayer:
    channels = []

    def __init__(self):
        self.channel = pygame.mixer.Channel(len(self.channels))
        SoundPlayer.channels.append(self.channel)

    def play(self, name):
        if self.channel.get_busy():
            self.channel.stop()

        sound_path = SoundPlayer.get_sound_path(name)

        if sound_path:
            sound = pygame.mixer.Sound(sound_path)
            self.channel.play(sound)
        else:
            print(f"Error: sound file '{name}' not found")

    def stop(self):
        self.channel.stop()

    @staticmethod
    def get_sound_path(name):
        sound_root = r".\assets\sound"
        sound_file_path = f"{sound_root}\{name}.mp3"
        if sound_file_path in GamePath.sound:
            return sound_file_path
        else:
            return None
