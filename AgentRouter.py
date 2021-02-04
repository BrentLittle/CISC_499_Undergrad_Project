import pygame

class AgentRouter(pygame.sprite.Sprite):

#                         r    g    b    a
    COLOUR            = (230, 184,   0, 255)
    CONNECTION_COLOUR = (255, 224, 102,  50)

    def __init__(self, xPos, yPos, connectionRadius):
        self.xPos = round(xPos)
        self.yPos = round(yPos)
        self.connectionRadius = connectionRadius
        self.radius = 12
        self.scene = None

    def SetScene(self, scene):
        self.scene = scene

    def Update(self):
        self.Move(1, 0)
    
    def Move(self, xDelta, yDelta):
        self.xPos += xDelta
        self.yPos += yDelta

        if(self.scene != None):
            if (self.xPos >= self.scene.columns):
                self.xPos = self.scene.columns - 1
            elif (self.xPos < 0):
                self.xPos = 0

            if (self.yPos >= self.scene.rows):
                self.yPos = self.scene.rows - 1
            elif (self.yPos < 0):
                self.yPos = 0