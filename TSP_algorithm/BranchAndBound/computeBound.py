######################
# 1300374
# 
# This file is included by the TSPNode class to provide a definition for
# the computeBound method
######################

def computeBound(self):
    '''
    Returns a lowerbound on the optimal tour for this node
    '''
    # Use getAt to find distance between nodes
    # Sum of shortest individual paths from each node
    shortest = 0
    for name1 in self.state.nodeNames:
        short = None
        if name1 not in self.path:
            for name2 in self.state.nodeNames:
                if name2 not in self.path and name1 != name2:
                    if short == None or self.state.getAt(name1, name2) < short:
                        short = self.state.getAt(name1, name2)
        if short:
            shortest += short
    return (shortest + self.path_length)
