__author__ = 'jcovino'
from sys import  argv
from collections import defaultdict
import collections
import numpy as np

"""
yzzzyxzxxx
x y z
BBABABABAB
A B C
Sample Output:
	A	B	C
A	0.0	1.0	0.0         # how many A's go to A, B and C
B	0.8	0.2	0.0         # how many B's go to A, B and C
C	0.333	0.333	0.333
--------
	x	y	z
A	0.25	0.25	0.5
B	0.5	0.167	0.333
C	0.333	0.333	0.333

"""

def define_stateMatrix(StateMatrix,StatesChar,States):
    print StatesChar
    print States
    charCounts=[]
    Transitions=defaultdict(list)
    number=1

    for i in range (len(States)-1):
        charCounts.append(States[i])
        spot=States[i]+States[i+1]
        Transitions[spot].append(number)


    CharCountsDict=collections.Counter(charCounts)

    combinationsStates=[['AA', 'AB', 'AC'],
                        ['BA', 'BB', 'BC'],
                        ['CA', 'CB', 'CC']]
    # calculate matrix scores
    for i in range (len(StatesChar)):
        for j in range (len(StatesChar)):
            Trans=combinationsStates[i][j]
            if Trans in Transitions:
                StateMatrix[i][j]= 1.0*len(Transitions[Trans])/CharCountsDict[Trans[0]]

    # if row is empty(all zeros) update scores
    for i in range (len (StatesChar)):
        sumrow=sum(StateMatrix[i])*1.0
        if sumrow == 0:
            # update the row
            for j in range (len(StatesChar)):
                StateMatrix[i][j]=1.0 * 1/len(StatesChar)
    print np.array(StateMatrix)
    print
    return StateMatrix

def define_EmissionMatrix(EmissionMatrix,StatesChar,States,EmissionsChar,Emissions):
    combinationsEmissions=[['Ax', 'Ay', 'Az'],
                           ['Bx', 'By', 'Bz'],
                           ['Cx', 'Cy', 'Cz']]
    charCounts=[]
    for i in range (len(States)):
        charCounts.append(States[i])
    CharCountsDict=collections.Counter(charCounts)


    Transitions=defaultdict(list)

    for i in range(len(States)):
        spot=States[i]+Emissions[i]
        Transitions[spot].append(1)

    print Transitions
    print CharCountsDict
    for i in range (len(StatesChar)):
        for j in range (len(StatesChar)):
            Trans=combinationsEmissions[i][j]
            if Trans in Transitions:
                EmissionMatrix[i][j]= 1.0*len(Transitions[Trans])/CharCountsDict[Trans[0]]

    for i in range (len (StatesChar)):
        sumrow=sum(EmissionMatrix[i])*1.0
        if sumrow == 0:
            # update the row
            for j in range (len(StatesChar)):
                EmissionMatrix[i][j]=1.0 * 1/len(StatesChar)

    return EmissionMatrix



def main(argv):

    Distances=[]
    with open(argv[1], "r") as fstream:
       Emissions=fstream.readline().rstrip()
       EmissionCharsInput=fstream.readline().rstrip()
       EmissionChar=EmissionCharsInput.split(' ')
       States=fstream.readline().rstrip()
       StatesCharInput=fstream.readline().rstrip()
       StatesChar=StatesCharInput.split(' ')




    EmissionMatrix = [[0 for j in range(len(EmissionChar))] for i in range(len(EmissionChar))]  # 2D list-zero out the list
    StateMatrix = [[0 for j in range(len(StatesChar))] for i in range(len(StatesChar))]  # 2D list-zero out the list

    updated_StateMatrix = define_stateMatrix(StateMatrix,StatesChar,States)

    updated_EmissionMatrix=define_EmissionMatrix(EmissionMatrix,StatesChar,States,EmissionChar,Emissions)



    print
    #print('%.3f' % val)
    for item in StatesChar:
        print "\t", item,
    print

    i=0
    for scorerow in updated_StateMatrix :
        print StatesChar[i],"\t",
        for element in scorerow:
            print ('%.3f' % element),"\t",
        print
        i=i+1


    print "--------"
    for item in EmissionChar:
        print "\t", item,
    print
    j=0
    for scorerow in updated_EmissionMatrix:
        print StatesChar[j], "\t",
        for element in scorerow:
              print ('%.3f' % element),"\t",
        j=j+1
        print



if __name__== "__main__":
    main(argv)
