# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

HIGH_BLOCK = 1000

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foods = newFood.asList()  
        closestFood = HIGH_BLOCK
        closestGhost = HIGH_BLOCK    
            
        for i in foods:
            closestFood = min(closestFood, manhattanDistance(i, newPos))
        if not foods:
            closestFood = 0       
        for ghostState in newGhostStates:
            getGhostPos = ghostState.getPosition()
            ghostA, ghostB = getGhostPos
            ghostA = int(ghostA)
            ghostB = int(ghostB)
            ghostPos = (ghostA, ghostB)
            if ghostState.scaredTimer == 0:
                closestGhost = min(closestGhost, manhattanDistance(ghostPos, newPos))     
        Score = successorGameState.getScore() - ((closestFood/3) + (7/(closestGhost+1)))
        return Score



def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"   
        agentIndex = 0   
        depth=self.depth
        return self.search(gameState, agentIndex, depth)[1]
    
    def search(self, gameState, agentIndex, depth):
        if depth != 0 and gameState.isLose() is False and gameState.isWin() is False:
            if agentIndex > 0:
                searchVal = self.min(gameState, agentIndex, depth)
            else:
                searchVal = self.max(gameState, agentIndex, depth)
        else:
            searchVal = self.evaluationFunction(gameState), Directions.STOP
        return searchVal

    def min(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        minAction = Directions.STOP
        minVal = HIGH_BLOCK
        
        if agentIndex < gameState.getNumAgents() - 1:
            nextAgent = agentIndex + 1
            nextDepth = depth    
        else:
            nextAgent = 0
            nextDepth = depth - 1
        for i in actions:
            newVal = self.search(gameState.generateSuccessor(agentIndex, i), nextAgent, nextDepth)[0]
            if minVal >= newVal:
                minVal = newVal
                minAction = i
        return minVal, minAction

    def max(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        maxAction = Directions.STOP
        maxVal = -HIGH_BLOCK
     
        if agentIndex < gameState.getNumAgents() - 1:
            nextAgent = agentIndex + 1
            nextDepth = depth
        else:
            nextAgent = 0
            nextDepth = depth - 1
        for i in actions:
            newVal = self.search(gameState.generateSuccessor(agentIndex, i), nextAgent, nextDepth)[0]
            if maxVal <= newVal:
                maxVal = newVal
                maxAction = i
        return maxVal, maxAction
        #util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.search(gameState, 0, self.depth, -HIGH_BLOCK, HIGH_BLOCK)[1]

    def search(self, gameState, agentIndex, depth, alpha, beta):
        if depth != 0 and gameState.isWin() is False and gameState.isLose() is False:
            if agentIndex > 0:
                searchVal = self.searchB(gameState, agentIndex, depth, alpha, beta)
            else:
                searchVal = self.searchA(gameState, agentIndex, depth, alpha, beta) 
        else:
            searchVal = self.evaluationFunction(gameState), Directions.STOP
        return searchVal

    def searchA(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        maxVal = -HIGH_BLOCK
        maxAction = Directions.STOP
        
        if agentIndex < gameState.getNumAgents() - 1:
            nextAgent, nextDepth = agentIndex + 1, depth
        else:
            nextAgent = 0
            nextDepth = depth - 1       
        for i in actions:
            newVal = self.search(gameState.generateSuccessor(agentIndex, i), nextAgent, nextDepth, alpha, beta)[0]
            if maxVal <= newVal:
                maxVal = newVal
                maxAction = i
            if beta < newVal:
                return newVal, i
            else:
                alpha = max(alpha, maxVal)
        return maxVal, maxAction
    
    def searchB(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        minVal = HIGH_BLOCK
        minAction = Directions.STOP
        
        if agentIndex < gameState.getNumAgents() - 1:
            nextAgent = agentIndex + 1
            nextDepth = depth
        else:
            nextAgent = 0
            nextDepth = depth - 1
        for i in actions:
            newVal = self.search(gameState.generateSuccessor(agentIndex, i), nextAgent, nextDepth, alpha, beta)[0]
            if minVal >= newVal:
                minVal = newVal
                minAction = i
            if alpha > newVal:
                return newVal, i
            else:
                beta = min(beta, minVal)
        return minVal, minAction  
        #util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.search(gameState, 0, self.depth)[1]

    def search(self, gameState, agentIndex, depth):
        if depth != 0 and gameState.isWin() is False and gameState.isLose() is False:
            if agentIndex > 0:
                searchVal = self.searchExpct(gameState, agentIndex, depth)
            else:
                searchVal = self.searchMax(gameState, agentIndex, depth)
        else:    
            searchVal = self.evaluationFunction(gameState), Directions.STOP
        return searchVal

    def searchMax(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        maxVal = -HIGH_BLOCK
        maxAction = Directions.STOP
        
        if agentIndex < gameState.getNumAgents() - 1:    
            nextAgent = agentIndex + 1
            nextDepth = depth
        else:
            nextAgent = 0
            nextDepth = depth - 1
        for i in actions:
            nextVal = self.search(gameState.generateSuccessor(agentIndex, i), nextAgent, nextDepth)[0]
            if maxVal < nextVal:
                maxVal = nextVal
                maxAction = i
        return maxVal, maxAction

    def searchExpct(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        expctVal = 0
        expctAction = Directions.STOP
        
        if agentIndex < gameState.getNumAgents() - 1:
            nextAgent = agentIndex + 1
            nextDepth = depth
        else:
            nextAgent = 0
            nextDepth = depth - 1
        for i in actions:
            expctVal += self.search(gameState.generateSuccessor(agentIndex, i), nextAgent, nextDepth)[0]
        expctVal = expctVal/len(actions)
        return expctVal, expctAction
        #util.raiseNotDefined()




def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"  
    currPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    closestFood = HIGH_BLOCK
    currGhostStates = currentGameState.getGhostStates()  
    closestGhost = HIGH_BLOCK
    for i in foods:
        closestFood = min(closestFood, manhattanDistance(i, currPos))
    if not foods:
        closestFood = 0
    for i in currGhostStates:
        ghostA, ghostB = i.getPosition()
        ghostA, ghostB = int(ghostA), int(ghostB)
        if i.scaredTimer > 0:
            closestGhost = -8
        else:
            closestGhost = min(closestGhost, manhattanDistance((ghostA, ghostB), currPos))
    score = currentGameState.getScore() - ((closestFood/3) +(7/(closestGhost+1)))
    return score
    #util.raiseNotDefined()
# Abbreviation
better = betterEvaluationFunction

