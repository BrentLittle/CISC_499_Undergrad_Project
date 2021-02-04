import random

class Device():

    COLOUR = (255, 0, 0, 255)

    def __init__(self, xPos, yPos):
        self.xPos = round(xPos)
        self.yPos = round(yPos)
        self.xBias = 0
        self.yBias = 0
        self.radius = 6
        self.scene = None
    
    def SetBias(self, xBias, yBias):
        self.xBias = xBias
        self.yBias = yBias

    def SetScene(self, scene):
        self.scene = scene

    def Update(self):

        xDelta = self.Clamp(-1, 1, round(random.randint(-1, 1) + self.xBias))
        yDelta = self.Clamp(-1, 1, round(random.randint(-1, 1) + self.yBias))

        self.Move(xDelta, yDelta)

    def Clamp(self, minVal, maxVal, value):
        if value <= minVal : return minVal
        elif value >= maxVal : return maxVal
        
        return value
    
    def Move(self, xDelta, yDelta):
        self.xPos += xDelta
        self.yPos += yDelta

        if(self.scene != None):
            if (self.xPos >= self.scene.columns or self.xPos < 0):
                self.Remove()

            if (self.yPos >= self.scene.rows or self.yPos < 0):
                self.Remove()
    
    def Remove(self):
        if(self.scene != None):
            self.scene.RemoveDevice(self)