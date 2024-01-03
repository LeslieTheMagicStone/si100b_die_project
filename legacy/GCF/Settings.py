from enum import Enum

class WindowSettings:
    name = "小李做的都队"
    width = 1280
    height = 720

class GameSettings:
    fps = 30

class PlayerSettings:
    speed = 5
    width = 60
    height = 55

class GamePath:
    # player/npc related path
    player = [
        r".\assets\player\1.png"
    ]
    npc = r".\assets\npc\npc.png"
    monster = r".\assets\npc\monster\1.png"

    groundTiles = [
        r".\assets\tiles\ground1.png", 
        r".\assets\tiles\ground2.png", 
        r".\assets\tiles\ground3.png", 
        r".\assets\tiles\ground4.png", 
        r".\assets\tiles\ground5.png", 
        r".\assets\tiles\ground6.png", 
    ]

    tree = r".\assets\tiles\tree.png"