"""
Karl Fezer
10/3/2016
STILL IN PROGRESS

1.       Design a quad tree to store elevation data for a given (lat, lon) coordinate.
 
Include the ability to:
a.       find N nearest neighbour (lat, lon, elevation) tuples for a given coordinate.
b.       find all (lat, lon, elevation) tuples in a given bounding box.
c.       Specify the depth of the tree
d.       Print the tree structure


This is broken up into 2 classes, one representing the Nodes themselves and one performing the QuadTree structure
and operations
"""

import sys
import queue

class Node:
    #Node is one individual node on the QuadTree
    #Nodes are devided into 3 types, root, which only has children, and branches and leaves
    ROOT = "root"
    BRANCH = "branch"
    LEAF = "leaf"
    MAXCHILDREN = 4

    #NOTE, CAN ONLY STORE POSITIONS AT X,Y COORDINATES. Does not handle multiple elevations

    #Branches are only created once it has 4 leaves. A tree starts with a root, 4 branches, 0 leaves
    #Branches only hold data for the range of the leaves they contain
    def __init__(self, parent, rect, x, y, elevation):
        self.parent = parent
        self.children = [None,None,None,None]
        if parent == None:
            self.depth = 0
        else:
            self.depth = parent.depth + 1
        #create a root
        if self.parent == None:
            print("ROOT CREATED")
            self.type = Node.ROOT
            self.rect = rect
            #Creates 4 child branches for root
            self.subDivide()
            self.numbOfChild = 4
        #create a leaf
        elif rect == None:
            self.type = Node.LEAF
            self.x = x
            self.y = y
            self.elevat = elevation
            self.numbOfChild = 0
            self.children = [None, None, None, None]
        #create a branch
        else:
            self.numbOfChild = 0
            self.type = Node.BRANCH
            self.rect=rect

    #Returns the type of the node, ROOT, BRANCH, or LEAF
    def getType(self):
        #print(self.type)
        return self.type

    #Check to see if the Branch or Root node contain the Coordinates
    #DOES NOT CHECK FOR EXISTANCE
    def containsCoord(self, x, y):
        xMin, yMin, xMax, yMax = self.rect
        if x >= xMin and x <= xMax and y >= yMin and y <= yMax:
            return True
        else:
            return False

 #Check to see if the Branch or Root node contain the Branch
    def containsBranch(self, rect):
        x1, y1, x2, y2 = rect
        xMin, yMin, xMax, yMax = self.rect
        if x1 >= xMin and x2 <= xMax and y1 >= yMin and y2 <= yMax:
            return True
        else:
            return False


    #recursively traverse tree and find the leaf representing x,y and elevation, if it exists
    #if not, print error and return False
    def findLeaf(self, x, y, elevation):
        if self.getType() == Node.LEAF:
            if self.x == x and self.y == y and self.elevat == elevation:
                print("Leaf Found! Depth is {}" .format(self.depth))
                return self
            elif self.x == x and self.y == y and not self.elevat == elevation:
                print("Elevation Not Valid")
                return self
        else:
            for i in self.children:
                if i != None:
                    if i.getType() == Node.BRANCH and i.containsCoord(x,y):
                        n = i.findLeaf(x,y,elevation)
                        if n != None:
                            return n;
                    elif i.getType() == Node.LEAF:
                        n = i.findLeaf(x,y,elevation)
                        if n != None:
                            return n;
            return self

        return None

    #Breaks Node into 4 Children and distributes rect range among them
    """
    min----------
    |  A  |  B  |
    |     |     |
    |-----------|
    |  C  |  D  |
    |     |     |
    ----------max
    """
    def subDivide(self):
        xMin, yMin, xMax, yMax, = self.rect
        aRect = [xMin, yMin, xMax/2, yMax/2]
        bRect = [xMin, yMax/2, xMax/2, yMax]
        cRect = [xMax/2, yMin, xMax, yMax/2]
        dRect = [xMax/2, yMax/2, xMax, yMax]
        a= Node(self, aRect, None, None, None)
        b= Node(self, bRect, None, None, None)
        c= Node(self, cRect, None, None, None)
        d= Node(self, dRect, None, None, None)
        childs = [a, b, c, d]
        self.children = childs
        #deepen the children
        for i in self.children:
            self.deepen(i)


#recursively increases depth of Node and all children
    def deepen(self, Node):
        Node.depth +=1
        if(self.type == Node.LEAF):
            return
        else:
            for i in Node.children:
                if i is not None:
                    self.deepen(i)


