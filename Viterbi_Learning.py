__author__ = 'jcovino'
from sys import  argv
import numpy as np
import math
from collections import defaultdict

"""
CODE CHALLENGE: Implement Viterbi learning for estimating the parameters of an HMM.
Sample Input:
100
--------
zyzxzxxxzz
--------
x y z
--------
A B
--------
	A	B
A	0.599	0.401
B	0.294	0.706
--------
	x	y	z
A	0.424	0.367	0.209
B	0.262	0.449	0.289


Sample Output:
	A	B
A	0.5	0.5
B	0.0	1.0
--------
	x	y	z
A	0.333	0.333	0.333
B	0.4	0.1	0.5

"""

def Gen_Score(InitialString,States,Emission,CharStates):
    print "---", CharStates
    ScoreDict=defaultdict(list)  # stores State-> scores in list
    revScoreDict={} # stores score-> State from previous round
    # generate initial score for first spot using 0.5 as
    Initialspot=InitialString[0]

    EmissionList=[]  # cretes list of Ax, Bx ect.- number of possible Emissions:  states X current char
    for char in CharStates:
        EmissionList.append(char+Initialspot)
    PrevScore=[]  # list stores scores from previous iteration for sum

    for item in EmissionList:
        Score=0.5*Emission[item]
        PrevScore.append(math.log(Score,2))
        ScoreDict[item[0]].append(math.log(Score,2))
        revScoreDict[math.log(Score,2)]=item[0]

    # print ScoreDict
    #print "rev", revScoreDict
    # print PrevScore
###################################### subsequent scoring after first position
    for i in range (1,len(InitialString)):  # for every other string position
        Spot= InitialString[i]

        maxScore=max(PrevScore)  # find maxscore from prevscore to use dynamically
        PrevScore=[] # reset PrevScore
        maxState=revScoreDict[maxScore]

        StateList=[]
        for char in CharStates: # generate all states and store in StateList
            StateList.append(maxState+char)
        print Spot
        print "states ", StateList

        EmissionList=[] # generate all emissions
        for char in CharStates:
            EmissionList.append(char+Spot)
        print "Emission ", EmissionList

        # score time
        for i in range (len(EmissionList)):
            Score=States[StateList[i]] * Emission[EmissionList[i]]
            sumScore=math.log(Score,2) + maxScore
            PrevScore.append(sumScore)
            ScoreDict[EmissionList[i][0]].append(sumScore)
            revScoreDict[sumScore]=EmissionList[i][0]

    return ScoreDict

def main(argv):

    Distances=[]
    CharStates=[]
    with open(argv[1], "r") as fstream:
       NumberStates=int(fstream.readline())

       for i in range (NumberStates):
           tempString=fstream.readline()
           CharStates.append(tempString.rstrip())

       InitialString=fstream.readline().rstrip()



    States= {'AA':0.641, 'AB':0.359,
             'BA':0.729, 'BB':0.271}

    Emission = {'Ax': 0.117, 'Ay': 0.691, 'Az':0.192,
                'Bx':0.097,   'By':0.42, 'Bz': 0.483
              }

    Scores = [[0 for j in range(len(InitialString))] for i in range(NumberStates)]  # 2D list-zero out the list  # this is the score list


    ScoreDict=Gen_Score(InitialString,States,Emission,CharStates)





if __name__== "__main__":
    main(argv)
