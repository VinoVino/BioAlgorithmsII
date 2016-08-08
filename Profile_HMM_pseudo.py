__author__ = 'jcovino'
from sys import  argv
import numpy as np
import math
import copy
from collections import defaultdict
import sys

"""
0.358 0.01
--------
A B C D E
--------
A-A
ADA
ACA
A-C
-EA
D-A
"""

def printFormat(ScoreSateMatrix,ScoreEmissionMatrix,columnNames,CharStates):
    print
    #print('%.3f' % val)
    print " ".join(columnNames)
    i=0
    for scorerow in ScoreEmissionMatrix:
        print columnNames[i],
        for element in scorerow:
            print ('%.3f' % element),
        i=i+1

        print
    print "--------"
    print " ".join(CharStates)
    j=0
    for scorerow in ScoreSateMatrix:
        print columnNames[j],
        for element in scorerow:
             print ('%.3f' % element),
        j=j+1
        print

def deleteColumns(theta,npalignment,CharStates):
    # function to determine if column from alignment should be deleted
    #  remove the columns from the original alignments that do not satisfy the theta threshold, meaning the column in is deleted if ratio >= theta, where
    #  ratio = #deletions / #alignments
    columnsTallyList=[]
    alignementcopy=copy.deepcopy(npalignment)

    tallyColumns=alignementcopy.transpose((1, 0))
    tallyColumns=np.ndarray.tolist(tallyColumns)
    columnLength=len(tallyColumns[0])*1.0

    columnScores=[]
    for row in tallyColumns:
        score=0
        for item in row:
            if "-" in item:
                score=score+1
        columnScores.append(score)
    ColumnstoDelete=[]
    for i in range (len(columnScores)):
        if (columnScores[i]/columnLength) >= theta:
            ColumnstoDelete.append(i)
    Cleaned_alignedment=[]  #  alignment with columns removed from original alignment
    for i in range (len(tallyColumns)):
        if i not in ColumnstoDelete:
            Cleaned_alignedment.append(tallyColumns[i])
    return Cleaned_alignedment, ColumnstoDelete



def Calc_Matrix(TransMatrixnp,npalignment,CharStates,Cleaned_alignment,ColumnstoDelete,columnNames,state_emissions,pscounts):
    # for each sequence:
    # for each character in the sequence:
    #     if the character is in a seed column
    #         if the character is a '-' the current state is D[column]
    #         otherwise the current state is M[column]
    #     if the character is not in a seed column
    #         if the character is a '-', skip this character
    #         otherwise the current state is I[column]
    #     add one to the tally of the transition from the previous state to the current state
    #     add one to the denominator of the previous state
    currentState=''
    totalPath=[]
    alignmentList=np.ndarray.tolist(npalignment)
    #print ColumnstoDelete
    for listrow in alignmentList:
        #print listrow
        column=1
        spot=0
        path=['S']
        for character in listrow:
            if spot not in ColumnstoDelete:        # if the character is in a seed column
                if character == '-':                 # if the character is a '-' the current state is D[column]
                    currentState ='D'+ str(column)
                    path.append(currentState)
                else:
                    currentState='M'+ str(column)        #otherwise the current state is M[column]
            if spot  in ColumnstoDelete:           #if the character is not in a seed column
                column=column-1
                if character =='-':                  #if the character is a '-', skip this character
                    currentState=''

                else:
                    currentState= 'I'+str(column)   #otherwise the current state is I[column]

            column=column+1
            spot=spot+1

            if  character != '-':
                state_emissions[currentState].append(character)
                path.append(currentState)

        path.append('E')
        totalPath.append(path)
    print state_emissions
    print
    print totalPath

    ScoreEmissionMatrix=scorePaths(totalPath,TransMatrixnp, columnNames,pscounts)
    ScoreStateMatrix=scoreStates(state_emissions,CharStates,columnNames,pscounts)

    #printFormat(ScoreStateMatrix,ScoreEmissionMatrix,columnNames,CharStates)

    pseudoCounts(ScoreEmissionMatrix,ScoreStateMatrix,pscounts,columnNames,CharStates)

