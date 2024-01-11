# -*- coding:utf-8 -*-

import pygame

from typing import *
from Settings import *
from Attributes import *
from NPCs import NPC


class DialogBox(Renderable):
    def __init__(
        self,
        npc: NPC = None,
        fontSize: int = DialogSettings.textSize,
        fontColor: Tuple[int, int, int] = (255, 255, 255),
        bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150),
    ):
        Renderable.__init__(self, render_index=100)

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        """初始化窗口,字体大小和颜色以及类型"""

        self.bg = pygame.Surface(
            (DialogSettings.boxWidth, DialogSettings.boxHeight), pygame.SRCALPHA
        )
        self.bg.fill(bgColor)
        """背景的颜色是bgColor"""

        self.npc = npc
        """npc图像更新"""

        self.text = ""
        """文本框显示的文字"""

    def set_text(self, text):
        self.text = text

    def set_npc(self, npc):
        self.npc = npc

    def draw(self, window: pygame.Surface):
        if not self.is_active:
            return

        window.blit(
            self.bg, (DialogSettings.boxStartX, DialogSettings.boxStartY)
        )  # 绘制背景
        
        if self.npc is not None:
            image = pygame.Surface.copy(self.npc)
            image = pygame.transform.scale(
                self.npc, (DialogSettings.npcWidth, DialogSettings.npcHeight)
            )
            window.blit(
                image, (DialogSettings.npcCoordX, DialogSettings.npcCoordY)
            )  # 绘制npc

        text_surface = self.font.render(self.text, True, self.fontColor)  # 创建文本表面
        window.blit(
            text_surface, (DialogSettings.boxStartX, DialogSettings.boxStartY)
        )  # 绘制文本
