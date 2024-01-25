# 此处是测试代码语法正确性的地方


import pygame
import sys
from Settings import *

# 初始化 Pygame
pygame.init()

# 创建显示窗口
screen = pygame.display.set_mode((800, 600))

# 定义文本和字体样式
text = "test\ntest"
font = pygame.font.Font(None, 36)

# 渲染文本
text_surface = font.render(text, True, (255, 255, 255))

# 定义文本位置
text_x = 100
text_y = 100

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))  # 填充背景色
    screen.blit(text_surface, (text_x, text_y))  # 绘制文本

    pygame.display.flip()

