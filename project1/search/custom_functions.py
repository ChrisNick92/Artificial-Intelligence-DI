"""This Python script contains my custom functions
        for Berkley's Project1
"""


class tree_node():
    """
    Custom Class implementing the nodes
    of the search tree for BFS, DFS, UFS etc.
    """
    def __init__(self, state, ParentNode, Action, PathCost,
                 Depth):
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
        
        
def expand_tree(node, fringe, problem):
    """This is implemented only for DFS - Stack data structure"""
    successors = problem.getSuccessors(node.state) # Get successors of current node
    # Push to the data structure
    for successor in successors:
        # Successors has is a triple of the form (state, action, cost)
        temp_node = tree_node(state = successor[0], ParentNode=node,
                              Action=successor[1], PathCost=node.pathcost+1,
                              Depth=node.depth + 1)
        fringe.push(temp_node)
        
    return fringe