def pseudoCounts(ScoreEmissionMatrix,ScoreStateMatrix,pscounts,columnNames,CharStates):

    print columnNames
    #print len(columnNames)
    IteraitonsofThree=2
    print "----", IteraitonsofThree
    # for row in ScoreEmissionMatrix:
    #     print row
    #add pseduo counts to first to rows
    for i in range (2):  #rows
        for j in range (1,4): # columns
            ScoreEmissionMatrix[i][j]=ScoreEmissionMatrix[i][j]+pscounts

    # add pseduo counts in groups of three rows starting at column 2

    rowspot=2
    columnspot=4
    for x in range (IteraitonsofThree):
        for i in range (rowspot,rowspot+3):
            for j in range (columnspot,columnspot+3):
                ScoreEmissionMatrix[i][j]=ScoreEmissionMatrix[i][j]+pscounts
        rowspot=rowspot+3
        columnspot=columnspot+3

    # add pseudo counts to last group of 3 rows, 2 columns

    for i in range (3): # for rows
        for j in range (2): # columns
            ScoreEmissionMatrix[i+rowspot][j+columnspot]=ScoreEmissionMatrix[i+rowspot][j+columnspot] + pscounts


    #normalize
    for i in range (len(ScoreEmissionMatrix)):
        sumrow=sum(ScoreEmissionMatrix[i])*1.0
        if sumrow >0:
            for j in range (len(ScoreEmissionMatrix[0])):
                ScoreEmissionMatrix[i][j]=float(ScoreEmissionMatrix[i][j]/sumrow)


    #apply pseduo counts to states
    startrow=1

    while startrow < len(columnNames)-1:
        currentspot= columnNames[startrow][0]
        if currentspot != 'D':
            for i in range (len(ScoreStateMatrix[0])):
                ScoreStateMatrix[startrow][i]=ScoreStateMatrix[startrow][i] + pscounts
        startrow=startrow+1

    # normalize
    for i in range (len(ScoreStateMatrix)):
        sumrow=sum(ScoreStateMatrix[i])*1.0
        if sumrow >0:
            for j in range (len(ScoreStateMatrix[0])):
                ScoreStateMatrix[i][j]=float(ScoreStateMatrix[i][j]/sumrow)


    printFormat(ScoreStateMatrix,ScoreEmissionMatrix,columnNames,CharStates)








def scorePaths(totalPath,TransMatrixnp,columnNames,pscounts):  # calculate scores for emissions
    #norm_Transmatrix=copy.deepcopy(TransMatrixnp)
    norm_TransmatrixList=np.ndarray.tolist(TransMatrixnp)
    for path in totalPath:
        for i in range(len(path)-1):
            Xstart=columnNames.index(path[i])
            Ystop=columnNames.index(path[i+1])
            TransMatrixnp[Xstart][Ystop]=TransMatrixnp[Xstart][Ystop]+1
    #normalize to sum of row
    for i in range (len(TransMatrixnp)):
        sumrow=sum(TransMatrixnp[i])*1.0
        if sumrow >0:
            for j in range (len(TransMatrixnp[0])):
                norm_TransmatrixList[i][j]=float(TransMatrixnp[i][j]/sumrow)
    # print norm_TransmatrixList
    return norm_TransmatrixList

def scoreStates(state_emissions,CharSates,columnNames,pscounts ):
    StateMatrix = [[0 for j in range(len(CharSates))] for i in range(len(columnNames))]  # 2D list-zero out the list  # this is the score list
    for keyrow in state_emissions:
        rowIndex=columnNames.index(keyrow)
        valueColumns=state_emissions[keyrow]
        for char in valueColumns:
            columnIndex=CharSates.index(char)
            StateMatrix[rowIndex][columnIndex]=StateMatrix[rowIndex][columnIndex]+1

    for i in range (len(StateMatrix)):
        sumrow=sum(StateMatrix[i])*1.0
        if sumrow >0:
            for j in range (len(StateMatrix[0])):
                StateMatrix[i][j]=float(StateMatrix[i][j]/sumrow)

    return StateMatrix

def main(argv):

    CharStatesDouble=[]

    with open(argv[1], "r") as fstream:
        theta=float(fstream.readline())
        pscounts=float(fstream.readline())
        CharStatesRead=fstream.readline()
        CharStatesStrip=CharStatesRead.rstrip()
        CharStatesDouble.append(CharStatesStrip.split(' '))
        Alignment=fstream.readlines()

    print "Theta ", theta
    print "pscounts ", pscounts

    CharStates=CharStatesDouble[0]

    alignmentList=[]
    for element in Alignment:
        alignmentList.append(element.rstrip())
    # put into list of lists with columns
    alignmentColumns=[]
    for element in alignmentList:
        temp=[]
        for subitem in element:
            temp.append(subitem)
        alignmentColumns.append(temp)

    npalignment=np.array(alignmentColumns)  ### this is the orginal alignment

    Cleaned_alignment, ColumnstoDelete=deleteColumns(theta,npalignment,CharStates)  # call to function to remove columns less than theta score

    numberColumnsLeft=len(Cleaned_alignment)
    TransMatrixSize= 2 + numberColumnsLeft*2 + numberColumnsLeft+1
    TransMatrix = [[0 for j in range(TransMatrixSize)] for i in range(TransMatrixSize)]  # 2D list-zero out the list  # this is the score list
    TransMatrixnp= np.array(TransMatrix)

    #########column names
    Start='S'
    Insert="I0"
    End='E'
    repeats=["M","D","I"]
    columnNames=[]
    columnNames.append(Start)
    columnNames.append(Insert)
    for i in range (numberColumnsLeft):
        for letter in repeats:
            columnNames.append(letter + str(i+1))
    columnNames.append(End)
    ############

    print CharStates
    print columnNames

    state_emissions=defaultdict(list)
    Calc_Matrix(TransMatrixnp,npalignment,CharStates,Cleaned_alignment,ColumnstoDelete,columnNames,state_emissions,pscounts)




if __name__== "__main__":
    main(argv)
