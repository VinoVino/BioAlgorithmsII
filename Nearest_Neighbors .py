__author__ = 'jcovino'
from sys import  argv
from collections import defaultdict
import copy

"""
CODE CHALLENGE: Solve the Nearest Neighbors of a Tree Problem.
     Input: Two internal nodes a and b specifying an edge e, followed by an adjacency
     list of an unrooted binary tree.
     Output: Two adjacency lists representing the nearest neighbors of the tree with
     respect to e. Separate the adjacency lists with a blank line.

Extra Dataset

Sample Input:
5 4
0->4
4->0
1->4
4->1
2->5
5->2
3->5
5->3
4->5
5->4

Sample Output:
1->4
0->5
3->4
2->5
5->2
5->4
5->0
4->1
4->5
4->3

1->5
0->4
3->4
2->5
5->2
5->4
5->1
4->0
4->5
4->3
"""

def flipgraph(Node1,Node2,graph):
    print Node1, Node2
    graph2=copy.deepcopy(graph)

    print "node1 ", Node1, "-->", graph[Node1]
    print "node2 ", Node2, "-->", graph[Node2]
    # find the first legs that are not equal to NODE1 or NODE2
    for i in range (len(graph[Node1])):
         node1Leg1= graph[Node1][i]
         node2Leg1= graph[Node2][i]
         Group1SpotFound=i
         if node1Leg1 != Node1 or node1Leg1 != Node2:
             break
         if node2Leg1 != Node1 or node2Leg1 != Node2:
             break
    #print "swap_node1Leg1 ", node1Leg1
    #print "swap_node2Leg1 ",node2Leg1
    #add leg1 and leg2 to Node2 and Node1 , swap them
    graph2[Node1].append(node2Leg1)
    graph2[Node2].append(node1Leg1)
    #also do the reverse, have the new leg point back to it's new node
    graph2[node2Leg1].append(Node1)
    graph2[node1Leg1].append(Node2)

    node1Side=graph2[Node1]  # need to delete  node pointing node1leg1
    node2Side=graph2[Node2]  # need to delete node pointing node2leg1
    # find the spot to delete
    for i in range (len(node1Side)):
        if node1Side[i]==node1Leg1:
            delnode1_spot=i
    for i in range(len(node2Side)):
        if node2Side[i]==node2Leg1:
            delnode2_spot=i
    del graph2[Node1][delnode1_spot]
    del graph2[Node2][delnode2_spot]

    # now need to delete moved legs and correct themselves to where they point
    toNode1Side=graph2[node1Leg1]
    toNode2Side=graph2[node2Leg1]
    # find the spot to delete

    #print "node1Leg1", node1Leg1, "--->", toNode1Side
    #print "node2Leg1", node2Leg1, "--->", toNode2Side

    for i in range(len(toNode1Side)):
        if toNode1Side[i]==Node1:
            delToNode1Side_spot=i
    for i in range(len(toNode2Side)):
        if toNode2Side[i]==Node2:
            delToNode2Side_spot=i
    del graph2[node1Leg1][delToNode1Side_spot]
    del graph2[node2Leg1][delToNode2Side_spot]

    #print "first graph", graph2
    #############find second mirror image of graph###################################################################
    #print Group1SpotFound
    graph3=copy.deepcopy(graph)

    for i in range (Group1SpotFound+1, len(graph[Node1])):
         node1Leg1= graph[Node1][i]
         node2Leg1= graph[Node2][i]
         Group1SpotFound=i
         if node1Leg1 != Node1 or node1Leg1 != Node2:
             break
         if node2Leg1 != Node1 or node2Leg1 != Node2:
             break
    #print "swap_node1Leg1 ", node1Leg1
    #print "swap_node2Leg1 ",node2Leg1
    #add leg1 and leg2 to Node2 and Node1 , swap them
    graph3[Node1].append(node2Leg1)
    graph3[Node2].append(node1Leg1)
    #also do the reverse, have the new leg point back to it's new node
    graph3[node2Leg1].append(Node1)
    graph3[node1Leg1].append(Node2)

    node1Side=graph3[Node1]  # need to delete  node pointing node1leg1
    node2Side=graph3[Node2]  # need to delete node pointing node2leg1
    # find the spot to delete
    for i in range (len(node1Side)):
        if node1Side[i]==node1Leg1:
            delnode1_spot=i
    for i in range(len(node2Side)):
        if node2Side[i]==node2Leg1:
            delnode2_spot=i
    del graph3[Node1][delnode1_spot]
    del graph3[Node2][delnode2_spot]
    # now need to delete moved legs and correct themselves to where they point
    toNode1Side=graph3[node1Leg1]
    toNode2Side=graph3[node2Leg1]
    # find the spot to delete

    #print "node1Leg1", node1Leg1, "--->", toNode1Side
    #print "node2Leg1", node2Leg1, "--->", toNode2Side

    for i in range(len(toNode1Side)):
        if toNode1Side[i]==Node1:
            delToNode1Side_spot=i
    for i in range(len(toNode2Side)):
        if toNode2Side[i]==Node2:
            delToNode2Side_spot=i
    del graph3[node1Leg1][delToNode1Side_spot]
    del graph3[node2Leg1][delToNode2Side_spot]


    #print "second graph", graph3

    return graph2,graph3





def main(argv):

    graph=defaultdict(list)
    graphList=[]
    with open(argv[1], "r") as fstream:
        Node1=int(fstream.readline())    ##starting node
        Node2 =int(fstream.readline())
        path=fstream.readlines()

    for i in range(len(path)):
        #if i%2==0:
            element=path[i].rstrip()
            temp= element.split("->")
            graph[int(temp[0])].append(int(temp[1]))
            graphList.append(element)

    graph2,graph3=flipgraph(Node1,Node2,graph)

    for key in graph2.keys():
        printvalues=graph2[key]
        for value in printvalues:
            print "{}->{}".format(key, value)

    print

    for key in graph3.keys():
        printvalues=graph3[key]
        for value in printvalues:
            print "{}->{}".format(key, value)




if __name__== "__main__":
    main(argv)
