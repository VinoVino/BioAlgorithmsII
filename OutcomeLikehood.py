__author__ = 'jcovino'
from sys import  argv
import numpy as np
import math
from collections import defaultdict
from decimal import Decimal
"""
CODE CHALLENGE: Solve the Outcome Likelihood Problem.
     Input: A string x, followed by the alphabet from which x was constructed,
     followed by the states States, transition matrix Transition, and emission matrix

Output: The probability Pr(x) that the HMM emits x.

Note: You may assume that transitions from the initial state occur with equal probability.
Extra Dataset

Sample Input:
xzyyzzyzyy
--------
x y z
--------
A B
--------
	A	B
A	0.303	0.697
B	0.831	0.169
--------
	x	y	z
A	0.533	0.065	0.402
B	0.342	0.334	0.324
Sample Output:
1.1005510319694847e-06

"""

def Gen_Score(ScoresNP,InitialString,States,Emission,CharStates):
    print "---", CharStates
    ScoreDict=defaultdict(list)  # stores State-> scores in list
    PrevScore={}

    # generate initial score for first spot using 0.5 as
    #forward(a0) = 0.5 * ax
    #forward(b0) = 0.5 * bx
    Initialspot=InitialString[0]

    EmissionList=[]  # cretes list of Ax, Bx ect.- number of possible Emissions:  states X current char
    for char in CharStates:
        EmissionList.append(char+Initialspot)

    initialStates= float (1.000000000000000000000000000000000000000000000/len(CharStates))
    print initialStates
    for item in EmissionList:
        Score=initialStates*Emission[item]
        ScoreDict[item[0]].append(Score)
        PrevScore[item[0]]=Score

    #print ScoreDict

    #print PrevScore
###################################### subsequent scoring after first position
    #print
    #forward(a1) = forward(a0) * aa * az + forward(b0) * ba * az = 0.089585901
                                #aa                      #ba
    #forward(b1) = forward(a0) * ab * bz + forward(b0) * bb * bz = 0.069546438
                                #ab                     #bb
    aList=['AA','BA']
    bList=['AB','BB']

    for i in range (1,len(InitialString)):  # for every other string position
        Spot= InitialString[i]
        #print Spot

        EmissionList=[]  # cretes list of Ax, Bx ect.- number of possible Emissions:  states X current char
        for char in CharStates:
            EmissionList.append(char+Spot)  # emision list (A,B,C)-->  AY, BY, CY

        ScoreA=(PrevScore['A']*States[aList[0]]*Emission[EmissionList[0]]) + (PrevScore['B']*States[aList[1]]*Emission[EmissionList[0]])
        ScoreB=(PrevScore['A']*States[bList[0]]*Emission[EmissionList[1]]) + (PrevScore['B']*States[bList[1]]*Emission[EmissionList[1]])

        ScoreDict['A'].append(ScoreA)
        ScoreDict['B'].append(ScoreB)
        PrevScore['A']=ScoreA
        PrevScore['B']=ScoreB

    #print ScoreDict

    FinalScore=PrevScore['A']+PrevScore['B']

    #print('%.100f' % FinalScore)
    print "%.10g" % FinalScore
    print FinalScore

def main(argv):

    Distances=[]
    CharStates=[]
    with open(argv[1], "r") as fstream:
       NumberStates=int(fstream.readline())

       for i in range (NumberStates):
           tempString=fstream.readline()
           CharStates.append(tempString.rstrip())


       InitialString=fstream.readline().rstrip()
       print InitialString

# 	A	B
# A	0.039	0.961
# B	0.445	0.555
# --------
# 	x	y	z
# A	0.9	0.05	0.05
# B	0.29	0.41	0.3

    States= {'AA':0.039, 'AB':0.961,
             'BA':0.445, 'BB':0.555}

    Emission = {'Ax': 0.9, 'Ay': 0.05, 'Az':0.05,
             'Bx':0.29, 'By':0.41, 'Bz': 0.3,
              }

    Scores = [[0 for j in range(len(InitialString))] for i in range(NumberStates)]  # 2D list-zero out the list  # this is the score list
    ScoresNP=np.array(Scores)

    ScoreDict=Gen_Score(ScoresNP,InitialString,States,Emission,CharStates)





if __name__== "__main__":
    main(argv)
