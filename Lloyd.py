__author__ = 'jcovino'
from sys import  argv
import numpy
from collections import defaultdict

"""
 Input: Integers k and m followed by a set of points Data in m-dimensional space.
     Output: A set Centers consisting of k points (centers) resulting from applying the
     Lloyd algorithm to Data and Centers, where the first k points from Data are selected
     as the first k centers.
Sample Input:
2 2
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
1.800 2.867
1.060 1.140

"""
#####################################
def NearestCenter(Centers,datapoint,M): # called in Center_Clusters funciton
                                        #After centers have been selected, assign each data point to the cluster corresponding to its nearest center; ties are broken arbitrarily.
    coordinate=''
    minScore=100000000000
    for center in Centers:
        Score=0
        for j in range (M):
            Score =((center[j]-datapoint[j])**2)+ Score    # distance score  (XA-XB)^2 + (YA-YB)^2= C^2
        if Score < minScore:
            minScore=Score
            coordinate=center
    #print "closest center", coordinate
    return coordinate  # return the closest center for datapoint

def Clusters_Centers(DatapointCenters):
                                        #assign each clusters center of gravity to be the new centers, return new centers
    newCenters=[]
    #print
    for clusters in DatapointCenters.values():
        print clusters
        currentCluster=[]
        for i in range(len(clusters[0])):
             gravitySum=0
             for element in clusters:    #calculate gravity
                 gravitySum=gravitySum+element[i]

             currentCluster.append(gravitySum/len(clusters))

        newCenters.append(currentCluster)
    print
    for element in newCenters:
        print element

    return newCenters


def Centers_Clusters(Centers,Distances,M):  #main function calls others
    for i in range (1000):
        #print "Centers ", Centers
        DatapointCenters=defaultdict(list)
        for datapoint in Distances:  # for each datapoint
            nearest=NearestCenter(Centers,datapoint,M)  #find the nearest center
            DatapointCenters[str(nearest)].append(datapoint)  #group in Dict, Center-> datapoints

        newCenters=Clusters_Centers(DatapointCenters)  #determine newcenter using gravity of datapoints
        Centers=newCenters


    return newCenters


def main(argv):
    print
    Distances=[]
    with open(argv[1], "r") as fstream:
        K=int(fstream.readline())    #K- Centers
        M=int(fstream.readline())    #M- M dimensional space-
        for line in fstream:
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            splitLineInt=map(float,splitLine)  # convert to float
            Distances.append(splitLineInt)

    Centers=[]
    for i in range (K):
        Centers.append(Distances[i])
    print "initial Centers ", Centers

    Answer=Centers_Clusters(Centers,Distances,M)

    #print Answer


if __name__== "__main__":
    main(argv)
