__author__ = 'jcovino'
from sys import  argv
import numpy as np
from collections import defaultdict
import math

"""
Say we have the following Data and HiddenMatrix:

Data: (2,6), (4,9), (5,7), (6,5), (8,3)

HiddenMatrix:
0.6 0.1 0.8 0.5 0.7
0.4 0.9 0.2 0.5 0.3

Compute the weighted center of gravity corresponding to the second row
of HiddenMatrix. Enter the coordinates of the weighted center of gravity as a
pair space-separated numbers rounded to three decimal places.
"""
#####################################

def EuclideanDistance(center,datapoint,M):
    Score=0
    for j in range (M):
        Score =((center[j]-datapoint[j])**2)+ Score    # distance score  (XA-XB)^2 + (YA-YB)^2= C^2
    return math.sqrt(Score)

def Weighted(HiddenMatrix,Distances,M,K):  #main function calls others, generates soft clusters from Centers/ generates hidden matrix

      centersList=[]
      for L in range (K): # for each center/ or row of Hidden Data
        divisor=sum(HiddenMatrix[L])
        newCenters=[]
        for i in range(M):  # for each x,y,z dimension of data
            dotproduct=0
            z=0
            for data in Distances: # for each data point
                dotproduct=dotproduct+(data[i] * HiddenMatrix[L][z])
                z=z+1
            newCenters.append(dotproduct/divisor)
        centersList.append(newCenters)
        print "row ", L, centersList[-1]

      print centersList

      return centersList


def main(argv):
    print
    Distances=[]
    HiddenMatrix=[]
    with open(argv[1], "r") as fstream:
        K=int(fstream.readline())    #K- Centers
        M=int(fstream.readline())    #M- M dimensional space-
        for i in range(5):
            line=fstream.readline()
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Distances.append(splitLineInt)
        print Distances

        for line in fstream:
             stripLine=line.rstrip()
             splitLine=stripLine.split(' ')
             splitLineInt=map(float,splitLine)  # convert to float
             HiddenMatrix.append(splitLineInt)

        print HiddenMatrix

    Weighted(HiddenMatrix,Distances,M,K)

if __name__== "__main__":
    main(argv)
