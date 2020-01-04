#!/usr/bin/python

import string
import random
import math

class Graph:
    '''
    A simple class that represents a graph as an NxN matrix of numbers.
    The graph also includes a list of node "names" that are used to
    interpret the contents
    '''

    def __init__(self, nodeNames, randomSeed=None, density=None, symmetry=True, lazy=None):
        '''
        Create a graph of the given size populated with random numbers
        with the given density percentage
        Arguments:
            nodeNames - list of names of nodes, used to create the graph
                        of len(nodeNames) x len(nodeNames)
            randomSeed - int value for repeatable results
            density - float 0.0-1.0   e.g., .7 = 70% filled
            symmetry - boolean indicating whether graph should be
                       symmetrical or not - default is True
            lazy - boolean indicating whether graph should be
                       built as list of X,Y coordinates with distances
                       computed lazily - default is None allowing us to
                       decide based on a threshold
        '''

        _THRESHOLD = 1000  # More nodes than this and we go "lazy"

        self.nodeNames = nodeNames
        self.symmetry = symmetry
#         print lazy
#         print self.nodeNames 

        # If the number of nodes is > some threshold, we're going to 
        # build a "lazy graph" that stores nodes as X,Y coordinates and 
        # computes the edges when necessary. Note that lazy graphs 
        # will ALWAYS be symmetrical and density is 1.0

        if lazy!=True and len(nodeNames) < _THRESHOLD:
            self.lazy = False

            # Allocate the NxN matrix that will hold the edges and fill
            # with None
            self.matrix = [None] * len(nodeNames)
            size = len(nodeNames)
            for i in range(len(nodeNames)):
                self.matrix[i] = [None] * size

            # If they gave us a random seed, then 
            # fill the matrix with lists of random numbers
            if randomSeed:
                for i in range(size):
                    self.matrix[i] = randomIntList(size, randomSeed+i, 100)
          
                # If they gave us a density, go back and eliminate some of the 
                # elements based on the density value
                if density:
                    for i in range(size):
                        for j in range(size):
                            # Pick a random number and if it's greater
                            # than the density value, remove this edge
                            if random.random() > density:
                                self.matrix[i][j] = None

                # If we want symmetry, take the lower-half and copy it to
                # the upper half - this is wastefull to do twice, but I
                # don't care
                if self.symmetry:
                    for i in range(size):
                        for j in range(size):
                            self.matrix[j][i] = self.matrix[i][j]

                # Finally, set the diagonal elements to have 0 distance so
                # there's no cost in going from a vertex to itself
                for i in range(size):
                    self.matrix[i][i] = 0
        else:
            self.lazy = True

            # Allocate a list for the X,Y pairs
            self.matrix = [None]* len(nodeNames)

            # Create a map to use as a cache that we'll populate with edges 
            # as we generate them - the map will be indexed by a pair of
            # vertices
            self.cache = {}

            # If they gave us a random seed, then 
            # fill the matrix with lists of random numbers
            if randomSeed:
                for i in range(size):
                    self.matrix[i] = randomIntList(2, randomSeed+i, 1000)

    def getMatrix(self):
        '''
        Return our matrix attribute
        '''
        return self.matrix


    def getNames(self):
        '''
        Return our nodeNames 
        '''
        return self.nodeNames


    def index(self, nodeName):
        '''
        Return the index into the matrix for this nodeName
        '''
        return self.nodeNames.index(nodeName)


    def size(self):
        '''
        Return the size of the matrix
        '''
        return len(self.matrix)


    def addNode(self, nodeName):
        '''
        Add a new node to the graph with None in the matrix
        
        Arguments:
            nodeName - name of the new node
        '''

        if self.lazy:
            raise NotImplementedError("Can't add to 'lazy' graph")
        
        self.nodeNames.append(nodeName)
        # To each existing row, append a new value
        for list in self.matrix:
            list.append(None)
        # Append a new row
        self.matrix.append([None] * len(self.nodeNames))


    def setAt(self, fromNode, toNode, value):
        '''
        Set the value at fromNode, toNode in the matrix by looking up
        the index of fromNode and toNode and indexing into the matrix.

        Arguments:
            fromNode - the from Node name
            toNode - the to Node name
            value - the value to set in the matrix
        '''

        if self.lazy:
            raise NotImplementedError("Can't set explicit edge in 'lazy' graph")

        self.matrix[self.nodeNames.index(fromNode)][self.nodeNames.index(toNode)] = value


    def setLoc(self, node, coordinates):
        '''
        Set the location of node at X,Y coordinates

        Arguments:
            node - the Node name
            coordinates - (X,Y) coordinates 
        '''

        if not self.lazy:
            raise NotImplementedError("Can't set location in non-'lazy' graph")

        self.matrix[self.nodeNames.index(node)] = coordinates


    def getAt(self, fromNode, toNode):
        '''
        Return the distance between fromNode and toNode 

        Arguments:
            fromNode - the from Node name
            toNode - the to Node name
        Returns:
            distance between nodes
        '''
        # If this is a lazy graph, compute the distance by triangulating
        # between the points using c^2 = a^2 + b^2
        if self.lazy:
            # See if we've already cached a computed value, and 
            # if not, then compute it, and cache it
            if not (self.cache.has_key((fromNode, toNode)) or \
                  (self.symmetry and self.cache.has_key((toNode, fromNode)))):
                (x1, y1) = self.matrix[self.nodeNames.index(fromNode)]
                (x2, y2) = self.matrix[self.nodeNames.index(toNode)]
                self.cache[(fromNode,toNode)] = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            
            # The cache now holds either the to-from edge, or the from-to
            # edge if we're symmetrical. Decide which one and return it
            if self.cache.has_key((fromNode, toNode)):
                return self.cache[(fromNode, toNode)]
            else: 
                # Must be symmetrical and found that edge above so return it
                return self.cache[(toNode, fromNode)]

        else: # Not lazy, index into the matrix and return the value
            return self.matrix[self.nodeNames.index(fromNode)][self.nodeNames.index(toNode)]



    def __str__(self):
        '''
        Displays our contents as an n+1 x n+1 matrix with the first
        row and column holding node names.
        '''
 
        # Format strings and numbers to exactly 10 spaces
        _FMT = '%10.10s'
 
        # Logical [0,0] of display is empty
        result = _FMT % ' '
 
        # First row is node names
        for name in self.nodeNames:
            result += _FMT % name
        result += '\n'
 
        # Following rows are the node name followed by the list of
        # integer values
        i = 0
        for nodeList in self.matrix:
            # Node name
            result += _FMT % self.nodeNames[i]
            i += 1
            # List of integer values
            for node in nodeList:
                result += _FMT % node
            result += '\n'
 
        return result



