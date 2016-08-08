__author__ = 'jcovino'
from sys import  argv
import sys
from collections import defaultdict

"""
CODE CHALLENGE: Solve the Converting a Peptide Vector into a Peptide Problem.
     Given: A space-delimited binary vector P
     Return: An amino acid string whose binary peptide vector matches P. For masses
     with more than one amino acid, any choice may be used.

Extra Dataset

Sample Input:
0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 1
Sample Output:
XZZXX
"""

def ConvertVector(vector,AAmasstable):
    massList=[]
    print len(vector)
    for i in range (len(vector)):
        if vector[i] == 1:
            massList.append(i+1)
    constructGraph(massList,AAmasstable)

def constructGraph(massarray,AAmasstable):
    print
    Answerlist=[]
    Answerlist.append(AAmasstable[massarray[0]])
    for i in range (len(massarray)):
        for j in range (len(massarray)):
            masssubtract=int(massarray[i]-massarray[j])
            if masssubtract in AAmasstable:
                Answerlist.append((AAmasstable[masssubtract]))
                break
    print massarray
    print "".join(Answerlist)

def main(argv):
    AAmasstable={}


    with open(argv[1], "r") as massTable:
        for line in massTable:
            line=line.rstrip()
            tokens=line.split(" ")
            AAsymbol=tokens[0]
            mass=int(tokens[1])
            AAmasstable[mass]=AAsymbol

    with open(argv[2], "r") as VectorInput:
        vector=(VectorInput.readline().rstrip())


    vectorList=vector.split(" ")
    vectorList=map(int,vectorList)

    ConvertVector(vectorList,AAmasstable)







if __name__== "__main__":
    main(argv)
