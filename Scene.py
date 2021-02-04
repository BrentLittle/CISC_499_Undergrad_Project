from AgentRouter import AgentRouter
from FixedRouter import FixedRouter
from Device import Device
import random

class Scene():

    def __init__(self, columns, rows):

        self.fixedRouters = []
        self.agentRouters = []
        self.devices = []

        self._fixedRouterCount = 0
        self._agentCount = 0
        self._deviceCount = 0

        self.tickCount = 0

        self.columns = columns
        self.rows = rows

    def Update(self):

        self.tickCount += 1

        for device in self.devices:
            device.Update()

        for fixedRouter in self.fixedRouters:
            fixedRouter.Update()

        for agent in self.agentRouters:
            agent.Update()

        if (self.tickCount % 2 == 0):
            self.CreateDevice()

    def CreateFixedRouter(self, xPos, yPos, connectionRadius, borderLines):
        fixedRouter = FixedRouter(xPos, yPos, connectionRadius, borderLines)
        self.AddFixedRouter(fixedRouter)
        return fixedRouter
    
    def AddFixedRouter(self, fixedrouter):
        self.fixedRouters.append(fixedrouter)
        self._fixedRouterCount += 1
    
    def RemoveFixedRouter(self, fixedRouter):
        self.fixedRouters.remove(fixedRouter)
        self._fixedRouterCount -= 1

    def CreateAgent(self, xPos, yPos, connectionRadius, borderLines):
        agent = AgentRouter(xPos, yPos, connectionRadius, borderLines)
        AddAgent(self, agent)
        return agent

    def AddAgent(self, agent):
        agent.SetScene(self)
        self.agentRouters.append(agent)
        self._agentCount += 1

    def RemoveAgent(self, agent):
        self.agentRouters.remove(agent)
        self._agentCount -= 1

    def CreateDevice(self):

        xPos = 0
        yPos = 0
        xBias = 0
        yBias = 0

        location = random.randint(0, 3)

        if(location % 2 == 0):
            xPos = random.randint(0, self.columns - 1)
            
            top = random.randint(0, 1)
            if (top):
                yBias = random.random() * 2
            else:
                yBias = random.random() * -2

        else:
            yPos = random.randint(0, self.rows - 1)

            right = random.randint(0, 1)
            if (right):
                xBias = random.random() * -2
            else:
                xBias = random.random() * 2

        device = Device(xPos, yPos)
        device.SetBias(xBias, yBias)
        self.devices.append(device)
        self._deviceCount += 1
        return device

    def AddDevice(self, device):
        device.SetScene(self)
        self.devices.append(device)
        self._deviceCount += 1

    def RemoveDevice(self, device):
        try:
            self.devices.remove(device)
            self._deviceCount -= 1
        except:
            print("Error when trying to remove " + str(device))
