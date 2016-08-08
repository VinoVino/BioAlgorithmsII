__author__ = 'jcovino'
from sys import  argv
import numpy
from collections import defaultdict

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
#####################################
def FarthestTraverse(Distances,K,M):
    # "K", K   #this is how many clusters to identify
    # "M", M   #m dimensional space- if =2 x,y coordinates, if =3 x,y,z ect
    Centers=[]
    Center=Distances[0]  #this is the first center
    Centers.append(Center)
    DistanceNP=Distances[:]

    while len(Centers) < K:
        MaxDistanceCoord=[]  # coordinates of max distance

        for Center in Centers:          # delete centers from list of Cooridinates
            if Center in DistanceNP:
                deleterow= DistanceNP.index(Center)
                del DistanceNP[deleterow]
        Maximus=0
        if len(Centers)> 1:
            for row in DistanceNP:
                minScore=100000000000

                for center in Centers:                      # calculate score of Datapoint against each center, store the minumum score, and the datapoint
                    Score=0
                    for k in range (M):
                        Score +=((center[k]-row[k])**2)    # distance score  (XA-XB)^2 + (YA-YB)^2= C^2

                    if Score < minScore:
                        minScore=Score
                        coordinate=row

                if minScore > Maximus:
                    Maximus= minScore
                    MaxCoord=coordinate

                    #print "Center", center, "row ", row,  " Score ", Score
            MaxDistanceCoord.append(MaxCoord)
            print

        else: # first time through
            MaxScore=0
            for i in range (len(DistanceNP)):
                rows=DistanceNP[i]  # for every row/datapoint
                score=0
                for k in range (M): #score Datapoint vs. every row in list to find new center
                    score=(Center[k]-rows[k])**2 + score  # max distance score  (XA-XB)^2 + (YA-YB)^2= C^2
                if score > MaxScore :
                    MaxScore=score
                    secondPointSpot=i
            MaxDistanceCoord.append(DistanceNP[secondPointSpot])
        Centers.append(MaxDistanceCoord[0])  # this is the new center coordinate
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
    print
    Centers= FarthestTraverse(Distances,K,M)
    print

    for element in Centers:
        print element


if __name__== "__main__":
    main(argv)
