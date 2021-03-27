import pygame
import random

import math as m

SPACE_INIT_VALUE = 0                                                    # The value we use to init state action pairs in the Q table

GAMMA = 0.8                                                             # The discount value
ALPHA = 0.8                                                             # The the learning rate
epsilon = 0.4                                                          # The exploration rate
MAX_EPISODES = 35000                                                    # The iterations we use to determine convergence
PLANNING_STEPS = 50                                                      # The number of planning steps we take
EPSILON_DECAY = 0.95
EPSILON_DECAY_FREQUENCY = 1000

ACTION_SET = [0, 1, 2, 3, 4]

Q_FILENAME = "policy.txt"

class AgentRouter(pygame.sprite.Sprite):

#                         r    g    b    a
    COLOUR            = (230, 184,   0, 255)
    CONNECTION_COLOUR = (255, 224, 102,  50)

    def __init__(self, xPos, yPos, connectionRadius, importPolicy):
        self.xPos = round(xPos)
        self.yPos = round(yPos)
        self.connectionRadius = connectionRadius
        self.radius = 12
        self.scene = None
        self.observedReward = 0
        self.currentState = [self.xPos, self.yPos]
        self.nextState = [self.xPos, self.yPos]
        self.actionTaken = [0]
        self.exploring = True
        self.stepCounter = 0

        self.Q = {GetHash(self.currentState) : [SPACE_INIT_VALUE for x in range(len(ACTION_SET))]}
        self.model = {GetHash(self.currentState) : [[] for x in range(len(ACTION_SET))]}
        self.visitedStates = {}

        if (importPolicy) :
            #self.Q = ImportQTable(Q_FILENAME)
            #self.model = CreateModel(self.Q)
            print("This needs to be implemented")
        else :
            self.Q = AddState(self.Q, self.currentState)
            self.model = AddModel(self.model, self.currentState)

        # If our next state is not in the Q table, then add it to both the Q table and the model
        if(self.Q.get(GetHash(self.currentState)) == None) :
            self.Q = AddState(self.Q, self.currentState)
            self.model = AddModel(self.model, self.currentState)

    def SetScene(self, scene):
        self.scene = scene

    def Update(self):
        
        self.actionTaken = SelectNextAction(self.Q, self.currentState, self.exploring)
        wishState = GetNextState(self.currentState, self.actionTaken);

        self.xPos = wishState[0]
        self.yPos = wishState[1]

        return

    def StepQ(self, reward):
        
        boardHash = GetHash(self.currentState)

        self.nextState = [self.xPos, self.yPos]

        # If our next state is not in the Q table, then add it to both the Q table and the model
        if(self.Q.get(GetHash(self.nextState)) == None) :
            self.Q = AddState(self.Q, self.nextState)
            self.model = AddModel(self.model, self.nextState)

        self.Q = UpdateQ(self.Q, self.currentState, self.actionTaken, reward, self.nextState) # Update the Q table
        self.model[boardHash][self.actionTaken] = [reward, self.nextState] # Update the model

        print(self.Q.get(GetHash(self.currentState)))

        # Planning steps
        for n in range(PLANNING_STEPS) :

            if(self.visitedStates == {}) : break # If there are no previously visited states action pairs, then we want to break

            keyList = list(self.visitedStates.keys())
            
            chosenStateAction = keyList[random.randint(0, len(keyList) - 1)] # Randomly get the index for a state action pair
            s1 = self.visitedStates[chosenStateAction][0] # Get the state
            a1 = self.visitedStates[chosenStateAction][1] # Get the action

            observedReward = self.model[GetHash(s1)][a1][0] # Observe the reward
            sPrime = self.model[GetHash(s1)][a1][1] # Observe the next state

            # If our next state is not in the Q table, then add it to both the Q table and the model
            if(self.Q.get(GetHash(sPrime)) == None) :
                self.Q = AddState(self.Q, sPrime)
                self.model = AddModel(self.model, sPrime)

            self.Q = UpdateQ(self.Q, s1, a1, observedReward, sPrime) # Update the Q table

        self.visitedStates[GetHash([self.currentState, self.actionTaken])] = [self.currentState, self.actionTaken] # append our state to the visited states

        self.currentState = [self.nextState[0], self.nextState[1]]# update our current state

        self.stepCounter += 1
        if(self.stepCounter == EPSILON_DECAY_FREQUENCY):
            self.stepCounter = 0
            global epsilon 
            epsilon = epsilon * EPSILON_DECAY

            print("******************************************************************************************************************************************")

    
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

    def SetPosition(self, newX, newY):

        self.xPos = newX
        self.yPos = newY

        self.currentState = [newX, newY]

        # If our next state is not in the Q table, then add it to both the Q table and the model
        if(self.Q.get(GetHash(self.currentState)) == None) :
            self.Q = AddState(self.Q, self.currentState)
            self.model = AddModel(self.model, self.currentState)




def ImportQTable(fileName):
    return None

def CreateModel(Q):
    return None

# Updates the Q table when given a current state, action, reward and the next state
def UpdateQ(Q, currentState, action, reward, nextState):

    boardHash = GetHash(currentState) # Gets the board hash

    currentQ = Q[boardHash][action] # Get the value of the current state action pair
    maxAction = SelectNextAction(Q, nextState, False) # Find which action has the maximum value for the next state
    nextQ = 0

    if (maxAction != None) : nextQ = -Q[GetHash(nextState)][maxAction] # Get the value of the next state

    Q[boardHash][action] = currentQ + (ALPHA * (reward + (GAMMA * nextQ) - currentQ)) # Update the Q table

    return Q # return the Q table

# The policy for selecting the next state
def SelectNextAction(Q, currentState, willExplore):

    actionValues = Q[GetHash(currentState)] # Get the value of each action

    # If we decide to explore this time, then just choose a random action
    if (willExplore and random.random() < epsilon) : return ACTION_SET[random.randint(0, len(ACTION_SET) - 1)]

    if (len(ACTION_SET) == 0) : return None

    validActions = [ACTION_SET[0]] # Initialize our set of valid actions

    # Loop through all of the actions
    for i in range(len(ACTION_SET)) :

        # If the Q value of the current action is greater then the Q value of the valid actions
        if (actionValues[ACTION_SET[i]] > actionValues[validActions[0]]) : 
            validActions = [ACTION_SET[i]] # Set the set of valid actions to just be the current action

        # if our current action has an equal Q value to our valid actions
        elif (actionValues[ACTION_SET[i]] == actionValues[validActions[0]]) : 
            validActions.append(ACTION_SET[i]) # add the current action to the list of valid actions

    return validActions[random.randint(0, len(validActions) - 1)] # Pick a random action that is valid

# Adds a new state to the model hash table
def AddModel(Model, state):

    actionValues = [[] for x in range(len(ACTION_SET))]
    Model[GetHash(state)] = actionValues

    return Model

# Adds a new state to the Q hash table
def AddState(Q, state):

    actionValues = [SPACE_INIT_VALUE for x in range(len(ACTION_SET))]
    Q[GetHash(state)] = actionValues

    return Q

def GetNextState(currentState, actionTaken):
    xPos = currentState[0]
    yPos = currentState[1]

    if(actionTaken == 0):
        return currentState
    elif(actionTaken == 1):
        yPos -= 1
    elif(actionTaken == 2):
        xPos += 1
    elif(actionTaken == 3):
        yPos += 1
    elif(actionTaken == 4):
        xPos -= 1

    return [xPos, yPos]

# Returns the hash of a given state
def GetHash(state):
    return str(state) # In this case we found that just turning the state into a string was good enough