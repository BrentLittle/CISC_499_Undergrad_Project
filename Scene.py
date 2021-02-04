class Scene():

    _fixedRouterCount = 0
    _agentCount = 0
    _deviceCount = 0

    def __init__(self, columns, rows):

        self.fixedRouters = []
        self.agentRouters = []
        self.devices = []

        self.columns = columns
        self.rows = rows

    def CreateAgent(self, xPos, yPos, connectionRadius, borderLines):
        agent = new AgentRouter(xPos, yPos, connectionRadius, borderLines)

    def AddAgent(self, agent):
        self.agentRouters.append(agent)
        _agentCount++
