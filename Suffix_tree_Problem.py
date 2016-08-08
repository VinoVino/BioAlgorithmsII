__author__ = 'jcovino'
from sys import argv
"""
CODE CHALLENGE: Solve the Suffix Tree Construction Problem.
     Input: A string Text.
     Output: The edge labels of SuffixTree(Text). You may return these strings in any order.

     Sample Input:
ATAAATG$
Sample Output:
AAATG$
G$
T
ATG$
TG$
A
A
AAATG$
G$
T
G$
$
"""
class Node(object):   # numbers
    def __init__(self,id,Length=1, startStringIndex=0):
        self.id= id
        self.out_edges={}

        self.Length=Length
        self.startStringIndex=startStringIndex

class Edge(object):   # letters
    def __init__(self,from_node, to_node,symbol):
        self.from_node=from_node
        self.to_node=to_node
        self.symbol= symbol

class trie(object):
    def __init__(self):
        self.max_node = 0
        self.nodes = {0: Node(0)}  # dictionary of Node objects (id and out edges)

    def add_pattern(self, pattern,startStringIndex):
        current_node_id = 0
        Length=1

        for c in pattern:  # c is current symbol in string
            current_node = self.nodes[current_node_id] # current node = key current id-> Node object( ID and out_edges)
            if c in current_node.out_edges: # if C is in out edges dict
                current_node_id = current_node.out_edges[c].to_node  #.to_node  # move to next node---
                continue

            self.max_node += 1   # increment max node by 1, adding new node
            self.nodes[self.max_node] = Node(self.max_node)  # adding the new node, ID is current max node,
            current_node.out_edges[c] = Edge(current_node_id, self.max_node, c)  # add edge to current node

            self.nodes[current_node_id].Length= Length
            self.nodes[current_node_id].startStringIndex=startStringIndex

            print c,"Length " , self.nodes[current_node_id].Length, "startI ",self.nodes[current_node_id].startStringIndex
            Length=Length+1
            current_node_id= self.max_node

        return trie

    def suffixTree(self, pattern):
        ####convert to SuffixTree
        print pattern

        for nodekey in self.nodes:  # for every node, number 0-30
            #print nodekey
            spot=self.nodes[nodekey] #start node, current node out edge, letter
            """
            NodeStart= self.nodes[nodekey].startStringIndex
            Length= (self.nodes[nodekey].Length)
            #print Length


            if len(spot.out_edges) > 1:  # This is a branch location.  Follow all paths down.
               for edgekey in spot.out_edges: # move through each branch, letter
                   Length=1
                   theTruth= True
                   nextNode_id= spot.out_edges[edgekey].to_node   # this is the key, number

                   while theTruth:
                       nextNode =self.nodes[nextNode_id]

                       lengthOutEdges= len(nextNode.out_edges)  # check edges from next node

                       if lengthOutEdges== 0:
                           theTruth=False

                       elif lengthOutEdges >1:
                           theTruth=False

                       elif lengthOutEdges == 1:       # move to next node, increase path length
                           Length = Length+1
                           PrevNode_ID= nextNode_id
                           nextNode_id=nextNode.out_edges.values()[0].to_node
                           #del self.nodes[PrevNode_ID] need to delete in between nodes/edges

                   # add path length
                   #self.nodes[nextNode_id].Length= path_length
            #print NodeStart,Length,
            #print pattern[NodeStart:NodeStart+Length]

            """



"""
for node in self.nodes:
if len(node.out_edges) > 1:
# This is a branch location.  Follow all paths down.
for edge in node.out_edges:
path_length = 0
while True
get node below this edge
how many out edges are there?
if 0: STOP and collapse
if >1: STOP and collapse
if =1: path_length += 1, get node below edge, repeat
collapse means remove inbetween nodes and increase length of edge by path_length"""




def main(argv):

    with open(argv[1],"r") as fstream:
        for line in fstream:
            lineInput = line.rstrip()

    answer=[]
    trees = trie()  # create a trees object trie

    for id in range  (0,len(lineInput)):
        substring= lineInput[id:]
        substring=substring
        startStringIndex=id
        Suffix= trees.add_pattern(substring,startStringIndex)

    trees.suffixTree(lineInput)

    #fileOut=open('Answer.txt','w')
    #print "-"
    #for line in answer:
            #for element in line:
                #print element

    #fileOut.close()


if __name__== "__main__":
    main(argv)