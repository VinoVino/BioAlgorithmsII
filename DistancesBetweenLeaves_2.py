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

def find_path(graph, start, end, path=[]):
#recursive algorithm-- study this
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: return newpath
        return None

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

    weightPath, graph =genNumberGraph(numbersPath)  # generate graph

    C = [[0 for j in range(Matrix)] for i in range(Matrix)]  # this is the matrix

    for i in range (0, Matrix):
        for j in range (0, Matrix):
            sourceNode=i
            sinkNode=j
            if i != j:
                ToScorePath= find_path(graph,str(sourceNode),str(sinkNode),path=[])
                score= ScoreGraph(ToScorePath,weightPath)
            else:
                score=0
            C[i][j]=score

    for element in C:
           print
           for items in element:
               print items,

  


if __name__== "__main__":
    main(argv)
