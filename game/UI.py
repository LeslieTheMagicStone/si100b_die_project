import pygame
from Attributes import *
from Settings import *
from globals import *
from EventSystem import *


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

        self.font = pygame.font.Font(None, 15)
        self.fontColor = (255, 255, 255)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        if not self.is_active:
            return

        if self.owner.max_hp != 0:
            # Calculate the width of the health bar based on current health
            bar_fill = (self.owner.cur_hp / self.owner.max_hp) * self.width
        else:
            bar_fill = self.width
            print(f"Zero max hp: {self.owner}")

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

        # Draw the hp text
        text_surface = self.font.render(
            f"{self.owner.cur_hp}/{self.owner.max_hp}", True, self.fontColor
        )
        window.blit(
            text_surface,
            (
                self.owner_rect.centerx - text_surface.get_width() // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
            ),
        )


class ExpBar(Renderable):
    def __init__(
        self,
        owner: Levelable,
        owner_rect: pygame.Rect,
        width=ExpBarSettings.width,
        height=ExpBarSettings.height,
        render_index=RenderIndex.ui,
        is_active=True,
        dy=ExpBarSettings.dy,
    ):
        super().__init__(render_index, is_active)

        self.owner = owner
        self.owner_rect = owner_rect

        self.width = width
        self.height = height

        self.dy = dy

        self.font = pygame.font.Font(None, 25)
        self.fontColor = (255, 255, 255)

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        if not self.is_active:
            return

        # Calculate the width of the bar based on current health
        bar_fill = (self.owner.cur_exp / self.owner.max_exp) * self.width

        # Draw the background bar
        pygame.draw.rect(
            window,
            (122, 122, 122),
            (
                self.owner_rect.centerx - self.width // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
                self.width,
                self.height,
            ),
        )

        # Draw the filled portion of the bar
        pygame.draw.rect(
            window,
            (200, 200, 200),
            (
                self.owner_rect.centerx - self.width // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
                bar_fill,
                self.height,
            ),
        )

        # Draw the level text
        text_surface = self.font.render(
            f"Lv. {self.owner.level}", True, self.fontColor, (0, 0, 0)
        )
        window.blit(
            text_surface,
            (
                self.owner_rect.centerx
                - self.width // 2
                - text_surface.get_width()
                + dx,
                self.owner_rect.y - self.height - self.dy + dy,
            ),
        )


class DialogIcon(Renderable):
    def __init__(
        self,
        owner_rect: pygame.Rect,
        text: str,
        width=HealthBarSettings.width,
        height=HealthBarSettings.height,
        render_index=RenderIndex.ui,
        is_active=True,
        dy=HealthBarSettings.dy,
    ):
        super().__init__(render_index, is_active)

        self.owner_rect = owner_rect

        self.width = width
        self.height = height

        self.dy = dy
        self.font = pygame.font.Font(GamePath.youYuan, 25)
        self.fontColor = (255, 255, 255)
        self.text_surface = self.font.render(text, True, self.fontColor)
        self.width = self.text_surface.get_width()
        self.height = self.text_surface.get_height()

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        if not self.is_active:
            return

        window.blit(
            self.text_surface,
            (
                self.owner_rect.centerx - self.width // 2 + dx,
                self.owner_rect.y - self.height - self.dy + dy,
            ),
        )


class Text(Renderable):
    def __init__(
        self,
        x,
        y,
        text,
        size,
        color=(255, 255, 255),
        duration=-1,
        render_index=RenderIndex.ui,
        is_active=True,
        contains_chinese=False,
    ):
        super().__init__(render_index, is_active)

        if contains_chinese:
            self.font = pygame.font.Font(GamePath.youYuan, size)
        else:
            self.font = pygame.font.Font(None, size)

        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.duration = duration
        self.life_time = duration

    def draw(self, window: pygame.Surface, dx=0, dy=0):
        if not self.is_active:
            return

        if self.duration == -1:
            window.blit(self.image, self.rect)
            return
        elif self.life_time < 0:
            EventSystem.fire_destroy_event(self)

        # Fade in, hold, fade out
        self.life_time -= Time.delta_time

        # Fade in state
        if self.duration / 3 * 2 < self.life_time < self.duration:
            alpha = 255 * (
                1 - ((self.life_time - self.duration / 3 * 2) / (self.duration / 3))
            )
        # Hold state
        elif self.duration / 3 * 1 < self.life_time < self.duration / 3 * 2:
            alpha = 255
        # Fade out state
        else:
            alpha = 255 * ((self.life_time - 0) / (self.duration / 3))
        
        self.image.set_alpha(alpha)

        window.blit(self.image, self.rect)



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

        self.callback = None
        """对话显示完毕后调用的函数"""

    def set_text(self, text: str):
        self.text = text.split("，")
        self.cur_page = 0

    def set_callback(self, callback):
        self.callback = callback

    def next_page(self):
        self.cur_page += 1

        # Close the box when the text is over
        if self.cur_page >= len(self.text):
            self.close()

    def close(self):
        self.cur_page = 0
        self.set_active(False)
        CurrentState.state = GameState.NORMAL
        if self.callback is not None:
            self.callback()

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

        text_surface = self.font.render(
            self.text[self.cur_page], True, self.fontColor
        )  # 创建文本表面
        window.blit(
            text_surface, (DialogSettings.boxStartX, DialogSettings.boxStartY)
        )  # 绘制文本
