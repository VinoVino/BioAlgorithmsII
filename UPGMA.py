__author__ = 'jcovino'
from sys import  argv
from collections import defaultdict
import numpy
"""
CODE CHALLENGE: Implement UPGMA.
     Input: An integer n followed by a space separated n x n distance matrix.
     Output: An adjacency list for the ultrametric tree returned by UPGMA. Edge weights
     should be accurate to three decimal places.
Note on formatting: The adjacency list must have consecutive integer node labels starting from 0. The n leaves must be labeled 0, 1, ..., n - 1 in order of their appearance in the distance matrix. Labels for internal nodes may be labeled in any order but must start from n and increase consecutively.

Extra Dataset
Sample Input:
4
0	20	17	11
20	0	20	13
17	20	0	10
11	13	10	0

Sample Output:
0->5:7.000
1->6:8.833
2->4:5.000
3->4:5.000
4->2:5.000
4->3:5.000
4->5:2.000
5->0:7.000
5->4:2.000
5->6:1.833
6->5:1.833
6->1:8.833
"""

def DistanceToCoordinate_Generate(DistanceMatrix):  # function returns a default dict(list) with distances and repsective row,column coordinate for that score
     DistanceToCordinate=defaultdict(list)
     for index,value in enumerate(DistanceMatrix):
        #print index # position of the row
        #print value
        for index2, value2 in enumerate(value):
            #print index2 # position of the column
            #print value2  # value at the row, column position
            coordinateList=[]
            coordinateList.append(index)
            coordinateList.append(index2)
            #CoordinateString= (str(index) + "," + str(index2))
            DistanceToCordinate[float(value2)].append(coordinateList)  # dist
     return DistanceToCordinate


def main(argv):
    Distances=[]
    with open(argv[1], "r") as fstream:
        MatrixSize=int(fstream.readline())    ##matrix size, 4 = 4 x 4 matrix
        for line in fstream:
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to ints
            #print splitLine
            Distances.append(splitLineInt)

    PathDict={} # two D dict with start node (key)- End node (key)-> distance value (value)

    DistanceToCordinate=defaultdict(list)
    #######This can be repeated- add as function to regenerate
    for index,value in enumerate(Distances):
        #print index # position of the row
        #print value
        for index2, value2 in enumerate(value):
            #print index2 # position of the column
            #print value2  # value at the row, column position
            #CoordinateString= (str(index) + "," + str(index2))
            coordinateList=[]
            coordinateList.append(index)
            coordinateList.append(index2)
            if index not in PathDict:
                PathDict[index] = dict()
            PathDict[float(index)][float(index2)]=float(value2)    # 2D dict
            DistanceToCordinate[float(value2)].append(coordinateList)  # distance value gives coordinate, need to reupdate with function

    DistanceNP = numpy.array(Distances,dtype=numpy.float)  # convert to numpy array

    #print Distances  # Distances is the distance matrix
    #print DistanceNP  # numpy array version of the distance matrix

###################################
    ultraTree=defaultdict(dict)

    clusters=MatrixSize-1

    #while clusters > 1:
    nextspot=MatrixSize
    DistanceList=[]
    for key in DistanceToCordinate.keys():
        DistanceList.append(key)

    minDistance= min(v for v in DistanceList if not v in (None,0))  #find mininum distance, excluding 0
    #print "minscore", minDistance
    coordinates= DistanceToCordinate[minDistance]  # takes in list of coordinates

    # calculate distance from smallest adjacent nodes
    #print "coordinate", coordinates
    NumX=int(coordinates[0][0])
    NumY=int(coordinates[0][1])
    #print NumX
    #print NumY

    distance=PathDict[(NumX)][(NumY)]
    #print "---", distance
    #distance=PathDict[(NumY)][(NumX)]
    #print "---", distance
    #print distance/2.0

    #update ultrameric Tree
    ultraTree[NumX][nextspot]=distance/2.0
    ultraTree[NumY][nextspot]=distance/2.0
    ultraTree[nextspot][NumX]=distance/2.0
    ultraTree[nextspot][NumY]=distance/2.0
    #print "ultra tree", ultraTree

    #print Distances
    # update the scoring matrix for the - collapse collumns and rows
    #print NumX, "x"
    #print NumY, "y---"


    #update matrix
    #print DistanceNP
    for i in  range (NumX):
        #print Distances[i][NumX]
        #print Distances[i][NumY]
        DistanceiNumX=int(DistanceNP[i][NumX])
        DistanceiNumY=int(DistanceNP[i][NumY])
        combinedDistance=(DistanceiNumX+DistanceiNumY)/2.0
        DistanceNP[i][NumX]=combinedDistance
        DistanceNP[NumX][i]=combinedDistance
        PathDict[int(NumX)][int(i)]=combinedDistance
        PathDict[int(i)][int(NumX)]=combinedDistance

    # delete rows and columns
    print
    distanceNP_delROW= numpy.delete(DistanceNP,3,0)
    distanceNP_delROW_delCol= numpy.delete(distanceNP_delROW,3,1)

    print distanceNP_delROW_delCol


    DistanceToCordinate=DistanceToCoordinate_Generate(distanceNP_delROW_delCol)
    print DistanceToCordinate













if __name__== "__main__":
    main(argv)
