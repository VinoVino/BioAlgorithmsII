__author__ = 'jcovino'
from sys import  argv
import sys
from collections import defaultdict
from utils_15 import Graph

"""
CODE CHALLENGE: Solve the Peptide Sequencing Problem.
     Given: A space-delimited spectral vector Spectrum'.
     Return: An amino acid string with maximum score against Spectrum'. For masses
     with more than one amino acid, any choice may be used.
Extra Dataset

Sample Input:
0 0 0 4 -2 -3 -1 -7 6 5 3 2 1 9 3 -8 0 3 1 2 1 8
Sample Output:
XZZXX
"""

def constructSequence(massarray,AAmasstable):
    Answerlist=[]
    Answerlist.append(AAmasstable[massarray[0]])
    for i in range (len(massarray)-1):
        difference=massarray[i+1]-massarray[i]
        Answerlist.append(AAmasstable[difference])
    print massarray
    print len(massarray)
    print "".join(Answerlist)


def constructSpectrumDAG(vector,masslist):
    #construct list as DAG(startnode, Tonode, weight)
    edges=[]
    for i in range (len(vector)):
        for mass in masslist:
            if i + mass < len(vector):
              sum=i+mass
              edges.append([i,sum,vector[sum]])
    return edges

def main(argv):
    Mass_AA={}
    AA_Mass={}

    with open(argv[1], "r") as massTable:
        for line in massTable:
            line=line.rstrip()
            tokens=line.split(" ")
            AAsymbol=tokens[0]
            mass=int(tokens[1])
            Mass_AA[mass]=AAsymbol
            AA_Mass[AAsymbol]=mass

    with open(argv[2], "r") as VectorInput:
        vector=(VectorInput.readline().rstrip())

    vectorList=vector.split(" ")
    vectorList=map(int,vectorList)

    Masslist=Mass_AA.keys()
    edges=constructSpectrumDAG(vectorList,Masslist)


    G = Graph(edges)

    G.calculate_path_information(0)
    path_nodes = G.backtrack_longest_path(0, len(vectorList)-1)

    # remove source
    path_nodes=path_nodes[1:]
    # replace sink
    print path_nodes


    path_nodes[-1]=len(vectorList)-1
    constructSequence(path_nodes,Mass_AA)


if __name__== "__main__":
    main(argv)
