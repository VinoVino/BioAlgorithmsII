__author__ = 'jcovino'
from sys import argv
import re
import sys
from collections import defaultdict
"""
CODE CHALLENGE: Solve the Multiple Pattern Matching Problem.
     Input: A string Text followed by a collection of strings Patterns.
     Output: All starting positions in Text where a string from Patterns appears as a substring.

Extra Dataset

Sample Input:
AATCGGGTTCAATCGGGGT
ATCG
GGGT
Sample Output:
1 4 11 15
Time Limit: 5 mins
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

def findKmerPositions(parent,kmers, kmerLength):
    #print parent
    #print kmers
    #print kmerLength
    parent_kmers=defaultdict(list)
    print len(parent)

    i=0
    while i < len (parent)-kmerLength+1:
        tempkmer= parent[i:i+kmerLength]
        #print tempkmer
        parent_kmers[tempkmer].append(i)
        i=i+1
    #print parent_kmers

    positions_kmers=[]
    for kmer in kmers:
        if kmer in parent_kmers:
            positions_kmers.append(parent_kmers[kmer])

    #print positions_kmers
    answer=[]
    for element in positions_kmers:
        for item in element:
            answer.append(item)

    answer.sort()
    #print answer

    for item in answer:
        print item,

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




def main(argv):
    PatternInput=[]
    with open(argv[1],"r") as fstream:
            lineInput = fstream.readline()
            lineInput=lineInput+'$'
            for line in fstream:
                PatternInput.append(line.rstrip())
    lineInput=lineInput.rstrip()
    #ReversedBWA=RBWA(lineInput)  # reverse BWA into orginal text
    #print ReversedBWA

    PatternLength = len (PatternInput[0])

    findKmerPositions(lineInput,PatternInput,PatternLength)

if __name__== "__main__":
    main(argv)