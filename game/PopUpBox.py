# -*- coding:utf-8 -*-

import pygame

from typing import *
from Settings import *


class DialogBox:
    def __init__(
        self,
        window,
        npc,
        fontSize: int = DialogSettings.textSize,
        fontColor: Tuple[int, int, int] = (255, 255, 255),
        bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150),
    ):
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        """初始化窗口,字体大小和颜色以及类型"""

        self.bg = pygame.Surface(
            (DialogSettings.boxWidth, DialogSettings.boxHeight), pygame.SRCALPHA
        )
        self.bg.fill(bgColor)
        """背景的颜色是bgColor"""

        self.npc = pygame.image.load(npc)
        self.npc = pygame.transform.scale(
            self.npc, (DialogSettings.npcWidth, DialogSettings.npcHeight)
        )

        """npc图像更新"""

    def draw(self, input_: str):
        self.window.blit(
            self.bg, (DialogSettings.boxStartX, DialogSettings.boxStartY)
        )  # 绘制背景
        self.window.blit(
            self.npc, (DialogSettings.npcCoordX, DialogSettings.npcCoordY)
        )  # 绘制npc
        text_surface = self.font.render(input_, True, self.fontColor)  # 创建文本表面
        self.window.blit(
            text_surface, (DialogSettings.boxStartX, DialogSettings.boxStartY)
        )  # 绘制文本
