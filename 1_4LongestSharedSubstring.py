__author__ = 'jcovino'
from sys import argv
import string
"""
Longest Shared Substring Problem: Find the longest substring shared by two strings.
     Input: Strings Text1 and Text2.
     Output: The longest substring that occurs in both Text1 and Text2.

CODE CHALLENGE: Solve the Longest Shared Substring Problem. (Multiple solutions may exist, in which case you may return any one.)

Sample Input:
     TCGGTAGATTGCGCCCACTC
     AGGGGCTCGCAGTGTAAGAA

Sample Output:
     AGA
     """

def longestSharedKmer(seq1,seq2):
    kmers=[]
    kmerLength=2

    print seq1

    while kmerLength <= (len(seq1)/2):
        i=0
        while i < len (seq1)-kmerLength+1:
            tempKmer=seq1[i:i+kmerLength]
            kmers.append(tempKmer)
            i=i+1
        kmerLength=kmerLength+1
    #print kmers

    maxLength=1
    for kmer in kmers:
        if seq2.find(kmer) >= 0:
            if len(kmer) > maxLength:
                maxLength=len(kmer)
                answer=kmer

    print answer

def main(argv):

    with open(argv[1],"r") as fstream:
        seq1=fstream.readline().rstrip()
        seq2=fstream.readline().rstrip()

    longestSharedKmer(seq1,seq2)

if __name__== "__main__":
    main(argv)

