__author__ = 'jcovino'
from sys import argv
from random import randint
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
    def __init__(self,id):
        self.id= id
        self.out_edges={}  # keys are letters, to object of type EDGE

class Edge(object):   # letters
    def __init__(self,from_node, to_node,symbol, Length=1, startStringIndex=0):
        self.from_node=from_node
        self.to_node=to_node
        self.symbol= symbol

        self.Length=Length
        self.startStringIndex=startStringIndex

class trie(object):
    def __init__(self):
        self.max_node = 0
        self.nodes = {0: Node(0)}  # dictionary of Node objects (id and out edges)

    def add_pattern(self, pattern,startStringIndexVar):
        current_node_id = 0

        #print pattern
        for c in pattern:  # c is current symbol in string
            #print "----",c
            current_node = self.nodes[current_node_id]      # current node = key current id-> Node object( ID and out_edges)
            if c in current_node.out_edges:                 # if C is in out edges dict
                startStringIndexVar=startStringIndexVar+1
                current_node_id = current_node.out_edges[c].to_node     #.to_node  # move to next node---
                continue

            self.max_node += 1                                # increment max node by 1, adding new node
            self.nodes[self.max_node] = Node(self.max_node)  # adding the new node, ID is current max node,

            current_node.out_edges[c] = Edge(current_node_id, self.max_node, c, Length=1, startStringIndex=startStringIndexVar)  # add edge to current node

            #print c, "Length " , self.nodes[current_node_id].Length, "startI ",self.nodes[current_node_id].startStringIndex
            startStringIndexVar=startStringIndexVar+1
            current_node_id= self.max_node

        return trie
#############################################################
    def suffixTree(self, pattern):
        branching_nodes = [node_id for node_id in self.nodes            #list comprehension to find only branching nodes
                           if len(self.nodes[node_id].out_edges) > 1]

        for nodekey in branching_nodes:  # for every branching node, number
            startNode=self.nodes[nodekey] #start node number, to object of NODE

            for edgekey in startNode.out_edges: # move through each branch, letter
                Length=1
                theTruth= True

                nextNode_id= startNode.out_edges[edgekey].to_node   # nextnode id--to node is number
                while theTruth:
                    currentsymbol= startNode.out_edges[edgekey].symbol
                    nextNode =self.nodes[nextNode_id]  # nextNode_id is number accessing object nextnode

                    lengthOutEdges= len(nextNode.out_edges)  # check edges from next node
                    if lengthOutEdges== 0:
                       theTruth=False

                    elif lengthOutEdges >1:
                       theTruth=False

                    elif lengthOutEdges == 1:       # move to next node, increase path length
                       Length = Length+1
                       delNode_ID= nextNode_id
                       # update concatenate current symbol with its string plus deleted node symbol
                       nextNode_id=nextNode.out_edges.values()[0].to_node  # new number
                       nextsymbol=nextNode.out_edges.values()[0].symbol # new symbol
                       
                       del self.nodes[delNode_ID]
                       startNode.out_edges[edgekey].to_node= nextNode_id  # update the connection edge
                       startNode.out_edges[edgekey].symbol= currentsymbol+nextsymbol
                #add path length to out Edges
                startNode.out_edges[edgekey].Length =Length
        answer=[]
        self.Recuprint(self.nodes[0],answer)  # call recursive print
        return answer
################################################################
    def Recuprint(self,spot,answer):
        for edge in spot.out_edges.values():
            answer.append(edge.symbol) # edge.from_node ,  edge.to_node
            # update to node
            nextnode=self.nodes[edge.to_node]
            self.Recuprint(nextnode,answer)


def main(argv):

    with open(argv[1],"r") as fstream:
        for line in fstream:
            lineInput = line.rstrip()


    trees = trie()  # create a trees object trie

    for id in range  (0,len(lineInput)):
        substring= lineInput[id:]
        #print substring
        trees.add_pattern(substring,id)

    Answer=trees.suffixTree(lineInput)

    fileOut=open('Answer.txt','w')

    for line in Answer:
        fileOut.write(line)
        fileOut.write("\n")

    fileOut.close()


if __name__== "__main__":
    main(argv)