__author__ = 'jcovino'
from sys import  argv
import numpy as np
from collections import defaultdict
import math

"""
Given the following Data and Centers, compute HiddenMatrix1,3 (i.e., the responsibility of the first center for the third datapoint)
using the Newtonian inverse-square law. Give your answer to three decimal places.

Data: (2,8), (2,5), (6,9), (7,5), (5,2)
Centers: (3,5), (5,4)
"""
#####################################

def EuclideanDistance(center,datapoint,M):
    Score=0
    for j in range (M):
        Score =((center[j]-datapoint[j])**2)+ Score    # distance score  (XA-XB)^2 + (YA-YB)^2= C^2
    return Score

def Centers_SoftClusters(Centers,Distances,M):  #main function calls others, generates soft clusters from Centers/ generates hidden matrix
      HiddenMatrix = [[0 for j in range(len(Distances))] for i in range(len(Centers))]  # 2D list-zero out, this is the hidden matrix
      CenterDataResp=[[0 for j in range(len(Distances))] for i in range(len(Centers))]

    #Estep: After centers have been selected, assign each data point a responsibility value for each cluster, where higher values correspond to stronger cluster membership.
      for j in range (len(Distances)): # for each datapoint
          TotalResp=0
          for i in range (len(Centers)):  # for each center
              EucDistance=EuclideanDistance(Centers[i],Distances[j],M)
              Resp=1/EucDistance
              CenterDataResp[i][j]=Resp
              TotalResp=TotalResp +Resp

          for k in range (len(Centers)):
              HiddenMatrix[k][j]=CenterDataResp[k][j]/TotalResp
      HiddenNp=np.array(HiddenMatrix)
      print HiddenNp

def main(argv):
    print
    Distances=[]
    Centers=[]
    with open(argv[1], "r") as fstream:
        M=int(fstream.readline())    #M- M dimensional space-
        for i in range (2):
            line=fstream.readline()
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Centers.append(splitLineInt)



        for line in fstream:

            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Distances.append(splitLineInt)

    print Centers
    print Distances

    Centers_SoftClusters(Centers,Distances,M)




if __name__== "__main__":
    main(argv)
