__author__ = 'jcovino'
from sys import  argv
from collections import defaultdict
from random import randint
import copy
import itertools

"""
CODE CHALLENGE: Solve the Distances Between Leaves Problem. The tree is given as an adjacency list of a graph whose leaves are integers between 0 and n - 1;
the notation a->b:c means that node a is connected to node b by an edge of weight c. The matrix you return should be space-separated.

Extra Dataset

Sample Input:
4  4X4 matrix
0->4:11
1->4:2
2->5:6
3->5:7
4->0:11
4->1:2
4->5:4
5->4:4
5->3:7
5->2:6
Sample Output:
0	13	21	22
13	0	12	13
21	12	0	13
22  13	13	0

0 13 21 22
13 0 12 13
21 12 0 13
22 13 13 0
"""

def genNumberGraph(numbersPath):  # generate graphs, weighted and unweighted
    weightPathDict={}  #keys are nodes: 1,2 (1 to 2), value needs to be weight-- directed graph
    pathDict=defaultdict(list)
    # key is start node, value[0]-> node, value[1]- weight to travel to node
    for line in numbersPath:
        tokens=line[0].split("->")
        weight=tokens[1].split(":")
        weightPathDict[tokens[0]+"-"+weight[0]]=int(weight[1])
        pathDict[tokens[0]].append(weight[0])
    return weightPathDict,pathDict

def thePath_SourcetoSink(graphInput,sourceNode,sinkNode):  #function to find 'all' paths that start at source and end at sink

     PathsFound=[]
     i=0

     while i < 100000000:  # loop through X times to find the paths
         graph=copy.deepcopy(graphInput)
         v=[]
         Path=[]
         Path.append(str(sourceNode)) # start path with SourceNode
         theTruth=True
         visited = []
         ##########-----------need to add code that limits the revisiting of the same node- keep track in list of nodes visited if visited again- break

         while theTruth:
             #print graph
             v = Path[-1] # select the starting vertex or last entered vertex

             #if v not in graph:    # or v==str(sinkNode):  #if end is found
                 #theTruth=False
                 #print "here"
                 #break

             if str(sinkNode) in graph[v]:  # if sinknode is in list of values for a given key, then add to path and end
                 Path.append(str(sinkNode))
                 theTruth=False
                 #break

             if graph[v]: # if there are unused edges from the starting vertex
                 spot=0
                 if len(graph[v]) > 1:
                     spot=randint(0,len(graph[v])-1)
                 w = graph[v][spot] # select the vertex connected, if more than one connection-pick at random
                 if w in Path:
                     if w not in visited:
                         visited.append(w)
                     break
                 Path.append(w) # add the new vertex to, to become the new starting vertex
                             # delete edge v-w from the graph
                             # del graph[v][spot]
                 visited.append(spot)

                 if str(sinkNode) in graph[w]:   #  if sinknode is in list of values for a given key, then add to path and end
                     Path.append(str(sinkNode))
                     theTruth=False
                     #break

                 if len(graph[w])==0:
                     theTruth=False
                     #break

         i=i+1
         if Path[-1]==str(sinkNode):
             if Path not in PathsFound:
                 PathsFound.append(Path)

    # print PathsFound
    # print sourceNode
    # print sinkNode

     print PathsFound
     print sourceNode
     print sinkNode
     ####return the shortest path
     ShortestPath=PathsFound[-1]
     ShortestPathLength=len(PathsFound[-1]) # set ShortestPathLength to length of value in list
     for paths in PathsFound:
         if len(paths) < ShortestPathLength:
             ShortestPathLength= len(paths)
             ShortestPath=paths

     return ShortestPath



def ScoreGraph(Unique_Paths,weightPath ): # function determines total weight of paths that start at source and end at sink
    #weight path is weighted graph with keys as nodes connected and value is the weight
    # unqique_path is the total path
    scoreMe=[]
    finalPath=0

    i=0
    tempList=[]
    while i < len(Unique_Paths)-1 :
        tempList.append(Unique_Paths[i])
        tempList.append(Unique_Paths[i+1])
        if tempList not in scoreMe:
            scoreMe.append(tempList)
        i=i+1
    #print "--->", tempList ['3', '5', '5', '2']
    #print scoreMe [['3', '5', '5', '2']]

    totalScore=0
    for paths in scoreMe: # do the scoring of the matrix

        i=0
        while i < len(paths)-1:
            score=str(paths[i])+"-"+str(paths[i+1])
            intScore= weightPath[score]
            totalScore=totalScore+intScore
            i=i+2

    return totalScore


def main(argv):

    with open(argv[1], "r") as fstream:
        Matrix=int(fstream.readline())    ##starting node
        numbersPathInput = fstream.readlines()
    numbersPath=[]
    temp=[]
    for line in numbersPathInput:
        temp.append(line.rstrip())
        numbersPath.append(temp)
        temp=[]

    print(numbersPath)

    weightPath, graph =genNumberGraph(numbersPath)  # generate graph

    C = [[0 for j in range(Matrix)] for i in range(Matrix)]  # this is the matrix
    """
    for i in range (0, Matrix):
        for j in range (0, Matrix):
            sourceNode=i
            sinkNode=j
            if i != j:
                ToScorePath= thePath_SourcetoSink(graph,sourceNode,sinkNode)
                score= ScoreGraph(ToScorePath,weightPath)
            else:
                score=0
            C[i][j]=score"""
    sourceNode=0
    sinkNode=2


    ToScorePath= thePath_SourcetoSink(graph,sourceNode,sinkNode)
    score= ScoreGraph(ToScorePath,weightPath)
    print score
    # print C
    """for element in C:
            print
            for items in element:
                print items,"""
    # print
    # print graph
    # print weightPath
    #ScoreGraph(ToScorePath,weightPath)


if __name__== "__main__":
    main(argv)
