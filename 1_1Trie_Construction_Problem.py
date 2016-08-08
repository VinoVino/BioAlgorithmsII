__author__ = 'jcovino'
from sys import argv
import sys

"""
CODE CHALLENGE: Solve the Trie Construction Problem.
     Input: A collection of strings Patterns.
     Output: The adjacency list corresponding to Trie(Patterns), in the following format. If
     Trie(Patterns) has n nodes, first label the root with 0 and then label the remaining nodes with
     the integers 1 through n - 1 in any order you like. Each edge of the adjacency list of
    Trie(Patterns) will be encoded by a triple: the first two members of the triple must be the
    integers labeling the initial and terminal nodes of the edge, respectively; the third member
     of the triple must be the symbol labeling the edge.

Sample Input:
ATAGA
ATC
GAT
Sample Output:
0->1:A
1->2:T
2->3:A
3->4:G
4->5:A
2->6:C
0->7:G
7->8:A
8->9:T

"""

class Node(object):
    def __init__(self,id,label=None):
        self.id= id
        self.out_edges={}
        self.label=label

class Edge(object):
    def __init__(self,from_node, to_node,symbol):
        self.from_node=from_node
        self.to_node=to_node
        self.symbol= symbol

class trie(object):
    def __init__(self):
        self.max_node = 0
        self.nodes = {0: Node(0)}  # dictionary of Node objects (id and out edges)

    def add_pattern(self, pattern):
        answer=[]
        current_node_id = 0
        for c in pattern:  # C is current symbol
            current_node = self.nodes[current_node_id] # current node = key current id-> Node object( ID and out_edges)
            if c in current_node.out_edges: # if C is in  out edges dict
                current_node_id = current_node.out_edges[c].to_node  #.to_node?  # move to next node , ???
                continue
            self.max_node += 1   # increment max node by 1, adding new node
            self.nodes[self.max_node] = Node(self.max_node)  # adding the new node, ID is current max node,
            current_node.out_edges[c] = Edge(current_node_id, self.max_node, c)  # add edge to current node
            lineAnswer=str(current_node_id) + '->' + str(self.max_node) + ":" + str(c)
            sys.stdout.write(str(current_node_id))
            sys.stdout.write('->')
            sys.stdout.write(str(self.max_node))
            sys.stdout.write(':')
            sys.stdout.write(str(c))
            answer.append(lineAnswer)
            print
            current_node_id= self.max_node

        return answer

def main(argv):
    patterns=[]
    with open(argv[1],"r") as fstream:
        for line in fstream:
            line_input=line.rstrip()
            patterns.append(line_input)
    answer=[]

    #print patterns


    trees = trie()
    for pattern in patterns:
        answer.append(trees.add_pattern(pattern))
    fileOut=open('Answer.txt','w')
    print "-"
    for line in answer:
            for element in line:
                print element
                fileOut.write(element)
                fileOut.write('\n')


    fileOut.close()




if __name__== "__main__":
    main(argv)