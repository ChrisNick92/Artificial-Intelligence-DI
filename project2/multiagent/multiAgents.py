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
import math # To use the infinity values

from game import Agent
from pacman import GameState

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
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        total_score = 0
        if newFood != []:
            dist = min([manhattanDistance(newPos, food_pos) for food_pos in newFood])
            total_score += 1/dist
        ghost_distances = []
        blue_ghost_distances = []
        for i,num_moves in enumerate(newScaredTimes):
            if num_moves == 0:
                ghost_distances.append(successorGameState.getGhostPosition(i+1))
            else:
                blue_ghost_distances.append(successorGameState.getGhostPosition(i+1))
        if ghost_distances != []:
            d1 = min([manhattanDistance(newPos, ghostPos) for ghostPos in ghost_distances])
            if d1 <= 2:
                total_score = total_score + d1
        if blue_ghost_distances != []:
            d2 = min([manhattanDistance(newPos, ghostPos) for ghostPos in blue_ghost_distances])
            total_score = total_score + 1/d2
        return total_score + successorGameState.getScore()

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
        action = self.minimax_decision(gameState,self.depth,gameState.getNumAgents(), self.evaluationFunction)
        return action
        util.raiseNotDefined()
    
    """Utility functions for Minimax search"""

    def minimax_decision(self, gameState, depth, num_agents, evalFn):
        _, action = self.max_value(gameState, depth, num_agents, evalFn)
        return action
    
    def max_value(self, gameState, depth, num_agents, evalFn):
        # Pacman makes a move
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return evalFn(gameState), "Stop"
        else:
            v = -math.inf
            for action in gameState.getLegalActions(0):
                v_temp = self.min_value(gameState.generateSuccessor(0, action), depth, num_agents, evalFn, 1)
                if v_temp > v:
                    best_action = action
                    v = v_temp
            return v,best_action

    def min_value(self, gameState, depth, num_agents, evalFn, ghost_index):
        # Enemy agents (ghosts) make their move
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return evalFn(gameState)
        else:
            if ghost_index == num_agents-1: # The last ghost is now playing
                v = math.inf
                for action in gameState.getLegalActions(ghost_index):
                    v_temp,_ = self.max_value(gameState.generateSuccessor(ghost_index, action), depth-1, num_agents, evalFn)
                    if v_temp < v:
                        v = v_temp
                return v
            else:
                v = math.inf
                for action in gameState.getLegalActions(ghost_index):
                    v_temp = self.min_value(gameState.generateSuccessor(ghost_index, action), depth, num_agents, evalFn, ghost_index+1)
                    if v_temp < v:
                        v = v_temp
                return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        action = self.alpha_beta_search(gameState, self.depth, gameState.getNumAgents(), self.evaluationFunction)
        return action
        util.raiseNotDefined()
    
    """Utility functions for alpha-beta search"""
    
    def alpha_beta_search(self, gameState, depth, num_agents, evalFn):
        a = -math.inf
        b = math.inf
        _, action = self.max_value(gameState, depth, num_agents, evalFn, a, b)
        return action
    
    
    def max_value(self, gameState, depth, num_agents, evalFn, a, b):
    # Pacman makes a move
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return evalFn(gameState), "Stop"
        else:
            v = -math.inf
            for action in gameState.getLegalActions(0):
                v_temp = self.min_value(gameState.generateSuccessor(0, action), depth, num_agents,
                                        evalFn, 1, a, b)
                if v_temp > v:
                    best_action = action
                    v = v_temp
                if v > b: return v, action
                a = max(a, v)
            return v,best_action
    
    def min_value(self, gameState, depth, num_agents, evalFn, ghost_index, a, b):
        # Enemy agents (ghosts) make their move
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return evalFn(gameState)
        else:
            if ghost_index == num_agents-1: # The last ghost is now playing
                v = math.inf
                for action in gameState.getLegalActions(ghost_index):
                    v_temp, _ = self.max_value(gameState.generateSuccessor(ghost_index, action), depth-1, num_agents,
                                              evalFn, a , b)
                    if v_temp < v:
                        v = v_temp
                    if v < a: return v
                    b = min(v, b)
                return v
            else:
                v = math.inf
                for action in gameState.getLegalActions(ghost_index):
                    v_temp = self.min_value(gameState.generateSuccessor(ghost_index, action), depth, num_agents, evalFn,
                                            ghost_index+1, a, b)
                    if v_temp < v:
                        v = v_temp
                    if v < a: return v
                    b = min(v, b)
                return v

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
        action = self.expectimax_decision(gameState, self.depth, gameState.getNumAgents(),
                                          self.evaluationFunction)
        return action
        util.raiseNotDefined()
        
    """Utility functions for expectimax"""
    
    def expectimax_decision(self, gameState, depth, num_agents, evalFn):
        _, action = self.max_value(gameState, depth, num_agents, evalFn)
        return action

    
    def max_value(self, gameState, depth, num_agents, evalFn):
        # Pacman makes a move
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return evalFn(gameState), "Stop"
        else:
            v = -math.inf
            for action in gameState.getLegalActions(0):
                v_temp = self.min_value(gameState.generateSuccessor(0, action), depth, num_agents, evalFn, 1)
                if v_temp > v:
                    best_action = action
                    v = v_temp
            return v,best_action
        
    def min_value(self, gameState, depth, num_agents, evalFn, ghost_index):
        # Enemy agents (ghosts) make their move
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return evalFn(gameState)
        else:
            legal_actions = gameState.getLegalActions(ghost_index)
            v = 0
            N = len(legal_actions)
            if ghost_index == num_agents-1: # The last ghost is now playing
                for action in legal_actions:
                    v_temp,_ = self.max_value(gameState.generateSuccessor(ghost_index, action),
                                              depth-1, num_agents, evalFn)
                    v += (1/N)*v_temp
                return v
            else:
                for action in legal_actions:
                    v_temp = self.min_value(gameState.generateSuccessor(ghost_index, action),
                                            depth, num_agents, evalFn, ghost_index+1)
                    v += (1/N)*v_temp
                return v

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food_left = currentGameState.getFood().asList()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    GhostPositions = currentGameState.getGhostPositions()
    capsules = currentGameState.getCapsules()
    currentPos = currentGameState.getPacmanPosition()
    
    weights = {}
    
    evaluation_score = 0
    if food_left != []:
        food_dist = min([manhattanDistance(currentPos, foodPos) for foodPos in food_left])
        weights["food"] = (1/food_dist, 1)
    ghost_distances = []
    white_ghost_distances = []
    for idx, time in enumerate(ScaredTimes):
        if time == 0: ghost_distances.append(GhostPositions[idx])
        else: white_ghost_distances.append((GhostPositions[idx], time))
    if white_ghost_distances != []:
        time, white_ghost_dist = min([(manhattanDistance(currentPos, ghostPos[0]), ghostPos[1]) for ghostPos in white_ghost_distances])
        if time < white_ghost_dist:
            weights["Eat_ghosts"] = ((white_ghost_dist-time)*(1/white_ghost_dist), 40)
    if capsules != []:
        capsule_dist = min([manhattanDistance(currentPos, capsulePos) for capsulePos in capsules])
        weights["capsules"] = (1/capsule_dist, 1)
        
    for val in weights.values():
        evaluation_score += val[0]*val[1]

    return evaluation_score + currentGameState.getScore()
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
