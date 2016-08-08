__author__ = 'jcovino'
from sys import  argv
import numpy as np
import math
from collections import defaultdict

"""
 Input: A string x, followed by the alphabet from which x was constructed,
     followed by the states States, transition matrix Transition, and emission matrix
     Emission of an HMM

     Sample Input:
xyxzzxyxyy
--------
x y z
--------
A B
--------
	A	B
A	0.641	0.359
B	0.729	0.271
--------
	x	y	z
A	0.117	0.691	0.192
B	0.097	0.42	0.483
Sample Output:
AAABBAAAAA


"""

def Gen_Score(ScoresNP,InitialString,States,Emission,CharStates):
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

    print ScoreDict
    return ScoreDict

def main(argv):


    CharStates=[]
    with open(argv[1], "r") as fstream:
       NumberStates=int(fstream.readline())

       for i in range (NumberStates):
           tempString=fstream.readline()
           CharStates.append(tempString.rstrip())


       InitialString=fstream.readline().rstrip()
       print InitialString



    States= {'AA':0.641, 'AB':0.359,
             'BA':0.729, 'BB':0.271}

    Emission = {'Ax': 0.117, 'Ay': 0.691, 'Az':0.192,
             'Bx':0.097,   'By':0.42, 'Bz': 0.483
              }

    Scores = [[0 for j in range(len(InitialString))] for i in range(NumberStates)]  # 2D list-zero out the list  # this is the score list
    ScoresNP=np.array(Scores)

    ScoreDict=Gen_Score(ScoresNP,InitialString,States,Emission,CharStates)





if __name__== "__main__":
    main(argv)