def fromTSPFile(tspFilename):
    '''
    Builds a Graph object from the data in the TSP file (see
    http://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/
    for file format description)

    Arguments:
        tspFilename - file from TSPLIB
    Returns:
        Graph object populated with data from file
    '''

    # Open the TSP file and read the parameter section.  We need to know
    # whether it's symmetrical (TSP) or aysmmetrical (ATSP) in order to
    # build the graph.  Most of file's parameters are discarded

    tspFile = open(tspFilename)

    # Read in the parameter section and build a dictionary of the values
    parameters = {}
    line = tspFile.readline()
    while line.find(':') >= 0:
        (key, value) = line.split(':')
        parameters[key.strip()] = value.strip()
        line = tspFile.readline()


    # How we handle the data depends on the EDGE_WEIGHT_TYPE.  We'll
    # handle just a couple of types here
    if parameters['EDGE_WEIGHT_TYPE'] not in ['EUC_2D', 'CEIL_2D', 'EXPLICIT']:
        raise NotImplementedError('%s not supported' % parameters['EDGE_WEIGHT_TYPE'])

    elif parameters['EDGE_WEIGHT_TYPE'] in ['EUC_2D', 'CEIL_2D']:
        # Data is given as X,Y points in a plane.  So we have a 'lazy'
        # graph.  Create a 'lazy' graph that has nothing in it
        theGraph = Graph(range(int(parameters['DIMENSION'])))
        locations = []
        coordination = []
        
  
  
        for i in range(theGraph.size()):
            (num, x, y) = tspFile.readline().split()
            locations.append((float(x), float(y)))
            # num is ignored, just append to a list
            coordination.append([i, int(x), int(y)]) 
        for i in range(theGraph.size()): 
            for j in range(theGraph.size()): 
                if i == j:
                    pass
                else:
                    distance = math.sqrt((locations[i][0] - locations[j][0])**2 + (locations[i][1] - locations[j][1])**2)
                    theGraph.setAt(i,j, round(distance)) 
                 
    else:  # Must be an explicit matrix
        # This is a pain as we have to contextually read the list of
        # values depending on one of 9 different formats.  We'll handle
        # only the most common here.
        ####### if parameters['EDGE_WEIGHT_FORMAT'] == 'FULL_MATRIX':
        raise NotImplementedError('%s not supported' % parameters['EDGE_WEIGHT_TYPE'])

    tspFile.close()

    return theGraph, coordination
