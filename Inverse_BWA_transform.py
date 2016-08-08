__author__ = 'jcovino'
from sys import argv
from random import randint
import re
"""
Inverse Burrows-Wheeler Transform Problem: Reconstruct a string from its Burrows-Wheeler transform.
     Input: A string Transform (with a single "$" symbol).
     Output: The string Text such that BWT(Text) = Transform.

CODE CHALLENGE: Solve the Inverse Burrows-Wheeler Transform Problem.
Sample Input:
TTCCTAACG$A
Sample Output:
TACATCACGT$
"""


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]



def RBWA(pattern):

    pattern=list(pattern)
    #print len(pattern)
    #add number to symbol
    for i in range (0,len(pattern)):
        if pattern[i]=='$':
            tempSymbol='$'
        else:
            number=i+10
            tempSymbol=pattern[i]+str(number)

        pattern[i]=tempSymbol
    #print pattern
    sortedPattern=pattern[:]
    sortedPattern.sort(key=natural_keys)

    #print sortedPattern

    PathDict={}

    for i in range (0,len(pattern)):
        patterspot=pattern[i]
        sortedpatternspot=sortedPattern[i]
        PathDict[patterspot]=sortedpatternspot

    #print PathDict

    InversedBWA=[]
    currentspot='$'
    for i in range (0,len(pattern)):
        InversedBWA.append(PathDict[currentspot])
        currentspot=PathDict[currentspot]
    #print InversedBWA

    InverseBWAString=''

    for i in range(0,len(pattern)):
        CharacterAtSpot=InversedBWA[i]
        CharacterAtSpotMinusNumber=CharacterAtSpot[:1]
        InverseBWAString=InverseBWAString +CharacterAtSpotMinusNumber

    print InverseBWAString

def main(argv):

    with open(argv[1],"r") as fstream:
        for line in fstream:
            lineInput = line.rstrip()


    RBWA(lineInput)


if __name__== "__main__":
    main(argv)