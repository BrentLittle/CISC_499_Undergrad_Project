import pygame

class FixedRouter(pygame.sprite.Sprite):
    
#                         r    g    b    a
    COLOUR            = ( 46, 184,  46, 255)
    CONNECTION_COLOUR = (153, 230, 153,  32)

    def __init__(self, xPos, yPos, connectionRadius):
        self.xPos = round(xPos)
        self.yPos = round(yPos)
        self.connectionRadius = connectionRadius
        self.radius = 12

    def Update(self):
        return