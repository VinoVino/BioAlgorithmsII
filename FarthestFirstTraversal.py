__author__ = 'jcovino'
from sys import  argv
import numpy

"""
CODE CHALLENGE: Implement the FarthestFirstTraversal clustering heuristic.
     Input: Integers k and m followed by a set of points Data in m-dimensional space.
     Output: A set Centers consisting of k points (centers) resulting from applying
     FarthestFirstTraversal(Data, k), where the first point from Data is chosen as the
     first center to initialize the algorithm.

Sample Input:
3 2
0.0 0.0
5.0 5.0
0.0 5.0
1.0 1.0
2.0 2.0
3.0 3.0
1.0 2.0
Sample Output:
0.0 0.0
5.0 5.0
0.0 5.0

"""
###################################################
def MaximalDistance(DistanceNP,DataPoint,MaxScore,M):
    firstPoint=[]  # this is the center, coordinates will be pulled based on M
    MaxScore=0
    for i in range(M):
        firstPoint.append(DataPoint[i])

    MaxDistanceCoord=[]  # coordinates of max distance

    for i in range (len(DistanceNP)):
        row=DistanceNP[i]
        secondPoint=[]   # this is the comparison point, coordinates will be pulled based on M
        for j in range (M):
            secondPoint.append(row[j])
        score=0
        for k in range (M):
            score=(firstPoint[k]-secondPoint[k])**2 + score  # max distance score  (XA-XB)^2 + (YA-YB)^2= C^2

        print "max ", MaxScore, "score ", score, "--", DistanceNP[i]
        if score > MaxScore :
            MaxScore=score
            secondPointSpot=i
            deleteRow=i

    print

    # have to remove other rows that also are clustered around center-- Check Distance to current list of centers. if potential points are closer to current center than new center

    MaxDistanceCoord.append(DistanceNP[secondPointSpot])

    DistanceNP_delROW= numpy.delete(DistanceNP,deleteRow,0) #don't need to delete if we use minum distance from existing centers to pick new spot**********************
    return MaxDistanceCoord,DistanceNP_delROW


#####################################
def FarthestTraverse(DistanceNP,K,M):
    #print DistanceNP
    print "K", K   #this is how many clusters to identify
    print "M", M   #m dimensional space- if =2 x,y coordinates, if =3 x,y,z ect
    Centers=[]
    MaxScore=0        # max distance score  (XA-XB)^2 + (YA-YB)^2= C^2
    DataPoint=DistanceNP[0]
    Centers.append(DataPoint)
    DistanceNP = numpy.delete(DistanceNP,0,0)  # delete the first row from matrix*****************************

    while len(Centers) < K:
        NewDataPoint,DistanceNP=(MaximalDistance(DistanceNP,DataPoint,MaxScore,M))  ## call to the function that calculates maxDistance
        DataPoint=NewDataPoint[0]
        Centers.append(DataPoint)


    return Centers




def main(argv):
    Distances=[]
    with open(argv[1], "r") as fstream:
        K=int(fstream.readline())    #K- Centers
        M=int(fstream.readline())    #M- M dimensional space-
        for line in fstream:
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Distances.append(splitLineInt)

    DistanceNP = numpy.array(Distances,dtype=numpy.float)
    print DistanceNP
    Centers= FarthestTraverse(DistanceNP,K,M)

    print

    print Centers
    #numpy.around(Centers, decimals=1)

    for element in Centers:
        print element


if __name__== "__main__":
    main(argv)
