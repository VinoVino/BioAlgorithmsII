__author__ = 'jcovino'
from sys import  argv
import numpy
from collections import defaultdict

"""
CODE CHALLENGE: Solve the Squared Error Distortion Problem.
     Input: Integers k and m, followed by a set of centers Centers and a set of points Data.
     Output: The squared error distortion Distortion(Data, Centers).

Extra Dataset

Sample Input:
2 2
2.31 4.55
5.96 9.08
-----------
3.42 6.03
6.23 8.25
4.76 1.64
4.47 4.33
3.95 7.61
8.93 2.97
9.74 4.03
1.73 1.28
9.72 5.01
7.27 3.77
Sample Output:
18.246

"""

def Distortion(Centers,Datapoints,K,M):
    meanList=[]
    sumMinScore=0

    for DataRow in Datapoints:  # for each datapoint
        minScore=1000000000
        for center in Centers: # for each center
            Score=0
            for j in range (M): # for each point in Datapoint
                Score =((center[j]-DataRow[j])**2) + Score # distance score  (XA-XB)^2 + (YA-YB)^2= C^2

            if Score < minScore: # store minscore
                minScore=Score

        sumMinScore=sumMinScore + minScore # sum up minscore from each round


    print sumMinScore/len(Datapoints) 



def main(argv):
    Centers=[]
    Datapoints=[]
    with open(argv[1], "r") as fstream:
        K=int(fstream.readline())    #K- Centers
        M=int(fstream.readline())    #M- M dimensional space-

        for i in range(K):
            line=fstream.readline()
            linstrip=line.rstrip()
            Center_splitLine=linstrip.split(' ')
            Center_splitLineInt=map(float,Center_splitLine)  # convert to float
            Centers.append(Center_splitLineInt)
        junk=fstream.readline()

        for line in fstream:
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Datapoints.append(splitLineInt)

    print Centers

    DatapointsNP = numpy.array(Datapoints,dtype=numpy.float)
    print DatapointsNP



    Distortion(Centers,Datapoints,K,M)




if __name__== "__main__":
    main(argv)
