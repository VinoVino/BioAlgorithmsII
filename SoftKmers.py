__author__ = 'jcovino'
from sys import  argv
import numpy as np
from collections import defaultdict
import math

"""
     Implement the expectation maximization algorithm for soft k-means clustering.
     Input: Integers k and m, followed by a stiffness parameter Beta, followed by a set of points
     Data in m-dimensional space.
     Output: A set Centers consisting of k points (centers) resulting from applying the
     expectation maximization algorithm for soft k-means clustering. Select the first k points
     from Data as the first centers for the algorithm and run the algorithm for 100 E-steps
     and 100 M-steps. Results should be accurate up to three decimal places.

Sample Input:
2 2
2.7
1.3 1.1
1.3 0.2
0.6 2.8
3.0 3.2
1.2 0.7
1.4 1.6
1.2 1.0
1.2 1.1
0.6 1.5
1.8 2.6
1.2 1.3
1.2 1.0
0.0 1.9

Sample Output:
1.662 2.623
1.075 1.148

"""
#####################################

def EuclideanDistance(center,datapoint,M):
    Score=0
    for j in range (M):
        Score =((center[j]-datapoint[j])**2)+ Score    # distance score  (XA-XB)^2 + (YA-YB)^2= C^2
    return math.sqrt(Score)

def Centers_SoftClusters(Centers,Distances,M,Beta,K):  #main function calls others, generates soft clusters from Centers/ generates hidden matrix
      HiddenMatrix = [[0 for j in range(len(Distances))] for i in range(len(Centers))]  # 2D list-zero out, this is the hidden matrix
      CenterDataResp=[[0 for j in range(len(Distances))] for i in range(len(Centers))]

    #Estep: After centers have been selected, assign each data point a responsibility value for each cluster, where higher values correspond to stronger cluster membership.
      for j in range (len(Distances)): # for each datapoint
          TotalResp=0
          for i in range (len(Centers)):  # for each center
              EucDistance=EuclideanDistance(Centers[i],Distances[j],M)
              Resp=math.exp(-1*Beta*EucDistance)
              CenterDataResp[i][j]=Resp
              TotalResp=TotalResp +Resp

          for k in range (len(Centers)):
              HiddenMatrix[k][j]=CenterDataResp[k][j]/TotalResp

    # M-Step, After data points have been assigned to soft clusters, compute new centers.
    #np.dot(hiddenmatrix[cluster_index,:], data[:,data_index])
    #                       x     y               x    y               x    y
    #new center1 = 0.854 * (1.3, 1.1) + 0.146 * (1.3, 0.2) + 0.831 * (0.6, 2.8) + ...
    #new center2 = 0.146 * (1.3, 1.1) + 0.854 * (1.3, 0.2) + 0.169 * (0.6, 2.8) + ...
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
      print
      print centersList

      return centersList


def main(argv):
    print
    Distances=[]
    with open(argv[1], "r") as fstream:
        K=int(fstream.readline())    #K- Centers
        M=int(fstream.readline())    #M- M dimensional space-
        Beta=float(fstream.readline())  #beta factor as float
        for line in fstream:
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Distances.append(splitLineInt)

    Centers=[]
    for i in range (K):
        Centers.append(Distances[i])

    for i in range (100):
        newCenter=Centers_SoftClusters(Centers,Distances,M,Beta,K)
        Centers=newCenter[:]



if __name__== "__main__":
    main(argv)
