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
###################################################
def MaximalDistance(DistanceNP,DataPoint,M,Centers):
    MaxScore=0
    MaxDistanceCoord=[]  # coordinates of max distance
    CenterGroups=defaultdict(list)
    #DistanceNP_delROW= numpy.delete(DistanceNP,deleteRow,0)

    if len(Centers)> 1:                         #find the score for each data point to the centers-- take the minumum
        for i in range (len(DistanceNP)):
            MinScoreDict={} # stores scores
            row=DistanceNP[i]                   # for each data point/row

            for center in Centers:                      # calculate score of Datapoint against each center, store the minumum score, and the datapoint
                MinScore=0
                for k in range (M):
                    MinScore=(center[k]-row[k])**2 + MinScore               # distance score  (XA-XB)^2 + (YA-YB)^2= C^2

                #print MinScore, " row ", row, "-- ", MinScore
                MinScoreDict[MinScore]=row                                 #store score-> datapoint /row in dict
                minList=MinScoreDict.keys()
                #print  "minlist ", minList
                minkey=min(minList)

                #print "minkey ", minkey
                CenterGroups[minkey].append(row)        #This is the dictionary of minimums
                #print "minScore", MinScoreDict



        #print "centergroups, ", CenterGroups
        maxList=CenterGroups.keys()
        maxList.sort(reverse=True)
        #print "maxList ", maxList
        #print "------>", Centers
        for item in maxList:
            #print item
            centerMax=CenterGroups[item][0]
            #print centerMax
            if centerMax not in Centers:
                MaxDistanceCoord.append(centerMax)
                break


    else:
        for i in range (len(DistanceNP)):
            row=DistanceNP[i]  # for every row/datapoint
            score=0
            for k in range (M): #score Datapoint vs. every row in list to find new center
                score=(DataPoint[k]-row[k])**2 + score  # max distance score  (XA-XB)^2 + (YA-YB)^2= C^2
            #print "max ", MaxScore, "score ", score, "--", DistanceNP[i]
            if score > MaxScore :
                MaxScore=score
                secondPointSpot=i

        MaxDistanceCoord.append(DistanceNP[secondPointSpot])

    print MaxDistanceCoord
    return MaxDistanceCoord  # this is the new center coordinate


#####################################
def FarthestTraverse(DistanceNP,K,M):
    #print "K", K   #this is how many clusters to identify
    #print "M", M   #m dimensional space- if =2 x,y coordinates, if =3 x,y,z ect
    Centers=[]
    DataPoint=DistanceNP[0]
    Centers.append(DataPoint)

    while len(Centers) < K:
        NewDataPoint=(MaximalDistance(DistanceNP,DataPoint,M,Centers))  ## call to the function that determines center and returns sample coordinates
        DataPoint=NewDataPoint[0]
        Centers.append(DataPoint)
    return Centers

#######################################

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

    DistanceNP = numpy.array(Distances,dtype=numpy.float)  #need to delete previous centers

    print DistanceNP


    Centers= FarthestTraverse(Distances,K,M)

    print

    for element in Centers:
        print element


if __name__== "__main__":
    main(argv)
