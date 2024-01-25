# -*- coding:utf-8 -*-

from enum import Enum
import pygame


class WindowSettings:
    name = "完蛋，我被coke老师包围了！"
    width = 1280
    height = 720
    outdoorScale = 1.5  # A necessary scale to allow camera movement in outdoor scenes


class SceneSettings:
    tileXnum = 48  # 64
    tileYnum = 27  # 36
    tileWidth = tileHeight = 40
    obstacleDensity = 0.12


class PlayerSettings:
    # Initial Player Settings
    speed = 7
    width = 60
    height = 55
    hp = 20
    attack = 5
    defence = 1
    money = 100
    animIntervalSecond = 0.1


class NPCSettings:
    npcSpeed = 1
    npcWidth = 60
    npcHeight = 60


class NPCType(Enum):
    DIALOG = 1
    MONSTER = 2
    SHOP = 3


class BossSettings:
    width = 300
    height = 300
    coordX = (SceneSettings.tileXnum / 2) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2


class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxStartX = WindowSettings.width // 4  # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20  # Coordinate Y of the box

    textSize = 48  # Default font size
    textStartX = (
        WindowSettings.width // 4 + 10
    )  # Coordinate X of the first line of dialog
    textStartY = (
        WindowSettings.height // 3 * 2 + 30
    )  # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3  # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20


class BattleSettings:
    boxWidth = WindowSettings.width * 3 // 4
    boxHeight = WindowSettings.height * 3 // 4
    boxStartX = WindowSettings.width // 8  # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 48  # Default font size
    textStartX = WindowSettings.width // 4
    textPlayerStartX = (
        WindowSettings.width // 4
    )  # Coordinate X of the first line of dialog
    textMonsterStartX = WindowSettings.width // 2 + 100
    textStartY = WindowSettings.height // 3  # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3  # Vertical distance of two lines

    playerWidth = WindowSettings.width // 6
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8
    playerCoordY = WindowSettings.height // 2

    monsterWidth = WindowSettings.width // 6
    monsterHeight = WindowSettings.height // 3
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 2

    stepSize = 20


class ShopSettings:
    boxWidth = 800
    boxHeight = 200
    boxStartX = WindowSettings.width // 4  # Coordinate X of the box
    boxStartY = WindowSettings.height // 3  # Coordinate Y of the box

    textSize = 56  # Default font size
    textStartX = boxStartX + 10  # Coordinate X of the first line of dialog
    textStartY = boxStartY + 25  # Coordinate Y of the first line of dialog


class GamePath:
    # Window related path
    menu = r".\assets\background\menu.png"
    wild = r".\assets\background\wild.png"
    mapBlock = r".\assets\background\map.png"

    # player/npc related path
    npc = r".\assets\npc\npc.png"
    player = [
        r".\assets\player\1.png",
        r".\assets\player\2.png",
        r".\assets\player\3.png",
        r".\assets\player\4.png",
        # 8 frames for a single loop of animation looks much better.
    ]
    monster = r".\assets\npc\monster\1.png"
    iceMonster = r".\assets\npc\monster\ice_small_rival.png"
    fireMonster = r".\assets\npc\monster\fire_small_rival.png"
    boss = r".\assets\npc\boss.png"

    groundTiles = [
        r".\assets\tiles\ground1.png",
        r".\assets\tiles\ground2.png",
        r".\assets\tiles\ground3.png",
        r".\assets\tiles\ground4.png",
        r".\assets\tiles\ground5.png",
        r".\assets\tiles\ground6.png",
    ]

    cityTiles = [
        r".\assets\tiles\city1.png",
        r".\assets\tiles\city2.png",
        r".\assets\tiles\city3.png",
        r".\assets\tiles\city4.png",
        r".\assets\tiles\city5.png",
        r".\assets\tiles\city6.png",
    ]

    cityWall = r".\assets\tiles\cityWall.png"

    snowTiles = [
        r".\assets\tiles\snow1.png",
        r".\assets\tiles\snow2.png",
        r".\assets\tiles\snow3.png",
        r".\assets\tiles\snow4.png",
        r".\assets\tiles\snow5.png",
        r".\assets\tiles\snow6.png",
    ]

    bossTiles = [
        r".\assets\tiles\boss1.png",
        r".\assets\tiles\boss2.png",
        r".\assets\tiles\boss3.png",
        r".\assets\tiles\boss4.png",
        r".\assets\tiles\boss5.png",
        r".\assets\tiles\boss6.png",
    ]

    bossWall = r".\assets\tiles\bossWall.png"

    portal = r".\assets\background\portal.png"

    tree = r".\assets\tiles\tree.png"

    bgm = [r".\assets\bgm\city.mp3", r".\assets\bgm\wild.mp3", r".\assets\bgm\boss.mp3"]

    smoke = [
        r".\assets\effects\Smoke\FX001\FX001_01.png",
        r".\assets\effects\Smoke\FX001\FX001_02.png",
        r".\assets\effects\Smoke\FX001\FX001_03.png",
        r".\assets\effects\Smoke\FX001\FX001_04.png",
        r".\assets\effects\Smoke\FX001\FX001_05.png",
    ]

    teleport = [
        r".\assets\effects\Smoke\FX002\FX002_01.png",
        r".\assets\effects\Smoke\FX002\FX002_02.png",
        r".\assets\effects\Smoke\FX002\FX002_03.png",
        r".\assets\effects\Smoke\FX002\FX002_04.png",
        r".\assets\effects\Smoke\FX002\FX002_05.png",
        r".\assets\effects\Smoke\FX002\FX002_06.png",
        r".\assets\effects\Smoke\FX002\FX002_07.png",
        r".\assets\effects\Smoke\FX002\FX002_08.png",
    ]


class PortalSettings:
    width = 160
    height = 160
    coordX = (SceneSettings.tileXnum - 10) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2


class HealthBarSettings:
    width = 60
    height = 10
    dy = 10


class RenderIndex:
    portal = 0
    player = 1
    monster = 2
    npc = 4
    block = -1
    tileMap = -2
    projectile = 3
    ui = 10
    effect = 9


class ProjectileSettings:
    bulletSpeed = 20
    bulletDamage = 2


class Causality(Enum):
    NORMAL = 0
    ICE = 1
    FIRE = 2


class GameState(Enum):
    GAME_MAIN_MENU = 1
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY = 6


class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    # Go to another scene
    EVENT_SWITCH = pygame.USEREVENT + 3
    # Restart the game
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5
    # Player gets hurt
    EVENT_HURT = pygame.USEREVENT + 6
    # Append object to scene._objects
    EVENT_GENERATE = pygame.USEREVENT + 7
    # Enemy gets hurt
    EVENT_HIT = pygame.USEREVENT + 8
    # Remove object from scene._objects
    EVENT_DESTROY = pygame.USEREVENT + 9
