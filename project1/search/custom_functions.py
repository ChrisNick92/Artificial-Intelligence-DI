"""This Python script contains my custom functions
        for Berkley's Project1
"""


class tree_node():
    """
    Custom Class implementing the nodes
    of the search tree for BFS, DFS, UFS etc.
    """
    def __init__(self, state, ParentNode, Action, PathCost,
                 Depth, L1_dist = None):
        self.state = state
        self.parentnode = ParentNode
        self.action = Action
        self.pathcost = PathCost
        self.depth = Depth
        
        
def get_path(node):
    moves = []
    temp_node = node
    while temp_node.parentnode != None:
        moves.append(temp_node.action)
        temp_node = temp_node.parentnode
    return list(reversed(moves))
        
        
def expand_tree(node, fringe, problem, mode = "BFS",
                heuristic = None):
    """Categorical variable mode determines the type of algorithm BFS/DFS/UCS etc"""
    successors = problem.getSuccessors(node.state) # Get successors of current node
    # Push to the data structure
    for successor in successors:
        # Successors has is a triple of the form (state, action, cost)
        temp_node = tree_node(state = successor[0], ParentNode=node,
                              Action=successor[1], PathCost=node.pathcost+successor[2],
                              Depth=node.depth + 1)
        if mode == "BFS" or mode == "DFS":
            fringe.push(temp_node)
        elif mode == "UCS":
            priority = temp_node.pathcost
            fringe.update(temp_node, priority)
        elif mode == "aStar":
            priority = temp_node.pathcost + heuristic(temp_node.state, problem)
            fringe.push(temp_node, priority)
    return fringe

