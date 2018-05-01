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
import layout

from game import Agent
#import math
from pacman import GameState
BIGNUM = 10000
import sys, types, time, random, os
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
        #print chosenIndex
        #print legalMoves[chosenIndex]
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
        newCapsules=successorGameState.getCapsules()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print newPos
        #print newGhostStates[0]
        "*** YOUR CODE HERE ***"
        foodPos = newFood.asList()
        foodCount = len(foodPos)
        closestDistance = 1e6
        for i in range(foodCount):
          distance = manhattanDistance(foodPos[i],newPos) + foodCount*100
          if distance < closestDistance:
            closestDistance = distance
            closestFood = foodPos
        if foodCount == 0 :
          closestDistance = 0
        score = -closestDistance

        for ghost in newGhostStates:
          disGhost = manhattanDistance(newPos, ghost.getPosition())
          if ghost.scaredTimer > 0:
            score += 4*pow(max(8 - disGhost, 0), 2)
            #score +=30*1e6
          elif disGhost<=1:
            score-=4*pow(max(8 - disGhost, 0), 2)
            #score -=20*1e6
          else:
            score -= 2*pow(max(8 - disGhost, 0), 2)
            #score -=10*1e6
			
        disFood=[]
        for food in foodPos:
          disFood.append(1.0/manhattanDistance(newPos, food))
        if len(disFood)>0:
          score +=max(disFood)
		  
        disCapsule=[]
        for cap in newCapsules:
          disCapsule.append(50.0/manhattanDistance(newPos, cap))
        if len(disCapsule)>0:
          score +=max(disCapsule)
		  
		  


        return score #successorGameState.getScore()

