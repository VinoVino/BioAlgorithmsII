__author__ = 'jcovino'
from sys import argv
import string

"""
Shortest Non-Shared Substring Problem: Find the shortest substring of one string that does not appear in another string.
     Input: Strings Text1 and Text2.
     Output: The shortest substring of Text1 that does not appear in Text2.

CODE CHALLENGE: Solve the Shortest Non-Shared Substring Problem. (Multiple solutions may exist, in which case you may return any one.)

Sample Input:
     CCAAGCTGCTAGAGG
     CATGCTGGGCTGGCT

Sample Output:
     AA
     """
def longestNonSharedKmer(seq1,seq2):
    kmers=[]
    kmerLength=2

    print seq1

    while kmerLength < 20:
        i=0
        while i < len (seq1)-kmerLength+1:
            tempKmer=seq1[i:i+kmerLength]
            kmers.append(tempKmer)
            i=i+1
        kmerLength=kmerLength+1
    print kmers

    minLength=25
    for kmer in kmers:
        if seq2.find(kmer) ==-1:
            if len(kmer) < minLength:
                minLength=len(kmer)
                answer=kmer

    print answer

def main(argv):

    with open(argv[1],"r") as fstream:
        seq1=fstream.readline().rstrip()
        seq2=fstream.readline().rstrip()

    longestNonSharedKmer(seq1,seq2)

if __name__== "__main__":
    main(argv)

