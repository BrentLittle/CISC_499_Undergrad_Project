import pygame

class FixedRouter(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, connectionRadius):
        self.xPos = xPos
        self.yPos = yPos
        self.connectionRadius = connectionRadius
        self.radius = 12