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
def MaximalDistance(Distances,DataPoint,M,Centers):
    MaxScore=0
    MaxDistanceCoord=[]  # coordinates of max distance
    CenterGroups=defaultdict(list)
    CenterGroups.clear()
    DistanceNP=Distances[:]

    for Center in Centers:          # delete centers from list of Cooridinates
        deleterow= DistanceNP.index(Center)
        del DistanceNP[deleterow]

    MinScoreDict={}                     # stores scores
    if len(Centers)> 1:
        for i in range (len(DistanceNP)):  #find the score for each data point to the centers-- take the minumum
            MinScoreDict.clear()
            row=DistanceNP[i]                   # for each data point/row

            for center in Centers:                      # calculate score of Datapoint against each center, store the minumum score, and the datapoint
                Score=0
                for k in range (M):
                    Score=((center[k]-row[k])**2) + Score               # distance score  (XA-XB)^2 + (YA-YB)^2= C^2
                #print MinScore, " row ", row, "-- ", MinScore
                MinScoreDict[Score]=row                                 #store score-> datapoint /row in dict
                minList=MinScoreDict.keys()
                minList.sort()  # sort list , min is first element
                CenterGroups[minList[0]].append(row)        #This is the dictionary of scores

        maxList=CenterGroups.keys()
        maxList.sort(reverse=True)  #sort highest to lowest
        print maxList
        centerMax= maxList[0] #max is first element
        MaxDistanceCoord.append(CenterGroups[centerMax][0])
        print


    else: # first time through
        for i in range (len(DistanceNP)):
            row=DistanceNP[i]  # for every row/datapoint
            score=0
            for k in range (M): #score Datapoint vs. every row in list to find new center
                score=(DataPoint[k]-row[k])**2 + score  # max distance score  (XA-XB)^2 + (YA-YB)^2= C^2
            if score > MaxScore :
                MaxScore=score
                secondPointSpot=i
        MaxDistanceCoord.append(DistanceNP[secondPointSpot])


    return MaxDistanceCoord  # this is the new center coordinate


#####################################
def FarthestTraverse(Distances,K,M):
    #print "K", K   #this is how many clusters to identify
    #print "M", M   #m dimensional space- if =2 x,y coordinates, if =3 x,y,z ect
    Centers=[]
    Center=Distances[0]  #this is the first center
    Centers.append(Center)

    while len(Centers) < K:
        NewCenter=(MaximalDistance(Distances,Center,M,Centers))  ## call to the function that determines center and returns sample coordinates
        DataPoint=NewCenter[0]
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

    DistanceNP = numpy.array(Distances,dtype=numpy.float)

    print DistanceNP


    Centers= FarthestTraverse(Distances,K,M)

    print

    for element in Centers:
        print element


if __name__== "__main__":
    main(argv)
