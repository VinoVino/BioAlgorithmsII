__author__ = 'jcovino'
from sys import  argv
from collections import defaultdict
from random import randint
import copy
import itertools

"""
CODE CHALLENGE: Solve the Limb Length Problem.
     Input: An integer n, followed by an integer j between 0 and n, followed by a space-separated
     additive distance matrix D (whose elements are integers).
     Output: The limb length of the leaf in Tree(D) corresponding to the j-th row of this distance
     matrix (use 0-based indexing).

Extra Dataset

Sample Input:
4
1
0	13	21	22
13	0	12	13
21	12	0	13
22	13	13	0
Sample Output:
2
"""

def limbLength(DistanceMatrix,jlimb,Matrix):
    # (DiJ + DjK - DiK)/2 = smallest value equals limb length
    #print DistanceMatrix
    #print jlimb
    comparisonMatrix=[]

    for i in range (Matrix):  # generate a comparison matrix
        for j in range (Matrix):
            tempList=[]
            tempList.append(i)
            tempList.append(j)
            comparisonMatrix.append(tempList)

    refinedComparisonMatrix=[]  # weed out number pairs that equal each other or have the same value as jlimb
    for numberPair in comparisonMatrix:
        if numberPair[0]!=numberPair[1]:
            if numberPair[0] != jlimb and numberPair[1]!=jlimb:
                refinedComparisonMatrix.append(numberPair)
    #print DistanceMatrix
    #print refinedComparisonMatrix

    jlimbDistances=[]
     # (DiJ + DjK - DiK)/2 = smallest value equals limb len
    for numberPair in refinedComparisonMatrix:
      iSpot=numberPair[0]
      kspot=numberPair[1]
      Dij=int(DistanceMatrix[iSpot][jlimb])
      Djk=int(DistanceMatrix[jlimb][kspot])
      Dik=int(DistanceMatrix[iSpot][kspot])


      Distances=(Dij+Djk-Dik)/2

      jlimbDistances.append(Distances)

    print min(jlimbDistances)




def main(argv):

    Distances=[]
    with open(argv[1], "r") as fstream:
        Matrix=int(fstream.readline())    ##matrix size
        jlimb=int(fstream.readline()) # find the limb length of this variable
        for line in fstream:
            stripLine=line.rstrip()
            splitLine=stripLine.split(' ')
            Distances.append(splitLine)

    limbLength(Distances,jlimb,Matrix)








  


if __name__== "__main__":
    main(argv)