#splits a full branch into 4 sub-branches when full
    def split(self):
        prevChildren = self.children
        self.subDivide()
        #redistribute previous children to new children
        if prevChildren[0].getType()==LEAF:
            for i in prevChildren:
                for j in self.children:
                    if j.containsCoord(i.x, i.y):
                        j.children.append(i)
        #Else is a branch:
        else:
            for i in prevChildren:
                for j in self.children:
                    if j.containsBranch(i.rect):
                        j.children.append(i)
    def printNode(self, indent):
        if self.getType() == Node.BRANCH or self.getType() == Node.ROOT:
            xMin, yMin, xMax, yMax, = self.rect
            print("%sNode [%s,%s,%s,%s] is %s, %s children" % (indent, xMin, yMin, xMax, yMax, self.getType(), self.numbOfChild))
            for c in self.children:
              if c is not None:
                  c.printNode("%s  " % indent)
        elif self.getType() == Node.LEAF:
            print("%sNode (%s,%s,%s) is %s" % (indent, self.x, self.y, self.elevat, self.getType()))
        else:
            print("%sNode unhandled type %s" % (indent, self.getType()))


#QUADTREE Class that uses Node to construct the tree, rebalance, and print
class QuadTree:
    maxDepth = 0
    root = None
    boundaryRect = []


    def __init__(self, rect):
        self.root = Node(None, rect, None,None,None)
        self.boundaryRect = rect
        print(rect)


    def getDepth(self):
        return self.maxDepth


    #Prints Tree Structure
    #TODO: COMPLETE
    """
    recursively prints tree, starting at root
    Branches are represented by |
    Each line will be one layer of the tree
    Use a Queue to print in BFS

    """
    def printTree(self):
        self.root.printNode("");
        #print("Level      ****************************************")
        #printQ = queue.Queue()
        #printQ.put(" ")
        #current = self.root
        #while(not printQ.empty()):
        #    print(printQ.get())
        #    for i in current.children:
        #        if i.getType == Node.BRANCH:
        #            printQ.put("|")
        #        if i.getType == Node.LEAF:
        #            tuple = i.x, i.y, i.elevat
        #            printQ.put(tuple)

    #def printBranch(self):

    #Add a new Leaf to the Tree, automatically creates new branches
    #Returns True if succesful
    def AddLeaf(self, x, y, elevation):
        if not self.root.containsCoord(x,y):
            print("Position Out of Bounds! Bounds are {}" .format(self.boundaryRect))
        else:

            j = self.root.findLeaf(x,y, elevation)

            if j is None:
                print("ERROR Add Leaf %s %s %s" % (x, y, elevation))
            elif j.getType() == Node.BRANCH:
                howDeep = j.depth+1
                if j.numbOfChild < Node.MAXCHILDREN:
                    j.children.append(Node(j, None, x, y, elevation))
                    j.numbOfChild += 1
                else:
                    j.split()
                    k = j.findLeaf(x, y, elevation)
                    k.children.append(Node(k, None, x, y, elevation))
                    howDeep += 1
                if self.maxDepth < howDeep:
                        self.maxDepth = howDeep
                print("Child created at depth: " .format(howDeep))
                return True
            elif j.getType() == Node.LEAF:
                print("LEAF ALREADY EXISTS!")
                return False

    #Find N Nearest Neighbors
    """
    Modified version of FindLeaf
    While searching, stores Branch Nodes in a Queue
    Once it finds the Leaf, goes back to queue and loops until N children are returned
    """



    #Find all tuples/leaves within a certain RECT
    #NOTE, Logic for rect that overlapps branches, but not fully
    """
    Uses FindBranch to search tree

    In order to find a RECT in the case that overlaps several branches, the SEARCH RECT
    needs to be broken into smaller rects that are correctly devided based on positioning within Quadtree structure, using the boundaryRect variable.

    """


#TEST FUNCTIONS WHEN RUN FROM COMMAND LINE
def test():
    print("TESTING IN PROGRESS")
    #Create a tree
    rect = [0,0,20,20]
    tree = QuadTree(rect)

    tree.printTree()
    #Fill with elevations
    tree.AddLeaf(1, 2, 23)
    tree.AddLeaf(15, 19, 40)
    tree.AddLeaf(21, 21, 300) #check for out of bounds
    tree.AddLeaf(15, 19, 40) #check for duplicates
    tree.AddLeaf(15, 19, 30) #check for same x,y, but different elevation

    #print Tree
    tree.printTree()



if __name__ == '__main__':
    test()



