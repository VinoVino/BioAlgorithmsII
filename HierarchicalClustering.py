__author__ = 'jcovino'
from sys import  argv
from collections import defaultdict
import numpy
"""
7
0.00 0.74 0.85 0.54 0.83 0.92 0.89
0.74 0.00 1.59 1.35 1.20 1.48 1.55
0.85 1.59 0.00 0.63 1.13 0.69 0.73
0.54 1.35 0.63 0.00 0.66 0.43 0.88
0.83 1.20 1.13 0.66 0.00 0.72 0.55
0.92 1.48 0.69 0.43 0.72 0.00 0.80
0.89 1.55 0.73 0.88 0.55 0.80 0.00
Sample Output:
4 6
5 7
3 4 6
1 2
5 7 3 4 6
1 2 5 7 3 4 6
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

def delete_matrix(DistanceNP,delete_coord):
     # delete rows and columns
        distanceNP_delROW= numpy.delete(DistanceNP,delete_coord,0)
        distanceNP_delROW_delCol= numpy.delete(distanceNP_delROW,delete_coord,1)
        return distanceNP_delROW_delCol


def Calc_combinedistance(Larger_coord,Smaller_coord,DistanceNP,MergedCoords,i):      #determine if X,Y originate from rows that were combined. And how many rows were combined to make them
    DistanceiNumX=float(DistanceNP[i][Smaller_coord])
    DistanceiNumY=float(DistanceNP[i][Larger_coord])

    #print "cords", Larger_coord,Smaller_coord, ":   ",
    #print DistanceiNumY, DistanceiNumX

    if Smaller_coord not in MergedCoords and Larger_coord not in MergedCoords:
    #     print "solo"
        combinedDistance=(DistanceiNumX+DistanceiNumY)/2.0

    elif Smaller_coord in MergedCoords:
        MergedLength= len(MergedCoords[Smaller_coord])  # this tells you how many rows were combined at that current row (-1)
        combinedDistance= ((MergedLength+1) * DistanceiNumX + DistanceiNumY )/ (MergedLength+2)
    else:
        MergedLength= len(MergedCoords[Larger_coord])  # this tells you how many rows were combined at that current row (-1)
        combinedDistance= ((MergedLength+1) * DistanceiNumY + DistanceiNumX )/ (MergedLength+2)
    #
    return combinedDistance

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

    #print Distances  # Distances is the distance matrix------Original Distance matrix----DistanceNP  # numpy array version of the distance matrix
######################################
    ultraTree=defaultdict(dict)
    collapsedCoord=defaultdict(list)  # dictionary to keep track of collapsed coordinates
    conversionDict={}  # dictionary to keep track of collapsed coordinates - overwritten with each use of of same key that has been used before
    ConnectedNodes=[]
    clusters=MatrixSize-1
    print DistanceNP
    nextspot=MatrixSize

    print "--------------------------------------------------------"
    while clusters > 0:

        DistanceList=[]
        for key in DistanceToCordinate.keys():
            DistanceList.append(key)
        minDistance= min(v for v in DistanceList if not v in (None,0))  #find mininum distance, excluding 0
        #print "minscore", minDistance
        coordinates= DistanceToCordinate[minDistance]  # takes in list of coordinates for a given distance

        XYCoord=[]
        NumX=int(coordinates[0][0])
        NumY=int(coordinates[0][1])
        XYCoord.append(NumX)
        XYCoord.append(NumY)

        Larger_coord= max(XYCoord)
        Smaller_coord=min(XYCoord)
        LargeSmall=[]
        LargeSmall.append(Larger_coord)
        LargeSmall.append(Smaller_coord) # keep track for collapsed coordinate

        #print "----------", minDistance/2
        #update ultrameric Tree--

        if NumX in conversionDict:
            NumX=conversionDict[NumX]
           # print "NumX in"
        elif NumY in conversionDict:
            #print "Numy in"
            NumY=conversionDict[NumY]

        conversionDict[Smaller_coord]=nextspot+1
        conversionDict[Larger_coord]=nextspot+1

        #print "numx,next",NumX,nextspot, "---", minDistance/2.0
        #print "numy,next",NumY,nextspot, "----", minDistance/2.0

        if NumX != nextspot:
            ultraTree[NumX][nextspot]=minDistance/2.0
            ultraTree[nextspot][NumX]=minDistance/2.0
        if NumY != nextspot:
            ultraTree[NumY][nextspot]=minDistance/2.0
            ultraTree[nextspot][NumY]=minDistance/2.0

        print
        #update matrix
        for i in  range (len(DistanceNP)):

            combinedDistance=Calc_combinedistance(Larger_coord,Smaller_coord,DistanceNP,collapsedCoord,i)
            #print combinedDistance
            DistanceNP[i][Smaller_coord]=combinedDistance  # reset values of matrix to smaller coordinates- Larger value will get deleted
            DistanceNP[Smaller_coord][i]=combinedDistance


        for i in range(len(DistanceNP)): # zero out diagnonal part of matrix
            DistanceNP[i][i]=0

        DistanceNP=delete_matrix(DistanceNP,Larger_coord)
        DistanceToCordinate=DistanceToCoordinate_Generate(DistanceNP)

        collapsedCoord[Smaller_coord].append(LargeSmall)   # update collapsedCoordinates with key of smaller coord _> list of (Large and small coord)
        ConnectedNodes.append(nextspot)
        nextspot=nextspot+1
        clusters=clusters-1

        #print DistanceNP



    print ConnectedNodes
    #print nextspot
    print ultraTree

if __name__== "__main__":
    main(argv)
