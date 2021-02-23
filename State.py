import copy
import math

class State(object):

    cellDict = {
        "FixedService": False,
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

        self.ParseState()

    def GetGrid(self):
        return self._grid

    def ParseState(self):

        for router in self._fixedRouters:
            self._FixedCoverage(router)

        for agent in self._agentRouters:
            self._AgentCoverage(agent)

        for device in self._devices:
            self._CheckDevice(device)

    def _VerifyGridLocation(self, column, row):
        if(row < 0 or column < 0 or row >= self._rows or column >= self._columns):
            return False
        return True

    def _AgentCoverage(self, agent):

        x = agent.xPos
        y = agent.yPos
        cRad = agent.connectionRadius

        minX = x - cRad
        minY = y - cRad
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
                    self._grid[row][col]["AgentService"] = True

                    if(self._grid[row][col]["FixedService"]):
                        self.interference += 1
                    else:
                        self.coverage += 1

    def _CheckDevice(self, device):
        
        col = device.xPos
        row = device.yPos

        #print("%d, %d" % (row, col))

        if(not self._VerifyGridLocation(col, row)):
            return
        
        if(self._grid[row][col]["AgentService"]):
            self.devicesServiced += 1

    def _FixedCoverage(self, router):

        x = router.xPos
        y = router.yPos
        cRad = router.connectionRadius

        minX = x - cRad
        minY = y - cRad
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