import pygame
from Attributes import Renderable, Damageable
from Settings import *


class HealthBar(Renderable):
    def __init__(
        self,
        owner: Damageable,
        owner_rect: pygame.Rect,
        width=HealthBarSettings.width,
        height=HealthBarSettings.height,
        render_index=RenderIndex.ui,
        is_active=True,
        dy=HealthBarSettings.dy,
    ):
        super().__init__(render_index, is_active)

        self.owner = owner
        self.owner_rect = owner_rect

        self.width = width
        self.height = height

        self.dy = dy

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        # Calculate the width of the health bar based on current health
        bar_fill = (self.owner.cur_hp / self.owner.max_hp) * self.width

        # Draw the background bar
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                self.owner_rect.centerx - self.width // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
                self.width,
                self.height,
            ),
        )

        # Draw the filled portion of the health bar
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                self.owner_rect.centerx - self.width // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
                bar_fill,
                self.height,
            ),
        )


class DialogBox(Renderable):
    def __init__(
        self,
        fontSize: int = DialogSettings.textSize,
        fontColor: tuple[int, int, int] = (255, 255, 255),
        bgColor: tuple[int, int, int, int] = (0, 0, 0, 150),
    ):
        Renderable.__init__(self, render_index=100)

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(GamePath.youYuan, self.fontSize)

        """初始化窗口,字体大小和颜色以及类型"""

        self.bg = pygame.Surface(
            (DialogSettings.boxWidth, DialogSettings.boxHeight), pygame.SRCALPHA
        )
        self.bg.fill(bgColor)
        """背景的颜色是bgColor"""

        self.portrait = None
        """npc图像更新"""

        self.text = ""
        """文本框显示的文字"""

        self.cur_page = 0
        """当前页数"""

    def set_text(self, text: str):
        self.text = text.split("，")
        self.cur_page = 0

    def next_page(self):
        self.cur_page += 1

        # Close the box when the text is over
        if self.cur_page >= len(self.text):
            self.cur_page = 0
            self.is_active = False

    def set_portrait(self, portrait):
        self.portrait = portrait

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        if not self.is_active:
            return

        window.blit(
            self.bg, (DialogSettings.boxStartX, DialogSettings.boxStartY)
        )  # 绘制背景

        if self.portrait is not None:
            image = pygame.Surface.copy(self.portrait)
            image = pygame.transform.scale(
                self.portrait, (DialogSettings.npcWidth, DialogSettings.npcHeight)
            )
            window.blit(
                image, (DialogSettings.npcCoordX, DialogSettings.npcCoordY)
            )  # 绘制头像

        text_surface = self.font.render(self.text[self.cur_page], True, self.fontColor)  # 创建文本表面
        window.blit(
            text_surface, (DialogSettings.boxStartX, DialogSettings.boxStartY)
        )  # 绘制文本