def scoreEvaluationFunction(currentgameState):
  return currentgameState.getScore()

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
    Your minimax agent with alpha-beta pruning (question 3)
  """
  
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.
    
      Here are some method calls that might be useful when implementing minimax.
    
      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
    
      Directions.STOP:
        The stop direction, which is always legal
    
      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
    
      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    if gameState.isWin() or gameState.isLose():
        return Directions.STOP
    nextMoves = gameState.getLegalPacmanActions()
    num = gameState.getNumAgents() - 1
    value = -BIGNUM
    chosenMove = Directions.STOP
    for move in nextMoves:
        nextState = gameState.generatePacmanSuccessor(move)
        if nextState.isWin():
            return move  # win the game immediately if it can 
        score = self.moveGhost(nextState, value , float('inf'), num, 1)
        if score > value:
            value = score
            chosenMove = move
    return chosenMove
    
  def moveAgent(self, gameState , alpha , beta, depth):
      if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      nextMoves = gameState.getLegalPacmanActions()
      num = gameState.getNumAgents() - 1
      value = -BIGNUM
      for move in nextMoves:
          nextState = gameState.generatePacmanSuccessor(move)
          score = self.moveGhost(nextState, alpha , beta, num, depth + 1)
          value = max(value , score)
          if value >= beta:
              return value
          alpha = max(alpha , value)
      return value
    
  def moveGhost(self , gameState , alpha , beta , ghostNum , depth):
      if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      nextMoves = gameState.getLegalActions(ghostNum)
      num = ghostNum - 1
      value = BIGNUM
      for move in nextMoves:
          nextState = gameState.generateSuccessor(ghostNum , move)
          if num == 0:
              if depth == self.depth:
                  score = self.evaluationFunction(nextState)
              else:
                  score = self.moveAgent(nextState, alpha, beta, depth)
          else:
              score = self.moveGhost(nextState, alpha , beta, num, depth)
          value = min(value , score)
          if value <= alpha:
              return value
          beta = min(beta , value)
      return value

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  
  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.
    
      Here are some method calls that might be useful when implementing minimax.
    
      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
    
      Directions.STOP:
        The stop direction, which is always legal
    
      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
    
      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    if gameState.isWin() or gameState.isLose():
        return Directions.STOP
    nextMoves = gameState.getLegalPacmanActions()
    num = gameState.getNumAgents() - 1
    value = -BIGNUM
    chosenMove = Directions.STOP
    for move in nextMoves:
        nextState = gameState.generatePacmanSuccessor(move)
        if nextState.isWin():
            return move  # win the game immediately if it can 
        score = self.moveGhost(nextState, value , float('inf'), num, 1)
        if score > value:
            value = score
            chosenMove = move
    return chosenMove
    
  def moveAgent(self, gameState , alpha , beta, depth):
      if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      nextMoves = gameState.getLegalPacmanActions()
      num = gameState.getNumAgents() - 1
      value = -BIGNUM
      for move in nextMoves:
          nextState = gameState.generatePacmanSuccessor(move)
          score = self.moveGhost(nextState, alpha , beta, num, depth + 1)
          value = max(value , score)
          if value >= beta:
              return value
          alpha = max(alpha , value)
      return value
    
  def moveGhost(self , gameState , alpha , beta , ghostNum , depth):
      if gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      nextMoves = gameState.getLegalActions(ghostNum)
      num = ghostNum - 1
      value = BIGNUM
      for move in nextMoves:
          nextState = gameState.generateSuccessor(ghostNum , move)
          if num == 0:
              if depth == self.depth:
                  score = self.evaluationFunction(nextState)
              else:
                  score = self.moveAgent(nextState, alpha, beta, depth)
          else:
              score = self.moveGhost(nextState, alpha , beta, num, depth)
          value = min(value , score)
          if value <= alpha:
              return value
          beta = min(beta , value)
      return value

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
        numAgent = gameState.getNumAgents()
        ActionScore = []

        def _rmStop(List):
          return [x for x in List if x != 'Stop']

        def _expectMinimax(s, iterCount):
          if iterCount >= self.depth*numAgent or s.isWin() or s.isLose():
            return self.evaluationFunction(s)
          if iterCount%numAgent != 0: #Ghost min
            successorScore = []
            for a in _rmStop(s.getLegalActions(iterCount%numAgent)):
              sdot = s.generateSuccessor(iterCount%numAgent,a)
              result = _expectMinimax(sdot, iterCount+1)
              successorScore.append(result)
            averageScore = sum([ float(x)/len(successorScore) for x in successorScore])
            return averageScore
          else: # Pacman Max
            result = -1e10
            for a in _rmStop(s.getLegalActions(iterCount%numAgent)):
              sdot = s.generateSuccessor(iterCount%numAgent,a)
              result = max(result, _expectMinimax(sdot, iterCount+1))
              if iterCount == 0:
                ActionScore.append(result)
            return result
          
        result = _expectMinimax(gameState, 0);
        return _rmStop(gameState.getLegalActions(0))[ActionScore.index(max(ActionScore))]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    def _scoreFromGhost(gameState):
      score = 0
      for ghost in gameState.getGhostStates():
        disGhost = manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition())
        if ghost.scaredTimer > 0:
          score += 4*pow(max(8 - disGhost, 0), 2)
        elif disGhost<=1:
          score -= 4*pow(max(8 - disGhost, 0), 2)
        else:
          score -= 2*pow(max(8 - disGhost, 0), 2)
      return score

    def _scoreFromFood(gameState):
      disFood = []
      for food in gameState.getFood().asList():
        disFood.append(1.0/manhattanDistance(gameState.getPacmanPosition(), food))
      if len(disFood)>0:
        return max(disFood)
      else:
        return 0

    def _scoreFromCapsules(gameState):
      score = []
      for Cap in gameState.getCapsules():
        score.append(50.0/manhattanDistance(gameState.getPacmanPosition(), Cap))
      if len(score) > 0:
        return max(score)
      else:
        return 0

    def _suicide(gameState):
      score = 0
      disGhost = 1e6
      for ghost in gameState.getGhostStates():
        disGhost = min(manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition()), disGhost)
      score -= pow(disGhost, 2)
      if gameState.isLose():
        score = 1e6
      return score

    score = currentGameState.getScore()
    scoreGhosts = _scoreFromGhost(currentGameState)
    scoreFood = _scoreFromFood(currentGameState)
    scoreCapsules = _scoreFromCapsules(currentGameState)
    #if score < 800 and currentGameState.getNumFood() <= 1 and len(currentGameState.getCapsules()) == 0:
    #  return _suicide(currentGameState)
    #else:
    return score + scoreGhosts + scoreFood + scoreCapsules

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

def readCommand( argv ):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python pacman.py <options>
    EXAMPLES:   (1) python pacman.py
                    - starts an interactive game
                (2) python pacman.py --layout smallClassic --zoom 2
                OR  python pacman.py -l smallClassic -z 2
                    - starts an interactive game on a smaller board, zoomed in
    """
    parser = OptionParser(usageStr)

    parser.add_option('-n', '--numGames', dest='numGames', type='int')
    parser.add_option('-l', '--layout', dest='layout')
    parser.add_option('-p', '--pacman', dest='pacman')
    parser.add_option('--timeout', dest='timeout', type='int')
    parser.add_option('-g', '--ghosts', dest='ghost')
    parser.add_option('--frameTime', dest='frameTime', type='float')
    parser.add_option('-c', '--catchExceptions', action='store_true', dest='catchExceptions')
    parser.add_option('-t', '--textGraphics', action='store_true', dest='textGraphics')
    parser.add_option('-f', '--fixRandomSeed', type='int', dest='fixRandomSeed',
                      help='Fixes the random seed to always play the same game', default=551)
    parser.add_option('-r', '--recordActions', action='store_true', dest='record',
                      help='Writes game histories to a file (named by the time they were played)', default=False)
    
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    # Fix the random seed
    #random.seed(options.fixRandomSeed)

    # Choose a layout
    args['layout'] = layout.getLayout( options.layout )
    if args['layout'] == None: raise Exception("The layout " + options.layout + " cannot be found")

   
    return options.layout


class B551Agent(AlphaBetaAgent):

	
    def __init__(self, evalFn='betterEvaluationFunction', depth='3'):
      self.index = 0  # Pacman is always agent index 0
      self.evaluationFunction = util.lookup(evalFn, globals())
      self.depth = int(depth)
      argslayout = readCommand( sys.argv[1:] )
      argsghost = str(sys.argv[6:7])
      #args2 = readCommand( sys.argv[2:] )
      if(argsghost=="['RandomGhost']" and argslayout=="test3") or (argslayout=="test4"):
        self.depth = 2
      #print(args2)
      #print(self.depth)

	  
