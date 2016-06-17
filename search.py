# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    directionList = []          # Initialize empty direction list
    exploredSet = []            # Initialize exploredSet as an empty list
    frontier = util.Stack()     # Define frontier as a Stack

    # The frontier will be a Stack of 3-tuples in the form of (position, direction, cost)
    # Initialize frontier with Start State, which has no direction or cost
    startPath = [(problem.getStartState(), None, 0)]
    frontier.push(startPath)
    
    while (not frontier.isEmpty()):

        # While frontier is not empty, remove leaf node (last in) from frontier
        leaf = frontier.pop()
        
        # If coordinates of last element in leaf node is the goal state, return the directionList
        if (problem.isGoalState(leaf[-1][0])): 
                       
            # Direction is the 2nd item in each tuple in the leaf list
            for leafItem in leaf[1:]:               #Skip first item, as that is the Start position
                directionList.append(leafItem[1])
            
            return directionList

        # Else, add leaf's successors to path and add to frontier (if leaf is not aleady in explored list)
        if (not (leaf[-1][0] in exploredSet)):
            exploredSet.append(leaf[-1][0])
            succList = problem.getSuccessors(leaf[-1][0])
            for succ in succList:
                newPath = list(leaf)    # Make a copy of current leaf
                newPath.append(succ)    # Append successor to current path 
                frontier.push(newPath)  # Add new path to the frontier

    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"

    directionList = []          # Initialize empty direction list
    exploredSet = []            # Initialize exploredSet as an empty list
    frontier = util.Queue()     # Define frontier as a Queue

    # The frontier will be a Queue of 3-tuples in the form of (position, direction, cost)
    # Initialize frontier with Start State, which has no direction or cost
    startPath = [(problem.getStartState(), None, 0)]
    frontier.push(startPath)
    
    while (not frontier.isEmpty()):

        # While frontier is not empty, remove leaf node (first in) from frontier
        leaf = frontier.pop()
        
        # If coordinates of last element in leaf node is the goal state, return the directionList
        if (problem.isGoalState(leaf[-1][0])): 
                       
            # Direction is the 2nd item in each tuple in the leaf list
            for leafItem in leaf[1:]:               #Skip first item, as that is the Start position
                directionList.append(leafItem[1])
            
            return directionList

        # Else, add leaf's successors to path and add to frontier (if leaf is not aleady in explored list)
        if (not (leaf[-1][0] in exploredSet)):
            exploredSet.append(leaf[-1][0])
            succList = problem.getSuccessors(leaf[-1][0])
            for succ in succList:
                newPath = list(leaf)    # Make a copy of current leaf
                newPath.append(succ)    # Append successor to current path 
                frontier.push(newPath)  # Add new path to the frontier


    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    directionList = []          # Initialize empty direction list
    exploredSet = []            # Initialize exploredSet as an empty list
    
    # Define frontier as a PriorityQueue that calls
    # GetCost each time an object is pushed to get priority 
    frontier = util.PriorityQueueWithFunction(getCost)      
                                                            
    # The frontier will be a Queue of 3-tuples in the form of (position, direction, cost)
    # Initialize frontier with Start State, which has no direction or cost
    startPath = [(problem.getStartState(), None, 0)]
    frontier.push(startPath)
    
    while (not frontier.isEmpty()):

        # While frontier is not empty, remove leaf node (lowest priority) from frontier
        leaf = frontier.pop()
        
        # If coordinates of last element in leaf node is the goal state, return the directionList
        if (problem.isGoalState(leaf[-1][0])): 
                       
            # Direction is the 2nd item in each tuple in the leaf list
            for leafItem in leaf[1:]:               #Skip first item, as that is the Start position
                directionList.append(leafItem[1])
            
            return directionList

        # Else, add leaf's successors to path and add to frontier (if leaf is not aleady in explored list)
        if (not (leaf[-1][0] in exploredSet)):
            exploredSet.append(leaf[-1][0])
            succList = problem.getSuccessors(leaf[-1][0])
            for succ in succList:
                newPath = list(leaf)    # Make a copy of current leaf
                newPath.append(succ)    # Append successor to current path 
                frontier.push(newPath)  # Add new path to the frontier      

    util.raiseNotDefined()


def getCost(path):
    cost = 0
    for item in path:
        cost += item[2]

    return cost


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    directionList = []          # Initialize empty direction list
    exploredSet = []            # Initialize exploredSet as an empty list 
    frontier = util.PriorityQueue() # Define frontier as a PriorityQueue      

    # Initialize frontier with Start State, which has no direction or cost
    startPath = [(problem.getStartState(), None, 0)]
    # Priority for the queue is path cost (0 for start state) + heuristic value of the start state
    frontier.push(startPath, heuristic(startPath[0][0],problem))
    
    while (not frontier.isEmpty()):

        # while frontier is not empty, remove leaf node (lowest priority) from frontier
        leaf = frontier.pop()
          
        # If coordinates of last element in list is the goal state, return the directionList
        if (problem.isGoalState(leaf[-1][0])): 
            
            # The Direction is the 2nd item in each tuple in the leaf list
            for leafItem in leaf[1:]:               #Skip first item, as that is the Start position
                directionList.append(leafItem[1])
            
            return directionList

        # Else, add leaf's successors to path and add to frontier (if leaf is not aleady in explored list)
        if (not (leaf[-1][0] in exploredSet)):
            exploredSet.append(leaf[-1][0])
            succList = problem.getSuccessors(leaf[-1][0])
            for succ in succList:
                newPath = list(leaf)
                newPath.append(succ)
                # Priority for the queue is path cost + heuristic value of the successor
                aStarCost = getCost(newPath) + heuristic(succ[0],problem)     
                frontier.push(newPath, aStarCost)
                
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
