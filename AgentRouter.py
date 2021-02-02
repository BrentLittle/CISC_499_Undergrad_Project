import pygame

class AgentRouter(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, connectionRadius, borderLines):
        self.xPos = xPos
        self.yPos = yPos
        self.connectionRadius = connectionRadius
        self.radius = 12
        self.borders = borderLines

    def DistanceToTopBorder(self):
        upperEdgeofRouter = self.yPos - self.radius
        borderYCoord = self.borders[0].startY
        return upperEdgeofRouter - borderYCoord

    def DistanceToRightBorder(self):
        rightEdgeofRouter = self.xPos + self.radius
        borderXCoord = self.borders[1].startX
        return borderXCoord - rightEdgeofRouter

    def DistanceToBottomBorder(self):
        bottomEdgeofRouter = self.yPos + self.radius
        borderYCoord = self.borders[2].startY
        return borderYCoord - bottomEdgeofRouter

    def DistanceToLeftBorder(self):
        leftEdgeofRouter = self.xPos - self.radius
        borderXCoord = self.borders[3].startX
        return leftEdgeofRouter - borderXCoord 