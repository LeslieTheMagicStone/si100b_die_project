import pygame
from Settings import *


class BgmPlayer:
    def __init__(self):
        self.current_bgm = None
        self.is_playing = False

    def play(self, name, loop=-1):
        if self.is_playing:
            self.stop()

        bgm_path = self.get_bgm_path(name)
        if bgm_path:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(loop)
            self.current_bgm = name
            self.is_playing = True
        else:
            print(f"Error: BGM file '{name}' not found")

    def stop(self):
        pygame.mixer.music.stop()
        self.current_bgm = None
        self.is_playing = False

    def get_bgm_path(self, name):
        bgm_root = r".\assets\bgm"
        bgm_file_path = f"{bgm_root}\{name}.mp3"
        if bgm_file_path in GamePath.bgm:
            return bgm_file_path
        else:
            return None
