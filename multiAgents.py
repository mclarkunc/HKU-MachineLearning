# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        newGhostPositions = successorGameState.getGhostPositions()

        "*** YOUR CODE HERE ***"
         
        foodLocations = []
        

        for x in range(newFood.width):
          for y in range(newFood.height):
            if newFood[x][y] == True:
              foodLocations.append((x,y))

        distToFood = [manhattanDistance(newPos, food) for food in foodLocations]
        if len(distToFood) == 0:
          distToNearFood = 0
        else: 
          distToNearFood = min(distToFood)

        distToGhosts = [manhattanDistance(newPos, gPos) for gPos in newGhostPositions]
        if len(distToGhosts) == 0:
          distToNearGhost = 0
        else:
          distToNearGhost = min(distToGhosts)

        if distToNearFood == 0:
          distToNearFood = 1
        else:
          distToNearFood *= 2
        

        return distToNearGhost/distToNearFood + successorGameState.getScore()
        

def scoreEvaluationFunction(currentGameState):
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
        self.pacmanMove = None

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        
        # Start minimax evaluation with initial depth 0
        minimaxValue = self.getMax(gameState, 0)
        bestMove = self.pacmanMove

        
        return bestMove 


    def getMax(self, myGameState, myDepth):
      if myDepth == self.depth:
        return self.evaluationFunction(myGameState)

      actionList = myGameState.getLegalActions(0)

      if len(actionList) == 0: return self.evaluationFunction(myGameState)

      v = -float("inf")
      
      for action in actionList:
        minValue = self.getMin(myGameState.generateSuccessor(0, action), myDepth, 1)
        if (minValue > v):
          v = minValue
          if (myDepth == 0):
            self.pacmanMove = action

      return v

    def getMin(self, myGameState, myDepth, ghostIndex):
      if myDepth == self.depth:
        return self.evaluationFunction(myGameState)

      ghostActions = myGameState.getLegalActions(ghostIndex)
     
      if len(ghostActions) == 0: return self.evaluationFunction(myGameState)

      if ghostIndex < (myGameState.getNumAgents() - 1):
        nextGhostIndex = ghostIndex + 1
        minValues = [self.getMin(myGameState.generateSuccessor(ghostIndex, gAction), myDepth, nextGhostIndex) for gAction in ghostActions]
        return min(minValues)
      else:
        nextDepth = myDepth + 1
        maxValues = [self.getMax(myGameState.generateSuccessor(ghostIndex, gAction), nextDepth) for gAction in ghostActions]
        return min(maxValues)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        #pacMoves = gameState.getLegalActions(0)
        

        minimaxValue = self.getABMax(gameState, 0, -float("inf"), float("inf"))
        bestMove = self.pacmanMove


        return bestMove #pacMoves[minValues.index(bestMove)]
       


    def getABMax(self, myGameState, myDepth, alpha, beta):
      if myDepth == self.depth:
        return self.evaluationFunction(myGameState)
      
      #Initialize v with negative infinity
      v = -float("inf")

      actionList = myGameState.getLegalActions(0)
      if len(actionList) == 0: return self.evaluationFunction(myGameState)

      for action in actionList:
        v = max(v, self.getABMin(myGameState.generateSuccessor(0, action), myDepth, 1, alpha, beta) )
        if v > beta: return v
        if (myDepth == 0 and v > alpha):
          self.pacmanMove = action
        alpha = max(alpha, v)        
      return v
      

    def getABMin(self, myGameState, myDepth, ghostIndex, alpha, beta):
      if myDepth == self.depth:
        return self.evaluationFunction(myGameState)

      #Initialize v with negative infinity
      v = float("inf")

      ghostActions = myGameState.getLegalActions(ghostIndex)
      
      if len(ghostActions) == 0: return self.evaluationFunction(myGameState)

      if ghostIndex < (myGameState.getNumAgents() - 1):
        for gAction in ghostActions:
          v = min(v, self.getABMin(myGameState.generateSuccessor(ghostIndex, gAction), myDepth, ghostIndex + 1, alpha, beta) )
          if v < alpha: return v
          beta = min(beta, v)
        return v
      else:
        for gAction in ghostActions:
          v = min(v, self.getABMax(myGameState.generateSuccessor(ghostIndex, gAction), myDepth + 1, alpha, beta) )
          if v < alpha: return v
          beta = min(beta, v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        expectimaxValue = self.getExpMax(gameState, 0)
        bestMove = self.pacmanMove
        
        return bestMove


    def getExpMax(self, myGameState, myDepth):
      if myDepth == self.depth:
        return self.evaluationFunction(myGameState)

      actionList = myGameState.getLegalActions(0)

      if len(actionList) == 0: return self.evaluationFunction(myGameState)

      v = -float("inf")

      for action in actionList:
        chanceValue = self.getExpChance(myGameState.generateSuccessor(0, action), myDepth, 1)
        if (chanceValue > v):
          v = chanceValue
          if (myDepth == 0):
            self.pacmanMove = action
          
      return v 

    def getExpChance(self, myGameState, myDepth, ghostIndex):
      if myDepth == self.depth:
        return self.evaluationFunction(myGameState)

      ghostActions = myGameState.getLegalActions(ghostIndex)
      
      if len(ghostActions) == 0: return self.evaluationFunction(myGameState)

      if ghostIndex < (myGameState.getNumAgents() - 1):
        nextGhostIndex = ghostIndex + 1
        chanceValues = [self.getExpChance(myGameState.generateSuccessor(ghostIndex, gAction), myDepth, nextGhostIndex) for gAction in ghostActions]
      else:
        nextDepth = myDepth + 1
        chanceValues = [self.getExpMax(myGameState.generateSuccessor(ghostIndex, gAction), nextDepth) for gAction in ghostActions]

      avgValue = sum(chanceValues) / len(chanceValues)
      return avgValue



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Evaluation function tries to maximize distance to ghosts,
                    minimize the distance to the nearest food pellet, tries to maximize the score,
                    and tries to eliminate Capsules quickly (increasing chances of eating ghosts)

                    I use manhattanDistance to find distance to the ghosts and the food pellet, then
                    I use length of getCapsules (how many Capsules left) and multiply by 1000 to make it 
                    a priority. I multiply current game score by 2 to increase priority on getting a higher score.

    """
    "*** YOUR CODE HERE ***"

    # Useful information you can extract from a GameState (pacman.py)
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    ghostPositions = currentGameState.getGhostPositions()
    capsulePos = currentGameState.getCapsules()

    "*** YOUR CODE HERE ***"
    
    foodLocations = []
    
    for x in range(food.width):
      for y in range(food.height):
        if food[x][y] == True:
          foodLocations.append((x,y))

    distToFood = [manhattanDistance(pos, f) for f in foodLocations]
    if len(distToFood) == 0:
      distToNearFood = 0
    else: 
      distToNearFood = min(distToFood)

    distToGhosts = [manhattanDistance(pos, gPos) for gPos in ghostPositions]
    if len(distToGhosts) == 0:
      distToNearGhost = 0
    else:
      distToNearGhost = min(distToGhosts)

    if distToNearFood == 0:
      distToNearFood = 1
    else:
      distToNearFood *= 2
    
    # If capsule eaten, subtract distance to scared ghosts
    distToAllGhosts = 0
    for i in range (len(distToGhosts)):
      if scaredTimes[i] > distToGhosts[i]:
        distToAllGhosts -= distToGhosts[i]
      else:
        distToAllGhosts += distToGhosts[i]


    return distToAllGhosts - distToNearFood - (1000*len(capsulePos))+ (2 * currentGameState.getScore())


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

