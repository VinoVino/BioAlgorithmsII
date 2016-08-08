__author__ = 'jcovino'
from sys import  argv
import sys
from collections import defaultdict
from utils_15 import Graph

"""
CODE CHALLENGE: Solve the Peptide Identification Problem.
     Given: A space-delimited spectral vector Spectrum' and an amino acid string Proteome.
     Return: A substring of Proteome with maximum score against Spectrum'.

Extra Dataset

Sample Input:
0 0 0 4 -2 -3 -1 -7 6 5 3 2 1 9 3 -8 0 3 1 2 1 8
XZZXZXXXZXZZXZXXZ
Sample Output:
ZXZXX
"""

def generatekmers(lowLength,highLength,protein):
    peptidekmers=[]

    window=lowLength
    while window < highLength:
        for i in range(len(protein)-window):
            subpeptide=protein[i:i+window]
            peptidekmers.append(subpeptide)
        window=window+1

    return peptidekmers

def scorepeptides(peptidekmers,vectorList,AA_Mass):
    filter_peptidekmers=[]
    for peptide in peptidekmers:
        totalMass=0
        mass=0
        for aa in peptide:
            mass=AA_Mass[aa]
            totalMass=totalMass+mass
        if totalMass == len(vectorList):
            print totalMass
            filter_peptidekmers.append(peptide)

    print filter_peptidekmers

    maxScore=0
    Toppep=[]

    for peptide in filter_peptidekmers:
        score=0
        mass=0
        for aa in peptide:
            mass=AA_Mass[aa] + mass
            #if mass< len(vectorList):
            score=vectorList[mass-1] +score
        if score > maxScore:
            maxScore=score
            Toppep=[]
            Toppep.append(peptide)
        if score == maxScore:
            Toppep.append(peptide)

    return Toppep


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
        # add zero to vector input--you do it

    with open(argv[3],"r") as proteinInput:
        protein=(proteinInput.readline().rstrip())

    vectorList=vector.split(" ")
    vectorList=map(int,vectorList)
    Masslist=Mass_AA.keys()

    massofPeptide=len(vectorList)
    highLength= massofPeptide/57
    lowLength= massofPeptide/186


    peptidekmers=generatekmers(lowLength,highLength,protein)
    TopPep=scorepeptides(peptidekmers,vectorList,AA_Mass)
    print "---", TopPep

    print len(vectorList)
    mass=0
    for AA in TopPep[0]:
        mass=mass+ AA_Mass[AA]
    print mass

if __name__== "__main__":
    main(argv)
