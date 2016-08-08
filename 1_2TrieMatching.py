__author__ = 'jcovino'

from sys import argv
import sys
from collections import defaultdict
"""
CODE CHALLENGE: Implement TRIEMATCHING to solve the Multiple Pattern Matching Problem.
     Input: A string Text and a collection of strings Patterns.
     Output: All starting positions in Text where a string from Patterns appears as a substring.
"""


def findKmerPositions(parent,kmers, kmerLength):
    print parent
    print kmers
    print kmerLength
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

def main(argv):
    kmers=[]
    parent=''
    with open(argv[1],"r") as fstream:
        parent=fstream.readline()

        for line in fstream:
            kmers.append(line.rstrip())


    kmerLength = len (kmers[0])

    findKmerPositions(parent,kmers,kmerLength)
    """
    trees = trie()
    for pattern in patterns:
        answer.append(trees.add_pattern(pattern))
    fileOut=open('Answer.txt','w')
    print "-"
    for line in answer:
            for element in line:
                print element
                fileOut.write(element)
                fileOut.write('\n')


    fileOut.close()
    """



if __name__== "__main__":
    main(argv)