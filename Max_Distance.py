__author__ = 'jcovino'
from sys import  argv
import numpy
import math

"""
Calculate Max Distance

Sample Input:
Centers
2 # number of centers
3 5
5 4   # Centers
2 8   # Data
2 5
6 9
7 5
5 2





"""
#####################################

def MaxDistance(Centers,DataPoints):
    Maximus=0

    for row in DataPoints:
                minScore=100000000000

                for center in Centers:                      # calculate score of Datapoint against each center, store the minumum score, and the datapoint
                    Score=0
                    for k in range (2):
                        Score +=((center[k]-row[k])**2)    # distance score  (XA-XB)^2 + (YA-YB)^2= C^2

                    if Score < minScore:
                        minScore=Score
                        coordinate=row

                if minScore > Maximus:
                    Maximus= minScore


    print "1 ", math.sqrt(Maximus)








    maxScore=0
    Scores=[]
    for row in DataPoints:  # for each datapoint

                for center in Centers:                      # calculate score of Datapoint against each center, store the minumum score, and the datapoint
                    Score=0
                    for k in range (2):
                        Score +=((center[k]-row[k])**2)    # distance score  (XA-XB)^2 + (YA-YB)^2= C^2


                    if Score > maxScore:
                        maxScore=Score



    print math.sqrt(maxScore)
    

def main(argv):
    Distances=[]
    Centers=[]
    with open(argv[1], "r") as fstream:
        K=int(fstream.readline())    #K-  # of centers Centers

        for i in range(K):
            line=fstream.readline()
            linstrip=line.rstrip()
            Center_splitLine=linstrip.split(' ')
            Center_splitLineInt=map(float,Center_splitLine)  # convert to float
            Centers.append(Center_splitLineInt)

        for line in fstream:
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Distances.append(splitLineInt)


    DistanceNP = numpy.array(Distances,dtype=numpy.float)
    print "Centers ", Centers
    print "Data points ", DistanceNP

    MaxDistance(Centers,Distances)




if __name__== "__main__":
    main(argv)
