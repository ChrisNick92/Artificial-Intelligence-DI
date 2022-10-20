# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

from custom_functions import expand_tree, tree_node
from custom_functions import get_path

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    # My implementation of GraphSearch with DFS
    # DFS is implemented using a stack 
    fringe = util.Stack() # Initialize an empty stack
    closed = []
    starting_node = tree_node(state = problem.getStartState(),
                              ParentNode=None, Action=None, PathCost=0,
                              Depth=0) # Initialize the Starting node
    fringe.push(starting_node) # Append the starting node in stack
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state): # Then we have found the goal state
            return get_path(node) # Return the path that leads to the goal
        elif node.state not in closed:
            closed.append(node.state)
            fringe = expand_tree(node, fringe, problem, mode = "DFS")
    if fringe.isEmpty():
        print(f"- Search algorithm finished without reaching to a solution.")
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    # My BFS Iplementation of GraphSearch with BFS
    # BFS is implemented using a queue
    fringe = util.Queue() # Initialize an empty queue
    closed = []
    starting_node = tree_node(state = problem.getStartState(),
                              ParentNode=None, Action=None, PathCost=0,
                              Depth=0) # Initialize the Starting node
    fringe.push(starting_node) # Append the starting node in queue
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state): # Then we have found the goal state
            return get_path(node) # Return the path that leads to the goal
        elif node.state not in closed:
            closed.append(node.state)
            fringe = expand_tree(node, fringe, problem, mode = "BFS")
    if fringe.isEmpty():
        print(f"- Search algorithm finished without reaching to a solution.")
     
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    # My Iplementation of uniform-cost graph
    # UCS is implemented using a priorityQueue where the
    # node with the minimum cost path has the highest priority
    
    fringe = util.PriorityQueue() # Initialize an empty priority Queue
    closed = []
    starting_node = tree_node(state = problem.getStartState(),
                              ParentNode=None, Action=None, PathCost=0,
                              Depth=0) # Initialize the Starting node
    fringe.push(starting_node, starting_node.pathcost) # Append the starting node in queue
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state): # Then we have found the goal state
            return get_path(node) # Return the path that leads to the goal
        elif node.state not in closed:
            closed.append(node.state)
            priority = node.pathcost
            fringe = expand_tree(node = node, fringe = fringe, problem = problem, mode = "UCS")
    if fringe.isEmpty():
        print(f"- Search algorithm finished without reaching to a solution.")
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

from util import manhattanDistance


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # My implementation of aStar algorithm
    # We use a queue with function as a data structure
    fringe = util.PriorityQueue() # Initialize an empty priority Queue/L1 distance
    closed = []
    starting_node = tree_node(state = problem.getStartState(),
                              ParentNode=None, Action=None, PathCost=0,
                              Depth=0) # Initialize the Starting node
    priority = starting_node.pathcost+heuristic(starting_node.state, problem)
    fringe.push(starting_node, priority) # Append the starting node in queue
    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state): # Then we have found the goal state
            return get_path(node) # Return the path that leads to the goal
        elif node.state not in closed:
            priority = node.pathcost + heuristic(node.state, problem) # The priority is the sum of pathcost + heuristic
            closed.append(node.state)
            fringe = expand_tree(node = node, fringe = fringe, problem = problem, 
                                 mode = "aStar", heuristic=heuristic)
    if fringe.isEmpty():
        print(f"- Search algorithm finished without reaching to a solution.")
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
