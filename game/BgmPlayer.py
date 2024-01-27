import pygame
import os
from Settings import *


class BgmPlayer:
    current_bgm = None
    is_playing = False
    bgm_cache = {}

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

    @staticmethod
    def set_volume(value):
        pygame.mixer.music.set_volume(value)

    @classmethod
    def stop(cls):
        pygame.mixer.music.stop()
        cls.current_bgm = None
        cls.is_playing = False

    @staticmethod
    def get_bgm_path(name):
        bgm_root = GamePath.soundRoot
        bgm_file_paths = [
            f"{bgm_root}\{name}.mp3",
            f"{bgm_root}\{name}.wav",
            f"{bgm_root}\{name}.mp3",
        ]
        for bgm_file_path in bgm_file_paths:
            # Check if the file path exists in the cache
            if bgm_file_path in SoundPlayer.sound_cache:
                return BgmPlayer.bgm_cache[name]
        
        for bgm_file_path in bgm_file_paths:
            # Perform the file existence check
            if os.path.isfile(bgm_file_path):
                BgmPlayer.bgm_cache[name] = bgm_file_path
                return bgm_file_path
                    
        return None


class SoundPlayer:
    channels = []
    sound_cache  = {}

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

    def set_volume(self, value):
        self.channel.set_volume(value)

    def stop(self):
        self.channel.stop()

    @staticmethod
    def get_sound_path(name):
        sound_root = GamePath.soundRoot
        sound_file_paths = [
            f"{sound_root}\{name}.mp3",
            f"{sound_root}\{name}.wav",
            f"{sound_root}\{name}.mp3",
        ]
        for sound_file_path in sound_file_paths:
            # Check if the file path exists in the cache
            if sound_file_path in SoundPlayer.sound_cache:
                return SoundPlayer.sound_cache[name]
        
        for sound_file_path in sound_file_paths:
            # Perform the file existence check
            if os.path.isfile(sound_file_path):
                SoundPlayer.sound_cache[name] = sound_file_path
                return sound_file_path
                    
        return None
