__author__ = 'jcovino'
from sys import  argv
import numpy as np
import math
from collections import defaultdict
import decimal
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

def Gen_Score(InitialString,States,Emission,CharStates):
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

    print EmissionList
    initialStates=  float(1.0/len(CharStates))
    print "--->>>", initialStates
    for item in EmissionList:
        Score=initialStates*Emission[item]
        ScoreDict[item[0]].append(Score)
        PrevScore[item[0]]=Score

    print ScoreDict

    print PrevScore
###################################### subsequent scoring after first position
    print
    #forward(a1) = forward(a0) * aa * az + forward(b0) * ba * az  + forward(c0) * ca * az
                                #aa                      ba                       ca

    #forward(b1) = forward(a0) * ab * bz + forward(b0) * bb * bz  + forward(c0) * cb * bz
                                #ab                     bb                       cb

    #forward(c1) = forward(a0) * ac * cz  + forward(b0) * bc * cz + forward(c0) * cc * cz


    aList=['AA','BA','CA']
    bList=['AB','BB','CB']
    cList=['AC', 'BC','CC']

    for i in range (1,len(InitialString)):  # for every other string position
        Spot= InitialString[i]
        #print Spot

        EmissionList=[]  # cretes list of Ax, Bx ect.- number of possible Emissions:  states X current char
        for char in CharStates:
            EmissionList.append(char+Spot)  # emision list (A,B,C)-->  AY, BY, CY (0,1,2)

        ScoreA=(PrevScore['A']*States[aList[0]]*Emission[EmissionList[0]]) + (PrevScore['B']*States[aList[1]]*Emission[EmissionList[0]]) +            \
               (PrevScore['C']*States[aList[2]]*Emission[EmissionList[0]])


        ScoreB=(PrevScore['A']*States[bList[0]]*Emission[EmissionList[1]]) + (PrevScore['B']*States[bList[1]]*Emission[EmissionList[1]]) +  \
               (PrevScore['C']*States[bList[2]]*Emission[EmissionList[1]])

        ScoreC= (PrevScore['A']*States[cList[0]]*Emission[EmissionList[2]]) + (PrevScore['B']*States[cList[1]]*Emission[EmissionList[2]]) + \
                (PrevScore['C']*States[cList[2]]*Emission[EmissionList[2]])

        ScoreDict['A'].append(ScoreA)
        ScoreDict['B'].append(ScoreB)
        ScoreDict['C'].append(ScoreC)
        PrevScore['A']=ScoreA
        PrevScore['B']=ScoreB
        PrevScore['C']=ScoreC

    #print ScoreDict

    FinalScore=PrevScore['A']+PrevScore['B'] + PrevScore['C']

    #print "%.16e" % FinalScore
    #print('%.100f' % FinalScore)
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

# 	A	B	C
# A	0.384	0.461	0.155
# B	0.435	0.246	0.319
# C	0.185	0.462	0.353
# --------
# 	x	y	z
# A	0.481	0.241	0.278
# B	0.541	0.421	0.038
# C	0.483	0.349	0.168


    States= {'AA':0.384, 'AB':0.461, 'AC':0.155,
             'BA':0.435, 'BB':0.246, 'BC':0.319,
              'CA':0.185,  'CB':0.462,    'CC':0.353}

    Emission = {'Ax': 0.481, 'Ay': 0.241, 'Az':0.278,
             'Bx':0.541, 'By':0.421, 'Bz': 0.038,
             'Cx':0.483,  'Cy':0.349, 'Cz':0.168
              }



    ScoreDict=Gen_Score(InitialString,States,Emission,CharStates)





if __name__== "__main__":
    main(argv)
