import copy
import math

collisionWithRouter = -2
collisionWithWall = -1
totalCoverageReward = 0
serviceReward = 3
stayReward = 0

class State(object):

    cellDict = {
        "FixedService": False,
        "FixedRouterLocation": False,
        "AgentService": False,
        "DeviceCount": 0}

    def __init__(self, rows, columns, devices, fixedRouters, agentRouters):

        if(rows < 0): rows = 0
        if(columns < 0): columns = 0

        self._rows = rows
        self._columns = columns
        self._devices = devices
        self._fixedRouters = fixedRouters
        self._agentRouters = agentRouters

        self._grid = [copy.deepcopy([copy.deepcopy(self.cellDict) for y in range(columns)]) for x in range(rows)]
        self.devicesServiced = 0
        self.coverage = 0
        self.interference = 0

        self.lastDevicesServiced = 0
        self.lastCoverage = 0
        self.lastInterference = 0

        self.baseReward = 0

    def GetGrid(self):
        return self._grid

    def ParseState(self):

        self.lastDevicesServiced = self.devicesServiced
        self.lastCoverage = self.coverage
        self.lastInterference = self.interference

        self._grid = [copy.deepcopy([copy.deepcopy(self.cellDict) for y in range(self._columns)]) for x in range(self._rows)]
        self.devicesServiced = 0
        self.coverage = 0
        self.interference = 0

        self.baseReward = 0

        for router in self._fixedRouters:
            self._FixedCoverage(router)

        for agent in self._agentRouters:
            self._AgentCoverage(agent)

        for device in self._devices:
            self._CheckDevice(device)

    def GetReward(self, takenAction):

        curCoverageRatio = (self.coverage / (self.interference + self.coverage))
        lastCoverageRatio = 0
        actionReward = 0

        if(takenAction == 0): actionReward = stayReward

        if(self.lastInterference + self.lastCoverage != 0): 
            lastCoverageRatio = (self.lastCoverage / (self.lastInterference + self.lastCoverage))

        curCoverageReward = curCoverageRatio * totalCoverageReward
        curServiceReward = self.devicesServiced * serviceReward
        return self.baseReward + curCoverageReward + curServiceReward + actionReward

    def _VerifyGridLocation(self, column, row):
        if(row < 0 or column < 0 or row >= self._rows or column >= self._columns):
            return False
        return True

    def _AgentCoverage(self, agent):

        collided = False
        
        if(agent.xPos < 0):
            agent.xPos = 0
            collided = True
        elif(agent.xPos >= self._columns):
            agent.xPos = self._columns - 1
            collided = True

        if(agent.yPos < 0):
            agent.yPos = 0
            collided = True
        elif(agent.yPos >= self._rows):
            agent.yPos = self._rows - 1
            collided = True

        if(collided): 
            self.baseReward += collisionWithWall
            print("That is a wall")
        
        x = agent.xPos
        y = agent.yPos
        cRad = agent.connectionRadius

        dia = (2 * cRad) + 1

        if(self._grid[y][x]["FixedRouterLocation"]): self.baseReward += collisionWithRouter

        for xOffset in range(dia):
            for yOffset in range(dia):

                row = (y - cRad) + yOffset
                col = (x - cRad) + xOffset

                if(not self._VerifyGridLocation(col, row)):
                    self.interference += 1
                    continue
                
                xDif = x - col
                yDif = y - row

                distance = math.sqrt((xDif * xDif) + (yDif * yDif)) - 0.5
                
                if(distance <= cRad):
                    self._grid[row][col]["AgentService"] = True

                    if(self._grid[row][col]["FixedService"]):
                        self.interference += 1
                    else:
                        self.coverage += 1
        
        #self.runningReward += (self.coverage / (self.interference + self.coverage)) * totalCoverageReward


    def _CheckDevice(self, device):
        
        col = device.xPos
        row = device.yPos

        #print("%d, %d" % (row, col))

        if(not self._VerifyGridLocation(col, row)):
            return
        
        if(not self._grid[row][col]["FixedService"] and self._grid[row][col]["AgentService"]):
            self.devicesServiced += 1

    def _FixedCoverage(self, router):

        x = router.xPos
        y = router.yPos
        cRad = router.connectionRadius

        self._grid[y][x]["FixedRouterLocation"] = True

        dia = (2 * cRad) + 1

        for xOffset in range(dia):
            for yOffset in range(dia):

                row = (y - cRad) + yOffset
                col = (x - cRad) + xOffset

                if(not self._VerifyGridLocation(col, row)):
                    continue

                xDif = x - col
                yDif = y - row

                distance = math.sqrt((xDif * xDif) + (yDif * yDif)) - 0.5
                
                if(distance <= cRad):
                    self._grid[row][col]["FixedService"] = True