import pygame

class BorderLine (pygame.sprite.Sprite):
    def __init__(self, startX, startY, endX, endY):
        pygame.sprite.Sprite.__init__(self)
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY