__author__ = 'jcovino'
from sys import argv
import re
import collections
"""
Longest Repeat Problem: Find the longest repeat in a string.
     Input: A string Text.
     Output: A longest repeat in Text, i.e., a longest substring of Text that appears in Text more than once.

CODE CHALLENGE: Solve the Longest Repeat Problem. (Multiple solutions may exist, in which case you may return any one.)

Sample Input:
     ATATCGTTTTATCGTT

Sample Output:
     TATCGTT
     """

def findLongestRepeat(parent):
    print parent
    kmers=[]
    kmerLength=60
    while kmerLength < 120:
        i=0
        while i < len (parent)-kmerLength:
            tempkmer= parent[i:i+kmerLength]
            i=i+1
            kmers.append(tempkmer)
        kmerLength=kmerLength+1
    count=collections.Counter(kmers)
    print ""
    #print count

    tuple_list = sorted([(v,k) for k,v in dict(count).items()])
    tuple_list.reverse()
    answer= tuple_list[:1000]

    answerList=[]
    for item in answer:
        if item[0] ==2:
            print len(item[1]), item



def main(argv):


    with open(argv[1],"r") as fstream:
        parent=fstream.readline()

    findLongestRepeat(parent)



if __name__== "__main__":
    main(argv)