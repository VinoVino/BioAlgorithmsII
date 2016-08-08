__author__ = 'jcovino'
from sys import argv
import re
import sys
"""
CODE CHALLENGE: Implement BWMATCHING.
     Input: A string BWT(Text), followed by a collection of Patterns.
     Output: A list of integers, where the i-th integer corresponds to the number of substring
     matches of the i-th member of Patterns in Text.

Extra Dataset

Sample Input:
TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC
CCT CAC GAG CAG ATC
Sample Output:
2 1 1 0 1
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

    return InverseBWAString


def BWAMatching(Rev_BWA,searchPatterns):  #finds the number of times a patterns are found in the original text (REV_BWA)
    numberofFind=[]
    for pattern in searchPatterns:
        numberofFind.append(len(re.findall(pattern,Rev_BWA)))

    return numberofFind

def main(argv):
    PatternInput=[]
    with open(argv[1],"r") as fstream:
            lineInput = fstream.readline()
            for line in fstream:
                PatternInput.append(line.rstrip())
    lineInput=lineInput.rstrip()


    ReversedBWA=RBWA(lineInput)  # reverse BWA into orginal text


    PatternsOneString=PatternInput[0]
    splitPatterns= PatternsOneString.split(" ")


    AnswerList=BWAMatching(ReversedBWA,splitPatterns)
    print
    for element in AnswerList:
       sys.stdout.write(str(element))
       sys.stdout.write(' ')

    print

if __name__== "__main__":
    main(argv)