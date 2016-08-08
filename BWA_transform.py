__author__ = 'jcovino'
from sys import argv
from random import randint
"""
Burrows-Wheeler Transform Construction Problem: Construct the Burrows-Wheeler transform of a string.
     Input: A string Text.
     Output: BWT(Text).

CODE CHALLENGE: Solve the Burrows-Wheeler Transform Construction Problem.

Note: Although it is possible to construct the Burrows-Wheeler transform in O(|Text|) time and space, we do not expect you to implement such a fast algorithm. In other words, it is perfectly fine to produce BWT(Text) by first producing the complete Burrows-Wheeler matrix M(Text).

Sample Input:
GCGTGCCTGGTCA$
Sample Output:
ACTGGCT$TGCGGC
"""

def BWA(pattern):
    newPattern=pattern[:]
    newPattern[0]=pattern[-1]
    newPattern[1]=pattern[0]

    for i in range (1,len(pattern)-1):
        newPattern[i+1]=pattern[i]

    return newPattern

def main(argv):

    with open(argv[1],"r") as fstream:
        for line in fstream:
            lineInput = line.rstrip()

    BWAlist=[]

    BWAlist.append(lineInput)
    pattern=list(lineInput)

    for i in range (1,len(pattern)):
        nextPattern = BWA(pattern)
        returnString = ''.join(nextPattern)
        BWAlist.append(returnString)
        pattern=nextPattern

    sortedBWAList=sorted(BWAlist)


    Answer=''
    for element in sortedBWAList:
        Answer=Answer+ element[-1]

    print Answer


    #BWA_Answer=''
    #for element in BWAlist:
     #   BWA_Answer=BWA_Answer+str(element[-1])
    #print  BWA_Answer

if __name__== "__main__":
    main(argv)