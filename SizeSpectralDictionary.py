__author__ = 'jcovino'
from sys import  argv
import sys
from collections import defaultdict
from utils_15 import Graph
import numpy as np

"""
Given: A spectral vector Spectrum', an integer threshold, and an integer max_score.
     Return: The size of the dictionary Dictionarythreshold(Spectrum').

Note: Use the provided max_score for the height of your table. Your answer should be the number of peptides whose score is
at least Threshold and at most max_score.

Extra Dataset

Sample Input:
4 -3 -2 3 3 -4 5 -3 -1 -1 3 4 1 3
1  # threshold
8  # max score
Sample Output:
3
"""

def SizeScore(AA_Mass,vector,threhold,maxScore):
    print " threshold", threhold
    print  "maxscore", maxScore
    # for i = 1, ..., m:
    #  for t = 0, ..., maxScore:
    #       total = 0
    #       for a in aminoAcids:
    #            if i - mass(a) >= 0    and t - specVector[i] <= maxScore   and t - specVector[i] >= 0:
    #                 total = total + size[t - specVector[i], i - mass(a)]
    #        size[t,i] = total


    #if i = t = 0 -> Size(i,t) = 1
    #else if i <= 0 -> Size(i,t) = 0
    #else Size(i,t) = sum(Size(i-aw, score-spec[i]) for aw in AW)
    #if spec[i] is negative, then score-spec[i] may exceed max score.

    Scores = [[0 for i in range(len(vector))] for j in range(maxScore+1)]  # create 2 d array
    Scores[0][0]=1

    for i in range (1, len(vector)):
        for t in range (0, maxScore):
            total=0
            for amino in AA_Mass:
                if  i-(AA_Mass[amino]) >= 0:
                    if t-vector[i] <= maxScore:
                        if t-vector[i] >=0:
                            total=total + Scores[t-vector[i]][i-(AA_Mass[amino])]
                Scores[t][i]=total

    scorelist=[]
    for i in range (maxScore):
            score= Scores[i][-1]
            scorelist.append(score)


    print scorelist
    slicedlist= scorelist[threhold:]
    print slicedlist
    print sum(slicedlist)


    #size[0,m] I get 61 and for size[37,m] I get 47.
    #print Scores[0][490]
    #print Scores[37][490]
    

def main(argv):
    Mass_AA={}
    AA_Mass={}

    with open(argv[1], "r") as massTable:
        for line in massTable:
            line=line.rstrip()
            tokens=line.split(" ")
            AAsymbol=tokens[0]
            mass=int(tokens[1])
            Mass_AA[mass]=AAsymbol
            AA_Mass[AAsymbol]=mass

    with open(argv[2], "r") as VectorInput:
        vector=VectorInput.readline().rstrip()
        threshold=int(VectorInput.readline().rstrip())
        maxScore=int(VectorInput.readline().rstrip())
        # add zero to vector input--you do it

    vectorList=vector.split(" ")
    vectorList=map(int,vectorList)

    SizeScore(AA_Mass,vectorList,threshold,maxScore)







if __name__== "__main__":
    main(argv)
